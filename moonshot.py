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


VERSION = "moonshot-radar-0.7"
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
    # ---- verificación de wallets (add-wallet)
    "wallet_min_pnl_usd": 1_000_000,
    "wallet_min_closed": 20,
    "wallet_min_tokens": 5,
    "wallet_max_top_share": 0.50,
    "wallet_pages": 3,               # páginas de 1000 tx a revisar al verificar una wallet
    # ---- coste
    "wallet_scan_pages": 3,          # páginas de firmas por wallet en cada radar
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
            "window_days", "meets_criteria", "verified_at"]
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

    def top_pool(self, mint):
        j = self.get(f"/networks/solana/tokens/{mint}/pools", {"page": 1})
        pools = (j or {}).get("data") or []
        if not pools:
            return None
        pools.sort(key=lambda p: float(p["attributes"].get("reserve_in_usd") or 0), reverse=True)
        return pools[0]["attributes"]["address"]

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


def parse_wallet_trade(tx, wallet, sig):
    """Swap del propio wallet: exactamente un mint (no-SOL) cambia -> compra o venta de ese mint."""
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


def wallet_trades(rpc, store, wallet, since_ts, pages):
    out = []
    for s in recent_signatures(rpc, wallet, since_ts, pages):
        t = parse_wallet_trade(store.get(rpc, s["signature"]), wallet, s["signature"])
        if t:
            out.append(t)
    return sorted(out, key=lambda t: t["ts"])


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


def evaluate(mint, buys, candles, supply, mi, holdings, T, R):
    """buys: compras relevantes de smart wallets en este mint. Devuelve la tarjeta con etiqueta."""
    card = {"mint": mint, "smart_wallets": sorted({b["label"] or b["wallet"][:6] for b in buys}),
            "n_smart": len({b["wallet"] for b in buys}), "reasons": []}
    hard = sf.hard_checks(mi)
    if hard:
        card.update(label="NO", reasons=["HARD: " + h for h in hard])
        return card
    if candles is None or candles.empty or not supply:
        card.update(label="NODATA", reasons=["sin historial de precio (GeckoTerminal) o sin supply"])
        return card
    c = candles.copy()
    c["mc"] = c.c * supply
    first = min(buys, key=lambda b: b["ts"])
    tb = first["ts"]
    pre = c[c.ts <= tb]
    if pre.empty:
        card.update(label="NODATA", reasons=["no hay historial anterior a la compra del trader"])
        return card
    peak_pre = float(pre.h.max() * supply)
    mc_buy = float(pre.c.iloc[-1] * supply)
    mc_now = float(c.c.iloc[-1] * supply)
    peak_all = float(c.h.max() * supply)
    dd_buy = 1 - mc_buy / peak_pre if peak_pre else None
    dd_now = 1 - mc_now / peak_all if peak_all else None
    fb = flat_state(c, tb, R["flat_hours"], R["flat_band"], R["min_flat_candles"])
    fn = flat_state(c, int(c.ts.iloc[-1]), R["flat_hours"], R["flat_band"], R["min_flat_candles"])
    vol24 = c.v.rolling(24, min_periods=1).sum()
    hist_peak_vol = float(vol24[c.ts <= tb].max()) if (c.ts <= tb).any() else 0.0
    since = base_since(c, tb, R["flat_band"])
    premium = mc_now / mc_buy - 1 if mc_buy else None
    bought = sum(b["tokens"] for b in buys if b["wallet"] == first["wallet"])
    hold = holdings.get(first["wallet"])
    held_frac = min(1.0, hold / bought) if (hold is not None and bought > 0) else None
    card.update({
        "symbol": None, "mc_now": mc_now, "mc_at_trader_buy": mc_buy, "peak_mc": peak_pre, "peak_mc_all": peak_all,
        "drawdown_at_buy": dd_buy, "drawdown_now": dd_now, "premium": premium,
        "flat_at_buy": fb, "flat_now": fn, "base_since_ts": since,
        "base_hours": (tb - since) / 3600 if (since and fb.get("flat")) else None,
        "hist_peak_vol_24h": hist_peak_vol, "vol_24h_now": float(vol24.iloc[-1]),
        "trader": first["label"] or first["wallet"], "trader_wallet": first["wallet"],
        "trader_buy_ts": tb, "trader_buy_usd": sum(b["usd"] for b in buys if b["wallet"] == first["wallet"]),
        "trader_held_frac": held_frac, "floor_mc": (fb.get("floor") or 0) * supply if fb.get("flat") else None,
    })
    # ---------- reglas
    red, yellow = [], []
    if peak_pre < R["peak_mc_min_usd"]:
        red.append(f"pico previo ${peak_pre/1e3:,.0f}k < ${R['peak_mc_min_usd']/1e3:,.0f}k")
    if dd_buy is not None and dd_buy < R["drawdown_min"]:
        (yellow if dd_buy >= R["drawdown_min"] - 0.10 else red).append(f"caída desde el pico {dd_buy:.0%} < {R['drawdown_min']:.0%}")
    if fb["flat"] is None:
        yellow.append(f"pocas velas para juzgar la base ({fb['n']} < {R['min_flat_candles']})")
    elif not fb["flat"]:
        red.append(f"no estaba plano en las {R['flat_hours']} h previas a la compra")
    if R["min_hist_peak_vol_usd"] and hist_peak_vol < R["min_hist_peak_vol_usd"]:
        red.append(f"volumen 24 h máximo histórico ${hist_peak_vol/1e3:,.0f}k < ${R['min_hist_peak_vol_usd']/1e3:,.0f}k")
    if held_frac is not None and held_frac <= 1 - R["trader_sold_exit"]:
        red.append(f"el trader ya vendió {1-held_frac:.0%} de lo que compró")
    elif held_frac is None:
        yellow.append("no pude comprobar si el trader sigue dentro")
    if premium is not None:
        if premium > R["watch_premium"]:
            red.append(f"precio {premium:+.0%} sobre el del trader: llegas tarde")
        elif premium > R["max_premium"]:
            yellow.append(f"precio {premium:+.0%} sobre el del trader (máx. {R['max_premium']:+.0%})")
    if fn["flat"] is False and (premium or 0) <= R["max_premium"]:
        yellow.append("la base se está rompiendo (ya no está plano)")
    if red:
        card.update(label="NO", reasons=red + yellow)
    elif yellow:
        card.update(label="WATCH", reasons=yellow)
    else:
        card.update(label="ENTRY", reasons=["cumple todas tus reglas"])
    return card


