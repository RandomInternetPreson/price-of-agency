# Small divergence model v0 — results (model world)
Grid: Na=60, Ny=2, Nb=4; beta=0.96, r=0.03, y=(0.5,1.5); noise k_min=0.02, k_tax=0.30; tunneling 0.06 (control: both 0); time floors T=(0.8, 1.6) vs gate 1.0; entropy taxes s=(0.35, 0.08); scarcity tax 0.25 below m=0.9.

## P-A  small time transfer vs small money transfer — change in next-period savings by wealth quintile
(money effect net of the transfer itself; both models share every parameter except k_tax)
| model | transfer | Q1 (poorest) | Q2 | Q3 | Q4 | Q5 | bottom-share of total effect |
|---|---|---|---|---|---|---|---|
| bandwidth model (noise + tunneling) | time (+floor over gate) | -0.0000 | -0.0001 | +0.0067 | +0.0261 | +0.0524 | 0.00 |
| bandwidth model (noise + tunneling) | money (+5% of low income) | -0.0209 | -0.0208 | -0.0222 | -0.0265 | -0.0262 | 0.18 |
| control (both off) | time (+floor over gate) | +0.0000 | +0.0000 | +0.0000 | -0.0000 | +0.0000 | 0.00 |
| control (both off) | money (+5% of low income) | -0.0288 | -0.0286 | -0.0284 | -0.0268 | -0.0255 | 0.21 |

HtM share (low income): base 0.628 -> time 0.580 / money 0.633  [bandwidth model];  base 0.335 -> time 0.335 / money 0.357  [control]
Reading: in the control the time transfer does NOTHING (time is not a state there); in the bandwidth model it acts through the gate and concentrates where bandwidth is lowest. P-A holds in this world if the time row's bottom-share exceeds the money row's. A model constant, not a world constant.

## P-B  schedule-stability policy vs equal-dollar wage transfer (low-income households)
Stability = entropy tax s(y_L) cut from 0.35 to 0.15; priced at `cost` per period, paid as the wage transfer in the comparison arm.
| model | cost | arm | median assets (low y) | HtM share (low y) | mean bandwidth (low y) | E[log c] |
|---|---|---|---|---|---|---|
| bandwidth model (noise + tunneling) | — | baseline | 0.254 | 0.628 | 0.83 | -0.1016 |
| bandwidth model (noise + tunneling) | 0.02 | stability | 0.254 | 0.589 | 1.26 | -0.0823 |
| bandwidth model (noise + tunneling) | 0.02 | wage +0.02 | 0.254 | 0.631 | 0.83 | -0.0873 |
| bandwidth model (noise + tunneling) | 0.05 | stability | 0.254 | 0.589 | 1.26 | -0.0823 |
| bandwidth model (noise + tunneling) | 0.05 | wage +0.05 | 0.254 | 0.637 | 0.83 | -0.0664 |
| bandwidth model (noise + tunneling) | 0.10 | stability | 0.254 | 0.589 | 1.26 | -0.0823 |
| bandwidth model (noise + tunneling) | 0.10 | wage +0.10 | 0.254 | 0.630 | 0.82 | -0.0353 |
| control (both off) | — | baseline | 1.525 | 0.335 | 0.89 | 0.0248 |
| control (both off) | 0.02 | stability | 1.525 | 0.335 | 1.44 | 0.0248 |
| control (both off) | 0.02 | wage +0.02 | 1.271 | 0.350 | 0.89 | 0.0318 |
| control (both off) | 0.05 | stability | 1.525 | 0.335 | 1.44 | 0.0248 |
| control (both off) | 0.05 | wage +0.05 | 1.017 | 0.372 | 0.89 | 0.0424 |
| control (both off) | 0.10 | stability | 1.525 | 0.335 | 1.44 | 0.0248 |
| control (both off) | 0.10 | wage +0.10 | 0.763 | 0.412 | 0.88 | 0.0604 |
Reading: find the cost at which the wage arm first matches the stability arm on HtM share -- that is the model's shadow price of schedule stability in wage units. In the control it is zero by construction (stability is not a state). Mas & Pallais 2017 measured an experimental WTP (~20% of wage) for avoiding employer-set schedules; the model's shadow price is the quantity a field audit would compare to it. Not a prediction of that number.

## P-C  liquidity repaired, bandwidth not: does hand-to-mouth persist?
Liquidity repair = borrowing limit opened to 1.0 (from 0) AND the scarcity tax removed (m_scar = 0). Bandwidth repair = low-income time floor lifted over the gate.
| model | arm | HtM share (low y) | HtM share (all) | mean bandwidth (low y) | median assets (low y) |
|---|---|---|---|---|---|
| bandwidth model (noise + tunneling) | baseline | 0.628 | 0.314 | 0.83 | 0.254 |
| bandwidth model (noise + tunneling) | liquidity repaired | 0.865 | 0.613 | 0.83 | -0.729 |
| bandwidth model (noise + tunneling) | bandwidth repaired | 0.580 | 0.290 | 1.97 | 0.254 |
| bandwidth model (noise + tunneling) | both repaired | 0.785 | 0.516 | 1.96 | -0.729 |
| noise face only | baseline | 0.487 | 0.244 | 0.87 | 0.508 |
| noise face only | liquidity repaired | 0.711 | 0.461 | 0.87 | -0.458 |
| noise face only | bandwidth repaired | 0.415 | 0.208 | 2.04 | 0.763 |
| noise face only | both repaired | 0.596 | 0.370 | 2.03 | -0.186 |
| tunneling face only | baseline | 0.612 | 0.336 | 0.85 | 0.000 |
| tunneling face only | liquidity repaired | 0.811 | 0.541 | 0.85 | -1.000 |
| tunneling face only | bandwidth repaired | 0.534 | 0.271 | 1.99 | 0.254 |
| tunneling face only | both repaired | 0.736 | 0.466 | 1.99 | -0.729 |
| control (both off) | baseline | 0.335 | 0.168 | 0.89 | 1.525 |
| control (both off) | liquidity repaired | 0.486 | 0.290 | 0.89 | 0.627 |
| control (both off) | bandwidth repaired | 0.335 | 0.168 | 2.07 | 1.525 |
| control (both off) | both repaired | 0.486 | 0.290 | 2.07 | 0.627 |
Reading: P-C holds in this world if, in the bandwidth model, 'liquidity repaired' leaves HtM well above 'both repaired' while in the control the two coincide (there, liquidity is the whole story). The residual is the bandwidth share of hand-to-mouth -- the quantity the wealthy-HtM data (Kaplan-Violante-Weidner) could be asked about.

## Dose-response: the divergence as the bandwidth channel closes (scale x multiplies k_tax=0.30 and tunnel=0.06; x=0 is the control)
| scale x | HtM (low y) | time-transfer effect on Q1 savings | money-transfer effect on Q1 savings (net) | P-C residual (liq. repaired − both) |
|---|---|---|---|---|
| 0.00 | 0.335 | +0.0000 | -0.0288 | +0.000 |
| 0.25 | 0.511 | +0.0009 | -0.0250 | +0.101 |
| 0.50 | 0.580 | -0.0002 | -0.0209 | +0.089 |
| 1.00 | 0.628 | -0.0000 | -0.0209 | +0.080 |
| 1.50 | 0.647 | +0.0003 | -0.0214 | +0.044 |
| 2.00 | 0.657 | +0.0004 | -0.0218 | +0.038 |

figure: figures/divergence_small_v0.png   (13s)