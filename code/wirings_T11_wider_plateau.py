"""
wirings_T11_wider_plateau.py -- T11's two wirings re-run on the wider-plateau
policy (R4), exact floors only.

Model (arms_race.py conventions): n = 4, s = 0.5. A deterministic action table
G[f,e,S,U] realizes the policy by inverse-CDF at a quantile built from a
persistent habit seed S (m_S = 8 states) and fresh per-step entropy U
(h = log2 m_U bits):
  GATED    : rfrac = ((S + (U+0.5)/m_U) mod m_S) / m_S   (U jitters inside the habit cell)
  ADDITIVE : rfrac = ((S+0.5)/m_S + (U+0.5)/m_U) mod 1   (U spans the full range; S is a phase)
Floors (S known to the observer, U fresh): delta_inf(h) = E_S[H(A|E,S)]/log n.
Reference: delta_A(seed unknown) = H(A|E) with S marginalized.
T9' walls: the lower wall I(A;F|E)/log n binds EVERY seed-known floor (U is still private);
the sage upper wall H(F|E)/log n binds only the fully surveilled floor, h = 0.
"""
import sys, numpy as np
n, s = 4, 0.5
log2n = np.log2(n)
pF = np.full(n, 1 / n)
C_E = np.full((n, n), s / n); C_E[np.arange(n), np.arange(n)] += 1 - s
p_fe = pF[:, None] * C_E; p_e = p_fe.sum(0); q = (p_fe / p_e[None]).T   # (e,f)

def H(p):
    p = np.asarray(p, float).ravel(); p = p[p > 1e-15]
    return float(-(p * np.log2(p)).sum())

def lam_policy():
    lam = 1.0 / (n * q.max())
    pol = np.zeros((n, n, n))
    for e in range(n):
        r = np.clip((1.0 / n - lam * q[e]) / (1 - lam), 0, None); r /= r.sum()
        for f in range(n):
            pol[f, e, :] = (1 - lam) * r; pol[f, e, f] += lam
    return pol

def hand_policy():
    qq = 1.0 / (n * (1 - s) + s); pol = np.zeros((n, n, n))
    for e in range(n):
        for f in range(n):
            if f != e: pol[f, e, f] = 1.0
            else: pol[f, e, :] = (1 - qq) / (n - 1); pol[f, e, e] = qq
    return pol

def floors(pol, wiring, m_S=8, hs=(0, 1, 2, 3)):
    cdf = np.cumsum(pol, axis=-1)
    out = {}
    for h in hs:
        m_U = 2 ** h
        L = np.zeros((m_S, n, n))
        for S in range(m_S):
            for U in range(m_U):
                if wiring == 'gated':
                    rfrac = ((S + (U + 0.5) / m_U) % m_S) / m_S
                else:
                    rfrac = ((S + 0.5) / m_S + (U + 0.5) / m_U) % 1.0
                G = (cdf < rfrac).sum(axis=-1)          # (f,e)
                for e in range(n):
                    for f in range(n):
                        L[S, e, G[f, e]] += q[e, f] / m_U
        dinf = np.mean([sum(p_e[e] * H(L[S, e]) for e in range(n)) for S in range(m_S)]) / log2n
        pred0 = L.mean(0); d0 = sum(p_e[e] * H(pred0[e]) for e in range(n)) / log2n
        out[h] = (d0, dinf)
    return out

def I_AF_given_E(pol):
    p = p_fe[:, :, None] * pol
    return ((H(p.sum(0)) - H(p_e)) - (H(p) - H(p_fe))) / log2n

if __name__ == "__main__":
    sage = (H(p_fe) - H(p_e)) / log2n
    for name, pol in [("lambda* policy (T11 as printed)", lam_policy()), ("hand plateau policy (R4)", hand_policy())]:
        lo = I_AF_given_E(pol)
        print(f"\n{name}:  aim = {((H((p_fe[:,:,None]*pol).sum(1).sum(0)) + H((p_fe[:,:,None]*pol).sum(1).sum(1)) - H((p_fe[:,:,None]*pol).sum(1)))/log2n):.4f}"
              f"   lower wall {lo:.4f} <= every floor; h=0 floor <= sage {sage:.4f}")
        for wiring in ['gated', 'additive']:
            fl = floors(pol, wiring)
            row = "  ".join(f"h={h}: {d:.3f} (seed-unknown {d0:.3f})" for h, (d0, d) in fl.items())
            ok = all(lo - 1e-9 <= d for _, (d0, d) in fl.items()) and fl[0][1] <= sage + 1e-9
            print(f"  {wiring:8s} floors: {row}   walls ok: {ok}")
