# Wiring theorem, hardened — exact floors

3372 configurations; n ∈ {4,6}, s ∈ {0.3,0.5,0.7}, policies lam/hand, m_S ∈ [8, 64, 1024], h ∈ [0, 1, 2, 3, 4, 5, 6, 7]. All exact enumeration (no sampling). Model-world quantities only.

## Refutation hunt

- gated-like (gated, span:1) floors NOT below the sage at h ≥ 1: **5** of 288
  - n=6 s=0.3 hand m_S=8 h=2 gated: floor 0.5642 vs sage 0.5384
  - n=6 s=0.3 hand m_S=8 h=2 span:1: floor 0.5473 vs sage 0.5384
  - n=6 s=0.3 hand m_S=8 h=3 gated: floor 0.5642 vs sage 0.5384
  - n=6 s=0.3 hand m_S=8 h=3 span:1: floor 0.5583 vs sage 0.5384
  - n=6 s=0.3 hand m_S=8 h=4 gated: floor 0.5642 vs sage 0.5384
- additive (printed formula) at h ≥ 3 NOT within 1e-3 of seed-unknown d0: **48** of 144
  - n=4 s=0.3 lam m_S=64 h=3: floor 0.9862 vs d0 0.9997
  - n=4 s=0.3 lam m_S=64 h=4: floor 0.9959 vs d0 0.9997
  - n=4 s=0.3 lam m_S=1024 h=3: floor 0.9868 vs d0 1.0000
  - n=4 s=0.3 lam m_S=1024 h=4: floor 0.9959 vs d0 1.0000
  - n=4 s=0.3 hand m_S=64 h=3: floor 0.9894 vs d0 0.9998
  - n=4 s=0.3 hand m_S=64 h=4: floor 0.9968 vs d0 0.9998
  - n=4 s=0.3 hand m_S=1024 h=3: floor 0.9897 vs d0 1.0000
  - n=4 s=0.3 hand m_S=1024 h=4: floor 0.9971 vs d0 1.0000
  - n=4 s=0.5 lam m_S=64 h=3: floor 0.9845 vs d0 0.9999
  - n=4 s=0.5 lam m_S=64 h=4: floor 0.9972 vs d0 0.9999
  - n=4 s=0.5 lam m_S=1024 h=3: floor 0.9852 vs d0 1.0000
  - n=4 s=0.5 lam m_S=1024 h=4: floor 0.9975 vs d0 1.0000
  - n=4 s=0.5 hand m_S=64 h=3: floor 0.9923 vs d0 0.9999
  - n=4 s=0.5 hand m_S=64 h=4: floor 0.9984 vs d0 0.9999
  - n=4 s=0.5 hand m_S=1024 h=3: floor 0.9922 vs d0 1.0000
  - n=4 s=0.5 hand m_S=1024 h=4: floor 0.9984 vs d0 1.0000
  - n=4 s=0.7 lam m_S=64 h=3: floor 0.9901 vs d0 1.0000
  - n=4 s=0.7 lam m_S=64 h=4: floor 0.9979 vs d0 1.0000
  - n=4 s=0.7 lam m_S=1024 h=3: floor 0.9894 vs d0 1.0000
  - n=4 s=0.7 lam m_S=1024 h=4: floor 0.9976 vs d0 1.0000
