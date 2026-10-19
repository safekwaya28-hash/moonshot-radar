# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-19 19:07 UTC** · 1616 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 879 | 540 | 0.32x | 79% | 25% | 5% | 2% | 5% (n=813) | 3% (n=801) | 3% (n=542) |
| B | FUERA | 113 | 78 | 0.44x | 76% | 43% | 8% | 1% | 6% (n=90) | 6% (n=84) | 50% (n=2) |
| B | WATCH | 442 | 331 | 0.26x | 89% | 36% | 11% | 4% | 12% (n=360) | 8% (n=356) | 6% (n=259) |
| C-meta | 🟡 META ACTIVÁNDOSE | 181 | 93 | 0.86x | 28% | 24% | 6% | 2% | 44% (n=59) | 25% (n=36) | 14% (n=22) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 503 | 205 | 0.39x | 60% | 3% | 1% | 3% (n=455) | 2% (n=448) | 1% (n=321) |
| dev vendió | 207 | 184 | 0.30x | 92% | 8% | 4% | 8% (n=193) | 5% (n=189) | 6% (n=114) |
| compras en el bloque de creación | 159 | 143 | 0.27x | 90% | 8% | 4% | 9% (n=156) | 6% (n=155) | 5% (n=101) |
| volumen en bucle | 8 | 6 | 0.14x | 100% | 12% | 12% | 29% (n=7) | 0% (n=7) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
