"""v02_control_nonlinear.py -- the control economy's own nonlinear path in the own-hours host, to separate the
gate's contribution from the lumpy hours choice that both economies share. Appends to results_exact/hank_v02_irf_RESULTS.md."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hank_ge_labor as HL
RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results_exact'))
T = 150; t0 = time.time()
ssc = HL.control_ss()
out = ['Y', 'HOURS', 'BELOW', 'BW', 'HTM']
G = HL.model.solve_jacobian(ssc, unknowns=HL.UNKNOWNS, targets=HL.TARGETS, inputs=['rstar'], outputs=out, T=T)
lines = ["", "## Control economy, same shocks (nonlinear vs linear) — added 2026-11-09 evening", ""]
for sz in [-0.01, -0.03]:
    dz = sz * 0.8 ** np.arange(T); t1 = time.time()
    try:
        nl = HL.model.solve_impulse_nonlinear(ssc, unknowns=HL.UNKNOWNS, targets=HL.TARGETS, inputs={'rstar': dz}, outputs=out, verbose=False)
        lin = {o: G[o]['rstar'] @ dz for o in out}
        lines.append(f"- control {sz*1e4:+.0f} bp: peak Δhours {nl['HOURS'].max():+.4f}; ΔBELOW peak nonlinear {nl['BELOW'].max():+.4f} vs linear {lin['BELOW'].max():+.4f}; "
                     f"cum ΔY nonlinear {nl['Y'].sum():+.4f} vs linear {lin['Y'].sum():+.4f} (ratio {nl['Y'].sum()/lin['Y'].sum():.2f}) [{time.time()-t1:.0f}s]")
    except Exception as ex:
        lines.append(f"- control {sz*1e4:+.0f} bp: nonlinear solve failed ({type(ex).__name__}: {str(ex)[:80]})")
    print(lines[-1], flush=True)
open(os.path.join(RES, 'hank_v02_irf_RESULTS.md'), 'a', encoding='utf-8').write('\n'.join(lines) + '\n')
