# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-04 14:59 UTC** · 92 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | — | — | — |
| B | DESCARTAR | 59 | 30 | 0.28x | 90% | 44% | 10% | 4% | 12% (n=50) | 6% (n=47) | 4% (n=27) |
| B | FUERA | 7 | 3 | 0.52x | 33% | 50% | 17% | 17% | 17% (n=6) | 25% (n=4) | 100% (n=1) |
| B | WATCH | 19 | 12 | 0.25x | 92% | 41% | 12% | 6% | 12% (n=17) | 6% (n=17) | 9% (n=11) |
| C-meta | 🟡 META ACTIVÁNDOSE | 6 | 2 | 0.74x | 50% | 20% | 20% | 0% | 50% (n=2) | 50% (n=2) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 27 | 7 | 0.41x | 86% | 0% | 0% | 11% (n=18) | 0% (n=17) | 0% (n=10) |
| dev vendió | 16 | 11 | 0.26x | 82% | 6% | 6% | 6% (n=16) | 7% (n=14) | 12% (n=8) |
| compras en el bloque de creación | 14 | 10 | 0.24x | 100% | 21% | 0% | 14% (n=14) | 14% (n=14) | 0% (n=7) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | — | — | — |
| snipers | 1 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
