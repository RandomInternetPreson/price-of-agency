"""summarize_living_town_skill.py -- the acting -> reading conjecture: where is the point of no return?"""
import os, glob, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'results_living2')
FIG = os.path.normpath(os.path.join(HERE, '..', '..', 'figures'))
rows = []
for fn in glob.glob(os.path.join(OUT, '*.csv')):
    for r in csv.DictReader(open(fn, encoding='utf-8')):
        rows.append({k: float(v) for k, v in r.items()})
lines = [f"# Living town with skill decay — {len(rows)} configurations", "",
         "Skill decays toward chance at rate λ on days a fisher follows the hub and recovers at rate μ on days he acts on his own reading. "
         "Start: everyone follows the hub (broadcast town). 'converted' = hub fraction below 1/2 at the end.", ""]
lams = sorted({r['lam'] for r in rows}); mus = sorted({r['mu'] for r in rows})
for q in sorted({r['q'] for r in rows}):
    for Y in sorted({r['Y'] for r in rows}):
        lines += [f"## q = {q}, yield Y = {Y} (crowding penalty strength: lower Y = stronger)", "",
                  "| λ \\ μ | " + " | ".join(f"μ = {m}" for m in mus) + " |", "|---|" + "---|" * len(mus)]
        for lam in lams:
            cells = []
            for m in mus:
                sub = [r for r in rows if r['q'] == q and r['Y'] == Y and r['lam'] == lam and r['mu'] == m and r['p0'] == 0.7]
                cells.append(f"hub {sub[0]['hub_frac_end']:.2f}, skill {sub[0]['skill_end']:.2f}, maj {sub[0]['maj_end']:.2f}" if sub else "—")
            lines.append(f"| λ = {lam} | " + " | ".join(cells) + " |")
        lines.append("")
# point of no return: smallest lam at which the town fails to convert (hub_frac_end >= 0.5) for each (mu, q, Y), p0 = 0.7
lines += ["## Point of no return: smallest λ at which the broadcast town stays a broadcast town (p0 = 0.7)", "", "| q | Y | μ | λ* |", "|---|---|---|---|"]
for q in sorted({r['q'] for r in rows}):
    for Y in sorted({r['Y'] for r in rows}):
        for m in mus:
            sub = sorted([r for r in rows if r['q'] == q and r['Y'] == Y and r['mu'] == m and r['p0'] == 0.7], key=lambda r: r['lam'])
            fail = [r['lam'] for r in sub if r['hub_frac_end'] >= 0.5]
            lines.append(f"| {q} | {Y} | {m} | {min(fail) if fail else 'none in grid'} |")
lines += ["", "## Starting with half the skill already gone (p0 = 0.5): does the town ever recover?", "", "| q | Y | μ | λ | hub_end | skill_end |", "|---|---|---|---|---|---|"]
for r in sorted([r for r in rows if r['p0'] == 0.5 and r['lam'] in (0.0, 0.01, 0.05)], key=lambda r: (r['q'], r['Y'], r['mu'], r['lam'])):
    lines.append(f"| {r['q']} | {r['Y']} | {r['mu']} | {r['lam']} | {r['hub_frac_end']:.2f} | {r['skill_end']:.2f} |")
open(os.path.join(OUT, 'LIVING_SKILL_SUMMARY.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines))
try:
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(10, 3.8))
    for m in mus:
        sub = sorted([r for r in rows if r['q'] == 0.8 and r['Y'] == 1.0 and r['mu'] == m and r['p0'] == 0.7], key=lambda r: r['lam'])
        ax[0].plot([r['lam'] for r in sub], [r['hub_frac_end'] for r in sub], 'o-', label=f'μ = {m}')
        ax[1].plot([r['lam'] for r in sub], [r['skill_end'] for r in sub], 'o-', label=f'μ = {m}')
    ax[0].axhline(0.5, c='gray', ls='--', lw=0.7); ax[0].set_xscale('symlog', linthresh=0.002); ax[0].set_xlabel('decay λ'); ax[0].set_ylabel('hub fraction, long run'); ax[0].set_title('does the town de-herd? (q=0.8, Y=12)'); ax[0].legend(fontsize=8)
    ax[1].set_xscale('symlog', linthresh=0.002); ax[1].set_xlabel('decay λ'); ax[1].set_ylabel('mean reading skill, long run'); ax[1].set_title('what is left to read with')
    plt.tight_layout(); os.makedirs(FIG, exist_ok=True); plt.savefig(os.path.join(FIG, 'living_town_skill.png'), dpi=130)
except Exception as ex:
    print('figure skipped:', ex)
