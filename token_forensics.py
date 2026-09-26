#!/usr/bin/env python3
"""
TOKEN FORENSICS — reconstruye un token de Pump.fun desde la cadena (RPC de Solana).

Dado un mint:
  1. descarga TODAS las transacciones que tocan el mint (getSignaturesForAddress + getTransaction),
     con caché en disco: se puede interrumpir y reanudar sin volver a descargar;
  2. reconstruye trades (compra/venta, SOL, tokens, wallet, slot) y balances de holders
     a partir de pre/postTokenBalances (incluye transferencias entre wallets);
  3. calcula las métricas del plan: holders por minuto, time-to-10/100 holders, compradores
     únicos, ratio compra/venta, top1/top10, compras en el mismo slot (bundles), snipers,
     y opcionalmente edad de wallets y vínculo con el creador;
  4. escribe tokens/trades/migrations en el esquema de phase0_audit.py + un config listo.

CONTROL NEGATIVO: si conoces la verdad del creador (no compró, no tiene otras wallets),
declárala con --declare-no-creator-buys / --own-wallets y el informe compara lo declarado
con lo que las métricas detectan. Un "sospechoso" en un token limpio = falso positivo del detector.

Uso:
  python token_forensics.py --mint <MINT> --rpc https://mainnet.helius-rpc.com/?api-key=XXX \\
         --out late_out --fee-mode holder_rewards --declare-no-creator-buys --wallet-age 150

Limitaciones (explícitas):
  * El importe en SOL de cada trade es el cambio de saldo del firmante (SOL + wSOL) menos la
    comisión de red, corregido por el alquiler de cuentas de token creadas/cerradas. Incluye
    comisiones de plataforma y propinas de prioridad: es una aproximación del precio, no el
    precio de la curva.
  * Un trade = transacción cuyo firmante cambia su saldo del token. Routers/agregadores que
    operan en nombre de otro wallet se atribuyen al firmante.
  * Cuentas "de sistema" (bonding curve, pool) = owners que NUNCA firman (PDAs) y reciben el supply
    al crear, reciben tokens en la migración o son contraparte de >=10 firmantes distintos.
    Se listan en el informe para verificarlas.
  * Trade = el firmante cambia su saldo del token Y la contraparte es una cuenta de sistema.
    Movimientos entre wallets sin curva/pool = transferencias (cuentan para holders, no como trades).
"""
from __future__ import annotations

import argparse
import json
import math
import os
import sys
import time
from collections import defaultdict
from datetime import datetime, timezone

import pandas as pd

# Versión máxima de transacción que aceptamos del RPC (Solana ya emite v1; con 0 el RPC rechaza la petición)
TX_VERSION = 1


WSOL = "So11111111111111111111111111111111111111112"
TOKEN_ACCOUNT_RENT = 2_039_280          # lamports; alquiler de una cuenta SPL de 165 bytes
LAMPORTS = 1e9
PUMP_SUPPLY = 1_000_000_000


# ======================================================================================
# RPC
# ======================================================================================
class RPC:
    def __init__(self, url: str, min_interval: float = 0.12, max_retries: int = 8, timeout: int = 30):
        import requests  # import perezoso: los tests usan un RPC falso
        self.s = requests.Session()
        self.url = url
        self.min_interval = min_interval
        self.max_retries = max_retries
        self.timeout = timeout
        self._last = 0.0
        self.calls = 0

    def call(self, method: str, params: list):
        body = {"jsonrpc": "2.0", "id": 1, "method": method, "params": params}
        delay = 0.5
        for attempt in range(self.max_retries):
            wait = self.min_interval - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.time()
            try:
                r = self.s.post(self.url, json=body, timeout=self.timeout)
                self.calls += 1
                if r.status_code == 429 or r.status_code >= 500:
                    raise IOError(f"HTTP {r.status_code}")
                j = r.json()
                if "error" in j:
                    msg = str(j["error"])
                    if any(x in msg.lower() for x in ("rate", "too many", "timeout", "unavailable")):
                        raise IOError(msg)
                    raise RuntimeError(f"RPC error en {method}: {msg}")
                return j["result"]
            except (IOError, ValueError) as e:
                if attempt == self.max_retries - 1:
                    raise RuntimeError(f"RPC {method} falló tras {self.max_retries} intentos: {e}")
                time.sleep(delay)
                delay = min(delay * 2, 20)
            except Exception as e:  # errores de red de requests
                if e.__class__.__module__.startswith("requests") and attempt < self.max_retries - 1:
                    time.sleep(delay)
                    delay = min(delay * 2, 20)
                    continue
                raise


