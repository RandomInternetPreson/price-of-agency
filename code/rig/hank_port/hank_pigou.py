"""
hank_pigou.py -- the GE-closure argument as a model: schedule entropy S is a firm-side
choice with a private benefit (a lower labor-cost factor g(S)), a private cost, and an
UNPRICED cost that lands on households as bandwidth drain. Competition drives S to the
private optimum S_priv (min g); the planner's S_soc maximizes aggregate true-beta welfare
in GE; the Pigou tax tau* = -g'(S_soc) makes the private optimum coincide with S_soc.

Firm: labor-cost factor g(S) = 1 - eta_S (1 - e^{-S}) + nu_S S^2 / 2  (saving saturates; a
convex private cost of errors/turnover gives an interior private optimum), marginal cost
w (g + tau_S S)/Z, tax revenue tau_S S w N rebated lump-sum. With eta_S = nu_S = tau_S = 0
this is hank_ge exactly; the control economy has the same firm technology, so model minus
control isolates the externality.
"""
import os, sys
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sequence_jacobian import simple, create_model
import hank_ge as H
from bw_hank import BandwidthHH

hh = H.hh


def g_of_S(S, eta_S, nu_S):
    return 1 - eta_S * (1 - np.exp(-S)) + nu_S * S ** 2 / 2


def gprime(S, eta_S, nu_S):
    return -eta_S * np.exp(-S) + nu_S * S


@simple
def entropy_cost(S, eta_S, nu_S):
    g = 1 - eta_S * (1 - (-S).apply(np.exp)) + nu_S * S ** 2 / 2
    return g


@simple
def firm(Y, w, Z, pi, mu, kappa, S, g, tau_S):
    N = Y / Z
    Div = Y - w * N * (g + tau_S * S) - mu / (mu - 1) / (2 * kappa) * (1 + pi).apply(np.log) ** 2 * Y
    return N, Div


@simple
def nkpc_ss(Z, mu, g, tau_S, S):
    w = Z / (mu * (g + tau_S * S))
    return w


@simple
def fiscal(r, B, Tr_low, pi_low, G_time, tau_S, S, w, N):
    Tax = r * B + Tr_low * pi_low + G_time - tau_S * S * w * N
    return Tax


model_ss = create_model([hh, entropy_cost, firm, H.monetary, fiscal, H.mkt_clearing, nkpc_ss, H.union], name='SS-Pigou')
CAL = dict(H.CAL, eta_S=0.06, nu_S=0.02, tau_S=0.0)


def ss_at(cal, beta, vphi, unknowns=None, guess=(0.005, 1.0)):
    c = dict(cal, beta=beta, vphi=vphi)
    unknowns = unknowns or {'rstar': guess[0], 'Y': guess[1]}
    return model_ss.solve_steady_state(c, unknowns=unknowns, targets={'asset_mkt': 0.0, 'wnkpc_res': 0.0},
                                       solver='broyden_custom', ttol=1e-6)


def ce_welfare(ss):
    """Aggregate true-beta welfare in consumption-equivalent units: the constant consumption stream
    whose CRRA value equals mean WELF (eis = 0.5 -> u(c) = -1/c)."""
    eis = ss['eis']; beta = ss['beta']; W = ss['WELF']
    if abs(eis - 1) < 1e-12:
        return float(np.exp((1 - beta) * W))
    return float(((1 - beta) * W * (1 - 1 / eis)) ** (1 / (1 - 1 / eis)))


