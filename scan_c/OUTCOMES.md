# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-13 06:47 UTC** · 771 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 408 | 207 | 0.31x | 86% | 27% | 5% | 2% | 5% (n=385) | 3% (n=377) | 3% (n=235) |
| B | FUERA | 53 | 28 | 0.48x | 61% | 45% | 9% | 2% | 4% (n=47) | 5% (n=41) | 50% (n=2) |
| B | WATCH | 214 | 127 | 0.25x | 84% | 42% | 14% | 6% | 15% (n=171) | 13% (n=168) | 9% (n=116) |
| C-meta | 🟡 META ACTIVÁNDOSE | 95 | 34 | 0.84x | 35% | 24% | 7% | 1% | 44% (n=32) | 23% (n=22) | 7% (n=14) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 209 | 67 | 0.33x | 70% | 2% | 1% | 3% (n=191) | 1% (n=188) | 1% (n=123) |
| dev vendió | 123 | 88 | 0.31x | 91% | 10% | 4% | 6% (n=118) | 7% (n=113) | 8% (n=62) |
| compras en el bloque de creación | 70 | 47 | 0.26x | 96% | 7% | 1% | 7% (n=70) | 6% (n=70) | 2% (n=44) |
| volumen en bucle | 4 | 3 | 0.10x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 3 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=1) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
