# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-09 02:33 UTC** · 275 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 152 | 80 | 0.28x | 91% | 32% | 6% | 3% | 5% (n=140) | 3% (n=137) | 3% (n=90) |
| B | FUERA | 15 | 11 | 0.52x | 36% | 43% | 7% | 7% | 8% (n=13) | 12% (n=8) | 100% (n=1) |
| B | WATCH | 74 | 39 | 0.27x | 87% | 42% | 12% | 3% | 14% (n=59) | 9% (n=58) | 6% (n=36) |
| C-meta | 🟡 META ACTIVÁNDOSE | 33 | 13 | 0.85x | 38% | 22% | 12% | 3% | 38% (n=13) | 40% (n=10) | 17% (n=6) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 69 | 18 | 0.33x | 78% | 2% | 2% | 4% (n=57) | 0% (n=56) | 2% (n=40) |
| dev vendió | 53 | 41 | 0.28x | 93% | 6% | 2% | 2% (n=53) | 2% (n=51) | 3% (n=29) |
| compras en el bloque de creación | 27 | 18 | 0.24x | 100% | 15% | 4% | 11% (n=27) | 11% (n=27) | 6% (n=18) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
