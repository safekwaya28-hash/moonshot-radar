# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-16 01:07 UTC** · 1253 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 683 | 391 | 0.32x | 82% | 27% | 6% | 2% | 6% (n=642) | 4% (n=629) | 3% (n=407) |
| B | FUERA | 83 | 59 | 0.45x | 73% | 42% | 8% | 2% | 5% (n=66) | 5% (n=61) | 50% (n=2) |
| B | WATCH | 349 | 247 | 0.27x | 87% | 37% | 11% | 5% | 13% (n=289) | 10% (n=287) | 8% (n=200) |
| C-meta | 🟡 META ACTIVÁNDOSE | 137 | 66 | 0.86x | 30% | 22% | 6% | 1% | 45% (n=44) | 21% (n=28) | 6% (n=17) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 368 | 132 | 0.39x | 61% | 4% | 1% | 3% (n=334) | 2% (n=328) | 1% (n=222) |
| dev vendió | 180 | 151 | 0.31x | 92% | 9% | 3% | 7% (n=174) | 5% (n=169) | 6% (n=97) |
| compras en el bloque de creación | 129 | 102 | 0.27x | 92% | 8% | 5% | 9% (n=128) | 6% (n=126) | 6% (n=82) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
