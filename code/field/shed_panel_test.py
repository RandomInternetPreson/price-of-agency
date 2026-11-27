"""
shed_panel_test.py -- the PREREGISTERED within-person test (H4) and industry control (H5) of
docs/SHED_PREREG_v0.2.md, on the SHED public-use files 2019-2023.

H4: the same respondent (shedid) observed as an employee with a stated schedule type in two ADJACENT waves.
    Weighted least squares of the within-person change in each outcome on the change in E (schedule varies on the
    employer's needs) and in O (varies at the worker's request), with wave-pair dummies; weights = later wave's
    cross-section weight; intervals by bootstrap over PERSONS.
H5: the v0.1 pooled cross-section, all five waves, with and without industry dummies (ind1, harmonized).
Loading, sample definition, outcomes and plumbing are those of shed_first_look.py / shed_oos_test.py (imported).

Usage: python shed_panel_test.py public2019.csv public2020.csv public2021.csv public2022.csv public2023.csv [B4] [B5]
NOT CAUSAL: first differences remove fixed traits, not shocks; see the preregistration's last section.
"""
import sys, os, warnings
import numpy as np, pandas as pd
import shed_first_look as F
import shed_oos_test as T
warnings.filterwarnings('ignore')
rng = np.random.default_rng(404)
CONF = ['strained', 'billvar']; SEC = ['cant400', 'nofund3']
IND = [('Professional', 'professional'), ('Health', 'health'), ('Educat', 'education'), ('Retail', 'retail'), ('Factory', 'manufacturing'),
       ('Manufactur', 'manufacturing'), ('Financ', 'finance'), ('Transport', 'transport'), ('Delivery', 'transport'), ('Public Admin', 'public admin'),
       ('Administrative', 'admin support'), ('Accommodation', 'food and lodging'), ('Information', 'information'), ('Community', 'nonprofit'),
       ('Construction', 'construction'), ('Repairs', 'repairs'), ('Arts', 'arts'), ('Utilities', 'utilities'), ('Wholesale', 'wholesale'),
       ('Agricultur', 'agriculture'), ('Farming', 'agriculture'), ('Real Estate', 'real estate'), ('Armed', 'armed forces'), ('Personal', 'personal services'),
       ('Child', 'child care'), ('Mining', 'mining')]


def industry(lab):
    for pre, name in IND:
        if str(lab).startswith(pre):
            return name
    return 'other or not coded'


def f1(pt, c):
    return f"{pt:+.1f} [{c[0]:+.1f}, {c[1]:+.1f}]"


def pairs(waves):
    out = []
    yrs = sorted(waves)
    for a, b in zip(yrs[:-1], yrs[1:]):
        A = waves[a].set_index('shedid'); Bw = waves[b].set_index('shedid')
        ids = A.index.intersection(Bw.index)
        A = A.loc[ids]; Bw = Bw.loc[ids]
        p = pd.DataFrame({'id': ids, 'pair': f'{a}-{b}', 'w': Bw['w'].values,
                          'E0': (A['sched'] == 'employer').astype(int).values, 'E1': (Bw['sched'] == 'employer').astype(int).values,
                          'O0': (A['sched'] == 'own').astype(int).values, 'O1': (Bw['sched'] == 'own').astype(int).values,
                          'dinc': Bw['ppinc7'].map(T.INC7.index).values - A['ppinc7'].map(T.INC7.index).values})
        for y in CONF + SEC:
            p['d_' + y] = Bw[y].values - A[y].values
            p['ok_' + y] = (A['ok_' + y].values & Bw['ok_' + y].values)
        p['dE'] = p['E1'] - p['E0']; p['dO'] = p['O1'] - p['O0']
        out.append(p)
    return pd.concat(out, ignore_index=True)


def wls(p, y, extra=(), weighted=True):
    q = p[p['ok_' + y]]
    X = pd.get_dummies(q['pair']).astype(float)
    X.insert(0, 'dO', q['dO'].values.astype(float)); X.insert(0, 'dE', q['dE'].values.astype(float))
    for c in extra: X[c] = q[c].values.astype(float)
    w = q['w'].values if weighted else np.ones(len(q))
    Xw = X.values * np.sqrt(w)[:, None]; yw = q['d_' + y].values * np.sqrt(w)
    b = np.linalg.lstsq(Xw, yw, rcond=None)[0]
    return 100 * b[0], 100 * b[1]


def cells(p, y):
    q = p[p['ok_' + y]]; m = {}
    for e0 in (0, 1):
        for e1 in (0, 1):
            s = q[(q['E0'] == e0) & (q['E1'] == e1)]
            m[(e0, e1)] = (100 * np.average(s['d_' + y], weights=s['w']) if len(s) else np.nan, len(s))
    return m


