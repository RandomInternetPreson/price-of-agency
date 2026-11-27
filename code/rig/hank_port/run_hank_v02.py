"""
run_hank_v02.py -- HANK v0.2 (own hours, own gate): the experiments the one-asset host could not run.
 1. The sold floor: who works below their own time gate, in control and model, naive and sophisticated.
 2. A time transfer with endogenous hours: is the freed hour kept, or sold back for income (hours rise)?
    vs an equal-cost money transfer. Low-skill group, GE.
 3. Working-time regulation: cap the low-skill shift at 1.0 (no long shift) vs a wage subsidy of equal cost.
 4. GE transmission in this host (r, Y, HtM) and the monetary IRF amplification.
Writes code/rig/results_exact/hank_v02_RESULTS.md.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hank_ge_labor as HL

RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results_exact'))


def run():
    t0 = time.time()
    ssc = HL.control_ss(); beta, phi = ssc['beta'], ssc['phi_h']
    gs = HL.group_stats
    c = gs(ssc); m = gs(HL.ge_ss(HL.CAL, beta, phi)); ms = gs(HL.ge_ss(dict(HL.CAL, naive=0), beta, phi))
    lines = ["# HANK v0.2 — households choose their hours, and their hours set their gate (2026-11-09)", "",
             "Host: sticky prices, flexible wage clearing efficiency hours, bonds fixed. Hours grid {0.75, 1.0, 1.25}; "
             "the low-skill floor is below the gate at 1.0 and above it at 0.75 (the short shift buys the gate); the middle "
             "floor is above the gate at 1.0 and below at 1.25 (the long shift sells it). Control: knobs off.", "",
             "## 1. The sold floor (GE levels)", "",
             "| economy | r | Y | hours low/mid/high | share below own gate low/mid/high | BW low/mid/high | HTM |", "|---|---|---|---|---|---|---|"]
    for lab, g in [('control', c), ('model, naive', m), ('model, sophisticated', ms)]:
        lines.append(f"| {lab} | {g['r']:.4f} | {g['Y']:.4f} | {g['hours_low']:.3f}/{g['hours_mid']:.3f}/{g['hours_high']:.3f} | "
                     f"{g['below_low']:.2f}/{g['below_mid']:.2f}/{g['below_high']:.2f} | {g['bw_low']:.2f}/{g['bw_mid']:.2f}/{g['bw_high']:.2f} | {g['HTM']:.3f} |")
    print(lines[-1], f"[{time.time()-t0:.0f}s]", flush=True)
    # 2. time transfer vs money transfer, with hours free to respond
    e_low = 0.43622974; dT = 0.30                     # the low floor 1.80 -> 2.10: above the gate at hours 1.0 (free time 1.10), still below at 1.25 (0.85)
    cost = ssc['w'] * e_low * dT
    arms = {'time': dict(dT_low=dT, G_time=cost * HL.CAL['pi_low']), 'money': dict(Tr_low=cost)}
    lines += ["", "## 2. Time transfer vs equal-cost money transfer, hours endogenous (low-skill group, GE, model − control)", "",
              f"Time transfer dT = {dT} (the floor clears the gate at full-time hours); equal cost = w·e_low·dT = {cost:.4f}.", "",
              "| arm | Δhours_low model | Δhours_low control | Δbelow-gate low (model) | ΔHTM_low model−control | ΔBW_low model | ΔWELF model−control |", "|---|---|---|---|---|---|---|"]
    for arm, kw in arms.items():
        am = gs(HL.ge_ss(dict(HL.CAL, **kw), beta, phi)); ac = gs(HL.ge_ss(dict(HL.CAL, **HL.CONTROL, **kw), beta, phi))
        lines.append(f"| {arm} | {am['hours_low']-m['hours_low']:+.3f} | {ac['hours_low']-c['hours_low']:+.3f} | {am['below_low']-m['below_low']:+.2f} | "
                     f"{(am['htm_low']-m['htm_low'])-(ac['htm_low']-c['htm_low']):+.4f} | {am['bw_low']-m['bw_low']:+.3f} | {(am['WELF']-m['WELF'])-(ac['WELF']-c['WELF']):+.3f} |")
        print(lines[-1], f"[{time.time()-t0:.0f}s]", flush=True)
    # 3. working-time regulation vs wage subsidy
    lines += ["", "## 3. Working-time regulation (no long shift for anyone: hours grid {0.75, 1.0}) vs a low-skill wage subsidy of equal fiscal cost (GE)", "",
              "| policy | economy | hours low/mid | below-gate low/mid | BW low/mid | HTM | Y | WELF − baseline |", "|---|---|---|---|---|---|---|---|"]
    reg_m = gs(HL.ge_ss(dict(HL.CAL, h_grid=[0.75, 1.0]), beta, phi)); reg_c = gs(HL.ge_ss(dict(HL.CAL, **HL.CONTROL, h_grid=[0.75, 1.0]), beta, phi))
    sub = 0.05 * ssc['w'] * e_low                      # a 5% wage subsidy to the low skill, as a per-household transfer proportional to hours ≈ Tr_low
    sub_m = gs(HL.ge_ss(dict(HL.CAL, Tr_low=sub), beta, phi)); sub_c = gs(HL.ge_ss(dict(HL.CAL, **HL.CONTROL, Tr_low=sub), beta, phi))
    for lab, g, base in [('regulation', reg_c, c), ('regulation', reg_m, m), ('subsidy', sub_c, c), ('subsidy', sub_m, m)]:
        econ = 'control' if base is c else 'model'
        lines.append(f"| {lab} | {econ} | {g['hours_low']:.3f}/{g['hours_mid']:.3f} | {g['below_low']:.2f}/{g['below_mid']:.2f} | {g['bw_low']:.2f}/{g['bw_mid']:.2f} | {g['HTM']:.3f} | {g['Y']:.4f} | {g['WELF']-base['WELF']:+.3f} |")
    print(lines[-1], f"[{time.time()-t0:.0f}s]", flush=True)
    # 4. transmission
    T = 120; dz = -0.0025 * 0.8 ** np.arange(T)
    try:
        Gc = HL.model.solve_jacobian(ssc, unknowns=HL.UNKNOWNS, targets=HL.TARGETS, inputs=['rstar'], outputs=['Y'], T=T)
        ssm = HL.ge_ss(HL.CAL, beta, phi)
        Gm = HL.model.solve_jacobian(ssm, unknowns=HL.UNKNOWNS, targets=HL.TARGETS, inputs=['rstar'], outputs=['Y'], T=T)
        yc = Gc['Y']['rstar'] @ dz; ym = Gm['Y']['rstar'] @ dz
        lines += ["", f"## 4. Monetary transmission with own hours: impact ΔY model/control = {ym[0]/yc[0]:.2f}, cumulative {ym.sum()/yc.sum():.2f} "
                  f"(one-asset host: 1.78 / 1.58)."]
    except Exception as ex:
        lines += ["", f"## 4. Monetary transmission: Jacobian failed ({type(ex).__name__}: {str(ex)[:80]})"]
    lines.append(f"\nRuntime {time.time()-t0:.0f}s.")
    open(os.path.join(RES, 'hank_v02_RESULTS.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    run()
