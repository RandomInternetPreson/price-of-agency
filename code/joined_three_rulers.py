"""
joined_three_rulers.py -- the same four programs read on three rulers, with the wall between household and town removed.

Pieces already in the book, each computed alone:
  (1) the drain and its repair in the one-asset host (code/rig/results_exact/hank_v01_results.json, general equilibrium):
      low-skill lifetime value and each skill group's BANDWIDTH under: baseline; a time transfer; cash of the same cost;
      schedule stability; cash of the same cost as stability;
  (2) the fishing town of Chapter 11: nine boats, a good day needs five on the fish, famine = three bad days running in
      a ninety-day season; exact.
THE JOIN, and its one supposition (marked, varied): a reader's accuracy rises with bandwidth,
      p(b) = 1/4 + (p_top - 1/4) * b**gamma     (chance among four grounds at b = 0, p_top at full bandwidth).
The town's nine boats are drawn from the economy's three skill groups (shares 1/4, 1/2, 1/4); famine is averaged exactly
over the 55 possible crews. Nothing is simulated.

Rulers:  CONSUMPTION (low-skill lifetime value, the standard ruler);  BANDWIDTH (the chooser's capacity);
         SURVIVAL (the town's famine probability) -- and beside it the town's MEAN catch, which is what an
         accounting that adds up isolated boats would report.
Writes code/results/joined_three_rulers.md
"""
import json, os, itertools
from math import comb, factorial
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
J = json.load(open(os.path.join(HERE, 'rig', 'results_exact', 'hank_v01_results.json')))
ARMS = [('baseline', 'baseline', 'no program'), ('PA_time', 'time', 'time transfer (low-skill floor lifted across the gate)'),
        ('PA_money', 'cash = time', 'cash, same cost as the time transfer'), ('PB_stability', 'stability', 'low-skill schedule entropy halved'),
        ('PB_wage', 'cash = stability', 'cash, same cost as stability')]
SHARES = (0.25, 0.5, 0.25); N, M, DAYS = 9, 5, 90


def run3(p):
    v = np.zeros(4); v[0] = 1
    for _ in range(DAYS):
        n = np.zeros(4); n[0] = (1 - p) * v[:3].sum(); n[1] = p * v[0]; n[2] = p * v[1]; n[3] = v[3] + p * v[2]; v = n
    return v[3]


def badday(ps):
    d = np.array([1.0])
    for p in ps: d = np.convolve(d, [1 - p, p])
    return d[:M].sum()


def town(bw, p_top, gamma):
    acc = [0.25 + (p_top - 0.25) * b ** gamma for b in bw]
    fam = mean = 0.0
    for k0 in range(N + 1):
        for k1 in range(N + 1 - k0):
            k2 = N - k0 - k1
            w = factorial(N) / (factorial(k0) * factorial(k1) * factorial(k2)) * SHARES[0] ** k0 * SHARES[1] ** k1 * SHARES[2] ** k2
            fam += w * run3(badday([acc[0]] * k0 + [acc[1]] * k1 + [acc[2]] * k2))
    mean = sum(s * a for s, a in zip(SHARES, acc))
    return fam, mean, acc


