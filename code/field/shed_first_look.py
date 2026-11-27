"""
shed_first_look.py -- a first DESCRIPTIVE look at public data for the Chapter 13 question: among employees,
is a schedule that varies at the EMPLOYER's discretion associated with financial fragility at equal household
income -- and does a schedule that varies at the WORKER's request (same variability, different hand on the
eraser) look the same or different?

Data: Federal Reserve Survey of Household Economics and Decisionmaking (SHED), public-use files for 2022 and 2023
(not redistributed here; pass the two CSV paths). Sample: respondents working for someone else with a stated
schedule type (question D30). Survey weights used throughout.

Outcomes (all 0/1):
  cant400     could not pay a $400 emergency expense right now (EF3_h)
  notcash400  would not cover $400 entirely with cash, savings or a card paid in full (the Fed's headline measure)
  nofund3     no rainy-day fund covering three months (EF1)
  strained    "just getting by" or "finding it difficult to get by" (B2)
  incvar      income varies month to month (I9)
  billvar     struggled to pay bills because income varied (I12; 0 if income does not vary)
Method: weighted logit on schedule type with controls (household income in 7 bands, education, age band, gender,
race/ethnicity, children, marital status, survey year; full/part-time where asked), reported as average marginal
effects in percentage points with bootstrap 95% intervals. In 2022 the survey also asked employer-varying workers
how much notice they get (D31): outcomes by notice are tabulated, raw and adjusted.

NOT CAUSAL. A cross-section cannot separate what a schedule does to a household from who ends up in such jobs;
household income is a band, not a wage; some respondents appear in both years. This is the audit's first
descriptive column, nothing more.
Usage: python shed_first_look.py public2022.csv public2023.csv
"""
import sys, os, warnings
import numpy as np, pandas as pd
import statsmodels.api as sm
warnings.filterwarnings('ignore')
OUT = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results'))
os.makedirs(OUT, exist_ok=True)
rng = np.random.default_rng(11)


def load(path, year):
    d = pd.read_csv(path, encoding='latin-1', low_memory=False)
    d['year'] = year
    return d


def prep(d):
    d = d[(d['D3A'] == 'Working for someone else') & d['D30'].notna() & (d['D30'].astype(str).str.len() > 0)].copy()
    s = d['D30'].astype(str)
    d['sched'] = np.where(s.str.startswith('Normally'), 'same', np.where(s.str.contains('request'), 'own', 'employer'))
    yes = lambda col, prefix: d[col].astype(str).str.startswith(prefix).astype(int)
    d['cant400'] = yes('EF3_h', 'I wouldn')
    cashlike = (yes('EF3_a', 'Put it') == 1) | (yes('EF3_c', 'With the money') == 1)
    other = sum(yes(c, p) for c, p in [('EF3_b', 'Put it'), ('EF3_d', 'Using'), ('EF3_e', 'By borrowing'), ('EF3_f', 'Using'), ('EF3_g', 'By selling')]) + d['cant400']
    d['notcash400'] = (~(cashlike & (other == 0))).astype(int)
    d['nofund3'] = (d['EF1'] == 'No').astype(int)
    d['strained'] = d['B2'].isin(['Just getting by', 'Finding it difficult to get by']).astype(int)
    d['incvar'] = (~d['I9'].astype(str).str.startswith('Roughly')).astype(int)
    d['billvar'] = (d['I12'] == 'Yes').astype(int)
    d['kids'] = (pd.to_numeric(d['ppkid017'], errors='coerce').fillna(0) > 0).astype(int)
    d['w'] = pd.to_numeric(d['weight'], errors='coerce')
    return d[d['w'].notna()]


CONTROLS = ['ppinc7', 'ppeducat', 'ppagecat', 'ppgender', 'race_5cat', 'ppmarit5']
OUTCOMES = ['cant400', 'notcash400', 'nofund3', 'strained', 'incvar', 'billvar']


def design(d, extra=()):
    X = pd.get_dummies(d[CONTROLS + list(extra)].astype(str), drop_first=True).astype(float)
    X['kids'] = d['kids'].values
    if d['year'].nunique() > 1:
        X['y2023'] = (d['year'] == 2023).astype(float).values
    return X


def ame(d, y, X, levels=('own', 'employer'), ref='same', var='sched'):
    """Average marginal effects (pp) of each level vs ref from a weighted logit; returns dict level -> effect."""
    Z = X.copy()
    for lv in levels:
        Z['s_' + lv] = (d[var] == lv).astype(float).values
    Z = sm.add_constant(Z, has_constant='add')
    fit = sm.GLM(d[y].values, Z.values, family=sm.families.Binomial(), freq_weights=d['w'].values).fit(maxiter=50)
    b = fit.params; cols = list(Z.columns); out = {}
    base = Z.values.copy()
    for lv in levels:
        base[:, cols.index('s_' + lv)] = 0.0
    p0 = 1 / (1 + np.exp(-(base @ b)))
    for lv in levels:
        Z1 = base.copy(); Z1[:, cols.index('s_' + lv)] = 1.0
        p1 = 1 / (1 + np.exp(-(Z1 @ b)))
        out[lv] = 100 * np.average(p1 - p0, weights=d['w'].values)
    return out