# ======================================================================================
# Radar
# ======================================================================================
LABELS = {"ENTRY": "🟢 ZONA DE ENTRADA", "WATCH": "🟡 VIGILAR", "NO": "🔴 NO", "NODATA": "⚫ SIN DATOS"}
ORDER = {"ENTRY": 0, "WATCH": 1, "NO": 2, "NODATA": 3}


def run_radar(rpc, gecko, cfg, T=None, sol_usd=None, wallets=None, log=True, state_dir=None,
              log_file="default"):
    R = cfg["rules"]
    T = int(T or time.time())
    wallets = wallets if wallets is not None else load_wallets()
    if not wallets:
        return []
    store = TxStore(state_dir)
    since = T - R["lookback_hours"] * 3600

    def say(m):
        if log:
            print(m, file=sys.stderr, flush=True)
    say(f"[1/4] compras de {len(wallets)} smart wallets en las últimas {R['lookback_hours']} h")
    buys = []
    for w in wallets:
        for t in wallet_trades(rpc, store, w["wallet"], since, R["wallet_scan_pages"]):
            if t["side"] == "buy" and t["ts"] <= T:
                t["usd"] = t["sol"] * sol_usd
                t["label"] = w.get("label") or ""
                if t["usd"] >= R["min_trader_buy_usd"]:
                    buys.append(t)
    by_mint = {}
    for b in buys:
        by_mint.setdefault(b["mint"], []).append(b)
    say(f"[2/4] {len(buys)} compras relevantes en {len(by_mint)} tokens")
    mints = list(by_mint)
    minfo = pdsc.get_multiple(rpc, mints, "jsonParsed") if mints else {}
    cards = []
    for i, m in enumerate(mints, 1):
        say(f"[3/4] {i}/{len(mints)} {m[:8]}… historial de precio")
        acct = minfo.get(m)
        mi = pdsc.mint_info(acct, pdsc.DEFAULTS)
        supply = None
        try:
            info = acct["data"]["parsed"]["info"]
            supply = int(info["supply"]) / 10 ** int(info["decimals"])
        except (KeyError, TypeError, ValueError):
            pass
        candles = None
        try:
            pool = gecko.top_pool(m)
            if pool:
                candles = gecko.ohlcv_hour(pool, m)
        except RuntimeError as e:
            say(f"    {e}")
        holdings = {}
        for w in {b["wallet"] for b in by_mint[m]}:
            try:
                holdings[w] = token_balance(rpc, w, m)
            except RuntimeError:
                holdings[w] = None
        card = evaluate(m, by_mint[m], candles, supply, mi, holdings, T, R)
        card["name"], card["symbol"] = token_meta(acct)
        cards.append(card)
    say("[4/4] informe")
    store.prune(since - 24 * 3600)
    cards.sort(key=lambda c: (ORDER[c["label"]], -c["n_smart"], c.get("premium") if c.get("premium") is not None else 9))
    if log_file == "default":
        log_file = HERE / "radar_log.jsonl"
    if log_file:
        with open(log_file, "a", encoding="utf-8") as fh:   # registro para validar las reglas después
            for c in cards:
                fh.write(json.dumps({"T": T, "version": VERSION, "rules": R, **c}, default=str) + "\n")
    return cards


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


