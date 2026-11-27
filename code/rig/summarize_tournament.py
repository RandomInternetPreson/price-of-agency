"""
summarize_tournament.py -- tables + figures from watcher_tournament.py results.

  python summarize_tournament.py results/            -> results/TOURNAMENT_SUMMARY.md, results/fig_*.png

Reads every shard_*.jsonl, merges by config id (latest wins), and writes:
  Table Q3  how much watcher does the inversion cost  (per policy/wiring/m_S/h: exact floor
            vs wrong-Bayesian vs best pattern-miner vs gru-l vs tf-l; inverted flags; gaps)
  Table Q5  dichotomy on random wirings and large habit spaces (exact AND learned floors)
  Table Q7  the regress: floors vs coin generator (iid vs lcg:k) per watcher
  Fig  1    floors vs h, one panel per (policy, wiring), watcher = line
  Fig  2    delta_W(t) lifetimes for the m_S=1024 gated/additive configs (exact vs learned)
  Fig  3    regress: floor vs generator state bits
Every number is a model-world quantity (n, s, m_S fixed); none is asserted of the world.
"""
import glob, json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# fixed hue order by watcher identity (never cycled): exact, wrong, miner, gru, tf
PAL = {'bayes': '#2a78d6', 'bayes-wrong': '#eb6834', 'markov': '#1baf7a', 'gru-l': '#eda100',
       'tf-l': '#e87ba4', 'gru-s': '#eda100', 'tf-s': '#e87ba4', 'sage': '#555555', 'exact': '#2a78d6'}
WATCHERS = ['bayes', 'bayes-wrong', 'markov', 'gru-l', 'tf-l', 'gru-s', 'tf-s']


def load(outdir):
    recs = {}
    for fn in sorted(glob.glob(os.path.join(outdir, 'shard_*.jsonl'))):
        with open(fn) as f:
            for line in f:
                try:
                    r = json.loads(line); recs[r['id']] = r
                except Exception:
                    pass
    return list(recs.values())


def best_markov(r):
    ks = [k for k in r['floors'] if k.startswith('markov')]
    return min(r['floors'][k] for k in ks) if ks else float('nan')


def group(recs, keys):
    g = {}
    for r in recs:
        g.setdefault(tuple(r[k] for k in keys), []).append(r)
    return g


def fmt(x):
    return '  —  ' if x is None or (isinstance(x, float) and np.isnan(x)) else f"{x:.3f}"


def table_rows(recs, keys, header_extra=''):
    """one row per (keys): floors per watcher, taking the arch-specific floor from the record that trained it."""
    rows = []
    for key, rs in sorted(group(recs, keys).items()):
        r0 = rs[0]
        fl = {'exact': r0['dinf_exact'], 'd0': r0['d0'], 'sage': r0['sage'], 'wall': r0['wall'],
              'bayes-wrong': np.mean([r['floors']['bayes-wrong'] for r in rs]),
              'markov': np.mean([best_markov(r) for r in rs])}
        conv = max(abs(r['bayes_converged']) for r in rs)
        for arch in ['gru-s', 'gru-l', 'tf-s', 'tf-l']:
            a = [r['floors'][arch] for r in rs if r['arch'] == arch]
            fl[arch] = np.mean(a) if a else float('nan')
        rows.append((key, fl, conv))
    return rows


def md_table(rows, keys):
    archs = [a for a in ['gru-s', 'gru-l', 'tf-s', 'tf-l'] if any(not np.isnan(fl[a]) for _, fl, _ in rows)]
    head = ['/'.join(keys), 'sage', 'wall', 'd0 (seed unk.)', 'exact floor', 'wrong-Bayes', 'best miner'] + archs + ['inv exact', 'inv learned', 'conv']
    out = ['| ' + ' | '.join(head) + ' |', '|' + '---|' * len(head)]
    for key, fl, conv in rows:
        learned = [fl[a] for a in archs if not np.isnan(fl[a])]
        inv_l = 'yes' if learned and min(learned) < fl['sage'] else ('no' if learned else '—')
        out.append('| ' + ' | '.join([' / '.join(map(str, key)), fmt(fl['sage']), fmt(fl['wall']), fmt(fl['d0']), fmt(fl['exact']),
                                      fmt(fl['bayes-wrong']), fmt(fl['markov'])] + [fmt(fl[a]) for a in archs]
                                     + ['yes' if fl['exact'] < fl['sage'] else 'no', inv_l, ('ok' if conv < 0.01 else f'{conv:+.3f}')]) + ' |')
    return '\n'.join(out)


