"""
sweep_signs.py -- the sign-stability map of the HANK results (stress objective #1).

Random draws over the whole box of bandwidth constants, calibrations, gate positions and both
forecasts; for each draw the control is recalibrated (beta, vphi), then the model's GE and PE
steady states and the policy arms are solved, and every signed result of Ch 14 §5C is recorded.
Output: one JSON line per draw in results_sweep/shard_<id>.jsonl (resumable; rerun the same
command and finished draws are skipped). Summarize with summarize_sweep.py.

Usage (Windows PowerShell, from code/rig/hank_port, venv active, sequence-jacobian installed):
    $env:PYTHONUTF8=1
    python sweep_signs.py --fast --draws 600 --workers 24 --seed 1
Fast mode: ~1-2 minutes per draw on one core (nA=80, nref=3, PE arms only for P-A'); 24 workers -> 600 draws in ~45 min.
Full mode (no --fast): ~4 minutes per draw; do not exceed ~24 workers on the Xeon or memory bandwidth throttles every worker. --smoke runs 2 draws
on 2 workers in a few minutes. Numpy threading is pinned to 1 per worker.
"""
import os, sys, json, time, argparse, traceback
os.environ.setdefault('OMP_NUM_THREADS', '1'); os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1'); os.environ.setdefault('NUMBA_NUM_THREADS', '1')
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, 'results_sweep')

# the box (uniform unless noted). Centers are the v0.1 defaults.
BOX = dict(
    k_min=(0.002, 0.02), k_tax=(0.01, 0.15), tunnel=(0.003, 0.04),
    p_up=(0.05, 0.40), omega_low=(0.03, 0.20), omega_ratio_mid=(0.2, 0.6), omega_ratio_high=(0.1, 0.4),
    s_scar=(0.0, 0.15), m_scar=(0.4, 0.8),
    Tbar_low=(1.60, 2.00), Tbar_mid_gap=(0.01, 0.30), Tbar_high=(2.2, 2.6),   # mid floor = T_gate + N(=1) + gap
    B=(3.0, 8.0), sigma_s=(0.3, 0.7), rho_s=(0.93, 0.98), mu=(1.1, 1.3),
)
CHOICES = dict(eis=[0.5, 1.0], naive=[1, 1, 1, 0])     # naive 3:1


def draw(rng, i):
    d = {k: float(rng.uniform(*v)) for k, v in BOX.items()}
    for k, v in CHOICES.items():
        d[k] = v[rng.integers(len(v))]
    d['draw'] = i
    return d


def to_cal(d, base):
    cal = dict(base)
    cal.update(k_min=d['k_min'], k_tax=d['k_tax'], tunnel=d['tunnel'], p_up=d['p_up'],
               omega=[d['omega_low'], d['omega_low'] * d['omega_ratio_mid'], d['omega_low'] * d['omega_ratio_high']],
               s_scar=d['s_scar'], m_scar=d['m_scar'],
               Tbar=[d['Tbar_low'], 1.0 + base['T_gate'] + d['Tbar_mid_gap'], d['Tbar_high']],
               B=d['B'], sigma_s=d['sigma_s'], rho_s=d['rho_s'], mu=d['mu'], eis=d['eis'], naive=d['naive'])
    return cal


