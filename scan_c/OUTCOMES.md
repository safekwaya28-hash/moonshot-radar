# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-05 22:02 UTC** · 132 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | — | — |
| B | DESCARTAR | 84 | 43 | 0.29x | 88% | 36% | 9% | 3% | 8% (n=75) | 4% (n=73) | 2% (n=45) |
| B | FUERA | 7 | 5 | 0.52x | 40% | 50% | 17% | 17% | 17% (n=6) | 25% (n=4) | 100% (n=1) |
| B | WATCH | 26 | 18 | 0.18x | 89% | 33% | 8% | 4% | 9% (n=23) | 4% (n=23) | 7% (n=15) |
| C-meta | 🟡 META ACTIVÁNDOSE | 14 | 2 | 0.74x | 50% | 15% | 15% | 0% | 20% (n=5) | 40% (n=5) | 0% (n=2) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 37 | 10 | 0.37x | 80% | 0% | 0% | 7% (n=28) | 0% (n=28) | 0% (n=17) |
| dev vendió | 28 | 18 | 0.28x | 83% | 11% | 4% | 4% (n=28) | 4% (n=26) | 6% (n=16) |
| compras en el bloque de creación | 17 | 13 | 0.24x | 100% | 18% | 0% | 12% (n=17) | 12% (n=17) | 0% (n=10) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | — | — |
| snipers | 1 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
