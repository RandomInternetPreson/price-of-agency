"""summarize_sweep.py -- sign-stability table from results_sweep/*.jsonl (stress objective #1).
Writes results_sweep/SWEEP_SUMMARY.md and figures/hank_sweep_signs.png."""
import os, sys, json, glob
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, sys.argv[1] if len(sys.argv) > 1 else 'results_sweep_fast')
if not os.path.isdir(OUT): OUT = os.path.join(HERE, 'results_sweep')
FIG = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'figures'))
rows = []
byd = {}
for fn in sorted(glob.glob(os.path.join(OUT, '*.jsonl'))):
    for line in open(fn, encoding='utf-8'):
        try:
            r = json.loads(line)
            if r['draw'] not in byd or r.get('status') == 'ok':      # a retried draw's ok record replaces its fail record
                byd[r['draw']] = r
        except Exception: pass
rows = list(byd.values())
ok = [r for r in rows if r.get('status') == 'ok']
print(f"{len(rows)} draws, {len(ok)} ok, {sum(r.get('status')=='fail' for r in rows)} failed, "
      f"{sum(r.get('status')=='beta_too_high' for r in rows)} beta too high")
TESTS = [  # name, lambda -> bool, description
    ('GE transmission: r_model > r_ctrl', lambda r: r['dr_ge'] > 0),
    ('asset demand falls at fixed prices', lambda r: r['dA_pe'] < 0),
    ('dose: half dose gives smaller dr', lambda r: 0 <= r['dr_half'] <= r['dr_ge'] + 1e-6),
    ("P-A' GE: time < money < 0 (model-control HtM_low)", lambda r: r['PA_time_ge'] < r['PA_money_ge'] < 0),
    ("P-A' GE: time beats money", lambda r: r['PA_time_ge'] < r['PA_money_ge']),
    ("P-A' PE: time beats money", lambda r: r['PA_time_pe'] < r['PA_money_pe']),
    ('P-B GE: stability beats wage on HtM', lambda r: r['PB_stab_ge'] < r['PB_wage_ge']),
    ('P-B GE: stability beats wage on welfare', lambda r: r['PB_stab_welf_ge'] > r['PB_wage_welf_ge']),
    ('P-C GE: residual > 0 after liquidity repair', lambda r: r['PC_resid_ge'] > 0),
    ('P-E: dr*/dS > 0', lambda r: r['PE_dr_dS_ge'] > 0),
    ('P-E: dA/dS < 0 at fixed prices', lambda r: r['PE_dA_dS_pe'] < 0),
    ('HtM_low higher in model (GE)', lambda r: r['dHTM_low_ge'] > 0),
]
lines = [f"# Sign-stability map — {len(ok)} successful draws over the box in sweep_signs.py", "",
         "| result | holds (all) | naive | sophisticated |", "|---|---|---|---|"]
def frac(sub, f):
    return f"{np.mean([f(r) for r in sub]):.3f} ({len(sub)})" if sub else "—"
for name, f in TESTS:
    nv = [r for r in ok if r['naive'] == 1]; so = [r for r in ok if r['naive'] == 0]
    lines.append(f"| {name} | {frac(ok, f)} | {frac(nv, f)} | {frac(so, f)} |")
# where does P-A' GE fail? simple logistic-free diagnostics: compare parameter means in holds vs fails
lines += ["", "## Where results fail (mean of each parameter, holds vs fails, naive draws)", ""]
params = ['k_min', 'k_tax', 'tunnel', 'p_up', 'omega_low', 's_scar', 'm_scar', 'Tbar_low', 'Tbar_mid_gap', 'B', 'sigma_s', 'rho_s', 'mu', 'eis']
for name, f in TESTS:
    nv = [r for r in ok if r['naive'] == 1]
    H = [r for r in nv if f(r)]; F = [r for r in nv if not f(r)]
    if not F or not H: continue
    diffs = sorted(((np.mean([r[p] for r in F]) - np.mean([r[p] for r in H])) / (np.std([r[p] for r in nv]) + 1e-12), p) for p in params)
    lines.append(f"- **{name}** fails in {len(F)}/{len(nv)} naive draws; failing draws differ most in: " +
                 ", ".join(f"{p} ({z:+.2f} sd)" for z, p in diffs[:2] + diffs[-2:]))
open(os.path.join(OUT, 'SWEEP_SUMMARY.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    nv = [r for r in ok if r['naive'] == 1]
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
    ax[0].scatter([r['k_tax'] for r in nv], [r['dr_ge'] * 400 for r in nv], s=8, c=[r['tunnel'] for r in nv]); ax[0].set_xlabel('k_tax'); ax[0].set_ylabel('Δr* annual pp'); ax[0].set_title('GE transmission (color = tunnel)')
    ax[1].scatter([r['PA_money_ge'] for r in nv], [r['PA_time_ge'] for r in nv], s=8); lim = ax[1].get_xlim(); ax[1].plot(lim, lim, 'k--', lw=0.7); ax[1].set_xlabel('money arm'); ax[1].set_ylabel('time arm'); ax[1].set_title("P-A' GE: below the line = time wins")
    ax[2].scatter([r['PB_wage_ge'] for r in nv], [r['PB_stab_ge'] for r in nv], s=8); lim = ax[2].get_xlim(); ax[2].plot(lim, lim, 'k--', lw=0.7); ax[2].set_xlabel('wage arm'); ax[2].set_ylabel('stability arm'); ax[2].set_title('P-B GE: below the line = stability wins')
    plt.tight_layout(); os.makedirs(FIG, exist_ok=True); plt.savefig(os.path.join(FIG, 'hank_sweep_signs.png'), dpi=130)
except Exception as ex:
    print('figure skipped:', ex)
