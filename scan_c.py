#!/usr/bin/env python3
"""
SCAN C — META / FLYWHEEL: cambios estructurales que se desarrollan en días/semanas (ventana $0,5M–$5M de MC).

  1. REVENUE ENGINE   DefiLlama: comisiones, ingresos y recompras de cada plataforma (7 días vs 7 anteriores).
  2. META             GeckoTerminal: pools nuevos por token de pago (ZEC, GPRO, KOx…), 1h / 6h / 24h vs ventana anterior.
  3. LEADER           por meta: el de más volumen, el que más acelera, el primero que llegó a $1M, y el token de pago.
  4. CALL TRACKER     canales públicos de Telegram (t.me/s/…): cada CA con hora y MC al publicar; luego +1h, +6h, ATH, caída.
  5. TAX FLOW         impuesto: %, fijo o modificable, quién lo controla, quién lo cobra.

Estados: 🟡 META ACTIVÁNDOSE / 🟡 FLYWHEEL ACELERANDO  ->  🟢 CANDIDATA (solo si el líder pasa seguridad, liquidez y
concentración y está en la ventana de MC). Nunca "COMPRA AHORA": la entrada la decides tú con el análisis técnico.
Solo se guardan señales hacia delante (scan_c/signals.jsonl), sin reinterpretar el pasado.
Diseñado por "cadenas" (CHAINS) para añadir otras redes sin reescribir.
"""
from __future__ import annotations

import html as htmlmod
import json
import re
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

DATA = HERE / "scan_c"
CHAINS = {"solana": {"llama": "solana", "gecko": "solana", "dexscreener": "solana"}}
CFG = {
    "chain": "solana",
    "telegram_channels": ["SoapsGems1"],
    "base_quotes": {"So11111111111111111111111111111111111111112", "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v",
                    "Es9vMFrzaCERmJfrF4H2FYD4KCoNkY11McCe8BenwNYB"},   # SOL, USDC, USDT no son "metas"
    "gecko_pages": 10,
    # umbrales (provisionales, se registran todas las señales para calibrar)
    "meta_min_pools_24h": 10, "meta_accel": 2.0,
    "rev_min_7d": 50_000, "rev_accel": 2.0,
    "mc_min": 500_000, "mc_max": 5_000_000, "liq_min_frac": 0.05,
    "keep_days": 7,
}
B58 = re.compile(r"\b[1-9A-HJ-NP-Za-km-z]{32,44}\b")


# ------------------------------------------------------------------------------------------------
# HTTP mínimo (inyectable en los tests)
# ------------------------------------------------------------------------------------------------
class Http:
    def __init__(self, min_interval=1.0):
        import requests
        self.s = requests.Session()
        self.s.headers["User-Agent"] = "moonshot-scan-c/1.0"
        self.min_interval, self._last = min_interval, 0.0

    def _get(self, url, params=None):
        for attempt in range(4):
            wait = self.min_interval - (time.time() - self._last)
            if wait > 0:
                time.sleep(wait)
            self._last = time.time()
            r = self.s.get(url, params=params or {}, timeout=30)
            if r.status_code in (429, 500, 502, 503, 504):
                time.sleep(3 * (attempt + 1))
                continue
            if r.status_code == 404:
                return None
            r.raise_for_status()
            return r
        raise RuntimeError(f"no responde: {url}")

    def json(self, url, params=None):
        r = self._get(url, params)
        return r.json() if r is not None else None

    def text(self, url, params=None):
        r = self._get(url, params)
        return r.text if r is not None else None


# ------------------------------------------------------------------------------------------------
# 1. REVENUE ENGINE (DefiLlama)
# ------------------------------------------------------------------------------------------------
def revenue_engine(http, chain):
    base = f"https://api.llama.fi/overview/fees/{CHAINS[chain]['llama']}"
    out = {}
    for dtype in ("dailyRevenue", "dailyHoldersRevenue"):
        j = http.json(base, {"excludeTotalDataChart": "true", "excludeTotalDataChartBreakdown": "true",
                             "dataType": dtype}) or {}
        for p in j.get("protocols") or []:
            key = p.get("slug") or p.get("name")
            r = out.setdefault(key, {"name": p.get("displayName") or p.get("name"), "slug": p.get("slug"),
                                     "category": p.get("category"), "gecko_id": p.get("gecko_id")})
            pre = "rev" if dtype == "dailyRevenue" else "hold"
            r[f"{pre}_24h"] = p.get("total24h")
            r[f"{pre}_prev24h"] = p.get("total48hto24h")
            r[f"{pre}_7d"] = p.get("total7d")
            r[f"{pre}_prev7d"] = p.get("total14dto7d")
            r[f"{pre}_30d"] = p.get("total30d")
    sig = []
    for r in out.values():
        r7, p7 = r.get("rev_7d") or 0, r.get("rev_prev7d") or 0
        if r7 < CFG["rev_min_7d"]:
            continue
        r["rev_accel"] = (r7 / p7) if p7 else float("inf")
        if r["rev_accel"] >= CFG["rev_accel"]:
            sig.append(r)
    sig.sort(key=lambda r: -(r["rev_7d"] or 0))
    return sig


