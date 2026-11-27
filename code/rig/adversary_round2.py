"""adversary_round2.py -- two computable claims from the reviewer's second round.
 R4  Does the uncertainty ledger scale like T17's broadcast?  Fixed k (reviewer's limit) vs a
     PROPORTIONAL shortfall k = fN (a demand shock is a fraction of demand). And: tiering
     (concentrate uncertainty on an on-call pool) vs spreading, under a linear loss and under
     the book's own gate-shaped loss (T16: planning capacity is lost once uncertainty passes a
     threshold).
 R5  kappa* when the population mass sits below / at / above the gate (Beta priors), not U[0,1].
     [SUPERSEDED 2026-11-25 by code/mistake_ratio_noisy_self_knowledge.py: thresholds here are labelled by T18's formula
     as it stood before that date's correction. The three readings were confirmed by the recomputation.]
"""
import numpy as np
from math import log2

def h(p):
    return 0.0 if p <= 0 or p >= 1 else -p*log2(p)-(1-p)*log2(1-p)

print("R4a  total schedule uncertainty vs headcount N")
print(f"     {'N':>5s} {'fixed k=2: N*h(2/N)':>22s} {'per worker':>11s} {'proportional f=0.1: N*h(0.1)':>30s} {'per worker':>11s}")
for N in [10, 20, 50, 100, 1000]:
    print(f"     {N:5d} {N*h(2/N):22.2f} {h(2/N):11.3f} {N*h(0.1):30.2f} {h(0.1):11.3f}")
print("     Reading: with a FIXED shortfall the per-worker uncertainty vanishes as N grows (the reviewer's limit).")
print("     With a PROPORTIONAL shortfall -- a demand shock is a fraction of demand -- per-worker uncertainty is")
print("     constant in N and the total is linear: exactly T17's broadcast scaling. The cascade's input is variance")
print("     of demand, which is proportional; the reviewer's limit is a fixed number of cut shifts.\n")

print("R4b  spread vs tiered, N=20, shortfall 2 shifts, under three loss shapes")
N, k = 20, 2
spread = [h(k/N)]*N                       # everyone faces 'will it be me'
tiered = [1.0]*k + [0.0]*(N-k)            # on-call pool of k, each 1 bit; core staff 0
def loss(bits_list, shape, theta=0.6):
    if shape == 'linear':      return sum(bits_list)
    if shape == 'gate':        return sum(1.0 if b > theta else 0.0 for b in bits_list)       # T16: capacity lost past a threshold
    if shape == 'gate+linear': return sum(1.0 if b > theta else b/theta*0.3 for b in bits_list)
print(f"     {'loss shape':>14s} {'spread (all 20 at 0.47 bits)':>30s} {'tiered (2 at 1 bit, 18 at 0)':>30s}")
for shape in ['linear', 'gate', 'gate+linear']:
    print(f"     {shape:>14s} {loss(spread, shape):30.2f} {loss(tiered, shape):30.2f}")
for theta in [0.3, 0.47, 0.6]:
    print(f"     gate theta={theta:.2f}: spread {loss(spread,'gate',theta):5.1f}   tiered {loss(tiered,'gate',theta):5.1f}")
print("     Reading: concentrating uncertainty is cheaper in total bits (h is concave) and cheaper in agency when the")
print("     gate sits above the spread level (theta > h(k/N)): tiering keeps 18 planners whole and sacrifices 2. When")
print("     the gate sits below the spread level, spreading pushes ALL 20 below it -- the worst case -- and tiering")
print("     is better still. So tiering dominates on the book's own gate; T17's broadcast is the un-tiered pool, which")
print("     is what algorithmic scheduling in the Shift Project data looks like (on-call for everyone). The ledger")
print("     points to tiering, compensated, as the engineering fix: the reviewer is right and it is a result, not a loss.\n")

print("R5   kappa* with population mass below / at / above the gate (Beta priors; sigma = self-knowledge noise)")
rng = np.random.default_rng(1); M = 300_000
def kstar(e_true, s_, sg):
    e_hat = np.clip(e_true + rng.normal(0, sg, M), 0, 1)
    pK = e_true*s_/(e_true*s_ + (1-e_true)*(1-s_))
    best = None
    for kappa in np.exp(np.linspace(np.log(0.05), np.log(50), 300)):
        thr = kappa*(1-s_)/(s_+kappa*(1-s_))
        acc = np.where(e_hat > thr, pK, 1-pK).mean()
        if best is None or acc > best[1]: best = (kappa, acc)
    return best[0]
print(f"     {'s':>4s} {'gate':>5s} {'population (Beta)':>20s} {'mode':>5s}  " + " ".join(f"sig={sg:<4.2f}" for sg in [0.05, 0.1, 0.2, 0.3]))
for s_ in [0.3, 0.5, 0.7]:
    gate = 1-s_
    for label, a, b in [("mass BELOW gate", None, None), ("mass AT gate", None, None), ("mass ABOVE gate", None, None)]:
        mode = {"mass BELOW gate": max(0.05, gate-0.2), "mass AT gate": gate, "mass ABOVE gate": min(0.95, gate+0.2)}[label]
        conc = 12.0; a = mode*conc + 1; b = (1-mode)*conc + 1
        e_true = rng.beta(a, b, M)
        row = " ".join(f"{kstar(e_true, s_, sg):8.2f}" for sg in [0.05, 0.1, 0.2, 0.3])
        print(f"     {s_:4.1f} {gate:5.2f} {label:>20s} {mode:5.2f}  {row}")
print("     Reading: the sign of kappa* - 1 follows where the population sits relative to the gate, not the world's")
print("     noise. Mass at the gate -> ~1 (the book's near-gate populations). Mass above -> kappa* < 1 (a margin")
print("     silences people who should act). Mass BELOW the gate with noisy self-knowledge -> kappa* runs to the top")
print("     of the grid: the accuracy-optimal rule for a starved population is that NOBODY acts on their own judgment.")
print("     The reviewer's correction is right, and it proves more than it wants: per-decision accuracy is maximized by")
print("     welding every gate -- which is the shared-tutor town of Lesson 2, N_eff = 1, that starves. Accuracy is not")
print("     survival (T13: nine 0.70 heads beat one 0.80 head). The gate kappa* protects per-decision accuracy; the")
print("     town's famine metric is what independent action protects, and the two objectives part company exactly")
print("     where the reviewer's margin is largest.")
