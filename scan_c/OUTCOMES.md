# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-12 11:39 UTC** · 620 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 323 | 184 | 0.31x | 85% | 28% | 6% | 2% | 5% (n=308) | 3% (n=300) | 3% (n=183) |
| B | FUERA | 42 | 25 | 0.48x | 60% | 45% | 11% | 3% | 5% (n=38) | 7% (n=28) | 100% (n=1) |
| B | WATCH | 170 | 105 | 0.26x | 84% | 41% | 14% | 6% | 15% (n=137) | 13% (n=134) | 9% (n=92) |
| C-meta | 🟡 META ACTIVÁNDOSE | 84 | 26 | 0.82x | 38% | 21% | 7% | 1% | 48% (n=25) | 31% (n=16) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 161 | 61 | 0.36x | 69% | 1% | 1% | 3% (n=148) | 1% (n=146) | 1% (n=94) |
| dev vendió | 99 | 77 | 0.30x | 91% | 9% | 4% | 5% (n=97) | 5% (n=92) | 8% (n=52) |
| compras en el bloque de creación | 57 | 42 | 0.26x | 95% | 9% | 2% | 9% (n=57) | 7% (n=56) | 3% (n=31) |
| volumen en bucle | 4 | 2 | 0.09x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 0 | —x | — | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