def fetch_signatures(rpc, address: str, max_pages: int | None = None, log=True):
    """Todas las firmas de una dirección, de la más antigua a la más reciente."""
    out, before, pages = [], None, 0
    while True:
        params = {"limit": 1000}
        if before:
            params["before"] = before
        res = rpc.call("getSignaturesForAddress", [address, params])
        pages += 1
        if not res:
            break
        out.extend(res)
        before = res[-1]["signature"]
        if log:
            print(f"    firmas: {len(out):,}", file=sys.stderr, end="\r")
        if len(res) < 1000 or (max_pages and pages >= max_pages):
            break
    if log:
        print(file=sys.stderr)
    exhausted = not (max_pages and pages >= max_pages and len(res) == 1000)
    return list(reversed(out)), exhausted


class TxCache:
    """Caché JSONL append-only: sig -> transacción. Permite reanudar."""
    def __init__(self, path: str):
        self.path = path
        self.d = {}
        if os.path.exists(path):
            with open(path) as f:
                for line in f:
                    try:
                        o = json.loads(line)
                        self.d[o["sig"]] = o["tx"]
                    except (json.JSONDecodeError, KeyError):
                        continue  # línea truncada por una interrupción
        self.f = open(path, "a")

    def get(self, sig):
        return self.d.get(sig)

    def put(self, sig, tx):
        self.d[sig] = tx
        self.f.write(json.dumps({"sig": sig, "tx": tx}) + "\n")
        self.f.flush()


def fetch_transactions(rpc, sigs, cache: TxCache):
    todo = [s["signature"] for s in sigs if cache.get(s["signature"]) is None]
    for i, sig in enumerate(todo, 1):
        tx = rpc.call("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": TX_VERSION,
                                               "commitment": "confirmed"}])
        cache.put(sig, tx)
        if i % 25 == 0 or i == len(todo):
            print(f"    transacciones: {i:,}/{len(todo):,}", file=sys.stderr, end="\r")
    if todo:
        print(file=sys.stderr)


# ======================================================================================
# Parseo
# ======================================================================================
def _keys(tx):
    ks = tx["transaction"]["message"]["accountKeys"]
    return [k["pubkey"] if isinstance(k, dict) else k for k in ks]


def _amt(tb):
    ui = tb.get("uiTokenAmount", {})
    if ui.get("amount") is not None and ui.get("decimals") is not None:
        return int(ui["amount"]) / 10 ** int(ui["decimals"])
    return float(ui.get("uiAmount") or 0.0)


def parse_tx(sig: str, tx: dict, mint: str) -> dict | None:
    if tx is None:
        return None
    meta = tx.get("meta") or {}
    keys = _keys(tx)
    # claves cargadas desde lookup tables (si el RPC no las fusionó en accountKeys)
    la = meta.get("loadedAddresses") or {}
    if len(keys) < len(meta.get("preBalances", [])):
        keys = keys + la.get("writable", []) + la.get("readonly", [])
    signer = keys[0]
    fee = int(meta.get("fee", 0))
    pre_b, post_b = meta.get("preBalances", []), meta.get("postBalances", [])
    sol_delta = (post_b[0] - pre_b[0]) if pre_b and post_b else 0

    def by_acct(lst):
        return {tb["accountIndex"]: tb for tb in (lst or [])}
    pre_t, post_t = by_acct(meta.get("preTokenBalances")), by_acct(meta.get("postTokenBalances"))
    owner_delta = defaultdict(float)
    wsol_delta = 0
    rent_adj = 0
    for idx in set(pre_t) | set(post_t):
        a, b = pre_t.get(idx), post_t.get(idx)
        tb = b or a
        m, owner = tb.get("mint"), tb.get("owner")
        if m == mint:
            owner_delta[owner] += (_amt(b) if b else 0.0) - (_amt(a) if a else 0.0)
            if owner == signer:
                if a is None and b is not None:
                    rent_adj += TOKEN_ACCOUNT_RENT      # abrió cuenta: el alquiler no es precio
                elif a is not None and b is None:
                    rent_adj -= TOKEN_ACCOUNT_RENT      # cerró cuenta: recupera alquiler
        elif m == WSOL and owner == signer:
            wsol_delta += int((b or {}).get("uiTokenAmount", {}).get("amount") or 0) - \
                          int((a or {}).get("uiTokenAmount", {}).get("amount") or 0)
    logs = meta.get("logMessages") or []
    lj = " | ".join(logs)
    return {
        "signature": sig, "slot": tx.get("slot"), "block_time": tx.get("blockTime"),
        "err": meta.get("err") is not None, "signer": signer, "fee_lamports": fee,
        "signer_sol_delta": sol_delta, "signer_wsol_delta": wsol_delta, "rent_adj": rent_adj,
        "owner_delta": {k: v for k, v in owner_delta.items() if abs(v) > 0},
        "is_create_log": ("Instruction: Create" in lj) or ("Instruction: InitializeMint" in lj),
        "is_migrate_log": ("Instruction: Migrate" in lj) or ("Instruction: CreatePool" in lj),
        "keys": keys,
    }


