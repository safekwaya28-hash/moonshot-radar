#!/usr/bin/env python3
"""
SCAN B — DESPEGUES (objetivo 100x+): monedas de pump.fun recién creadas, en la ventana $8k–$40k.

Dos velocidades (para no gastar créditos de Helius en miles de monedas):
  RÁPIDA  (todas): las ~5.000 creaciones más recientes (API DAS de Helius) -> estado de su bonding curve en lotes de 100
           -> quedan las que están en $8k–$40k y no han graduado; se guarda su MC para medir la aceleración.
  PROFUNDA (las K mejores): operaciones de la curva -> compradores, aceleración, presión, retención, wallet dominante,
           snipers, compras en el bloque de creación, prueba de venta, dev, distribución, smart money.

Resultado en report/SCAN_B.md:  🟢 COMPRA AHORA · 🟡 WATCH (siempre el top, para tu análisis técnico) · 🔴 DESCARTAR.
Todo se guarda en scan_b_log.jsonl para calibrar después qué combinación precede a los 50x-100x.
Umbrales PROVISIONALES: se calibran con el registro.
"""
from __future__ import annotations

import json
import math
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import moonshot as ms  # noqa: E402
import pump_discovery as pdsc  # noqa: E402
import scam_filter as sf  # noqa: E402

STATE = HERE / ".moonshot" / "scan_b_state.json"
LOG = HERE / "scan_b_log.jsonl"

R = {
    "mc_min": 8_000, "mc_max": 40_000, "max_age_h": 6,
    "das_pages": 5,              # 5 x 1000 creaciones más recientes
    "deep_k": 5,                 # monedas con análisis profundo por ejecución
    "recent_tx": 100,            # operaciones recientes que se leen por moneda
    "early_tx": 15,              # primeras operaciones (snipers / bloque de creación)
    # --- A: seguridad (si falla -> DESCARTAR)
    "snipers_max": 15, "bundle_max": 0.20, "top10_max": 0.30, "wallet_max": 0.05, "dev_hold_max": 0.10,
    "dev_sold_max": 0.50, "wash_top5_max": 0.50,
    # --- B / M
    "buyers_30m": 80, "ratio_min": 1.5, "median_buy_lo": 20, "median_buy_hi": 200, "dominant_max": 0.20,
    "hr_min": 0.80, "sell_proof_min": 3, "sell_hold_min": 5, "funding_check": 6, "coverage_min": 25,
    "buy_b": 6, "buy_m": 4,
}


# ------------------------------------------------------------------------------------------
# Vía rápida
# ------------------------------------------------------------------------------------------
def recent_mints(rpc, pages):
    """Creaciones más recientes de pump.fun (DAS de Helius, autoridad = cuenta de mint de pump)."""
    out = []
    for page in range(1, pages + 1):
        res = rpc.call("getAssetsByAuthority", {"authorityAddress": pdsc.PUMP_MINT_AUTHORITY, "page": page, "limit": 1000,
                                                 "sortBy": {"sortBy": "created", "sortDirection": "desc"}})
        items = (res or {}).get("items") or []
        out += [it["id"] for it in items if it.get("id")]
        if len(items) < 1000:
            break
    return out


def fast_path(rpc, mints, sol_usd):
    curves = {m: ms.pump_curve_address(m) for m in mints}
    accts = pdsc.get_multiple(rpc, list(curves.values()), "base64")
    out = []
    for m, c in curves.items():
        st = pdsc.decode_curve(accts.get(c), pdsc.DEFAULTS)
        if not st or st["complete"] or not st.get("mc_sol"):
            continue
        mc = st["mc_sol"] * sol_usd
        out.append({"mint": m, "curve": c, "mc": mc, "progress": st["progress"], "real_sol": st["real_sol"]})
    return out


