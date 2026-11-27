"""make_figures.py -- every chart in the designed edition, drawn in one style.

    python design/make_figures.py          (writes design/fig/*.pdf; prints the numbers each chart is checked against)

Each function says where its numbers come from: computed here with the book's own model (and checked against the figure the
book prints), read from a results file in the repository, or copied from a number the book states. Nothing is fitted or
smoothed. The diagrams (design/fig/*.tex) are drawings of the stories, not data.
"""
import os, sys, re
from math import comb
import numpy as np, matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from matplotlib import font_manager as fm

HERE = os.path.dirname(os.path.abspath(__file__)); ROOT = os.path.dirname(HERE); OUT = os.path.join(HERE, 'fig')
os.makedirs(OUT, exist_ok=True)
for f in fm.findSystemFonts():
    if 'FiraSans' in f: fm.fontManager.addfont(f)
plt.rcParams.update({'font.family': 'Fira Sans', 'font.size': 8.4, 'axes.linewidth': 0.6, 'pdf.fonttype': 42,
                     'mathtext.fontset': 'custom', 'mathtext.rm': 'Fira Sans', 'mathtext.it': 'Fira Sans:italic',
                     'mathtext.bf': 'Fira Sans:bold', 'axes.labelsize': 8.4, 'xtick.labelsize': 8, 'ytick.labelsize': 8})
INK, MUTED, GRID, SOFT = '#1a1a1a', '#5b5b57', '#e4e3df', '#b9b8b3'
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'          # validated: design skill palette, slots 1-3
W = 4.42                                                       # the text block, inches


def axes(h, w=W, **kw):
    fig, ax = plt.subplots(figsize=(w, h), **kw)
    for a in np.atleast_1d(ax).ravel(): clean(a)
    return fig, ax


def clean(ax, grid='y'):
    for sp in ('top', 'right', 'left'): ax.spines[sp].set_visible(False)
    ax.spines['bottom'].set_color(SOFT); ax.tick_params(length=0, colors=MUTED)
    if grid: ax.grid(axis=grid, color=GRID, lw=0.6)
    ax.set_axisbelow(True)
    ax.xaxis.label.set_color(MUTED); ax.yaxis.label.set_color(MUTED)


def save(fig, name):
    fig.savefig(os.path.join(OUT, name + '.pdf'), transparent=True); plt.close(fig)


def H(p):
    p = np.asarray(p, float); p = p[p > 1e-15]; return float(-(p * np.log2(p)).sum())


