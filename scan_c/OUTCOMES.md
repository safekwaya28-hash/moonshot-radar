# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-09 00:52 UTC** · 255 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 144 | 78 | 0.28x | 91% | 32% | 7% | 3% | 5% (n=133) | 3% (n=130) | 4% (n=85) |
| B | FUERA | 14 | 11 | 0.52x | 36% | 46% | 8% | 8% | 8% (n=13) | 12% (n=8) | 100% (n=1) |
| B | WATCH | 63 | 36 | 0.29x | 89% | 43% | 13% | 4% | 13% (n=54) | 9% (n=53) | 6% (n=32) |
| C-meta | 🟡 META ACTIVÁNDOSE | 33 | 13 | 0.85x | 38% | 22% | 12% | 3% | 38% (n=13) | 40% (n=10) | 17% (n=6) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 64 | 18 | 0.33x | 78% | 2% | 2% | 4% (n=53) | 0% (n=52) | 3% (n=37) |
| dev vendió | 52 | 40 | 0.28x | 92% | 6% | 2% | 2% (n=52) | 2% (n=50) | 4% (n=28) |
| compras en el bloque de creación | 25 | 18 | 0.24x | 100% | 16% | 4% | 12% (n=25) | 12% (n=25) | 6% (n=17) |
| snipers | 2 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
