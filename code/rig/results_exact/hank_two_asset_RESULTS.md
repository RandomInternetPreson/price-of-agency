# Two-asset host (liquid + illiquid): the hand-to-mouth results, stress objective #9 (2026-11-09)

Liquid return 0.005/qtr, illiquid 0.015/qtr, fixed fee 0.02 and proportional fee 0.02 on moving the illiquid account; control's β = 0.9746 calibrated to liquid assets = 1.04. Hand-to-mouth (HtM) = liquid savings within 0.15 of the limit; wealthy HtM = HtM holding illiquid wealth above 0.5. Fixed returns unless marked. Naive forecast. Bandwidth constants as in the one-asset host.

## 1. Levels

| economy | liquid A | illiquid K | HtM | wealthy HtM | poor HtM | HtM low-skill | BW | mass at top of a / k grid |
|---|---|---|---|---|---|---|---|---|
| control | 1.040 | 5.808 | 0.448 | 0.263 | 0.185 | 0.576 | 0.701 | 0.0000 / 0.0000 |
| model | 0.889 | 4.533 | 0.469 | 0.182 | 0.287 | 0.696 | 0.698 | 0.0000 / 0.0000 |
| noise face only | 1.007 | 5.604 | 0.460 | 0.239 | 0.221 | 0.600 | 0.701 | 0.0000 / 0.0000 |
| horizon face only | 0.912 | 4.737 | 0.476 | 0.193 | 0.283 | 0.678 | 0.698 | 0.0000 / 0.0000 |
| half dose | 0.957 | 5.015 | 0.464 | 0.207 | 0.257 | 0.644 | 0.700 | 0.0000 / 0.0000 |
| 1.5× dose | 0.838 | 4.178 | 0.475 | 0.158 | 0.317 | 0.731 | 0.697 | 0.0000 / 0.0000 |

## 2. The liquid rate that clears the liquid market at the control's β

Control: r_a = 0.0050. Model: r_a* = 0.0090 per quarter (+1.60 points a year). At that rate:

| control | 1.040 | 5.808 | 0.448 | 0.263 | 0.185 | 0.576 | 0.701 | 0.0000 / 0.0000 |
| model | 0.889 | 4.533 | 0.469 | 0.182 | 0.287 | 0.696 | 0.698 | 0.0000 / 0.0000 |
| model at r_a* | 1.040 | 4.720 | 0.423 | 0.157 | 0.266 | 0.677 | 0.699 | 0.0000 / 0.0000 |

## 3. Policies at fixed returns: low-skill group, model and control

| policy | HtM_low control | HtM_low model | residual (model − control) | Δ poor-HtM share model | Δ illiquid K_low model | ΔWELF_low model − control |
|---|---|---|---|---|---|---|
| none | 0.576 | 0.696 | +0.120 | — | — | — |
| liquidity repaired (limit 0 → 0.5) | 0.575 | 0.734 | +0.158 | +0.047 | -0.100 | -0.485 |
| time transfer (floor across the gate) | 0.578 | 0.667 | +0.089 | -0.026 | +0.081 | +0.551 |
| money transfer, equal cost | 0.735 | 0.804 | +0.069 | +0.162 | -0.513 | +1.251 |
| stability (low-skill entropy halved) | 0.577 | 0.679 | +0.103 | -0.012 | +0.067 | +0.278 |
| transfer, equal cost to stability | 0.622 | 0.729 | +0.107 | +0.051 | -0.160 | +0.438 |
| no drain at all | 0.576 | 0.576 | -0.000 | -0.102 | +0.683 | +2.401 |

Runtime 1479s.