# ------------------------------------------------------------------------------------------------ Chapter 2
def staircase():
    """F = R/(2(R+1)), R = 2^floor((n-1)/2): arXiv:2608.00124 (each even size repeats the odd size below it)."""
    n = np.arange(3, 23); R = 2.0 ** ((n - 1) // 2); F = R / (2 * (R + 1))
    fig, ax = axes(2.3)
    ax.axhline(0.5, color=INK, lw=0.8)
    ax.step(n, F, where='post', color=BLUE, lw=1.8)
    ax.plot(n[::2], F[::2], 'o', ms=5, color=BLUE, mec='white', mew=1.2)
    for k, lab in ((3, '1/3'), (5, '2/5'), (7, '4/9'), (9, '8/17')):
        ax.text(k + 0.25, F[k - 3] - 0.012, lab, color=MUTED, fontsize=7.6, ha='left', va='top')
    ax.text(22.6, 0.5065, 'one half: never reached', color=MUTED, fontsize=7.6, ha='right', va='bottom')
    ax.set_xlim(2.4, 22.8); ax.set_ylim(0.30, 0.525); ax.set_xticks([3, 5, 7, 9, 11, 13, 15, 17, 19, 21]); ax.set_yticks([0.30, 0.35, 0.40, 0.45, 0.50])
    ax.set_xlabel('Number of particles'); ax.set_ylabel('Measurement independence relaxed')
    fig.tight_layout(pad=0.3); save(fig, 'staircase')
    print('staircase:', [f"{x:.4f}" for x in F[:8:2]], 'last', F[-1])


# ------------------------------------------------------------------------------------------------ Chapter 5
def gate_test(n, s, e):                      # code/dichotomy_scaling_and_audits.py, with a hard argmax
    pF = np.full(n, 1 / n)
    C = np.full((n, n), s / n); C[np.arange(n), np.arange(n)] += 1 - s
    CK = np.full((n, n), (1 - e) / n); CK[np.arange(n), np.arange(n)] += e
    p_fek = pF[:, None, None] * C[:, :, None] * CK[:, None, :]
    post = np.nan_to_num(p_fek / p_fek.sum(0)[None], nan=1 / n)
    lg = 1e9 * post; lg -= lg.max(0, keepdims=True)
    pol = np.exp(lg); pol /= pol.sum(0, keepdims=True)
    p = p_fek[:, :, :, None] * np.transpose(pol, (1, 2, 0))[None]
    pea = p.sum(axis=(0, 2))
    return (H(pea) - H(pea.sum(1))) / np.log2(n)


def gate():
    n = 16; es = np.round(np.linspace(0.0, 0.995, 400), 6)
    fig, ax = axes(2.5)
    for s, col, lab in ((0.6, BLUE, 'Noisy world, s = 0.6'), (0.2, ORANGE, 'Orderly world, s = 0.2')):
        g = 1 - s; e2 = np.sort(np.concatenate([es, [g - 1e-6, g + 1e-6]]))
        d = np.array([gate_test(n, s, e) for e in e2])
        ax.plot(e2, d, color=col, lw=1.8, solid_joinstyle='round', label=lab, zorder=3)
        ax.plot([g], [0], 'o', ms=5.5, color=col, mec='white', mew=1.4, zorder=4)
        print('gate s', s, 'below', round(gate_test(n, s, g - 0.01), 4), 'above', round(gate_test(n, s, g + 0.01), 4))
    ax.text(0.415, 0.045, 'gate at 0.40', ha='left', va='center', color=MUTED, fontsize=7.5)
    ax.text(0.815, 0.045, 'gate at 0.80', ha='left', va='center', color=MUTED, fontsize=7.5)
    ax.set_xlim(0, 1); ax.set_ylim(-0.03, 1.0); ax.set_xticks([0, 0.2, 0.4, 0.6, 0.8, 1.0]); ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel(r'Education fidelity  $e$'); ax.set_ylabel(r'Independence  $\delta_A$')
    ax.legend(loc='upper left', frameon=False, handlelength=1.4, fontsize=8, labelcolor=INK, borderaxespad=0.2)
    fig.tight_layout(pad=0.3); save(fig, 'gate')


# ------------------------------------------------------------------------------------------------ Chapter 6
def frontier():
    """Certified points: figures/frontier_certified_points.npy (code/frontier_polytope_attack.py), the list printed in
    Chapter 6 §5. Plateau to c0 = 0.247 (closed form); best strategy found at full unreadability 0.335 (vertex search)."""
    rows = np.load(os.path.join(ROOT, 'figures', 'frontier_certified_points.npy'))
    sage_d = 0.7533
    best = {}
    for r in rows:
        d, a = round(float(r[2]), 4), float(r[4])
        if d >= sage_d - 1e-3: best[d] = max(best.get(d, 0), a)
    D = np.array(sorted(best, reverse=True)); A = np.array([best[d] for d in D])
    print('frontier points (aim, independence):', [(round(a, 2), round(d, 3)) for a, d in zip(A, D)])
    fig, ax = axes(3.5, grid=None) if False else axes(3.5)
    ax.grid(axis='x', color=GRID, lw=0.6)
    ax.fill_between([0, 1.02], 1.0, 1.06, color='#f1f0ec', lw=0)
    ax.plot([0, 0.2467], [1, 1], color=BLUE, lw=5, solid_capstyle='butt', zorder=3)
    ax.plot([0.2467, 0.335], [1, 1], color=BLUE, lw=5, alpha=0.35, solid_capstyle='butt', zorder=3)
    ax.plot(A, D, '-', color=BLUE, lw=1.8, zorder=4); ax.plot(A, D, 'o', ms=4.6, color=BLUE, mec='white', mew=1.1, zorder=5)
    ax.plot([0.335], [1.0], 'o', ms=5.5, mfc='white', mec=BLUE, mew=1.3, zorder=6)
    ax.plot([0], [1], 'o', ms=6, color=ORANGE, mec='white', mew=1.2, zorder=6)
    ax.plot([0.2467], [0], 's', ms=5.5, color=MUTED, mec='white', mew=1.2, zorder=6, clip_on=False)
    ax.plot([1], [sage_d], 'D', ms=6, color=INK, mec='white', mew=1.2, zorder=6, clip_on=False)
    t = dict(fontsize=7.7, color=INK)
    ax.annotate('the lost tourist', (0, 1), (0.04, 0.87), **t, arrowprops=dict(arrowstyle='-', color=SOFT, lw=0.7))
    ax.annotate('the plateau, where Ines plays:\nunreadable, and still winning.\nProven to an aim of 0.247, found\nto 0.335; its edge is open', (0.20, 1.0), (0.10, 0.60), **t,
                arrowprops=dict(arrowstyle='-', color=SOFT, lw=0.7))
    ax.annotate('past the edge, more aim\nis paid for in readability', (0.615, 0.895), (0.42, 0.36), **t, arrowprops=dict(arrowstyle='-', color=SOFT, lw=0.7))
    ax.annotate('full aim (the sage point):\nindependence 0.75', (1, sage_d), (0.68, 0.54), **t, arrowprops=dict(arrowstyle='-', color=SOFT, lw=0.7))
    ax.annotate('the ferry captain\nin this weather', (0.2467, 0), (0.31, 0.10), **t, arrowprops=dict(arrowstyle='-', color=SOFT, lw=0.7))
    ax.text(0.5, 1.03, 'no strategy reaches here', fontsize=7.4, color=MUTED, ha='center', va='center', style='italic')
    ax.set_xlim(-0.02, 1.02); ax.set_ylim(-0.02, 1.06); ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel('Aim'); ax.set_ylabel(r'Independence  $\delta_A$')
    fig.tight_layout(pad=0.3); save(fig, 'frontier')


# ------------------------------------------------------------------------------------------------ Chapter 7
def pricelist():
    """Elasticities printed in Chapter 7 §4 (code/theft_equilibrium.py)."""
    rows = [('Independence of an unreadable agent,\nany resource taken', 0.009, 'at most 0.009'),
            ('Aim of a time-rich agent, time taken', 0.008, '0.008'),
            ('Aim of a time-poor agent, time taken', 0.565, '0.565'),
            ('Aim of an unreadable agent,\nany resource taken', 1.75, '1.5 to 2.0'),
            ('Independence near the gate,\nworld made more predictable', 4.5, 'about 4.5'),
            ('Independence near the gate,\neducation taken', 9.0, 'about 9')]
    fig, ax = axes(2.75); ax.grid(False); ax.grid(axis='x', color=GRID, lw=0.6)
    y = np.arange(len(rows))
    for i, (lab, v, txt) in enumerate(rows):
        ax.plot([0.004, v], [i, i], color=GRID, lw=1.2, zorder=1)
        if i == 3: ax.plot([1.5, 2.0], [i, i], color=BLUE, lw=3.2, solid_capstyle='round', zorder=3)
        else: ax.plot([v], [i], 'o', ms=6.5, color=BLUE, mec='white', mew=1.3, zorder=3)
        ax.text(v * 1.35 if i != 3 else 2.5, i, txt, va='center', ha='left', fontsize=7.8, color=INK)
    ax.set_yticks(y); ax.set_yticklabels([r[0] for r in rows], color=INK, fontsize=7.7)
    ax.set_xscale('log'); ax.set_xlim(0.004, 60); ax.set_ylim(-0.6, len(rows) - 0.4)
    ax.set_xticks([0.01, 0.1, 1, 10]); ax.set_xticklabels(['0.01', '0.1', '1', '10'])
    ax.set_xlabel('Percent lost per percent taken (log scale)')
    ax.spines['bottom'].set_visible(False)
    fig.tight_layout(pad=0.3); save(fig, 'pricelist')


# ------------------------------------------------------------------------------------------------ Chapter 8
def watchers():
    """Theorem 9: endpoints printed in Chapter 8 (1.00 -> 0.29; wider plateau 1.00 -> 0.65; open expert 0.75);
    partial watching is exactly the straight line between the endpoints."""
    r = np.array([0, 1.0])
    fig, ax = axes(2.5)
    ax.axhline(0.75, color=INK, lw=0.9, label='An open expert who hides nothing: 0.75')
    ax.plot(r, [1, 0.29], color=BLUE, lw=1.8, label="Ines's simplest strategy")
    ax.plot(r, [1, 0.65], color=ORANGE, lw=1.8, label='Chance spent only where the world is wrong')
    for x1, col in (((1 - 0.75) / (1 - 0.29), BLUE), ((1 - 0.75) / (1 - 0.65), ORANGE)):
        ax.plot([x1], [0.75], 'o', ms=5.5, color=col, mec='white', mew=1.3, zorder=5)
        ax.text(x1, 0.705, f'{x1:.2f}', ha='center', va='top', fontsize=7.6, color=MUTED)
    ax.text(1.0, 0.31, '0.29', fontsize=7.6, color=MUTED, ha='right', va='bottom'); ax.text(1.0, 0.665, '0.65', fontsize=7.6, color=MUTED, ha='right', va='bottom')
    ax.set_xlim(0, 1); ax.set_ylim(0.2, 1.02); ax.set_xticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel("Share of her source of chance the watcher sees"); ax.set_ylabel(r'Independence from that seat')
    ax.legend(loc='lower left', frameon=False, handlelength=1.4, fontsize=7.8, labelcolor=INK, borderaxespad=0.3)
    fig.tight_layout(pad=0.3); save(fig, 'watchers')
    print('watcher crossovers:', round((1 - 0.75) / (1 - 0.29), 3), round((1 - 0.75) / (1 - 0.65), 3))


# ------------------------------------------------------------------------------------------------ Chapter 9
def wirings():
    """Exact floors against a watcher who knows the habit (code/arms_race.py's world: n = 4, s = 0.5, eight habits).
    Checked against docs/THEOREMS_v1.md, Theorem 11: additive 0.761 / 0.947 / 0.984 at h = 1, 2, 3; gated 0.45-0.49."""
    n = 4; s = 0.5; log2n = 2.0; mS = 8
    C = np.full((n, n), s / n); C[np.arange(n), np.arange(n)] += 1 - s
    p_fe = C / n; p_e = p_fe.sum(0); q = (p_fe / p_e[None]).T
    lam = 1.0 / (n * q.max()); pol = np.zeros((n, n, n))
    for e in range(n):
        r = np.clip((1.0 / n - lam * q[e]) / (1 - lam), 0, None); r /= r.sum()
        for f in range(n):
            pol[f, e, :] = (1 - lam) * r; pol[f, e, f] += lam
    cdf = np.cumsum(pol, axis=-1)

    def floor(mU, wiring):
        L = np.zeros((mS, n, n))
        for S in range(mS):
            for U in range(mU):
                rf = ((S + (U + 0.5) / mU) % mS) / mS if wiring == 'gated' else ((S + 0.5) / mS + (U + 0.5) / mU) % 1.0
                G = (cdf < rf).sum(axis=-1)
                for e in range(n):
                    for f in range(n): L[S, e, G[f, e]] += q[e, f] / mU
        d0 = sum(p_e[e] * H(L.mean(0)[e]) for e in range(n)) / log2n
        dinf = np.mean([sum(p_e[e] * H(L[S, e]) for e in range(n)) for S in range(mS)]) / log2n
        return d0, dinf
    hs = [0, 1, 2, 3]
    gated = [floor(2 ** h, 'gated') for h in hs]; add = [floor(2 ** h, 'additive') for h in hs]
    sage = (H(p_fe) - H(p_e)) / log2n
    print('wirings: gated floors', [round(x[1], 3) for x in gated], 'additive floors', [round(x[1], 3) for x in add],
          'first-day (additive)', [round(x[0], 3) for x in add], 'sage', round(sage, 3))
    fig, ax = axes(2.6)
    ax.axhline(sage, color=INK, lw=0.9)
    ax.text(3.0, sage + 0.012, 'someone who never disguised anything', fontsize=7.5, color=MUTED, ha='right', va='bottom')
    ax.plot(hs, [x[1] for x in add], '-o', color=BLUE, lw=1.8, ms=5.5, mec='white', mew=1.3, label='Flips decide the big things')
    ax.plot(hs, [x[1] for x in gated], '-o', color=ORANGE, lw=1.8, ms=5.5, mec='white', mew=1.3, label='Flips decide the small things')
    ax.plot(hs, [x[0] for x in add], color=SOFT, lw=1.0, zorder=1)
    ax.text(0.05, add[0][0] + 0.012, 'first day, before the file exists', fontsize=7.5, color=MUTED, va='bottom')
    ax.set_xlim(-0.12, 3.12); ax.set_ylim(0.25, 1.06); ax.set_xticks(hs); ax.set_yticks([0.25, 0.5, 0.75, 1.0])
    ax.set_xlabel('Honest flips per decision'); ax.set_ylabel('Independence once the\nwatcher knows the habit')
    ax.legend(loc='lower right', frameon=False, handlelength=1.6, fontsize=7.8, labelcolor=INK, bbox_to_anchor=(1.0, -0.02))
    fig.tight_layout(pad=0.3); save(fig, 'wirings')


def wirings_routes():
    """Chapter 9, the story. Two hundred and fifty mornings under each wiring, every route drawn. A picture of the story, not a
    result: the days per district are those of the figure Aaron kept from 2026-08-15 (veras_two_wirings_v2, whose script was
    never committed); the curves are drawn here with a fixed seed. Wiring one: habit picks the district, the flips pick the
    alley. Wiring two: three flips pick the district, habit tilts the odds."""
    import matplotlib.patheffects as pe
    from matplotlib.path import Path
    from matplotlib.collections import PathCollection
    D = np.array([(-3.40, 3.80), (-2.22, 3.96), (-1.73, 5.56), (-0.51, 5.16), (0.46, 4.47), (1.65, 5.23), (2.32, 4.10), (3.63, 4.04)])
    days = {'one': [4, 3, 198, 26, 6, 7, 4, 2], 'two': [25, 22, 47, 37, 22, 28, 38, 31]}
    assert sum(days['one']) == 250 and sum(days['two']) == 250
    WW = W + 1.12 + 0.24                                           # text block plus the ledger column
    fig, axs = plt.subplots(1, 2, figsize=(WW, 3.05))
    halo = [pe.withStroke(linewidth=2.2, foreground='white', alpha=0.9)]
    spec = (('one', ORANGE, 'Wiring one: flips decide the small things', 'Habit picks the district.'),
            ('two', BLUE, 'Wiring two: flips decide the big things', 'Habit only bends the odds.'))
    for ax, (key, col, title, sub) in zip(axs, spec):
        rng = np.random.default_rng(9 if key == 'one' else 11)
        paths = []
        for d, k in enumerate(days[key]):
            for _ in range(k):
                end = D[d] + rng.normal(0, 0.30, 2)
                c1 = np.array([rng.normal(0.22 * end[0], 0.85), rng.uniform(1.2, 2.7)])
                c2 = end + np.array([rng.normal(0, 0.75), -rng.uniform(0.8, 2.0)])
                paths.append(Path([(0, 0), c1, c2, end], [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]))
        ax.add_collection(PathCollection(paths, facecolors='none', edgecolors=col, linewidths=0.55, alpha=0.13 if key == 'one' else 0.16, zorder=2))
        ax.plot(D[:, 0], D[:, 1], 'o', ms=3.6, color=INK, mec='white', mew=0.7, zorder=5)
        for d, k in enumerate(days[key]):
            ax.text(D[d, 0], D[d, 1] + 0.26, f'D{d + 1}\n{k} days', ha='center', va='bottom', fontsize=6.3, color=INK, linespacing=1.0, zorder=6, path_effects=halo)
        ax.plot([0], [0], 's', ms=5.5, color=INK, zorder=6); ax.text(0, -0.36, 'home', ha='center', va='top', fontsize=6.8, color=INK)
        ax.text(0.5, 1.085, title, transform=ax.transAxes, ha='center', va='bottom', fontsize=8.2, color=INK, fontweight='semibold')
        ax.text(0.5, 1.075, sub, transform=ax.transAxes, ha='center', va='top', fontsize=7.6, color=MUTED)
        ax.set_xlim(-4.5, 4.75); ax.set_ylim(-0.95, 6.75); ax.set_aspect('equal'); ax.axis('off')
    axs[0].annotate('the rut the file reads:\nthe robber waits\non this road', (-0.72, 2.75), (1.25, 1.15), fontsize=7.0, color=INK, va='center', linespacing=1.1,
                    arrowprops=dict(arrowstyle='->', color=INK, lw=0.7, shrinkA=2, shrinkB=1), zorder=7, path_effects=halo)
    axs[1].text(-4.45, 0.72, 'no rut forms. The lean\nshows (D3 is the busiest)\nand buys nothing: no one\nroad is worth waiting on', fontsize=7.0, color=INK, va='center', ha='left',
                linespacing=1.1, zorder=7, path_effects=halo)
    fig.subplots_adjust(left=0.0, right=1.0, top=0.87, bottom=0.0, wspace=0.02); save(fig, 'wirings_routes')
    print('wirings_routes: days', days)


# ------------------------------------------------------------------------------------------------ Chapter 10
def neighbors():
    """Theorem 12, numbers as printed (code/neighbors_T12_P15.py)."""
    labs = ['Alone', 'Unreadable\nneighbor', 'Ordinary\nneighbor', 'Flawless\nexpert']
    ceil = [0.77, 0.71, 0.61, 0.0]; gate_ = [0.50, 0.18, 0.01, None]
    fig, ax = axes(2.35, ncols=2)
    for a, vals, title in ((ax[0], ceil, 'Ceiling on your independence'), (ax[1], gate_, 'Education needed to open your gate')):
        for i, v in enumerate(vals):
            if v is None:
                a.text(i, 0.03, 'never\nopens', ha='center', va='bottom', fontsize=7.6, color=INK); continue
            a.bar(i, v, width=0.5, color=BLUE, lw=0)
            a.text(i, v + 0.02, f'{v:.2f}' if v else '0', ha='center', va='bottom', fontsize=7.6, color=INK)
        a.set_xticks(range(4)); a.set_xticklabels(labs, fontsize=6.5, color=INK, linespacing=1.05)
        a.set_ylim(0, 0.95); a.set_yticks([0, 0.25, 0.5, 0.75]); a.set_title(title, fontsize=8, color=INK, loc='left', pad=6)
    fig.tight_layout(pad=0.3, w_pad=1.6); save(fig, 'neighbors')


# ------------------------------------------------------------------------------------------------ Chapter 11
def run3(q, days=90):
    """chance of three bad days running within a season, when each day is bad with chance q (exact)"""
    st = np.array([1.0, 0, 0]); dead = 0.0
    for _ in range(days):
        new = np.zeros(3); new[0] = (st.sum()) * (1 - q); new[1] = st[0] * q; new[2] = st[1] * q; dead += st[2] * q; st = new
    return dead


def maj_fail(n, p, need=None):
    need = need or (n // 2 + 1)
    return sum(comb(n, k) * p ** k * (1 - p) ** (n - k) for k in range(need))


def town_heads():
    ns = [1, 3, 5, 7, 9, 11, 13, 15]; fam = [run3(maj_fail(n, 0.7)) for n in ns]
    master = run3(0.2)
    print('town: famine by independent fishers', dict(zip(ns, np.round(fam, 4))), 'master', round(master, 3), '(book: nine 0.074, master 0.44)')
    fig, ax = axes(2.6)
    ax.axhline(master, color=ORANGE, lw=1.6)
    ax.text(15.4, master * 0.86, 'every boat behind an 80% master', fontsize=7.6, color=MUTED, ha='right', va='top')
    ax.plot(ns, fam, '-o', color=BLUE, lw=1.8, ms=5.5, mec='white', mew=1.3)
    ax.annotate('nine fishers taught by one tutor\nsit here, with the single fisher', (1, fam[0]), (2.2, 0.98), fontsize=7.6, color=INK, va='center',
                arrowprops=dict(arrowstyle='-', color=SOFT, lw=0.7))
    ax.annotate(f'nine independent fishers: {fam[4]:.3f}', (9, fam[4]), (9.4, fam[4] * 1.9), fontsize=7.6, color=INK,
                arrowprops=dict(arrowstyle='-', color=SOFT, lw=0.7))
    ax.set_yscale('log'); ax.set_ylim(0.004, 1.3); ax.set_yticks([0.01, 0.1, 1]); ax.set_yticklabels(['1 in 100', '1 in 10', 'certain'])
    ax.set_xticks(ns); ax.set_xlim(0.4, 15.6)
    ax.set_xlabel('Independent fishers, each right 70 days in 100'); ax.set_ylabel('Chance of famine in a season')
    fig.tight_layout(pad=0.3); save(fig, 'town_heads')


def town_dose():
    """k boats follow an 80% master, 9-k read for themselves at 70%; a good day needs five boats on the fish."""
    def bad(k):
        r = 9 - k
        ok_right = sum(comb(r, j) * 0.7 ** j * 0.3 ** (r - j) for j in range(max(0, 5 - k), r + 1))      # master right: k on the fish
        ok_wrong = sum(comb(r, j) * 0.7 ** j * 0.3 ** (r - j) for j in range(5, r + 1)) if r >= 5 else 0.0
        return 1 - (0.8 * ok_right + 0.2 * ok_wrong)
    ks = list(range(10)); fam = [run3(bad(k)) for k in ks]
    print('town: famine by followers', dict(zip(ks, np.round(fam, 4))), '(book: one follower safest; five or more = the master alone)')
    fig, ax = axes(2.4)
    cols = [BLUE if k < 5 else ORANGE for k in ks]
    ax.bar(ks, fam, width=0.55, color=cols, lw=0)
    for k in ks: ax.text(k, fam[k] + 0.012, f'{100 * fam[k]:.0f}%' if fam[k] > 0.095 else f'{100 * fam[k]:.1f}%', ha='center', va='bottom', fontsize=7.4, color=INK)
    ax.text(7, 0.52, 'from five followers on,\nthe master decides every day', fontsize=7.6, color=MUTED, ha='center', va='bottom')
    ax.set_xticks(ks); ax.set_ylim(0, 0.62); ax.set_yticks([0, 0.2, 0.4, 0.6]); ax.set_yticklabels(['0', '20%', '40%', '60%'])
    ax.set_xlabel('Boats of the nine that follow the master'); ax.set_ylabel('Chance of famine in a season')
    fig.tight_layout(pad=0.3); save(fig, 'town_dose')


def town_window():
    """Theorem 21: a public signal right with chance a; readers right 0.7; the reading town's majority right 0.901."""
    p = 0.7; pm = 1 - maj_fail(9, p); a = np.linspace(0.5, 1.0, 501)
    fam = np.where(a > p, [run3(1 - x) for x in a], run3(1 - pm))
    print('town: window', round(p, 3), 'to', round(pm, 3), 'famine at lower edge', round(run3(1 - 0.7001), 3), 'reading town', round(run3(1 - pm), 3))
    fig, ax = axes(2.5)
    ax.axvspan(p, pm, color='#f1f0ec', lw=0)
    ax.axhline(run3(1 - pm), color=INK, lw=0.9)
    lo = a <= p
    ax.plot(a[lo], fam[lo], color=BLUE, lw=1.8); ax.plot(a[~lo], fam[~lo], color=BLUE, lw=1.8)
    ax.plot([p, p], [run3(1 - pm), run3(1 - p)], color=BLUE, lw=1.0, alpha=0.5)
    ax.text(pm - 0.006, 0.94, 'the window', fontsize=7.8, color=INK, ha='right')
    ax.text(pm - 0.006, 0.88, 'every boat right more often,\nthe town hungry more often', fontsize=7.3, color=MUTED, ha='right', va='top')
    ax.text(0.505, run3(1 - pm) + 0.02, 'the town that reads for itself: 7.4%', fontsize=7.5, color=MUTED, va='bottom')
    ax.set_xlim(0.5, 1.0); ax.set_ylim(0, 1.0); ax.set_xticks([0.5, 0.6, 0.7, 0.8, 0.9, 1.0]); ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0]); ax.set_yticklabels(['0', '25%', '50%', '75%', '100%'])
    ax.set_xlabel('How often the signal everyone can see is right'); ax.set_ylabel('Chance of famine in a season')
    fig.tight_layout(pad=0.3); save(fig, 'town_window')


