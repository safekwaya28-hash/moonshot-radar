#!/usr/bin/env python3
"""
SCAM FILTER — features point-in-time + clasificación.

    ⚫ INVALID DATA   no se puede reconstruir el estado con fiabilidad
    🔴 MANIPULATED    bloqueo estructural (HARD) o >= 2 señales de manipulación
    🟡 WATCH          1 señal, actividad insuficiente o datos parciales
    🟢 CLEAN          ninguna señal

IMPORTANTE: los umbrales de PROVISIONAL son el preset MOONSHOT_SAFE_V1 SIN CALIBRAR.
Sirven para ordenar la revisión, no para decidir. Cada scan registra TODAS las features
(scan_log.jsonl) para calibrarlos después contra resultados reales ($1M / rug) y congelarlos.

Todos los porcentajes de supply son sobre el supply TOTAL (1.000M) y EXCLUYEN las cuentas
de sistema (bonding curve, pool). Sin esa exclusión, la curva (~80% al inicio) bloquearía todo.
"""
from __future__ import annotations

from collections import defaultdict

import numpy as np
import pandas as pd

PROVISIONAL = {                       # MOONSHOT_SAFE_V1 · SIN CALIBRAR
    "dev_buy_share": 0.05,
    "single_wallet_share": 0.10,
    "insider_cluster_share": 0.15,
    "same_slot_buyer_share": 0.20,
    "sniper_share": 0.10,
    "fresh_wallet_share": 0.60,
    "volume_top_wallet_share": 0.20,
}
MIN_ACTIVITY = {"buys": 5, "sells": 5, "unique_buyers": 5}
LABELS = {"INVALID": "⚫ INVALID DATA", "MANIPULATED": "🔴 MANIPULATED", "WATCH": "🟡 WATCH", "CLEAN": "🟢 CLEAN"}


def hard_checks(mi: dict) -> list[str]:
    r = []
    if not mi.get("ok"):
        return r
    if mi.get("mint_authority"):
        r.append("mint authority activa")
    if mi.get("freeze_authority"):
        r.append("freeze authority activa")
    if mi.get("dangerous_extensions"):
        r.append("extensiones Token-2022: " + ",".join(mi["dangerous_extensions"]))
    return r


def features(tr: pd.DataFrame, final_bal: dict, info: dict, m: dict, wa: pd.DataFrame | None,
             T: int, supply: float, snipe_slots: int = 2, first_n_buyers: int = 50,
             same_slot_min_wallets: int = 3, hubs: set | None = None) -> dict:
    hubs = hubs or set()
    f = {"age_min": round((T - info["create_ts"]) / 60, 2)}
    buys = tr[tr.side == "buy"] if len(tr) else tr
    sells = tr[tr.side == "sell"] if len(tr) else tr
    f["buys"], f["sells"] = int(len(buys)), int(len(sells))
    f["unique_buyers"] = int(buys.wallet.nunique()) if len(buys) else 0
    f["unique_sellers"] = int(sells.wallet.nunique()) if len(sells) else 0
    f["holders"] = int(len(final_bal))
    f["volume_sol"] = round(float(tr.sol_amount.sum()), 6) if len(tr) else 0.0
    f["buy_sell_ratio"] = round(len(buys) / len(sells), 4) if len(sells) else None
    creator = info["creator"]
    cb = buys[buys.wallet == creator] if len(buys) else buys
    f["dev_buy_share"] = round(float(cb.token_amount.sum()) / supply, 6) if len(cb) else 0.0
    f["creator_sold"] = bool(len(sells) and (sells.wallet == creator).any())
    held = sorted(final_bal.values(), reverse=True)
    f["single_wallet_share"] = round(held[0] / supply, 6) if held else 0.0
    f["top10_share"] = round(sum(held[:10]) / supply, 6) if held else 0.0
    # snipers: wallets que compraron en los primeros slots; cuánto supply siguen teniendo
    if len(buys):
        sn = set(buys[(buys.slot_offset <= snipe_slots) & (buys.wallet != creator)].wallet)
        f["sniper_share"] = round(sum(final_bal.get(w, 0) for w in sn) / supply, 6)
        f["sniper_wallets"] = len(sn)
        first = buys.sort_values(["slot", "block_time"]).drop_duplicates("wallet").head(first_n_buyers)
        per_slot = buys.groupby("slot").wallet.nunique()
        multi = set(per_slot[per_slot >= same_slot_min_wallets].index)
        f["same_slot_buyer_share"] = round(float(first.slot.isin(multi).mean()), 4) if len(first) else 0.0
        vol = tr.groupby("wallet").sol_amount.sum()
        f["volume_top_wallet_share"] = round(float(vol.max() / vol.sum()), 4) if vol.sum() > 0 else None
    else:
        f.update({"sniper_share": 0.0, "sniper_wallets": 0, "same_slot_buyer_share": 0.0,
                  "volume_top_wallet_share": None})
    # cluster de insiders: creador + wallets financiadas por el creador + grupos (>=2) con el mismo financiador
    insiders = {creator}
    f["funders_known"] = 0
    f["fresh_wallet_share"] = None
    if wa is not None and len(wa):
        known = wa[wa.history_exhausted]
        f["funders_known"] = int(known.funder.notna().sum())
        insiders |= set(wa[wa.first_tx_involves_creator == True].wallet)  # noqa: E712
        insiders |= set(wa[wa.funder == creator].wallet)
        grp = known[known.funder.notna() & ~known.funder.isin(hubs)].groupby("funder").wallet.apply(set)
        clusters = [s for s in grp if len(s) >= 2]
        for s in clusters:
            insiders |= s
        f["funder_clusters"] = len(clusters)
        f["largest_funder_cluster"] = max((len(s) for s in clusters), default=0)
        f["fresh_wallet_share"] = round(float(known.fresh.mean()), 4) if len(known) else None
        f["wallets_scanned"] = int(len(wa))
        f["wallets_history_exhausted"] = int(len(known))
    f["insider_cluster_share"] = round(sum(final_bal.get(w, 0) for w in insiders) / supply, 6)
    f["insider_wallets"] = len([w for w in insiders if final_bal.get(w, 0) > 0])
    f["parse_inconsistent_rate"] = m.get("parse_sol_sign_inconsistent_rate")
    return f


