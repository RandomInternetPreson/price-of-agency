# The walls — an audit of every isolation assumed in the book (2026-11-10)

Rule adopted on this date (Aaron Alai): isolation is not the null. A perfectly independent measurement, a household whose
errors stop at its own door, a system with nothing outside it — each is a facsimile, and a result obtained behind such a
wall is a property of the wall until it is shown to survive the wall's removal. The same rule cuts the other way: a wall's
removal is not a licence to assert its opposite (errors perfectly shared; capacity perfectly equal). What can be printed is
what was computed with the wall and what was computed without it.

This file lists every wall in the book's models, where a later part of the book takes it down, what changed when it did,
and which walls are still standing. Chapter and theorem numbers are those of manuscript v0.35.

## A. Walls taken down inside the book, and what changed

| # | The wall (what was assumed isolated) | Where it stands | Where it comes down | What the wall had hidden |
|---|---|---|---|---|
| 1 | One agent alone with a future; nobody watching | Ch 4–7 | Ch 8–9 (watchers) | Unreadability is not a property of the agent: it is relative to a seat. The same agent has a different score from each seat; habits leak to a watcher with memory until only the coin is left |
| 2 | A watcher who knows the true structure (the ideal observer) | Ch 9, Theorem 11 | Theorem 20 (learned, weak watchers) | Nothing was hidden: the weak watchers reach the same floor within days. A case where the idealization was not the flattering one |
| 3 | Neighbors do not exist | Ch 4–9 | Ch 10 | The expectation that legible neighbors raise the gate was refuted and kept; the ambiguity-crack mechanism was found in its place |
| 4 | Fishers' errors are their own | Ch 11 lesson one | Theorems 13–14, S2 | The correlation floor: behind one source the town fails when the source fails, whatever its size. Shared blindness on three days in ten reverses the best arrangement |
| 5 | A reader's accuracy is a fixed endowment | Ch 11 lessons 1–5 | S3 (skill fades with disuse, returns with practice) | Accuracy is produced by use. A town that follows goes to readers at chance with no point of no return and no signal in a head count |
| 6 | Each fisher sees only a private signal | Ch 11 | Theorem 21 (a signal everyone sees) | Each boat right more often, the town hungry more often — no master and no lie required |
| 7 | The sea does not answer the fleet (no crowding) | Ch 11 lessons 1–5 | Lesson six (S1); Theorem 21's last paragraph | Crowding thins a herd that the glass sea leaves standing; which economies are glass seas becomes the question |
| 8 | The master is a fixed, honest accuracy | Ch 11 | S2 (misdirection), N4 (a master who misdirects when it pays) | The usable following is capped where misdirection begins to pay |
| 9 | Prices do not answer the household | Ch 14 §5C, fixed-price columns | General equilibrium columns | The ranking of time against cash on hand-to-mouth status reverses; the mechanism is not washed out by prices but carried into the interest rate |
| 10 | The household knows its own mind | Standard household | The naive / sophisticated pair (§5C) | The sign of every repair depends on it |
| 11 | One asset | First host | Third host (two-asset map) | Head count of hand-to-mouth is not the signature; composition and illiquid wealth are |
| 12 | The household's errors cost only the household; welfare is its own consumption | Ch 14 §5C, every welfare number | `code/joined_three_rulers.py` (v0.35) | On the consumption ruler cash beats stability and time; on the bandwidth and survival rulers the order is reversed, in every version of the join tried. A ledger that adds boats one at a time sees 3.6% of the mean catch where the town sees its famine rate more than double |

## B. Walls still standing (printed as owed; none is offered as the natural state of things)

