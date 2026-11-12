# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-11-12 02:32 UTC** · 2240 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1193 | 746 | 0.33x | 75% | 24% | 5% | 2% | 5% (n=1108) | 3% (n=1096) | 2% (n=760) |
| B | FUERA | 153 | 117 | 0.44x | 78% | 48% | 9% | 2% | 7% (n=119) | 7% (n=113) | 50% (n=4) |
| B | WATCH | 596 | 458 | 0.26x | 90% | 37% | 11% | 5% | 11% (n=462) | 8% (n=457) | 6% (n=345) |
| C-meta | 🟡 META ACTIVÁNDOSE | 296 | 167 | 0.86x | 29% | 24% | 7% | 2% | 41% (n=93) | 24% (n=62) | 11% (n=37) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 725 | 317 | 0.46x | 53% | 4% | 1% | 2% (n=665) | 2% (n=659) | 1% (n=483) |
| dev vendió | 251 | 228 | 0.28x | 93% | 8% | 3% | 7% (n=234) | 4% (n=229) | 5% (n=140) |
| compras en el bloque de creación | 203 | 187 | 0.27x | 91% | 8% | 3% | 9% (n=195) | 5% (n=194) | 4% (n=129) |
| volumen en bucle | 12 | 12 | 0.34x | 92% | 8% | 8% | 17% (n=12) | 0% (n=12) | 0% (n=6) |
| impuesto modificable | 7 | 7 | 0.64x | 29% | 0% | 0% | 14% (n=7) | 0% (n=5) | 0% (n=5) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| puede crear tokens | 2 | 2 | 0.98x | 0% | 0% | 0% | — | — | — |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
