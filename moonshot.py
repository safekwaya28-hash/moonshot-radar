#!/usr/bin/env python3
"""
MOONSHOT RADAR — tu estrategia en un clic.

    Top trader (>= $1M de ganancia) compra un token
    que llegó a >= $500k de MC, cayó >= 70% y está PLANO
    -> te avisa si todavía puedes entrar cerca de su precio.

Uso (o doble clic en MOONSHOT.bat / MOONSHOT.command):
    python moonshot.py                      # radar -> abre el informe en el navegador
    python moonshot.py add-wallet <ADDR> [etiqueta]   # verifica su PnL y la añade a tu lista
    python moonshot.py wallets              # lista tus smart wallets
    python moonshot.py doctor               # comprueba RPC + fuente de precios
    python moonshot.py demo                 # informe de ejemplo con datos simulados (sin internet)

Fuentes: RPC de Solana (tu API key; nunca sale de tu ordenador) para ver qué compran las wallets
y si siguen dentro; GeckoTerminal (API pública, sin clave) para el historial de precio/MC.

Las reglas son TUS reglas, escritas en moonshot_config.json. Son PROVISIONALES hasta que
smart_money_study.py las valide con datos. El informe ordena qué mirar: no es una orden de compra.
"""
from __future__ import annotations

import csv
import html
import json
import math
import os
import sys
import time
import webbrowser
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pump_discovery as pdsc  # noqa: E402
import scam_filter as sf  # noqa: E402
import token_forensics as tf  # noqa: E402

# Versión máxima de transacción que aceptamos del RPC (Solana ya emite v1; con 0 el RPC rechaza la petición)
TX_VERSION = 1


VERSION = "moonshot-scan-v1.5"
CONFIG_FILE = HERE / "moonshot_config.json"
WALLETS_FILE = HERE / "smart_wallets.csv"
STATE_DIR = HERE / ".moonshot"
WSOL = tf.WSOL
TOKEN_PROGRAMS = [pdsc.TOKEN_PROGRAM, pdsc.TOKEN_2022]

DEFAULT_RULES = {
    # ---- tus reglas (provisionales hasta validarlas con smart_money_study.py)
    "peak_mc_min_usd": 500_000,      # el token tuvo un pico >= esto
    "drawdown_min": 0.70,            # y ahora está >= 70% por debajo del pico
    "flat_hours": 72,                # plano durante las últimas 72 h
    "flat_band": 0.25,               # "plano" = todos los cierres horarios dentro de ±25% de la mediana
    "min_flat_candles": 12,          # mínimo de velas horarias con trades en esa ventana
    "min_trader_buy_usd": 5_000,     # compra relevante del top trader
    "max_premium": 0.30,             # 🟢 si el precio actual está <= +30% sobre el precio del trader
    "watch_premium": 0.60,           # 🟡 entre +30% y +60%; por encima, llegas tarde
    "trader_sold_exit": 0.50,        # si el trader ya vendió >= 50% de lo que compró -> 🔴
    "lookback_hours": 48,            # compras de las últimas 48 h
    "min_hist_peak_vol_usd": 0,      # opcional: volumen 24 h máximo histórico mínimo (0 = desactivado)
    # ---- SCAN v1: criterios 6-11
    "mc_max_usd": 150_000,           # 6  MC actual <= $150k
    "retention_min": 0.60,           # 7  holders hoy / holders en el ATH >= 60%
    "retention_excellent": 0.80,     #    >= 80% excelente
    "liq_min_frac": 0.10,            # 8  liquidez >= 10% del MC
    "top10_max": 0.25,               # 10 top 10 <= 25% del supply (sin pools/curvas/lockers)
    "wallet_max": 0.05,              #    ninguna wallet > 5%
    "dev_pages": 2,                  # 11 páginas de historial de la cuenta de token del dev
    "max_fails_wait": 2,             # con 1-2 fallos que pueden cambiar -> ESPERAR; más -> DESCARTAR
    # ---- verificación de wallets (add-wallet)
    "wallet_min_pnl_usd": 1_000_000,
    "wallet_min_closed": 20,
    "wallet_min_tokens": 5,
    "wallet_max_top_share": 0.50,
    "wallet_pages": 3,               # páginas de 1000 tx a revisar al verificar una wallet
    "wallet_verify_per_run": 12,     # máximo de wallets nuevas verificadas por ejecución...
    "verify_minutes": 18,            # ...y como mucho estos minutos (el resto espera a la siguiente)
    "radar_minutes": 15,             # tiempo máximo descargando transacciones nuevas en cada radar
    # ---- coste
    "wallet_scan_pages": 1,          # páginas de 1000 firmas por wallet en cada radar (con caché, basta)
    "gecko_min_interval": 2.2,       # API pública: ~30 llamadas/min
}


# ======================================================================================
# Config, estado, wallets
# ======================================================================================
def load_config(interactive=True) -> dict:
    cfg = {"rpc_url": os.environ.get("SOLANA_RPC"), "sol_usd": None, "rules": dict(DEFAULT_RULES)}
    if CONFIG_FILE.exists():
        user = json.loads(CONFIG_FILE.read_text(encoding="utf-8"))
        cfg["rules"].update(user.get("rules", {}))
        cfg.update({k: v for k, v in user.items() if k != "rules" and v is not None})
    if os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"):
        interactive = False
        if not cfg.get("rpc_url"):
            raise SystemExit("Falta el secreto SOLANA_RPC en GitHub (Settings > Secrets and variables > Actions).")
    if not cfg.get("rpc_url") and interactive:
        print("\nPRIMERA VEZ · configuración\n")
        print("Necesito la URL de tu RPC de Solana (se guarda SOLO en tu ordenador, en moonshot_config.json).")
        print("Gratis en https://www.helius.dev  ->  copia algo como https://mainnet.helius-rpc.com/?api-key=XXXX\n")
        try:
            url = input("Pega aquí tu URL de RPC (o Enter para ver una DEMO sin internet): ").strip()
        except EOFError:
            url = ""
        if not url:
            return {**cfg, "demo": True}
        cfg["rpc_url"] = url
        save_config(cfg)
        print(f"Guardado en {CONFIG_FILE.name}.\n")
    return cfg


def save_config(cfg: dict):
    out = {"rpc_url": cfg.get("rpc_url"), "sol_usd": cfg.get("sol_usd"), "rules": cfg["rules"]}
    CONFIG_FILE.write_text(json.dumps(out, indent=2), encoding="utf-8")


def load_wallets(path=None) -> list[dict]:
    path = path or WALLETS_FILE                     # se resuelve al llamar (no al definir)
    if not Path(path).exists():
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh) if r.get("wallet", "").strip() and not r["wallet"].startswith("#")]


def save_wallets(rows: list[dict], path=None):
    path = path or WALLETS_FILE
    cols = ["wallet", "label", "verified_pnl_usd", "closed_positions", "distinct_tokens", "top_token_share",
            "window_days", "meets_criteria", "forced", "verified_at"]
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols)
        w.writeheader()
        for r in rows:
            w.writerow({c: r.get(c, "") for c in cols})


