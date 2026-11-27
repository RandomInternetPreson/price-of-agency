"""
delta_A v1 -- Exact computation of the agent-level free fraction (AND)
=====================================================================
Model class: bounded-rational agent (free-energy / softmax control) in a
stochastic environment with a latent future. Everything below is computed
by EXACT enumeration over finite alphabets -- no sampling, no Monte Carlo.

Structure
---------
  F  : latent future state, |F| = nF, uniform prior.
  E  : local environment signal. E is a noisy channel from F with
       corruption rate s (environmental stochasticity). With prob (1-s)
       E reveals F; with prob s, E is uniform noise. NOTE: s degrades the
       *informativeness* of the local environment about the future.
  K  : the agent's internal knowledge channel ("education"). K reveals F
       with fidelity e in the same way: with prob e, K = F; else uniform.
       K is conditionally independent of E given F. Education is access
       to information about the future NOT carried by the immediate
       environment (books, models, other people's decorrelated reports).
  A  : action, |A| = nF. Reward r(a, f) = 1 if a == f else 0.
  tau: time budget -> inverse temperature beta = tau in the
       bounded-rational softmax policy
           p(a | e_obs, k_obs)  proportional to  exp(beta * Q(a | e,k))
       where Q(a|e,k) = P(F = a | E = e_obs, K = k_obs)  (exact posterior).
       beta -> 0   : no time to compute -> uniform random action
       beta -> inf : full deliberation  -> argmax of the exact posterior

Reported quantities (all exact, in bits, normalized where stated):
  delta_A       = H(A | E) / log2(nA)      -- conditional independence of
                                              action from local environment
  competence    = I(A ; F)  / log2(nF)     -- goal information the action
                                              carries about the future
  AND corner    = agents scoring high on BOTH. The rock: delta_A = 0.
                  The gas: delta_A = 1, competence = 0.

Claim under test (exact, not simulated):
  (1) Education raises delta_A *while raising competence* -- it buys
      conditional independence from the local environment with real
      information, not noise.
  (2) Time theft (beta -> 0) fakes delta_A: H(A|E) rises but competence
      collapses -- the agent is randomized, not freed. The two-axis
      definition catches this; the one-axis definition is fooled.
  (3) Environmental stochasticity s interacts: when the local environment
      is informative (s low), even the uneducated agent is competent but
      has delta_A ~ 0 (it is the rock: right answers, fully predictable
      from circumstance). As s rises, only the educated agent retains
      competence, and its actions decorrelate from E. This is the
      continuum from the rock to the person, computed.
"""

import numpy as np
import itertools
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

np.set_printoptions(precision=4, suppress=True)

nF = 8          # latent future alphabet
nE = nF         # environment signal alphabet
nK = nF         # knowledge signal alphabet
nA = nF         # action alphabet


def channel(fidelity, n):
    """p(out | in): identity with prob fidelity, else uniform over n."""
    C = np.full((n, n), (1.0 - fidelity) / n)
    C[np.arange(n), np.arange(n)] += fidelity
    return C


def exact_system(e_edu, s_env, beta):
    """Return exact joint p(f, e, k, a) as a 4-D array."""
    pF = np.full(nF, 1.0 / nF)
    C_E = channel(1.0 - s_env, nE)      # env informativeness falls with s
    C_K = channel(e_edu, nK)            # education fidelity

    # joint p(f,e,k) = pF * C_E[f,e] * C_K[f,k]
    p_fek = pF[:, None, None] * C_E[:, :, None] * C_K[:, None, :]

    # exact posterior P(F=f | E=e, K=k)
    p_ek = p_fek.sum(axis=0)                          # (e,k)
    with np.errstate(divide="ignore", invalid="ignore"):
        post = p_fek / p_ek[None, :, :]               # (f,e,k)
    post = np.nan_to_num(post, nan=1.0 / nF)

    # bounded-rational policy: softmax_beta over Q(a|e,k) = post[a,e,k]
    logits = beta * post                              # (a,e,k)
    logits -= logits.max(axis=0, keepdims=True)
    pol = np.exp(logits)
    pol /= pol.sum(axis=0, keepdims=True)             # p(a | e,k)

    # full joint p(f,e,k,a)
    p = p_fek[:, :, :, None] * np.transpose(pol, (1, 2, 0))[None, :, :, :]
    return p                                          # (f,e,k,a)


