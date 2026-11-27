# Welfare criteria and the Pigou wedge (2026-11-09)

Aggregate welfare (utility units, mean over households) by schedule entropy S, model economy at its GE; the firm's private optimum is S_priv = argmin g(S).

| S | g(S) | TRUE (β policy eval.) | TUN (β_eff honored) | OWN (household's own V) |
|---|---|---|---|---|
| 0.0 | 1.0000 | -63.4143 | -58.6626 | -59.8666 |
| 0.25 | 0.9874 | -62.9577 | -55.4124 | -57.1119 |
| 0.5 | 0.9789 | -62.6709 | -53.0131 | -55.0294 |
| 0.75 | 0.9740 | -62.5285 | -51.2055 | -53.4185 |
| 1.0 | 0.9721 | -62.5108 | -49.8250 | -52.1526 |
| 1.25 | 0.9728 | -62.6025 | -48.7254 | -51.1173 |
| 1.5 | 0.9759 | -62.7905 | -47.8622 | -50.2791 |
| 2.0 | 0.9881 | -63.4176 | -46.6279 | -49.0219 |

S_priv = 1.000 (grid; refined 1.055 in hank_pigou).

- **TRUE**: planner's S = 0.915 (interior optimum); wedge S_priv − S_soc = +0.085 → the planner wants LESS entropy than the firm: Pigou tax positive
- **TUN**: planner's S = 2.000 (rising in S); wedge S_priv − S_soc = -1.000 → the planner wants MORE entropy than the firm: a Pigou SUBSIDY — the criterion scores the loss of bandwidth as a gain
- **OWN**: planner's S = 2.000 (rising in S); wedge S_priv − S_soc = -1.000 → the planner wants MORE entropy than the firm: a Pigou SUBSIDY — the criterion scores the loss of bandwidth as a gain

Reading. Under the household's own valuation, impatience shrinks the weight on future hardship, so a more degraded household reports itself better off; a planner using that criterion would subsidize the drain. The book's default scores the degraded planner at the undegraded discount rate — the choice is a premise and is printed as one; this table shows which conclusion depends on it.
Runtime 250s.
