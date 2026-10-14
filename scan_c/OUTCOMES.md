# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-14 17:57 UTC** · 1018 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 539 | 324 | 0.33x | 82% | 26% | 6% | 2% | 6% (n=472) | 4% (n=465) | 3% (n=292) |
| B | FUERA | 69 | 50 | 0.45x | 72% | 42% | 7% | 2% | 4% (n=54) | 4% (n=48) | 50% (n=2) |
| B | WATCH | 288 | 189 | 0.27x | 86% | 37% | 11% | 5% | 15% (n=211) | 12% (n=210) | 8% (n=149) |
| C-meta | 🟡 META ACTIVÁNDOSE | 121 | 48 | 0.84x | 33% | 24% | 7% | 1% | 45% (n=40) | 22% (n=27) | 6% (n=17) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 285 | 110 | 0.38x | 62% | 3% | 0% | 3% (n=242) | 2% (n=240) | 1% (n=157) |
| dev vendió | 151 | 131 | 0.33x | 92% | 9% | 3% | 7% (n=138) | 5% (n=134) | 7% (n=74) |
| compras en el bloque de creación | 97 | 77 | 0.26x | 94% | 8% | 3% | 9% (n=86) | 7% (n=85) | 5% (n=55) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