def classify(f: dict, hard: list[str], data_problems: list[str], thr=PROVISIONAL, mins=MIN_ACTIVITY):
    if data_problems:
        return "INVALID", data_problems
    if hard:
        return "MANIPULATED", ["HARD: " + h for h in hard]
    reasons, breaches = [], []
    if f.get("creator_sold"):
        return "MANIPULATED", ["creador ha vendido"]
    for k, t in thr.items():
        v = f.get(k)
        if v is not None and v > t:
            breaches.append(f"{k} {v:.0%} > {t:.0%}")
    strong = f.get("insider_cluster_share", 0) > 2 * thr["insider_cluster_share"]
    if len(breaches) >= 2 or strong:
        return "MANIPULATED", breaches
    low = [f"{k} {f.get(k)} < {v}" for k, v in mins.items() if (f.get(k) or 0) < v]
    partial = []
    if f.get("fresh_wallet_share") is None:
        partial.append("edad/financiadores de wallets no disponibles")
    if breaches or low or partial:
        return "WATCH", breaches + low + partial
    return "CLEAN", ["ninguna señal con los umbrales provisionales"]


def moonshot_scores(rows: list[dict]) -> None:
    """Score RELATIVO al lote (0–100): media de percentiles de velocidad de demanda.
    NO es una probabilidad. Solo para tokens no MANIPULATED/INVALID. Provisional hasta calibrar."""
    elig = [r for r in rows if r["label"] in ("CLEAN", "WATCH")]
    for r in rows:
        r["moonshot_score"] = None
    if not elig:
        return
    comp = {
        "buyers_per_min": lambda r: r["f"]["unique_buyers"] / max(r["f"]["age_min"], 1),
        "holders_per_min": lambda r: r["f"]["holders"] / max(r["f"]["age_min"], 1),
        "net_buy_sol_per_min": lambda r: r.get("net_buy_sol", 0) / max(r["f"]["age_min"], 1),
        "mc_usd": lambda r: r.get("mc_usd") or 0,
    }
    mat = pd.DataFrame({k: [fn(r) for r in elig] for k, fn in comp.items()})
    pct = mat.rank(pct=True) if len(elig) > 1 else mat * 0 + 0.5
    score = (pct.mean(axis=1) * 100).round(0)
    for r, s in zip(elig, score):
        r["moonshot_score"] = int(s)
