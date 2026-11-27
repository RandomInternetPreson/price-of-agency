import numpy as np, sys
sys.path.insert(0, 'repo/AND_repo/code')
from hiding_theorem_econ import make_world, stats, H, lam_star, theorem6_construction
from scipy.optimize import minimize

def h_row(m, n):  # entropy of a row with match prob m, others (1-m)/(n-1)
    o = (1-m)/(n-1); return -(m*np.log2(m) + (n-1)*o*np.log2(o))

def hand_policy(n, s):
    pF, C_E, p_fe, p_e, p_fge = make_world(n, s)
    q = lam_star(n, s); pol = np.zeros((n,n,n))
    for e in range(n):
        for f in range(n):
            if f != e: pol[f,e,f] = 1.0
            else: pol[f,e,:] = (1-q)/(n-1); pol[f,e,e] = q
    return pol

def numerical_edge(n, s, restarts=12, seed=5):
    rng = np.random.default_rng(seed)
    pF, C_E, p_fe, p_e, p_fge = make_world(n, s)
    k = n**3
    def unpack(x): return x.reshape(n,n,n)
    negaim = lambda x: -stats(unpack(x), p_fe, n)[0]
    cons = [{'type':'eq','fun': lambda x: unpack(x).sum(2).ravel()-1},
            {'type':'eq','fun': lambda x: (np.einsum('ef,fea->ea', p_fge, unpack(x)) - 1/n).ravel()}]
    best = -1
    starts = [hand_policy(n, s)]
    for r in range(restarts):
        z = rng.random((n,n,n)); z /= z.sum(2, keepdims=True)
        starts.append(0.5*hand_policy(n,s) + 0.5*z if r % 2 else 0.5*np.full((n,n,n),1/n) + 0.5*z)
    for x0 in starts:
        res = minimize(negaim, x0.ravel(), method='SLSQP', bounds=[(0,1)]*k, constraints=cons,
                       options={'maxiter':300,'ftol':1e-12})
        x = np.clip(res.x,0,1).reshape(n,n,n); x /= x.sum(2,keepdims=True)
        if np.abs(np.einsum('ef,fea->ea', p_fge, x) - 1/n).max() < 1e-7:
            best = max(best, stats(x, p_fe, n)[0])
    return best

print(" n    s    c0 (T6 printed)   c0' closed form   c0' computed   numerical edge   sage delta")
for n, s in [(6,0.3),(6,0.5),(6,0.7),(4,0.5),(8,0.5)]:
    pF, C_E, p_fe, p_e, p_fge = make_world(n, s)
    c0 = stats(theorem6_construction(n, s, lam_star(n,s)-1e-9, p_fe), p_fe, n)[0]
    m = s + (1-s)/n                       # match prob of "reveal F w.p. s" channel
    c0p_formula = 1 - h_row(m, n)/np.log2(n)
    a, d, pae = stats(hand_policy(n,s), p_fe, n); assert abs(d-1)<1e-9
    sage_delta = (H(p_fe)-H(p_e))/np.log2(n)
    ne = numerical_edge(n, s) if n <= 6 else float('nan')
    print(f" {n}   {s:.1f}      {c0:.4f}           {c0p_formula:.4f}          {a:.4f}          {ne:.4f}          {sage_delta:.4f}")
