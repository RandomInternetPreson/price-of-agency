"""
bw_hank.py -- the book's bandwidth household block as a custom Block for the
Sequence-Space Jacobian toolkit (Auclert, Bardoczy, Rognlie, Straub 2021), so that it
can be dropped into a standard one-asset HANK with sticky prices and sticky wages and
solved in general equilibrium: steady state, sequence-space Jacobians (fake-news
algorithm on the block's own dense transition operator), and nonlinear transition paths.

WHAT THE BLOCK IS. Household state (b, e, a): bandwidth level b in {0..Nb-1}, skill e
(Rouwenhorst Markov), assets a on a grid. Each period the household receives
(1+r)a + w*e*N + T_e and chooses next-period assets a' on the grid. The quality of
its own optimization is the bandwidth state, in the two faces of the v0 model
(code/rig/divergence_model_small.py), kept as SEPARATE knobs:
  noise      quantal (logit) response at temperature kappa(b) = k_min + k_tax*(1 - b/(Nb-1))
  tunneling  effective discount factor beta_eff(b) = beta*(1 - tunnel*(1 - b/(Nb-1)))
Bandwidth moves by a Markov law driven by
  time floor  free time Tfree_e = Tbar_e - N (hours worked are the aggregate N of the
              canonical model); b rises w.p. p_up ONLY if Tfree_e >= T_gate   (the gate)
  entropy     b falls w.p. s_e = S * omega_e  (S = schedule entropy, a firm-side variable)
  scarcity    b falls w.p. s_scar additionally if cash-on-hand < m_scar.
CONTROL = same block with k_tax = 0 and tunnel = 0: bandwidth is then payoff-irrelevant
and the block is a canonical incomplete-markets household with a discretized savings
choice and a small logit smoothing k_min (it converges to the EGM household of the
toolkit as k_min -> 0 and the grid is refined; the check is printed by run_hank_v01.py).
Welfare is scored at the TRUE beta by policy evaluation (a degraded planner, not a
changed preference).
FORECAST (ruling of 2026-11-09, both kept as a switch `naive`): by default the household is
NAIVE about its own bandwidth -- it plans as if its current level were permanent, which is
what the scarcity literature describes (the tunnel is not perceived from inside); the true law
of motion acts on the distribution. The SOPHISTICATED variant (naive = 0) lets the household
forecast its own degradation, and then it saves to buffer against its own future noise, so
that repairing bandwidth LOWERS saving -- a precautionary-against-oneself effect that reverses
the sign of every repair experiment. Printed in hank_v01_RESULTS as the forecast comparison.

Outputs (aggregates): A (end-of-period assets), C, UCE (mean e*u'(c), for the wage
Phillips curve), HTM (mass choosing a' within htm_cut of the borrowing limit), BW (mean bandwidth / (Nb-1)),
SCARCE (mass below m_scar), WELF (mean true-beta value).
Inputs: r, w, N, Div, Tax, S and the parameters named in PARAMS below.

Nothing here is asserted of the world; every bandwidth parameter is a model constant.
"""
import numpy as np
from sequence_jacobian import grids
from sequence_jacobian.blocks.block import Block
from sequence_jacobian.classes import SteadyStateDict, ImpulseDict, JacobianDict
from sequence_jacobian.utilities.ordered_set import OrderedSet

PARAMS = ['beta', 'eis', 'rho_s', 'sigma_s', 'nS', 'amax', 'nA', 'nref', 'c_min',
          'Nb', 'k_min', 'k_tax', 'tunnel', 'Tbar', 'T_gate', 'p_up', 'omega', 's_scar', 'm_scar', 'htm_cut', 'naive',
          'pb_tax', 'sparse_tax', 'a_default']
AGG_INPUTS = ['r', 'w', 'N', 'Div', 'Tax', 'S', 'Tr_low', 'dT_low', 'a_borrow']