# ======================================================================================
# GeckoTerminal (historial de precio en USD)
# ======================================================================================
class Gecko:
    BASE = "https://api.geckoterminal.com/api/v2"

    def __init__(self, min_interval=2.2, retries=5):
        import requests
        self.s = requests.Session()
        self.s.headers["Accept"] = "application/json;version=20230302"
        self.min_interval, self.retries, self._last, self.calls = min_interval, retries, 0.0, 0

    def get(self, path, params=None):
        delay = 5.0
        for i in range(self.retries):
            wait = self.min_interval - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.time()
            r = self.s.get(self.BASE + path, params=params or {}, timeout=20)
            self.calls += 1
            if r.status_code == 404:
                return None
            if r.status_code == 429 or r.status_code >= 500:
                time.sleep(delay); delay *= 2
                continue
            r.raise_for_status()
            return r.json()
        raise RuntimeError(f"GeckoTerminal no responde ({path})")

    def top_pool_attrs(self, mint):
        j = self.get(f"/networks/solana/tokens/{mint}/pools", {"page": 1})
        pools = (j or {}).get("data") or []
        if not pools:
            return None
        pools.sort(key=lambda p: float(p["attributes"].get("reserve_in_usd") or 0), reverse=True)
        return pools[0]["attributes"]

    def top_pool(self, mint):
        a = self.top_pool_attrs(mint)
        return a["address"] if a else None

    def socials(self, mint):
        """Enlaces a X / Telegram / web del token (para el check de comunidad)."""
        a = ((self.get(f"/networks/solana/tokens/{mint}/info") or {}).get("data") or {}).get("attributes") or {}
        out = {}
        if a.get("twitter_handle"):
            out["x"] = f"https://x.com/{a['twitter_handle']}"
        if a.get("telegram_handle"):
            out["telegram"] = f"https://t.me/{a['telegram_handle']}"
        if a.get("websites"):
            out["web"] = a["websites"][0]
        return out

    def ohlcv_hour(self, pool, mint, limit=1000):
        j = self.get(f"/networks/solana/pools/{pool}/ohlcv/hour",
                     {"aggregate": 1, "limit": limit, "currency": "usd", "token": mint})
        rows = ((j or {}).get("data") or {}).get("attributes", {}).get("ohlcv_list") or []
        df = pd.DataFrame(rows, columns=["ts", "o", "h", "l", "c", "v"])
        if df.empty:
            return df
        df["ts"] = df.ts.astype("int64")
        return df.sort_values("ts").drop_duplicates("ts").reset_index(drop=True)


# ======================================================================================
# Wallets: qué compran y qué tienen (RPC)
# ======================================================================================
def recent_signatures(rpc, address, since_ts, max_pages):
    out, before = [], None
    for _ in range(max_pages):
        p = {"limit": 1000}
        if before:
            p["before"] = before
        res = rpc.call("getSignaturesForAddress", [address, p])
        if not res:
            break
        stop = False
        for s in res:
            if (s.get("blockTime") or 0) < since_ts:
                stop = True
                break
            if s.get("err") is None:
                out.append(s)
        if stop or len(res) < 1000:
            break
        before = res[-1]["signature"]
    return out


STABLES = {"EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v": "USDC", "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB": "USDT",
           "2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo": "PYUSD", "USD1ttGY1N17NEEHLmELoaybftRBUSErhqYiQzvEmuB": "USD1"}


def parse_wallet_trade(tx, wallet, sig, sol_usd=None):
    """Swap del propio wallet contra SOL o contra un stablecoin (USDC/USDT/...): compra o venta de un mint.
    Vale aunque firme otro (agregadores tipo DFlow/Jupiter que pagan la comisión por ti)."""
    if not tx or (tx.get("meta") or {}).get("err") is not None:
        return None
    meta = tx["meta"]
    keys = tf._keys(tx)
    if wallet not in keys:
        return None
    wi = keys.index(wallet)
    pre_b, post_b = meta.get("preBalances") or [], meta.get("postBalances") or []
    sol_delta = (post_b[wi] - pre_b[wi]) if wi < len(pre_b) and wi < len(post_b) else 0
    fee = int(meta.get("fee", 0)) if wi == 0 else 0
    pre = {tb["accountIndex"]: tb for tb in meta.get("preTokenBalances") or [] if tb.get("owner") == wallet}
    post = {tb["accountIndex"]: tb for tb in meta.get("postTokenBalances") or [] if tb.get("owner") == wallet}
    deltas, wsol, rent = {}, 0, 0
    for idx in set(pre) | set(post):
        a, b = pre.get(idx), post.get(idx)
        tb = b or a
        m = tb["mint"]
        if m == WSOL:
            wsol += int((b or {}).get("uiTokenAmount", {}).get("amount") or 0) - int((a or {}).get("uiTokenAmount", {}).get("amount") or 0)
            continue
        deltas[m] = deltas.get(m, 0.0) + (tf._amt(b) if b else 0.0) - (tf._amt(a) if a else 0.0)
        if a is None and b is not None:
            rent += tf.TOKEN_ACCOUNT_RENT
        elif a is not None and b is None:
            rent -= tf.TOKEN_ACCOUNT_RENT
    deltas = {m: d for m, d in deltas.items() if abs(d) > 0}
    stable = {m: d for m, d in deltas.items() if m in STABLES}
    others = {m: d for m, d in deltas.items() if m not in STABLES}
    if len(stable) == 1 and len(others) == 1:            # swap contra USDC/USDT: precio directo en USD
        (qm, qd), = stable.items()
        (mint, d), = others.items()
        if (d > 0) == (qd > 0):
            return None                                   # entran/salen los dos: no es un swap
        usd_amt = abs(qd)
        return {"sig": sig, "ts": tx.get("blockTime"), "wallet": wallet, "mint": mint,
                "side": "buy" if d > 0 else "sell", "tokens": abs(d), "usd": usd_amt, "quote": STABLES[qm],
                "sol": usd_amt / sol_usd if sol_usd else None}
    if len(deltas) != 1:
        return None
    (mint, d), = deltas.items()
    spent = -(sol_delta + wsol) - fee - rent          # >0 compra con SOL, <0 venta
    side = "buy" if d > 0 else "sell"
    if (side == "buy" and spent <= 0) or (side == "sell" and spent >= 0):
        return None                                   # transferencia/airdrop, no swap contra SOL
    return {"sig": sig, "ts": tx.get("blockTime"), "wallet": wallet, "mint": mint, "side": side,
            "tokens": abs(d), "sol": abs(spent) / 1e9}


class TxStore:
    def __init__(self, state_dir=None):
        d = Path(state_dir or STATE_DIR)
        d.mkdir(exist_ok=True)
        self.cache = tf.TxCache(str(d / "tx_cache.jsonl"))

    def prune(self, min_ts):
        """Reescribe la caché conservando solo transacciones con blockTime >= min_ts."""
        keep = {k: v for k, v in self.cache.d.items() if v and (v.get("blockTime") or 0) >= min_ts}
        self.cache.f.close()
        with open(self.cache.path, "w") as fh:
            for k, v in keep.items():
                fh.write(json.dumps({"sig": k, "tx": v}) + "\n")
        self.cache.d = keep
        self.cache.f = open(self.cache.path, "a")
        return len(keep)

    def get(self, rpc, sig):
        tx = self.cache.get(sig)
        if tx is None:
            tx = rpc.call("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": TX_VERSION}])
            self.cache.put(sig, tx)
        return tx


def token_moves(tx, wallet):
    """Mints (sin SOL/wSOL) cuyo saldo del wallet cambia en la tx: {mint: delta}."""
    if not tx or not tx.get("meta") or tx["meta"].get("err") is not None:
        return {}
    out = {}
    for key, sign in (("preTokenBalances", -1), ("postTokenBalances", 1)):
        for b in tx["meta"].get(key) or []:
            if b.get("owner") == wallet and b.get("mint") != WSOL:
                out[b["mint"]] = out.get(b["mint"], 0.0) + sign * tf._amt(b)
    return {m: d for m, d in out.items() if abs(d) > 1e-12}


def wallet_trades(rpc, store, wallet, since_ts, pages, sol_usd=None, deadline=None):
    """Compras/ventas del wallet desde since_ts. Con deadline: pasado ese instante solo usa lo ya descargado
    (lo pendiente se descarga en la siguiente ejecución; la caché conserva el progreso). Devuelve (trades, completo)."""
    out, complete = [], True
    for s in recent_signatures(rpc, wallet, since_ts, pages):
        tx = store.cache.get(s["signature"])
        if tx is None:
            if deadline and time.time() > deadline:
                complete = False
                continue
            tx = store.get(rpc, s["signature"])
        t = parse_wallet_trade(tx, wallet, s["signature"], sol_usd)
        if t:
            out.append(t)
    return sorted(out, key=lambda t: t["ts"]), complete


def token_balance(rpc, wallet, mint):
    res = rpc.call("getTokenAccountsByOwner", [wallet, {"mint": mint}, {"encoding": "jsonParsed"}])
    tot = 0.0
    for a in (res or {}).get("value", []):
        try:
            tot += float(a["account"]["data"]["parsed"]["info"]["tokenAmount"]["uiAmount"] or 0)
        except (KeyError, TypeError):
            continue
    return tot


