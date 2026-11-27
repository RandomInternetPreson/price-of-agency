"""
adversary_round4.py -- the computable claims in the Gemini (8 attacks) and ChatGPT (10 objections)
reviews of v0.25. Each block states the claim, computes, and prints the reading.

 C2  ChatGPT 2: Proposition 13.1 counterexample (B = 1 xor A xor E xor Z). Verify the numbers; then
     test the conditional quantities I(B;F|E) vs I(A;F|E) -- is the lower wall the Goodhart-immune
     statistic?
 C5  ChatGPT 5: the "seventy-fold" is a ratio of elasticities; compute the ratio of PER-UNIT returns
     dQ/dbeta at the two operating points of Theorem 10(iii), using the book's own overt-agent model.
 G3  Gemini 3: tiering vs pooling under the book's actual time->competence curve (concave above the
     gate): where is the boundary at which concentrating the shortfall stops being better?
 G5  Gemini 5: real-sea defection inequality 0.7 V > 0.8 V/k; does pooling a fraction phi of the catch
     re-herd the town? With and without a cost of independent reading.
 C9  ChatGPT 9: per-signal gates (Theorem 5c) on a random channel -- is the aggregate activation vs
     education still a step, or does it smooth out?
"""
import sys, os, itertools
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(HERE, '..'))
sys.path.insert(0, HERE)


def H(p):
    p = np.asarray(p, float).ravel(); p = p[p > 1e-15]
    return float(-(p * np.log2(p)).sum())


# ------------------------------------------------------------------ C2
print("C2  Proposition 13.1 counterexample, verified by enumeration")
# F fair bit; E = F w.p. 3/4; A = F xor E; Z ~ Bern(1/8); B = 1 xor A xor E xor Z
P = {}
for f in (0, 1):
    for e in (0, 1):
        pe = 0.75 if e == f else 0.25
        a = f ^ e
        for z in (0, 1):
            pz = 0.125 if z else 0.875
            b = 1 ^ a ^ e ^ z
            P[(f, e, a, b)] = P.get((f, e, a, b), 0) + 0.5 * pe * pz
def marg(keys):
    out = {}
    for k, v in P.items():
        kk = tuple(k[i] for i in keys); out[kk] = out.get(kk, 0) + v
    return np.array(list(out.values()))
def Hm(keys): return H(marg(keys))
iF, iE, iA, iB = 0, 1, 2, 3
HF = Hm([iF]); HE = Hm([iE])
for name, iX in [('A', iA), ('B', iB)]:
    dA = (Hm([iE, iX]) - HE) / 1.0                       # log2|A| = 1
    aim = (HF + Hm([iX]) - Hm([iF, iX])) / HF
    aim_c = (Hm([iE, iX]) - HE + Hm([iF, iE]) - Hm([iF, iE, iX])) / HF   # I(X;F|E)/H(F)
    succ = sum(v for k, v in P.items() if k[iX] == k[iF])
    print(f"    {name}: independence {dA:.4f}  aim {aim:.4f}  I(.;F|E)/H(F) {aim_c:.4f}  P(match F) {succ:.3f}")
print("    Reading: the reviewer's numbers reproduce (0.811/0 -> 0.896/0.456). Unconditional aim rose because the")
print("    processor used E, which carries future information on its own; A xor E recovers F. The CONDITIONAL")
print("    aim I(.;F|E) -- the lower wall of Theorem 9' -- FELL (0.811 -> 0.353): data processing holds given E.")
print("    So P13.1 as printed is false for processors that may use E; the immune statistic is the conditional one.\n")

# ------------------------------------------------------------------ C5
print("C5  seventy-fold: elasticities vs per-unit returns (overt agent, e=0.7, s=0.5)")
import theft_equilibrium as te   # the book's own model (prints its own tables on import)
def comp(beta): return te.overt_metrics(0.7, beta, 0.5)[0]
for b in (6.0, 20.0):
    h = 0.02; el = (np.log(comp(b * np.exp(h))) - np.log(comp(b * np.exp(-h)))) / (2 * h)
    dq = (comp(b + 0.01) - comp(b - 0.01)) / 0.02
    print(f"    beta={b:4.0f}: competence {comp(b):.4f}  elasticity {el:.3f}  dQ/dbeta {dq:.5f}")
e6 = (np.log(comp(6 * np.exp(0.02))) - np.log(comp(6 * np.exp(-0.02)))) / 0.04
e20 = (np.log(comp(20 * np.exp(0.02))) - np.log(comp(20 * np.exp(-0.02)))) / 0.04
d6 = (comp(6.01) - comp(5.99)) / 0.02; d20 = (comp(20.01) - comp(19.99)) / 0.02
print(f"    ratio of elasticities {e6 / e20:.1f};  ratio of per-unit returns dQ/dbeta {d6 / d20:.1f}")
print("    Reading: the reviewer is right that the two ratios differ; the per-unit ratio is what 'an hour returned'")
print("    means, and it is the number to print.\n")

