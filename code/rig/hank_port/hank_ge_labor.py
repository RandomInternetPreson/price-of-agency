"""
hank_ge_labor.py -- HANK v0.2 host for the labor-margin block (bw_hank_labor.BandwidthHHLabor):
sticky prices, FLEXIBLE wage clearing efficiency hours, Taylor rule, bonds fixed, lump-sum tax by skill.
Control: beta and the hours-disutility scale phi_h calibrated so that A = B and efficiency hours = 1.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sequence_jacobian import simple, create_model
import hank_ge as H
from bw_hank_labor import BandwidthHHLabor

hh = BandwidthHHLabor()


@simple
def labor_mkt(HEFF, N):
    labor_mkt = HEFF - N
    return labor_mkt


BLOCKS = [hh, H.firm, H.monetary, H.fiscal, H.mkt_clearing, H.nkpc, labor_mkt]
model = create_model(BLOCKS, name='HANK v0.2 (own hours, flexible wage)')
model_ss = create_model([hh, H.firm, H.monetary, H.fiscal, H.mkt_clearing, H.nkpc_ss, labor_mkt], name='SS v0.2')
UNKNOWNS = ['Y', 'w', 'pi']; TARGETS = ['asset_mkt', 'labor_mkt', 'nkpc_res']
CAL = dict(H.CAL, h_grid=[0.75, 1.0, 1.25], phi_h=1.0, nu=0.5)
CONTROL = H.CONTROL


def control_ss(cal=CAL):
    c = dict(cal, **CONTROL)
    ss = model_ss.solve_steady_state(c, unknowns={'beta': 0.98, 'phi_h': 1.0}, targets={'asset_mkt': 0.0, 'labor_mkt': 0.0},
                                     solver='broyden_custom', ttol=1e-6)
    return model.steady_state(ss)


def ge_ss(cal, beta, phi_h, guess=(0.005, 1.0)):
    c = dict(cal, beta=beta, phi_h=phi_h)
    ss = model_ss.solve_steady_state(c, unknowns={'rstar': guess[0], 'Y': guess[1]}, targets={'asset_mkt': 0.0, 'labor_mkt': 0.0},
                                     solver='broyden_custom', ttol=1e-6)
    return model.steady_state(ss)


def pe_ss(cal, beta, phi_h):
    return model_ss.steady_state(dict(cal, beta=beta, phi_h=phi_h))


def group_stats(ss):
    D = ss.internals['hh_bwl']['D']; P = ss.internals['hh_bwl']['P']
    st = hh.setup({k: ss[k] for k in hh.inputs}); o = hh.per_state_outputs(st, P)
    out = {}
    for ie, tag in enumerate(['low', 'mid', 'high']):
        m = D[:, ie, :]; w = m.sum()
        for k in ['htm', 'bw', 'hours', 'below', 'c', 'a']:
            out[f'{k}_{tag}'] = float((m * o[k][:, ie, :]).sum() / w)
    for k in ['r', 'Y', 'N', 'w', 'A', 'C', 'HTM', 'BW', 'HOURS', 'BELOW', 'WELF']:
        out[k] = float(ss[k])
    return out


if __name__ == '__main__':
    import time
    t0 = time.time(); ssc = control_ss()
    g = group_stats(ssc)
    print(f"control: beta={ssc['beta']:.5f} phi_h={ssc['phi_h']:.4f} r={g['r']:.4f} Y={g['Y']:.4f} hours low/mid/high={g['hours_low']:.3f}/{g['hours_mid']:.3f}/{g['hours_high']:.3f} "
          f"below-gate low/mid/high={g['below_low']:.2f}/{g['below_mid']:.2f}/{g['below_high']:.2f} HTM={g['HTM']:.3f} [{time.time()-t0:.0f}s]")
    t0 = time.time(); ssm = ge_ss(CAL, ssc['beta'], ssc['phi_h']); g = group_stats(ssm)
    print(f"model GE: r={g['r']:.4f} Y={g['Y']:.4f} w={g['w']:.4f} hours={g['hours_low']:.3f}/{g['hours_mid']:.3f}/{g['hours_high']:.3f} "
          f"below={g['below_low']:.2f}/{g['below_mid']:.2f}/{g['below_high']:.2f} BW={g['bw_low']:.2f}/{g['bw_mid']:.2f}/{g['bw_high']:.2f} HTM={g['HTM']:.3f} [{time.time()-t0:.0f}s]")
