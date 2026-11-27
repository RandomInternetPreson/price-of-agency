"""
plateau_edge_bnb.py -- a CERTIFIED upper bound on the plateau edge (stress objective #2).

The edge c0*(n, s) = max aim subject to delta_A = 1 (A uniform given E), i.e.
    c0* = 1 - min_pol H(A|F) / log2 n,   H(A|F) = sum_f pF(f) h( y_f ),  y_f[a] = sum_e C[f,e] pol[f,e,a],
with pol in a polytope (row sums 1; sum_f q[e,f] pol[f,e,a] = 1/n). H is SEPARABLE CONCAVE in the n^2
variables y = (y_fa), so its convex envelope over a box is the sum of chords, and rectangular
branch-and-bound (Falk-Soland) gives a certified lower bound on min H, hence a certified UPPER bound
on the edge. The vertex search (plateau_edge_vertex_search.py) supplies the incumbent (a lower bound
on the edge); this script closes the gap from above.

Node: a box [l, u] on y. Relaxation: LP over (pol, y) with the chord objective -> LB. The LP solution
is feasible, so H at it (after a few successive-linearization steps to a vertex) updates the
incumbent UB on min H. Branch on the (f, a) with the largest weighted chord gap, split at the LP
value. Best-first. Symmetry: the problem is invariant under joint relabelings of (f, e, a); only the
cheap fix of ordering y_00 >= y_11 >= ... is NOT applied (it would need care); the search is exact.

Usage: python plateau_edge_bnb.py [n] [s] [tol_aim] [seconds] [--workers K]
    tol_aim: stop when (edge_upper - edge_lower) < tol_aim. Prints the certified interval.
    --workers K: split the root box K ways on the largest-range variables and run subtrees in parallel
                 (multiprocessing); certified LB = min over subtrees.
"""
import sys, time, heapq, argparse, os
os.environ.setdefault('OMP_NUM_THREADS', '1')
import numpy as np
from scipy.optimize import linprog


def setup(n, s, symmetry=True):
    pF = np.full(n, 1 / n)
    C = np.full((n, n), s / n); C[np.arange(n), np.arange(n)] += 1 - s
    p_fe = pF[:, None] * C; p_e = p_fe.sum(0); q = (p_fe / p_e[None]).T       # q[e,f]
    N = n ** 3; M = n * n
    idx = lambda f, e, a: (f * n + e) * n + a
    yidx = lambda f, a: N + f * n + a
    rows, rhs = [], []
    for f in range(n):
        for e in range(n):
            r = np.zeros(N + M); r[[idx(f, e, a) for a in range(n)]] = 1; rows.append(r); rhs.append(1.0)
    for e in range(n):
        for a in range(n):
            r = np.zeros(N + M)
            for f in range(n):
                r[idx(f, e, a)] = q[e, f]
            rows.append(r); rhs.append(1.0 / n)
    for f in range(n):
        for a in range(n):
            r = np.zeros(N + M); r[yidx(f, a)] = -1.0
            for e in range(n):
                r[idx(f, e, a)] = C[f, e]
            rows.append(r); rhs.append(0.0)
    # symmetry breaking (valid: the problem is invariant under joint relabelings of f, e, a, which permute the
    # diagonal of y): require y_00 >= y_11 >= ... >= y_{n-1,n-1}
    A_ub, b_ub = [], []
    if symmetry:
        for f in range(n - 1):
            r = np.zeros(N + M); r[yidx(f, f)] = -1.0; r[yidx(f + 1, f + 1)] = 1.0
            A_ub.append(r); b_ub.append(0.0)
    return dict(n=n, s=s, pF=pF, C=C, N=N, M=M, A_eq=np.array(rows), b_eq=np.array(rhs),
                A_ub=np.array(A_ub) if A_ub else None, b_ub=np.array(b_ub) if b_ub else None, log2n=np.log2(n))


def phi(p):
    p = np.asarray(p, float)
    with np.errstate(divide='ignore', invalid='ignore'):
        return np.where(p > 1e-15, -p * np.log2(p), 0.0)


def H_of_y(P, y):
    return float((P['pF'][:, None] * phi(y.reshape(P['n'], P['n']))).sum())