def build(parsed: list[dict], mint: str, min_counterparties: int = 10, until_ts: int | None = None):
    """until_ts: reconstruye el estado tal como era en ese instante (point-in-time; para calibrar)."""
    ok = [p for p in parsed if p and not p["err"] and p["block_time"] is not None
          and (until_ts is None or p["block_time"] <= until_ts)]
    ok.sort(key=lambda p: (p["slot"], p["block_time"]))
    n_failed = sum(1 for p in parsed if p and p["err"])
    if not ok:
        raise SystemExit("No hay transacciones exitosas para este mint.")
    # creación: primera tx exitosa (con log de Create si existe)
    create = next((p for p in ok[:5] if p["is_create_log"]), ok[0])
    creator = create["signer"]
    create_slot, create_ts = create["slot"], create["block_time"]
    n = len(ok)
    # Cuentas de sistema (bonding curve, pool): NUNCA firman (PDAs de programa) y además
    #   (a) reciben el supply en la tx de creación (curva), o
    #   (b) reciben tokens en la tx de migración (pool; en Pump real ~20% del supply), o
    #   (c) son contraparte (delta de signo opuesto al firmante) de >= min_counterparties firmantes distintos.
    # Una ballena puede acumular mucho supply, pero firma sus compras. Un receptor de una
    # transferencia nunca firma, pero tiene una sola contraparte.
    signers = {p["signer"] for p in ok}
    cps = defaultdict(set)
    for p in ok:
        sd = p["owner_delta"].get(p["signer"], 0.0)
        if sd == 0:
            continue
        for o, d in p["owner_delta"].items():
            if o != p["signer"] and d * sd < 0:
                cps[o].add(p["signer"])
    mig = next((p for p in ok if p["is_migrate_log"]), None)
    seeded = {o for o, d in create["owner_delta"].items() if d > 0}
    mig_receivers = {o for o, d in mig["owner_delta"].items() if d > 0} if mig else set()
    candidates = seeded | mig_receivers | {o for o, s_ in cps.items() if len(s_) >= min_counterparties}
    system = {o for o in candidates if o not in signers}
    # trades y holders
    trades, holders_ts, transfers = [], [], 0
    bal = defaultdict(float)
    for p in ok:
        for o, d in p["owner_delta"].items():
            bal[o] += d
        sd = p["owner_delta"].get(p["signer"], 0.0)
        moved_non_system = [o for o in p["owner_delta"] if o not in system]
        counterparty_system = any(o in system for o in p["owner_delta"])
        if abs(sd) > 0 and p["signer"] not in system and counterparty_system:
            spent = -(p["signer_sol_delta"] + p["signer_wsol_delta"]) - p["fee_lamports"]
            spent -= p["rent_adj"]
            side = "buy" if sd > 0 else "sell"
            q = abs(spent) / LAMPORTS
            trades.append({
                "mint": mint, "signature": p["signature"], "slot": p["slot"], "block_time": p["block_time"],
                "wallet": p["signer"], "side": side, "sol_amount": q, "token_amount": abs(sd),
                "price_sol": q / abs(sd) if abs(sd) > 0 else None,
                "is_creator": p["signer"] == creator,
                "slot_offset": p["slot"] - create_slot,
                "sol_sign_consistent": (spent > 0) == (side == "buy") or q < 1e-6,
            })
        elif len(moved_non_system) >= 2 and not counterparty_system:
            transfers += 1
        h = sum(1 for o, b in bal.items() if o not in system and b > 1e-9)
        holders_ts.append({"block_time": p["block_time"], "slot": p["slot"], "holders": h})
    tr = pd.DataFrame(trades)
    hs = pd.DataFrame(holders_ts)
    final_bal = {o: b for o, b in bal.items() if o not in system and b > 1e-9}
    info = {"creator": creator, "create_slot": create_slot, "create_ts": create_ts,
            "create_signature": create["signature"], "system_accounts": sorted(system),
            "migration_signature": mig["signature"] if mig else None,
            "migration_ts": mig["block_time"] if mig else None,
            "n_tx_ok": n, "n_tx_failed": n_failed, "transfers_between_wallets": transfers}
    return tr, hs, final_bal, info