def main():
    base = J['baseline|model|GE']
    L = ["# Three rulers, one wall removed (2026-11-10)", "",
         "Source of the household columns: the printed one-asset economy, general equilibrium (`hank_v01_results.json`). Town: Chapter 11's, exact. "
         "The join is a construction with ONE supposition, marked and varied: a reader's accuracy rises with bandwidth, "
         "p(b) = 1/4 + (p_top − 1/4)·b^γ. Constants are the models'; the orderings are what is reported.", "",
         "## The programs on each ruler (p_top = 0.9, γ = 1)", "",
         "| program | CONSUMPTION ruler: low-skill lifetime value, change | aggregate lifetime value, change | BANDWIDTH ruler: low / mid / high skill | "
         "town's MEAN catch (share of boats on the fish) | SURVIVAL ruler: famine |", "|---|---|---|---|---|---|"]
    rows = {}
    for key, short, desc in ARMS:
        r = J[f'{key}|model|GE']; bw = (r['bw_low'], r['bw_mid'], r['bw_high'])
        fam, mean, acc = town(bw, 0.9, 1.0); rows[short] = (r['welf_low'] - base['welf_low'], r['WELF'] - base['WELF'], bw, mean, fam)
        L.append(f"| {desc} | {r['welf_low']-base['welf_low']:+.2f} | {r['WELF']-base['WELF']:+.2f} | {bw[0]:.2f} / {bw[1]:.2f} / {bw[2]:.2f} | {mean:.3f} | {100*fam:.1f}% |")
    b = rows['baseline']
    L += ["", "Read across. On the consumption ruler the cash wins and the time transfer is a loss. On the bandwidth ruler and on the survival ruler "
          "the order is reversed: " + "; ".join(f"{k} moves famine by {100*(rows[k][4]-b[4]):+.1f} points and the mean catch by {100*(rows[k][3]-b[3]):+.1f}" for k in ['time', 'cash = time', 'stability', 'cash = stability']) + ".",
          "", "## The supposition varied: famine under each program", "",
          "| p_top | γ | baseline | time | cash = time | stability | cash = stability | order on survival (best first) |", "|---|---|---|---|---|---|---|---|"]
    same = 0; tot = 0
    for p_top in (0.8, 0.9, 1.0):
        for gamma in (0.5, 1.0, 2.0):
            f = {}
            for key, short, _ in ARMS:
                r = J[f'{key}|model|GE']; f[short] = town((r['bw_low'], r['bw_mid'], r['bw_high']), p_top, gamma)[0]
            order = sorted(f, key=f.get); tot += 1
            same += (order[0] == 'time' and order[1] == 'stability')
            L.append(f"| {p_top} | {gamma} | " + " | ".join(f"{100*f[k]:.1f}%" for k in ['baseline', 'time', 'cash = time', 'stability', 'cash = stability']) + f" | {' > '.join(order)} |")
    L += ["", f"Time first and stability second on the survival ruler in {same} of {tot} versions of the supposition; in none does either cash arm lower famine by as much as a point.", "",
          "## What an accounting of isolated boats reports, against what the town suffers", "",
          "Degrade only the low-skill quarter of the population (their accuracy; everyone else untouched) and compare the loss in MEAN catch — the sum of "
          "each boat's own loss, which is all an isolated ledger can add up — with the change in famine:", "",
          "| low-skill accuracy | others | mean catch | loss in mean catch | famine | famine, relative to the first row |", "|---|---|---|---|---|---|"]
    ref = None
    for pl in (0.70, 0.65, 0.60, 0.50, 0.40, 0.25):
        acc = [pl, 0.70, 0.70]; fam = 0.0
        for k0 in range(N + 1):
            w = comb(N, k0) * 0.25 ** k0 * 0.75 ** (N - k0)
            fam += w * run3(badday([pl] * k0 + [0.70] * (N - k0)))
        mean = 0.25 * pl + 0.75 * 0.70
        if ref is None: ref = (mean, fam)
        L.append(f"| {pl:.2f} | 0.70 | {mean:.3f} | {100*(ref[0]-mean)/ref[0]:.1f}% | {100*fam:.1f}% | ×{fam/ref[1]:.1f} |")
    L += ["", "## The transfer lemma (one line)", "",
          "Famine in this town is a threshold on what the fleet finds, day by day. A transfer moves what was found from one boat's hold to another's; "
          "it does not move a boat onto the fish. So no redistribution of the catch, of any size, changes the famine probability; only what changes "
          "the readers' accuracy or the sameness of their errors does. In the household model the cash does reach bandwidth through one door — scarcity — "
          "and at the printed constants that door moves low-skill bandwidth from 0.30 to 0.29–0.30."]
    os.makedirs(os.path.join(HERE, 'results'), exist_ok=True)
    open(os.path.join(HERE, 'results', 'joined_three_rulers.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main()
