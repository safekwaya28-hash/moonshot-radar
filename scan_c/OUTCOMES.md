# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-11 08:02 UTC** · 473 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 257 | 139 | 0.32x | 83% | 29% | 4% | 2% | 4% (n=246) | 2% (n=241) | 3% (n=149) |
| B | FUERA | 25 | 16 | 0.50x | 50% | 59% | 14% | 5% | 9% (n=22) | 12% (n=16) | 100% (n=1) |
| B | WATCH | 129 | 70 | 0.26x | 83% | 43% | 17% | 8% | 17% (n=103) | 15% (n=101) | 12% (n=67) |
| C-meta | 🟡 META ACTIVÁNDOSE | 61 | 21 | 0.85x | 38% | 21% | 9% | 2% | 45% (n=20) | 33% (n=15) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 133 | 44 | 0.38x | 66% | 1% | 1% | 2% (n=122) | 0% (n=120) | 1% (n=76) |
| dev vendió | 77 | 61 | 0.31x | 89% | 6% | 3% | 4% (n=77) | 4% (n=74) | 5% (n=43) |
| compras en el bloque de creación | 43 | 30 | 0.25x | 97% | 9% | 2% | 9% (n=43) | 7% (n=43) | 4% (n=26) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| volumen en bucle | 2 | 2 | 0.09x | 100% | 50% | 50% | 100% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
