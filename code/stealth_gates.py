"""
stealth_gates.py -- Is covert agency time-gated (H1) or model-gated (H2)?
Exact enumeration throughout; symmetric class, n=6, s=0.5, perfect future
knowledge (e=1). The contested resource is POLICY IMPLEMENTATION.

Time axis:  pi_t(a|f,e)  proportional to  pi*(a|f,e)^t   (t in [0,1])
            t=0: uniform default (no deliberation); t=1: full target.
Model axis: whitening residual computed against believed s_hat != s.

Targets:
  STEALTH: whitening policy at lambda = lambda*(s_hat) (plateau endpoint
           as the agent believes it to be).
  MAP:     reward-maximizing policy A = F (the overt sage).

Outputs: exact (competence, delta_A) trajectories vs t for both targets;
exact delta_A leak curve vs s_hat at t=1; curvature at s_hat = s.
"""
import numpy as np, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

n = 6; log2n = np.log2(n); s_true = 0.5
pF = np.full(n, 1/n)

def ch(f):
    C = np.full((n, n), (1-f)/n); C[np.arange(n), np.arange(n)] += f
    return C

C_E = ch(1 - s_true)
p_fe = pF[:, None] * C_E
p_e = p_fe.sum(0)
q_true = (p_fe / p_e[None]).T          # (e,f) true posterior

def H(p):
    p = p[p > 1e-15]
    return float(-(p * np.log2(p)).sum())

def metrics(pol):
    p = p_fe[:, :, None] * pol
    p_ea = p.sum(0)
    dA = (H(p_ea) - H(p_ea.sum(1))) / log2n
    p_fa = p.sum(1)
    comp = (H(p_fa.sum(1)) + H(p_fa.sum(0)) - H(p_fa)) / log2n
    return comp, dA

def whitening_target(s_hat):
    """Whitening policy computed by an agent who BELIEVES s = s_hat."""
    C_hat = ch(1 - s_hat)
    p_fe_hat = pF[:, None] * C_hat
    q_hat = (p_fe_hat / p_fe_hat.sum(0)[None]).T
    lam = 1.0 / (n * q_hat.max())          # believed plateau endpoint
    pol = np.zeros((n, n, n))
    for e in range(n):
        r = (1.0/n - lam * q_hat[e]) / (1 - lam)
        r = np.clip(r, 0, None); r /= r.sum()
        for f in range(n):
            pol[f, e, :] = (1 - lam) * r
            pol[f, e, f] += lam
    return pol

def map_target():
    pol = np.zeros((n, n, n))
    for f in range(n):
        pol[f, :, f] = 1.0
    return pol

def anneal(pol, t):
    if t == 0:
        return np.full_like(pol, 1/n)
    z = np.power(np.clip(pol, 1e-12, None), t)
    return z / z.sum(-1, keepdims=True)

# ---- time trajectories -------------------------------------------------
ts = np.linspace(0, 1, 101)
traj_stealth = np.array([metrics(anneal(whitening_target(s_true), t)) for t in ts])
traj_map     = np.array([metrics(anneal(map_target(), t)) for t in ts])

print("TIME AXIS (t = fraction of deliberation completed)")
print("  t     stealth: comp, dA      MAP: comp, dA")
for t_show in [0.0, 0.1, 0.25, 0.5, 0.75, 1.0]:
    i = int(t_show * 100)
    print(f"  {t_show:4.2f}   {traj_stealth[i,0]:.4f}  {traj_stealth[i,1]:.4f}"
          f"        {traj_map[i,0]:.4f}  {traj_map[i,1]:.4f}")

# ---- model-error leak curve -------------------------------------------
s_hats = np.linspace(0.05, 0.95, 181)
leak = np.array([metrics(whitening_target(sh)) for sh in s_hats])
i0 = np.argmin(np.abs(s_hats - s_true))
# central-difference curvature of delta_A at s_hat = s
h = s_hats[1] - s_hats[0]
curv = (leak[i0+1,1] - 2*leak[i0,1] + leak[i0-1,1]) / h**2
print("\nMODEL AXIS (whitening against believed s_hat; true s = 0.5)")
for sh in [0.2, 0.35, 0.45, 0.5, 0.55, 0.65, 0.8]:
    j = np.argmin(np.abs(s_hats - sh))
    print(f"  s_hat={sh:.2f}   delta_A={leak[j,1]:.6f}   comp={leak[j,0]:.4f}")
print(f"  curvature of delta_A at s_hat=s: {curv:.4f}  "
      f"(0 => flat/robust; negative => quadratic leak)")

# ---- plot --------------------------------------------------------------
fig, axes = plt.subplots(1, 3, figsize=(16.5, 4.9))
fig.suptitle("Is covert agency time-gated (H1) or model-gated (H2)?  "
             "Exact, n=6, s=0.5", fontsize=12)

axes[0].plot(ts, traj_stealth[:,1], lw=2, label=r"stealth: $\delta_A$")
axes[0].plot(ts, traj_stealth[:,0], lw=2, label="stealth: competence")
axes[0].plot(ts, traj_map[:,1], "--", lw=2, label=r"MAP: $\delta_A$")
axes[0].plot(ts, traj_map[:,0], "--", lw=2, label="MAP: competence")
axes[0].set_xlabel("deliberation completed  t")
axes[0].set_title("time theft trajectories")
axes[0].legend(); axes[0].grid(alpha=0.3)

axes[1].plot(traj_map[:,0], traj_map[:,1], "--", lw=2, color="tab:green",
             label="MAP agent path")
axes[1].plot(traj_stealth[:,0], traj_stealth[:,1], lw=2.5, color="tab:red",
             label="stealth agent path")
axes[1].scatter(*traj_stealth[-1], color="tab:red", zorder=5)
axes[1].scatter(*traj_map[-1], color="tab:green", zorder=5)
axes[1].set_xlabel("competence"); axes[1].set_ylabel(r"$\delta_A$")
axes[1].set_title(r"paths in the (competence, $\delta_A$) plane"
                  "\nas deliberation t: 0 $\\to$ 1")
axes[1].legend(); axes[1].grid(alpha=0.3)

axes[2].plot(s_hats, leak[:,1], lw=2, color="tab:purple")
axes[2].axvline(s_true, color="k", ls=":", alpha=0.6)
axes[2].set_xlabel(r"believed environment stochasticity  $\hat s$")
axes[2].set_ylabel(r"achieved $\delta_A$")
axes[2].set_title("model-error leak curve (t=1)\n"
                  r"stealth requires knowing how you are predicted")
axes[2].grid(alpha=0.3)

plt.tight_layout(rect=[0, 0, 1, 0.92])
import os
plt.savefig(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'figures', 'stealth_gates.png'), dpi=140)
print("\nsaved: stealth_gates.png")