def chord_coeffs(l, u):
    """Linear underestimator of phi on [l, u]: slope, intercept (per variable)."""
    w = u - l
    slope = np.where(w > 1e-12, (phi(u) - phi(l)) / np.maximum(w, 1e-12), 0.0)
    inter = phi(l) - slope * l
    return slope, inter


def lp_node(P, l, u):
    n, N, M = P['n'], P['N'], P['M']
    slope, inter = chord_coeffs(l, u)
    w = np.repeat(P['pF'], n)                                   # weight pF(f) for each (f,a)
    c = np.zeros(N + M); c[N:] = w * slope
    bounds = [(0, 1)] * N + list(zip(l, u))
    res = linprog(c, A_eq=P['A_eq'], b_eq=P['b_eq'], A_ub=P['A_ub'], b_ub=P['b_ub'], bounds=bounds, method='highs')
    if res.status != 0:
        return None, None
    lb = res.fun + float((w * inter).sum())
    # second valid bound from min-entropy: h(y_f) >= -log2 max_a y_fa >= -log2 max_a u_fa
    n = P['n']
    lb2 = float((P['pF'] * (-np.log2(np.maximum(u.reshape(n, n).max(1), 1e-15)))).sum())
    return max(lb, lb2), res.x


def polish(P, x, iters=30):
    """Successive linearization from a feasible point to a local vertex minimum of H (improves the incumbent)."""
    n, N, M = P['n'], P['N'], P['M']
    w = np.repeat(P['pF'], n)
    best = H_of_y(P, x[N:])
    for _ in range(iters):
        y = x[N:]
        g = -(np.log2(np.maximum(y, 1e-15)) + 1 / np.log(2)) * w
        c = np.zeros(N + M); c[N:] = g
        res = linprog(c, A_eq=P['A_eq'], b_eq=P['b_eq'], A_ub=P['A_ub'], b_ub=P['b_ub'], bounds=[(0, 1)] * (N + M), method='highs')
        if res.status != 0:
            break
        h = H_of_y(P, res.x[N:])
        if h >= best - 1e-12:
            break
        x, best = res.x, h
    return best, x


def bnb(P, l0, u0, ub_init, tol_H, budget, verbose=False, log_every=2000, max_open=3_000_000):
    """Best-first rectangular B&B on the box [l0, u0]. Returns (certified LB on min H, incumbent UB, best x, nodes)."""
    n, N = P['n'], P['N']
    w = np.repeat(P['pF'], n)
    UB, best_x = ub_init, None
    lb0, x0 = lp_node(P, l0, u0)
    if lb0 is None:
        return np.inf, UB, None, 0
    h0, x0p = polish(P, x0)
    if h0 < UB:
        UB, best_x = h0, x0p
    heap = [(lb0, 0, l0, u0)]; nodes = 1; t0 = time.time(); counter = 1
    LB = lb0
    cert = np.inf        # smallest lower bound among nodes discarded by the tolerance rule: the certificate must not exceed it
    while heap:
        LB = heap[0][0]
        if UB - LB < tol_H or time.time() - t0 > budget or len(heap) > max_open:
            break                                                  # (the open-node cap bounds memory: ~1 KB per node)
        lb, _, l, u = heapq.heappop(heap)
        if lb >= UB - tol_H:
            cert = min(cert, lb)
            continue
        _, x = lp_node(P, l, u)
        if x is None:
            continue
        y = x[N:]
        slope, inter = chord_coeffs(l, u)
        gap = w * (phi(y) - (slope * y + inter))                   # weighted chord gap per variable (phi >= chord)
        j = int(np.argmax(gap))
        if gap[j] < 1e-12:
            h = H_of_y(P, y)
            if h < UB:
                UB, best_x = h, x
            cert = min(cert, lb)                                   # relaxation exact on this box
            continue
        split = float(np.clip(y[j], l[j] + 1e-9, u[j] - 1e-9))
        for (lo, hi) in ((l[j], split), (split, u[j])):
            l2, u2 = l.copy(), u.copy(); l2[j], u2[j] = lo, hi
            lb2, x2 = lp_node(P, l2, u2)
            nodes += 1
            if lb2 is None:
                continue                                           # infeasible box: nothing to certify
            if lb2 >= UB - tol_H:
                cert = min(cert, lb2)
                continue
            h2 = H_of_y(P, x2[N:])
            if h2 < UB:
                h2p, x2p = polish(P, x2, iters=5)
                if h2p < UB:
                    UB, best_x = h2p, x2p
            counter += 1
            heapq.heappush(heap, (lb2, counter, l2, u2))
        if verbose and nodes % log_every < 2:
            print(f"    nodes {nodes:7d}  open {len(heap):6d}  LB {LB:.6f}  UB {UB:.6f}  "
                  f"edge in [{1-UB/P['log2n']:.5f}, {1-LB/P['log2n']:.5f}]  {time.time()-t0:.0f}s", flush=True)
    LB = min([h[0] for h in heap] + [cert, UB])                 # open nodes, tolerance-discarded nodes, incumbent
    return LB, UB, best_x, nodes