class BandwidthHH(Block):
    def __init__(self, name='hh_bw'):
        self.name = name
        self.inputs = OrderedSet(AGG_INPUTS + PARAMS)
        self.outputs = OrderedSet(['A', 'C', 'UCE', 'HTM', 'BW', 'SCARCE', 'WELF', 'WELF_OWN', 'WELF_TUN'])
        self.internals = OrderedSet(['D', 'V', 'P', 'a_grid', 'e_grid', 'b_grid'])
        super().__init__()

    # ------------------------------------------------------------------ primitives
    @staticmethod
    def grids(ss):
        e_grid, pi_e, Pi = grids.markov_rouwenhorst(rho=ss['rho_s'], sigma=ss['sigma_s'], N=int(ss['nS']))
        a_borrow = float(ss.get('a_borrow', 0.0))
        if a_borrow > 0:
            a_grid = grids.asset_grid(-a_borrow, ss['amax'], int(ss['nA']))
        else:
            a_grid = grids.agrid(amax=ss['amax'], n=int(ss['nA']))
        return e_grid, pi_e, Pi, a_grid

    @staticmethod
    def bandwidth_law(ss, e_grid, N, S):
        """Pb[e, scarce, b, b'] for current (e, scarcity flag, b)."""
        Nb = int(ss['Nb']); Ne = len(e_grid)
        Tbar = np.array(np.broadcast_to(np.asarray(ss['Tbar'], float), (Ne,)))
        Tbar[0] += float(ss.get('dT_low', 0.0))                    # time transfer to the lowest skill
        omega = np.broadcast_to(np.asarray(ss['omega'], float), (Ne,))
        Pb = np.zeros((Ne, 2, Nb, Nb))
        for ie in range(Ne):
            up = ss['p_up'] if (Tbar[ie] - N) >= ss['T_gate'] else 0.0
            s_e = min(1.0, S * omega[ie])
            for sc in range(2):
                down = 1 - (1 - s_e) * (1 - (ss['s_scar'] if sc else 0.0))
                for b in range(Nb):
                    pu = up if b < Nb - 1 else 0.0
                    pd = down if b > 0 else 0.0
                    Pb[ie, sc, b, b] += (1 - pu) * (1 - pd) + pu * pd
                    if b < Nb - 1: Pb[ie, sc, b, b + 1] += pu * (1 - pd)
                    if b > 0: Pb[ie, sc, b, b - 1] += pd * (1 - pu)
        return Pb

    def setup(self, ss, inputs=None):
        """Everything that depends on inputs but not on V: utilities, feasibility, laws of motion."""
        x = dict(ss)
        if inputs is not None:
            x.update(inputs)
        e_grid, pi_e, Pi, a_grid = self.grids(x)
        Nb = int(x['Nb']); Ne = len(e_grid); Na = len(a_grid)
        b_grid = np.arange(Nb)
        # choice grid: each state-grid interval subdivided nref times; lottery W (Nc x Na) maps a choice
        # onto the two bracketing state points (the toolkit's own device), so continuation values are
        # linearly interpolated and the savings choice is not forced onto the coarse state grid
        nref = int(x.get('nref', 1))
        a_c = np.concatenate([np.linspace(a_grid[i], a_grid[i + 1], nref, endpoint=False) for i in range(Na - 1)] + [a_grid[-1:]])
        Nc = len(a_c)
        idx = np.minimum(np.searchsorted(a_grid, a_c, side='right') - 1, Na - 2)
        wt_hi = (a_c - a_grid[idx]) / (a_grid[idx + 1] - a_grid[idx])
        W = np.zeros((Nc, Na))
        W[np.arange(Nc), idx] = 1 - wt_hi
        W[np.arange(Nc), idx + 1] += wt_hi
        kappa = x['k_min'] + x['k_tax'] * (1 - b_grid / max(Nb - 1, 1))
        beta_eff = x['beta'] * (1 - x['tunnel'] * (1 - b_grid / max(Nb - 1, 1)))
        # alternative faces (stress objective #5): present bias pb(b) multiplies the continuation in the CHOICE only
        # (naive quasi-hyperbolic: the household believes its future selves are exponential); sparse attention m(b)
        # shrinks the perceived asset state toward a default (Gabaix): a_perc = a_default + m (a - a_default)
        pb = 1 - float(x.get('pb_tax', 0.0)) * (1 - b_grid / max(Nb - 1, 1))
        attn = 1 - float(x.get('sparse_tax', 0.0)) * (1 - b_grid / max(Nb - 1, 1))
        # transfers: SSJ incidence rule, proportional to skill
        Tr = (x['Div'] - x['Tax']) / np.sum(pi_e * e_grid) * e_grid
        Tr = Tr.copy(); Tr[0] += float(x.get('Tr_low', 0.0))                    # money transfer to the lowest skill
        y = x['w'] * e_grid * x['N'] + Tr                                      # (Ne,)
        coh = (1 + x['r']) * a_grid[None, :] + y[:, None]                        # (Ne, Na)
        c = coh[:, :, None] - a_c[None, None, :]                                 # (Ne, Na, Nc)
        feas = c >= x['c_min']
        cc = np.maximum(c, x['c_min'])
        eis = x['eis']
        if abs(eis - 1.0) < 1e-12:
            u = np.log(cc)
        else:
            u = cc ** (1 - 1 / eis) / (1 - 1 / eis)
        u = np.where(feas, u, -1e9)
        uc = cc ** (-1 / eis)
        scarce = (coh < x['m_scar']).astype(int)                                 # (Ne, Na)
        Pb = self.bandwidth_law(x, e_grid, x['N'], x['S'])
        return dict(e_grid=e_grid, pi_e=pi_e, Pi=Pi, a_grid=a_grid, a_c=a_c, W=W, Nc=Nc, b_grid=b_grid, Nb=Nb, Ne=Ne, Na=Na,
                    kappa=kappa, beta_eff=beta_eff, beta=x['beta'], pb=pb, attn=attn, a_default=float(x.get('a_default', 0.0)),
                    y=y, coh=coh, c=cc, feas=feas, r=float(x['r']),
                    u=u, uc=uc, scarce=scarce, Pb=Pb, htm_cut=float(x.get('htm_cut', 0.0)),
                    naive=bool(int(x.get('naive', 1))))

    @staticmethod
    def bellman(st, V, act=True):
        """One backward step. V[b, e, a] -> (V_new, P[b, e, a, a'], Q). act=False skips the alternative-face
        action maps (present bias, sparse attention), which do not enter the value recursion."""
        Pi, Pb, u, feas, kappa, beta_eff, scarce = st['Pi'], st['Pb'], st['u'], st['feas'], st['kappa'], st['beta_eff'], st['scarce']
        Nb, Ne, Na, Nc, W = st['Nb'], st['Ne'], st['Na'], st['Nc'], st['W']
        # expectation over e' and lottery onto the choice grid: EVe[b', e, c] = sum_e' Pi[e,e'] sum_a' W[c,a'] V[b', e', a']
        EVe = np.einsum('ef,bfa->bea', Pi, V) @ W.T
        Q = np.empty((Nb, Ne, Na, Nc))
        for ie in range(Ne):
            if st['naive']:
                # naive forecast: the household plans as if its bandwidth level were permanent
                # (the tunnel is not perceived from inside); the true law of motion acts only on the distribution
                Q[:, ie, :, :] = u[ie][None, :, :] + beta_eff[:, None, None] * EVe[:, ie, None, :]
                continue
            for sc in range(2):
                mask = scarce[ie] == sc
                if not mask.any():
                    continue
                # sophisticated forecast: cont[b, a'] = sum_b' Pb[ie, sc, b, b'] EVe[b', ie, a']
                cont = Pb[ie, sc] @ EVe[:, ie, :]                                # (Nb, Nc)
                Q[:, ie, mask, :] = u[ie, mask, :][None, :, :] + beta_eff[:, None, None] * cont[:, None, :]
        z = Q / kappa[:, None, None, None]
        z = z - z.max(-1, keepdims=True)
        P = BandwidthHH.normalize(np.exp(z) * feas[None, :, :, :])
        Vn = (P * Q).sum(-1)
        pb = st['pb']
        if not act:
            return Vn, P, Q
        if np.any(pb < 1):
            # present bias: the chosen action discounts the continuation by pb(b) more; the value recursion
            # (what the household believes about its future selves) stays exponential
            Qp = u[None] + pb[:, None, None, None] * (Q - u[None])
            zp = Qp / kappa[:, None, None, None]; zp = zp - zp.max(-1, keepdims=True)
            P = BandwidthHH.normalize(np.exp(zp) * feas[None, :, :, :])
        if np.any(st['attn'] < 1):
            P = BandwidthHH.sparse_policy(st, P)
        return Vn, P, Q

    @staticmethod
    def normalize(P):
        """Row-normalize a choice kernel; a state with no feasible choice puts its mass on the lowest savings choice
        (consumption at the floor) instead of producing NaN."""
        tot = P.sum(-1, keepdims=True)
        corner = np.zeros_like(P); corner[..., 0] = 1.0
        return np.where(tot > 0, P / np.where(tot > 0, tot, 1.0), corner)

    @staticmethod
    def sparse_policy(st, P):
        """Gabaix-style inattention to the asset state: the household chooses CONSUMPTION as if its assets
        were a_perc = a_default + attn(b) (a - a_default); actual savings are a' = coh_actual - c, which
        shifts the choice distribution down by (1+r)(a_perc - a) and clips at the borrowing limit."""
        a_grid, a_c, attn, r = st['a_grid'], st['a_c'], st['attn'], st['r']
        Nb, Ne, Na, Nc = st['Nb'], st['Ne'], st['Na'], st['Nc']
        out = np.empty_like(P)
        for b in range(Nb):
            if attn[b] >= 1:
                out[b] = P[b]; continue
            a_perc = np.clip(st['a_default'] + attn[b] * (a_grid - st['a_default']), a_grid[0], a_grid[-1])
            i = np.minimum(np.searchsorted(a_grid, a_perc, side='right') - 1, Na - 2)
            wt = (a_perc - a_grid[i]) / (a_grid[i + 1] - a_grid[i])
            Pp = (1 - wt)[None, :, None] * P[b][:, i, :] + wt[None, :, None] * P[b][:, i + 1, :]   # policy at perceived state
            shift = (1 + r) * (a_perc - a_grid)                                                   # (Na,)
            for ia in range(Na):
                tgt = np.clip(a_c - shift[ia], a_c[0], a_c[-1])                                    # actual a' for each perceived choice
                k = np.minimum(np.searchsorted(a_c, tgt, side='right') - 1, Nc - 2)
                w = (tgt - a_c[k]) / (a_c[k + 1] - a_c[k])
                Q = np.zeros((Ne, Nc))
                np.add.at(Q, (slice(None), k), Pp[:, ia, :] * (1 - w)[None, :])
                np.add.at(Q, (slice(None), k + 1), Pp[:, ia, :] * w[None, :])
                Q = Q * st['feas'][:, ia, :]
                tot = Q.sum(-1, keepdims=True)
                corner = np.zeros_like(Q); corner[:, 0] = 1.0
                out[b, :, ia, :] = np.where(tot > 1e-12, Q / np.maximum(tot, 1e-12), corner)
        return out

    @staticmethod
    def evaluate(st, V, P, sweeps=10):
        """Howard improvement: hold the logit policy P fixed and apply V <- sum_c P (u + beta_eff cont(V))."""
        Pi, Pb, u, beta_eff, scarce = st['Pi'], st['Pb'], st['u'], st['beta_eff'], st['scarce']
        W = st['W']; Ne = st['Ne']
        Pu = (P * u[None]).sum(-1)                                                # (Nb, Ne, Na)
        for _ in range(sweeps):
            EVe = np.einsum('ef,bfa->bea', Pi, V) @ W.T                          # (Nb, Ne, Nc)
            Vn = Pu.copy()
            for ie in range(Ne):
                if st['naive']:
                    Vn[:, ie, :] += beta_eff[:, None] * np.einsum('bac,bc->ba', P[:, ie, :, :], EVe[:, ie, :])
                    continue
                for sc in range(2):
                    mask = scarce[ie] == sc
                    if not mask.any():
                        continue
                    cont = Pb[ie, sc] @ EVe[:, ie, :]                            # (Nb, Nc)
                    Vn[:, ie, mask] += beta_eff[:, None] * np.einsum('bac,bc->ba', P[:, ie, mask, :], cont)
            V = Vn
        return V

    @staticmethod
    def transition(st, P):
        """Dense Lambda[(b,e,a) -> (b',e',a')] from policy P and the exogenous laws."""
        Nb, Ne, Na, W = st['Nb'], st['Ne'], st['Na'], st['W']
        Pi, Pb, scarce = st['Pi'], st['Pb'], st['scarce']
        Pa = P @ W                                                                # (Nb, Ne, Na, Na') lottery-weighted
        L = np.zeros((Nb, Ne, Na, Nb, Ne, Na))
        for ie in range(Ne):
            for sc in range(2):
                mask = scarce[ie] == sc
                if not mask.any():
                    continue
                # Pa[b, ie, a, a'] * Pb[ie, sc, b, b'] * Pi[ie, e']
                L[:, ie, mask, :, :, :] = np.einsum('bac,bd,f->bacdf', Pa[:, ie, mask, :],
                                                    Pb[ie, sc], Pi[ie]).transpose(0, 1, 3, 4, 2)
        return L.reshape(Nb * Ne * Na, Nb * Ne * Na)

    @staticmethod
    def per_state_outputs(st, P):
        """Per-state expected outcomes o[b, e, a] for each aggregate output."""
        a_c, c, uc, e_grid, b_grid, Nb = st['a_c'], st['c'], st['uc'], st['e_grid'], st['b_grid'], st['Nb']
        o = {}
        o['a'] = (P * a_c[None, None, None, :]).sum(-1)
        o['c'] = (P * c[None]).sum(-1)
        o['uce'] = e_grid[None, :, None] * (P * uc[None]).sum(-1)
        o['htm'] = (P * (a_c <= a_c[0] + st['htm_cut'])[None, None, None, :]).sum(-1)   # hand-to-mouth: a' within htm_cut of the limit
        o['bw'] = np.broadcast_to((b_grid / max(Nb - 1, 1))[:, None, None], o['a'].shape).copy()
        o['scarce'] = np.broadcast_to(st['scarce'][None].astype(float), o['a'].shape).copy()
        return o

    OUT = {'A': 'a', 'C': 'c', 'UCE': 'uce', 'HTM': 'htm', 'BW': 'bw', 'SCARCE': 'scarce', 'WELF': 'welf', 'WELF_OWN': 'welf_own', 'WELF_TUN': 'welf_tun'}

    def tunnel_welfare(self, st, P, L):
        """Policy evaluation honoring tunneling as preference (state-dependent discount) but scoring noise as error."""
        Eu = (P * st['u']).sum(-1).ravel()
        n = L.shape[0]
        bdisc = np.repeat(st['beta_eff'], st['Ne'] * st['Na'])
        return np.linalg.solve(np.eye(n) - bdisc[:, None] * L, Eu)

    def true_welfare(self, st, P, L):
        """Policy evaluation at the TRUE beta: Vt = Eu + beta * Lambda Vt."""
        Eu = (P * st['u']).sum(-1).ravel()
        n = L.shape[0]
        return np.linalg.solve(np.eye(n) - st['beta'] * L, Eu)

    # ------------------------------------------------------------------ steady state
    def solve_ss(self, st, V0=None, tol=1e-8, maxit=5000, sweeps=10):
        Nb, Ne, Na = st['Nb'], st['Ne'], st['Na']
        key = (Nb, Ne, Na)
        if V0 is None:
            V0 = getattr(self, '_Vcache', {}).get(key)       # warm start from the last solve on this grid
        V = np.zeros((Nb, Ne, Na)) if V0 is None else V0.copy()
        if V0 is None:
            V[:] = st['u'].max(-1)[None] / (1 - st['beta'])
        hist = []
        V_init = V.copy()
        converged = False
        np_err = np.seterr(all='ignore')
        try:
            for it in range(maxit):
                Vn, P, Q = self.bellman(st, V, act=False)
                d = np.max(np.abs(Vn - V)); hist.append(d)
                if not np.isfinite(d) or d > 1e6:
                    if sweeps:
                        # the Howard sweeps blew up for this calibration: restart plain value iteration from the start
                        sweeps = 0; V = V_init.copy(); hist = []
                        continue
                    raise ValueError('bandwidth household: value iteration diverged')
                if d < tol:
                    V = Vn; converged = True
                    break
                # Howard sweeps can oscillate at high noise temperatures: if the error stops falling, drop them
                if sweeps and len(hist) >= 60 and d > 0.5 * hist[-51]:
                    sweeps = 0
                V = self.evaluate(st, Vn, P, sweeps) if sweeps else Vn
        finally:
            np.seterr(**np_err)
        if not converged:
            if np.max(np.abs(Vn - V)) > 1e-5 * (1 + np.max(np.abs(V))):
                raise ValueError('bandwidth household: no convergence of V')
            V = Vn   # converged to a loose tolerance; accept
        if not hasattr(self, '_Vcache'):
            self._Vcache = {}
        self._Vcache[key] = V.copy()
        _, P, _ = self.bellman(st, V, act=True)       # actions, with the alternative-face maps applied once
        L = self.transition(st, P)
        n = L.shape[0]
        # stationary distribution: solve (I - L^T) D = 0 with normalization
        M = np.eye(n) - L.T
        M[-1, :] = 1.0
        rhs = np.zeros(n); rhs[-1] = 1.0
        D = np.linalg.solve(M, rhs)
        D = np.maximum(D, 0); D /= D.sum()
        return V, P, L, D.reshape(Nb, Ne, Na)

    def _steady_state(self, calibration, tol=1e-8, maxit=5000, sweeps=10):
        ss = {k: calibration[k] for k in self.inputs}
        st = self.setup(ss)
        V, P, L, D = self.solve_ss(st, tol=tol, maxit=maxit, sweeps=sweeps)
        o = self.per_state_outputs(st, P)
        o['welf'] = self.true_welfare(st, P, L).reshape(D.shape)
        o['welf_own'] = V            # the household's own valuation (degraded discount, own forecast): the revealed-preference criterion
        o['welf_tun'] = self.tunnel_welfare(st, P, L).reshape(D.shape)   # tunneling honored as preference, noise scored as error
        aggs = {K: float(np.vdot(D, o[k])) for K, k in self.OUT.items()}
        internals = {'D': D, 'V': V, 'P': P, 'a_grid': st['a_grid'], 'e_grid': st['e_grid'], 'b_grid': st['b_grid']}
        return SteadyStateDict({**ss, **aggs}, {self.name: internals})

    # ------------------------------------------------------------------ Jacobian (fake news)
    def _jacobian(self, ss, inputs, outputs, T, h=1e-4):
        base = {k: ss[k] for k in self.inputs}
        st = self.setup(base)
        D = ss.internals[self.name]['D']; V = ss.internals[self.name]['V']
        Vss, Pss, Qss = self.bellman(st, V)
        Lss = self.transition(st, Pss)
        oss = self.per_state_outputs(st, Pss)
        outputs = [o for o in outputs if o in self.OUT and o not in ('WELF', 'WELF_OWN', 'WELF_TUN')]
        Dflat = D.ravel()
        # expectation vectors E_t[o] = Lss^t o
        E = {o: np.empty((T, Dflat.size)) for o in outputs}
        for o in outputs:
            v = oss[self.OUT[o]].ravel().copy()
            for t in range(T):
                E[o][t] = v
                v = Lss @ v
        J = {o: {} for o in outputs}
        for i in inputs:
            # curlyY[u][o], curlyD[u] (u = periods before the shock hits)
            cY = {o: np.empty(T) for o in outputs}; cD = np.empty((T, Dflat.size))
            # u = 0: shock to inputs at the date of the policy (two-sided)
            def one_step(delta):
                st_i = self.setup(base, {i: base[i] + delta})
                Vn, P, _ = self.bellman(st_i, Vss)
                return Vn, P, self.transition(st_i, P), self.per_state_outputs(st_i, P)
            Vp, Pp, Lp, op = one_step(h); Vm, Pm, Lm, om = one_step(-h)
            for o in outputs:
                k = self.OUT[o]
                cY[o][0] = np.vdot(Dflat, (op[k] - om[k]).ravel()) / (2 * h)
            cD[0] = (Lp - Lm).T @ Dflat / (2 * h)
            dV = (Vp - Vm) / (2 * h)
            # u >= 1: unperturbed inputs, perturbed continuation (linear in dV)
            for u in range(1, T):
                Vn_p, P_p, _ = self.bellman(st, Vss + h * dV)
                Vn_m, P_m, _ = self.bellman(st, Vss - h * dV)
                dP = (P_p - P_m) / (2 * h)
                dV = (Vn_p - Vn_m) / (2 * h)
                dL = self.transition(st, dP)        # linear in P
                cD[u] = dL.T @ Dflat
                do = self.per_state_outputs(st, dP)  # linear in P for a, c, uce, htm; bw/scarce zero
                for o in outputs:
                    k = self.OUT[o]
                    cY[o][u] = np.vdot(Dflat, do[k].ravel()) if k not in ('bw', 'scarce') else 0.0
            for o in outputs:
                F = np.empty((T, T))
                F[0, :] = cY[o]
                F[1:, :] = E[o][:T - 1] @ cD.T
                Jm = F.copy()
                for t in range(1, T):
                    Jm[1:, t] += Jm[:-1, t - 1]
                J[o][i] = Jm
        return JacobianDict(J, name=self.name, T=T)

    def _impulse_linear(self, ss, inputs, outputs, Js, h=1e-4):
        return ImpulseDict(self._jacobian(ss, list(inputs.keys()), outputs, inputs.T, h=h).apply(inputs))

    # ------------------------------------------------------------------ nonlinear transition
    def _impulse_nonlinear(self, ssin, inputs, outputs, internals, ss_initial):
        base = {k: ssin[k] for k in self.inputs}
        T = inputs.T
        Vss = ssin.internals[self.name]['V']
        D0 = ssin.internals[self.name]['D'] if ss_initial is None else ss_initial.internals[self.name]['D']
        paths = {t: {k: base[k] + inputs[k][t] for k in inputs.keys()} for t in range(T)}
        sts = [self.setup(base, paths[t]) for t in range(T)]
        Ps = [None] * T
        V = Vss
        for t in reversed(range(T)):
            V, P, _ = self.bellman(sts[t], V)
            Ps[t] = P
        D = D0.ravel().copy()
        aggs = {o: np.empty(T) for o in outputs if o in self.OUT}
        for t in range(T):
            o = self.per_state_outputs(sts[t], Ps[t])
            L = self.transition(sts[t], Ps[t])
            if 'WELF' in aggs:
                o['welf'] = self.true_welfare(sts[t], Ps[t], L).reshape(D0.shape)
            for kk in ('WELF_OWN', 'WELF_TUN'):
                if kk in aggs:
                    o[self.OUT[kk]] = Vss * 0 + np.nan
            for K in aggs:
                aggs[K][t] = np.vdot(D, o[self.OUT[K]].ravel())
            D = L.T @ D
        return ImpulseDict(aggs, {}, T) - ssin
