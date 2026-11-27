"""
ricardian.py -- stress objective #8(d), owed since the macro-objections run: RICARDIAN EQUIVALENCE in dynamics.

Question a referee asks of any heterogeneous-agent result: "your households are not Ricardian anyway; what does
bandwidth add?" Experiment: a lump-sum tax cut today paid for with government debt that is retired later.
A Ricardian household does not respond (the present value of its taxes is unchanged). Any consumption
response is a departure from Ricardian equivalence; the comparison is how far the CONTROL economy (standard
incomplete-markets households) departs and how far the MODEL economy (same households, bandwidth tax) departs.

Fiscal block with a debt path:  Tax_t = (1 + r_t) B_{t-1} - B_t + Tr_low*pi_low + G_time   (B fixed -> Tax = r B).
Shock: dB_t = b0 * rho^t  (debt up by b0 at t = 0, retired geometrically; b0 = 1% of annual output = 0.04).
Reported, control vs model: (i) the household block alone at fixed prices (the intertemporal marginal propensities
to consume out of the tax path); (ii) general equilibrium, linear; (iii) the same with slower repayment.
Writes results_exact/hank_ricardian.md.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from sequence_jacobian import simple, create_model
import hank_ge as H

RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results_exact'))
T = 200


@simple
def fiscal_debt(r, B, Tr_low, pi_low, G_time):
    Tax = (1 + r) * B(-1) - B + Tr_low * pi_low + G_time
    return Tax


model_debt = create_model([H.hh, H.firm, H.monetary, fiscal_debt, H.mkt_clearing, H.nkpc, H.union], name='HANK with a debt path')


def run():
    t0 = time.time()
    ssc = H.control_ss(); beta, vphi = ssc['beta'], ssc['vphi']
    ssm = H.ge_ss(H.CAL, beta, vphi)
    print(f"steady states [{time.time()-t0:.0f}s] control r={ssc['r']:.4f} model r={ssm['r']:.4f}", flush=True)
    out = ['Y', 'C', 'A', 'HTM', 'BW', 'r', 'pi', 'Tax']
    L = ["# Ricardian equivalence in the bandwidth HANK: a debt-financed tax cut, model vs control (2026-11-10)", "",
         "Debt rises by b0 = 0.04 (1% of annual output) at t = 0 and is retired at rate 1 − ρ per quarter; the tax cut at t = 0 is b0 and "
         "taxes are higher afterwards. A Ricardian household's consumption does not move. Linear responses from sequence-space Jacobians "
         f"(T = {T}); naive forecast; constants as in HANK v0.1.", ""]
    b0 = 0.04; res = {}
    for name, ss in [('control', ssc), ('model', ssm)]:
        t1 = time.time()
        ssd = model_debt.steady_state(dict(ss))
        assert abs(ssd['Tax'] - ss['Tax']) < 1e-9 and abs(ssd['asset_mkt']) < 1e-5, (ssd['Tax'], ss['Tax'], ssd['asset_mkt'])
        G = model_debt.solve_jacobian(ssd, unknowns=H.UNKNOWNS, targets=H.TARGETS, inputs=['B'], outputs=out, T=T)
        Jh = H.hh.jacobian(ssd, inputs=['Tax'], outputs=['C', 'A', 'HTM'], T=T)
        res[name] = (ssd, G, Jh)
        print(f"Jacobians {name} [{time.time()-t1:.0f}s]", flush=True)
    for rho, lab in [(0.8, 'fast repayment (ρ = 0.8: half retired in three quarters)'), (0.95, 'slow repayment (ρ = 0.95: half retired in fourteen quarters)'),
                     (0.99, 'very slow repayment (ρ = 0.99: half retired in seventeen years)')]:
        dB = b0 * rho ** np.arange(T)
        L += [f"## {lab}", "", "| economy | fixed prices: ΔC at impact / tax cut | first-year ΔC / tax cut | GE: ΔC at impact / tax cut | first-year ΔC / tax cut | "
              "first-year ΔY / tax cut | peak Δr (bp) | ΔHTM at impact |", "|---|---|---|---|---|---|---|---|"]
        vals = {}
        for name in ['control', 'model']:
            ssd, G, Jh = res[name]
            dBlag = np.concatenate([[0.0], dB[:-1]])
            dTax_pe = (1 + ssd['r']) * dBlag - dB                       # prices fixed
            dC_pe = Jh['C']['Tax'] @ dTax_pe
            dC = G['C']['B'] @ dB; dY = G['Y']['B'] @ dB; dr = G['r']['B'] @ dB; dH = G['HTM']['B'] @ dB
            vals[name] = (dC_pe[0] / b0, dC_pe[:4].sum() / b0, dC[0] / b0, dC[:4].sum() / b0, dY[:4].sum() / b0, 1e4 * dr[np.argmax(np.abs(dr))], dH[0])
            v = vals[name]
            L.append(f"| {name} | {v[0]:.3f} | {v[1]:.3f} | {v[2]:.3f} | {v[3]:.3f} | {v[4]:.3f} | {v[5]:+.1f} | {v[6]:+.4f} |")
        c, m = vals['control'], vals['model']
        L += ["", f"Model / control: fixed-price impact {m[0]/c[0]:.2f}, fixed-price first year {m[1]/c[1]:.2f}, GE impact {m[2]/c[2]:.2f}, "
              f"GE first year {m[3]/c[3]:.2f}, GE output first year {m[4]/c[4]:.2f}.", ""]
        print('\n'.join(L[-6:]), flush=True)
    # intertemporal MPCs out of a one-time transfer at t = 0 (column 0 of -J^{C,Tax}) and an ANNOUNCED one at t = 8
    L += ["## Intertemporal marginal propensities to consume (household block, fixed prices)", "",
          "| economy | out of a transfer today: spent in quarter 0 | within a year | within three years | out of a transfer announced for quarter 8: spent before it arrives |", "|---|---|---|---|---|"]
    for name in ['control', 'model']:
        J = -res[name][2]['C']['Tax']
        L.append(f"| {name} | {J[0,0]:.3f} | {J[:4,0].sum():.3f} | {J[:12,0].sum():.3f} | {J[:8,8].sum():.3f} |")
    L.append(f"\nRuntime {time.time()-t0:.0f}s.")
    open(os.path.join(RES, 'hank_ricardian.md'), 'w', encoding='utf-8').write('\n'.join(L) + '\n')
    print('\n'.join(L[-8:]), flush=True)


if __name__ == '__main__':
    run()
