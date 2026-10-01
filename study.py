#!/usr/bin/env python3
"""
ESTUDIO FLAT BASE v2 — ¿qué ENTRADA y qué forma de VENDER dan más 10x-50x COBRADOS (no solo tocados)?

Corre en segundo plano en GitHub Actions (study.yml, cada hora, ~22 min) y va acumulando:
  1. Descubre TODAS las graduadas de pump.fun (pools PumpSwap/SOL vía Helius; plan B: listas de GeckoTerminal).
  2. Para cada moneda, en orden aleatorio: velas diarias -> si el pico >= $500k, velas horarias de todo su historial.
  3. Para cada variante de ENTRADA busca la primera entrada (point-in-time) y la simula con 5 formas de SALIR.
  4. Publica report/STUDY.md (ranking), STUDY_DIST.md (distribución) y STUDY_REGIME.md (por trimestre).

Solo monedas de pump.fun (sufijo "pump", supply 1.000M): MC = precio x 1.000M.
No mide retención de holders, compras/ventas ni top traders (demasiado caro hacia atrás: se mide en vivo con el radar).
"""
from __future__ import annotations

import base64
import csv
import json
import random
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import numpy as np
import pandas as pd

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import pump_discovery as pdsc  # noqa: E402

PUMPSWAP = "pAMMBay6oceH9fJKBRHGP5D4bD4sWpmSwMn52FMfXEA"
WSOL = "So11111111111111111111111111111111111111112"
SUPPLY = 1_000_000_000
DATA = HERE / "study"
POOLS_FILE = DATA / "pools.csv"
DONE_FILE = DATA / "done_v2.csv"
EVENTS_FILE = DATA / "events_v2.csv"

# ---------------------------------------------------------------------------------------------
# Reglas de ENTRADA
# ---------------------------------------------------------------------------------------------
COMMON = {
    "peak_min": 500_000,      # ATH hasta ese momento >= $500k
    "band": 0.25,             # base "plana": cierres horarios dentro de ±25% de su mediana
    "acum_band": 0.30,        # base de "acumulación": precio dentro de ±30% ...
    "acum_vol_ratio": 1.5,    # ... y volumen de las últimas 72 h >= 1,5x el de los 7 días anteriores
    "breakout_days": 14,
    "breakout_vol_mult": 3.0,
}
VARIANTS = []
for dd in (0.70, 0.85):
    for cap in (150_000, 50_000):
        for fh in (72, 168):
            for trig in ("base", "ruptura"):
                VARIANTS.append({"id": f"dd{int(dd*100)}_mc{cap//1000}k_{fh}h_{trig}", "dd": dd, "cap": cap,
                                 "flat_h": fh, "trigger": trig, "kind": "plana"})
        VARIANTS.append({"id": f"dd{int(dd*100)}_mc{cap//1000}k_72h_acum", "dd": dd, "cap": cap,
                         "flat_h": 72, "trigger": "base", "kind": "acum"})
for dd in (0.70, 0.85):
    VARIANTS.append({"id": f"REF_dd{int(dd*100)}_mc150k_sin_base", "dd": dd, "cap": 150_000, "flat_h": 72,
                     "trigger": "base", "kind": "ninguna"})
# Variante "tipo Soap" (aproximación a lo que describe en público; NO es una reproducción exacta de su método)
for trig in ("base", "ruptura"):
    VARIANTS.append({"id": f"TIPO_SOAP_pico200k_dd75_mc50k_72h_{trig}", "peak": 200_000, "dd": 0.75, "cap": 50_000,
                     "flat_h": 72, "trigger": trig, "kind": "plana"})
PEAK_COLLECT = min(v.get("peak", COMMON["peak_min"]) for v in VARIANTS)
YOUR_RULES = ("dd70_mc150k_72h_base", "tuya")

# ---------------------------------------------------------------------------------------------
# Reglas de SALIDA (las 5 se simulan sobre las mismas entradas)
# ---------------------------------------------------------------------------------------------
EXITS = {
    "tuya":       {"levels": [(3, 1 / 3)], "floor": True, "trail": False, "struct": False},
    "solo_stop":  {"levels": [], "floor": True, "trail": False, "struct": False},
    "trailing":   {"levels": [], "floor": True, "trail": True, "struct": False},
    "escalonada": {"levels": [(3, .15), (10, .15), (25, .15)], "floor": True, "trail": True, "struct": False},
    "estructura": {"levels": [], "floor": False, "trail": False, "struct": True},
}
TRAIL = {"activate_x": 5.0, "k_atr": 2.5, "atr_days": 14, "min_dist": 0.15, "max_dist": 0.60}
STRUCT = {"days": 7, "vol_mult": 2.0}


