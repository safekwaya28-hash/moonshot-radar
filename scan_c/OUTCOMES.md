# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-12 11:03 UTC** · 615 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 320 | 183 | 0.31x | 85% | 28% | 6% | 2% | 5% (n=305) | 3% (n=297) | 3% (n=183) |
| B | FUERA | 41 | 25 | 0.48x | 60% | 46% | 11% | 3% | 5% (n=37) | 7% (n=27) | 100% (n=1) |
| B | WATCH | 169 | 105 | 0.26x | 84% | 41% | 14% | 6% | 15% (n=136) | 13% (n=133) | 9% (n=90) |
| C-meta | 🟡 META ACTIVÁNDOSE | 84 | 26 | 0.82x | 38% | 21% | 7% | 1% | 48% (n=25) | 31% (n=16) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 161 | 60 | 0.35x | 70% | 1% | 1% | 3% (n=148) | 1% (n=146) | 1% (n=94) |
| dev vendió | 98 | 77 | 0.30x | 91% | 9% | 4% | 5% (n=96) | 5% (n=91) | 8% (n=52) |
| compras en el bloque de creación | 55 | 42 | 0.26x | 95% | 9% | 2% | 9% (n=55) | 7% (n=54) | 3% (n=31) |
| volumen en bucle | 4 | 2 | 0.09x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 0 | —x | — | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