def run_draw(d):
    import hank_ge as H
    from run_hank_v01 import group_stats
    t0 = time.time()
    rec = dict(d)
    FAST = bool(d.get('fast', 0))
    try:
        CAL = to_cal(d, H.CAL)
        if FAST:
            CAL.update(nA=80, nref=3)
        CTRL = dict(CAL, **H.CONTROL)
        # control calibration
        ssc = H.model_ss.solve_steady_state(CTRL, unknowns={'beta': 0.98, 'vphi': 0.88},
                                            targets={'asset_mkt': 0.0, 'wnkpc_res': 0.0}, solver='broyden_custom', ttol=1e-6)
        beta, vphi = ssc['beta'], ssc['vphi']
        rec.update(beta=float(beta), vphi=float(vphi), w=float(ssc['w']))
        if beta * (1 + CAL['rstar']) >= 0.9995:
            rec['status'] = 'beta_too_high'; return rec

        guesses = {}

        def econ(cal, ge):
            if ge:
                g = guesses.get('m' if cal.get('k_tax', 0) > 0 or cal.get('tunnel', 0) > 0 else 'c', (0.005, 1.0))
                ss = H.ge_ss(cal, beta, vphi, guess=g)
            else:
                ss = H.pe_ss(cal, beta, vphi)
            return group_stats(ss)
        c_ge = econ(CTRL, True); guesses['c'] = (c_ge['r'], c_ge['Y'])
        m_ge = econ(CAL, True); guesses['m'] = (m_ge['r'], m_ge['Y'])
        m_pe = econ(CAL, False); c_pe = econ(CTRL, False)
        # the low skill value depends on sigma_s: recompute for the wage-valued cost of the time transfer
        from sequence_jacobian import grids
        e_grid, _, _ = grids.markov_rouwenhorst(rho=CAL['rho_s'], sigma=CAL['sigma_s'], N=3)
        dT = max(0.05, CAL['T_gate'] + 1.0 - d['Tbar_low'] + 0.05)   # lift the low floor just across the gate
        cost = ssc['w'] * e_grid[0] * dT
        time_m = dict(CAL, dT_low=dT, G_time=cost * CAL['pi_low']); time_c = dict(CTRL, dT_low=dT, G_time=cost * CAL['pi_low'])
        money_m = dict(CAL, Tr_low=cost); money_c = dict(CTRL, Tr_low=cost)
        om_stab = [CAL['omega'][0] / 2, CAL['omega'][1], CAL['omega'][2]]; sc = 0.02
        stab_m = dict(CAL, omega=om_stab, G_time=sc * CAL['pi_low']); stab_c = dict(CTRL, omega=om_stab, G_time=sc * CAL['pi_low'])
        wage_m = dict(CAL, Tr_low=sc); wage_c = dict(CTRL, Tr_low=sc)
        liq_m = dict(CAL, a_borrow=0.5); liq_c = dict(CTRL, a_borrow=0.5)
        res = {}
        for name, cm, cc in [('time', time_m, time_c), ('money', money_m, money_c), ('stab', stab_m, stab_c),
                             ('wage', wage_m, wage_c), ('liq', liq_m, liq_c)]:
            for ge, tag in [(True, 'ge'), (False, 'pe')]:
                if FAST and not ge and name not in ('time', 'money'):
                    res[(name, 'm', tag)] = m_pe; res[(name, 'c', tag)] = c_pe      # PE arms skipped in fast mode
                    continue
                res[(name, 'm', tag)] = econ(cm, ge); res[(name, 'c', tag)] = econ(cc, ge)
        S2_ge = econ(dict(CAL, S=2.0), True); S2_pe = econ(dict(CAL, S=2.0), False)
        half = econ(dict(CAL, k_tax=CAL['k_tax'] / 2, tunnel=CAL['tunnel'] / 2), True)

        def dd(name, tag, key='htm_low'):
            m = res[(name, 'm', tag)]; c = res[(name, 'c', tag)]
            bm = m_ge if tag == 'ge' else m_pe; bc = c_ge if tag == 'ge' else c_pe
            return (m[key] - bm[key]) - (c[key] - bc[key])
        out = dict(
            r_ctrl=c_ge['r'], r_model=m_ge['r'], dr_ge=m_ge['r'] - c_ge['r'],
            dA_pe=m_pe['A'] - c_pe['A'], dHTM_low_ge=m_ge['htm_low'] - c_ge['htm_low'],
            dr_half=half['r'] - c_ge['r'],
            PA_time_ge=dd('time', 'ge'), PA_money_ge=dd('money', 'ge'), PA_time_pe=dd('time', 'pe'), PA_money_pe=dd('money', 'pe'),
            PB_stab_ge=dd('stab', 'ge'), PB_wage_ge=dd('wage', 'ge'), PB_stab_pe=dd('stab', 'pe'), PB_wage_pe=dd('wage', 'pe'),
            PB_stab_welf_ge=dd('stab', 'ge', 'welf_low'), PB_wage_welf_ge=dd('wage', 'ge', 'welf_low'),
            PC_resid_ge=res[('liq', 'm', 'ge')]['htm_low'] - res[('liq', 'c', 'ge')]['htm_low'],
            PC_resid_base_ge=m_ge['htm_low'] - c_ge['htm_low'],
            PE_dr_dS_ge=S2_ge['r'] - m_ge['r'], PE_dA_dS_pe=S2_pe['A'] - m_pe['A'],
            BW_model=m_ge['BW'], HTM_model=m_ge['HTM'], Y_model=m_ge['Y'],
        )
        # levels and bandwidth by program (general equilibrium), so each program can be read on every ruler
        # (consumption: low-skill and aggregate lifetime value; bandwidth by skill group) -- added 2026-11-10
        for nm, mm, cc_ in [('base', m_ge, c_ge)] + [(k, res[(k, 'm', 'ge')], res[(k, 'c', 'ge')]) for k in ('time', 'money', 'stab', 'wage')]:
            out.update({f'L_{nm}_welf_m': mm['welf_low'], f'L_{nm}_welf_c': cc_['welf_low'], f'L_{nm}_WELF_m': mm['WELF'],
                        f'L_{nm}_bw_low': mm['bw_low'], f'L_{nm}_bw_mid': mm['bw_mid'], f'L_{nm}_bw_high': mm['bw_high'],
                        f'L_{nm}_c_low': mm['c_low'], f'L_{nm}_scarce_low': mm['scarce_low']})
        rec.update(out); rec['status'] = 'ok'
    except Exception as ex:
        rec['status'] = 'fail'; rec['error'] = f"{type(ex).__name__}: {str(ex)[:120]}"
    rec['seconds'] = round(time.time() - t0, 1)
    return rec


