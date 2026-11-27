# Preregistration — out-of-sample test of the SHED first look (written 2026-11-09, before any other wave is opened)

## What was seen (2022 and 2023 public-use files; `code/field/shed_first_look.py`; `code/field/results/shed_first_look.md`)
Among 11,503 employees: (a) schedules that vary at the employer's discretion fall steadily with household income
(28.5% in the lowest band to 11.1% in the highest); (b) at equal household income band, education, age, gender,
race/ethnicity, marital status and children, workers whose schedule varies at the EMPLOYER's needs are more fragile
than fixed-schedule workers on every measure (cannot pay $400: +2.8 pp; no three-month fund: +4.9; just getting by:
+7.2; struggled with bills because income varied: +11.2), while workers whose schedule varies at their OWN request
are indistinguishable from fixed-schedule workers on the first four; (c) EXPLORATORY, contrast chosen after seeing
the table: among employer-varying workers in 2022, those with three weeks' notice or more look like fixed-schedule
workers on every fragility measure, and those with less do not (strained +8.5 pp, bills +11.4 pp), although income
varies equally in both groups.

## The test (to be run unchanged on every other SHED wave that asks D30 and D31; 2022 and 2023 excluded)
Same script, same sample definition, same controls, same weights. Committed in advance:
- **H1 (control, not variability).** employer − own > 0 on `cant400`, `nofund3`, `strained`, `billvar`, with the
  own − same differences on the first three within ±3 pp. *Fails if* employer − own is ≤ 0 on two or more of the four.
- **H2 (the three-week break).** Among employer-varying workers: (under three weeks − three weeks or more) > 0 on
  `strained` and `billvar`; and (three weeks or more − same hours) within ±5 pp on `strained`. *Fails if* either
  difference in the first clause is ≤ 0 in the pooled out-of-sample waves.
- **H3 (who bears it).** The employer-varying share falls from the lowest to the highest household-income band, with
  at most one reversal between adjacent bands.
No other contrasts will be reported as confirmatory. Whatever comes out is printed, including a failure.

## What this cannot show, in any wave
Causation. Selection into jobs, the wage itself, occupation and industry are not in the model; household income is a
band; the outcome is self-reported. H1–H3 are the audit's descriptive column, and the design that could attribute
(Chapter 13's audit box, items 6–9) is still owed.
