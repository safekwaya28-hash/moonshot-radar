# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-18 04:48 UTC** · 1417 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 769 | 500 | 0.32x | 80% | 26% | 6% | 2% | 6% (n=724) | 4% (n=712) | 3% (n=473) |
| B | FUERA | 95 | 68 | 0.45x | 75% | 42% | 8% | 1% | 5% (n=75) | 6% (n=70) | 50% (n=2) |
| B | WATCH | 385 | 299 | 0.27x | 88% | 37% | 11% | 5% | 12% (n=315) | 9% (n=312) | 7% (n=223) |
| C-meta | 🟡 META ACTIVÁNDOSE | 167 | 79 | 0.86x | 30% | 23% | 7% | 2% | 48% (n=54) | 27% (n=33) | 16% (n=19) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 430 | 183 | 0.39x | 60% | 3% | 1% | 3% (n=393) | 2% (n=386) | 1% (n=272) |
| dev vendió | 190 | 176 | 0.31x | 92% | 9% | 3% | 8% (n=183) | 4% (n=179) | 6% (n=105) |
| compras en el bloque de creación | 141 | 133 | 0.27x | 89% | 9% | 4% | 9% (n=140) | 6% (n=139) | 6% (n=90) |
| volumen en bucle | 6 | 6 | 0.14x | 100% | 17% | 17% | 33% (n=6) | 0% (n=6) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
