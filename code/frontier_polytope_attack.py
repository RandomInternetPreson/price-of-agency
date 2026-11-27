"""
frontier_polytope_attack.py -- re-attack of the (aim, delta_A) frontier with
the method that found R4: fix the visible choice pattern p(a|e) and maximize
I(A;F) over the polytope of policies consistent with it (SLSQP, seeded with
the structured policies: noise reading, sage, hand plateau policy).

Each run gives an EXACT feasible point, hence a certified LOWER BOUND on the
frontier at that delta_A. Two one-parameter families of choice pattern:
  (a) legible rule (a = e) w.p. mu, uniform otherwise   [Tomas <-> Nadia]
  (b) the sage's own row p(f=a|e) w.p. mu, uniform otherwise
The pointwise max over families is reported against the old mixing-sage
candidate curve (Ch 6's first kept corpse) at equal delta_A.
"""
import sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import hiding_theorem_econ as ht

n, s = 6, 0.5
ht.s_global = s
pF, C_E, p_fe, p_e, p_fge = ht.make_world(n, s)
log2n = np.log2(n)

def h_n(alpha):
    m = alpha + (1 - alpha) / n; o = (1 - alpha) / n
    return -(m * np.log2(m) + (n - 1) * o * np.log2(o))

def mixing_sage_at_delta(d):
    # delta(lam) = h_n(lam(1-s))/log n is decreasing in lam; invert by bisection
    lo, hi = 0.0, 1.0
    for _ in range(60):
        mid = (lo + hi) / 2
        if h_n(mid * (1 - s)) / log2n > d: lo = mid
        else: hi = mid
    lam = (lo + hi) / 2
    return 1 - h_n(lam) / log2n

rows = []
for fam in ['a', 'b']:
    for mu in [0.0, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]:
        if fam == 'a':
            P = np.full((n, n), (1 - mu) / n); P[np.arange(n), np.arange(n)] += mu
        else:
            P = mu * p_fge + (1 - mu) / n     # p(f=a|e) row mixed with uniform
        dA = (ht.H(p_e[:, None] * P) - ht.H(p_e)) / log2n
        amin = ht.aim_min(P, p_fe, n)
        if fam == 'a' and mu == 1.0:
            amax = amin
        else:
            amax, _ = ht.aim_max(P, p_fge, p_fe, n, restarts=6)
        rows.append((fam, mu, dA, amin, amax))
        print(f"fam {fam} mu={mu:4.2f}  delta_A={dA:.4f}  aim_min={amin:.4f}  aim_max>={amax:.4f}  "
              f"mixing-sage@delta={mixing_sage_at_delta(dA) if dA >= 0.7533 else float('nan'):.4f}", flush=True)

import os
# This run's points. figures/frontier_certified_points.npy, which the figures draw, holds these and the better points later searches added.
np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', 'frontier_rows.npy'),
        np.array([(0 if r[0]=='a' else 1, *r[1:]) for r in rows]))
print("done")
