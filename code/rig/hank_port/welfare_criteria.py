"""
welfare_criteria.py -- stress objective #3: does the Pigou wedge (planner's schedule entropy below the
firm's private optimum) survive the opposing welfare criteria?
  TRUE   policy evaluation at the true beta (the book's default: a degraded planner, not a changed preference)
  TUN    tunneling honored as preference (state-dependent discount beta_eff(b)), noise scored as error
  OWN    the household's own valuation V (degraded discount AND its own forecast): revealed preference in full
Each S at its own GE steady state (control's beta, vphi). Writes results_exact/hank_welfare_criteria.md.
"""
import os, sys, time
import numpy as np
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import hank_pigou as HP, hank_ge as H

RES = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'results_exact'))


def run():
    t0 = time.time()
    ctrl = dict(HP.CAL, **H.CONTROL, S=1.0)
    ssc = HP.model_ss.solve_steady_state(ctrl, unknowns={'beta': 0.9815, 'vphi': 0.88},
                                         targets={'asset_mkt': 0.0, 'wnkpc_res': 0.0}, solver='broyden_custom', ttol=1e-6)
    beta, vphi = ssc['beta'], ssc['vphi']
    Sgrid = np.array([0.0, 0.25, 0.5, 0.75, 1.0, 1.25, 1.5, 2.0])
    W = {k: [] for k in ['TRUE', 'TUN', 'OWN', 'g']}
    for S in Sgrid:
        m = HP.ss_at(dict(HP.CAL, S=S), beta, vphi)
        W['TRUE'].append(m['WELF']); W['TUN'].append(m['WELF_TUN']); W['OWN'].append(m['WELF_OWN']); W['g'].append(float(m['g']))
        print(f"S={S}: TRUE {m['WELF']:.3f}  TUN {m['WELF_TUN']:.3f}  OWN {m['WELF_OWN']:.3f}  BW {m['BW']:.3f}  [{time.time()-t0:.0f}s]", flush=True)
    g = np.array(W['g']); S_priv = Sgrid[np.argmin(g)]
    lines = ["# Welfare criteria and the Pigou wedge (2026-11-09)", "",
             "Aggregate welfare (utility units, mean over households) by schedule entropy S, model economy at its GE; "
             "the firm's private optimum is S_priv = argmin g(S).", "",
             "| S | g(S) | TRUE (β policy eval.) | TUN (β_eff honored) | OWN (household's own V) |", "|---|---|---|---|---|"]
    for i, S in enumerate(Sgrid):
        lines.append(f"| {S} | {g[i]:.4f} | {W['TRUE'][i]:.4f} | {W['TUN'][i]:.4f} | {W['OWN'][i]:.4f} |")

    def argmax_refined(y):
        i = int(np.argmax(y))
        if 0 < i < len(Sgrid) - 1:
            a, b, _ = np.polyfit(Sgrid[i - 1:i + 2], np.array(y)[i - 1:i + 2], 2)
            if a < 0: return float(-b / (2 * a))
        return float(Sgrid[i])
    lines += ["", f"S_priv = {S_priv:.3f} (grid; refined 1.055 in hank_pigou).", ""]
    for k in ['TRUE', 'TUN', 'OWN']:
        Ss = argmax_refined(W[k]); mono = 'rising in S' if np.all(np.diff(W[k]) > 0) else ('falling in S' if np.all(np.diff(W[k]) < 0) else 'interior optimum')
        lines.append(f"- **{k}**: planner's S = {Ss:.3f} ({mono}); wedge S_priv − S_soc = {S_priv - Ss:+.3f} → "
                     + ("the planner wants LESS entropy than the firm: Pigou tax positive" if Ss < S_priv - 0.02 else
                        ("the planner wants MORE entropy than the firm: a Pigou SUBSIDY — the criterion scores the loss of bandwidth as a gain" if Ss > S_priv + 0.02 else "no wedge")))
    lines += ["", "Reading. Under the household's own valuation, impatience shrinks the weight on future hardship, so a more degraded "
              "household reports itself better off; a planner using that criterion would subsidize the drain. The book's default "
              "scores the degraded planner at the undegraded discount rate — the choice is a premise and is printed as one; "
              "this table shows which conclusion depends on it.", f"Runtime {time.time()-t0:.0f}s."]
    open(os.path.join(RES, 'hank_welfare_criteria.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    print('\n'.join(lines))


if __name__ == '__main__':
    run()