def two_arrangements():
    """Chapter 11 §2, 'Two more arrangements': every number the paragraph states, on one scale of a hundred.
    code/results/borrowed_record.md (Theorem 22), stay_ashore.md and attack_T22_T23.md (Theorem 23)."""
    rows = [('H', "The sage's tally"),
            ('S', 'One boat: mornings right, in a hundred'),
            ('R', 'reading for itself', 79.5, BLUE, '79.5'), ('R', 'behind the sage', 85.0, ORANGE, '85'),
            ('S', 'The town: seasons of famine, in a hundred'),
            ('R', 'every boat reads for itself', 11.0, BLUE, '11'), ('R', 'every boat behind the sage', 22.5, ORANGE, '22.5'),
            ('R', 'two tallies kept, plain days and hard', 10.9, BLUE, '11'), ('R', 'the catch is shared: two boats follow', 14.2, BLUE, '14'),
            ('G',),
            ('H', 'The boat that stays in'),
            ('S', 'The town: seasons of famine, in a hundred'),
            ('R', 'every boat sails', 7.4, BLUE, '7'), ('R', 'four boats in ten stay in', 98.2, ORANGE, '98'),
            ('S', "Mornings in a hundred on which one more boatload saves the day"),
            ('R', 'in a town of nine boats', 26.7, BLUE, '27'), ('R', 'in a town of ninety-nine', 7.9, BLUE, '8')]
    step = {'H': 1.25, 'S': 1.05, 'R': 1.0, 'G': 0.55}
    y = 0.0; ys = []
    for r in rows:
        y -= step[r[0]]; ys.append(y)
    fig = plt.figure(figsize=(W, 3.95)); ax = fig.add_axes([0.50, 0.015, 0.47, 0.97])
    ax.axis('off'); ax.set_xlim(0, 108); ax.set_ylim(y - 0.6, 0.1)
    for r, yy in zip(rows, ys):
        if r[0] == 'H':
            ax.text(-113, yy, r[1], fontsize=8.6, color=INK, fontweight='semibold', va='center', ha='left')
            ax.plot([-113, 108], [yy - 0.52, yy - 0.52], color=SOFT, lw=0.6, clip_on=False)
        elif r[0] == 'S':
            ax.text(-113, yy - 0.08, r[1], fontsize=7.6, color=MUTED, va='center', ha='left')
        elif r[0] == 'R':
            _, lab, v, col, txt = r
            ax.text(-3, yy, lab, fontsize=7.7, color=INK, va='center', ha='right')
            ax.plot([0, 100], [yy, yy], color=GRID, lw=5.2, solid_capstyle='butt', zorder=1)
            ax.plot([0, v], [yy, yy], color=col, lw=5.2, solid_capstyle='butt', zorder=2)
            ax.text(v + 2.5 if v < 88 else v - 2.5, yy, txt, fontsize=7.8, color=INK if v < 88 else 'white', va='center', ha='left' if v < 88 else 'right',
                    fontweight='medium', zorder=3)
    save(fig, 'two_arrangements')
    print('two arrangements: checked against borrowed_record.md (79.5/85; 11.0/22.5/10.9/14.2) and stay_ashore.md, attack (7.4/98.2; 0.267/0.079)')


