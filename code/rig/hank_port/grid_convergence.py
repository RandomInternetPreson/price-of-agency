"""grid_convergence.py -- numerical robustness: the headline GE numbers at three grid resolutions."""
import os, sys, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hank_ge as H
from run_hank_v01 import group_stats
RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results_exact'))
lines = ["# Grid convergence of the headline GE numbers (2026-11-09)", "", "| nA | nref | β (control) | r* model | ΔHTM_low (GE) | ΔA (PE) | BW model | seconds |", "|---|---|---|---|---|---|---|---|"]
for nA, nref in [(120, 4), (160, 6), (200, 8)]:
    t0 = time.time()
    cal = dict(H.CAL, nA=nA, nref=nref)
    ssc = H.model_ss.solve_steady_state(dict(cal, **H.CONTROL), unknowns={'beta': 0.9815, 'vphi': 0.88}, targets={'asset_mkt': 0.0, 'wnkpc_res': 0.0}, solver='broyden_custom', ttol=1e-6)
    c = group_stats(H.model.steady_state(ssc)); m = group_stats(H.ge_ss(cal, ssc['beta'], ssc['vphi'])); p = group_stats(H.pe_ss(cal, ssc['beta'], ssc['vphi']))
    lines.append(f"| {nA} | {nref} | {ssc['beta']:.5f} | {m['r']:.4f} | {m['htm_low']-c['htm_low']:+.4f} | {p['A']-c['A']:+.3f} | {m['BW']:.3f} | {time.time()-t0:.0f} |")
    print(lines[-1], flush=True)
open(os.path.join(RES, 'hank_grid_convergence.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
