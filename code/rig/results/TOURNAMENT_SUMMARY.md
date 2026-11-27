# Neural-watcher tournament — summary (112 configurations)

Floors = mean log-loss over the last quarter of the lifetime, in units of log2 n. 'exact floor' = seed-known enumeration (the book's δ_∞). 'conv' = ok when the exact Bayesian's simulated reading is within 0.01 of its exact floor by the last eighth of life (else the lifetime was too short for that habit space; treat learned floors there as upper bounds on what a longer watch extracts). 'wall' = I(A;F|E)/log n, the T9′ lower wall. All quantities are model-world (n, s fixed).

## Q3 / Q5 — how much watcher does the inversion cost; dichotomy on random wirings and large habit spaces

### n = 4, watcher sees EA

| policy/wiring/m_S/h | sage | wall | d0 (seed unk.) | exact floor | wrong-Bayes | best miner | gru-l | tf-l | inv exact | inv learned | conv |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hand / additive / 8 / 1 | 0.774 | 0.399 | 0.994 | 0.851 | 1.312 | 0.873 | 0.853 | 0.853 | no | no | ok |
| hand / additive / 8 / 2 | 0.774 | 0.399 | 0.994 | 0.973 | 1.288 | 0.993 | 0.973 | 0.973 | no | no | ok |
| hand / additive / 8 / 3 | 0.774 | 0.399 | 0.984 | 0.984 | 1.388 | 0.999 | 0.984 | 0.984 | no | no | ok |
| hand / additive / 1024 / 1 | 0.774 | 0.399 | 1.000 | 0.860 | 1.271 | 0.870 | 0.860 | 0.860 | no | no | ok |
| hand / additive / 1024 / 2 | 0.774 | 0.399 | 1.000 | 0.971 | 1.367 | 0.981 | 0.971 | 0.971 | no | no | ok |
| hand / additive / 1024 / 3 | 0.774 | 0.399 | 1.000 | 0.992 | 1.422 | 1.002 | 0.993 | 0.993 | no | no | ok |
| hand / gated / 8 / 1 | 0.774 | 0.399 | 0.999 | 0.667 | 0.889 | 0.687 | 0.667 | 0.667 | yes | yes | ok |
| hand / gated / 8 / 2 | 0.774 | 0.399 | 1.000 | 0.700 | 0.947 | 0.720 | 0.700 | 0.700 | yes | yes | ok |
| hand / gated / 8 / 3 | 0.774 | 0.399 | 1.000 | 0.697 | 1.014 | 0.712 | 0.697 | 0.697 | yes | yes | ok |
| hand / gated / 1024 / 1 | 0.774 | 0.399 | 1.000 | 0.628 | 0.853 | 0.638 | 0.629 | 0.629 | yes | yes | ok |
| hand / gated / 1024 / 2 | 0.774 | 0.399 | 1.000 | 0.629 | 0.935 | 0.638 | 0.629 | 0.629 | yes | yes | ok |
| hand / gated / 1024 / 3 | 0.774 | 0.399 | 1.000 | 0.629 | 0.951 | 0.638 | 0.629 | 0.629 | yes | yes | ok |
| hand / random:1 / 8 / 1 | 0.774 | 0.399 | 0.999 | 0.833 | 1.227 | 0.852 | 0.833 | 0.833 | no | no | ok |
| hand / random:1 / 8 / 2 | 0.774 | 0.399 | 1.000 | 0.909 | 1.159 | 0.927 | 0.906 | 0.906 | no | no | ok |
| hand / random:1 / 8 / 3 | 0.774 | 0.399 | 1.000 | 0.956 | 1.294 | 0.974 | 0.955 | 0.956 | no | no | ok |
| hand / random:1 / 1024 / 1 | 0.774 | 0.399 | 1.000 | 0.789 | 1.018 | 0.801 | 0.791 | 0.791 | no | no | ok |
| hand / random:1 / 1024 / 2 | 0.774 | 0.399 | 1.000 | 0.893 | 1.207 | 0.902 | 0.892 | 0.894 | no | no | ok |
| hand / random:1 / 1024 / 3 | 0.774 | 0.399 | 1.000 | 0.948 | 1.320 | 0.958 | 0.951 | 0.952 | no | no | ok |
| lam / additive / 8 / 1 | 0.774 | 0.142 | 0.984 | 0.753 | 1.562 | 0.775 | 0.755 | 0.755 | yes | yes | ok |
| lam / additive / 8 / 2 | 0.774 | 0.142 | 0.984 | 0.960 | 1.352 | 0.980 | 0.961 | 0.961 | no | no | ok |
| lam / additive / 8 / 3 | 0.774 | 0.142 | 0.978 | 0.978 | 1.441 | 0.993 | 0.978 | 0.978 | no | no | ok |
| lam / additive / 1024 / 1 | 0.774 | 0.142 | 1.000 | 0.751 | 1.369 | 0.763 | 0.753 | 0.753 | yes | yes | ok |
| lam / additive / 1024 / 2 | 0.774 | 0.142 | 1.000 | 0.950 | 1.459 | 0.959 | 0.950 | 0.950 | no | no | ok |
| lam / additive / 1024 / 3 | 0.774 | 0.142 | 1.000 | 0.985 | 1.543 | 0.995 | 0.986 | 0.986 | no | no | ok |
| lam / gated / 8 / 1 | 0.774 | 0.142 | 0.999 | 0.453 | 0.832 | 0.472 | 0.453 | 0.453 | yes | yes | ok |
| lam / gated / 8 / 2 | 0.774 | 0.142 | 0.999 | 0.485 | 0.948 | 0.505 | 0.485 | 0.485 | yes | yes | ok |
| lam / gated / 8 / 3 | 0.774 | 0.142 | 1.000 | 0.474 | 1.021 | 0.488 | 0.473 | 0.473 | yes | yes | ok |
| lam / gated / 1024 / 1 | 0.774 | 0.142 | 1.000 | 0.363 | 0.679 | 0.370 | 0.361 | 0.361 | yes | yes | ok |
| lam / gated / 1024 / 2 | 0.774 | 0.142 | 1.000 | 0.363 | 0.870 | 0.371 | 0.361 | 0.361 | yes | yes | ok |
| lam / gated / 1024 / 3 | 0.774 | 0.142 | 1.000 | 0.363 | 0.910 | 0.371 | 0.361 | 0.361 | yes | yes | ok |
| lam / random:1 / 8 / 1 | 0.774 | 0.142 | 0.999 | 0.718 | 1.389 | 0.734 | 0.715 | 0.715 | yes | yes | ok |
| lam / random:1 / 8 / 2 | 0.774 | 0.142 | 0.999 | 0.850 | 1.161 | 0.866 | 0.846 | 0.846 | no | no | ok |
| lam / random:1 / 8 / 3 | 0.774 | 0.142 | 1.000 | 0.931 | 1.362 | 0.948 | 0.929 | 0.930 | no | no | ok |
| lam / random:1 / 1024 / 1 | 0.774 | 0.142 | 1.000 | 0.641 | 1.047 | 0.658 | 0.648 | 0.648 | yes | yes | ok |
| lam / random:1 / 1024 / 2 | 0.774 | 0.142 | 1.000 | 0.824 | 1.296 | 0.833 | 0.824 | 0.825 | no | no | ok |
| lam / random:1 / 1024 / 3 | 0.774 | 0.142 | 1.000 | 0.913 | 1.432 | 0.923 | 0.916 | 0.917 | no | no | ok |

**Gated configs (h ≥ 1): exact watcher inverted in 28/28; the trained watcher of the config inverted in 28/28.**

Additive at h = 3 (one-time-pad equality claims δ_∞ = seed-unknown): max |exact − d0| = 0.0148; learned floors minus d0: -0.014 … +0.000 (a learned watcher cannot beat d0 here except by noise; negative values of size > 0.01 would refute equality).

Random wirings: exact floors h=1: 0.745, h=2: 0.869, h=3: 0.937 (sage 0.774); gated-like if below the sage at every h, additive-like if rising to d0.

## Q7 — the regress: floors vs coin generator (h = 3 nominal bits, m_S = 8, T = 512)

| policy/wiring/gen | sage | wall | d0 (seed unk.) | exact floor | wrong-Bayes | best miner | gru-l | tf-l | inv exact | inv learned | conv |
|---|---|---|---|---|---|---|---|---|---|---|---|
| hand / additive / iid | 0.774 | 0.399 | 0.984 | 0.984 | 1.389 | 0.994 | 0.984 | 0.984 | no | no | ok |
| hand / additive / lcg:12 | 0.774 | 0.399 | 0.984 | 0.984 | 1.388 | 0.994 | 0.795 | 0.983 | no | no | ok |
| hand / additive / lcg:16 | 0.774 | 0.399 | 0.984 | 0.984 | 1.388 | 0.994 | 0.982 | 0.984 | no | no | ok |
| hand / additive / lcg:32 | 0.774 | 0.399 | 0.984 | 0.984 | 1.387 | 0.994 | 0.984 | 0.984 | no | no | ok |
| hand / additive / lcg:8 | 0.774 | 0.399 | 0.984 | 0.984 | 1.388 | 0.994 | 0.812 | 0.589 | no | yes | ok |
| hand / gated / iid | 0.774 | 0.399 | 1.000 | 0.697 | 1.014 | 0.707 | 0.698 | 0.698 | yes | yes | ok |
| hand / gated / lcg:12 | 0.774 | 0.399 | 1.000 | 0.697 | 1.014 | 0.708 | 0.698 | 0.698 | yes | yes | ok |
| hand / gated / lcg:16 | 0.774 | 0.399 | 1.000 | 0.697 | 1.014 | 0.708 | 0.699 | 0.699 | yes | yes | ok |
| hand / gated / lcg:32 | 0.774 | 0.399 | 1.000 | 0.697 | 1.014 | 0.708 | 0.699 | 0.699 | yes | yes | ok |
| hand / gated / lcg:8 | 0.774 | 0.399 | 1.000 | 0.697 | 1.014 | 0.708 | 0.698 | 0.699 | yes | yes | ok |
| lam / additive / iid | 0.774 | 0.142 | 0.978 | 0.978 | 1.443 | 0.987 | 0.978 | 0.978 | no | no | ok |
| lam / additive / lcg:12 | 0.774 | 0.142 | 0.978 | 0.978 | 1.441 | 0.988 | 0.359 | 0.976 | no | yes | ok |
| lam / additive / lcg:16 | 0.774 | 0.142 | 0.978 | 0.978 | 1.441 | 0.988 | 0.898 | 0.978 | no | no | ok |
| lam / additive / lcg:32 | 0.774 | 0.142 | 0.978 | 0.978 | 1.441 | 0.988 | 0.978 | 0.978 | no | no | ok |
| lam / additive / lcg:8 | 0.774 | 0.142 | 0.978 | 0.978 | 1.443 | 0.989 | 0.343 | 0.349 | no | yes | ok |
| lam / gated / iid | 0.774 | 0.142 | 1.000 | 0.474 | 1.021 | 0.483 | 0.473 | 0.473 | yes | yes | ok |
| lam / gated / lcg:12 | 0.774 | 0.142 | 1.000 | 0.474 | 1.021 | 0.483 | 0.473 | 0.473 | yes | yes | ok |
| lam / gated / lcg:16 | 0.774 | 0.142 | 1.000 | 0.474 | 1.020 | 0.484 | 0.475 | 0.475 | yes | yes | ok |
| lam / gated / lcg:32 | 0.774 | 0.142 | 1.000 | 0.474 | 1.021 | 0.484 | 0.474 | 0.474 | yes | yes | ok |
| lam / gated / lcg:8 | 0.774 | 0.142 | 1.000 | 0.474 | 1.020 | 0.484 | 0.401 | 0.474 | yes | yes | ok |

Reading: under 'iid' the nominal coin is real. Under lcg:k the coin is a deterministic map of a k-bit hidden seed — a habit one level up. If a learned watcher's floor falls with k while the fresh-coin Bayesian's does not, the watcher has acquired the generator (the regress in action); the gap between them is the price of assuming freshness.

## Figures
- `fig_floors_vs_h.png`
- `fig_lifetimes_large_mS.png`
- `fig_regress.png`

Compute: 10.89 GPU-hours across 112 configs; devices ['cuda:0'].