def standing():
    """Part V, 'Why the self-anointed rule'. code/results/borrowed_record.md, 'How long the standing lasts': days to the first
    recorded miss of a voice believed never wrong = 1 / (hard-day share 0.3 x miss rate 0.5 x share recorded)."""
    labs = ['Every hard day scored', 'One in three', 'One in ten', 'One in thirty', 'One in a hundred']
    v = [1, 0.3, 0.1, 0.03, 0.01]; days = [1 / (0.3 * 0.5 * x) for x in v]
    print('standing: days to the first recorded miss', [round(d) for d in days], '(results file: 7, 22, 67, 222, 667)')
    txt = ['a week', '22 days', '67 days', '222 days: two and a half seasons', '667 days: over seven seasons']
    fig, ax = axes(1.8); ax.grid(False); ax.grid(axis='x', color=GRID, lw=0.6)
    for i, (d, t) in enumerate(zip(days, txt)):
        yy = len(v) - 1 - i
        ax.plot([3, d], [yy, yy], color=GRID, lw=1.2, zorder=1)
        ax.plot([d], [yy], 'o', ms=6.5, color=BLUE, mec='white', mew=1.3, zorder=3)
        ax.text(d * 1.28, yy, t, va='center', ha='left', fontsize=7.8, color=INK)
    ax.set_yticks(range(len(v))); ax.set_yticklabels(labs[::-1], color=INK, fontsize=7.8)
    ax.set_xscale('log'); ax.set_xlim(3, 90000); ax.set_ylim(-0.6, len(v) - 0.4)
    ax.set_xticks([7, 90, 900]); ax.set_xticklabels(['one week', 'one season', 'ten seasons']); ax.minorticks_off()
    ax.set_xlabel("Days until the sage's first recorded miss (log scale)")
    ax.spines['bottom'].set_visible(False)
    fig.tight_layout(pad=0.3); save(fig, 'standing')