def token_address(http, gecko_id, chain):
    if not gecko_id:
        return None
    j = http.json(f"https://api.coingecko.com/api/v3/coins/{gecko_id}",
                  {"localization": "false", "tickers": "false", "market_data": "false", "community_data": "false",
                   "developer_data": "false"}) or {}
    return (j.get("platforms") or {}).get(chain) or None


def token_mcaps(http, gecko_ids):
    ids = [g for g in gecko_ids if g]
    if not ids:
        return {}
    j = http.json("https://api.coingecko.com/api/v3/coins/markets",
                  {"vs_currency": "usd", "ids": ",".join(ids[:100])}) or []
    return {c["id"]: {"mc": c.get("market_cap"), "fdv": c.get("fully_diluted_valuation"), "symbol": c.get("symbol"),
                      "price_change_7d": None, "volume": c.get("total_volume")} for c in j if isinstance(c, dict)}


# ------------------------------------------------------------------------------------------------
# 2. META ACCELERATION (GeckoTerminal new pools por token de pago)
# ------------------------------------------------------------------------------------------------
def fetch_new_pools(http, chain, pages):
    out, toks = [], {}
    for page in range(1, pages + 1):
        j = http.json(f"https://api.geckoterminal.com/api/v2/networks/{CHAINS[chain]['gecko']}/new_pools",
                      {"page": page, "include": "base_token,quote_token"})
        if not j:
            break
        for t in j.get("included") or []:
            a = t.get("attributes") or {}
            toks[t.get("id")] = {"symbol": a.get("symbol"), "address": a.get("address")}
        for p in j.get("data") or []:
            a, rel = p.get("attributes") or {}, p.get("relationships") or {}
            try:
                bid = rel["base_token"]["data"]["id"]
                qid = rel["quote_token"]["data"]["id"]
            except (KeyError, TypeError):
                continue
            created = a.get("pool_created_at")
            try:
                ts = int(datetime.fromisoformat(created.replace("Z", "+00:00")).timestamp())
            except (AttributeError, ValueError):
                continue
            out.append({"pool": a.get("address"), "ts": ts, "base": bid.split("_", 1)[-1], "quote": qid.split("_", 1)[-1],
                        "dex": ((rel.get("dex") or {}).get("data") or {}).get("id"),
                        "fdv": _num(a.get("fdv_usd")), "mc": _num(a.get("market_cap_usd")),
                        "liq": _num(a.get("reserve_in_usd")), "vol24": _num((a.get("volume_usd") or {}).get("h24"))})
        if len(j.get("data") or []) < 20:
            break
    for p in out:
        p["quote_symbol"] = (toks.get(f"{CHAINS[chain]['gecko']}_{p['quote']}") or {}).get("symbol")
        p["base_symbol"] = (toks.get(f"{CHAINS[chain]['gecko']}_{p['base']}") or {}).get("symbol")
    return out


