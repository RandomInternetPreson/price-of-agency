"""T18 (Theorem 5b in the book): the mistake-budget gate. Asymmetric error costs move the gate.

The agent sees E (its surroundings, reliability 1-s) and K (its own knowledge, fidelity e), over n options.
Loss: acting with the surroundings and being wrong costs 1; acting against them and being wrong costs kappa >= 1
(the arithmetic of living without a buffer: one wrong bet of your own means eviction). The agent minimizes expected loss.

When E and K agree there is nothing to decide. When they disagree, with posterior weights w_K, w_E and r on "neither":
    act on K  iff  kappa*(1 - w_K) < 1 - w_E   iff   kappa*(w_E + r) < w_K + r.
Writing X = e/(1-e) and Y = (1-s)/s, the three weights are proportional to 1 + nX, 1 + nY and n - 2, so
    act on K  iff  X > kappa*Y + (kappa - 1)*(1 - 1/n),
and the gate is
    e*(kappa) / (1 - e*(kappa)) = kappa*(1-s)/s + (kappa - 1)*(1 - 1/n).
kappa = 1 recovers e* = 1 - s exactly, and n cancels there (Theorem 5). For kappa > 1 it does not cancel: when both
sources are wrong the conformist pays 1 and the self-directed pays kappa, and with more options that case is more common.

CORRECTION, 2026-11-25. Earlier versions of this file printed e*(kappa) = kappa(1-s) / (s + kappa(1-s)), which is the
formula above without its second term, and "verified" it by testing the same inequality it was derived from. This file
now verifies by brute force: it builds the exact posterior for every pair of observations, lets the agent minimize
expected loss, and bisects on e for the point where the agent first acts against its surroundings.
"""
import numpy as np


def gate_closed(kappa, s, n):
    x = kappa * (1 - s) / s + (kappa - 1) * (1 - 1 / n)
    return max(0.0, x / (1 + x))


def acts_on_own_knowledge(e, kappa, s, n):
    pE = np.full((n, n), s / n); pE[np.arange(n), np.arange(n)] += 1 - s          # p(E = column | F = row)
    pK = np.full((n, n), (1 - e) / n); pK[np.arange(n), np.arange(n)] += e        # p(K = column | F = row)
    for eo in range(n):
        for ko in range(n):
            w = pE[:, eo] * pK[:, ko]; w = w / w.sum()                            # exact posterior over the future
            loss = [(1 - w[a]) if a == eo else kappa * (1 - w[a]) for a in range(n)]
            if int(np.argmin(loss)) != eo: return True
    return False


def gate_brute(kappa, s, n):
    lo, hi = 0.0, 1.0
    for _ in range(50):
        mid = (lo + hi) / 2
        if acts_on_own_knowledge(mid, kappa, s, n): hi = mid
        else: lo = mid
    return hi


worst = 0.0; cases = 0
for n in (2, 3, 4, 6, 8, 16, 64):
    for s in (0.2, 0.3, 0.5, 0.7):
        for kappa in (1, 1.5, 2, 3, 5, 10, 20):
            worst = max(worst, abs(gate_closed(kappa, s, n) - gate_brute(kappa, s, n))); cases += 1
print(f"closed form against brute force, {cases} worlds (n = 2..64, s = 0.2..0.7, kappa = 1..20): largest gap {worst:.1e}")

for s in (0.5, 0.3):
    print(f"\ns = {s}:")
    for kappa in (1, 2, 3, 5, 10, 20):
        print(f"  kappa={kappa:>2}: " + "  ".join(f"n={n}: {gate_closed(kappa, s, n):.4f} (brute {gate_brute(kappa, s, n):.4f})" for n in (2, 4, 8, 64)))

print()
for n in (2, 4, 8, 64):
    g = gate_closed(10, 0.5, n)
    print(f"reference kappa=10 s=0.5 n={n}: gate {g:.4f}; the knowledge is then right {g + (1 - g) / n:.4f} of the time")
x_inf = 10 * 0.5 / 0.5 + 9                                   # the closed form as n grows without bound
print(f"reference kappa=10 s=0.5 limit of many options: gate {x_inf / (1 + x_inf):.4f}")
print(f"reference kappa=1 s=0.5 any n: gate {gate_closed(1, 0.5, 8):.4f}")
print(f"the formula printed before 2026-11-25, kappa=10 s=0.5: {10 * 0.5 / (0.5 + 10 * 0.5):.4f}")