# ------------------------------------------------------------------------------------------
# Vía profunda
# ------------------------------------------------------------------------------------------
def curve_trades(rpc, store, curve, mint, sol_usd, n_recent, n_early):
    """Operaciones de la curva: (recientes, primeras, t_creación, total_firmas_vistas)."""
    sigs, before = [], None
    for _ in range(3):
        p = {"limit": 1000}
        if before:
            p["before"] = before
        page = rpc.call("getSignaturesForAddress", [curve, p]) or []
        sigs += [s for s in page if s.get("err") is None]
        if len(page) < 1000:
            break
        before = page[-1]["signature"]
    complete_history = len(sigs) < 3000

    def parse(slist):
        tr = []
        for s in slist:
            tx = store.get(rpc, s["signature"])
            if not tx:
                continue
            signer = ms.tf._keys(tx)[0]
            t = ms.parse_wallet_trade(tx, signer, s["signature"], sol_usd)
            if t and t["mint"] == mint:
                t["slot"] = tx.get("slot")
                t["usd"] = t.get("usd") if t.get("usd") is not None else (t["sol"] or 0) * sol_usd
                tr.append(t)
        return tr
    recent = parse(sigs[:n_recent])
    early = parse(list(reversed(sigs[-n_early:]))) if complete_history else []
    t0 = sigs[-1].get("blockTime") if (sigs and complete_history) else None
    slot0 = sigs[-1].get("slot") if (sigs and complete_history) else None
    return recent, early, t0, slot0, len(sigs)


def funder_of(rpc, store, wallet):
    """Quién financió la wallet: en su transacción MÁS ANTIGUA, la cuenta que más SOL perdió (≠ la propia wallet).
    Solo para wallets con < 1000 transacciones (las 'nuevas', que son las que se usan para bundles)."""
    sigs = rpc.call("getSignaturesForAddress", [wallet, {"limit": 1000}]) or []
    if len(sigs) >= 1000:
        return f"veterana:{wallet}"          # ≥1000 operaciones: no es una wallet recién creada para un bundle -> independiente
    if not sigs:
        return None
    tx = store.get(rpc, sigs[-1]["signature"])
    if not tx or not tx.get("meta"):
        return None
    keys = ms.tf._keys(tx)
    pre, post = tx["meta"].get("preBalances") or [], tx["meta"].get("postBalances") or []
    best, drop = None, 0
    for i, k in enumerate(keys):
        if k == wallet or i >= len(pre) or i >= len(post):
            continue
        d = pre[i] - post[i]
        if d > drop:
            best, drop = k, d
    return best


def funding_clusters(rpc, store, wallets, shares=None, max_wallets=10):
    """Agrupa wallets por quien las financió (1 nivel). Devuelve (clusters, financiador por wallet)."""
    fund = {}
    for w in wallets[:max_wallets]:
        try:
            fund[w] = funder_of(rpc, store, w)
        except (RuntimeError, ValueError, KeyError):
            fund[w] = None
    groups = {}
    for w, f in fund.items():
        if f and not f.startswith("veterana:"):
            groups.setdefault(f, []).append(w)
    clusters = [{"funder": f, "wallets": ws, "share": sum((shares or {}).get(w, 0.0) for w in ws)}
                for f, ws in groups.items() if len(ws) >= 2]
    clusters.sort(key=lambda c: (-len(c["wallets"]), -c["share"]))
    return clusters, fund


def window(trades, t_from, t_to):
    return [t for t in trades if t_from < (t["ts"] or 0) <= t_to]


