# Reproduction report

Manuscript: `docs/THE_PRICE_OF_AGENCY_unified_v0.50.md`. Python 3.13.18 on Linux. 2026-11-27.
A number passes when the value a script prints, rounded the way the book prints it, is the book's number.

## Ran here

`code/verify_theorems.py`

- ran   **five hundred** — computed 500. Chapter 4 §5: “Theorem 1 was machine-checked on five hundred randomized worlds”
- ran   **machine-checked** — computed largest error 1.0e-15. Chapter 4 §5: “Theorem 1 was machine-checked on five hundred randomized worlds”
- ran   **no** — computed 0. Chapter 4 §5: “Theorem 2 was checked the same way (no violations; equality exactly where the proof says)”

`code/dichotomy_scaling_and_audits.py`

- ran   **zero below** — computed 4.5e-10, 3.8e-10, 3.3e-10. Chapter 5 §6: “the gate at n = 16, 32, 64: zero below, ~0.93–0.95 above, at the predicted location every time”
- ran   **0.93–0.95** — computed 0.9519, 0.9406, 0.9296. Chapter 5 §6: “the gate at n = 16, 32, 64: zero below, ~0.93–0.95 above, at the predicted location every time”
- ran   **stress-tested** — computed -0.01472, -0.02346, -0.02516. Chapter 4 §5: “additionally stress-tested at alphabet sizes up to 64”

`code/mistake_budget_T18.py`

- ran   **0.936** — computed 0.9355. Chapter 5 §3: “At κ = 10 in a half-noisy world, the gate sits at 0.936 with two options, 0.947 with eight, and under 0.95 with any number”
- ran   **0.947** — computed 0.947. Chapter 5 §3: “At κ = 10 in a half-noisy world, the gate sits at 0.936 with two options, 0.947 with eight, and under 0.95 with any number”
- ran   **under 0.95** — computed 0.9496. Chapter 5 §3: “At κ = 10 in a half-noisy world, the gate sits at 0.936 with two options, 0.947 with eight, and under 0.95 with any number”
- ran   **ninety-five** — computed 95.36. Chapter 5 §2: “the same lessons must be right ninety-five times in a hundred before she acts on them”
- ran   **ninety-five** — computed 95.04. Chapter 5 §2: “the same lessons must be right ninety-five times in a hundred before she acts on them”
- ran   **fifty** — computed 50. Chapter 5 §2: “lessons open the gate once they are right more than fifty times in a hundred”
- ran   **196** — computed 196. Chapter 5 §6: “Theorem 5b in 196 worlds”
- ran   **in 196 worlds** — computed largest gap between the formula and brute force 8.9e-16. Chapter 5 §6: “Theorem 5b in 196 worlds”

`code/calculator_model.py`

- ran   **Theorems 5b** — computed the model's one-glimpse gate equals Theorem 5b at four mistake ratios. Appendix I: “The model inside it is code/calculator_model.py, which checks itself against Theorems 5b and 16”
- ran   **and 16** — computed independence and accuracy equal iterative_time_T16.py at 0 to 4 sittings. Appendix I: “The model inside it is code/calculator_model.py, which checks itself against Theorems 5b and 16”

`code/mistake_ratio_noisy_self_knowledge.py`

- ran   **one where the population sits at its gate** — computed at the gate, the best ratio lies between 0.99 and 1.03 (eight options, noise 0.05 and 0.10). Chapter 5 §3: “one where the population sits at its gate; below one where most sit above it (a margin silences people who should act); and without bound where most sit below it and do not know it”
- ran   **below one where most sit above it** — computed above the gate, the best ratio is below 1 in 12 of 12 populations, at 2, 8 and 64 options. Chapter 5 §3: “one where the population sits at its gate; below one where most sit above it (a margin silences people who should act); and without bound where most sit below it and do not know it”
- ran   **without bound where most sit below it and do not know it** — computed below the gate, the best ratio is above 1 in 12 of 12 populations and at the top of the search (nobody acts) in every world once the noise reaches 0.3. Chapter 5 §3: “one where the population sits at its gate; below one where most sit above it (a margin silences people who should act); and without bound where most sit below it and do not know it”

