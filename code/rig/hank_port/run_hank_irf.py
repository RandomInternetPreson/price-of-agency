"""
run_hank_irf.py -- general-equilibrium dynamics of the bandwidth HANK: sequence-space
Jacobians of the bandwidth block (fake-news algorithm on its dense transition operator),
the GE impulse responses to a monetary shock (rstar) and a schedule-entropy shock (S), model
vs control, and the nonlinear GE path for a shock large enough to push hours through the
middle group's time gate -- the thing a linearization cannot see.
Writes code/rig/results_exact/hank_irf_RESULTS.md and figures/hank_irf_*.png.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hank_ge as H

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.normpath(os.path.join(HERE, '..', 'results_exact'))
FIG = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'figures'))
T = 200


def run():
    t0 = time.time()
    ssc = H.control_ss(); beta, vphi = ssc['beta'], ssc['vphi']
    ssm = H.ge_ss(H.CAL, beta, vphi)
    print(f"steady states [{time.time()-t0:.0f}s]  control r={ssc['r']:.4f}  model r={ssm['r']:.4f} Y={ssm['Y']:.4f}", flush=True)
    exog = ['rstar', 'S']
    out = ['Y', 'C', 'A', 'HTM', 'BW', 'r', 'pi', 'w', 'N']
    G = {}
    for name, ss in [('control', ssc), ('model', ssm)]:
        t1 = time.time()
        G[name] = H.model.solve_jacobian(ss, unknowns=H.UNKNOWNS, targets=H.TARGETS, inputs=exog, outputs=out, T=T)
        print(f"GE Jacobian {name} [{time.time()-t1:.0f}s]", flush=True)
    lines = ["# HANK port v0.1 — general-equilibrium dynamics, model vs control (2026-11-09)", "",
             f"T = {T}. Shocks: monetary (rstar, −25 bp, AR 0.8) and schedule entropy (S, +0.5, AR 0.9). "
             "Linear GE responses from sequence-space Jacobians; the fake-news algorithm is run on the bandwidth block's "
             "own dense transition operator (states b×e×a), so the stochastic (logit) policy is handled exactly.", ""]
    rho = {'rstar': 0.8, 'S': 0.9}; size = {'rstar': -0.0025, 'S': 0.5}
    irf = {}
    for sh in exog:
        dz = size[sh] * rho[sh] ** np.arange(T)
        for name in ['control', 'model']:
            irf[(sh, name)] = {o: G[name][o][sh] @ dz for o in out if sh in G[name][o]}
        lines += [f"## Linear GE response to {sh} shock", "",
                  "| horizon | ΔY control | ΔY model | ΔC control | ΔC model | ΔHTM model | ΔBW model | Δr model |", "|---|---|---|---|---|---|---|---|"]
        for h in [0, 1, 2, 4, 8, 12, 20]:
            c = irf[(sh, 'control')]; m = irf[(sh, 'model')]
            lines.append(f"| {h} | {c['Y'][h]:+.5f} | {m['Y'][h]:+.5f} | {c['C'][h]:+.5f} | {m['C'][h]:+.5f} | {m['HTM'][h]:+.5f} | {m['BW'][h]:+.5f} | {m['r'][h]:+.5f} |")
        cumY_c = irf[(sh, 'control')]['Y'].sum(); cumY_m = irf[(sh, 'model')]['Y'].sum()
        ratio = f"{cumY_m/cumY_c:.3f}" if abs(cumY_c) > 1e-9 else "n/a (control does not respond to S)"
        lines += ["", f"Cumulative ΔY: control {cumY_c:+.4f}, model {cumY_m:+.4f} (ratio {ratio}).", ""]
    # MPC-like: aggregate consumption response at impact per unit of impact income (Y) change
    for name in ['control', 'model']:
        m = irf[('rstar', name)]
        lines.append(f"{name}: impact ΔC/ΔY to the monetary shock = {m['C'][0]/m['Y'][0]:.3f}; peak ΔY = {m['Y'][np.argmax(np.abs(m['Y']))]:+.5f}.")
    lines.append("")

    # nonlinear GE path: a monetary expansion large enough to push N through the middle gate (N > 1.05)
    lines += ["## Nonlinear GE path through the time gate (model)", "",
              "A monetary expansion sized so hours cross the middle group's gate (free time Tbar_mid − N < T_gate). "
              "Linear and nonlinear paths are compared; the bandwidth drop at the crossing is what linearization misses.", ""]
    for sz in [-0.01, -0.03, -0.05]:
        dz = sz * 0.8 ** np.arange(T)
        t1 = time.time()
        try:
            nl = H.model.solve_impulse_nonlinear(ssm, unknowns=H.UNKNOWNS, targets=H.TARGETS, inputs={'rstar': dz},
                                                 outputs=out, Js={}, verbose=False)
            lin = {o: G['model'][o]['rstar'] @ dz for o in out}
            Npeak = ssm['N'] + nl['N'].max()
            lines.append(f"- shock {sz*1e4:+.0f} bp: peak N = {Npeak:.4f} (gate at {H.CAL['Tbar'][1]-H.CAL['T_gate']:.3f}); "
                         f"ΔBW min nonlinear {nl['BW'].min():+.4f} vs linear {lin['BW'].min():+.4f}; "
                         f"cum ΔY nonlinear {nl['Y'].sum():+.4f} vs linear {lin['Y'].sum():+.4f}; "
                         f"cum ΔHTM nonlinear {nl['HTM'].sum():+.4f} vs linear {lin['HTM'].sum():+.4f}  [{time.time()-t1:.0f}s]")
            irf[('nl', sz)] = nl
        except Exception as ex:
            lines.append(f"- shock {sz*1e4:+.0f} bp: nonlinear solve failed ({type(ex).__name__}: {str(ex)[:80]})")
        print(lines[-1], flush=True)
    lines.append("")
    lines.append(f"Runtime {time.time()-t0:.0f}s.")
    open(os.path.join(RES, 'hank_irf_RESULTS.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')

    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(2, 3, figsize=(13, 7))
    h = np.arange(40)
    for j, sh in enumerate(exog):
        for k, o in enumerate(['Y', 'C', 'BW']):
            a = ax[j, k]
            a.plot(h, irf[(sh, 'control')][o][:40], label='control'); a.plot(h, irf[(sh, 'model')][o][:40], label='model')
            a.axhline(0, c='gray', lw=0.5); a.set_title(f'{o} to {sh} shock'); a.set_xlabel('quarters')
            if j == 0 and k == 0: a.legend()
    plt.tight_layout(); plt.savefig(os.path.join(FIG, 'hank_irf_linear.png'), dpi=130)
    if ('nl', -0.05) in irf:
        fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
        for k, o in enumerate(['N', 'BW', 'HTM']):
            for sz, ls in [(-0.01, ':'), (-0.03, '--'), (-0.05, '-')]:
                if ('nl', sz) in irf:
                    ax[k].plot(h, irf[('nl', sz)][o][:40], ls, label=f'{sz*1e4:+.0f} bp nonlinear')
            ax[k].plot(h, (G['model'][o]['rstar'] @ (-0.05 * 0.8 ** np.arange(T)))[:40], c='gray', lw=1, label='−500 bp linear')
            ax[k].axhline(0, c='gray', lw=0.5); ax[k].set_title(o); ax[k].set_xlabel('quarters')
        ax[0].legend(fontsize=8); plt.tight_layout(); plt.savefig(os.path.join(FIG, 'hank_irf_gate.png'), dpi=130)
    print(open(os.path.join(RES, 'hank_irf_RESULTS.md'), encoding='utf-8').read())


if __name__ == '__main__':
    run()