def fig_floors_vs_h(recs, outdir):
    core = [r for r in recs if r['gen'] == 'iid' and r['obs'] == 'EA' and r['n'] == 4]
    if not core:
        return None
    pols = sorted({r['policy'] for r in core}); wirs = sorted({r['wiring'] for r in core})
    mSs = sorted({r['m_S'] for r in core})
    fig, axes = plt.subplots(len(pols), len(wirs), figsize=(4.2 * len(wirs), 3.4 * len(pols)), squeeze=False, sharey=True)
    for i, pol in enumerate(pols):
        for j, wir in enumerate(wirs):
            ax = axes[i, j]
            rs = [r for r in core if r['policy'] == pol and r['wiring'] == wir]
            if not rs:
                ax.axis('off'); continue
            ax.axhline(rs[0]['sage'], color=PAL['sage'], lw=1, ls='--')
            ax.text(0.98, rs[0]['sage'] + 0.01, 'sage', ha='right', va='bottom', fontsize=8, color=PAL['sage'], transform=ax.get_yaxis_transform())
            for mi, m_S in enumerate(mSs):
                ls = ['-', ':', '-.'][mi % 3]
                sub = sorted([r for r in rs if r['m_S'] == m_S], key=lambda r: r['h'])
                hs = sorted({r['h'] for r in sub})
                ex = [np.mean([r['dinf_exact'] for r in sub if r['h'] == h]) for h in hs]
                ax.plot(hs, ex, color=PAL['bayes'], lw=2, ls=ls, marker='o', ms=4, label=f'exact watcher, m_S={m_S}')
                mk = [np.mean([best_markov(r) for r in sub if r['h'] == h]) for h in hs]
                ax.plot(hs, mk, color=PAL['markov'], lw=1.5, ls=ls, marker='s', ms=4, label=f'best miner, m_S={m_S}')
                for arch in ['gru-l', 'tf-l']:
                    a = [[r['floors'][arch] for r in sub if r['h'] == h and r['arch'] == arch] for h in hs]
                    if all(len(x) for x in a):
                        ax.plot(hs, [np.mean(x) for x in a], color=PAL[arch], lw=1.5, ls=ls, marker='^', ms=4, label=f'{arch}, m_S={m_S}')
            ax.set_title(f'{pol} policy / {wir}', fontsize=10)
            ax.set_xlabel('fresh bits per action h'); ax.grid(alpha=0.25); ax.set_ylim(0.2, 1.1)
            if j == 0:
                ax.set_ylabel(r'floor $\delta_W$ (log-loss / log n)')
    h_, l_ = axes[0, 0].get_legend_handles_labels()
    fig.legend(h_, l_, loc='lower center', ncol=4, fontsize=8, frameon=False)
    fig.suptitle('Sustainable floors by watcher: exact Bayesian vs structure-free watchers  (model world n=4, s=0.5)', fontsize=11)
    fig.tight_layout(rect=[0, 0.1, 1, 0.95])
    p = os.path.join(outdir, 'fig_floors_vs_h.png'); fig.savefig(p, dpi=140); plt.close(fig)
    return p


