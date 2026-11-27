# Adversarial referee report on THEOREMS_v1 — self-administered, July 2026

## Attack 1: "This is already known."
FINDING: Two established adjacent literatures. Empowerment (Klyubin/Polani/
Nehaniv 2005+): channel capacity actions→sensors as task-independent agency
measure — cousin of our competence axis. Rational inattention (Sims 2003+):
finite Shannon capacity agents in economics — cousin of our time/capacity
axis. VERDICT: components known; the (competence, δ_A) frontier, theft-as-
frontier-displacement, and Theorems 5–11 not found in this form. Claim
"novel configuration + new exact results," never "new field." Full review
still owed: covert channels, differential privacy, obfuscation (Brunton &
Nissenbaum), security games, Scott's legibility. [QUEUED]

## Attack 2: "Toy model class; constants aren't portable."
CONCEDED in part. All results proven on symmetric channels, n=4–6, uniform
priors; T11 constants (0.45, 0.984, h=3) are class properties. Door-2 pass
shows the dichotomy SHAPE is invariant across n∈{4,5,6}, s∈{0.3,0.5,0.7},
and random asymmetric channels (gated floors saturate below sage ceiling;
additive floors reach ≈0.99 at h=3 in every setting). Shape claims stand;
constants must always be reported with their class. [STANDING RULE]

## Attack 3: "Competence = I(A;F) is a choice; reward-based competence may
behave differently." CONCEDED as open. I(A;F) can rise while accuracy
falls and vice versa. Dual-track both definitions in Phase 2 revisions.
[QUEUED]

## Attack 4: "Annealing π_t ∝ π*^t is one model of time; elasticities in
log-resource space embed a scale choice." CONCEDED. Annealing is standard
(bounded-rational bridge) but not unique — replicate P7/P8/T10 under an
iterative-computation model of time. Log-elasticities are unit-free but
not reparametrization-free; report alternative parametrizations. [QUEUED]

## Attack 5: "'Theft' smuggles normativity."
RESPONSE: All definitions are structural (frontier displacement; elasticity
yields); the word is an interpretive label. Papers should define
Δ-frontier displacement first and introduce 'theft' explicitly as a label.
[ADOPTED]

## Attack 6: "Which observer? δ_A(𝒪) makes every social claim
observer-indexed." ACCEPTED as a feature: T9 forces every application to
name its observer (the state, the employer, the platform, the neighbor).
Ambiguity here was the pre-T9 defect, not the post-T9 one.

## Attack 7: "Gate definition sensitivity."
FOUND VIA DOOR 3: the gate 'min e with δ>0 anywhere' is weak — composite
environments create ambiguity pockets that open it at tiny e. Define also
the strong gate (aggregate δ_A exceeding threshold) and re-derive. [QUEUED]

## Scored predictions (preregistration ledger opens here)
- Claude, session 3: "stealth is time-gated" — MISS (P7 refuted it).
- Claude, session 6: "legible neighbors raise your gate" — MISS (they
  lower it via ambiguity pockets; only the perfect sage welds it shut).
- Aaron: claims broad anticipation of results to date — unscored
  (post-hoc); preregistration begins next session.
