"""
figure_plane_and_frontier_v2.py -- redraw of the Ch 6 figure after R4.

Draws: the first printing's frontier curve (mixing-sage closed form; dashed,
labelled as the kept corpse); the certified lower-bound points from
frontier_polytope_attack.py (exact feasible policies) joined as the new
frontier lower bound; the plateau bar to c0' (exact) with a dashed extension
to the best numerical point (edge open); the sage point; the rock; the
tourist.  Every plotted point is an exact feasible policy except where
labelled 'open'.
"""
import sys, numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, __file__.rsplit('/', 1)[0])
import hiding_theorem_econ as ht

n, s = 6, 0.5
pF, C_E, p_fe, p_e, p_fge = ht.make_world(n, s)
log2n = np.log2(n)
sage_d = (ht.H(p_fe) - ht.H(p_e)) / log2n
rock_aim = 1 - sage_d          # g = identity is sufficient here
c0_old = 0.0522
c0_new = 0.2467
edge_num = 0.2774

def h_n(a):
    m = a + (1 - a) / n; o = (1 - a) / n
    return -(m * np.log2(m) + (n - 1) * o * np.log2(o))

lam = np.linspace(1e-3, 1, 400)
old_aim = 1 - h_n(lam) / log2n
old_d = h_n(lam * (1 - s)) / log2n

import os
rows = np.load(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'frontier_certified_points.npy'))
# rows: fam, mu, delta, aim_min, aim_max
pts = sorted({(round(r[2], 4), r[4]) for r in rows}, key=lambda t: t[0])
# keep the pointwise max per delta, add exact anchors
best = {}
for d, a in pts:
    best[d] = max(best.get(d, 0), a)
best[round(sage_d, 4)] = 1.0
best[1.0] = max(best.get(1.0, 0), edge_num)
best[0.0] = rock_aim
D = np.array(sorted(best)); A = np.array([best[d] for d in D])
hid = D >= sage_d - 1e-9          # hidden side of the sage point: the frontier bound
leg = ~hid                        # legible side: reachable points only (no bound claimed)

fig, ax = plt.subplots(figsize=(10.5, 7.2), dpi=150)
ax.fill_between([0, 1.05], 1.0, 1.08, color='0.9', zorder=0)
ax.plot(old_aim, old_d, '--', color='0.55', lw=1.8,
        label="first printing's frontier (the kept corpse: wrong near the plateau)")
ax.plot(A[hid], D[hid], '-', color='#1f77b4', lw=3, zorder=3,
        label='frontier, hidden side: certified lower bound (every point an exact strategy)')
ax.plot(A[hid], D[hid], 'o', color='#1f77b4', ms=5, zorder=4)
ax.plot(A[leg], D[leg], 'o', mfc='white', mec='#1f77b4', ms=7, mew=1.5, zorder=4,
        label='legible side: reachable points (exact), frontier there not drawn')
ax.plot([0, c0_new], [1, 1], color='#d62728', lw=9, solid_capstyle='butt', zorder=2,
        label=f"Ines's plateau: perfectly unreadable, aim at least c₀ = {c0_new:.3f} (exact)")
ax.plot([c0_new, edge_num], [1, 1], color='#d62728', lw=9, alpha=0.35, solid_capstyle='butt', zorder=2)
ax.annotate(f"edge: open\n(≥ {edge_num:.3f} found;\n≤ 0.56 proven)", xy=(edge_num, 1.0), xytext=(0.40, 0.955),
            fontsize=9, color='#d62728', arrowprops=dict(arrowstyle='->', color='#d62728', lw=1))
ax.plot([c0_old], [1.0], 'x', color='0.4', ms=9, mew=2, zorder=5)
ax.annotate(f"c₀ as first printed = {c0_old:.3f}", xy=(c0_old, 1.0), xytext=(0.07, 1.035), fontsize=8.5, color='0.4')
ax.plot([1], [sage_d], '*', color='#2ca02c', ms=22, zorder=5, label=f"the sage point (Thm 1 ceiling): (1, {sage_d:.3f})")
ax.plot([0], [1], 'o', color='#ff7f0e', ms=13, zorder=5)
ax.annotate("the lost tourist\n(unreadable, aimless)", xy=(0, 1), xytext=(0.04, 0.86), fontsize=10,
            arrowprops=dict(arrowstyle='-', color='0.4', lw=0.8))
ax.plot([rock_aim], [0], 's', color='0.3', ms=9, zorder=5)
ax.annotate("the ferry captain, in this weather\n(fully readable; aim capped by what\nthe sky reveals — Thm 2)",
            xy=(rock_aim, 0), xytext=(0.02, 0.30), fontsize=10, arrowprops=dict(arrowstyle='-', color='0.4', lw=0.8))
ax.text(0.80, 0.60, "the sailor's territory:\nhigh on both rulers,\nbounded by the frontier", color='#1f77b4', fontsize=12, ha='center')
ax.text(0.55, 1.04, "unreachable (no strategy exists here)", color='0.5', fontsize=10, ha='center', style='italic')
ax.set_xlim(-0.03, 1.05); ax.set_ylim(-0.05, 1.08)
ax.set_xlabel("aim  —  how much your actions serve where you're going   [ I(A;F)/H(F) ]", fontsize=12)
ax.set_ylabel("independence  —  how little circumstances predict you   [ δ_A = H(A|E)/log₂|A| ]", fontsize=12)
ax.set_title("The plane of the two rulers, and its frontier — second printing\n"
             "(model world of Chapters 4–6: n = 6 options, environment reliability 1−s = 0.5)", fontsize=13)
ax.grid(alpha=0.25); ax.legend(loc='lower right', fontsize=9.5, framealpha=0.95)
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'the_plane_and_frontier_v2.png')
plt.tight_layout(); plt.savefig(out); print("wrote", out)
