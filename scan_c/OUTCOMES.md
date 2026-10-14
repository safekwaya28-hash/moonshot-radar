# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-14 14:50 UTC** · 995 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 529 | 318 | 0.33x | 83% | 26% | 5% | 2% | 6% (n=468) | 3% (n=461) | 3% (n=288) |
| B | FUERA | 68 | 50 | 0.45x | 72% | 43% | 7% | 2% | 4% (n=54) | 4% (n=47) | 50% (n=2) |
| B | WATCH | 279 | 189 | 0.27x | 86% | 37% | 11% | 5% | 14% (n=205) | 11% (n=204) | 7% (n=145) |
| C-meta | 🟡 META ACTIVÁNDOSE | 118 | 45 | 0.82x | 36% | 24% | 7% | 1% | 45% (n=40) | 22% (n=27) | 6% (n=17) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 281 | 107 | 0.38x | 63% | 2% | 0% | 2% (n=241) | 1% (n=239) | 1% (n=157) |
| dev vendió | 147 | 128 | 0.33x | 92% | 9% | 3% | 7% (n=136) | 5% (n=132) | 7% (n=71) |
| compras en el bloque de creación | 95 | 77 | 0.26x | 94% | 8% | 3% | 9% (n=85) | 7% (n=84) | 6% (n=54) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 4 | 0.69x | 25% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=2) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
