# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-20 02:58 UTC** · 1651 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 901 | 554 | 0.32x | 80% | 24% | 5% | 2% | 5% (n=849) | 3% (n=838) | 3% (n=566) |
| B | FUERA | 114 | 86 | 0.44x | 77% | 42% | 8% | 1% | 5% (n=91) | 6% (n=85) | 50% (n=2) |
| B | WATCH | 450 | 349 | 0.26x | 89% | 37% | 12% | 4% | 12% (n=376) | 9% (n=372) | 6% (n=269) |
| C-meta | 🟡 META ACTIVÁNDOSE | 185 | 95 | 0.86x | 27% | 25% | 6% | 2% | 45% (n=62) | 24% (n=37) | 13% (n=23) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 520 | 210 | 0.38x | 60% | 3% | 1% | 3% (n=478) | 2% (n=472) | 1% (n=335) |
| dev vendió | 208 | 186 | 0.30x | 92% | 8% | 3% | 8% (n=200) | 5% (n=196) | 6% (n=118) |
| compras en el bloque de creación | 162 | 149 | 0.28x | 90% | 9% | 4% | 9% (n=161) | 6% (n=160) | 5% (n=107) |
| volumen en bucle | 9 | 7 | 0.14x | 100% | 11% | 11% | 25% (n=8) | 0% (n=8) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
