# Town stress (T13) — 972 configurations

Columns: famine at k = 0 (all read), at the best dose k*, at k = 9 (bloc); 'independence beats bloc' = famine(k=0) < famine(k=9); 'some following helps' = min over k ≥ 1 below famine(k=0); k* = argmin.

## By master accuracy q (all other stresses pooled)

| group | n | indep. beats bloc | some following helps | k* = 1 | k* ≥ 5 | median famine k=0 | k=9 |
|---|---|---|---|---|---|---|---|
| q = 0.7 | 243 | 0.87 | 0.28 | 0.12 | 0.13 | 0.684 | 0.989 |
| q = 0.8 | 243 | 0.75 | 0.61 | 0.34 | 0.22 | 0.683 | 0.950 |
| q = 0.9 | 243 | 0.54 | 0.80 | 0.22 | 0.36 | 0.683 | 0.726 |
| q = 0.99 | 243 | 0.28 | 0.93 | 0.10 | 0.65 | 0.684 | 0.147 |

## By sea memory ρ_G (q = 0.8 only)

| group | n | indep. beats bloc | some following helps | k* = 1 | k* ≥ 5 | median famine k=0 | k=9 |
|---|---|---|---|---|---|---|---|
| sea memory ρ_G = 0.0 | 81 | 0.75 | 0.60 | 0.33 | 0.22 | 0.683 | 0.951 |
| sea memory ρ_G = 0.5 | 81 | 0.74 | 0.62 | 0.35 | 0.22 | 0.684 | 0.949 |
| sea memory ρ_G = 0.9 | 81 | 0.75 | 0.60 | 0.33 | 0.22 | 0.683 | 0.950 |

## By reader error persistence ρ_err (q = 0.8 only)

| group | n | indep. beats bloc | some following helps | k* = 1 | k* ≥ 5 | median famine k=0 | k=9 |
|---|---|---|---|---|---|---|---|
| reader error persistence ρ_err = 0.0 | 81 | 0.81 | 0.43 | 0.25 | 0.19 | 0.388 | 0.950 |
| reader error persistence ρ_err = 0.5 | 81 | 0.67 | 0.70 | 0.33 | 0.30 | 0.684 | 0.949 |
| reader error persistence ρ_err = 0.9 | 81 | 0.77 | 0.69 | 0.43 | 0.19 | 0.689 | 0.951 |

## By shared blindness c (q = 0.8 only)

| group | n | indep. beats bloc | some following helps | k* = 1 | k* ≥ 5 | median famine k=0 | k=9 |
|---|---|---|---|---|---|---|---|
| shared blindness c = 0.0 | 81 | 0.93 | 0.56 | 0.41 | 0.00 | 0.520 | 0.950 |
| shared blindness c = 0.1 | 81 | 0.93 | 0.59 | 0.52 | 0.07 | 0.683 | 0.950 |
| shared blindness c = 0.3 | 81 | 0.40 | 0.68 | 0.09 | 0.59 | 0.959 | 0.950 |

## By master's slump persistence ρ_h (q = 0.8 only)

| group | n | indep. beats bloc | some following helps | k* = 1 | k* ≥ 5 | median famine k=0 | k=9 |
|---|---|---|---|---|---|---|---|
| master's slump persistence ρ_h = 0.0 | 81 | 0.63 | 0.70 | 0.26 | 0.30 | 0.684 | 0.773 |
| master's slump persistence ρ_h = 0.5 | 81 | 0.88 | 0.53 | 0.42 | 0.11 | 0.683 | 0.972 |
| master's slump persistence ρ_h = 0.9 | 81 | 0.74 | 0.59 | 0.33 | 0.26 | 0.684 | 0.830 |

## By master misdirection rate (q = 0.8 only)

| group | n | indep. beats bloc | some following helps | k* = 1 | k* ≥ 5 | median famine k=0 | k=9 |
|---|---|---|---|---|---|---|---|
| master misdirection rate = 0.0 | 81 | 0.54 | 0.93 | 0.48 | 0.37 | 0.684 | 0.812 |
| master misdirection rate = 0.1 | 81 | 0.74 | 0.83 | 0.49 | 0.26 | 0.682 | 0.830 |
| master misdirection rate = 0.3 | 81 | 0.96 | 0.07 | 0.04 | 0.04 | 0.684 | 0.994 |

## Configurations where the bloc beats independence (worst ten)

| q | p | rho_G | rho_err | c | rho_h | lie | famine k=0 | k=9 |
|---|---|---|---|---|---|---|---|---|
| 0.99 | 0.7 | 0.0 | 0.5 | 0.3 | 0.0 | 0.0 | 0.974 | 0.000 |
| 0.99 | 0.7 | 0.5 | 0.5 | 0.3 | 0.0 | 0.0 | 0.973 | 0.000 |
| 0.99 | 0.7 | 0.9 | 0.5 | 0.3 | 0.0 | 0.0 | 0.972 | 0.000 |
| 0.99 | 0.7 | 0.5 | 0.0 | 0.3 | 0.0 | 0.0 | 0.961 | 0.000 |
| 0.99 | 0.7 | 0.0 | 0.0 | 0.3 | 0.0 | 0.0 | 0.959 | 0.000 |
| 0.99 | 0.7 | 0.9 | 0.0 | 0.3 | 0.0 | 0.0 | 0.958 | 0.000 |
| 0.99 | 0.7 | 0.5 | 0.9 | 0.3 | 0.0 | 0.0 | 0.953 | 0.000 |
| 0.99 | 0.7 | 0.0 | 0.9 | 0.3 | 0.0 | 0.0 | 0.950 | 0.000 |
| 0.99 | 0.7 | 0.9 | 0.9 | 0.3 | 0.0 | 0.0 | 0.950 | 0.000 |
| 0.99 | 0.7 | 0.0 | 0.5 | 0.3 | 0.9 | 0.0 | 0.974 | 0.074 |
