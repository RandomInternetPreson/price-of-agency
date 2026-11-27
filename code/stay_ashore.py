"""
stay_ashore.py -- the fisher who may stay ashore (Chapter 11's last unmodeled choice), exact.

Nine boats; a good day needs five on the fish; famine = three bad days running in ninety. Each morning a fisher's reading
is CLEAR (probability g, right with probability p_c) or MURKY (right with probability p_m). Sailing costs c, in units of a
boatload (fuel, gear, the day itself); a boat on the fish lands one boatload. A fisher sails when his reading is worth the
trip: p >= c. He stays ashore otherwise.
  - While c <= p_m every boat sails every day: the town of Chapter 11 (overall accuracy g p_c + (1-g) p_m).
  - Once c > p_m the murky boats stay in. Each stays in for a good private reason, and each was landing a boatload p_m of
    the time.
The town's remedy is priced: pay s = c - p_m per murky sailing (a mistake budget: the cost of a doubtful trip, covered).
Writes code/results/stay_ashore.md
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


def bad(x):
    """each boat is on the fish with probability x, independently"""
    return sum(comb(N, j) * x ** j * (1 - x) ** (N - j) for j in range(M))


def main():
    L = ["# The fisher who may stay ashore (2026-11-12)", "",
         "A reading is clear (probability g, right p_c of the time) or murky (right p_m). Sailing costs c boatloads; a fisher sails when p ≥ c.", "",
         "| g | p_c | p_m | everyone sails: boats on the fish / famine | murky boats stay in (any c above p_m): boats on the fish / famine | catch per boat, net of cost at c = p_m + 0.05: all sail / murky stay | subsidy that brings them out, per boat per day, as a share of the mean catch |",
         "|---|---|---|---|---|---|---|"]
    for g, pc, pm in [(0.6, 0.9, 0.4), (0.5, 0.9, 0.5), (0.7, 0.85, 0.35), (0.6, 0.8, 0.55), (0.8, 0.8, 0.3), (0.4, 0.95, 0.53)]:
        x_all = g * pc + (1 - g) * pm; x_in = g * pc; c = pm + 0.05
        net_all = x_all - c; net_in = g * (pc - c)
        sub = (1 - g) * (c - pm)
        L.append(f"| {g} | {pc} | {pm} | {x_all:.2f} / {100*run3(bad(x_all)):.1f}% | {x_in:.2f} / {100*run3(bad(x_in)):.1f}% | {net_all:.3f} / {net_in:.3f} | {100*sub/x_all:.1f}% |")
    g, pc, pm = 0.6, 0.9, 0.4; x_all = g * pc + (1 - g) * pm
    L += ["", "## Reading (first row: the printed town's 70% reader, split into clear and murky mornings)",
          f"- With sailing cheap, every boat goes and the town is Chapter 11's: famine {100*run3(bad(x_all)):.1f}%.",
          f"- Let a trip cost more than a murky reading is worth ({pm} of a boatload) and four boats in ten stay in on any morning. Each is right to: "
          f"its own net catch rises (third column). The town's famine goes from {100*run3(bad(x_all)):.1f}% to {100*run3(bad(g*pc)):.1f}%.",
          "- The murky boat was carrying the town: it landed a boatload four mornings in ten, and the town's good day is a count of boatloads, not of confident fishers.",
          "- The remedy is small and exact: cover the gap between the cost of a doubtful trip and what the doubtful reading is worth. At a cost five hundredths of a boatload above the murky reading's worth, "
          f"that is {100*(1-g)*0.05/x_all:.1f}% of the mean catch — against a famine rate cut from {100*run3(bad(g*pc)):.0f}% to {100*run3(bad(x_all)):.0f}%.",
          "- This is Theorem 5b in a boat. A wrong bet of one's own that costs more than it is worth is not made; a town that prices its fishers' doubtful mornings at their private worth loses the boats it was living on."]
    os.makedirs(os.path.join(HERE, 'results'), exist_ok=True)
    open(os.path.join(HERE, 'results', 'stay_ashore.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n'); print('\n'.join(L))


if __name__ == '__main__':
    main()
