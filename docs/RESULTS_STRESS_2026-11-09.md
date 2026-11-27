# Stress campaign — consolidated results and the conditions they put on the book (2026-11-09)

Companion to `STRESS_CAMPAIGN_v1.0.md` (objectives and status) and `THEOREMS_v1.md` (entries S3–S10). This file
states, result by result, what the book may claim and under which condition, so that §5C and Chapter 15 can be
written from it. Rig results (#1 sign map, #2 plateau bound, #4 town stress, #6 living town) are appended when
they arrive.

## What holds across every host, face, criterion and grid tried
1. **GE transmission into the real rate.** Bandwidth cuts asset demand at fixed prices; with bonds fixed, r rises
   (0.50 → 0.66–0.68%/qtr) — in the sticky-wage host, in the own-hours flexible-wage host, with three or five skill
   states, at three grid resolutions, under every face that touches the discount rate or the choice noise (pure
   attention moves it by +0.01 pp only). *Claim as unconditional within the model class, with the attention caveat.*
2. **The gate is a cliff in general equilibrium.** Hours through a group's time gate drop aggregate bandwidth
   discontinuously; linearization reports nothing at the gate; nonlinear paths show output +40% to ×2 over the
   linear path and balance-sheet repair cut in half when an expansion crosses it. *Claim as a theorem-level
   structural fact (the position of the gate is a constant; the asymmetry around it is not).*
3. **The dose–response is monotone and zero at zero.** *Unconditional.*
4. **Every repair's sign depends on the household's knowledge of its own mind.** Naive: repairs help (2–4 pp HtM);
   sophisticated: time transfer null, stability backfires — in both hosts. *Claim as a stated condition; the
   book's default is naive, dated.*

## What holds under a stated condition
5. **MPC amplification (×1.8 impact)** — only in the sticky-wage, demand-determined host. With own hours against a
   flexible wage the taxed economy responds *less* (×0.7, confirmed by nonlinear paths). *Claim for the first host
   only.*
6. **Stability beats the equal-dollar transfer on HtM** — under tunneling, present bias or sparse attention; *not*
   under pure logit noise; and only when HtM is measured as a band (within 0.15–0.30 of quarterly mean income of
   the limit), not at the limit itself. *Claim with both conditions.*
7. **P-C residual (HtM persists after liquidity repair)** — holds in the one-asset host with the band measure;
   reverses at the exact limit. *Claim with the band condition; the two-asset host is owed.*
8. **The Pigou wedge (planner's entropy below the firm's)** — under the book's welfare criterion (degraded planner
   scored at the undegraded horizon). Under any criterion honoring the shortened horizon as preference, welfare
   rises with entropy and the planner subsidizes the drain. *Claim with the criterion stated as a premise.*
9. **Time transfer vs money transfer.** Time wins on bandwidth and welfare in every host; on HtM status it wins only
   in the one-asset GE case, and loses at fixed prices and in the own-hours host. *Withdraw the HtM form of P-A′ as
   a general claim; keep "the two instruments buy different things" and the price-dependence warning.*

## What the audit must do (from #7, #8)
- One cross-section with free time measured to σ = 0.1 of its range detects a sharp gate at N ≥ 3,000 (power 0.99);
  it cannot distinguish a gate from a ramp of half-width 0.25 at N = 10,000. BIC-type model selection fails under
  measurement error; a size-controlled max-LR test is the rule.
- Estimates are regime-specific (transmission multiplier 1.4/1.8/1.7 at S = 0.5/1/2): Lucas applies.
- Hand-to-mouth is a band. Instrument comparisons must hold or model prices.

## What the own-hours host adds (#10)
- 91% of low-skill households work below their own gate in the control: the floor is sold for income before any
  bandwidth tax exists. A freed hour is kept (Δhours +0.005), not sold back; the below-gate share falls 15 points.
- A working-time cap destroys welfare (−1.5 utility units, Y −3%) with the below-gate share unchanged; a wage
  subsidy of equal cost raises welfare. The book's instruments are stability and time, not prohibition.
- The sophisticated household collapses this host too (97%/86% below gate, r 1.32%): the naive ruling is not
  host-specific.

## Rig results (W2, W3, W4 — received 16:26)
- **Plateau edge.** n = 3 closed at 1 − 1/log₂3; n = 4 certified in [0.3105, 0.334]; n = 6 vertex at or above the
  n = 4 ceiling. *Claim: one case closed, one fenced; the edge does not fall as futures are added.*