def fringe():
    """Part V, 'The law's own exhibit': the total coincidence rate against the relative analyzer angle. The curve is the second
    paper's (arXiv:2608.18886, Sec. 8), recomputed by code/fringe_2608_18886.py and checked there against the paper's printed
    numbers (12.4 percent deep; equal at 22.5 and 67.5 degrees). The book's text gives the surviving share: about a seventh."""
    d = np.loadtxt(os.path.join(HERE, '..', 'code', 'results', 'fringe_2608_18886.csv'), delimiter=',', skiprows=1); D, R = d[:, 0], d[:, 1]
    print(f'fringe: peak to peak {R.max() - R.min():.4f} (paper 0.124); R(22.5) - R(67.5) = {R[45] - R[135]:.1e}')
    fig, ax = axes(2.95)
    l1, = ax.plot(D, R, color='#a9c8ef', lw=1.6, zorder=2); l2, = ax.plot(D, 1 + (R - 1) / 7, color=BLUE, lw=2.0, zorder=3)
    l0 = ax.axhline(1, color=INK, lw=1.1, zorder=4)
    for a in (22.5, 67.5):
        ax.axvline(a, color=MUTED, lw=0.7, ls=(0, (3, 2)), zorder=1)
        ax.plot([a], [R[int(2 * a)]], 'o', ms=4.6, color='#a9c8ef', mec='white', mew=0.9, zorder=5)
        ax.plot([a], [1 + (R[int(2 * a)] - 1) / 7], 'o', ms=4.6, color=BLUE, mec='white', mew=0.9, zorder=6)
    ax.text(71, 0.9265, 'the two angles the standard test compares:\nthe fringe has the same value at both', ha='left', va='center', fontsize=7.4, color=INK, linespacing=1.1)
    ax.legend([l0, l1, l2], ['Quantum mechanics: flat', 'The solved class at full strength, 12.4 percent deep: ruled out by the record',
                             'The same class at a one-seventh share: the most the record allows'],
              loc='lower left', bbox_to_anchor=(-0.215, 1.0), frameon=False, fontsize=7.5, handlelength=1.6, labelspacing=0.25, borderaxespad=0.2, labelcolor=INK)
    ax.set_xlim(0, 180); ax.set_ylim(0.908, 1.082); ax.set_xticks([0, 22.5, 45, 67.5, 90, 135, 180]); ax.set_xticklabels(['0°', '22.5°', '45°', '67.5°', '90°', '135°', '180°'])
    ax.set_yticks([0.94, 0.97, 1.0, 1.03, 1.06]); ax.set_yticklabels(['−6%', '−3%', 'mean', '+3%', '+6%'])
    ax.set_xlabel('Angle between the two analyzers'); ax.set_ylabel('Rate of paired detections,\nall outcomes summed')
    fig.tight_layout(pad=0.3); save(fig, 'fringe')


