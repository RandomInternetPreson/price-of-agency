# RESULTS — the bandwidth block in a standard HANK, general equilibrium (v0.1, 2026-11-09)

Code: `code/rig/hank_port/` (bw_hank.py — the block; hank_ge.py — the economy; run_hank_v01.py,
hank_pigou.py, run_hank_irf.py — the experiments). Tables: `code/rig/results_exact/hank_v01_RESULTS.md`,
`hank_pigou_RESULTS.md`, `hank_irf_RESULTS.md`. Figures: `figures/hank_v01_summary.png`, `hank_pigou.png`,
`hank_irf_linear.png`, `hank_irf_gate.png`. Preregistration: `docs/HANK_PREREG_v0.1.md` (signs committed
before the runs; one dated addendum). Host: the Sequence-Space Jacobian toolkit (Auclert, Bardóczy,
Rognlie, Straub 2021), one-asset HANK with sticky prices and sticky wages, the toolkit's own calibration.
CPU only; each experiment set runs in ~12 minutes.

## What was built
The book's bandwidth household — state (bandwidth b, skill e, assets a); logit noise κ(b) and tunneling
β_eff(b) as separate knobs; bandwidth moved by a time-floor gate, schedule entropy, and scarcity — as a
native block of the toolkit: steady state, sequence-space Jacobians (the fake-news algorithm run on the
block's own dense transition operator, so the stochastic policy is handled exactly), nonlinear transition
paths. **Nesting check:** with the knobs off and the noise floor → 0 the block converges to the toolkit's
EGM household (wealth within 1.3%, consumption within 0.1% at the finest grid; the residual is grid).
Control = knobs off; every result is **model minus control**, each at its own GE steady state, with the
partial-equilibrium (prices fixed) number beside it.

## The ruling made on the way (dated in the preregistration)
The first run's household forecast its own bandwidth transitions. Under that household the repairs lost
their effect or reversed it — the time transfer left the low-skill hand-to-mouth share unchanged while
lifting the group's bandwidth by half; stability raised it — structurally, not by bug (no drain → identical to control; all at b = 0 →
maximal HtM): a sophisticated household plans around its future degraded selves, the opposite of what the
scarcity literature describes. Default is now **naive** (plans as if its bandwidth level were permanent; the
true law of motion acts on the distribution); the sophisticated variant is a switch and is printed beside it.
**The finding itself:** whether bandwidth repairs help, do nothing, or hurt depends on whether the household
anticipates its own tunneling. This is a stated condition of the book's mechanism from now on, not a footnote.

