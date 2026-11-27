"""
run_two_asset.py -- stress objective #9: the hand-to-mouth results in a two-asset host (liquid + illiquid).
Model minus control at fixed returns (r_a, r_k), plus one general-equilibrium margin: the liquid rate that
clears the liquid-asset market at the control's beta. Writes results_exact/hank_two_asset_RESULTS.md.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import bw_two_asset as T
RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results_exact'))
hh = T.TwoAssetBW(); t0 = time.time()
GRID = dict(nA=50, nK=12)
B_LIQ = 1.04            # liquid assets = 26% of annual income (a quarter's income, roughly), the usual two-asset target
Vc = {}


def S(cal, key=None):
    c = dict(GRID); c.update(cal)
    s = hh.solve(c, V0=Vc.get(key))
    if key: Vc[key] = s['_V']
    return s


# 1. calibrate the control's beta to the liquid target (secant)
b0, b1 = 0.970, 0.978
f0 = S(dict(T.CONTROL, beta=b0), 'c')['A'] - B_LIQ; f1 = S(dict(T.CONTROL, beta=b1), 'c')['A'] - B_LIQ
for _ in range(12):
    b2 = min(0.9845, max(0.90, b1 - f1 * (b1 - b0) / (f1 - f0)))
    f2 = S(dict(T.CONTROL, beta=b2), 'c')['A'] - B_LIQ
    b0, f0, b1, f1 = b1, f1, b2, f2
    if abs(f2) < 2e-4: break
beta = b1
print(f"beta = {beta:.5f} (A - target = {f1:+.1e})  [{time.time()-t0:.0f}s]", flush=True)
C = dict(T.CONTROL, beta=beta); M = dict(beta=beta)
c = S(C, 'c'); m = S(M, 'm')
L = ["# Two-asset host (liquid + illiquid): the hand-to-mouth results, stress objective #9 (2026-11-09)", "",
     f"Liquid return {T.DEFAULTS['r_a']:.3f}/qtr, illiquid {T.DEFAULTS['r_k']:.3f}/qtr, fixed fee {T.DEFAULTS['chi_f']} and proportional fee "
     f"{T.DEFAULTS['chi_p']} on moving the illiquid account; control's β = {beta:.4f} calibrated to liquid assets = {B_LIQ}. "
     "Hand-to-mouth (HtM) = liquid savings within 0.15 of the limit; wealthy HtM = HtM holding illiquid wealth above 0.5. "
     "Fixed returns unless marked. Naive forecast. Bandwidth constants as in the one-asset host.", "",
     "## 1. Levels", "", "| economy | liquid A | illiquid K | HtM | wealthy HtM | poor HtM | HtM low-skill | BW | mass at top of a / k grid |", "|---|---|---|---|---|---|---|---|---|"]
row = lambda lab, s: f"| {lab} | {s['A']:.3f} | {s['K']:.3f} | {s['HTM']:.3f} | {s['WHTM']:.3f} | {s['PHTM']:.3f} | {s['htm_low']:.3f} | {s['BW']:.3f} | {s['top_a']:.4f} / {s['top_k']:.4f} |"
L += [row('control', c), row('model', m)]
for lab, cal in [('noise face only', dict(M, tunnel=0.0)), ('horizon face only', dict(M, k_tax=0.0)), ('half dose', dict(M, k_tax=0.025, tunnel=0.00765)), ('1.5× dose', dict(M, k_tax=0.075, tunnel=0.02295))]:
    L.append(row(lab, S(cal, 'm')))
print('\n'.join(L[-8:]), flush=True)
# 2. GE margin: the liquid rate that clears the liquid market in the model
lo, hi = T.DEFAULTS['r_a'], min(T.DEFAULTS['r_k'] - 5e-4, 1 / beta - 1 - 5e-4)
flo = m['A'] - B_LIQ; fhi = S(dict(M, r_a=hi), 'm')['A'] - B_LIQ
if flo * fhi < 0:
    for _ in range(12):
        mid = 0.5 * (lo + hi); fm = S(dict(M, r_a=mid), 'm')['A'] - B_LIQ
        if flo * fm <= 0: hi, fhi = mid, fm
        else: lo, flo = mid, fm
    r_star = 0.5 * (lo + hi); g = S(dict(M, r_a=r_star), 'm')
    L += ["", f"## 2. The liquid rate that clears the liquid market at the control's β", "",
          f"Control: r_a = {T.DEFAULTS['r_a']:.4f}. Model: r_a* = {r_star:.4f} per quarter ({(r_star-T.DEFAULTS['r_a'])*400:+.2f} points a year). At that rate:", "", L[8], L[9], row('model at r_a*', g)]
else:
    L += ["", "## 2. Liquid-market clearing", "", f"No crossing below the illiquid return: liquid demand at r_a = {hi:.4f} is {fhi+B_LIQ:.3f} against {B_LIQ}."]
print('\n'.join(L[-6:]), flush=True)
# 3. policies (fixed returns), model minus control
e_low = hh.setup(dict(T.DEFAULTS, **GRID))['e_grid'][0]; w0 = T.DEFAULTS['w']
dT = 0.25; cost = w0 * e_low * dT; pi_low = 0.25
om = T.DEFAULTS['omega']; om_stab = [om[0] / 2, om[1], om[2]]; sc = 0.02
arms = {'liquidity repaired (limit 0 → 0.5)': dict(a_borrow=0.5),
        'time transfer (floor across the gate)': dict(dT_low=dT, Tax=T.DEFAULTS['Tax'] + cost * pi_low),
        'money transfer, equal cost': dict(Tr_low=cost, Tax=T.DEFAULTS['Tax'] + cost * pi_low),
        'stability (low-skill entropy halved)': dict(omega=om_stab, Tax=T.DEFAULTS['Tax'] + sc * pi_low),
        'transfer, equal cost to stability': dict(Tr_low=sc, Tax=T.DEFAULTS['Tax'] + sc * pi_low),
        'no drain at all': dict(omega=[0, 0, 0], s_scar=0.0, dT_low=1.0)}
L += ["", "## 3. Policies at fixed returns: low-skill group, model and control", "",
      "| policy | HtM_low control | HtM_low model | residual (model − control) | Δ poor-HtM share model | Δ illiquid K_low model | ΔWELF_low model − control |", "|---|---|---|---|---|---|---|"]
L.append(f"| none | {c['htm_low']:.3f} | {m['htm_low']:.3f} | {m['htm_low']-c['htm_low']:+.3f} | — | — | — |")
for lab, kw in arms.items():
    pc = S(dict(C, **kw)); pm = S(dict(M, **kw))
    L.append(f"| {lab} | {pc['htm_low']:.3f} | {pm['htm_low']:.3f} | {pm['htm_low']-pc['htm_low']:+.3f} | {pm['PHTM']-m['PHTM']:+.3f} | {pm['k_low']-m['k_low']:+.3f} | "
             f"{(pm['welf_low']-m['welf_low'])-(pc['welf_low']-c['welf_low']):+.3f} |")
    print(L[-1], f"[{time.time()-t0:.0f}s]", flush=True)
L.append(f"\nRuntime {time.time()-t0:.0f}s.")
open(os.path.join(RES, 'hank_two_asset_RESULTS.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
