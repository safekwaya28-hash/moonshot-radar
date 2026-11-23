# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-11-23 14:48 UTC** · 2439 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1334 | 808 | 0.33x | 74% | 23% | 5% | 2% | 4% (n=1242) | 3% (n=1231) | 2% (n=888) |
| B | FUERA | 166 | 125 | 0.43x | 78% | 48% | 10% | 2% | 8% (n=130) | 8% (n=124) | 27% (n=11) |
| B | WATCH | 633 | 481 | 0.25x | 90% | 37% | 11% | 5% | 12% (n=486) | 8% (n=482) | 6% (n=371) |
| C-meta | 🟡 META ACTIVÁNDOSE | 304 | 172 | 0.86x | 28% | 23% | 6% | 2% | 40% (n=95) | 24% (n=63) | 11% (n=37) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 843 | 358 | 0.48x | 51% | 3% | 1% | 2% (n=778) | 1% (n=772) | 1% (n=590) |
| dev vendió | 267 | 241 | 0.27x | 92% | 8% | 3% | 8% (n=248) | 5% (n=244) | 5% (n=155) |
| compras en el bloque de creación | 210 | 195 | 0.26x | 91% | 7% | 3% | 9% (n=202) | 5% (n=201) | 4% (n=135) |
| volumen en bucle | 12 | 12 | 0.34x | 92% | 8% | 8% | 17% (n=12) | 0% (n=12) | 0% (n=6) |
| impuesto modificable | 7 | 7 | 0.64x | 29% | 0% | 0% | 14% (n=7) | 0% (n=5) | 0% (n=5) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| puede crear tokens | 2 | 2 | 0.98x | 0% | 0% | 0% | — | — | — |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
