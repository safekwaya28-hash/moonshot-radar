# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-11 01:37 UTC** · 406 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 223 | 134 | 0.32x | 84% | 30% | 5% | 2% | 5% (n=210) | 3% (n=204) | 3% (n=126) |
| B | FUERA | 19 | 16 | 0.50x | 50% | 56% | 11% | 6% | 11% (n=18) | 17% (n=12) | 100% (n=1) |
| B | WATCH | 107 | 67 | 0.26x | 82% | 43% | 16% | 8% | 16% (n=87) | 14% (n=85) | 13% (n=53) |
| C-meta | 🟡 META ACTIVÁNDOSE | 56 | 20 | 0.88x | 35% | 24% | 10% | 2% | 45% (n=20) | 33% (n=15) | 11% (n=9) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 111 | 42 | 0.37x | 67% | 1% | 1% | 2% (n=100) | 0% (n=98) | 2% (n=59) |
| dev vendió | 70 | 60 | 0.31x | 88% | 7% | 3% | 4% (n=70) | 4% (n=67) | 5% (n=40) |
| compras en el bloque de creación | 38 | 29 | 0.26x | 97% | 11% | 3% | 11% (n=36) | 9% (n=35) | 4% (n=23) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| volumen en bucle | 2 | 1 | 0.10x | 100% | 50% | 50% | 100% (n=2) | 0% (n=2) | 0% (n=2) |
| impuesto modificable | 2 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=2) | 0% (n=1) | 0% (n=1) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