def person_boot(p, fn, B):
    ids = p['id'].unique(); grp = {k: v.values for k, v in p.groupby('id').groups.items()}; draws = []
    for _ in range(B):
        take = rng.choice(ids, len(ids)); idx = np.concatenate([grp[i] for i in take])
        draws.append(fn(p.loc[idx]))
    return np.array(draws, dtype=float)


def ci(v):
    return (np.nanpercentile(v, 2.5), np.nanpercentile(v, 97.5))


def main(paths, B4=1000, B5=200):
    waves = {}
    for yr, pth in zip((2019, 2020, 2021, 2022, 2023), paths):
        waves[yr], _, _ = T.load_wave(pth, yr)
    P = pairs(waves)
    L = ["# SHED within-person test (H4) and industry control (H5) — preregistration v0.2", "",
         "Script: `code/field/shed_panel_test.py`. Descriptive, not causal: first differences remove fixed traits of a person, not the shocks "
         "that arrive with a change of schedule.", "",
         f"## Sample: {len(P)} adjacent-wave pairs from {P['id'].nunique()} persons employed with a stated schedule type in both waves", "",
         "| wave pair | pairs | stayed out (0→0) | moved in (0→1) | moved out (1→0) | stayed in (1→1) | own-request: moved in / out |", "|---|---|---|---|---|---|---|"]
    for pr, s in list(P.groupby('pair')) + [('all', P)]:
        c = lambda a, b: int(((s['E0'] == a) & (s['E1'] == b)).sum())
        L.append(f"| {pr} | {len(s)} | {c(0,0)} | {c(0,1)} | {c(1,0)} | {c(1,1)} | {int((s['dO']==1).sum())} / {int((s['dO']==-1).sum())} |")

    # ---- H4a / H4b
    L += ["", "## H4a, H4b — change in outcome on change in schedule type (percentage points; person-bootstrap 95% intervals)", "",
          "| outcome | ΔE (employer's needs) | ΔO (own request) | **ΔE − ΔO** | ΔE, adding Δ income band | ΔE, unweighted |", "|---|---|---|---|---|---|"]
    res = {}
    for y in CONF + SEC:
        bE, bO = wls(P, y)
        d = person_boot(P, lambda q: wls(q, y), B4)
        bEi, _ = wls(P, y, extra=('dinc',)); di = person_boot(P, lambda q: wls(q, y, extra=('dinc',))[0], B4 // 2)
        bEu, _ = wls(P, y, weighted=False); du = person_boot(P, lambda q: wls(q, y, weighted=False)[0], B4 // 2)
        res[y] = (bE, ci(d[:, 0]), bO, ci(d[:, 1]), bE - bO, ci(d[:, 0] - d[:, 1]))
        L.append(f"| {y}{'' if y in CONF else ' (secondary)'} | {f1(bE, ci(d[:,0]))} | {f1(bO, ci(d[:,1]))} | {f1(bE-bO, ci(d[:,0]-d[:,1]))} | {f1(bEi, ci(di))} | {f1(bEu, ci(du))} |")
        print('H4', y, 'done', flush=True)
    va = "FAILS" if any(res[y][0] <= 0 for y in CONF) else "HOLDS"
    vb = "FAILS" if any(res[y][4] <= 0 for y in CONF) else "HOLDS"
    ex = lambda k: [y for y in CONF if res[y][k][0] > 0]
    L += ["", f"**H4a verdict: {va}.** ΔE coefficient: " + ", ".join(f"{y} {f1(res[y][0], res[y][1])}" for y in CONF)
          + f"; interval excludes zero on: {', '.join(ex(1)) or 'neither'}.",
          f"**H4b verdict: {vb}.** ΔE − ΔO: " + ", ".join(f"{y} {f1(res[y][4], res[y][5])}" for y in CONF)
          + f"; interval excludes zero on: {', '.join(ex(5)) or 'neither'}."]

    # ---- by pair
    L += ["", "ΔE coefficient by wave pair (weighted, pp):", "", "| outcome | " + " | ".join(sorted(P['pair'].unique())) + " |", "|---|" + "---|" * P['pair'].nunique()]
    for y in CONF + SEC:
        row = f"| {y} |"
        for pr in sorted(P['pair'].unique()):
            s = P[P['pair'] == pr]; b = wls(s, y)[0]; d = person_boot(s, lambda q: wls(q, y)[0], B4 // 4)
            row += f" {f1(b, ci(d))} |"
        L.append(row)

    # ---- H4c
    L += ["", "## H4c — both directions (weighted mean within-person change, pp)", "",
          "| outcome | stayed out (0→0) | moved in (0→1) | **in − stayed out** | stayed in (1→1) | moved out (1→0) | **out − stayed in** |", "|---|---|---|---|---|---|---|"]
    wrong = {'in': 0, 'out': 0}
    for y in CONF + SEC:
        m = cells(P, y)
        fin = lambda q: (lambda c: c[(0, 1)][0] - c[(0, 0)][0])(cells(q, y)); fout = lambda q: (lambda c: c[(1, 0)][0] - c[(1, 1)][0])(cells(q, y))
        din = person_boot(P, fin, B4 // 2); dout = person_boot(P, fout, B4 // 2)
        vin = m[(0, 1)][0] - m[(0, 0)][0]; vout = m[(1, 0)][0] - m[(1, 1)][0]
        if y in CONF:
            wrong['in'] += vin <= 0; wrong['out'] += vout >= 0
        L.append(f"| {y}{'' if y in CONF else ' (secondary)'} | {m[(0,0)][0]:+.1f} | {m[(0,1)][0]:+.1f} | {f1(vin, ci(din))} | {m[(1,1)][0]:+.1f} | {m[(1,0)][0]:+.1f} | {f1(vout, ci(dout))} |")
    vc = "FAILS" if (wrong['in'] == 2 or wrong['out'] == 2) else ("HOLDS" if (wrong['in'] == 0 and wrong['out'] == 0) else "HOLDS IN PART")
    L += ["", f"**H4c verdict: {vc}.** Wrong-signed confirmatory outcomes: moving in {wrong['in']} of 2, moving out {wrong['out']} of 2 "
          "(committed: fails if either direction is wrong-signed on both)."]
    open(os.path.join(F.OUT, 'shed_panel_test.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L), flush=True)

    # ---- H5
    d = pd.concat(waves.values(), ignore_index=True)
    d['industry'] = d['ind1'].map(industry)
    L += ["", "## H5 — industry held fixed (pooled cross-section, all five waves; robustness, not out-of-sample)", "",
          f"{len(d)} employee-wave observations from {d['shedid'].nunique()} persons; {d['industry'].nunique()} industry groups; intervals by bootstrap over persons. "
          "Largest groups: " + ", ".join(f"{k} {v}" for k, v in d['industry'].value_counts().head(6).items()) + f"; other or not coded {int((d['industry']=='other or not coded').sum())}.", "",
          "| outcome | employer − own, no industry | employer − own, with industry | share kept | employer − same, with industry | own − same, with industry |", "|---|---|---|---|---|---|"]
    grp = {k: v.values for k, v in d.groupby('shedid').groups.items()}; ids = np.array(list(grp))
    v5 = []
    for y in CONF + SEC:
        dd = d[d['ok_' + y]]
        def est(q, extra):
            X = T.design(q, extra); a = F.ame(q, y, X); return a['employer'] - a['own'], a['employer'], a['own']
        p0 = est(dd, ()); p1 = est(dd, ('industry',)); D0, D1 = [], []
        for _ in range(B5):
            take = rng.choice(ids, len(ids)); q = d.loc[np.concatenate([grp[i] for i in take])]; q = q[q['ok_' + y]]
            try:
                e0 = est(q, ()); e1 = est(q, ('industry',))
            except Exception:
                continue
            if np.all(np.isfinite(e0 + e1)): D0.append(e0); D1.append(e1)
        D0 = np.array(D0); D1 = np.array(D1); keep = p1[0] / p0[0] if p0[0] != 0 else np.nan
        L.append(f"| {y}{'' if y in CONF else ' (secondary)'} | {f1(p0[0], ci(D0[:,0]))} | {f1(p1[0], ci(D1[:,0]))} | {100*keep:.0f}% | {f1(p1[1], ci(D1[:,1]))} | {f1(p1[2], ci(D1[:,2]))} |")
        if y in CONF: v5.append((p1[0], keep))
        print('H5', y, 'done', flush=True)
    vv = "FAILS" if any(a <= 0 for a, _ in v5) else ("HOLDS" if all(k >= 0.5 for _, k in v5) else "HOLDS IN PART")
    L += ["", f"**H5 verdict: {vv}.** With industry held fixed, employer − own is " + ", ".join(f"{y} {a:+.1f} pp ({100*k:.0f}% kept)" for y, (a, k) in zip(CONF, v5)) + "."]
    L += ["", "## Reading", "",
          "H4 asks whether the same person reports more strain in the wave in which the employer holds the schedule than in the wave in which "
          "the employer does not; H5 asks whether the cross-sectional gap is an industry composition effect. Neither is an experiment. A change "
          "of schedule type usually arrives with a change of job; a strained household may take the job on offer; self-classification errors "
          "manufacture false switchers and pull first differences toward zero. The audit design (Chapter 13's box, items 6–9) is still owed."]
    open(os.path.join(F.OUT, 'shed_panel_test.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L[-12:]), flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a[:5], B4=int(a[5]) if len(a) > 5 else 1000, B5=int(a[6]) if len(a) > 6 else 200)
