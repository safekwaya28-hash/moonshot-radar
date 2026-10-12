# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-12 02:41 UTC** · 526 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 278 | 163 | 0.30x | 85% | 30% | 5% | 2% | 5% (n=265) | 3% (n=256) | 3% (n=159) |
| B | FUERA | 28 | 18 | 0.50x | 50% | 56% | 16% | 4% | 8% (n=24) | 11% (n=18) | 100% (n=1) |
| B | WATCH | 141 | 88 | 0.28x | 82% | 41% | 16% | 7% | 16% (n=114) | 14% (n=112) | 11% (n=75) |
| C-meta | 🟡 META ACTIVÁNDOSE | 78 | 26 | 0.82x | 38% | 21% | 7% | 1% | 48% (n=25) | 33% (n=15) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 142 | 54 | 0.33x | 70% | 2% | 1% | 2% (n=130) | 1% (n=127) | 1% (n=81) |
| dev vendió | 87 | 69 | 0.30x | 90% | 7% | 2% | 5% (n=86) | 4% (n=80) | 4% (n=46) |
| compras en el bloque de creación | 45 | 36 | 0.24x | 94% | 9% | 2% | 9% (n=45) | 7% (n=45) | 4% (n=28) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| volumen en bucle | 2 | 2 | 0.09x | 100% | 50% | 50% | 100% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
