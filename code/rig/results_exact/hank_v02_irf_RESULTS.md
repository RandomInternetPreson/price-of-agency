# HANK v0.2 dynamics — own hours, flexible wage (2026-11-09)

T = 150; monetary shock −25 bp AR 0.8; entropy shock +0.5 AR 0.9.

## Linear GE response to rstar

| h | ΔY ctrl | ΔY model | ΔN model | Δw model | ΔBELOW model | ΔBW model | ΔHTM model |
|---|---|---|---|---|---|---|---|
| 0 | +0.00231 | +0.00160 | +0.00160 | +0.00549 | -0.00019 | +0.00000 | -0.00396 |
| 1 | +0.00166 | +0.00157 | +0.00157 | +0.00498 | +0.00169 | +0.00010 | -0.00297 |
| 2 | +0.00126 | +0.00114 | +0.00114 | +0.00382 | +0.00111 | +0.00012 | -0.00230 |
| 4 | +0.00077 | +0.00066 | +0.00066 | +0.00239 | +0.00041 | +0.00013 | -0.00174 |
| 8 | +0.00031 | +0.00025 | +0.00025 | +0.00101 | -0.00005 | +0.00014 | -0.00120 |
| 12 | +0.00013 | +0.00009 | +0.00009 | +0.00044 | -0.00016 | +0.00013 | -0.00083 |
| 20 | +0.00003 | +0.00001 | +0.00001 | +0.00009 | -0.00013 | +0.00011 | -0.00039 |

Cumulative ΔY control +0.0101, model +0.0081 (ratio 0.80)

## Linear GE response to S

| h | ΔY ctrl | ΔY model | ΔN model | Δw model | ΔBELOW model | ΔBW model | ΔHTM model |
|---|---|---|---|---|---|---|---|
| 0 | -0.00000 | -0.00174 | -0.00174 | -0.00486 | -0.00456 | +0.00000 | +0.00300 |
| 1 | +0.00000 | -0.00126 | -0.00126 | -0.00414 | -0.00392 | -0.00553 | +0.00169 |
| 2 | +0.00000 | -0.00055 | -0.00055 | -0.00294 | -0.00151 | -0.00995 | +0.00112 |
| 4 | -0.00000 | +0.00025 | +0.00025 | -0.00155 | +0.00158 | -0.01634 | +0.00133 |
| 8 | -0.00000 | +0.00086 | +0.00086 | -0.00027 | +0.00418 | -0.02252 | +0.00256 |
| 12 | -0.00000 | +0.00098 | +0.00098 | +0.00024 | +0.00478 | -0.02363 | +0.00357 |
| 20 | -0.00000 | +0.00076 | +0.00076 | +0.00043 | +0.00406 | -0.01982 | +0.00448 |

Cumulative ΔY control -0.0000, model +0.0224

## Nonlinear GE paths (model): expansions that push households through their own gates

- -100 bp: peak Δhours +0.0151; ΔBELOW peak nonlinear +0.0325 vs linear +0.0067; ΔBW min nonlinear -0.0000 vs linear -0.0000; cum ΔY nonlinear +0.0507 vs linear +0.0324 [261s]
- -300 bp: peak Δhours +0.0956; ΔBELOW peak nonlinear +0.1914 vs linear +0.0202; ΔBW min nonlinear -0.0042 vs linear -0.0000; cum ΔY nonlinear +0.2550 vs linear +0.0973 [568s]

Runtime 1219s.

## Control economy, same shocks (nonlinear vs linear) — added 2026-11-09 evening

- control -100 bp: peak Δhours +0.0131; ΔBELOW peak nonlinear +0.0313 vs linear +0.0083; cum ΔY nonlinear +0.0501 vs linear +0.0404 (ratio 1.24) [336s]
- control -300 bp: peak Δhours +0.0651; ΔBELOW peak nonlinear +0.1763 vs linear +0.0250; cum ΔY nonlinear +0.2113 vs linear +0.1212 (ratio 1.74) [428s]
