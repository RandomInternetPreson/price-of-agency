"""run_hank_v02_irf.py -- dynamics in the own-hours host: linear GE IRFs (rstar, S) model vs control, and the
nonlinear path for expansions that push households through their own gates. Writes results_exact/hank_v02_irf_RESULTS.md."""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hank_ge_labor as HL
RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results_exact'))
T = 150

def run():
    t0 = time.time()
    ssc = HL.control_ss(); beta, phi = ssc['beta'], ssc['phi_h']; ssm = HL.ge_ss(HL.CAL, beta, phi)
    out = ['Y', 'C', 'N', 'w', 'HTM', 'BW', 'BELOW', 'HOURS', 'r']
    G = {n: HL.model.solve_jacobian(ss, unknowns=HL.UNKNOWNS, targets=HL.TARGETS, inputs=['rstar', 'S'], outputs=out, T=T) for n, ss in [('control', ssc), ('model', ssm)]}
    print(f"Jacobians [{time.time()-t0:.0f}s]", flush=True)
    lines = ["# HANK v0.2 dynamics — own hours, flexible wage (2026-11-09)", "", f"T = {T}; monetary shock −25 bp AR 0.8; entropy shock +0.5 AR 0.9.", ""]
    for sh, dz in [('rstar', -0.0025 * 0.8 ** np.arange(T)), ('S', 0.5 * 0.9 ** np.arange(T))]:
        lines += [f"## Linear GE response to {sh}", "", "| h | ΔY ctrl | ΔY model | ΔN model | Δw model | ΔBELOW model | ΔBW model | ΔHTM model |", "|---|---|---|---|---|---|---|---|"]
        I = {n: {o: G[n][o][sh] @ dz for o in out if sh in G[n][o]} for n in G}
        for h in [0, 1, 2, 4, 8, 12, 20]:
            m = I['model']; c = I['control']
            lines.append(f"| {h} | {c['Y'][h]:+.5f} | {m['Y'][h]:+.5f} | {m['N'][h]:+.5f} | {m['w'][h]:+.5f} | {m.get('BELOW', np.zeros(T))[h]:+.5f} | {m['BW'][h]:+.5f} | {m['HTM'][h]:+.5f} |")
        cy = I['control']['Y'].sum(); my = I['model']['Y'].sum()
        lines += ["", f"Cumulative ΔY control {cy:+.4f}, model {my:+.4f}" + (f" (ratio {my/cy:.2f})" if abs(cy) > 1e-9 else ""), ""]
    lines += ["## Nonlinear GE paths (model): expansions that push households through their own gates", ""]
    for sz in [-0.01, -0.03]:
        dz = sz * 0.8 ** np.arange(T); t1 = time.time()
        try:
            nl = HL.model.solve_impulse_nonlinear(ssm, unknowns=HL.UNKNOWNS, targets=HL.TARGETS, inputs={'rstar': dz}, outputs=out, verbose=False)
            lin = {o: G['model'][o]['rstar'] @ dz for o in out}
            lines.append(f"- {sz*1e4:+.0f} bp: peak Δhours {nl['HOURS'].max():+.4f}; ΔBELOW peak nonlinear {nl['BELOW'].max():+.4f} vs linear {lin['BELOW'].max():+.4f}; "
                         f"ΔBW min nonlinear {nl['BW'].min():+.4f} vs linear {lin['BW'].min():+.4f}; cum ΔY nonlinear {nl['Y'].sum():+.4f} vs linear {lin['Y'].sum():+.4f} [{time.time()-t1:.0f}s]")
        except Exception as ex:
            lines.append(f"- {sz*1e4:+.0f} bp: nonlinear solve failed ({type(ex).__name__}: {str(ex)[:80]})")
        print(lines[-1], flush=True)
    lines.append(f"\nRuntime {time.time()-t0:.0f}s.")
    open(os.path.join(RES, 'hank_v02_irf_RESULTS.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n'); print('\n'.join(lines))

if __name__ == '__main__':
    run()
