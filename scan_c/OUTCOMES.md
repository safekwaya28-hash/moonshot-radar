# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-19 14:01 UTC** · 1590 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 864 | 530 | 0.32x | 79% | 25% | 5% | 2% | 6% (n=796) | 3% (n=784) | 3% (n=529) |
| B | FUERA | 112 | 77 | 0.44x | 75% | 41% | 7% | 1% | 4% (n=89) | 5% (n=83) | 50% (n=2) |
| B | WATCH | 433 | 323 | 0.26x | 89% | 36% | 11% | 4% | 12% (n=353) | 8% (n=349) | 6% (n=252) |
| C-meta | 🟡 META ACTIVÁNDOSE | 180 | 91 | 0.86x | 29% | 24% | 6% | 2% | 44% (n=59) | 25% (n=36) | 14% (n=22) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 498 | 200 | 0.39x | 60% | 3% | 1% | 3% (n=441) | 2% (n=434) | 1% (n=310) |
| dev vendió | 200 | 181 | 0.31x | 92% | 9% | 4% | 8% (n=192) | 5% (n=188) | 6% (n=113) |
| compras en el bloque de creación | 157 | 141 | 0.27x | 89% | 8% | 4% | 9% (n=154) | 6% (n=153) | 5% (n=100) |
| volumen en bucle | 7 | 6 | 0.14x | 100% | 14% | 14% | 29% (n=7) | 0% (n=7) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