`code/delta_A_v1.py`

- ran   **δ_A = 0** — computed 0. Chapter 4 §4: “δ_A = 0: the captain — circumstances leave no doubt. δ_A = 1: the tourist — circumstances say nothing.”
- ran   **δ_A = 1** — computed 1. Chapter 4 §4: “δ_A = 0: the captain — circumstances leave no doubt. δ_A = 1: the tourist — circumstances say nothing.”

`code/plateau_hit_rate_bound.py`

- ran   **more than half the time** — computed the most a perfectly unreadable strategy can be right, by linear program in 42 worlds, exceeds the captain exactly when the noise is above one half. Chapter 6 §2: “not more than the captain who simply follows the table's tells, unless those tells are noise more than half the time”

`code/frontier_attack.py`

- ran   **killed** — computed the optimizer beats the conjectured curve by 0.0321. Chapter 6 §6: “the optimizer that killed the simple- strategy conjecture”

`code/theft_equilibrium.py`

- ran   **0.009** — computed largest 0.009. Chapter 7 §4: “the independence ruler by elasticity at most 0.009 while moving aim by 1.5 to 2.0”
- ran   **1.5 to 2.0** — computed 1.94, 2.018, 1.719, 1.797, 1.466, 1.969. Chapter 7 §4: “the independence ruler by elasticity at most 0.009 while moving aim by 1.5 to 2.0”
- ran   **9** — computed 9.16. Chapter 7 §4: “education spikes to about 9, and against the world's predictability to about 4.5”
- ran   **4.5** — computed 4.541. Chapter 7 §4: “education spikes to about 9, and against the world's predictability to about 4.5”
- ran   **0.565** — computed 0.565. Chapter 7 §4: “aim's elasticity against time is 0.565 for a time-poor agent versus 0.008 for a time-rich one”
- ran   **0.008** — computed 0.008. Chapter 7 §4: “aim's elasticity against time is 0.565 for a time-poor agent versus 0.008 for a time-rich one”
- ran   **0.29** — computed 0.2909. Chapter 8 §4: “Result: δ_A({circumstances, die}) = 0.29 in the model, versus 0.75 for the undisguised expert”
- ran   **0.75** — computed 0.7533. Chapter 8 §4: “Result: δ_A({circumstances, die}) = 0.29 in the model, versus 0.75 for the undisguised expert”

`code/surveillance_T9_wider_plateau.py`

- ran   **0.29** — computed 0.2909. Chapter 8 §3: “at 0.29 for the strategy that follows the target a fixed fraction of the time and compensates the rest, and at 0.65 for”
- ran   **0.65** — computed 0.6533. Chapter 8 §3: “at 0.29 for the strategy that follows the target a fixed fraction of the time and compensates the rest, and at 0.65 for”
- ran   **one third** — computed 0.348. Chapter 8 §3: “crossover comes at roughly one third visibility of the source of chance for the first strategy and seven tenths for the second”
- ran   **seven tenths** — computed 0.711. Chapter 8 §3: “crossover comes at roughly one third visibility of the source of chance for the first strategy and seven tenths for the second”

`code/wirings_T11_wider_plateau.py`

- ran   **0.62–0.70** — computed gated floors 0.622, 0.667, 0.700, 0.697. Chapter 9 §5: “half-noisy world (gated floors rising to 0.62–0.70 but staying below the open expert; additive equality at three bits)”
- ran   **staying below the open expert** — computed open expert 0.7744. Chapter 9 §5: “half-noisy world (gated floors rising to 0.62–0.70 but staying below the open expert; additive equality at three bits)”
- ran   **additive equality at three bits** — computed at three bits the floor equals the first-day value, 0.984. Chapter 9 §5: “half-noisy world (gated floors rising to 0.62–0.70 but staying below the open expert; additive equality at three bits)”

`code/arms_race.py`

