# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-08 07:07 UTC** · 204 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 119 | 76 | 0.28x | 91% | 33% | 6% | 2% | 6% (n=109) | 3% (n=107) | 1% (n=68) |
| B | FUERA | 12 | 10 | 0.51x | 40% | 55% | 9% | 9% | 9% (n=11) | 14% (n=7) | 100% (n=1) |
| B | WATCH | 43 | 34 | 0.24x | 88% | 42% | 12% | 2% | 15% (n=40) | 10% (n=39) | 5% (n=22) |
| C-meta | 🟡 META ACTIVÁNDOSE | 29 | 10 | 0.74x | 40% | 21% | 11% | 4% | 40% (n=10) | 38% (n=8) | 17% (n=6) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 53 | 17 | 0.33x | 76% | 0% | 0% | 5% (n=43) | 0% (n=43) | 0% (n=28) |
| dev vendió | 43 | 39 | 0.29x | 92% | 7% | 2% | 2% (n=43) | 2% (n=41) | 4% (n=24) |
| compras en el bloque de creación | 20 | 18 | 0.24x | 100% | 15% | 0% | 10% (n=20) | 10% (n=20) | 0% (n=13) |
| snipers | 2 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
