# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-27 19:01 UTC** · 2007 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1064 | 688 | 0.33x | 77% | 25% | 6% | 2% | 5% (n=983) | 3% (n=972) | 2% (n=657) |
| B | FUERA | 144 | 112 | 0.44x | 77% | 46% | 9% | 1% | 6% (n=112) | 7% (n=106) | 33% (n=3) |
| B | WATCH | 532 | 422 | 0.26x | 90% | 38% | 11% | 5% | 12% (n=424) | 8% (n=421) | 6% (n=314) |
| C-meta | 🟡 META ACTIVÁNDOSE | 265 | 150 | 0.86x | 29% | 24% | 7% | 2% | 41% (n=83) | 25% (n=55) | 13% (n=31) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 629 | 285 | 0.42x | 55% | 4% | 1% | 3% (n=568) | 2% (n=562) | 1% (n=399) |
| dev vendió | 234 | 213 | 0.29x | 92% | 9% | 3% | 7% (n=220) | 5% (n=216) | 5% (n=131) |
| compras en el bloque de creación | 188 | 177 | 0.28x | 91% | 8% | 3% | 8% (n=182) | 6% (n=181) | 4% (n=119) |
| volumen en bucle | 11 | 11 | 0.34x | 91% | 9% | 9% | 18% (n=11) | 0% (n=11) | 0% (n=6) |
| impuesto modificable | 5 | 5 | 0.77x | 20% | 0% | 0% | 20% (n=5) | 0% (n=3) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
