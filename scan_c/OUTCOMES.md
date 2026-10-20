# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-20 00:18 UTC** · 1631 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 888 | 549 | 0.32x | 79% | 25% | 5% | 2% | 5% (n=831) | 3% (n=820) | 3% (n=554) |
| B | FUERA | 113 | 83 | 0.44x | 76% | 43% | 8% | 1% | 6% (n=90) | 6% (n=84) | 50% (n=2) |
| B | WATCH | 444 | 341 | 0.26x | 89% | 37% | 11% | 4% | 13% (n=370) | 9% (n=366) | 6% (n=266) |
| C-meta | 🟡 META ACTIVÁNDOSE | 185 | 95 | 0.86x | 27% | 24% | 6% | 2% | 45% (n=60) | 25% (n=36) | 14% (n=22) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 509 | 209 | 0.38x | 60% | 3% | 1% | 3% (n=464) | 2% (n=458) | 1% (n=326) |
| dev vendió | 208 | 186 | 0.30x | 92% | 8% | 3% | 8% (n=199) | 5% (n=195) | 6% (n=117) |
| compras en el bloque de creación | 160 | 146 | 0.27x | 90% | 9% | 4% | 9% (n=159) | 6% (n=158) | 5% (n=105) |
| volumen en bucle | 9 | 6 | 0.14x | 100% | 11% | 11% | 29% (n=7) | 0% (n=7) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
