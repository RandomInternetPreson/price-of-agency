"""plateau_hit_rate_bound.py -- how often a perfectly unreadable agent can be right, against the captain.

Chapter 6 section 2: Ines wins "not more than the captain who simply follows the table's tells, unless those tells are
noise more than half the time".

World of Chapter 4: a future F, one of n, uniform; the situation E names F with probability 1 - s and is otherwise
uniform. The agent knows F and sees E. Perfectly unreadable means the action is uniform given every E.

Claim.  max over perfectly unreadable strategies of P(A = F)  =  1/n + s(n-1)/n,
        the captain (A = E) is right                             1 - s + s/n,
        and the first exceeds the second exactly when s > 1/2, for every n.

Proof of the bound.  Fix E = e. For each action a,  P(A = a | e) = 1/n  >=  P(F = a | e) P(A = a | e, F = a),
so the hit rate given e is at most  sum_a min(P(F = a | e), 1/n) = 1/n + (n-1) s/n   (one entry of P(F | e) is
1 - s + s/n >= 1/n, the other n - 1 are s/n <= 1/n). The strategy "act on F when the situation is wrong; when it is
right, scatter so the pattern is uniform" (Chapter 6 section 4) attains it.

This file checks the claim without using the proof: for each world it maximizes the hit rate by linear programming over
every strategy P(A | E, F) with A uniform given E.
"""
import numpy as np
from scipy.optimize import linprog


def best_hidden_hit_rate(n, s):
    # by symmetry one situation e = 0 suffices; variables x[f, a] = P(A = a | e, F = f)
    pf = np.full(n, s / n); pf[0] += 1 - s
    c = np.zeros((n, n))
    for f in range(n): c[f, f] = -pf[f]
    A_eq, b_eq = [], []
    for f in range(n):                                   # rows sum to one
        row = np.zeros((n, n)); row[f, :] = 1; A_eq.append(row.ravel()); b_eq.append(1.0)
    for a in range(n):                                   # the action is uniform given e
        row = np.zeros((n, n)); row[:, a] = pf; A_eq.append(row.ravel()); b_eq.append(1.0 / n)
    r = linprog(c.ravel(), A_eq=np.array(A_eq), b_eq=np.array(b_eq), bounds=(0, 1), method='highs')
    assert r.success
    return -r.fun


if __name__ == '__main__':
    worst, crossings = 0.0, []
    print('  n     s   best hidden   closed form   captain')
    for n in (2, 3, 4, 6, 8, 16):
        for s in (0.1, 0.3, 0.45, 0.5, 0.55, 0.7, 0.9):
            lp, closed, cap = best_hidden_hit_rate(n, s), 1 / n + s * (n - 1) / n, 1 - s + s / n
            worst = max(worst, abs(lp - closed))
            assert (lp > cap + 1e-9) == (s > 0.5) and (abs(lp - cap) < 1e-9) == (s == 0.5)
            if n in (2, 6): print(f'  {n:>2}  {s:.2f}   {lp:.4f}        {closed:.4f}        {cap:.4f}')
    print(f'closed form against linear program, 42 worlds: largest gap {worst:.1e}')
    print('the hidden agent is right more often than the captain exactly when s > 1/2: true in 42 of 42 worlds')
