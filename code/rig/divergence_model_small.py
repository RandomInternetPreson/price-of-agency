"""
divergence_model_small.py -- the SMALL divergence model (MACRO_STEELMAN §3), built
before anything large. CPU, numpy only, ~1 minute.

WHAT IT IS. A HANK-adjacent household block in which the quality of the household's
own optimization is an endogenous, depletable state ("bandwidth" b), fed by time
floors (gated, per T5/T16: zero-then-jump) and taxed by schedule entropy and by
scarcity itself. Everything else is standard: assets on a grid, a two-state Markov
income, a borrowing limit, log utility, a stationary distribution found by iterating
the Fokker-Planck (transition) operator on the solved policy.

THE ONE NEW INGREDIENT, stated precisely (G1 of the steelman): the optimizer itself is
degraded by low bandwidth, in two faces that the scarcity literature describes and
that we keep as SEPARATE knobs so the reader can see which face carries which result:
  noise      the household picks next-period assets a' by a quantal (logit) response to
             its own continuation values, temperature kappa(b):
             P(a' | a, y, b) propto exp( Q(a'; a, y, b) / kappa(b) ),  kappa(b) = k_min + k_tax*(1 - b/(N_b-1))
  tunneling  the household's effective horizon shortens: beta_eff(b) = beta*(1 - tunnel*(1 - b/(N_b-1)))
             (Mullainathan-Shafir "tunneling": the future falls out of the frame; a degraded
             planner, not a changed preference -- the household's welfare is still scored at beta)
The CONTROL model is the same economy with k_tax = 0 and tunnel = 0: the bandwidth channel
is switched off and the model nests the standard block. The divergence is model-minus-
control, so no claim rides on the level of anything.

BANDWIDTH DYNAMICS (all parameters, none asserted of the world):
  time floor  T(y):   b rises by 1 w.p. p_up ONLY if T(y) >= T_gate   (the gate)
  entropy tax s(y):   b falls by 1 w.p. s(y)                            (schedule entropy)
  scarcity tax:       b falls by 1 w.p. s_scar if cash-on-hand < m_scar  (Mani et al. channel)
Low-income households get the lower time floor and the higher entropy by default.

THE THREE PREDICTIONS (steelman §3), each run model-vs-control:
  P-A  returns to a small TIME transfer concentrate at the bottom of the wealth
       distribution beyond what a MONEY transfer's profile shows;
  P-B  a schedule-stability policy (lower s(y_L)) beats an equal-dollar wage transfer
       on downstream outcomes (assets, hand-to-mouth share) for time-poor households;
  P-C  hand-to-mouth behavior persists after liquidity is repaired if bandwidth is not.
Each prints a table and the script writes figures/divergence_small_*.png.
A dose-response sweep over k_tax shows the divergence vanishing as the channel closes.

Usage: python divergence_model_small.py [--quick]
"""
import argparse, os, time
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

HERE = os.path.dirname(os.path.abspath(__file__))
FIGDIR = os.path.normpath(os.path.join(HERE, '..', '..', 'figures'))


class Params:
    def __init__(self, **kw):
        # economy
        self.beta = 0.96; self.r = 0.03; self.Na = 60; self.a_min = 0.0; self.a_max = 15.0
        self.y = np.array([0.5, 1.5]); self.Py = np.array([[0.9, 0.1], [0.1, 0.9]])
        self.c_min = 0.05
        # bandwidth
        self.Nb = 4; self.k_min = 0.02; self.k_tax = 0.30; self.tunnel = 0.06
        self.T = np.array([0.8, 1.6]); self.T_gate = 1.0; self.p_up = 0.5      # time floors by income; the gate
        self.s = np.array([0.35, 0.08]); self.s_scar = 0.25; self.m_scar = 0.9   # entropy taxes; scarcity tax
        # policy knobs (set by experiments)
        self.transfer = np.array([0.0, 0.0]); self.a_borrow = 0.0
        for k, v in kw.items():
            setattr(self, k, np.array(v) if isinstance(getattr(self, k), np.ndarray) else v)