def analyse(rpc, store, cand, T, sol_usd, smart, prev_mc):
    m, curve = cand["mint"], cand["curve"]
    minfo = pdsc.get_multiple(rpc, [m], "jsonParsed").get(m)
    mi = pdsc.mint_info(minfo, pdsc.DEFAULTS)
    prog = (minfo or {}).get("owner") or pdsc.TOKEN_PROGRAM
    name, sym = ms.token_meta(minfo)
    recent, early, t0, slot0, nsig = curve_trades(rpc, store, curve, m, sol_usd, R["recent_tx"], R["early_tx"])
    age_h = (T - t0) / 3600 if t0 else None
    c = {"mint": m, "symbol": sym, "name": name, "mc": cand["mc"], "progress": cand["progress"], "age_h": age_h,
         "n_sigs": nsig, "hard": [], "warn": [], "manual": []}

    # ---------------- A · seguridad
    hard = sf.hard_checks(mi)                         # mint/freeze authority, extensiones peligrosas (PermanentDelegate, fees…)
    creator = None
    try:
        creator, _ = ms.pump_creator(rpc, m)
    except (RuntimeError, ValueError):
        pass
    if early and slot0 is not None:
        snipers = {t["wallet"] for t in early if t["side"] == "buy" and t.get("slot") is not None
                   and t["slot"] <= slot0 + 2 and t["wallet"] != creator}
        bundle = sum(t["tokens"] for t in early if t["side"] == "buy" and t.get("slot") == slot0
                     and t["wallet"] != creator) / pdsc.DEFAULTS["total_supply"]
        c.update(snipers=len(snipers), bundle=bundle)
        if len(snipers) >= R["snipers_max"]:
            hard.append(f"{len(snipers)} snipers en los 3 primeros bloques")
        if bundle >= R["bundle_max"]:
            hard.append(f"{bundle:.0%} del supply comprado en el bloque de creación")
    else:
        c["manual"].append("snipers/bundle: mucha actividad, míralo en GMGN")
    try:
        ds = ms.distribution(rpc, m, pdsc.DEFAULTS["total_supply"], exclude={curve})
    except (RuntimeError, ValueError):
        ds = None
    if ds:
        c.update(top10=ds["top10"], max_wallet=ds["max_wallet"])
        shares = dict(ds.get("holders") or [])
        try:
            cl, _ = funding_clusters(rpc, store, list(shares), shares, R["funding_check"])
        except (RuntimeError, ValueError):
            cl = []
        c["clusters"] = [{"funder": x["funder"], "n": len(x["wallets"]), "share": x["share"]} for x in cl]
        big = [x for x in cl if len(x["wallets"]) >= 3 or x["share"] >= 0.10]
        if big:
            c["warn"].append(f"cluster de financiación: {len(big[0]['wallets'])} holders del top financiados por "
                             f"{big[0]['funder'][:6]}… ({big[0]['share']:.0%} del supply)")
        if ds["top10"] > R["top10_max"] or ds["max_wallet"] > R["wallet_max"]:
            hard.append(f"concentración: top10 {ds['top10']:.0%}, wallet máx {ds['max_wallet']:.1%}")
    dev = None
    if creator:
        try:
            dev = ms.dev_activity(rpc, store, creator, m, prog, 1)
        except (RuntimeError, ValueError):
            dev = None
    if dev:
        held = max(0.0, dev["bought"] - dev["sold"] - dev["moved_out"]) / pdsc.DEFAULTS["total_supply"]
        sold_frac = (dev["sold"] + dev["moved_out"]) / dev["bought"] if dev["bought"] else 0.0
        c.update(dev=creator, dev_hold=held, dev_sold=sold_frac)
        if held > R["dev_hold_max"]:
            hard.append(f"dev tiene {held:.0%}")
        if sold_frac > R["dev_sold_max"]:
            hard.append(f"dev vendió/sacó {sold_frac:.0%} de su compra")
    else:
        c["manual"].append("dev: no identificado")
    vol = {}
    for t in recent:
        vol[t["wallet"]] = vol.get(t["wallet"], 0.0) + t["usd"]
    tot = sum(vol.values())
    top5 = sum(sorted(vol.values(), reverse=True)[:5]) / tot if tot else 0.0
    loops = sum(1 for w in vol if sum(1 for t in recent if t["wallet"] == w and t["side"] == "sell") >= 3
                and sum(1 for t in recent if t["wallet"] == w and t["side"] == "buy") >= 3)
    c.update(top5_vol=top5, loop_wallets=loops)
    if top5 > R["wash_top5_max"] and loops >= 2:
        hard.append(f"volumen en bucle: 5 wallets = {top5:.0%} y {loops} compran-venden repetidamente")
    first_buy = {}
    for t in sorted(recent + early, key=lambda t: t["ts"] or 0):
        if t["side"] == "buy":
            first_buy.setdefault(t["wallet"], t["ts"] or 0)
    sellers_ok = sorted({t["wallet"] for t in recent if t["side"] == "sell" and t["wallet"] != creator
                         and t["wallet"] in first_buy and (t["ts"] or 0) - first_buy[t["wallet"]] >= R["sell_hold_min"] * 60})
    c["sell_proof_raw"] = len(sellers_ok)
    try:
        _, fund = funding_clusters(rpc, store, sellers_ok, None, R["funding_check"])
    except (RuntimeError, ValueError):
        fund = {}
    seen_f, indep, unknown = set(), 0, 0
    for w in sellers_ok:
        f = fund.get(w)
        if f is None:                              # no verificable (sin datos o no consultada): NO cuenta
            unknown += 1
        elif f not in seen_f:                      # financiador verificado y distinto: cuenta
            indep += 1
            seen_f.add(f)
    c["sell_proof"] = indep
    c["sell_proof_unverified"] = unknown
    c["hard"] = hard

    # ---------------- momento
    def buyers(ts_from, ts_to):
        return {t["wallet"] for t in window(recent, ts_from, ts_to) if t["side"] == "buy"}
    def sellers(ts_from, ts_to):
        return {t["wallet"] for t in window(recent, ts_from, ts_to) if t["side"] == "sell"}
    first_seen = {}
    for t in sorted(recent + early, key=lambda t: t["ts"] or 0):
        if t["side"] == "buy":
            first_seen.setdefault(t["wallet"], t["ts"])
    new = lambda a, b: sum(1 for w, ts in first_seen.items() if a < (ts or 0) <= b)  # noqa: E731
    covered_from = min((t["ts"] for t in recent), default=T)
    n5, n5p = new(T - 300, T), new(T - 600, T - 300)
    bai = n5 / n5p if n5p else (float("inf") if n5 else 0.0)
    b15, s15 = buyers(T - 900, T), sellers(T - 900, T)
    ratio = len(b15) / len(s15) if s15 else (float("inf") if b15 else 0.0)
    v15 = sum(t["usd"] for t in window(recent, T - 900, T))
    v15p = sum(t["usd"] for t in window(recent, T - 1800, T - 900))
    w15 = {}
    for t in window(recent, T - 900, T):
        w15[t["wallet"]] = w15.get(t["wallet"], 0.0) + t["usd"]
    dominant = max(w15.values()) / v15 if v15 else 0.0
    cohort = buyers(T - 1800, T - 900)
    hr = 1 - len(cohort & sellers(T - 900, T)) / len(cohort) if cohort else None
    buys_usd = [t["usd"] for t in recent if t["side"] == "buy"]
    med_buy = statistics.median(buys_usd) if buys_usd else None
    b30 = len(buyers(T - 1800, T))
    mc_prev = prev_mc.get(m)
    w30 = window(recent, T - 1800, T)
    act30 = {t["wallet"] for t in w30}
    nb = {w for w in act30 if T - 1800 < (first_buy.get(w) or 0) <= T}
    buys_by = {}
    for t in w30:
        if t["side"] == "buy":
            buys_by[t["wallet"]] = buys_by.get(t["wallet"], 0) + 1
    flippers = {w for w in act30 if any(t["wallet"] == w and t["side"] == "buy" for t in w30)
                and any(t["wallet"] == w and t["side"] == "sell" for t in w30)}
    liq = cand.get("real_sol", 0) * sol_usd
    c.update(new_buyers30=len(nb), repeat_buyers30=sum(1 for v in buys_by.values() if v >= 2),
             flipper_ratio=len(flippers) / len(act30) if act30 else None,
             liq_usd=liq, vol15_liq=(sum(t["usd"] for t in window(recent, T - 900, T)) / liq) if liq else None)
    c.update(bai=bai, new5=n5, new5_prev=n5p, ratio15=ratio, vol15=v15, vol15_prev=v15p, dominant=dominant, hr15=hr,
             median_buy=med_buy, buyers30=b30, mc_prev=mc_prev,
             window_min=round((T - covered_from) / 60) if recent else 0)
    truncated = nsig > R["recent_tx"]
    c["coverage_min"] = c["window_min"] if truncated else (round(age_h * 60) if age_h else c["window_min"])

    # ---------------- smart money (tus wallets verificadas)
    sm = []
    for t in recent + early:
        w = smart.get(t["wallet"])
        if w and t["side"] == "buy":
            tier = "A" if str(w.get("meets_criteria")).lower() == "true" else "B"
            sm.append((tier, w.get("label") or t["wallet"][:6], t["usd"]))
    best = {}
    for tier, lab, usd in sm:
        best[lab] = min(best.get(lab, tier), tier)
    c["smart"] = sorted(best.items(), key=lambda x: x[1])
    sm_ts = sorted((t["ts"] or 0, t["wallet"]) for t in recent + early if t["side"] == "buy" and t["wallet"] in smart)
    conv = 0
    for i, (t0_, _) in enumerate(sm_ts):                 # máx. de smart wallets distintas en 10 min
        conv = max(conv, len({w for ts_, w in sm_ts[i:] if ts_ - t0_ <= 600}))
    order = [w for w, _ in sorted(first_buy.items(), key=lambda x: x[1])]
    c["smart_convergence"] = conv
    c["smart_rank"] = sorted(order.index(w) + 1 for w in {w for _, w in sm_ts} if w in order)
    # posición entre los compradores OBSERVADOS (primeras + últimas operaciones), no entre todos

    # ---------------- puntuaciones
    B = 0
    if any(t == "A" for _, t in c["smart"]):
        B += 3 if c["smart_convergence"] >= 2 else 2
    elif c["smart"]:
        B += 1
    B += b30 >= R["buyers_30m"]
    B += ratio >= R["ratio_min"]
    B += bool(med_buy and R["median_buy_lo"] <= med_buy <= R["median_buy_hi"])
    B += bai >= 1 and n5 > 0
    B += bool(mc_prev and cand["mc"] > 1.3 * mc_prev)
    B += bool(dev and c.get("dev_hold", 1) < 0.05 and c.get("dev_sold", 1) == 0)
    M = 0
    M += bai > 1
    M += ratio >= R["ratio_min"]
    M += bool(hr is not None and hr >= R["hr_min"])
    M += v15 > v15p > 0 or (v15 > 0 and v15p == 0)
    M += bool(v15 and dominant < R["dominant_max"])
    c.update(B=int(B), M=int(M))
    c["manual"] += ["origen del dinero de los compradores (bundles/insiders en GMGN)", "narrativa (X/Telegram)"]

    # ---------------- decisión
    timing = R["mc_min"] <= cand["mc"] <= R["mc_max"] and (age_h is None or age_h <= R["max_age_h"])
    if hard:
        dec = "DESCARTAR"
    elif not timing:
        dec = "FUERA"
    elif (B >= R["buy_b"] and M >= R["buy_m"] and c["smart"] and c["sell_proof"] >= R["sell_proof_min"]
          and dominant < R["dominant_max"] and c["coverage_min"] >= R["coverage_min"]):
        dec = "COMPRA AHORA"
    else:
        dec = "WATCH"
        if not c["smart"]:
            c["warn"].append("sin smart money")
        if c["sell_proof"] < R["sell_proof_min"]:
            c["warn"].append(f"prueba de venta {c['sell_proof']}/3")
        if B < R["buy_b"]:
            c["warn"].append(f"B {B}/{R['buy_b']}")
        if M < R["buy_m"]:
            c["warn"].append(f"M {M}/{R['buy_m']}")
        if dominant >= R["dominant_max"]:
            c["warn"].append(f"una wallet = {dominant:.0%} del volumen 15m")
        if c["coverage_min"] < R["coverage_min"]:
            c["warn"].append(f"datos incompletos: solo {c['coverage_min']} min observados (las métricas de 30 min no son fiables)")
    c["decision"] = dec
    return c


