# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-10 01:59 UTC** · 334 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 183 | 108 | 0.30x | 87% | 32% | 6% | 3% | 5% (n=171) | 4% (n=166) | 4% (n=106) |
| B | FUERA | 17 | 14 | 0.51x | 43% | 50% | 12% | 6% | 12% (n=16) | 18% (n=11) | 100% (n=1) |
| B | WATCH | 88 | 56 | 0.26x | 86% | 46% | 17% | 9% | 17% (n=70) | 14% (n=70) | 13% (n=47) |
| C-meta | 🟡 META ACTIVÁNDOSE | 45 | 14 | 0.74x | 43% | 19% | 10% | 2% | 40% (n=15) | 36% (n=11) | 17% (n=6) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 86 | 31 | 0.33x | 68% | 1% | 1% | 3% (n=74) | 0% (n=72) | 2% (n=48) |
| dev vendió | 63 | 50 | 0.30x | 94% | 8% | 3% | 5% (n=63) | 5% (n=60) | 6% (n=35) |
| compras en el bloque de creación | 31 | 24 | 0.25x | 96% | 13% | 3% | 10% (n=31) | 10% (n=31) | 5% (n=20) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