def text_report(cards, T):
    L = [f"MOONSHOT RADAR · {datetime.fromtimestamp(T, timezone.utc):%Y-%m-%d %H:%M} UTC",
         "  ".join(f"{LABELS[k]} {sum(1 for c in cards if c['label']==k)}" for k in ORDER), ""]
    for c in cards:
        name = c.get("symbol") or c["mint"][:6]
        L.append(f"{LABELS[c['label']]}  ${name}  {c['mint']}")
        if c.get("mc_now") is not None:
            L.append(f"   MC {usd(c['mc_now'])} · pico {usd(c.get('peak_mc'))} · caída {c['drawdown_now']:.0%} · "
                     f"en base {dur(c['base_hours'])}" if c.get("base_hours") else
                     f"   MC {usd(c['mc_now'])} · pico {usd(c.get('peak_mc'))} · caída {c['drawdown_now']:.0%}")
            held = "—" if c["trader_held_frac"] is None else f"{c['trader_held_frac']:.0%}"
            L.append(f"   {c['trader']} compró {usd(c['trader_buy_usd'])} a MC {usd(c['mc_at_trader_buy'])} "
                     f"{ago(c['trader_buy_ts'], T)} · tú: {pct(c['premium'])} · sigue dentro: {held}"
                     + (f" · {c['n_smart']} smart wallets" if c["n_smart"] > 1 else ""))
        L.append("   " + "; ".join(c["reasons"]))
        L.append("")
    return "\n".join(L)


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
.sym{font-size:18px;font-weight:700}.ca{color:var(--mut);font-size:12px;word-break:break-all;margin:2px 0 10px}
.grid{display:grid;grid-template-columns:repeat(auto-fit,minmax(150px,1fr));gap:8px 16px;margin:6px 0 10px}
.k{color:var(--mut);font-size:12px}.v{font-weight:600}.why{font-size:13px;color:var(--mut)}.links a{color:inherit;font-size:13px;margin-right:12px}
details{margin-top:18px;color:var(--mut);font-size:13px}.warn{font-size:12px;color:var(--mut);margin-top:24px;border-top:1px solid var(--line);padding-top:12px}
"""
    def cell(k, v):
        return f'<div><div class="k">{html.escape(k)}</div><div class="v">{html.escape(v)}</div></div>'
    body = []
    for c in cards:
        sym = c.get("symbol") or c["mint"][:6]
        m = c["mint"]
        cells = ""
        if c.get("mc_now") is not None:
            held = "—" if c["trader_held_frac"] is None else f"{c['trader_held_frac']:.0%}"
            cells = "".join([
                cell("MC ahora", usd(c["mc_now"])), cell("Pico previo", usd(c["peak_mc"])),
                cell("Caída desde pico", f"{c['drawdown_now']:.0%}" if c.get("drawdown_now") is not None else "—"),
                cell("En base", dur(c.get("base_hours"))),
                cell("Trader", str(c["trader"])[:22]), cell("Compró", f"{usd(c['trader_buy_usd'])} · {ago(c['trader_buy_ts'], T)}"),
                cell("MC al comprar él", usd(c["mc_at_trader_buy"])), cell("Tu precio vs el suyo", pct(c["premium"])),
                cell("Sigue dentro", held), cell("Smart wallets", str(c["n_smart"])),
            ] + ([cell("Suelo (stop)", usd(c.get("floor_mc"))), cell("Objetivo 2×", usd(2 * c["mc_now"]))]
                 if c["label"] in ("ENTRY", "WATCH") else []))
        links = (f'<div class="links"><a href="https://pump.fun/coin/{m}" target="_blank">pump.fun</a>'
                 f'<a href="https://dexscreener.com/solana/{m}" target="_blank">DexScreener</a>'
                 f'<a href="https://gmgn.ai/sol/token/{m}" target="_blank">GMGN</a>'
                 f'<a href="https://solscan.io/token/{m}" target="_blank">Solscan</a></div>')
        body.append(f'<div class="card {c["label"]}"><div class="hd"><span class="sym">${html.escape(str(sym))}</span>'
                    f'<span class="tag">{LABELS[c["label"]]}</span></div><div class="ca">{m}</div>'
                    f'<div class="grid">{cells}</div><div class="why">{html.escape("; ".join(c["reasons"]))}</div>{links}</div>')
    counts = "".join(f'<span class="pill">{LABELS[k]} · {sum(1 for c in cards if c["label"]==k)}</span>' for k in ORDER)
    doc = f"""<!doctype html><html lang="es"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>Moonshot Radar</title><style>{css}</style></head><body><div class="wrap">
