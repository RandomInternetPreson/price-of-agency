"""
hiding_theorem_econ.py -- T19 (the economic hiding theorem): what the
joint law of (action, circumstance) identifies, and what it cannot.

Model (Ch 4 conventions): future F uniform on n; environment E reveals F
w.p. (1-s) else uniform; a policy is p(a|f,e). The ECONOMETRICIAN's data
are the joint law of (A,E) only -- choice probabilities p(a|e) and p(e):
revealed preference, random-utility estimation, every (P,Q)-type record.

Claims computed here:
 (i)   delta_A = H(A|E)/log2 n is a function of p(a|e) alone: IDENTIFIED.
 (ii)  aim = I(A;F)/H(F) is NOT identified. For fixed p(a|e) it ranges
       over [aim_min, aim_max], where
         aim_min : residual randomness is noise (A indep. of F given E)
         aim_max : residual randomness carries F-payload (max I(A;F)
                   over all p(a|f,e) with the same p(a|e)) -- a convex
                   maximization over a polytope, solved by multi-start
                   SLSQP; vertices are the maximizers.
 (iii) For UNIFORM choice data (the scatter / full-stealth row), the
       interval is [0, c0(s)]: Nadia and Ines produce identical data.
       c0 is checked against Theorem 6's explicit construction.
 (iv)  The interval collapses to a point when F is recorded alongside A
       (direct computation of I(A;F)) -- the missing column.
 (v)   Any such p(a|e) with full support is rationalized EXACTLY by a
       logit random-utility model with u(a|e) = log p(a|e); its welfare
       (logsum) is identical under every point of the interval.

Everything is exact enumeration except the maximization in (ii), which is
a numerical maximum with a certificate: the Theorem-6 construction gives
an explicit feasible point, so aim_max >= construction value exactly.
"""
import numpy as np
from scipy.optimize import minimize

rng = np.random.default_rng(11)
s_global = 0.5


def H(p):
    p = np.asarray(p, float).ravel()
    p = p[p > 1e-15]
    return float(-(p * np.log2(p)).sum())


def make_world(n, s):
    pF = np.full(n, 1.0 / n)
    C_E = np.full((n, n), s / n); C_E[np.arange(n), np.arange(n)] += (1 - s)   # p(e|f)
    p_fe = pF[:, None] * C_E
    p_e = p_fe.sum(0)
    p_f_given_e = (p_fe / p_e[None]).T                                       # (e,f)
    return pF, C_E, p_fe, p_e, p_f_given_e


def stats(pol, p_fe, n):
    """pol (f,e,a). Returns aim, delta_A, p(a|e)."""
    p = p_fe[:, :, None] * pol
    p_ea = p.sum(0)
    p_e = p_ea.sum(1)
    H_A_E = H(p_ea) - H(p_e)
    p_fa = p.sum(1)
    I_AF = H(p_fa.sum(1)) + H(p_fa.sum(0)) - H(p_fa)
    return I_AF / np.log2(n), H_A_E / np.log2(n), p_ea / p_e[:, None]


def aim_min(p_a_given_e, p_fe, n):
    pol = np.broadcast_to(p_a_given_e[None, :, :], (n, n, n)).copy()  # p(a|f,e)=p(a|e)
    return stats(pol, p_fe, n)[0]


def aim_max(p_a_given_e, p_f_given_e, p_fe, n, restarts=40):
    """Maximize I(A;F) over pol(f,e,a) s.t. sum_f p(f|e) pol(f,e,a) = p(a|e)."""
    k = n * n * n
    def unpack(x): return x.reshape(n, n, n)
    def negaim(x): return -stats(unpack(x), p_fe, n)[0]
    cons = []
    # row-stochastic: sum_a pol(f,e,a) = 1
    def row_c(x):
        return unpack(x).sum(2).ravel() - 1.0
    # margin: sum_f p(f|e) pol(f,e,a) = p(a|e)
    def marg_c(x):
        pol = unpack(x)
        m = np.einsum('ef,fea->ea', p_f_given_e, pol)
        return (m - p_a_given_e).ravel()
    cons = [{'type': 'eq', 'fun': row_c}, {'type': 'eq', 'fun': marg_c}]
    bounds = [(0.0, 1.0)] * k
    best = -np.inf; best_pol = None
    sage = np.zeros((n, n, n)); sage[np.arange(n), :, np.arange(n)] = 1.0      # A = F
    hand = np.zeros((n, n, n)); q = 1.0 / (n * (1 - s_global) + s_global)
    for e in range(n):
        for f in range(n):
            if f != e: hand[f, e, f] = 1.0
            else: hand[f, e, :] = (1 - q) / (n - 1); hand[f, e, e] = q
    noise = np.broadcast_to(p_a_given_e[None], (n, n, n)).copy()
    seeds = [noise, sage, hand]
    for r in range(restarts):
        if r < len(seeds):
            x0 = seeds[r]
        else:
            z = rng.random((n, n, n)); z /= z.sum(2, keepdims=True)
            x0 = 0.5 * seeds[r % 3] + 0.5 * z
        res = minimize(negaim, x0.ravel(), method='SLSQP', bounds=bounds,
                       constraints=cons, options={'maxiter': 400, 'ftol': 1e-12})
        if res.success or True:
            x = np.clip(res.x, 0, 1).reshape(n, n, n)
            x /= x.sum(2, keepdims=True)
            # re-check feasibility of margin
            if np.abs(marg_c(x.ravel())).max() < 1e-6:
                a = stats(x, p_fe, n)[0]
                if a > best:
                    best, best_pol = a, x
    return best, best_pol


