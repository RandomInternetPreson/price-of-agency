"""calculator_model.py -- the model inside web/calculator.html, in Python, so that the page's numbers can be checked.

The page joins two of the book's gates in one small world and adds nothing else.

  Theorem 16 (the time gate; code/iterative_time_T16.py). A future F, one of n = 4, uniform. The situation E names F
  with probability 1 - s (s = 0.5), otherwise something uniform. Knowledge arrives in sittings: each sitting kept is a
  glimpse G that names F with probability g = 0.35, otherwise something uniform, independent given F.
  Theorem 5b (the mistake-budget gate; code/mistake_budget_T18.py). Acting with the situation and being wrong costs 1;
  acting against it and being wrong costs kappa. The agent minimizes expected loss.

For t sittings kept the agent's posterior is exact, and so is everything reported: whether it ever acts on its own
knowledge (the gate, in sittings), how often its action is right, and the two rulers of Chapter 4
(independence H(A|E)/log n and aim I(A;F)/log n). At kappa = 1 the numbers are those of iterative_time_T16.py. With one
glimpse of fidelity e in place of the sittings, the gate is Theorem 5b's closed form.

A person on a schedule keeps each booked sitting with some probability. The page books one sitting a week with the
times set at sign-up, so sitting j is a plan made j weeks ahead and each sitting has its own probability of being kept;
cohort() takes one probability or a list of them.

The page adds one supposition that is not the book's: the course ends in a certificate, and the certificate goes to
whoever kept every sitting. A person who kept all T acts with the knowledge of T sittings; a person who missed one acts
as if there had been no course (t = 0). A cohort's rulers are computed on that two-part mixture (the observer of
independence sees the situation, not who finished). In the book's own model every sitting kept adds something; the
tables by sittings kept, below, are that model.

The page's ninth question (how much a shift leaves for learning) scales what one sitting teaches: g = 0.35 for "as much
as on a day off", 0.175 for "about half", 0.0875 for "very little". That a tired person learns less in exact proportion
is the page's supposition and is printed on it; the gate that follows from each g is exact.

    python code/calculator_model.py          prints the tables the page uses and the checks against the two scripts
"""
import numpy as np
from math import comb, log2

N_OPT, S_WORLD, G_SIT = 4, 0.5, 0.35


def compositions(t, n):
    if n == 1:
        yield (t,); return
    for k in range(t + 1):
        for rest in compositions(t - k, n - 1): yield (k,) + rest


def multinomial(c):
    out, left = 1, sum(c)
    for k in c: out *= comb(left, k); left -= k
    return out


def joint(t, kappa, n=N_OPT, s=S_WORLD, g=G_SIT):
    """J[f, e, a]: exact joint of future, situation and action after t sittings, for a loss-minimizing agent."""
    pE = np.full((n, n), s / n); pE[np.arange(n), np.arange(n)] += 1 - s
    pG = np.full((n, n), (1 - g) / n); pG[np.arange(n), np.arange(n)] += g
    J = np.zeros((n, n, n))
    for e in range(n):
        for c in compositions(t, n):
            like = np.array([pE[f, e] * np.prod(pG[f, :] ** np.array(c)) for f in range(n)]) / n    # p(f, e, glimpse counts) up to the multinomial
            w = like / like.sum()
            alt = max((a for a in range(n) if a != e), key=lambda a: (w[a], -a))                    # best alternative, lowest index on ties (as np.argmax)
            a = alt if kappa * (1 - w[alt]) < (1 - w[e]) else e
            J[:, e, a] += multinomial(c) * like
    return J


def H(p):
    p = np.asarray(p, float).ravel(); p = p[p > 1e-15]
    return float(-(p * np.log2(p)).sum())


def rulers(J):
    n = J.shape[0]
    p_ea = J.sum(0); p_fa = J.sum(1)
    return {'independence': (H(p_ea) - H(p_ea.sum(1))) / log2(n), 'aim': (H(p_fa.sum(1)) + H(p_fa.sum(0)) - H(p_fa)) / log2(n),
            'right': float(sum(J[f, :, f].sum() for f in range(n))), 'own': float(1 - sum(J[:, e, e].sum() for e in range(n)))}


def gate_sittings(kappa, tmax=40, **kw):
    for t in range(tmax + 1):
        if rulers(joint(t, kappa, **kw))['own'] > 1e-12: return t
    return None