<h1>Moonshot Radar</h1><div class="sub">{datetime.fromtimestamp(T, timezone.utc):%d %b %Y · %H:%M} UTC · top traders comprando bases planas</div>
<div class="sum">{counts}</div>{''.join(body) or '<p>Ninguna compra de tus smart wallets en la ventana.</p>'}
<div class="warn">Reglas PROVISIONALES (moonshot_config.json) hasta validarlas con smart_money_study.py. Esto ordena qué mirar; no es una recomendación de compra. Mira siempre el gráfico y la liquidez antes de operar.</div>
</div></body></html>"""
    Path(path).write_text(doc, encoding="utf-8")
    return path


def json_report(cards, T, path, n_wallets):
    doc = {"version": VERSION, "generated_utc": datetime.fromtimestamp(T, timezone.utc).isoformat(), "T": T,
           "n_wallets": n_wallets, "counts": {k: sum(1 for c in cards if c["label"] == k) for k in ORDER},
           "cards": [{k: v for k, v in c.items() if k not in ("flat_at_buy", "flat_now")} for c in cards]}
    Path(path).write_text(json.dumps(doc, indent=1, default=str, ensure_ascii=False), encoding="utf-8")


def md_report(cards, T, path, n_wallets):
    L = [f"# Moonshot Radar", f"**{datetime.fromtimestamp(T, timezone.utc):%Y-%m-%d %H:%M} UTC** · {n_wallets} smart wallets vigiladas",
         "", " · ".join(f"{LABELS[k]} **{sum(1 for c in cards if c['label']==k)}**" for k in ORDER), ""]
    if n_wallets == 0:
        L += ["> Tu lista de smart wallets está vacía. Añade direcciones en `wallets_to_add.txt` (una por línea: `dirección,nombre`)."]
    elif not cards:
        L += ["Ninguna compra relevante de tus smart wallets en la ventana."]
    for c in cards:
        sym = c.get("symbol") or c["mint"][:6]
        L.append(f"## {LABELS[c['label']]} · ${sym}")
        L.append(f"`{c['mint']}` · [pump.fun](https://pump.fun/coin/{c['mint']}) · [DexScreener](https://dexscreener.com/solana/{c['mint']}) · [GMGN](https://gmgn.ai/sol/token/{c['mint']})")
        if c.get("mc_now") is not None:
            held = "—" if c["trader_held_frac"] is None else f"{c['trader_held_frac']:.0%}"
            L += ["", "| MC ahora | Pico | Caída | En base |", "|---|---|---|---|",
                  f"| {usd(c['mc_now'])} | {usd(c['peak_mc'])} | {c['drawdown_now']:.0%} | {dur(c.get('base_hours'))} |", "",
                  "| Trader | Compró | MC al comprar él | Tu precio vs el suyo | Sigue dentro | Smart wallets |", "|---|---|---|---|---|---|",
                  f"| {c['trader']} | {usd(c['trader_buy_usd'])} {ago(c['trader_buy_ts'], T)} | {usd(c['mc_at_trader_buy'])} | {pct(c['premium'])} | {held} | {c['n_smart']} |"]
            if c["label"] in ("ENTRY", "WATCH"):
                L.append(f"\nSuelo (stop): **{usd(c.get('floor_mc'))}** · Objetivo 2×: **{usd(2*c['mc_now'])}**")
        L += ["", f"_{'; '.join(c['reasons'])}_", ""]
    L += ["---", "_Reglas provisionales (moonshot_config.json). Ordena qué mirar; no es una recomendación de compra._"]
    Path(path).write_text("\n".join(L) + "\n", encoding="utf-8")


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
    trades = []
    for i, s in enumerate(sigs, 1):
        t = parse_wallet_trade(store.get(rpc, s["signature"]), wallet, s["signature"])
        if t:
            trades.append(t)
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
           "window_days": round(span, 1), "n_trades": len(trades), "n_tx_reviewed": len(sigs)}
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
            rows.append({**v, "label": label, "verified_at": datetime.now(timezone.utc).isoformat()[:19]})
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
           "| Wallet | Nombre | PnL realizado | Cierres | Tokens | Top token | Ventana | Resultado |", "|---|---|---|---|---|---|---|---|"]
    for ln in lines:
        parts = [p.strip() for p in ln.split(",")]
        addr, label = parts[0], (parts[1] if len(parts) > 1 else "")
        force = len(parts) > 2 and parts[2].lower() == "force"
        if addr in have:
            log.append(f"| `{addr[:6]}…` | {label} | | | | | | ya estaba |"); continue
        try:
            v = verify_wallet(rpc, store, addr, R, sol_usd, log=False)
        except Exception as e:  # noqa: BLE001
            log.append(f"| `{addr[:6]}…` | {label} | | | | | | ⚠️ error (se reintentará en la próxima ejecución): {e} |")
            retry.append(ln); continue
        ok = v["meets_criteria"] or force
        if ok:
            rows.append({**v, "label": label, "verified_at": datetime.now(timezone.utc).isoformat()[:19]})
            have.add(addr)
        res = "✅ añadida" + (" (forzada)" if force and not v["meets_criteria"] else "") if ok else "❌ no cumple"
        top = "—" if v["top_token_share"] is None else f"{v['top_token_share']:.0%}"
        log.append(f"| `{addr[:6]}…` | {label} | ${v['verified_pnl_usd']:,} | {v['closed_positions']} | {v['distinct_tokens']} | "
                   f"{top} | {v['window_days']} d | {res} |")
    save_wallets(rows)
    path.write_text("# una wallet por línea:  dirección,nombre   (añade ,force para saltarte la verificación)\n"
                    + "".join(l + "\n" for l in retry), encoding="utf-8")
    out = HERE / "report"
    out.mkdir(exist_ok=True)
    (out / "wallet_checks.md").write_text("\n".join(log) + "\n", encoding="utf-8")
    print("\n".join(log))


if __name__ == "__main__":
    main()
