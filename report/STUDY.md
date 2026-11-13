# ESTUDIO · ¿qué entrada y qué forma de vender dan más 10x–50x cobrados?
**2026-11-13 22:39 UTC** · fuente: todas las graduadas de pump.fun (PumpSwap)

- Monedas revisadas: **54,372 / 206,007** (26%) · con pico ≥ $500k: **11,203**
- Entradas simuladas: **1,046 monedas** · **100% con < 180 días de datos después** (⚠️ con tanta censura el estudio todavía no puede afirmar nada sobre 50x)

## Ranking (EV = lo que multiplicas de media por operación, cobrado con esa regla de venta)

| # | Entrada | Venta | Ops | EV | IC 95% EV | EV sin top 3 | Mediana | p90 | Cobró ≥10x | Cobró ≥50x | ROI 10×50€ | Caída máx. |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | dd70_mc50k_72h_base | trailing | 126 | 2.55x | 0.72x–3.85x | 0.95x ⚠️ | 0.95x | 1.22x | 1% | 1% | -25% | -31% |
| 2 | dd85_mc50k_72h_base | trailing | 126 | 2.55x | 0.72x–3.85x | 0.95x ⚠️ | 0.95x | 1.22x | 1% | 1% | -25% | -31% |
| 3 | dd85_mc150k_72h_base | trailing | 131 | 2.48x | 0.72x–3.72x | 0.94x ⚠️ | 0.95x | 1.21x | 1% | 1% | +1968% | -38% |
| 4 | dd70_mc150k_72h_base | trailing | 133 | 2.46x | 0.72x–3.68x | 0.94x ⚠️ | 0.95x | 1.21x | 1% | 1% | +1968% | -38% |
| 5 | dd70_mc50k_72h_base | escalonada | 126 | 1.89x | 0.72x–2.64x | 0.96x ⚠️ | 0.95x | 1.27x | 1% | 1% | -21% | -28% |
| 6 | dd85_mc50k_72h_base | escalonada | 126 | 1.89x | 0.72x–2.64x | 0.96x ⚠️ | 0.95x | 1.27x | 1% | 1% | -21% | -28% |
| 7 | dd85_mc150k_72h_base | escalonada | 131 | 1.85x | 0.72x–2.56x | 0.95x ⚠️ | 0.95x | 1.23x | 1% | 1% | +1125% | -35% |
| 8 | dd70_mc150k_72h_base | escalonada | 133 | 1.83x | 0.72x–2.54x | 0.95x ⚠️ | 0.95x | 1.22x | 1% | 1% | +1125% | -35% |
| 9 | TIPO_SOAP_pico200k_dd75_mc50k_72h_base | trailing | 281 | 1.68x | 0.90x–2.27x | 0.96x ⚠️ | 0.95x | 1.19x | 0% | 0% | +20% | -21% |
| 10 | REF_dd85_mc150k_sin_base | trailing | 469 | 1.46x | 0.82x–2.01x | 0.99x ⚠️ | 0.98x | 1.27x | 0% | 0% | +79% | -27% |
| 11 | REF_dd70_mc150k_sin_base | trailing | 475 | 1.45x | 0.79x–1.99x | 0.98x ⚠️ | 0.98x | 1.27x | 0% | 0% | +68% | -28% |
| 12 | TIPO_SOAP_pico200k_dd75_mc50k_72h_base | escalonada | 281 | 1.40x | 0.92x–1.75x | 0.97x ⚠️ | 0.96x | 1.22x | 0% | 0% | +25% | -18% |
| 13 | REF_dd85_mc150k_sin_base | escalonada | 469 | 1.29x | 0.87x–1.60x | 1.01x | 0.98x | 1.28x | 0% | 0% | +94% | -23% |
| 14 | REF_dd70_mc150k_sin_base | escalonada | 475 | 1.28x | 0.79x–1.59x | 1.00x | 0.98x | 1.28x | 0% | 0% | +72% | -23% |
| 15 | dd70_mc150k_168h_ruptura | estructura | 15 | 1.07x | 1.05x–1.09x | 1.00x | 1.09x | 1.29x | 0% | 0% | +8% | -4% |
| 16 | dd70_mc150k_72h_base ⭐ | tuya | 133 | 0.98x | 0.72x–0.99x | 0.96x | 0.95x | 1.30x | 0% | 0% | -17% | -31% |

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
