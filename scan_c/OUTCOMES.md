# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-12 14:50 UTC** · 647 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 340 | 184 | 0.31x | 85% | 28% | 5% | 2% | 5% (n=323) | 3% (n=316) | 3% (n=193) |
| B | FUERA | 45 | 25 | 0.48x | 60% | 44% | 10% | 2% | 5% (n=41) | 6% (n=34) | 100% (n=1) |
| B | WATCH | 175 | 105 | 0.26x | 84% | 42% | 14% | 6% | 16% (n=139) | 12% (n=136) | 8% (n=95) |
| C-meta | 🟡 META ACTIVÁNDOSE | 86 | 26 | 0.82x | 38% | 21% | 7% | 1% | 50% (n=26) | 31% (n=16) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 169 | 61 | 0.36x | 69% | 1% | 1% | 3% (n=155) | 1% (n=153) | 1% (n=98) |
| dev vendió | 104 | 77 | 0.30x | 91% | 9% | 4% | 5% (n=101) | 5% (n=96) | 7% (n=54) |
| compras en el bloque de creación | 61 | 42 | 0.26x | 95% | 8% | 2% | 8% (n=61) | 7% (n=61) | 3% (n=35) |
| volumen en bucle | 4 | 2 | 0.09x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 0 | —x | — | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
