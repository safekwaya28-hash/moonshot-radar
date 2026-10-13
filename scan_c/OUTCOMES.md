# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-13 23:09 UTC** · 872 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 469 | 258 | 0.30x | 87% | 27% | 5% | 2% | 5% (n=445) | 3% (n=437) | 3% (n=272) |
| B | FUERA | 59 | 43 | 0.46x | 74% | 48% | 8% | 2% | 4% (n=50) | 5% (n=44) | 50% (n=2) |
| B | WATCH | 238 | 147 | 0.26x | 84% | 39% | 12% | 5% | 14% (n=194) | 11% (n=192) | 7% (n=135) |
| C-meta | 🟡 META ACTIVÁNDOSE | 105 | 42 | 0.80x | 38% | 23% | 8% | 1% | 44% (n=34) | 25% (n=24) | 7% (n=15) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 245 | 81 | 0.33x | 72% | 1% | 0% | 2% (n=225) | 0% (n=222) | 1% (n=148) |
| dev vendió | 138 | 107 | 0.31x | 92% | 10% | 4% | 7% (n=134) | 5% (n=130) | 7% (n=68) |
| compras en el bloque de creación | 80 | 64 | 0.26x | 97% | 8% | 2% | 9% (n=80) | 6% (n=79) | 4% (n=50) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 3 | 0.53x | 33% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=1) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