def _num(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def meta_acceleration(registry, T):
    """registry: {pool: {...}} acumulado. Devuelve metas por token de pago con conteos y aceleración."""
    by_q = {}
    for p in registry.values():
        if p["quote"] in CFG["base_quotes"]:
            continue
        by_q.setdefault(p["quote"], []).append(p)
    metas = []
    for q, ps in by_q.items():
        def n(a, b):
            return sum(1 for p in ps if T - a * 3600 < p["ts"] <= T - b * 3600)
        m = {"quote": q, "symbol": next((p.get("quote_symbol") for p in ps if p.get("quote_symbol")), None),
             "n1h": n(1, 0), "n1h_prev": n(2, 1), "n6h": n(6, 0), "n6h_prev": n(12, 6),
             "n24h": n(24, 0), "n24h_prev": n(48, 24), "pools": ps}
        m["accel24"] = m["n24h"] / m["n24h_prev"] if m["n24h_prev"] else (float("inf") if m["n24h"] else 0)
        m["accel6"] = m["n6h"] / m["n6h_prev"] if m["n6h_prev"] else (float("inf") if m["n6h"] else 0)
        m["active"] = m["n24h"] >= CFG["meta_min_pools_24h"] and (m["accel24"] >= CFG["meta_accel"] or m["accel6"] >= CFG["meta_accel"])
        metas.append(m)
    metas.sort(key=lambda m: (-m["active"], -m["n24h"]))
    return metas


# ------------------------------------------------------------------------------------------------
# 3. LEADER DETECTION
# ------------------------------------------------------------------------------------------------
def dexscreener(http, chain, addrs):
    out = {}
    addrs = [a for a in dict.fromkeys(addrs) if a]
    for i in range(0, len(addrs), 30):
        j = http.json("https://api.dexscreener.com/latest/dex/tokens/" + ",".join(addrs[i:i + 30])) or {}
        for p in j.get("pairs") or []:
            if p.get("chainId") != CHAINS[chain]["dexscreener"]:
                continue
            a = (p.get("baseToken") or {}).get("address")
            liq = (p.get("liquidity") or {}).get("usd") or 0
            if a in out and (out[a]["liq"] or 0) >= liq:
                continue
            out[a] = {"symbol": (p.get("baseToken") or {}).get("symbol"), "mc": p.get("marketCap") or p.get("fdv"),
                      "liq": liq, "vol24": (p.get("volume") or {}).get("h24"), "vol6": (p.get("volume") or {}).get("h6"),
                      "chg1": (p.get("priceChange") or {}).get("h1"), "chg6": (p.get("priceChange") or {}).get("h6"),
                      "chg24": (p.get("priceChange") or {}).get("h24"), "created": (p.get("pairCreatedAt") or 0) // 1000,
                      "pair": p.get("pairAddress"), "dex": p.get("dexId"), "price": _num(p.get("priceUsd"))}
    return out


def leaders(meta, ds):
    rows = []
    for p in meta["pools"]:
        d = ds.get(p["base"])
        if d:
            rows.append({**d, "address": p["base"]})
    if not rows:
        return {}
    by_vol = max(rows, key=lambda r: r["vol24"] or 0)
    by_up = max(rows, key=lambda r: r["chg24"] or -1e9)
    first_1m = min((r for r in rows if (r["mc"] or 0) >= 1_000_000), key=lambda r: r["created"] or 9e18, default=None)
    return {"volumen": by_vol, "mayor_subida_24h": by_up, "primero_1M": first_1m}


# ------------------------------------------------------------------------------------------------
# 5. SEGURIDAD + TAX FLOW del líder (si hay RPC)
# ------------------------------------------------------------------------------------------------
def security(rpc, mint, mc, liq):
    import pump_discovery as pdsc
    import scam_filter as sf
    risks, hard = [], []
    tax = None
    if rpc is not None:
        acct = pdsc.get_multiple(rpc, [mint], "jsonParsed").get(mint)
        mi = pdsc.mint_info(acct, pdsc.DEFAULTS)
        hard += sf.hard_checks(mi)
        tax = mi.get("tax")
        try:
            import moonshot as ms
            supply = int(acct["data"]["parsed"]["info"]["supply"]) / 10 ** int(acct["data"]["parsed"]["info"]["decimals"])
            ds = ms.distribution(rpc, mint, supply)
            if ds and (ds["top10"] > 0.30 or ds["max_wallet"] > 0.05):
                risks.append(f"concentración: top10 {ds['top10']:.0%}, wallet máx {ds['max_wallet']:.1%}")
        except (KeyError, TypeError, ValueError, RuntimeError):
            risks.append("concentración: no pude leerla")
    else:
        risks.append("seguridad on-chain no comprobada (sin RPC)")
    if mc and liq is not None and liq < CFG["liq_min_frac"] * mc:
        risks.append(f"liquidez {liq / mc:.0%} del MC")
    if tax:
        who = "nadie (fijo)" if not tax["config_authority"] else ("launchpad conocido" if tax["known_authority"] else tax["config_authority"][:6] + "…")
        risks.append(f"impuesto {tax['pct']:g}% · lo puede cambiar: {who} · cobra: "
                     f"{(tax['withdraw_authority'] or '—')[:6]}… → revisar a dónde va y si esa wallet vende")
    return hard, risks, tax


# ------------------------------------------------------------------------------------------------
# 4. TELEGRAM CALL TRACKER
# ------------------------------------------------------------------------------------------------
def parse_channel(page_html):
    """Mensajes de la vista pública t.me/s/<canal>: [(post_id, ts, texto)]."""
    out = []
    for m in re.finditer(r'data-post="([^"]+)".*?<time[^>]*datetime="([^"]+)"', page_html or "", re.S):
        post, when = m.group(1), m.group(2)
        start = m.start()
        nxt = page_html.find('data-post="', m.end())
        block = page_html[start: nxt if nxt > 0 else len(page_html)]
        tm = re.search(r'tgme_widget_message_text[^>]*>(.*?)</div>', block, re.S)
        text = htmlmod.unescape(re.sub(r"<[^>]+>", " ", tm.group(1))) if tm else ""
        links = " ".join(re.findall(r'href="([^"]+)"', block))
        try:
            ts = int(datetime.fromisoformat(when.replace("Z", "+00:00")).timestamp())
        except ValueError:
            continue
        out.append((post, ts, text + " " + links))
    return out


def gecko_candles(http, chain, pool, tf, before=None, limit=1000):
    p = {"aggregate": 1, "limit": limit, "currency": "usd", "token": "base"}
    if before:
        p["before_timestamp"] = int(before)
    j = http.json(f"https://api.geckoterminal.com/api/v2/networks/{CHAINS[chain]['gecko']}/pools/{pool}/ohlcv/{tf}", p)
    rows = ((j or {}).get("data") or {}).get("attributes", {}).get("ohlcv_list") or []
    return sorted(rows, key=lambda r: r[0])          # [ts, o, h, l, c, v]


def mc_at(http, chain, c, d, ts):
    """MC en el minuto `ts` usando velas de 1 min: precio histórico × (MC actual / precio actual)."""
    if not d.get("pair") or not d.get("price") or not d.get("mc"):
        return None
    k = float(d["mc"]) / float(d["price"])
    rows = gecko_candles(http, chain, d["pair"], "minute", before=ts + 60, limit=90)
    rows = [r for r in rows if r[0] <= ts]
    if not rows:
        return None
    at = rows[-1]
    out = {"mc_at_call": at[4] * k, "call_mc_source": "velas 1 min (GeckoTerminal)"}
    for lab, mins in (("mc_m30", 30), ("mc_m15", 15), ("mc_m5", 5), ("mc_m60", 60)):
        before = [r for r in rows if r[0] <= ts - mins * 60]
        if before and before[-1][0] >= ts - (mins + 5) * 60:
            out[lab] = before[-1][4] * k
    for lab, mins in (("runup_15", 15), ("runup_5", 5)):
        b = out.get(f"mc_m{mins}")
        out[lab] = round((out["mc_at_call"] / b - 1) * 100, 1) if b else None
    if out.get("mc_m60"):
        out["chg1_before_call"] = round((out["mc_at_call"] / out["mc_m60"] - 1) * 100, 1)
    return out


def mc_after(http, chain, d, ts):
    """MC +1, +5, +15, +30 min tras la llamada (velas de 1 min). Se pide cuando ya han pasado ≥ 31 min."""
    if not d.get("pair") or not d.get("price") or not d.get("mc"):
        return None
    k = float(d["mc"]) / float(d["price"])
    rows = [r for r in gecko_candles(http, chain, d["pair"], "minute", before=ts + 31 * 60, limit=40) if r[0] >= ts]
    out = {}
    for lab, mins in (("mc_p1", 1), ("mc_p5", 5), ("mc_p15", 15), ("mc_p30", 30)):
        aft = [r for r in rows if r[0] <= ts + mins * 60]
        if aft and aft[-1][0] >= ts + (mins - 5) * 60:
            out[lab] = aft[-1][4] * k
    out["post_done"] = True
    return out


def track_calls(http, chain, channels, calls, T):
    """calls: {f"{canal}|{post}|{ca}": {...}} acumulado. Añade llamadas nuevas y actualiza seguimiento."""
    new = []
    for ch in channels:  # noqa: B007
        page = http.text(f"https://t.me/s/{ch}")
        if not page:
            continue
        for post, ts, text in parse_channel(page):
            for ca in dict.fromkeys(B58.findall(text)):
                key = f"{ch}|{post}|{ca}"
                if key not in calls and T - ts < 6 * 3600:          # solo llamadas recientes (MC "al publicar" fiable)
                    calls[key] = {"source": ch, "post": post, "timestamp": ts, "ca": ca}
                    new.append(key)
    mark_origins(calls)
    todo = [k for k, c in calls.items() if T - c["timestamp"] < 30 * 86400]
    ds = dexscreener(http, chain, [calls[k]["ca"] for k in todo])
    for k in todo:
        c, d = calls[k], ds.get(calls[k]["ca"])
        if not d or not d.get("mc"):
            continue
        mc = float(d["mc"])
        age = T - c["timestamp"]
        if "mc_first_seen" not in c:
            # lo que vemos al detectar el mensaje (puede ser hasta ~30 min después de publicarse)
            c.update(mc_first_seen=mc, detection_lag_min=round(age / 60), chg1_first_seen=d.get("chg1"),
                     chg6_first_seen=d.get("chg6"), symbol=d.get("symbol"), pair=d.get("pair"))
            try:
                c.update(mc_at(http, chain, c, d, c["timestamp"]) or {})
            except Exception:  # noqa: BLE001  (sin velas: nos quedamos con la primera observación, etiquetada)
                pass
        if age >= 31 * 60 and not c.get("post_done") and c.get("mc_at_call"):
            try:
                c.update(mc_after(http, chain, d, c["timestamp"]) or {})
            except Exception:  # noqa: BLE001
                pass
        if age >= 3600 and "mc_1h" not in c:
            c["mc_1h"] = mc
        if age >= 6 * 3600 and "mc_6h" not in c:
            c["mc_6h"] = mc
        c["ath_observed_mc"] = max(c.get("ath_observed_mc", 0), mc)
        c["last_mc"] = mc
        c["max_drawdown_observed"] = round(min(c.get("max_drawdown_observed", 0.0), mc / c["ath_observed_mc"] - 1) * 100, 1)
        # ATH real desde la llamada con velas de 1 h (máximo de cada hora), como mucho cada 6 h por llamada
        if c.get("pair") and d.get("price") and T - c.get("ath_candles_at", 0) >= 6 * 3600:
            try:
                k = mc / float(d["price"])
                rows = [r for r in gecko_candles(http, chain, c["pair"], "hour", limit=720) if r[0] >= c["timestamp"] - 3600]
                if rows:
                    c["ath_mc"] = max(r[2] for r in rows) * k
                    peak_i = max(range(len(rows)), key=lambda i: rows[i][2])
                    # dentro de la vela del máximo no sabemos si el mínimo fue antes o después: usamos su cierre
                    low_after = min([rows[peak_i][4]] + [r[3] for r in rows[peak_i + 1:]])
                    c["max_drawdown"] = round((low_after / rows[peak_i][2] - 1) * 100, 1)
                    c["ath_candles_at"] = T
            except Exception:  # noqa: BLE001
                pass
    return new


def mark_origins(calls):
    """Misma CA en varios canales: la primera es el ORIGEN, las demás son ECOS (no cuentan como señales independientes)."""
    by_ca = {}
    for k, c in calls.items():
        by_ca.setdefault(c["ca"], []).append((c["timestamp"], k))
    for ca, lst in by_ca.items():
        lst.sort()
        origin_key = lst[0][1]
        for i, (ts, k) in enumerate(lst):
            calls[k]["origin"] = i == 0
            calls[k]["echo_of"] = None if i == 0 else calls[origin_key]["source"]
            calls[k]["echo_delay_s"] = None if i == 0 else ts - lst[0][0]
        calls[origin_key]["echoes"] = len(lst) - 1


def call_stats(calls):
    by = {}
    for c in calls.values():
        if "mc_first_seen" in c and c.get("origin", True):       # solo llamadas ORIGEN (los ecos no son independientes)
            by.setdefault(c["source"], []).append(c)
    out = {}
    for src, cs in by.items():
        base = lambda c: c.get("mc_at_call") or c["mc_first_seen"]  # noqa: E731
        x = [(c.get("ath_mc") or c["ath_observed_mc"]) / base(c) for c in cs]
        pre = [c for c in cs if c.get("chg1_before_call") is not None]
        ru = [c["runup_15"] for c in cs if c.get("runup_15") is not None]
        out[src] = {"n": len(cs), "n_exact": sum(1 for c in cs if c.get("mc_at_call")),
                    "mc_med": sorted(base(c) for c in cs)[len(cs) // 2],
                    "x2": sum(v >= 2 for v in x) / len(x), "x5": sum(v >= 5 for v in x) / len(x),
                    "x10": sum(v >= 10 for v in x) / len(x),
                    "pumped_before": (sum((c["chg1_before_call"] or 0) > 30 for c in pre) / len(pre)) if pre else None,
                    "lag_med": sorted(c["detection_lag_min"] for c in cs)[len(cs) // 2],
                    "runup15_med": sorted(ru)[len(ru) // 2] if ru else None,
                    "echoes": sum(c.get("echoes", 0) for c in cs)}
    return out


# ------------------------------------------------------------------------------------------------
# Informe + registro
# ------------------------------------------------------------------------------------------------
def _usd(x):
    if x is None:
        return "—"
    return f"${x/1e6:.2f}M" if x >= 1e6 else f"${x/1e3:.1f}k" if x >= 1e3 else f"${x:.0f}"


def _pct(a, b):
    if not b:
        return "nuevo" if a else "—"
    return f"{(a / b - 1):+.0%}"


def report(T, metas, flywheel, calls, out_md, notes):
    L = ["# SCAN C — Meta / Flywheel", f"**{datetime.fromtimestamp(T, timezone.utc):%Y-%m-%d %H:%M} UTC** · "
         "cambios estructurales de días/semanas · nunca es orden de compra: la entrada la decides tú", ""]
    L += [f"> {n}" for n in notes] + ([""] if notes else [])
    act = [m for m in metas if m["active"]]
    L += [f"## Metas por token de pago ({len(act)} activándose)", ""]
    if not metas:
        L.append("_Sin datos de pools nuevos todavía._")
    for m in metas[:10]:
        st = m.get("state") or ("🟡 META ACTIVÁNDOSE" if m["active"] else "⚪ en observación")
        L += [f"### {st} — {m['symbol'] or m['quote'][:6]}",
              f"- **Quote:** `{m['quote']}`",
              f"- **Pools nuevos:** 1h {m['n1h']} (antes {m['n1h_prev']}) · 6h {m['n6h']} (antes {m['n6h_prev']}, {_pct(m['n6h'], m['n6h_prev'])}) · "
              f"24h {m['n24h']} (antes {m['n24h_prev']}, {_pct(m['n24h'], m['n24h_prev'])})"]
        b = m.get("breadth")
        if b:
            tv = "—" if b["top_vol_share"] is None else f"{b['top_vol_share']:.0%}"
            L.append(f"- **Amplitud (24h):** {b['tokens']} tokens distintos · {b['over_100k']} superan $100k · {b['over_1m']} superan $1M · "
                     f"el mayor = {tv} del volumen" + (" ⚠️ una sola moneda domina: puede no ser una moda" if b["top_vol_share"] and b["top_vol_share"] > 0.8 else ""))
        q = m.get("quote_info")
        if q:
            L.append(f"- **Token de pago:** MC {_usd(q.get('mc'))} · volumen 24h {_usd(q.get('vol24'))} · liquidez {_usd(q.get('liq'))}")
        for k, lab in (("volumen", "más volumen"), ("mayor_subida_24h", "mayor subida 24h"), ("primero_1M", "primero en $1M")):
            ld = (m.get("leaders") or {}).get(k)
            if ld:
                L.append(f"- **Líder ({lab}):** {ld.get('symbol')} `{ld['address']}` · MC {_usd(ld.get('mc'))} · "
                         f"vol 24h {_usd(ld.get('vol24'))} · 24h {ld.get('chg24')}%")
        if m.get("catalyst"):
            L.append(f"- **Catalizador:** {m['catalyst']}")
        if m.get("risks"):
            L.append("- **Riesgos:** " + "; ".join(m["risks"]))
        if m.get("hard"):
            L.append("- **Descartado por seguridad:** " + "; ".join(m["hard"]))
        L.append("")
    L += ["## Plataformas con ingresos acelerando (DefiLlama)", ""]
    if not flywheel:
        L.append("_Ninguna plataforma con ingresos 7d ≥ $50k que se hayan multiplicado ×2 o más._")
    for r in flywheel[:10]:
        st = r.get("state") or "🟡 FLYWHEEL ACELERANDO"
        acc = "nuevo" if r["rev_accel"] == float("inf") else f"{r['rev_accel']:.1f}×"
        L += [f"### {st} — {r['name']} ({r.get('category') or '—'})",
              f"- **Ingresos 7d:** {_usd(r.get('rev_7d'))} · 7d anteriores {_usd(r.get('rev_prev7d'))} · cambio {acc}",
              f"- **Ingresos 24h:** {_usd(r.get('rev_24h'))} · 24h anteriores {_usd(r.get('rev_prev24h'))} · "
              f"{_pct(r.get('rev_24h') or 0, r.get('rev_prev24h'))} (¿sigue acelerando hoy?)",
              f"- **A holders (recompras/quemas/repartos) 7d:** {_usd(r.get('hold_7d'))}"]
        tk = r.get("token")
        if tk:
            L.append(f"- **Token:** {(tk.get('symbol') or '').upper()} · MC {_usd(tk.get('mc'))} · FDV {_usd(tk.get('fdv'))}"
                     + (f" · liquidez {_usd(tk.get('liq'))}" if tk.get("liq") else "")
                     + (" · en ventana $0,5M–$5M" if r.get("in_window") else "")
                     + (f" · `{tk['address']}`" if tk.get("address") else ""))
            if r.get("risks"):
                L.append("- **Riesgos:** " + "; ".join(r["risks"]))
            if r.get("hard"):
                L.append("- **Descartado por seguridad:** " + "; ".join(r["hard"]))
        else:
            L.append("- **Token:** sin token listado en CoinGecko")
        L.append("")
    L += ["## Llamadas de Telegram (registro hacia delante)", ""]
    st = call_stats(calls)
    if not st:
        L.append("_Aún sin llamadas registradas (o el canal no tiene vista pública)._")
    else:
        L += ["| Canal | Llamadas origen | con MC exacto | MC mediano en la llamada | Máx. ≥2x | ≥5x | ≥10x | Subía >30% la hora antes | "
              "Subida mediana 15 min antes | Ecos en otros canales | Retraso de detección (mediana) |",
              "|---|---|---|---|---|---|---|---|---|---|---|"]
        for src, s in st.items():
            pb = "—" if s["pumped_before"] is None else f"{s['pumped_before']:.0%}"
            ru = "—" if s["runup15_med"] is None else f"{s['runup15_med']:+.0f}%"
            L.append(f"| {src} | {s['n']} | {s['n_exact']} | {_usd(s['mc_med'])} | {s['x2']:.0%} | {s['x5']:.0%} | {s['x10']:.0%} | "
                     f"{pb} | {ru} | {s['echoes']} | {s['lag_med']} min |")
        recent = sorted((c for c in calls.values() if "mc_first_seen" in c), key=lambda c: -c["timestamp"])[:10]
        L += ["", "| Publicada (UTC) | Canal | Moneda | −15 min | −5 min | MC en la llamada | +5 min | +30 min | MC al detectarla (retraso) | +1h | +6h | Máximo | Caída tras el máximo |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        for c in recent:
            exact = _usd(c["mc_at_call"]) + " ✓" if c.get("mc_at_call") else "— (sin velas)"
            ath = (_usd(c["ath_mc"]) + " (velas 1h)") if c.get("ath_mc") else (_usd(c.get("ath_observed_mc")) + " (observado)")
            dd = c.get("max_drawdown", c.get("max_drawdown_observed", 0))
            src = c["source"] + (f" (eco de {c['echo_of']}, +{c['echo_delay_s']}s)" if c.get("echo_of") else "")
            L.append(f"| {datetime.fromtimestamp(c['timestamp'], timezone.utc):%m-%d %H:%M} | {src} | "
                     f"[{c.get('symbol') or c['ca'][:6]}](https://dexscreener.com/solana/{c['ca']}) | {_usd(c.get('mc_m15'))} | "
                     f"{_usd(c.get('mc_m5'))} | {exact} | {_usd(c.get('mc_p5'))} | {_usd(c.get('mc_p30'))} | "
                     f"{_usd(c['mc_first_seen'])} ({c['detection_lag_min']} min) | {_usd(c.get('mc_1h'))} | {_usd(c.get('mc_6h'))} | {ath} | {dd}% |")
        L += ["", "_✓ = MC exacto en el minuto de la llamada (velas de 1 min). Sin velas, solo hay la primera observación del scanner "
              "(hasta ~30 min después): no se usa como \"MC en la llamada\". Máximo \"(velas 1h)\" = máximo real de cada hora; "
              "\"(observado)\" = solo lo visto en las pasadas, puede quedarse corto. \"Subía la hora antes\" solo se calcula con velas._"]
    L += ["", "---", "🟡 = algo estructural se está activando · 🟢 CANDIDATA = además el líder pasa seguridad (sin crear/congelar tokens, "
          "impuesto fijo o nulo), liquidez y concentración, y su MC está entre $0,5M y $5M · la entrada la decides tú."]
    Path(out_md).write_text("\n".join(L) + "\n", encoding="utf-8")


def run(http, rpc=None, T=None, data_dir=None, out_md=None, log=print):
    T = int(T or time.time())
    d = Path(data_dir or DATA)
    d.mkdir(parents=True, exist_ok=True)
    chain = CFG["chain"]
    reg_f, calls_f, sig_f = d / "pools.json", d / "calls.json", d / "signals.jsonl"
    registry = json.loads(reg_f.read_text()) if reg_f.exists() else {}
    calls = json.loads(calls_f.read_text()) if calls_f.exists() else {}
    notes = []
    # 2. metas
    try:
        for p in fetch_new_pools(http, chain, CFG["gecko_pages"]):
            if p["pool"]:
                registry.setdefault(p["pool"], p)
    except Exception as e:  # noqa: BLE001
        notes.append(f"GeckoTerminal no disponible: {str(e)[:120]}")
    registry = {k: v for k, v in registry.items() if v["ts"] > T - CFG["keep_days"] * 86400}
    span_h = (T - min((p["ts"] for p in registry.values()), default=T)) / 3600
    if span_h < 48:
        notes.append(f"Llevo {span_h:.0f} h acumulando pools: las comparaciones 24h vs 24h anteriores son fiables a partir de 48 h.")
    metas = meta_acceleration(registry, T)
    # 3. líderes de las metas activas (+ datos del token de pago)
    act = [m for m in metas if m["active"]][:5]
    addrs = [p["base"] for m in act for p in m["pools"]] + [m["quote"] for m in act]
    ds = {}
    try:
        ds = dexscreener(http, chain, addrs)
    except Exception as e:  # noqa: BLE001
        notes.append(f"DexScreener no disponible: {str(e)[:120]}")
    for m in act:
        recent_bases = {p["base"] for p in m["pools"] if p["ts"] > T - 86400}
        vols = sorted(((ds.get(b) or {}).get("vol24") or 0 for b in recent_bases), reverse=True)
        m["breadth"] = {"tokens": len(recent_bases),
                        "over_100k": sum(1 for b in recent_bases if ((ds.get(b) or {}).get("mc") or 0) >= 100_000),
                        "over_1m": sum(1 for b in recent_bases if ((ds.get(b) or {}).get("mc") or 0) >= 1_000_000),
                        "top_vol_share": (vols[0] / sum(vols)) if vols and sum(vols) else None}
        m["leaders"] = leaders(m, ds)
        m["quote_info"] = ds.get(m["quote"])
        m["catalyst"] = f"META ACCELERATION (pools 24h {_pct(m['n24h'], m['n24h_prev'])})"
        cand = (m["leaders"] or {}).get("volumen") or m["quote_info"]
        m["state"] = "🟡 META ACTIVÁNDOSE"
        if cand:
            addr = cand.get("address") or m["quote"]
            try:
                hard, risks, tax = security(rpc, addr, cand.get("mc"), cand.get("liq"))
            except Exception as e:  # noqa: BLE001
                hard, risks, tax = [], [f"seguridad: error {str(e)[:80]}"], None
            m["hard"], m["risks"] = hard, risks
            in_win = CFG["mc_min"] <= (cand.get("mc") or 0) <= CFG["mc_max"]
            if not hard and in_win and rpc is not None and not any(r.startswith(("liquidez", "concentración", "seguridad"))
                                                                    for r in risks):
                m["state"] = "🟢 CANDIDATA"
    # 1. flywheel
    fly = []
    try:
        fly = revenue_engine(http, chain)
        mcs = token_mcaps(http, [r.get("gecko_id") for r in fly])
        for r in fly:
            r["token"] = mcs.get(r.get("gecko_id"))
            r["in_window"] = bool(r["token"] and r["token"].get("mc") and CFG["mc_min"] <= r["token"]["mc"] <= CFG["mc_max"])
            r["state"] = "🟡 FLYWHEEL ACELERANDO"
            if not r["in_window"]:
                continue
            # token -> contrato en esta cadena -> liquidez -> seguridad + concentración -> solo entonces 🟢
            addr = token_address(http, r.get("gecko_id"), chain)
            r["token"]["address"] = addr
            if not addr:
                r["risks"] = ["no encuentro el contrato del token en esta cadena: seguridad sin comprobar"]
                continue
            dd = dexscreener(http, chain, [addr]).get(addr) or {}
            try:
                hard, risks, tax = security(rpc, addr, r["token"].get("mc"), dd.get("liq"))
            except Exception as e:  # noqa: BLE001
                hard, risks = [], [f"seguridad: error {str(e)[:80]}"]
            r["hard"], r["risks"], r["token"]["liq"] = hard, risks, dd.get("liq")
            if not hard and rpc is not None and dd.get("liq") and not any(x.startswith(("liquidez", "concentración", "seguridad"))
                                                                     for x in risks):
                r["state"] = "🟢 CANDIDATA"
    except Exception as e:  # noqa: BLE001
        notes.append(f"DefiLlama no disponible: {str(e)[:120]}")
    # 4. llamadas
    try:
        new_calls = track_calls(http, chain, CFG["telegram_channels"], calls, T)
    except Exception as e:  # noqa: BLE001
        new_calls = []
        notes.append(f"Telegram no disponible: {str(e)[:120]}")
    # registro hacia delante (solo señales nuevas de esta pasada)
    with open(sig_f, "a", encoding="utf-8") as fh:
        for m in act:
            fh.write(json.dumps({"T": T, "type": "meta", "state": m["state"], "quote": m["quote"], "symbol": m["symbol"],
                                 "n24h": m["n24h"], "n24h_prev": m["n24h_prev"], "breadth": m.get("breadth"),
                                 "leaders": {k: (v or {}).get("address") for k, v in (m.get("leaders") or {}).items()},
                                 "leader_mc": ((m.get("leaders") or {}).get("volumen") or {}).get("mc"),
                                 "risks": m.get("risks"), "hard": m.get("hard")}, default=str) + "\n")
        for r in fly:
            fh.write(json.dumps({"T": T, "type": "flywheel", "state": r["state"], "name": r["name"], "slug": r.get("slug"),
                                 "rev_7d": r.get("rev_7d"), "rev_prev7d": r.get("rev_prev7d"),
                                 "token_mc": (r.get("token") or {}).get("mc"), "token": (r.get("token") or {}).get("address"),
                                 "risks": r.get("risks"), "hard": r.get("hard")}, default=str) + "\n")
        for k in new_calls:
            fh.write(json.dumps({"T": T, "type": "call", **calls[k]}, default=str) + "\n")
    reg_f.write_text(json.dumps(registry))
    calls_f.write_text(json.dumps(calls, indent=0))
    out = Path(out_md or HERE / "report" / "SCAN_C.md")
    out.parent.mkdir(exist_ok=True)
    report(T, metas, fly, calls, out, notes)
    try:                                     # seguimiento de TODAS las decisiones (A, B, C), incluidas las descartadas
        import outcomes
        outcomes.update(http, T, base=d.parent, store=d / "outcomes.json", log=log)
    except Exception as e:  # noqa: BLE001
        log(f"outcomes: {str(e)[:120]}")
    log(f"SCAN C: {len(registry)} pools en registro · {len(act)} metas activas · {len(fly)} plataformas acelerando · "
        f"{len(new_calls)} llamadas nuevas")
    return {"metas": metas, "flywheel": fly, "calls": calls, "notes": notes}


def main():
    rpc = None
    try:
        import moonshot as ms
        cfg = ms.load_config(interactive=False)
        rpc = ms.tf.RPC(cfg["rpc_url"], min_interval=0.1)
    except SystemExit:
        pass
    run(Http(1.2), rpc)


if __name__ == "__main__":
    main()
