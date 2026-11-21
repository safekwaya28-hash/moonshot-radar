# ESTUDIO · ¿qué entrada y qué forma de vender dan más 10x–50x cobrados?
**2026-11-21 02:17 UTC** · fuente: todas las graduadas de pump.fun (PumpSwap)

- Monedas revisadas: **56,476 / 206,007** (27%) · con pico ≥ $500k: **11,617**
- Entradas simuladas: **1,064 monedas** · **100% con < 180 días de datos después** (⚠️ con tanta censura el estudio todavía no puede afirmar nada sobre 50x)

## Ranking (EV = lo que multiplicas de media por operación, cobrado con esa regla de venta)

| # | Entrada | Venta | Ops | EV | IC 95% EV | EV sin top 3 | Mediana | p90 | Cobró ≥10x | Cobró ≥50x | ROI 10×50€ | Caída máx. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | dd70_mc50k_72h_base | trailing | 131 | 2.48x | 0.75x–3.81x | 0.95x ⚠️ | 0.95x | 1.21x | 1% | 1% | -22% | -26% |
| 2 | dd85_mc50k_72h_base | trailing | 131 | 2.48x | 0.75x–3.81x | 0.95x ⚠️ | 0.95x | 1.21x | 1% | 1% | -22% | -26% |
| 3 | dd85_mc150k_72h_base | trailing | 136 | 2.42x | 0.75x–3.68x | 0.94x ⚠️ | 0.94x | 1.21x | 1% | 1% | +1979% | -25% |
| 4 | dd70_mc150k_72h_base | trailing | 138 | 2.40x | 0.75x–3.65x | 0.94x ⚠️ | 0.94x | 1.21x | 1% | 1% | +1979% | -25% |
| 5 | dd70_mc50k_72h_base | escalonada | 131 | 1.85x | 0.75x–2.62x | 0.96x ⚠️ | 0.95x | 1.23x | 1% | 1% | -19% | -22% |
| 6 | dd85_mc50k_72h_base | escalonada | 131 | 1.85x | 0.75x–2.62x | 0.96x ⚠️ | 0.95x | 1.23x | 1% | 1% | -19% | -22% |
| 7 | dd85_mc150k_72h_base | escalonada | 136 | 1.81x | 0.75x–2.54x | 0.95x ⚠️ | 0.95x | 1.22x | 1% | 1% | +1136% | -22% |
| 8 | dd70_mc150k_72h_base | escalonada | 138 | 1.80x | 0.75x–2.51x | 0.95x ⚠️ | 0.95x | 1.22x | 1% | 1% | +1136% | -22% |
| 9 | TIPO_SOAP_pico200k_dd75_mc50k_72h_base | trailing | 290 | 1.65x | 0.88x–2.23x | 0.95x ⚠️ | 0.95x | 1.19x | 0% | 0% | +2% | -21% |
| 10 | REF_dd85_mc150k_sin_base | trailing | 482 | 1.45x | 0.82x–1.96x | 1.00x ⚠️ | 0.98x | 1.27x | 0% | 0% | +35% | -27% |
| 11 | REF_dd70_mc150k_sin_base | trailing | 488 | 1.44x | 0.79x–1.95x | 0.99x ⚠️ | 0.98x | 1.27x | 0% | 0% | -22% | -27% |
| 12 | TIPO_SOAP_pico200k_dd75_mc50k_72h_base | escalonada | 290 | 1.38x | 0.90x–1.72x | 0.97x ⚠️ | 0.96x | 1.22x | 0% | 0% | +7% | -18% |
| 13 | REF_dd85_mc150k_sin_base | escalonada | 482 | 1.29x | 0.87x–1.57x | 1.01x | 0.98x | 1.28x | 0% | 0% | +60% | -23% |
| 14 | REF_dd70_mc150k_sin_base | escalonada | 488 | 1.28x | 0.79x–1.56x | 1.00x | 0.98x | 1.28x | 0% | 0% | -10% | -23% |
| 15 | dd70_mc50k_72h_acum | tuya | 19 | 1.04x | 0.74x–1.12x | 0.95x ⚠️ | 0.94x | 1.25x | 0% | 0% | +11% | -4% |
| 16 | dd70_mc150k_72h_base ⭐ | tuya | 138 | 0.98x | 0.75x–0.98x | 0.96x | 0.95x | 1.25x | 0% | 0% | -6% | -20% |

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
