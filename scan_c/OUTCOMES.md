# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-15 09:58 UTC** · 1150 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 625 | 346 | 0.33x | 82% | 27% | 6% | 2% | 6% (n=537) | 4% (n=528) | 3% (n=337) |
| B | FUERA | 75 | 55 | 0.45x | 73% | 43% | 7% | 2% | 3% (n=59) | 4% (n=54) | 50% (n=2) |
| B | WATCH | 319 | 212 | 0.27x | 87% | 36% | 11% | 5% | 14% (n=250) | 10% (n=249) | 8% (n=172) |
| C-meta | 🟡 META ACTIVÁNDOSE | 130 | 58 | 0.85x | 33% | 23% | 6% | 1% | 44% (n=43) | 21% (n=28) | 6% (n=17) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 335 | 117 | 0.40x | 62% | 3% | 1% | 3% (n=272) | 2% (n=268) | 1% (n=179) |
| dev vendió | 170 | 134 | 0.33x | 93% | 10% | 4% | 7% (n=155) | 5% (n=151) | 7% (n=86) |
| compras en el bloque de creación | 114 | 89 | 0.27x | 91% | 8% | 4% | 9% (n=104) | 7% (n=103) | 6% (n=66) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