class Model:
    def __init__(self, p):
        self.p = p
        self.a = np.linspace(-p.a_borrow, p.a_max, p.Na)
        self.b = np.arange(p.Nb)
        self.kappa = p.k_min + p.k_tax * (1 - self.b / (p.Nb - 1))          # (Nb,)
        self.beta_eff = p.beta * (1 - p.tunnel * (1 - self.b / (p.Nb - 1)))   # (Nb,)
        # bandwidth transition Pb[y, scarce, b, b']
        Nb = p.Nb
        self.Pb = np.zeros((2, 2, Nb, Nb))
        for yi in range(2):
            up = p.p_up if p.T[yi] >= p.T_gate else 0.0
            for sc in range(2):
                down = 1 - (1 - p.s[yi]) * (1 - (p.s_scar if sc else 0.0))
                for bi in range(Nb):
                    pu = up if bi < Nb - 1 else 0.0
                    pd = down if bi > 0 else 0.0
                    # up and down can both fire; net move
                    self.Pb[yi, sc, bi, bi] += (1 - pu) * (1 - pd) + pu * pd
                    if bi < Nb - 1: self.Pb[yi, sc, bi, bi + 1] += pu * (1 - pd)
                    if bi > 0: self.Pb[yi, sc, bi, bi - 1] += pd * (1 - pu)
        # cash on hand m[a, y]; consumption for each a': c[a, y, a']
        self.m = (1 + p.r) * self.a[:, None] + p.y[None, :] + p.transfer[None, :]
        c = self.m[:, :, None] - self.a[None, None, :]
        self.feasible = c >= p.c_min
        self.u = np.where(self.feasible, np.log(np.maximum(c, p.c_min)), -1e9)   # (a, y, a')
        self.scarce = (self.m < p.m_scar).astype(int)                             # (a, y)

    def solve(self, tol=1e-7, maxit=3000):
        p = self.p; Na, Nb = p.Na, p.Nb
        V = np.zeros((Na, 2, Nb))
        for it in range(maxit):
            # EV[a', y, b] = sum_{y', b'} Py[y,y'] Pb[y, scarce(a,y)?..] -- b' depends on current (y, scarcity of current state)
            # continuation: next bandwidth drawn from current (y, scarce) state
            EVy = np.einsum('yz,azc->ayc', p.Py, V)                              # (a', y, b')  expectation over y'
            Q = np.empty((Na, 2, Nb, Na))                                        # (a, y, b, a')
            for yi in range(2):
                for sc in range(2):
                    # E over b' given current b: Pb[yi, sc, b, b'] . EVy[a', yi, b']
                    cont = np.einsum('bc,ac->ab', self.Pb[yi, sc], EVy[:, yi, :])   # (a', b)
                    mask = self.scarce[:, yi] == sc
                    Q[mask, yi, :, :] = self.u[mask, yi, None, :] + self.beta_eff[None, :, None] * cont.T[None, :, :]
            # logit policy at temperature kappa(b)
            z = Q / self.kappa[None, None, :, None]
            z = z - z.max(-1, keepdims=True)
            P = np.exp(z) * self.feasible[:, :, None, :]
            P /= P.sum(-1, keepdims=True)
            Vn = (P * Q).sum(-1)
            if np.max(np.abs(Vn - V)) < tol:
                V = Vn; break
            V = Vn
        self.V, self.P = V, P
        return self

    def stationary(self, tol=1e-10, maxit=20000):
        p = self.p; Na, Nb = p.Na, p.Nb
        mu = np.full((Na, 2, Nb), 1.0 / (Na * 2 * Nb))
        for it in range(maxit):
            nxt = np.zeros_like(mu)
            for yi in range(2):
                for sc in range(2):
                    mask = self.scarce[:, yi] == sc
                    flow = mu[mask, yi, :]                                          # (a_sub, b)
                    # a' distribution: P[a, yi, b, a'] ; b' via Pb ; y' via Py
                    w = self.P[mask, yi, :, :] * flow[:, :, None]                 # (a_sub, b, a')
                    wb = np.einsum('abc,bd->cd', w, self.Pb[yi, sc])              # (a', b')
                    nxt += wb[:, None, :] * p.Py[yi][None, :, None]
            if np.max(np.abs(nxt - mu)) < tol:
                mu = nxt; break
            mu = nxt
        self.mu = mu
        return self

    # ---- moments -----------------------------------------------------------
    def moments(self):
        p = self.p; mu = self.mu
        wa = mu.sum((1, 2)); mean_a = float((wa * self.a).sum())
        # hand-to-mouth: next assets <= half a period's low income
        anext = np.einsum('aybc,c->ayb', self.P, self.a)
        htm = float((mu * (anext <= 0.5 * p.y[0])).sum())
        low = mu[:, 0, :].sum(); htm_low = float((mu[:, 0, :] * (anext[:, 0, :] <= 0.5 * p.y[0])).sum() / low)
        mean_b = float((mu.sum((0, 1)) * self.b).sum())
        mean_b_low = float((mu[:, 0, :].sum(0) * self.b).sum() / low)
        # expected consumption and a welfare proxy: mean log c
        c = self.m[:, :, None] - self.a[None, None, :]
        Elogc = float((mu * (self.P * np.log(np.maximum(c, p.c_min))[:, :, None, :]).sum(-1)).sum())
        return dict(mean_assets=mean_a, htm=htm, htm_low=htm_low, mean_b=mean_b, mean_b_low=mean_b_low, Elogc=Elogc,
                    median_assets_low=self._quantile(mu[:, 0, :].sum(1) / low, 0.5))

    def _quantile(self, w, q):
        cw = np.cumsum(w); return float(self.a[np.searchsorted(cw, q * cw[-1])])

    def by_wealth_quintile(self, fn):
        """mean of per-state quantity fn[a,y,b] within wealth quintiles of the stationary distribution."""
        mu = self.mu; wa = mu.sum((1, 2)); cw = np.cumsum(wa) / wa.sum()
        out = []
        for lo, hi in zip([0, .2, .4, .6, .8], [.2, .4, .6, .8, 1.0001]):
            sel = (cw > lo) & (cw <= hi)
            if sel.sum() == 0:
                sel = np.zeros_like(sel); sel[np.searchsorted(cw, lo)] = True
            w = mu[sel]; out.append(float((w * fn[sel]).sum() / w.sum()))
        return np.array(out)


