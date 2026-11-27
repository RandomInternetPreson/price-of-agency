# SHED preregistration v0.3 — did the pay rise? (H6)

Written 2026-11-12, before the quantity below was computed. The household-income band of each respondent has been
used as a control and as a secondary column in v0.1 and v0.2 (the ΔE coefficient with and without the change in income
band, which did not move). Its own relation to who holds the schedule has not been tabulated in any form.

## Why
Chapter 13 §2D compares employees at equal household income. The reply an economist makes first: a compensating
differential predicts exactly that pattern — if unstable schedules were paid more, then at equal income the worker on
the unstable schedule would be worse off by construction. The reply has one checkable consequence. If the instability
is priced in, households whose schedule the employer varies are PAID MORE than they otherwise would be: more than the
same person in a year the employer does not hold the schedule, and more than employees of the same education, age,
gender, race and ethnicity, marital status, children and year on fixed hours.

## H6a — within person
Sample and estimator of H4 (adjacent-wave pairs, same `shedid`, employed with a stated schedule type in both; weighted
least squares with wave-pair dummies; weights = later wave; bootstrap over persons, B = 1000). Outcome: the change in
household-income band (seven bands, indexed 0–6; `ppinc7`, with `ppincimp` collapsed to the same seven in 2019–20).
Coefficient of interest: ΔE; reported beside it ΔO and ΔE − ΔO.

## H6b — across persons
All five waves pooled, employees with a stated schedule type. Weighted least squares of the income-band index on
E and O with the v0.1 controls EXCEPT income (education, age band, gender, race and ethnicity, marital status,
children) and wave dummies; bootstrap over persons, B = 300. Quantity of interest: employer − same; reported beside it
employer − own. Also reported: the same contrast as a probability of household income of $50,000 or more (weighted
logit, average marginal effect).

## H6c — full-time only (secondary)
H6b restricted to respondents `Working full-time` (`ppemploy`, carried in 2021–2023 only), so that a gap produced by
fewer hours is removed.

## Committed readings (each of H6a, H6b)
- **Pay rose** — the coefficient is > 0 and its 95% interval excludes zero: the sentence "it was not priced in" is
  WITHDRAWN from Chapter 13 for that comparison, and the size is printed.
- **Pay fell** — the coefficient is < 0 and its interval excludes zero: the sentence stands, with the size.
- **No raise distinguishable** — the interval includes zero: the sentence is restated as what the file supports — "no
  raise can be found" — with the largest raise the interval allows, in bands.
A full compensating differential would have to do more than appear: it would have to remove the strain. H4 already
showed that it does not (the same person is more strained in the employer-held year, income band controlled or not).
H6 asks the weaker and prior question — whether any raise is there at all.

## What this measures and what it does not
Household income is a band, not the respondent's wage: a second earner, and hours, are in it. H6c removes the hours
for three of the five waves. A raise smaller than a band's width is visible only as a shift in the share of households
crossing a band edge. Whatever comes out is printed.
