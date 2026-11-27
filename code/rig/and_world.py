"""
and_world.py -- shared model world for the rig jobs (pure numpy, no torch).

Everything here reproduces the conventions of code/arms_race.py,
code/wirings_T11_wider_plateau.py and code/surveillance_T9_wider_plateau.py
so that rig results are comparable to the printed T9/T9'/T11/T11' numbers.

World: n equiprobable futures F; environment signal E through the symmetric
channel C_E (P(E=F) = 1 - s + s/n). Policies pol[f, e, a] = P(A=a | F=f, E=e).
Coin realization: a deterministic action table G[f, e, S, U] obtained by
inverse-CDF of pol[f, e, :] at a quantile rfrac(S, U), where S in {0..m_S-1}
is the persistent habit seed (drawn once per lifetime) and U in {0..m_U-1}
is the fresh per-step entropy, h = log2 m_U bits per action.

Wirings (how the fresh bits are wired to the habit) are quantile maps
rfrac(S, U) in [0, 1):
  gated      rfrac = ((S + (U+0.5)/m_U) mod m_S) / m_S      [printed formula, arms_race.py]
  additive   rfrac = ((S+0.5)/m_S + (U+0.5)/m_U) mod 1      [printed formula, wirings_T11_wider_plateau.py]
Cell-grid family (the quantile axis cut into M = m_S*m_U cells, rfrac = (cell+0.5)/M):
  additive:c cell = (S + U*m_S) mod M         (U spans the whole range at full resolution)
  span:d     cell = (S + U*d) mod M           (U spread with stride d; d=1 = contiguous
                                               window ~ gated-like, d=m_S = additive:c)
  random:k   cell = perm_k[S*m_U + U]         (random bijection of cells, seed k)
NOTE: 'gated' coincides with span:1 up to the window offset (S*m_U vs S); the
printed 'additive' uses a coarse quantile grid whose floors differ at the third
decimal from additive:c -- the dichotomy is a class property, the digits are not
(THEOREMS: Door-2 note). Self-test reproduces the printed T11' floors.
"""
import numpy as np

LOG2 = np.log2


def H(p, axis=-1):
    """Shannon entropy in bits along axis (0 log 0 = 0)."""
    p = np.asarray(p, float)
    with np.errstate(divide='ignore', invalid='ignore'):
        t = np.where(p > 1e-300, p * np.log2(np.where(p > 1e-300, p, 1.0)), 0.0)
    return -t.sum(axis=axis)


class World:
    def __init__(self, n=4, s=0.5):
        self.n, self.s = n, s
        self.log2n = float(np.log2(n))
        self.pF = np.full(n, 1.0 / n)
        C = np.full((n, n), s / n); C[np.arange(n), np.arange(n)] += 1 - s
        self.C_E = C                                  # C_E[f, e] = P(E=e | F=f)
        self.p_fe = self.pF[:, None] * C              # (f, e)
        self.p_e = self.p_fe.sum(0)
        self.q = (self.p_fe / self.p_e[None]).T       # q[e, f] = P(F=f | E=e)
        self.sage = float((H(self.p_fe.ravel()) - H(self.p_e)) / self.log2n)   # H(F|E)/log n

    # ---- policies -------------------------------------------------------
    def lam_star(self):
        return 1.0 / (self.n * self.q.max())

    def lam_policy(self):
        """Theorem 6 construction at lambda* (the T11 policy as printed)."""
        n, q = self.n, self.q
        lam = self.lam_star()
        pol = np.zeros((n, n, n))
        for e in range(n):
            r = np.clip((1.0 / n - lam * q[e]) / (1 - lam), 0, None); r /= r.sum()
            for f in range(n):
                pol[f, e, :] = (1 - lam) * r; pol[f, e, f] += lam
        return pol

    def hand_policy(self):
        """R4 hand plateau policy: act on F where E is wrong; scatter (weight q) where E is right."""
        n = self.n
        qq = self.lam_star()
        pol = np.zeros((n, n, n))
        for e in range(n):
            for f in range(n):
                if f != e:
                    pol[f, e, f] = 1.0
                else:
                    pol[f, e, :] = (1 - qq) / (n - 1); pol[f, e, e] = qq
        return pol

    def sage_policy(self):
        pol = np.zeros((self.n,) * 3)
        for f in range(self.n):
            pol[f, :, f] = 1.0
        return pol

    def policy(self, name):
        return {'lam': self.lam_policy, 'hand': self.hand_policy, 'sage': self.sage_policy}[name]()

    # ---- information quantities of a policy (exact) ----------------------
    def stats(self, pol):
        """returns aim = I(A;F)/log n, delta_A({E}) = H(A|E)/log n, lower wall I(A;F|E)/log n."""
        n = self.n
        p = self.p_fe[:, :, None] * pol                  # (f, e, a)
        p_a = p.sum((0, 1)); p_fa = p.sum(1); p_ea = p.sum(0)
        aim = (H(self.pF) + H(p_a) - H(p_fa.ravel())) / self.log2n
        dA = (H(p_ea.ravel()) - H(self.p_e)) / self.log2n
        wall = ((H(p_ea.ravel()) - H(self.p_e)) - (H(p.ravel()) - H(self.p_fe.ravel()))) / self.log2n
        return float(aim), float(dA), float(wall)


