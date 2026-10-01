#!/usr/bin/env python3
"""
OUTCOMES — qué pasó DESPUÉS con cada decisión de los scanners, incluidas las DESCARTADAS.

Lee los registros (radar_log.jsonl = Radar A, scan_b_log.jsonl = SCAN B, scan_c/signals.jsonl = SCAN C) y, sin tocar
la decisión original, sigue cada moneda: MC +1h, +6h, +24h, máximo (velas de 1 h) y último valor, durante 7 días.
Publica scan_c/OUTCOMES.md: por escáner y decisión, y por MOTIVO de descarte -> "¿qué filtro mata ganadoras?".
Se ejecuta al final de cada pasada del SCAN C (no necesita workflow propio ni RPC).
"""
from __future__ import annotations

import json
import statistics
import time
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).resolve().parent
TRACK_DAYS = 7
MAX_CANDLE_UPDATES = 30          # máximos con velas por pasada (límite de GeckoTerminal)
REASONS = [("mint authority", "puede crear tokens"), ("freeze authority", "puede congelar"),
           ("impuesto", "impuesto modificable"), ("extensiones", "extensión peligrosa"), ("snipers", "snipers"),
           ("bloque de creación", "compras en el bloque de creación"), ("concentración", "concentración"),
           ("dev tiene", "dev con mucho supply"), ("dev vendió", "dev vendió"), ("bucle", "volumen en bucle"),
           ("HARD", "seguridad")]


def reason_of(hard):
    if not hard:
        return None
    h = hard[0] if isinstance(hard, list) else str(hard)
    for k, lab in REASONS:
        if k in h:
            return lab
    return "otro"


def _read_jsonl(path):
    out = []
    p = Path(path)
    if not p.exists():
        return out
    for line in p.read_text(encoding="utf-8").splitlines():
        try:
            out.append(json.loads(line))
        except ValueError:
            continue
    return out


def collect(base):
    """Primera aparición de cada (escáner, moneda) con su decisión original."""
    ev = []
    for r in _read_jsonl(base / "radar_log.jsonl"):
        if r.get("mint"):
            ev.append(("A", r["mint"], int(r["T"]), r.get("label"), r.get("mc_now"), reason_of(r.get("reasons") if r.get("label") == "NO" else None)))
    for r in _read_jsonl(base / "scan_b_log.jsonl"):
        if r.get("mint"):
            ev.append(("B", r["mint"], int(r["T"]), r.get("decision"), r.get("mc"), reason_of(r.get("hard"))))
    for r in _read_jsonl(base / "scan_c" / "signals.jsonl"):
        if r.get("type") == "meta" and (r.get("leaders") or {}).get("volumen"):
            ev.append(("C-meta", r["leaders"]["volumen"], int(r["T"]), r.get("state"), r.get("leader_mc"), reason_of(r.get("hard"))))
        elif r.get("type") == "flywheel" and r.get("token"):
            ev.append(("C-flywheel", r["token"], int(r["T"]), r.get("state"), r.get("token_mc"), reason_of(r.get("hard"))))
    return ev


def update(http, T=None, base=None, store=None, log=print):
    import scan_c as sc
    T = int(T or time.time())
    base = Path(base or HERE)
    store = Path(store or base / "scan_c" / "outcomes.json")
    db = json.loads(store.read_text()) if store.exists() else {}
    for src, mint, t0, dec, mc0, reason in collect(base):
        key = f"{src}|{mint}"
        if key not in db or t0 < db[key]["t0"]:
            if key not in db:
                db[key] = {"src": src, "mint": mint, "t0": t0, "decision": dec, "mc0": mc0, "reason": reason}
    live = [k for k, v in db.items() if T - v["t0"] < TRACK_DAYS * 86400]
    ds = {}
    try:
        ds = sc.dexscreener(http, sc.CFG["chain"], list({db[k]["mint"] for k in live}))
    except Exception as e:  # noqa: BLE001
        log(f"outcomes: DexScreener no disponible ({str(e)[:80]})")
    n_candles = 0
    for k in live:
        r, d = db[k], ds.get(db[k]["mint"])
        if not d or not d.get("mc"):
            if d is None and T - r["t0"] > 3600:
                r["missing"] = r.get("missing", 0) + 1         # sin par activo: probablemente muerta
            continue
        mc = float(d["mc"])
        if not r.get("mc0"):
            r["mc0"] = mc
        age = T - r["t0"]
        for lab, sec in (("mc_1h", 3600), ("mc_6h", 6 * 3600), ("mc_24h", 86400)):
            if age >= sec and lab not in r:
                r[lab], r[lab + "_lag_min"] = mc, round((age - sec) / 60)
        r["last_mc"], r["last_at"] = mc, T
        r["ath_obs"] = max(r.get("ath_obs", 0), mc)
        if d.get("pair") and d.get("price") and T - r.get("ath_at", 0) >= 6 * 3600 and n_candles < MAX_CANDLE_UPDATES:
            try:
                k_ = mc / float(d["price"])
                rows = [x for x in sc.gecko_candles(http, sc.CFG["chain"], d["pair"], "hour", limit=200) if x[0] >= r["t0"] - 3600]
                if rows:
                    r["ath"] = max(x[2] for x in rows) * k_
                    r["ath_at"] = T
                    r.update(path_stats(rows, k_, r.get("mc0") or mc))
                n_candles += 1
            except Exception:  # noqa: BLE001
                pass
    store.parent.mkdir(parents=True, exist_ok=True)
    store.write_text(json.dumps(db))
    report(db, T, base / "scan_c" / "OUTCOMES.md")
    return db