- one-time-pad LAW, sufficiency (m_S | m_U, i.e. h ≥ log2 m_S for the printed additive formula ⇒ EXACT equality; proof: the quantile set {(S+0.5)/m_S + (U+0.5)/m_U mod 1} is then the same grid for every S) violated: **0** of 48 predicted-equal configs. Necessity is generic, not exact: 4 configs reach equality early by saturation at d0 = 1 (of 204).
  Gap d0 − floor by h (printed additive, mean over n, s, policy): m_S=8: h=0: 0.5132, h=1: 0.2156, h=2: 0.0516, h=3: -0.0000, h=4: 0.0000; m_S=64: h=0: 0.5171, h=1: 0.2279, h=2: 0.0652, h=3: 0.0101, h=4: 0.0030, h=5: 0.0004, h=6: 0.0000, h=7: 0.0000; m_S=1024: h=0: 0.5177, h=1: 0.2285, h=2: 0.0654, h=3: 0.0101, h=4: 0.0031, h=5: 0.0006, h=6: 0.0001, h=7: 0.0000
  - n=4 s=0.7 lam m_S=64 h=5: floor 0.999989 d0 0.999989 predicted equal=False
  - n=4 s=0.7 hand m_S=64 h=5: floor 0.999989 d0 0.999989 predicted equal=False
  - n=6 s=0.3 lam m_S=64 h=5: floor 0.999986 d0 0.999986 predicted equal=False
  - n=6 s=0.3 hand m_S=64 h=5: floor 0.999986 d0 0.999986 predicted equal=False
- gated inversion MARGIN min over h ≥ 1 and m_S of (sage − floor), per (n, s, policy) — negative = inversion fails:
  | n | s | policy | min margin | wall/sage |
  |---|---|---|---|---|
  | 4 | 0.3 | hand | +0.020 | 0.41 |
  | 4 | 0.3 | lam | +0.188 | 0.12 |
  | 4 | 0.5 | hand | +0.074 | 0.52 |
  | 4 | 0.5 | lam | +0.289 | 0.20 |
  | 4 | 0.7 | hand | +0.084 | 0.63 |
  | 4 | 0.7 | lam | +0.291 | 0.27 |
  | 6 | 0.3 | hand | -0.026 | 0.48 |
  | 6 | 0.3 | lam | +0.206 | 0.09 |
  | 6 | 0.5 | hand | +0.017 | 0.58 |
  | 6 | 0.5 | lam | +0.318 | 0.12 |
  | 6 | 0.7 | hand | +0.067 | 0.68 |
  | 6 | 0.7 | lam | +0.393 | 0.18 |
- T9′ lower wall (wall ≤ every seed-known floor) or h=0 sage wall violated: **0** of 3372

## Floor vs reach (span family), n=4 s=0.5 hand policy, h=3

| m_S | d=1 | d=2 | d=4 | d=8 | d=16 | d=32 | d=64 | d=128 | d=256 | d=512 | d=1024 | additive (printed) | d0 | sage |
|---|---|---|---|---|---|---|---|---|---|---|---|---|---|---|
| 8 | 0.620 | 0.747 | 0.869 | 0.992 |  |  |  |  |  |  |  | 0.984 | 0.984 | 0.774 |
| 64 | 0.592 | 0.592 | 0.592 | 0.625 | 0.749 | 0.871 | 0.992 |  |  |  |  | 0.992 | 1.000 | 0.774 |
| 1024 | 0.592 | 0.592 | 0.592 | 0.592 | 0.592 | 0.592 | 0.592 | 0.624 | 0.749 | 0.871 | 0.992 | 0.992 | 1.000 | 0.774 |

Floor non-decreasing in reach: holds in 175/180 (n,s,policy,m_S,h) groups (violations listed in the CSV by filtering span rows).

REACH LAW check: across habit-space sizes m_S, configurations with the same (n, s, policy, h, reach) have floors differing by at most 0.0000 (36 comparable groups). If this is ~0 the floor is a function of reach alone for the span family -- the dichotomy is the two ends of one curve, parameterized by how far the fresh bits travel across the habit's choice space.

## Random wirings vs the two named ones (mean over random seeds)

