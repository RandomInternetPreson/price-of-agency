# Sign-stability map — 688 successful draws over the box in sweep_signs.py

| result | holds (all) | naive | sophisticated |
|---|---|---|---|
| GE transmission: r_model > r_ctrl | 1.000 (688) | 1.000 (526) | 1.000 (162) |
| asset demand falls at fixed prices | 1.000 (688) | 1.000 (526) | 1.000 (162) |
| dose: half dose gives smaller dr | 1.000 (688) | 1.000 (526) | 1.000 (162) |
| P-A' GE: time < money < 0 (model-control HtM_low) | 0.238 (688) | 0.272 (526) | 0.130 (162) |
| P-A' GE: time beats money | 0.381 (688) | 0.422 (526) | 0.247 (162) |
| P-A' PE: time beats money | 0.205 (688) | 0.217 (526) | 0.167 (162) |
| P-B GE: stability beats wage on HtM | 0.513 (688) | 0.639 (526) | 0.105 (162) |
| P-B GE: stability beats wage on welfare | 0.936 (688) | 0.996 (526) | 0.741 (162) |
| P-C GE: residual > 0 after liquidity repair | 0.746 (688) | 0.738 (526) | 0.772 (162) |
| P-E: dr*/dS > 0 | 0.993 (688) | 1.000 (526) | 0.969 (162) |
| P-E: dA/dS < 0 at fixed prices | 0.988 (688) | 1.000 (526) | 0.951 (162) |
| HtM_low higher in model (GE) | 0.749 (688) | 0.745 (526) | 0.759 (162) |

## Where results fail (mean of each parameter, holds vs fails, naive draws)

- **P-A' GE: time < money < 0 (model-control HtM_low)** fails in 383/526 naive draws; failing draws differ most in: tunnel (-0.34 sd), B (-0.30 sd), k_tax (+0.39 sd), eis (+0.66 sd)
- **P-A' GE: time beats money** fails in 304/526 naive draws; failing draws differ most in: B (-0.55 sd), sigma_s (-0.32 sd), k_tax (+0.74 sd), eis (+1.04 sd)
- **P-A' PE: time beats money** fails in 412/526 naive draws; failing draws differ most in: Tbar_low (-0.71 sd), B (-0.70 sd), k_tax (+0.55 sd), eis (+1.02 sd)
- **P-B GE: stability beats wage on HtM** fails in 190/526 naive draws; failing draws differ most in: B (-0.61 sd), tunnel (-0.35 sd), k_tax (+0.84 sd), eis (+1.00 sd)
- **P-B GE: stability beats wage on welfare** fails in 2/526 naive draws; failing draws differ most in: mu (-1.39 sd), B (-1.38 sd), rho_s (+1.44 sd), sigma_s (+1.52 sd)
- **P-C GE: residual > 0 after liquidity repair** fails in 138/526 naive draws; failing draws differ most in: B (-0.70 sd), sigma_s (-0.35 sd), k_tax (+0.74 sd), eis (+1.22 sd)
- **HtM_low higher in model (GE)** fails in 134/526 naive draws; failing draws differ most in: B (-0.75 sd), sigma_s (-0.41 sd), k_tax (+0.77 sd), eis (+1.17 sd)