def fig_lifetimes(recs, outdir):
    sel = [r for r in recs if r['gen'] == 'iid' and r['obs'] == 'EA' and r['n'] == 4 and r['m_S'] == max(x['m_S'] for x in recs)
           and r['wiring'] in ('gated', 'additive') and r['h'] == 3 and r['policy'] == 'hand']
    if not sel:
        return None
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    for ax, wir in zip(axes, ['gated', 'additive']):
        rs = [r for r in sel if r['wiring'] == wir]
        if not rs:
            ax.axis('off'); continue
        ax.axhline(rs[0]['sage'], color=PAL['sage'], lw=1, ls='--', label='sage ceiling')
        ax.axhline(rs[0]['dinf_exact'], color=PAL['bayes'], lw=1, ls=':', label='exact floor (seed known)')
        for r in rs:
            cur = np.load(os.path.join(outdir, 'curves', f"{r['id']}.npz"))
            t = np.arange(len(cur['bayes']))
            if r is rs[0]:
                ax.plot(t, cur['bayes'], color=PAL['bayes'], lw=2, label='exact Bayesian watcher')
                ax.plot(t, cur['bayes-wrong'], color=PAL['bayes-wrong'], lw=1.2, label='Bayesian with the wrong wiring')
                ks = [k for k in cur.files if k.startswith('markov')]
                if ks:
                    k = min(ks, key=lambda k: cur[k][-len(t) // 4:].mean())
                    ax.plot(t, cur[k], color=PAL['markov'], lw=1.2, label=f'best pattern miner ({k})')
            ax.plot(t, cur[r['arch']], color=PAL[r['arch']], lw=1.5, label=r['arch'])
        ax.set_title(f"hand policy / {wir} / m_S={rs[0]['m_S']} / h=3", fontsize=10)
        ax.set_xlabel('day of the watched lifetime'); ax.grid(alpha=0.25); ax.set_ylim(0.2, 1.15)
    axes[0].set_ylabel(r'$\delta_W(t)$ (log-loss / log n)')
    h_, l_ = axes[1].get_legend_handles_labels() if axes[1].lines else axes[0].get_legend_handles_labels()
    fig.legend(h_, l_, loc='lower center', ncol=4, fontsize=8, frameon=False)
    fig.suptitle('Watched lifetimes on the large habit space: how fast each watcher extracts the habit', fontsize=11)
    fig.tight_layout(rect=[0, 0.12, 1, 0.93])
    p = os.path.join(outdir, 'fig_lifetimes_large_mS.png'); fig.savefig(p, dpi=140); plt.close(fig)
    return p


def fig_regress(recs, outdir):
    rr = [r for r in recs if r['tier'] == 'R' or r['gen'] != 'iid']
    if not rr:
        return None
    gens = ['iid', 'lcg:32', 'lcg:16', 'lcg:12', 'lcg:8']
    xs = {'iid': 40, 'lcg:32': 32, 'lcg:16': 16, 'lcg:12': 12, 'lcg:8': 8}   # iid drawn at the right as "∞"
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8), sharey=True)
    for ax, wir in zip(axes, ['gated', 'additive']):
        for pol, mk in [('lam', 'o'), ('hand', 's')]:
            rs = [r for r in rr if r['wiring'] == wir and r['policy'] == pol]
            if not rs:
                continue
            ax.axhline(rs[0]['sage'], color=PAL['sage'], lw=1, ls='--')
            for arch in ['gru-l', 'tf-l']:
                pts = [(xs[g], np.mean([r['floors'][arch] for r in rs if r['gen'] == g and r['arch'] == arch])) for g in gens
                       if any(r['gen'] == g and r['arch'] == arch for r in rs)]
                if pts:
                    ax.plot(*zip(*pts), color=PAL[arch], marker=mk, ms=5, lw=1.5, ls='-' if pol == 'hand' else ':', label=f'{arch}, {pol} policy')
            pts = [(xs[g], np.mean([r['floors']['bayes'] for r in rs if r['gen'] == g])) for g in gens if any(r['gen'] == g for r in rs)]
            ax.plot(*zip(*pts), color=PAL['bayes'], marker=mk, ms=5, lw=2, ls='-' if pol == 'hand' else ':', label=f'Bayesian assuming a fresh coin, {pol}')
        ax.set_xticks([8, 12, 16, 32, 40]); ax.set_xticklabels(['8', '12', '16', '32', 'truly fresh'])
        ax.set_xlabel('hidden state of the coin generator (bits)'); ax.set_title(f'{wir} wiring, h=3, m_S=8', fontsize=10)
        ax.grid(alpha=0.25); ax.set_ylim(0.2, 1.15)
    axes[0].set_ylabel(r'floor $\delta_W$ (log-loss / log n)')
    h_, l_ = axes[0].get_legend_handles_labels()
    fig.legend(h_, l_, loc='lower center', ncol=3, fontsize=8, frameon=False)
    fig.suptitle('The regress: a pseudo-random coin is a habit one level up — can the watcher acquire it?', fontsize=11)
    fig.tight_layout(rect=[0, 0.14, 1, 0.93])
    p = os.path.join(outdir, 'fig_regress.png'); fig.savefig(p, dpi=140); plt.close(fig)
    return p


