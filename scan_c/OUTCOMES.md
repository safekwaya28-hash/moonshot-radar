# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-12 08:42 UTC** · 589 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 306 | 181 | 0.31x | 85% | 29% | 5% | 2% | 5% (n=291) | 3% (n=283) | 3% (n=173) |
| B | FUERA | 37 | 22 | 0.49x | 55% | 47% | 12% | 3% | 6% (n=34) | 9% (n=22) | 100% (n=1) |
| B | WATCH | 162 | 105 | 0.26x | 84% | 40% | 15% | 6% | 15% (n=130) | 13% (n=128) | 9% (n=87) |
| C-meta | 🟡 META ACTIVÁNDOSE | 83 | 26 | 0.82x | 38% | 21% | 7% | 1% | 48% (n=25) | 31% (n=16) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 155 | 59 | 0.33x | 69% | 1% | 1% | 3% (n=142) | 1% (n=139) | 1% (n=89) |
| dev vendió | 94 | 76 | 0.30x | 91% | 10% | 3% | 4% (n=92) | 5% (n=88) | 6% (n=50) |
| compras en el bloque de creación | 51 | 42 | 0.26x | 95% | 8% | 2% | 8% (n=51) | 6% (n=50) | 4% (n=28) |
| volumen en bucle | 4 | 2 | 0.09x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 0 | —x | — | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
