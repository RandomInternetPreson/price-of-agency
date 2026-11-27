"""summarize_two_asset.py -- reads results_two_asset/shard_*.jsonl (or a folder given as argv[1]) and writes TWO_ASSET_SWEEP_SUMMARY.md there."""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'results_two_asset')
R = {}
for fn in sorted(glob.glob(os.path.join(OUT, 'shard_*.jsonl'))):
    for line in open(fn, encoding='utf-8'):
        try:
            r = json.loads(line); R[r['draw']] = r
        except Exception:
            pass
ok = [r for r in R.values() if r.get('status') == 'ok']; bad = [r for r in R.values() if r.get('status') != 'ok']
did = lambda r, arm: (r[arm + '_dW_m'] - r[arm + '_dW_c'])
CLAIMS = [
    ('illiquid wealth lower in the model', lambda r: r['m_K'] < r['c_K']),
    ('liquid wealth lower (fixed returns)', lambda r: r['m_A'] < r['c_A']),
    ('market-clearing liquid rate above the control\'s (no crossing in the searched range: the sign of excess demand at the control\'s rate)',
     lambda r: (r['r_star'] > 0.005) if r.get('r_cross') else (r['m_A'] < r['c_A'])),
    ('poor hand-to-mouth share higher', lambda r: r['m_PHTM'] > r['c_PHTM']),
    ('wealthy hand-to-mouth share lower', lambda r: r['m_WHTM'] < r['c_WHTM']),
    ('total hand-to-mouth share higher', lambda r: r['m_HTM'] > r['c_HTM']),
    ('low-skill hand-to-mouth higher', lambda r: r['m_htm_low'] > r['c_htm_low']),
    ('dose: half dose moves illiquid wealth less, same sign', lambda r: 0 < (r['c_K'] - r['h_K']) < (r['c_K'] - r['m_K'])),
    ('P-C: low-skill gap stays positive after liquidity repair', lambda r: r['liq_htm_m'] - r['liq_htm_c'] > 0),
    ('time transfer lowers low-skill hand-to-mouth (model)', lambda r: r['time_htm_m'] < r['m_htm_low']),
    ('stability lowers low-skill hand-to-mouth (model)', lambda r: r['stab_htm_m'] < r['m_htm_low']),
    ('time transfer raises low-skill illiquid wealth (model)', lambda r: r['time_dK_m'] > 0),
    ('stability raises low-skill illiquid wealth (model)', lambda r: r['stab_dK_m'] > 0),
    ('equal-cost cash lowers low-skill illiquid wealth (model)', lambda r: r['money_dK_m'] < 0),
    ('time beats equal-cost cash on low-skill hand-to-mouth (model)', lambda r: r['time_htm_m'] < r['money_htm_m']),
    ('stability beats equal-cost cash on low-skill hand-to-mouth (model)', lambda r: r['stab_htm_m'] < r['trans_htm_m']),
    ('CASH beats time on low-skill welfare (model gain minus control gain)', lambda r: did(r, 'money') > did(r, 'time')),
    ('CASH beats stability on low-skill welfare (model gain minus control gain)', lambda r: did(r, 'trans') > did(r, 'stab')),
    ('cash beats time on low-skill welfare in the model economy alone', lambda r: r['money_dW_m'] > r['time_dW_m']),
    ('cash beats stability on low-skill welfare in the model economy alone', lambda r: r['trans_dW_m'] > r['stab_dW_m']),
    ('stability raises low-skill welfare by more in the model than in the control', lambda r: did(r, 'stab') > 0),
    ('stability, charged at its assumed price, raises low-skill welfare in the model economy', lambda r: r['stab_dW_m'] > 0),
    ('time transfer raises low-skill illiquid wealth WHERE IT CLEARS THE GATE (Tbar_low + 0.25 >= 2)', lambda r: (r['time_dK_m'] > 0) if r['Tbar_low'] >= 1.75 else None),
    ('time transfer raises low-skill illiquid wealth where it stops short of the gate', lambda r: (r['time_dK_m'] > 0) if r['Tbar_low'] < 1.75 else None),
]
def share(rs, f):
    v = [f(r) for r in rs]; v = [x for x in v if x is not None]
    return f"{np.mean(v):.3f} ({sum(v)}/{len(v)})" if v else 'n/a'
