"""
adversary_2026-10-24.py -- three of the six attacks in the Gemini adversarial review
are computable inside the book's own models. Run them, exactly, and let them land or not.

 A3  Fishing town (T13): is the Harbor Master beaten only because he is forbidden to hedge?
     Compare, on BOTH survival metrics of Ch 11 (majority famine: <5 of 9 boats find fish on
     3 consecutive days; total failure: 0 boats, 3 days): all-in master, hedged master
     (6-1-1-1 on his posterior), nine independent fishers, and a master who polls the nine
     independent readings and dispatches on the majority (information kept, allocation
     centralized).
 A4  Ledger of imposition (T17): the printed 93.4% assumes unabsorbed variance is BROADCAST
     to every subordinate. Recompute under PARTITION (residual split 1/b among children) and
     under the entropy accounting that the book actually prices (schedule uncertainty: when
     k of N shifts are cut at random, every one of the N faces the uncertainty while only k
     bear the magnitude).
 A5  [SUPERSEDED 2026-11-25 by code/mistake_ratio_noisy_self_knowledge.py: this section labels thresholds by T18's
     formula as it stood before that date's correction. Its three readings were confirmed by the recomputation.]
     Mistake-budget gate (T18): with noisy self-knowledge e_hat = e + eps, is kappa > 1 the
     Bayesian safety margin? Find the accuracy-maximizing kappa* as a function of the noise
     and the world's clarity s.
"""
import numpy as np
from math import comb, log2

# ---------------------------------------------------------------- A3
n, N, s, e, hub, DAYS, ST = 4, 9, 0.5, 0.6, 0.8, 90, 3
acc = e + (1 - e) / n                     # independent fisher accuracy on the right ground: 0.70


def streak_prob(pf, st=ST, days=DAYS):
    M = np.zeros((st + 1, st + 1))
    for k in range(st):
        M[k, 0] = 1 - pf; M[k, k + 1] = pf
    M[st, st] = 1; v = np.zeros(st + 1); v[0] = 1
    for _ in range(days):
        v = v @ M
    return v[st]


def binom_lt(p, Nn, need):            # P(fewer than `need` successes)
    return sum(comb(Nn, k) * p ** k * (1 - p) ** (Nn - k) for k in range(need))


def a3():
    print("A3  fishing town: who is really being compared?")
    print(f"    {'policy':46s} {'P(day<5 boats)':>15s} {'majority famine':>16s} {'P(day 0 boats)':>15s} {'total-failure famine':>21s}")
    rows = []
    # all-in master: right w.p. 0.8 -> 9 boats; wrong -> 0 boats
    rows.append(("master, all 9 boats on his pick", 1 - hub, 1 - hub))
    # hedged master 6-1-1-1: right -> 6 boats (>=5 ok); wrong -> the right ground has exactly 1 boat
    rows.append(("master, hedged 6-1-1-1 on his posterior", 1 - hub, 0.0))
    # hedged master 5-2-1-1: right -> 5; wrong -> right ground has 2 or 1 boat
    rows.append(("master, hedged 5-2-1-1", 1 - hub, 0.0))
    # nine independent fishers
    rows.append(("nine independent fishers (0.70 each)", binom_lt(acc, N, 5), (1 - acc) ** N))
    # master polls the nine independent readings, dispatches ALL boats on the majority
    rows.append(("master polls 9 independent readings, all-in", binom_lt(acc, N, 5), binom_lt(acc, N, 5)))
    # same master, hedged 6-1-1-1 on the majority
    rows.append(("master polls 9 readings, hedged 6-1-1-1", binom_lt(acc, N, 5), 0.0))
    for name, pmaj, ptot in rows:
        print(f"    {name:46s} {pmaj:15.3f} {streak_prob(pmaj):16.3f} {ptot:15.2e} {streak_prob(ptot):21.3f}")
    print("    Reading: hedging changes NOTHING on the majority metric (a master with one signal cannot put >=5 boats on two")
    print("    grounds); it buys total-failure insurance, which is Lesson 5's wildcard by another route. What beats the master")
    print("    is nine independent READINGS, whoever dispatches. The comparison in T13 is information structure, not who")
    print("    decides -- and the living town (S1) is where centralized dispatch bites: fishers who watch the hub stop reading.\n")


