"""
bw_two_asset.py -- stress objective #9: the bandwidth household with TWO assets, liquid and illiquid
(the Kaplan-Violante structure in its simplest steady-state form), to ask whether the one-asset host's
hand-to-mouth results are an artifact of having a single asset.

State (b, e, a, k): bandwidth, skill, liquid assets a (return r_a, borrowing limit -a_borrow), illiquid
assets k (return r_k > r_a, paid out as income). Moving the illiquid account costs a fixed fee chi_f plus a
proportional fee chi_p |k' - k|; leaving it alone is free. Choice (a', k'): a' on a refined grid with the
toolkit's lottery, k' on the illiquid grid. Budget:
    c + a' + (k' - k) + adj(k, k') = (1 + r_a) a + r_k k + w e N + T_e .
Bandwidth as in bw_hank.BandwidthHH (naive forecast): noise kappa(b), tunneling beta_eff(b); the law of
motion is driven by the time-floor gate, schedule entropy and scarcity (cash on hand below m_scar).
Hand-to-mouth = liquid a' within htm_cut of the borrowing limit; WEALTHY hand-to-mouth = hand-to-mouth
with illiquid k' above k_cut; POOR hand-to-mouth otherwise.

Steady state only. The distribution and the true-beta welfare are computed with factored operators
(no dense transition matrix), so the state space can be 7,200+ points on a laptop core.
"""
import numpy as np
from sequence_jacobian import grids
from bw_hank import BandwidthHH

DEFAULTS = dict(r_a=0.005, r_k=0.015, w=1 / 1.2, N=1.0, Div=1 - 1 / 1.2, Tax=0.028, S=1.0,
                beta=0.975, eis=0.5, rho_s=0.966, sigma_s=0.5, nS=3,
                amax=20.0, nA=50, nref=2, kmax=40.0, nK=12, a_borrow=0.0, chi_f=0.02, chi_p=0.02, c_min=1e-3,
                Nb=4, k_min=0.005, k_tax=0.05, tunnel=0.0153, Tbar=[1.80, 2.05, 2.30], T_gate=1.0, p_up=0.159,
                omega=[0.102, 0.040, 0.021], s_scar=0.069, m_scar=0.6, Tr_low=0.0, dT_low=0.0,
                htm_cut=0.15, k_cut=0.5)
CONTROL = dict(k_tax=0.0, tunnel=0.0)