# ======================================================================================
# Métricas
# ======================================================================================
def metrics(tr: pd.DataFrame, hs: pd.DataFrame, final_bal: dict, info: dict, snipe_slots: int = 2):
    t0 = info["create_ts"]
    m = {}
    if len(tr) == 0:
        return {"note": "sin trades"}
    tr = tr.copy()
    tr["t_min"] = (tr["block_time"] - t0) / 60.0
    hs = hs.copy()
    hs["t_min"] = (hs["block_time"] - t0) / 60.0

    def first_time(k):
        r = hs[hs["holders"] >= k]
        return round(float(r["t_min"].iloc[0]), 3) if len(r) else None
    m["time_to_10_holders_min"] = first_time(10)
    m["time_to_100_holders_min"] = first_time(100)
    m["time_to_1000_holders_min"] = first_time(1000)
    for w in (1, 3, 5, 10, 15, 30, 60, 180, 1440):
        sub = hs[hs["t_min"] <= w]
        m[f"holders_at_{w}m"] = int(sub["holders"].iloc[-1]) if len(sub) else 0
    for w in (5, 30, 60, 180):
        m[f"holder_rate_per_min_first_{w}m"] = round(m[f"holders_at_{w}m"] / w, 4)
    buys, sells = tr[tr.side == "buy"], tr[tr.side == "sell"]
    for w in (30, 60, 180, None):
        b = buys if w is None else buys[buys.t_min <= w]
        s = sells if w is None else sells[sells.t_min <= w]
        tag = "all" if w is None else f"{w}m"
        m[f"unique_buyers_{tag}"] = int(b.wallet.nunique())
        m[f"unique_sellers_{tag}"] = int(s.wallet.nunique())
        m[f"buy_sell_count_ratio_{tag}"] = round(len(b) / len(s), 4) if len(s) else None
        m[f"buy_sell_sol_ratio_{tag}"] = round(b.sol_amount.sum() / s.sol_amount.sum(), 4) if len(s) and s.sol_amount.sum() else None
        m[f"sol_bought_{tag}"] = round(float(b.sol_amount.sum()), 6)
    tot = sum(final_bal.values())
    top = sorted(final_bal.values(), reverse=True)
    m["final_holders"] = len(final_bal)
    m["top1_share_final"] = round(top[0] / tot, 4) if tot else None
    m["top10_share_final"] = round(sum(top[:10]) / tot, 4) if tot else None
    if tot and len(top) > 1:
        x = sorted(top)
        n = len(x)
        m["gini_final"] = round(float(sum((2 * i - n - 1) * v for i, v in enumerate(x, 1)) / (n * sum(x))), 4)
    # snipers y bundles
    snip = buys[buys.slot_offset <= snipe_slots]
    m["sniper_buys_first_%d_slots" % snipe_slots] = int(len(snip))
    m["sniper_wallets"] = int(snip.wallet.nunique())
    m["sniper_sol"] = round(float(snip.sol_amount.sum()), 6)
    same = buys[buys.t_min <= 10].groupby("slot").wallet.nunique()
    m["slots_with_multiwallet_buys_first_10m"] = int((same >= 2).sum())
    m["max_wallets_buying_same_slot_first_10m"] = int(same.max()) if len(same) else 0
    m["buys_in_creation_slot_non_creator"] = int(((buys.slot_offset == 0) & ~buys.is_creator).sum())
    # creador
    c = tr[tr.is_creator]
    m["creator_trades"] = int(len(c))
    m["creator_buys"] = int((c.side == "buy").sum())
    m["creator_sells"] = int((c.side == "sell").sum())
    m["creator_sol_bought"] = round(float(c[c.side == "buy"].sol_amount.sum()), 6)
    # calidad del parseo
    m["parse_sol_sign_inconsistent_rate"] = round(float((~tr.sol_sign_consistent).mean()), 4)
    return m


