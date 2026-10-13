# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-13 00:49 UTC** · 710 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 372 | 186 | 0.31x | 85% | 28% | 6% | 2% | 5% (n=353) | 3% (n=347) | 3% (n=216) |
| B | FUERA | 49 | 25 | 0.48x | 60% | 47% | 9% | 2% | 5% (n=43) | 5% (n=37) | 50% (n=2) |
| B | WATCH | 194 | 107 | 0.26x | 84% | 44% | 15% | 6% | 17% (n=153) | 14% (n=150) | 9% (n=103) |
| C-meta | 🟡 META ACTIVÁNDOSE | 94 | 31 | 0.78x | 39% | 24% | 7% | 1% | 45% (n=31) | 25% (n=20) | 8% (n=13) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 185 | 62 | 0.37x | 69% | 1% | 1% | 2% (n=170) | 1% (n=168) | 1% (n=108) |
| dev vendió | 115 | 78 | 0.30x | 91% | 11% | 4% | 6% (n=111) | 7% (n=107) | 8% (n=61) |
| compras en el bloque de creación | 66 | 42 | 0.26x | 95% | 8% | 2% | 8% (n=66) | 6% (n=66) | 2% (n=41) |
| volumen en bucle | 4 | 2 | 0.09x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 3 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=3) | 0% (n=1) | 0% (n=1) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 0 | —x | — | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
