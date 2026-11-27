"""
run_hank_v01.py -- the preregistered predictions (docs/HANK_PREREG_v0.1.md) in general
equilibrium, model minus control, with the partial-equilibrium check beside each.
Writes code/rig/results_exact/hank_v01_RESULTS.md and figures/hank_v01_*.png.
Steady-state experiments only (dynamics in run_hank_irf.py). CPU; ~15 minutes.
"""
import os, sys, time, json
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hank_ge as H
from bw_hank import BandwidthHH

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.normpath(os.path.join(HERE, '..', 'results_exact'))
FIG = os.path.normpath(os.path.join(HERE, '..', '..', '..', 'figures'))
os.makedirs(RES, exist_ok=True); os.makedirs(FIG, exist_ok=True)
blk = H.hh


def group_stats(ss):
    """Per-skill statistics from the block's internals: HTM, true-beta welfare, bandwidth, consumption."""
    D = ss.internals['hh_bw']['D']; P = ss.internals['hh_bw']['P']
    st = blk.setup({k: ss[k] for k in blk.inputs})
    o = blk.per_state_outputs(st, P)
    L = blk.transition(st, P)
    o['welf'] = blk.true_welfare(st, P, L).reshape(D.shape)
    out = {}
    for ie, tag in enumerate(['low', 'mid', 'high']):
        m = D[:, ie, :]; w = m.sum()
        for k in ['htm', 'welf', 'bw', 'c', 'a', 'scarce']:
            out[f'{k}_{tag}'] = float((m * o[k][:, ie, :]).sum() / w)
    for k in ['r', 'Y', 'N', 'A', 'C', 'HTM', 'BW', 'SCARCE', 'WELF']:
        out[k] = float(ss[k])
    return out


def economy(cal, beta, vphi, ge=True, guess=(0.005, 1.0)):
    ss = H.ge_ss(cal, beta, vphi, guess=guess) if ge else H.pe_ss(cal, beta, vphi)
    return group_stats(ss)


