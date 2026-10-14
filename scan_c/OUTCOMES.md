# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-14 05:48 UTC** · 927 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 495 | 275 | 0.31x | 85% | 26% | 5% | 2% | 5% (n=454) | 3% (n=446) | 3% (n=275) |
| B | FUERA | 63 | 46 | 0.45x | 74% | 45% | 8% | 2% | 4% (n=53) | 4% (n=46) | 50% (n=2) |
| B | WATCH | 253 | 166 | 0.27x | 85% | 38% | 12% | 5% | 14% (n=198) | 11% (n=197) | 7% (n=139) |
| C-meta | 🟡 META ACTIVÁNDOSE | 115 | 42 | 0.80x | 38% | 25% | 8% | 1% | 45% (n=40) | 26% (n=27) | 7% (n=15) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 264 | 90 | 0.37x | 67% | 2% | 0% | 2% (n=231) | 1% (n=229) | 1% (n=150) |
| dev vendió | 140 | 112 | 0.32x | 91% | 10% | 4% | 7% (n=135) | 5% (n=130) | 7% (n=68) |
| compras en el bloque de creación | 85 | 67 | 0.26x | 97% | 8% | 4% | 10% (n=82) | 7% (n=81) | 6% (n=51) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 3 | 0.53x | 33% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=1) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
