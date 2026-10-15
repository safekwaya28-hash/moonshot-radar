# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-15 04:50 UTC** · 1108 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 594 | 334 | 0.33x | 82% | 27% | 6% | 2% | 6% (n=534) | 4% (n=524) | 3% (n=334) |
| B | FUERA | 73 | 53 | 0.46x | 72% | 43% | 7% | 2% | 3% (n=59) | 4% (n=53) | 50% (n=2) |
| B | WATCH | 312 | 196 | 0.27x | 86% | 37% | 11% | 5% | 13% (n=247) | 10% (n=246) | 7% (n=168) |
| C-meta | 🟡 META ACTIVÁNDOSE | 128 | 57 | 0.85x | 33% | 23% | 6% | 1% | 44% (n=43) | 21% (n=28) | 6% (n=17) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 316 | 114 | 0.39x | 61% | 3% | 1% | 3% (n=270) | 2% (n=266) | 1% (n=178) |
| dev vendió | 165 | 132 | 0.33x | 92% | 10% | 4% | 7% (n=155) | 5% (n=151) | 7% (n=86) |
| compras en el bloque de creación | 107 | 82 | 0.27x | 91% | 8% | 5% | 9% (n=103) | 7% (n=101) | 6% (n=64) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
