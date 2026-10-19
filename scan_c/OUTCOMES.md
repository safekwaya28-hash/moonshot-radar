# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-19 08:10 UTC** · 1571 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 852 | 519 | 0.32x | 79% | 25% | 5% | 2% | 6% (n=789) | 3% (n=777) | 3% (n=524) |
| B | FUERA | 111 | 77 | 0.44x | 75% | 40% | 7% | 1% | 5% (n=87) | 5% (n=81) | 50% (n=2) |
| B | WATCH | 427 | 316 | 0.26x | 89% | 36% | 11% | 4% | 12% (n=351) | 8% (n=348) | 6% (n=250) |
| C-meta | 🟡 META ACTIVÁNDOSE | 180 | 90 | 0.86x | 29% | 23% | 6% | 2% | 46% (n=57) | 26% (n=35) | 14% (n=21) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 488 | 195 | 0.39x | 59% | 3% | 1% | 3% (n=435) | 2% (n=428) | 1% (n=306) |
| dev vendió | 199 | 178 | 0.31x | 92% | 9% | 4% | 8% (n=192) | 5% (n=188) | 6% (n=113) |
| compras en el bloque de creación | 156 | 138 | 0.27x | 89% | 8% | 4% | 9% (n=153) | 6% (n=152) | 5% (n=99) |
| volumen en bucle | 7 | 6 | 0.14x | 100% | 14% | 14% | 29% (n=7) | 0% (n=7) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
