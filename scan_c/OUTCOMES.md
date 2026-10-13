# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-13 09:38 UTC** · 802 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 427 | 215 | 0.31x | 86% | 27% | 5% | 2% | 5% (n=398) | 3% (n=390) | 3% (n=243) |
| B | FUERA | 54 | 34 | 0.46x | 68% | 44% | 8% | 2% | 4% (n=48) | 5% (n=42) | 50% (n=2) |
| B | WATCH | 224 | 133 | 0.25x | 84% | 40% | 13% | 6% | 15% (n=179) | 12% (n=177) | 8% (n=122) |
| C-meta | 🟡 META ACTIVÁNDOSE | 96 | 34 | 0.84x | 35% | 24% | 7% | 1% | 44% (n=32) | 23% (n=22) | 7% (n=14) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 220 | 68 | 0.35x | 69% | 1% | 0% | 3% (n=198) | 1% (n=195) | 1% (n=129) |
| dev vendió | 128 | 91 | 0.30x | 91% | 9% | 4% | 6% (n=123) | 6% (n=118) | 8% (n=63) |
| compras en el bloque de creación | 73 | 50 | 0.27x | 96% | 7% | 1% | 7% (n=71) | 6% (n=71) | 2% (n=45) |
| volumen en bucle | 4 | 4 | 0.12x | 100% | 25% | 25% | 50% (n=4) | 0% (n=4) | 0% (n=4) |
| impuesto modificable | 4 | 2 | 0.45x | 50% | 0% | 0% | 0% (n=3) | 0% (n=2) | 0% (n=1) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| puede crear tokens | 1 | 1 | 0.95x | 0% | 0% | 0% | — | — | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
