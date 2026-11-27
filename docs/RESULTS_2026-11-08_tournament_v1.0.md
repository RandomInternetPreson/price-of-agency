# RESULTS 2026-11-08 — the neural-watcher tournament (Ch 15 §3, problems 3 / 5 / 7) — for ruling

Run on Aaron's rig: 112 configurations, tiers A (core) and R (regress), 10.9 GPU-hours on four
RTX 4090s; every config converged (`conv = ok` in all 112; the exact Bayesian's simulated reading
matched the enumerated floor to ≤ 0.01 everywhere). Raw shards, lifetime curves and figures in
`code/rig/results/`; figures copied to `figures/watcher_tournament_*.png`. Model world: n = 4,
s = 0.5, λ* and hand policies, gated / additive / random wirings, m_S ∈ {8, 1024}, h ∈ {1, 2, 3}.
All quantities are model-world; nothing is asserted of the world.

Watchers scored by log-loss in units of log₂ n (= the book's δ_A for the exact watcher, verified side by
side): **bayes** (exact posterior, true wiring — the book's watcher), **bayes-wrong** (exact posterior,
the *other* wiring), **markov-k** (in-context count miners, k = 0, 1, 2), **gru-l** (795k parameters),
**tf-l** (1.8M parameters) — the last two trained from scratch on unlimited fresh lifetimes, never told
the wiring, the habit space, or that a habit exists.

---

## Q3 — How much watcher does the inversion cost? **Nothing.** [EXACT floors; learned to 3 decimals]

Across all 72 tier-A configurations the structure-free neural watchers reach the exact seed-known
floor: max |learned − exact| = 0.008, mean 0.001. The gated inversion (watcher reads the agent *below*
the sage) is achieved by the exact watcher in 28/28 gated configs and by the learned watcher in
28/28. Speed: the GRU and the transformer reach within 0.02 of the floor in **5–10 days** — the same
day the exact Bayesian does (7–10). Even the dumbest miner — a frequency count of A given today's E,
no history structure at all — lands within 0.015–0.022 of the floor by day ~100.

The *only* watcher that fails is the one with a confident wrong theory: the Bayesian who assumes the
other wiring reads worse than ignorance (δ_W > 1) in **52 of 72** configs (0.83–1.56). A habit cannot
be hidden from a watcher who knows nothing; it can only be hidden from one who insists on knowing the
wrong thing.

**Candidate (T20, model-world):** *The surveillance inversion of Theorem 9/11 is not a property of
an idealized watcher. Any sufficiently flexible learner — a sequence model of under a million
parameters, or a frequency table — attains the exact floor within a season, without knowledge of the
habit's structure. The theorems' "strongest watcher" is the floor's* name, *not its* price. The
single way to read above the floor is to hold a wrong model and not update it.*
Ch 15 §3 problem 3 ("the clever weak watcher"): **closed** — there is no gap for cleverness to
occupy; the weak watcher is already at the floor.

## Q5 — Does the habit space's size protect? **No — it sharpens the read.** [EXACT + learned]

Floors at m_S = 1024 are *lower* than at m_S = 8 (gated, hand: 0.629 vs 0.700; gated, λ*: 0.363 vs
0.474), and the watchers reach them *faster* (7 days vs 9–10; λ*: 5 vs 8). A richer repertoire of
habits is not a disguise: finer quantile cells make each action more determinate given the habit, so
the watcher has less to learn per day and less left over once it has learned. Random wirings sit
between gated and additive at every h, exactly where the exact sweep put them (h = 1/2/3: 0.745 /
0.869 / 0.937), and the learned watchers match those floors too. The one-time-pad check at h = 3:
learned floors never beat d0 beyond noise (−0.014 … 0.000); equality at m_S = 8, the 0.01 gap at
m_S = 1024 as the log₂ m_S law predicts.

Ch 15 §3 problem 5 ("the wiring theorem hardened"): with the exact sweep of Oct 24 (R5 margin,
log₂ m_S law, reach law) and this run, **closed for the learned side** on random wirings and large
habit spaces; the arbitrary-structure theorem stays open as stated.

