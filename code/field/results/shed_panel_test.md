# SHED within-person test (H4) and industry control (H5) — preregistration v0.2

Script: `code/field/shed_panel_test.py`. Descriptive, not causal: first differences remove fixed traits of a person, not the shocks that arrive with a change of schedule.

## Sample: 7390 adjacent-wave pairs from 4816 persons employed with a stated schedule type in both waves

| wave pair | pairs | stayed out (0→0) | moved in (0→1) | moved out (1→0) | stayed in (1→1) | own-request: moved in / out |
|---|---|---|---|---|---|---|
| 2019-2020 | 1817 | 1432 | 108 | 143 | 134 | 92 / 98 |
| 2020-2021 | 1876 | 1454 | 118 | 152 | 152 | 103 / 114 |
| 2021-2022 | 1824 | 1457 | 125 | 124 | 118 | 133 / 92 |
| 2022-2023 | 1873 | 1480 | 119 | 120 | 154 | 105 / 110 |
| all | 7390 | 5823 | 470 | 539 | 558 | 433 / 414 |

## H4a, H4b — change in outcome on change in schedule type (percentage points; person-bootstrap 95% intervals)

| outcome | ΔE (employer's needs) | ΔO (own request) | **ΔE − ΔO** | ΔE, adding Δ income band | ΔE, unweighted |
|---|---|---|---|---|---|
| strained | +3.0 [+0.3, +5.7] | -2.5 [-5.5, +0.5] | +5.6 [+1.8, +9.0] | +3.0 [+0.1, +5.8] | +2.0 [-0.5, +4.5] |
| billvar | +6.1 [+3.7, +8.7] | +2.3 [-0.2, +4.7] | +3.8 [+0.7, +7.0] | +6.1 [+3.8, +8.7] | +5.8 [+3.1, +8.2] |
| cant400 (secondary) | -0.5 [-2.6, +1.5] | +0.1 [-1.9, +2.2] | -0.6 [-3.1, +1.9] | -0.5 [-2.7, +1.3] | -0.8 [-2.4, +0.9] |
| nofund3 (secondary) | +1.8 [-1.4, +5.1] | -0.2 [-3.7, +3.5] | +2.0 [-2.3, +6.3] | +1.8 [-1.2, +5.6] | +2.4 [-0.5, +5.3] |

**H4a verdict: HOLDS.** ΔE coefficient: strained +3.0 [+0.3, +5.7], billvar +6.1 [+3.7, +8.7]; interval excludes zero on: strained, billvar.
**H4b verdict: HOLDS.** ΔE − ΔO: strained +5.6 [+1.8, +9.0], billvar +3.8 [+0.7, +7.0]; interval excludes zero on: strained, billvar.

ΔE coefficient by wave pair (weighted, pp):

| outcome | 2019-2020 | 2020-2021 | 2021-2022 | 2022-2023 |
|---|---|---|---|---|
| strained | +4.4 [+0.1, +9.7] | +1.1 [-3.7, +6.4] | +1.5 [-3.9, +6.6] | +5.6 [-0.8, +11.1] |
| billvar | +8.0 [+3.0, +13.1] | +0.9 [-3.4, +5.8] | +5.5 [+1.3, +9.4] | +11.0 [+4.7, +16.1] |
| cant400 | -1.2 [-5.6, +3.8] | -1.8 [-4.7, +0.6] | +0.4 [-4.1, +4.2] | +0.8 [-3.2, +5.1] |
| nofund3 | +0.5 [-5.9, +6.8] | +4.0 [-2.2, +10.1] | +1.3 [-4.4, +6.2] | +1.3 [-3.9, +6.4] |

## H4c — both directions (weighted mean within-person change, pp)

| outcome | stayed out (0→0) | moved in (0→1) | **in − stayed out** | stayed in (1→1) | moved out (1→0) | **out − stayed in** |
|---|---|---|---|---|---|---|
| strained | +0.7 | +5.0 | +4.3 [+0.2, +7.8] | -1.6 | -2.3 | -0.7 [-5.9, +4.4] |
| billvar | -0.4 | +4.8 | +5.2 [+1.1, +9.0] | -2.7 | -6.6 | -3.9 [-8.8, +0.6] |
| cant400 (secondary) | -0.3 | -0.3 | -0.0 [-3.1, +3.3] | -1.6 | +0.6 | +2.2 [-1.1, +5.6] |
| nofund3 (secondary) | -1.7 | +0.7 | +2.4 [-2.4, +7.4] | -0.9 | -3.3 | -2.4 [-8.0, +3.6] |

**H4c verdict: HOLDS.** Wrong-signed confirmatory outcomes: moving in 0 of 2, moving out 0 of 2 (committed: fails if either direction is wrong-signed on both).

## H5 — industry held fixed (pooled cross-section, all five waves; robustness, not out-of-sample)

29771 employee-wave observations from 19426 persons; 24 industry groups; intervals by bootstrap over persons. Largest groups: professional 3651, health 3513, education 3059, retail 2412, manufacturing 2134, finance 1903; other or not coded 1845.

| outcome | employer − own, no industry | employer − own, with industry | share kept | employer − same, with industry | own − same, with industry |
|---|---|---|---|---|---|
| strained | +7.0 [+5.0, +9.0] | +6.7 [+4.5, +8.6] | 96% | +6.0 [+4.6, +7.7] | -0.6 [-2.1, +0.9] |
| billvar | +6.4 [+4.7, +8.0] | +5.9 [+4.3, +7.4] | 92% | +9.6 [+8.4, +10.8] | +3.7 [+2.5, +5.0] |
| cant400 (secondary) | +2.7 [+1.5, +4.1] | +2.5 [+1.2, +3.9] | 91% | +2.4 [+1.5, +3.4] | -0.1 [-1.2, +1.2] |
| nofund3 (secondary) | +3.7 [+1.3, +6.2] | +3.4 [+1.0, +5.8] | 91% | +2.9 [+1.3, +4.6] | -0.4 [-2.5, +1.5] |

**H5 verdict: HOLDS.** With industry held fixed, employer − own is strained +6.7 pp (96% kept), billvar +5.9 pp (92% kept).

## Reading

H4 asks whether the same person reports more strain in the wave in which the employer holds the schedule than in the wave in which the employer does not; H5 asks whether the cross-sectional gap is an industry composition effect. Neither is an experiment. A change of schedule type usually arrives with a change of job; a strained household may take the job on offer; self-classification errors manufacture false switchers and pull first differences toward zero. The audit design (Chapter 13's box, items 6–9) is still owed.
