# Ricardian equivalence in the bandwidth HANK: a debt-financed tax cut, model vs control (2026-11-10)

Debt rises by b0 = 0.04 (1% of annual output) at t = 0 and is retired at rate 1 − ρ per quarter; the tax cut at t = 0 is b0 and taxes are higher afterwards. A Ricardian household's consumption does not move. Linear responses from sequence-space Jacobians (T = 200); naive forecast; constants as in HANK v0.1.

## fast repayment (ρ = 0.8: half retired in three quarters)

| economy | fixed prices: ΔC at impact / tax cut | first-year ΔC / tax cut | GE: ΔC at impact / tax cut | first-year ΔC / tax cut | first-year ΔY / tax cut | peak Δr (bp) | ΔHTM at impact |
|---|---|---|---|---|---|---|---|
| control | 0.041 | 0.040 | 0.046 | 0.063 | 0.063 | +1.6 | -0.0053 |
| model | 0.029 | 0.053 | 0.038 | 0.078 | 0.078 | +2.0 | -0.0114 |

Model / control: fixed-price impact 0.70, fixed-price first year 1.32, GE impact 0.82, GE first year 1.24, GE output first year 1.24.

## slow repayment (ρ = 0.95: half retired in fourteen quarters)

| economy | fixed prices: ΔC at impact / tax cut | first-year ΔC / tax cut | GE: ΔC at impact / tax cut | first-year ΔC / tax cut | first-year ΔY / tax cut | peak Δr (bp) | ΔHTM at impact |
|---|---|---|---|---|---|---|---|
| control | 0.051 | 0.090 | 0.040 | 0.058 | 0.058 | -4.9 | -0.0054 |
| model | 0.040 | 0.104 | 0.044 | 0.076 | 0.076 | -5.5 | -0.0116 |

Model / control: fixed-price impact 0.79, fixed-price first year 1.15, GE impact 1.10, GE first year 1.29, GE output first year 1.29.

## very slow repayment (ρ = 0.99: half retired in seventeen years)

| economy | fixed prices: ΔC at impact / tax cut | first-year ΔC / tax cut | GE: ΔC at impact / tax cut | first-year ΔC / tax cut | first-year ΔY / tax cut | peak Δr (bp) | ΔHTM at impact |
|---|---|---|---|---|---|---|---|
| control | 0.062 | 0.137 | 0.034 | 0.040 | 0.040 | -6.0 | -0.0054 |
| model | 0.051 | 0.147 | 0.042 | 0.057 | 0.057 | -6.7 | -0.0116 |

Model / control: fixed-price impact 0.82, fixed-price first year 1.08, GE impact 1.21, GE first year 1.43, GE output first year 1.43.

## Intertemporal marginal propensities to consume (household block, fixed prices)

| economy | out of a transfer today: spent in quarter 0 | within a year | within three years | out of a transfer announced for quarter 8: spent before it arrives |
|---|---|---|---|---|
| control | 0.072 | 0.178 | 0.378 | 0.203 |
| model | 0.062 | 0.193 | 0.390 | 0.203 |

Runtime 244s.
