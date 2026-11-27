# δ_A Phase 1 — Measurement theory: first exact results

Notation. Latent future F with prior p(f); local environment E with channel
p(e|f); knowledge channel K with p(k|f), conditionally independent of E given
F; action A on alphabet 𝒜 with |𝒜| = |ℱ|; reward r(a,f) = 1[a=f].
Bounded-rational policy: p(a|e,k) ∝ exp(β·P(F=a|e,k)). Definitions:

    δ_A        = H(A|E) / log₂|𝒜|          (normalized conditional entropy)
    competence = I(A;F) / H(F)             (normalized goal information)

"Sage" = perfect education (K = F) at β → ∞. "Rock" = null education
(K ⟂ F) at β → ∞ with any fixed tie-breaking rule, so A = g(E) for a
deterministic decision rule g (the MAP rule given E alone).

---

## Theorem 1 (Sage ceiling). [PROVEN]
For any prior p(f), any environment channel p(e|f):

    δ_A(sage) = H(F|E) / log₂|𝒜| .

If additionally the prior is uniform (H(F) = log₂|𝒜|):

    δ_A(sage) = 1 − I(F;E)/H(F) .

*Proof.* With K = F, the posterior P(F|E,K) is a point mass at k, so as
β → ∞ the policy selects A = K = F with probability 1. Hence H(A|E) =
H(F|E) = H(F) − I(F;E). Normalize. ∎

*Reading.* The maximum purchasable free fraction is set entirely by the
environment's information about the future — not by any property of the
agent. Education buys back exactly the future-irrelevant predictability and
can never (rationally) buy back the future-relevant part. Ceiling theorem,
same genre as F ≤ 1/2: total decorrelation from circumstance is never
achievable in a predictive environment, and never required to reach full
competence.

## Theorem 2 (Complementarity). [PROVEN]
With uniform prior, for any environment channel:

    δ_A(sage) + competence(rock) ≤ 1 ,

with equality iff the rock's decision rule g(E) is a sufficient statistic
for F within I(·;F) — i.e. I(g(E);F) = I(E;F).

*Proof.* competence(rock) = I(g(E);F)/H(F) ≤ I(E;F)/H(F) by the data-
processing inequality (A = g(E) is a function of E). Add Theorem 1's
equality δ_A(sage) = 1 − I(E;F)/H(F). Equality iff data processing is
tight, i.e. g loses no information about F. ∎

*Reading.* Circumstance's information about the future, I(E;F), is
partitioned exactly: it is simultaneously (i) the ceiling on the rock's
competence and (ii) the floor on the sage's environmental predictability.
What the environment knows about tomorrow is the common currency of both
extremes. The symmetric-channel model of v1 satisfies the equality
condition (g = identity is sufficient there), which is why the corner
values summed to 1.0000 exactly.

## Proposition 3 (Time theft is not freedom). [PROVEN, model class]
As β → 0, p(a|e,k) → uniform for all (e,k), hence δ_A → 1 and
I(A;F) → 0 jointly. Raw H(A|E) is therefore maximized by the agent with
*no* deliberation resources; only the pair (δ_A, competence) separates
deprivation from agency. ∎

## Conjecture 4 (Education monotonicity). [REFUTED — exact counterexamples]
δ_A is NOT monotone in education fidelity e. Refuted by exact enumeration
(verify_theorems.py: thousands of strict decreases across symmetric and
random channel classes, at both high and finite β). The refutation
decomposes into two exact phenomena:

### 4a. Activation threshold (dead zone). → PROMOTED to Theorem 5 below.

## Theorem 5 (Activation threshold e* = 1 − s). [PROVEN]
Symmetric class, uniform prior, β → ∞. Parametrize the environment
channel as "reveal F w.p. (1−s), else uniform" and the knowledge channel
as "reveal F w.p. e, else uniform." When the two signals disagree
(e_obs ≠ k_obs), the MAP agent follows K iff e > 1 − s; when they agree
the action is common. Hence for e < 1 − s the optimal action is a
function of E alone (δ_A = 0 exactly), and for e > 1 − s the agent
defects to K wherever the signals disagree (δ_A > 0).

*Proof.* Posterior odds of f = k_obs against f = e_obs are
[P(e_obs|k_obs)·P(k_obs|k_obs)] / [P(e_obs|e_obs)·P(k_obs|e_obs)]
= [ (s/n)·(e + (1−e)/n) ] / [ ((1−s) + s/n)·((1−e)/n) ].
This exceeds 1 iff s·e·n + s(1−e) > (1−s)(1−e)n + s(1−e), iff
s·e > (1−s)(1−e), iff e + s > 1, i.e. e > 1 − s. All other candidate
futures carry the miss probability on both channels and never win. ∎

*Corollaries.* (i) e* = 1 − s is INDEPENDENT of the alphabet size n:
the gate's location is not an artifact of how finely the future is
resolved. (ii) The condition is symmetric in the two channels — the gate
is a *reliability race* between the environment and the agent's knowledge,
nothing more. (iii) The dead zone is exactly the region where the local
environment out-competes the agent's education as a predictor of the
agent's own future; inside it, rational agents are rocks regardless of
partial education. Gate verified numerically for n ∈ {4,…,10}.

### 4b. Noise-subsidized freedom (overshoot). [exact on model class]
Just above e*, δ_A OVERSHOOTS the sage ceiling of Theorem 1 (e.g. s = 0.5:
δ_A = 0.903 at e = 0.6 vs ceiling 0.753), then decays monotonically down
to the ceiling as e → 1. The excess conditional entropy is the noise of
the imperfect knowledge channel, carried into action. It looks like
freedom on the one-axis measure and is not: competence at the overshoot
peak is far below 1. Consequence: Theorem 1's ceiling bounds the δ_A
purchasable AT full competence; raw δ_A above the ceiling is diagnostic of
error, not agency. The correct object is therefore the Pareto frontier in
the (competence, δ_A) plane; genuine AND is position relative to that
frontier, and the sage point (1, H(F|E)/log₂|𝒜|) is its endpoint.

Epistemic note: the conjecture was proposed, hunted adversarially, and
refuted by exact computation in the same session; the refutation is
recorded because it produced more structure than the conjecture would
have.

## Theorem 6 (Covert agency plateau). [PROVEN by explicit construction]
Symmetric class, uniform prior, e = 1. There exists a policy family
p(a|f,e) = λ·δ_{a,f} + (1−λ)·r_e(a), with r_e the E-dependent residual
that whitens the action distribution, achieving

    δ_A = 1 exactly, with competence > 0,   for all λ ≤ λ* = 1/(n(1−s)+s).

The plateau ends at c₀(s) = competence(λ*): c₀ = 0.016 (s=0.3), 0.052
(s=0.5), 0.138 (s=0.7) at n=6; c₀ is increasing in s. [closed form: TODO]

*Reading.* Perfect unpredictability from local circumstance is FREE up to
c₀ bits of normalized goal-information; beyond c₀, additional competence
must be purchased with visibility. Two-sided structure, same genre as
F ≤ 1/2: full stealth is never impossible (plateau exists at every s), and
full competence is never stealthy (Theorem 1 ceiling < 1). Note the sign:
the more stochastic the environment, the MORE covert competence is
available — chaos subsidizes illegible agency.

## Frontier status. 
- Mixing-sage candidate: [REFUTED] — beaten by +0.0321 (exact metrics) by
  an E-conditioned policy found under adversarial optimization.
- Water-filling family (flatten p(a|e) subject to following F w.p. λ):
  [CONJECTURE — near-optimal lower bound] dominates mixing everywhere;
  best attack exceeds it by only +0.0014, so it is not exactly optimal or
  the curve is non-concave at low competence. Exact frontier: OPEN.

## Proposition 7 (Robustness of illegibility). [exact, model class]
Along the bounded-deliberation path π_t ∝ π*^t from the uniform default to
the whitening target, δ_A remains ≥ 0.9926 for all t (n=6, s=0.5), while
competence falls from c₀ to 0 as t → 0. Against model misspecification
(whitening vs believed ŝ), δ_A is second-order insensitive: leak is
quadratic with small curvature (−0.23 at ŝ = s); the first-order cost of
misbelief is competence miscalibration (ŝ < s: safe competence unclaimed;
ŝ > s: overreach, gentle visibility leak). H1 ("stealth is time-gated"):
REFUTED. H2 ("stealth is model-gated"): PARTIALLY — model knowledge
locates the safe operating point on the plateau; it does not protect
δ_A itself, which is robust.

## Corollary 7.1 (Cheap theft / the third failure of the one-axis measure).
Time theft applied to a covert agent CONSERVES δ_A ≈ 1 while destroying
competence. Coercion therefore never needs to make an agent predictable:
making its unpredictability USELESS is sufficient, cheaper, and invisible
on any one-axis freedom measure. Unpredictability is cheap; effective
unpredictability is the scarce, thievable good. This is the third
independent failure mode of raw H(A|E) (after β→0 randomization and
noise-subsidized overshoot) and the strongest argument yet that AND must
be defined on the (competence, δ_A) frontier.

## Proposition 8 (Front-loaded returns to deliberation). [exact, model class]
For the overt MAP agent, the deliberation path buys competence
concavely — 47.7% of full competence by t = 0.10, 97.8% by t = 0.25 —
and pays the visibility price on the same schedule. First moments of
thought are the most valuable and the most visible.

## Theorem 9 (Observer-relativity and surveillance inversion). [exact, model class]
δ_A is observer-relative: δ_A(𝒪) = H(A|𝒪)/log₂|𝒜| for information set 𝒪.
For the on-plateau covert agent implemented with private randomness R:
δ_A({E}) = 1, but δ_A({E,R}) = 0.291 < 0.753 = sage ceiling. Under partial
surveillance capturing R w.p. ρ, δ_A(ρ) is exactly linear, crossing the
sage ceiling at ρ ≈ 0.348. INVERSION: a fully surveilled stealth agent is
MORE predictable than a fully overt sage — the stealth policy's mass is
deterministic residual machinery; once its coin is watched, only the
λ-fraction routing genuine F-information retains any entropy. Privacy is
the load-bearing resource of covert agency; it is the ONLY channel through
which δ_A of a covert agent can be attacked, and its yield is linear.

## Theorem 10 (Theft equilibrium from the elasticity matrix). [exact, model class]
Unit-free elasticities (dlog y / dlog x), no cost assumptions:
(i) COVERT agents: δ_A-elasticity ≤ 0.009 for every resource attack (time,
model knowledge), while competence-elasticity ≈ 1.5–2.0. Competence
attacks dominate by ~10³:1 — cheap theft (Cor 7.1) is the coercer's
dominant strategy against covert agents for ANY objective mixing
legibility and incapacitation.
(ii) GATE KNIFE-EDGE: for overt agents at their activation threshold
(e ≈ 1−s), δ_A-elasticity w.r.t. education spikes to +9.2 and w.r.t.
environmental legibility to +4.5 — an order of magnitude above all other
entries. Agents near their gate are maximally vulnerable: marginal
education theft or legibility injection drops them into the dead zone
entirely.
(iii) TIME-POVERTY CONCENTRATION: competence-elasticity w.r.t. β is 0.565
at β = 6 vs 0.008 at β = 20 — marginal time theft yields ~70× more against
the already time-poor (P8's concavity, now unit-free).

*Derived coercer playbook (structural, zero moral premises):* attack
competence against the covert; attack education/legibility against the
gate-adjacent; attack time against the time-poor; attack privacy when
legibility of the covert is itself the objective. *Derived defense:* keep
populations far from their gates, floor the time budgets of the time-poor,
and protect randomization privacy — each provably the highest-elasticity
countermeasure for its regime.

## Theorem 11 (Sustainable stealth floor; the architecture dichotomy).
[floors exact; transients MC with exact per-step Bayesian updates]
Against an adaptive observer running exact Bayesian extraction of the
agent's habit seed S (m_S = 8) from the behavioral stream, with fresh
entropy rate h bits/action:
(i) TRANSIENT: δ_A(t) decays from ≈1 to the floor δ_∞(h) within ~10–20
    steps at h ≥ 1. The observer's information gain is front-loaded —
    the surveillance mirror of P8.
(ii) GATED MIXING (fresh randomness confined within the habit cell):
    δ_∞ ∈ [0.45, 0.49] for ALL h ≥ 1 — permanently below the sage
    ceiling 0.774. Dynamic surveillance inversion: the habit-gated covert
    agent under a converged observer is more predictable than an overt
    sage FOREVER, at every entropy rate tested. Adding fresh entropy
    cannot fix a gated architecture.
(iii) ADDITIVE MIXING (fresh randomness spans the full range; habit is a
    phase offset): δ_∞ rises with h — 0.753 (h=1), 0.960 (h=2), and at
    h = 3, δ_∞ = 0.978 = δ_A(seed unknown) EXACTLY: the habit seed
    becomes information-theoretically worthless to the observer.
    One-time-pad equality for behavior.
    [Corrected 2026-11-24. These are the exact floors of the printed wiring,
    from code/wirings_T11_wider_plateau.py and design/make_figures.py
    (wirings), which agree; the R4 entry below already printed them. The
    figures first printed here, 0.761 / 0.947 / 0.984, are reproduced by no
    script in the repository; 0.984 is the seed-unknown value at h ≤ 2.
    The statement is unchanged: the floor rises with h and meets the
    seed-unknown value exactly at h = 3 = log₂ m_S. The book prints none
    of these numbers.]
(iv) h = 0 is fully extractable under both architectures (floor ≈ 0.34),
    up to permanent aliasing classes (indistinguishable seeds).

*Reading.* What surveillance can extract is determined not by how much
unpredictability an agent has but by HOW its spontaneity is wired to its
habits. Routines that gate spontaneity (deciding when/where the coin gets
flipped) are extractable regardless of the coin; full-range spontaneity
with habitual bias is protected at modest entropy rates. Defensive
constant for this class: ~2–3 genuinely fresh bits per action, additively
mixed, make total habit surveillance worthless. Privacy engineering for
agency, quantified.

## Theorem 12 (Neighbor coupling: freedom capacity is rivalrous through
legible competence). [exact, model class; n=4, s=0.5, shared future]
B's environment = (E_B, A_A), A acting first on the shared future.
B's sage ceiling: 0.774 (no neighbor) → 0.712 (covert A) → 0.609 (rock A)
→ 0.000 (sage A). A neighbor consumes B's freedom capacity in proportion
to the F-information its actions leak; a perfectly transparent competent
neighbor consumes ALL of it — B can be fully competent by copying, but no
education at any strength buys B any independence (gate welded, e* > 0.999).
B's weak escape gate: 0.504 (alone, = 1−s per T5) → 0.175 (covert) →
0.010 (rock): imperfect neighbors create ambiguity pockets between signal
sources that make even weak education decisive somewhere. Nonmonotone in
neighbor legibility: partial legibility opens the gate, perfect legibility
welds it. (Weak-gate definition sensitivity flagged; strong-gate rerun
queued.)

