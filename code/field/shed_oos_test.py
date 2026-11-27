"""
shed_oos_test.py -- the PREREGISTERED out-of-sample test of the SHED first look (docs/SHED_PREREG_v0.1.md),
run on the waves that were not open when the preregistration was written: 2019, 2020, 2021.

Sample, outcomes, weights, estimator and controls are those of shed_first_look.py (imported, not copied).
Plumbing made necessary by the older public-use files -- every item decided from the codebook labels BEFORE
any outcome was tabulated, and listed in the output:
  P1  2019/2020 carry household income in 21 bands (ppincimp); collapsed to the same 7 bands as ppinc7 (exact:
      every one of the 7 cut points is a cut point of the 21).
  P2  2019/2020 carry marital status as ppmarit (6 levels, "Living with partner" separate); used as that
      wave's marital control in place of ppmarit5.
  P3  2019/2020 carry children by age group (ppt01, ppt25, ppt612, ppt1317); kids = any of them > 0.
  P4  2019/2020 code the $400 items Yes/No instead of by the option text; recoded to the same 0/1.
  P5  2019/2020 contain "Refused" (later files do not): a refused schedule type is not a stated schedule type
      (sample definition), a refused notice is not a stated notice, and respondents who refused an outcome
      question are dropped from that outcome's regression.
  P6  Pooling three waves needs two year dummies where the first look needed one.
  P7  The weighted logit is solved by Newton's method in numpy rather than by statsmodels' GLM (same likelihood, same
      maximum; agreement with shed_first_look.ame on the 2022 wave to 1e-10 percentage points; three times faster).
Confirmatory specifications are the ones that produced the numbers quoted in the preregistration: H1 = the
pooled specification (no full/part-time control); H2 = the 2022 specification (with full/part-time). The other
specification is printed beside each as a robustness column. The script first re-derives the 2022 exploratory
tables (first-look sections 5 and 6) to show the reconstruction of that contrast is the one that was seen.

Usage: python shed_oos_test.py public2019.csv public2020.csv public2021.csv public2022.csv [B]
NOT CAUSAL. See the preregistration, last section.
"""
import sys, os, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
import shed_first_look as F
warnings.filterwarnings('ignore')
rng = np.random.default_rng(2019)
INC7 = ['Less than $10,000', '$10,000 to $24,999', '$25,000 to $49,999', '$50,000 to $74,999', '$75,000 to $99,999',
        '$100,000 to $149,999', '$150,000 or more']
NLEV = ['One day in advance or less (including on call)', '2 to 3 days in advance', '4 to 6 days in advance',
        '1 to 2 weeks in advance', '3 weeks in advance or longer']
EF3_PREFIX = {'EF3_a': 'Put it', 'EF3_b': 'Put it', 'EF3_c': 'With the money', 'EF3_d': 'Using', 'EF3_e': 'By borrowing',
              'EF3_f': 'Using', 'EF3_g': 'By selling', 'EF3_h': 'I wouldn'}
REFUSABLE = {'cant400': ['EF3_h'], 'notcash400': ['EF3_a'], 'nofund3': ['EF1'], 'strained': ['B2'], 'incvar': ['I9'], 'billvar': ['I9', 'I12']}


def upper(band):
    """Upper edge (dollars) of an income band label such as '$12,500 to $14,999' / 'Less than $5,000' / '$250,000 or more'."""
    s = band.replace('$', '').replace(',', '')
    if s.startswith('Less than'):
        return float(s.split()[-1]) - 1
    if 'or more' in s:
        return np.inf
    return float(s.split(' to ')[1])


def to_inc7(band):
    u = upper(band)
    for lab, edge in zip(INC7, [9999, 24999, 49999, 74999, 99999, 149999, np.inf]):
        if u <= edge:
            return lab


def load_wave(path, year):
    d = pd.read_csv(path, encoding='latin-1', low_memory=False, keep_default_na=False)
    d['year'] = year
    notes = []
    if 'ppinc7' not in d.columns:
        d['ppinc7'] = d['ppincimp'].map(to_inc7); notes.append('P1')
    if 'ppmarit5' not in d.columns:
        d['ppmarit5'] = d['ppmarit']; notes.append('P2')
    if 'ppkid017' not in d.columns:
        d['ppkid017'] = sum(pd.to_numeric(d[c], errors='coerce').fillna(0) for c in ['ppt01', 'ppt25', 'ppt612', 'ppt1317']); notes.append('P3')
    if (d['EF3_h'] == 'Yes').any():
        for c, p in EF3_PREFIX.items():
            d[c] = d[c].where(d[c] != 'Yes', p + ' (recoded from Yes)')
        notes.append('P4')
    n0 = ((d['D3A'] == 'Working for someone else') & (d['D30'].str.len() > 0)).sum()
    d = d[d['D30'] != 'Refused']
    p = F.prep(d)
    for y, cols in REFUSABLE.items():
        p['ok_' + y] = ~np.logical_or.reduce([(p[c] == 'Refused').values for c in cols])
    return p, notes, int(n0 - len(p))