def boot(d, y, extra=(), B=300, **kw):
    X = design(d, extra); point = ame(d, y, X, **kw); draws = {k: [] for k in point}; diff = []
    n = len(d)
    for _ in range(B):
        idx = rng.integers(0, n, n); db = d.iloc[idx]
        try:
            e = ame(db, y, design(db, extra).reindex(columns=X.columns, fill_value=0.0), **kw)
        except Exception:
            continue
        for k in e: draws[k].append(e[k])
        if 'own' in e and 'employer' in e: diff.append(e['employer'] - e['own'])
    ci = {k: (np.percentile(v, 2.5), np.percentile(v, 97.5)) for k, v in draws.items()}
    dci = (np.percentile(diff, 2.5), np.percentile(diff, 97.5)) if diff else None
    return point, ci, dci


def wmean(d, col):
    return 100 * np.average(d[col], weights=d['w'])


def main(p22, p23):
    d22 = prep(load(p22, 2022)); d23 = prep(load(p23, 2023)); d = pd.concat([d22, d23], ignore_index=True)
    L = ["# SHED first look — schedule control and financial fragility among employees (descriptive; 2022 and 2023 public-use files)", "",
         f"Employees with a stated schedule type: {len(d22)} (2022) + {len(d23)} (2023) = {len(d)}. Weighted shares: "
         + ", ".join(f"{k} {100*np.average(d['sched']==k, weights=d['w']):.1f}%" for k in ['same', 'own', 'employer'])
         + ". 'same' = normally the same hours; 'own' = varies primarily at the worker's request; 'employer' = varies primarily on the employer's needs.", "",
         "## 1. Who has an employer-varying schedule (weighted share of employees, pooled)", "", "| household income | employer-varying | varies at own request | n |", "|---|---|---|---|"]
    order = ['Less than $10,000', '$10,000 to $24,999', '$25,000 to $49,999', '$50,000 to $74,999', '$75,000 to $99,999', '$100,000 to $149,999', '$150,000 or more']
    for inc in order:
        s = d[d['ppinc7'] == inc]
        L.append(f"| {inc} | {100*np.average(s['sched']=='employer', weights=s['w']):.1f}% | {100*np.average(s['sched']=='own', weights=s['w']):.1f}% | {len(s)} |")
    L += ["", "## 2. Raw outcome rates by schedule type (weighted %, pooled)", "", "| outcome | same hours | varies, own request | varies, employer's needs |", "|---|---|---|---|"]
    for y in OUTCOMES:
        L.append(f"| {y} | " + " | ".join(f"{wmean(d[d['sched']==k], y):.1f}" for k in ['same', 'own', 'employer']) + " |")
    L += ["", "## 3. Adjusted differences vs 'same hours' (average marginal effects, percentage points; bootstrap 95% intervals)", "",
          "Controls: household income band, education, age band, gender, race/ethnicity, marital status, children, year.", "",
          "| outcome | sample | own request − same | employer's needs − same | employer − own |", "|---|---|---|---|---|"]
    res = {}
    for lab, dd, extra in [('pooled', d, ()), ('2022 (+ full/part-time)', d22, ('D3B',)), ('2023', d23, ())]:
        for y in OUTCOMES:
            pt, ci, dci = boot(dd, y, extra)
            res[(lab, y)] = (pt, ci, dci)
            L.append(f"| {y} | {lab} | {pt['own']:+.1f} [{ci['own'][0]:+.1f}, {ci['own'][1]:+.1f}] | {pt['employer']:+.1f} [{ci['employer'][0]:+.1f}, {ci['employer'][1]:+.1f}] | "
                     f"{pt['employer']-pt['own']:+.1f} [{dci[0]:+.1f}, {dci[1]:+.1f}] |")
        print(f"section 3 {lab} done", flush=True)
    # notice (2022)
    e = d22[(d22['sched'] == 'employer') & d22['D31'].notna() & (d22['D31'].astype(str).str.len() > 0)].copy()
    nlev = ['One day in advance or less (including on call)', '2 to 3 days in advance', '4 to 6 days in advance', '1 to 2 weeks in advance', '3 weeks in advance or longer']
    L += ["", "## 4. Advance notice among employer-varying workers (2022 only): raw weighted outcome rates", "",
          "| notice | n | " + " | ".join(OUTCOMES) + " |", "|---|---|" + "---|" * len(OUTCOMES)]
    for nv in nlev:
        s = e[e['D31'] == nv]
        L.append(f"| {nv} | {len(s)} | " + " | ".join(f"{wmean(s, y):.1f}" for y in OUTCOMES) + " |")
    e['notice'] = np.where(e['D31'].isin(nlev[:2]), 'short', 'long')      # three days or less vs four days or more
    L += ["", "Adjusted: notice of three days or less vs four days or more, among employer-varying workers (same controls + full/part-time):", "",
          "| outcome | short − long notice (pp) |", "|---|---|"]
    for y in OUTCOMES:
        try:
            pt, ci, _ = boot(e, y, ('D3B',), levels=('short',), ref='long', var='notice')
            L.append(f"| {y} | {pt['short']:+.1f} [{ci['short'][0]:+.1f}, {ci['short'][1]:+.1f}] |")
        except Exception as ex:
            L.append(f"| {y} | not estimable ({type(ex).__name__}) |")
    L += ["", "## Reading", "",
          "Descriptive only. A cross-section cannot separate what a schedule does to a household from who ends up in such jobs; household "
          "income is a band, not a wage; some respondents appear in both years, which the intervals ignore. What the table can show is "
          "whether the fragility gap is specific to schedules the employer controls (employer − own) or common to any varying schedule."]
    open(os.path.join(OUT, 'shed_first_look.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L))


if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2])
