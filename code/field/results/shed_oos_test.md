# SHED out-of-sample test — the preregistered H1–H3 on the 2019, 2020 and 2021 public-use files

Preregistration: `docs/SHED_PREREG_v0.1.md` (written with only 2022 and 2023 open). Script: `code/field/shed_oos_test.py`. Descriptive, not causal.

- 2019: 6305 employees with a stated schedule type; plumbing P1, P2, P3, P4, P5 (7 refused schedule type dropped); outcome refusals dropped per regression: cant400 23, notcash400 23, nofund3 16, strained 4, incvar 16, billvar 16.
- 2020: 5925 employees with a stated schedule type; plumbing P1, P2, P3, P4, P5 (11 refused schedule type dropped); outcome refusals dropped per regression: cant400 26, notcash400 26, nofund3 15, strained 4, incvar 14, billvar 15.
- 2021: 6038 employees with a stated schedule type; plumbing none; outcome refusals dropped per regression: cant400 0, notcash400 0, nofund3 0, strained 0, incvar 0, billvar 0.

Pooled out-of-sample: 18268 employees. Weighted shares: same 74.5%, own 9.3%, employer 16.2%.
Some respondents are interviewed in more than one wave; the pooled intervals ignore that, the single-wave rows do not depend on it.

## 0. Coding check against the Federal Reserve's published headline (all adults, weighted)

| wave | would not cover a $400 expense entirely with cash or its equivalent (this script) | published |
|---|---|---|
| 2019 | 36.5% | 37% |
| 2020 | 35.6% | 36% |
| 2021 | 32.3% | 32% |

## 0b. Reconstruction check: the 2022 exploratory contrast re-derived by this script (compare first-look tables 5 and 6)

| outcome | sample | n employer-varying with notice | under 3 weeks − 3 weeks or more | 3+ weeks − same hours | under 3 weeks − same hours | (no full/part-time) under − 3+ | 3+ − same | under − same |
|---|---|---|---|---|---|---|---|---|
| cant400 | 2022 (seen) | 909 | +4.6 [-2.7, +11.0] | -2.1 [-6.0, +2.7] | +1.6 [-0.7, +3.9] | +5.4 [-2.5, +10.9] | -2.1 [-5.8, +2.2] | +1.9 [-0.4, +4.4] |
| notcash400 | 2022 (seen) | 909 | +6.5 [-2.2, +15.1] | -1.1 [-7.5, +6.3] | +4.8 [+1.2, +8.4] | +6.8 [-0.6, +14.2] | -1.1 [-8.0, +6.1] | +4.8 [+2.0, +8.4] |
| nofund3 | 2022 (seen) | 909 | +8.3 [-0.4, +18.4] | -0.3 [-8.0, +6.2] | +6.5 [+2.3, +10.5] | +8.5 [+0.8, +16.3] | -0.1 [-7.6, +7.3] | +7.0 [+3.0, +10.8] |
| strained | 2022 (seen) | 909 | +15.5 [+7.9, +23.4] | -3.4 [-9.5, +2.7] | +8.5 [+4.9, +12.1] | +16.5 [+9.6, +23.3] | -3.3 [-9.9, +2.9] | +9.0 [+5.4, +12.3] |
| incvar | 2022 (seen) | 909 | -2.0 [-12.7, +8.3] | +23.9 [+15.4, +31.9] | +21.7 [+16.9, +25.5] | +0.7 [-7.4, +9.0] | +24.5 [+15.9, +32.8] | +24.3 [+20.3, +28.4] |
| billvar | 2022 (seen) | 909 | +14.2 [+8.1, +20.8] | +1.0 [-4.5, +6.7] | +11.4 [+8.8, +14.5] | +15.7 [+9.1, +20.9] | +1.0 [-4.2, +6.4] | +12.5 [+9.4, +15.6] |

## H1 — control, not variability (average marginal effects, percentage points; bootstrap 95% intervals)

Confirmatory specification: pooled controls (household income band, education, age band, gender, race/ethnicity, marital status, children, year). Robustness: the same plus full/part-time.

