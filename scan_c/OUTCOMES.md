# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-05 09:42 UTC** · 111 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | — | — | — |
| B | DESCARTAR | 71 | 35 | 0.29x | 89% | 42% | 10% | 3% | 11% (n=62) | 5% (n=59) | 3% (n=36) |
| B | FUERA | 7 | 5 | 0.52x | 40% | 50% | 17% | 17% | 17% (n=6) | 25% (n=4) | 100% (n=1) |
| B | WATCH | 23 | 14 | 0.16x | 93% | 33% | 10% | 5% | 10% (n=21) | 5% (n=21) | 7% (n=14) |
| C-meta | 🟡 META ACTIVÁNDOSE | 9 | 2 | 0.74x | 50% | 25% | 25% | 0% | 50% (n=4) | 50% (n=4) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 32 | 9 | 0.41x | 78% | 0% | 0% | 9% (n=23) | 0% (n=23) | 0% (n=14) |
| dev vendió | 22 | 14 | 0.28x | 86% | 9% | 5% | 9% (n=22) | 5% (n=19) | 8% (n=12) |
| compras en el bloque de creación | 15 | 10 | 0.24x | 100% | 20% | 0% | 13% (n=15) | 13% (n=15) | 0% (n=8) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | — | — | — |
| snipers | 1 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
