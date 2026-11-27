"""Nesting check: the control block (k_tax = tunnel = 0) against the toolkit's EGM
household (sequence_jacobian.hetblocks.hh_sim) on identical grids and incomes.
The two differ only by (i) the discretized savings choice and (ii) the logit smoothing
k_min; the gap must shrink as k_min -> 0 and the grid is refined."""
import time, sys, os
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from bw_hank import BandwidthHH
from sequence_jacobian import hetblocks, grids

CAL = dict(r=0.005, w=1 / 1.2, N=1.0, Div=1 - 1 / 1.2, Tax=0.005 * 5.6, S=1.0,
           beta=0.986, eis=0.5, rho_s=0.966, sigma_s=0.5, nS=3, amax=60.0, nA=120, nref=1, c_min=1e-3,
           Nb=4, k_min=0.02, k_tax=0.0, tunnel=0.0, Tbar=[1.8, 2.05, 2.3], T_gate=1.0, p_up=0.5,
           omega=[0.35, 0.15, 0.08], s_scar=0.25, m_scar=0.6)


def egm_reference(cal):
    e_grid, pi_e, Pi = grids.markov_rouwenhorst(rho=cal['rho_s'], sigma=cal['sigma_s'], N=cal['nS'])
    a_grid = grids.agrid(amax=cal['amax'], n=cal['nA'])
    Tr = (cal['Div'] - cal['Tax']) / np.sum(pi_e * e_grid) * e_grid
    y = cal['w'] * e_grid * cal['N'] + Tr
    hh = hetblocks.hh_sim.hh
    ss = hh.steady_state(dict(a_grid=a_grid, y=y, r=cal['r'], beta=cal['beta'], eis=cal['eis'], Pi=Pi))
    return ss


if __name__ == '__main__':
    blk = BandwidthHH()
    ref = egm_reference(CAL)
    print(f"EGM reference (toolkit hh_sim):  A = {ref['A']:.5f}   C = {ref['C']:.5f}")
    for k_min, nA, nref in [(0.02, 120, 1), (0.02, 120, 4), (0.02, 120, 8), (0.005, 120, 8), (0.001, 120, 8), (0.001, 200, 8)]:
        cal = dict(CAL, k_min=k_min, nA=nA, nref=nref)
        t0 = time.time()
        ss = blk.steady_state(cal)
        dt = time.time() - t0
        reff = egm_reference(cal)
        print(f"control k_min={k_min:<6} nA={nA} nref={nref}: A = {ss['A']:.5f} ({ss['A']-reff['A']:+.4f})  "
              f"C = {ss['C']:.5f} ({ss['C']-reff['C']:+.4f})  HTM = {ss['HTM']:.3f}  BW = {ss['BW']:.3f}  [{dt:.1f}s]")
    # the model economy at the v0 knobs
    cal = dict(CAL, k_tax=0.30, tunnel=0.06, nref=4)
    t0 = time.time(); ss = blk.steady_state(cal); dt = time.time() - t0
    print(f"model  k_tax=0.30 tunnel=0.06: A = {ss['A']:.5f}  C = {ss['C']:.5f}  HTM = {ss['HTM']:.3f}  "
          f"BW = {ss['BW']:.3f}  SCARCE = {ss['SCARCE']:.3f}  [{dt:.1f}s]")
    # Jacobian timing + check against nonlinear impulse for a small r shock
    t0 = time.time()
    J = blk.jacobian(ss, ['r', 'w'], ['A', 'C', 'HTM'], T=100)
    print(f"Jacobian T=100, 2 inputs: {time.time()-t0:.1f}s ; dA/dr[0,0] = {J['A']['r'][0,0]:.4f}  dC/dr[0,0] = {J['C']['r'][0,0]:.4f}")
    T = 100; dr = np.zeros(T); dr[5] = 1e-3
    lin = J['A']['r'] @ dr
    t0 = time.time()
    nl = blk.impulse_nonlinear(ss, {'r': dr}, ['A'])['A']
    print(f"nonlinear impulse T=100: {time.time()-t0:.1f}s ; max|lin-nonlin|/max|lin| = {np.max(np.abs(lin-nl))/np.max(np.abs(lin)):.3e}")
