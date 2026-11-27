"""
frontier_attack.py -- T6: Pareto frontier in (competence, delta_A), e=1 class.

Candidate [CONJECTURE]: the "mixing sage" A = F w.p. lambda, uniform noise
otherwise. Closed form via h_n(alpha) = entropy of a symmetric row with
match prob alpha + (1-alpha)/n:
    competence(lam) = 1 - h_n(lam)/log2(n)
    delta_A(lam)    = h_n(lam*(1-s))/log2(n)
(uses: composition of 'identity w.p. a else uniform' channels multiplies a.)

Attack: maximize  J = H(A|E) + gamma * I(A;F)  over ALL policies p(a|f,e)
(full 6x6x6 = 216 parameters, softmax parametrization, Adam with analytic-
free finite-difference-free exact gradients via autodiff-by-hand? No --
we use simple numerical gradient-free? No: use exact gradients computed
with complex-step? Simplest robust: projected mirror ascent with exact
gradient of J computed by autograd-style manual differentiation is
error-prone; we instead use finite-difference Adam, feasible at this size.)
Multiple restarts, gamma swept over a grid; every optimized point is
compared against the candidate curve. Any point ABOVE the curve at equal
competence refutes the conjecture and is recorded.
"""
import numpy as np

rng = np.random.default_rng(7)
n = 6
s = 0.5
log2n = np.log2(n)
pF = np.full(n, 1.0 / n)


def ch(f):
    C = np.full((n, n), (1 - f) / n)
    C[np.arange(n), np.arange(n)] += f
    return C

C_E = ch(1 - s)                      # p(e|f)
p_fe = pF[:, None] * C_E             # joint (f,e)
p_e = p_fe.sum(0)
p_f_given_e = (p_fe / p_e[None]).T   # (e,f)


def H(p):
    p = p[p > 1e-15]
    return float(-(p * np.log2(p)).sum())


def objective(pol, gamma):
    """pol: (f,e,a) conditional p(a|f,e). Returns J, comp, dA."""
    # joint p(f,e,a)
    p = p_fe[:, :, None] * pol
    p_ea = p.sum(0)
    H_A_given_E = H(p_ea) - H(p_ea.sum(1))
    p_fa = p.sum(1)
    I_AF = H(p_fa.sum(1)) + H(p_fa.sum(0)) - H(p_fa)
    return H_A_given_E + gamma * I_AF, I_AF / log2n, H_A_given_E / log2n


def softmax(z):
    z = z - z.max(-1, keepdims=True)
    e = np.exp(z)
    return e / e.sum(-1, keepdims=True)


def optimize(gamma, iters=300, lr=0.25, restarts=6):
    best = (-np.inf, None, None)
    for r in range(restarts):
        z = rng.normal(0, 1.0, size=(n, n, n))
        m = np.zeros_like(z); v = np.zeros_like(z)
        for t in range(1, iters + 1):
            # finite-difference gradient (central), vectorized per-coordinate
            # is too slow; use SPSA (simultaneous perturbation) x4 averaged
            g = np.zeros_like(z)
            for _ in range(4):
                delta = rng.choice([-1.0, 1.0], size=z.shape)
                eps = 1e-3
                Jp, _, _ = objective(softmax(z + eps * delta), gamma)
                Jm, _, _ = objective(softmax(z - eps * delta), gamma)
                g += (Jp - Jm) / (2 * eps) * delta
            g /= 4
            m = 0.9 * m + 0.1 * g
            v = 0.999 * v + 0.001 * g * g
            z += lr * m / (np.sqrt(v) + 1e-8)
        J, comp, dA = objective(softmax(z), gamma)
        if J > best[0]:
            best = (J, comp, dA)
    return best[1], best[2]


def h_n(alpha):
    row = np.full(n, (1 - alpha) / n)
    row[0] += alpha
    return H(row)


# candidate curve
lams = np.linspace(0, 1, 401)
cand = np.array([[1 - h_n(l) / log2n, h_n(l * (1 - s)) / log2n] for l in lams])

# attack
print("gamma sweep -- optimized (competence, delta_A) vs candidate curve")
print(f"{'gamma':>6} {'comp':>8} {'dA_opt':>8} {'dA_cand':>9} {'excess':>9}")
records = []
for gamma in [0.0, 0.2, 0.4, 0.6, 0.8, 1.0, 1.3, 1.7, 2.2, 3.0, 5.0]:
    comp, dA = optimize(gamma)
    dA_cand = float(np.interp(comp, cand[:, 0], cand[:, 1]))
    records.append((comp, dA, dA_cand))
    print(f"{gamma:6.1f} {comp:8.4f} {dA:8.4f} {dA_cand:9.4f} {dA - dA_cand:+9.4f}")

worst = max(r[1] - r[2] for r in records)
print(f"\nmax excess over candidate curve across all attacks: {worst:+.4f}")
print("(positive beyond optimizer noise => candidate REFUTED; "
      "negative/zero => candidate survives as [NUMERICAL])")

import os
np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', 'frontier_candidate.npy'), cand)
np.save(os.path.join(os.path.dirname(os.path.abspath(__file__)), 'results', 'frontier_attacks.npy'), np.array(records))
