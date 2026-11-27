"""
surveillance_T9_wider_plateau.py -- does Chapter 8's surveillance inversion
survive on the wider-plateau policies of R4?

T9 (theft_equilibrium.py, Part B): for the lambda*-plateau policy, a watcher
who sees {E, R} (circumstances + the private coin) reads the agent at
delta_A = 0.29, below the sage's 0.753: INVERSION. Partial capture of R
w.p. rho gives an exactly linear delta_A(rho); crossover at rho ~ 0.348.

Here the same computation (identical coin model: inverse-CDF realization of
each row at r = (k+0.5)/m, m = 64, common uniform R) is run on
  (1) the lambda* policy            (T6 construction; aim 0.052)  -- replication
  (2) the hand plateau policy       (R4; aim c0' = 0.247)
  (3) the asymmetric SLSQP policy   (R4; aim 0.277, numerical)
All three have delta_A({E}) = 1. The question is delta_A({E,R}).
"""
import os, sys, numpy as np
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import hiding_theorem_econ as ht

n, s, m = 6, 0.5, 64
ht.s_global = s
pF, C_E, p_fe, p_e, p_fge = ht.make_world(n, s)
log2n = np.log2(n)
sage = (ht.H(p_fe) - ht.H(p_e)) / log2n


def surveilled(pol):
    cdf = np.cumsum(pol, axis=-1)
    g = np.zeros((n, n, m), dtype=int)
    for k in range(m):
        g[:, :, k] = (cdf < (k + 0.5) / m).sum(axis=-1)
    H_A_ER = 0.0
    for e in range(n):
        for k in range(m):
            dist = np.zeros(n)
            for f in range(n):
                dist[g[f, e, k]] += p_fge[e, f]
            H_A_ER += p_e[e] * (1.0 / m) * ht.H(dist)
    p_ea = np.zeros((n, n))
    for e in range(n):
        for k in range(m):
            for f in range(n):
                p_ea[e, g[f, e, k]] += p_e[e] * (1.0 / m) * p_fge[e, f]
    dA_O0 = (ht.H(p_ea) - ht.H(p_ea.sum(1))) / log2n
    return dA_O0, H_A_ER / log2n


def lam_policy():
    return ht.theorem6_construction(n, s, ht.lam_star(n, s) - 1e-9, p_fe)

def hand_policy():
    q = ht.lam_star(n, s); pol = np.zeros((n, n, n))
    for e in range(n):
        for f in range(n):
            if f != e: pol[f, e, f] = 1.0
            else: pol[f, e, :] = (1 - q) / (n - 1); pol[f, e, e] = q
    return pol

if __name__ == "__main__":
    pols = [("lambda* policy (T6 construction)", lam_policy()),
            ("hand plateau policy (R4, c0')", hand_policy())]
    try:
        pols.append(("asymmetric SLSQP policy (R4, 0.277)", np.load(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', 'best_slsqp.npy'))))
    except Exception as ex:
        print("asymmetric policy not loaded:", ex)
    print(f"sage ceiling delta_A = {sage:.4f}\n")
    print(f"{'policy':38s} {'aim':>7s} {'dA({E})':>9s} {'dA({E,R})':>10s} {'inverted?':>10s} {'rho*':>7s}")
    for name, pol in pols:
        aim, dA, _ = ht.stats(pol, p_fe, n)
        d0, d1 = surveilled(pol)
        inv = d1 < sage
        rho_star = (d0 - sage) / (d0 - d1) if d1 < sage else float('nan')
        print(f"{name:38s} {aim:7.4f} {d0:9.4f} {d1:10.4f} {str(inv):>10s} {rho_star:7.3f}")
    print("\nrho* = fraction of the coin a watcher must capture to read the agent below the sage.")