def H(p):
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())


def metrics(p):
    """delta_A = H(A|E)/log2 nA ; competence = I(A;F)/log2 nF -- exact."""
    p_ea = p.sum(axis=(0, 2))            # (e,a)
    p_e = p_ea.sum(axis=1)
    H_A_given_E = H(p_ea) - H(p_e)
    delta_A = H_A_given_E / np.log2(nA)

    p_fa = p.sum(axis=(1, 2))            # (f,a)
    I_AF = H(p_fa.sum(axis=1)) + H(p_fa.sum(axis=0)) - H(p_fa)
    competence = I_AF / np.log2(nF)
    return delta_A, competence


# ---------------------------------------------------------------- sweeps
grid = 41
edu_ax = np.linspace(0.0, 1.0, grid)          # education fidelity e
sto_ax = np.linspace(0.0, 1.0, grid)          # environmental stochasticity s
BETA_FULL = 60.0                              # ample deliberation time

D_es = np.zeros((grid, grid))                 # delta_A over (edu, s)
C_es = np.zeros((grid, grid))
for i, e in enumerate(edu_ax):
    for j, s in enumerate(sto_ax):
        p = exact_system(e, s, BETA_FULL)
        D_es[i, j], C_es[i, j] = metrics(p)

# time-theft sweep at fixed high stochasticity, educated agent
beta_ax = np.linspace(0.0, 60.0, 61)
S_FIX, E_FIX = 0.7, 0.9
D_b, C_b = np.zeros_like(beta_ax), np.zeros_like(beta_ax)
for i, b in enumerate(beta_ax):
    p = exact_system(E_FIX, S_FIX, b)
    D_b[i], C_b[i] = metrics(p)

# the four corners, exact values
corners = {
    "rock  (e=0, s=0, beta=60)": metrics(exact_system(0.0, 0.0, 60.0)),
    "gas   (any e/s, beta=0)":   metrics(exact_system(0.9, 0.7, 0.0)),
    "sage  (e=1, s=0.7, b=60)":  metrics(exact_system(1.0, 0.7, 60.0)),
    "naive (e=0, s=0.7, b=60)":  metrics(exact_system(0.0, 0.7, 60.0)),
}

print("Exact corner values  (delta_A, competence):")
for k, v in corners.items():
    print(f"  {k:28s} delta_A = {v[0]:.4f}   competence = {v[1]:.4f}")

# ---------------------------------------------------------------- plots
fig, axes = plt.subplots(1, 3, figsize=(16.5, 4.6))
fig.suptitle(
    r"$\delta_A$ v1 — exact bounded-rational agent, $|F|=|E|=|K|=|A|=8$"
    "  (no sampling; every value exact)", fontsize=12)

im0 = axes[0].imshow(D_es, origin="lower", aspect="auto",
                     extent=[0, 1, 0, 1], vmin=0, vmax=1, cmap="viridis")
axes[0].set_xlabel("environmental stochasticity  s")
axes[0].set_ylabel("education fidelity  e")
axes[0].set_title(r"$\delta_A = H(A|E)/\log_2|A|$   ($\beta=60$)")
fig.colorbar(im0, ax=axes[0])

im1 = axes[1].imshow(C_es, origin="lower", aspect="auto",
                     extent=[0, 1, 0, 1], vmin=0, vmax=1, cmap="magma")
axes[1].set_xlabel("environmental stochasticity  s")
axes[1].set_ylabel("education fidelity  e")
axes[1].set_title(r"competence $= I(A;F)/\log_2|F|$   ($\beta=60$)")
fig.colorbar(im1, ax=axes[1])

axes[2].plot(beta_ax, D_b, label=r"$\delta_A$", lw=2)
axes[2].plot(beta_ax, C_b, label="competence", lw=2)
axes[2].set_xlabel(r"time budget  $\beta$   (s=0.7, e=0.9 fixed)")
axes[2].set_title("time theft: low $\\beta$ fakes freedom\n"
                  "(high $H(A|E)$, zero goal information)")
axes[2].legend()
axes[2].grid(alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.94])
import os
out = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'delta_A_v1.png')
plt.savefig(out, dpi=140)
print("saved:", out)
