# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-17 10:51 UTC** · 1354 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 740 | 485 | 0.32x | 80% | 27% | 6% | 2% | 6% (n=695) | 4% (n=683) | 3% (n=449) |
| B | FUERA | 88 | 66 | 0.45x | 74% | 43% | 9% | 1% | 6% (n=70) | 6% (n=64) | 50% (n=2) |
| B | WATCH | 369 | 296 | 0.27x | 88% | 37% | 11% | 5% | 13% (n=302) | 9% (n=299) | 7% (n=213) |
| C-meta | 🟡 META ACTIVÁNDOSE | 156 | 76 | 0.86x | 32% | 22% | 6% | 1% | 46% (n=46) | 23% (n=30) | 11% (n=18) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 406 | 176 | 0.39x | 60% | 4% | 1% | 3% (n=369) | 2% (n=363) | 1% (n=255) |
| dev vendió | 189 | 173 | 0.31x | 92% | 9% | 3% | 8% (n=182) | 5% (n=177) | 6% (n=102) |
| compras en el bloque de creación | 137 | 130 | 0.27x | 89% | 9% | 4% | 10% (n=136) | 7% (n=135) | 6% (n=86) |
| volumen en bucle | 6 | 4 | 0.12x | 100% | 17% | 17% | 33% (n=6) | 0% (n=6) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