# ------------------------------------------------------------------ G3
print("G3  tiering vs pooling on the book's time->competence curve (concave above the gate)")
# treat deliberation beta as the time budget; a shortfall removes dbeta from the affected workers.
# pool: everyone loses the same small amount; tier: k workers lose k-fold more, the rest nothing.
def loss_total(betas, cut_list):
    return sum(comp(b) - comp(b - c) for b, c in zip(betas, cut_list))
N, k = 20, 2
for beta0 in (6.0, 8.0, 12.0, 20.0):
    for total_cut in (4.0, 10.0, 20.0):
        pool = loss_total([beta0] * N, [total_cut / N] * N)
        tier = loss_total([beta0] * N, [total_cut / k] * k + [0.0] * (N - k))
        tier_paid = loss_total([beta0 + total_cut / k] * k + [beta0] * (N - k), [total_cut / k] * k + [0.0] * (N - k))  # tier compensated back to beta0 beforehand
        print(f"    beta0={beta0:4.0f} total cut={total_cut:4.0f}:  pool loss {pool:.4f}   tier loss {tier:.4f}   tier-paid loss {tier_paid:.4f}   -> {'tier' if tier < pool else 'POOL'} wins unpaid; {'tier' if tier_paid < pool else 'POOL'} wins paid")
print("    Reading: above the gate the curve is concave and pooling wins (Jensen), exactly as the reviewer says;")
print("    tiering wins when the pooled cut would drag the whole pool toward the gate, or when the tier is paid")
print("    enough to sit on the flat part of the curve beforehand. Rule 7 needs its boundary condition.\n")

# ------------------------------------------------------------------ G5
print("G5  real-sea defection inequality with pooling fraction phi and a cost c of reading independently")
V = 1.0; acc_i, acc_h = 0.7, 0.8
print(f"    {'k (boats on the hub ground)':>28s} {'phi=0':>8s} {'phi=0.5':>8s} {'phi=0.9':>8s}  (independent payoff minus follower payoff, c=0)")
for k in (1, 2, 3, 5, 9):
    row = []
    for phi in (0.0, 0.5, 0.9):
        ind = acc_i * (1 - phi) * V; fol = acc_h * (1 - phi) * V / k
        row.append(ind - fol)
    print(f"    {k:28d} " + " ".join(f"{x:8.3f}" for x in row))
print("    With c > 0 the independent fisher defects iff (1-phi) V (0.7 - 0.8/k) > c, i.e. phi < 1 - c/(V(0.7-0.8/k)):")
for k in (2, 5, 9):
    for c in (0.05, 0.2):
        print(f"      k={k} c={c}: phi* = {1 - c / (V * (acc_i - acc_h / k)):.2f}")
print("    Reading: pooling a fraction of the catch does not change the ranking (phi cancels); only full pooling,")
print("    or a reading cost that the private residual no longer covers, re-herds the town. Crowding penalty is")
print("    needed; winner-take-all is not (k >= 2 suffices). 'Keep wildcards fed' is a transfer to a few, not pooling.\n")

# ------------------------------------------------------------------ C9
print("C9  aggregate gate on a random channel (Theorem 5c thresholds spread across signals)")
rng = np.random.default_rng(7)
n = 6
for trial in range(3):
    pF = rng.dirichlet(np.ones(n)); C = rng.dirichlet(np.ones(n) * 0.8, size=n)
    p_fe = pF[:, None] * C; p_e = p_fe.sum(0); q = (p_fe / p_e[None]).T
    es = np.linspace(0.01, 0.99, 99); frac = []
    for e in es:
        # fraction of (signal, K-reading) disagreements in which the agent defects, weighted by their probability
        tot = 0.0; act = 0.0
        for esig in range(n):
            fE = int(np.argmax(q[esig]))
            for k in range(n):
                if k == fE: continue
                pk = sum(q[esig, f] * ((e if f == k else 0) + (1 - e) / n) for f in range(n))
                w = p_e[esig] * pk
                thr = (q[esig, fE] - q[esig, k]) / (q[esig, fE] + (n - 1) * q[esig, k])
                tot += w; act += w * (e > thr)
        frac.append(act / tot)
    frac = np.array(frac); jumps = np.diff(frac)
    print(f"    channel {trial}: activation goes 0 -> {frac[-1]:.2f} over e; largest single step {jumps.max():.3f}; "
          f"steps > 0.05: {(jumps > 0.05).sum()}; thresholds span [{min((q[es_,int(np.argmax(q[es_]))]-q[es_,k])/(q[es_,int(np.argmax(q[es_]))]+(n-1)*q[es_,k]) for es_ in range(n) for k in range(n) if k!=int(np.argmax(q[es_]))):.2f}, "
          f"{max((q[es_,int(np.argmax(q[es_]))]-q[es_,k])/(q[es_,int(np.argmax(q[es_]))]+(n-1)*q[es_,k]) for es_ in range(n) for k in range(n) if k!=int(np.argmax(q[es_]))):.2f}]")
print("    Reading: per decision the gate is a step; across a channel whose signals point with different confidence")
print("    the aggregate activation is a staircase of small steps -- smooth-looking if the thresholds spread. The")
print("    knife edge is a per-decision fact; the aggregate dead zone is a property of the symmetric class.")
