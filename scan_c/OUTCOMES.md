# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-23 07:12 UTC** · 1877 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1017 | 631 | 0.32x | 79% | 24% | 5% | 2% | 5% (n=950) | 3% (n=937) | 3% (n=632) |
| B | FUERA | 132 | 99 | 0.44x | 77% | 46% | 7% | 1% | 6% (n=108) | 6% (n=102) | 33% (n=3) |
| B | WATCH | 500 | 397 | 0.26x | 90% | 38% | 12% | 5% | 13% (n=407) | 9% (n=404) | 6% (n=298) |
| C-meta | 🟡 META ACTIVÁNDOSE | 226 | 120 | 0.86x | 30% | 22% | 6% | 2% | 43% (n=70) | 25% (n=44) | 12% (n=26) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 598 | 252 | 0.39x | 59% | 4% | 1% | 3% (n=549) | 2% (n=543) | 1% (n=387) |
| dev vendió | 224 | 200 | 0.30x | 92% | 8% | 3% | 7% (n=212) | 4% (n=208) | 6% (n=125) |
| compras en el bloque de creación | 182 | 167 | 0.28x | 91% | 8% | 3% | 9% (n=176) | 6% (n=173) | 4% (n=113) |
| volumen en bucle | 11 | 10 | 0.29x | 90% | 9% | 9% | 18% (n=11) | 0% (n=11) | 0% (n=5) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