## Q7 — The regress. **The pad is a race, and it has a measured finish line.** [learned; existence results]

The additive wiring at h = 3 is the book's unreadable wiring: with a truly fresh coin every watcher
sits at the seed-unknown value (0.98) — exact, miners, and both learners alike. Replace the coin with a
deterministic generator carrying a hidden k-bit seed (an LCG; the coin's marginals are unchanged) and:

| generator | fresh-coin Bayesian | GRU (795k) | transformer (1.8M) | day the GRU's reading falls below the Bayesian's |
|---|---|---|---|---|
| truly fresh | 0.978 / 0.984 | 0.978 / 0.984 | 0.978 / 0.984 | never |
| 32-bit | 0.978 / 0.984 | 0.978 / 0.984 | 0.978 / 0.984 | never |
| 16-bit | 0.978 / 0.984 | **0.898** / 0.982 | 0.978 / 0.984 | day 24 (λ*) |
| 12-bit | 0.978 / 0.984 | **0.359** / **0.795** | 0.976 / 0.983 | day 12 (λ*) / 35 (hand) |
| 8-bit | 0.978 / 0.984 | **0.343** / **0.812** | **0.349** / **0.589** | day 5 (λ*) / 40 (hand) |

(λ* / hand policy.) An 8-bit coin is a habit: both learners read the "unreadable" wiring to **0.34** —
below the gated floor (0.47) and far below the sage (0.77) — within a week. A 12-bit coin is a habit
to the recurrent watcher within a season. A 16-bit coin is half-read. A 32-bit coin is a coin, at this
watcher's size and this lifetime. The Bayesian who *assumes* the coin is fresh never moves: that is the
price of assuming freshness, and it is the whole gap. In the gated wiring, cracking the coin buys the
watcher almost nothing (0.474 → 0.401 at 8 bits, λ*): the coin was never doing the work there.

Two honesty notes. (i) These are *existence* results — one training seed per config; the
transformer missed the 12- and 16-bit generators the GRU caught, which is inductive bias and
optimization luck, not a bound. What is established is that a watcher of this size *can* acquire
8–12 bits of generator within a lifetime. (ii) LCGs are the weakest generators there are; the
thresholds are for this family.

**Candidate (R6 / T11″, model-world):** *Theorem 11(iv) says that with no coin, both wirings are
fully extractable. Its extension: a coin is fresh only relative to a watcher. A pseudo-coin with k
bits of hidden state protects the additive wiring exactly as long as the watcher cannot acquire k
bits within the watched lifetime; for a learner of ~10⁶ parameters and a 512-day life, that line
falls between 12 and 32 bits for the weakest generator family. Below it the one-time pad is a
habit one level up, and the inversion returns in full.* This is the receipt for Ch 14's "protect
the privacy of the randomizer": the randomizer must be a coin, and *coin* is a word about the
watcher.
Ch 15 §3 problem 7 ("the regress"): **measured** — converted from an open question into a curve with
a stated budget; the general statement (any generator, any watcher) stays open.

---

## Candidate rulings (defaults)
1. Ch 9 §3/§5: print T20 as the empirical companion to T9/T11 — one paragraph and the floors table;
   "the strongest watcher is the floor's name, not its price"; the wrong-model result in one sentence.
2. Ch 9 §5: one sentence that the habit space's size sharpens the read (with the 1024 numbers).
3. Ch 9 §4 (coins) and Ch 14 (randomizer privacy): print R6 with the table and the two honesty notes;
   `figures/watcher_tournament_regress.png` as the chapter's figure.
4. Ch 15 §3: problems 3 and 5 marked closed (model-world); problem 7 marked measured, with the open
   general form restated.
5. THEOREMS_v1.md: T20, R6 appended; IMPACT_MAP: Ch 9, 14, 15 entries.
Tier B (n = 6, m_S = 64, watcher also sees outcomes; ~3 h on four GPUs) is optional hardening and
would only move digits, not any of the three readings above.
