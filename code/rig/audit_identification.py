"""
audit_identification.py -- stress objective #7: can the field audit tell a time GATE from a time SLOPE,
and at what sample size? A design study, not a result about the world.

Data-generating process (reduced form of the book's bandwidth block, individual level):
  each worker i has a free-time floor T_i ~ U(T_lo, T_hi) (continuous, unlike the three skill groups of
  the HANK), bandwidth b_i in {0..Nb-1} following the Markov law
      up   w.p. p_up * g(T_i)     where g = 1[T >= gate]           (GATE)
                                     or g = clip((T - gate + w)/(2w), 0, 1)   (RAMP of half-width w; w -> large = slope)
      down w.p. s_i (entropy, iid across workers around a mean)
  observed at stationarity: T_obs = T_i + measurement error N(0, sigma_T), and an outcome
      HtM_i ~ Bernoulli( logistic(alpha - gamma * b_i / (Nb-1)) ).
Audit test: fit (1) logistic HtM ~ T_obs (slope) and (2) logistic HtM ~ 1[T_obs >= c] with c on a grid
(step, threshold estimated), compare by BIC. Also (3) step + slope vs slope alone: likelihood-ratio test
at 5% with a Davies-type correction (threshold estimated -> bootstrap-free conservative: use the max-LR
distribution simulated under the slope DGP). Power = P(gate detected | GATE DGP); size = P(gate detected
| RAMP DGP with the widest ramp). Sweeps N, sigma_T, ramp width. ~5 minutes CPU.
Writes code/rig/results_exact/audit_identification.md and figures/audit_identification.png.
"""
import os, time
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
RES = os.path.join(HERE, 'results_exact'); FIG = os.path.normpath(os.path.join(HERE, '..', '..', 'figures'))
rng = np.random.default_rng(7)
Nb = 4; p_up = 0.16; s_mean = 0.08; gate = 1.0; T_lo, T_hi = 0.5, 1.5
alpha, gamma = 1.0, 2.5          # HtM probability 0.73 at b=0, 0.18 at b=3


def stationary_b(g_i, s_i):
    """Stationary distribution of the birth-death bandwidth chain per worker (vectorized over workers)."""
    up = p_up * g_i; down = s_i
    # birth-death chain: pi_b proportional to prod (up/down)
    ratio = np.where(down > 1e-12, up / np.maximum(down, 1e-12), 1e6)
    w = np.ones((len(g_i), Nb))
    for b in range(1, Nb):
        w[:, b] = w[:, b - 1] * ratio
    w = np.where(np.isfinite(w), w, 1e6); w = np.minimum(w, 1e12)
    return w / w.sum(1, keepdims=True)


def simulate(N, sigma_T, ramp_w):
    T = rng.uniform(T_lo, T_hi, N)
    g = (T >= gate).astype(float) if ramp_w == 0 else np.clip((T - gate + ramp_w) / (2 * ramp_w), 0, 1)
    s = np.clip(rng.normal(s_mean, 0.03, N), 0.01, 0.5)
    pi = stationary_b(g, s)
    b = (rng.uniform(size=N)[:, None] > pi.cumsum(1)).sum(1)
    p = 1 / (1 + np.exp(-(alpha - gamma * b / (Nb - 1))))
    y = (rng.uniform(size=N) < p).astype(float)
    return T + rng.normal(0, sigma_T, N), y


def logit_fit(X, y, iters=25):
    """Newton logistic regression; returns log-likelihood."""
    X = np.column_stack([np.ones(len(y)), X]); beta = np.zeros(X.shape[1])
    for _ in range(iters):
        z = X @ beta; p = 1 / (1 + np.exp(-z)); W = p * (1 - p) + 1e-9
        grad = X.T @ (y - p); Hm = (X * W[:, None]).T @ X
        step = np.linalg.solve(Hm + 1e-8 * np.eye(len(beta)), grad)
        beta += step
        if np.max(np.abs(step)) < 1e-8: break
    z = X @ beta; p = np.clip(1 / (1 + np.exp(-z)), 1e-12, 1 - 1e-12)
    return float((y * np.log(p) + (1 - y) * np.log(1 - p)).sum())


def tests(Tobs, y, grid):
    ll_slope = logit_fit(Tobs[:, None], y)
    best_step, best_both = -np.inf, -np.inf
    for c in grid:
        step = (Tobs >= c).astype(float)
        best_step = max(best_step, logit_fit(step[:, None], y))
        best_both = max(best_both, logit_fit(np.column_stack([Tobs, step]), y))
    N = len(y)
    bic_slope = -2 * ll_slope + 2 * np.log(N); bic_step = -2 * best_step + 3 * np.log(N)   # threshold counts as a parameter
    LR = 2 * (best_both - ll_slope)
    return bic_step < bic_slope, LR


