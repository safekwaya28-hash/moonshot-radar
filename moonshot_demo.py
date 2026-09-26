#!/usr/bin/env python3
"""
Mundo simulado con verdad conocida para `python moonshot.py demo` y para test_moonshot.py.
No usa internet. Casos:
  FLATCAT   pico 800k -> base plana ~90k; 2 smart wallets compran hace 2-3 h; siguen dentro   -> 🟢
  PUMPER    pico 700k -> cae -> sube fuerte las últimas 72 h (no es base)                  -> 🔴
  SOLDOUT   base plana; el trader compró y ya vendió el 80 %                                -> 🔴
  LATE      base plana a 60k; el trader compra; ahora +40 % sobre su precio                 -> 🟡
  SMALLPK   base plana pero el pico nunca pasó de 200k                                      -> 🔴
  MINTABLE  base perfecta pero con mint authority activa                                    -> 🔴 HARD
  NOGECKO   el trader compra un token sin historial de precio                               -> ⚫
  (una compra de $1k en otro token se ignora: < $5k)
"""
from __future__ import annotations

import math
import tempfile
from pathlib import Path

import numpy as np
import pandas as pd

SOL_USD = 150.0
DEC = 6
T_NOW = 1_790_000_000              # instante fijo para reproducibilidad
H = 3600


def addr(tag):
    return (tag + "1" * 44)[:44]


W1, W2, W3 = addr("TOPTRADERone"), addr("TOPTRADERtwo"), addr("MIDTRADER")
WALLETS = [{"wallet": W1, "label": "Solstice-like"}, {"wallet": W2, "label": "Whale B"}, {"wallet": W3, "label": "Trader C"}]
MINTS = {k: addr("MINT" + k) for k in ["FLATCAT", "PUMPER", "SOLDOUT", "LATE", "SMALLPK", "MINTABLE", "NOGECKO", "DUST"]}


def mc_path(kind, hours, rng):
    """Serie horaria de MC (USD) de las últimas `hours` horas; índice 0 = más antiguo."""
    t = np.arange(hours)
    noise = lambda s: np.exp(rng.normal(0, s, hours))  # noqa: E731
    if kind in ("FLATCAT", "SOLDOUT", "MINTABLE"):
        peak, base = 800_000, 90_000
    elif kind == "LATE":
        peak, base = 650_000, 60_000
    elif kind == "SMALLPK":
        peak, base = 200_000, 40_000
    else:
        peak, base = 700_000, 150_000
    x = np.empty(hours)
    p0 = int(hours * 0.30)                 # pico hacia el día 9 de 30
    x[:p0] = 8_000 * (peak / 8_000) ** (t[:p0] / p0)
    decay = int(hours * 0.25)
    x[p0:p0 + decay] = peak * (base / peak) ** ((t[p0:p0 + decay] - p0) / decay)
    x[p0 + decay:] = base
    x = x * noise(0.03)
    if kind == "PUMPER":                   # sube fuerte las últimas 72 h
        k = hours - 72
        x[k:] = base * (400_000 / base) ** ((t[k:] - k) / 72)
    if kind == "LATE":                     # +40 % en las últimas 5 h
        k = hours - 5
        x[k:] = base * 1.4 ** ((t[k:] - k + 1) / 5)
    return x


class FakeGecko:
    def __init__(self, series):
        self.series, self.calls = series, 0

    def top_pool(self, mint):
        self.calls += 1
        return ("POOL" + mint[:10]) if mint in self.series else None

    def ohlcv_hour(self, pool, mint, limit=1000):
        self.calls += 1
        mc = self.series[mint]
        n = len(mc)
        ts = T_NOW - (n - 1 - np.arange(n)) * H
        px = mc / 1e9
        return pd.DataFrame({"ts": ts.astype("int64"), "o": px, "h": px * 1.01, "l": px * 0.99, "c": px,
                             "v": np.full(n, 20_000.0)})


class World:
    def __init__(self):
        self.txs, self.hist, self.bal, self.accounts = {}, {}, {}, {}
        self.n = 0

    def swap(self, wallet, mint, side, sol, mc_usd, ts, tokens=None):
        """Swap contra SOL. tokens por defecto = SOL*SOL_USD/precio; para ventas parciales pasa tokens."""
        price = mc_usd / 1e9
        if tokens is None:
            tokens = sol * SOL_USD / price
        else:
            sol = tokens * price / SOL_USD
        sig = f"demo{self.n:06d}"
        self.n += 1
        b0 = self.bal.get((wallet, mint))
        d = tokens if side == "buy" else -min(tokens, b0 or 0)
        b1 = (b0 or 0) + d
        pre_t = [] if b0 is None else [self._tb(5, mint, wallet, b0)]
        post_t = [] if b1 <= 1e-9 else [self._tb(5, mint, wallet, b1)]
        rent = 0
        if b0 is None and side == "buy":
            rent = 2_039_280
        elif side == "sell" and b1 <= 1e-9:
            rent = -2_039_280                      # cierra la cuenta y recupera el alquiler
        lam = -int(sol * 1e9) - rent if side == "buy" else int(sol * 1e9) - rent
        fee = 5000
        self.txs[sig] = {"slot": ts, "blockTime": ts, "meta": {
            "err": None, "fee": fee, "preBalances": [10 ** 13, 1, 1], "postBalances": [10 ** 13 + lam - fee, 1, 1],
            "preTokenBalances": pre_t, "postTokenBalances": post_t, "logMessages": []},
            "transaction": {"message": {"accountKeys": [wallet, mint, "PumpSwapProgram"]}}}
        self.hist.setdefault(wallet, []).append((ts, sig))
        if b1 > 1e-9:
            self.bal[(wallet, mint)] = b1
        else:
            self.bal.pop((wallet, mint), None)
        return sig

    @staticmethod
    def _tb(idx, mint, owner, amt):
        return {"accountIndex": idx, "mint": mint, "owner": owner,
                "uiTokenAmount": {"amount": str(int(round(amt * 10 ** DEC))), "decimals": DEC, "uiAmount": amt}}


