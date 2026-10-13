# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-13 16:04 UTC** · 859 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 466 | 243 | 0.31x | 87% | 27% | 5% | 2% | 5% (n=442) | 3% (n=431) | 3% (n=265) |
| B | FUERA | 59 | 42 | 0.45x | 74% | 48% | 8% | 2% | 4% (n=50) | 5% (n=44) | 50% (n=2) |
| B | WATCH | 236 | 140 | 0.25x | 84% | 39% | 12% | 5% | 14% (n=192) | 11% (n=190) | 8% (n=130) |
| C-meta | 🟡 META ACTIVÁNDOSE | 97 | 37 | 0.83x | 35% | 24% | 7% | 1% | 42% (n=33) | 22% (n=23) | 7% (n=14) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 243 | 76 | 0.33x | 72% | 1% | 0% | 2% (n=223) | 0% (n=220) | 1% (n=144) |
| dev vendió | 138 | 101 | 0.31x | 91% | 8% | 4% | 7% (n=134) | 6% (n=127) | 8% (n=66) |
| compras en el bloque de creación | 79 | 60 | 0.27x | 97% | 8% | 3% | 9% (n=79) | 6% (n=78) | 4% (n=49) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=1) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
