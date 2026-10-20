# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-20 20:56 UTC** · 1694 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 927 | 582 | 0.32x | 79% | 24% | 6% | 2% | 5% (n=875) | 3% (n=864) | 3% (n=584) |
| B | FUERA | 117 | 91 | 0.44x | 77% | 43% | 7% | 1% | 6% (n=94) | 6% (n=87) | 33% (n=3) |
| B | WATCH | 457 | 370 | 0.26x | 89% | 38% | 12% | 5% | 13% (n=382) | 9% (n=379) | 6% (n=280) |
| C-meta | 🟡 META ACTIVÁNDOSE | 192 | 99 | 0.86x | 29% | 25% | 7% | 2% | 46% (n=63) | 26% (n=39) | 12% (n=24) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 541 | 222 | 0.39x | 59% | 3% | 1% | 3% (n=499) | 2% (n=493) | 1% (n=351) |
| dev vendió | 211 | 194 | 0.30x | 93% | 8% | 3% | 7% (n=203) | 5% (n=199) | 6% (n=119) |
| compras en el bloque de creación | 164 | 155 | 0.27x | 90% | 9% | 4% | 9% (n=163) | 6% (n=162) | 5% (n=108) |
| volumen en bucle | 9 | 9 | 0.34x | 89% | 11% | 11% | 25% (n=8) | 0% (n=8) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