## Door-2 generalization note. The T11 architecture dichotomy is
shape-invariant across n ∈ {4,5,6}, s ∈ {0.3,0.5,0.7}, and random
asymmetric environment channels: gated floors saturate strictly below the
sage ceiling in every setting; additive floors reach 0.984–0.997 at
h = 3 in every setting. Constants are class properties; the dichotomy is
not.

## Theorem 13 (The fishing town: survival structure). [exact; iid-day class]
N fishers, shared future, majority/total-failure survival metrics, 90-day
seasons, all famine probabilities exact via streak Markov chains.
(i) CONDORCET SURVIVAL EXPONENTIAL: famine probability falls exponentially
in the number of independent educated fishers (~×0.52 per +2 fishers,
N=3→13). Nine independent 0.70-accurate fishers beat one 0.80-accurate
central authority 6-fold on famine (0.074 vs 0.439) and on single-day
accuracy (0.901 vs 0.800). This is the computed mechanism of the Part XV
survival exponential.
(ii) HOMOGENEITY COLLAPSE: nine educated fishers sharing one tutor have
famine 0.833 — EXACTLY the single-fisher value. Identical competence
sources give N_eff = 1 at any N: same heads, same individual accuracy,
11× worse survival than privately-tutored, from correlation alone.
(iii) CENTRALIZATION DOSE–RESPONSE: famine vs hub-followers is NONMONOTONE
— a beneficial dip at 1 follower (0.049 < 0.074: importing the hub's
higher accuracy without bloc formation), then a rise and exact saturation
at bloc majority (5 of 9), where the hub decides everything (0.439,
N-independent). Small listening helps; bloc formation poisons.
(iv) WILDCARD INSURANCE: in the shared-tutor town, each covert fisher cuts
starvation ~6× (0.833 → 0.00015 at c=5) for ~0.23 boats/day of yield —
interior optimum under any combined yield-survival criterion. In the
private-tutor town, covert fishers strictly INCREASE starvation
(6.7e-13 → 5.5e-10): decorrelation insurance is worthless, indeed
harmful, when error sources are already independent.

## Preregistration scores, round 1
Aaron: A-P1 HIT (distributed beats centralized), A-P4 HIT (interior
wildcard optimum where blind spots are shared), A-P5 HIT — exact
(homogeneity collapse to N_eff = 1). 3/3 scored.
Claude: C-P1 HIT, C-P2 HALF (cliff located exactly at 5/9; missed the
beneficial dip), C-P3 UNTESTED (deferred), C-P4 HIT (both halves),
C-P5 HIT. Aaron leads.

