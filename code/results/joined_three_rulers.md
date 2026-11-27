# Three rulers, one wall removed (2026-11-10)

Source of the household columns: the printed one-asset economy, general equilibrium (`hank_v01_results.json`). Town: Chapter 11's, exact. The join is a construction with ONE supposition, marked and varied: a reader's accuracy rises with bandwidth, p(b) = 1/4 + (p_top − 1/4)·b^γ. Constants are the models'; the orderings are what is reported.

## The programs on each ruler (p_top = 0.9, γ = 1)

| program | CONSUMPTION ruler: low-skill lifetime value, change | aggregate lifetime value, change | BANDWIDTH ruler: low / mid / high skill | town's MEAN catch (share of boats on the fish) | SURVIVAL ruler: famine |
|---|---|---|---|---|---|
| no program | +0.00 | +0.00 | 0.30 / 0.80 / 0.91 | 0.707 | 10.7% |
| time transfer (low-skill floor lifted across the gate) | -0.68 | -0.63 | 0.65 / 0.86 / 0.93 | 0.787 | 0.2% |
| cash, same cost as the time transfer | +5.90 | +1.56 | 0.29 / 0.80 / 0.91 | 0.705 | 11.3% |
| low-skill schedule entropy halved | -0.07 | -0.11 | 0.42 / 0.82 / 0.92 | 0.733 | 4.3% |
| cash, same cost as stability | +1.38 | +0.36 | 0.30 / 0.80 / 0.91 | 0.707 | 10.8% |

Read across. On the consumption ruler the cash wins and the time transfer is a loss. On the bandwidth ruler and on the survival ruler the order is reversed: time moves famine by -10.4 points and the mean catch by +8.0; cash = time moves famine by +0.6 points and the mean catch by -0.2; stability moves famine by -6.3 points and the mean catch by +2.6; cash = stability moves famine by +0.1 points and the mean catch by -0.0.

## The supposition varied: famine under each program

| p_top | γ | baseline | time | cash = time | stability | cash = stability | order on survival (best first) |
|---|---|---|---|---|---|---|---|
| 0.8 | 0.5 | 8.8% | 1.1% | 9.2% | 4.5% | 8.9% | time > stability > baseline > cash = stability > cash = time |
| 0.8 | 1.0 | 41.1% | 7.2% | 42.1% | 27.7% | 41.3% | time > stability > baseline > cash = stability > cash = time |
| 0.8 | 2.0 | 85.9% | 45.1% | 86.3% | 78.0% | 86.0% | time > stability > baseline > cash = stability > cash = time |
| 0.9 | 0.5 | 0.5% | 0.0% | 0.5% | 0.1% | 0.5% | time > stability > baseline > cash = stability > cash = time |
| 0.9 | 1.0 | 10.7% | 0.2% | 11.3% | 4.3% | 10.8% | time > stability > baseline > cash = stability > cash = time |
| 0.9 | 2.0 | 55.9% | 10.0% | 56.8% | 42.2% | 56.1% | time > stability > baseline > cash = stability > cash = time |
| 1.0 | 0.5 | 0.0% | 0.0% | 0.0% | 0.0% | 0.0% | time > stability > baseline > cash = stability > cash = time |
| 1.0 | 1.0 | 1.9% | 0.0% | 2.1% | 0.4% | 1.9% | time > stability > baseline > cash = stability > cash = time |
| 1.0 | 2.0 | 27.6% | 1.1% | 28.5% | 16.3% | 27.8% | time > stability > baseline > cash = stability > cash = time |

Time first and stability second on the survival ruler in 9 of 9 versions of the supposition; in none does either cash arm lower famine by as much as a point.

## What an accounting of isolated boats reports, against what the town suffers

Degrade only the low-skill quarter of the population (their accuracy; everyone else untouched) and compare the loss in MEAN catch — the sum of each boat's own loss, which is all an isolated ledger can add up — with the change in famine:

| low-skill accuracy | others | mean catch | loss in mean catch | famine | famine, relative to the first row |
|---|---|---|---|---|---|
| 0.70 | 0.70 | 0.700 | 0.0% | 7.4% | ×1.0 |
| 0.65 | 0.70 | 0.687 | 1.8% | 11.4% | ×1.5 |
| 0.60 | 0.70 | 0.675 | 3.6% | 17.0% | ×2.3 |
| 0.50 | 0.70 | 0.650 | 7.1% | 32.6% | ×4.4 |
| 0.40 | 0.70 | 0.625 | 10.7% | 48.4% | ×6.5 |
| 0.25 | 0.70 | 0.587 | 16.1% | 64.8% | ×8.8 |

## The transfer lemma (one line)

Famine in this town is a threshold on what the fleet finds, day by day. A transfer moves what was found from one boat's hold to another's; it does not move a boat onto the fish. So no redistribution of the catch, of any size, changes the famine probability; only what changes the readers' accuracy or the sameness of their errors does. In the household model the cash does reach bandwidth through one door — scarcity — and at the printed constants that door moves low-skill bandwidth from 0.30 to 0.29–0.30.