def holdings():
    """Part V, 'Why the self-anointed rule': the four numbers the paragraph prints (Survey of Consumer Finances 2022; Federal
    Reserve Distributional Financial Accounts, mid-2026). The middle segment of the bar is what the two printed shares leave."""
    fig = plt.figure(figsize=(W, 2.05))
    fig.text(0.02, 0.985, 'Of all the stock American households hold', fontsize=8.2, color=INK, fontweight='semibold', va='top', ha='left')
    ax = fig.add_axes([0.02, 0.70, 0.96, 0.16]); ax.axis('off'); ax.set_xlim(0, 100); ax.set_ylim(0, 1)
    ax.barh(0.5, 88, left=0, height=1, color=BLUE, lw=0); ax.barh(0.5, 100 - 88 - 0.6 - 0.5, left=88.25, height=1, color='#a9c8ef', lw=0)
    ax.barh(0.5, 0.6, left=99.4, height=1, color=ORANGE, lw=0)
    ax.text(2, 0.5, 'the top tenth of households hold 88 percent', fontsize=7.8, color='white', va='center', ha='left', fontweight='medium')
    ax.annotate('the bottom half hold 0.6 percent', (99.7, -0.05), (99.7, -0.75), fontsize=7.6, color=INK, ha='right', va='top',
                arrowprops=dict(arrowstyle='-', color=MUTED, lw=0.6, shrinkA=1, shrinkB=0), annotation_clip=False)
    fig.text(0.02, 0.40, 'The typical holding, among households that hold any', fontsize=8.2, color=INK, fontweight='semibold', va='top', ha='left')
    ax2 = fig.add_axes([0.30, 0.0, 0.68, 0.29]); ax2.axis('off'); ax2.set_xlim(0, 608000 * 1.36); ax2.set_ylim(-0.6, 1.6)
    for yy, lab, v, col, txt in ((1, 'the top tenth', 608000, BLUE, '608,000 dollars'), (0, 'the lower half of incomes', 12600, ORANGE, '12,600 dollars')):
        ax2.barh(yy, v, height=0.52, color=col, lw=0)
        ax2.text(v + 608000 * 0.02, yy, txt, fontsize=7.8, color=INK, va='center', ha='left')
        ax2.text(-608000 * 0.02, yy, lab, fontsize=7.7, color=INK, va='center', ha='right')
    save(fig, 'holdings')


