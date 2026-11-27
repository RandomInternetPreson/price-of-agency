"""
verify_theorems.py -- adversarial numerical check of THEOREMS_v1.md
Every instance is computed by exact enumeration (float64); randomness is
only over *which* channel instances we test, never inside a computed value.

Checks:
  T1  sage identity  delta_A = H(F|E)/log2|A|  on RANDOM channels + priors
  T2  complementarity inequality + equality condition on random instances
  C4  monotonicity hunt: does delta_A or competence ever DECREASE in
      education fidelity e?  Tested at beta = inf-proxy (1e3) and finite
      beta over (a) the symmetric class, (b) random channel classes where
      "education" scales a random K-channel toward identity.
"""
import numpy as np

rng = np.random.default_rng(20260725)
nF = 6; nA = nF

def H(p):
    p = p[p > 0]
    return float(-(p * np.log2(p)).sum())

def system(pF, C_E, C_K, beta):
    p_fek = pF[:, None, None] * C_E[:, :, None] * C_K[:, None, :]
    p_ek = p_fek.sum(axis=0)
    with np.errstate(divide="ignore", invalid="ignore"):
        post = np.nan_to_num(p_fek / p_ek[None], nan=1.0/nF)
    logits = beta * post
    logits -= logits.max(axis=0, keepdims=True)
    pol = np.exp(logits); pol /= pol.sum(axis=0, keepdims=True)
    return p_fek[:, :, :, None] * np.transpose(pol, (1, 2, 0))[None]

def metrics(p, pF):
    p_ea = p.sum(axis=(0, 2)); p_e = p_ea.sum(axis=1)
    dA = (H(p_ea) - H(p_e)) / np.log2(nA)
    p_fa = p.sum(axis=(1, 2))
    comp = (H(p_fa.sum(1)) + H(p_fa.sum(0)) - H(p_fa)) / H(pF)
    return dA, comp

def rand_channel(sharp):
    C = rng.dirichlet(np.full(nF, sharp), size=nF)
    return C

def mix_to_identity(C, e):
    return (1 - e) * C + e * np.eye(nF)

# ---------------- T1: sage identity on random instances -----------------
BETA = 1e3
worst = 0.0
for _ in range(500):
    pF = rng.dirichlet(np.ones(nF))
    C_E = rand_channel(rng.uniform(0.2, 3.0))
    p = system(pF, C_E, np.eye(nF), BETA)          # K = F exactly
    dA, _ = metrics(p, pF)
    p_fe = (pF[:, None] * C_E); p_e = p_fe.sum(0)
    HF_given_E = H(p_fe) - H(p_e)
    worst = max(worst, abs(dA - HF_given_E / np.log2(nA)))
print(f"T1 sage identity, 500 random (prior, channel) instances: "
      f"max |error| = {worst:.2e}")

# ---------------- T2: complementarity on random instances ---------------
viol = 0; eq_hits = 0; worst_gap = 1.0
for _ in range(500):
    pF = np.full(nF, 1/nF)                          # uniform prior branch
    C_E = rand_channel(rng.uniform(0.2, 3.0))
    d_sage, _ = metrics(system(pF, C_E, np.eye(nF), BETA), pF)
    C_null = np.tile(pF, (nF, 1))                   # K independent of F
    _, c_rock = metrics(system(pF, C_E, C_null, BETA), pF)
    ssum = d_sage + c_rock
    if ssum > 1 + 1e-9: viol += 1
    if abs(ssum - 1) < 1e-9: eq_hits += 1
    worst_gap = min(worst_gap, 1 - ssum)
print(f"T2 complementarity, 500 instances: violations = {viol}, "
      f"exact-equality cases = {eq_hits}, min slack = {worst_gap:.4f}")

# ---------------- C4: monotonicity counterexample hunt ------------------
def hunt(beta, klass, trials=400, steps=21):
    bad_d = bad_c = 0; worst_drop = 0.0; example = None
    for _ in range(trials):
        pF = np.full(nF, 1/nF)
        C_E = (rand_channel(rng.uniform(0.2, 3.0)) if klass == "random"
               else mix_to_identity(np.tile(pF, (nF, 1)),
                                    1 - rng.uniform(0, 1)))
        C_K0 = rand_channel(rng.uniform(0.2, 3.0)) if klass == "random" \
               else np.tile(pF, (nF, 1))
        prev = None
        for e in np.linspace(0, 1, steps):
            m = metrics(system(pF, C_E, mix_to_identity(C_K0, e), beta), pF)
            if prev is not None:
                dd, dc = m[0] - prev[0], m[1] - prev[1]
                if dd < -1e-9:
                    bad_d += 1
                    if dd < worst_drop: worst_drop, example = dd, (e, beta, "delta_A")
                if dc < -1e-9:
                    bad_c += 1
                    if dc < worst_drop: worst_drop, example = dc, (e, beta, "competence")
            prev = m
    return bad_d, bad_c, worst_drop, example

for beta, klass in [(1e3, "symmetric"), (1e3, "random"),
                    (8.0, "symmetric"), (8.0, "random"),
                    (2.0, "random")]:
    bd, bc, wd, ex = hunt(beta, klass)
    print(f"C4 hunt  beta={beta:>6}  class={klass:9s}  "
          f"delta_A drops={bd:4d}  competence drops={bc:4d}  "
          f"worst drop={wd:+.4e}  at={ex}")
