# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-04 10:57 UTC** · 87 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | — | — | — |
| B | DESCARTAR | 56 | 27 | 0.26x | 89% | 44% | 10% | 4% | 12% (n=48) | 7% (n=45) | 4% (n=27) |
| B | FUERA | 7 | 3 | 0.52x | 33% | 33% | 0% | 0% | 0% (n=5) | 0% (n=3) | — |
| B | WATCH | 17 | 12 | 0.25x | 92% | 40% | 7% | 0% | 7% (n=15) | 0% (n=15) | 0% (n=9) |
| C-meta | 🟡 META ACTIVÁNDOSE | 6 | 2 | 0.74x | 50% | 20% | 20% | 0% | 50% (n=2) | 50% (n=2) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 26 | 6 | 0.44x | 83% | 0% | 0% | 11% (n=18) | 0% (n=17) | 0% (n=10) |
| dev vendió | 16 | 9 | 0.26x | 78% | 6% | 6% | 6% (n=16) | 7% (n=14) | 12% (n=8) |
| compras en el bloque de creación | 12 | 10 | 0.24x | 100% | 25% | 0% | 17% (n=12) | 17% (n=12) | 0% (n=7) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | — | — | — |
| snipers | 1 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