class FakeRPC:
    def __init__(self, w: World):
        self.w, self.calls = w, 0

    def call(self, method, params):
        self.calls += 1
        if method == "getSignaturesForAddress":
            a, opt = params
            h = sorted(self.w.hist.get(a, []), reverse=True)
            lst = [{"signature": s, "blockTime": t, "err": None} for t, s in h]
            if opt.get("before"):
                i = [x["signature"] for x in lst].index(opt["before"])
                lst = lst[i + 1:]
            return lst[: opt.get("limit", 1000)]
        if method == "getTransaction":
            return self.w.txs.get(params[0])
        if method == "getMultipleAccounts":
            return {"value": [self.w.accounts.get(a) for a in params[0]]}
        if method == "getTokenAccountsByOwner":
            wallet, flt = params[0], params[1]
            b = self.w.bal.get((wallet, flt["mint"]), 0.0)
            return {"value": [{"account": {"data": {"parsed": {"info": {"tokenAmount": {"uiAmount": b}}}}}}] if b else []}
        if method == "getSlot":
            return 1
        raise ValueError(method)


def build():
    rng = np.random.default_rng(3)
    w = World()
    series = {}
    for k, m in MINTS.items():
        if k in ("NOGECKO", "DUST"):
            continue
        series[m] = mc_path(k, 30 * 24, rng)
    for k, m in MINTS.items():
        w.accounts[m] = {"owner": "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb", "data": {"parsed": {"info": {
            "mintAuthority": addr("EVIL") if k == "MINTABLE" else None, "freezeAuthority": None,
            "supply": str(10 ** 9 * 10 ** DEC), "decimals": DEC,
            "extensions": [{"extension": "tokenMetadata", "state": {"name": k.title(), "symbol": k}}]}}}}
    mc_at = lambda m, h_ago: float(series[m][-1 - h_ago]) if m in series else 50_000.0  # noqa: E731
    # historial antiguo de W1: 25 cierres rentables en 6 tokens (para add-wallet)
    for i in range(25):
        m = addr(f"OLD{i % 6}")
        t0 = T_NOW - (30 - i) * 24 * H
        w.swap(W1, m, "buy", 100, 50_000, t0)
        w.swap(W1, m, "sell", 500, 250_000, t0 + 6 * H)   # vende todo x5
    # W3: pocas operaciones (no cumple criterios)
    w.swap(W3, addr("OLDX"), "buy", 10, 50_000, T_NOW - 20 * 24 * H)
    w.swap(W3, addr("OLDX"), "sell", 30, 150_000, T_NOW - 19 * 24 * H)
    # compras recientes (ventana 48 h)
    F = MINTS
    w.swap(W1, F["FLATCAT"], "buy", 8_000 / SOL_USD, mc_at(F["FLATCAT"], 3), T_NOW - 3 * H)
    w.swap(W2, F["FLATCAT"], "buy", 6_000 / SOL_USD, mc_at(F["FLATCAT"], 2), T_NOW - 2 * H)
    w.swap(W1, F["PUMPER"], "buy", 9_000 / SOL_USD, mc_at(F["PUMPER"], 1), T_NOW - 1 * H)
    w.swap(W3, F["SOLDOUT"], "buy", 10_000 / SOL_USD, mc_at(F["SOLDOUT"], 20), T_NOW - 20 * H)
    held = w.bal[(W3, F["SOLDOUT"])]
    w.swap(W3, F["SOLDOUT"], "sell", None, mc_at(F["SOLDOUT"], 10), T_NOW - 10 * H, tokens=0.8 * held)
    w.swap(W2, F["LATE"], "buy", 7_000 / SOL_USD, mc_at(F["LATE"], 5), T_NOW - 5 * H)
    w.swap(W1, F["SMALLPK"], "buy", 6_000 / SOL_USD, mc_at(F["SMALLPK"], 4), T_NOW - 4 * H)
    w.swap(W2, F["MINTABLE"], "buy", 12_000 / SOL_USD, mc_at(F["MINTABLE"], 6), T_NOW - 6 * H)
    w.swap(W3, F["NOGECKO"], "buy", 5_500 / SOL_USD, 30_000, T_NOW - 7 * H)
    w.swap(W2, F["DUST"], "buy", 1_000 / SOL_USD, 30_000, T_NOW - 8 * H)
    return w, series


def run_demo(log=False):
    import moonshot as ms
    w, series = build()
    cfg = {"rules": dict(ms.DEFAULT_RULES)}
    tmp = Path(tempfile.mkdtemp())
    cards = ms.run_radar(FakeRPC(w), FakeGecko(series), cfg, T=T_NOW, sol_usd=SOL_USD, wallets=WALLETS,
                         log=log, state_dir=tmp, log_file=None)
    return cards, T_NOW
