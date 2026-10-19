# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-19 03:16 UTC** · 1542 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 834 | 517 | 0.32x | 79% | 25% | 5% | 2% | 5% (n=777) | 3% (n=766) | 3% (n=516) |
| B | FUERA | 108 | 76 | 0.44x | 76% | 38% | 7% | 1% | 5% (n=85) | 5% (n=79) | 50% (n=2) |
| B | WATCH | 422 | 313 | 0.26x | 88% | 35% | 11% | 4% | 12% (n=344) | 8% (n=340) | 6% (n=246) |
| C-meta | 🟡 META ACTIVÁNDOSE | 177 | 89 | 0.86x | 29% | 23% | 6% | 2% | 45% (n=55) | 26% (n=34) | 15% (n=20) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 474 | 194 | 0.39x | 59% | 3% | 1% | 3% (n=428) | 2% (n=422) | 1% (n=301) |
| dev vendió | 198 | 178 | 0.31x | 92% | 8% | 3% | 7% (n=191) | 4% (n=187) | 5% (n=112) |
| compras en el bloque de creación | 153 | 137 | 0.27x | 89% | 8% | 4% | 9% (n=150) | 6% (n=149) | 5% (n=97) |
| volumen en bucle | 7 | 6 | 0.14x | 100% | 14% | 14% | 33% (n=6) | 0% (n=6) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