## Scorecard against the preregistration (naive default; GE unless marked)
| prediction | committed sign | result | verdict |
|---|---|---|---|
| **GE transmission** (not preregistered; seen first) | — | at the control's β, the model needs r = 0.67%/qtr vs 0.50% to hold the same bonds; asset demand −15% at fixed prices (−30% sophisticated) | GE transmits the mechanism into the real rate; it does not wash it out |
| **P-A′** time transfer vs equal-cost money, ΔHTM_low model−control | time < money < 0 | GE: time −0.028, money −0.017; PE: time −0.030, money −0.058 | **holds in GE, fails in PE**: at fixed prices the cash lifts households out of the scarcity drain and does the time transfer's job better; in GE that advantage shrinks by 2/3 and the time transfer wins. The preregistered failure mode (instruments converge) is what happens in PE |
| **P-B** stability vs equal-dollar transfer, HtM metric | stability wins | GE: −0.016 vs +0.001; PE: −0.016 vs −0.008 | **holds**, both equilibria |
| **P-B** welfare metric (true-β, low group) | none committed | GE: stability +0.141 vs wage +0.033; PE: +0.196 vs +0.172 | stability wins on welfare too in this host (v0 had the wage arm winning on consumption) |
| **P-C** HtM residual after liquidity repair (limit 0 → 0.5) | residual > 0 | GE: +0.075 (baseline +0.064); PE: +0.116 (+0.109) | **holds**; the residual does not shrink with liquidity. Repairing bandwidth too (time + stability) closes about half of it (0.568 vs control 0.536); removing the drain entirely closes it exactly |
| **P-E** dr*/dS > 0; dA/dS < 0 at fixed prices | both | r*: 0.51% → 0.81%/qtr over S = 0 → 2; A(PE): 5.53 → 4.13 | **holds** |
| **P-E** gate crossing (the T16 time gate in aggregate; called the 'T17 cascade' in this file's first printing, a mislabel): hours through the middle group's gate | discontinuous BW drop | PE: BW 0.701 → 0.343, HtM 0.24 → 0.41, A −1.1 in one step at N = 1.05 | **holds** (by construction the middle group sits 0.05 from its gate; the size is a model constant, the discontinuity is the theorem) |
| **Dose–response** | → 0 at dose 0, monotone | Δr*: 0, +0.05, +0.09, +0.17, +0.23 pp; ΔHTM_low: 0, .020, .039, .064, .081 over doses 0–1.5 | **holds** |

## The externality priced (hank_pigou.py)
Firm labor-cost factor g(S) = 1 − η(1 − e^{−S}) + νS²/2 (η = 0.06, ν = 0.02; saving saturates, convex
private cost): private optimum S_priv = 1.055. Planner (max aggregate true-β welfare in consumption
equivalents, each S at its own GE): **S_soc = 0.916** in the model; **1.055 in the control** — the control's
planner and firm agree, so the wedge is the externality and nothing else. Pigou tax **τ* = 0.57% of the wage
bill per unit of S**. Welfare cost of the bandwidth channel at the private optimum: **−0.42% of consumption**
(−0.72% at S = 2, −0.06% at S = 0). Modest at these knobs; dose-dependent; the point is that it is computable
in a standard host and that the private and social optima separate only when the channel is on.

## Dynamics (run_hank_irf.py)
- **Monetary shock (−25 bp, AR 0.8):** the model's output response is **1.78× the control's on impact and
  1.58× cumulative** — the bottom's taxed optimizer raises the economy's MPC profile, the question the plan
  asked a toy could not answer. The bandwidth state itself barely moves (the shock does not cross a gate).
- **Entropy shock (S +0.5, AR 0.9):** the control does not respond at all (S is payoff-irrelevant there); the
  model's bandwidth falls 2.4% at peak over 12 quarters, HtM rises with a lag, r rises; output dips on impact
  then rises as tunneling raises consumption.
- **Nonlinear path through the gate (the thing linearization cannot see):** expansions of −100 bp (peak
  N = 1.022, below the gate) leave linear and nonlinear paths within 3%. At **−300 bp** hours peak at 1.064,
  through the middle group's gate: bandwidth falls (−0.019; the linear path says 0), the cumulative output
  response is **+40% above the linear one** (0.221 vs 0.158), and the hand-to-mouth relief is **cut by 42%**
  (−0.256 vs −0.439). At −500 bp (peak N = 1.138): bandwidth −0.037, output **nearly double** the linear
  response (0.504 vs 0.263), HtM relief less than half (−0.341 vs −0.732). The crossing removes the middle
  group's recovery rather than adding a drain, so bandwidth erodes over the quarters above the gate and the
  tunneling it causes feeds consumption — an expansion that overworks the middle is louder in output and
  quieter in balance sheets than any linear model of it. (The gate's position is a model constant; the
  asymmetry around it is the theorem.)

## Honest limits
Three skill states, four bandwidth levels; hours are the union's, not the household's; the gate position,
the drains, the knobs are model constants rescaled from v0 to a quarter, not calibrated to data; the
externality is imposed as an unpriced cost, not derived from contracting; the naive/sophisticated ruling is
a modeling choice, dated, with both printed. The HtM effects of repairs are 2–3 pp — small; the GE
transmission into r and the MPC amplification are the robust results. Nothing here is a statement about the
world; the field audit (Shift Project + ATUS + SHED) remains the test, with P-A′'s PE failure as a
preregistered warning: an instrument comparison that ignores prices can rank the arms wrongly.
