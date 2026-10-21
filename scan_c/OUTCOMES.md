# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-21 18:59 UTC** · 1771 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 959 | 604 | 0.32x | 79% | 25% | 6% | 2% | 5% (n=897) | 3% (n=885) | 3% (n=596) |
| B | FUERA | 121 | 95 | 0.44x | 77% | 44% | 7% | 1% | 6% (n=97) | 6% (n=90) | 33% (n=3) |
| B | WATCH | 484 | 382 | 0.26x | 90% | 38% | 12% | 5% | 13% (n=396) | 9% (n=393) | 6% (n=287) |
| C-meta | 🟡 META ACTIVÁNDOSE | 206 | 107 | 0.86x | 29% | 24% | 7% | 2% | 45% (n=67) | 26% (n=42) | 12% (n=25) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 555 | 236 | 0.39x | 59% | 4% | 1% | 3% (n=508) | 2% (n=502) | 1% (n=356) |
| dev vendió | 216 | 198 | 0.30x | 92% | 8% | 3% | 7% (n=206) | 4% (n=202) | 6% (n=122) |
| compras en el bloque de creación | 176 | 159 | 0.28x | 91% | 8% | 4% | 8% (n=171) | 6% (n=170) | 5% (n=111) |
| volumen en bucle | 10 | 9 | 0.34x | 89% | 10% | 10% | 20% (n=10) | 0% (n=9) | 0% (n=5) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
