# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-09 11:01 UTC** · 285 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 157 | 82 | 0.28x | 91% | 33% | 7% | 3% | 5% (n=146) | 3% (n=144) | 3% (n=92) |
| B | FUERA | 15 | 11 | 0.52x | 36% | 43% | 7% | 7% | 7% (n=14) | 11% (n=9) | 100% (n=1) |
| B | WATCH | 77 | 40 | 0.30x | 88% | 42% | 15% | 6% | 15% (n=62) | 11% (n=62) | 10% (n=40) |
| C-meta | 🟡 META ACTIVÁNDOSE | 35 | 13 | 0.85x | 38% | 21% | 12% | 3% | 38% (n=13) | 40% (n=10) | 17% (n=6) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 73 | 20 | 0.32x | 80% | 2% | 2% | 3% (n=62) | 0% (n=62) | 2% (n=43) |
| dev vendió | 54 | 41 | 0.28x | 93% | 7% | 2% | 4% (n=54) | 4% (n=52) | 4% (n=28) |
| compras en el bloque de creación | 27 | 18 | 0.24x | 100% | 15% | 4% | 11% (n=27) | 11% (n=27) | 6% (n=18) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
