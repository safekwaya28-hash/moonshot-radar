# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-22 04:00 UTC** · 1790 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 967 | 615 | 0.32x | 78% | 25% | 5% | 2% | 5% (n=903) | 3% (n=891) | 3% (n=599) |
| B | FUERA | 123 | 96 | 0.44x | 77% | 44% | 8% | 1% | 5% (n=97) | 6% (n=90) | 33% (n=3) |
| B | WATCH | 485 | 386 | 0.26x | 90% | 37% | 12% | 5% | 13% (n=397) | 9% (n=393) | 7% (n=288) |
| C-meta | 🟡 META ACTIVÁNDOSE | 213 | 112 | 0.86x | 29% | 23% | 6% | 2% | 45% (n=67) | 26% (n=42) | 12% (n=25) |
| C-meta | 🟢 CANDIDATA | 1 | 0 | —x | — | 0% | 0% | 0% | 0% (n=1) | — | — |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 563 | 243 | 0.39x | 58% | 3% | 1% | 3% (n=514) | 2% (n=508) | 1% (n=359) |
| dev vendió | 216 | 199 | 0.30x | 92% | 8% | 3% | 7% (n=206) | 4% (n=202) | 6% (n=122) |
| compras en el bloque de creación | 176 | 162 | 0.28x | 91% | 8% | 4% | 8% (n=171) | 6% (n=170) | 5% (n=111) |
| volumen en bucle | 10 | 9 | 0.34x | 89% | 10% | 10% | 20% (n=10) | 0% (n=9) | 0% (n=5) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
