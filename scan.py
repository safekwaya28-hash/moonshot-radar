#!/usr/bin/env python3
"""
SCAN — descubrimiento + reconstrucción on-chain + filtro + score, en una sola orden.

    python scan.py --rpc "https://mainnet.helius-rpc.com/?api-key=XXX"
    python scan.py --doctor --rpc ...        # PRIMERA VEZ: verifica direcciones y layout en red real

Flujo por scan (instante T = ahora):
  1. Pump.fun: creaciones en [T - window, T - min_age]
  2. Estado barato por lotes: curva (MC, progreso, graduado) + mint (authorities, extensiones)
  3. HARD_SCAM para todos
  4. Presupuesto RPC: reconstrucción completa solo de los top-N por MC  (esto es un límite de
     coste, NO un filtro de calidad; los no analizados se registran igualmente)
  5. token_forensics a T  ->  features  ->  CLEAN / WATCH / MANIPULATED / INVALID
  6. MOONSHOT SCORE relativo al lote (provisional)
  7. Tarjetas en pantalla + scan_log.jsonl (TODOS los tokens descubiertos, para calibrar)
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import time
import uuid
from datetime import datetime, timezone

import pandas as pd

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import pump_discovery as pdsc  # noqa: E402
import scam_filter as sf  # noqa: E402
import token_forensics as tf  # noqa: E402

VERSION = "scan-0.1"
DEFAULTS = {
    **pdsc.DEFAULTS,
    "window_min": 30, "min_age_min": 2, "max_new": 400, "top_n": 25,
    "funder_top_k": 25, "funder_pages": 2, "max_sig_pages": 5,
    "snipe_slots": 2, "hubs": [],          # hubs: financiadores masivos (p.ej. hot wallets de exchanges)
    "thresholds": sf.PROVISIONAL, "min_activity": sf.MIN_ACTIVITY,
}


def sol_price(arg):
    if arg:
        return float(arg), "manual"
    try:
        import requests
        r = requests.get("https://api.coingecko.com/api/v3/simple/price",
                         params={"ids": "solana", "vs_currencies": "usd"}, timeout=10)
        return float(r.json()["solana"]["usd"]), "coingecko"
    except Exception as e:  # noqa: BLE001
        raise SystemExit(f"No pude obtener SOL/USD ({e}). Pásalo con --sol-usd 150")


def fmt_usd(x):
    if x is None:
        return "—"
    return f"${x/1e6:.2f}M" if x >= 1e6 else f"${x/1e3:.1f}k" if x >= 1e3 else f"${x:.0f}"


def fmt_pct(x):
    return "—" if x is None else f"{100*x:.1f}%"


def analyse(rpc, c, T, cfg, cache, sol_usd):
    """Reconstrucción on-chain de un token a T -> dict con features y etiqueta."""
    mint = c["mint"]
    problems = []
    sigs, exhausted = tf.fetch_signatures(rpc, mint, max_pages=cfg["max_sig_pages"], log=False)
    if not exhausted:
        return {"problems": [f"historial > {cfg['max_sig_pages']*1000} firmas (sube max_sig_pages)"]}
    sigs = [s for s in sigs if (s.get("blockTime") or 0) <= T]
    tf.fetch_transactions(rpc, sigs, cache)
    parsed = [tf.parse_tx(s["signature"], cache.get(s["signature"]), mint) for s in sigs]
    try:
        tr, hs, final_bal, info = tf.build(parsed, mint, until_ts=T)
    except SystemExit as e:
        return {"problems": [str(e)]}
    if info["create_signature"] != c["create_sig"]:
        problems.append("la primera tx del mint no es la creación descubierta")
    m = tf.metrics(tr, hs, final_bal, info, snipe_slots=cfg["snipe_slots"]) if len(tr) else {}
    if (m.get("parse_sol_sign_inconsistent_rate") or 0) > 0.05:
        problems.append(f"parseo SOL incoherente ({m['parse_sol_sign_inconsistent_rate']:.0%})")
    wa = None
    if len(tr) and cfg["funder_top_k"]:
        b = tr[(tr.side == "buy") & (tr.wallet != info["creator"])]
        first = b.groupby("wallet").block_time.min().sort_values()
        ws = list(first.index[: cfg["funder_top_k"]])
        if ws:
            wa = tf.wallet_age_scan(rpc, ws, first.to_dict(), info["creator"], cfg["funder_pages"], log=False)
    f = sf.features(tr, final_bal, info, m, wa, T, cfg["total_supply"], snipe_slots=cfg["snipe_slots"],
                    hubs=set(cfg["hubs"]))
    net_buy = float(tr[tr.side == "buy"].sol_amount.sum() - tr[tr.side == "sell"].sol_amount.sum()) if len(tr) else 0.0
    last_px = float(tr.sort_values("block_time").price_sol.dropna().iloc[-1]) if len(tr) and tr.price_sol.notna().any() else None
    return {"problems": problems, "f": f, "net_buy_sol": net_buy, "last_price_sol": last_px,
            "n_tx": info["n_tx_ok"], "migrated": info["migration_signature"] is not None}


def card(r):
    f = r.get("f") or {}
    sym = r.get("symbol") or r["mint"][:6]
    L = [sf.LABELS[r["label"]], "",
         f"${sym}" + (f"  ·  {r['name']}" if r.get("name") else ""),
         f"CA: {r['mint']}",
         f"MC: {fmt_usd(r.get('mc_usd'))}" + (f"  (curva {r['progress']:.0%})" if r.get("progress") is not None and not r.get("complete") else "  (graduado)" if r.get("complete") else ""),
         f"AGE: {r['age_min']:.0f} min",
         f"BUYERS: {f.get('unique_buyers', '—')}", f"SELLERS: {f.get('unique_sellers', '—')}",
         f"HOLDERS: {f.get('holders', '—')}",
         f"VOLUME: {fmt_usd(f['volume_sol'] * r['sol_usd']) if 'volume_sol' in f else '—'}", "",
         f"INSIDER CLUSTER: {fmt_pct(f.get('insider_cluster_share'))}  ({f.get('insider_wallets', 0)} wallets, cluster mayor {f.get('largest_funder_cluster', 0)})",
         f"SNIPER: {fmt_pct(f.get('sniper_share'))}  ({f.get('sniper_wallets', 0)} wallets)",
         f"FRESH WALLETS: {fmt_pct(f.get('fresh_wallet_share'))}",
         f"TOP HOLDERS: top1 {fmt_pct(f.get('single_wallet_share'))} · top10 {fmt_pct(f.get('top10_share'))}", "",
         f"MOONSHOT SCORE: {r['moonshot_score'] if r.get('moonshot_score') is not None else '—'}",
         "REASON: " + "; ".join(r["reasons"])]
    return "\n".join(L)


def run_scan(rpc, cfg, T, sol_usd, out, show_all=False, mints=None):
    os.makedirs(out, exist_ok=True)
    cache = tf.TxCache(os.path.join(out, "tx_cache.jsonl"))
    scan_id = datetime.fromtimestamp(T, timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:4]
    t0 = time.time()
    since, until = T - cfg["window_min"] * 60, T - cfg["min_age_min"] * 60
    print(f"[1/5] creaciones entre {datetime.fromtimestamp(since, timezone.utc):%H:%M} y "
          f"{datetime.fromtimestamp(until, timezone.utc):%H:%M} UTC", file=sys.stderr)
    creates, n_sigs = pdsc.discover(rpc, since, until, cfg, cfg["max_new"], cache=cache)
    if mints:
        creates = [c for c in creates if c["mint"] in set(mints)]
    print(f"[2/5] estado de {len(creates)} curvas y mints", file=sys.stderr)
    curves = pdsc.get_multiple(rpc, [c["curve"] for c in creates], "base64")
    minfo = pdsc.get_multiple(rpc, [c["mint"] for c in creates], "jsonParsed")
    rows = []
    for c in creates:
        cv = pdsc.decode_curve(curves.get(c["curve"]), cfg)
        mi = pdsc.mint_info(minfo.get(c["mint"]), cfg)
        r = {**c, "age_min": (T - c["create_ts"]) / 60, "sol_usd": sol_usd,
             "mc_usd": cv["mc_sol"] * sol_usd if cv and cv.get("mc_sol") else None,
             "progress": cv["progress"] if cv else None, "complete": cv["complete"] if cv else None,
             "hard": sf.hard_checks(mi), "mint_ok": mi.get("ok", False), "curve_ok": cv is not None}
        rows.append(r)
    # presupuesto: HARD se resuelve sin forensics; el resto por MC descendente
    for r in rows:
        if r["hard"]:
            r["label"], r["reasons"] = "MANIPULATED", ["HARD: " + h for h in r["hard"]]
    pend = sorted([r for r in rows if "label" not in r], key=lambda r: -(r["mc_usd"] or 0))
    todo, skipped = pend[: cfg["top_n"]], pend[cfg["top_n"]:]
    for r in skipped:
        r["label"], r["reasons"] = "NOT_ANALYZED", [f"fuera del presupuesto top-{cfg['top_n']} por MC"]
    print(f"[3/5] reconstrucción on-chain de {len(todo)} tokens", file=sys.stderr)
    for i, r in enumerate(todo, 1):
        print(f"    {i}/{len(todo)} {r.get('symbol') or r['mint'][:8]}", file=sys.stderr, end="\r")
        try:
            a = analyse(rpc, r, T, cfg, cache, sol_usd)
        except RuntimeError as e:
            a = {"problems": [f"RPC: {e}"]}
        probs = list(a.get("problems", []))
        if not r["curve_ok"] and not a.get("migrated"):
            probs.append("curva no decodificable (¿layout cambiado? ejecuta --doctor)")
        if not r["mint_ok"]:
            probs.append("cuenta mint no legible")
        r.update({k: v for k, v in a.items() if k != "problems"})
        if r.get("complete") and a.get("last_price_sol"):
            r["mc_usd"] = a["last_price_sol"] * cfg["total_supply"] * sol_usd
        r["label"], r["reasons"] = sf.classify(a.get("f") or {}, [], probs, cfg["thresholds"], cfg["min_activity"])
    print(file=sys.stderr)
    print("[4/5] score", file=sys.stderr)
    sf.moonshot_scores([r for r in rows if r["label"] in ("CLEAN", "WATCH", "MANIPULATED", "INVALID")])
    # salida
    order = {"CLEAN": 0, "WATCH": 1, "MANIPULATED": 2, "INVALID": 3, "NOT_ANALYZED": 4}
    rows.sort(key=lambda r: (order[r["label"]], -(r.get("moonshot_score") or -1), -(r.get("mc_usd") or 0)))
    counts = {k: sum(1 for r in rows if r["label"] == k) for k in order}
    head = [f"SCAN {scan_id} · {len(rows)} lanzamientos en {cfg['window_min']} min · SOL ${sol_usd:.2f} ({time.time()-t0:.0f}s, {getattr(rpc,'calls','?')} llamadas RPC)",
            f"🟢 {counts['CLEAN']}  🟡 {counts['WATCH']}  🔴 {counts['MANIPULATED']}  ⚫ {counts['INVALID']}  · no analizados {counts['NOT_ANALYZED']}",
            "Umbrales PROVISIONALES sin calibrar: ordena la revisión, no es una recomendación de compra.", ""]
    shown = [r for r in rows if r["label"] in ("CLEAN", "WATCH") or (show_all and r["label"] != "NOT_ANALYZED")]
    body = ["\n\n".join(card(r) for r in shown) if shown else "Ningún candidato CLEAN/WATCH en este scan."]
    bad = [r for r in rows if r["label"] in ("MANIPULATED", "INVALID")]
    if bad and not show_all:
        body.append("\n—— descartados ——")
        body += [f"{sf.LABELS[r['label']][:2]} ${r.get('symbol') or r['mint'][:6]} {fmt_usd(r.get('mc_usd'))} · "
                 + "; ".join(r["reasons"])[:140] for r in bad]
    text = "\n".join(head + body)
    with open(os.path.join(out, "scan_log.jsonl"), "a") as fh:
        for r in rows:
            fh.write(json.dumps({"scan_id": scan_id, "T": T, "version": VERSION, "thresholds": cfg["thresholds"],
                                 **{k: v for k, v in r.items() if k not in ("hard",)}}, default=str) + "\n")
    with open(os.path.join(out, f"scan_{scan_id}.txt"), "w") as fh:
        fh.write(text + "\n")
    print("[5/5] hecho", file=sys.stderr)
    return rows, text


def doctor(rpc, cfg, sol_usd):
    """Verifica en red real que descubrimiento y layout funcionan. No clasifica nada."""
    print("DOCTOR · comprobando supuestos en la red real\n")
    ok = True
    res = rpc.call("getSignaturesForAddress", [cfg["discovery_address"], {"limit": 10}])
    print(f"1. firmas recientes en discovery_address: {len(res)}")
    if not res:
        print("   ❌ ninguna: la dirección de descubrimiento es incorrecta"); return False
    lag = time.time() - (res[0].get("blockTime") or 0)
    print(f"   la más reciente hace {lag:.0f}s " + ("✅" if lag < 300 else "⚠️ (poco activa: ¿dirección correcta?)"))
    creates = []
    for s in res:
        tx = rpc.call("getTransaction", [s["signature"], {"encoding": "jsonParsed", "maxSupportedTransactionVersion": 0}])
        c = pdsc.parse_create(s["signature"], tx, cfg)
        if c:
            creates.append(c)
    print(f"2. de 10 tx, creaciones parseadas: {len(creates)} " + ("✅" if len(creates) >= 7 else "❌"))
    ok &= len(creates) >= 7
    if creates:
        print(f"   ejemplo: ${creates[0]['symbol']} · {creates[0]['name']} · {creates[0]['mint']}")
        curves = pdsc.get_multiple(rpc, [c["curve"] for c in creates], "base64")
        dec = [pdsc.decode_curve(curves.get(c["curve"]), cfg) for c in creates]
        good = [d for d in dec if d]
        print(f"3. curvas decodificadas: {len(good)}/{len(creates)} " + ("✅" if len(good) == len(creates) else "❌"))
        ok &= len(good) == len(creates)
        for c, d in list(zip(creates, dec))[:3]:
            if d:
                print(f"   ${c['symbol']}: MC {fmt_usd(d['mc_sol'] * sol_usd)} · progreso {d['progress']:.1%} "
                      f"· complete={d['complete']}  (un token recién creado debería estar ~$3k–$8k)")
        mi = pdsc.get_multiple(rpc, [c["mint"] for c in creates], "jsonParsed")
        infos = [pdsc.mint_info(mi.get(c["mint"]), cfg) for c in creates]
        progs = {i.get("program") for i in infos}
        print(f"4. programas de token: {progs} · extensiones vistas: "
              f"{sorted({e for i in infos for e in i.get('extensions', [])})}")
        auth = sum(1 for i in infos if i.get("mint_authority") or i.get("freeze_authority"))
        print(f"   tokens con authority activa: {auth}/{len(infos)} (en Pump estándar debería ser 0)")
    print("\n" + ("✅ Supuestos verificados. Puedes usar scan." if ok else "❌ NO uses scan hasta corregir la configuración."))
    return ok


def main():
    ap = argparse.ArgumentParser(description="SCAN: Pump.fun en tiempo real -> candidatos")
    ap.add_argument("--rpc", default=os.environ.get("SOLANA_RPC"), required=os.environ.get("SOLANA_RPC") is None)
    ap.add_argument("--config", help="JSON con overrides de DEFAULTS (ventana, top_n, umbrales, hubs...)")
    ap.add_argument("--out", default="scans")
    ap.add_argument("--sol-usd", type=float)
    ap.add_argument("--window", type=int, help="minutos hacia atrás (defecto 30)")
    ap.add_argument("--top", type=int, help="nº de tokens a reconstruir (defecto 25)")
    ap.add_argument("--now", type=int, help="epoch UTC para reproducir un scan pasado")
    ap.add_argument("--show-all", action="store_true")
    ap.add_argument("--doctor", action="store_true")
    ap.add_argument("--min-interval", type=float, default=0.1)
    a = ap.parse_args()
    cfg = dict(DEFAULTS)
    if a.config:
        with open(a.config) as fh:
            cfg.update(json.load(fh))
    if a.window:
        cfg["window_min"] = a.window
    if a.top:
        cfg["top_n"] = a.top
    rpc = tf.RPC(a.rpc, min_interval=a.min_interval)
    usd, src = sol_price(a.sol_usd)
    if a.doctor:
        sys.exit(0 if doctor(rpc, cfg, usd) else 1)
    _, text = run_scan(rpc, cfg, a.now or int(time.time()), usd, a.out, a.show_all)
    print(text)


if __name__ == "__main__":
    main()
