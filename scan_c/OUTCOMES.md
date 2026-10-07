# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-07 17:35 UTC** · 184 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 110 | 69 | 0.28x | 91% | 34% | 7% | 2% | 6% (n=100) | 3% (n=98) | 2% (n=61) |
| B | FUERA | 11 | 9 | 0.51x | 44% | 60% | 10% | 10% | 10% (n=10) | 14% (n=7) | 100% (n=1) |
| B | WATCH | 37 | 27 | 0.22x | 89% | 41% | 12% | 3% | 15% (n=34) | 9% (n=33) | 5% (n=20) |
| C-meta | 🟡 META ACTIVÁNDOSE | 25 | 8 | 0.54x | 50% | 25% | 8% | 0% | 40% (n=10) | 29% (n=7) | 0% (n=4) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 47 | 15 | 0.30x | 80% | 0% | 0% | 5% (n=37) | 0% (n=37) | 0% (n=24) |
| dev vendió | 41 | 34 | 0.28x | 91% | 7% | 2% | 2% (n=41) | 3% (n=39) | 5% (n=22) |
| compras en el bloque de creación | 20 | 18 | 0.24x | 100% | 15% | 0% | 10% (n=20) | 10% (n=20) | 0% (n=13) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| snipers | 1 | 1 | 0.15x | 100% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| volumen en bucle | 1 | 1 | 0.10x | 100% | 100% | 100% | 100% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
