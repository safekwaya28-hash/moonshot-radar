# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-10 21:32 UTC** · 364 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 200 | 127 | 0.31x | 85% | 31% | 6% | 3% | 5% (n=189) | 3% (n=184) | 3% (n=116) |
| B | FUERA | 18 | 16 | 0.50x | 50% | 53% | 12% | 6% | 12% (n=17) | 18% (n=11) | 100% (n=1) |
| B | WATCH | 91 | 65 | 0.26x | 83% | 44% | 18% | 10% | 18% (n=73) | 15% (n=73) | 15% (n=47) |
| C-meta | 🟡 META ACTIVÁNDOSE | 54 | 19 | 0.85x | 37% | 22% | 10% | 2% | 42% (n=19) | 33% (n=15) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 98 | 38 | 0.35x | 68% | 1% | 1% | 2% (n=87) | 0% (n=85) | 2% (n=54) |
| dev vendió | 64 | 58 | 0.31x | 90% | 8% | 3% | 5% (n=64) | 5% (n=61) | 6% (n=36) |
| compras en el bloque de creación | 34 | 28 | 0.26x | 96% | 12% | 3% | 9% (n=34) | 9% (n=34) | 5% (n=22) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| volumen en bucle | 2 | 1 | 0.10x | 100% | 50% | 50% | 100% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
