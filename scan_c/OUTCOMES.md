# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-14 07:03 UTC** · 937 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 500 | 281 | 0.32x | 85% | 26% | 5% | 2% | 5% (n=455) | 3% (n=447) | 3% (n=276) |
| B | FUERA | 65 | 47 | 0.45x | 74% | 44% | 7% | 2% | 4% (n=53) | 4% (n=46) | 50% (n=2) |
| B | WATCH | 256 | 169 | 0.27x | 85% | 38% | 12% | 5% | 14% (n=198) | 11% (n=197) | 7% (n=140) |
| C-meta | 🟡 META ACTIVÁNDOSE | 115 | 44 | 0.80x | 36% | 25% | 8% | 1% | 45% (n=40) | 26% (n=27) | 7% (n=15) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 268 | 91 | 0.36x | 67% | 2% | 0% | 2% (n=231) | 1% (n=229) | 1% (n=150) |
| dev vendió | 140 | 116 | 0.33x | 91% | 10% | 4% | 7% (n=136) | 5% (n=131) | 7% (n=69) |
| compras en el bloque de creación | 86 | 68 | 0.26x | 96% | 8% | 3% | 10% (n=82) | 7% (n=81) | 6% (n=51) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 3 | 0.53x | 33% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=1) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