TARGETS = ((2, 0.70, "2x_antes_-30"), (5, 0.50, "5x_antes_-50"), (10, 0.30, "10x_antes_-70"))


def path_stats(rows, k, mc0):
    """MFE/MAE y '¿llegó al objetivo ANTES de tocar el stop?' recorriendo las velas en orden.
    Si objetivo y stop caen en la misma vela, cuenta como stop (criterio conservador). None = aún sin resolver."""
    out = {"mfe": max(x[2] for x in rows) * k / mc0, "mae": min(x[3] for x in rows) * k / mc0 - 1}
    for tgt, stop, name in TARGETS:
        res = None
        for x in rows:
            if x[3] * k <= stop * mc0:
                res = False
                break
            if x[2] * k >= tgt * mc0:
                res = True
                break
        out[name] = res
    return out


def _mult(r, k):
    v = r.get(k)
    return v / r["mc0"] if (v and r.get("mc0")) else None


def _stats(rows):
    m24 = [x for x in (_mult(r, "mc_24h") for r in rows) if x is not None]
    peak = [x for x in ((r.get("ath") or r.get("ath_obs")) / r["mc0"] for r in rows if r.get("mc0") and (r.get("ath") or r.get("ath_obs"))) if x]
    return {"n": len(rows), "n24": len(m24),
            "med24": statistics.median(m24) if m24 else None,
            "dead24": (sum(x <= 0.5 for x in m24) / len(m24)) if m24 else None,
            "p2": (sum(x >= 2 for x in peak) / len(peak)) if peak else None,
            "p5": (sum(x >= 5 for x in peak) / len(peak)) if peak else None,
            "p10": (sum(x >= 10 for x in peak) / len(peak)) if peak else None,
            **{name: _hit(rows, name) for _, _, name in TARGETS}}


def _hit(rows, name):
    v = [r[name] for r in rows if r.get(name) is not None]
    return (sum(v) / len(v), len(v)) if v else (None, 0)


def _hits(s):
    cells = []
    for _, _, name in TARGETS:
        v, n = s[name]
        cells.append("—" if v is None else f"{v:.0%} (n={n})")
    return " | ".join(cells)


def report(db, T, path):
    f = lambda x, fmt: "—" if x is None else format(x, fmt)  # noqa: E731
    L = ["# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)",
         f"**{datetime.fromtimestamp(T, timezone.utc):%Y-%m-%d %H:%M} UTC** · {len(db)} monedas seguidas · "
         "la decisión original nunca se cambia", "",
         "| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | "
         "2x antes de −30% | 5x antes de −50% | 10x antes de −70% |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|"]
    groups = {}
    for r in db.values():
        groups.setdefault((r["src"], r.get("decision") or "—"), []).append(r)
    for (src, dec), rows in sorted(groups.items()):
        s = _stats(rows)
        L.append(f"| {src} | {dec} | {s['n']} | {s['n24']} | {f(s['med24'], '.2f')}x | {f(s['dead24'], '.0%')} | "
                 f"{f(s['p2'], '.0%')} | {f(s['p5'], '.0%')} | {f(s['p10'], '.0%')} | " + _hits(s) + " |")
    L += ["", "## ¿Qué filtro mata ganadoras? (descartadas por motivo)", "",
          "| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |",
          "|---|---|---|---|---|---|---|---|---|---|"]
    rs = {}
    for r in db.values():
        if r.get("reason"):
            rs.setdefault(r["reason"], []).append(r)
    if not rs:
        L.append("| — | 0 | | | | | |")
    for reason, rows in sorted(rs.items(), key=lambda x: -len(x[1])):
        s = _stats(rows)
        L.append(f"| {reason} | {s['n']} | {s['n24']} | {f(s['med24'], '.2f')}x | {f(s['dead24'], '.0%')} | {f(s['p5'], '.0%')} | "
                 f"{f(s['p10'], '.0%')} | " + _hits(s) + " |")
    L += ["", "Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, "
          "ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.",
          "Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).",
          "**\"2x antes de −30%\"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop "
          "(si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable."]
    Path(path).write_text("\n".join(L) + "\n", encoding="utf-8")