| outcome | sample | own − same | employer − same | **employer − own** | (+ full/part-time) own − same | employer − same | employer − own |
|---|---|---|---|---|---|---|---|
| cant400 | pooled 2019–2021 | +0.4 [-1.0, +1.7] | +2.8 [+1.6, +4.1] | +2.4 [+0.7, +4.4] | -0.0 [-1.6, +1.5] | +2.5 [+1.4, +3.5] | +2.5 [+0.8, +4.2] |
| notcash400 | pooled 2019–2021 | +2.3 [+0.0, +4.4] | +5.4 [+3.6, +7.3] | +3.1 [+0.6, +5.6] | +1.8 [-0.5, +4.5] | +5.0 [+3.3, +7.1] | +3.2 [+0.6, +6.2] |
| nofund3 | pooled 2019–2021 | +1.0 [-1.5, +4.0] | +2.6 [+0.8, +4.6] | +1.5 [-1.5, +4.7] | +0.5 [-2.2, +3.2] | +2.2 [+0.2, +4.2] | +1.7 [-1.1, +4.4] |
| strained | pooled 2019–2021 | -1.2 [-3.1, +0.8] | +6.3 [+4.6, +7.9] | +7.5 [+5.0, +9.8] | -2.7 [-4.4, -0.6] | +5.2 [+3.5, +6.9] | +7.8 [+5.6, +9.9] |
| incvar | pooled 2019–2021 | +17.2 [+14.5, +19.8] | +23.7 [+21.7, +25.7] | +6.5 [+3.8, +9.7] | +14.4 [+11.4, +17.3] | +21.7 [+19.5, +23.8] | +7.3 [+4.1, +10.2] |
| billvar | pooled 2019–2021 | +4.3 [+2.7, +5.9] | +9.8 [+8.4, +11.4] | +5.5 [+3.3, +7.7] | +3.4 [+1.8, +5.0] | +9.0 [+7.7, +10.7] | +5.7 [+3.6, +7.9] |
| cant400 | 2019 | -0.7 [-3.1, +2.1] | +4.0 [+1.9, +6.2] | +4.7 [+1.6, +7.7] | -1.1 [-3.5, +1.4] | +3.6 [+1.3, +5.9] | +4.7 [+1.8, +7.6] |
| notcash400 | 2019 | +0.5 [-3.8, +5.0] | +7.3 [+4.1, +10.5] | +6.9 [+1.9, +11.9] | -0.2 [-4.4, +4.6] | +6.8 [+3.6, +10.2] | +7.0 [+1.8, +11.5] |
| nofund3 | 2019 | -1.2 [-4.8, +3.5] | +3.7 [+0.2, +7.3] | +4.9 [-0.1, +9.9] | -0.8 [-5.7, +3.6] | +4.0 [-0.1, +7.9] | +4.9 [-0.3, +10.2] |
| strained | 2019 | -3.7 [-7.0, +0.1] | +6.3 [+3.5, +9.6] | +9.9 [+6.2, +13.8] | -5.0 [-8.7, -1.2] | +5.0 [+1.8, +8.0] | +10.0 [+5.5, +15.0] |
| incvar | 2019 | +16.6 [+12.0, +21.2] | +23.0 [+19.3, +26.4] | +6.3 [+0.4, +11.9] | +13.8 [+9.8, +18.9] | +20.6 [+16.4, +24.2] | +6.8 [+1.4, +11.6] |
| billvar | 2019 | +3.8 [+0.7, +6.6] | +11.2 [+8.7, +14.3] | +7.4 [+3.8, +10.8] | +3.1 [+0.4, +6.3] | +10.4 [+7.4, +12.7] | +7.3 [+3.4, +10.7] |
| cant400 | 2020 | +2.4 [-0.6, +5.2] | +2.5 [+0.4, +4.4] | +0.2 [-2.9, +3.2] | +2.0 [-0.9, +4.8] | +2.4 [+0.3, +4.5] | +0.4 [-2.8, +3.3] |
| notcash400 | 2020 | +4.4 [+1.0, +8.6] | +5.7 [+2.6, +8.9] | +1.3 [-3.7, +5.9] | +3.6 [-0.3, +7.4] | +5.1 [+1.7, +8.4] | +1.5 [-3.5, +6.3] |
| nofund3 | 2020 | +1.7 [-2.6, +5.9] | +2.9 [-0.4, +6.4] | +1.2 [-4.2, +6.6] | +0.5 [-3.9, +4.7] | +2.0 [-1.5, +5.5] | +1.5 [-3.5, +6.7] |
| strained | 2020 | +0.4 [-3.0, +3.6] | +6.7 [+3.5, +9.7] | +6.4 [+2.1, +10.8] | -1.2 [-4.6, +2.3] | +5.7 [+2.6, +8.8] | +6.9 [+3.3, +11.1] |
| incvar | 2020 | +17.1 [+12.1, +21.4] | +24.8 [+21.6, +28.5] | +7.7 [+3.3, +13.6] | +14.5 [+10.4, +18.7] | +22.9 [+18.8, +26.7] | +8.4 [+3.2, +13.4] |
| billvar | 2020 | +5.1 [+2.6, +8.0] | +9.5 [+7.4, +12.0] | +4.3 [+0.4, +7.6] | +3.9 [+1.1, +7.1] | +8.6 [+6.0, +11.2] | +4.7 [+1.0, +8.2] |
| cant400 | 2021 | -0.7 [-3.2, +1.8] | +2.2 [+0.4, +3.9] | +3.0 [+0.1, +6.0] | -1.1 [-3.4, +1.2] | +2.0 [+0.0, +3.9] | +3.0 [+0.3, +5.8] |
| notcash400 | 2021 | +1.9 [-2.2, +5.6] | +3.4 [+0.1, +6.6] | +1.5 [-3.8, +6.5] | +2.1 [-1.7, +6.3] | +3.5 [+0.1, +6.7] | +1.4 [-4.4, +6.3] |
| nofund3 | 2021 | +2.9 [-1.7, +8.2] | +1.2 [-2.4, +4.7] | -1.6 [-8.6, +3.2] | +1.8 [-3.5, +5.8] | +0.6 [-3.2, +3.9] | -1.2 [-6.8, +5.3] |
| strained | 2021 | -0.3 [-4.3, +3.0] | +6.1 [+2.8, +8.8] | +6.3 [+2.1, +10.7] | -1.8 [-5.5, +1.9] | +5.0 [+2.3, +7.8] | +6.8 [+2.6, +10.6] |
| incvar | 2021 | +17.7 [+12.3, +22.5] | +23.1 [+19.6, +26.8] | +5.5 [+0.3, +11.5] | +14.7 [+10.0, +18.8] | +21.5 [+18.2, +25.2] | +6.8 [+1.9, +13.2] |
| billvar | 2021 | +3.7 [+0.9, +6.5] | +8.6 [+6.2, +10.9] | +4.8 [+1.0, +8.5] | +2.9 [+0.1, +5.3] | +8.0 [+5.3, +10.5] | +5.0 [+1.6, +8.2] |

