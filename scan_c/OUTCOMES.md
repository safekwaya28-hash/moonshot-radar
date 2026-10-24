# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-24 21:53 UTC** · 1937 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1041 | 674 | 0.33x | 77% | 25% | 6% | 2% | 5% (n=972) | 3% (n=960) | 2% (n=649) |
| B | FUERA | 136 | 110 | 0.44x | 76% | 47% | 9% | 1% | 6% (n=111) | 7% (n=105) | 33% (n=3) |
| B | WATCH | 512 | 409 | 0.26x | 90% | 38% | 11% | 5% | 12% (n=417) | 8% (n=414) | 6% (n=306) |
| C-meta | 🟡 META ACTIVÁNDOSE | 246 | 133 | 0.86x | 30% | 22% | 6% | 2% | 42% (n=74) | 22% (n=49) | 10% (n=29) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 613 | 279 | 0.41x | 56% | 4% | 1% | 3% (n=563) | 2% (n=557) | 1% (n=395) |
| dev vendió | 232 | 209 | 0.30x | 92% | 8% | 3% | 7% (n=219) | 4% (n=214) | 5% (n=130) |
| compras en el bloque de creación | 183 | 173 | 0.28x | 91% | 8% | 3% | 8% (n=177) | 6% (n=176) | 4% (n=116) |
| volumen en bucle | 11 | 11 | 0.34x | 91% | 9% | 9% | 18% (n=11) | 0% (n=11) | 0% (n=6) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
