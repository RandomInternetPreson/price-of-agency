# Preregistration — the bandwidth block in general equilibrium (HANK port v0.1), 2026-11-09

Written BEFORE any prediction was run in the HANK host. The only runs made so far are the
nesting check (control block vs the toolkit's EGM household; gap closes with k_min → 0 and
grid refinement) and one steady state at the UNSCALED v0 knobs, which showed the knobs are
far too strong for a quarterly economy (real rate 0.5% → 4.1% per quarter). The defaults
below are the v0 (annual) constants rescaled to a quarter before any prediction is looked at:
per-period probabilities p → 1 − (1 − p)^{1/4}; tunnel → 1 − (1 − 0.06)^{1/4}. Noise
temperatures are in utility units and are swept (dose–response), not calibrated.

## Host
One-asset HANK, sticky prices (Rotemberg) and sticky wages (union), the Sequence-Space Jacobian
toolkit's layout and calibration (r = 0.5%/qtr, B/Y = 1.4 annual, μ = 1.2, EIS 0.5, Rouwenhorst
3-state skill with ρ = 0.966, σ = 0.5). Control: the same economy with k_tax = tunnel = 0
(bandwidth payoff-irrelevant). The control's β and union parameter vphi are calibrated once
(A = B, N = 1); every other economy keeps them and clears markets by (r, Y).

## Reporting rule
Every number is **model minus control**, each at its own general-equilibrium steady state;
the partial-equilibrium (prices held at the control's) version is printed beside it as the
check for whether GE amplifies, damps, or reverses the toy's result. Levels are never the claim.

## Predictions, with the sign committed in advance
- **P-A′ (time transfer → hand-to-mouth exit).** A time transfer to the low-skill group that lifts
  its time floor across the gate lowers the low-skill hand-to-mouth share in the model and not in
  the control; an equal-cost money transfer (wage-valued) lowers it by less in model-minus-control
  terms. *Sign: ΔHTM_low(time) < ΔHTM_low(money) < 0 in the model; both ≈ 0 difference in control.*
  Failure mode to watch: in GE the money transfer raises the low group's cash-on-hand and so
  removes the scarcity drain — the two instruments may converge. If they do, the toy's P-A′ does
  not survive GE and will be printed as such.
- **P-B (stability vs equal-dollar wage transfer), two metrics.** Halving the low-skill schedule
  entropy beats an equal-cost wage transfer on HTM_low; on true-β welfare of the low group the
  wage arm may win (as in v0). *Sign: stability wins on HTM; no sign committed on welfare.*
- **P-C (liquidity repaired, bandwidth not).** Opening a borrowing limit of half a quarter's mean
  income cuts HTM_low in both economies; the model's residual HTM_low above the control's stays
  positive. *Sign: residual > 0; it closes when the bandwidth channel is also repaired.*
- **P-E (the GE externality, new to this host).** Raising schedule entropy S lowers aggregate
  bandwidth and raises the equilibrium real rate needed to hold B, i.e. the economy pays for the
  firm's private saving in a higher r and lower aggregate assets at the control's prices.
  *Sign: dr*/dS > 0 in GE; dA/dS < 0 in PE.* The cascade (T17) is live when hours N rise past
  a skill group's time gate: aggregate bandwidth then drops discontinuously. *Sign: BW falls when
  N crosses Tbar_mid − T_gate, by more than the smooth response on either side.*
- **Dose–response.** Every divergence above → 0 as (k_tax, tunnel) → 0; monotone in between.

## Honest limits, stated now
No labor-supply margin for bandwidth itself (hours are the canonical union's); three skill
states; four bandwidth levels; the gate is a model constant; tunneling and noise are
parametrizations of the scarcity literature, not derivations; the externality is imposed as an
unpriced cost, not derived from a contracting friction. Nothing here is a statement about the
world; the field audit (Shift Project + ATUS + SHED) remains the test.

## Addendum, same day, after the first full run (recorded, not hidden)
The first run used a SOPHISTICATED household — one that forecasts its own bandwidth transitions
and values the future through the degraded self's own value function. Under it the repairs
lost their effect or reversed it: the time transfer left the low-skill hand-to-mouth share where it
was (−0.0001 in GE) while lifting the group's bandwidth by half, and schedule stability RAISED it
(+0.027 model − control) and lowered low-skill wealth; P-A′ and P-B came out null or wrong-signed.
(Removing the drain entirely still closes the gap to the control under either forecast.) The reason is structural,
not a bug (checked: no drain → identical to control; all at b = 0 → maximal HtM): a sophisticated
household treats its future degraded selves as part of its planning problem, which is the
opposite of what the scarcity literature describes (the tunnel is not perceived from inside).
Ruling: the default household is NAIVE about its own bandwidth (plans as if its level were
permanent; the true law of motion acts on the distribution), with the sophisticated variant kept
as a switch and reported beside it. The preregistered signs above are re-run under the naive
default; the sophisticated results are printed in the same file as the forecast comparison.
A reader is entitled to treat this as a post-hoc modeling choice; it is dated here so that it can be.