def run(p):
    return Model(p).solve().stationary()


def model_and_control(base_kw, faces=False):
    kt, tu = base_kw.get('k_tax', 0.30), base_kw.get('tunnel', 0.06)
    out = [('bandwidth model (noise + tunneling)', dict(base_kw, k_tax=kt, tunnel=tu))]
    if faces:
        out += [('noise face only', dict(base_kw, k_tax=kt, tunnel=0.0)), ('tunneling face only', dict(base_kw, k_tax=0.0, tunnel=tu))]
    out.append(('control (both off)', dict(base_kw, k_tax=0.0, tunnel=0.0)))
    return out


def exp_PA(base_kw, control, log):
    """P-A: small time transfer vs small money transfer; effect on next-period savings by wealth quintile."""
    rows = {}
    for name, kw in model_and_control(base_kw):
        m0 = run(Params(**kw))
        anext0 = np.einsum('aybc,c->ayb', m0.P, m0.a)
        # time transfer: lift the low-income time floor over the gate
        m_t = run(Params(**dict(kw, T=[1.05, 1.6])))
        # money transfer: per-period cash to low income, sized to 5% of low income
        m_m = run(Params(**dict(kw, transfer=[0.03, 0.0])))
        d_time = m0.by_wealth_quintile(np.einsum('aybc,c->ayb', m_t.P, m_t.a) - anext0)
        lowmask = np.zeros_like(anext0); lowmask[:, 0, :] = 1
        d_money = m0.by_wealth_quintile(np.einsum('aybc,c->ayb', m_m.P, m_m.a) - anext0 - 0.03 * lowmask)
        rows[name] = (d_time, d_money, m0.moments(), m_t.moments(), m_m.moments())
    log("\n## P-A  small time transfer vs small money transfer — change in next-period savings by wealth quintile")
    log("(money effect net of the transfer itself; both models share every parameter except k_tax)")
    log("| model | transfer | Q1 (poorest) | Q2 | Q3 | Q4 | Q5 | bottom-share of total effect |")
    log("|---|---|---|---|---|---|---|---|")
    for name, (dt, dm, *_rest) in rows.items():
        for lab, d in [('time (+floor over gate)', dt), ('money (+5% of low income)', dm)]:
            tot = np.abs(d).sum() + 1e-12
            log(f"| {name} | {lab} | " + " | ".join(f"{x:+.4f}" for x in d) + f" | {abs(d[0]) / tot:.2f} |")
    bm, cm = rows['bandwidth model (noise + tunneling)'], rows['control (both off)']
    log(f"\nHtM share (low income): base {bm[2]['htm_low']:.3f} -> time {bm[3]['htm_low']:.3f} / money {bm[4]['htm_low']:.3f}  [bandwidth model];  "
        f"base {cm[2]['htm_low']:.3f} -> time {cm[3]['htm_low']:.3f} / money {cm[4]['htm_low']:.3f}  [control]")
    log("Reading: in the control the time transfer does NOTHING (time is not a state there); in the bandwidth model it "
        "acts through the gate and concentrates where bandwidth is lowest. P-A holds in this world if the time row's "
        "bottom-share exceeds the money row's. A model constant, not a world constant.")
    return rows


