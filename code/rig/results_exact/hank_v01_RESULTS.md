# HANK port v0.1 — preregistered predictions in general equilibrium (2026-11-09)

Every entry is model minus control unless marked level. GE: (r, Y) clear markets at the control's β, vphi. PE: prices at the control's values. Host and constants: hank_ge.py; preregistration: docs/HANK_PREREG_v0.1.md.

## Baselines (levels)

| economy | r (qtr) | Y | HTM | HTM_low | BW | BW_low | SCARCE | A |
|---|---|---|---|---|---|---|---|---|
| control GE | 0.0050 | 1.0000 | 0.153 | 0.568 | 0.705 | 0.307 | 0.140 | 5.600 |
| model GE | 0.0067 | 1.0081 | 0.225 | 0.632 | 0.703 | 0.302 | 0.156 | 5.600 |
| model PE | 0.0050 | 1.0000 | 0.246 | 0.677 | 0.701 | 0.296 | 0.167 | 4.784 |

## P-A′ — time transfer (floor across the gate) vs equal-cost money transfer; low-skill group

Time transfer dT = 0.25 (free time 0.80 → 1.05 at N = 1); equal cost = w·e_low·dT = 0.0909 per low household, both tax-financed.

| arm | eq. | ΔHTM_low model | ΔHTM_low control | model − control | ΔWELF_low model−control | ΔBW_low model |
|---|---|---|---|---|---|---|
| time | GE | -0.0320 | -0.0040 | -0.0281 | +0.3006 | +0.349 |
| time | PE | -0.0294 | +0.0010 | -0.0303 | +0.4456 | +0.347 |
| money | GE | +0.0492 | +0.0657 | -0.0165 | +0.0828 | -0.009 |
| money | PE | +0.1135 | +0.1712 | -0.0577 | +0.6007 | -0.019 |

## P-B — schedule stability (low-skill entropy halved) vs equal-dollar transfer; two metrics

Both arms cost 0.02 per low household. Welfare is true-β value of the low group.

| arm | eq. | ΔHTM_low (model−control) | ΔWELF_low (model−control) | ΔBW_low model | Δscarce_low model |
|---|---|---|---|---|---|
| stability | GE | -0.0161 | +0.1413 | +0.115 | -0.017 |
| stability | PE | -0.0164 | +0.1958 | +0.109 | -0.016 |
| wage | GE | +0.0008 | +0.0328 | -0.002 | +0.007 |
| wage | PE | -0.0083 | +0.1721 | -0.005 | +0.026 |

## P-C — hand-to-mouth after liquidity is repaired (borrowing limit 0 → 0.5), bandwidth not

| eq. | HTM_low control | HTM_low model | residual (model − control) | residual at baseline | model, liquidity + bandwidth repaired |
|---|---|---|---|---|---|
| GE | 0.5362 | 0.6112 | +0.0750 | +0.0640 | 0.5678 |
| PE | 0.5692 | 0.6848 | +0.1156 | +0.1092 | 0.6430 |

## P-E — the externality: schedule entropy S and the equilibrium real rate

| S | r* GE (qtr) | Y GE | BW GE | HTM GE | A at control prices (PE) | BW PE |
|---|---|---|---|---|---|---|
| 0.0 | 0.0051 | 1.0013 | 0.903 | 0.176 | 5.530 | 0.903 |
| 0.5 | 0.0059 | 1.0049 | 0.787 | 0.204 | 5.143 | 0.784 |
| 1.0 | 0.0067 | 1.0081 | 0.703 | 0.225 | 4.784 | 0.701 |
| 1.5 | 0.0074 | 1.0109 | 0.637 | 0.240 | 4.447 | 0.636 |
| 2.0 | 0.0081 | 1.0134 | 0.581 | 0.251 | 4.131 | 0.580 |

### The cascade: hours through the middle group's time gate (PE, model)

| N | free time mid | BW | BW_mid | HTM | A |
|---|---|---|---|---|---|
| 0.98 | 1.070 | 0.701 | 0.800 | 0.246 | 4.692 |
| 1.0 | 1.050 | 0.701 | 0.800 | 0.246 | 4.784 |
| 1.02 | 1.030 | 0.701 | 0.800 | 0.245 | 4.876 |
| 1.04 | 1.010 | 0.701 | 0.800 | 0.244 | 4.967 |
| 1.049 | 1.001 | 0.701 | 0.800 | 0.243 | 5.008 |
| 1.051 | 0.999 | 0.343 | 0.270 | 0.407 | 3.884 |
| 1.06 | 0.990 | 0.343 | 0.270 | 0.406 | 3.913 |
| 1.08 | 0.970 | 0.343 | 0.270 | 0.403 | 3.977 |
| 1.1 | 0.950 | 0.343 | 0.270 | 0.401 | 4.040 |

## Dose–response (GE, model − control at baseline policies)

| dose | k_tax | tunnel | Δr* | ΔHTM_low | ΔBW | ΔA (PE) |
|---|---|---|---|---|---|---|
| 0.0 | 0.0000 | 0.0000 | +0.0000 | -0.0000 | +0.000 | +0.000 |
| 0.25 | 0.0125 | 0.0038 | +0.0005 | +0.0204 | -0.001 | -0.240 |
| 0.5 | 0.0250 | 0.0076 | +0.0009 | +0.0394 | -0.001 | -0.459 |
| 1.0 | 0.0500 | 0.0153 | +0.0017 | +0.0640 | -0.002 | -0.816 |
| 1.5 | 0.0750 | 0.0229 | +0.0023 | +0.0808 | -0.003 | -1.105 |

## Forecast comparison (PE): naive vs sophisticated household

The default household is naive about its own bandwidth (plans as if its level were permanent). The sophisticated variant forecasts its own degradation. Same knobs, same policies.

| forecast | economy | HTM_low | a_low | A | BW_low |
|---|---|---|---|---|---|
| naive | baseline | 0.6775 | 1.108 | 4.784 | 0.296 |
| naive | time transfer | 0.6479 | 1.174 | 4.910 | 0.643 |
| naive | stability | 0.6612 | 1.154 | 4.839 | 0.405 |
| naive | no drain at all | 0.5683 | 1.477 | 5.600 | 1.000 |
| sophisticated | baseline | 0.8099 | 0.746 | 3.903 | 0.269 |
| sophisticated | time transfer | 0.8050 | 0.786 | 4.037 | 0.618 |
| sophisticated | stability | 0.8395 | 0.663 | 3.702 | 0.350 |
| sophisticated | no drain at all | 0.5683 | 1.477 | 5.600 | 1.000 |

Runtime 678s.
