# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-11 13:34 UTC** · 485 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 264 | 139 | 0.32x | 83% | 30% | 5% | 2% | 5% (n=253) | 3% (n=246) | 3% (n=152) |
| B | FUERA | 28 | 16 | 0.50x | 50% | 56% | 16% | 4% | 8% (n=24) | 12% (n=17) | 100% (n=1) |
| B | WATCH | 130 | 70 | 0.26x | 83% | 44% | 17% | 8% | 17% (n=105) | 15% (n=104) | 11% (n=70) |
| C-meta | 🟡 META ACTIVÁNDOSE | 62 | 24 | 0.82x | 38% | 21% | 9% | 2% | 45% (n=20) | 33% (n=15) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 136 | 44 | 0.38x | 66% | 2% | 1% | 2% (n=125) | 1% (n=122) | 1% (n=77) |
| dev vendió | 80 | 61 | 0.31x | 89% | 8% | 2% | 4% (n=80) | 4% (n=76) | 5% (n=44) |
| compras en el bloque de creación | 44 | 30 | 0.25x | 97% | 9% | 2% | 9% (n=44) | 7% (n=44) | 4% (n=27) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| volumen en bucle | 2 | 2 | 0.09x | 100% | 50% | 50% | 100% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
