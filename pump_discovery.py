#!/usr/bin/env python3
"""
PUMP DISCOVERY — encuentra lanzamientos nuevos de Pump.fun usando solo RPC de Solana.

Método (barato, sin APIs de terceros):
  * Todas las creaciones de Pump.fun incluyen la cuenta "mint authority" del programa.
    getSignaturesForAddress(<esa cuenta>) devuelve (casi) solo transacciones de creación.
  * De cada creación se extrae: mint, bonding curve (quien recibe el supply), creador,
    nombre y ticker (del instruction data de Anchor: disc(8) + borsh name + symbol + uri).
  * Estado barato por lotes de 100 (getMultipleAccounts):
      - bonding curve  -> reservas virtuales -> precio y MC en SOL, progreso, complete
      - mint           -> mint/freeze authority, programa (Token / Token-2022), extensiones

Las direcciones y el layout son configurables. Ejecuta primero `python scan.py --doctor`:
comprueba en la red real que la dirección de descubrimiento devuelve creaciones y que la curva
se decodifica con valores plausibles. Si falla, NO sigas: cambia la configuración.
"""
from __future__ import annotations

import base64
import struct
import sys

# Versión máxima de transacción que aceptamos del RPC (Solana ya emite v1; con 0 el RPC rechaza la petición)
TX_VERSION = 1


PUMP_PROGRAM = "6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P"
PUMP_MINT_AUTHORITY = "TSLvdd1pWpHVjahSpsvCXUbgwsL3JAcvokwaKt1eokM"
TOKEN_PROGRAM = "TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA"
TOKEN_2022 = "TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb"
DEFAULTS = {
    "discovery_address": PUMP_MINT_AUTHORITY,
    "pump_program": PUMP_PROGRAM,
    "total_supply": 1_000_000_000,
    "token_decimals": 6,
    "initial_real_token_reserves": 793_100_000,   # tokens vendibles en la curva al crear
    "benign_extensions": ["metadataPointer", "tokenMetadata", "mintCloseAuthority"],
}
B58 = "123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz"


