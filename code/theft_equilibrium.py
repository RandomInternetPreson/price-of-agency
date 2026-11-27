"""
theft_equilibrium.py -- Phase 3 opening, two exact computations.

PART A: Theft elasticity matrix (parameter-free attack analysis)
  Outcomes y in {competence, delta_A}; resources x in {e, t, s, s_hat}.
  Elasticity E[y,x] = dlog y / dlog x, central differences on exact values.
  Computed for two target types at realistic operating points:
    OVERT  agent: reward-seeker, resources (e, beta) in env s
    COVERT agent: whitening stealth at believed s_hat, deliberation t
  Test: does |elasticity| of competence dominate |elasticity| of delta_A
  across the space? If yes, ANY coercer objective mixing the two allocates
  to competence attacks -> cheap theft as equilibrium, no cost assumptions.

PART B: Observer-relative delta_A and privacy theft
  Covert agent implements whitening via private uniform randomness R
  (inverse-CDF realization, discretized m=64). Observer info sets:
    O0 = {E}            -> delta_A(O0) = 1 on plateau (proven)
    O1 = {E, R}         -> full surveillance of the randomizer
  Partial surveillance: observer captures R w.p. rho (with knowledge of
  capture) -> H(A|E,S) = rho*H(A|E,R) + (1-rho)*H(A|E) exactly (linear).
  Question: what does delta_A collapse TO under full surveillance?
"""
import numpy as np

n = 6; log2n = np.log2(n)
pF = np.full(n, 1/n)

def ch(f):
    C = np.full((n, n), (1-f)/n); C[np.arange(n), np.arange(n)] += f
    return C

def H(p):
    p = p[p > 1e-15]
    return float(-(p * np.log2(p)).sum())

def joint_env(s):
    C_E = ch(1-s); p_fe = pF[:, None]*C_E
    return p_fe, (p_fe/p_fe.sum(0)[None]).T   # p(f,e), q(e,f)=p(f|e)

def overt_metrics(e_edu, beta, s):
    p_fe, _ = joint_env(s)
    C_K = ch(e_edu)
    p_fek = p_fe[:, :, None]*C_K[:, None, :]
    post = np.nan_to_num(p_fek/p_fek.sum(0)[None], nan=1/n)
    lg = beta*post; lg -= lg.max(0, keepdims=True)
    pol = np.exp(lg); pol /= pol.sum(0, keepdims=True)
    p = p_fek[:, :, :, None]*np.transpose(pol, (1, 2, 0))[None]
    p_ea = p.sum(axis=(0, 2)); dA = (H(p_ea)-H(p_ea.sum(1)))/log2n
    p_fa = p.sum(axis=(1, 2))
    comp = (H(p_fa.sum(1))+H(p_fa.sum(0))-H(p_fa))/log2n
    return comp, dA

def covert_policy(s_hat, t, s_true):
    """whitening target believed at s_hat, annealed by deliberation t."""
    _, q_hat = joint_env(s_hat)
    lam = 1.0/(n*q_hat.max())
    pol = np.zeros((n, n, n))
    for e in range(n):
        r = np.clip((1.0/n - lam*q_hat[e])/(1-lam), 0, None); r /= r.sum()
        for f in range(n):
            pol[f, e, :] = (1-lam)*r; pol[f, e, f] += lam
    z = np.power(np.clip(pol, 1e-12, None), t)
    return z/z.sum(-1, keepdims=True)

def covert_metrics(s_hat, t, s_true):
    pol = covert_policy(s_hat, t, s_true)
    p_fe, _ = joint_env(s_true)
    p = p_fe[:, :, None]*pol
    p_ea = p.sum(0); dA = (H(p_ea)-H(p_ea.sum(1)))/log2n
    p_fa = p.sum(1)
    comp = (H(p_fa.sum(1))+H(p_fa.sum(0))-H(p_fa))/log2n
    return comp, dA

def elasticity(fn, x0, idx, h=0.02):
    """dlog y / dlog x by central difference in log-space."""
    xp = list(x0); xm = list(x0)
    xp[idx] = x0[idx]*np.exp(h); xm[idx] = x0[idx]*np.exp(-h)
    yp = np.array(fn(*xp)); ym = np.array(fn(*xm))
    with np.errstate(divide="ignore", invalid="ignore"):
        out = (np.log(yp)-np.log(ym))/(2*h)
    return np.nan_to_num(out, nan=0.0, posinf=0.0, neginf=0.0)

