# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-13 13:50 UTC** · 842 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 453 | 233 | 0.31x | 87% | 27% | 5% | 2% | 5% (n=429) | 3% (n=419) | 3% (n=255) |
| B | FUERA | 57 | 41 | 0.46x | 73% | 46% | 8% | 2% | 4% (n=48) | 5% (n=42) | 50% (n=2) |
| B | WATCH | 235 | 137 | 0.26x | 84% | 39% | 12% | 5% | 14% (n=191) | 11% (n=189) | 8% (n=128) |
| C-meta | 🟡 META ACTIVÁNDOSE | 96 | 35 | 0.83x | 34% | 24% | 7% | 1% | 42% (n=33) | 22% (n=23) | 7% (n=14) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 236 | 73 | 0.33x | 71% | 1% | 0% | 2% (n=216) | 0% (n=213) | 1% (n=139) |
| dev vendió | 133 | 96 | 0.31x | 92% | 8% | 4% | 7% (n=129) | 6% (n=123) | 8% (n=63) |
| compras en el bloque de creación | 78 | 58 | 0.27x | 97% | 8% | 1% | 9% (n=78) | 6% (n=77) | 2% (n=47) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=1) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