def main(outdir):
    recs = load(outdir)
    if not recs:
        print('no results found in', outdir); return
    md = [f"# Neural-watcher tournament — summary ({len(recs)} configurations)\n",
          "Floors = mean log-loss over the last quarter of the lifetime, in units of log2 n. "
          "'exact floor' = seed-known enumeration (the book's δ_∞). 'conv' = ok when the exact Bayesian's "
          "simulated reading is within 0.01 of its exact floor by the last eighth of life (else the lifetime was too short "
          "for that habit space; treat learned floors there as upper bounds on what a longer watch extracts). "
          "'wall' = I(A;F|E)/log n, the T9′ lower wall. All quantities are model-world (n, s fixed).\n"]
    core = [r for r in recs if r['gen'] == 'iid']
    if core:
        md.append("## Q3 / Q5 — how much watcher does the inversion cost; dichotomy on random wirings and large habit spaces\n")
        for (n, obs), rs in sorted(group(core, ['n', 'obs']).items()):
            md.append(f"### n = {n}, watcher sees {obs}\n")
            md.append(md_table(table_rows(rs, ['policy', 'wiring', 'm_S', 'h']), ['policy', 'wiring', 'm_S', 'h']) + '\n')
        # headline counts
        inv_ex = [r for r in core if r['wiring'] == 'gated' and r['h'] >= 1]
        n_inv_exact = sum(r['inverted_exact'] for r in inv_ex); n_inv_learned = sum(r['inverted_neural'] for r in inv_ex)
        md.append(f"**Gated configs (h ≥ 1): exact watcher inverted in {n_inv_exact}/{len(inv_ex)}; the trained watcher of the config "
                  f"inverted in {n_inv_learned}/{len(inv_ex)}.**\n")
        add3 = [r for r in core if r['wiring'] == 'additive' and r['h'] == 3]
        if add3:
            md.append("Additive at h = 3 (one-time-pad equality claims δ_∞ = seed-unknown): max |exact − d0| = "
                      f"{max(abs(r['dinf_exact'] - r['d0']) for r in add3):.4f}; learned floors minus d0: "
                      f"{min(r['floors'][r['arch']] - r['d0'] for r in add3):+.3f} … {max(r['floors'][r['arch']] - r['d0'] for r in add3):+.3f} "
                      "(a learned watcher cannot beat d0 here except by noise; negative values of size > 0.01 would refute equality).\n")
        rnd = [r for r in core if r['wiring'].startswith('random')]
        if rnd:
            md.append("Random wirings: exact floors " + ', '.join(f"h={h}: {np.mean([r['dinf_exact'] for r in rnd if r['h'] == h]):.3f}" for h in sorted({r['h'] for r in rnd}))
                      + f" (sage {rnd[0]['sage']:.3f}); gated-like if below the sage at every h, additive-like if rising to d0.\n")
    rr = [r for r in recs if r['tier'] == 'R' or r['gen'] != 'iid']
    if rr:
        md.append("## Q7 — the regress: floors vs coin generator (h = 3 nominal bits, m_S = 8, T = 512)\n")
        md.append(md_table(table_rows(rr, ['policy', 'wiring', 'gen']), ['policy', 'wiring', 'gen']) + '\n')
        md.append("Reading: under 'iid' the nominal coin is real. Under lcg:k the coin is a deterministic map of a k-bit hidden seed — "
                  "a habit one level up. If a learned watcher's floor falls with k while the fresh-coin Bayesian's does not, "
                  "the watcher has acquired the generator (the regress in action); the gap between them is the price of assuming freshness.\n")
    figs = [p for p in [fig_floors_vs_h(recs, outdir), fig_lifetimes(recs, outdir), fig_regress(recs, outdir)] if p]
    md.append("## Figures\n" + '\n'.join(f"- `{os.path.basename(p)}`" for p in figs) + '\n')
    secs = sum(r.get('seconds', 0) for r in recs)
    md.append(f"Compute: {secs / 3600:.2f} GPU-hours across {len(recs)} configs; devices {sorted({r['device'] for r in recs})}.\n")
    p = os.path.join(outdir, 'TOURNAMENT_SUMMARY.md')
    open(p, 'w', encoding='utf-8').write('\n'.join(md))
    print('\n'.join(md)); print('\nwrote', p, 'and', figs)


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results'))
