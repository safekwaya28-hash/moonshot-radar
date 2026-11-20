# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-11-20 03:26 UTC** · 2376 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1291 | 787 | 0.33x | 74% | 23% | 5% | 2% | 4% (n=1201) | 3% (n=1190) | 2% (n=849) |
| B | FUERA | 161 | 123 | 0.43x | 78% | 49% | 10% | 2% | 9% (n=125) | 8% (n=119) | 43% (n=7) |
| B | WATCH | 621 | 471 | 0.26x | 90% | 37% | 11% | 5% | 11% (n=477) | 8% (n=473) | 6% (n=362) |
| C-meta | 🟡 META ACTIVÁNDOSE | 301 | 171 | 0.86x | 29% | 23% | 6% | 2% | 40% (n=94) | 24% (n=62) | 11% (n=37) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 808 | 344 | 0.47x | 52% | 3% | 1% | 2% (n=745) | 1% (n=739) | 1% (n=559) |
| dev vendió | 261 | 235 | 0.28x | 92% | 8% | 3% | 7% (n=242) | 5% (n=238) | 5% (n=148) |
| compras en el bloque de creación | 208 | 194 | 0.27x | 91% | 8% | 3% | 8% (n=200) | 5% (n=199) | 4% (n=134) |
| volumen en bucle | 12 | 12 | 0.34x | 92% | 8% | 8% | 17% (n=12) | 0% (n=12) | 0% (n=6) |
| impuesto modificable | 7 | 7 | 0.64x | 29% | 0% | 0% | 14% (n=7) | 0% (n=5) | 0% (n=5) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| puede crear tokens | 2 | 2 | 0.98x | 0% | 0% | 0% | — | — | — |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