# ------------------------------------------------------------------------------------------
# Informe
# ------------------------------------------------------------------------------------------
def _f(x, fmt):
    if x is None:
        return "—"
    if isinstance(x, float) and math.isinf(x):
        return "∞"
    return format(x, fmt)


def card(c):
    m = c["mint"]
    sm = ", ".join(f"{lab} ({t})" for lab, t in c["smart"]) or "ninguna de tus wallets"
    L = [f"### {c['decision_icon']} {c['decision']} — ${c.get('symbol') or m[:6]}",
         f"- **CA:** `{m}`",
         f"- **MC:** ${c['mc']/1e3:,.1f}k · curva {c['progress']:.0%} · edad {_f(c['age_h'], '.1f')} h"
         + (f" · hace 30 min: ${c['mc_prev']/1e3:,.1f}k" if c.get("mc_prev") else ""),
         f"- **Smart money:** {sm}",
         f"- **B:** {c['B']}/9 · **M:** {c['M']}/5",
         f"- **Compradores:** 30m {c['buyers30']} · nuevos 5m {c['new5']} (antes {c['new5_prev']}, BAI {_f(c['bai'], '.2f')}) · "
         f"compradores/vendedores 15m {_f(c['ratio15'], '.2f')}",
         f"- **Volumen 15m:** ${c['vol15']:,.0f} (antes ${c['vol15_prev']:,.0f}) · wallet dominante {c['dominant']:.0%} · "
         f"retención 15m {_f(c['hr15'], '.0%')} · compra mediana ${_f(c['median_buy'], ',.0f')}",
         f"- **Seguridad:** snipers {c.get('snipers', '—')} · bloque creación {_f(c.get('bundle'), '.0%')} · "
         f"top10 {_f(c.get('top10'), '.0%')} · wallet máx {_f(c.get('max_wallet'), '.1%')} · dev tiene {_f(c.get('dev_hold'), '.1%')}"
         f" · dev vendió {_f(c.get('dev_sold'), '.0%')} · 5 wallets = {c['top5_vol']:.0%} del volumen",
         f"- **Prueba de venta:** {c['sell_proof']}/3 con financiador verificado y distinto (no-dev, mantuvieron ≥5 min y vendieron; "
         f"{c.get('sell_proof_raw', 0)} en total, {c.get('sell_proof_unverified', 0)} no verificables)",
         f"- **Cobertura de datos:** {c.get('coverage_min')} min observados" + ("" if c.get("coverage_min", 0) >= R["coverage_min"] else " ⚠️ insuficiente"),
         f"- **Participantes 30m:** nuevos {c.get('new_buyers30')} · recompran {c.get('repeat_buyers30')} · "
         f"compran y venden (flippers) {_f(c.get('flipper_ratio'), '.0%')} · volumen 15m / liquidez {_f(c.get('vol15_liq'), '.1f')}×",
         f"- **Smart money:** convergencia {c.get('smart_convergence', 0)} wallets en 10 min · posición entre los compradores "
         f"{c.get('smart_rank') or '—'} (entre los compradores observados, no entre todos)",
         f"- **Financiación del top:** " + ("; ".join(f"{x['n']} holders ← {x['funder'][:6]}… ({x['share']:.0%})" for x in c.get('clusters') or [])
                                            or "sin grupos detectados (1 nivel, wallets nuevas)"),
         ]
    if c["hard"]:
        L.append(f"- **Descartada por:** {'; '.join(c['hard'])}")
    if c["warn"]:
        L.append(f"- **Falta para COMPRA AHORA:** {'; '.join(c['warn'])}")
    L.append(f"- **A mano:** {'; '.join(c['manual'])}")
    L.append(f"- [GMGN](https://gmgn.ai/sol/token/{m}) · [pump.fun](https://pump.fun/coin/{m}) · "
             f"[DexScreener](https://dexscreener.com/solana/{m}) · [Solscan](https://solscan.io/token/{m})")
    return "\n".join(L)