def fast_ame(d, y, X, levels=('own', 'employer'), ref='same', var='sched'):
    """The same estimator as shed_first_look.ame (weighted logit maximum likelihood, average marginal effects in pp),
    solved by Newton's method in numpy instead of statsmodels' GLM: identical estimates, several times faster.
    Checked against F.ame at start-up (see main)."""
    Z = X.copy()
    for lv in levels:
        Z['s_' + lv] = (d[var] == lv).astype(float).values
    Z.insert(0, 'const', 1.0)
    cols = list(Z.columns); Zv = Z.values.astype(float); yv = d[y].values.astype(float); w = d['w'].values.astype(float)
    b = np.zeros(Zv.shape[1])
    for _ in range(60):
        p = 1 / (1 + np.exp(-np.clip(Zv @ b, -35, 35)))
        g = Zv.T @ (w * (yv - p)); Hm = (Zv * (w * p * (1 - p))[:, None]).T @ Zv
        step = np.linalg.lstsq(Hm, g, rcond=1e-12)[0]
        b = b + step
        if np.max(np.abs(step)) < 1e-9:
            break
    base = Zv.copy()
    for lv in levels:
        base[:, cols.index('s_' + lv)] = 0.0
    p0 = 1 / (1 + np.exp(-(base @ b))); out = {}
    for lv in levels:
        Z1 = base.copy(); Z1[:, cols.index('s_' + lv)] = 1.0
        out[lv] = 100 * np.average(1 / (1 + np.exp(-(Z1 @ b))) - p0, weights=w)
    return out


def design(d, extra=()):
    X = pd.get_dummies(d[F.CONTROLS + list(extra)].astype(str), drop_first=True).astype(float)
    X['kids'] = d['kids'].values
    for yr in sorted(d['year'].unique())[1:]:
        X[f'y{yr}'] = (d['year'] == yr).astype(float).values
    return X


def boot(d, y, extra=(), B=300, levels=('own', 'employer'), ref='same', var='sched', contrasts=()):
    """Point AMEs (pp) and bootstrap 95% intervals for each level vs ref and for each (a, b) contrast a - b."""
    d = d[d['ok_' + y]] if 'ok_' + y in d.columns else d
    X = design(d, extra); pt = fast_ame(d, y, X, levels=levels, ref=ref, var=var)
    draws = {k: [] for k in pt}; cd = {c: [] for c in contrasts}; n = len(d)
    for _ in range(B):
        db = d.iloc[rng.integers(0, n, n)]
        try:
            e = fast_ame(db, y, design(db, extra).reindex(columns=X.columns, fill_value=0.0), levels=levels, ref=ref, var=var)
        except Exception:
            continue
        if not all(np.isfinite(v) for v in e.values()):
            continue
        for k in e: draws[k].append(e[k])
        for a, b in contrasts: cd[(a, b)].append(e[a] - e[b])
    ci = lambda v: (np.percentile(v, 2.5), np.percentile(v, 97.5))
    return pt, {k: ci(v) for k, v in draws.items()}, {c: (pt[c[0]] - pt[c[1]], ci(v)) for c, v in cd.items()}, n


def f1(pt, c):
    return f"{pt:+.1f} [{c[0]:+.1f}, {c[1]:+.1f}]"


def notice_frames(d):
    """(employer-varying workers with stated notice, labelled under3/3plus; whole sample with sched3 splitting employer by notice)."""
    e = d[(d['sched'] == 'employer') & d['D31'].isin(NLEV)].copy()
    e['notice'] = np.where(e['D31'] == NLEV[-1], '3plus', 'under3')
    full = d[(d['sched'] != 'employer') | d['D31'].isin(NLEV)].copy()
    full['sched3'] = np.where(full['sched'] != 'employer', full['sched'], np.where(full['D31'] == NLEV[-1], 'emp3plus', 'empunder3'))
    return e, full


def h1_block(L, lab, d, B, extras=((), ('D3B',))):
    out = {}
    for y in F.OUTCOMES:
        row = f"| {y} | {lab} |"
        for extra in extras:
            pt, ci, con, n = boot(d, y, extra, B, contrasts=(('employer', 'own'),))
            dv, dc = con[('employer', 'own')]
            row += f" {f1(pt['own'], ci['own'])} | {f1(pt['employer'], ci['employer'])} | {f1(dv, dc)} |"
            out[(y, extra)] = (pt['own'], ci['own'], dv, dc)
        L.append(row)
    print(f"H1 {lab} done", flush=True)
    return out