def wallet_age_scan(rpc, wallets: list[str], first_buy_ts: dict, creator: str, max_pages: int, fresh_hours=24,
                    log=True):
    rows = []
    for i, w in enumerate(wallets, 1):
        sigs, exhausted = fetch_signatures(rpc, w, max_pages=max_pages, log=False)
        ok = [s for s in sigs if s.get("blockTime")]
        oldest = ok[0] if ok else None
        age_h = None
        linked = None
        funder = None
        if oldest and exhausted:
            age_h = (first_buy_ts[w] - oldest["blockTime"]) / 3600
            tx = rpc.call("getTransaction", [oldest["signature"], {"encoding": "jsonParsed",
                                                                  "maxSupportedTransactionVersion": TX_VERSION}])
            if tx:
                ks = _keys(tx)
                linked = creator in ks
                # una wallet sin SOL no puede firmar: su primera tx la firma quien la financia
                funder = ks[0] if ks[0] != w else None
        rows.append({"wallet": w, "history_exhausted": exhausted, "age_hours_at_first_buy": age_h,
                     "fresh": (age_h is not None and age_h < fresh_hours),
                     "first_tx_involves_creator": linked, "funder": funder})
        if log:
            print(f"    edad de wallets: {i}/{len(wallets)}", file=sys.stderr, end="\r")
    if log:
        print(file=sys.stderr)
    return pd.DataFrame(rows)


# ======================================================================================
# Informe
# ======================================================================================
def control_negative(m, info, wa, declared_no_buys, own_wallets):
    checks = []
    if declared_no_buys:
        ok = m.get("creator_trades", 0) == 0
        checks.append(("Creador sin trades (declarado)", ok,
                       f"detectados {m.get('creator_trades')} trades del creador"))
    own_seen = []
    if own_wallets:
        own_seen = [w for w in own_wallets if w in set(info.get("_trader_wallets", []))]
        checks.append(("Wallets propias declaradas sin actividad", not own_seen,
                       f"activas: {own_seen}" if own_seen else "ninguna activa"))
    flags = []
    if m.get("buys_in_creation_slot_non_creator", 0) > 0:
        flags.append(f"{m['buys_in_creation_slot_non_creator']} compras de terceros en el slot de creación (bundle/sniper)")
    if wa is not None and len(wa):
        linked = wa[wa.first_tx_involves_creator == True]  # noqa: E712
        if len(linked):
            flags.append(f"{len(linked)} wallets cuya primera tx involucra al creador")
    fp = [f for f in flags if "involucra al creador" in f]
    verdict = ("FALSO POSITIVO del detector: marca vínculo con el creador en un token declarado limpio"
               if (declared_no_buys and fp) else
               "Sin vínculos creador→compradores detectados" if declared_no_buys else "no declarado")
    return {"checks": [{"check": c, "pass": p, "detail": d} for c, p, d in checks],
            "detector_flags": flags, "verdict": verdict,
            "note": "Snipers/bundles de TERCEROS no son falsos positivos: son reales. El control negativo "
                    "solo prueba la parte 'creator-linked' del detector."}