def worker(args):
    d, path = args
    rec = run_draw(d)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec) + '\n')
    return rec['draw'], rec['status'], rec['seconds']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--draws', type=int, default=2000); ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--seed', type=int, default=1); ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--retry-failed', dest='retry_failed', action='store_true', help='rerun draws recorded as fail (ok draws are kept)')
    ap.add_argument('--fast', action='store_true', help='nA=80, nref=3, PE arms only for P-A; ~3x faster; writes to results_sweep_fast')
    ap.add_argument('--out', default='', help='output folder name under hank_port (default: results_sweep or results_sweep_fast)')
    a = ap.parse_args()
    global OUT
    if a.fast:
        OUT = os.path.join(HERE, 'results_sweep_fast')
    if a.out:
        OUT = os.path.join(HERE, a.out)
    os.makedirs(OUT, exist_ok=True)
    if a.smoke:
        a.draws, a.workers = 2, 2
    rng = np.random.default_rng(a.seed)
    draws = [draw(rng, i) for i in range(a.draws)]
    for d in draws:
        d['fast'] = int(a.fast)
    done = set()
    for fn in os.listdir(OUT):
        if fn.endswith('.jsonl'):
            for line in open(os.path.join(OUT, fn), encoding='utf-8'):
                try:
                    rec = json.loads(line)
                    if rec.get('status') == 'ok' or not a.retry_failed:
                        done.add(rec['draw'])
                except Exception:
                    pass
    todo = [d for d in draws if d['draw'] not in done]
    print(f"{len(done)} draws already done; {len(todo)} to run on {a.workers} workers", flush=True)
    import multiprocessing as mp
    t0 = time.time(); n = 0
    with mp.Pool(a.workers) as pool:
        jobs = [(d, os.path.join(OUT, f"shard_{d['draw'] % a.workers:03d}.jsonl")) for d in todo]
        for i, st, sec in pool.imap_unordered(worker, jobs):
            n += 1
            if n % 10 == 0 or a.smoke:
                el = time.time() - t0
                print(f"  {n}/{len(todo)} done  (draw {i}: {st}, {sec}s)  elapsed {el/60:.1f} min, "
                      f"eta {el/n*(len(todo)-n)/60:.0f} min", flush=True)
    print("done.", flush=True)


if __name__ == '__main__':
    main()