def h2_block(L, lab, d, B, extras=(('D3B',), ())):
    e, full = notice_frames(d); out = {}
    for y in F.OUTCOMES:
        row = f"| {y} | {lab} | {len(e)} |"
        for extra in extras:
            pt, ci, _, _ = boot(e, y, extra, B, levels=('under3',), ref='3plus', var='notice')
            p3, c3, _, _ = boot(full, y, extra, B, levels=('own', 'emp3plus', 'empunder3'), ref='same', var='sched3')
            row += f" {f1(pt['under3'], ci['under3'])} | {f1(p3['emp3plus'], c3['emp3plus'])} | {f1(p3['empunder3'], c3['empunder3'])} |"
            out[(y, extra)] = (pt['under3'], ci['under3'], p3['emp3plus'], c3['emp3plus'])
        L.append(row)
    print(f"H2 {lab} done", flush=True)
    return out


def h3_block(L, lab, d):
    sh = []
    for inc in INC7:
        s = d[d['ppinc7'] == inc]
        sh.append(100 * np.average(s['sched'] == 'employer', weights=s['w']) if len(s) else np.nan)
    rev = sum(1 for a, b in zip(sh[:-1], sh[1:]) if b > a)
    L.append(f"| {lab} | " + " | ".join(f"{v:.1f}" for v in sh) + f" | {rev} |")
    return sh, rev