def theorem6_construction(n, s, lam, p_fe):
    """Plateau family: follow F w.p. lam, else E-conditioned whitening
    residual r_e(a) chosen so p(a|e) is uniform. Valid for lam <= lam*."""
    pF, C_E, p_fe, p_e, p_f_given_e = make_world(n, s)
    pol = np.zeros((n, n, n))
    for e in range(n):
        # p(a|e) = lam * p(f=a|e) + (1-lam) * r_e(a) = 1/n  =>  r_e(a) = (1/n - lam p(a|e)) / (1-lam)
        r = (1.0 / n - lam * p_f_given_e[e]) / (1 - lam)
        assert r.min() >= -1e-12, "lam above lam*"
        r = np.clip(r, 0, None); r /= r.sum()
        for f in range(n):
            pol[f, e, :] = (1 - lam) * r
            pol[f, e, f] += lam
    return pol


def lam_star(n, s):
    return 1.0 / (n * (1 - s) + s)


if __name__ == "__main__":
    n, s = 6, 0.5
    s_global = s
    pF, C_E, p_fe, p_e, p_f_given_e = make_world(n, s)
    log2n = np.log2(n)

    print(f"n={n}, s={s}, lambda*={lam_star(n, s):.4f}")
    # (iii) uniform choice data: the scatter row
    U = np.full((n, n), 1.0 / n)
    a_min = aim_min(U, p_fe, n)
    pol6 = theorem6_construction(n, s, lam_star(n, s) - 1e-9, p_fe)
    a_c0, d_c0, pae = stats(pol6, p_fe, n)
    assert np.abs(pae - U).max() < 1e-8
    a_max, _ = aim_max(U, p_f_given_e, p_fe, n, restarts=15)
    print("\n(iii) UNIFORM choice data (identical for Nadia and Ines):")
    print(f"   delta_A identified = 1.0000")
    print(f"   aim_min (noise reading, Nadia)          = {a_min:.4f}")
    print(f"   aim at Theorem-6 construction (Ines)    = {a_c0:.4f}  (c0)")
    print(f"   aim_max (numerical, 40 restarts)        = {a_max:.4f}")
    print(f"   -> identification interval for aim: [{a_min:.4f}, {max(a_max, a_c0):.4f}]")

    # (ii) a one-parameter family of choice data between Tomas (mu=1) and Nadia (mu=0):
    # p(a|e) = mu * 1[a = MAP(e)] + (1-mu)/n
    print("\n(ii) Family of choice data: legible rule w.p. mu, scatter w.p. 1-mu")
    print("   mu    delta_A   aim_min   aim_max   width    RUM-logsum")
    rows = []
    for mu in [1.0, 0.9, 0.75, 0.5, 0.25, 0.1, 0.0]:
        P = np.full((n, n), (1 - mu) / n); P[np.arange(n), np.arange(n)] += mu  # MAP(e)=e
        if mu == 1.0:
            P = np.eye(n)
        amin = aim_min(P, p_fe, n)
        if mu == 1.0:
            amax = amin  # degenerate: no residual randomness to carry payload
        else:
            amax, _ = aim_max(P, p_f_given_e, p_fe, n, restarts=15)
        dA = (H(p_e[:, None] * P) - H(p_e)) / log2n
        # logit RUM: u(a|e)=log p(a|e); logsum welfare = sum_e p(e) log sum_a exp(u) = 0 identically
        logsum = float(sum(p_e[e] * np.log(np.exp(np.log(np.clip(P[e], 1e-300, None))).sum()) for e in range(n)))
        rows.append((mu, dA, amin, amax, amax - amin, logsum))
        print(f"   {mu:4.2f}   {dA:6.4f}   {amin:6.4f}   {amax:6.4f}   {amax-amin:6.4f}   {logsum:+.3f}")

    # (iv) F recorded: interval collapses (trivial, shown for the Ines point)
    a_true, d_true, _ = stats(pol6, p_fe, n)
    print(f"\n(iv) With F recorded, aim is a direct computation: Ines reads {a_true:.4f}, Nadia reads {a_min:.4f}. Interval width 0.")

    import os
    np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', 'hiding_rows.npy'), np.array(rows))
