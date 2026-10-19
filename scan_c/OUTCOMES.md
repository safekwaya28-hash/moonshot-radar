# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-19 07:21 UTC** · 1565 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 848 | 518 | 0.32x | 79% | 24% | 5% | 2% | 5% (n=781) | 3% (n=770) | 3% (n=518) |
| B | FUERA | 111 | 76 | 0.44x | 76% | 39% | 7% | 1% | 5% (n=86) | 5% (n=80) | 50% (n=2) |
| B | WATCH | 426 | 315 | 0.26x | 89% | 35% | 11% | 4% | 12% (n=347) | 8% (n=343) | 6% (n=247) |
| C-meta | 🟡 META ACTIVÁNDOSE | 179 | 90 | 0.86x | 29% | 23% | 6% | 2% | 46% (n=56) | 26% (n=34) | 15% (n=20) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 485 | 194 | 0.39x | 59% | 3% | 1% | 3% (n=430) | 2% (n=424) | 1% (n=302) |
| dev vendió | 199 | 178 | 0.31x | 92% | 9% | 4% | 7% (n=191) | 4% (n=187) | 5% (n=112) |
| compras en el bloque de creación | 155 | 138 | 0.27x | 89% | 8% | 4% | 9% (n=151) | 6% (n=150) | 5% (n=98) |
| volumen en bucle | 7 | 6 | 0.14x | 100% | 14% | 14% | 29% (n=7) | 0% (n=7) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