def run():
    import time
    t0 = time.time()
    lines = ["# HANK port v0.1 — the externality priced: private vs social schedule entropy, Pigou tax (2026-11-09)", "",
             "Firm labor-cost factor g(S) = 1 − η(1 − e^{−S}) + νS²/2 with η = 0.06, ν = 0.02: the private optimum "
             "(min g) is S_priv = 1.0 by construction. Welfare: aggregate true-β value in consumption equivalents, "
             "each S at its own GE steady state (r, Y clear) at the control's β, vphi. Control economy: same firm, "
             "bandwidth channel off.", ""]
    # calibrate control at S = S_priv = 1
    ctrl = dict(CAL, **H.CONTROL, S=1.0)
    ssc = model_ss.solve_steady_state(ctrl, unknowns={'beta': 0.9815, 'vphi': 0.88},
                                      targets={'asset_mkt': 0.0, 'wnkpc_res': 0.0}, solver='broyden_custom', ttol=1e-6)
    beta, vphi = ssc['beta'], ssc['vphi']
    Sgrid = np.array([0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0])
    rows = []
    lines += ["| S | g(S) | control: r, Y, CE-welfare | model: r, Y, BW, HTM_low, CE-welfare | model − control CE |", "|---|---|---|---|---|"]
    for S in Sgrid:
        c = ss_at(dict(ctrl, S=S), beta, vphi); m = ss_at(dict(CAL, S=S), beta, vphi)
        cec, cem = ce_welfare(c), ce_welfare(m)
        D = m.internals['hh_bw']['D']; P = m.internals['hh_bw']['P']
        st = hh.setup({k: m[k] for k in hh.inputs}); o = hh.per_state_outputs(st, P)
        htm_low = float((D[:, 0, :] * o['htm'][:, 0, :]).sum() / D[:, 0, :].sum())
        rows.append((S, float(c['g']), c['r'], c['Y'], cec, m['r'], m['Y'], m['BW'], htm_low, cem))
        lines.append(f"| {S} | {c['g']:.4f} | {c['r']:.4f}, {c['Y']:.4f}, {cec:.5f} | {m['r']:.4f}, {m['Y']:.4f}, {m['BW']:.3f}, {htm_low:.3f}, {cem:.5f} | {cem-cec:+.5f} |")
        print(lines[-1], flush=True)
    R = np.array(rows)
    # private optimum: argmin g; social optimum: argmax model CE welfare (quadratic interpolation around the grid max)
    i_priv = int(np.argmin(R[:, 1])); i_soc = int(np.argmax(R[:, 9])); i_soc_c = int(np.argmax(R[:, 4]))

    def refine(i, col, sign):
        if 0 < i < len(Sgrid) - 1:
            x = Sgrid[i - 1:i + 2]; y = sign * R[i - 1:i + 2, col]
            a, b, _ = np.polyfit(x, y, 2)
            return float(-b / (2 * a)) if a < 0 else float(Sgrid[i])
        return float(Sgrid[i])
    S_priv = refine(i_priv, 1, -1.0); S_soc = refine(i_soc, 9, 1.0); S_soc_c = refine(i_soc_c, 4, 1.0)
    tau = -gprime(S_soc, CAL['eta_S'], CAL['nu_S'])
    lines += ["", f"S_priv (firm's private optimum, min g) = {S_priv:.3f}; S_soc (model planner, max CE welfare) = {S_soc:.3f}; "
              f"control planner = {S_soc_c:.3f} (the control's planner and firm agree up to the grid: no externality there).",
              f"Pigou tax τ* = −g'(S_soc) = {tau:.4f} per unit of S per unit of the wage bill: with it the firm's private FOC "
              f"g'(S) + τ* = 0 holds at S_soc.", ""]
    # verify: with tau*, the private optimum of g + tau S is S_soc, and the GE at (S_soc, tau*) is the planner's
    m_tax = ss_at(dict(CAL, S=S_soc, tau_S=tau), beta, vphi)
    lines.append(f"GE at (S_soc, τ*), revenue rebated: r = {m_tax['r']:.4f}, Y = {m_tax['Y']:.4f}, BW = {m_tax['BW']:.3f}, "
                 f"CE welfare = {ce_welfare(m_tax):.5f} (vs {R[i_soc, 9]:.5f} at the grid optimum without the tax: the rebate is "
                 f"lump-sum, so the difference is the incidence of the rebate, not the allocation).")
    lines.append(f"Runtime {time.time()-t0:.0f}s.")
    out = os.path.join(H.__file__.rsplit('/hank_port/', 1)[0], 'results_exact', 'hank_pigou_RESULTS.md')
    open(out, 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    ax[0].plot(Sgrid, R[:, 1], 'o-'); ax[0].set_title("firm's labor-cost factor g(S)"); ax[0].set_xlabel('S'); ax[0].axvline(S_priv, ls='--', c='gray')
    ax[1].plot(Sgrid, R[:, 4] - R[i_soc_c, 4], 's-', label='control'); ax[1].plot(Sgrid, R[:, 9] - R[i_soc_c, 9], 'o-', label='model')
    ax[1].axvline(S_priv, ls='--', c='gray', label='S_priv'); ax[1].axvline(S_soc, ls=':', c='k', label='S_soc (model)')
    ax[1].set_title('CE welfare (rel. to control max)'); ax[1].set_xlabel('S'); ax[1].legend(fontsize=8)
    plt.tight_layout(); plt.savefig(os.path.join(H.__file__.rsplit('/code/', 1)[0], 'figures', 'hank_pigou.png'), dpi=130)
    print('\n'.join(lines[-6:]))


if __name__ == '__main__':
    run()
