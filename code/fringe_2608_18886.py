"""fringe_2608_18886.py -- the fringe of the second paper (arXiv:2608.18886, Sec. 5 and Sec. 8), recomputed for Figure V.3.

The paper's own code is not in this repository, so the curve is rebuilt here from the paper's stated model and checked
against the four numbers the paper prints.

Model (Sec. 5): shared phase lambda; outcome sgn cos 2(lambda - a); click probability D(m), m = |cos 2(lambda - a)|.
With x = 2 lambda, g(x) = D(|cos x|), f(x) = sgn(cos x) g(x):  E(Delta) = -C_f(2 Delta) / C_g(2 Delta), and the exact singlet
correlation is the functional equation  C_f(theta) = cos(theta) C_g(theta)  for all theta. Edge law: D(m) = sqrt(m) h(m).
In harmonics (P_n, Q_n the powers of g and f):  2 Q_1 = P_0 + P_2,  2 Q_m = P_{m-1} + P_{m+1} (m odd >= 3).
The total coincidence rate is R_d(Delta) proportional to C_g(2 Delta) (Sec. 8).

Published checks: h(0)/h(1) = 1.17450854538894; efficiency 80.1%; fringe 12.4% peak to peak; leading harmonic to first
overtone about 6:1; R_d(22.5 deg) = R_d(67.5 deg) exactly (Theorem 2, the hiding theorem).
"""
import os
import numpy as np
from numpy.polynomial import chebyshev as Ch
from scipy.optimize import least_squares

HERE = os.path.dirname(os.path.abspath(__file__))
N = 2 ** 15; x = (np.arange(N) + 0.5) * 2 * np.pi / N; m = np.abs(np.cos(x)); sg = np.sign(np.cos(x)); J = 14; MODES = 80


def profile(c, mm): return np.sqrt(mm) * Ch.chebval(2 * mm - 1, c)


def spectra(c):
    g = profile(c, m)
    return np.abs(np.fft.rfft(g) / N) ** 2, np.abs(np.fft.rfft(sg * g) / N) ** 2


def resid(c):
    P, Q = spectra(c)
    r = [2 * Q[1] - (P[0] + P[2])] + [2 * Q[k] - (P[k - 1] + P[k + 1]) for k in range(3, MODES, 2)]
    return np.concatenate([np.array(r) * 1e3, [Ch.chebval(1.0, c) - 1.0]])           # the scale is fixed by h(1) = 1


if __name__ == '__main__':
    c0 = np.zeros(J + 1); c0[0] = 1.0
    sol = least_squares(resid, c0, xtol=1e-15, ftol=1e-15, gtol=1e-15, max_nfev=4000); c = sol.x; P, Q = spectra(c)
    th = np.linspace(0, np.pi, 721)
    Cg = P[0] + 2 * sum(P[n] * np.cos(n * th) for n in range(2, 400, 2)); Cf = 2 * sum(Q[n] * np.cos(n * th) for n in range(1, 400, 2))
    ratio = Ch.chebval(-1.0, c) / Ch.chebval(1.0, c); eff = profile(c, m).mean(); depth = (Cg.max() - Cg.min()) / Cg.mean()
    D = np.linspace(0, 180, 361); R = P[0] + 2 * sum(P[n] * np.cos(n * 2 * np.radians(D)) for n in range(2, 400, 2)); R = R / R.mean()
    lines = ["# The fringe of arXiv:2608.18886, recomputed (code/fringe_2608_18886.py)", "",
             "| quantity | here | the paper |", "|---|---|---|",
             f"| h(0)/h(1) | {ratio:.6f} | 1.17450854538894 |",
             f"| efficiency of the exact profile | {eff:.4f} | 0.801 |",
             f"| fringe, peak to peak over mean | {depth:.4f} | 0.124 |",
             f"| leading harmonic : first overtone | {P[2] / P[4]:.2f} : 1 | about 6 : 1 |",
             f"| R(22.5 deg) / R(67.5 deg) - 1 | {R[45] / R[135] - 1:.1e} | 0, exactly (Theorem 2) |",
             f"| largest error of the correlation curve against -cos 2 Delta | {np.abs(-Cf / Cg + np.cos(th)).max():.1e} | 4e-11 |", "",
             "The paper solves the profile to 1e-11 with a quadrature built for the square-root edge; this script uses a plain",
             "grid and agrees to four figures, which is finer than the width of a printed line. The curve is in",
             "`fringe_2608_18886.csv` (relative analyzer angle in degrees; total coincidence rate over its mean)."]
    assert abs(ratio - 1.17450854538894) < 5e-4 and abs(eff - 0.801) < 1e-3 and abs(depth - 0.124) < 1e-3 and abs(R[45] - R[135]) < 1e-12
    os.makedirs(os.path.join(HERE, 'results'), exist_ok=True)
    np.savetxt(os.path.join(HERE, 'results', 'fringe_2608_18886.csv'), np.c_[D, R], delimiter=',', header='relative_angle_deg,total_rate_over_mean', comments='', fmt='%.8f')
    open(os.path.join(HERE, 'results', 'fringe_2608_18886.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))