**H1 verdict (pooled out-of-sample, confirmatory specification): HOLDS.** employer − own is positive on 4 of 4 confirmatory outcomes (cant400 +2.4, nofund3 +1.5, strained +7.5, billvar +5.5); the interval excludes zero on 3 (cant400, strained, billvar). own − same on the first three: cant400 +0.4, nofund3 +1.0, strained -1.2 (committed band ±3 pp).

## H2 — the three-week break (employer-varying workers with stated notice)

Confirmatory specification: the 2022 one (pooled controls plus full/part-time). Robustness: without full/part-time.

| outcome | sample | n employer-varying with notice | **under 3 weeks − 3 weeks or more** | **3+ weeks − same hours** | under 3 weeks − same hours | (no full/part-time) under − 3+ | 3+ − same | under − same |
|---|---|---|---|---|---|---|---|---|
| cant400 | pooled 2019–2021 | 2865 | +2.6 [-1.3, +6.0] | +0.4 [-1.9, +2.8] | +2.8 [+1.4, +4.2] | +2.8 [-0.9, +6.1] | +0.6 [-1.9, +2.9] | +3.1 [+1.8, +4.4] |
| notcash400 | pooled 2019–2021 | 2865 | +7.1 [+2.3, +11.8] | -0.8 [-5.4, +2.8] | +6.0 [+3.9, +8.2] | +7.3 [+2.9, +11.9] | -0.6 [-5.3, +3.3] | +6.4 [+4.3, +8.4] |
| nofund3 | pooled 2019–2021 | 2865 | +1.5 [-3.0, +6.3] | +0.7 [-4.1, +5.2] | +2.4 [+0.1, +4.6] | +1.7 [-3.0, +7.0] | +0.9 [-4.0, +5.6] | +2.8 [+0.7, +5.0] |
| strained | pooled 2019–2021 | 2865 | +10.5 [+6.5, +14.3] | -2.4 [-6.2, +0.9] | +6.5 [+4.7, +8.4] | +11.0 [+6.3, +15.0] | -1.7 [-5.0, +2.1] | +7.7 [+5.7, +9.5] |
| incvar | pooled 2019–2021 | 2865 | +8.3 [+3.2, +13.2] | +14.6 [+10.0, +18.4] | +23.1 [+20.7, +25.5] | +8.9 [+3.7, +14.4] | +16.0 [+11.6, +21.0] | +25.1 [+22.7, +27.6] |
| billvar | pooled 2019–2021 | 2865 | +8.9 [+4.8, +12.4] | +2.7 [+0.2, +5.4] | +10.2 [+8.5, +11.9] | +9.2 [+5.1, +12.7] | +3.0 [+0.3, +6.0] | +10.9 [+9.1, +12.7] |
| cant400 | 2019 | 1024 | +0.9 [-6.6, +7.3] | +2.2 [-1.8, +7.0] | +3.8 [+1.6, +6.5] | +1.1 [-5.6, +8.1] | +2.4 [-2.1, +7.3] | +4.3 [+1.9, +7.0] |
| notcash400 | 2019 | 1024 | +12.3 [+3.6, +19.8] | -4.3 [-10.9, +3.9] | +8.8 [+4.9, +12.6] | +12.6 [+4.0, +19.8] | -3.9 [-10.5, +1.6] | +9.4 [+6.2, +13.0] |
| nofund3 | 2019 | 1024 | +2.0 [-5.8, +9.6] | +0.7 [-5.7, +8.5] | +4.6 [+0.4, +8.5] | +1.9 [-5.6, +9.0] | +0.5 [-6.9, +7.7] | +4.3 [+0.8, +7.9] |
| strained | 2019 | 1024 | +14.0 [+6.4, +20.4] | -5.7 [-11.5, -0.2] | +7.0 [+3.5, +10.3] | +14.5 [+6.4, +20.9] | -5.0 [-11.1, +1.0] | +8.3 [+4.9, +11.9] |
| incvar | 2019 | 1024 | +10.5 [+2.8, +18.4] | +10.7 [+2.8, +19.1] | +22.8 [+18.7, +27.2] | +11.4 [+3.0, +20.4] | +12.3 [+4.9, +20.5] | +25.3 [+21.5, +29.5] |
| billvar | 2019 | 1024 | +11.6 [+5.3, +16.7] | +2.1 [-2.3, +7.3] | +12.0 [+9.1, +15.2] | +12.1 [+4.9, +18.0] | +2.3 [-2.0, +7.8] | +12.8 [+10.0, +15.8] |
| cant400 | 2020 | 932 | +6.9 [+0.8, +11.2] | -1.9 [-5.0, +2.2] | +2.9 [+0.8, +5.2] | +7.4 [+2.4, +12.0] | -1.8 [-4.8, +2.2] | +3.1 [+1.1, +5.4] |
| notcash400 | 2020 | 932 | +5.2 [-3.1, +14.1] | +1.8 [-4.5, +9.5] | +5.7 [+2.3, +9.2] | +6.2 [-1.7, +13.6] | +2.0 [-5.6, +10.0] | +6.4 [+2.9, +10.1] |
| nofund3 | 2020 | 932 | +8.2 [-0.8, +16.3] | -3.9 [-10.9, +4.0] | +3.2 [-1.0, +6.8] | +9.1 [+0.8, +17.0] | -3.6 [-10.5, +3.5] | +4.2 [+0.6, +8.2] |
| strained | 2020 | 932 | +11.6 [+4.1, +18.7] | -1.1 [-6.8, +4.7] | +7.1 [+4.0, +10.4] | +12.5 [+5.2, +19.1] | -0.9 [-7.4, +4.9] | +8.2 [+4.8, +11.6] |
| incvar | 2020 | 932 | +9.1 [+0.0, +19.1] | +16.6 [+9.0, +24.4] | +24.1 [+20.1, +28.1] | +10.6 [+1.3, +18.5] | +17.3 [+10.6, +24.7] | +26.2 [+22.6, +30.2] |
| billvar | 2020 | 932 | +11.4 [+4.8, +17.1] | +2.6 [-2.1, +7.6] | +9.8 [+6.9, +12.3] | +11.8 [+5.5, +17.0] | +2.7 [-2.6, +8.4] | +10.8 [+7.7, +14.2] |
| cant400 | 2021 | 909 | +0.6 [-5.0, +6.6] | +1.2 [-2.8, +5.2] | +2.0 [+0.5, +4.1] | +0.2 [-5.5, +5.6] | +1.6 [-2.0, +6.2] | +2.3 [+0.3, +3.9] |
| notcash400 | 2021 | 909 | +1.0 [-8.0, +10.5] | +1.6 [-5.8, +9.3] | +3.8 [+0.8, +7.1] | +0.9 [-7.3, +11.4] | +1.5 [-5.9, +9.2] | +3.7 [+0.5, +7.0] |
| nofund3 | 2021 | 909 | -6.1 [-14.9, +2.9] | +5.7 [-2.2, +13.3] | -0.3 [-4.5, +3.4] | -6.5 [-16.5, +1.7] | +6.5 [-2.3, +14.8] | +0.3 [-2.9, +4.0] |
| strained | 2021 | 909 | +6.2 [-2.0, +15.2] | -0.0 [-7.0, +6.5] | +5.7 [+2.4, +8.8] | +5.4 [-3.5, +14.1] | +1.4 [-5.6, +8.2] | +6.7 [+3.5, +9.9] |
| incvar | 2021 | 909 | +4.6 [-3.3, +13.8] | +17.7 [+10.2, +25.8] | +22.2 [+17.9, +26.5] | +3.9 [-6.4, +14.6] | +19.9 [+11.3, +27.9] | +23.7 [+20.0, +28.3] |
| billvar | 2021 | 909 | +3.8 [-4.2, +12.0] | +3.9 [-2.4, +10.7] | +8.5 [+5.9, +11.0] | +3.2 [-3.8, +11.2] | +4.7 [-0.9, +10.3] | +9.1 [+6.5, +11.3] |