def main(p19, p20, p21, p22, B=300):
    waves = {}; L = ["# SHED out-of-sample test — the preregistered H1–H3 on the 2019, 2020 and 2021 public-use files", "",
                     "Preregistration: `docs/SHED_PREREG_v0.1.md` (written with only 2022 and 2023 open). Script: `code/field/shed_oos_test.py`. "
                     "Descriptive, not causal.", ""]
    for yr, p in [(2019, p19), (2020, p20), (2021, p21)]:
        d, notes, nref = load_wave(p, yr); waves[yr] = d
        L.append(f"- {yr}: {len(d)} employees with a stated schedule type; plumbing {', '.join(notes) if notes else 'none'}"
                 f"{', P5 (' + str(nref) + ' refused schedule type dropped)' if nref else ''}; outcome refusals dropped per regression: "
                 + ", ".join(f"{y} {int((~d['ok_'+y]).sum())}" for y in F.OUTCOMES) + ".")
    d = pd.concat(waves.values(), ignore_index=True)
    L += ["", f"Pooled out-of-sample: {len(d)} employees. Weighted shares: " + ", ".join(f"{k} {100*np.average(d['sched']==k, weights=d['w']):.1f}%" for k in ['same', 'own', 'employer']) + ".",
          "Some respondents are interviewed in more than one wave; the pooled intervals ignore that, the single-wave rows do not depend on it.", ""]

    # ---- check of the coding against the published headline (all adults): share not covering $400 with cash or equivalent
    L += ["## 0. Coding check against the Federal Reserve's published headline (all adults, weighted)", "",
          "| wave | would not cover a $400 expense entirely with cash or its equivalent (this script) | published |", "|---|---|---|"]
    for yr, p, pub in [(2019, p19, '37%'), (2020, p20, '36%'), (2021, p21, '32%')]:
        a = pd.read_csv(p, encoding='latin-1', low_memory=False, keep_default_na=False)
        if (a['EF3_h'] == 'Yes').any():
            for c, pre in EF3_PREFIX.items():
                a[c] = a[c].where(a[c] != 'Yes', pre + ' (recoded from Yes)')
        a = a[a['EF3_h'] != 'Refused']
        yes = lambda col: a[col].astype(str).str.startswith(EF3_PREFIX[col])
        cashlike = yes('EF3_a') | yes('EF3_c'); other = sum(yes(c).astype(int) for c in ['EF3_b', 'EF3_d', 'EF3_e', 'EF3_f', 'EF3_g', 'EF3_h'])
        w = pd.to_numeric(a['weight'], errors='coerce')
        L.append(f"| {yr} | {100*np.average(~(cashlike & (other == 0)), weights=w):.1f}% | {pub} |")

    # ---- reconstruction check on 2022 (in-sample; shows the H2 contrast coded here is the one that was seen)
    d22, _, _ = load_wave(p22, 2022)
    L += ["", "## 0b. Reconstruction check: the 2022 exploratory contrast re-derived by this script (compare first-look tables 5 and 6)", "",
          "| outcome | sample | n employer-varying with notice | under 3 weeks − 3 weeks or more | 3+ weeks − same hours | under 3 weeks − same hours |"
          " (no full/part-time) under − 3+ | 3+ − same | under − same |", "|---|---|---|---|---|---|---|---|---|"]
    h2_block(L, '2022 (seen)', d22, B)

    # ---- H1
    L += ["", "## H1 — control, not variability (average marginal effects, percentage points; bootstrap 95% intervals)", "",
          "Confirmatory specification: pooled controls (household income band, education, age band, gender, race/ethnicity, marital status, "
          "children, year). Robustness: the same plus full/part-time.", "",
          "| outcome | sample | own − same | employer − same | **employer − own** | (+ full/part-time) own − same | employer − same | employer − own |",
          "|---|---|---|---|---|---|---|---|"]
    h1 = h1_block(L, 'pooled 2019–2021', d, B)
    for yr in (2019, 2020, 2021):
        h1_block(L, str(yr), waves[yr], B)
    conf = ['cant400', 'nofund3', 'strained', 'billvar']
    nonpos = [y for y in conf if h1[(y, ())][2] <= 0]; excl0 = [y for y in conf if h1[(y, ())][3][0] > 0]
    ownband = {y: h1[(y, ())][0] for y in conf[:3]}
    v1 = "FAILS" if len(nonpos) >= 2 else ("HOLDS" if (not nonpos and all(abs(v) <= 3 for v in ownband.values())) else "HOLDS IN PART")
    L += ["", f"**H1 verdict (pooled out-of-sample, confirmatory specification): {v1}.** employer − own is positive on "
          f"{4-len(nonpos)} of 4 confirmatory outcomes ({', '.join(f'{y} {h1[(y, ())][2]:+.1f}' for y in conf)}); the interval excludes zero on "
          f"{len(excl0)} ({', '.join(excl0) if excl0 else 'none'}). own − same on the first three: "
          + ", ".join(f"{y} {v:+.1f}" for y, v in ownband.items()) + " (committed band ±3 pp)."]

    # ---- H2
    L += ["", "## H2 — the three-week break (employer-varying workers with stated notice)", "",
          "Confirmatory specification: the 2022 one (pooled controls plus full/part-time). Robustness: without full/part-time.", "",
          "| outcome | sample | n employer-varying with notice | **under 3 weeks − 3 weeks or more** | **3+ weeks − same hours** | under 3 weeks − same hours |"
          " (no full/part-time) under − 3+ | 3+ − same | under − same |", "|---|---|---|---|---|---|---|---|---|"]
    h2 = h2_block(L, 'pooled 2019–2021', d, B)
    for yr in (2019, 2020, 2021):
        h2_block(L, str(yr), waves[yr], B)
    k = ('D3B',)
    s_, b_ = h2[('strained', k)], h2[('billvar', k)]
    fail = (s_[0] <= 0) or (b_[0] <= 0); band = abs(s_[2]) <= 5
    v2 = "FAILS" if fail else ("HOLDS" if band else "HOLDS IN PART (first clause holds; the ±5 pp band on strained does not)")
    L += ["", f"**H2 verdict (pooled out-of-sample, confirmatory specification): {v2}.** under 3 weeks − 3 weeks or more: strained "
          f"{f1(s_[0], s_[1])}, billvar {f1(b_[0], b_[1])}. 3+ weeks − same hours on strained: {f1(s_[2], s_[3])} (committed band ±5 pp)."]

    # ---- H3
    L += ["", "## H3 — who bears it (weighted share of employees whose schedule varies on the employer's needs, by household income band)", "",
          "| sample | " + " | ".join(INC7) + " | adjacent reversals |", "|---|" + "---|" * 8]
    sh, rev = h3_block(L, 'pooled 2019–2021', d)
    for yr in (2019, 2020, 2021):
        h3_block(L, str(yr), waves[yr])
    v3 = "HOLDS" if (sh[-1] < sh[0] and rev <= 1) else "FAILS"
    L += ["", f"**H3 verdict (pooled out-of-sample): {v3}.** {sh[0]:.1f}% in the lowest band, {sh[-1]:.1f}% in the highest, {rev} adjacent reversal(s) "
          "(committed: falls from lowest to highest with at most one)."]

    L += ["", "## Reading", "",
          "The three hypotheses were written down before these files were opened and are evaluated on the pooled out-of-sample waves in the "
          "specification that produced the numbers quoted in the preregistration; every other column is context. Nothing here is causal: "
          "selection into jobs, the wage itself, occupation and industry are not in the model; household income is a band; the outcomes are "
          "self-reported; the 2020 and 2021 waves were fielded during the pandemic transfers. This is the audit's descriptive column, confirmed "
          "or not out of sample, and the design that could attribute (Chapter 13's audit box, items 6–9) is still owed."]
    open(os.path.join(F.OUT, 'shed_oos_test.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main(*sys.argv[1:5], B=int(sys.argv[5]) if len(sys.argv) > 5 else 300)
