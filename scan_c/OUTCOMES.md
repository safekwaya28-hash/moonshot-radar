# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-15 20:57 UTC** · 1223 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 668 | 383 | 0.32x | 82% | 26% | 6% | 2% | 6% (n=581) | 4% (n=571) | 3% (n=369) |
| B | FUERA | 83 | 57 | 0.45x | 74% | 42% | 8% | 2% | 5% (n=61) | 5% (n=56) | 50% (n=2) |
| B | WATCH | 338 | 239 | 0.27x | 87% | 35% | 11% | 5% | 13% (n=260) | 10% (n=259) | 7% (n=180) |
| C-meta | 🟡 META ACTIVÁNDOSE | 133 | 63 | 0.85x | 32% | 22% | 6% | 1% | 44% (n=43) | 21% (n=28) | 6% (n=17) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 356 | 131 | 0.39x | 62% | 3% | 1% | 3% (n=300) | 2% (n=296) | 1% (n=198) |
| dev vendió | 179 | 149 | 0.31x | 93% | 9% | 3% | 7% (n=163) | 5% (n=158) | 7% (n=92) |
| compras en el bloque de creación | 127 | 97 | 0.26x | 92% | 8% | 4% | 8% (n=112) | 6% (n=111) | 5% (n=73) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
