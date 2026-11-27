# HANK v0.2 — households choose their hours, and their hours set their gate (2026-11-09)

Host: sticky prices, flexible wage clearing efficiency hours, bonds fixed. Hours grid {0.75, 1.0, 1.25}; the low-skill floor is below the gate at 1.0 and above it at 0.75 (the short shift buys the gate); the middle floor is above the gate at 1.0 and below at 1.25 (the long shift sells it). Control: knobs off.

## 1. The sold floor (GE levels)

| economy | r | Y | hours low/mid/high | share below own gate low/mid/high | BW low/mid/high | HTM |
|---|---|---|---|---|---|---|
| control | 0.0050 | 1.0000 | 1.167/0.985/0.975 | 0.91/0.09/0.00 | 0.31/0.77/0.90 | 0.190 |
| model, naive | 0.0066 | 1.0049 | 1.159/1.000/0.972 | 0.90/0.17/0.00 | 0.30/0.74/0.89 | 0.273 |
| model, sophisticated | 0.0132 | 1.0855 | 1.181/1.192/0.958 | 0.97/0.86/0.00 | 0.10/0.27/0.73 | 0.341 |

## 2. Time transfer vs equal-cost money transfer, hours endogenous (low-skill group, GE, model − control)

Time transfer dT = 0.3 (the floor clears the gate at full-time hours); equal cost = w·e_low·dT = 0.1091.

| arm | Δhours_low model | Δhours_low control | Δbelow-gate low (model) | ΔHTM_low model−control | ΔBW_low model | ΔWELF model−control |
|---|---|---|---|---|---|---|
| time | +0.005 | +0.003 | -0.15 | +0.0034 | +0.041 | +0.015 |
| money | -0.060 | -0.029 | -0.04 | -0.0493 | +0.004 | +0.007 |

## 3. Working-time regulation (no long shift for anyone: hours grid {0.75, 1.0}) vs a low-skill wage subsidy of equal fiscal cost (GE)

| policy | economy | hours low/mid | below-gate low/mid | BW low/mid | HTM | Y | WELF − baseline |
|---|---|---|---|---|---|---|---|
| regulation | control | 0.983/0.966 | 0.93/0.00 | 0.33/0.80 | 0.155 | 0.9718 | -1.531 |
| regulation | model | 0.979/0.963 | 0.92/0.00 | 0.33/0.81 | 0.238 | 0.9666 | -1.661 |
| subsidy | control | 1.163/0.986 | 0.91/0.10 | 0.30/0.77 | 0.216 | 1.0012 | +0.479 |
| subsidy | model | 1.152/1.002 | 0.89/0.18 | 0.30/0.74 | 0.283 | 1.0061 | +0.489 |

## 4. Monetary transmission with own hours: impact ΔY model/control = 0.69, cumulative 0.80 (one-asset host: 1.78 / 1.58).

Runtime 1184s.
