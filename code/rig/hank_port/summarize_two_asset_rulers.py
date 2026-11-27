"""summarize_two_asset_rulers.py -- the programs of the two-asset host on three rulers, across the drawn economies.
Reads results_two_asset_rulers/shard_*.jsonl (or argv[1]); writes TWO_ASSET_RULERS_SUMMARY.md there.
Survival: famine of Chapter 11's town manned from the economy's three skill groups (shares 1/4, 1/2, 1/4), reader accuracy
p(b) = 1/4 + (p_top - 1/4) b**gamma -- the join's one supposition, varied."""
import os, sys, json, glob
from math import factorial
import numpy as np
HERE = os.path.dirname(os.path.abspath(__file__))
OUT = sys.argv[1] if len(sys.argv) > 1 else os.path.join(HERE, 'results_two_asset_rulers')
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
            if r.get('status') == 'ok' and 'm_bw_groups' in r: R[r['draw']] = r
        except Exception:
            pass
ok = list(R.values()); rich = [r for r in ok if r['c_K'] >= 1.0]
ARMS = [('time', 'time transfer'), ('money', 'cash, same cost as time'), ('stab', 'stability'), ('trans', 'cash, same cost as stability')]
sh = lambda v: f"{np.mean(v):.3f} ({int(np.sum(v))}/{len(v)})"
L = [f"# Two-asset host on three rulers — {len(rich)} economies whose control holds illiquid wealth ({len(ok)} solved in all)", "",
     "Each program's change from the taxed economy's own baseline (fixed returns). Survival at p_top = 0.9, γ = 1.", "",
     "| program | CONSUMPTION: low-skill value rises | median | BANDWIDTH: low-skill rises | median | SURVIVAL: famine falls | median (points) |", "|---|---|---|---|---|---|---|"]
for r in rich:
    r['_f'] = {'base': famine(r['m_bw_groups'])}
    for a, _ in ARMS: r['_f'][a] = famine(r[a + '_bw_groups_m'])
for a, lab in ARMS:
    dc = np.array([r[a + '_dW_m'] for r in rich]); db = np.array([r[a + '_bw_groups_m'][0] - r['m_bw_groups'][0] for r in rich]); df = np.array([r['_f'][a] - r['_f']['base'] for r in rich])
    L.append(f"| {lab} | {sh(dc > 0)} | {np.median(dc):+.3f} | {sh(db > 0.005)} | {np.median(db):+.3f} | {sh(df < -0.001)} | {100*np.median(df):+.2f} |")
L += ["", "| head to head, equal cost | on CONSUMPTION | on BANDWIDTH (low-skill) | on SURVIVAL |", "|---|---|---|---|"]
for a, b, lab in [('stab', 'trans', 'stability beats cash'), ('time', 'money', 'time beats cash')]:
    L.append(f"| {lab} | {sh(np.array([r[a+'_dW_m'] > r[b+'_dW_m'] for r in rich]))} | {sh(np.array([r[a+'_bw_groups_m'][0] > r[b+'_bw_groups_m'][0] for r in rich]))} | {sh(np.array([r['_f'][a] < r['_f'][b] for r in rich]))} |")
L += ["", "| p_top | γ | stability beats cash on survival | time beats cash on survival |", "|---|---|---|---|"]
for p_top in (0.8, 0.9, 1.0):
    for g in (0.5, 1.0, 2.0):
        F = [{a: famine(r[a + '_bw_groups_m'], p_top, g) for a, _ in ARMS} for r in rich]
        L.append(f"| {p_top} | {g} | {sh(np.array([f['stab'] < f['trans'] for f in F]))} | {sh(np.array([f['time'] < f['money'] for f in F]))} |")
L.append(f"\nCash raises low-skill bandwidth by more than 0.01 in {sh(np.array([r['trans_bw_groups_m'][0] - r['m_bw_groups'][0] > 0.01 for r in rich]))} (small cash) and "
         f"{sh(np.array([r['money_bw_groups_m'][0] - r['m_bw_groups'][0] > 0.01 for r in rich]))} (large cash) of economies. Time transfers that stop short of the gate are included.")
open(os.path.join(OUT, 'TWO_ASSET_RULERS_SUMMARY.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
print('\n'.join(L))