# ---- wirings -------------------------------------------------------------
def quantile_map(wiring, m_S, m_U):
    """returns float array rfrac[S, U] in [0, 1)."""
    M = m_S * m_U
    S = np.arange(m_S)[:, None]; U = np.arange(m_U)[None, :]
    if wiring == 'gated':
        return ((S + (U + 0.5) / m_U) % m_S) / m_S
    if wiring == 'additive':
        return ((S + 0.5) / m_S + (U + 0.5) / m_U) % 1.0
    if wiring == 'additive:c':
        cell = (S + U * m_S) % M
    elif wiring.startswith('span:'):
        d = int(wiring.split(':')[1])
        cell = (S + U * d) % M
    elif wiring.startswith('random:'):
        k = int(wiring.split(':')[1])
        perm = np.random.default_rng(1000 + k).permutation(M)
        cell = perm[S * m_U + U]
    else:
        raise ValueError(wiring)
    return (cell + 0.5) / M


def action_table(pol, rfrac, m_S, m_U):
    """G[f, e, S, U] by inverse-CDF of pol[f, e, :] at quantile rfrac[S, U]."""
    n = pol.shape[0]
    cdf = np.cumsum(pol, axis=-1)                       # (f, e, a)
    G = (cdf[:, :, None, None, :] < rfrac[None, None, :, :, None]).sum(-1)
    return np.minimum(G, n - 1).astype(np.int64)


def lik_tables(G, world):
    """
    L_F[S, f, e, a] = P(A=a | F=f, E=e, S)  (U marginalized)
    L[S, e, a]      = P(A=a | E=e, S) = sum_f q(e,f) L_F[S,f,e,a]
    """
    n = world.n
    _, _, m_S, m_U = G.shape
    # memory-light histogram over U: counts[f, e, S, a]
    base = (np.arange(n * n * m_S) * n).reshape(n, n, m_S, 1)
    counts = np.bincount((base + G).ravel(), minlength=n * n * m_S * n).reshape(n, n, m_S, n)
    L_F = (counts / m_U).transpose(2, 0, 1, 3)                   # (S, f, e, a)
    L = np.einsum('ef,sfea->sea', world.q, L_F)
    return L_F, L


def exact_floors(L, world):
    """delta_0 (seed unknown, uniform prior) and delta_inf (seed known), both /log n."""
    pred0 = L.mean(0)                                            # (e, a)
    d0 = float((world.p_e * H(pred0)).sum() / world.log2n)
    dinf = float((world.p_e[None, :] * H(L)).sum(1).mean() / world.log2n)
    return d0, dinf


# ---- fresh-input generators (for the regress arm) -------------------------
def fresh_U(rng, B, T, m_U, gen='iid'):
    """
    U[B, T] in {0..m_U-1}.
      iid        truly fresh (the book's assumption)
      lcg:k      k-bit linear congruential generator, hidden seed per lifetime;
                 U = top log2(m_U) bits of the state (a pseudo-random coin)
    """
    if gen == 'iid':
        return rng.integers(m_U, size=(B, T), dtype=np.int64)
    if gen.startswith('lcg:'):
        k = int(gen.split(':')[1]); mod = 1 << k
        # Hull-Dobell full-period parameters for modulus 2^k
        a = {8: 141, 12: 1229, 16: 25173, 24: 1664525, 32: 1664525}.get(k, 1664525) % mod
        c = {8: 29, 12: 1, 16: 13849, 24: 1013904223, 32: 1013904223}.get(k, 1013904223) % mod
        x = rng.integers(mod, size=B, dtype=np.int64)
        bits = int(np.log2(m_U))
        U = np.empty((B, T), dtype=np.int64)
        for t in range(T):
            x = (a * x + c) % mod
            U[:, t] = (x >> (k - bits)) if bits > 0 else 0
        return U
    raise ValueError(gen)


def sample_streams(rng, world, G, m_S, m_U, B, T, gen='iid'):
    """Lifetimes: returns dict of int arrays S[B], F[B,T], E[B,T], U[B,T], A[B,T]."""
    n = world.n
    S = rng.integers(m_S, size=B)
    F = rng.integers(n, size=(B, T))
    # E | F via inverse CDF on C_E rows
    cdfE = np.cumsum(world.C_E, axis=1)
    r = rng.random((B, T))
    E = np.minimum((cdfE[F] < r[..., None]).sum(-1), n - 1)
    U = fresh_U(rng, B, T, m_U, gen)
    A = G[F, E, S[:, None], U]
    return dict(S=S, F=F, E=E, U=U, A=A)


# ---- self-test against the printed T11' numbers ---------------------------
if __name__ == "__main__":
    w = World(4, 0.5)
    print(f"n=4 s=0.5 sage={w.sage:.3f}")
    for pname, want in [('lam', dict(gated=[0.338, 0.453, 0.485, 0.474], additive=[0.338, 0.753, 0.960, 0.978])),
                        ('hand', dict(gated=[0.622, 0.667, 0.700, 0.697], additive=[0.622, 0.851, 0.973, 0.984]))]:
        pol = w.policy(pname)
        aim, dA, wall = w.stats(pol)
        print(f"policy {pname}: aim={aim:.3f} dA(E)={dA:.3f} wall={wall:.3f}")
        for wiring in ['gated', 'additive']:
            got = []
            for h in range(4):
                m_S, m_U = 8, 2 ** h
                G = action_table(pol, quantile_map(wiring, m_S, m_U), m_S, m_U)
                _, L = lik_tables(G, w)
                d0, dinf = exact_floors(L, w)
                got.append(dinf)
            ok = np.allclose(got, want[wiring], atol=2e-3)
            print(f"  {wiring:8s} floors h=0..3: {np.round(got, 3)}  printed {want[wiring]}  match={ok}")
    # streams sanity
    rng = np.random.default_rng(0)
    G = action_table(w.policy('hand'), quantile_map('additive', 8, 8), 8, 8)
    st = sample_streams(rng, w, G, 8, 8, 4, 10)
    print("stream sample A[0]:", st['A'][0])
    print("lcg fresh U sample:", fresh_U(rng, 1, 12, 8, 'lcg:8')[0])