- ran   **does not raise** — computed gated floors 0.3379, 0.4532, 0.485, 0.4737, all under one half. Chapter 9 §3: “More coin does not raise a gated floor.”

`code/stealth_gates.py`

- ran   **0.052** — computed 0.0522. Chapter 6 §4: “(In the reference world, 0.247 against the first printing's 0.052”

`code/iterative_time_T16.py`

- ran   **the time gate** — computed independence 0, 0, then 0.4593 at the third step. Chapter 7 §6: “the time gate and the Tomas version”

`code/neighbors_T12_P15.py`

- ran   **0.77** — computed 0.7744. Chapter 10 §3: “from 0.77 alone, to 0.71 beside an unreadable neighbor, to 0.61 beside an ordinary one, to exactly 0 beside a flawless visible expert”
- ran   **0.71** — computed 0.712. Chapter 10 §3: “from 0.77 alone, to 0.71 beside an unreadable neighbor, to 0.61 beside an ordinary one, to exactly 0 beside a flawless visible expert”
- ran   **0.61** — computed 0.6087. Chapter 10 §3: “from 0.77 alone, to 0.71 beside an unreadable neighbor, to 0.61 beside an ordinary one, to exactly 0 beside a flawless visible expert”
- ran   **exactly 0** — computed 0. Chapter 10 §3: “from 0.77 alone, to 0.71 beside an unreadable neighbor, to 0.61 beside an ordinary one, to exactly 0 beside a flawless visible expert”
- ran   **0.17** — computed 0.1657. Chapter 10 §3: “first costs 0.17, the second 0.13, the third 0.10, the fourth 0.08”
- ran   **0.13** — computed 0.1292. Chapter 10 §3: “first costs 0.17, the second 0.13, the third 0.10, the fourth 0.08”
- ran   **0.10** — computed 0.1004. Chapter 10 §3: “first costs 0.17, the second 0.13, the third 0.10, the fourth 0.08”
- ran   **0.08** — computed 0.0788. Chapter 10 §3: “first costs 0.17, the second 0.13, the third 0.10, the fourth 0.08”

`code/fishing_town_T13.py`

- ran   **0.074** — computed 0.07395. Chapter 11 §4: “giving 0.074 per ninety-day season”
- ran   **0.44** — computed 0.4388. Chapter 11 §4: “its famine probability, 0.44, does not improve by one decimal if the town grows”
- ran   **six-fold** — computed 5.933. Chapter 11 §3: “Nine independent 70%-fishers beat one 80% authority six-fold on famine”
- ran   **roughly halving per two added** — computed each two fishers added multiply famine by 0.54, 0.52, 0.51, 0.52, 0.52. Chapter 11 §3: “falls exponentially in the number of independent educated fishers (roughly halving per two added)”
- ran   **a benefit at one** — computed famine by followers 0 to 5: 0.074, 0.049, 0.064, 0.140, 0.299, 0.439; unchanged from 5 to 9. Chapter 11 §3: “a benefit at one, worsening after, saturating exactly at bloc majority”
- ran   **7 | 5 | 6 | 14 | 44 | 44** — computed exact: 7 | 5 | 6 | 14 | 44 | 44 (the table is simulated; this is the exact computation). Chapter 11 §5, table: “| Nothing changed (master right 80) | 7 | 5 | 6 | 14 | 44 | 44 | one |”

`code/correlated_weather_T14.py`

- ran   **a floor** — computed thirty-one boats, shared mirage on 5, 15, 30 days in a hundred: famine 0.001196, 0.01242, 0.06958 against floors 2.9e-04, 0.007635, 0.05689. Chapter 11 §4: “a floor that size cannot touch, only sameness can lower”

`code/living_town_S1.py`

- ran   **halved** — computed 0.5218. Chapter 11 §3: “finite resources convert it (interior mix, higher accuracy, famine halved)”
- ran   **interior mix** — computed share following the hub at the end: 0.485. Chapter 11 §3: “finite resources convert it (interior mix, higher accuracy, famine halved)”
- ran   **higher accuracy** — computed majority right more often with finite fish. Chapter 11 §3: “finite resources convert it (interior mix, higher accuracy, famine halved)”

`code/borrowed_record.py`

- ran   **85** — computed 85. Chapter 11 §3: “his record is 85 against a reader's 79.5, every boat follows him, and famine doubles, from 11 seasons in a hundred to 22.5”
- ran   **79.5** — computed 79.5. Chapter 11 §3: “his record is 85 against a reader's 79.5, every boat follows him, and famine doubles, from 11 seasons in a hundred to 22.5”
- ran   **11** — computed 11. Chapter 11 §3: “his record is 85 against a reader's 79.5, every boat follows him, and famine doubles, from 11 seasons in a hundred to 22.5”
- ran   **22.5** — computed 22.5. Chapter 11 §3: “his record is 85 against a reader's 79.5, every boat follows him, and famine doubles, from 11 seasons in a hundred to 22.5”
- ran   **999** — computed 999.1. Chapter 11 §3: “the town's majority was right 999 times in a thousand”
- ran   **11** — computed 10.9. Chapter 11 §3: “put him back where he is right and the town back at 11”
- ran   **a week** — computed 7. Chapter 11 §3: “a week away when every hard day is scored, seven seasons away when one in a hundred is”
- ran   **seven** — computed 7.4. Chapter 11 §3: “a week away when every hard day is scored, seven seasons away when one in a hundred is”
- ran   **14** — computed 14.2. Chapter 11 §3: “and famine stops at 14 seasons in a hundred”
- ran   **85** — computed 85. Part V, Why the self-anointed rule: “85 right in a hundred against a fisher's 79”
- ran   **79** — computed 79.5. Part V, Why the self-anointed rule: “85 right in a hundred against a fisher's 79”

`code/attack_T22_T23.py`

- ran   **0.109** — computed 0.109. Chapter 11 §3: “a third would land 0.109 of the catch where a reader lands 0.111”
- ran   **0.111** — computed 0.111. Chapter 11 §3: “a third would land 0.109 of the catch where a reader lands 0.111”
- ran   **27** — computed 26.7. Chapter 11 §3: “27 in a hundred in the printed town — and the murky boats stay in above a trip cost of 0.51 where they had stayed in above 0.40; at three boatloads of hunger, above 0.72”
- ran   **0.51** — computed 0.51. Chapter 11 §3: “27 in a hundred in the printed town — and the murky boats stay in above a trip cost of 0.51 where they had stayed in above 0.40; at three boatloads of hunger, above 0.72”
- ran   **0.40** — computed 0.4. Chapter 11 §3: “27 in a hundred in the printed town — and the murky boats stay in above a trip cost of 0.51 where they had stayed in above 0.40; at three boatloads of hunger, above 0.72”
- ran   **0.72** — computed 0.72. Chapter 11 §3: “27 in a hundred in the printed town — and the murky boats stay in above a trip cost of 0.51 where they had stayed in above 0.40; at three boatloads of hunger, above 0.72”
- ran   **8** — computed 7.9. Chapter 11 §3: “that chance is 8 in a hundred and the line moves from 0.40 to 0.43”
- ran   **0.43** — computed 0.43. Chapter 11 §3: “that chance is 8 in a hundred and the line moves from 0.40 to 0.43”

`code/stay_ashore.py`

- ran   **7** — computed 7.4. Chapter 11 §3: “ashore on any morning, famine goes from 7 seasons in a hundred to 98”
- ran   **98** — computed 98.2. Chapter 11 §3: “ashore on any morning, famine goes from 7 seasons in a hundred to 98”
- ran   **under three percent** — computed 2.9. Chapter 11 §3: “for under three percent of the catch when the gap is a twentieth of a boatload”

`code/two_towns_aid.py`

- ran   **twenty-fold** — computed 20.9. Chapter 14 §5B: “famine falls twenty-fold for both”
- ran   **7** — computed 7.4. Chapter 15 §3: “cut famine from 7 seasons in a hundred to a third of one”
- ran   **a third** — computed 0.35. Chapter 15 §3: “cut famine from 7 seasons in a hundred to a third of one”

`code/duty_trade_exact.py`

- ran   **refuted** — computed cases in which the trade pays every party and starves the town: 0 of 48. Chapter 15 §3: “The expectation that such a trade would starve the town was refuted”
- ran   **in most cases computed** — computed the trade is better for the town in 40 of 48 cases. Chapter 15 §3: “selling the burden to the same few boats is better for the town than drawing it by lot in most cases computed”

`code/joined_three_rulers.py`

- ran   **0.30** — computed 0.3. Chapter 14 §5C: “the time transfer lifts the low-skill group's from 0.30 to 0.65, stability lifts it to 0.42, and cash leaves it where it was”
- ran   **0.65** — computed 0.65. Chapter 14 §5C: “the time transfer lifts the low-skill group's from 0.30 to 0.65, stability lifts it to 0.42, and cash leaves it where it was”
- ran   **0.42** — computed 0.42. Chapter 14 §5C: “the time transfer lifts the low-skill group's from 0.30 to 0.65, stability lifts it to 0.42, and cash leaves it where it was”
- ran   **where it was** — computed with the cash 0.29. Chapter 14 §5C: “the time transfer lifts the low-skill group's from 0.30 to 0.65, stability lifts it to 0.42, and cash leaves it where it was”
- ran   **11** — computed 10.7. Chapter 14 §5C: “The town starves in 11 seasons of a hundred with no program, in fewer than one with the time transfer, in 4 with stability, and in 11 with the cash”
- ran   **fewer than one** — computed 0.2. Chapter 14 §5C: “The town starves in 11 seasons of a hundred with no program, in fewer than one with the time transfer, in 4 with stability, and in 11 with the cash”
- ran   **4** — computed 4.3. Chapter 14 §5C: “The town starves in 11 seasons of a hundred with no program, in fewer than one with the time transfer, in 4 with stability, and in 11 with the cash”
- ran   **11** — computed 11.3. Chapter 14 §5C: “The town starves in 11 seasons of a hundred with no program, in fewer than one with the time transfer, in 4 with stability, and in 11 with the cash”
- ran   **3.6** — computed 3.6. Chapter 14 §5C: “records 3.6 percent less fish, while the town's famine rate more than doubles”
- ran   **more than doubles** — computed 2.3. Chapter 14 §5C: “records 3.6 percent less fish, while the town's famine rate more than doubles”

`code/imposition_cascade_T17.py`

- ran   **93.4** — computed 93.4. Chapter 13 §2B: “cascade, the bottom layer bears 93.4% of all agency destroyed”
- ran   **14** — computed 14. Chapter 13 §2B: “| Worker | 64 | 14 | 1 | 0.565 | 7.91 | 506.2 |”
- ran   **1** — computed 1. Chapter 13 §2B: “| Worker | 64 | 14 | 1 | 0.565 | 7.91 | 506.2 |”
- ran   **7.91** — computed 7.91. Chapter 13 §2B: “| Worker | 64 | 14 | 1 | 0.565 | 7.91 | 506.2 |”
- ran   **506.2** — computed 506.2. Chapter 13 §2B: “| Worker | 64 | 14 | 1 | 0.565 | 7.91 | 506.2 |”
- ran   **100** — computed 100. Chapter 13 §2B: “| Executive | 1 | 100 | 60 | 0.008 | 0.80 | 0.8 |”
- ran   **60** — computed 60. Chapter 13 §2B: “| Executive | 1 | 100 | 60 | 0.008 | 0.80 | 0.8 |”
- ran   **0.80** — computed 0.8. Chapter 13 §2B: “| Executive | 1 | 100 | 60 | 0.008 | 0.80 | 0.8 |”
- ran   **ten times** — computed 10. Chapter 13 §2B: “ten times more agency per person”

`code/rig/wiring_hardening_exact.py`

- ran   **3,372** — computed 3372. Chapter 9 §3: “**Theorem 11′ (The dichotomy, hardened). [EXACT; 3,372 wirings]**”
- ran   **0.07** — computed 0.074. Chapter 9 §3: “four options in a half-noisy world it stays below by 0.07; in a six-option world that is mostly right it crosses above, 0.564 against 0.538”
- ran   **0.564** — computed 0.5642. Chapter 9 §3: “four options in a half-noisy world it stays below by 0.07; in a six-option world that is mostly right it crosses above, 0.564 against 0.538”
- ran   **0.538** — computed 0.5384. Chapter 9 §3: “four options in a half-noisy world it stays below by 0.07; in a six-option world that is mostly right it crosses above, 0.564 against 0.538”
- ran   **0.026** — computed 0.026. Chapter 9 §5: “failed by 0.026 in a six-option world that is mostly right”

`code/fringe_2608_18886.py`

- ran   **arXiv:2608.18886** — computed efficiency 0.8013 against the paper's 0.801. The paper the essay "The law's own exhibit" stands on (arXiv:2608.18886); the figure in the designed edition: “arXiv:2608.18886”
- ran   **arXiv:2608.18886** — computed fringe 0.1242 against the paper's 0.124. The paper the essay "The law's own exhibit" stands on (arXiv:2608.18886); the figure in the designed edition: “arXiv:2608.18886”

`code/plateau_edge_T6prime.py`

- ran   **0.247** — computed 0.2467. Chapter 6 §4: “(In the reference world, 0.247 against the first printing's 0.052”
- ran   **0.052** — computed 0.0522. Chapter 6 §4: “(In the reference world, 0.247 against the first printing's 0.052”
- ran   **In the reference world** — computed the closed form and the computed value agree. Chapter 6 §4: “(In the reference world, 0.247 against the first printing's 0.052”
- ran   **0.10** — computed 0.097. Chapter 6 §5: “0.10, 0.25, 0.46 as the world's noise rises through 0.3, 0.5, 0.7 in the reference world”
- ran   **0.25** — computed 0.2467. Chapter 6 §5: “0.10, 0.25, 0.46 as the world's noise rises through 0.3, 0.5, 0.7 in the reference world”
- ran   **0.46** — computed 0.4616. Chapter 6 §5: “0.10, 0.25, 0.46 as the world's noise rises through 0.3, 0.5, 0.7 in the reference world”

`code/frontier_polytope_attack.py`

- ran   **δ_A = 0.75** — computed 0.7533. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **aim at least 1.00** — computed 1. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **δ_A = 0.80** — computed 0.7966. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **0.86 at δ_A = 0.80** — computed 0.8576. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **δ_A = 0.85** — computed 0.8542. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **0.70 at δ_A = 0.85** — computed 0.705. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **δ_A = 0.93** — computed 0.9306. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **0.53 at δ_A = 0.93** — computed 0.5273. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **δ_A = 0.98** — computed 0.981. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **0.37 at δ_A = 0.98** — computed 0.3673. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **δ_A = 0.99** — computed 0.9875. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **0.35 at δ_A = 0.99** — computed 0.3453. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **δ_A = 0.997** — computed 0.9967. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”
- ran   **0.29 at δ_A = 0.997** — computed 0.2939. Chapter 6 §5: “certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997”

`code/hiding_theorem_econ.py`

- ran   **0.07** — computed 0.0694. Chapter 13 §2C: “is produced by a town of Tomases and Nadias at aim 0.07 — and, identically, by the sage, acting on perfect knowledge of the future through a half-reliable world, at aim 1.00”
- ran   **1.00** — computed 1. Chapter 13 §2C: “is produced by a town of Tomases and Nadias at aim 0.07 — and, identically, by the sage, acting on perfect knowledge of the future through a half-reliable world, at aim 1.00”
- ran   **zero** — computed 0. Chapter 13 §2C: “is produced by pure scatter at aim zero and by Ines's plateau strategy at aim c₀, identically”
- ran   **identically** — computed both produce choice data with independence 1.0000. Chapter 13 §2C: “is produced by pure scatter at aim zero and by Ines's plateau strategy at aim c₀, identically”

## Recorded: read from results files in the repository, not re-run

`code/rig/results_town/town_stress_00.csv, code/rig/results_town2/town_stress2.csv` — Chapter 11 §5, table: “famine, in seasons of a hundred, by how many of the nine boats follow the master”

- recorded  **Nothing changed (master right 80)** — in the file: | Nothing changed (master right 80) | 7 | 5 | 6 | 14 | 44 | 44 |
- recorded  **Master right 90** — in the file: | Master right 90 | 7 | 3 | 2 | 3 | 8 | 8 |
- recorded  **Master right 99** — in the file: | Master right 99 | 8 | 2 | 0.3 | 0.1 | 0 | 0 |
- recorded  **Master misdirects, one known day in ten** — in the file: | Master misdirects, one known day in ten | 8 | 7 | 12 | 30 | 77 | 78 |
- recorded  **Master misdirects, three days in ten** — in the file: | Master misdirects, three days in ten | 7 | 12 | 31 | 70 | 99 | 99 |
- recorded  **The same, master right 99** — in the file: | The same, master right 99 | 7 | 8 | 15 | 37 | 85 | 85 |
- recorded  **Master's errors come in slumps** — in the file: | Master's errors come in slumps | 7 | 7 | 22 | 58 | 95 | 95 |
- recorded  **The same, master right 90** — in the file: | The same, master right 90 | 8 | 4 | 10 | 31 | 72 | 72 |
- recorded  **Readers have bad weeks; master does not** — in the file: | Readers have bad weeks; master does not | 51 | 40 | 29 | 26 | 44 | 45 |
- recorded  **Readers and master both have bad weeks** — in the file: | Readers and master both have bad weeks | 52 | 44 | 51 | 71 | 95 | 95 |
- recorded  **Readers share a blindness, 3 days in 10** — in the file: | Readers share a blindness, 3 days in 10 | 96 | 95 | 95 | 97 | 43 | 44 |
- recorded  **The sea remembers yesterday** — in the file: | The sea remembers yesterday | 8 | 5 | 6 | 14 | 44 | 44 |
- recorded  **Self-serving master; readers' bad weeks** — in the file: | Self-serving master; readers' bad weeks | 52 | 39 | 28 | 100 | 100 | 100 |

`code/rig/hank_port/results_sweep_fast/SWEEP_SUMMARY.md` — Chapter 14 §5C, table: “the share of drawn economies, in a hundred, in which each signed claim holds”

- recorded  **The real rate is higher under the tax** — in the file: | The real rate is higher under the tax | 100 | 100 | 100 |
- recorded  **Asset demand is lower at fixed prices** — in the file: | Asset demand is lower at fixed prices | 100 | 100 | 100 |
- recorded  **Half the dose moves the rate less** — in the file: | Half the dose moves the rate less | 100 | 100 | 100 |
- recorded  **More schedule entropy raises the rate** — in the file: | More schedule entropy raises the rate | 99 | 100 | 97 |
- recorded  **Stability beats the equal-dollar transfer on welfare** — in the file: | Stability beats the equal-dollar transfer on welfare | 94 | 99.6 | 74 |
- recorded  **More low-skill households hand to mouth under the tax** — in the file: | More low-skill households hand to mouth under the tax | 75 | 75 | 76 |
- recorded  **The gap stays positive after liquidity is repaired** — in the file: | The gap stays positive after liquidity is repaired | 75 | 74 | 77 |
- recorded  **Stability beats the transfer on hand-to-mouth status** — in the file: | Stability beats the transfer on hand-to-mouth status | 51 | 64 | 10 |
- recorded  **Time beats cash on hand-to-mouth status** — in the file: | Time beats cash on hand-to-mouth status | 38 | 42 | 25 |
- recorded  **Time beats cash on hand-to-mouth status, prices fixed** — in the file: | Time beats cash on hand-to-mouth status, prices fixed | 20 | 22 | 17 |

`code/field/results/shed_first_look.md` — Chapter 13 §2D: “from 28 percent of employees in the lowest band to 11 in the highest”

- recorded  **28** — in the file: 28.5
- recorded  **11** — in the file: 11.1

`code/field/results/shed_first_look.md` — Chapter 13 §2D: “more often just getting by or worse (7 points), more often without three months of savings (5), more often unable to meet a four-hundred-dollar expense (3), and more often behind on bills because income varied (11)”

- recorded  **(7 points)** — in the file: 7.2
- recorded  **(5)** — in the file: 4.9
- recorded  **(3)** — in the file: 2.8
- recorded  **(11)** — in the file: 11.2

`code/field/results/shed_oos_test.md` — Chapter 13 §2D: “and 2021 files, which had not been opened (18,268 employees)”

- recorded  **18,268** — in the file: 18268

`code/field/results/shed_oos_test.md` — Chapter 13 §2D: “7.5 points on just getting by, 5.5 on bills, 2.4 on the four-hundred-dollar expense, each distinguishable from zero, and 1.5 on the three-month fund”

- recorded  **7.5** — in the file: 7.5
- recorded  **5.5** — in the file: 5.5
- recorded  **2.4** — in the file: 2.4
- recorded  **1.5** — in the file: 1.5

`code/field/results/shed_panel_test.md` — Chapter 13 §2D: “4,816 employees, 7,390 pairs of adjacent years”

- recorded  **4,816** — in the file: 4816
- recorded  **7,390** — in the file: 7390

`code/field/results/shed_panel_test.md` — Chapter 13 §2D: “person is 3.0 points more likely to be just getting by and 6.1 points more likely to be behind on bills”

- recorded  **3.0** — in the file: 3
- recorded  **6.1** — in the file: 6.1

`code/field/results/shed_panel_test.md` — Chapter 13 §2D: “measures (5.6 and 3.8 points)”

- recorded  **5.6** — in the file: 5.6
- recorded  **3.8** — in the file: 3.8

## Not re-run by this command

- `code/rig/plateau_edge_vertex_search.py, plateau_edge_bnb.py` — the edge of the plateau (Chapter 6 §6, Chapter 15 §2): 0.335 at six options and the certified ceilings. Not re-run: these are searches, and the printed values are the best of long runs; a twenty-second run of the first finds 0.331, under the printed 0.335 as a floor should be. To run it: python code/rig/plateau_edge_vertex_search.py 6 0.5 <restarts> <seconds>; the long runs' outputs are in code/rig/results_exact/.
- `code/rig/watcher_tournament.py` — the learned watchers of Chapter 9 (Theorem 20, Result R6). Not re-run: needs a GPU; about an hour on six. To run it: see code/rig/README_RIG.md; results in code/rig/results/.
- `code/rig/town_stress_T13.py, town_stress2.py, living_town_skill.py` — the towns under stress (S2, S3) and the table of Chapter 11 §5. Not re-run: twenty thousand simulated seasons a cell, written for a GPU with PyTorch (they fall back to the processor, slowly). To run it: the launchers in code/rig/ (RUN_ALL.bat on Windows); the table is checked above against the results files.
- `code/rig/hank_port/` — Chapter 14 §5C: the household model in general equilibrium, and its sweeps of 688 and 273 drawn economies. Not re-run: hours of processor time on many cores. To run it: the launchers in code/rig/ (RUN_NIGHT.bat, RUN_DAY.bat, RUN_RULERS.bat, RUN_TWOASSET_RULERS.bat); the first sweep's table is checked above against its summary.
- `code/field/shed_*.py` — Chapter 13 §2D: the Federal Reserve survey. Not re-run: needs the survey's public files, which are the Federal Reserve's to distribute and are not copied into this repository. To run it: download the SHED public-use files for 2019 to 2023 from federalreserve.gov; each script's first lines say which files it takes (python code/field/shed_first_look.py public2022.csv public2023.csv); they also need pandas and statsmodels. The printed numbers are checked above against code/field/results/.

## Result

176 checks. 176 match the book, 0 do not.
