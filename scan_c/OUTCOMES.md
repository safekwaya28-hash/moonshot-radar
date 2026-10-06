# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-06 08:01 UTC** · 152 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 96 | 46 | 0.28x | 89% | 37% | 8% | 2% | 7% (n=87) | 4% (n=85) | 2% (n=49) |
| B | FUERA | 10 | 5 | 0.52x | 40% | 56% | 11% | 11% | 12% (n=8) | 20% (n=5) | 100% (n=1) |
| B | WATCH | 29 | 20 | 0.18x | 90% | 38% | 8% | 4% | 8% (n=26) | 4% (n=26) | 7% (n=15) |
| C-meta | 🟡 META ACTIVÁNDOSE | 16 | 3 | 0.63x | 33% | 13% | 13% | 0% | 17% (n=6) | 33% (n=6) | 0% (n=4) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 41 | 11 | 0.33x | 82% | 0% | 0% | 6% (n=32) | 0% (n=32) | 0% (n=20) |
| dev vendió | 33 | 20 | 0.28x | 85% | 9% | 3% | 3% (n=33) | 3% (n=31) | 6% (n=16) |
| compras en el bloque de creación | 20 | 13 | 0.24x | 100% | 15% | 0% | 10% (n=20) | 10% (n=20) | 0% (n=11) |
| impuesto modificable | 2 | 0 | —x | — | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| snipers | 1 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
