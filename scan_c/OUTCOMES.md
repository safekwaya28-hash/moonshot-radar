# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-10 23:34 UTC** · 384 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 210 | 127 | 0.31x | 85% | 31% | 6% | 2% | 5% (n=197) | 3% (n=192) | 3% (n=120) |
| B | FUERA | 19 | 16 | 0.50x | 50% | 56% | 11% | 6% | 11% (n=18) | 17% (n=12) | 100% (n=1) |
| B | WATCH | 100 | 65 | 0.26x | 83% | 41% | 17% | 9% | 17% (n=82) | 15% (n=82) | 14% (n=51) |
| C-meta | 🟡 META ACTIVÁNDOSE | 54 | 19 | 0.85x | 37% | 22% | 10% | 2% | 42% (n=19) | 33% (n=15) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 102 | 38 | 0.35x | 68% | 1% | 1% | 2% (n=91) | 0% (n=89) | 2% (n=55) |
| dev vendió | 67 | 58 | 0.31x | 90% | 7% | 3% | 4% (n=67) | 5% (n=64) | 5% (n=38) |
| compras en el bloque de creación | 37 | 28 | 0.26x | 96% | 11% | 3% | 9% (n=35) | 9% (n=35) | 4% (n=23) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| volumen en bucle | 2 | 1 | 0.10x | 100% | 50% | 50% | 100% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
