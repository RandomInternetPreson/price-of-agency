"""
hank_ge.py -- the one-asset HANK with sticky prices (Rotemberg) and sticky wages (union),
in the Sequence-Space Jacobian toolkit's own layout (Auclert, Bardoczy, Rognlie, Straub
2021; the `hank` and `two_asset` examples shipped with the package), with the household
block replaced by the book's bandwidth block (bw_hank.BandwidthHH).

Blocks: firm (linear in labor, price-adjustment cost), monetary (Taylor rule), price NKPC,
union (wage NKPC on mean e*u'(c)), fiscal (bonds B fixed, lump-sum tax by skill, optional
transfer to the lowest skill financed by the same tax), market clearing.

Steady state of the CONTROL economy: beta and vphi calibrated so that A = B and the wage
NKPC holds at N = 1, Y = 1, r = rstar = 0.5% per quarter (the toolkit's calibration).
The MODEL economy keeps beta and vphi from the control and lets (rstar, Y) adjust so that
markets clear -- the general-equilibrium feedback the toy could not see.
Policies are inputs of the household block: Tr_low (money transfer per low-skill household,
tax-financed), dT_low (time transfer: raises the low-skill time floor), S (schedule
entropy), a_borrow (borrowing limit, for the liquidity-repair experiment).
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sequence_jacobian import simple, create_model
from bw_hank import BandwidthHH

hh = BandwidthHH()


@simple
def firm(Y, w, Z, pi, mu, kappa):
    N = Y / Z
    Div = Y - w * N - mu / (mu - 1) / (2 * kappa) * (1 + pi).apply(np.log) ** 2 * Y
    return N, Div


@simple
def monetary(pi, rstar, phi):
    r = (1 + rstar(-1) + phi * pi(-1)) / (1 + pi) - 1
    return r


@simple
def nkpc(pi, w, Z, Y, r, mu, kappa):
    nkpc_res = kappa * (w / Z - 1 / mu) + Y(+1) / Y * (1 + pi(+1)).apply(np.log) / (1 + r(+1)) \
               - (1 + pi).apply(np.log)
    return nkpc_res


@simple
def nkpc_ss(Z, mu):
    w = Z / mu
    return w


@simple
def union(w, pi, N, UCE, beta, vphi, frisch, muw, kappaw):
    piw = (1 + pi) * w / w(-1) - 1
    wnkpc_res = kappaw * (vphi * N ** (1 + 1 / frisch) - w * N * UCE / muw) \
                + beta * (1 + piw(+1)).apply(np.log) - (1 + piw).apply(np.log)
    return piw, wnkpc_res


@simple
def fiscal(r, B, Tr_low, pi_low, G_time):
    Tax = r * B + Tr_low * pi_low + G_time   # bonds fixed; transfers and the time program are tax-financed
    return Tax


@simple
def mkt_clearing(A, B, Y, C, pi, mu, kappa):
    asset_mkt = A - B
    goods_mkt = Y - C - mu / (mu - 1) / (2 * kappa) * (1 + pi).apply(np.log) ** 2 * Y
    return asset_mkt, goods_mkt


BLOCKS = [hh, firm, monetary, fiscal, mkt_clearing, nkpc, union]
model = create_model(BLOCKS, name='One-asset HANK with bandwidth')
model_ss = create_model([hh, firm, monetary, fiscal, mkt_clearing, nkpc_ss, union], name='SS')

UNKNOWNS = ['Y', 'w', 'pi']
TARGETS = ['asset_mkt', 'wnkpc_res', 'nkpc_res']

# ---- calibration (quarterly). Economy: the toolkit's. Bandwidth: model constants, none asserted of the world.
CAL = dict(rstar=0.005, Z=1.0, Y=1.0, pi=0.0, mu=1.2, kappa=0.1, phi=1.5, B=5.6,
           frisch=0.5, muw=1.1, kappaw=0.1,
           eis=0.5, rho_s=0.966, sigma_s=0.5, nS=3, amax=60.0, nA=120, nref=4, c_min=1e-3, a_borrow=0.0,
           # bandwidth: the v0 (annual) constants rescaled to a quarter, p -> 1-(1-p)^(1/4); see HANK_PREREG_v0.1
           Nb=4, k_min=0.005, k_tax=0.05, tunnel=0.0153,
           Tbar=[1.80, 2.05, 2.30], T_gate=1.0, p_up=0.159, omega=[0.102, 0.040, 0.021], s_scar=0.069, m_scar=0.6,
           Tr_low=0.0, dT_low=0.0, S=1.0, pi_low=0.25, G_time=0.0, htm_cut=0.15, naive=1,
           pb_tax=0.0, sparse_tax=0.0, a_default=5.6)
CONTROL = dict(k_tax=0.0, tunnel=0.0)


def control_ss(cal=CAL, verbose=False):
    """Calibrate beta, vphi in the control economy at r = rstar, Y = N = 1."""
    c = dict(cal, **CONTROL)
    ss = model_ss.solve_steady_state(c, unknowns={'beta': 0.986, 'vphi': 0.8},
                                     targets={'asset_mkt': 0.0, 'wnkpc_res': 0.0},
                                     solver='broyden_custom', verbose=verbose, ttol=1e-6)
    return model.steady_state(ss)


def ge_ss(cal, beta, vphi, guess=(0.005, 1.0), verbose=False):
    """General-equilibrium steady state for any calibration at the control's beta, vphi:
    (rstar, Y) adjust so that the asset market and the wage NKPC clear. Broyden first; if it fails
    (it can step past r = 1/beta - 1, where asset demand explodes), a bounded least-squares solve."""
    c = dict(cal, beta=beta, vphi=vphi)
    try:
        ss = model_ss.solve_steady_state(c, unknowns={'rstar': guess[0], 'Y': guess[1]},
                                         targets={'asset_mkt': 0.0, 'wnkpc_res': 0.0},
                                         solver='broyden_custom', verbose=verbose, ttol=1e-6)
        return model.steady_state(ss)
    except Exception:
        return ge_ss_bounded(c, guess)


def ge_ss_bounded(c, guess=(0.005, 1.0)):
    from scipy.optimize import least_squares
    rmax = 1.0 / c['beta'] - 1.0 - 2e-4

    def resid(x):
        try:
            ss = model_ss.steady_state(dict(c, rstar=float(x[0]), Y=float(x[1])))
            return np.array([ss['asset_mkt'] / c['B'], ss['wnkpc_res']])
        except Exception:
            return np.array([10.0, 10.0])
    x0 = [min(max(guess[0], -0.015), rmax - 1e-4), min(max(guess[1], 0.6), 1.8)]
    best = None
    for start in (x0, [0.5 * rmax, 1.0]):
        sol = least_squares(resid, x0=start, bounds=([-0.02, 0.5], [rmax, 2.0]), xtol=1e-12, ftol=1e-14, gtol=1e-14,
                            diff_step=1e-4, max_nfev=30)
        if best is None or sol.cost < best.cost:
            best = sol
        if np.max(np.abs(sol.fun)) < 2e-6:
            break
    if np.max(np.abs(best.fun)) > 2e-5:
        raise ValueError(f"bounded GE solve did not clear markets (max residual {np.max(np.abs(best.fun)):.2e})")
    return model.steady_state(model_ss.steady_state(dict(c, rstar=float(best.x[0]), Y=float(best.x[1]))))


def pe_ss(cal, beta, vphi):
    """Partial-equilibrium steady state: prices at the control's values, markets not required to clear."""
    c = dict(cal, beta=beta, vphi=vphi)
    return model_ss.steady_state(c)


if __name__ == '__main__':
    import time
    t0 = time.time()
    ssc = control_ss(verbose=True)
    print(f"control: beta={ssc['beta']:.5f} vphi={ssc['vphi']:.4f} r={ssc['r']:.4f} Y={ssc['Y']:.4f} "
          f"A={ssc['A']:.3f} C={ssc['C']:.4f} HTM={ssc['HTM']:.3f} BW={ssc['BW']:.3f} [{time.time()-t0:.0f}s]")
    t0 = time.time()
    ssm = ge_ss(CAL, ssc['beta'], ssc['vphi'], verbose=True)
    print(f"model GE: r={ssm['r']:.4f} Y={ssm['Y']:.4f} N={ssm['N']:.4f} w={ssm['w']:.4f} A={ssm['A']:.3f} "
          f"C={ssm['C']:.4f} HTM={ssm['HTM']:.3f} BW={ssm['BW']:.3f} SCARCE={ssm['SCARCE']:.3f} [{time.time()-t0:.0f}s]")