# ---------------------------------------------------------------- A4
def cascade(mode, L=4, b=4, sigma=100.0, cap=(60.0, 20.0, 6.0, 1.0), elast=(0.008, 0.02, 0.1, 0.565)):
    heads = np.array([b ** l for l in range(L)]); cap = np.array(cap); elast = np.array(elast)
    faced = np.zeros(L); resid = sigma
    for l in range(L):
        faced[l] = resid
        absorbed = min(resid, cap[l])
        resid = resid - absorbed
        if mode == 'partition':
            resid = resid / b                 # split among the b children
    loss_pc = faced * elast; loss_total = loss_pc * heads
    return faced, loss_pc, loss_total


def a4():
    print("A4  ledger of imposition: broadcast vs partition")
    for mode in ['broadcast', 'partition']:
        faced, pc, tot = cascade(mode)
        share = tot[-1] / tot.sum() if tot.sum() > 0 else float('nan')
        print(f"    {mode:10s} faced/person by level {np.round(faced, 2)}  worker share of agency loss = {share:.1%}")
    # entropy accounting: k of N shifts cut at random
    print("    Entropy accounting (what Ch 13 prices as schedule entropy): a shortfall of k of N shifts, assigned at random:")
    for N_, k in [(20, 2), (20, 5), (64, 8)]:
        h = -(k / N_) * log2(k / N_) - (1 - k / N_) * log2(1 - k / N_)
        print(f"      N={N_:3d} k={k:2d}: magnitude borne = {k} shift-units (partitioned); uncertainty faced = {N_} x h({k}/{N_}) = {N_ * h:.1f} bits (broadcast to all {N_})")
    print("    Reading: the 93.4% is the broadcast regime. Under pure partition at the printed capacities the hierarchy absorbs")
    print("    everything before the worker level (the regional's 20 units of capacity swallow a 10-unit share). The book's")
    print("    ledger prices UNCERTAINTY (schedule entropy), which does broadcast -- every worker faces 'will I be cut?' --")
    print("    while the MAGNITUDE (lost hours) partitions. T17 must say which it counts; as printed it says 'variance'.\n")


# ---------------------------------------------------------------- A5
def a5():
    print("A5  mistake-budget gate with noisy self-knowledge: the accuracy-maximizing kappa*")
    rng = np.random.default_rng(0)
    M = 400_000
    e_true = rng.uniform(0, 1, M)
    print(f"    {'s':>5s} {'gate 1-s':>9s} " + " ".join(f"sigma={sg:<4.2f}" for sg in [0.0, 0.05, 0.1, 0.2, 0.3]))
    for s_ in [0.3, 0.5, 0.7]:
        line = f"    {s_:5.2f} {1 - s_:9.2f} "
        for sg in [0.0, 0.05, 0.1, 0.2, 0.3]:
            e_hat = np.clip(e_true + rng.normal(0, sg, M), 0, 1)
            # on a disagreement between K and E: P(K right) = e s / (e s + (1-e)(1-s)); conform is right with the complement
            pK = e_true * s_ / (e_true * s_ + (1 - e_true) * (1 - s_))
            best = None
            for kappa in np.exp(np.linspace(np.log(0.05), np.log(50), 400)):
                thr = kappa * (1 - s_) / (s_ + kappa * (1 - s_))
                defect = e_hat > thr
                accuracy = np.where(defect, pK, 1 - pK).mean()
                if best is None or accuracy > best[1]:
                    best = (kappa, accuracy)
            line += f"  {best[0]:8.2f}  "
        print(line)
    print("    Reading: kappa* = 1 exactly when the gate sits at the population's mean self-knowledge (s = 0.5); above 1 in")
    print("    CLEAR worlds (s = 0.3: the gate is high, noisy estimates regress to the mean, a margin protects accuracy);")
    print("    BELOW 1 in noisy worlds (s = 0.7). The 'Bayesian necessity of kappa > 1' is a statement about clear worlds")
    print("    with a uniform population -- and the sign flips where the book's time-poor live. Externalized losses are a")
    print("    separate ledger (who pays), not a correction to the gate.\n")


if __name__ == "__main__":
    a3(); a4(); a5()
