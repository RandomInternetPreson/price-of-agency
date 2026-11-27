# Field-audit identification: gate vs slope (design study, 2026-11-09)

DGP: 4 bandwidth levels, p_up = 0.16, mean entropy drain 0.08, free time U(0.5,1.5), gate at 1.0; HtM logistic in bandwidth (α=1.0, γ=2.5). 200 replications per cell. Detection rule A: BIC prefers the step model over the slope model. Rule B: max-LR test (step added to slope) with critical value = 95th percentile of the same statistic under the widest-ramp DGP (size-controlled by construction).

## Power of detecting the gate (DGP = sharp gate), by N and measurement error σ_T

| N | σ_T | rule A (BIC) | rule B (max-LR, 5%) | LR critical value |
|---|---|---|---|---|
| 1000 | 0.0 | 0.99 | 0.99 | 14.0 |
| 1000 | 0.1 | 0.60 | 0.57 | 14.2 |
| 1000 | 0.2 | 0.18 | 0.28 | 11.3 |
| 3000 | 0.0 | 1.00 | 1.00 | 21.0 |
| 3000 | 0.1 | 0.80 | 0.99 | 18.2 |
| 3000 | 0.2 | 0.07 | 0.61 | 14.9 |
| 10000 | 0.0 | 1.00 | 1.00 | 40.7 |
| 10000 | 0.1 | 0.85 | 1.00 | 36.3 |
| 10000 | 0.2 | 0.01 | 0.97 | 24.7 |
| 30000 | 0.0 | 1.00 | 1.00 | 85.6 |
| 30000 | 0.1 | 0.97 | 1.00 | 64.2 |
| 30000 | 0.2 | 0.00 | 1.00 | 48.2 |

## Detection rate when the DGP is a RAMP (σ_T = 0.1): how wide a slope still reads as a gate

| N | ramp half-width | rule A | rule B |
|---|---|---|---|
| 3000 | 0.0 | 0.70 | 1.00 |
| 3000 | 0.1 | 0.54 | 0.97 |
| 3000 | 0.25 | 0.09 | 0.58 |
| 3000 | 0.5 | 0.01 | 0.07 |
| 10000 | 0.0 | 0.90 | 1.00 |
| 10000 | 0.1 | 0.61 | 1.00 |
| 10000 | 0.25 | 0.01 | 0.94 |
| 10000 | 0.5 | 0.00 | 0.02 |

Reading. Rule B is size-controlled at the widest ramp by construction (0.05 there). The question the table answers is the audit's: at ATUS/SHED-scale samples (10,000–30,000) and measurement error of a tenth of an hour-unit, is a sharp gate distinguishable from a ramp of a given width? Where the ramp column equals the gate column, the audit cannot tell them apart at that N. Nothing here is a statement about the world; the DGP is the book's own block, reduced to one worker.
Runtime 420s.
