# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-13 03:46 UTC** · 740 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 387 | 199 | 0.31x | 85% | 28% | 6% | 2% | 5% (n=366) | 4% (n=360) | 3% (n=225) |
| B | FUERA | 50 | 25 | 0.48x | 60% | 45% | 9% | 2% | 5% (n=44) | 5% (n=38) | 50% (n=2) |
| B | WATCH | 208 | 114 | 0.25x | 84% | 42% | 14% | 6% | 16% (n=166) | 13% (n=162) | 9% (n=112) |
| C-meta | 🟡 META ACTIVÁNDOSE | 94 | 32 | 0.80x | 38% | 24% | 7% | 1% | 44% (n=32) | 24% (n=21) | 7% (n=14) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 197 | 67 | 0.33x | 70% | 2% | 1% | 2% (n=179) | 1% (n=177) | 1% (n=115) |
| dev vendió | 117 | 84 | 0.31x | 90% | 11% | 4% | 6% (n=114) | 7% (n=110) | 8% (n=62) |
| compras en el bloque de creación | 67 | 44 | 0.26x | 95% | 7% | 1% | 7% (n=67) | 6% (n=67) | 2% (n=42) |
| volumen en bucle | 4 | 2 | 0.09x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 3 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=3) | 0% (n=1) | 0% (n=1) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 0 | —x | — | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
