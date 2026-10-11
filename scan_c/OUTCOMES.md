# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-11 06:41 UTC** · 458 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 250 | 138 | 0.32x | 83% | 30% | 5% | 2% | 5% (n=239) | 3% (n=233) | 3% (n=143) |
| B | FUERA | 24 | 16 | 0.50x | 50% | 62% | 14% | 5% | 10% (n=21) | 13% (n=15) | 100% (n=1) |
| B | WATCH | 122 | 70 | 0.26x | 83% | 45% | 17% | 7% | 18% (n=96) | 15% (n=93) | 11% (n=61) |
| C-meta | 🟡 META ACTIVÁNDOSE | 61 | 20 | 0.88x | 35% | 21% | 9% | 2% | 45% (n=20) | 33% (n=15) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 129 | 44 | 0.38x | 66% | 1% | 1% | 2% (n=118) | 0% (n=116) | 1% (n=72) |
| dev vendió | 75 | 61 | 0.31x | 89% | 7% | 3% | 4% (n=75) | 4% (n=72) | 5% (n=42) |
| compras en el bloque de creación | 42 | 30 | 0.25x | 97% | 10% | 2% | 10% (n=42) | 7% (n=41) | 4% (n=25) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| volumen en bucle | 2 | 1 | 0.10x | 100% | 50% | 50% | 100% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
