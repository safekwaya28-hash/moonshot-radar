# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-13 04:45 UTC** · 750 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 394 | 202 | 0.31x | 85% | 28% | 6% | 2% | 5% (n=373) | 4% (n=366) | 3% (n=230) |
| B | FUERA | 52 | 26 | 0.49x | 58% | 43% | 9% | 2% | 4% (n=46) | 5% (n=40) | 50% (n=2) |
| B | WATCH | 209 | 117 | 0.25x | 85% | 42% | 14% | 6% | 16% (n=166) | 13% (n=162) | 9% (n=112) |
| C-meta | 🟡 META ACTIVÁNDOSE | 94 | 33 | 0.82x | 36% | 24% | 7% | 1% | 44% (n=32) | 23% (n=22) | 7% (n=14) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 202 | 67 | 0.33x | 70% | 2% | 1% | 3% (n=184) | 1% (n=181) | 1% (n=119) |
| dev vendió | 117 | 86 | 0.31x | 91% | 11% | 4% | 6% (n=114) | 7% (n=110) | 8% (n=62) |
| compras en el bloque de creación | 69 | 45 | 0.26x | 96% | 7% | 1% | 7% (n=69) | 6% (n=69) | 2% (n=43) |
| volumen en bucle | 4 | 2 | 0.09x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 3 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=1) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 0 | —x | — | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
