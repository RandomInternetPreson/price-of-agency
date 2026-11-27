"""
sweep_two_asset.py -- the sign-stability map of the TWO-ASSET host (stress objective #9b).

The two-asset results printed in Chapter 14 5C come from one set of constants (run_two_asset.py). This draws the
constants at random -- bandwidth constants, income process, curvature, the two returns, both fees on the illiquid
account, the discount factor -- and scores every signed two-asset claim in each economy:
  K_down      illiquid wealth is lower in the model than in the control
  A_down      liquid wealth is lower (fixed returns)
  r_up        the liquid rate that clears the liquid market at the control's beta is above the control's
  poor_up     the POOR hand-to-mouth share rises            wealthy_down   the WEALTHY hand-to-mouth share falls
  dose        half the dose moves illiquid wealth less than the full dose, same sign
  PC          the low-skill hand-to-mouth gap (model - control) stays positive after the borrowing limit is opened
  time_htm / stab_htm      the time transfer / stability lowers low-skill hand-to-mouth in the model
  time_K / stab_K          ... and raises low-skill illiquid wealth
  cash_K_down              the equal-cost cash transfer lowers low-skill illiquid wealth
  cash_welf_time / cash_welf_stab   cash beats time / stability on low-skill welfare (model gain minus control gain)
                                    -- the REVERSAL of the one-asset ranking that the printed economy showed
Per draw: beta drawn, the control's liquid holdings taken as the liquid supply, model and control solved, the
market-clearing liquid rate by bisection, five policy arms in both economies: 23 household solves, 15-25 minutes on one core.
Output: one JSON line per draw in results_two_asset/shard_<id>.jsonl (resumable). Summarize: summarize_two_asset.py.

Usage:  python sweep_two_asset.py --draws 300 --workers 24      (--smoke: 2 draws on a coarse grid)
"""
import os, sys, json, time, argparse, traceback
os.environ.setdefault('OMP_NUM_THREADS', '1'); os.environ.setdefault('MKL_NUM_THREADS', '1')
os.environ.setdefault('OPENBLAS_NUM_THREADS', '1'); os.environ.setdefault('NUMBA_NUM_THREADS', '1')
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
OUT = os.path.join(HERE, 'results_two_asset')

BOX = dict(
    k_min=(0.002, 0.02), k_tax=(0.01, 0.15), tunnel=(0.003, 0.04),
    p_up=(0.05, 0.40), omega_low=(0.03, 0.20), omega_ratio_mid=(0.2, 0.6), omega_ratio_high=(0.1, 0.4),
    s_scar=(0.0, 0.15), m_scar=(0.4, 0.8), Tbar_low=(1.60, 2.00), Tbar_mid_gap=(0.01, 0.30), Tbar_high=(2.2, 2.6),
    sigma_s=(0.3, 0.7), rho_s=(0.93, 0.98),
    spread=(0.005, 0.015),            # r_k - r_a per quarter
    chi_f=(0.005, 0.05), chi_p=(0.0, 0.05),
    beta_gap=(0.004, 0.020),          # beta = 1/(1 + r_k) - gap  (the printed economy: 0.0106)
)
CHOICES = dict(eis=[0.5, 1.0])


def draw(rng, i):
    d = {k: float(rng.uniform(*v)) for k, v in BOX.items()}
    for k, v in CHOICES.items():
        d[k] = v[rng.integers(len(v))]
    d['draw'] = i
    return d


