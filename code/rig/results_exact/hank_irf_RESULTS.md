# HANK port v0.1 — general-equilibrium dynamics, model vs control (2026-11-09)

T = 200. Shocks: monetary (rstar, −25 bp, AR 0.8) and schedule entropy (S, +0.5, AR 0.9). Linear GE responses from sequence-space Jacobians; the fake-news algorithm is run on the bandwidth block's own dense transition operator (states b×e×a), so the stochastic (logit) policy is handled exactly.

## Linear GE response to rstar shock

| horizon | ΔY control | ΔY model | ΔC control | ΔC model | ΔHTM model | ΔBW model | Δr model |
|---|---|---|---|---|---|---|---|
| 0 | +0.00261 | +0.00464 | +0.00261 | +0.00464 | -0.00299 | +0.00000 | -0.00230 |
| 1 | +0.00187 | +0.00298 | +0.00187 | +0.00298 | -0.00340 | +0.00000 | -0.00117 |
| 2 | +0.00134 | +0.00199 | +0.00134 | +0.00199 | -0.00309 | +0.00000 | -0.00069 |
| 4 | +0.00070 | +0.00093 | +0.00070 | +0.00093 | -0.00220 | +0.00002 | -0.00027 |
| 8 | +0.00019 | +0.00025 | +0.00019 | +0.00025 | -0.00127 | +0.00004 | -0.00006 |
| 12 | +0.00003 | +0.00005 | +0.00003 | +0.00005 | -0.00091 | +0.00006 | -0.00000 |
| 20 | -0.00003 | -0.00004 | -0.00003 | -0.00004 | -0.00050 | +0.00008 | +0.00002 |

Cumulative ΔY: control +0.0083, model +0.0132 (ratio 1.580).

## Linear GE response to S shock

| horizon | ΔY control | ΔY model | ΔC control | ΔC model | ΔHTM model | ΔBW model | Δr model |
|---|---|---|---|---|---|---|---|
| 0 | -0.00000 | -0.00250 | -0.00000 | -0.00250 | -0.00050 | +0.00000 | -0.00042 |
| 1 | +0.00000 | -0.00181 | -0.00000 | -0.00181 | -0.00014 | -0.00580 | +0.00011 |
| 2 | +0.00000 | -0.00094 | -0.00000 | -0.00094 | -0.00001 | -0.01047 | +0.00012 |
| 4 | +0.00000 | +0.00017 | -0.00000 | +0.00017 | +0.00029 | -0.01714 | +0.00027 |
| 8 | +0.00000 | +0.00108 | -0.00000 | +0.00108 | +0.00159 | -0.02329 | +0.00051 |
| 12 | -0.00000 | +0.00132 | -0.00000 | +0.00132 | +0.00291 | -0.02401 | +0.00056 |
| 20 | -0.00000 | +0.00119 | -0.00000 | +0.00119 | +0.00427 | -0.01921 | +0.00041 |

Cumulative ΔY: control -0.0000, model +0.0380 (ratio n/a (control does not respond to S)).

control: impact ΔC/ΔY to the monetary shock = 1.000; peak ΔY = +0.00261.
model: impact ΔC/ΔY to the monetary shock = 1.000; peak ΔY = +0.00464.

## Nonlinear GE path through the time gate (model)

A monetary expansion sized so hours cross the middle group's gate (free time Tbar_mid − N < T_gate). Linear and nonlinear paths are compared; the bandwidth drop at the crossing is what linearization misses.

- shock -100 bp: peak N = 1.0216 (gate at 1.050); ΔBW min nonlinear +0.0000 vs linear +0.0000; cum ΔY nonlinear +0.0513 vs linear +0.0527; cum ΔHTM nonlinear -0.1326 vs linear -0.1465  [182s]
- shock -300 bp: peak N = 1.0637 (gate at 1.050); ΔBW min nonlinear -0.0191 vs linear +0.0000; cum ΔY nonlinear +0.2214 vs linear +0.1580; cum ΔHTM nonlinear -0.2560 vs linear -0.4394  [244s]
- shock -500 bp: peak N = 1.1377 (gate at 1.050); ΔBW min nonlinear -0.0374 vs linear +0.0000; cum ΔY nonlinear +0.5043 vs linear +0.2633; cum ΔHTM nonlinear -0.3413 vs linear -0.7324  [247s]

Runtime 911s.
