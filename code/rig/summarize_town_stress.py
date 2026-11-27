"""summarize_town_stress.py -- the town under stress: does Theorem 13's structure survive? Reads results_town/*.csv."""
import os, glob, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'results_town')
FIG = os.path.normpath(os.path.join(HERE, '..', '..', 'figures'))
rows = []
for fn in glob.glob(os.path.join(OUT, '*.csv')):
    for r in csv.DictReader(open(fn, encoding='utf-8')):
        rows.append({k: float(v) for k, v in r.items()})
keys = ['q', 'p', 'rho_G', 'rho_err', 'c', 'rho_h', 'lie']
F = lambda r: np.array([r[f'famine_k{k}'] for k in range(10)])
lines = [f"# Town stress (T13) — {len(rows)} configurations", "",
         "Columns: famine at k = 0 (all read), at the best dose k*, at k = 9 (bloc); 'independence beats bloc' = famine(k=0) < famine(k=9); "
         "'some following helps' = min over k ≥ 1 below famine(k=0); k* = argmin.", ""]
def table(title, groups):
    out = [f"## {title}", "", "| group | n | indep. beats bloc | some following helps | k* = 1 | k* ≥ 5 | median famine k=0 | k=9 |", "|---|---|---|---|---|---|---|---|"]
    for name, sub in groups:
        if not sub: continue
        f0 = np.array([F(r)[0] for r in sub]); f9 = np.array([F(r)[9] for r in sub])
        ks = np.array([int(np.argmin(F(r))) for r in sub]); best = np.array([F(r)[1:].min() for r in sub])
        out.append(f"| {name} | {len(sub)} | {np.mean(f0 < f9):.2f} | {np.mean(best < f0):.2f} | {np.mean(ks == 1):.2f} | {np.mean(ks >= 5):.2f} | {np.median(f0):.3f} | {np.median(f9):.3f} |")
    return out + [""]
lines += table("By master accuracy q (all other stresses pooled)", [(f"q = {q}", [r for r in rows if r['q'] == q]) for q in sorted({r['q'] for r in rows})])
for key, label in [('rho_G', 'sea memory ρ_G'), ('rho_err', 'reader error persistence ρ_err'), ('c', 'shared blindness c'), ('rho_h', "master's slump persistence ρ_h"), ('lie', 'master misdirection rate')]:
    lines += table(f"By {label} (q = 0.8 only)", [(f"{label} = {v}", [r for r in rows if r['q'] == 0.8 and r[key] == v]) for v in sorted({r[key] for r in rows})])
# worst cases for the headline claim
bad = sorted([r for r in rows if F(r)[0] >= F(r)[9]], key=lambda r: F(r)[0] - F(r)[9], reverse=True)[:10]
lines += ["## Configurations where the bloc beats independence (worst ten)", "", "| " + " | ".join(keys) + " | famine k=0 | k=9 |", "|" + "---|" * (len(keys) + 2)]
for r in bad:
    lines.append("| " + " | ".join(f"{r[k]}" for k in keys) + f" | {F(r)[0]:.3f} | {F(r)[9]:.3f} |")
open(os.path.join(OUT, 'TOWN_STRESS_SUMMARY.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    for q in sorted({r['q'] for r in rows}):
        sub = [r for r in rows if r['q'] == q and r['rho_G'] == 0 and r['rho_err'] == 0 and r['c'] == 0 and r['rho_h'] == 0 and r['lie'] == 0]
        if sub: ax[0].plot(range(10), F(sub[0]), 'o-', label=f'q = {q}')
    ax[0].set_yscale('log'); ax[0].set_xlabel('followers k'); ax[0].set_ylabel('famine probability'); ax[0].set_title('clean town (T13)'); ax[0].legend(fontsize=8)
    for key, ls in [('rho_err', '-'), ('c', '--'), ('lie', ':')]:
        vals = sorted({r[key] for r in rows})
        ys = [np.mean([F(r)[0] < F(r)[9] for r in rows if r['q'] == 0.8 and r[key] == v]) for v in vals]
        ax[1].plot(vals, ys, 'o' + ls, label=key)
    ax[1].set_ylim(0, 1.05); ax[1].set_xlabel('stress parameter value'); ax[1].set_ylabel('P(independence beats bloc), q = 0.8'); ax[1].legend(fontsize=8)
    plt.tight_layout(); os.makedirs(FIG, exist_ok=True); plt.savefig(os.path.join(FIG, 'town_stress_T13.png'), dpi=130)
except Exception as ex:
    print('figure skipped:', ex)
