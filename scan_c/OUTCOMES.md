# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-22 14:59 UTC** · 1803 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 974 | 627 | 0.32x | 78% | 25% | 6% | 2% | 5% (n=912) | 3% (n=901) | 2% (n=607) |
| B | FUERA | 126 | 97 | 0.44x | 77% | 46% | 8% | 1% | 6% (n=102) | 6% (n=94) | 33% (n=3) |
| B | WATCH | 485 | 396 | 0.26x | 90% | 37% | 12% | 5% | 13% (n=397) | 9% (n=394) | 7% (n=289) |
| C-meta | 🟡 META ACTIVÁNDOSE | 216 | 114 | 0.86x | 29% | 23% | 6% | 2% | 45% (n=67) | 26% (n=42) | 12% (n=25) |
| C-meta | 🟢 CANDIDATA | 1 | 0 | —x | — | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 569 | 248 | 0.40x | 58% | 4% | 1% | 3% (n=522) | 2% (n=516) | 1% (n=366) |
| dev vendió | 217 | 200 | 0.30x | 92% | 8% | 3% | 7% (n=207) | 4% (n=203) | 6% (n=123) |
| compras en el bloque de creación | 176 | 167 | 0.28x | 91% | 8% | 4% | 8% (n=171) | 6% (n=170) | 5% (n=111) |
| volumen en bucle | 10 | 10 | 0.29x | 90% | 10% | 10% | 20% (n=10) | 0% (n=10) | 0% (n=5) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
