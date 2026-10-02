# ESTUDIO · ¿qué entrada y qué forma de vender dan más 10x–50x cobrados?
**2026-10-02 05:30 UTC** · fuente: todas las graduadas de pump.fun (PumpSwap)

- Monedas revisadas: **1,239 / 206,007** (1%) · con pico ≥ $500k: **258**
- Entradas simuladas: **23 monedas** · **100% con < 180 días de datos después** (⚠️ con tanta censura el estudio todavía no puede afirmar nada sobre 50x)

## Ranking (EV = lo que multiplicas de media por operación, cobrado con esa regla de venta)

| # | Entrada | Venta | Ops | EV | IC 95% EV | EV sin top 3 | Mediana | p90 | Cobró ≥10x | Cobró ≥50x | ROI 10×50€ | Caída máx. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | REF_dd70_mc150k_sin_base | estructura | 13 | 1.04x | — | 0.89x ⚠️ | 1.20x | 1.52x | 0% | 0% | +10% | -9% |
| 2 | REF_dd85_mc150k_sin_base | estructura | 13 | 1.04x | — | 0.89x ⚠️ | 1.20x | 1.52x | 0% | 0% | +10% | -9% |
| 3 | TIPO_SOAP_pico200k_dd75_mc50k_72h_base | escalonada | 5 | 0.98x | — | 0.75x | 0.87x | 1.32x | 0% | 0% | -1% | -7% |
| 4 | TIPO_SOAP_pico200k_dd75_mc50k_72h_base | solo_stop | 5 | 0.98x | — | 0.75x | 0.87x | 1.32x | 0% | 0% | -1% | -7% |
| 5 | TIPO_SOAP_pico200k_dd75_mc50k_72h_base | trailing | 5 | 0.98x | — | 0.75x | 0.87x | 1.32x | 0% | 0% | -1% | -7% |
| 6 | TIPO_SOAP_pico200k_dd75_mc50k_72h_base | tuya | 5 | 0.98x | — | 0.75x | 0.87x | 1.32x | 0% | 0% | -1% | -7% |
| 7 | REF_dd70_mc150k_sin_base | escalonada | 13 | 0.98x | — | 0.85x | 0.96x | 1.30x | 0% | 0% | -3% | -15% |
| 8 | REF_dd70_mc150k_sin_base | solo_stop | 13 | 0.98x | — | 0.85x | 0.96x | 1.30x | 0% | 0% | -3% | -15% |
| 9 | REF_dd70_mc150k_sin_base | trailing | 13 | 0.98x | — | 0.85x | 0.96x | 1.30x | 0% | 0% | -3% | -15% |
| 10 | REF_dd70_mc150k_sin_base | tuya | 13 | 0.98x | — | 0.85x | 0.96x | 1.30x | 0% | 0% | -3% | -15% |
| 11 | REF_dd85_mc150k_sin_base | escalonada | 13 | 0.98x | — | 0.85x | 0.96x | 1.30x | 0% | 0% | -3% | -15% |
| 12 | REF_dd85_mc150k_sin_base | solo_stop | 13 | 0.98x | — | 0.85x | 0.96x | 1.30x | 0% | 0% | -3% | -15% |
| 13 | REF_dd85_mc150k_sin_base | trailing | 13 | 0.98x | — | 0.85x | 0.96x | 1.30x | 0% | 0% | -3% | -15% |
| 14 | REF_dd85_mc150k_sin_base | tuya | 13 | 0.98x | — | 0.85x | 0.96x | 1.30x | 0% | 0% | -3% | -15% |
| 15 | TIPO_SOAP_pico200k_dd75_mc50k_72h_base | estructura | 5 | 0.94x | — | 0.47x | 0.74x | 1.52x | 0% | 0% | -3% | -6% |
| 16 | dd70_mc150k_72h_base ⭐ | tuya | 3 | 1.13x | — | — | 0.93x | 1.46x | 0% | 0% | +4% | -2% |

⭐ = tus reglas actuales. ⚠️ = el EV pasa de ganar a perder quitando las 3 mejores: es suerte, no estrategia.
EV > 1x = gana de media. Solo filas con ≥ 5 operaciones (con menos de ~30 los números bailan mucho).
Detalle completo: `STUDY_DIST.md` (distribución) y `STUDY_REGIME.md` (por trimestre).

## Reglas

**Entrada** (se comprueba hora a hora, solo con datos de ese momento):
- ATH de MC hasta ese momento ≥ $500k (MC = precio × 1.000M); caída desde el ATH ≥ 70% / 85%; MC ≤ $150k / $50k.
- Base `plana`: cierres horarios de las últimas 72 h / 7 días dentro de ±25% de su mediana (mín. 1 vela cada 6 h).
- Base `acum` (acumulación): precio dentro de ±30% en 72 h **y** volumen de esas 72 h ≥ 1,5× el de los 7 días anteriores.
- `base` = entra en la primera hora que se cumple · `ruptura` = primer cierre por encima del techo de la base con volumen ≥ 3× la mediana de la base, en ≤ 14 días (si antes pierde el suelo, no entra).
- `REF_…_sin_base` = sin exigir base (para ver si la base aporta algo). Una entrada por moneda y variante.
- `TIPO_SOAP_…` = variante tipo Soap: pico ≥ $200k, caída ≥ 75%, MC ≤ $50k, base plana 72 h (entrar en base o en ruptura). Aproxima lo que él describe en público; NO es una reproducción exacta ni está verificado que opere así.

**Venta** (se decide cada día al cierre, solo con datos hasta ese día):
- `tuya`: 1/3 a 3×; el resto al primer cierre diario por debajo del suelo de la base.
- `solo_stop`: todo al primer cierre diario bajo el suelo; nunca vende antes.
- `trailing`: stop en el suelo; al tocar 5× se activa un stop que sube: sale si el cierre cae más de 2.5× la volatilidad diaria media (14 días, en %) desde el máximo cierre (distancia entre 15% y 60%).
- `escalonada`: 15% a 3×, 15% a 10×, 15% a 25×; el 55% restante con el mismo stop que `trailing`.
- `estructura`: sale al cerrar por debajo del mínimo de los 7 días anteriores con volumen ≥ 2× su media.
- Si no ha salido, se valora al último precio. Las ventas parciales se cuentan al múltiplo exacto (ligeramente optimista).

**Qué no mide:** retención de holders, compras/ventas, top traders y comunidad (se miden en vivo con el radar). GeckoTerminal da ~6 meses de historial: los 50x lentos quedan cortados (ver % de censura).
