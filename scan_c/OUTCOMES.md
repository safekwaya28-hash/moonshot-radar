# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-17 05:53 UTC** · 1337 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 733 | 484 | 0.32x | 80% | 27% | 6% | 2% | 6% (n=688) | 4% (n=675) | 3% (n=444) |
| B | FUERA | 86 | 66 | 0.45x | 74% | 43% | 9% | 1% | 6% (n=68) | 6% (n=62) | 50% (n=2) |
| B | WATCH | 368 | 296 | 0.27x | 88% | 37% | 11% | 5% | 13% (n=301) | 9% (n=298) | 7% (n=213) |
| C-meta | 🟡 META ACTIVÁNDOSE | 149 | 74 | 0.85x | 32% | 23% | 6% | 2% | 46% (n=46) | 23% (n=30) | 11% (n=18) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 401 | 175 | 0.39x | 60% | 4% | 1% | 3% (n=364) | 2% (n=358) | 1% (n=250) |
| dev vendió | 188 | 173 | 0.31x | 92% | 9% | 3% | 7% (n=181) | 5% (n=175) | 6% (n=102) |
| compras en el bloque de creación | 136 | 130 | 0.27x | 89% | 9% | 4% | 10% (n=135) | 7% (n=134) | 6% (n=86) |
| volumen en bucle | 6 | 4 | 0.12x | 100% | 17% | 17% | 33% (n=6) | 0% (n=6) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
