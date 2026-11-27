"""
shed_pay_test.py -- the PREREGISTERED test H6 of docs/SHED_PREREG_v0.3.md: did the pay rise?

If instability were priced in, households whose schedule the employer varies would be paid more than they otherwise
would be. H6a: the same person, year to year (change in household-income band on the change in schedule type).
H6b: across persons at equal education, age, gender, race and ethnicity, marital status, children and year.
H6c: H6b among full-time workers only (2021-2023).
Loading, sample and plumbing are those of shed_oos_test.py / shed_panel_test.py (imported).

Usage: python shed_pay_test.py public2019.csv public2020.csv public2021.csv public2022.csv public2023.csv [B6a] [B6b]
"""
import sys, os, warnings
import numpy as np, pandas as pd
import shed_first_look as F
import shed_oos_test as T
import shed_panel_test as P4
warnings.filterwarnings('ignore')
rng = np.random.default_rng(606)
CTRL = [c for c in F.CONTROLS if c != 'ppinc7']


def f2(pt, c):
    return f"{pt:+.3f} [{c[0]:+.3f}, {c[1]:+.3f}]"


def ci(v):
    return (np.nanpercentile(v, 2.5), np.nanpercentile(v, 97.5))


def reading(pt, c):
    if c[0] > 0: return "PAY ROSE"
    if c[1] < 0: return "PAY FELL"
    return "NO RAISE DISTINGUISHABLE"


def fd(p):
    X = pd.get_dummies(p['pair']).astype(float)
    X.insert(0, 'dO', p['dO'].values.astype(float)); X.insert(0, 'dE', p['dE'].values.astype(float))
    w = p['w'].values; b = np.linalg.lstsq(X.values * np.sqrt(w)[:, None], p['dinc'].values * np.sqrt(w), rcond=None)[0]
    return b[0], b[1]


def xdesign(d):
    X = pd.get_dummies(d[CTRL].astype(str), drop_first=True).astype(float)
    X['kids'] = d['kids'].values
    for yr in sorted(d['year'].unique())[1:]:
        X[f'y{yr}'] = (d['year'] == yr).astype(float).values
    return X


def xs(d, cols=None):
    X = xdesign(d)
    if cols is not None: X = X.reindex(columns=cols, fill_value=0.0)
    Z = X.copy(); Z.insert(0, 'O', (d['sched'] == 'own').astype(float).values); Z.insert(0, 'E', (d['sched'] == 'employer').astype(float).values)
    Z.insert(0, 'const', 1.0); w = d['w'].values
    b = np.linalg.lstsq(Z.values * np.sqrt(w)[:, None], d['band'].values * np.sqrt(w), rcond=None)[0]
    return b[1], b[1] - b[2], X.columns


def xs_boot(d, B):
    pt = xs(d); grp = {k: v.values for k, v in d.groupby('shedid').groups.items()}; ids = np.array(list(grp)); D = []
    for _ in range(B):
        q = d.loc[np.concatenate([grp[i] for i in rng.choice(ids, len(ids))])]
        e = xs(q, pt[2]); D.append(e[:2])
    D = np.array(D); return pt[0], ci(D[:, 0]), pt[1], ci(D[:, 1])