print("PART A -- THEFT ELASTICITY MATRIX  (rows: resource; cols: comp, dA)")
print("\nOVERT agent, operating points (e, beta, s):")
for pt in [(0.7, 20.0, 0.5), (0.9, 20.0, 0.5), (0.7, 6.0, 0.5),
           (0.7, 20.0, 0.3), (0.55, 20.0, 0.5)]:
    E_e = elasticity(overt_metrics, pt, 0)
    E_b = elasticity(overt_metrics, pt, 1)
    E_s = elasticity(overt_metrics, pt, 2)
    print(f"  at (e={pt[0]}, beta={pt[1]}, s={pt[2]}):")
    print(f"    d/dlog e     : comp {E_e[0]:+7.3f}   dA {E_e[1]:+7.3f}")
    print(f"    d/dlog beta  : comp {E_b[0]:+7.3f}   dA {E_b[1]:+7.3f}")
    print(f"    d/dlog s     : comp {E_s[0]:+7.3f}   dA {E_s[1]:+7.3f}")

print("\nCOVERT agent, operating points (s_hat, t, s_true=0.5):")
for pt in [(0.5, 1.0, 0.5), (0.5, 0.5, 0.5), (0.4, 1.0, 0.5)]:
    E_sh = elasticity(covert_metrics, pt, 0)
    E_t = elasticity(covert_metrics, pt, 1)
    print(f"  at (s_hat={pt[0]}, t={pt[1]}):")
    print(f"    d/dlog s_hat : comp {E_sh[0]:+7.3f}   dA {E_sh[1]:+7.3f}")
    print(f"    d/dlog t     : comp {E_t[0]:+7.3f}   dA {E_t[1]:+7.3f}")

# ---------------------------------------------------------------- PART B
print("\nPART B -- OBSERVER-RELATIVE delta_A, PRIVACY THEFT")
m = 64                                    # discretized private randomness
s_true = 0.5
pol = covert_policy(s_true, 1.0, s_true)  # (f,e,a), on-plateau stealth
p_fe, _ = joint_env(s_true)

# realize a = g(f,e,r): inverse-CDF of pol[f,e,:] at r=(k+0.5)/m
cdf = np.cumsum(pol, axis=-1)
g = np.zeros((n, n, m), dtype=int)
for k in range(m):
    u = (k+0.5)/m
    g[:, :, k] = (cdf < u).sum(axis=-1)

# joint p(f,e,r,a) with R uniform: exact
pR = 1.0/m
# H(A | E, R): for each (e,r), A's dist over posterior f
H_A_ER = 0.0
q = (p_fe/p_fe.sum(0)[None]).T            # (e,f)
p_e = p_fe.sum(0)
for e in range(n):
    for k in range(m):
        dist = np.zeros(n)
        for f in range(n):
            dist[g[f, e, k]] += q[e, f]
        H_A_ER += p_e[e]*pR*H(dist)
dA_O1 = H_A_ER/log2n

# H(A|E) check (should be ~1 on plateau, up to m-discretization)
p_ea = np.zeros((n, n))
for e in range(n):
    for k in range(m):
        for f in range(n):
            p_ea[e, g[f, e, k]] += p_e[e]*pR*q[e, f]
dA_O0 = (H(p_ea)-H(p_ea.sum(1)))/log2n

# Theorem 1 reference: sage ceiling H(F|E)/log2n
sage = (H(p_fe)-H(p_e))/log2n
print(f"  delta_A(O0={{E}})        = {dA_O0:.4f}   (plateau; 1.0 up to m-discretization)")
print(f"  delta_A(O1={{E,R}})      = {dA_O1:.4f}   (full surveillance of randomizer)")
print(f"  sage ceiling H(F|E)/log = {sage:.4f}")
print(f"  partial surveillance rho: delta_A(rho) = rho*{dA_O1:.4f} + (1-rho)*{dA_O0:.4f}  [exact, linear]")
lam = 1.0/(n*((1-s_true)+s_true/n))
print(f"  interpretation: surveilled stealth keeps only the F-uncertainty "
      f"routed through lambda={lam:.3f}-weighted action map")