def b58decode(s: str) -> bytes:
    n = 0
    for ch in s:
        n = n * 58 + B58.index(ch)
    raw = n.to_bytes((n.bit_length() + 7) // 8, "big") if n else b""
    pad = len(s) - len(s.lstrip("1"))
    return b"\x00" * pad + raw


def b58encode(b: bytes) -> str:
    n = int.from_bytes(b, "big")
    out = ""
    while n:
        n, r = divmod(n, 58)
        out = B58[r] + out
    pad = len(b) - len(b.lstrip(b"\x00"))
    return "1" * pad + out


def _borsh_str(buf: bytes, off: int):
    (ln,) = struct.unpack_from("<I", buf, off)
    if ln > 200:
        raise ValueError("string demasiado larga")
    return buf[off + 4: off + 4 + ln].decode("utf-8", "replace"), off + 4 + ln


def decode_create_args(data_b58: str):
    buf = b58decode(data_b58)
    name, off = _borsh_str(buf, 8)
    symbol, off = _borsh_str(buf, off)
    return name, symbol


def _keys(tx):
    ks = tx["transaction"]["message"]["accountKeys"]
    return [k["pubkey"] if isinstance(k, dict) else k for k in ks]


def parse_create(sig: str, tx: dict, cfg: dict) -> dict | None:
    """Devuelve el lanzamiento si la tx es una creación de Pump.fun, si no None."""
    if not tx or (tx.get("meta") or {}).get("err") is not None:
        return None
    meta = tx["meta"]
    logs = " | ".join(meta.get("logMessages") or [])
    if "Instruction: Create" not in logs:
        return None
    supply_raw = cfg["total_supply"] * 10 ** cfg["token_decimals"]
    pre_idx = {tb["accountIndex"] for tb in meta.get("preTokenBalances") or []}
    mint = curve = None
    for tb in meta.get("postTokenBalances") or []:
        amt = int(tb.get("uiTokenAmount", {}).get("amount") or 0)
        if tb["accountIndex"] not in pre_idx and amt >= supply_raw * 0.5:
            mint, curve = tb["mint"], tb["owner"]
            break
    if not mint:
        return None
    name = symbol = None
    for ix in tx["transaction"]["message"].get("instructions", []):
        if ix.get("programId") == cfg["pump_program"] and ix.get("data"):
            try:
                name, symbol = decode_create_args(ix["data"])
                break
            except (ValueError, struct.error, IndexError):
                continue
    return {"mint": mint, "curve": curve, "creator": _keys(tx)[0], "create_sig": sig,
            "create_ts": tx.get("blockTime"), "create_slot": tx.get("slot"), "name": name, "symbol": symbol}


def discover(rpc, since_ts: int, until_ts: int, cfg: dict, max_new: int, cache=None, log=True):
    """Creaciones con since_ts <= blockTime <= until_ts (más recientes primero)."""
    addr = cfg["discovery_address"]
    sigs, before = [], None
    while True:
        p = {"limit": 1000}
        if before:
            p["before"] = before
        res = rpc.call("getSignaturesForAddress", [addr, p])
        if not res:
            break
        for s in res:
            bt = s.get("blockTime")
            if bt is None or s.get("err") is not None:
                continue
            if bt > until_ts:
                continue
            if bt < since_ts:
                res = []
                break
            sigs.append(s["signature"])
        if not res or len(res) < 1000 or len(sigs) >= max_new:
            break
        before = res[-1]["signature"]
    sigs = sigs[:max_new]
    out = []
    for i, sig in enumerate(sigs, 1):
        tx = cache.get(sig) if cache else None
        if tx is None:
            tx = rpc.call("getTransaction", [sig, {"encoding": "jsonParsed", "maxSupportedTransactionVersion": TX_VERSION}])
            if cache:
                cache.put(sig, tx)
        c = parse_create(sig, tx, cfg)
        if c:
            out.append(c)
        if log and (i % 25 == 0 or i == len(sigs)):
            print(f"    creaciones: {i}/{len(sigs)}", file=sys.stderr, end="\r")
    if log and sigs:
        print(file=sys.stderr)
    return out, len(sigs)


def get_multiple(rpc, addresses: list[str], encoding: str):
    out = {}
    for i in range(0, len(addresses), 100):
        chunk = addresses[i:i + 100]
        res = rpc.call("getMultipleAccounts", [chunk, {"encoding": encoding}])
        for a, v in zip(chunk, res.get("value", []) if isinstance(res, dict) else res):
            out[a] = v
    return out


def decode_curve(acct: dict | None, cfg: dict) -> dict | None:
    """Layout BondingCurve (Anchor): disc(8) vTok vSol rTok rSol supply (u64) complete (bool)."""
    if not acct:
        return None
    try:
        data = base64.b64decode(acct["data"][0])
        vtok, vsol, rtok, rsol, sup = struct.unpack_from("<QQQQQ", data, 8)
        (complete,) = struct.unpack_from("<?", data, 48)
    except (KeyError, IndexError, struct.error, ValueError):
        return None
    dec = cfg["token_decimals"]
    supply_raw = cfg["total_supply"] * 10 ** dec
    # sanidad: si el layout no es el esperado, los números salen absurdos -> None (INVALID DATA)
    plausible = 0 < vtok <= supply_raw * 1.2 and 0 < vsol < 10 ** 15 and sup in (supply_raw, 0)
    if not plausible and not complete:
        return None
    price_sol = (vsol / 1e9) / (vtok / 10 ** dec) if vtok else None
    prog = 1 - (rtok / 10 ** dec) / cfg["initial_real_token_reserves"]
    return {"price_sol": price_sol, "mc_sol": price_sol * cfg["total_supply"] if price_sol else None,
            "real_sol": rsol / 1e9, "progress": max(0.0, min(1.0, prog)), "complete": bool(complete)}


def mint_info(acct: dict | None, cfg: dict) -> dict:
    if not acct:
        return {"ok": False}
    try:
        info = acct["data"]["parsed"]["info"]
    except (KeyError, TypeError):
        return {"ok": False}
    exts = [e.get("extension") for e in info.get("extensions", []) or []]
    return {"ok": True, "program": acct.get("owner"),
            "mint_authority": info.get("mintAuthority"), "freeze_authority": info.get("freezeAuthority"),
            "extensions": exts,
            "dangerous_extensions": [e for e in exts if e not in cfg["benign_extensions"]]}
