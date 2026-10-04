# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-04 21:45 UTC** · 102 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | — | — | — |
| B | DESCARTAR | 67 | 33 | 0.26x | 91% | 41% | 10% | 3% | 10% (n=58) | 5% (n=56) | 3% (n=35) |
| B | FUERA | 7 | 4 | 0.49x | 50% | 50% | 17% | 17% | 17% (n=6) | 25% (n=4) | 100% (n=1) |
| B | WATCH | 21 | 12 | 0.25x | 92% | 37% | 11% | 5% | 11% (n=19) | 5% (n=19) | 8% (n=12) |
| C-meta | 🟡 META ACTIVÁNDOSE | 6 | 2 | 0.74x | 50% | 20% | 20% | 0% | 50% (n=2) | 50% (n=2) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 30 | 8 | 0.37x | 88% | 0% | 0% | 10% (n=21) | 0% (n=21) | 0% (n=13) |
| dev vendió | 20 | 13 | 0.26x | 85% | 10% | 5% | 5% (n=20) | 6% (n=18) | 8% (n=12) |
| compras en el bloque de creación | 15 | 10 | 0.24x | 100% | 20% | 0% | 13% (n=15) | 13% (n=15) | 0% (n=8) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | — | — | — |
| snipers | 1 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
