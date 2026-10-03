# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-03 01:00 UTC** · 43 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | — | — | — |
| B | DESCARTAR | 24 | 6 | 0.32x | 83% | 50% | 0% | 0% | 14% (n=14) | 0% (n=11) | 0% (n=6) |
| B | FUERA | 4 | 1 | 0.52x | 0% | 33% | 0% | 0% | 0% (n=2) | 0% (n=1) | — |
| B | WATCH | 11 | 4 | 0.26x | 100% | 44% | 11% | 0% | 0% (n=9) | 0% (n=9) | 0% (n=4) |
| C-meta | 🟡 META ACTIVÁNDOSE | 3 | 1 | 0.46x | 100% | 50% | 50% | 0% | 50% (n=2) | 50% (n=2) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 11 | 1 | 0.33x | 100% | 0% | 0% | 100% (n=1) | 0% (n=1) | 0% (n=1) |
| dev vendió | 9 | 4 | 0.35x | 75% | 0% | 0% | 11% (n=9) | 0% (n=6) | 0% (n=3) |
| compras en el bloque de creación | 4 | 1 | 0.23x | 100% | 0% | 0% | 0% (n=4) | 0% (n=4) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
