# RESULTS 2026-10-24 (rig session) v1.0 — for ruling; manuscript untouched

Three items were queued for Aaron's rig. Two turned out not to need it (exact enumeration in
seconds; a small CPU model in 15 s). Both ran here and are reported below with candidate rulings.
The third — the neural-watcher tournament — is packaged in `code/rig/` and is the GPU job
(`code/rig/README_RIG.md`). All quantities are model-world; nothing is asserted of the world.

Scripts: `code/rig/and_world.py` (shared world; self-test reproduces the printed T11′ floors to
3 decimals), `code/rig/wiring_hardening_exact.py`, `code/rig/divergence_model_small.py`,
`code/rig/watcher_tournament.py` + `summarize_tournament.py`. Outputs: `code/rig/results_exact/`.

---

## A. The wiring theorem, hardened — EXACT (3,372 configurations, 7 s)

Grid: n ∈ {4,6}; s ∈ {0.3,0.5,0.7}; λ* and hand (wider-plateau) policies; m_S ∈ {8,64,1024};
h ∈ 0..7; wirings gated, additive (printed formula), additive at full resolution, the span family
`cell(S,U) = (S + U·d) mod M` for d = 1..m_S, and 8 random bijections per cell. T9′ lower wall
checked on the *realized* policy of each finite quantile grid: **0 violations of 3,372**.

### A1. [REFUTED, scoped — candidate R5] "Gated: permanent inversion at every h" does not survive the wider-plateau policy in low-noise worlds.

Minimum over h ≥ 1 and m_S of (sage − gated floor):

| n | s | λ* policy | hand policy | wall/sage (hand) |
|---|---|---|---|---|
| 4 | 0.3 | +0.188 | **+0.020** | 0.41 |
| 4 | 0.5 | +0.289 | +0.074 | 0.52 |
| 4 | 0.7 | +0.291 | +0.084 | 0.63 |
| 6 | 0.3 | +0.206 | **−0.026** | 0.48 |
| 6 | 0.5 | +0.318 | **+0.017** | 0.58 |
| 6 | 0.7 | +0.393 | +0.067 | 0.68 |

At (6, 0.3, hand, m_S = 8): gated floors 0.528 (h=1), 0.564 (h ≥ 2) vs sage 0.538. The gated
habit-reader does **not** read this agent below the open expert. The Door-2 note's shape-invariance
claim was made for the λ* policy and holds there with margins of 0.19–0.39; T11′ extended the
dichotomy to the hand policy at (4, 0.5) only, where the margin is 0.074. The margin is thin
everywhere on the wider plateau and crosses zero in one of six worlds.

*Mechanism (same as T9′):* the hand policy routes its unpredictability through F where E is wrong.
That part is protected by the lower wall I(A;F|E) whatever the wiring — "chance spent where the world
is wrong cannot be bought" — and when the wall is a large fraction of the sage ceiling, the
habit-gated remainder is enough to lift the floor over the sage. The λ* policy's wall is 0.09–0.27
of the sage; the hand policy's is 0.41–0.68.

**Candidate ruling (default):** keep T11(ii) as printed for the λ* policy; re-scope the Ch 9 §5
passport sentence "the gated floors rise … but stay permanently below the open expert" to "at
(4, 0.5)", and add one sentence: on the wider plateau the inversion's margin is thin and in low-noise
worlds it can fail — the policies that beat full surveillance best are the ones a habit-reader has the
least left to take. Corpse kept inline per the failures policy. Ch 15 §2 "wiring theorem, hardened"
entry: partly closed (see A2–A3), partly sharpened (the inversion is a margin, not a law).

### A2. [PROVEN, 2 lines + verified 0/48 failures] The one-time-pad point is log₂ m_S, not "three bits".

For the printed additive formula, rfrac = ((S+½)/m_S + (U+½)/m_U) mod 1. If m_S | m_U the set
{rfrac : U} is the same grid for every S, so L[S,·,·] is S-independent and δ_∞ = δ₀ exactly. Verified
in all 48 predicted-equal configurations to 1e-9. Below that point the gap δ₀ − δ_∞ shrinks
continuously (mean over worlds): m_S = 64: h=3: 0.010, h=4: 0.003, h=5: 0.0004, h=6: 0; m_S = 1024 the
same digits through h=5, exact at h ≥ 10. The book's "three fresh choices" is log₂ 8 — the key must be
as long as the habit, which is Shannon's condition verbatim. (Necessity is generic, not exact: 4
configs hit equality early by saturating at δ₀ = 1.)