def cover_art():
    """The cover: two hundred and fifty routes under the second wiring (Chapter 9), drawn large. Decoration, not data."""
    from matplotlib.path import Path
    from matplotlib.collections import PathCollection
    D = np.array([(-3.40, 3.80), (-2.22, 3.96), (-1.73, 5.56), (-0.51, 5.16), (0.46, 4.47), (1.65, 5.23), (2.32, 4.10), (3.63, 4.04)])
    days = [25, 22, 47, 37, 22, 28, 38, 31]; rng = np.random.default_rng(11); paths = []
    for d, k in enumerate(days):
        for _ in range(k):
            end = D[d] + rng.normal(0, 0.30, 2)
            c1 = np.array([rng.normal(0.22 * end[0], 0.85), rng.uniform(1.2, 2.7)]); c2 = end + np.array([rng.normal(0, 0.75), -rng.uniform(0.8, 2.0)])
            paths.append(Path([(0, 0), c1, c2, end], [Path.MOVETO, Path.CURVE4, Path.CURVE4, Path.CURVE4]))
    fig = plt.figure(figsize=(5.6, 4.29)); ax = fig.add_axes([0, 0, 1, 1]); ax.axis('off')
    ax.add_collection(PathCollection(paths, facecolors='none', edgecolors='#1C5CAB', linewidths=0.8, alpha=0.17))
    ax.plot([0], [0], 's', ms=7, color=INK)
    ax.set_xlim(-4.75, 4.95); ax.set_ylim(-0.25, 7.18); ax.set_aspect('equal')
    save(fig, 'cover_art')


# ------------------------------------------------------------------------------------------------ Chapter 13
def cascade():
    """code/imposition_cascade_T17.py, reference cascade (its printed table)."""
    lev = ['Executive\n(1)', 'Regionals\n(4)', 'Managers\n(16)', 'Workers\n(64)']
    faced = [100, 40, 20, 14]; loss = [0.80, 0.80, 2.00, 7.91]
    fig, ax = axes(2.3, ncols=2)
    for a, vals, title, fmt in ((ax[0], faced, 'Uncertainty reaching each person\n(the executive = 100)', '{:.0f}'), (ax[1], loss, 'Agency lost by each person\n(model units)', '{:.2f}')):
        a.bar(range(4), vals, width=0.5, color=BLUE, lw=0)
        for i, v in enumerate(vals): a.text(i, v * 1.02 + max(vals) * 0.01, fmt.format(v), ha='center', va='bottom', fontsize=7.6, color=INK)
        a.set_xticks(range(4)); a.set_xticklabels(lev, fontsize=6.9, color=INK); a.set_title(title, fontsize=8, color=INK, loc='left', pad=6)
        a.set_ylim(0, max(vals) * 1.17); a.set_yticks([])
        a.grid(False)
    fig.tight_layout(pad=0.3, w_pad=1.4); save(fig, 'cascade')
    tot = np.array(loss) * np.array([1, 4, 16, 64]); print('cascade: share borne by workers', round(tot[-1] / tot.sum(), 4))