def exp_PB(base_kw, log):
    """P-B: schedule stability vs equal-dollar wage transfer for the low-income group."""
    log("\n## P-B  schedule-stability policy vs equal-dollar wage transfer (low-income households)")
    log("Stability = entropy tax s(y_L) cut from 0.35 to 0.15; priced at `cost` per period, paid as the wage transfer in the comparison arm.")
    log("| model | cost | arm | median assets (low y) | HtM share (low y) | mean bandwidth (low y) | E[log c] |")
    log("|---|---|---|---|---|---|---|")
    out = {}
    for name, kw in model_and_control(base_kw):
        base = run(Params(**kw)).moments()
        log(f"| {name} | — | baseline | {base['median_assets_low']:.3f} | {base['htm_low']:.3f} | {base['mean_b_low']:.2f} | {base['Elogc']:.4f} |")
        for cost in [0.02, 0.05, 0.10]:
            st = run(Params(**dict(kw, s=[0.15, 0.08]))).moments()
            wg = run(Params(**dict(kw, transfer=[cost, 0.0]))).moments()
            log(f"| {name} | {cost:.2f} | stability | {st['median_assets_low']:.3f} | {st['htm_low']:.3f} | {st['mean_b_low']:.2f} | {st['Elogc']:.4f} |")
            log(f"| {name} | {cost:.2f} | wage +{cost:.2f} | {wg['median_assets_low']:.3f} | {wg['htm_low']:.3f} | {wg['mean_b_low']:.2f} | {wg['Elogc']:.4f} |")
            out[(name, cost)] = (st, wg)
    log("Reading: find the cost at which the wage arm first matches the stability arm on HtM share -- that is the model's "
        "shadow price of schedule stability in wage units. In the control it is zero by construction (stability is not a state). "
        "Mas & Pallais 2017 measured an experimental WTP (~20% of wage) for avoiding employer-set schedules; the model's shadow "
        "price is the quantity a field audit would compare to it. Not a prediction of that number.")
    return out


def exp_PC(base_kw, log):
    """P-C: liquidity repair with and without bandwidth repair."""
    log("\n## P-C  liquidity repaired, bandwidth not: does hand-to-mouth persist?")
    log("Liquidity repair = borrowing limit opened to 1.0 (from 0) AND the scarcity tax removed (m_scar = 0). Bandwidth repair = low-income time floor lifted over the gate.")
    log("| model | arm | HtM share (low y) | HtM share (all) | mean bandwidth (low y) | median assets (low y) |")
    log("|---|---|---|---|---|---|")
    res = {}
    for name, kw in model_and_control(base_kw, faces=True):
        arms = [('baseline', {}), ('liquidity repaired', dict(a_borrow=1.0, m_scar=0.0)),
                ('bandwidth repaired', dict(T=[1.05, 1.6])), ('both repaired', dict(a_borrow=1.0, m_scar=0.0, T=[1.05, 1.6]))]
        for lab, ch in arms:
            mo = run(Params(**dict(kw, **ch))).moments()
            res[(name, lab)] = mo
            log(f"| {name} | {lab} | {mo['htm_low']:.3f} | {mo['htm']:.3f} | {mo['mean_b_low']:.2f} | {mo['median_assets_low']:.3f} |")
    log("Reading: P-C holds in this world if, in the bandwidth model, 'liquidity repaired' leaves HtM well above 'both repaired' "
        "while in the control the two coincide (there, liquidity is the whole story). The residual is the bandwidth share of "
        "hand-to-mouth -- the quantity the wealthy-HtM data (Kaplan-Violante-Weidner) could be asked about.")
    return res