def run_sub(args):
    P, l, u, ub, tol_H, budget = args
    return bnb(P, l, u, ub, tol_H, budget)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('n', type=int, nargs='?', default=4); ap.add_argument('s', type=float, nargs='?', default=0.5)
    ap.add_argument('tol_aim', type=float, nargs='?', default=1e-3); ap.add_argument('seconds', type=float, nargs='?', default=600)
    ap.add_argument('--workers', type=int, default=1); ap.add_argument('--incumbent', type=float, default=None,
                    help='known edge lower bound (aim) from the vertex search, e.g. 0.334841 for (6,0.5)')
    a = ap.parse_args()
    P = setup(a.n, a.s)
    tol_H = a.tol_aim * P['log2n']
    l0 = np.zeros(P['M']); u0 = np.ones(P['M'])
    ub = (1 - a.incumbent) * P['log2n'] if a.incumbent is not None else np.inf
    t0 = time.time()
    print(f"plateau edge B&B: n={a.n} s={a.s} tol_aim={a.tol_aim} budget={a.seconds}s workers={a.workers}"
          + (f"  incumbent edge >= {a.incumbent}" if a.incumbent else ""), flush=True)
    if a.workers <= 1:
        LB, UB, x, nodes = bnb(P, l0, u0, ub, tol_H, a.seconds, verbose=True)
    else:
        # split the root K ways on the first variables (y_00, y_01, ...) into equal slabs
        import multiprocessing as mp, itertools
        K = a.workers
        # choose m variables with 2^m >= K ... use halving on successive variables
        boxes = [(l0.copy(), u0.copy())]
        j = 0
        while len(boxes) < K:
            new = []
            for (l, u) in boxes:
                mid = 0.5 * (l[j] + u[j])
                l2, u2 = l.copy(), u.copy(); u2[j] = mid; new.append((l2, u2))
                l3, u3 = l.copy(), u.copy(); l3[j] = mid; new.append((l3, u3))
            boxes = new; j = (j + 1) % P['M']
        # a quick incumbent from the root polish
        _, x0 = lp_node(P, l0, u0)
        h0, _ = polish(P, x0)
        ub = min(ub, h0)
        with mp.Pool(min(K, len(boxes))) as pool:
            outs = pool.map(run_sub, [(P, l, u, ub, tol_H, a.seconds) for (l, u) in boxes])
        LB = min(o[0] for o in outs); UB = min(o[1] for o in outs); nodes = sum(o[3] for o in outs)
        x = min((o for o in outs if o[2] is not None), key=lambda o: o[1], default=(None, None, None))[2]
    lo, hi = 1 - UB / P['log2n'], 1 - LB / P['log2n']
    print(f"\nn={a.n} s={a.s}: certified plateau edge in [{lo:.6f}, {hi:.6f}]  (width {hi-lo:.2e}; "
          f"{nodes} nodes; {time.time()-t0:.0f}s){'  CLOSED to tolerance' if hi-lo < a.tol_aim + 1e-12 else '  budget exhausted'}")
    if x is not None:
        y = x[P['N']:].reshape(P['n'], P['n'])
        print("incumbent P(A|F) rows:\n", np.round(y, 4))
    out = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results_exact', f'plateau_edge_bnb_n{a.n}_s{a.s}.txt')
    os.makedirs(os.path.dirname(out), exist_ok=True)
    with open(out, 'a', encoding='utf-8') as f:
        f.write(f"{time.strftime('%Y-%m-%d %H:%M')} n={a.n} s={a.s} tol_aim={a.tol_aim} budget={a.seconds}s workers={a.workers}: "
                f"edge in [{lo:.6f}, {hi:.6f}] nodes={nodes}\n")


if __name__ == '__main__':
    main()