**H2 verdict (pooled out-of-sample, confirmatory specification): HOLDS.** under 3 weeks − 3 weeks or more: strained +10.5 [+6.5, +14.3], billvar +8.9 [+4.8, +12.4]. 3+ weeks − same hours on strained: -2.4 [-6.2, +0.9] (committed band ±5 pp).

## H3 — who bears it (weighted share of employees whose schedule varies on the employer's needs, by household income band)

| sample | Less than $10,000 | $10,000 to $24,999 | $25,000 to $49,999 | $50,000 to $74,999 | $75,000 to $99,999 | $100,000 to $149,999 | $150,000 or more | adjacent reversals |
|---|---|---|---|---|---|---|---|---|
| pooled 2019–2021 | 27.8 | 24.9 | 21.7 | 17.3 | 15.9 | 13.4 | 11.9 | 0 |
| 2019 | 26.1 | 27.2 | 22.0 | 17.2 | 16.3 | 12.5 | 12.3 | 1 |
| 2020 | 27.5 | 22.3 | 21.7 | 18.3 | 14.3 | 15.4 | 11.3 | 1 |
| 2021 | 29.9 | 24.2 | 21.2 | 16.2 | 17.2 | 12.4 | 12.0 | 1 |

**H3 verdict (pooled out-of-sample): HOLDS.** 27.8% in the lowest band, 11.9% in the highest, 0 adjacent reversal(s) (committed: falls from lowest to highest with at most one).

## Reading

The three hypotheses were written down before these files were opened and are evaluated on the pooled out-of-sample waves in the specification that produced the numbers quoted in the preregistration; every other column is context. Nothing here is causal: selection into jobs, the wage itself, occupation and industry are not in the model; household income is a band; the outcomes are self-reported; the 2020 and 2021 waves were fielded during the pandemic transfers. This is the audit's descriptive column, confirmed or not out of sample, and the design that could attribute (Chapter 13's audit box, items 6–9) is still owed.
