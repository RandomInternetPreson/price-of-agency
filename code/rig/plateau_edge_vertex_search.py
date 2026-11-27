"""
plateau_edge_vertex_search.py -- the plateau's exact edge as concave minimization over a polytope.

The edge c0* = max aim subject to delta_A = 1, i.e. P(A=a | E=e) = 1/n for every (e, a).
With A uniform, aim = 1 - H(A|F)/log2 n, and H(A|F) = sum_f pF(f) H( sum_e C_E[f,e] pol[f,e,:] )
is CONCAVE in pol. The feasible set is a polytope. A concave function attains its minimum at a
vertex, so the edge is a vertex-search problem (this is why SPSA/softmax missed it, R4).
Method: successive linearization from many random vertices (each LP solution is a vertex; the
linearized objective at a vertex is minimized by another vertex; iterate to a local vertex
minimum), plus pure random-objective vertex sampling. Reports the best aim found and how often it
recurs. A certified upper bound needs a different tool; this script tightens the lower bound.
Usage: python plateau_edge_vertex_search.py [n] [s] [restarts] [seconds]
"""
import sys, time
import numpy as np
from scipy.optimize import linprog

n = int(sys.argv[1]) if len(sys.argv) > 1 else 6
s = float(sys.argv[2]) if len(sys.argv) > 2 else 0.5
R = int(sys.argv[3]) if len(sys.argv) > 3 else 2000
budget = float(sys.argv[4]) if len(sys.argv) > 4 else 600.0
rng = np.random.default_rng(0)
pF = np.full(n, 1 / n)
C = np.full((n, n), s / n); C[np.arange(n), np.arange(n)] += 1 - s
p_fe = pF[:, None] * C; p_e = p_fe.sum(0); q = (p_fe / p_e[None]).T       # q[e,f]
log2n = np.log2(n)
N = n ** 3
idx = lambda f, e, a: (f * n + e) * n + a
# equality constraints
rows, rhs = [], []
for f in range(n):
    for e in range(n):
        r = np.zeros(N); r[[idx(f, e, a) for a in range(n)]] = 1; rows.append(r); rhs.append(1.0)
for e in range(n):
    for a in range(n):
        r = np.zeros(N)
        for f in range(n):
            r[idx(f, e, a)] = q[e, f]
        rows.append(r); rhs.append(1.0 / n)
A_eq = np.array(rows); b_eq = np.array(rhs)


def H_AF(x):
    pol = x.reshape(n, n, n)
    pa_f = np.einsum('fe,fea->fa', C, pol)
    with np.errstate(divide='ignore', invalid='ignore'):
        t = np.where(pa_f > 1e-15, pa_f * np.log2(pa_f), 0.0)
    return float(-(pF[:, None] * t).sum())


def grad(x):
    pol = x.reshape(n, n, n)
    pa_f = np.einsum('fe,fea->fa', C, pol)
    g_pa = -(np.log2(np.maximum(pa_f, 1e-15)) + 1 / np.log(2)) * pF[:, None]   # dH/dpa_f
    return np.einsum('fe,fa->fea', C, g_pa).ravel()


def lp(c):
    res = linprog(c, A_eq=A_eq, b_eq=b_eq, bounds=(0, 1), method='highs')
    return res.x if res.status == 0 else None


def aim(x):
    return 1 - H_AF(x) / log2n


best, hist, t0 = None, [], time.time()
for r in range(R):
    if time.time() - t0 > budget:
        break
    x = lp(rng.normal(size=N))
    if x is None:
        continue
    for it in range(50):                       # successive linearization
        y = lp(grad(x))
        if y is None or H_AF(y) >= H_AF(x) - 1e-12:
            break
        x = y
    a = aim(x); hist.append(a)
    if best is None or a > best[0] + 1e-12:
        best = (a, x.copy())
        print(f"restart {r:5d}  new best aim {a:.6f}   ({time.time() - t0:.0f}s)", flush=True)
hist = np.array(hist)
print(f"\nn={n} s={s}: best aim at delta_A=1 found = {best[0]:.6f}  (restarts {len(hist)}, "
      f"within 1e-6 of best in {np.mean(hist > best[0] - 1e-6):.1%} of restarts; median {np.median(hist):.4f})")
pol = best[1].reshape(n, n, n)
print("support size (nonzeros):", int((pol > 1e-9).sum()), "of", N)
np.save(f'results_exact/plateau_edge_vertex_n{n}_s{s}.npy', pol)
# reference values
lam = 1 / (n * q.max()); c0p = 1 - (-(s + (1 - s) / n) * np.log2(s + (1 - s) / n) - (n - 1) * ((1 - s) / n) * np.log2((1 - s) / n)) / log2n
print(f"reference: c0' (hand plateau, closed form) = {c0p:.4f}; previously best asymmetric numerical = 0.277 at (6,0.5); crude upper bound 0.56")
