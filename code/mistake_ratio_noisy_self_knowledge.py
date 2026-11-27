"""mistake_ratio_noisy_self_knowledge.py -- which mistake ratio gives a population its best per-decision accuracy,
when people know their own reliability only roughly. (THEOREMS D5; Chapter 5 section 3.)

Recomputed 2026-11-25 with Theorem 5b as corrected that day. It replaces sections A5 of
code/rig/adversary_2026-10-24.py and R5 of code/rig/adversary_round2.py, which (a) labelled each threshold with the
mistake ratio of the uncorrected formula and (b) scored accuracy on disagreements only, as if there were two options.

The setting. A person's knowledge has fidelity e; the surroundings have reliability 1 - s; n options. The person does not
know e, only a noisy reading e_hat = e + noise (standard deviation sigma). A rule is a mistake ratio kappa: the person
acts on their own knowledge when e_hat is above Theorem 5b's gate for that kappa,

    e*(kappa) / (1 - e*(kappa)) = kappa (1-s)/s + (kappa - 1)(1 - 1/n),

and otherwise does what the surroundings say.

Accuracy, exactly. A person who acts on their own knowledge whenever it disagrees with the surroundings is, in effect,
always acting on it, and is right e + (1-e)/n of the time. A person who conforms is right (1-s) + s/n of the time. So a
population's accuracy under a rule is the average of those two numbers, weighted by who acts. No sampling: the
population is a density on a grid of e, and the share with e_hat above the gate is a normal tail.

What is reported: kappa*, the ratio with the highest accuracy, searched on a grid from 0.05 to 50 (50 is "the top of
the grid": nobody acts). Three statements are then tested, the ones the book makes:
    a population sitting at its gate   -> kappa* about 1
    a population mostly above its gate -> kappa* below 1 (a margin silences people who should act)
    a population mostly below its gate, with enough noise -> kappa* at the top of the grid (nobody should act)
"""
import numpy as np
from math import erf, sqrt, lgamma, log, exp

GRID_E = (np.arange(4000) + 0.5) / 4000
KAPPAS = np.exp(np.linspace(log(0.05), log(50), 600))


def gate(kappa, s, n):
    x = kappa * (1 - s) / s + (kappa - 1) * (1 - 1 / n)
    return 0.0 if x <= 0 else x / (1 + x)


def share_above(thr, sigma):
    """P(e_hat > thr | e) on the grid; e_hat is e plus normal noise, kept inside [0, 1]"""
    if thr <= 0: return np.ones_like(GRID_E)
    if thr >= 1: return np.zeros_like(GRID_E)
    if sigma == 0: return (GRID_E > thr).astype(float)
    return np.array([0.5 * (1 - erf((thr - e) / (sigma * sqrt(2)))) for e in GRID_E])


def kappa_star(density, s, n, sigma):
    w = density / density.sum(); a_own = GRID_E + (1 - GRID_E) / n; a_conf = (1 - s) + s / n
    best = (None, -1.0)
    for kappa in KAPPAS:
        p = share_above(gate(kappa, s, n), sigma)
        acc = float((w * (p * a_own + (1 - p) * a_conf)).sum())
        if acc > best[1] + 1e-12: best = (kappa, acc)
    return best[0]


def beta_density(mode, conc=12.0):
    a, b = mode * conc + 1, (1 - mode) * conc + 1
    return np.exp((a - 1) * np.log(GRID_E) + (b - 1) * np.log(1 - GRID_E) - (lgamma(a) + lgamma(b) - lgamma(a + b)))


def fmt(k): return 'top (50)' if k > 49.9 else ('bottom' if k < 0.0501 else f'{k:8.2f}')


if __name__ == '__main__':
    SIG = [0.05, 0.1, 0.2, 0.3]
    for n in (2, 8, 64):
        print(f'n = {n} options')
        print('  everyone equally likely to have any fidelity (uniform population)')
        print(f"    {'s':>4s} {'gate 1-s':>9s}  " + ' '.join(f'sigma={sg:<4.2f}' for sg in [0.0] + SIG))
        for s in (0.3, 0.5, 0.7):
            print(f'    {s:4.1f} {1 - s:9.2f}  ' + ' '.join(f'{fmt(kappa_star(np.ones_like(GRID_E), s, n, sg)):>10s}' for sg in [0.0] + SIG))
        print('  population gathered below, at, or above its gate (Beta, concentration 12)')
        print(f"    {'s':>4s} {'gate':>5s} {'population':>12s} {'mode':>5s}  " + ' '.join(f'sigma={sg:<4.2f}' for sg in SIG))
        rows = {}
        for s in (0.3, 0.5, 0.7):
            g = 1 - s
            for label, mode in (('below', max(0.05, g - 0.2)), ('at', g), ('above', min(0.95, g + 0.2))):
                ks = [kappa_star(beta_density(mode), s, n, sg) for sg in SIG]; rows[(s, label)] = ks
                print(f'    {s:4.1f} {g:5.2f} {label:>12s} {mode:5.2f}  ' + ' '.join(f'{fmt(k):>10s}' for k in ks))
        at = [k for (s, lab), ks in rows.items() if lab == 'at' for k in ks[:2]]
        above = [k for (s, lab), ks in rows.items() if lab == 'above' for k in ks]
        below_noisy = [k for (s, lab), ks in rows.items() if lab == 'below' for k in ks[2:]]
        below_all = [k for (s, lab), ks in rows.items() if lab == 'below' for k in ks]
        print(f'  CHECK n={n}: at the gate, kappa* between {min(at):.2f} and {max(at):.2f} (noise 0.05 and 0.10)')
        print(f'  CHECK n={n}: above the gate, kappa* below 1 in {sum(k < 1 for k in above)} of {len(above)} cells (largest {max(above):.2f})')
        print(f'  CHECK n={n}: below the gate, kappa* above 1 in {sum(k > 1 for k in below_all)} of {len(below_all)} cells; at the top of the grid in {sum(k > 49.9 for k in below_noisy)} of {len(below_noisy)} cells with noise 0.2 or 0.3 (smallest {min(below_noisy):.2f})')
        print()
