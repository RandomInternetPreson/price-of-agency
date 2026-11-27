"""
faces_v01.py -- stress objective #5: does the GE transmission belong to the mechanism or to one
parametrization of the degraded optimizer? Four faces, each alone, each dosed to the SAME
fixed-price hand-to-mouth increase as the book's default (so the comparison is at equal
behavioral footprint):
  noise      logit temperature kappa(b) -- which is also the Sims / Matejka-McKay rational-inattention
             solution with uniform prior (so 'rational inattention' is not a fifth face but this one);
  tunnel     effective discount beta_eff(b) (Mullainathan-Shafir);
  present    naive quasi-hyperbolic present bias pb(b) on the choice (Laibson), exponential beliefs;
  sparse     Gabaix sparse attention to the asset state (consumption chosen at a perceived wealth).
Reports, model minus control: dr* (GE), dA (PE), dHTM_low (GE), P-B stability-vs-wage sign, and the
impact output response to a -25 bp monetary shock relative to the control (MPC amplification).
Writes code/rig/results_exact/hank_faces_RESULTS.md.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hank_ge as H
from run_hank_v01 import group_stats

RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results_exact'))
FACES = {'noise': ('k_tax', 0.05, (0.0, 0.25)), 'tunnel': ('tunnel', 0.0153, (0.0, 0.08)),
         'present': ('pb_tax', 0.15, (0.0, 0.9)), 'sparse': ('sparse_tax', 0.6, (0.0, 1.0))}
OFF = dict(k_tax=0.0, tunnel=0.0, pb_tax=0.0, sparse_tax=0.0)


def run():
    t0 = time.time()
    ssc = H.control_ss(); beta, vphi = ssc['beta'], ssc['vphi']
    c_pe = group_stats(H.pe_ss(dict(H.CAL, **H.CONTROL), beta, vphi))
    c_ge = group_stats(H.ge_ss(dict(H.CAL, **H.CONTROL), beta, vphi))
    d_pe = group_stats(H.pe_ss(H.CAL, beta, vphi))
    target = d_pe['HTM'] - c_pe['HTM']
    print(f"control HTM {c_pe['HTM']:.4f}; default model HTM (PE) {d_pe['HTM']:.4f}; target dHTM = {target:+.4f}  [{time.time()-t0:.0f}s]", flush=True)
    T = 120
    Gc = H.model.solve_jacobian(ssc, unknowns=H.UNKNOWNS, targets=H.TARGETS, inputs=['rstar'], outputs=['Y'], T=T)
    dz = -0.0025 * 0.8 ** np.arange(T); dYc = (Gc['Y']['rstar'] @ dz)[0]
    lines = ["# Faces of the degraded optimizer, each alone, each dosed to the same fixed-price hand-to-mouth increase (2026-11-09)", "",
             f"Target: ΔHTM(PE) = {target:+.4f} (the default model's). Control impact ΔY to −25 bp = {dYc:+.5f}.", "",
             "| face | knob at target | Δr* GE (qtr) | ΔA PE | ΔHTM_low GE | ΔBW | P-B: stab − wage (HtM_low, GE) | ΔY impact / control | ΔWELF (true β) |",
             "|---|---|---|---|---|---|---|---|---|"]
    for face, (knob, x0, (lo, hi)) in FACES.items():
        # secant/bisection on the knob to hit the target dHTM at fixed prices
        def f(x):
            cal = dict(H.CAL, **OFF); cal[knob] = x
            return group_stats(H.pe_ss(cal, beta, vphi))['HTM'] - c_pe['HTM'] - target
        a, b = lo, hi; fa, fb = f(a), f(b)
        if fa * fb > 0:
            x = b if abs(fb) < abs(fa) else a
            note = f"(target not reachable in [{lo},{hi}]; knob at bound, ΔHTM {min(fa,fb,key=abs)+target:+.4f})"
        else:
            for _ in range(14):
                x = 0.5 * (a + b); fx = f(x)
                if fa * fx <= 0: b, fb = x, fx
                else: a, fa = x, fx
                if abs(b - a) < 1e-3: break
            note = ""
        cal = dict(H.CAL, **OFF); cal[knob] = x
        m_pe = group_stats(H.pe_ss(cal, beta, vphi)); ssm = H.ge_ss(cal, beta, vphi); m_ge = group_stats(ssm)
        om = list(H.CAL['omega']); om_stab = [om[0] / 2, om[1], om[2]]; sc = 0.02
        st_m = group_stats(H.ge_ss(dict(cal, omega=om_stab, G_time=sc * H.CAL['pi_low']), beta, vphi))
        st_c = group_stats(H.ge_ss(dict(H.CAL, **H.CONTROL, omega=om_stab, G_time=sc * H.CAL['pi_low']), beta, vphi))
        wg_m = group_stats(H.ge_ss(dict(cal, Tr_low=sc), beta, vphi)); wg_c = group_stats(H.ge_ss(dict(H.CAL, **H.CONTROL, Tr_low=sc), beta, vphi))
        pb = ((st_m['htm_low'] - m_ge['htm_low']) - (st_c['htm_low'] - c_ge['htm_low'])) - ((wg_m['htm_low'] - m_ge['htm_low']) - (wg_c['htm_low'] - c_ge['htm_low']))
        try:
            Gm = H.model.solve_jacobian(ssm, unknowns=H.UNKNOWNS, targets=H.TARGETS, inputs=['rstar'], outputs=['Y'], T=T)
            amp = (Gm['Y']['rstar'] @ dz)[0] / dYc
            amp_s = f"{amp:.2f}"
        except Exception as ex:
            amp_s = f"n/a ({type(ex).__name__})"
        lines.append(f"| {face} | {knob} = {x:.4f} {note} | {m_ge['r']-c_ge['r']:+.4f} | {m_pe['A']-c_pe['A']:+.3f} | {m_ge['htm_low']-c_ge['htm_low']:+.4f} | "
                     f"{m_ge['BW']-c_ge['BW']:+.3f} | {pb:+.4f} | {amp_s} | {m_ge['WELF']-c_ge['WELF']:+.3f} |")
        print(lines[-1], f"[{time.time()-t0:.0f}s]", flush=True)
    lines += ["", "Reading: a negative P-B entry means stability beats the equal-dollar transfer on low-skill hand-to-mouth status; "
              "ΔY impact / control > 1 means the face amplifies the monetary transmission. The noise face is the rational-inattention face.",
              f"Runtime {time.time()-t0:.0f}s."]
    open(os.path.join(RES, 'hank_faces_RESULTS.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    run()