def write_report(path, mint, info, m, cn, wa):
    L = [f"# Token forensics — `{mint}`", ""]
    L.append(f"- Creación: {datetime.fromtimestamp(info['create_ts'], timezone.utc):%Y-%m-%d %H:%M:%S} UTC · slot {info['create_slot']}")
    L.append(f"- Creador: `{info['creator']}`")
    L.append(f"- Tx exitosas: {info['n_tx_ok']:,} · fallidas: {info['n_tx_failed']:,} · transferencias entre wallets: {info['transfers_between_wallets']}")
    L.append(f"- Cuentas de sistema detectadas (curva/pool): {info['system_accounts']}")
    L.append(f"- Migración: {info['migration_signature'] or 'no detectada'}")
    L.append("\n## Primeros minutos\n")
    L.append("| | 1m | 3m | 5m | 10m | 15m | 30m | 60m | 180m | 24h |\n|---|---|---|---|---|---|---|---|---|---|")
    L.append("| holders | " + " | ".join(str(m.get(f"holders_at_{w}m")) for w in (1, 3, 5, 10, 15, 30, 60, 180, 1440)) + " |")
    L.append(f"\nTime to 10 / 100 / 1000 holders (min): {m.get('time_to_10_holders_min')} / "
             f"{m.get('time_to_100_holders_min')} / {m.get('time_to_1000_holders_min')}\n")
    L.append("## Flujo\n")
    for tag in ("30m", "60m", "180m", "all"):
        L.append(f"- {tag}: compradores {m.get('unique_buyers_'+tag)}, vendedores {m.get('unique_sellers_'+tag)}, "
                 f"ratio compras/ventas (nº) {m.get('buy_sell_count_ratio_'+tag)}, (SOL) {m.get('buy_sell_sol_ratio_'+tag)}")
    L.append("\n## Concentración (final, sin cuentas de sistema)\n")
    L.append(f"- holders {m.get('final_holders')} · top1 {m.get('top1_share_final')} · top10 {m.get('top10_share_final')} · Gini {m.get('gini_final')}")
    L.append("\n## Snipers / bundles\n")
    for k in [k for k in m if k.startswith(("sniper", "slots_with", "max_wallets", "buys_in_creation"))]:
        L.append(f"- {k}: {m[k]}")
    L.append("\n## Creador\n")
    for k in ("creator_trades", "creator_buys", "creator_sells", "creator_sol_bought"):
        L.append(f"- {k}: {m.get(k)}")
    if wa is not None and len(wa):
        f = wa[wa.history_exhausted]
        L.append("\n## Edad de wallets compradoras\n")
        L.append(f"- escaneadas {len(wa)} · historial completo {len(f)} · fresh (<24h) {int(f.fresh.sum())} "
                 f"({(f.fresh.mean() if len(f) else float('nan')):.1%} de las medibles) · "
                 f"primera tx con el creador: {int((wa.first_tx_involves_creator == True).sum())}")  # noqa: E712
    L.append("\n## Control negativo\n")
    L.append(f"**{cn['verdict']}**\n")
    for c in cn["checks"]:
        L.append(f"- {'✅' if c['pass'] else '❌'} {c['check']} — {c['detail']}")
    for f in cn["detector_flags"]:
        L.append(f"- ⚑ {f}")
    L.append(f"\n_{cn['note']}_")
    L.append(f"\nCalidad de parseo: tasa de signo SOL inconsistente = {m.get('parse_sol_sign_inconsistent_rate')}")
    with open(path, "w") as fh:
        fh.write("\n".join(L) + "\n")


