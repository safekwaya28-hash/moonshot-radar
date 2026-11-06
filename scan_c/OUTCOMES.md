# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-11-06 23:33 UTC** · 2158 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1148 | 731 | 0.33x | 76% | 25% | 5% | 2% | 5% (n=1070) | 3% (n=1059) | 2% (n=728) |
| B | FUERA | 151 | 117 | 0.44x | 78% | 48% | 9% | 2% | 7% (n=118) | 7% (n=112) | 50% (n=4) |
| B | WATCH | 573 | 451 | 0.26x | 91% | 37% | 11% | 5% | 12% (n=452) | 8% (n=449) | 6% (n=338) |
| C-meta | 🟡 META ACTIVÁNDOSE | 284 | 166 | 0.86x | 29% | 24% | 7% | 2% | 40% (n=92) | 24% (n=62) | 11% (n=37) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 692 | 309 | 0.45x | 54% | 4% | 1% | 2% (n=634) | 2% (n=628) | 1% (n=456) |
| dev vendió | 245 | 224 | 0.29x | 92% | 8% | 3% | 7% (n=231) | 4% (n=227) | 5% (n=138) |
| compras en el bloque de creación | 197 | 184 | 0.27x | 91% | 8% | 3% | 9% (n=191) | 5% (n=190) | 4% (n=126) |
| volumen en bucle | 12 | 12 | 0.34x | 92% | 8% | 8% | 17% (n=12) | 0% (n=12) | 0% (n=6) |
| impuesto modificable | 7 | 7 | 0.64x | 29% | 0% | 0% | 14% (n=7) | 0% (n=5) | 0% (n=5) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| puede crear tokens | 2 | 2 | 0.98x | 0% | 0% | 0% | — | — | — |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