# ---------------------------------------------------------------------------------------------
# Entrada (point-in-time)
# ---------------------------------------------------------------------------------------------
def find_event(c: pd.DataFrame, v: dict):
    """Primera hora en que se cumplen las reglas de la variante. c: velas horarias (ts,o,h,l,c,v) en USD."""
    if len(c) < 24:
        return None
    ts, close, high, vol = c.ts.values, c.c.values * SUPPLY, c.h.values * SUPPLY, c.v.values
    ath = np.maximum.accumulate(high)
    fh = v["flat_h"]
    min_n = max(6, fh // 6)
    j0 = j7 = 0
    for i in range(len(c)):
        while ts[j0] <= ts[i] - fh * 3600:
            j0 += 1
        while ts[j7] <= ts[i] - (fh + 168) * 3600:
            j7 += 1
        if ath[i] < v.get("peak", COMMON["peak_min"]) or close[i] > v["cap"] or 1 - close[i] / ath[i] < v["dd"]:
            continue
        if ts[i] - ts[0] < fh * 3600:
            continue
        w = close[j0:i + 1]
        if v["kind"] != "ninguna":
            if len(w) < min_n:
                continue
            band = COMMON["band"] if v["kind"] == "plana" else COMMON["acum_band"]
            med = float(np.median(w))
            if w.min() < med * (1 - band) or w.max() > med * (1 + band):
                continue
            if v["kind"] == "acum":
                if ts[i] - ts[0] < (fh + 168) * 3600:
                    continue
                v_now = float(vol[j0:i + 1].sum()) / fh
                v_old = float(vol[j7:j0].sum()) / 168
                if v_now < COMMON["acum_vol_ratio"] * max(v_old, 1e-9):
                    continue
        floor, ceil = float(w.min()), float(w.max())
        if v["trigger"] == "base":
            return {"i": i, "ts": int(ts[i]), "mc": float(close[i]), "floor": floor, "ath": float(ath[i])}
        base_vol = float(np.median(vol[j0:i + 1]))
        lim = ts[i] + COMMON["breakout_days"] * 86400
        for k in range(i + 1, len(c)):
            if ts[k] > lim or close[k] < floor * 0.999:
                return None
            if close[k] > ceil and vol[k] >= COMMON["breakout_vol_mult"] * max(base_vol, 1.0):
                return {"i": k, "ts": int(ts[k]), "mc": float(close[k]), "floor": floor, "ath": float(ath[k])}
        return None
    return None


# ---------------------------------------------------------------------------------------------
# Salida: simulación día a día (solo con información hasta ese día)
# ---------------------------------------------------------------------------------------------
def daily(c: pd.DataFrame) -> pd.DataFrame:
    d = c.assign(day=c.ts // 86400).groupby("day").agg(ts=("ts", "first"), o=("o", "first"), h=("h", "max"),
                                                       l=("l", "min"), c=("c", "last"), v=("v", "sum")).reset_index()
    return d


def simulate(d: pd.DataFrame, ev: dict, rule: dict):
    """d: velas diarias de toda la historia. Entra al MC del evento; decide cada día al cierre."""
    entry = ev["mc"] / SUPPLY
    e_day = ev["ts"] // 86400
    f = d[d.day > e_day].reset_index(drop=True)
    pre = d[d.day <= e_day]
    left, cash = 1.0, 0.0
    levels = list(rule["levels"])
    peak_close, peak_high, peak_day = entry, entry, e_day
    tr_hist = list(((pre.h - pre.l) / pre.c.replace(0, np.nan)).fillna(0).values[-TRAIL["atr_days"]:])
    lows7 = list(pre.l.values[-STRUCT["days"]:])
    vols7 = list(pre.v.values[-STRUCT["days"]:])
    exit_day = None
    for _, r in f.iterrows():
        if r.h > peak_high:
            peak_high, peak_day = r.h, r.day
        for lvl, frac in list(levels):                 # ventas parciales al tocar el múltiplo
            if r.h >= lvl * entry:
                cash += frac * lvl
                left -= frac
                levels.remove((lvl, frac))
        peak_close = max(peak_close, r.c)
        tr_hist = (tr_hist + [(r.h - r.l) / r.c if r.c else 0])[-TRAIL["atr_days"]:]
        out = False
        if rule["floor"] and r.c < ev["floor"] / SUPPLY:
            out = True
        if rule["trail"] and peak_high >= TRAIL["activate_x"] * entry:
            dist = min(TRAIL["max_dist"], max(TRAIL["min_dist"], TRAIL["k_atr"] * float(np.mean(tr_hist))))
            if r.c < peak_close * (1 - dist):
                out = True
        if rule["struct"] and len(lows7) >= 3:
            if r.c < min(lows7) and r.v > STRUCT["vol_mult"] * float(np.mean(vols7)):
                out = True
        lows7 = (lows7 + [r.l])[-STRUCT["days"]:]
        vols7 = (vols7 + [r.v])[-STRUCT["days"]:]
        if out:
            cash += left * r.c / entry
            left = 0.0
            exit_day = r.day
            break
    last = f.c.iloc[-1] / entry if len(f) else 1.0
    realized = cash + left * last
    end_day = exit_day if exit_day is not None else (f.day.iloc[-1] if len(f) else e_day)
    return {"realized": round(float(realized), 4), "exited": exit_day is not None,
            "days_held": int(end_day - e_day), "peak_x": round(float(peak_high / entry), 3),
            "days_to_peak": int(peak_day - e_day)}


def analyse_token(mint: str, c: pd.DataFrame, T_end: int) -> list[dict]:
    rows = []
    if c.empty:
        return rows
    d = daily(c)
    for v in VARIANTS:
        ev = find_event(c, v)
        if not ev:
            continue
        after = c[c.ts > ev["ts"]]
        touched = float(after.h.max() * SUPPLY / ev["mc"]) if len(after) else 1.0
        base = {"mint": mint, "variant": v["id"], "entry_ts": ev["ts"], "entry_mc": round(ev["mc"]),
                "days_obs": round((T_end - ev["ts"]) / 86400, 1), "touched_x": round(touched, 3)}
        for name, rule in EXITS.items():
            rows.append({**base, "exit": name, **simulate(d, ev, rule)})
    return rows


# ---------------------------------------------------------------------------------------------
# Datos: descubrimiento de pools y velas de GeckoTerminal
# ---------------------------------------------------------------------------------------------
def discover_pools(rpc, log=print):
    """Pools de PumpSwap contra SOL: (pool, base_mint). Layout Pool: disc8 bump1 index2 creator32 base_mint32 quote_mint32."""
    res = rpc.call("getProgramAccounts", [PUMPSWAP, {"encoding": "base64",
                   "filters": [{"memcmp": {"offset": 75, "bytes": WSOL}}],
                   "dataSlice": {"offset": 43, "length": 32}}])
    rows = res.get("value", []) if isinstance(res, dict) else (res or [])
    out = []
    for a in rows:
        try:
            mint = pdsc.b58encode(base64.b64decode(a["account"]["data"][0])[:32])
        except (KeyError, IndexError, TypeError, ValueError):
            continue
        if mint.endswith("pump"):
            out.append((a["pubkey"], mint))
    log(f"descubrimiento: {len(rows)} pools PumpSwap/SOL · {len(out)} de pump.fun")
    if not out:
        raise RuntimeError("getProgramAccounts no devolvió pools de pump.fun")
    return out


def discover_gecko(gecko, log=print):
    """Plan B (sesgo de supervivencia): listas públicas de GeckoTerminal."""
    out = {}
    for path in ("/networks/solana/dexes/pumpswap/pools", "/networks/solana/trending_pools", "/networks/solana/pools"):
        for page in range(1, 11):
            try:
                j = gecko.get(path, {"page": page})
            except RuntimeError:
                break
            data = (j or {}).get("data") or []
            if not data:
                break
            for p in data:
                try:
                    mint = p["relationships"]["base_token"]["data"]["id"].split("_", 1)[1]
                    pool = p["attributes"]["address"]
                except (KeyError, IndexError, TypeError):
                    continue
                if mint.endswith("pump"):
                    out[pool] = mint
    log(f"descubrimiento (GeckoTerminal, plan B): {len(out)} pools")
    return list(out.items())


def ohlcv(gecko, pool, mint, tf, before=None, limit=1000):
    p = {"aggregate": 1, "limit": limit, "currency": "usd", "token": mint}
    if before:
        p["before_timestamp"] = before
    j = gecko.get(f"/networks/solana/pools/{pool}/ohlcv/{tf}", p)
    rows = ((j or {}).get("data") or {}).get("attributes", {}).get("ohlcv_list") or []
    df = pd.DataFrame(rows, columns=["ts", "o", "h", "l", "c", "v"])
    if df.empty:
        return df
    df["ts"] = df.ts.astype("int64")
    return df.sort_values("ts").drop_duplicates("ts").reset_index(drop=True)


def hourly_history(gecko, pool, mint, max_pages=6):
    parts, before = [], None
    for _ in range(max_pages):
        df = ohlcv(gecko, pool, mint, "hour", before)
        if df.empty:
            break
        parts.append(df)
        if len(df) < 1000:
            break
        before = int(df.ts.min())
    if not parts:
        return pd.DataFrame(columns=["ts", "o", "h", "l", "c", "v"])
    return pd.concat(parts).sort_values("ts").drop_duplicates("ts").reset_index(drop=True)


# ---------------------------------------------------------------------------------------------
# Estado incremental
# ---------------------------------------------------------------------------------------------
def load_csv(path, cols):
    if not path.exists():
        return []
    with open(path, newline="", encoding="utf-8") as fh:
        return [r for r in csv.DictReader(fh)]


def append_csv(path, rows, cols):
    new = not path.exists()
    with open(path, "a", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        if new:
            w.writeheader()
        for r in rows:
            w.writerow(r)



EV_COLS = ["mint", "variant", "exit", "entry_ts", "entry_mc", "days_obs", "touched_x", "realized", "exited",
           "days_held", "peak_x", "days_to_peak"]



def run(rpc, gecko, minutes=22, log=print, T_end=None):
    DATA.mkdir(exist_ok=True)
    T_end = int(T_end or time.time())
    meta_f = DATA / "meta.json"
    meta = json.loads(meta_f.read_text()) if meta_f.exists() else {}
    if not POOLS_FILE.exists():
        try:
            pools, meta["source"] = discover_pools(rpc, log), "pumpswap"
        except Exception as e:  # noqa: BLE001
            log(f"getProgramAccounts falló ({str(e)[:120]}); uso GeckoTerminal")
            pools, meta["source"] = discover_gecko(gecko, log), "gecko"
        random.Random(7).shuffle(pools)
        with open(POOLS_FILE, "w", newline="", encoding="utf-8") as fh:
            w = csv.writer(fh)
            w.writerow(["pool", "mint"])
            w.writerows(pools)
        meta["discovered_at"] = T_end
        meta_f.write_text(json.dumps(meta))
    pools = load_csv(POOLS_FILE, None)
    done = {r["pool"] for r in load_csv(DONE_FILE, None)}
    todo = [p for p in pools if p["pool"] not in done]
    deadline = time.time() + minutes * 60
    n = 0
    for p in todo:
        if time.time() > deadline:
            break
        try:
            d = ohlcv(gecko, p["pool"], p["mint"], "day")
            peak = float(d.h.max() * SUPPLY) if not d.empty else 0.0
            evs, nh = [], 0
            if peak >= PEAK_COLLECT:
                h = hourly_history(gecko, p["pool"], p["mint"])
                nh = len(h)
                evs = analyse_token(p["mint"], h, T_end)
                append_csv(EVENTS_FILE, evs, EV_COLS)
            append_csv(DONE_FILE, [{"pool": p["pool"], "mint": p["mint"], "peak": round(peak),
                                    "hours": nh, "events": len(evs), "at": T_end}],
                       ["pool", "mint", "peak", "hours", "events", "at"])
            n += 1
        except RuntimeError as e:
            log(f"  {p['mint'][:8]}… {e}")
            break                                   # GeckoTerminal saturado: seguimos en la próxima
    log(f"estudio: {n} monedas nuevas esta vez · {len(done) + n}/{len(pools)} en total")
    report(T_end)


# ---------------------------------------------------------------------------------------------
# Métricas
# ---------------------------------------------------------------------------------------------
MATURE_DAYS = 180


def bootstrap_ev(e: pd.DataFrame, n_boot=500, block_days=30, seed=0):
    """Intervalo de confianza del EV remuestreando bloques de 30 días (no operaciones sueltas)."""
    blk = (e.entry_ts.astype("int64") // (block_days * 86400)).values
    ub = np.unique(blk)
    if len(ub) < 2:
        return None, None
    groups = [e.realized.values[blk == b] for b in ub]
    rng = np.random.default_rng(seed)
    evs = []
    for _ in range(n_boot):
        pick = rng.integers(0, len(groups), len(groups))
        vals = np.concatenate([groups[k] for k in pick])
        evs.append(vals.mean())
    return float(np.quantile(evs, 0.025)), float(np.quantile(evs, 0.975))


def portfolio(e: pd.DataFrame, slots=10, stake=50.0):
    """10 huecos de 50 €: entra si hay hueco libre; cada hueco se libera al salir. ROI y máxima caída."""
    e = e.sort_values("entry_ts")
    busy, pnl_events, taken = [], [], 0
    for _, r in e.iterrows():
        busy = [t for t in busy if t > r.entry_ts]
        if len(busy) >= slots:
            continue
        end = r.entry_ts + max(1, r.days_held) * 86400
        busy.append(end)
        taken += 1
        pnl_events.append((end, stake * (r.realized - 1)))
    if not pnl_events:
        return None
    pnl_events.sort()
    curve = np.cumsum([p for _, p in pnl_events])
    peak = np.maximum.accumulate(np.concatenate([[0.0], curve]))
    dd = float(((np.concatenate([[0.0], curve]) - peak).min()) / (slots * stake))
    return {"roi": float(curve[-1] / (slots * stake)), "max_dd": dd, "taken": taken}


def metrics(e: pd.DataFrame):
    if e.empty:
        return None
    x = e.realized.values
    top3 = np.sort(x)[-3:]
    rest = np.sort(x)[:-3] if len(x) > 3 else np.array([])
    lo, hi = bootstrap_ev(e)
    pf = portfolio(e)
    return {"n": len(e), "censored": float((e.days_obs < MATURE_DAYS).mean()),
            "ev": float(x.mean()), "med": float(np.median(x)),
            "p75": float(np.quantile(x, .75)), "p90": float(np.quantile(x, .90)), "p99": float(np.quantile(x, .99)),
            "r10": float((x >= 10).mean()), "r50": float((x >= 50).mean()),
            "t10": float((e.touched_x >= 10).mean()), "t50": float((e.touched_x >= 50).mean()),
            "dpk_med": float(e.days_to_peak.median()), "dpk_p90": float(e.days_to_peak.quantile(.9)),
            "ev_no_top3": float(rest.mean()) if len(rest) else None, "top3": top3.tolist(),
            "ci_lo": lo, "ci_hi": hi,
            "roi": pf["roi"] if pf else None, "max_dd": pf["max_dd"] if pf else None}


def load_events():
    ev = pd.DataFrame(load_csv(EVENTS_FILE, None))
    if ev.empty:
        return ev
    for col in ("entry_ts", "entry_mc", "days_obs", "touched_x", "realized", "days_held", "peak_x", "days_to_peak"):
        ev[col] = pd.to_numeric(ev[col], errors="coerce")
    ev["entry_ts"] = ev.entry_ts.astype("int64")
    return ev


# ---------------------------------------------------------------------------------------------
# Informes
# ---------------------------------------------------------------------------------------------
def _x(v, nd=2):
    return "—" if v is None or (isinstance(v, float) and np.isnan(v)) else f"{v:.{nd}f}x"


def _p(v):
    return "—" if v is None else f"{v:.0%}"


def report(T_end, outdir=None, min_days=30):
    out = Path(outdir or HERE / "report")
    out.mkdir(exist_ok=True)
    meta = json.loads((DATA / "meta.json").read_text()) if (DATA / "meta.json").exists() else {}
    done = load_csv(DONE_FILE, None)
    pools = load_csv(POOLS_FILE, None)
    ev = load_events()
    n_peak = sum(1 for r in done if float(r.get("peak") or 0) >= COMMON["peak_min"])
    when = f"{datetime.fromtimestamp(T_end, timezone.utc):%Y-%m-%d %H:%M} UTC"
    src = ("todas las graduadas de pump.fun (PumpSwap)" if meta.get("source") == "pumpswap"
           else "listas de GeckoTerminal (⚠️ sesgo de supervivencia)")
    head = [f"**{when}** · fuente: {src}", "",
            f"- Monedas revisadas: **{len(done):,} / {len(pools):,}** ({len(done)/max(1, len(pools)):.0%}) · "
            f"con pico ≥ $500k: **{n_peak:,}**"]
    rows = []
    if not ev.empty:
        use = ev[ev.days_obs >= min_days]
        for (var, ex), e in use.groupby(["variant", "exit"]):
            m = metrics(e)
            if m:
                rows.append({"variant": var, "exit": ex, **m})
    L = ["# ESTUDIO · ¿qué entrada y qué forma de vender dan más 10x–50x cobrados?"] + head
    if not rows:
        L += ["", "_Aún no hay entradas con ≥ 30 días observados. Se va llenando cada hora._"]
    else:
        cens = float((ev.days_obs < MATURE_DAYS).mean())
        L += [f"- Entradas simuladas: **{ev.mint.nunique():,} monedas** · **{cens:.0%} con < 180 días de datos después** "
              + ("(⚠️ con tanta censura el estudio todavía no puede afirmar nada sobre 50x)" if cens > 0.5 else ""),
              "", "## Ranking (EV = lo que multiplicas de media por operación, cobrado con esa regla de venta)", "",
              "| # | Entrada | Venta | Ops | EV | IC 95% EV | EV sin top 3 | Mediana | p90 | Cobró ≥10x | Cobró ≥50x | ROI 10×50€ | Caída máx. |",
              "|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
        rows.sort(key=lambda r: -r["ev"])
        shown = [r for r in rows if r["n"] >= 5][:15]
        yours = next((r for r in rows if (r["variant"], r["exit"]) == YOUR_RULES), None)
        if yours and yours not in shown:
            shown.append(yours)
        for k, r in enumerate(shown, 1):
            star = " ⭐" if (r["variant"], r["exit"]) == YOUR_RULES else ""
            luck = " ⚠️" if r["ev_no_top3"] is not None and r["ev_no_top3"] < 1 <= r["ev"] else ""
            ci = f"{_x(r['ci_lo'])}–{_x(r['ci_hi'])}" if r["ci_lo"] is not None else "—"
            roi = "—" if r["roi"] is None else f"{r['roi']:+.0%}"
            L.append(f"| {k} | {r['variant']}{star} | {r['exit']} | {r['n']} | {_x(r['ev'])} | {ci} | {_x(r['ev_no_top3'])}{luck} | "
                     f"{_x(r['med'])} | {_x(r['p90'])} | {_p(r['r10'])} | {_p(r['r50'])} | {roi} | {_p(r['max_dd'])} |")
        L += ["", "⭐ = tus reglas actuales. ⚠️ = el EV pasa de ganar a perder quitando las 3 mejores: es suerte, no estrategia.",
              "EV > 1x = gana de media. Solo filas con ≥ 5 operaciones (con menos de ~30 los números bailan mucho).",
              "Detalle completo: `STUDY_DIST.md` (distribución) y `STUDY_REGIME.md` (por trimestre)."]
    L += ["", "## Reglas", "",
          "**Entrada** (se comprueba hora a hora, solo con datos de ese momento):",
          "- ATH de MC hasta ese momento ≥ $500k (MC = precio × 1.000M); caída desde el ATH ≥ 70% / 85%; MC ≤ $150k / $50k.",
          "- Base `plana`: cierres horarios de las últimas 72 h / 7 días dentro de ±25% de su mediana (mín. 1 vela cada 6 h).",
          "- Base `acum` (acumulación): precio dentro de ±30% en 72 h **y** volumen de esas 72 h ≥ 1,5× el de los 7 días anteriores.",
          "- `base` = entra en la primera hora que se cumple · `ruptura` = primer cierre por encima del techo de la base con "
          "volumen ≥ 3× la mediana de la base, en ≤ 14 días (si antes pierde el suelo, no entra).",
          "- `REF_…_sin_base` = sin exigir base (para ver si la base aporta algo). Una entrada por moneda y variante.",
          "- `TIPO_SOAP_…` = variante tipo Soap: pico ≥ $200k, caída ≥ 75%, MC ≤ $50k, base plana 72 h (entrar en base o en ruptura). "
          "Aproxima lo que él describe en público; NO es una reproducción exacta ni está verificado que opere así.",
          "", "**Venta** (se decide cada día al cierre, solo con datos hasta ese día):",
          "- `tuya`: 1/3 a 3×; el resto al primer cierre diario por debajo del suelo de la base.",
          "- `solo_stop`: todo al primer cierre diario bajo el suelo; nunca vende antes.",
          f"- `trailing`: stop en el suelo; al tocar {TRAIL['activate_x']:.0f}× se activa un stop que sube: sale si el cierre cae "
          f"más de {TRAIL['k_atr']}× la volatilidad diaria media (14 días, en %) desde el máximo cierre "
          f"(distancia entre {TRAIL['min_dist']:.0%} y {TRAIL['max_dist']:.0%}).",
          "- `escalonada`: 15% a 3×, 15% a 10×, 15% a 25×; el 55% restante con el mismo stop que `trailing`.",
          f"- `estructura`: sale al cerrar por debajo del mínimo de los {STRUCT['days']} días anteriores con volumen ≥ "
          f"{STRUCT['vol_mult']:.0f}× su media.",
          "- Si no ha salido, se valora al último precio. Las ventas parciales se cuentan al múltiplo exacto (ligeramente optimista).",
          "", "**Qué no mide:** retención de holders, compras/ventas, top traders y comunidad (se miden en vivo con el radar). "
          "GeckoTerminal da ~6 meses de historial: los 50x lentos quedan cortados (ver % de censura)."]
    (out / "STUDY.md").write_text("\n".join(L) + "\n", encoding="utf-8")

    # ---- distribución completa
    D = ["# ESTUDIO · distribución por entrada × venta"] + head + ["",
         "| Entrada | Venta | Ops | Censura <180d | EV | Mediana | p75 | p90 | p99 | Cobró ≥10x | Tocó ≥10x | Cobró ≥50x | Tocó ≥50x | Días al pico (med/p90) | Top 3 |",
         "|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|"]
    for r in sorted(rows, key=lambda r: (r["variant"], r["exit"])):
        D.append(f"| {r['variant']} | {r['exit']} | {r['n']} | {_p(r['censored'])} | {_x(r['ev'])} | {_x(r['med'])} | "
                 f"{_x(r['p75'])} | {_x(r['p90'])} | {_x(r['p99'])} | {_p(r['r10'])} | {_p(r['t10'])} | {_p(r['r50'])} | "
                 f"{_p(r['t50'])} | {r['dpk_med']:.0f} / {r['dpk_p90']:.0f} | {', '.join(f'{t:.1f}x' for t in r['top3'])} |")
    (out / "STUDY_DIST.md").write_text("\n".join(D) + "\n", encoding="utf-8")

    # ---- por trimestre
    R = ["# ESTUDIO · por trimestre (¿funciona en todos o solo en uno?)"] + head + [""]
    if rows:
        use = ev[ev.days_obs >= min_days].copy()
        use["q"] = pd.to_datetime(use.entry_ts, unit="s").dt.to_period("Q").astype(str)
        qs = sorted(use.q.unique())
        best = [(r["variant"], r["exit"]) for r in sorted(rows, key=lambda r: -r["ev"]) if r["n"] >= 5][:8]
        if YOUR_RULES not in best:
            best.append(YOUR_RULES)
        R += ["EV por trimestre de entrada (entre paréntesis, nº de operaciones y % que cobró ≥10x):", "",
              "| Entrada | Venta | " + " | ".join(qs) + " |", "|---|---|" + "---|" * len(qs)]
        for var, ex in best:
            cells = []
            for q in qs:
                e = use[(use.variant == var) & (use.exit == ex) & (use.q == q)]
                cells.append("—" if e.empty else f"{e.realized.mean():.2f}x ({len(e)}, {(e.realized >= 10).mean():.0%})")
            R.append(f"| {var} | {ex} | " + " | ".join(cells) + " |")
        R += ["", "Si todas las ganancias salen de un solo trimestre, se está midiendo el mercado de ese momento, no la estrategia."]
    else:
        R.append("_Aún sin datos._")
    (out / "STUDY_REGIME.md").write_text("\n".join(R) + "\n", encoding="utf-8")
    return out / "STUDY.md"


def main(argv=None):
    import moonshot as ms
    import token_forensics as tf
    argv = list(sys.argv[1:] if argv is None else argv)
    minutes = float(argv[argv.index("--minutes") + 1]) if "--minutes" in argv else 22
    cfg = ms.load_config(interactive=False)
    rpc = tf.RPC(cfg["rpc_url"], min_interval=0.1, timeout=120)
    run(rpc, ms.Gecko(2.2), minutes=minutes, log=lambda m: print(ms.scrub(m, cfg), flush=True))


if __name__ == "__main__":
    main()
