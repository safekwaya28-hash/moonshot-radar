# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-11-16 07:22 UTC** · 2314 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1245 | 769 | 0.33x | 74% | 24% | 5% | 2% | 4% (n=1158) | 3% (n=1147) | 2% (n=808) |
| B | FUERA | 158 | 120 | 0.44x | 78% | 48% | 10% | 2% | 8% (n=121) | 8% (n=115) | 60% (n=5) |
| B | WATCH | 610 | 466 | 0.26x | 90% | 37% | 11% | 5% | 11% (n=470) | 8% (n=466) | 6% (n=355) |
| C-meta | 🟡 META ACTIVÁNDOSE | 299 | 170 | 0.86x | 28% | 23% | 7% | 2% | 40% (n=94) | 24% (n=62) | 11% (n=37) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 772 | 333 | 0.47x | 52% | 3% | 1% | 2% (n=709) | 1% (n=703) | 1% (n=524) |
| dev vendió | 254 | 232 | 0.28x | 92% | 8% | 3% | 7% (n=238) | 5% (n=234) | 6% (n=145) |
| compras en el bloque de creación | 205 | 190 | 0.27x | 91% | 8% | 3% | 9% (n=197) | 5% (n=196) | 4% (n=131) |
| volumen en bucle | 12 | 12 | 0.34x | 92% | 8% | 8% | 17% (n=12) | 0% (n=12) | 0% (n=6) |
| impuesto modificable | 7 | 7 | 0.64x | 29% | 0% | 0% | 14% (n=7) | 0% (n=5) | 0% (n=5) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| puede crear tokens | 2 | 2 | 0.98x | 0% | 0% | 0% | — | — | — |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
