"""adversary_round5.py -- computable claims in round 5 (Gemini 6, ChatGPT 4) against v0.26."""
import numpy as np
from math import comb
N, n, DAYS, ST = 9, 4, 90, 3
def streak(pf):
    M=np.zeros((ST+1,ST+1))
    for k in range(ST): M[k,0]=1-pf; M[k,k+1]=pf
    M[ST,ST]=1; v=np.zeros(ST+1); v[0]=1
    for _ in range(DAYS): v=v@M
    return v[ST]
def day_success(k_follow, p=0.7, q=0.8):
    """k boats follow the master, 9-k read independently; success = >=5 boats on the right ground."""
    m = N - k_follow; tot = 0.0
    for right in (True, False):
        pm = q if right else 1-q
        for j in range(m+1):
            pj = comb(m, j) * p**j * (1-p)**(m-j)          # j independents right
            boats_right = j + (k_follow if right else 0)
            tot += pm * pj * (boats_right >= 5)
    return tot
print("C1  follower dose vs master accuracy (famine over 90 days)")
print(f"    {'master q':>9s} " + " ".join(f"k={k:<2d}" for k in [0,1,2,3,5,9]) + "   best k")
for q in [0.8, 0.85, 0.9, 0.95, 0.99]:
    fam = [streak(1 - day_success(k, 0.7, q)) for k in [0,1,2,3,5,9]]
    best = [0,1,2,3,5,9][int(np.argmin(fam))]
    print(f"    {q:9.2f} " + " ".join(f"{f:5.3f}" for f in fam) + f"   {best}")
print("    Reading: one follower is optimal for q <= ~0.85; by q = 0.90 the herd line is where safety lies. T13(iii)'s")
print("    dose curve is a statement about an expert only somewhat better than the room; the general rule is to set the")
print("    dose by the expert's margin -- and by the dependence of his errors, which iid days cannot show.\n")

print("G3/C2  pooling with joint arrival and the fisher's effect on the town's catch (eight follow the master)")
def U(alpha, read, p, q, k_follow=8):
    # ninth boat: read independently or follow. Town catches V when some boat is on the right ground.
    # private share: boats on the right ground split V; pooled share: total catch / 9.
    if not read:
        # all 9 on master's ground: right w.p. q -> each gets V/9 private; total catch V
        priv = q * 1/9; tot = q
    else:
        # master right (q): if fisher right too (p) she shares with 8 -> V/9 ; if wrong, she gets 0, catch V
        # master wrong (1-q): fisher right (p) -> she alone -> V, catch V ; else 0
        priv = q*p*(1/9) + (1-q)*p*1.0
        tot = q + (1-q)*p
    return (1-alpha)*priv + alpha*tot/9
for p,q in [(0.7,0.8),(0.7,0.9),(0.7,0.99)]:
    print(f"    p={p} q={q}:  " + "  ".join(f"alpha={a:.2f}: read {U(a,True,p,q):.4f} follow {U(a,False,p,q):.4f} ({'read' if U(a,True,p,q)>U(a,False,p,q) else 'FOLLOW'})" for a in [0.0,0.5,0.9,1.0]))
print("    Reading: the v0.26 inequality 0.7V > 0.8V/k was wrong twice -- it ignored joint arrival (when both are right they")
print("    share) and the fact that the reader's choice changes the town's total catch, so the pooled share does not cancel.")
print("    In the printed town (0.7 vs 0.8) reading pays at every pooling fraction, full pooling included; against a 0.99")
print("    master, following pays at every fraction. Pooling is not what decides it; the master's margin is.\n")

print("G2A  hit rate of the plateau strategy vs the captain")
for n_,s in [(4,0.3),(4,0.5),(4,0.7),(6,0.3),(6,0.5)]:
    pE = 1-s+s/n_; hand = 1/n_ + s*(n_-1)/n_
    print(f"    n={n_} s={s}: captain P(A=F)={pE:.3f}  plateau (hand) P(A=F)={hand:.3f}  chance={1/n_:.3f}   plateau {'>' if hand>pE else '<' if hand<pE else '='} captain")
print("    Reading: the plateau strategy beats chance always and the captain only when s > 1/2 (equal at 1/2). 'Ines still")
print("    wins' must say 'more than chance', which is what Theorem 6 claims; beating the captain was never the claim.\n")

print("C4  menu padding: an irrelevant random tag with m values appended to the action")
for m in [1,2,4,8]:
    HAE = 0.8113; logA = 1.0
    print(f"    m={m}: delta_A = {(HAE+np.log2(m))/(logA+np.log2(m)):.4f}   (aim unchanged)")
print("    Reading: independence depends on the action alphabet; two labels with identical consequences on every future must")
print("    be one action, or the ruler can be inflated for free. Audit rule: the alphabet is quotiented by consequence.")