- **Town under stress.** The dose rule survives as: follow the channel whose errors are independent of the rest,
  in proportion to its margin net of its lies. The all-readers headline (famine 7%) is confined to readers whose
  errors are their own across readers and days; with bad weeks it is 51–65% and a bloc beats it; with shared
  blindness on 3 days in 10 only a bloc behind an independent master survives. *Claim the structure, not the headline.*
- **Town that stops reading.** No point of no return (refuted, kept). One attractor from any start; with slack in
  the crowding and fading faster than recovery, 0.7–0.95 of boats follow and readers are at chance; under the
  strongest crowding a third still act on readings that carry nothing. *Claim: a slope with one bottom; invisible
  to a head count, visible on the aim ruler; reversible when its causes move.*

## The sign map (W1 — received 18:20)
400 random economies, 331 solved. **Unconditional:** asset demand down, real rate up, dose monotone (331/331);
entropy raises the rate (329/331); stability beats the transfer on welfare (242/243 naive). **Conditional:** every
hand-to-mouth claim — near-universal at EIS 0.5 (98–99%; stability-vs-transfer 86%), about half under log utility,
80% there where tunneling dominates noise. P-A′'s HtM form holds in 39% of naive economies: withdrawn. *What the book
claims after the map: the mechanism's signature in the price of credit and in welfare is robust to the constants; its
signature on balance sheets depends on which face of the degraded optimizer dominates, and an audit scoring only
hand-to-mouth status can miss it.* One in six economies did not solve; they are missing from every count.
## The two-asset host and the own-hours dynamics (night)
- **Two assets.** The mechanism's robust signature is wealth and its composition: illiquid −22%, liquid −15%, liquid rate
  +1.6 pp/yr, wealthy hand-to-mouth converted to poor hand-to-mouth (26% → 18%; 19% → 29%) with the head count nearly
  flat. P-C holds. Time and stability win on balance sheets; cash wins on welfare at fixed returns. *Claim: P-C is not a
  one-asset artifact; the welfare ranking of stability over cash is a one-asset GE result and is scoped to it.*
- **Own hours, large easings.** Model/control cumulative output 0.80 (small), 1.01 (100 bp), 1.21 (300 bp). Most of the
  nonlinearity is the lumpy hours choice both economies share.

## Night run on the rig (N1–N4 — received 2026-11-10 07:15)
- **N1, sign map at 800 draws (688 solved).** No claim changes category. Unconditional: asset demand, real rate, dose
  (688/688); entropy → rate 683/688 (526/526 naive); stability beats transfer on welfare 524/526 naive. Conditional: the
  hand-to-mouth claims (97–98% at EIS 0.5; about half under log utility; 73% vs 33% above/below the median
  tunnel-to-noise ratio). Unsolved draws (112) load on low income risk and high debt, not on bandwidth constants.
  *Claim unchanged; counts updated.*
- **N3, plateau n = 4: closed to 2e-4** at (5 log₂5 + 9 log₂3 − 6)/64 ≈ 0.3105. **N2, n = 6: ceiling 0.641** — useless;
  the tool does not scale. *Claim: closed at three, fenced to the fourth decimal at four, not monotone in the number of
  futures; the reference world's edge stays open with a floor of 0.335.*
- **N4, fishers who consult yesterday; a master who misdirects when it pays.** The public-signal window (Theorem 21 in
  the book, S11 in the ledger): a public signal more accurate than a reader and less accurate than the readers' majority
  is individually rational to follow and collectively ruinous — exact, no master needed. The self-interested master: the
  usable dose is capped at the following where misdirection begins to pay. *Claim: both as stated; the first is a theorem.*

## Correction, 2026-11-10 (afternoon): how welfare may be claimed
- Items 6, 9 and the sign map's "stability beats the transfer on welfare" are statements about the MECHANISM'S SHARE
  (model gain minus control gain). They may be printed only with that wording.
- On the household's own ledger inside the taxed economy, equal-cost cash beats stability (178/182 two-asset economies;
  +1.38 vs −0.07 in the one-asset printed economy) and beats time (181/182). Halving low-skill schedule entropy is worth
  about 0.002 of mean quarterly income per quarter in cash; the program was priced at 0.02 (an assumed constant).
- *What the book may claim:* stability and time are the instruments that act through the mechanism; whether they beat
  cash for the household depends on the price of providing them, which is not known, and on values this host cannot
  score (it counts consumption only). *What it may not claim:* that the modeled household is better off with stability
  than with the same dollars.
- Two-asset map: illiquid wealth and the composition of hand-to-mouth are the robust signatures (182/182, 181/182);
  liquid wealth and its rate hold in six of seven; the rest is conditional as in the one-asset host.
