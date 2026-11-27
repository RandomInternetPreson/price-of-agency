"""
arms_race.py -- Adaptive observer vs covert agent with finite entropy rate.

Agent: whitening stealth at lambda* in symmetric env (n=4, s=0.5).
Randomization: inverse-CDF of the whitening policy at resolution
m_S * m_U; per-step fresh entropy h = log2(m_U) bits (U_t iid uniform);
S in {0..m_S-1} is a fixed personal offset ("habit"), drawn once.

Observer: knows the policy family, the environment, everything except
(S, U_t, F_t). Sees the stream (E_t, A_t). Maintains EXACT Bayesian
posterior over S. Its predictive uncertainty defines the dynamic
delta_A(t) = E[H(A_t | E_t, posterior_t)] / log2(n).

Exact anchors (no sampling):
  delta_A(0)      : S marginalized under uniform prior
  delta_inf(h)    : S known -- the sustainable stealth floor
Trajectory-averaged transition: Monte Carlo over (S, F_t, E_t, U_t) with
exact per-step posterior updates. [MC, exact updates]
"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

rng = np.random.default_rng(20260726)
n = 4; log2n = np.log2(n); s = 0.5
pF = np.full(n, 1/n)

def ch(f):
    C = np.full((n, n), (1-f)/n); C[np.arange(n), np.arange(n)] += f
    return C

C_E = ch(1-s)
p_fe = pF[:, None]*C_E
p_e = p_fe.sum(0)
q = (p_fe/p_e[None]).T                      # (e,f) posterior p(f|e)

def H(p):
    p = p[p > 1e-15]
    return float(-(p*np.log2(p)).sum())

# whitening policy at plateau end
lam = 1.0/(n*q.max())
pol = np.zeros((n, n, n))                   # (f,e,a)
for e in range(n):
    r = np.clip((1.0/n - lam*q[e])/(1-lam), 0, None); r /= r.sum()
    for f in range(n):
        pol[f, e, :] = (1-lam)*r
        pol[f, e, f] += lam
cdf = np.cumsum(pol, axis=-1)

def action_table(m_S, m_U):
    """G[f,e,S,U] deterministic action via inverse-CDF at seed-offset
    quantile: r_frac = ((S + (U+0.5)/m_U) mod m_S) / m_S  -- S is a
    persistent phase, U fresh jitter within the phase cell."""
    G = np.zeros((n, n, m_S, m_U), dtype=int)
    for S in range(m_S):
        for U in range(m_U):
            rfrac = ((S + (U+0.5)/m_U) % m_S)/m_S
            G[:, :, S, U] = (cdf < rfrac).sum(axis=-1)
    return G

def lik_table(G, m_S, m_U):
    """L[S,e,a] = P(A=a | E=e, S) = sum_f q(e,f) * (1/m_U) sum_U [G=a]."""
    L = np.zeros((m_S, n, n))
    for S in range(m_S):
        for e in range(n):
            for f in range(n):
                for U in range(m_U):
                    L[S, e, G[f, e, S, U]] += q[e, f]/m_U
    return L

def exact_anchors(L, m_S):
    """delta_A with S marginalized (t=0) and S known (floor), exact."""
    pred0 = L.mean(axis=0)                          # (e,a)
    d0 = sum(p_e[e]*H(pred0[e]) for e in range(n))/log2n
    dinf = np.mean([sum(p_e[e]*H(L[S, e]) for e in range(n))
                    for S in range(m_S)])/log2n
    return d0, dinf

def run_mc(G, L, m_S, m_U, T=40, trials=3000):
    dA = np.zeros(T); postH = np.zeros(T)
    for _ in range(trials):
        S_true = rng.integers(m_S)
        post = np.full(m_S, 1/m_S)
        for t in range(T):
            f = rng.integers(n)
            e = rng.choice(n, p=C_E[f])
            U = rng.integers(m_U)
            a = G[f, e, S_true, U]
            pred = post @ L[:, e, :]                # predictive P(a|e,post)
            dA[t] += H(pred)
            postH[t] += H(post)
            post = post*L[:, e, a]                  # exact Bayes
            post /= post.sum()
    return dA/(trials*log2n), postH/(trials*np.log2(m_S))

m_S = 8
configs = [(m_S, 1), (m_S, 2), (m_S, 4), (m_S, 8)]
T = 40
fig, axes = plt.subplots(1, 2, figsize=(13.5, 5))
fig.suptitle("Arms race: exact Bayesian observer vs finite-entropy stealth "
             f"(n={n}, s={s}, m_S={m_S} habit states)  [MC over trajectories, "
             "exact per-step updates]", fontsize=11)

print(f"{'h (bits/step)':>13} {'delta_A(0)':>11} {'floor d_inf':>12} "
      f"{'d_A(T=40)':>10} {'seed H left':>12}")
for m_S_, m_U in configs:
    G = action_table(m_S_, m_U)
    L = lik_table(G, m_S_, m_U)
    d0, dinf = exact_anchors(L, m_S_)
    dA_t, pH_t = run_mc(G, L, m_S_, m_U, T=T)
    h = np.log2(m_U)
    print(f"{h:13.0f} {d0:11.4f} {dinf:12.4f} {dA_t[-1]:10.4f} {pH_t[-1]:12.4f}")
    axes[0].plot(range(T), dA_t, lw=2, label=f"h={h:.0f} bits/step")
    axes[0].axhline(dinf, ls=":", alpha=0.5,
                    color=axes[0].lines[-1].get_color())
    axes[1].plot(range(T), pH_t, lw=2, label=f"h={h:.0f} bits/step")

axes[0].set_xlabel("time step"); axes[0].set_ylabel(r"$\delta_A(t)$ vs adaptive observer")
axes[0].set_title("stealth decay to the sustainable floor (dotted = exact $\\delta_\\infty$)")
axes[0].legend(); axes[0].grid(alpha=0.3)
axes[1].set_xlabel("time step"); axes[1].set_ylabel("normalized posterior entropy over habit seed")
axes[1].set_title("observer's remaining uncertainty about the agent's habits")
axes[1].legend(); axes[1].grid(alpha=0.3)
plt.tight_layout(rect=[0, 0, 1, 0.91])
import os
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'arms_race.png'), dpi=140)
print("saved: arms_race.png")