**Candidate ruling (default):** Ch 9 §3(iii)/§4 already names Shannon; print the scaling in one
sentence ("at m_S habits the additive wiring reaches equality at log₂ m_S fresh bits; the three in the
model world is log₂ 8"). Constant → law. Inherited (Shannon 1949), which is the good kind.

### A3. [EXACT] The dichotomy is the two ends of one curve: floor = f(reach).

For the span family the seed-known floor depends on (n, s, policy, h) and on **reach** = d(m_U−1)+1
over M only — the fraction of the quantile axis a habit's fresh bits can travel. 36 cross-m_S groups
with identical reach have floors identical to 4 decimals. n=4, s=0.5, hand, h=3:

| m_S | reach 1/8 | 1/4 | 1/2 | 1 | d0 | sage |
|---|---|---|---|---|---|---|
| 8 | 0.620 | 0.747 | 0.869 | 0.992 | 0.984 | 0.774 |
| 64 | 0.625 | 0.749 | 0.871 | 0.992 | 1.000 | 0.774 |
| 1024 | 0.624 | 0.749 | 0.871 | 0.992 | 1.000 | 0.774 |

Monotone non-decreasing in reach in 175/180 groups; the 5 exceptions are all the h=1 full-wrap edge
(two quantile points, d = m_S). Random wirings sit well inside the interval, nearer the additive end:
at h=3, m_S=1024: hand 0.948 (gated 0.629, additive 0.992), λ* 0.913 (0.363, 0.985); at n=6 the same
ordering. Generic wirings are mostly-additive; the gated wiring is the special, low-reach structure.

**Candidate ruling (default):** Ch 9 §5 one sentence: "the two wirings are the ends of a continuum
indexed by how far the fresh bits travel across the habit's choice space; a random wiring lands near
the additive end, so gating is a thing a routine has to *do*." Ch 15 §2 entry re-worded from "a
general theorem does not exist" to "the one-parameter law for the span family is exact; the general
(arbitrary habit structure) theorem is still open."

### A4. Code hygiene (no ruling needed)
`code/wirings_T11_wider_plateau.py` prints "sandwich ok: False" for the additive wiring because it
tests the sage *upper* wall on seed-known floors, where U is still private; T9′'s upper wall binds
only the fully surveilled floor (h = 0). The book's text makes no such claim; the script's check
message is wrong, not the theorem. Fixed in the rig module (lower wall for every floor, sage wall at
h = 0 only).

---

## B. The small divergence model (HJB–FP, v0) — CPU, 13 s

`code/rig/divergence_model_small.py`; results `code/rig/results_exact/divergence_small_RESULTS.md`;
figure `figures/divergence_small_v0.png`. A standard incomplete-markets household block (assets on
a grid, two-state Markov income, borrowing limit, log utility; β = 0.96, r = 0.03; stationary
distribution by iterating the transition operator) plus ONE new state: bandwidth b ∈ {0..3}, raised
through a gate by the time floor (T5/T16 zero-then-jump), lowered by schedule entropy and by scarcity.
The optimizer is degraded by low bandwidth in two faces kept as separate knobs — **noise** (logit choice
at temperature κ(b)) and **tunneling** (effective horizon β_eff(b) < β; welfare still scored at β). The
control is the same economy with both knobs at 0; every result is model-minus-control; a dose-response
sweep shows the divergence vanishing as the channel closes.

| prediction (MACRO_STEELMAN §3) | v0 verdict | numbers (low-income group unless stated) |
|---|---|---|
| **P-C** HtM persists after liquidity repair if bandwidth is not repaired | **HOLDS as a divergence** | bandwidth model: liquidity repaired → HtM 0.865; both repaired → 0.785 (residual 0.08; 0.04–0.10 across the dose sweep); control: residual 0.000 by construction. Each face alone carries it (noise 0.115, tunneling 0.075). |
| **P-B** schedule stability beats equal-dollar wage transfer on downstream outcomes | **HOLDS on HtM, LOSES on consumption welfare** | stability (s_L 0.35→0.15): HtM 0.628→0.589, bandwidth 0.83→1.26. Wage +0.02/+0.05/+0.10 (4–20% of low income): HtM 0.631/0.637/0.630 — never matches stability on this metric. On E[log c] the wage arm wins from +0.05 up. Control: stability does nothing (not a state there). The model's shadow price of stability is metric-dependent; the HtM metric says "unbounded", the welfare metric says "≈ +0.02–0.05 of income". |
| **P-A** returns to small time transfers concentrate at the bottom beyond money's profile | **REFUTED as stated (on savings)** | time transfer over the gate: Δ savings by wealth quintile +0.000 / −0.000 / +0.007 / +0.026 / +0.052 — the response is at the TOP, because the bottom is corner-constrained (nothing to save out of). It shows up instead in the HtM share: 0.628 → 0.580 (model) vs no change (control). Money transfer: flat profile, both models. |

**Candidate rulings (default):** (i) keep P-C as the lead prediction — it is the one existing data
(wealthy hand-to-mouth, Kaplan–Violante–Weidner) can be asked about; (ii) restate P-A in the
steelman as a prediction about *exit from hand-to-mouth*, not savings levels, and record the v0
refutation of the savings form (the corner constraint is the reason, and it is a real one);
(iii) P-B is printed with both metrics or not at all — the audit must be able to lose, and on E[log c]
it does. (iv) Preregistered form before any dataset: P-A′, P-B (two metrics), P-C, each with the
model-vs-control sign.

Honest limits of v0: two income states, four bandwidth levels, parameters chosen for a sensible
control (HtM 20% overall, 34% low-income), no general equilibrium, no labor supply, tunneling is a
parametrization of the scarcity literature's "the future falls out of the frame", not a derivation.
Built SMALL as ruled. Larger versions only after the field-audit columns exist.

---

## C. The GPU job — not run here

`code/rig/watcher_tournament.py`. Zoo: exact Bayesian (true wiring), Bayesian with the wrong wiring,
three in-context count miners, GRU and causal transformer trained from scratch on unlimited fresh
lifetimes; obs = (E, A) or (E, A, F-lagged); scored by log-loss in units of log₂ n (= the book's δ_A
for the exact watcher, checked side by side). Tier A: 72 configs (n=4; both policies; gated /
additive / random; m_S 8 and 1024; h 1–3; two architectures). Tier R: 40 configs (the regress: the
"fresh" coin is an LCG with 8/12/16/32-bit hidden state, vs truly iid). Smoke test on CPU: a 128-k
parameter GRU trained 500 steps reaches 0.704 vs the exact floor 0.700 at m_S = 8 — the structure-free
watcher gets the inversion there. The question the rig answers is whether it still does at m_S = 1024
with a 512-day window, and what happens to the floor when the coin is secretly a generator.
