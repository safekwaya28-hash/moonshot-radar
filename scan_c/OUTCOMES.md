# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-04 02:19 UTC** · 86 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | — | — | — |
| B | DESCARTAR | 56 | 15 | 0.26x | 93% | 43% | 11% | 4% | 13% (n=45) | 7% (n=41) | 4% (n=27) |
| B | FUERA | 6 | 3 | 0.52x | 33% | 40% | 0% | 0% | 0% (n=4) | 0% (n=3) | — |
| B | WATCH | 17 | 9 | 0.15x | 89% | 40% | 7% | 0% | 8% (n=13) | 0% (n=13) | 0% (n=7) |
| C-meta | 🟡 META ACTIVÁNDOSE | 6 | 1 | 0.46x | 100% | 20% | 20% | 0% | 50% (n=2) | 50% (n=2) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 26 | 1 | 0.33x | 100% | 0% | 0% | 12% (n=16) | 0% (n=14) | 0% (n=10) |
| dev vendió | 16 | 7 | 0.26x | 86% | 6% | 6% | 6% (n=16) | 7% (n=14) | 12% (n=8) |
| compras en el bloque de creación | 12 | 6 | 0.24x | 100% | 25% | 0% | 18% (n=11) | 18% (n=11) | 0% (n=7) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | — | — | — |
| snipers | 1 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| volumen en bucle | 1 | 0 | —x | — | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