# ======================================================================================
# Estado de la base (point-in-time)
# ======================================================================================
def flat_state(c: pd.DataFrame, t_end: int, hours: float, band: float, min_n: int):
    w = c[(c.ts > t_end - hours * 3600) & (c.ts <= t_end)]
    if len(w) < min_n:
        return {"flat": None, "n": len(w)}
    med = float(w.c.median())
    lo, hi = float(w.c.min()), float(w.c.max())
    flat = lo >= med * (1 - band) and hi <= med * (1 + band)
    return {"flat": flat, "n": len(w), "floor": lo, "ceiling": hi, "median": med}


def base_since(c: pd.DataFrame, t_end: int, band: float, ref_hours=24):
    """Desde cuándo el precio está continuamente dentro de ±band de la mediana de las últimas 24 h."""
    ref = c[(c.ts > t_end - ref_hours * 3600) & (c.ts <= t_end)]
    if ref.empty:
        return None
    med = float(ref.c.median())
    inside = (c.c >= med * (1 - band)) & (c.c <= med * (1 + band)) & (c.ts <= t_end)
    since = None
    for ts, ok in zip(c.ts[::-1], inside[::-1]):
        if ts > t_end:
            continue
        if not ok:
            break
        since = ts
    return since


# ======================================================================================
# Direcciones derivadas (PDA) — sin dependencias: bonding curve de Pump y cuenta de token del dev
# ======================================================================================
_P = 2 ** 255 - 19
_D = (-121665 * pow(121666, _P - 2, _P)) % _P
ATA_PROGRAM = "ATokenGPvbdGVxr1b2hvZbsiqW5xWH25efTNsLJA8knL"
SYSTEM_PROGRAM = "11111111111111111111111111111111"
INCINERATOR = "1nc1nerator11111111111111111111111111111111"