def run():
    t0 = time.time()
    lines = ["# HANK port v0.1 — preregistered predictions in general equilibrium (2026-11-09)", "",
             "Every entry is model minus control unless marked level. GE: (r, Y) clear markets at the control's β, vphi. "
             "PE: prices at the control's values. Host and constants: hank_ge.py; preregistration: docs/HANK_PREREG_v0.1.md.", ""]
    ssc = H.control_ss()
    beta, vphi = ssc['beta'], ssc['vphi']
    CAL = dict(H.CAL)
    CTRL = dict(CAL, **H.CONTROL)
    res = {}

    def both(name, cal_m, cal_c):
        for ge in (True, False):
            tag = 'GE' if ge else 'PE'
            res[(name, 'model', tag)] = economy(cal_m, beta, vphi, ge)
            res[(name, 'control', tag)] = economy(cal_c, beta, vphi, ge)
        print(f"  {name:<22} done [{time.time()-t0:.0f}s]", flush=True)

    # baselines
    both('baseline', CAL, CTRL)
    b = res[('baseline', 'model', 'GE')]; c = res[('baseline', 'control', 'GE')]
    lines += ["## Baselines (levels)", "",
              "| economy | r (qtr) | Y | HTM | HTM_low | BW | BW_low | SCARCE | A |", "|---|---|---|---|---|---|---|---|---|"]
    for lab, d in [('control GE', c), ('model GE', b), ('model PE', res[('baseline', 'model', 'PE')])]:
        lines.append(f"| {lab} | {d['r']:.4f} | {d['Y']:.4f} | {d['HTM']:.3f} | {d['htm_low']:.3f} | {d['BW']:.3f} | {d['bw_low']:.3f} | {d['SCARCE']:.3f} | {d['A']:.3f} |")
    lines.append("")

    # P-A': time transfer that lifts the low time floor across the gate vs equal-cost money transfer
    e_low = 0.43622974; w0 = ssc['w']
    dT = 0.25                                   # free time 0.80 -> 1.05 (gate at 1.00 with N = 1)
    cost = w0 * e_low * 1.0 * dT                # wage-valued, per low household
    time_m = dict(CAL, dT_low=dT, G_time=cost * CAL['pi_low']); time_c = dict(CTRL, dT_low=dT, G_time=cost * CAL['pi_low'])
    money_m = dict(CAL, Tr_low=cost); money_c = dict(CTRL, Tr_low=cost)
    both('PA_time', time_m, time_c); both('PA_money', money_m, money_c)
    lines += ["## P-A′ — time transfer (floor across the gate) vs equal-cost money transfer; low-skill group", "",
              f"Time transfer dT = {dT} (free time 0.80 → 1.05 at N = 1); equal cost = w·e_low·dT = {cost:.4f} per low household, both tax-financed.", "",
              "| arm | eq. | ΔHTM_low model | ΔHTM_low control | model − control | ΔWELF_low model−control | ΔBW_low model |",
              "|---|---|---|---|---|---|---|"]
    for arm in ['PA_time', 'PA_money']:
        for tag in ['GE', 'PE']:
            m = res[(arm, 'model', tag)]; cc = res[(arm, 'control', tag)]
            bm = res[('baseline', 'model', tag)]; bc = res[('baseline', 'control', tag)]
            dm = m['htm_low'] - bm['htm_low']; dc = cc['htm_low'] - bc['htm_low']
            dw = (m['welf_low'] - bm['welf_low']) - (cc['welf_low'] - bc['welf_low'])
            lines.append(f"| {arm[3:]} | {tag} | {dm:+.4f} | {dc:+.4f} | {dm-dc:+.4f} | {dw:+.4f} | {m['bw_low']-bm['bw_low']:+.3f} |")
    lines.append("")

    # P-B: halve low-skill entropy vs equal-cost wage transfer (cost = ? the stability program is priced at the same fiscal cost)
    om = list(CAL['omega']); om_stab = [om[0] / 2, om[1], om[2]]
    stab_cost = 0.02                            # resource cost of the stability program per low household (model constant)
    stab_m = dict(CAL, omega=om_stab, G_time=stab_cost * CAL['pi_low']); stab_c = dict(CTRL, omega=om_stab, G_time=stab_cost * CAL['pi_low'])
    wage_m = dict(CAL, Tr_low=stab_cost); wage_c = dict(CTRL, Tr_low=stab_cost)
    both('PB_stability', stab_m, stab_c); both('PB_wage', wage_m, wage_c)
    lines += ["## P-B — schedule stability (low-skill entropy halved) vs equal-dollar transfer; two metrics", "",
              f"Both arms cost {stab_cost} per low household. Welfare is true-β value of the low group.", "",
              "| arm | eq. | ΔHTM_low (model−control) | ΔWELF_low (model−control) | ΔBW_low model | Δscarce_low model |", "|---|---|---|---|---|---|"]
    for arm in ['PB_stability', 'PB_wage']:
        for tag in ['GE', 'PE']:
            m = res[(arm, 'model', tag)]; cc = res[(arm, 'control', tag)]
            bm = res[('baseline', 'model', tag)]; bc = res[('baseline', 'control', tag)]
            dh = (m['htm_low'] - bm['htm_low']) - (cc['htm_low'] - bc['htm_low'])
            dw = (m['welf_low'] - bm['welf_low']) - (cc['welf_low'] - bc['welf_low'])
            lines.append(f"| {arm[3:]} | {tag} | {dh:+.4f} | {dw:+.4f} | {m['bw_low']-bm['bw_low']:+.3f} | {m['scarce_low']-bm['scarce_low']:+.3f} |")
    lines.append("")

    # P-C: liquidity repaired (borrowing limit 0.5), bandwidth not; then both
    liq_m = dict(CAL, a_borrow=0.5); liq_c = dict(CTRL, a_borrow=0.5)
    both_m = dict(CAL, a_borrow=0.5, dT_low=dT, omega=om_stab)
    both('PC_liquidity', liq_m, liq_c)
    for ge in (True, False):
        res[('PC_both', 'model', 'GE' if ge else 'PE')] = economy(both_m, beta, vphi, ge)
    lines += ["## P-C — hand-to-mouth after liquidity is repaired (borrowing limit 0 → 0.5), bandwidth not", "",
              "| eq. | HTM_low control | HTM_low model | residual (model − control) | residual at baseline | model, liquidity + bandwidth repaired |", "|---|---|---|---|---|---|"]
    for tag in ['GE', 'PE']:
        m = res[('PC_liquidity', 'model', tag)]; cc = res[('PC_liquidity', 'control', tag)]
        bm = res[('baseline', 'model', tag)]; bc = res[('baseline', 'control', tag)]
        bb = res[('PC_both', 'model', tag)]
        lines.append(f"| {tag} | {cc['htm_low']:.4f} | {m['htm_low']:.4f} | {m['htm_low']-cc['htm_low']:+.4f} | {bm['htm_low']-bc['htm_low']:+.4f} | {bb['htm_low']:.4f} |")
    lines.append("")

    # P-E: schedule entropy S sweep (model, GE and PE) + the gate crossing in N
    lines += ["## P-E — the externality: schedule entropy S and the equilibrium real rate", "",
              "| S | r* GE (qtr) | Y GE | BW GE | HTM GE | A at control prices (PE) | BW PE |", "|---|---|---|---|---|---|---|"]
    Sgrid = [0.0, 0.5, 1.0, 1.5, 2.0]
    PE = []
    for S in Sgrid:
        g = economy(dict(CAL, S=S), beta, vphi, True); p = economy(dict(CAL, S=S), beta, vphi, False)
        PE.append((S, g, p))
        lines.append(f"| {S} | {g['r']:.4f} | {g['Y']:.4f} | {g['BW']:.3f} | {g['HTM']:.3f} | {p['A']:.3f} | {p['BW']:.3f} |")
    print(f"  S sweep done [{time.time()-t0:.0f}s]", flush=True)
    lines.append("")
    # gate crossing: PE, hours N raised through the middle group's gate (Tbar_mid - N = T_gate at N = 1.05)
    lines += ["### The cascade: hours through the middle group's time gate (PE, model)", "",
              "| N | free time mid | BW | BW_mid | HTM | A |", "|---|---|---|---|---|---|"]
    Ngrid = [0.98, 1.00, 1.02, 1.04, 1.049, 1.051, 1.06, 1.08, 1.10]
    gate = []
    for N in Ngrid:
        p = economy(dict(CAL, N=N, Y=N), beta, vphi, False)
        gate.append((N, p))
        lines.append(f"| {N} | {CAL['Tbar'][1]-N:.3f} | {p['BW']:.3f} | {p['bw_mid']:.3f} | {p['HTM']:.3f} | {p['A']:.3f} |")
    lines.append("")

    # dose-response: scale both knobs together
    lines += ["## Dose–response (GE, model − control at baseline policies)", "",
              "| dose | k_tax | tunnel | Δr* | ΔHTM_low | ΔBW | ΔA (PE) |", "|---|---|---|---|---|---|---|"]
    doses = [0.0, 0.25, 0.5, 1.0, 1.5]
    dose_rows = []
    for d in doses:
        cm = dict(CAL, k_tax=CAL['k_tax'] * d, tunnel=CAL['tunnel'] * d)
        g = economy(cm, beta, vphi, True); p = economy(cm, beta, vphi, False)
        dose_rows.append((d, g, p))
        lines.append(f"| {d} | {cm['k_tax']:.4f} | {cm['tunnel']:.4f} | {g['r']-c['r']:+.4f} | {g['htm_low']-c['htm_low']:+.4f} | {g['BW']-c['BW']:+.3f} | {p['A']-res[('baseline','control','PE')]['A']:+.3f} |")
    print(f"  dose sweep done [{time.time()-t0:.0f}s]", flush=True)
    lines.append("")
    # forecast comparison: the same repairs under the SOPHISTICATED household (PE)
    lines += ["## Forecast comparison (PE): naive vs sophisticated household", "",
              "The default household is naive about its own bandwidth (plans as if its level were permanent). "
              "The sophisticated variant forecasts its own degradation. Same knobs, same policies.", "",
              "| forecast | economy | HTM_low | a_low | A | BW_low |", "|---|---|---|---|---|---|"]
    for nv, lab in [(1, 'naive'), (0, 'sophisticated')]:
        for name, cm in [('baseline', dict(CAL, naive=nv)), ('time transfer', dict(CAL, naive=nv, dT_low=dT)),
                         ('stability', dict(CAL, naive=nv, omega=om_stab)), ('no drain at all', dict(CAL, naive=nv, omega=[0, 0, 0], s_scar=0.0, dT_low=1.0))]:
            p = economy(cm, beta, vphi, False)
            lines.append(f"| {lab} | {name} | {p['htm_low']:.4f} | {p['a_low']:.3f} | {p['A']:.3f} | {p['bw_low']:.3f} |")
    print(f"  forecast comparison done [{time.time()-t0:.0f}s]", flush=True)
    lines.append("")
    lines.append(f"Runtime {time.time()-t0:.0f}s.")
    open(os.path.join(RES, 'hank_v01_RESULTS.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    json.dump({f"{k[0]}|{k[1]}|{k[2]}": v for k, v in res.items()}, open(os.path.join(RES, 'hank_v01_results.json'), 'w'), indent=1)

    # figures
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 3, figsize=(13, 3.8))
    ax[0].plot([x[0] for x in PE], [x[1]['r'] * 400 for x in PE], 'o-', label='r* GE (annual %)')
    ax[0].set_xlabel('schedule entropy S'); ax[0].set_ylabel('real rate, annual %'); ax[0].set_title('P-E: entropy → real rate')
    ax[1].plot([x[0] for x in gate], [x[1]['BW'] for x in gate], 'o-'); ax[1].axvline(CAL['Tbar'][1] - CAL['T_gate'], ls='--', c='gray')
    ax[1].set_xlabel('hours N'); ax[1].set_ylabel('aggregate bandwidth'); ax[1].set_title('cascade: hours through the gate (PE)')
    ax[2].plot(doses, [x[1]['htm_low'] - c['htm_low'] for x in dose_rows], 'o-', label='ΔHTM_low')
    ax[2].plot(doses, [(x[1]['r'] - c['r']) * 400 for x in dose_rows], 's-', label='Δr* (annual pp)')
    ax[2].axhline(0, c='gray', lw=0.5); ax[2].set_xlabel('dose (× baseline knobs)'); ax[2].set_title('dose–response, GE'); ax[2].legend()
    plt.tight_layout(); plt.savefig(os.path.join(FIG, 'hank_v01_summary.png'), dpi=130)
    print(open(os.path.join(RES, 'hank_v01_RESULTS.md'), encoding='utf-8').read())


if __name__ == '__main__':
    run()
