"""
macro_objections.py -- stress objective #8: the standard macro objections, computed.
 (a) Lucas: is the model's own reduced form policy-invariant? The impact output response to a monetary
     shock is computed at three levels of schedule entropy S. If it moves, a reduced-form MPC estimated
     under one schedule regime misprices policy under another -- the model's Lucas critique of the audit.
 (b) Aggregation / measurement: the hand-to-mouth results under three cutoffs (a' within 0.05, 0.15, 0.30
     of the limit) -- do the GE signs depend on how HtM is measured?
 (c) Income process: five skill states instead of three (Rouwenhorst), same persistence and dispersion --
     does GE transmission survive a finer income grid?
 (d) Ricardian equivalence is not testable in steady state (a permanent program needs a permanent tax);
     printed as owed to the dynamics.
Writes code/rig/results_exact/hank_macro_objections.md.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hank_ge as H
from run_hank_v01 import group_stats

RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results_exact'))


def run():
    t0 = time.time(); T = 120
    ssc = H.control_ss(); beta, vphi = ssc['beta'], ssc['vphi']
    dz = -0.0025 * 0.8 ** np.arange(T)
    Gc = H.model.solve_jacobian(ssc, unknowns=H.UNKNOWNS, targets=H.TARGETS, inputs=['rstar'], outputs=['Y', 'C'], T=T)
    dYc = (Gc['Y']['rstar'] @ dz)
    lines = ["# Standard macro objections, computed (2026-11-09)", "", "## (a) Lucas: the monetary transmission under three schedule regimes (model)", "",
             f"Control impact ΔY = {dYc[0]:+.5f}, cumulative {dYc.sum():+.4f} (−25 bp, AR 0.8).", "",
             "| S | r* | impact ΔY / control | cumulative ΔY / control | HTM |", "|---|---|---|---|---|"]
    for S in [0.5, 1.0, 2.0]:
        ssm = H.ge_ss(dict(H.CAL, S=S), beta, vphi)
        Gm = H.model.solve_jacobian(ssm, unknowns=H.UNKNOWNS, targets=H.TARGETS, inputs=['rstar'], outputs=['Y'], T=T)
        dYm = Gm['Y']['rstar'] @ dz
        lines.append(f"| {S} | {ssm['r']:.4f} | {dYm[0]/dYc[0]:.3f} | {dYm.sum()/dYc.sum():.3f} | {ssm['HTM']:.3f} |")
        print(lines[-1], f"[{time.time()-t0:.0f}s]", flush=True)
    lines += ["", "If the ratio moves with S, the economy's measured transmission is a function of the schedule regime: a reduced-form "
              "estimate taken under one regime does not transfer to another. The bandwidth constants themselves (gate, drains, knobs) "
              "are technology of attention in the model and are policy-invariant by construction; the forecast assumption (naive) is the "
              "one behavioral premise a policy could change.", ""]
    # (b) HtM cutoffs
    lines += ["## (b) Hand-to-mouth cutoff: GE signs under three measurements", "",
              "| cutoff | HTM_low control | HTM_low model | Δ | P-B stab − wage (HtM_low) | P-C residual after liquidity |", "|---|---|---|---|---|---|"]
    om = list(H.CAL['omega']); om_stab = [om[0] / 2, om[1], om[2]]; sc = 0.02
    for cut in [0.05, 0.15, 0.30]:
        C_ = dict(H.CAL, **H.CONTROL, htm_cut=cut); M_ = dict(H.CAL, htm_cut=cut)
        c = group_stats(H.ge_ss(C_, beta, vphi)); m = group_stats(H.ge_ss(M_, beta, vphi))
        sm = group_stats(H.ge_ss(dict(M_, omega=om_stab, G_time=sc * H.CAL['pi_low']), beta, vphi)); scn = group_stats(H.ge_ss(dict(C_, omega=om_stab, G_time=sc * H.CAL['pi_low']), beta, vphi))
        wm = group_stats(H.ge_ss(dict(M_, Tr_low=sc), beta, vphi)); wc = group_stats(H.ge_ss(dict(C_, Tr_low=sc), beta, vphi))
        pb = ((sm['htm_low'] - m['htm_low']) - (scn['htm_low'] - c['htm_low'])) - ((wm['htm_low'] - m['htm_low']) - (wc['htm_low'] - c['htm_low']))
        lm = group_stats(H.ge_ss(dict(M_, a_borrow=0.5), beta, vphi)); lc = group_stats(H.ge_ss(dict(C_, a_borrow=0.5), beta, vphi))
        lines.append(f"| {cut} | {c['htm_low']:.3f} | {m['htm_low']:.3f} | {m['htm_low']-c['htm_low']:+.4f} | {pb:+.4f} | {lm['htm_low']-lc['htm_low']:+.4f} |")
        print(lines[-1], f"[{time.time()-t0:.0f}s]", flush=True)
    # (c) five skill states
    lines += ["", "## (c) Five skill states (same ρ, σ): GE transmission", "", "| economy | r* | Y | A (PE) | HTM | BW |", "|---|---|---|---|---|---|"]
    cal5 = dict(H.CAL, nS=5, pi_low=None)
    from sequence_jacobian import grids
    e5, pi5, _ = grids.markov_rouwenhorst(rho=cal5['rho_s'], sigma=cal5['sigma_s'], N=5)
    cal5['pi_low'] = float(pi5[0]); cal5['Tbar'] = [1.70, 1.80, 2.05, 2.30, 2.40]; cal5['omega'] = [0.12, 0.10, 0.04, 0.025, 0.02]
    c5 = H.model_ss.solve_steady_state(dict(cal5, **H.CONTROL), unknowns={'beta': 0.98, 'vphi': 0.88},
                                       targets={'asset_mkt': 0.0, 'wnkpc_res': 0.0}, solver='broyden_custom', ttol=1e-6)
    m5 = H.ge_ss(cal5, c5['beta'], c5['vphi']); p5 = H.pe_ss(cal5, c5['beta'], c5['vphi'])
    lines.append(f"| control (5 states) | {c5['r']:.4f} | {c5['Y']:.4f} | {c5['A']:.3f} | {c5['HTM']:.3f} | {c5['BW']:.3f} |")
    lines.append(f"| model (5 states) | {m5['r']:.4f} | {m5['Y']:.4f} | {p5['A']:.3f} | {m5['HTM']:.3f} | {m5['BW']:.3f} |")
    lines += ["", "## (d) Ricardian equivalence", "", "Not testable in steady state: a permanent program needs a permanent tax, and bonds in fixed supply pin the "
              "debt path. Owed to the dynamics (a debt-financed temporary program vs a tax-financed one).", f"Runtime {time.time()-t0:.0f}s."]
    open(os.path.join(RES, 'hank_macro_objections.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    run()
