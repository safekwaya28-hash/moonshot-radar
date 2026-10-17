# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-17 00:59 UTC** · 1315 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 720 | 471 | 0.32x | 80% | 26% | 6% | 2% | 6% (n=672) | 4% (n=659) | 3% (n=435) |
| B | FUERA | 85 | 66 | 0.45x | 74% | 43% | 9% | 1% | 6% (n=67) | 6% (n=62) | 50% (n=2) |
| B | WATCH | 362 | 286 | 0.27x | 88% | 37% | 11% | 5% | 13% (n=299) | 9% (n=296) | 7% (n=211) |
| C-meta | 🟡 META ACTIVÁNDOSE | 147 | 71 | 0.86x | 31% | 23% | 6% | 2% | 46% (n=46) | 23% (n=30) | 11% (n=18) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 394 | 168 | 0.39x | 60% | 3% | 1% | 3% (n=355) | 2% (n=349) | 1% (n=244) |
| dev vendió | 185 | 170 | 0.31x | 92% | 9% | 3% | 7% (n=178) | 5% (n=172) | 6% (n=100) |
| compras en el bloque de creación | 135 | 127 | 0.27x | 89% | 9% | 4% | 10% (n=133) | 7% (n=132) | 6% (n=85) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