ICON = {"COMPRA AHORA": "🟢", "WATCH": "🟡", "DESCARTAR": "🔴", "FUERA": "⚪"}


def report(cards, T, n_seen, n_window, path):
    for c in cards:
        c["decision_icon"] = ICON[c["decision"]]
    order = {"COMPRA AHORA": 0, "WATCH": 1, "DESCARTAR": 2, "FUERA": 3}
    cards = sorted(cards, key=lambda c: (order[c["decision"]], -(c["B"] + c["M"]), -c["mc"]))
    cnt = {k: sum(c["decision"] == k for c in cards) for k in order}
    L = ["# SCAN B — Despegues (objetivo 100x+)",
         f"**{datetime.fromtimestamp(T, timezone.utc):%Y-%m-%d %H:%M} UTC** · {n_seen:,} creaciones recientes revisadas · "
         f"{n_window} en la ventana $8k–$40k · {len(cards)} con análisis profundo", "",
         " · ".join(f"{ICON[k]} {k} **{v}**" for k, v in cnt.items()), ""]
    if not cards:
        L.append("_Ninguna moneda en la ventana ahora mismo._")
    for c in cards:
        L += [card(c), ""]
    L += ["---", "**COMPRA AHORA** = seguridad OK + MC $8k–40k + edad < 6 h + B ≥ 6 + M ≥ 4 + smart money + prueba de venta ≥ 3 "
          "+ ninguna wallet > 20% del volumen 15m. **WATCH** = pasa seguridad y ventana, falta algo (se indica). "
          "Umbrales provisionales: se calibran con `scan_b_log.jsonl`.",
          "Tamaño de entrada pequeño; no vender antes de 10x; a 10x recuperar lo invertido; el resto corre."]
    Path(path).write_text("\n".join(L) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------------------------
def run(rpc, sol_usd, T=None, log=print, outdir=None, state_file=None, log_file=None, smart=None):
    T = int(T or time.time())
    state_file = Path(state_file or STATE)
    state = json.loads(state_file.read_text()) if state_file.exists() else {}
    prev_mc = state.get("mc", {})
    try:
        mints = recent_mints(rpc, R["das_pages"])
        src = "DAS"
    except Exception as e:  # noqa: BLE001
        log(f"DAS no disponible ({str(e)[:100]}); uso las creaciones más recientes (limitado)")
        created, _ = pdsc.discover(rpc, T - 3 * 3600, T, pdsc.DEFAULTS, max_new=300, log=False)
        mints, src = [x["mint"] for x in created], "creaciones"
    cands = fast_path(rpc, mints, sol_usd)
    inwin = [c for c in cands if R["mc_min"] * 0.8 <= c["mc"] <= R["mc_max"] * 1.2]
    for c in inwin:                                   # prioridad: aceleración desde la última pasada, luego MC
        p = prev_mc.get(c["mint"])
        c["rank"] = (c["mc"] / p if p else 1.0, c["real_sol"])
    inwin.sort(key=lambda c: c["rank"], reverse=True)
    log(f"rápida ({src}): {len(mints)} creaciones · {len(cands)} en curva · {len(inwin)} en la ventana")
    store = ms.TxStore(state_file.parent)
    smart = smart if smart is not None else {w["wallet"]: w for w in ms.load_wallets()}
    cards = []
    for c in inwin[:R["deep_k"]]:
        try:
            cards.append(analyse(rpc, store, c, T, sol_usd, smart, prev_mc))
        except (RuntimeError, ValueError, KeyError, TypeError) as e:
            log(f"  {c['mint'][:8]}… {ms.scrub(e)}")
    store.prune(T - 6 * 3600)
    out = Path(outdir or HERE / "report")
    out.mkdir(exist_ok=True)
    report(cards, T, len(mints), len(inwin), out / "SCAN_B.md")
    state["mc"] = {c["mint"]: c["mc"] for c in cands if c["mc"] >= R["mc_min"] * 0.5}
    state_file.parent.mkdir(exist_ok=True)
    state_file.write_text(json.dumps(state))
    lf = Path(log_file or LOG)
    with open(lf, "a", encoding="utf-8") as fh:
        for c in cards:
            fh.write(json.dumps({"T": T, **{k: v for k, v in c.items() if k != "decision_icon"}}, default=str) + "\n")
    return cards


def main():
    cfg = ms.load_config(interactive=False)
    import scan as scanmod
    rpc = ms.tf.RPC(cfg["rpc_url"], min_interval=0.1)
    sol_usd, _ = scanmod.sol_price(cfg.get("sol_usd"))
    run(rpc, sol_usd, log=lambda m: print(ms.scrub(m, cfg), flush=True))


if __name__ == "__main__":
    main()
