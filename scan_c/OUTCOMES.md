# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-18 19:09 UTC** · 1484 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 807 | 513 | 0.32x | 79% | 26% | 5% | 2% | 6% (n=757) | 3% (n=744) | 3% (n=497) |
| B | FUERA | 99 | 75 | 0.44x | 76% | 41% | 8% | 1% | 5% (n=77) | 6% (n=72) | 50% (n=2) |
| B | WATCH | 403 | 308 | 0.26x | 88% | 35% | 11% | 4% | 12% (n=332) | 9% (n=329) | 6% (n=238) |
| C-meta | 🟡 META ACTIVÁNDOSE | 174 | 83 | 0.86x | 30% | 23% | 7% | 2% | 45% (n=55) | 26% (n=34) | 15% (n=20) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 456 | 191 | 0.39x | 60% | 3% | 1% | 3% (n=415) | 2% (n=409) | 1% (n=290) |
| dev vendió | 196 | 178 | 0.31x | 92% | 8% | 3% | 7% (n=189) | 4% (n=184) | 6% (n=109) |
| compras en el bloque de creación | 147 | 136 | 0.27x | 89% | 8% | 4% | 10% (n=145) | 6% (n=143) | 5% (n=92) |
| volumen en bucle | 6 | 6 | 0.14x | 100% | 17% | 17% | 33% (n=6) | 0% (n=6) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