# ======================================================================================
def run(rpc, mint, out, fee_mode=None, wallet_age=0, wallet_age_pages=3, declare_no_buys=False,
        own_wallets=None, sol_usd=None, snipe_slots=2):
    os.makedirs(out, exist_ok=True)
    print(f"[1/4] firmas del mint {mint}", file=sys.stderr)
    sigs, _ = fetch_signatures(rpc, mint)
    print(f"[2/4] transacciones ({len(sigs):,})", file=sys.stderr)
    cache = TxCache(os.path.join(out, "tx_cache.jsonl"))
    fetch_transactions(rpc, sigs, cache)
    parsed = [parse_tx(s["signature"], cache.get(s["signature"]), mint) for s in sigs]
    print("[3/4] reconstrucción y métricas", file=sys.stderr)
    tr, hs, final_bal, info = build(parsed, mint)
    info["_trader_wallets"] = tr.wallet.unique().tolist() if len(tr) else []
    m = metrics(tr, hs, final_bal, info, snipe_slots=snipe_slots)
    wa = None
    if wallet_age and len(tr):
        first = tr[tr.side == "buy"].groupby("wallet").block_time.min().sort_values()
        ws = [w for w in first.index if w != info["creator"]][:wallet_age]
        print(f"[+] edad de las primeras {len(ws)} wallets compradoras", file=sys.stderr)
        wa = wallet_age_scan(rpc, ws, first.to_dict(), info["creator"], wallet_age_pages)
        wa.to_csv(os.path.join(out, "wallet_age.csv"), index=False)
    cn = control_negative(m, info, wa, declare_no_buys, own_wallets or [])
    print("[4/4] escribiendo salidas", file=sys.stderr)
    tr.to_csv(os.path.join(out, "trades.csv"), index=False)
    hs.to_csv(os.path.join(out, "holders_timeseries.csv"), index=False)
    # esquema phase0_audit
    tr.assign(side=tr.side).to_parquet(os.path.join(out, "p0_trades.parquet"), index=False)
    pd.DataFrame([{"mint": mint, "created_at": pd.Timestamp(info["create_ts"], unit="s"), "creator": info["creator"],
                   "quote_asset": "SOL", "fee_mode": fee_mode}]).to_parquet(os.path.join(out, "p0_tokens.parquet"), index=False)
    if info["migration_ts"]:
        pd.DataFrame([{"mint": mint, "ts": pd.Timestamp(info["migration_ts"], unit="s")}]).to_parquet(
            os.path.join(out, "p0_migrations.parquet"), index=False)
    cfg = {"tables": {
        "tokens": {"path": os.path.abspath(os.path.join(out, "p0_tokens.parquet")),
                   "columns": {"mint": "mint", "created_at": "created_at", "creator": "creator",
                               "quote_asset": "quote_asset", "fee_mode": "fee_mode"}},
        "trades": {"path": os.path.abspath(os.path.join(out, "p0_trades.parquet")),
                   "columns": {"mint": "mint", "ts": "block_time", "signature": "signature", "wallet": "wallet",
                               "side": "side", "sol_amount": "sol_amount", "token_amount": "token_amount"}}},
        "timestamp_units": {"trades": "s"}}
    if info["migration_ts"]:
        cfg["tables"]["migrations"] = {"path": os.path.abspath(os.path.join(out, "p0_migrations.parquet")),
                                       "columns": {"mint": "mint", "ts": "ts"}}
    if sol_usd:
        cfg["sol_usd_constant"] = sol_usd
    with open(os.path.join(out, "p0_config.json"), "w") as fh:
        json.dump(cfg, fh, indent=2)
    info.pop("_trader_wallets", None)
    result = {"mint": mint, "info": info, "metrics": m, "control_negative": cn,
              "run_utc": datetime.now(timezone.utc).isoformat(), "rpc_calls": getattr(rpc, "calls", None)}
    with open(os.path.join(out, "metrics.json"), "w") as fh:
        json.dump(result, fh, indent=2, default=str)
    write_report(os.path.join(out, "report.md"), mint, info, m, cn, wa)
    return result


def main():
    ap = argparse.ArgumentParser(description="Reconstrucción on-chain de un token de Pump.fun")
    ap.add_argument("--mint", required=True)
    ap.add_argument("--rpc", default=os.environ.get("SOLANA_RPC", "https://api.mainnet-beta.solana.com"),
                    help="URL RPC (recomendado: uno con API key; el público limita mucho)")
    ap.add_argument("--out", default="forensics_out")
    ap.add_argument("--fee-mode", default=None, help="creator_fee | holder_rewards (lo que elegiste al crear)")
    ap.add_argument("--wallet-age", type=int, default=0, help="nº de primeras wallets compradoras a escanear")
    ap.add_argument("--wallet-age-pages", type=int, default=3, help="páginas de 1000 firmas por wallet (más = más lento)")
    ap.add_argument("--declare-no-creator-buys", action="store_true")
    ap.add_argument("--own-wallets", nargs="*", default=[], help="otras wallets tuyas (deberían no aparecer)")
    ap.add_argument("--sol-usd", type=float, default=None)
    ap.add_argument("--snipe-slots", type=int, default=2)
    ap.add_argument("--min-interval", type=float, default=0.12, help="segundos entre llamadas RPC")
    a = ap.parse_args()
    rpc = RPC(a.rpc, min_interval=a.min_interval)
    r = run(rpc, a.mint, a.out, a.fee_mode, a.wallet_age, a.wallet_age_pages, a.declare_no_creator_buys,
            a.own_wallets, a.sol_usd, a.snipe_slots)
    print(open(os.path.join(a.out, "report.md")).read())


if __name__ == "__main__":
    main()
