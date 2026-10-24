# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-24 02:01 UTC** · 1913 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1036 | 651 | 0.32x | 78% | 25% | 6% | 2% | 5% (n=967) | 3% (n=954) | 2% (n=645) |
| B | FUERA | 134 | 107 | 0.44x | 79% | 47% | 9% | 1% | 6% (n=110) | 7% (n=104) | 33% (n=3) |
| B | WATCH | 504 | 405 | 0.26x | 90% | 38% | 12% | 5% | 12% (n=411) | 9% (n=408) | 6% (n=301) |
| C-meta | 🟡 META ACTIVÁNDOSE | 237 | 127 | 0.86x | 31% | 22% | 6% | 1% | 41% (n=73) | 23% (n=48) | 11% (n=28) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 611 | 264 | 0.40x | 58% | 4% | 1% | 3% (n=561) | 2% (n=555) | 1% (n=395) |
| dev vendió | 229 | 204 | 0.29x | 93% | 8% | 3% | 7% (n=216) | 4% (n=211) | 6% (n=127) |
| compras en el bloque de creación | 183 | 171 | 0.28x | 91% | 8% | 3% | 8% (n=177) | 6% (n=175) | 4% (n=115) |
| volumen en bucle | 11 | 10 | 0.29x | 90% | 9% | 9% | 18% (n=11) | 0% (n=11) | 0% (n=6) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=4) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