L = [f"# Two-asset sign map — {len(ok)} solved economies of {len(R)} drawn", "",
     "An economy whose CONTROL holds almost no illiquid wealth has nothing for the bandwidth tax to remove, and logit noise scatters its "
     "households upward off the floor; those economies are counted in 'all' and separated out in the other columns (control illiquid wealth "
     "of at least one quarter's mean income).", "",
     "| result | all | control holds illiquid wealth (K ≥ 1) | … and EIS 0.5 | … and log utility | control K < 1 |", "|---|---|---|---|---|---|"]
rich = [r for r in ok if r['c_K'] >= 1.0]; poor = [r for r in ok if r['c_K'] < 1.0]
for name, f in CLAIMS:
    L.append(f"| {name} | {share(ok, f)} | {share(rich, f)} | {share([r for r in rich if r['eis'] == 0.5], f)} | {share([r for r in rich if r['eis'] == 1.0], f)} | {share(poor, f)} |")
if ok:
    med = lambda k: np.median([r[k] for r in ok])
    L += ["", "## Magnitudes (median; 5th–95th percentile)", ""]
    for lab, fn in [('illiquid wealth, model / control', lambda r: r['m_K'] / r['c_K']), ('liquid wealth, model / control', lambda r: r['m_A'] / r['c_A']),
                    ('market-clearing liquid rate minus control\'s, points a year', lambda r: 400 * (r['r_star'] - 0.005) if r.get('r_cross') else np.nan),
                    ('poor hand-to-mouth, model − control', lambda r: r['m_PHTM'] - r['c_PHTM']), ('wealthy hand-to-mouth, model − control', lambda r: r['m_WHTM'] - r['c_WHTM']),
                    ('mass at the top of the liquid / illiquid grid (model)', lambda r: max(r['m_top_a'], r['m_top_k']))]:
        v = np.array([fn(r) for r in ok], dtype=float); v = v[np.isfinite(v)]
        L.append(f"- {lab}: {np.median(v):.3f} ({np.percentile(v, 5):.3f} to {np.percentile(v, 95):.3f}); n = {len(v)}")
    keys = ['k_min', 'k_tax', 'tunnel', 'p_up', 'omega_low', 's_scar', 'm_scar', 'Tbar_low', 'sigma_s', 'rho_s', 'spread', 'chi_f', 'chi_p', 'beta_gap', 'eis']
    L += ["", "## Where each result fails (constants that differ most between failing and holding draws, in sd)", ""]
    for name, f in CLAIMS:
        v = [(r, f(r)) for r in ok]; v = [(r, x) for r, x in v if x is not None]
        fl = [r for r, x in v if not x]; hd = [r for r, x in v if x]
        if len(fl) >= 3 and len(hd) >= 3:
            z = sorted(((np.mean([r[k] for r in fl]) - np.mean([r[k] for r in hd])) / (np.std([r[k] for r, _ in v]) + 1e-12), k) for k in keys)
            L.append(f"- **{name}** fails in {len(fl)}/{len(v)}: " + ", ".join(f"{k} ({s:+.2f})" for s, k in (z[:2] + z[-2:])))
if ok:
    X = np.array([0.02 * (r['stab_dW_m'] - r['stab_dW_c']) / (r['trans_dW_m'] - r['stab_dW_c']) for r in rich])
    L += ["", "## What halving low-skill schedule entropy is worth in cash (control K ≥ 1)", "",
          "Gross gain from stability (model change minus the control's change, which is the tax alone) divided by the gross gain per unit of the "
          f"equal-cost transfer, times the transfer (0.02): median {np.median(X):.4f} of mean quarterly income per quarter "
          f"(5th–95th percentile {np.percentile(X, 5):.4f} to {np.percentile(X, 95):.4f}); the program was priced at 0.0200."]
if bad:
    L += ["", f"## Unsolved: {len(bad)}", ""]
    from collections import Counter
    for e, n in Counter(r.get('error', '?')[:90] for r in bad).most_common(6):
        L.append(f"- {n} × {e}")
    if ok:
        keys = ['sigma_s', 'rho_s', 'spread', 'chi_f', 'chi_p', 'beta_gap', 'eis', 'k_tax', 'tunnel']
        L.append("- unsolved minus solved, in sd: " + ", ".join(f"{k} {(np.mean([r[k] for r in bad]) - np.mean([r[k] for r in ok])) / (np.std([r[k] for r in R.values()]) + 1e-12):+.2f}" for k in keys))
L.append(f"\nMedian seconds per solved draw: {np.median([r['seconds'] for r in ok]):.0f}." if ok else "")
open(os.path.join(OUT, 'TWO_ASSET_SWEEP_SUMMARY.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))
