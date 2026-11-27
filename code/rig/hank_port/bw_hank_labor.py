"""
bw_hank_labor.py -- HANK v0.2 (stress objective #10): the household chooses its own HOURS, and its own
hours set its time floor. Choice = (a', h) with h on a small grid; income w*e*h; disutility of hours
phi_h * h^(1+1/nu)/(1+1/nu); free time Tbar_e - h decides whether bandwidth can recover (the gate).
The naive household does not perceive the bandwidth cost of a long shift (the floor is sold without
being priced); the sophisticated variant (naive = 0) does. Everything else is bw_hank.BandwidthHH.
Labor market: flexible wage clears efficiency hours H = sum D e h against the firm's demand Y/Z (no union).
"""
import numpy as np
from sequence_jacobian.utilities.ordered_set import OrderedSet
from bw_hank import BandwidthHH, PARAMS, AGG_INPUTS


class BandwidthHHLabor(BandwidthHH):
    def __init__(self, name='hh_bwl'):
        super().__init__(name)
        self.inputs = OrderedSet([i for i in AGG_INPUTS if i != 'N'] + PARAMS + ['h_grid', 'phi_h', 'nu'])
        self.outputs = OrderedSet(['A', 'C', 'HEFF', 'HOURS', 'HTM', 'BW', 'SCARCE', 'WELF', 'WELF_OWN', 'WELF_TUN', 'BELOW'])
        self.internals = OrderedSet(['D', 'V', 'P', 'a_grid', 'e_grid', 'b_grid', 'h_grid'])

    OUT = {'A': 'a', 'C': 'c', 'HEFF': 'heff', 'HOURS': 'hours', 'HTM': 'htm', 'BW': 'bw', 'SCARCE': 'scarce',
           'WELF': 'welf', 'WELF_OWN': 'welf_own', 'WELF_TUN': 'welf_tun', 'BELOW': 'below'}

    def setup(self, ss, inputs=None):
        x = dict(ss)
        if inputs is not None:
            x.update(inputs)
        x['N'] = 1.0                                   # the base class needs an N; the gate here uses own hours
        st = super().setup(x)
        h_grid = np.asarray(x['h_grid'], float); Nh = len(h_grid)
        Ne, Na, Nc, Nb = st['Ne'], st['Na'], st['Nc'], st['Nb']
        e_grid, a_grid, a_c = st['e_grid'], st['a_grid'], st['a_c']
        Tr = st['y'] - x['w'] * e_grid * 1.0            # transfers (the base put income = w e N + Tr with N = 1)
        coh = (1 + x['r']) * a_grid[None, :, None] + (x['w'] * e_grid[:, None, None] * h_grid[None, None, :]) + Tr[:, None, None]   # (Ne, Na, Nh)
        c = coh[:, :, None, :] - a_c[None, None, :, None]                                   # (Ne, Na, Nc, Nh)
        feas = c >= x['c_min']; cc = np.maximum(c, x['c_min']); eis = x['eis']
        u = np.log(cc) if abs(eis - 1) < 1e-12 else cc ** (1 - 1 / eis) / (1 - 1 / eis)
        nu = float(x['nu']); dis = float(x['phi_h']) * h_grid ** (1 + 1 / nu) / (1 + 1 / nu)
        u = np.where(feas, u - dis[None, None, None, :], -1e9)
        # flatten the (c, h) choice: index k = c * Nh + h
        st.update(h_grid=h_grid, Nh=Nh, Nk=Nc * Nh, coh_h=coh, c=cc.reshape(Ne, Na, Nc * Nh), feas=feas.reshape(Ne, Na, Nc * Nh),
                  u=u.reshape(Ne, Na, Nc * Nh), uc=(cc ** (-1 / eis)).reshape(Ne, Na, Nc * Nh),
                  scarce=(coh.min(-1) < x['m_scar']).astype(int))                         # scarcity flag on the lowest-hours cash
        # bandwidth law by own hours: Pb_h[h][e, sc, b, b']
        st['Pb_h'] = [self.bandwidth_law(x, e_grid, float(h), x['S']) for h in h_grid]
        st['below'] = (np.broadcast_to(np.asarray(x['Tbar'], float), (Ne,))[:, None] + float(x.get('dT_low', 0.0)) * (np.arange(Ne) == 0)[:, None]
                       - h_grid[None, :]) < x['T_gate']                                     # (Ne, Nh): below the gate at these hours
        return st

    @staticmethod
    def bellman(st, V, act=True):
        Pi, u, feas, kappa, beta_eff, scarce = st['Pi'], st['u'], st['feas'], st['kappa'], st['beta_eff'], st['scarce']
        Nb, Ne, Na, Nc, Nh, W = st['Nb'], st['Ne'], st['Na'], st['Nc'], st['Nh'], st['W']
        EVe = np.einsum('ef,bfa->bea', Pi, V) @ W.T                                       # (Nb, Ne, Nc)
        Q = np.empty((Nb, Ne, Na, Nc, Nh))
        for ie in range(Ne):
            if st['naive']:
                Q[:, ie] = u[ie].reshape(Na, Nc, Nh)[None] + beta_eff[:, None, None, None] * EVe[:, ie, None, :, None]
                continue
            for sc in range(2):
                mask = scarce[ie] == sc
                if not mask.any():
                    continue
                for ih in range(Nh):
                    cont = st['Pb_h'][ih][ie, sc] @ EVe[:, ie, :]                          # (Nb, Nc)
                    val = u[ie, mask].reshape(mask.sum(), Nc, Nh)[None, :, :, ih] + beta_eff[:, None, None] * cont[:, None, :]   # (Nb, n_mask, Nc)
                    Q[:, ie, mask, :, ih] = val.transpose(1, 0, 2)      # numpy moves the advanced-index axes to the front here
        Q = Q.reshape(Nb, Ne, Na, Nc * Nh)
        z = Q / kappa[:, None, None, None]; z = z - z.max(-1, keepdims=True)
        P = BandwidthHH.normalize(np.exp(z) * feas[None])
        Vn = (P * Q).sum(-1)
        if act and np.any(st['pb'] < 1):
            Qp = u[None] + st['pb'][:, None, None, None] * (Q - u[None])
            zp = Qp / kappa[:, None, None, None]; zp = zp - zp.max(-1, keepdims=True)
            P = BandwidthHH.normalize(np.exp(zp) * feas[None])
        return Vn, P, Q

    @staticmethod
    def evaluate(st, V, P, sweeps=10):
        Pi, u, beta_eff, W = st['Pi'], st['u'], st['beta_eff'], st['W']
        Nb, Ne, Na, Nc, Nh = st['Nb'], st['Ne'], st['Na'], st['Nc'], st['Nh']
        Pu = (P * u[None]).sum(-1)
        Pc = P.reshape(Nb, Ne, Na, Nc, Nh).sum(-1)                                       # choice mass over a' (naive: h irrelevant to continuation)
        if not st['naive']:
            return V                                                                         # no Howard for the sophisticated labor block
        for _ in range(sweeps):
            EVe = np.einsum('ef,bfa->bea', Pi, V) @ W.T
            V = Pu + beta_eff[:, None, None] * np.einsum('beac,bec->bea', Pc, EVe)
        return V

    @staticmethod
    def transition(st, P):
        Nb, Ne, Na, Nc, Nh, W = st['Nb'], st['Ne'], st['Na'], st['Nc'], st['Nh'], st['W']
        Pi, scarce = st['Pi'], st['scarce']
        P5 = P.reshape(Nb, Ne, Na, Nc, Nh)
        L = np.zeros((Nb, Ne, Na, Nb, Ne, Na))
        for ih in range(Nh):
            Pa = P5[..., ih] @ W                                                             # (Nb, Ne, Na, Na')
            for ie in range(Ne):
                for sc in range(2):
                    mask = scarce[ie] == sc
                    if not mask.any():
                        continue
                    L[:, ie, mask] += np.einsum('bac,bd,f->bacdf', Pa[:, ie, mask, :], st['Pb_h'][ih][ie, sc], Pi[ie]).transpose(0, 1, 3, 4, 2)
        return L.reshape(Nb * Ne * Na, Nb * Ne * Na)

    @staticmethod
    def per_state_outputs(st, P):
        Nb, Ne, Na, Nc, Nh = st['Nb'], st['Ne'], st['Na'], st['Nc'], st['Nh']
        a_c, h_grid, e_grid, b_grid = st['a_c'], st['h_grid'], st['e_grid'], st['b_grid']
        P5 = P.reshape(Nb, Ne, Na, Nc, Nh)
        o = {}
        o['a'] = np.einsum('beach,c->bea', P5, a_c)
        o['c'] = (P * st['c'][None]).sum(-1)
        o['hours'] = np.einsum('beach,h->bea', P5, h_grid)
        o['heff'] = e_grid[None, :, None] * o['hours']
        o['htm'] = np.einsum('beach,c->bea', P5, (a_c <= a_c[0] + st['htm_cut']).astype(float))
        o['bw'] = np.broadcast_to((b_grid / max(Nb - 1, 1))[:, None, None], o['a'].shape).copy()
        o['scarce'] = np.broadcast_to(st['scarce'][None].astype(float), o['a'].shape).copy()
        o['below'] = np.einsum('beach,eh->bea', P5, st['below'].astype(float))             # P(working below one's gate)
        return o

    def _steady_state(self, calibration, tol=1e-8, maxit=5000, sweeps=10):
        from sequence_jacobian.classes import SteadyStateDict
        ss = {k: calibration[k] for k in self.inputs}
        st = self.setup(ss)
        V, P, L, D = self.solve_ss(st, tol=tol, maxit=maxit, sweeps=sweeps)
        o = self.per_state_outputs(st, P)
        o['welf'] = self.true_welfare(st, P, L).reshape(D.shape)
        o['welf_own'] = V
        o['welf_tun'] = self.tunnel_welfare(st, P, L).reshape(D.shape)
        aggs = {K: float(np.vdot(D, o[k])) for K, k in self.OUT.items()}
        internals = {'D': D, 'V': V, 'P': P, 'a_grid': st['a_grid'], 'e_grid': st['e_grid'], 'b_grid': st['b_grid'], 'h_grid': st['h_grid']}
        return SteadyStateDict({**ss, **aggs}, {self.name: internals})
