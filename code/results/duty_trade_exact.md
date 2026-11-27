# Who is on call (2026-11-10) — the same burden, drawn by lot or sold

Nine boats; k on call each day; skill fades on call (rate λ) and returns with reading (rate μ = 0.02); d = how much of an on-call day's reading is lost. Long-run skill at the mean of the dynamics; famine and mean catch exact given those accuracies.

## p_max = 0.7

| k on call | d | λ/μ | LOT: every boat's skill | mean catch | famine | TRADE: sellers' / buyers' skill | mean catch | famine | trade raises mean catch | trade raises famine |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | 0.5 | 0.25 | 0.686 | 0.662 | 22.2% | 0.250 / 0.700 | 0.650 | 26.5% | no | YES |
| 1 | 0.5 | 1.0 | 0.650 | 0.628 | 48.1% | 0.250 / 0.700 | 0.650 | 26.5% | yes | no |
| 1 | 0.5 | 4.0 | 0.550 | 0.533 | 98.9% | 0.250 / 0.700 | 0.650 | 26.5% | yes | no |
| 1 | 1.0 | 0.25 | 0.686 | 0.638 | 35.8% | 0.250 / 0.700 | 0.650 | 26.5% | yes | no |
| 1 | 1.0 | 1.0 | 0.650 | 0.606 | 64.7% | 0.250 / 0.700 | 0.650 | 26.5% | yes | no |
| 1 | 1.0 | 4.0 | 0.550 | 0.517 | 99.7% | 0.250 / 0.700 | 0.650 | 26.5% | yes | no |
| 2 | 0.5 | 0.25 | 0.670 | 0.623 | 51.1% | 0.250 / 0.700 | 0.600 | 65.0% | no | YES |
| 2 | 0.5 | 1.0 | 0.600 | 0.561 | 93.7% | 0.250 / 0.700 | 0.600 | 65.0% | yes | no |
| 2 | 0.5 | 4.0 | 0.460 | 0.437 | 100.0% | 0.250 / 0.700 | 0.600 | 65.0% | yes | no |
| 2 | 1.0 | 0.25 | 0.670 | 0.577 | 84.1% | 0.250 / 0.700 | 0.600 | 65.0% | yes | no |
| 2 | 1.0 | 1.0 | 0.600 | 0.522 | 99.5% | 0.250 / 0.700 | 0.600 | 65.0% | yes | no |
| 2 | 1.0 | 4.0 | 0.460 | 0.413 | 100.0% | 0.250 / 0.700 | 0.600 | 65.0% | yes | no |
| 3 | 0.5 | 0.25 | 0.650 | 0.583 | 83.0% | 0.250 / 0.700 | 0.550 | 95.1% | no | YES |
| 3 | 0.5 | 1.0 | 0.550 | 0.500 | 99.9% | 0.250 / 0.700 | 0.550 | 95.1% | yes | no |
| 3 | 0.5 | 4.0 | 0.400 | 0.375 | 100.0% | 0.250 / 0.700 | 0.550 | 95.1% | yes | no |
| 3 | 1.0 | 0.25 | 0.650 | 0.517 | 99.6% | 0.250 / 0.700 | 0.550 | 95.1% | yes | no |
| 3 | 1.0 | 1.0 | 0.550 | 0.450 | 100.0% | 0.250 / 0.700 | 0.550 | 95.1% | yes | no |
| 3 | 1.0 | 4.0 | 0.400 | 0.350 | 100.0% | 0.250 / 0.700 | 0.550 | 95.1% | yes | no |
| 4 | 0.5 | 0.25 | 0.625 | 0.542 | 97.9% | 0.250 / 0.700 | 0.500 | 99.9% | no | YES |
| 4 | 0.5 | 1.0 | 0.500 | 0.444 | 100.0% | 0.250 / 0.700 | 0.500 | 99.9% | yes | no |
| 4 | 0.5 | 4.0 | 0.357 | 0.333 | 100.0% | 0.250 / 0.700 | 0.500 | 99.9% | yes | no |
| 4 | 1.0 | 0.25 | 0.625 | 0.458 | 100.0% | 0.250 / 0.700 | 0.500 | 99.9% | yes | no |
| 4 | 1.0 | 1.0 | 0.500 | 0.389 | 100.0% | 0.250 / 0.700 | 0.500 | 99.9% | yes | no |
| 4 | 1.0 | 4.0 | 0.357 | 0.310 | 100.0% | 0.250 / 0.700 | 0.500 | 99.9% | yes | no |

## Across all 48 cases (p_max 0.7 and 0.8; k 1–4; d 0.5, 1; λ/μ 0.25, 1, 4)

- trade raises the mean catch AND raises famine (every party can be made whole and the town starves more often): **0**
- trade raises the mean catch and lowers famine (specialization pays the town too): **40**
- trade lowers the mean catch and raises famine (no compensated trade is possible; lot is better on both): **8**
- trade lowers the mean catch and lowers famine: **0**

## The rule the numbers follow
Total skill kept by the fleet: by lot, 9 (1−f) μ Δ / ((1−f) μ + f λ) above chance; by trade, 9 (1−f) Δ (Δ = p_max − 1/4, f = k/9). So the lot keeps more skill than the trade exactly when skill fades more slowly than it returns (λ < μ), and less when it fades faster — and on top of that, by lot an on-call boat still brings whatever its skill is worth that day (d < 1), where a boat that is always on call brings chance.

## The buyer's own ledger (always the same sign)
A boat that buys its way off the rota reads every day: its own accuracy goes from the lot's mix to p_max in every case above. The trade is therefore always wanted by the buyer; whether the sellers can be made whole is the mean-catch column; whether the town is better off is the famine column. The three need not agree.