def main(paths, B6a=1000, B6b=300):
    waves = {}
    for yr, pth in zip((2019, 2020, 2021, 2022, 2023), paths):
        waves[yr], _, _ = T.load_wave(pth, yr)
    L = ["# SHED: did the pay rise? (H6) — preregistration v0.3", "",
         "Script: `code/field/shed_pay_test.py`. Household income in seven bands, indexed 0–6 (under $10,000; $10,000–24,999; $25,000–49,999; "
         "$50,000–74,999; $75,000–99,999; $100,000–149,999; $150,000 or more). One band is one unit.", ""]
    # ---- H6a
    Pp = P4.pairs(waves); Pp = Pp[np.isfinite(Pp['dinc'])]
    bE, bO = fd(Pp); grp = {k: v.values for k, v in Pp.groupby('id').groups.items()}; ids = Pp['id'].unique(); D = []
    for _ in range(B6a):
        q = Pp.loc[np.concatenate([grp[i] for i in rng.choice(ids, len(ids))])]; D.append(fd(q))
    D = np.array(D); cE = ci(D[:, 0]); cO = ci(D[:, 1]); cD = ci(D[:, 0] - D[:, 1])
    L += [f"## H6a — the same person, year to year ({len(Pp)} pairs, {Pp['id'].nunique()} persons)", "",
          "| | change in household-income band |", "|---|---|",
          f"| hours pass into the employer's hands (ΔE) | {f2(bE, cE)} |", f"| hours pass to the worker's own request (ΔO) | {f2(bO, cO)} |", f"| ΔE − ΔO | {f2(bE - bO, cD)} |", "",
          f"**H6a reading: {reading(bE, cE)}.** Largest raise the interval allows: {max(cE[1], 0):.3f} of a band.", ""]
    m = {}
    for e0 in (0, 1):
        for e1 in (0, 1):
            s = Pp[(Pp['E0'] == e0) & (Pp['E1'] == e1)]; m[(e0, e1)] = (np.average(s['dinc'], weights=s['w']), len(s))
    L += ["Weighted mean change in band: stayed out " + f"{m[(0,0)][0]:+.3f} (n={m[(0,0)][1]}), moved in {m[(0,1)][0]:+.3f} (n={m[(0,1)][1]}), "
          f"moved out {m[(1,0)][0]:+.3f} (n={m[(1,0)][1]}), stayed in {m[(1,1)][0]:+.3f} (n={m[(1,1)][1]}).", ""]
    print('\n'.join(L), flush=True)
    # ---- H6b
    d = pd.concat(waves.values(), ignore_index=True); d['band'] = d['ppinc7'].map(T.INC7.index); d = d[d['band'].notna()].reset_index(drop=True)
    r = xs_boot(d, B6b)
    d['hi'] = (d['band'] >= 3).astype(int); X = xdesign(d); a = T.fast_ame(d, 'hi', X)
    A = []
    grp = {k: v.values for k, v in d.groupby('shedid').groups.items()}; ids = np.array(list(grp))
    for _ in range(B6b):
        q = d.loc[np.concatenate([grp[i] for i in rng.choice(ids, len(ids))])]
        try:
            e = T.fast_ame(q, 'hi', xdesign(q).reindex(columns=X.columns, fill_value=0.0))
        except Exception:
            continue
        if np.isfinite(e['employer']) and np.isfinite(e['own']): A.append((e['employer'], e['employer'] - e['own']))
    A = np.array(A)
    wm = lambda s: np.average(s['band'], weights=s['w'])
    L += [f"## H6b — across persons, at equal education, age, gender, race and ethnicity, marital status, children and year ({len(d)} employee-waves, {d['shedid'].nunique()} persons)", "",
          "| | employer-varied − fixed hours | employer-varied − own-request |", "|---|---|---|",
          f"| household-income band (0–6) | {f2(r[0], r[1])} | {f2(r[2], r[3])} |",
          f"| household income $50,000 or more (percentage points) | {a['employer']:+.1f} [{ci(A[:,0])[0]:+.1f}, {ci(A[:,0])[1]:+.1f}] | {a['employer']-a['own']:+.1f} [{ci(A[:,1])[0]:+.1f}, {ci(A[:,1])[1]:+.1f}] |", "",
          f"**H6b reading: {reading(r[0], r[1])}.** Unadjusted weighted mean band: fixed hours {wm(d[d['sched']=='same']):.2f}, own-request {wm(d[d['sched']=='own']):.2f}, employer-varied {wm(d[d['sched']=='employer']):.2f}.", ""]
    print('\n'.join(L[-8:]), flush=True)
    # ---- H6c
    ft = d[(d['year'] >= 2021) & (d['ppemploy'] == 'Working full-time')].reset_index(drop=True)
    r3 = xs_boot(ft, B6b)
    L += [f"## H6c — full-time workers only, 2021–2023 ({len(ft)} employee-waves; secondary)", "",
          "| | employer-varied − fixed hours | employer-varied − own-request |", "|---|---|---|",
          f"| household-income band (0–6) | {f2(r3[0], r3[1])} | {f2(r3[2], r3[3])} |", "",
          f"Reading: {reading(r3[0], r3[1])}. Share of employer-varied employees working full-time, 2021–2023: "
          f"{100*np.average(d[(d['year']>=2021)&(d['sched']=='employer')]['ppemploy']=='Working full-time', weights=d[(d['year']>=2021)&(d['sched']=='employer')]['w']):.0f}%; of fixed-hours employees: "
          f"{100*np.average(d[(d['year']>=2021)&(d['sched']=='same')]['ppemploy']=='Working full-time', weights=d[(d['year']>=2021)&(d['sched']=='same')]['w']):.0f}%.", "",
          "## What this measures", "",
          "Household income is a band, not the respondent's wage; a second earner and hours are in it (H6c removes the hours for three waves). "
          "A compensating differential large enough to matter to the household would move it across band edges at a visible rate; "
          "the intervals above say how large a raise the files leave room for."]
    open(os.path.join(F.OUT, 'shed_pay_test.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L[-9:]), flush=True)


if __name__ == '__main__':
    a = sys.argv[1:]
    main(a[:5], B6a=int(a[5]) if len(a) > 5 else 1000, B6b=int(a[6]) if len(a) > 6 else 300)
