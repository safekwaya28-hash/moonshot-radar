# OUTCOMES — qué pasó después de cada decisión (incluidas las descartadas)
**2026-11-26 03:51 UTC** · 2475 monedas seguidas · la decisión original nunca se cambia

| Escáner | Decisión | Monedas | con 24h | Mediana MC 24h / inicial | Muertas a 24h (≤ −50%) | Máx. ≥2x | ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|---|---|
| A | NO | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |
| B | DESCARTAR | 1353 | 818 | 0.33x | 74% | 23% | 5% | 2% | 4% (n=1261) | 3% (n=1250) | 2% (n=906) |
| B | FUERA | 168 | 129 | 0.43x | 79% | 48% | 10% | 2% | 8% (n=132) | 8% (n=126) | 23% (n=13) |
| B | WATCH | 642 | 484 | 0.26x | 90% | 37% | 11% | 5% | 11% (n=489) | 8% (n=485) | 6% (n=374) |
| C-meta | 🟡 META ACTIVÁNDOSE | 310 | 177 | 0.86x | 29% | 24% | 7% | 2% | 41% (n=99) | 25% (n=65) | 10% (n=39) |
| C-meta | 🟢 CANDIDATA | 1 | 1 | 0.03x | 100% | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | 0% (n=1) |

## ¿Qué filtro mata ganadoras? (descartadas por motivo)

| Motivo del descarte | Monedas | con 24h | Mediana 24h | Muertas a 24h | Máx. ≥5x | ≥10x | 2x antes de −30% | 5x antes de −50% | 10x antes de −70% |
|---|---|---|---|---|---|---|---|---|---|
| concentración | 858 | 364 | 0.48x | 51% | 3% | 1% | 2% (n=793) | 2% (n=787) | 1% (n=604) |
| dev vendió | 271 | 244 | 0.27x | 92% | 8% | 3% | 8% (n=252) | 4% (n=248) | 5% (n=159) |
| compras en el bloque de creación | 210 | 196 | 0.27x | 91% | 7% | 3% | 9% (n=202) | 5% (n=201) | 4% (n=135) |
| volumen en bucle | 12 | 12 | 0.34x | 92% | 8% | 8% | 17% (n=12) | 0% (n=12) | 0% (n=6) |
| impuesto modificable | 7 | 7 | 0.64x | 29% | 0% | 0% | 14% (n=7) | 0% (n=5) | 0% (n=5) |
| snipers | 2 | 2 | 0.16x | 100% | 0% | 0% | 0% (n=2) | 0% (n=2) | 0% (n=2) |
| puede crear tokens | 2 | 2 | 0.98x | 0% | 0% | 0% | — | — | — |
| extensión peligrosa | 1 | 1 | 1.00x | 0% | 0% | 0% | 0% (n=1) | 0% (n=1) | — |

Lectura: un filtro es bueno si sus descartadas mueren mucho y casi nunca hacen ≥5x. Si un motivo tiene muchas ≥5x, ese filtro está matando ganadoras y hay que revisarlo. Con < 30 monedas por fila, todavía es ruido.
Máximo = velas de 1 h desde la decisión cuando hay; si no, el máximo observado en las pasadas (puede quedarse corto).
**"2x antes de −30%"** es la métrica operable: de las que ya se resolvieron, % que llegó al objetivo ANTES de caer al stop (si ambos ocurren en la misma vela de 1 h, cuenta como stop). Un 10x que antes cayó −80% no cuenta como operable.
