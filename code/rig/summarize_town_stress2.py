"""summarize_town_stress2.py -- fishers who consult yesterday's sea; a master who misdirects when it pays."""
import os, csv
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__)); OUT = os.path.join(HERE, 'results_town2')
rows = [{k: float(v) for k, v in r.items()} for r in csv.DictReader(open(os.path.join(OUT, 'town_stress2.csv'), encoding='utf-8'))]
F = lambda r: np.array([r[f'famine_k{k}'] for k in range(10)])
def get(**kw):
    return [r for r in rows if all(abs(r[k] - v) < 1e-9 for k, v in kw.items())]
lines = [f"# Town stress 2 — {len(rows)} configurations", "",
         "Columns: famine with all reading (k=0), at the best dose (k*), with a bloc (k=9).", ""]
lines += ["## Fishers who consult yesterday's sea (honest master, fresh reader errors)", "", "| q | sea memory ρ_G | memory used? | all read | best dose | bloc |", "|---|---|---|---|---|---|"]
for q in sorted({r['q'] for r in rows}):
    for rg in sorted({r['rho_G'] for r in rows}):
        for mem in (0, 1):
            for r in get(q=q, rho_G=rg, mem=mem, Yc=0, rho_err=0.0):
                f = F(r); lines.append(f"| {q} | {rg} | {'yes' if mem else 'no'} | {f[0]:.3f} | k={int(np.argmin(f))}, {f.min():.3f} | {f[9]:.3f} |")
lines += ["", "## A master who misdirects once his following exceeds Yc boats (no memory, fresh errors, ρ_G = 0)", "", "| q | Yc | famine by dose k = 0..9 | best dose |", "|---|---|---|---|"]
for q in sorted({r['q'] for r in rows}):
    for yc in sorted({r['Yc'] for r in rows}):
        for r in get(q=q, rho_G=0.0, mem=0, Yc=yc, rho_err=0.0):
            f = F(r); lines.append(f"| {q} | {'honest' if yc == 0 else int(yc)} | " + " ".join(f"{x:.2f}" for x in f) + f" | k={int(np.argmin(f))} |")
lines += ["", "## Both, with readers' bad weeks (ρ_err = 0.5)", "", "| q | ρ_G | memory | Yc | all read | best dose | bloc |", "|---|---|---|---|---|---|---|"]
for r in sorted(get(rho_err=0.5), key=lambda r: (r['q'], r['rho_G'], r['mem'], r['Yc'])):
    f = F(r); lines.append(f"| {r['q']} | {r['rho_G']} | {'yes' if r['mem'] else 'no'} | {'honest' if r['Yc']==0 else int(r['Yc'])} | {f[0]:.3f} | k={int(np.argmin(f))}, {f.min():.3f} | {f[9]:.3f} |")
open(os.path.join(OUT, 'TOWN_STRESS2_SUMMARY.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\n'.join(lines[:60]))
