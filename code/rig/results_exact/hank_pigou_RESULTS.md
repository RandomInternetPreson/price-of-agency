# HANK port v0.1 — the externality priced: private vs social schedule entropy, Pigou tax (2026-11-09)

Firm labor-cost factor g(S) = 1 − η(1 − e^{−S}) + νS²/2 with η = 0.06, ν = 0.02: the private optimum (min g) is S_priv = 1.0 by construction. Welfare: aggregate true-β value in consumption equivalents, each S at its own GE steady state (r, Y clear) at the control's β, vphi. Control economy: same firm, bandwidth channel off.

| S | g(S) | control: r, Y, CE-welfare | model: r, Y, BW, HTM_low, CE-welfare | model − control CE |
|---|---|---|---|---|
| 0.0 | 1.0000 | 0.0052, 1.0048, 0.83890 | 0.0054, 1.0061, 0.903, 0.577, 0.83830 | -0.00060 |
| 0.25 | 0.9874 | 0.0051, 1.0026, 0.84591 | 0.0057, 1.0058, 0.839, 0.597, 0.84438 | -0.00153 |
| 0.5 | 0.9789 | 0.0051, 1.0012, 0.85068 | 0.0060, 1.0061, 0.786, 0.613, 0.84824 | -0.00244 |
| 0.75 | 0.9740 | 0.0050, 1.0003, 0.85350 | 0.0064, 1.0069, 0.741, 0.627, 0.85017 | -0.00332 |
| 1.0 | 0.9721 | 0.0050, 1.0000, 0.85458 | 0.0067, 1.0081, 0.703, 0.638, 0.85041 | -0.00417 |
| 1.25 | 0.9728 | 0.0050, 1.0001, 0.85416 | 0.0071, 1.0097, 0.668, 0.648, 0.84917 | -0.00499 |
| 1.5 | 0.9759 | 0.0050, 1.0007, 0.85240 | 0.0075, 1.0116, 0.637, 0.655, 0.84662 | -0.00577 |
| 2.0 | 0.9881 | 0.0051, 1.0027, 0.84548 | 0.0083, 1.0163, 0.581, 0.666, 0.83825 | -0.00722 |

S_priv (firm's private optimum, min g) = 1.055; S_soc (model planner, max CE welfare) = 0.916; control planner = 1.055 (the control's planner and firm agree up to the grid: no externality there).
Pigou tax τ* = −g'(S_soc) = 0.0057 per unit of S per unit of the wage bill: with it the firm's private FOC g'(S) + τ* = 0 holds at S_soc.

GE at (S_soc, τ*), revenue rebated: r = 0.0066, Y = 1.0063, BW = 0.715, CE welfare = 0.84934 (vs 0.85041 at the grid optimum without the tax: the rebate is lump-sum, so the difference is the incidence of the rebate, not the allocation).
Runtime 745s.
