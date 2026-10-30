# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-30 23:17 UTC** · 2085 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1106 | 707 | 0.33x | 77% | 25% | 5% | 2% | 5% (n=1029) | 3% (n=1018) | 2% (n=692) |
| B | FUERA | 149 | 114 | 0.44x | 77% | 47% | 9% | 1% | 6% (n=116) | 6% (n=110) | 33% (n=3) |
| B | WATCH | 551 | 433 | 0.26x | 90% | 37% | 11% | 5% | 12% (n=443) | 8% (n=440) | 6% (n=330) |
| C-meta | 🟡 META ACTIVÁNDOSE | 277 | 158 | 0.86x | 28% | 24% | 7% | 2% | 42% (n=89) | 24% (n=59) | 12% (n=34) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 662 | 295 | 0.41x | 56% | 4% | 1% | 2% (n=604) | 2% (n=598) | 1% (n=428) |
| dev vendió | 238 | 218 | 0.28x | 92% | 8% | 3% | 7% (n=225) | 5% (n=221) | 5% (n=135) |
| compras en el bloque de creación | 192 | 180 | 0.27x | 91% | 8% | 3% | 8% (n=186) | 5% (n=185) | 4% (n=121) |
| volumen en bucle | 12 | 12 | 0.34x | 92% | 8% | 8% | 17% (n=12) | 0% (n=12) | 0% (n=6) |
| impuesto modificable | 7 | 6 | 0.70x | 17% | 0% | 0% | 14% (n=7) | 0% (n=5) | 0% (n=4) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| puede crear tokens | 2 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
