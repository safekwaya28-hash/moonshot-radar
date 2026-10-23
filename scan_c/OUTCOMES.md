# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-23 17:47 UTC** · 1903 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1033 | 638 | 0.32x | 78% | 24% | 6% | 2% | 5% (n=957) | 3% (n=945) | 3% (n=638) |
| B | FUERA | 134 | 105 | 0.44x | 78% | 46% | 8% | 1% | 6% (n=109) | 7% (n=103) | 33% (n=3) |
| B | WATCH | 503 | 401 | 0.26x | 90% | 38% | 12% | 5% | 12% (n=409) | 9% (n=406) | 6% (n=300) |
| C-meta | 🟡 META ACTIVÁNDOSE | 231 | 123 | 0.86x | 30% | 22% | 6% | 1% | 43% (n=70) | 25% (n=44) | 12% (n=26) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 611 | 256 | 0.40x | 58% | 4% | 1% | 3% (n=555) | 2% (n=549) | 1% (n=390) |
| dev vendió | 226 | 202 | 0.30x | 93% | 8% | 3% | 7% (n=212) | 4% (n=208) | 6% (n=125) |
| compras en el bloque de creación | 183 | 168 | 0.28x | 91% | 8% | 3% | 8% (n=177) | 6% (n=175) | 4% (n=115) |
| volumen en bucle | 11 | 10 | 0.29x | 90% | 9% | 9% | 18% (n=11) | 0% (n=11) | 0% (n=6) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