def dose_response(base_kw, log, quick=False):
    log("\n## Dose-response: the divergence as the bandwidth channel closes (scale x multiplies k_tax=0.30 and tunnel=0.06; x=0 is the control)")
    log("| scale x | HtM (low y) | time-transfer effect on Q1 savings | money-transfer effect on Q1 savings (net) | P-C residual (liq. repaired − both) |")
    log("|---|---|---|---|---|")
    taxes = [0.0, 0.25, 0.5, 1.0, 1.5, 2.0] if not quick else [0.0, 0.5, 1.0]
    curve = []
    for kt in taxes:
        kw = dict(base_kw, k_tax=0.30 * kt, tunnel=0.06 * kt)
        m0 = run(Params(**kw)); an0 = np.einsum('aybc,c->ayb', m0.P, m0.a)
        mt = run(Params(**dict(kw, T=[1.05, 1.6]))); mm = run(Params(**dict(kw, transfer=[0.03, 0.0])))
        dt = m0.by_wealth_quintile(np.einsum('aybc,c->ayb', mt.P, mt.a) - an0)[0]
        lowmask = np.zeros_like(an0); lowmask[:, 0, :] = 1
        dm = m0.by_wealth_quintile(np.einsum('aybc,c->ayb', mm.P, mm.a) - an0 - 0.03 * lowmask)[0]
        liq = run(Params(**dict(kw, a_borrow=1.0, m_scar=0.0))).moments()['htm_low']
        both = run(Params(**dict(kw, a_borrow=1.0, m_scar=0.0, T=[1.05, 1.6]))).moments()['htm_low']
        curve.append((kt, m0.moments()['htm_low'], dt, dm, liq - both))
        log(f"| {kt:.2f} | {curve[-1][1]:.3f} | {dt:+.4f} | {dm:+.4f} | {liq - both:+.3f} |")
    return curve


def figure(curve, pa_rows):
    os.makedirs(FIGDIR, exist_ok=True)
    fig, axes = plt.subplots(1, 2, figsize=(11, 3.8))
    ax = axes[0]
    q = np.arange(1, 6)
    for (name, (dt, dm, *_)), ls in zip(pa_rows.items(), ['-', ':']):
        ax.plot(q, dt, color='#2a78d6', ls=ls, marker='o', ms=5, lw=2, label=f'time transfer, {name}')
        ax.plot(q, dm, color='#eb6834', ls=ls, marker='s', ms=5, lw=2, label=f'money transfer (net), {name}')
    ax.axhline(0, color='#888', lw=0.8); ax.set_xticks(q); ax.set_xticklabels(['Q1\npoorest', 'Q2', 'Q3', 'Q4', 'Q5'])
    ax.set_ylabel('Δ next-period savings'); ax.set_title('P-A: where a small transfer lands', fontsize=10); ax.grid(alpha=0.25)
    ax.legend(fontsize=7, frameon=False)
    ax = axes[1]
    kt = [c[0] for c in curve]
    ax.plot(kt, [c[2] for c in curve], color='#2a78d6', marker='o', lw=2, label='time-transfer effect on Q1 savings')
    ax.plot(kt, [c[4] for c in curve], color='#1baf7a', marker='^', lw=2, label='P-C residual HtM (liquidity − both repaired)')
    ax.set_xlabel('bandwidth-channel scale x (0 = control)'); ax.set_title('dose-response: divergence vs the bandwidth channel', fontsize=10)
    ax.grid(alpha=0.25); ax.legend(fontsize=7, frameon=False)
    fig.suptitle('Small divergence model (model world; parameters, not measurements)', fontsize=11)
    fig.tight_layout(rect=[0, 0, 1, 0.93])
    p = os.path.join(FIGDIR, 'divergence_small_v0.png'); fig.savefig(p, dpi=140); plt.close(fig)
    return p


if __name__ == "__main__":
    ap = argparse.ArgumentParser(); ap.add_argument('--quick', action='store_true'); args = ap.parse_args()
    base_kw = dict(Na=40 if args.quick else 60)
    lines = []

    def log(msg):
        print(msg, flush=True); lines.append(msg)
    t0 = time.time()
    log("# Small divergence model v0 — results (model world)")
    log(f"Grid: Na={base_kw['Na']}, Ny=2, Nb=4; beta=0.96, r=0.03, y=(0.5,1.5); noise k_min=0.02, k_tax=0.30; tunneling 0.06 (control: both 0); time floors T=(0.8, 1.6) vs gate 1.0; entropy taxes s=(0.35, 0.08); scarcity tax 0.25 below m=0.9.")
    pa = exp_PA(base_kw, True, log)
    exp_PB(base_kw, log)
    exp_PC(base_kw, log)
    curve = dose_response(base_kw, log, quick=args.quick)
    figp = figure(curve, pa)
    log(f"\nfigure: figures/{os.path.basename(figp)}   ({time.time() - t0:.0f}s)")
    outp = os.path.join(HERE, 'results_exact', 'divergence_small_RESULTS.md')
    os.makedirs(os.path.dirname(outp), exist_ok=True)
    open(outp, 'w', encoding='utf-8').write('\n'.join(lines)); print('wrote', outp)
