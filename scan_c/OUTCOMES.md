# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-22 23:13 UTC** · 1845 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 994 | 629 | 0.32x | 79% | 25% | 6% | 2% | 5% (n=929) | 3% (n=918) | 3% (n=622) |
| B | FUERA | 130 | 97 | 0.44x | 77% | 47% | 8% | 1% | 6% (n=106) | 6% (n=100) | 33% (n=3) |
| B | WATCH | 496 | 396 | 0.26x | 90% | 38% | 12% | 5% | 13% (n=405) | 9% (n=402) | 6% (n=294) |
| C-meta | 🟡 META ACTIVÁNDOSE | 223 | 119 | 0.86x | 30% | 23% | 6% | 2% | 42% (n=71) | 25% (n=44) | 12% (n=26) |
| C-meta | 🟢 CANDIDATA | 1 | 0 | —x | — | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 582 | 250 | 0.40x | 58% | 4% | 1% | 3% (n=534) | 2% (n=528) | 1% (n=377) |
| dev vendió | 221 | 200 | 0.30x | 92% | 8% | 3% | 7% (n=210) | 4% (n=206) | 6% (n=125) |
| compras en el bloque de creación | 179 | 167 | 0.28x | 91% | 8% | 3% | 8% (n=173) | 6% (n=172) | 4% (n=113) |
| volumen en bucle | 10 | 10 | 0.29x | 90% | 10% | 10% | 20% (n=10) | 0% (n=10) | 0% (n=5) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
