"""summarize_rulers.py -- three-ruler table across the drawn economies of the one-asset host.
Reads results_sweep_rulers/shard_*.jsonl (or argv[1]); writes RULERS_SUMMARY.md there.
Rulers per program (time; cash of the same cost; stability; cash of the same cost), general equilibrium, naive household:
  CONSUMPTION  change in low-skill lifetime value in the taxed economy (and aggregate)
  BANDWIDTH    change in low-skill bandwidth
  SURVIVAL     change in the famine probability of Chapter 11's town manned from the economy's three skill groups,
               reader accuracy p(b) = 1/4 + (p_top - 1/4) b**gamma  (the join's one supposition; varied)."""
import os, sys, json, glob
from math import factorial
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'results_sweep_rulers')
SH = (0.25, 0.5, 0.25); N, M, DAYS = 9, 5, 90
CREWS = [(k0, k1, N - k0 - k1, factorial(N) / (factorial(k0) * factorial(k1) * factorial(N - k0 - k1)) * SH[0] ** k0 * SH[1] ** k1 * SH[2] ** (N - k0 - k1))
         for k0 in range(N + 1) for k1 in range(N + 1 - k0)]


def run3(p):
    v = np.zeros(4); v[0] = 1
    for _ in range(DAYS):
        n = np.zeros(4); n[0] = (1 - p) * v[:3].sum(); n[1] = p * v[0]; n[2] = p * v[1]; n[3] = v[3] + p * v[2]; v = n
    return v[3]


def famine(bw, p_top=0.9, gamma=1.0):
    acc = [0.25 + (p_top - 0.25) * max(b, 0.0) ** gamma for b in bw]; f = 0.0
    for k0, k1, k2, w in CREWS:
        d = np.array([1.0])
        for p in [acc[0]] * k0 + [acc[1]] * k1 + [acc[2]] * k2: d = np.convolve(d, [1 - p, p])
        f += w * run3(d[:M].sum())
    return f


R = {}
for fn in sorted(glob.glob(os.path.join(OUT, 'shard_*.jsonl'))):
    for line in open(fn, encoding='utf-8'):
        try:
            r = json.loads(line)
            if r.get('status') == 'ok' and 'L_base_welf_m' in r: R[r['draw']] = r
        except Exception:
            pass
ok = list(R.values()); nv = [r for r in ok if r.get('naive', 1) == 1]
ARMS = [('time', 'time transfer'), ('money', 'cash, same cost as time'), ('stab', 'stability'), ('wage', 'cash, same cost as stability')]
bw = lambda r, a: (r[f'L_{a}_bw_low'], r[f'L_{a}_bw_mid'], r[f'L_{a}_bw_high'])
for r in nv:
    r['_f'] = {a: famine(bw(r, a)) for a in ['base'] + [a for a, _ in ARMS]}
L = [f"# Three rulers across the drawn economies — {len(nv)} naive economies ({len(ok)} solved in all)", "",
     "Each program's change from the taxed economy's own baseline. Survival: famine of Chapter 11's town manned from the economy (p_top = 0.9, γ = 1).", "",
     "| program | CONSUMPTION: low-skill value rises | median change | aggregate value rises | BANDWIDTH: low-skill rises | median change | SURVIVAL: famine falls | median change (points) |",
     "|---|---|---|---|---|---|---|---|"]
sh = lambda v: f"{np.mean(v):.3f} ({int(np.sum(v))}/{len(v)})"
for a, lab in ARMS:
    dc = np.array([r[f'L_{a}_welf_m'] - r['L_base_welf_m'] for r in nv]); dC = np.array([r[f'L_{a}_WELF_m'] - r['L_base_WELF_m'] for r in nv])
    db = np.array([r[f'L_{a}_bw_low'] - r['L_base_bw_low'] for r in nv]); df = np.array([r['_f'][a] - r['_f']['base'] for r in nv])
    L.append(f"| {lab} | {sh(dc > 0)} | {np.median(dc):+.3f} | {sh(dC > 0)} | {sh(db > 0.005)} | {np.median(db):+.3f} | {sh(df < -0.001)} | {100*np.median(df):+.2f} |")
L += ["", "## Head to head, equal cost", "", "| comparison | on CONSUMPTION (low-skill value) | on BANDWIDTH (low-skill) | on SURVIVAL (famine) |", "|---|---|---|---|"]
for a, b, lab in [('stab', 'wage', 'stability beats cash'), ('time', 'money', 'time beats cash')]:
    L.append(f"| {lab} | {sh(np.array([r[f'L_{a}_welf_m'] > r[f'L_{b}_welf_m'] for r in nv]))} | {sh(np.array([r[f'L_{a}_bw_low'] > r[f'L_{b}_bw_low'] for r in nv]))} | "
             f"{sh(np.array([r['_f'][a] < r['_f'][b] for r in nv]))} |")
L += ["", "## The supposition varied: share of economies in which stability / time beats equal-cost cash on survival", "",
      "| p_top | γ | stability beats cash | time beats cash | median baseline famine |", "|---|---|---|---|---|"]
for p_top in (0.8, 0.9, 1.0):
    for g in (0.5, 1.0, 2.0):
        F = [{a: famine(bw(r, a), p_top, g) for a in ['base', 'time', 'money', 'stab', 'wage']} for r in nv]
        L.append(f"| {p_top} | {g} | {sh(np.array([f['stab'] < f['wage'] for f in F]))} | {sh(np.array([f['time'] < f['money'] for f in F]))} | {100*np.median([f['base'] for f in F]):.1f}% |")
X = np.array([0.02 * ((r['L_stab_welf_m'] - r['L_base_welf_m']) - (r['L_stab_welf_c'] - r['L_base_welf_c'])) /
              ((r['L_wage_welf_m'] - r['L_base_welf_m']) - (r['L_stab_welf_c'] - r['L_base_welf_c'])) for r in nv])
L += ["", f"Cash-equivalent of halving low-skill schedule entropy on the consumption ruler: median {np.median(X):.4f} of mean quarterly income "
      f"(5th–95th percentile {np.percentile(X, 5):.4f} to {np.percentile(X, 95):.4f}); the program was priced at 0.0200.",
      f"Cash raises low-skill bandwidth by more than 0.01 in {sh(np.array([r['L_wage_bw_low'] - r['L_base_bw_low'] > 0.01 for r in nv]))} (small cash) and "
      f"{sh(np.array([r['L_money_bw_low'] - r['L_base_bw_low'] > 0.01 for r in nv]))} (large cash) of economies."]
open(os.path.join(OUT, 'RULERS_SUMMARY.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))
