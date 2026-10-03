# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-10-03 11:25 UTC** · 71 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | — | — | — |
| B | DESCARTAR | 45 | 7 | 0.30x | 86% | 49% | 11% | 3% | 19% (n=37) | 10% (n=31) | 5% (n=21) |
| B | FUERA | 5 | 1 | 0.52x | 0% | 25% | 0% | 0% | 0% (n=3) | 0% (n=2) | — |
| B | WATCH | 14 | 5 | 0.15x | 100% | 42% | 8% | 0% | 8% (n=12) | 0% (n=11) | 0% (n=5) |
| C-meta | 🟡 META ACTIVÁNDOSE | 6 | 1 | 0.46x | 100% | 20% | 20% | 0% | 50% (n=2) | 50% (n=2) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 20 | 1 | 0.33x | 100% | 0% | 0% | 17% (n=12) | 0% (n=10) | 0% (n=7) |
| dev vendió | 12 | 5 | 0.30x | 80% | 8% | 8% | 25% (n=12) | 12% (n=8) | 20% (n=5) |
| compras en el bloque de creación | 11 | 1 | 0.23x | 100% | 27% | 0% | 18% (n=11) | 18% (n=11) | 0% (n=7) |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | — | — | — |
| snipers | 1 | 0 | —x | — | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |
| volumen en bucle | 1 | 0 | —x | — | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
