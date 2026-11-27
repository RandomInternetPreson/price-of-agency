"""
attack_T22_T23.py -- Theorems 22 and 23 went into the manuscript the day they were computed. This file attacks them the way
every earlier theorem was attacked before promotion, and prints what each attack did.

T22 (the borrowed record)
  A1. "Fishers would notice." Give them full knowledge of the structure but no way to tell a plain morning from a hard one.
  A2. "Crowding would thin the herd." Real sea: boats on the same ground share its catch (lesson six).
  A3. "One reader could simply ignore him." What a lone dissenter earns, glass sea and real sea.
T23 (the boat that stays in)
  B1. "A fisher goes hungry too; he would sail for the town's sake." Let each fisher count his own loss L (in boatloads) from
      a bad day, and sail whenever his catch plus his chance of saving the day is worth the trip.
  B2. "Bigger towns?" The same with 99 boats needing 55.
Writes code/results/attack_T22_T23.md
"""
import os
from math import comb
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))


def binom(n, k, p):
    return comb(n, k) * p ** k * (1 - p) ** (n - k)


def main():
    L = ["# Theorems 22 and 23 under attack (2026-11-12)", ""]
    # ---------- T22
    h, pe, ph, qe, qh, N = 0.3, 0.90, 0.55, 1.0, 0.50, 9
    a = (1 - h) * qe + h * qh; p = (1 - h) * pe + h * ph
    L += ["## Theorem 22 — the borrowed record", "",
          "**A1. Fishers who know everything except which morning is hard.** A fisher who knows the shares of plain and hard days and every accuracy, "
          "but cannot tell this morning's kind, compares being right by following (a) with being right by reading (p). "
          f"a = {a:.3f} > p = {p:.3f}: he follows, knowing the structure. The harm does not need a fooled fisher; it needs a fisher who cannot sort the days. *The theorem stands, and is sharper: ignorance of the sage is not required.*", ""]
    # A2 real sea, every boat counted: the boats that are right share the fish (V), the rest land nothing.
    def pay(k):
        """(follower's expected catch, reader's expected catch) with k boats behind the sage and N-k reading."""
        f = r = 0.0
        for w, pr, q in ((1 - h, pe, qe), (h, ph, qh)):
            nr = N - k
            for j in range(nr + 1):                       # j readers right
                pj = binom(nr, j, pr)
                if k: f += w * pj * q / (k + j)            # sage right: k followers + j readers share
                if nr and j:                               # a given reader is right with chance j/nr and then shares
                    r += w * pj * (j / nr) * (q / (k + j) + (1 - q) / j)
        return f, r
    L += ["**A2. Crowding.** Real sea: the boats that find the fish share it, V in all. Every boat counted, k behind the sage and the rest reading:", "",
          "| boats behind the sage | a follower's catch | a reader's catch | a reader who joins him would get |", "|---|---|---|---|"]
    kstar = None
    for k in range(0, N):
        f, r = pay(k); fj = pay(k + 1)[0]
        if kstar is None and fj <= r: kstar = k
        L.append(f"| {k} | {'—' if not k else f'{f:.3f} V'} | {r:.3f} V | {fj:.3f} V |")
    L += ["", f"Joining him stops paying once {kstar} boat{'s are' if kstar != 1 else ' is'} behind him: where the boats that are right share what they find, the herd stops at {kstar} of {N}. "
          "*The theorem is a theorem of the free answer — it rules wherever agreeing with a voice costs the agreer nothing. An opinion, a forecast, a doctrine can be held by everyone at no cost to any holder; a fishing ground cannot.*", "",
          "**A3. The lone dissenter, glass sea.** He is right "
          f"{100*p:.1f}% of days against the followers' {100*a:.1f}%: he pays {100*(a-p):.1f} points of his own accuracy to keep reading, and on every hard day he is the town's better guide. "
          "*This is Chapter 11's wildcard again, with the price of being one stated.*", ""]
    # ---------- T23
    g, pc, pm = 0.6, 0.9, 0.4
    L += ["## Theorem 23 — the boat that stays in", "",
          "**B1. A fisher who counts his own hunger.** Let a bad day cost each fisher L boatloads. A murky boat's trip is then worth p_m (1 + π L), "
          "where π is the chance that his landing a boatload turns a bad day into a good one, given what the others do.", "",
          "| town | others' rule | π (chance one more boatload saves the day) | he stays in when the trip costs more than: L = 0 | L = 1 | L = 3 | L = 10 |", "|---|---|---|---|---|---|---|"]
    for N_, M_ in ((9, 5), (99, 55)):
        for lab, x in (("murky boats stay in", g * pc), ("every boat sails", g * pc + (1 - g) * pm)):
            pi = binom(N_ - 1, M_ - 1, x)
            L.append(f"| {N_} boats, {M_} needed | {lab} | {pi:.3f} | {pm:.2f} | {pm*(1+pi):.2f} | {min(pm*(1+3*pi),9.99):.2f} | {min(pm*(1+10*pi),9.99):.2f} |")
    pi9 = binom(8, 4, g * pc); pi99 = binom(98, 54, g * pc)
    L += ["", f"In the nine-boat town a murky boat that counts one boatload of hunger still stays in whenever a trip costs more than {pm*(1+pi9):.2f} — the band of costs in which staying in is rational narrows, and does not close. "
          f"In a town of ninety-nine the chance that one boat decides the day is {pi99:.3f}; counting his hunger changes almost nothing (threshold {pm*(1+pi99):.2f} at L = 1). "
          "*The theorem stands and gains a clause: the larger the town, the less any fisher's own hunger brings him out. It is the free-rider problem of Olson (1965) and Samuelson (1954), in the spirit of — with the difference that what is under-supplied here is not effort but doubtful judgment.*", "",
          "**B2. Between the two thresholds.** One more boat matters more when fewer are out, so the two rules cannot both hold: below the lower threshold every boat sails, "
          "above the upper one every murky boat stays in, and between them the murky fleet splits — just enough of it sails that the rest are indifferent.", "",
          "| hunger L (boatloads lost on a bad day) | every boat sails when a trip costs less than | every murky boat stays in when it costs more than |", "|---|---|---|"]
    def bad(x, N_=9, M_=5):
        return sum(binom(N_, k, x) for k in range(M_))
    for Lh in (1, 3, 10):
        L.append(f"| {Lh} | {pm * (1 + Lh * binom(8, 4, g * pc + (1 - g) * pm)):.2f} | {pm * (1 + Lh * pi9):.2f} |")
    a_, b_ = 0.0, 1.0                                    # midway in pivot probability: the share sailing does not depend on L
    tgt = 0.5 * (binom(8, 4, g * pc + (1 - g) * pm) + pi9)
    for _ in range(60):
        sg = 0.5 * (a_ + b_)
        if binom(8, 4, g * pc + (1 - g) * sg * pm) > tgt: a_ = sg
        else: b_ = sg
    L += ["", f"Midway between the two, {100*sg:.0f}% of murky boats sail and the town has a bad day {100*bad(g*pc+(1-g)*sg*pm):.1f}% of the time, "
          f"against {100*bad(g*pc+(1-g)*pm):.1f}% with every boat out and {100*bad(g*pc):.1f}% with every murky boat in."]
    L += ["", "*At every level of hunger a fisher can feel on his own account, there is a band of trip costs in which doubtful boats stay in and the town's bad days rise above what full sailing would give. "
          "His own hunger moves the band; it does not remove it.*"]
    os.makedirs(os.path.join(HERE, 'results'), exist_ok=True)
    open(os.path.join(HERE, 'results', 'attack_T22_T23.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