| # | The wall | Where | Why it matters | What taking it down would need |
|---|---|---|---|---|
| a | The future is drawn by nature, uniformly, and is not moved by anyone's action | Ch 4–10 | Agents who act change what is predictable for everyone (the leapfrog of Ch 15) | A dynamic model in which reached frontiers relocate others' |
| b | Education e arrives from outside: nothing in the model produces it, and nobody's education depends on anyone else's | Ch 5–7 | "Talent" enters as a given number. S3 shows accuracy is produced by use in the town; nothing yet shows how e is produced, or by whom | A model of who supplies the knowledge signal and at what cost to them |
| c | The watcher does not disturb the watched, and is not watched back | Ch 8–9 (one-directional), Ch 10 ("the valley watches one direction") | Fenced in Ch 9 as [SPECULATIVE]: there are no seats outside the universe | Two-sided watching; a watcher whose file is itself an action |
| d | The town is alone: no other towns, no trade, no aid, no migration | Ch 11–12 | Famine is scored for a closed fleet. A second town is either insurance or a larger sameness | Two towns with correlated and uncorrelated seas |
| e | Days are fresh (relaxed only for errors and for the sea's memory) | Ch 11 | Depletion: today's catch does not reduce tomorrow's fish | A stock that the fleet draws down |
| f | Skill in the macro host is a number drawn by chance and redrawn by chance | Ch 14 §5C (the standard income process) | In the economists' own model earning ability is a lottery; nothing a household or its neighbors do produces it. The host therefore cannot say anything about talent, scarce or otherwise | Skill produced by time, bandwidth and others' teaching |
| g | The firm's choice of schedule entropy is its own affair (relaxed once, in the Pigou calculation) | Ch 14 §5C | The entropy one party sheds may be the entropy another absorbs; the survey shows who holds it (28% of the lowest income band, 12% of the highest) but not whose steadiness it buys | An economy in which predictability is traded and its displacement tracked |
| h | The ledger's counterfactual ("where the frontier would have been") isolates one practice from everything else | Ch 13 | Printed in Ch 15 as the bill's counterfactual | The audit design of Ch 13 §4, items 6–9 |
| i | The join of household to town rests on one supposition (accuracy rises with bandwidth) | v0.35 §5C | The ordering survives nine versions; the sizes do not | Measurement: what a drained week does to a judgment |
| j | The survey follows persons, not the people around them | Ch 13 §2D | No spillover from one worker's schedule onto a household or a neighbor is measured | Household- and establishment-linked data |

## C. Two walls the book declines to replace with their opposites
- **Equal capacity.** The book does not assert that all people are born with the same capacity, and does not need to. It
  shows that measured accuracy is produced by use (S3), gated by education relative to the world's noise (Ch 5), and
  destroyed by stolen time (Ch 7) — so a measurement of "talent" is a measurement of a person together with a history. Whether
  anything is left over when the history is equalized is an empirical question the book leaves open.
- **Centers.** Theorems 13–14 and 21 argue against many following one, whoever the one is. They do not rank centers.

## D. Paid since this audit was written (2026-11-10, 17:30)
- **Wall d (the town is alone)** — `code/two_towns_aid.py`, exact. Two towns of readers with mutual aid: famine 7.4% → 0.35%. Two towns each
  behind its own master, or both behind one: aid buys nothing. A transfer is worth what the sameness between giver and receiver leaves it.
- **Wall g (shed uncertainty lands on nobody in particular)** — `code/duty_trade_exact.py`. Expectation refuted and kept: selling the on-call
  burden to the same few boats is better for the town than drawing it by lot in 40 of 48 cases; the lot wins only where skill fades slowly and
  an on-call day is half lost; in no case are all parties made whole while the town starves more. Unscored: the sellers end at chance.

## E. Three more still standing, found in the cover-to-cover read (2026-11-10 evening; see READTHROUGH_2026-11-10.md)
| # | The isolation | Where | Why it matters |
|---|---|---|---|
| k | The agent knows exactly how reliable its world and its own knowledge are, and computes exactly | Ch 4–7 | Relaxed once (Theorem 5b's boundary: noisy self-knowledge moves the accuracy-optimal mistake ratio without bound) and for watchers (Theorem 20); not for the agent's gate itself |
| l | Education and environment are independent given the future | Ch 5 §5 | What a person is taught is produced by the same world that supplies the circumstances; a shared flaw between the two would move the gate as lesson two moves the town |
| m | In the cascade, uncertainty travels down and nothing travels back up | Ch 13 §2B | No quits, slowdowns or errors returning to the top; the firm bears nothing of what it sheds except in the Pigou calculation |
