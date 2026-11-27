"""
two_towns_aid.py -- a wall still standing in Chapter 11, taken down: THE TOWN IS ALONE.

Two towns, each Chapter 11's (nine boats, a good day needs five boatloads). AID: a town with more than five boatloads
sends its surplus to the other. With aid, town A's day is bad iff  on_A + max(0, on_B - 5) < 5.
Famine = three bad days running in a ninety-day season. Everything exact.

Arrangements of each town: k boats follow a master of accuracy q, 9 - k read at accuracy p. The two towns' masters are
either their OWN (independent of each other) or ONE master shared by both. Readers' errors are always their own.
Writes code/results/two_towns_aid.md
"""
import os
from math import comb
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); N, M, DAYS = 9, 5, 90


def run3(p):
    v = np.zeros(4); v[0] = 1
    for _ in range(DAYS):
        n = np.zeros(4); n[0] = (1 - p) * v[:3].sum(); n[1] = p * v[0]; n[2] = p * v[1]; n[3] = v[3] + p * v[2]; v = n
    return v[3]


def readers(n, p):
    return np.array([comb(n, j) * p ** j * (1 - p) ** (n - j) for j in range(n + 1)])


def town_dist(k, p, master_right):
    """distribution of boats on the fish given whether the master is right"""
    d = np.zeros(N + 1); r = readers(N - k, p)
    for j, pr in enumerate(r): d[j + (k if master_right else 0)] += pr
    return d


def bad_alone(k, p, q):
    return sum((q if mr else 1 - q) * town_dist(k, p, mr)[:M].sum() for mr in (True, False))


def bad_with_aid(k, p, q, shared):
    tot = 0.0
    for ma in (True, False):
        for mb in ((ma,) if shared else (True, False)):
            w = (q if ma else 1 - q) * (1.0 if shared else (q if mb else 1 - q))
            da = town_dist(k, p, ma); db = town_dist(k, p, mb)
            tot += w * sum(da[a] * db[b] for a in range(N + 1) for b in range(N + 1) if a + max(0, b - M) < M)
    return tot


def main():
    L = ["# Two towns (2026-11-10) — is a second town insurance, or a larger sameness?", "",
         "Each town: nine boats, five boatloads needed; a town sends its surplus over five to the other. Readers 70% (errors their own). "
         "Famine = three bad days running in ninety. Exact.", "",
         "## Followers behind a master in each town (master right 80% of days)", "",
         "| boats following, per town | one town alone | two towns, each its OWN master | two towns behind ONE master | what aid bought (own masters) | (one master) |", "|---|---|---|---|---|---|"]
    for k in range(0, 10):
        a = run3(bad_alone(k, 0.7, 0.8)); o = run3(bad_with_aid(k, 0.7, 0.8, False)); s = run3(bad_with_aid(k, 0.7, 0.8, True))
        L.append(f"| {k} | {100*a:.2f}% | {100*o:.2f}% | {100*s:.2f}% | ×{a/max(o,1e-12):.1f} lower | ×{a/max(s,1e-12):.1f} lower |")
    L += ["", "## The same at other master accuracies (famine; alone → own masters → one master)", "", "| boats following | q = 0.8 | q = 0.9 | q = 0.99 |", "|---|---|---|---|"]
    for k in (0, 1, 3, 5, 9):
        L.append(f"| {k} | " + " | ".join(f"{100*run3(bad_alone(k,0.7,q)):.2f}% → {100*run3(bad_with_aid(k,0.7,q,False)):.2f}% → {100*run3(bad_with_aid(k,0.7,q,True)):.2f}%" for q in (0.8, 0.9, 0.99)) + " |")
    b0 = bad_alone(0, 0.7, 0.8); b1 = bad_with_aid(0, 0.7, 0.8, False)
    L += ["", "## Reading",
          f"- Two towns of readers: bad days fall from {100*b0:.1f}% to {100*b1:.2f}%, famine from {100*run3(b0):.1f}% to {100*run3(b1):.3f}%. A reading town fails by a boat or two, and a neighbor's surplus covers a boat or two.",
          "- Two towns each wholly behind its own master: aid buys nothing. A herd fails all at once — no boats on the fish — and a neighbor's whole surplus (four boatloads) cannot replace five.",
          "- Two towns behind one master fail on the same days; whatever aid could have bought, there is no surplus on the day it is needed.",
          "- So a transfer is worth exactly what the sameness between giver and receiver leaves it: inside one town on a bad day, nothing (the transfer lemma); "
          "between towns whose errors are their own, almost everything; between towns that follow the same voice, nothing again."]
    os.makedirs(os.path.join(HERE, 'results'), exist_ok=True)
    open(os.path.join(HERE, 'results', 'two_towns_aid.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