## Theorem 14 (The correlation floor). [exact; common-shock class]
Tutors share one draw with probability ρ per day (ρ=0: private-tutor town;
ρ=1: shared-tutor town — T13's endpoints become a continuum).
(i) The Condorcet survival exponential survives ONLY down to a floor:
famine(N) peels off exponential descent and plateaus at famine(ρ·(1−acc)),
which no N can breach. Scale buys the trip to the floor, never below.
(ii) Correlation taxes scale specifically: at N=9, ρ=0.05 costs 1.3×;
at N=31 the same ρ costs 16× (0.0012 vs 7.6e-5). The larger the society,
the more its safety is bounded by its correlation, not its size.
(iii) Convex poison: famine(ρ) at fixed N rises superlinearly (streak
mechanics compound the daily failure rate).
(iv) Wildcard asymmetry: covert fishers cut the STARVATION floor
multiplicatively (×0.525 per wildcard — immune to the shared mirage) but
cannot touch the FEAST floor (shock-wrong-day majority failure = 1.000 at
any insurable wildcard count): wildcards insure subsistence, not
prosperity.
Prior-art echo, filed for App E: (i)–(ii) are the information-theoretic
sibling of undiversifiable systematic risk in portfolio theory.

## Preregistration scores, round 2
Claude C-P6, C-P7, C-P8: HIT, HIT, HIT — with the honest caveat printed:
these were derivation sketches confirmed, not blind predictions; scored in
a separate column from blind hits. Aaron's slot was open this round;
resumes next round. Running blind-column score: Aaron 3/3, Claude 3.5/5.

## Strong-gate resolution (Referee Attack 7). [EXACT]
Gate redefined as min e with aggregate δ ≥ 0.05 (vs weak: δ > 0 anywhere).
Results identical to three decimals in every case (absent 0.500, covert
0.175, rock 0.010, sage welded): the δ_A jump at the threshold is
discontinuous, so weak and strong definitions coincide on this class.
T5 and T12 are definition-robust. Attack 7 closed.

## Proposition 15 (Ceiling erosion is submodular). [EXACT]
B's freedom ceiling vs k rock neighbors (shared future, n=4, s=0.5):
0.774 → 0.609 → 0.479 → 0.379 → 0.300; bites 0.166, 0.129, 0.100, 0.079.
Each additional legible neighbor consumes less capacity than the last
(conditional information of correlated sources is submodular). C-P3
(frozen in FISHING_TOWN_design.md before computation): HIT, blind column.
Blind score: Aaron 3/3, Claude 4.5/6.

## Dual-track competence audit (Referee Attack 3). [EXACT]
Rerun of core results under accuracy-competence P(A=F) in place of I(A;F):
- Gate T5: location IDENTICAL (MAP structure is metric-independent). ROBUST.
- Time theft P3/Cor 7.1: β→0 gives δ_A→1, accuracy→chance. ROBUST.
- Plateau T6: δ_A=1 with accuracy 0.475 > chance 0.25. ROBUST.
- Complementarity T2: I-SPECIFIC (accuracy version sums to 1.399; no
  identity). The book states T2 as an information-theoretic partition,
  which it is; no result downstream depends on the accuracy version.
Attack 3 closed with one scoped concession, printed.

## Theorem 16 (The time-model dichotomy; the time gate). [EXACT]
Rival deliberation model (Referee Attack 4): time = T sequential noisy
internal glimpses of F; environment reading is free; MAP action.
(i) THE GATE REAPPEARS IN TIME: δ_A = 0 EXACTLY at T = 0 and T = 1
(single-glimpse reliability 0.5125 < environment 0.625: rationally
ignored); independence activates only when ACCUMULATED evidence beats the
room (here T* = 2). The education gate (T5) and the time gate are the
same theorem — a reliability race — fought with different currencies.
(ii) FRONT-LOADING (P8) IS MODEL-ROBUST, with a corrected shape: returns
per unit time are zero (below gate), then largest, then diminishing
(+0.049, +0.041, +0.029, ...): "zero, spike, decay."
(iii) TIME-THEFT DIRECTION DEPENDS ON THE ZERO-TIME DEFAULT:
annealing default (noise) → victim driven to the GAS: erratic,
unpredictable, useless — scores "free" on naive measures.
Iterative default (the room) → victim driven to the ROCK: conformist,
moderately competent, fully legible — scores "orderly" on naive measures.
Cheap theft (Cor 7.1) SURVIVES IN BOTH MODELS — agency is destroyed
cheaply either way — but its observable signature inverts. Both
signatures are invisible to one-axis measurement; both are recognizable
social phenomena.
(iv) SCOPED REVISION OF P7, printed: "stealth is robust to time theft"
is ANNEALING-SPECIFIC. Under the iterative model, whitening costs
computation; below that cost the agent emits its free default (the room)
and stealth collapses to δ_A = 0 exactly. The architecture of the
zero-time default — noise vs room — decides whether time theft spares or
destroys covert agency. P7 stands within its model class; the class is
now named on its label.
Referee Attack 4 closed: results replicated where robust, scoped where
not, and the dichotomy itself is a new theorem.

## S1 (The living town). [SIMULATION — 400 seeded runs per condition,
adaptive payoff-learning fishers, established-broadcast start]
(i) OBSERVATION ALONE LOCKS THE HERD. With infinite fish (no crowding
cost), result-watching fishers rationally learn the hub (0.8) beats
their own signal (0.7) individually; as agents become more rational
(colder choice), hub-following RE-FORMS to 0.92. Individually rational,
collectively fragile: majority-hit stays hub-limited (~0.85).
(ii) FINITE FISH CONVERT THE TOWN. With daily yield split among boats
on the fish ground, the herd dissolves to an interior mix (~0.49-0.51
hub-following) that is an equilibrium, not noise — it PERSISTS as
agents become more rational — while majority accuracy RISES (0.85 →
0.89) and famine risk halves (0.21 → 0.09). Lone correct defectors eat
alone; crowded correct followers split nine ways; the fish themselves
teach the town to decentralize.
(iii) PREDICTION SCORED. Aaron's broadcast-conversion prediction:
CONDITIONAL HIT — true under the mechanism he himself supplied months
before the model existed ("wouldn't they realize they are overfishing
and move?"): conversion requires finite resources. The observation-only
version is REFUTED (it produces lock-in). His two old answers were one
prediction.
(iv) INTERPRETATION, flagged as such: scarcity decentralizes; costless
crowding herds. Any economy whose goods are infinitely shareable at
zero crowding cost — notably information feeds — removes the natural
force that dissolves herds, leaving the sameness floor of T14 with no
endogenous correction. [INTERPRETATION on SIMULATION; field-audit
relevance queued.]


## T17 (The Ledger of Imposition). [EXACT within model class]
Hierarchy of bounded agents (L levels, branching b); exogenous variance
arrives at top; each agent absorbs up to capacity (proportional to
resources, declining downward); unabsorbed variance is BROADCAST whole
to each subordinate. Results (reference parameterization L=4, b=4,
capacities 60/20/6/1, Ch7-shaped elasticities):
(i) Unabsorbed share rises monotonically downward (top absorbs 60% of
what it faces; bottom 7%).
(ii) Agency loss per person is 10x at the bottom vs the top, though the
bottom faces LESS absolute variance — the double penalty: least
capacity meets highest elasticity.
(iii) Level-total loss concentrates at the bottom: workers bear 93.4%
of all agency destroyed in the cascade.
(iv) Broadcast multiplication: each residual unit is duplicated b^(Δl)
times as it descends; imposition narrows upward, multiplies downward.
Origin: Aaron's coinage + boundedness rebuttal (2026-08-15). Script:
code/imposition_cascade_T17.py. Chapter impact: Ch 13 candidate section;
Ch 7 cross-reference. Shapes robust to parameter variation; constants
carry passports only.


## T18 (The mistake-budget gate). [EXACT — derivation below; verified by brute force, 196 worlds]
With asymmetric error costs (acting against the surroundings and being
wrong costs kappa times acting with them and being wrong), an agent that
minimizes expected loss has its education gate at
    e*(kappa) / (1 - e*(kappa)) = kappa(1-s)/s + (kappa-1)(1 - 1/n),
recovering T5 exactly at kappa=1 and rising monotonically in kappa and
(for kappa > 1) in n.
Derivation: on a disagreement the posterior weights on (what E names,
what K names, neither) are proportional to (1 + n(1-s)/s, 1 + n e/(1-e),
n - 2). Follow K iff kappa*(w_E + r) < w_K + r, i.e.
e/(1-e) > kappa(1-s)/s + (kappa-1)(1 - 1/n).
Reference values (s=0.5): kappa=1 -> 0.50 at every n; kappa=3 -> 0.800
(n=2), 0.826 (n=8); kappa=10 -> 0.9355 (n=2), 0.9437 (n=4), 0.9470 (n=8),
0.9496 (n=64), limit 0.95.

CORRECTION 2026-11-25 (found while building web/calculator.html; in the
book from v0.47). Until this date the entry read
e*(kappa) = kappa(1-s)/(s + kappa(1-s)), with 0.909 at kappa=10, tagged
EXACT and "verified". Two slips. (a) The derivation took "rational
defection iff posterior odds exceed kappa", which is the loss comparison
only when there are two options: with more, the case where BOTH sources
are wrong costs the conformist 1 and the defector kappa, and it does not
cancel. (b) It then dropped the +1 terms of the two likelihood ratios,
which cancel only at kappa=1. The printed formula is the corrected one
without its (kappa-1)(1-1/n) term. (c) The script's "numeric" column
evaluated the same inequality the formula came from, so it could not
have disagreed. code/mistake_budget_T18.py now builds the exact
posterior for every observation pair, minimizes expected loss, and
bisects for the gate; the corrected closed form agrees to 1e-15 over
n = 2..64, s = 0.2..0.7, kappa = 1..20. Direction of every consequence
below is unchanged; the gate is higher than was printed. The book does
not mention the earlier formula (Aaron, 2026-11-25).
D5 RECOMPUTED the same day (code/mistake_ratio_noisy_self_knowledge.py;
output in code/results/). The two older runs (A5 in
code/rig/adversary_2026-10-24.py, R5 in code/rig/adversary_round2.py)
labelled each threshold by the uncorrected formula and scored accuracy
on disagreements only, as if there were two options. The recomputation
uses the corrected gate and the exact accuracy for n options (a person
who acts on their own knowledge is right e + (1-e)/n of the time; one
who conforms, (1-s) + s/n), with the population as a density, no
sampling. At n = 2, 8, 64: population at its gate -> kappa* between 0.98
and 1.04 for noise up to 0.10 (drifting to about 2.2 in a clear world,
s = 0.3, and 0.8 in a noisy one, s = 0.7, at noise 0.30); population
above its gate -> kappa* < 1 in 12 of 12 cells; population below its
gate -> kappa* > 1 in 12 of 12 cells and at the top of the search grid
(nobody acts) in every world at noise 0.30. D5 stands as worded.
Consequences: (i) poverty welds gates through ERROR PRICES, not
only knowledge — a person above the T5 gate can remain rationally
conformist for want of a mistake budget; (ii) mistake budgets are a
stealable resource (zero-buffer scheduling, just-in-time lives = theft
of slack); (iii) purchased mistake budgets at the top (bailouts,
too-big-to-fail) are the premium tier of the right to err — premium
rights' most concrete instance. Origin: Aaron's note ("people need
environments that permit mistakes"), 2026-08-15. Script:
code/mistake_budget_T18.py. Impact: Ch 5 extension owed; Ch 13/14
cross-references owed; LEXICON entry: mistake budget.


## R4 — Theorem 6's plateau edge. [REFUTED — kept] (2026-10-24)
Claim as printed: plateau ends at c₀ = competence(λ*) of the λ-family
(0.016 / 0.052 / 0.138 at s = 0.3 / 0.5 / 0.7, n = 6). Refuted by explicit
construction: act A = F when F ≠ E; when F = E play a = e w.p. q and the
rest uniformly; uniform p(a|e) forces q = λ* = 1/(n(1−s)+s). Then δ_A = 1
exactly and aim = c₀′ = 1 − h_n(s + (1−s)/n)/log₂ n  (= 0.097 / 0.247 /
0.462). Equivalently c₀′(s) = 1 − δ_sage(1−s). Numerical search over the
uniform-margin polytope (SLSQP, seeded) finds asymmetric coding policies
further out (0.277 at n=6, s=0.5; feasible to 1e-14). Why missed: SPSA on
softmax, 6 restarts (frontier_attack.py) vs. vertex-seeking constrained
maximization (plateau_edge_T6prime.py). Status: existence PROVEN; c₀′
PROVEN lower bound on edge; exact edge OPEN (crude upper bound 0.56 at
(6, 0.5) from the row cap p(a|f=e,e) ≤ λ*). Water-filling frontier
conjecture REFUTED near δ_A = 1. T9/T11 constants re-scoped: properties of
the λ*-policy only.

## Theorem 19 (Economic hiding theorem — identification). [PROVEN (i,iii,iv,v); NUMERICAL endpoints (ii)]
Choice data = joint law of (A,E). (i) δ_A identified. (ii) aim ranges over
[aim_min(P), aim_max(P)]: noise reading vs. payload reading; feasible set
is a polytope, I(A;F) convex in the channel, max at a vertex. (iii) Exact
witnesses: uniform P ← scatter (0) and plateau policy (c₀′ = 0.247;
0.277 numerical); P = ½·rule + ½·uniform ← Tomas/Nadia mixture (0.069)
and the SAGE (1.000) identically. (iv) logit RUM with u = log p
rationalizes any full-support P exactly; logsum identical across the
interval. (v) recording F collapses the interval. Table (n=6, s=0.5):
μ=1: δ 0.000, aim pinned 0.247 | μ=.9: δ .235, [.203, ≥.322] | μ=.75:
δ .473, [.146, ≥.515] | μ=.5: δ .753, [.069, 1.000 exact] | μ=.25:
δ .931, [.019, ≥.527] | μ=.1: δ .988, [.003, ≥.346] | μ=0: δ 1,
[0, ≥.277]. Script: code/hiding_theorem_econ.py. Congruence (resonance
only): the fringe/torus structure of arXiv:2608.18886. Field: panels
linking actions to later outcomes are the instrument.

## Proposition 13.1 (Goodhart immunity of the two-ruler ledger). [PROVEN (i,ii,iv); EXACT on class (iii)]
A′ = h(A,E,N), N ⟂ F | (A,E). (i) I(A′;F) ≤ I(A,E;F) (DPI). (ii) (A′,E)
feasible ⇒ on/inside frontier. (iii) E-independent noise traces the
mixing family, strictly inside (mixing-sage refutation; far inside near
δ=1 by R4). (iv) no Pareto improvement without future-information.
Attack surface (printed): definitions of F and E. Rule: F recorded by
someone the audited party does not pay.


## T9′ — Surveillance inversion on the wider plateau. [EXACT, same coin model as T9] (2026-10-24)
δ_A({E,R}) under full coin capture (inverse-CDF realization, m = 64):
λ*-policy 0.291 (T9 replicated; ρ* = 0.348); hand plateau policy (c₀′)
0.653 (ρ* = 0.711); asymmetric SLSQP policy (0.277) 0.545 (ρ* = 0.542).
Sage ceiling 0.753. Inversion SURVIVES on the wider plateau but weakens:
the coin share a watcher must capture roughly doubles. Mechanism: those
policies route most of their unpredictability through F (acting on the
future where E is wrong), which a watcher who holds R still lacks.
"Chance spent where the world is wrong is chance the watcher cannot
buy." OPEN: the general law relating a hidden policy's coin-dependence
to its surveillance floor. Script: code/surveillance_T9_wider_plateau.py.

## Frontier re-attack (polytope method). [EXACT points; LOWER BOUNDS] (2026-10-24)
Fix p(a|e), maximize I(A;F) over consistent policies (SLSQP, seeded with
noise/sage/hand policies); every returned point is a feasible policy.
Hidden side (δ_A ≥ 0.753), n=6, s=0.5: δ 0.753 → 1.000 (sage, exact);
0.797 → ≥0.858; 0.854 → ≥0.705; 0.931 → ≥0.527 (two families agree);
0.981 → ≥0.367; 0.988 → ≥0.346; 0.997 → ≥0.294; 1.000 → ≥0.277.
First printing's curve (mixing-sage/water-filling) lies below every
point; e.g. 0.247 vs ≥0.527 at δ = 0.931. Legible side: reachable points
only (δ 0.235 → ≥0.322; 0.473 → ≥0.515), no bound claimed. Exact
frontier remains OPEN. Scripts: code/frontier_polytope_attack.py,
code/figure_plane_and_frontier_v2.py; data figures/frontier_certified_points.npy.


## Theorem 9′ (The surveillance sandwich). [PROVEN] (2026-10-24)
A = g(F,E,R) with R ⟂ F | E. Then I(A;F|E) ≤ H(A|E,R) ≤ H(F|E).
Proof. Upper: H(A|E,R) ≤ H(F|E,R) = H(F|E). Lower: A deterministic given
(F,E,R) ⇒ H(A|E,R) = I(A;F|E,R) = I(A,R;F|E) − I(R;F|E) = I(A,R;F|E) ≥
I(A;F|E). ∎  Equality (upper) iff A ↔ F bijective given (E,R).
Consequences: T9's inversion is UNIVERSAL (weak form) — no fully
surveilled agent is less readable than the sage; the surveilled floor is
bounded below by the policy's conditional future-information (the
coin-dependence law). Check (n=6, s=0.5): λ*-policy 0.088 ≤ 0.291 ≤
0.753; hand 0.431 ≤ 0.653; asymmetric 0.450 ≤ 0.545; sage 0.753 = 0.753;
rock 0 = 0. Script: inline in session log; sandwich check in
code/wirings_T11_wider_plateau.py (lower wall).

## T11′ — Two wirings on the wider plateau. [EXACT floors] (2026-10-24)
n=4, s=0.5, m_S=8. λ*-policy (replication): gated h=0..3: 0.338, 0.453,
0.485, 0.474; additive: 0.338, 0.753, 0.960, 0.978 (seed-unknown 0.984).
Hand plateau policy (aim 0.226): gated 0.622, 0.667, 0.700, 0.697 — all
below sage 0.774; additive 0.622, 0.851, 0.973, 0.984 = seed-unknown at
h=3. Dichotomy shape-invariant; floors lifted by the T9′ lower wall
(I(A;F|E)/log n = 0.399 vs 0.142). Script: code/wirings_T11_wider_plateau.py.

## Theorem 11′ (The dichotomy, hardened). [EXACT; 3,372 wirings] (2026-10-24 sweep; integrated 2026-11-08)
(i) One-time-pad law: for the printed additive wiring, δ_∞ = δ₀ exactly iff m_S | m_U (h ≥ log₂ m_S); proof: the quantile set {(S+½)/m_S + (U+½)/m_U mod 1} is the same grid for every S. Verified 0/48 failures; gap δ₀−δ_∞ shrinks continuously below the point (m_S=64: 0.010 at h=3, 0.003 at h=4, 0 at h=6).
(ii) Reach law: for the span family cell(S,U) = (S + U·d) mod M, the seed-known floor depends on (n, s, policy, h) and reach = (d(m_U−1)+1)/M only; identical to 4 decimals across m_S at equal reach (36 groups); non-decreasing in reach (175/180; exceptions the h=1 full-wrap edge). Random wirings sit near the additive end (hand, h=3, m_S=1024: 0.948 vs gated 0.629 / additive 0.992).
(iii) R5 — gated inversion margin on the wider plateau (hand policy): sage − floor = +0.020 (4,0.3), +0.074 (4,0.5), +0.084 (4,0.7), **−0.026 (6,0.3)**, +0.017 (6,0.5), +0.067 (6,0.7); λ* margins 0.19–0.39. REFUTED in one world of six; corpse kept. Condition (descriptive, not yet a theorem): inversion holds where wall/sage is small.
Code: code/rig/wiring_hardening_exact.py; results code/rig/results_exact/.

## Theorem 20 (The inversion costs no theory). [EXACT floors; learned to 3 decimals, 72/72] (2026-11-08)
Neural-watcher tournament (tier A; 10.9 GPU-h total with tier R): GRU (795k params) and causal transformer (1.8M) trained from scratch on unlimited fresh lifetimes, never told wiring/habit space, reach the exact seed-known floor: max |learned − exact| 0.008, mean 0.001; within 0.02 of the floor by day 5–10 (exact Bayesian: 7–10). Frequency miner (A | today's E): within 0.015–0.022 by day ~100. Gated inversion achieved by exact watcher 28/28 and learned 28/28. Habit space m_S=1024 gives LOWER floors than 8 (gated hand 0.629 vs 0.700; λ* 0.363 vs 0.474) and faster convergence (7 d vs 9–10). Wrong-wiring Bayesian (ε=1e-3 hedge) reads worse than ignorance in 52/72 (0.83–1.56).
Code: code/rig/watcher_tournament.py; code/rig/results/.

## Result R6 (The pad is a race; T11(iv) extended). [SIMULATION; existence] (2026-11-08)
Additive wiring, m_S=8, h=3, T=512, coin replaced by an LCG with k hidden bits (same marginals). Floors (λ*/hand): fresh 0.978/0.984 all watchers. k=8: GRU 0.343/0.812, TF 0.349/0.589 (drop below the fresh-coin Bayesian at day 5–7 λ*, 40–64 hand). k=12: GRU 0.359/0.795 (day 12/35), TF no gain. k=16: GRU 0.898 (λ*, day 24). k=32: no gain. Fresh-coin Bayesian never moves (0.978/0.984). Gated wiring: cracking buys ≤ 0.07. One seed per config; LCG family only.
Reading: a coin is fresh only relative to a watcher; the protection of the one-time pad lasts while the generator's hidden state exceeds what the watcher can acquire in a lifetime (between 12 and 32 bits at this budget).

## Definitions sharpened by adversarial review (2026-10-24, integrated 2026-11-08)
D1 Theft = displacement by taking a resource, weakly Pareto-inward (no reachable position improves, one worsens). Legibility = reshaping = rivalry (Ch 10), entered on the ledger, not theft. A dictate (κ→∞ on the task plane, T18) is a taking for the hours it governs; a prompt is information.
D2 F is exogenous to A on every plane; audit column = realized exogenous state outside the audited party's control; second audit rule: F must not be manufacturable from A (the treadmill gaming).
D3 T13 is about readings, not dispatch; acting→reading link = CONJECTURE (Ch 15). Famine-metric crossover: independence beats the 0.80 hub iff right-ground acc ≳ 0.63.
D4 T17 prices uncertainty (broadcast under proportional shocks; hours partition); 93.4% is the un-tiered-pool regime; tiering dominates on the T16 gate (Ch 14 rule 7).
D5 T18 boundary: κ* (per-decision accuracy, noisy self-knowledge) ≈ 1 at the gate, < 1 above, → ∞ below; accuracy ≠ survival (Lesson 2). [Recomputed 2026-11-25 with the corrected T18: code/mistake_ratio_noisy_self_knowledge.py. Holds as worded.]
D6 Ledger symmetry: a firm's agency is on the same books; only elasticity × headcount decides net; the audit log extracts the firm's model (T11) and that displacement is recorded.

## Theorem 5c (The gate for any environment). [PROVEN] (2026-11-08)
Model as T5: K = F w.p. e, else uniform. For an arbitrary channel C_E, observed signal e with
posterior q(e,·); q_max = max_f q(e,f) (the environment's pick), q_k = q(e,k) for the future k the
agent's knowledge names. Bayes: follow K iff q_k (e + (1−e)/n) > q_max (1−e)/n  ⟺  e > e*(e,k) =
(q_max − q_k)/(q_max + (n−1) q_k). Symmetric channel: q_max = 1−s+s/n, q_k = s/n ⇒ e* = 1−s.
Verified: 215,450 Bayesian decisions on 300 random channels (n ∈ 3..8, Dirichlet rows), 0 violations.
Closes Ch 15 §2 "the gate, generalized". Code: inline check in session log; to be added to
code/verify_theorems.py.

## Theorem 11′(iv) (Fine-habit inversion). [PROVEN; EXACT] (2026-11-08)
Gated wiring: rfrac ∈ [S/m_S, (S+1)/m_S). As m_S → ∞ the cell lies within one quantile bin of
cdf[f,e,·] for all (f,e) except a vanishing set of S, so A = a(F,E,S) deterministically ⇒
H(A|E=e,S) = H(a(F,e,S)|E=e) ≤ H(F|E=e) (data processing), strict unless f ↦ a(f,e,S) is injective.
Hence the gated floor converges (in m_S) to a value independent of h, equal to the h=0 floor, and
≤ sage. EXACT: at m_S=1024 the gated floor varies by ≤ 0.0015 across h ∈ 0..4 in every (n,s,policy);
no gated floor exceeds the sage at m_S ≥ 64 anywhere in the 3,372-config sweep. R5's failure
(6,0.3,hand) is m_S = 8 only: floors 0.46/0.528/0.564 (h=0/1/≥2) vs 0.457/0.457/0.463 at m_S=64 and
0.457/0.458/0.458 at 1024 (sage 0.538). The "condition" in T11′(iii) is thereby a theorem: the
inversion is universal for fine habits at every h.

## Plateau edge — numerical lower bound raised (2026-11-08)
Edge = max aim s.t. P(A|E) uniform. With A uniform, aim = 1 − H(A|F)/log n and H(A|F) is concave in
pol ⇒ minimum at a vertex of the polytope {pol ≥ 0, rows sum to 1, Σ_f q(e,f) pol[f,e,a] = 1/n}.
Successive linearization from random LP vertices (code/rig/plateau_edge_vertex_search.py):
(6,0.5): 0.334841 (support 54/216; <0.1% of 127,330 restarts; median local vertex 0.302);
(4,0.5): 0.310536 (support 24/64; 14.5% of 64,494 restarts; median 0.291). Previous: c₀′ 0.2467/0.2256 closed
form; 0.277 numerical (6,0.5). Upper bound unchanged (0.56 crude). Certified upper bound = open.


## Proposition 13.1, clause (iv) added; closing sentence withdrawn (2026-11-08, round 4)
Counterexample (ChatGPT, reproduced by enumeration): F fair, E = F w.p. 3/4, A = F⊕E, Z ~ Bern(1/8),
B = 1⊕A⊕E⊕Z. δ_A: 0.811 → 0.896; aim: 0 → 0.456; P(match F): 0.50 → 0.125; I(·;F|E)/H(F): 0.811 → 0.353.
A processor that sees E can launder E's future-information into the action column (unconditional aim
rises); it cannot raise I(A;F|E) (data processing given E). Immune audit statistic = the T9′ lower wall.
"No manipulation improves both rulers" holds only on the frontier; interior populations can be moved
toward it.

## Rule 7 corrected (round 4, G3) — tiering vs pooling on the book's time→competence curve
Overt agent (e=0.7, s=0.5), β as time budget, N=20, shortfall split: pooling wins in 11/12 (β0, cut)
settings unpaid (concavity above the gate; Jensen); tiering wins when the pooled cut drags the pool
toward the gate (β0=6, cut=20) or when the tier is compensated to stay above its own gate (all 12).
Rule 7 now conditional: spread above the gate; concentrate-and-pay near it.

## Per-unit vs elasticity (round 4, C5)
dQ/dβ at β=6 vs 20 (e=0.7,s=0.5): 0.03512 vs 0.00018 → ratio 191; elasticity ratio 70.8. "An hour
returned" = per-unit; text says "seventy in proportional terms, nearer two hundred per hour".

## Real-sea pooling (round 4, G5)
Independent 0.7 vs hub 0.8 with k boats on the hub ground: 0.7(1−φ)V > 0.8(1−φ)V/k ⇔ k > 8/7, φ < 1.
With reading cost c: φ* = 1 − c/(V(0.7 − 0.8/k)) (k=9, c=0.05: 0.92; c=0.2: 0.67). Winner-take-all not
required; crowding penalty is; partial pooling is neutral.

## Aggregate gate on asymmetric channels (round 4, C9)
T5c thresholds spread across signals ⇒ population activation vs e is a staircase (largest step ≤ 0.09
on random n=6 channels). Per-decision knife edge travels; aggregate cliff is a symmetric-class property.

## Round 5 corrections (2026-11-08 night; code/rig/adversary_round5.py)
- T13(iii) scoped: best follower count k* vs master accuracy q (readers 0.70, famine 90 d): q=0.80→1,
  0.85→2, 0.90→2, 0.95→3, 0.99→5+ (famine 0.000087 at k≥5).
- Real-sea payoff, eight on the master, ninth deciding, pooling fraction α: U_read = (1−α)·p(q/9 + (1−q))·V
  + α(q + (1−q)p)V/9; U_follow = qV/9. (0.7,0.8): read > follow ∀α (0.202→0.104 vs 0.089). (0.7,0.99):
  follow > read for α < ~0.98. The v0.26 inequality 0.7V > 0.8V/k is withdrawn.
- Plateau (hand) hit rate: 1/n + s(n−1)/n vs captain 1−s+s/n; equal at s=½; plateau below for s<½.
- Menu padding: δ_A' = (H(A|E)+log m)/(log|A|+log m) → 1; aim unchanged. Audit alphabet = consequence classes.
- P13.1(iv) re-scoped: I(A;F|E) is a check (un-inflatable), not a ruler; I(A;F|E) ≤ H(A|E).

## 2026-11-09 — the bandwidth block in general equilibrium (HANK port v0.1; docs/RESULTS_HANK_v0.1.md)
- **H1 (GE transmission) — COMPUTED.** In a standard one-asset HANK (SSJ toolkit layout and calibration)
  the bandwidth channel at quarterly-rescaled v0 knobs cuts asset demand 15% at fixed prices; with bonds in
  fixed supply the equilibrium real rate rises 0.50% → 0.67%/qtr (0.88% under the sophisticated forecast).
  GE transmits the mechanism; it does not wash it out. Dose–response monotone, zero at zero.
- **H2 (forecast condition) — COMPUTED, sign reversal.** The sign of every bandwidth-repair effect on
  saving and hand-to-mouth status depends on whether the household anticipates its own degradation:
  naive (plans as if its level were permanent) → repairs lower HtM (2–4 pp); sophisticated → the time
  transfer does nothing to HtM and stability RAISES it (+0.027) and lowers low-skill wealth. Ruling: naive default (the tunnel is not perceived from inside),
  both printed. A stated condition of the mechanism from now on.
- **P-A′ in GE — holds in GE, fails in PE.** Time transfer beats equal-cost money transfer on
  model-minus-control HtM exit in GE (−0.028 vs −0.017); at fixed prices money wins (−0.030 vs −0.058)
  because cash removes the scarcity drain. Prices decide the ranking of the instruments.
- **P-B in GE — holds on both metrics.** Stability beats the equal-dollar transfer on HtM (−0.016 vs
  +0.001) and on true-β welfare (+0.141 vs +0.033).
- **P-C in GE — holds.** HtM residual after liquidity repair +0.075 (baseline +0.064); half-closed by time
  + stability, fully closed only by removing the drain.
- **P-E (externality) — COMPUTED.** dr*/dS > 0 (0.51% → 0.81%/qtr over S 0 → 2); private optimum of a
  firm's schedule entropy S_priv = 1.055 vs planner's S_soc = 0.916 in the model, 1.055 in the control
  (no wedge without the channel); Pigou tax τ* = 0.57% of the wage bill per unit S; welfare cost of the
  channel −0.42% of consumption at the private optimum.
- **T17 in GE — the cascade is live.** Hours through the middle group's time gate: steady-state bandwidth
  0.70 → 0.34 in one step (PE). Dynamically, a −300 bp expansion that pushes N through the gate has an
  output response 40% above its linearization and HtM relief cut 42%; at −500 bp output nearly doubles the
  linear path. Linearization cannot see any of it (the gate's Jacobian is zero away from the edge).
- **MPC amplification — COMPUTED.** Output response to a −25 bp monetary shock 1.78× the control's on
  impact, 1.58× cumulative: the taxed bottom raises the economy's MPC profile.

## 2026-11-09 — stress campaign, container results (docs/STRESS_CAMPAIGN_v1.0.md)
- **S3 (welfare criterion) — COMPUTED.** Pigou wedge S_priv − S_soc = +0.085 under the book's criterion
  (degraded planner scored at the undegraded discount). Under criteria that honor the shortened horizon as
  preference (state-dependent β_eff, or the household's own V), aggregate welfare RISES monotonically in
  schedule entropy over S ∈ [0, 2]: such a planner subsidizes the drain. The criterion is a premise of the
  Pigou result; printed as one. (hank_welfare_criteria.md)
- **S7 (audit identification) — COMPUTED.** One-worker reduced form of the block, continuous free time,
  gate vs ramp. Size-controlled max-LR test: power to detect a sharp gate 0.99 at N = 3,000 with σ_T = 0.1
  (0.57 at N = 1,000; 0.61 at N = 3,000 with σ_T = 0.2; 1.00 at N ≥ 10,000 for σ_T ≤ 0.2). A ramp of
  half-width 0.25 is read as a gate 0.94 of the time at N = 10,000; half-width 0.5: 0.02. The audit can
  establish threshold-like nonlinearity at survey scale; it cannot certify sharpness finer than ≈ a quarter
  of the free-time range. BIC-based detection fails under measurement error (0.00–0.01 at σ_T = 0.2) and
  should not be the audit's rule. (audit_identification.md)
- **S8 (macro objections) — COMPUTED.** (a) Lucas: the model's monetary transmission relative to the
  control is 1.40 / 1.78 / 1.70 (impact) at S = 0.5 / 1 / 2 — regime-dependent, so a reduced-form MPC does
  not transfer across schedule regimes; the bandwidth constants are policy-invariant by construction, the
  naive forecast is the one behavioral premise a policy could change. (b) HtM measurement: with the
  cutoff at the limit itself (a' ≤ 0.05) the model has LESS hand-to-mouth than the control (−0.081) and P-B
  and P-C reverse; at a band of 0.15 or 0.30 of quarterly mean income the signs are the printed ones. Noise
  moves mass off the exact corner into the band beside it: the HtM results are statements about the band,
  and the book must define hand-to-mouth as a band (as the field does: liquid wealth within a fortnight of
  income) and say so. (c) Five skill states: GE transmission unchanged (r 0.50 → 0.68%/qtr). (d) Ricardian
  equivalence owed to dynamics. (hank_macro_objections.md)
- **S5 (faces of the degraded optimizer) — COMPUTED.** Four faces each alone, each dosed to the default
  model's fixed-price HtM increase (+0.093; the pure-noise face reaches only +0.077 at κ_tax = 0.25):
  noise (= rational inattention, Matějka–McKay) / tunneling / naive present bias / sparse attention.
  Monetary transmission relative to control: 2.00 / 1.79 / 1.44 / 1.22 — every face amplifies. Real-rate
  transmission Δr*: +0.17 / +0.19 / +0.10 / +0.01 pp per quarter; fixed-price asset demand −0.92 / −0.87 /
  −0.49 / −0.08 — the interest-rate result belongs to the faces that touch the discount or the choice noise,
  not to pure attention. Stability beats the equal-dollar transfer on HtM_low under tunneling (−0.016),
  present bias (−0.018) and sparse attention (−0.013), NOT under pure noise (+0.004). True-β welfare loss
  −0.67 / −0.24 / −0.15 / −0.15. (hank_faces_RESULTS.md)
- **S10 (HANK v0.2: own hours, own gate; flexible wage) — COMPUTED.** (i) The sold floor: 91% of low-skill
  households work below their own time gate in the CONTROL economy (income effect), 90% in the model; the
  sophisticated variant collapses (97%/86% below, BW 0.10/0.27, r 1.32%, Y +8.5%) — the sophisticated
  forecast is pathological in this host too. (ii) A time transfer with hours endogenous is KEPT, not sold
  back (Δhours_low +0.005), cuts the below-gate share by 0.15 and raises BW_low +0.04 and welfare, but leaves
  HtM_low unchanged (+0.003); the equal-cost money transfer lowers hours (−0.06), and wins on HtM_low
  (−0.049 model − control). **P-A′ (HtM form) fails with the labor margin**; the time transfer's gains are
  bandwidth and welfare. (iii) A working-time cap (no long shift) costs Y −3% and welfare −1.5 (utility
  units) in both economies with the below-gate share unchanged; a wage subsidy of equal cost raises welfare
  +0.48: prohibition is not the instrument. (iv) **Monetary transmission reverses:** model/control impact
  0.69 (cumulative 0.80) by Jacobian, 0.63 by nonlinear GE path — the ×1.8 amplification belongs to the
  sticky-wage, demand-determined host; with own hours against a flexible wage the taxed economy responds
  LESS, its hours answering the wage more sluggishly. r-transmission unchanged (0.50 → 0.66%/qtr).
  (hank_v02_RESULTS.md)
- **Grid convergence — CHECKED.** Headline GE numbers at (nA, nref) = (120,4)/(160,6)/(200,8): r* 0.0067/0.0066/0.0066;
  ΔHTM_low +0.064/+0.065/+0.065; ΔA(PE) −0.82/−0.83/−0.83; BW 0.703 throughout. (hank_grid_convergence.md)

## 2026-11-09 — stress campaign, rig results (W2, W3, W4)
- **S2-plateau (certified bounds) — COMPUTED.** Rectangular B&B (code/rig/plateau_edge_bnb.py; certificate
  includes tolerance-discarded nodes as of this date). n = 3, s = 0.5: edge = 1 − 1/log₂3 = 0.369070, tree
  exhausted (optimum: each future answered by an even split over two of three actions, H(A|F) = 1 bit).
  n = 4, s = 0.5 (rig, 6 workers, 1 h, 1.98 M nodes): edge ∈ [0.310536, 0.3331 + 0.001 tolerance] — stated as
  ≤ 0.334; incumbent unimproved. The n = 6 vertex (0.334841) sits at or marginally above the n = 4 ceiling:
  the edge is not decreasing in n. NOTE: the earlier "n = 3 closed exactly" statement was made with a
  certificate that ignored tolerance-discarded nodes; rerun with the corrected accounting it closes with
  width 1e-16, so the statement stands.
- **S4 (town under stress) — SIMULATION, 972 towns × 10 doses × 20,000 seasons (rig GPU).** Clean towns
  reproduce T13 (0.073/0.051/0.438 at q = 0.8). One stress at a time, q = 0.8: sea memory — no effect
  (fishers do not use yesterday); reader-error persistence 0.5/0.9 — all-readers famine 0.51/0.65, k* = 3
  (0.26/0.35), bloc 0.44 beats k = 0; shared blindness c = 0.1 — k* = 1 (0.34), c = 0.3 — everything below the
  herd line ≥ 0.945, bloc 0.43 (k* = 5); master slumps ρ_h 0.5/0.9 — one follower no help (0.073/0.102 vs
  0.073/0.076), bloc 0.95/0.81; misdirection 0.1 — k* = 1 barely (0.070 vs 0.077), 0.3 — k* = 0 at every q
  including 0.99 (effective accuracy q(1 − lie) < readers'). Pooled: with no shared blindness and q ≤ 0.9
  the best dose is below the herd line in 240/243 towns (exceptions: q = 0.9, honest, ρ_err = 0.9);
  independence beats the bloc in 100%/93%/78%/52% of c = 0 towns at q = 0.7/0.8/0.9/0.99 and in
  62%/40%/19%/0% at c = 0.3. Structure kept: protection = independent errors; the channel worth following
  is the one whose errors are uncorrelated with the rest.
- **S6 (living town with skill decay) — SIMULATION.** Rig run (216 configs) had a vacuous crowding axis
  (yield normalized away, inherited from living_town_S1.py: payoff 3/k at every Y); rerun in the container
  with per-boat capacity (Y boatloads; Y = 1 strongest crowding, Y = 9 glass sea; 144 configs × 500 runs ×
  600 days; results_living2). Skill fixed point matches mean field p* = [(1−h)μ·0.7 + hλ/4]/[(1−h)μ + hλ].
  Y = 1: hub fraction 0.48 → 0.66, skill 0.70 → 0.27 as λ/μ goes 0 → 10 (a third still "read", at chance).
  Y = 3, μ = 0.005: λ = 0.002 → hub 0.69 (0.75 at 1,500 days), λ ≥ 0.01 → 0.87–0.89, skill ≤ 0.29. Y = 9:
  0.74 → 0.94–0.97. NO HYSTERESIS: broadcast start and readers start reach the same state in all 8 cells
  tested (1,500 days) — the predicted point of no return is refuted; the state is a unique attractor set by
  λ/μ and crowding slack. The loss is invisible to a head count (hub fraction 0.66 with aim ≈ 0).

## 2026-11-09 — read-through corrections (Fable 5.2 pass over v0.28 and the v0.29 draft)
- **Label correction.** The entry above headed "T17 in GE — the cascade is live" is misnamed. T17 is the ledger
  of imposition (uncertainty broadcast down a hierarchy). What the HANK shows is the *time gate* (T16) acting in
  the aggregate: hours crossing a group's free-time threshold. The numbers stand; the name is "gate crossing".
  The book's §5C sentence "Chapter 13's cascade is live" is corrected in v0.29.
- **Nesting claim corrected.** §5C (v0.28) said the control "is the standard one, to the digit". It is the standard
  household on a discretized savings grid with logit smoothing; it converges to the toolkit's EGM household
  (wealth within 1.3%, consumption within 0.1% at k_min = 0.001, nA = 200, nref = 8). v0.29 says so.
- **What the host tests.** §5C (v0.28) said the time gate was placed in the host "unchanged". The host carries a
  reduced form (bandwidth recovers only with free time above a threshold); Theorem 16 itself is not what is tested.
- **Forecast wording.** "Reverses the sign of every repair" (Ch 15 §3, v0.28) becomes "erases or reverses": time
  transfer null, stability reversed, drain removal unaffected.
- **Other fixes in v0.29:** [SIMULATION] label defined in the front matter; Ch 9 §5 no longer calls the decay
  curves the only simulation-assisted results (T20 and R6 are too); Ch 11 §5 garbled "owed" paragraph rewritten;
  lesson three and Ch 14 rule six carry the stress conditions; Ch 14 §5C cites the time gate as Chapter 7's (not 5's);
  Gilens–Page citation flag resolved with its critics (Bashir 2015; Enns 2015; Branham, Soroka, Wlezien 2017);
  Coda links eight and nine updated; Appendix D names the HANK ancestors; Appendix E points to PAPER_SYNC v0.23;
  Appendix G (the stress record) added.

## 2026-11-09 (evening) — S1, the sign-stability map (rig W1; code/rig/hank_port/results_sweep_fast)
- **S1 — COMPUTED.** 400 random economies over the box in sweep_signs.py (fast grid nA = 80, nref = 3); 331 solved,
  69 did not (GE solver non-convergence; two thirds of the failures naive, half at EIS 1) and are absent from every count.
  **Hold in 331/331:** asset demand falls at fixed prices; r rises in GE; half dose gives less. **329/331:** more
  schedule entropy raises r (243/243 naive). **242/243 naive:** stability beats the equal-dollar transfer on true-β
  welfare (69/88 sophisticated). **Conditional (naive):** HtM_low higher in the model 72%; P-C residual > 0 71%;
  stability beats transfer on HtM 61%; time beats money on HtM (GE) 39%. By curvature: EIS 0.5 → 98% / 99% / 86% / 67%;
  EIS 1 → 50% / 47% / 40% / 16%, rising to 82% / 80% / 80% / 41% in the top third of tunnel-to-noise ratio. Failures load
  on EIS (+1.0–1.3 sd) and k_tax (+0.6–0.75 sd). Reading: the horizon face pulls households to the limit, the noise face
  scatters them off it; HtM counts report which is winning. Median Δr* = +0.84 pp/yr (naive +0.73). The sophisticated
  household: transmission 88/88; stability beats transfer on HtM in 12%.
- **Town stress, even comparison (correction to the S4 entry).** "Bloc beats zero followers under persistent reader
  errors" holds only when the master is exempt from the persistence: with ρ_err = ρ_h = 0.5 the town reads 0.516 /
  0.444 (k* = 1) / 0.948 (all-read / best / bloc); at 0.9/0.9: 0.646 / 0.593 / 0.812. The book's ordering returns.

## 2026-11-09 (night) — S9 two-asset host; own-hours dynamics; citation check
- **S9 (two-asset host) — COMPUTED** (code/rig/hank_port/bw_two_asset.py, run_two_asset.py; fixed returns r_a = 0.5%,
  r_k = 1.5%/qtr; fixed fee 0.02 + proportional 0.02 on the illiquid account; control β = 0.9746 calibrated to liquid
  assets 1.04; nA = 50, nK = 12, naive). Levels control → model: liquid 1.040 → 0.889 (−15%); illiquid 5.81 → 4.53
  (−22%); HtM 0.448 → 0.469; wealthy HtM 0.263 → 0.182; poor HtM 0.185 → 0.287; HtM_low 0.576 → 0.696. Faces:
  horizon only K = 4.74, noise only K = 5.60. Dose monotone (K 5.02 / 4.53 / 4.18 at 0.5 / 1 / 1.5). Liquid rate
  clearing the liquid market: 0.50% → 0.90%/qtr (+1.6 pp/yr). P-C: HtM_low residual +0.120 → +0.158 after the
  borrowing limit opens. Time transfer: HtM_low −0.029 (control +0.002), K_low +0.08. Stability: −0.017 (control
  +0.001), K_low +0.07. Money (equal cost to time): HtM_low +0.108 (control +0.159), K_low −0.51, ΔWELF_low
  model − control +1.25 vs time +0.55. Transfer equal to stability's cost: ΔWELF +0.44 vs stability +0.28.
  **So: balance-sheet composition and wealth respond robustly; P-C holds; stability/time beat cash on balance
  sheets; cash beats them on welfare at fixed returns — the one-asset welfare ranking (S1: 242/243) is host- and
  GE-specific.** No drain → identical to control.
- **Own-hours host, dynamics (S10 addendum).** Linear: model/control cumulative ΔY 0.80. Nonlinear cumulative ΔY,
  control vs model: −100 bp 0.0501 vs 0.0507 (ratio 1.01); −300 bp 0.2113 vs 0.2550 (ratio 1.21). Each economy's
  departure from its own linearization: control ×1.24 / ×1.74, model ×1.56 / ×2.62 — mostly the lumpy hours choice
  both share. Entropy shock (S +0.5, AR 0.9): control none; model BW −2.4% at 12 quarters, output −0.17% on impact.
- **Bounded fallback solver validated** on an unsolved sweep economy (draw 14: β = 0.9914, r_max = 0.87%;
  control r = 0.500%, model r = 0.530%).
- **Citation check (web, 2026-11-09).** Enns 2015 PoP 13(4):1053–1064; Gilens 2015 PoP 13(4):1065–1071 ("coincident
  beneficiaries"; influence distinct from match); Bashir 2015 Research & Politics 2(4); Branham–Soroka–Wlezien 2017
  PSQ (≈90% agreement; rich prevail 53% when they part — confirmed from a summary page, not the journal). Mas–Pallais
  2017 AER: 20% of wages to avoid employer-set schedule on a week's notice, which "largely represents workers'
  aversion to evening and weekend work, not scheduling unpredictability" — the book's earlier use overstated it;
  compensating-differential estimates "unstable ... and often wrong-signed". Golden 2015 (EPI Briefing Paper 394):
  irregular/on-call shifts 11% in the lowest income bracket vs 6–9% above (top bracket 9%: not monotone).

## 2026-11-10 — night-run results (N1–N4), the public-signal window, the field column
- **S1′ — sign map at 800 draws, COMPUTED** (rig, `hank_port/results_sweep_fast/`, bounded fallback solver; 688 solved,
  112 did not — unsolved draws load on low income risk σ_s (−1.1 sd), high debt B (+0.6 sd), high persistence ρ_s
  (+0.6 sd), not on the bandwidth constants). **688/688:** asset demand falls at fixed prices; r rises in GE; half dose
  gives less. **683/688:** more schedule entropy raises r (526/526 naive; the 5 failures are sophisticated, each within
  2e-4/qtr of zero). **524/526 naive:** stability beats the equal-cost wage transfer on true-β welfare (120/162
  sophisticated); the two naive failures have high income risk and low debt. **Conditional (naive, n = 526):** HtM_low
  higher 74.5%; P-C residual > 0 73.8%; stability beats transfer on HtM 63.9%; time beats money on HtM (GE) 42.2%.
  By curvature (naive): EIS 0.5 (n = 256) → 97.3% / 98.0% / 87.5% / 68.4%; log utility (n = 270) → 53.0% / 50.7% /
  41.5% / 17.4%; log utility split at the median tunnel-to-noise ratio: above → 73% / 70% / 69% / 33%; below → 33% /
  31% / 14% / 1.5%. Median Δr* = +0.81 pp/yr (5–95%: +0.16 to +3.5). The 331-draw map (S1) is confirmed at twice the
  sample; no claim changes category.
- **Plateau edge, n = 4 — CLOSED TO 2e-4** (rig, 6 h × 8 workers, 4.03 M nodes, certificate counts tolerance-discarded
  nodes): edge(4, 0.5) ∈ [0.310536, 0.310736]. With edge(3, 0.5) = 1 − 1/log₂3 = 0.369070 (closed) and the n = 6 vertex
  at 0.334841 (a lower bound): **the edge is not monotone in the number of futures** — it falls from three to four and
  is higher again by six. n = 6 certified interval after 6 h × 8 workers (8.87 M nodes): [0.334841, 0.641173] — the
  rectangular bound does not bite at n = 6 (worse than the crude 0.56); a different relaxation is needed. The earlier
  line "the edge is not falling as futures are added" is corrected to "not monotone".
- **S11 — The public-signal window (PROVEN, elementary; simulation agrees to three digits).** Town of Chapter 11
  (N boats reading independently at accuracy p; good day = at least m boats on the fish). Add a PUBLIC signal of
  accuracy a (here: yesterday's ground, a = ρ_G + (1 − ρ_G)/n_G). (i) A Bayesian reader whose own reading disagrees
  with the public signal follows the public signal iff a > p [posterior odds a(1−p) vs (1−a)p]. (ii) When it does,
  every reader goes where the signal points: the town is one head of accuracy a, bad-day probability 1 − a. (iii) The
  reading town's bad-day probability is P(Bin(N, p) < m). **Hence for p < a < 1 − P(Bin(N, p) < m) each boat is right
  more often than before and the town is hungry more often than before.** At N = 9, m = 5, p = 0.7: the window is
  0.70 < a < 0.9012 (ρ_G between 0.600 and 0.868); famine (three bad days running in ninety) jumps from 7.4% to 83% as
  the signal crosses the reader's own accuracy and is back to 7.4% only at a = 0.901. Exact run probabilities: 55.3% at
  ρ_G = 0.7, 3.4% at 0.9; simulated (N4, 20,000 seasons): 55.6%, 3.3%. Windows at other p: (0.6, 0.733), (0.8, 0.980),
  (0.9, 0.9991). No master, no lie, no error correlation assumed: the correlation is manufactured by each boat's correct
  use of a signal everyone can see. *Ancestors, in the spirit of, with the difference stated:* Condorcet's jury theorem
  (the upper edge of the window is the jury's accuracy); Banerjee 1992 and Bikhchandani–Hirshleifer–Welch 1992 (cascades
  form by watching others' ACTIONS in sequence — here nobody watches anybody); Morris–Shin 2002 (public information
  can lower welfare under strategic complementarity — here boats are strategic substitutes only through the day's
  threshold, and each would follow the signal with or without the others).
- **S12 — A master who misdirects when it pays (COMPUTED, N4).** Master announces a wrong ground whenever his
  following exceeds Yc boats. Famine is 100% at every dose above Yc and unchanged at every dose at or below it; the
  best dose is min(k*, Yc). So the insurance a town can buy from a master is capped by the size at which misdirection
  starts to pay him: with fresh reader errors the cap rarely binds (k* = 1–2 at q ≤ 0.9); with readers' bad weeks
  (ρ_err = 0.5) the town wants k* = 3–8 and Yc = 2 leaves famine at 28% / 18% / 11% (q = 0.8 / 0.9 / 0.99) against
  25% / 6% / 0% with an honest master. The towns that need a center most are the ones that can least afford his price.
- **N4, memory under the other stresses.** In the window (ρ_G = 0.7) every arrangement of readers is at 55% and only a
  following of an accurate honest master helps (q = 0.99: 0%); with Yc = 2 or 4 nothing does (55%). Above the window
  (ρ_G = 0.9) memory gives 3% under every other stress including bad weeks — a steady sea makes the public signal
  better than the jury.
- **Plateau edge, closed forms and the sawtooth (2026-11-10, container).** The n = 4 incumbent is exact arithmetic:
  one future answered (5/8, 1/4, 1/8), three answered (1/2, 3/8, 1/8); H(A|F) = 35/16 − (5/32) log₂5 − (9/32) log₂3;
  **edge(4, ½) ≥ (5 log₂5 + 9 log₂3 − 6)/64 = 0.310536**, certified ≤ 0.310736. n = 5 vertex search (40,000 restarts,
  best recurs in 3.5%): four futures answered (1/2, 3/10, 1/5), one answered (2/5, 2/5, 1/5): **edge(5, ½) ≥ 0.357101**.
  n = 7 (36,653 restarts, best found once): ≥ 0.359125. Floors by n = 3..7: 0.3691 (exact), 0.3105 (to 2e-4), 0.3571,
  0.3348, 0.3591. Certain: edge(4) < edge(3) and edge(4) < edge(5). Suggested, not proven: odd counts above even
  (at s = ½ the grid of attainable answer-probabilities is 1/(2n), and even splits are available to odd n).
- **#8(d) Ricardian equivalence in dynamics — COMPUTED** (`hank_port/ricardian.py`, `results_exact/hank_ricardian.md`;
  linear, sequence-space Jacobians, T = 200). Debt-financed lump-sum tax cut of 1% of annual output, debt retired at
  rate 1 − ρ. First-year consumption per dollar of tax cut, GE, control vs model: ρ = 0.8: 0.063 vs 0.078 (×1.24);
  ρ = 0.95: 0.058 vs 0.076 (×1.29); ρ = 0.99: 0.040 vs 0.057 (×1.43). Fixed prices: impact 0.041 vs 0.029 (×0.70),
  first year 0.040 vs 0.053 (×1.32) at ρ = 0.8. Intertemporal MPCs out of a transfer today: quarter 0 0.072 vs 0.062;
  within a year 0.178 vs 0.193; within three years 0.378 vs 0.390; out of a transfer announced eight quarters ahead,
  spent before arrival: 0.203 in both. **Reading: both economies are far from Ricardian and most of the departure is
  the incomplete-markets host's; the bandwidth tax adds a quarter to two fifths to the first-year GE response, more
  the longer repayment is deferred (the shortened horizon discounts the later taxes), and LOWERS the impact response
  at fixed prices (decision noise blunts the constrained household's one-for-one spending). The tax cut here is
  apportioned by skill, so it goes mostly to households far from the limit.** The "MPC ×1.8" of H1 is the consumption
  response to a monetary shock's income, not this object; the two are not to be conflated in the book.

## 2026-11-10 — the field column: SHED (descriptive; preregistered out of sample and within person)
Data: Federal Reserve SHED public-use files 2019–2023 (not redistributed). Scripts `code/field/`; outputs
`code/field/results/shed_first_look.md`, `shed_oos_test.md`, `shed_panel_test.md`; preregistrations
`docs/SHED_PREREG_v0.1.md` (written with only 2022–2023 open) and `v0.2` (committed before H4/H5 were computed:
commit f1f4317 precedes the results). NOT theorems and NOT causal; recorded here because the book now cites them.
- **F0 (free look, 2022–2023, 11,503 employees).** Employer-varying share 28.5% → 11.1% lowest → highest household
  income band. Adjusted, vs fixed hours: employer's needs +7.2 strained, +4.9 no 3-month fund, +2.8 cannot pay $400,
  +11.2 bills; own request ≈ 0 on the first three. Exploratory: the gap is absent at ≥ 3 weeks' notice.
- **H1 (control, not variability) — HOLDS out of sample** (2019–2021 pooled, 18,268 employees). employer − own:
  strained +7.5 [+5.0, +9.8]; bills +5.5 [+3.3, +7.7]; $400 +2.4 [+0.7, +4.4]; 3-month fund +1.5 [−1.5, +4.7].
  own − same within ±3 pp on the first three (+0.4, +1.0, −1.2). Each single year: strained and bills exclude zero.
- **H2 (three-week break) — HOLDS out of sample** (2,865 employer-varying with stated notice). Under 3 weeks − 3+
  weeks: strained +10.5 [+6.5, +14.3]; bills +8.9 [+4.8, +12.4]. 3+ weeks − same hours on strained: −2.4 [−6.2, +0.9].
  Not replicated from the free look: "income varies equally under long and short notice" (OOS: +8.3 [+3.2, +13.2]
  more variable under short notice). 2021 alone is weak (strained +6.2 [−2.0, +15.2]).
- **H3 (who bears it) — HOLDS out of sample.** 27.8% → 11.9%, zero adjacent reversals pooled (one in each single year).
- **Coding check:** share not covering $400 with cash or equivalent, all adults: 36.5 / 35.6 / 32.3% vs the published
  37 / 36 / 32% (2019 / 2020 / 2021).
- **H4 (within person) — HOLDS** (4,816 persons, 7,390 adjacent-wave pairs; WLS first differences, person bootstrap).
  ΔE: strained +3.0 [+0.3, +5.7]; bills +6.1 [+3.7, +8.7]. ΔO: −2.5 [−5.5, +0.5]; +2.3 [−0.2, +4.7]. ΔE − ΔO:
  +5.6 [+1.8, +9.0]; +3.8 [+0.7, +7.0]. Both directions right-signed on both outcomes; entering distinguishable
  (+4.3, +5.2), leaving not (−0.7, −3.9). Secondary: $400 −0.5 [−2.6, +1.5]; 3-month fund +1.8 [−1.4, +5.1].
  Unweighted: strained +2.0 [−0.5, +4.5]; bills +5.8 [+3.1, +8.2]. Adding Δ income band changes nothing (+3.0, +6.1).
  Half of those on employer-varied hours in one wave report another type in the next (539 of 1,097).
- **H5 (industry held fixed) — HOLDS** (29,771 employee-waves, 19,426 persons, 24 industry groups; robustness, not
  out of sample). employer − own with industry: strained +6.7 (96% kept); bills +5.9 (92%); $400 +2.5 (91%);
  3-month fund +3.4 (91%).
- **What it supports in the book, and what it does not.** Supports: Ch 13's distinction between variability and who
  controls it; the manager's "priced in" as an auditable claim. Does not measure: time floors, gates, aim, bandwidth,
  wages. Within-person estimates are about half the cross-sectional ones (selection, or misclassification
  attenuating first differences — not separable here). Job changes coincide with schedule changes.

## 2026-11-10 (afternoon) — day-run results (D1, D2) and a correction to the welfare claims
- **D2, plateau at five futures:** edge(5, ½) ∈ [0.357101, 0.468877] after 4 h × 12 workers, 11.36 M nodes. The ceiling is
  above edge(3) = 0.369: whether five sits above or below three is open. The rectangular bound is loose from n = 5 on.
- **S9′ — two-asset sign map, COMPUTED** (rig, `hank_port/results_two_asset/`, 300 drawn, 273 solved; 27 did not converge,
  loading on high income risk, patient households, EIS 0.5). Fixed returns. Among the 182 economies whose control holds
  illiquid wealth K ≥ 1 (one quarter's mean income):
  **182/182** illiquid wealth lower (median ratio 0.76); **182/182** half dose does less; **181/182** wealthy HtM lower;
  **181/182** equal-cost cash lowers low-skill illiquid wealth; **176/182** stability raises it.
  **157/182** liquid wealth lower, and hence the clearing liquid rate higher (corrected count: the first summary searched
  only upward and reported 162/162 "where a crossing exists" — in 25 economies the model holds MORE liquid wealth and the
  rate would be lower). Poor HtM higher 162/182 (115/116 at EIS 0.5; 47/66 log). Head count higher 114/182. P-C residual
  positive 152/182 (114/116; 38/66). Stability lowers low-skill HtM 135/182 (106/116; 29/66).
  Time transfer (fixed dT = 0.25, which clears the gate only when Tbar_low ≥ 1.75 — a design difference from the one-asset
  sweep, where dT was set to clear): where it clears (111), low-skill illiquid wealth rises in 99 and the mechanism's share
  of welfare is positive in 110; where it stops short (71), 2 and 16.
  In the 91 economies with control K < 1 (85% log utility; median control HtM 78%) the signs fail (illiquid lower in
  58/91): logit noise at a floor scatters upward. Printed as the map's edge.
- **CORRECTION — what "welfare" has meant in every instrument ranking (H1 P-B, S1, S9, S10).** Every such number is a
  difference-in-differences: (model gain) − (control gain), i.e. the mechanism's share. On that measure: stability beats
  the equal-cost transfer in 524/526 one-asset naive economies and in 128/182 two-asset ones (72/116 at EIS 0.5; 56/66 log).
  The printed two-asset economy was in the minority; "with two assets cash buys more welfare" is withdrawn as general.
  **In levels — the low-skill household's own true-β value inside the taxed economy, net of the tax that pays for the
  program — cash beats stability in 178/182 and beats time in 181/182 two-asset economies.** One-asset printed economy
  (GE, from `hank_v01_results.json`): cash +1.379; stability −0.074 (gross +0.141, tax −0.216); time −0.684; equal-cost
  money +5.903. Aggregate welfare falls under the stability and time programs at their assumed prices and rises under cash.
  **Cash-equivalent of halving low-skill schedule entropy:** 0.0018 of mean quarterly income per quarter in the one-asset
  printed economy (0.5% of low-skill labor income); two-asset median 0.0026 (5–95%: 0.0007–0.0155). The program was
  priced at 0.02 — an assumed constant; stability returns 9–13 cents of household welfare per dollar at that price and
  beats cash only if it can be delivered for less than its worth. Time transfer where it clears the gate: 11% (median)
  of the gross gain from equal-cost cash; 4% in the one-asset printed economy. The household draws no utility from time.
  **Why the worth is small:** the port values bandwidth only through the consumption–savings plan, and departures from
  the optimal plan are second-order in utility (ancestor: Cochrane 1989, AER 79(3):319–337, verified). Nothing the book
  says about aim, gates or mistake budgets has an entry in a consumption stream. This is a limit of the host and is now
  printed as one (v0.33, Ch 14 §5C). The Pigou result (S_soc < S_priv; −0.42% of consumption) is a level calculation and
  is unaffected, and is itself a small number for the same reason.
- **Re-statement, 2026-11-10 16:00 (Aaron's objection, accepted).** The afternoon correction called the consumption-utility
  score "the household's own ledger". That wording grants the standard ruler's supposition — that a chooser's capacity is
  worth exactly what it adds to consumption, evaluated by a chooser assumed whole — which is the thing the book dissects
  (the structural twin of assuming perfect measurement independence in a test of measurement independence). The port
  relaxed the CHOICE side (noise, shortened horizon) and left the YARDSTICK absolute. Both facts stand and are printed in
  v0.34: on the consumption ruler cash beats stability and time; on the bandwidth ruler (one-asset printed economy, GE,
  low-skill group: baseline 0.30; time 0.65; stability 0.42; cash 0.29–0.30) the order is reversed. Neither "the
  household is better off with stability" nor "better off with cash" is supported; the exchange rate between the two
  rulers is owed. Arm-level bandwidth was not stored in either sweep (only in `hank_v01_results.json`).

## 2026-11-10 (16:30) — the rule about walls; three rulers with one wall removed
- **Rule (Aaron Alai, on the record):** perfect measurement independence, the isolated household and the isolated system are
  facsimiles; isolation is not the null. Adopted as a reading rule in the front matter of v0.35, with its converse: taking a
  wall down does not license asserting the wall's opposite. Audit: `docs/ISOLATION_AUDIT_v1.0.md` (twelve walls taken down
  inside the book and what each had hidden; ten still standing).
- **S13 — three rulers (EXACT arithmetic on one marked supposition; `code/joined_three_rulers.py`).** Households of the printed
  one-asset economy (GE) man Chapter 11's nine boats, drawn from the three skill groups; reader accuracy
  p(b) = 1/4 + (p_top − 1/4) b^γ. Famine at p_top = 0.9, γ = 1: no program 10.7%; time transfer 0.2%; stability 4.3%; cash of
  the time transfer's cost 11.3%; cash of stability's cost 10.8%. Order time > stability > nothing > cash in 9 of 9 versions
  (p_top ∈ {0.8, 0.9, 1}, γ ∈ {0.5, 1, 2}). The order is the bandwidth order passed through a monotone map — it is not
  independent evidence; what the join adds is the amplification and the contrast with the mean. Isolated accounting vs the
  town (a quarter of the population degraded from 0.70): to 0.60 → mean catch −3.6%, famine 7.4% → 17.0% (×2.3); to 0.50 →
  −7.1%, ×4.4; to chance → −16.1%, ×8.8.
- **Transfer lemma (PROVEN, one line):** famine is a threshold on what the fleet finds; a transfer moves catch between holds
  and no boat onto the fish; so no redistribution changes the famine probability except through the readers' accuracy or
  the sameness of their errors.
- **Skill in the macro host is a lottery** (the standard exogenous income process): the host cannot represent talent as
  produced or as scarce. Printed as the host's supposition (v0.35, Ch 14 §5C). The book asserts neither fixed nor equal
  capacity at birth; S3 is its one result on where accuracy comes from.
- **Queued for the rig:** `code/rig/RUN_RULERS.bat` — the 800 economies of the sign map with every program's level welfare
  and bandwidth stored (`sweep_signs.py --out results_sweep_rulers`), summarized on three rulers (`summarize_rulers.py`).

## 2026-11-10 (17:30) — two walls of the audit paid
- **S14 — Two towns with aid (EXACT; `code/two_towns_aid.py`, wall d).** Two Chapter-11 towns; a town sends its surplus over
  five boatloads to the other. Two towns of readers: bad days 9.9% → 3.5%, famine 7.40% → 0.35% (×21). Each town wholly
  behind its OWN master (q = 0.8): 43.9% → 43.9% — aid buys nothing, because a herd fails all at once and a neighbor's whole
  surplus (four boatloads) cannot replace five. Both behind ONE master: nothing. Intermediate doses: with three followers
  per town, own masters 14.0% → 0.6%, one master 14.0% → 9.7%. **A transfer is worth what the sameness between giver and
  receiver leaves it: nothing inside one town on a bad day (transfer lemma), almost everything between towns whose errors
  are their own, nothing between towns that follow one voice.** Cash (insurance) and independence are complements.
- **S15 — Who is on call: by lot or sold (`code/duty_trade_exact.py`, wall g; skill dynamics of S3 at their mean; famine and
  mean catch exact given accuracies). EXPECTATION REFUTED — KEPT.** k of nine boats on call each day; on call, the day's
  reading is degraded (d) and skill fades (λ); reading restores it (μ). LOT = fresh draw daily; TRADE = the same k boats,
  paid. Across 48 cases (p_max 0.7/0.8; k 1–4; d 0.5/1; λ/μ 0.25/1/4): **the trade is better for the town in 40** (higher
  mean catch AND lower famine): spreading the burden degrades every boat's skill, concentrating it keeps the rest whole.
  The lot is better on both counts in 8 — exactly where skill fades more slowly than it returns (λ/μ = 0.25) and an
  on-call day is only half lost (d = 0.5). **In no case does the trade raise the mean catch while raising famine**: the
  expected region "every party made whole, town starves more" is empty in this model. Rule: total skill kept, lot vs trade,
  is μ / ((1−f) μ + f λ) — above one iff λ < μ. What the model does not score: the sellers end at chance permanently (a
  class with no reading skill), which S3 says is recoverable and the town's famine metric does not count; and the buyer
  always gains on his own ledger, so in the 8 lot-better cases the trade is wanted by buyers though it cannot make
  sellers whole — it can happen there only by imposition or by a seller's need.
- Rig: `code/rig/RUN_TWOASSET_RULERS.bat` (300 two-asset economies storing every program's bandwidth by skill group;
  `summarize_two_asset_rulers.py`).

## 2026-11-10 (20:00) — cover-to-cover read of v0.36; v0.37
Record in `docs/READTHROUGH_2026-11-10.md`: ten localized edits applied (model constants quoted as the world's; "has been measured" →
"has been given a measure"; "every single-ruler measure ever proposed"; the machinery was told what to count; undefined "walls"
vocabulary; S14 and S15 entered in Chapter 15's list), five judgment calls left to Aaron (J1 Part V's untagged "law"; J2 Chapter 2's
"the only one"; J3 "nothing about human nature was assumed"; J4 "no opinions required"; J5 the density of §5C), three isolations
added to the audit (k, l, m).

## 2026-11-12 — rig results R1/T1; Theorems 22 and 23; evidence that closes "owed" items; v0.38
- **R1 — three scores across the one-asset economies (528 naive of 691 solved; `hank_port/results_sweep_rulers/`).** Equal cost,
  taxed economy, GE. Stability beats cash: on low-skill lifetime consumption value **0/528**; on low-skill bandwidth **527/528**;
  on the joined town's famine **527/528**. Time beats cash: **0/528**; 523/528; 514/528. The survival order is stable across the
  nine versions of the join (0.964–0.998). Stability and time each LOWER the low-skill household's consumption value net of their
  assumed price in most economies (stability raises it in 138/528; time in 71/528); cash raises it in 528/528. Cash raises
  low-skill bandwidth by more than 0.01 in 11/528 (small) and 71/528 (large). Cash-equivalent of halving low-skill schedule
  entropy on the consumption score: median 0.0028 of mean quarterly income (5–95%: 0.0007–0.0075).
- **T1 — the same in the two-asset host (182 economies with illiquid wealth; `results_two_asset_rulers/`).** Stability beats cash:
  consumption 4/182; bandwidth 181/182; survival 181/182. Time beats cash: 1/182; 151/182; 151/182 (the fixed-size time transfer
  stops short of the gate in 71 economies).
- **Theorem 22 — the borrowed record (EXACT; `code/borrowed_record.py`).** Days plain (1−h) or hard (h). Reader right p_e / p_h; one
  voice right q_e / q_h. One tally per voice: record a = (1−h)q_e + h q_h vs p = (1−h)p_e + h p_h; followed iff a > p. Printed town
  (h 0.3; p_e 0.9, p_h 0.55; q_e 1, q_h 0.5): record 85.0% vs 79.5%; bad days reading 11.4% vs following 15.0%; famine 11.0% →
  22.5%; plain-day majority already right 99.91%; two tallies (follow on plain days only) 10.9%. Dose curve monotone worse from the
  first follower (12.0% at one). Grid of 450 worlds: followed-and-harmful in 185; followed while worse than each single reader on
  hard days in 195; both in 160. Standing: with a hard day's outcome recorded w.p. v, a reputation for never being wrong lasts
  1/(h v (1−q_h)) days (7 at v = 1; 667 = 7.4 seasons at v = 0.01); at odds 99:1 on "right 95% of hard days", ln 99/(h v KL)
  (18 days; 1,845 days). Gate beside him sits at his record (0.85), not at his hard-day accuracy (0.50). Ancestor: Tetlock (2005),
  in the spirit of; the theorem adds the mechanism (one tally where two are needed) and the decay rate. This is Part V's law in a
  model: an unmeasured domain is governed by standing; standing gives way at the rate the measuring spreads.
- **Theorem 23 — the boat that stays in (EXACT; `code/stay_ashore.py`).** Reading clear (g, p_c) or murky (p_m); sailing costs c; sail
  iff p ≥ c. Printed town (g 0.6, p_c 0.9, p_m 0.4; overall 0.70): all sail, famine 7.4%; murky boats stay in (any c > 0.4), boats on
  the fish 0.54 each, famine 98.2%; each stayer's net catch rises. Subsidy that brings them out at c = p_m + 0.05: 2.9% of the mean
  catch. Six worlds tabulated (famine 39%–100% with murky boats ashore). Closes Chapter 11's stay-ashore item; it is Theorem 5b's
  mistake budget in the town.
- **Evidence entered in Chapter 13 §2D (verified from the sources on 2026-11-12).** Harknett, Schneider and Irwin 2021, PNAS 118(42)
  e2107828118: Seattle's Secure Scheduling ordinance, difference-in-differences against the same employers in 24 metro areas; net
  −11 pp short notice, −13 pp unpaid last-minute changes, −10 pp material hardship, +11 pp good sleep, +7 pp happiness; no
  significant effect on psychological distress; on-call −7 pp (P ≈ 0.07). Williams, Lambert, Kesavan et al. 2018 (Stable Scheduling
  Study, Gap): 28 stores, 19 treatment / 9 control by random assignment, Nov 2015–Aug 2016; median sales +7%, labor productivity
  +5%, +$6.20 revenue per labor hour. Schneider and Harknett 2019, ASR: association of schedule instability with distress, sleep
  and unhappiness stronger than that of wages (wording confirmed from the Shift Project's release; sample size from a secondary
  page). Mani, Mullainathan, Shafir and Zhao 2013, Science: ≈13 IQ points, comparable to a lost night's sleep (university release).
  Federal Reserve DFA, Q2 2026: corporate equities and mutual fund shares — top 1% 50.9%, 90–99th 37.2% (top tenth 88.1%), bottom
  half 0.6%. SCF 2022 "58% of families hold stock directly or indirectly": confirmed from headlines only — to verify.
- **Voice (Aaron, 2026-11-12):** the book states scope as what a result covers and what the next step requires; "honest limits",
  "owed", "found under adversarial review", "will not pretend" are removed throughout (65 edits, `docs/integrate_v038.py`). Chapter 15
  retitled "What Each Open Question Requires"; every entry says whether it needs a proof, a model or a measurement. Refuted
  expectations stay kept and labeled. The sentence added in v0.37 to Chapter 14 §5 ("the machinery was told what to count") is
  removed at his direction.
- **Theorems 22 and 23 attacked after promotion (2026-11-12; `code/attack_T22_T23.py`, `code/results/attack_T22_T23.md`).**
  *T22, A1 — the fisher who knows everything.* Knowing h and every accuracy, unable to tell this morning's kind: right by following
  a = 0.850 > right by reading p = 0.795. Following is individually optimal; the harm needs no mistaken fisher, only days that cannot
  be sorted. *T22, A2 — crowding.* Real sea (boats that are right share V; every boat counted): a reader joins the sage while fewer
  than two boats are behind him (third joiner 0.109 V vs a reader's 0.111 V); the herd stops at 2 of 9 and famine at 14.2%, against
  22.5% in the glass sea. T22 is a theorem of the free answer: it rules where agreeing costs the agreer nothing. *T22, A3.* The lone
  reader pays 5.5 points of his own accuracy. *T23, B1 — the fisher who counts his own hunger.* Bad day costs him L boatloads; a
  murky trip is worth p_m(1 + πL), π = chance one more boatload turns the day. Nine boats: π = 0.267 with murky boats in, 0.136 with
  all out; stay-in threshold 0.51 (L = 1), 0.72 (L = 3), 1.47 (L = 10). Ninety-nine boats needing 55: π = 0.079 / 0.001; threshold
  0.43 at L = 1. *T23, B2.* Pivot chance is higher when fewer are out, so between the two thresholds the murky fleet splits (no two
  stable arrangements — an earlier line of the script claiming two was wrong and is corrected). Ancestors: Olson 1965; Palfrey and
  Rosenthal 1984 (threshold public goods, pivot probabilities), in the spirit of; the difference — what is unsupplied is doubtful
  judgment, not effort.
- **SHED H6 — did the pay rise? (preregistered `docs/SHED_PREREG_v0.3.md`, commit d53d713, before computing;
  `code/field/shed_pay_test.py`, `code/field/results/shed_pay_test.md`).** The compensating-differential reply to §2D predicts
  higher pay on employer-varied schedules. H6a, within person (7,390 pairs, 4,816 persons): change in household-income band on ΔE
  −0.024 [−0.080, +0.031] of a band (NO RAISE DISTINGUISHABLE; largest raise allowed 0.031 band); ΔO +0.048 [−0.018, +0.118].
  H6b, across persons at equal education, age, gender, race/ethnicity, marital status, children, year (29,771 employee-waves):
  employer − fixed −0.220 [−0.277, −0.158] band; P(household income ≥ $50k) −4.6 pp [−6.3, −3.2]; employer − own −0.238 (PAY FELL).
  H6c, full-time only 2021–2023: −0.150 [−0.227, −0.065]. Household income is a band, not the respondent's wage.
- **Citations checked against sources, 2026-11-12.** SCF 2022 (Federal Reserve Bulletin, Oct 2023): 58% of families hold stock
  directly or indirectly; conditional median holding $52,000 overall, $12,600 in the bottom half of usual income, $608,000 in the
  top decile; 54.3% hold retirement accounts, conditional median $86,900, mean $334,000. CRS IF12928: of all households ~30% hold
  retirement balances under $100k, 4.6% over $1M. Tetlock 2005: ~284 experts, ~28,000 predictions; average expert slightly better
  than guessing, slightly worse than simple extrapolation; credentials near-useless (the fame–accuracy sentence is NOT verified and
  was removed). Kaur, Mullainathan, Oh, Schilbach 2024 (QJE, doi 10.1093/qje/qjae038): early pay by lot, output +7% (0.11 SD), fewer
  costly mistakes. Carvalho, Meier, Wang 2016 AER 106(2):260–84: no before/after-payday difference in cognitive function (entered
  in §5C beside Mani). Index inclusion (Yahoo Finance, J. Blikre, 26 Oct 2026; Wikipedia "Initial public offering of SpaceX"):
  Nasdaq-100 fast-entry rule, 15 trading days in place of three months; SPCX listed 12 Jun 2026, joined 7 Jul; JPMorgan estimate
  ~$4.3 bn of index-fund buying; −15% over its first six sessions in the index. SECURE 2.0 §101 (IRC §414A): automatic enrollment
  required of plans established after 29 Dec 2022, for plan years from 2025 — stated from the statute's summary pages; confirm the
  section number before print. Still to confirm from the papers themselves: Branham–Soroka–Wlezien (53%), Schneider–Harknett sample.
- **Sources read in full, 2026-11-24 (PDFs supplied by Aaron); book sentences set to what each prints (`docs/integrate_v040.py`).**
  *Tetlock 2005* (ch. 2–3): 284 participants; 27,451 forecasts in the headline comparison (Fig. 2.4); "humanity barely bests the
  chimp"; experts "no more forecasting skill than dilettantes and less skill than simple extrapolation algorithms"; best humans
  ≤ 20% of outcome variance, crude extrapolation 25–30%, autoregressive models 47%; doctorates, discipline, policy experience,
  classified access, years of experience: "virtually no difference"; "the only consistent predictor was, ironically, fame" —
  better-known forecasters less well calibrated (p. 68); in-demand experts more overconfident, r = .33. The fame clause removed in
  v0.39 as unverified is restored, verified. *Branham, Soroka, Wlezien 2017 (PSQ 132(1))*: Gilens's 1,779 policies, 1981–2002;
  middle and rich majorities agree on 1,594 (89.6%); of 185 disagreements rich win 98 (53.0%), middle 87 (47.0%), not different
  from 50% (p = .41); rich-favor/middle-oppose adopted 37%, middle-favor/rich-oppose adopted 26% (p = .05). *Schneider and
  Harknett 2019 (ASR)*: 27,792 hourly retail and food-service workers at 80 large companies; unstable schedules "much more
  strongly associated" with distress, poor sleep, unhappiness than low wages. *Williams, Lambert, Kesavan et al. 2018*: 28 stores
  (15 Bay Area, 13 Chicago), 19 treatment / 9 control at random, Nov 2015–Aug 2016; median sales +7%; labor productivity +5%
  (+$6.20 per labor hour); $2.9 M added revenue over 35 weeks; only out-of-pocket cost ≈ $31,200; overall turnover unchanged,
  retention of experienced associates up; control stores already had two-week notice and no on-calls. *Mani et al. 2013
  (Science 341:976)*: lab n = 101/100/96 per experiment; 464 sugarcane farmers in 54 villages; effect ≈ 13 IQ points, comparable
  to losing a full night of sleep. The book's "nine months" for the Gap trial is corrected to thirty-five weeks.

## Records, 2026-11-24 (night)
- Theorem 11(iii): exact floors corrected in place (see the bracketed note there).
- Sources confirmed. SECURE 2.0: Pub. L. 117-328, div. T, §101, adding 26 U.S.C. §414A; applies to plan years beginning after
  2024-12-31; plans established before 2022-12-29 are exempt, as are new and small employers (read at law.cornell.edu). The
  book's sentence ("since 2025 the law enrolls the workers of a newly created plan unless they object") stands. Gilens and
  Page 2014: 1,779 policy issues, 1981-2002; average citizens "little or no independent influence"; economic elites and
  organized business groups "substantial independent impacts" (the abstract, as quoted by Journalist's Resource; the paper's
  own file could not be fetched). The book's "nearly two thousand policy questions" and "twenty-two years" stand.
- The fringe of arXiv:2608.18886 recomputed from the paper's stated model: code/fringe_2608_18886.py, results in
  code/results/fringe_2608_18886.md (efficiency 0.8013 against 0.801; fringe 0.1242 against 0.124; harmonics 5.87:1 against
  about 6:1; equal at 22.5 and 67.5 degrees to machine precision; h(0)/h(1) 1.17432 against 1.17451).
- Tables added to the book (v0.44) are read from: code/imposition_cascade_T17.py; code/rig/hank_port/bw_hank.py and hank_ge.py
  (the block and its constants); results_sweep_fast/SWEEP_SUMMARY.md; summarize_two_asset.py.


## 2026-11-27 — two notes from Aaron's read of v0.48

**T6, how often the hidden agent is right (Ch 6 §2).** The Round-5 line above gave the hand plateau strategy's hit rate,
1/n + s(n−1)/n, against the captain's 1 − s + s/n. It is more than that strategy's: it is the maximum over ALL perfectly
unreadable strategies. Proof. Fix E = e. Unreadable means P(A = a | e) = 1/n for every a, and
P(A = a | e) ≥ P(F = a | e)·P(A = a | e, F = a), so P(A = F | e) ≤ Σ_a min(P(F = a | e), 1/n) = 1/n + (n−1)s/n (one entry
of P(F | e) is 1 − s + s/n ≥ 1/n, the others are s/n ≤ 1/n). The hand strategy attains it. ∎ So a perfectly hidden agent
is right more often than the captain iff s > 1/2, for every n. [PROVEN; checked by linear program in 42 worlds,
`code/plateau_hit_rate_bound.py`.] The book's sentence said "except in rooms noisier than a coin", which stated no
condition a reader could use; it now says "unless those tells are noise more than half the time". The statement is about
being right. On the aim ruler the hidden agent overtakes the captain earlier (reference world, s = 0.5: best known
plateau aim 0.335 against the captain's 0.247), and the sentence does not speak of aim.

**T16, the unit of the time gate (Ch 7 §1, §4).** The model's t counts consultations of the agent's own knowledge, and
nothing in it is clock time. Two takings therefore move an agent down the same curve: fewer hours, and the same hours
with fewer consultations left in them. The second is how the book now books a job that returns the hours and takes
what they are for (the complaints-line script, Ch 7 §1). What is exact: the gate in consultations. What is DATA: that
such work depletes (Hochschild 1983; Hülsheger and Schewe 2011, J. Occup. Health Psychol. 16(3):361–389, 95 independent
samples, surface acting and emotion-rule dissonance against impaired well-being, ρ = .39–.48; citation checked
2026-11-27). What is NOT established: the rate at which depletion converts to lost consultations. The calculator's
ninth question supposes proportionality and says so on the page.