| n | s | policy | m_S | h | gated | random (mean ± sd) | additive:c | additive (printed) | d0 | sage |
|---|---|---|---|---|---|---|---|---|---|---|
| 4 | 0.5 | hand | 8 | 1 | 0.667 | 0.793 ± 0.029 | 0.863 | 0.851 | 0.994 | 0.774 |
| 4 | 0.5 | hand | 8 | 2 | 0.700 | 0.907 ± 0.016 | 0.971 | 0.973 | 0.994 | 0.774 |
| 4 | 0.5 | hand | 8 | 3 | 0.697 | 0.947 ± 0.012 | 0.992 | 0.984 | 0.984 | 0.774 |
| 4 | 0.5 | hand | 8 | 4 | 0.692 | 0.977 ± 0.006 | 0.998 | 0.999 | 0.999 | 0.774 |
| 4 | 0.5 | hand | 64 | 1 | 0.633 | 0.785 ± 0.013 | 0.860 | 0.860 | 1.000 | 0.774 |
| 4 | 0.5 | hand | 64 | 2 | 0.637 | 0.895 ± 0.012 | 0.971 | 0.971 | 1.000 | 0.774 |
| 4 | 0.5 | hand | 64 | 3 | 0.637 | 0.948 ± 0.005 | 0.992 | 0.992 | 1.000 | 0.774 |
| 4 | 0.5 | hand | 64 | 4 | 0.636 | 0.974 ± 0.002 | 0.998 | 0.998 | 1.000 | 0.774 |
| 4 | 0.5 | hand | 1024 | 1 | 0.628 | 0.791 ± 0.002 | 0.860 | 0.860 | 1.000 | 0.774 |
| 4 | 0.5 | hand | 1024 | 2 | 0.629 | 0.892 ± 0.003 | 0.971 | 0.971 | 1.000 | 0.774 |
| 4 | 0.5 | hand | 1024 | 3 | 0.629 | 0.948 ± 0.001 | 0.992 | 0.992 | 1.000 | 0.774 |
| 4 | 0.5 | hand | 1024 | 4 | 0.629 | 0.974 ± 0.001 | 0.998 | 0.998 | 1.000 | 0.774 |
| 4 | 0.5 | lam | 8 | 1 | 0.453 | 0.658 ± 0.047 | 0.741 | 0.753 | 0.984 | 0.774 |
| 4 | 0.5 | lam | 8 | 2 | 0.485 | 0.844 ± 0.025 | 0.947 | 0.960 | 0.984 | 0.774 |
| 4 | 0.5 | lam | 8 | 3 | 0.474 | 0.914 ± 0.022 | 0.984 | 0.978 | 0.978 | 0.774 |
| 4 | 0.5 | lam | 8 | 4 | 0.469 | 0.961 ± 0.009 | 0.997 | 0.999 | 0.999 | 0.774 |
| 4 | 0.5 | lam | 64 | 1 | 0.368 | 0.632 ± 0.022 | 0.751 | 0.754 | 1.000 | 0.774 |
| 4 | 0.5 | lam | 64 | 2 | 0.379 | 0.824 ± 0.022 | 0.949 | 0.951 | 1.000 | 0.774 |
| 4 | 0.5 | lam | 64 | 3 | 0.378 | 0.913 ± 0.009 | 0.985 | 0.984 | 1.000 | 0.774 |
| 4 | 0.5 | lam | 64 | 4 | 0.376 | 0.958 ± 0.004 | 0.997 | 0.997 | 1.000 | 0.774 |
| 4 | 0.5 | lam | 1024 | 1 | 0.363 | 0.645 ± 0.004 | 0.751 | 0.751 | 1.000 | 0.774 |
| 4 | 0.5 | lam | 1024 | 2 | 0.363 | 0.819 ± 0.006 | 0.949 | 0.950 | 1.000 | 0.774 |
| 4 | 0.5 | lam | 1024 | 3 | 0.363 | 0.913 ± 0.001 | 0.985 | 0.985 | 1.000 | 0.774 |
| 4 | 0.5 | lam | 1024 | 4 | 0.363 | 0.958 ± 0.001 | 0.998 | 0.997 | 1.000 | 0.774 |
| 6 | 0.5 | hand | 8 | 1 | 0.721 | 0.794 ± 0.015 | 0.822 | 0.822 | 0.993 | 0.753 |
| 6 | 0.5 | hand | 8 | 2 | 0.736 | 0.895 ± 0.011 | 0.950 | 0.948 | 0.993 | 0.753 |
| 6 | 0.5 | hand | 8 | 3 | 0.726 | 0.942 ± 0.010 | 0.993 | 0.981 | 0.981 | 0.753 |
| 6 | 0.5 | hand | 8 | 4 | 0.730 | 0.975 ± 0.006 | 0.997 | 0.997 | 0.997 | 0.753 |
| 6 | 0.5 | hand | 64 | 1 | 0.662 | 0.787 ± 0.005 | 0.821 | 0.821 | 1.000 | 0.753 |
| 6 | 0.5 | hand | 64 | 2 | 0.664 | 0.885 ± 0.007 | 0.949 | 0.949 | 1.000 | 0.753 |
| 6 | 0.5 | hand | 64 | 3 | 0.662 | 0.941 ± 0.005 | 0.993 | 0.993 | 1.000 | 0.753 |
| 6 | 0.5 | hand | 64 | 4 | 0.663 | 0.972 ± 0.002 | 0.997 | 0.997 | 1.000 | 0.753 |
| 6 | 0.5 | hand | 1024 | 1 | 0.654 | 0.788 ± 0.002 | 0.821 | 0.821 | 1.000 | 0.753 |
| 6 | 0.5 | hand | 1024 | 2 | 0.654 | 0.883 ± 0.002 | 0.949 | 0.949 | 1.000 | 0.753 |
| 6 | 0.5 | hand | 1024 | 3 | 0.654 | 0.941 ± 0.001 | 0.993 | 0.993 | 1.000 | 0.753 |
| 6 | 0.5 | hand | 1024 | 4 | 0.654 | 0.971 ± 0.001 | 0.997 | 0.997 | 1.000 | 0.753 |
| 6 | 0.5 | lam | 8 | 1 | 0.403 | 0.576 ± 0.033 | 0.673 | 0.698 | 0.991 | 0.753 |
| 6 | 0.5 | lam | 8 | 2 | 0.435 | 0.780 ± 0.024 | 0.856 | 0.881 | 0.991 | 0.753 |
| 6 | 0.5 | lam | 8 | 3 | 0.420 | 0.881 ± 0.027 | 0.988 | 0.981 | 0.981 | 0.753 |
| 6 | 0.5 | lam | 8 | 4 | 0.425 | 0.948 ± 0.014 | 0.995 | 0.995 | 0.995 | 0.753 |
| 6 | 0.5 | lam | 64 | 1 | 0.302 | 0.558 ± 0.015 | 0.675 | 0.678 | 1.000 | 0.753 |
| 6 | 0.5 | lam | 64 | 2 | 0.306 | 0.758 ± 0.014 | 0.859 | 0.862 | 1.000 | 0.753 |
| 6 | 0.5 | lam | 64 | 3 | 0.304 | 0.878 ± 0.011 | 0.987 | 0.988 | 1.000 | 0.753 |
| 6 | 0.5 | lam | 64 | 4 | 0.305 | 0.943 ± 0.004 | 0.995 | 0.996 | 1.000 | 0.753 |
| 6 | 0.5 | lam | 1024 | 1 | 0.289 | 0.560 ± 0.004 | 0.675 | 0.675 | 1.000 | 0.753 |
| 6 | 0.5 | lam | 1024 | 2 | 0.289 | 0.757 ± 0.004 | 0.859 | 0.859 | 1.000 | 0.753 |
| 6 | 0.5 | lam | 1024 | 3 | 0.289 | 0.879 ± 0.002 | 0.987 | 0.987 | 1.000 | 0.753 |
| 6 | 0.5 | lam | 1024 | 4 | 0.289 | 0.941 ± 0.002 | 0.995 | 0.995 | 1.000 | 0.753 |

Reading: if random wirings sit at the additive:c value, generic wirings are additive-like and the gated wiring is the special (measure-small) structure — the dichotomy becomes 'gated is the exception'. If they sit between, the floor is a continuous function of reach and the dichotomy is the two ends of a curve.
