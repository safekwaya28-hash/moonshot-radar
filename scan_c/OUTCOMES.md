# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-08 22:00 UTC** · 249 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 143 | 77 | 0.29x | 91% | 31% | 5% | 1% | 5% (n=132) | 2% (n=130) | 1% (n=84) |
| B | FUERA | 13 | 10 | 0.51x | 40% | 50% | 8% | 8% | 8% (n=12) | 12% (n=8) | 100% (n=1) |
| B | WATCH | 59 | 35 | 0.26x | 89% | 40% | 13% | 4% | 15% (n=52) | 12% (n=51) | 6% (n=31) |
| C-meta | 🟡 META ACTIVÁNDOSE | 33 | 13 | 0.85x | 38% | 19% | 9% | 3% | 36% (n=11) | 33% (n=9) | 17% (n=6) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 64 | 18 | 0.33x | 78% | 0% | 0% | 4% (n=53) | 0% (n=53) | 0% (n=37) |
| dev vendió | 51 | 39 | 0.29x | 92% | 6% | 2% | 2% (n=51) | 2% (n=49) | 4% (n=27) |
| compras en el bloque de creación | 25 | 18 | 0.24x | 100% | 12% | 0% | 8% (n=25) | 8% (n=25) | 0% (n=17) |
| snipers | 2 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