def run_draw(d):
    import bw_two_asset as T
    t0 = time.time(); rec = dict(d); hh = T.TwoAssetBW(); Vc = {}
    grid = dict(nA=30, nK=8, nref=2) if d.get('smoke') else dict(nA=50, nK=12, nref=2)
    r_a = T.DEFAULTS['r_a']; r_k = r_a + d['spread']
    base = dict(grid, r_k=r_k, eis=d['eis'], sigma_s=d['sigma_s'], rho_s=d['rho_s'], chi_f=d['chi_f'], chi_p=d['chi_p'],
                p_up=d['p_up'], omega=[d['omega_low'], d['omega_low'] * d['omega_ratio_mid'], d['omega_low'] * d['omega_ratio_high']],
                s_scar=d['s_scar'], m_scar=d['m_scar'], Tbar=[d['Tbar_low'], 1.0 + T.DEFAULTS['T_gate'] + d['Tbar_mid_gap'], d['Tbar_high']],
                k_min=d['k_min'])
    bw = dict(k_tax=d['k_tax'], tunnel=d['tunnel'])
    nsolve = [0]

    def S(cal, key=None):
        nsolve[0] += 1
        s = hh.solve(dict(base, **cal), V0=Vc.get(key))
        if key: Vc[key] = s['_V']
        return s
    try:
        # 1. beta is drawn (a gap below the illiquid return's bound); the control's liquid holdings are the liquid supply
        beta = 1.0 / (1.0 + r_k) - d['beta_gap']; rec['beta'] = beta
        C = dict(T.CONTROL, beta=beta); M = dict(bw, beta=beta)
        c = S(C, 'c'); target = c['A']; rec['b_liq'] = target
        m = S(M, 'm'); h = S(dict(M, k_tax=bw['k_tax'] / 2, tunnel=bw['tunnel'] / 2), 'm')
        for k in ['A', 'K', 'HTM', 'WHTM', 'PHTM', 'htm_low', 'k_low', 'welf_low', 'BW', 'top_a', 'top_k']:
            rec['c_' + k] = c[k]; rec['m_' + k] = m[k]
        rec['h_K'] = h['K']; rec['h_A'] = h['A']
        rec['m_bw_groups'] = m['bw_groups']; rec['c_bw_groups'] = c['bw_groups']
        # 2. the liquid rate that clears the liquid market in the model
        lo, hi = r_a, min(r_k - 5e-4, 1 / beta - 1 - 5e-4)
        flo = m['A'] - target; fhi = S(dict(M, r_a=hi), 'm')['A'] - target
        if flo * fhi < 0:
            for _ in range(9):
                mid = 0.5 * (lo + hi); fm = S(dict(M, r_a=mid), 'm')['A'] - target
                if flo * fm <= 0: hi, fhi = mid, fm
                else: lo, flo = mid, fm
            rec['r_star'] = 0.5 * (lo + hi); rec['r_cross'] = 1
        else:
            rec['r_star'] = float('nan'); rec['r_cross'] = 0; rec['A_at_rmax'] = fhi + target
        # 3. policy arms at fixed returns, both economies
        e_low = hh.setup(dict(T.DEFAULTS, **base))['e_grid'][0]
        dT = 0.25; cost = T.DEFAULTS['w'] * e_low * dT; pi_low = 0.25; sc = 0.02; Tax = T.DEFAULTS['Tax']
        om = base['omega']
        arms = {'liq': dict(a_borrow=0.5),
                'time': dict(dT_low=dT, Tax=Tax + cost * pi_low), 'money': dict(Tr_low=cost, Tax=Tax + cost * pi_low),
                'stab': dict(omega=[om[0] / 2, om[1], om[2]], Tax=Tax + sc * pi_low), 'trans': dict(Tr_low=sc, Tax=Tax + sc * pi_low)}
        for name, kw in arms.items():
            pc = S(dict(C, **kw)); pm = S(dict(M, **kw))
            rec[name + '_htm_c'] = pc['htm_low']; rec[name + '_htm_m'] = pm['htm_low']
            rec[name + '_dK_m'] = pm['k_low'] - m['k_low']; rec[name + '_dK_c'] = pc['k_low'] - c['k_low']
            rec[name + '_dW_m'] = pm['welf_low'] - m['welf_low']; rec[name + '_dW_c'] = pc['welf_low'] - c['welf_low']
            rec[name + '_dPHTM_m'] = pm['PHTM'] - m['PHTM']
            rec[name + '_bw_groups_m'] = pm['bw_groups']          # every program on the bandwidth ruler (added 2026-11-10)
        rec['status'] = 'ok'
    except Exception as ex:
        rec['status'] = 'fail'; rec['error'] = f"{type(ex).__name__}: {str(ex)[:200]}"; rec['trace'] = traceback.format_exc()[-400:]
    rec['solves'] = nsolve[0]; rec['seconds'] = round(time.time() - t0, 1)
    return rec


def worker(args):
    d, path = args
    rec = run_draw(d)
    with open(path, 'a', encoding='utf-8') as f:
        f.write(json.dumps(rec) + '\n')
    return d['draw'], rec['status'], rec['seconds']


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--draws', type=int, default=300); ap.add_argument('--workers', type=int, default=8)
    ap.add_argument('--seed', type=int, default=9); ap.add_argument('--smoke', action='store_true')
    ap.add_argument('--out', default='', help='output folder name under hank_port (default results_two_asset)')
    a = ap.parse_args()
    global OUT
    if a.out:
        OUT = os.path.join(HERE, a.out)
    if a.smoke:
        a.draws, a.workers = 2, 2; OUT = OUT + '_smoke'
    os.makedirs(OUT, exist_ok=True)
    rng = np.random.default_rng(a.seed)
    draws = [draw(rng, i) for i in range(a.draws)]
    for d in draws:
        d['smoke'] = int(a.smoke)
    done = set()
    for fn in os.listdir(OUT):
        if fn.endswith('.jsonl'):
            for line in open(os.path.join(OUT, fn), encoding='utf-8'):
                try: done.add(json.loads(line)['draw'])
                except Exception: pass
    todo = [d for d in draws if d['draw'] not in done]
    print(f"{len(done)} draws already done; {len(todo)} to run on {a.workers} workers", flush=True)
    import multiprocessing as mp
    t0 = time.time(); n = 0
    with mp.Pool(a.workers) as pool:
        jobs = [(d, os.path.join(OUT, f"shard_{d['draw'] % a.workers:03d}.jsonl")) for d in todo]
        for i, st, sec in pool.imap_unordered(worker, jobs):
            n += 1; el = time.time() - t0
            print(f"  {n}/{len(todo)} done  (draw {i}: {st}, {sec}s)  elapsed {el/60:.1f} min, eta {el/n*(len(todo)-n)/60:.0f} min", flush=True)
    print("done.", flush=True)


if __name__ == '__main__':
    main()