def kept(ps):
    """the distribution of the number of sittings kept when sitting j is kept with probability ps[j]"""
    d = np.array([1.0])
    for q in ps: d = np.append(d * (1 - q), 0.0) + np.append(0.0, d * q)
    return d


def cohort(T, p, kappa, g=G_SIT):
    """T sittings booked, kept with probability p (one number, or one per sitting). The course counts only when finished."""
    ps = [p] * T if np.isscalar(p) else list(p)
    assert len(ps) == T
    finished = float(kept(ps)[T])
    J = finished * joint(T, kappa, g=g) + (1 - finished) * joint(0, kappa, g=g)
    out = rulers(J); out['finished'] = finished
    return out


if __name__ == '__main__':
    print('check 1: kappa = 1 against iterative_time_T16.py (its printed values, to six places)')
    T16 = [(0.0, 0.625), (0.0, 0.625), (0.459326, 0.673984), (0.597637, 0.715193), (0.635022, 0.744328), (0.654867, 0.773274), (0.690388, 0.800314)]
    for t in range(7):
        r = rulers(joint(t, 1)); same = abs(r['independence'] - T16[t][0]) < 1e-6 and abs(r['right'] - T16[t][1]) < 1e-6
        print(f'  T {t} delta_A {r["independence"]:.6f} acc {r["right"]:.6f}  {"same" if same else "accuracy same; independence differs in the third or fourth place (ties, see below)"}')
        assert abs(r['right'] - T16[t][1]) < 1e-6 and (same or t >= 5)
    print('  At 5 and 6 sittings some glimpse sequences leave two options exactly tied (108 and 180 of them). This file gives a tie')
    print('  to the lower-numbered option. iterative_time_T16.py multiplies in sequence order, so rounding breaks its ties one way')
    print('  or the other. The book prints neither value.')
    print('check 2: one glimpse of fidelity e in place of the sittings; the gate against Theorem 5b, n = 4, s = 0.5')
    for kappa in (1, 2, 5, 10):
        lo, hi = 0.0, 1.0
        for _ in range(40):
            mid = (lo + hi) / 2
            if rulers(joint(1, kappa, g=mid))['own'] > 1e-12: hi = mid
            else: lo = mid
        x = kappa * (1 - S_WORLD) / S_WORLD + (kappa - 1) * (1 - 1 / N_OPT)
        print(f'  kappa={kappa:>2}: gate by this model {hi:.4f}; Theorem 5b {x / (1 + x):.4f}')
        assert abs(hi - x / (1 + x)) < 1e-6
    print('the gate in sittings, by mistake ratio (n = 4, s = 0.5, g = 0.35)')
    for kappa in (1, 1.5, 2, 3, 5, 10, 20):
        print(f'  kappa={kappa:>4}: {gate_sittings(kappa)} sittings')
    print('the gate in sittings when a sitting teaches less (the page\'s ninth question)')
    for g in (0.35, 0.175, 0.0875):
        print(f'  g={g}: ' + ', '.join(f'kappa={kappa}: {gate_sittings(kappa, g=g)}' for kappa in (1, 2, 5, 10)))
    print('by sittings kept: acts on own knowledge, right, independence, aim')
    for kappa in (1, 2, 5, 10):
        for t in range(0, 13):
            r = rulers(joint(t, kappa)); print(f'  kappa={kappa:>2} t={t:>2}: own {r["own"]:.4f} right {r["right"]:.4f} independence {r["independence"]:.4f} aim {r["aim"]:.4f}')
    print('a cohort: 6 sittings booked, each kept with probability p; the course counts only when all 6 are kept')
    for kappa in (1, 5, 10):
        for p in (0.3, 0.6, 0.9, 1.0):
            r = cohort(6, p, kappa); print(f'  kappa={kappa:>2} p={p:.1f}: finished {r["finished"]:.4f} right {r["right"]:.4f} independence {r["independence"]:.4f} aim {r["aim"]:.4f}')
    print('a cohort whose sittings are kept with different probabilities (the first two certain, the rest 0.68), and one that learns half as much')
    for kappa in (1, 10):
        for g in (0.35, 0.175):
            r = cohort(6, [1, 1, 0.68, 0.68, 0.68, 0.68], kappa, g=g); print(f'  kappa={kappa:>2} g={g}: finished {r["finished"]:.4f} right {r["right"]:.4f} independence {r["independence"]:.4f} aim {r["aim"]:.4f}')