def _on_curve(b: bytes) -> bool:
    y = int.from_bytes(b, "little") & ((1 << 255) - 1)
    if y >= _P:
        return False
    u, v = (y * y - 1) % _P, (_D * y * y + 1) % _P
    x2 = u * pow(v, _P - 2, _P) % _P
    return x2 == 0 or pow(x2, (_P - 1) // 2, _P) == 1


def _pk(s: str) -> bytes:
    b = pdsc.b58decode(s)
    if len(b) > 32:
        raise ValueError(f"dirección inválida: {s}")
    return b.rjust(32, b"\0")


def find_pda(seeds: list, program: str) -> str:
    import hashlib
    for bump in range(255, -1, -1):
        h = hashlib.sha256(b"".join(seeds) + bytes([bump]) + _pk(program) + b"ProgramDerivedAddress").digest()
        if not _on_curve(h):
            return pdsc.b58encode(h)
    raise ValueError("sin PDA")


def ata_address(owner: str, mint: str, token_program: str) -> str:
    return find_pda([_pk(owner), _pk(token_program), _pk(mint)], ATA_PROGRAM)


def pump_curve_address(mint: str) -> str:
    return find_pda([b"bonding-curve", _pk(mint)], pdsc.PUMP_PROGRAM)


# ======================================================================================
# Datos on-chain de los criterios 7, 10 y 11
# ======================================================================================
def _rows(res):
    return res.get("value", []) if isinstance(res, dict) else (res or [])


def holders_now(rpc, mint, token_program):
    """Nº de cuentas de token con saldo > 0 (holders actuales)."""
    flt = [{"memcmp": {"offset": 0, "bytes": mint}}]
    if token_program == pdsc.TOKEN_PROGRAM:
        flt.insert(0, {"dataSize": 165})
    res = rpc.call("getProgramAccounts", [token_program, {"encoding": "base64", "filters": flt,
                                                          "dataSlice": {"offset": 64, "length": 8}}])
    import base64
    n = 0
    for a in _rows(res):
        try:
            raw = base64.b64decode(a["account"]["data"][0])
            if int.from_bytes(raw[:8], "little") > 0:
                n += 1
        except (KeyError, IndexError, TypeError, ValueError):
            continue
    return n


def distribution(rpc, mint, supply, exclude=()):
    """Top 10 y mayor wallet sobre el supply, excluyendo pools/curvas/lockers (dueño = cuenta de un programa)."""
    top = _rows(rpc.call("getTokenLargestAccounts", [mint]))
    if not top or not supply:
        return None
    taccs = [t["address"] for t in top]
    tinfo = pdsc.get_multiple(rpc, taccs, "jsonParsed")
    owner_of = {}
    for a in taccs:
        try:
            owner_of[a] = tinfo[a]["data"]["parsed"]["info"]["owner"]
        except (KeyError, TypeError):
            owner_of[a] = None
    owners = sorted({o for o in owner_of.values() if o})
    oinfo = pdsc.get_multiple(rpc, owners, "base64") if owners else {}
    excl = set(exclude) | {INCINERATOR}
    held, skipped = {}, 0
    for t in top:
        o = owner_of.get(t["address"])
        prog = (oinfo.get(o) or {}).get("owner") if o else None
        if o is None or o in excl or (prog and prog != SYSTEM_PROGRAM):
            skipped += 1
            continue
        amt = float(t.get("uiAmount") or 0) if t.get("uiAmount") is not None else \
            int(t.get("amount") or 0) / 10 ** int(t.get("decimals") or 0)
        held[o] = held.get(o, 0.0) + amt
    shares = sorted((v / supply for v in held.values()), reverse=True)
    holders = sorted(((o, v / supply) for o, v in held.items()), key=lambda x: -x[1])
    return {"top10": sum(shares[:10]), "max_wallet": shares[0] if shares else 0.0, "excluded_accounts": skipped,
            "holders": holders[:20]}


def pump_creator(rpc, mint):
    """Creador guardado en la bonding curve de Pump.fun (offset 49). None si no es de Pump o curva antigua."""
    import base64
    try:
        curve = pump_curve_address(mint)
    except ValueError:
        return None, None
    acct = pdsc.get_multiple(rpc, [curve], "base64").get(curve)
    try:
        data = base64.b64decode(acct["data"][0])
    except (KeyError, IndexError, TypeError, ValueError):
        return None, curve
    if len(data) < 81 or data[49:81] == b"\0" * 32:
        return None, curve
    return pdsc.b58encode(data[49:81]), curve


def dev_activity(rpc, store, creator, mint, token_program, pages):
    """Historial de la cuenta de token del dev en este mint: ¿vendió o sacó tokens?"""
    ata = ata_address(creator, mint, token_program)
    sigs = recent_signatures(rpc, ata, 0, pages)
    complete = len(sigs) < pages * 1000
    bought = sold = moved = 0.0
    for s in sigs:
        tx = store.get(rpc, s["signature"])
        t = parse_wallet_trade(tx, creator, s["signature"])
        if t and t["mint"] == mint:
            if t["side"] == "buy":
                bought += t["tokens"]
            else:
                sold += t["tokens"]
            continue
        if not tx or not tx.get("meta"):
            continue
        pre = sum(tf._amt(b) for b in tx["meta"].get("preTokenBalances") or [] if b.get("owner") == creator and b.get("mint") == mint)
        post = sum(tf._amt(b) for b in tx["meta"].get("postTokenBalances") or [] if b.get("owner") == creator and b.get("mint") == mint)
        if post < pre:
            moved += pre - post
    return {"creator": creator, "bought": bought, "sold": sold, "moved_out": moved, "complete": complete, "n_tx": len(sigs)}


# ======================================================================================
# Chequeos manuales (manual_checks.csv): holders en el ATH y comunidad
# ======================================================================================
MANUAL_FILE_NAME = "manual_checks.csv"


def load_manual(path=None) -> dict:
    path = Path(path or HERE / MANUAL_FILE_NAME)
    if not path.exists():
        return {}
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            m = (r.get("mint") or "").strip()
            if not m or m.startswith("#"):
                continue
            def num(k):
                try:
                    return int(float(str(r.get(k) or "").replace(".", "").replace(",", "").strip()))
                except ValueError:
                    return None
            com = str(r.get("comunidad") or "").strip().lower()
            out[m] = {"holders_ath": num("holders_ath"), "holders_now": num("holders_now"),
                      "comunidad": True if com in ("si", "sí", "yes", "1", "ok", "✅") else False if com in ("no", "0", "❌") else None}
    return out


# ======================================================================================
# SCAN — Smart Money + Flat Base v1 (12 criterios)
# ======================================================================================
CRITERIA = ["Top trader", "Compra trader", "Pico MC", "Drawdown", "Base plana", "MC actual", "Retención holders",
            "Liquidez", "Comunidad", "Distribución", "Dev", "Distancia a entrada"]
STRUCTURAL = {1, 3, 11}             # si fallan, la moneda no vale: DESCARTAR (el resto puede cambiar: ESPERAR)


def _f(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def evaluate(mint, buys, candles, supply, mi, holdings, T, R, wallet_meta=None, extra=None, manual=None):
    """Tarjeta con los 12 criterios, 'pasa X/12', lo que falta y DECISIÓN (COMPRAR / ESPERAR / DESCARTAR)."""
    wallet_meta, extra, manual = wallet_meta or {}, extra or {}, manual or {}
    card = {"mint": mint, "smart_wallets": sorted({b["label"] or b["wallet"][:6] for b in buys}),
            "n_smart": len({b["wallet"] for b in buys}), "reasons": [], "criteria": [], "pending": [], "fails": []}
    hard = sf.hard_checks(mi)
    if hard:
        card.update(label="NO", decision="DESCARTAR", reasons=["HARD: " + h for h in hard])
        return card
    if candles is None or candles.empty or not supply:
        card.update(label="NODATA", decision="SIN DATOS", reasons=["sin historial de precio (GeckoTerminal) o sin supply"])
        return card
    c = candles.copy()

    # --- trader de referencia: la primera compra de un trader que cumple el criterio 1 (si no hay, la primera)
    def qualifies(w):
        m = wallet_meta.get(w) or {}
        if str(m.get("forced", "")).lower() in ("true", "1", "si", "sí"):
            return True                                  # la verificaste tú a mano (",force")
        pnl, closes = _f(m.get("verified_pnl_usd")), _f(m.get("closed_positions"))
        return pnl is not None and closes is not None and pnl >= R["wallet_min_pnl_usd"] and closes >= R["wallet_min_closed"]
    ordered = sorted(buys, key=lambda b: b["ts"])
    first = next((b for b in ordered if qualifies(b["wallet"])), ordered[0])
    tw = first["wallet"]
    tb = first["ts"]
    pre = c[c.ts <= tb]
    if pre.empty:
        card.update(label="NODATA", decision="SIN DATOS", reasons=["no hay historial anterior a la compra del trader"])
        return card
    mine = [b for b in buys if b["wallet"] == tw]
    tok = sum(b["tokens"] for b in mine)
    entry_px = sum(b["usd"] for b in mine) / tok if tok else float(pre.c.iloc[-1])
    mc_buy = entry_px * supply
    mc_now = float(c.c.iloc[-1] * supply)
    i_ath = int(c.h.values.argmax())
    ath_mc, ath_ts = float(c.h.iloc[i_ath] * supply), int(c.ts.iloc[i_ath])
    dd_now = 1 - mc_now / ath_mc if ath_mc else None
    t_last = int(c.ts.iloc[-1])
    fn = flat_state(c, t_last, R["flat_hours"], R["flat_band"], R["min_flat_candles"])
    since = base_since(c, t_last, R["flat_band"])
    base_h = (T - since) / 3600 if since else None
    premium = mc_now / mc_buy - 1 if mc_buy else None
    hold = holdings.get(tw)
    held_frac = min(1.0, hold / tok) if (hold is not None and tok > 0) else None
    meta = wallet_meta.get(tw) or {}
    floor_mc = fn["floor"] * supply if fn.get("flat") else None
    card.update({
        "symbol": None, "mc_now": mc_now, "mc_at_trader_buy": mc_buy, "peak_mc": ath_mc, "ath_ts": ath_ts,
        "drawdown_now": dd_now, "premium": premium, "base_hours": base_h, "flat_now": fn,
        "trader": first["label"] or tw, "trader_wallet": tw, "trader_pnl_usd": _f(meta.get("verified_pnl_usd")),
        "trader_closes": _f(meta.get("closed_positions")), "trader_buy_ts": tb,
        "trader_buy_usd": sum(b["usd"] for b in mine), "trader_held_frac": held_frac, "floor_mc": floor_mc,
        "target_3x_mc": 3 * mc_now,
    })
    crit = []

    def add(i, status, value, why=""):
        crit.append({"n": i, "name": CRITERIA[i - 1], "status": status, "value": value, "why": why or value})

    # 1 top trader
    pnl, closes = card["trader_pnl_usd"], card["trader_closes"]
    if qualifies(tw) and str(meta.get("forced", "")).lower() in ("true", "1", "si", "sí"):
        add(1, "ok", "verificada a mano" + (f" · en la ventana: {usd(pnl)}, {closes:.0f} cierres" if pnl is not None else ""))
    elif pnl is None:
        add(1, "fail", "sin verificar", "trader sin verificar (añádelo por wallets_to_add.txt)")
    elif qualifies(tw):
        add(1, "ok", f"{usd(pnl)} · {closes:.0f} cierres")
    else:
        add(1, "fail", f"{usd(pnl)} · {closes:.0f} cierres",
            f"trader {usd(pnl)} / {closes:.0f} cierres (mín. {usd(R['wallet_min_pnl_usd'])} y {R['wallet_min_closed']})")
    # 2 compra
    bu = card["trader_buy_usd"]
    add(2, "ok" if bu >= R["min_trader_buy_usd"] else "fail", usd(bu))
    # 3 pico
    add(3, "ok" if ath_mc >= R["peak_mc_min_usd"] else "fail", usd(ath_mc),
        f"ATH {usd(ath_mc)} < {usd(R['peak_mc_min_usd'])}")
    # 4 drawdown
    add(4, "ok" if dd_now is not None and dd_now >= R["drawdown_min"] else "fail", f"{dd_now:.0%}",
        f"caída {dd_now:.0%} < {R['drawdown_min']:.0%}")
    # 5 base
    if fn["flat"] is None:
        add(5, "fail", "pocas velas", f"pocas velas para juzgar la base ({fn['n']} en {R['flat_hours']} h)")
    elif not fn["flat"]:
        add(5, "fail", "no plano", f"no está plano en las últimas {R['flat_hours']} h")
    elif base_h is None or base_h < R["flat_hours"]:
        add(5, "fail", dur(base_h), f"base {dur(base_h)} < {R['flat_hours']} h")
    else:
        add(5, "ok", dur(base_h))
    # 6 MC actual
    add(6, "ok" if mc_now <= R["mc_max_usd"] else "fail", usd(mc_now), f"MC {usd(mc_now)} > {usd(R['mc_max_usd'])}")
    # 7 retención = holders ahora / holders en el ATH
    man = manual.get(mint) or {}
    h_now = man.get("holders_now") or extra.get("holders_now")
    h_ath = man.get("holders_ath")
    ath_s = f"{datetime.fromtimestamp(ath_ts, timezone.utc):%d/%m %H:%M} UTC"
    card.update(holders_now=h_now, holders_ath=h_ath)
    if h_now and h_ath:
        ret = h_now / h_ath
        card["retention"] = ret
        tag = " (excelente)" if ret >= R["retention_excellent"] else ""
        add(7, "ok" if ret >= R["retention_min"] else "fail", f"{ret:.0%}{tag} ({h_now:,} / {h_ath:,} en ATH)",
            f"retención {ret:.0%}")
    elif h_now:
        add(7, "manual", f"{h_now:,} holders hoy; ATH {ath_s}",
            f"retención: holders en el ATH ({ath_s}) deben ser ≤ {int(h_now / R['retention_min']):,}")
    else:
        add(7, "manual", f"ATH {ath_s}", f"retención: mira holders hoy y el {ath_s} en GMGN (≥60%)")
    # 8 liquidez
    liq = extra.get("liquidity_usd")
    if liq is None:
        add(8, "manual", "—", "liquidez: no la pude leer")
    else:
        lf = liq / mc_now if mc_now else 0
        card["liquidity_frac"] = lf
        add(8, "ok" if lf >= R["liq_min_frac"] else "fail", f"{lf:.0%} MC ({usd(liq)})", f"liquidez {lf:.0%} del MC")
    # 9 comunidad (actividad en X/Telegram 7 días: se confirma a mano)
    soc = extra.get("socials") or {}
    card["socials"] = soc
    links = " · ".join(v for v in soc.values() if v) or "sin redes enlazadas"
    if man.get("comunidad") is True:
        add(9, "ok", links)
    elif man.get("comunidad") is False:
        add(9, "fail", links, "comunidad inactiva")
    else:
        add(9, "manual", links, "comunidad: ¿X/Telegram activos en 7 días?")
    # 10 distribución
    ds = extra.get("distribution")
    if ds is None:
        add(10, "manual", "—", "distribución: no la pude leer")
    else:
        card.update(top10=ds["top10"], max_wallet=ds["max_wallet"])
        okd = ds["top10"] <= R["top10_max"] and ds["max_wallet"] <= R["wallet_max"]
        add(10, "ok" if okd else "fail", f"{ds['top10']:.0%} · wallet máx {ds['max_wallet']:.1%}",
            f"Top10 {ds['top10']:.0%} / wallet máx {ds['max_wallet']:.1%}")
    # 11 dev
    dv = extra.get("dev")
    if not dv:
        add(11, "manual", "dev no identificado", "dev: no identificado (¿no es de Pump.fun?), míralo en GMGN")
    else:
        card["dev"] = dv["creator"]
        if dv["sold"] > 0:
            add(11, "fail", f"vendió {dv['sold']/supply:.1%} del supply", "el dev vendió")
        elif dv["moved_out"] > 0:
            add(11, "fail", f"sacó {dv['moved_out']/supply:.1%} del supply a otra wallet", "el dev movió tokens fuera")
        elif not dv["complete"]:
            add(11, "manual", "historial largo", "dev: historial demasiado largo, míralo en GMGN")
        else:
            add(11, "ok", "No" + (" (nunca compró)" if dv["bought"] == 0 else ""))
    # 12 distancia
    if premium is None:
        add(12, "manual", "—", "distancia: sin precio del trader")
    else:
        add(12, "ok" if premium <= R["max_premium"] else "fail", pct(premium),
            f"distancia {pct(premium)} (máx. {pct(R['max_premium'])})")

    card["criteria"] = crit
    fails = [x for x in crit if x["status"] == "fail"]
    pending = [x for x in crit if x["status"] == "manual"]
    passed = sum(x["status"] == "ok" for x in crit)
    card.update(passed=passed, fails=[x["why"] for x in fails], pending=[x["why"] for x in pending])
    kill = [x["why"] for x in fails if x["n"] in STRUCTURAL]
    if premium is not None and premium > R["watch_premium"]:
        kill.append(f"llegas tarde ({pct(premium)} sobre el trader)")
    if held_frac is not None and held_frac <= 1 - R["trader_sold_exit"]:
        kill.append(f"el trader ya vendió {1-held_frac:.0%}")
    if kill or len(fails) > R["max_fails_wait"]:
        dec = "DESCARTAR"
    elif fails:
        dec = "ESPERAR"
    else:
        dec = "COMPRAR"
    summary = "; ".join([f"pasa {passed}/12"] + card["fails"] + [k for k in kill if k not in card["fails"]])
    if pending:
        summary += " · confirma: " + "; ".join(x["why"] for x in pending)
    if held_frac is None:
        summary += " · no pude comprobar si el trader sigue dentro"
    card.update(decision=dec, label={"COMPRAR": "ENTRY", "ESPERAR": "WATCH", "DESCARTAR": "NO"}[dec],
                reasons=[summary])
    return card


LABELS = {"ENTRY": "🟢 ENTRY", "WATCH": "🟡 ESPERAR", "NO": "🔴 DESCARTAR", "NODATA": "⚫ SIN DATOS"}
ORDER = {"ENTRY": 0, "WATCH": 1, "NO": 2, "NODATA": 3}


def run_radar(rpc, gecko, cfg, T=None, sol_usd=None, wallets=None, log=True, state_dir=None,
              log_file="default", manual=None):
    R = {**DEFAULT_RULES, **cfg["rules"]}
    T = int(T or time.time())
    wallets = wallets if wallets is not None else load_wallets()
    if not wallets:
        return []
    manual = load_manual() if manual is None else manual
    wmeta = {w["wallet"]: w for w in wallets}
    store = TxStore(state_dir)
    since = T - R["lookback_hours"] * 3600

    def say(m):
        if log:
            print(scrub(m, cfg), file=sys.stderr, flush=True)
    say(f"[1/4] compras de {len(wallets)} smart wallets en las últimas {R['lookback_hours']} h")
    buys = []
    import random
    order = list(wallets)
    random.Random(T // 1800).shuffle(order)          # orden distinto en cada ejecución: nadie se queda siempre al final
    deadline = time.time() + 60 * float(R.get("radar_minutes", 15))
    partial = []
    for w in order:
        trades, complete = wallet_trades(rpc, store, w["wallet"], since, R["wallet_scan_pages"], sol_usd, deadline)
        if not complete:
            partial.append(w.get("label") or w["wallet"][:6])
        for t in trades:
            if t["side"] == "buy" and t["ts"] <= T:
                if t.get("usd") is None:
                    t["usd"] = t["sol"] * sol_usd
                t["label"] = w.get("label") or ""
                if t["usd"] >= R["min_trader_buy_usd"]:
                    buys.append(t)
    by_mint = {}
    for b in buys:
        by_mint.setdefault(b["mint"], []).append(b)
    say(f"[2/4] {len(buys)} compras relevantes en {len(by_mint)} tokens"
        + (f" · a medias (se completan en la próxima): {', '.join(partial)}" if partial else ""))
    if log_file:
        _write_scan_progress(len(wallets), partial)
    mints = list(by_mint)
    minfo = pdsc.get_multiple(rpc, mints, "jsonParsed") if mints else {}
    cards = []
    for i, m in enumerate(mints, 1):
        say(f"[3/4] {i}/{len(mints)} {m[:8]}… precio + 12 criterios")
        acct = minfo.get(m)
        mi = pdsc.mint_info(acct, pdsc.DEFAULTS)
        supply = None
        try:
            info = acct["data"]["parsed"]["info"]
            supply = int(info["supply"]) / 10 ** int(info["decimals"])
        except (KeyError, TypeError, ValueError):
            pass
        candles, pool, extra = None, None, {}
        try:
            pa = gecko.top_pool_attrs(m) if hasattr(gecko, "top_pool_attrs") else None
            pool = pa["address"] if pa else gecko.top_pool(m)
            if pa and pa.get("reserve_in_usd") is not None:
                extra["liquidity_usd"] = float(pa["reserve_in_usd"])
            if pool:
                candles = gecko.ohlcv_hour(pool, m)
            if hasattr(gecko, "socials"):
                extra["socials"] = gecko.socials(m)
        except (RuntimeError, KeyError, TypeError, ValueError) as e:
            say(f"    {e}")
        holdings = {}
        for w in {b["wallet"] for b in by_mint[m]}:
            try:
                holdings[w] = token_balance(rpc, w, m)
            except RuntimeError:
                holdings[w] = None
        prog = (acct or {}).get("owner") or pdsc.TOKEN_PROGRAM
        if candles is not None and not candles.empty and supply and not sf.hard_checks(mi):
            curve = None
            try:
                creator, curve = pump_creator(rpc, m)
                if creator:
                    extra["dev"] = dev_activity(rpc, store, creator, m, prog, R["dev_pages"])
            except (RuntimeError, ValueError) as e:
                say(f"    dev: {e}")
            try:
                extra["distribution"] = distribution(rpc, m, supply, exclude={x for x in (pool, curve) if x})
            except (RuntimeError, ValueError) as e:
                say(f"    distribución: {e}")
            if not (manual.get(m) or {}).get("holders_now"):
                try:
                    extra["holders_now"] = holders_now(rpc, m, prog)
                except (RuntimeError, ValueError) as e:
                    say(f"    holders: {e}")
        card = evaluate(m, by_mint[m], candles, supply, mi, holdings, T, R, wallet_meta=wmeta, extra=extra, manual=manual)
        card["name"], card["symbol"] = token_meta(acct)
        cards.append(card)
    say("[4/4] informe")
    store.prune(since - 24 * 3600)
    cards.sort(key=lambda c: (ORDER[c["label"]], -(c.get("passed") or 0), -c["n_smart"],
                              c.get("premium") if c.get("premium") is not None else 9))
    if log_file == "default":
        log_file = HERE / "radar_log.jsonl"
    if log_file:
        with open(log_file, "a", encoding="utf-8") as fh:   # registro para validar las reglas después
            for c in cards:
                fh.write(json.dumps({"T": T, "version": VERSION, "rules": R, **c}, default=str) + "\n")
    return cards


def _write_scan_progress(n, partial):
    try:
        d = HERE / "report"
        d.mkdir(exist_ok=True)
        (d / "scan_progress.txt").write_text(f"{n - len(partial)}/{n} wallets al día"
                                             + (f"; pendientes: {', '.join(partial)}" if partial else "") + "\n", encoding="utf-8")
    except OSError:
        pass


def token_meta(acct):
    try:
        for e in acct["data"]["parsed"]["info"].get("extensions", []) or []:
            if e.get("extension") == "tokenMetadata":
                st = e.get("state", {})
                return st.get("name"), st.get("symbol")
    except (KeyError, TypeError):
        pass
    return None, None


# ======================================================================================
# Informe
# ======================================================================================
def usd(x):
    if x is None or (isinstance(x, float) and math.isnan(x)):
        return "—"
    return f"${x/1e6:.2f}M" if x >= 1e6 else f"${x/1e3:.1f}k" if x >= 1e3 else f"${x:.0f}"


def dur(h):
    if h is None:
        return "—"
    return f"{h:.0f} h" if h < 48 else f"{h/24:.1f} días"


def pct(x):
    return "—" if x is None else f"{x:+.0%}"


def ago(ts, T):
    if not ts:
        return "—"
    h = (T - ts) / 3600
    return f"hace {h*60:.0f} min" if h < 1 else f"hace {h:.1f} h" if h < 48 else f"hace {h/24:.1f} d"


MARK = {"ok": "✅", "fail": "❌", "manual": "✋"}


def card_fields(c, T):
    """Campos de la tarjeta en el orden que pediste. Devuelve [(clave, valor)]."""
    crit = {x["n"]: x for x in c.get("criteria") or []}

    def v(n, text=None):
        x = crit.get(n)
        return f"{MARK[x['status']]} {text if text is not None else x['value']}" if x else (text or "—")
    tw = c.get("trader_wallet") or ""
    held = "" if c.get("trader_held_frac") is None else f" · sigue dentro {c['trader_held_frac']:.0%}"
    return [
        ("CA", c["mint"]),
        ("Smart trader", f"{c.get('trader')} ({tw[:4]}…{tw[-4:]})" + (f" +{c['n_smart']-1} smart" if c.get("n_smart", 1) > 1 else "")),
        ("PnL trader", v(1)),
        ("Compra trader", v(2, f"{usd(c.get('trader_buy_usd'))} {ago(c.get('trader_buy_ts'), T)} a MC {usd(c.get('mc_at_trader_buy'))}{held}")),
        ("MC actual", v(6)),
        ("ATH MC", v(3)),
        ("Drawdown", v(4)),
        ("Base", v(5)),
        ("Holder retention", v(7)),
        ("Liquidez", v(8)),
        ("Comunidad", v(9)),
        ("Top10", v(10)),
        ("Dev sold", v(11)),
        ("Distancia a entrada trader", v(12)),
    ]


def plan_line(c):
    if c["label"] not in ("ENTRY", "WATCH"):
        return None
    return (f"Gestión: stop si cierre diario < suelo {usd(c.get('floor_mc'))} · vende 1/3 a 3× (MC {usd(c.get('target_3x_mc'))}) · "
            f"resto mientras retención ≥60% y el trader siga dentro")


def text_report(cards, T):
    L = [f"SCAN · Smart Money + Flat Base v1 · {datetime.fromtimestamp(T, timezone.utc):%Y-%m-%d %H:%M} UTC",
         "  ".join(f"{LABELS[k]} {sum(1 for c in cards if c['label']==k)}" for k in ORDER), ""]
    for c in cards:
        name = c.get("symbol") or c["mint"][:6]
        L.append(f"{LABELS[c['label']]}  ${name}  {c['mint']}")
        if c.get("criteria"):
            for k, val in card_fields(c, T)[1:]:
                L.append(f"   {k}: {val}")
        L.append(f"   DECISIÓN: {c.get('decision')} — " + "; ".join(c["reasons"]))
        if plan_line(c):
            L.append("   " + plan_line(c))
        L.append("")
    return "\n".join(L)


def md_report(cards, T, path, n_wallets):
    L = ["# SCAN — Smart Money + Flat Base v1",
         f"**{datetime.fromtimestamp(T, timezone.utc):%Y-%m-%d %H:%M} UTC** · {n_wallets} smart wallets vigiladas", "",
         " · ".join(f"{LABELS[k]} **{sum(1 for c in cards if c['label']==k)}**" for k in ORDER), ""]
    if n_wallets == 0:
        L += ["> Tu lista de smart wallets está vacía. Añade direcciones en `wallets_to_add.txt` (una por línea: `dirección,nombre`)."]
    elif not cards:
        L += ["Ninguna compra relevante de tus smart wallets en la ventana."]
    for c in cards:
        sym = c.get("symbol") or c["mint"][:6]
        m = c["mint"]
        L.append(f"## {LABELS[c['label']]} — ${sym}")
        if c.get("criteria"):
            for k, val in card_fields(c, T):
                L.append(f"- **{k}:** " + (f"`{val}`" if k == "CA" else val))
        else:
            L.append(f"- **CA:** `{m}`")
        L.append(f"\n**DECISIÓN: {c.get('decision')}** — " + "; ".join(c["reasons"]))
        if plan_line(c):
            L.append(f"\n_{plan_line(c)}_")
        L.append(f"\n[GMGN](https://gmgn.ai/sol/token/{m}) · [DexScreener](https://dexscreener.com/solana/{m}) · "
                 f"[pump.fun](https://pump.fun/coin/{m}) · [Solscan](https://solscan.io/token/{m}#holders)\n")
    L += ["---", "✅ cumple · ❌ no cumple · ✋ compruébalo tú (apunta holders en el ATH y comunidad en `manual_checks.csv` y el radar lo completa solo)"]
    Path(path).write_text("\n".join(L) + "\n", encoding="utf-8")


def html_report(cards, T, path):
    css = """
:root{--bg:#0f1115;--card:#171a21;--fg:#e8eaf0;--mut:#9aa3b2;--line:#262b36;--g:#22c55e;--y:#eab308;--r:#ef4444;--k:#6b7280}
@media (prefers-color-scheme: light){:root{--bg:#f6f7f9;--card:#fff;--fg:#141821;--mut:#5b6474;--line:#e3e6ec}}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font:15px/1.45 system-ui,-apple-system,Segoe UI,Roboto,sans-serif}
.wrap{max-width:860px;margin:0 auto;padding:20px 16px 60px}h1{font-size:20px;margin:0 0 4px}.sub{color:var(--mut);font-size:13px;margin-bottom:16px}
.sum{display:flex;gap:8px;flex-wrap:wrap;margin-bottom:18px}.pill{background:var(--card);border:1px solid var(--line);border-radius:999px;padding:4px 12px;font-size:13px}
.card{background:var(--card);border:1px solid var(--line);border-left:5px solid var(--k);border-radius:12px;padding:14px 16px;margin:0 0 12px}
.ENTRY{border-left-color:var(--g)}.WATCH{border-left-color:var(--y)}.NO{border-left-color:var(--r)}
.hd{display:flex;justify-content:space-between;gap:8px;flex-wrap:wrap;align-items:baseline}.tag{font-weight:700;font-size:13px}
.sym{font-size:18px;font-weight:700}table{width:100%;border-collapse:collapse;margin:8px 0;font-size:14px}
td{padding:3px 0;vertical-align:top;border-bottom:1px solid var(--line)}td.k{color:var(--mut);width:42%;padding-right:10px}
td.v{word-break:break-word}.dec{font-weight:700;margin-top:8px}.why{font-size:13px;color:var(--mut)}.links a{color:inherit;font-size:13px;margin-right:12px}
"""
    body = []
    for c in cards:
        sym = c.get("symbol") or c["mint"][:6]
        m = c["mint"]
        rows = card_fields(c, T) if c.get("criteria") else [("CA", m)]
        tbl = "".join(f'<tr><td class="k">{html.escape(k)}</td><td class="v">{html.escape(str(v))}</td></tr>' for k, v in rows)
        pl = f'<div class="why">{html.escape(plan_line(c))}</div>' if plan_line(c) else ""
        links = (f'<div class="links"><a href="https://gmgn.ai/sol/token/{m}" target="_blank">GMGN</a>'
                 f'<a href="https://dexscreener.com/solana/{m}" target="_blank">DexScreener</a>'
                 f'<a href="https://pump.fun/coin/{m}" target="_blank">pump.fun</a>'
                 f'<a href="https://solscan.io/token/{m}" target="_blank">Solscan</a></div>')
        body.append(f'<div class="card {c["label"]}"><div class="hd"><span class="sym">${html.escape(str(sym))}</span>'
                    f'<span class="tag">{LABELS[c["label"]]}</span></div><table>{tbl}</table>'
                    f'<div class="dec">DECISIÓN: {html.escape(str(c.get("decision")))}</div>'
                    f'<div class="why">{html.escape("; ".join(c["reasons"]))}</div>{pl}{links}</div>')
    counts = "".join(f'<span class="pill">{LABELS[k]} · {sum(1 for c in cards if c["label"]==k)}</span>' for k in ORDER)
    doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Moonshot Scan</title><style>{css}</style></head><body><div class="wrap">
<h1>SCAN — Smart Money + Flat Base v1</h1><div class="sub">{datetime.fromtimestamp(T, timezone.utc):%d %b %Y · %H:%M} UTC</div>
<div class="sum">{counts}</div>{''.join(body) or '<p>Ninguna compra de tus smart wallets en la ventana.</p>'}
</div></body></html>"""
    Path(path).write_text(doc, encoding="utf-8")
    return path


def json_report(cards, T, path, n_wallets):
    doc = {"version": VERSION, "generated_utc": datetime.fromtimestamp(T, timezone.utc).isoformat(), "T": T,
           "n_wallets": n_wallets, "counts": {k: sum(1 for c in cards if c["label"] == k) for k in ORDER},
           "cards": [{k: v for k, v in c.items() if k != "flat_now"} for c in cards]}
    Path(path).write_text(json.dumps(doc, indent=1, default=str, ensure_ascii=False), encoding="utf-8")


def publish(cards, T, outdir, n_wallets):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    json_report(cards, T, out / "report.json", n_wallets)
    md_report(cards, T, out / "SCAN.md", n_wallets)
    html_report(cards, T, out / "index.html")
    return out


# ======================================================================================
# Verificación de wallets (add-wallet)
# ======================================================================================
def verify_wallet(rpc, store, wallet, R, sol_usd, log=True):
    """PnL REALIZADO aproximado en la ventana revisada (coste medio por token, en SOL -> USD al precio actual)."""
    sigs = recent_signatures(rpc, wallet, 0, R["wallet_pages"])
    trades, unrec = [], {}
    for i, s in enumerate(sigs, 1):
        tx = store.get(rpc, s["signature"])
        t = parse_wallet_trade(tx, wallet, s["signature"], sol_usd)
        if t and t.get("sol") is not None:
            trades.append(t)
        elif not t:
            mv = token_moves(tx, wallet)
            if len(mv) == 2 and min(mv.values()) < 0 < max(mv.values()):   # swap token↔token que no sé valorar
                for m in mv:
                    unrec[m] = unrec.get(m, 0) + 1
        if log and i % 100 == 0:
            print(f"    {i}/{len(sigs)} transacciones", file=sys.stderr, end="\r")
    trades.sort(key=lambda t: t["ts"])
    pos, realized, closed = {}, {}, {}
    for t in trades:
        q, cost = pos.get(t["mint"], (0.0, 0.0))
        if t["side"] == "buy":
            pos[t["mint"]] = (q + t["tokens"], cost + t["sol"])
        elif q > 0:
            take = min(q, t["tokens"])
            avg = cost / q
            realized[t["mint"]] = realized.get(t["mint"], 0.0) + take * (t["sol"] / t["tokens"] - avg)
            closed[t["mint"]] = closed.get(t["mint"], 0) + 1
            pos[t["mint"]] = (q - take, cost - avg * take)
    pnl_usd = sum(realized.values()) * sol_usd
    pos_pnl = [v for v in realized.values() if v > 0]
    top_share = max(pos_pnl) / sum(pos_pnl) if pos_pnl else None
    span = (trades[-1]["ts"] - trades[0]["ts"]) / 86400 if len(trades) > 1 else 0
    out = {"wallet": wallet, "verified_pnl_usd": round(pnl_usd), "closed_positions": sum(closed.values()),
           "distinct_tokens": len(realized), "top_token_share": None if top_share is None else round(top_share, 3),
           "window_days": round(span, 1), "n_trades": len(trades), "n_tx_reviewed": len(sigs),
           "swaps_unrecognized": sum(unrec.values()) // 2,
           "unrecognized_quotes": ",".join(m[:6] for m, _ in sorted(unrec.items(), key=lambda x: -x[1])[:3])}
    out["meets_criteria"] = bool(pnl_usd >= R["wallet_min_pnl_usd"] and out["closed_positions"] >= R["wallet_min_closed"]
                                 and out["distinct_tokens"] >= R["wallet_min_tokens"]
                                 and top_share is not None and top_share <= R["wallet_max_top_share"])
    return out


# ======================================================================================
# CLI
# ======================================================================================
def open_report(path):
    if os.environ.get("MOONSHOT_NO_BROWSER"):
        return
    try:
        webbrowser.open(Path(path).resolve().as_uri())
    except Exception:  # noqa: BLE001
        pass


def main(argv=None):
    argv = list(sys.argv[1:] if argv is None else argv)
    cmd = argv[0] if argv else "radar"
    if cmd in ("-h", "--help", "help"):
        print(__doc__); return
    if cmd == "demo":
        import moonshot_demo
        cards, T = moonshot_demo.run_demo()
        print(text_report(cards, T))
        p = html_report(cards, T, HERE / "moonshot_report_DEMO.html")
        print(f"\nInforme DEMO: {p}")
        open_report(p); return
    cfg = load_config()
    if cfg.get("demo"):
        return main(["demo"])
    import scan as scanmod
    rpc = tf.RPC(cfg["rpc_url"], min_interval=0.1)
    sol_usd, _ = scanmod.sol_price(cfg.get("sol_usd"))
    R = cfg["rules"]
    if cmd == "doctor":
        print("RPC:", "OK" if rpc.call("getSlot", []) else "FALLA")
        g = Gecko(R["gecko_min_interval"])
        pool = g.top_pool(tf.WSOL)
        print("GeckoTerminal:", "OK" if pool else "FALLA", "· SOL/USD", sol_usd)
        print("Smart wallets en tu lista:", len(load_wallets())); return
    if cmd == "status":
        return write_status(cfg, rpc, sol_usd, Path(argv[1] if len(argv) > 1 else HERE / "report"))
    if cmd == "wallets":
        for w in load_wallets():
            print(f"{w['wallet']}  {w.get('label','')}  PnL ${float(w.get('verified_pnl_usd') or 0):,.0f}  "
                  f"cumple={w.get('meets_criteria')}")
        return
    if cmd == "add-wallet":
        if len(argv) < 2:
            raise SystemExit("Uso: python moonshot.py add-wallet <DIRECCIÓN> [etiqueta]")
        addr, label = argv[1], (argv[2] if len(argv) > 2 else "")
        print(f"Verificando {addr} (últimas {R['wallet_pages']*1000} transacciones)…")
        v = verify_wallet(rpc, TxStore(), addr, R, sol_usd)
        print(json.dumps(v, indent=2))
        rows = [w for w in load_wallets() if w["wallet"] != addr]
        ok = v["meets_criteria"] or "--force" in argv
        if ok:
            rows.append({**v, "label": label, "forced": not v["meets_criteria"],
                         "verified_at": datetime.now(timezone.utc).isoformat()[:19]})
            save_wallets(rows)
            print(f"\n✅ Añadida{' (forzada: NO cumple tus criterios)' if not v['meets_criteria'] else ''}. Tienes {len(rows)} smart wallets.")
        else:
            print(f"\n❌ NO cumple tus criterios en la ventana revisada ({v['window_days']} días). "
                  "No la añado. Si aun así la quieres: añade --force al final.")
        return
    if cmd == "add-wallets-file":
        return add_wallets_file(rpc, R, sol_usd, Path(argv[1] if len(argv) > 1 else HERE / "wallets_to_add.txt"))
    if cmd != "radar":
        raise SystemExit(f"Comando desconocido: {cmd}. Usa: radar | add-wallet | add-wallets-file | wallets | doctor | demo")
    wallets = load_wallets()
    cards = run_radar(rpc, Gecko(R["gecko_min_interval"]), cfg, sol_usd=sol_usd, wallets=wallets)
    T = int(time.time())
    if not wallets:
        print("Tu lista de smart wallets está vacía: añade una con  python moonshot.py add-wallet <DIRECCIÓN> <nombre>")
    print(text_report(cards, T))
    if "--publish" in argv:
        out = publish(cards, T, argv[argv.index("--publish") + 1], len(wallets))
        print(f"\nPublicado en {out}/")
        return
    p = html_report(cards, T, HERE / "moonshot_report.html")
    print(f"\nInforme: {p}")
    open_report(p)


def add_wallets_file(rpc, R, sol_usd, path: Path):
    """Procesa wallets_to_add.txt (una por línea: dirección[,nombre][,force]). Añade las que cumplen,
    deja constancia en report/wallet_checks.md y vacía el archivo (las rechazadas quedan en el informe)."""
    if not path.exists():
        return
    lines = [l.strip() for l in path.read_text(encoding="utf-8").splitlines() if l.strip() and not l.startswith("#")]
    if not lines:
        return
    rows = load_wallets()
    have = {w["wallet"] for w in rows}
    store = TxStore()
    retry = []
    log = [f"# Verificación de wallets · {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC", "",
           "| Wallet | Nombre | PnL realizado | Cierres | Tokens | Top token | Ventana | Swaps leídos | Resultado |", "|---|---|---|---|---|---|---|---|---|"]
    budget = int(R.get("wallet_verify_per_run", 12))
    t_end = time.time() + 60 * float(R.get("verify_minutes", 18))
    for ln in lines:
        parts = [p.strip() for p in ln.split(",")]
        addr, label = parts[0], (parts[1] if len(parts) > 1 else "")
        force = len(parts) > 2 and parts[2].lower() == "force"
        if addr in have:
            log.append(f"| `{addr[:6]}…` | {label} | | | | | | | ya estaba |"); continue
        if budget <= 0 or time.time() > t_end:
            retry.append(ln); continue                    # se verifica en la siguiente ejecución
        budget -= 1
        try:
            v = verify_wallet(rpc, store, addr, {**R, "wallet_pages": 1} if force else R, sol_usd, log=False)
        except Exception as e:  # noqa: BLE001
            log.append(f"| `{addr[:6]}…` | {label} | | | | | | | ⚠️ error (se reintentará en la próxima ejecución): {scrub(e)} |")
            retry.append(ln); continue
        ok = v["meets_criteria"] or force
        if ok:
            rows.append({**v, "label": label, "forced": bool(force and not v["meets_criteria"]),
                         "verified_at": datetime.now(timezone.utc).isoformat()[:19]})
            have.add(addr)
        res = "✅ añadida" + (" (forzada)" if force and not v["meets_criteria"] else "") if ok else "❌ no cumple"
        top = "—" if v["top_token_share"] is None else f"{v['top_token_share']:.0%}"
        nu = v.get("swaps_unrecognized", 0)
        cov = f"{v['n_trades'] / (v['n_trades'] + nu):.0%}" if v["n_trades"] + nu else "—"
        if nu:
            cov += f" (no leídos: {nu}, contra {v.get('unrecognized_quotes')})"
        log.append(f"| `{addr[:6]}…` | {label} | ${v['verified_pnl_usd']:,} | {v['closed_positions']} | {v['distinct_tokens']} | "
                   f"{top} | {v['window_days']} d | {cov} | {res} |")
    save_wallets(rows)
    path.write_text("# una wallet por línea:  dirección,nombre   (añade ,force para saltarte la verificación)\n"
                    + "".join(l + "\n" for l in retry), encoding="utf-8")
    out = HERE / "report"
    out.mkdir(exist_ok=True)
    prev = out / "wallet_checks.md"                     # acumula: no borra las verificaciones anteriores
    old = [l for l in prev.read_text(encoding="utf-8").splitlines() if l.startswith("| `")] if prev.exists() else []
    new = [l for l in log[4:]]
    log = log[:4] + new + [l for l in old if l not in new]
    log[0] = f"# Verificación de wallets · última: {datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC"
    prev.write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


# ======================================================================================
# Diagnóstico publicado (report/STATUS.md): se puede leer desde el chat sin ver GitHub
# ======================================================================================
def scrub(text, cfg=None):
    """Quita la URL/API key del RPC de cualquier mensaje antes de publicarlo."""
    import re
    text = str(text)
    url = (cfg or {}).get("rpc_url") or os.environ.get("SOLANA_RPC") or ""
    if url:
        text = text.replace(url, "<RPC>")
    return re.sub(r"(api[-_]?key=)[^&\s'\"]+", r"\1***", text, flags=re.I)


def write_status(cfg, rpc, sol_usd, outdir):
    out = Path(outdir)
    out.mkdir(parents=True, exist_ok=True)
    T = datetime.now(timezone.utc)
    L = [f"# STATUS · {T:%Y-%m-%d %H:%M} UTC", "", f"- Versión: `{VERSION}` (TX_VERSION={TX_VERSION})",
         f"- Secreto SOLANA_RPC: {'✅ presente' if cfg.get('rpc_url') else '❌ FALTA'}"]
    try:
        L.append(f"- RPC getSlot: ✅ {rpc.call('getSlot', [])}")
    except Exception as e:  # noqa: BLE001
        L.append(f"- RPC getSlot: ❌ {scrub(e, cfg)}")
    try:
        sig = rpc.call("getSignaturesForAddress", [pdsc.PUMP_PROGRAM, {"limit": 1}])[0]["signature"]
        tx = rpc.call("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": TX_VERSION}])
        L.append(f"- RPC getTransaction (versión {tx.get('version')}): ✅")
    except Exception as e:  # noqa: BLE001
        L.append(f"- RPC getTransaction: ❌ {scrub(e, cfg)}")
    try:
        L.append(f"- GeckoTerminal: {'✅' if Gecko(cfg['rules']['gecko_min_interval']).top_pool(tf.WSOL) else '❌ sin datos'}")
    except Exception as e:  # noqa: BLE001
        L.append(f"- GeckoTerminal: ❌ {scrub(e, cfg)}")
    L.append(f"- SOL/USD: {sol_usd}")
    ws = load_wallets()
    L += ["", f"## Smart wallets vigiladas: {len(ws)}"]
    for w in ws:
        L.append(f"- `{w['wallet'][:6]}…` {w.get('label','')} · PnL ventana ${float(w.get('verified_pnl_usd') or 0):,.0f} · "
                 f"cierres {w.get('closed_positions')} · {'forzada (verificada a mano)' if str(w.get('forced')).lower()=='true' else 'cumple' if str(w.get('meets_criteria')).lower()=='true' else 'no cumple'}")
    pend = HERE / "wallets_to_add.txt"
    pl = [l for l in (pend.read_text(encoding="utf-8").splitlines() if pend.exists() else []) if l.strip() and not l.startswith("#")]
    L.append(f"- Pendientes en wallets_to_add.txt: {len(pl)}")
    prog = out / "scan_progress.txt"
    L.append(f"- Último radar: {prog.read_text(encoding='utf-8').strip() if prog.exists() else '—'}")
    err = out / "last_error.txt"
    L += ["", "## Último error", "```", err.read_text(encoding="utf-8")[-3000:] if err.exists() else "ninguno", "```"]
    (out / "STATUS.md").write_text("\n".join(L) + "\n", encoding="utf-8")
    print("\n".join(L))


if __name__ == "__main__":
    import traceback
    errf = HERE / "report" / "last_error.txt"
    try:
        main()
        if len(sys.argv) > 1 and sys.argv[1] == "radar" and errf.exists():
            errf.unlink()
    except BaseException as ex:  # noqa: BLE001
        if not isinstance(ex, SystemExit) or ex.code not in (0, None):
            errf.parent.mkdir(exist_ok=True)
            errf.write_text(f"{datetime.now(timezone.utc):%Y-%m-%d %H:%M} UTC · {' '.join(sys.argv[1:])}\n"
                            + scrub(traceback.format_exc()), encoding="utf-8")
        raise
