# Preregistration v0.2 — the within-person test and the industry control (written 2026-11-10, before either is computed)

## State of knowledge when this was written
Seen: the 2022–2023 cross-section (`code/field/results/shed_first_look.md`). Running, results not yet seen: the
out-of-sample cross-section on 2019–2021 (`shed_oos_test.py`, preregistration v0.1). Not computed in any form: any
within-person change, any regression with industry. What was inspected for this document: column names, the value
labels of `ind1` (industry, about 24 groups, present in every wave 2019–2023), and the count of respondent
identifiers (`shedid`) shared between waves (3,700–3,900 between adjacent waves, all adults). No outcome was tabulated
by either.

## Why
The cross-section cannot separate what a schedule does to a household from who ends up in such jobs. Two cheap steps
narrow that gap without closing it: (i) compare the SAME PERSON across two waves when the hand on the schedule
changes — anything fixed about the person drops out; (ii) hold industry fixed in the cross-section — "these are just
retail and restaurant jobs" drops out.

## H4 — within person (first differences)
Sample: every pair of ADJACENT waves (2019→20, 20→21, 21→22, 22→23) in which the same `shedid` is working for someone
else with a stated schedule type in both. Exposure E = 1 if the schedule varies on the employer's needs, O = 1 if it
varies at the worker's request. Outcomes as in v0.1 (`strained`, `billvar`, `cant400`, `nofund3`), each differenced
within person (−1, 0, +1).
Estimator: weighted least squares of Δoutcome on ΔE and ΔO with wave-pair dummies, weights = the later wave's
cross-section weight; intervals by bootstrap resampling PERSONS (a person can contribute several pairs).
- **H4a.** The coefficient on ΔE is > 0 on `strained` and on `billvar`. *Fails if* it is ≤ 0 on either.
- **H4b (control, not variability, within person).** coefficient(ΔE) − coefficient(ΔO) > 0 on `strained` and on
  `billvar`. *Fails if* ≤ 0 on either.
- **H4c (both directions).** Reported separately and committed in sign: persons moving INTO an employer-varying
  schedule (0→1) show a higher mean Δ than persons staying out (0→0), and persons moving OUT (1→0) a lower mean Δ
  than persons staying in (1→1), on `strained` and `billvar`. *Fails if* either direction has the wrong sign on both
  outcomes.
Secondary, reported, not confirmatory: `cant400`, `nofund3`; the same regression adding the change in household-income
band (a mediator as much as a confounder — unstable hours move income — so the version WITHOUT it is the confirmatory
one); unweighted; each wave pair alone.

## H5 — industry held fixed (cross-section, all five waves pooled)
The v0.1 pooled specification plus industry dummies (`ind1`, labels harmonized across the 2019–20 and 2021–23
wordings; missing/uncoded as its own level) and wave dummies.
- **H5.** employer − own stays > 0 on `strained` and `billvar`, and keeps at least half of its size without industry
  in the same pooled sample. *Fails if* either goes ≤ 0; *holds in part* if positive but under half.
This one is not out-of-sample (2022–2023 are in it); it is a robustness column and is labeled so.

## What these still cannot show
A person who changes schedule type has usually changed jobs, shifts or employers at the same time; a household under
strain may take whatever job is offered (reverse order); the schedule question is self-classified and misclassification
manufactures false switchers, which pulls first-difference estimates toward zero. First differences remove fixed traits,
not shocks. The audit design (Chapter 13's box, items 6–9) is still owed. Whatever comes out is printed, including a
failure.