def shed_bands():
    """code/field/results/shed_oos_test.md, H3, pooled 2019-2021 (weighted share of employees)."""
    bands = ['under\n$10k', '$10k–\n25k', '$25k–\n50k', '$50k–\n75k', '$75k–\n100k', '$100k–\n150k', '$150k\nor more']
    v = [27.8, 24.9, 21.7, 17.3, 15.9, 13.4, 11.9]
    fig, ax = axes(2.25)
    ax.bar(range(7), v, width=0.52, color=BLUE, lw=0)
    for i, x in enumerate(v): ax.text(i, x + 0.6, f'{x:.0f}%', ha='center', va='bottom', fontsize=7.6, color=INK)
    ax.set_xticks(range(7)); ax.set_xticklabels(bands, fontsize=7, color=INK); ax.set_ylim(0, 33); ax.set_yticks([0, 10, 20, 30]); ax.set_yticklabels(['0', '10%', '20%', '30%'])
    ax.set_xlabel('Household income'); ax.set_ylabel("Employees whose hours\nvary on the employer's needs")
    fig.tight_layout(pad=0.3); save(fig, 'shed_bands')


def shed_tests():
    """code/field/results/shed_oos_test.md (H1, employer - own, pooled 2019-2021) and shed_panel_test.md (H4, same person)."""
    left = [('Just getting by, or worse', 7.5, 5.0, 9.8), ('Behind on bills because\nincome varied', 5.5, 3.3, 7.7),
            ('Cannot meet a $400 expense', 2.4, 0.7, 4.4), ('No three-month fund', 1.5, -1.5, 4.7)]
    right = [('Just getting by, or worse', 3.0, 0.3, 5.7), ('Behind on bills because\nincome varied', 6.1, 3.7, 8.7),
             ('Cannot meet a $400 expense', -0.5, -2.6, 1.5), ('No three-month fund', 1.8, -1.4, 5.1)]
    fig, ax = axes(2.4, ncols=2, sharey=True)
    for a, rows, title in ((ax[0], left, "Across employees,\n2019–2021"),
                           (ax[1], right, "The same person,\nacross years")):
        a.grid(False); a.grid(axis='x', color=GRID, lw=0.6); a.axvline(0, color=INK, lw=0.8)
        for i, (lab, m, lo, hi) in enumerate(rows):
            y = len(rows) - 1 - i
            a.plot([lo, hi], [y, y], color=BLUE, lw=1.6, solid_capstyle='round'); a.plot([m], [y], 'o', ms=5.5, color=BLUE, mec='white', mew=1.2)
            a.text(hi + 0.5, y, f'{m:+.1f}', va='center', ha='left', fontsize=7.6, color=INK)
        a.set_xlim(-4, 13.5); a.set_xticks([0, 5, 10]); a.set_ylim(-0.6, len(rows) - 0.4)
        a.set_title(title, fontsize=7.4, color=INK, loc='left', pad=6); a.spines['bottom'].set_visible(False)
        a.set_xlabel('Percentage points')
    ax[0].set_yticks(range(len(left))); ax[0].set_yticklabels([r[0] for r in left][::-1], fontsize=7.4, color=INK)
    fig.subplots_adjust(left=0.345, right=0.985, top=0.83, bottom=0.18, wspace=0.14); save(fig, 'shed_tests')


# ------------------------------------------------------------------------------------------------ Chapter 14
def three_scores():
    """code/results/joined_three_rulers.md, the printed economy (p_top = 0.9, gamma = 1)."""
    prog = ['No program', 'Time transfer', 'Cash, cost of the time transfer', 'Steadier schedule', 'Cash, cost of the steadier schedule']
    cons = [0.0, -0.68, 5.90, -0.07, 1.38]; bw = [0.30, 0.65, 0.29, 0.42, 0.30]; fam = [10.7, 0.2, 11.3, 4.3, 10.8]
    cols = [SOFT, BLUE, ORANGE, BLUE, ORANGE]
    fig, ax = axes(2.35, ncols=3, sharey=True)
    specs = ((ax[0], cons, "Consumption\n(lifetime value)", '{:+.2f}', (-1.6, 9.4)),
             (ax[1], bw, 'Capacity to plan\n(bandwidth)', '{:.2f}', (0, 0.9)),
             (ax[2], fam, 'Survival (famine\nseasons per 100)', '{:.1f}', (0, 16.5)))
    for a, vals, title, fmt, xl in specs:
        a.grid(False); a.axvline(0, color=SOFT, lw=0.8)
        for i, v in enumerate(vals):
            y = len(vals) - 1 - i
            a.barh(y, v, height=0.5, color=cols[i], lw=0)
            a.text((v if v > 0 else 0) + (xl[1] - xl[0]) * 0.03, y, fmt.format(v), va='center', ha='left', fontsize=7.4, color=INK)
        a.set_xlim(*xl); a.set_xticks([]); a.set_title(title, fontsize=7.6, color=INK, loc='left', pad=6); a.spines['bottom'].set_visible(False)
    ax[0].set_yticks(range(5)); ax[0].set_yticklabels(prog[::-1], fontsize=7.4, color=INK)
    fig.subplots_adjust(left=0.40, right=0.99, top=0.82, bottom=0.04, wspace=0.12); save(fig, 'three_scores')


if __name__ == '__main__':
    for f in (staircase, gate, frontier, pricelist, watchers, wirings_routes, wirings, neighbors, town_heads, town_dose, town_window, two_arrangements,
              standing, fringe, holdings, cover_art, cascade, shed_bands, shed_tests, three_scores):
        f()
    print('charts written to design/fig/')