class TwoAssetBW:
    def setup(self, x):
        e_grid, pi_e, Pi = grids.markov_rouwenhorst(rho=x['rho_s'], sigma=x['sigma_s'], N=int(x['nS']))
        Na, Nk, Nb = int(x['nA']), int(x['nK']), int(x['Nb']); Ne = len(e_grid)
        a_grid = grids.agrid(amax=x['amax'] + x['a_borrow'], n=Na) - x['a_borrow']
        k_grid = grids.agrid(amax=x['kmax'], n=Nk)
        nref = int(x['nref'])
        a_c = np.concatenate([np.linspace(a_grid[i], a_grid[i + 1], nref, endpoint=False) for i in range(Na - 1)] + [a_grid[-1:]])
        Nc = len(a_c)
        idx = np.minimum(np.searchsorted(a_grid, a_c, side='right') - 1, Na - 2)
        wt = (a_c - a_grid[idx]) / (a_grid[idx + 1] - a_grid[idx])
        W = np.zeros((Nc, Na)); W[np.arange(Nc), idx] = 1 - wt; W[np.arange(Nc), idx + 1] += wt
        b_grid = np.arange(Nb); frac = 1 - b_grid / max(Nb - 1, 1)
        kappa = x['k_min'] + x['k_tax'] * frac; beta_eff = x['beta'] * (1 - x['tunnel'] * frac)
        Tr = (x['Div'] - x['Tax']) / np.sum(pi_e * e_grid) * e_grid; Tr = Tr.copy(); Tr[0] += x['Tr_low']
        y = x['w'] * e_grid * x['N'] + Tr
        coh = (1 + x['r_a']) * a_grid[None, :, None] + x['r_k'] * k_grid[None, None, :] + y[:, None, None]      # (Ne, Na, Nk)
        d = k_grid[None, :] - k_grid[:, None]                                                                     # (Nk, Nk'): k' - k
        adj = x['chi_f'] * (d != 0) + x['chi_p'] * np.abs(d)
        c = coh[:, :, :, None, None] - a_c[None, None, None, :, None] - (d + adj)[None, None, :, None, :]        # (Ne,Na,Nk,Nc,Nk')
        feas = c >= x['c_min']; cc = np.maximum(c, x['c_min']); eis = x['eis']
        u = np.log(cc) if abs(eis - 1) < 1e-12 else cc ** (1 - 1 / eis) / (1 - 1 / eis)
        u = np.where(feas, u, -1e9)
        scarce = (coh < x['m_scar'])                                                                              # (Ne, Na, Nk) bool
        Pb = BandwidthHH.bandwidth_law(x, e_grid, x['N'], x['S'])                                                # (Ne, 2, Nb, Nb)
        return dict(x=x, e_grid=e_grid, pi_e=pi_e, Pi=Pi, a_grid=a_grid, k_grid=k_grid, a_c=a_c, W=W, Na=Na, Nk=Nk, Nb=Nb, Ne=Ne, Nc=Nc,
                    kappa=kappa, beta_eff=beta_eff, beta=x['beta'], u=u, c=cc, feas=feas, scarce=scarce, Pb=Pb, b_grid=b_grid)

    @staticmethod
    def cont(st, V):
        """EVc[b, e, c, k'] = sum_e' Pi[e,e'] sum_a' W[c,a'] V[b, e', a', k']   (naive: own bandwidth level)."""
        EVe = np.einsum('ef,bfak->beak', st['Pi'], V)
        return np.einsum('beak,ca->beck', EVe, st['W'])

    def bellman(self, st, V):
        EVc = self.cont(st, V)
        Q = st['u'][None] + st['beta_eff'][:, None, None, None, None, None] * EVc[:, :, None, None, :, :]
        sh = Q.shape
        Qf = Q.reshape(sh[0], sh[1], sh[2], sh[3], -1)
        z = Qf / st['kappa'][:, None, None, None, None]; z -= z.max(-1, keepdims=True)
        P = BandwidthHH.normalize(np.exp(z) * st['feas'].reshape(1, sh[1], sh[2], sh[3], -1))
        Vn = (P * Qf).sum(-1)
        return Vn, P.reshape(sh)

    def evaluate(self, st, V, P, sweeps):
        Pu = (P * st['u'][None]).sum((-1, -2))
        for _ in range(sweeps):
            EVc = self.cont(st, V)
            V = Pu + st['beta_eff'][:, None, None, None] * np.einsum('beakcj,becj->beak', P, EVc)
        return V

    def solve(self, cal, tol=1e-7, maxit=3000, sweeps=15, V0=None):
        x = dict(DEFAULTS); x.update(cal)
        st = self.setup(x)
        Nb, Ne, Na, Nk = st['Nb'], st['Ne'], st['Na'], st['Nk']
        V = V0 if V0 is not None and V0.shape == (Nb, Ne, Na, Nk) else np.broadcast_to(st['u'].max((-1, -2))[None] / (1 - st['beta']), (Nb, Ne, Na, Nk)).copy()
        err = np.seterr(all='ignore')
        try:
            for it in range(maxit):
                Vn, P = self.bellman(st, V)
                dlt = np.max(np.abs(Vn - V))
                if not np.isfinite(dlt):
                    raise ValueError('two-asset household: value iteration diverged')
                if dlt < tol:
                    V = Vn; break
                V = self.evaluate(st, Vn, P, sweeps)
            else:
                raise ValueError('two-asset household: no convergence')
        finally:
            np.seterr(**err)
        # choice kernel onto the state grid: Pa[b,e,(a,k),(a',k')]
        Pa = np.tensordot(P, st['W'], axes=([4], [0])).transpose(0, 1, 2, 3, 5, 4).reshape(Nb, Ne, Na * Nk, Na * Nk)
        sc = st['scarce'].reshape(Ne, Na * Nk)
        D = np.full((Nb, Ne, Na * Nk), 1.0 / (Nb * Ne * Na * Nk))
        for it in range(20000):
            Dn = np.zeros_like(D)
            for s_ in (0, 1):
                Dm = D * (sc == bool(s_))[None]
                M = np.einsum('beq,beqr->ber', Dm, Pa)
                Dn += np.einsum('ber,ebd,ef->dfr', M, st['Pb'][:, s_], st['Pi'], optimize=True)
            if np.max(np.abs(Dn - D)) < 1e-11:
                D = Dn; break
            D = Dn
        D = D / D.sum()
        # true-beta welfare by policy evaluation
        Eu = (P * st['u'][None]).sum((-1, -2)).reshape(Nb, Ne, Na * Nk)
        Vt = Eu / (1 - st['beta'])
        for it in range(5000):
            new = Eu.copy()
            for s_ in (0, 1):
                EVn = np.einsum('ebd,ef,dfr->ber', st['Pb'][:, s_], st['Pi'], Vt, optimize=True)
                new += st['beta'] * (sc == bool(s_))[None] * np.einsum('beqr,ber->beq', Pa, EVn)
            if np.max(np.abs(new - Vt)) < 1e-6:
                Vt = new; break
            Vt = new
        return self.stats(st, P, D.reshape(Nb, Ne, Na, Nk), Vt.reshape(Nb, Ne, Na, Nk), V)

    def stats(self, st, P, D, Vt, V):
        x = st['x']; a_c, k_grid = st['a_c'], st['k_grid']
        Pc = P.sum(-1); Pk = P.sum(-2)                                   # marginals over a' choice and k' choice
        a_pol = np.einsum('beakc,c->beak', Pc, a_c); k_pol = np.einsum('beakj,j->beak', Pk, k_grid)
        c_pol = (P * st['c'][None]).sum((-1, -2))
        lim = (a_c <= a_c[0] + x['htm_cut']).astype(float); rich = (k_grid > x['k_cut']).astype(float)
        htm = np.einsum('beakcj,c->beak', P, lim)
        whtm = np.einsum('beakcj,c,j->beak', P, lim, rich)
        bw = np.broadcast_to((st['b_grid'] / max(st['Nb'] - 1, 1))[:, None, None, None], D.shape)
        out = dict(A=float((D * a_pol).sum()), K=float((D * k_pol).sum()), C=float((D * c_pol).sum()),
                   HTM=float((D * htm).sum()), WHTM=float((D * whtm).sum()), BW=float((D * bw).sum()),
                   WELF=float((D * Vt).sum()), SCARCE=float((D * st['scarce'][None]).sum()),
                   top_a=float(D[:, :, -1, :].sum()), top_k=float(D[:, :, :, -1].sum()))
        out['PHTM'] = out['HTM'] - out['WHTM']
        m = D[:, 0]; w0 = m.sum()
        for key, arr in [('htm_low', htm), ('whtm_low', whtm), ('a_low', a_pol), ('k_low', k_pol), ('bw_low', bw), ('welf_low', Vt)]:
            out[key] = float((m * arr[:, 0]).sum() / w0)
        out['bw_groups'] = [float((D[:, ie] * bw[:, ie]).sum() / D[:, ie].sum()) for ie in range(st['Ne'])]   # bandwidth by skill group
        out['_V'] = V
        return out


if __name__ == '__main__':
    import time
    hh = TwoAssetBW()
    for lab, cal in [('control', CONTROL), ('model', {})]:
        t0 = time.time(); s = hh.solve(cal)
        print(f"{lab}: A={s['A']:.3f} K={s['K']:.3f} C={s['C']:.4f} HTM={s['HTM']:.3f} (wealthy {s['WHTM']:.3f}, poor {s['PHTM']:.3f}) "
              f"BW={s['BW']:.3f} top_a={s['top_a']:.4f} top_k={s['top_k']:.4f} [{time.time()-t0:.0f}s]", flush=True)
