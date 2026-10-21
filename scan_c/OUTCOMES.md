# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-21 04:50 UTC** · 1727 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 940 | 593 | 0.32x | 79% | 25% | 5% | 2% | 5% (n=883) | 3% (n=872) | 3% (n=588) |
| B | FUERA | 120 | 93 | 0.44x | 77% | 44% | 7% | 1% | 6% (n=96) | 6% (n=89) | 33% (n=3) |
| B | WATCH | 468 | 376 | 0.26x | 90% | 38% | 12% | 5% | 13% (n=386) | 9% (n=383) | 6% (n=282) |
| C-meta | 🟡 META ACTIVÁNDOSE | 198 | 101 | 0.85x | 30% | 24% | 6% | 2% | 45% (n=65) | 25% (n=40) | 12% (n=25) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 546 | 230 | 0.38x | 60% | 3% | 1% | 3% (n=501) | 2% (n=495) | 1% (n=352) |
| dev vendió | 213 | 195 | 0.30x | 93% | 8% | 3% | 7% (n=205) | 4% (n=201) | 6% (n=121) |
| compras en el bloque de creación | 170 | 157 | 0.28x | 90% | 8% | 4% | 8% (n=167) | 6% (n=166) | 5% (n=109) |
| volumen en bucle | 9 | 9 | 0.34x | 89% | 11% | 11% | 25% (n=8) | 0% (n=8) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
