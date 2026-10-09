# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-09 17:33 UTC** · 306 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 169 | 94 | 0.29x | 88% | 33% | 6% | 3% | 6% (n=158) | 3% (n=155) | 3% (n=96) |
| B | FUERA | 17 | 12 | 0.51x | 42% | 50% | 6% | 6% | 12% (n=16) | 10% (n=10) | 100% (n=1) |
| B | WATCH | 80 | 45 | 0.26x | 89% | 43% | 15% | 8% | 15% (n=65) | 12% (n=65) | 12% (n=43) |
| C-meta | 🟡 META ACTIVÁNDOSE | 39 | 14 | 0.74x | 43% | 21% | 11% | 3% | 43% (n=14) | 40% (n=10) | 17% (n=6) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 76 | 23 | 0.33x | 70% | 2% | 2% | 3% (n=65) | 0% (n=65) | 2% (n=44) |
| dev vendió | 60 | 46 | 0.29x | 93% | 7% | 2% | 5% (n=60) | 4% (n=57) | 3% (n=30) |
| compras en el bloque de creación | 30 | 22 | 0.25x | 95% | 13% | 3% | 10% (n=30) | 10% (n=30) | 5% (n=19) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