def run():
    t0 = time.time(); grid = np.linspace(0.6, 1.4, 33); R = 200
    lines = ["# Field-audit identification: gate vs slope (design study, 2026-11-09)", "",
             f"DGP: {Nb} bandwidth levels, p_up = {p_up}, mean entropy drain {s_mean}, free time U({T_lo},{T_hi}), gate at {gate}; "
             f"HtM logistic in bandwidth (α={alpha}, γ={gamma}). {R} replications per cell. "
             "Detection rule A: BIC prefers the step model over the slope model. Rule B: max-LR test (step added to slope) "
             "with critical value = 95th percentile of the same statistic under the widest-ramp DGP (size-controlled by construction).", ""]
    Ns = [1000, 3000, 10000, 30000]; sigmas = [0.0, 0.1, 0.2]; ramps = [0.0, 0.1, 0.25, 0.5]
    # critical values under the slope-like DGP (ramp 0.5) per (N, sigma)
    crit = {}
    for N in Ns:
        for sg in sigmas:
            LRs = [tests(*simulate(N, sg, 0.5), grid)[1] for _ in range(R)]
            crit[(N, sg)] = float(np.percentile(LRs, 95))
    lines += ["## Power of detecting the gate (DGP = sharp gate), by N and measurement error σ_T", "",
              "| N | σ_T | rule A (BIC) | rule B (max-LR, 5%) | LR critical value |", "|---|---|---|---|---|"]
    power = {}
    for N in Ns:
        for sg in sigmas:
            A, B = [], []
            for _ in range(R):
                a, lr = tests(*simulate(N, sg, 0.0), grid); A.append(a); B.append(lr > crit[(N, sg)])
            power[(N, sg)] = (np.mean(A), np.mean(B))
            lines.append(f"| {N} | {sg} | {np.mean(A):.2f} | {np.mean(B):.2f} | {crit[(N, sg)]:.1f} |")
        print(f"N={N} done [{time.time()-t0:.0f}s]", flush=True)
    lines += ["", "## Detection rate when the DGP is a RAMP (σ_T = 0.1): how wide a slope still reads as a gate", "",
              "| N | ramp half-width | rule A | rule B |", "|---|---|---|---|"]
    ramp_res = {}
    for N in [3000, 10000]:
        for w in ramps:
            A, B = [], []
            for _ in range(R):
                a, lr = tests(*simulate(N, 0.1, w), grid); A.append(a); B.append(lr > crit[(N, 0.1)])
            ramp_res[(N, w)] = (np.mean(A), np.mean(B))
            lines.append(f"| {N} | {w} | {np.mean(A):.2f} | {np.mean(B):.2f} |")
    lines += ["", "Reading. Rule B is size-controlled at the widest ramp by construction (0.05 there). The question the table "
              "answers is the audit's: at ATUS/SHED-scale samples (10,000–30,000) and measurement error of a tenth of an hour-"
              "unit, is a sharp gate distinguishable from a ramp of a given width? Where the ramp column equals the gate "
              "column, the audit cannot tell them apart at that N. Nothing here is a statement about the world; the DGP is "
              "the book's own block, reduced to one worker.", f"Runtime {time.time()-t0:.0f}s."]
    os.makedirs(RES, exist_ok=True); open(os.path.join(RES, 'audit_identification.md'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
    import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt
    fig, ax = plt.subplots(1, 2, figsize=(9, 3.6))
    for sg in sigmas:
        ax[0].plot(Ns, [power[(N, sg)][1] for N in Ns], 'o-', label=f'σ_T = {sg}')
    ax[0].set_xscale('log'); ax[0].set_xlabel('N'); ax[0].set_ylabel('power (rule B)'); ax[0].set_title('detecting a sharp gate'); ax[0].legend(fontsize=8)
    for N in [3000, 10000]:
        ax[1].plot(ramps, [ramp_res[(N, w)][1] for w in ramps], 's-', label=f'N = {N}')
    ax[1].axhline(0.05, c='gray', ls='--', lw=0.7); ax[1].set_xlabel('ramp half-width (0 = gate)'); ax[1].set_ylabel('detection rate'); ax[1].set_title('a ramp read as a gate'); ax[1].legend(fontsize=8)
    plt.tight_layout(); os.makedirs(FIG, exist_ok=True); plt.savefig(os.path.join(FIG, 'audit_identification.png'), dpi=130)
    print('\n'.join(lines))


if __name__ == '__main__':
    run()
