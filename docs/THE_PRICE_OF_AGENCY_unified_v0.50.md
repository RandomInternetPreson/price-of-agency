# THE PRICE OF AGENCY
### Freedom, measured. Theft, priced. No opinions required.
Aaron Alai, with Claude (Anthropic) as mathematical collaborator — draft v0.50

---

## How to read this book

This book runs on two assumptions about the world, and only two:

**Axiom 1. No one has perfect knowledge.**
**Axiom 2. Mistakes are inevitable.**

That is the entire list — and because everything downstream leans on
these two sentences, they will return by name wherever a theorem
stands on one of them. If you accept those two sentences — and no
physicist, economist, priest, or skeptic can demonstrate or prove otherwise — then
everything that follows is either *derived* from them or *labeled* as
something less. (Every model in the book adds structure of its own —
which signals exist, how errors correlate, what counts as survival —
and each chapter's §5 prints that structure and says what travels
beyond it.) The labels are printed beside every claim:

- **[PROVEN]** — a proof you can read, short enough to check by hand.
- **[EXACT]** — computed by exhaustive enumeration, no sampling, no
  approximation.
- **[NUMERICAL]** / **[MC]** / **[SIMULATION]** — computed with stated
  error, or by many simulated lifetimes with exact bookkeeping inside
  each; the weakest results in the book, and marked so.
- **[DATA]** — measured in the world by someone else and tabulated
  here; descriptive unless a design is named, and never a proof of a
  model.
- **[CONJECTURE]** — a potential pattern, not proven.
- **[SPECULATIVE]** — an interesting idea, fenced off so it cannot
  pretend to be a result.
- **[REFUTED — kept]** — something assumed a priori that the
  mathematics killed. There are several, and they are kept, because
  you may have had the same assumptions.

Every chapter is built the same way: §1–2 are for every reader; §3
onward for those who want the machinery; §6 for anyone who trusts
nothing — the best kind of reader this book can have.

And the book has two doors. Part I is the physics: the license under
everything after it, in three short chapters. A reader who came for
the schedule and not the particle can start at the harbor in Chapter 4
and miss nothing the measuring depends on; Chapter 3 says in one
sentence what the physics contributes, and Part I is there whenever
the license is questioned.

One more rule. The word *theft* appears throughout. It is defined
mathematically in Chapter 7 — a measurable displacement, like a dent
measured with calipers — before it is ever used as an accusation. If you
dislike the word, strike it and read the equations. They do not change.

---

# PART I — THE VERDICT AND THE APPEAL

## Chapter 1. The sealed verdict

There is a sentence that has been said to students, to prisoners, to
employees, to whole populations, for about a century, always with the
same borrowed confidence:

*"Free will is an illusion."*

Notice what kind of sentence that is. It is not an argument — arguments
can be answered. It is a claim of *authority*: somewhere, allegedly, in
mathematics you have not read, the question was closed, and your
protest is not a position but a symptom. You are, the sentence implies,
a very complicated rock — and everything that follows from being a rock
follows quietly: a rock cannot be robbed of choices it never had; a rock
cannot be owed an education it could not use; what is done *to* a rock
is arranged, not inflicted.

Living under an unanswerable sentence is a particular kind of
confinement. This book calls it the sealed verdict: a judgment passed
on your deepest nature, in a court you are forbidden to enter,
delivered to you as final. Most people respond to a sealed verdict in
one of two ways. They ignore it, and live as if free, with a small
unpaid debt of doubt. Or they accept it, and discover
that acceptance is oddly convenient for whoever is speaking.

There is a second sentence, politer, usually from kinder mouths, that
does the same work by shrug instead of decree:

*"It doesn't matter whether you have free will or not."*

Notice what this one accomplishes. It concedes nothing and closes
everything: no need to read the mathematics, because nothing allegedly
hinges on it — live your life either way. The full answer to the
second sentence is this entire book. The short answer: it matters, and
it matters in the way things matter that can be counted. Whether a person's actions are partly
their own decides whether they can be *robbed* — whether taking their
time, their options, their room to be wrong is an injury or merely a
rearrangement of objects; whether an education is owed to something
that could use one; whether what lands on a life was inflicted or just
occurred. Every one of those questions turns out, in the chapters
ahead, to be a measurable quantity with a price. And the shrug has
been the accounting instrument by which that price is set to zero.
"It doesn't matter" is what it sounds like when the bill is being
sent to someone else.

This book does not argue that you have free will. The wording is
exact: *it does not claim to prove freedom exists.* No honest person currently can. What can
be done — what has now been done, with theorems — is smaller and
sharper: the *authority* of the sentence can be revoked. It can be shown,
exactly, what physics does and does not require; it can be shown that
the deterministic reading is a choice with a price sheet, not a
conclusion with a proof; and it can be shown that the verdict
was never entered — that at every size at which the question has been
priced, the universe declines to sign it.

Revoking an authority is not a metaphorical act. It requires arithmetic
the authority cannot survive. Chapter 2 is that arithmetic.

And then — because a door is only interesting if something lies beyond
it — the rest of the book walks through. If a universe *permits* what this
book calls apparent non-determinism, then agency becomes a quantity: a
thing with an anatomy, a price list, thresholds, floors, and thieves.
The remaining chapters measure it.

## Chapter 2. The price of locality, in one chapter

In 1964, John Bell proved that three innocent-sounding assumptions
cannot all survive contact with experiment. Stated plainly:

1. **Locality.** Influence does not travel faster than light.
2. **Determinism.** Outcomes are fixed by prior facts.
3. **Measurement independence.** The experimenter's choice of what to
   measure is statistically independent of the hidden facts of the thing
   measured — in slogan form: *the universe does not rig your questions
   to fit its answers.*

Experiments violate Bell's inequalities. Therefore at least one
assumption is false. Physicists mostly shop between abandoning the
first (resulting in spooky action) and abandoning single outcomes altogether (resulting in many
worlds). The third exit — that measurement independence fails, not by
cosmic conspiracy but lawfully and partially — was long treated as the
disreputable door. Then in 2010, Michael Hall asked the question that
changes the register of the whole debate: *if you take the third exit,
what is the fare?* And he answered it exactly, for the simplest case:
to reproduce the quantum correlations of two entangled particles with a
local, deterministic model, measurement independence must be relaxed by
precisely (√2 − 1)/3 — about 13.81%. Not all of it. Not none of it.
That number.

A door with a posted price is a different object from a forbidden door.

Hall priced the two-particle case and one fragment of the three-particle
case, and left the general problem open in 2011. It stayed open for
fifteen years. The solution — the mathematics this book's lineage rests
on — computes the exact minimum relaxation for the full faithful
statistics of the canonical multiparticle experiments, certified in
exact arithmetic out to twenty-two particles, and finds the answers are
not a mess but a law — stated there for every size, and since proven
for every size [PROVEN / EXACT; the published record — arXiv:2608.00124,
Zenodo DOI 10.5281/zenodo.21445609]:

    F = R / (2(R + 1)),   where R doubles with every second particle.

One third at three particles. Two fifths at five. Four ninths at seven.
8/17, 16/33, 32/65 — a staircase, climbing with perfect regularity
toward, and this is the theorem that matters most, a **ceiling it can
never reach: F ≤ 1/2, at every size, forever.** The universe's
statistics never require measurement independence to be relaxed by more
than half. Total determinism-by-conspiracy is never *forced*. The
door is never welded.

The staircase was the first paper. There is now a second [CONJECTURED
SURFACE, certified exactly at the quantum point and at six rational
points; the published record — arXiv:2608.18886], and Part V takes
its exhibit from it. The original experiment that
started all of this — two particles, two detectors — turns out to have
not one posted price but two, on two different doors: how much
measurement independence a local account must relax, and how
efficient its detectors are permitted to be. The second paper computes
the exact exchange rate between the two — relax less of one, pay
more of the other, at a rate written down in closed form — exact to the digit where it has been certified, conjectured between — and then
does something no result in this lineage had done before: it finds a
specific, physical quantity that the standard experiment is
mathematically incapable of seeing — checked only at the percent level
through four decades of the most scrutinized experiments in physics,
never below it, which is where the surviving accounts live — and it
hands over a protocol that any well-equipped laboratory can run to
measure it there. Whichever way that measurement comes out, a named
family of accounts is bounded an order of magnitude tighter than the
record now holds it. And one thing it cannot do, whichever way it
comes out: touch the license. The ceiling above was proven by
arithmetic over every strategy a local account could adopt; no
coincidence count can raise it or lower it. The scan audits which
ledger the surviving accounts pay in — never whether the door is
open. (And to keep this book's own fence intact: that exchange rate
prices trade-offs *within* the surviving local accounts, between their
two internal ledgers — never *across* the exits from Bell's theorem,
which remain unranked.) An exact price, an unmeasured column, an
instrument anyone can pick up: the second half of this book uses all
three.

Now, exactly what this result licenses and what it does not:

**It does not prove you are free.** A fully superdeterministic universe
remains logically consistent. So does ordinary quantum mechanics with no
hidden layer at all. The staircase takes no side.

One argument, made by the author of the two papers and labeled as an
argument, not a result. To compare exits at all, a common currency must
be chosen — and here is a principled candidate: score each exit's extrapolation against the
constraints every *other* science already answers to. Thermodynamics.
Information theory. No privileged observer standing outside the
universe. No effects preceding causes. Every other discipline must
tell its story through that highly constrained lens; the exits from
Bell's theorem have historically enjoyed a free pass from it — perhaps
precisely because this third exit went unpriced. Under that currency,
the priced exit is the conservative one: no influence outrunning
light, no unobservable proliferating worlds, no retrocausality — full
congruence with the physics everything else already obeys. Under
other currencies — dynamical parsimony, or the refusal of hidden
variables altogether — other exits win, which is why physicists still
disagree, and why this paragraph is an argument. There is a second
candidate currency, worth naming with its own caveat attached: the
capacity to be audited. The canonical forms of the other exits are
built to agree with quantum mechanics everywhere, which makes them
untestable against it by design — their falsifiable cousins exist,
but purchase their testability by disagreeing with the record in
territory already measured, where the record squeezes them. The exit
priced in this book turned out to carry its testable content in a
column no experiment had measured — congruent with everything ever
recorded, and still auditable [the sequel, arXiv:2608.18886; the
exhibit that closes Part V tells that story — the unmeasured quantity,
the theorem that hid it, the protocol that measures it]. And it does more than survive there. The paper that priced the exit also built it — an explicit local mechanism, with no stochastic ingredient, that pays exactly the posted price — and both the price and the mechanism come with things an experiment can look for. The solved detection sector predicts a fringe in the total coincidence rate as the analyzers turn (the exhibit of Part V), in a quantity recorded for forty years at the percent level and never below it. And the mechanism itself leaves a fingerprint on the correlation curve every Bell experiment measures: a softening of its extremes — where the quantum curve reaches perfect agreement and perfect disagreement, the mechanism falls short by up to about a percent, concentrated between the Bell angles. Resolving the mechanism more finely shrinks that softening and moves it between the angles tested; at every resolution tried it keeps the same shape, and whether it survives to the continuum is a question the paper leaves open and says so. No other account on the record is all of these at once: local, deterministic, priced below total conspiracy at every size, built as an explicit mechanism, and specific about what an experiment should find — a softening in a curve every Bell experiment already records, and a fringe in a sum that quantum mechanics says is flat. And whichever way those experiments come out, the ceiling of this chapter stands: the scan decides which ledger the surviving accounts pay in, never whether the door is open. Under that currency too, the priced
exit stands alone — and the same caveat applies: an argument, not a
theorem. But the reader is entitled to notice which currencies the
rest of science is already paying in.

**It proves that no one can claim mathematics took the side against
you.** Anyone asserting that physics *requires* the fully rigged
universe is now making a claim with an exact counter-theorem. The
sealed verdict — its authority borrowed from proofs that turn out not
to lend it — is vacated on appeal. What remains is, *just, like, your opinion, man* — and you are free
to decline opinions.

Hold on to the shape of what just happened, because the entire book
repeats it at larger scales. A question that sounded metaphysical
(*am I free?*) was converted into a question with units (*what is the
minimum price of pretending otherwise?*), and the answer came back
bounded, exact, and universal. Freedom was not proven. Freedom was
*priced* — and its price, in measurement independence, was capped at
one half.

The next chapter names the thing on the far side of the door — apparent
non-determinism — and states exactly
what the physics contributes to it (a license, never a number) before
the measuring begins.

---

## Chapter 3. Apparent non-determinism: the claim, precisely

Every framework has one chapter where a careless sentence would poison
all the others. This is that chapter, so it will be short and it will be
exact.

The thing on the far side of the door needs a name that does not smuggle
in a conclusion. *Free will* is a courtroom of a phrase — two thousand
years of theology and neuroscience shouting in it. This book uses a cooler term:
**apparent non-determinism**, AND for short, and in mathematics the
symbol δ_A. Here is what it means, in one breath: *an entity exhibits
AND to the degree that its actions cannot be predicted from its local
circumstances.* A rock exhibits none — give the slope and the rain,
and the rock is given. A person may exhibit a great deal — or,
under certain conditions this book will price with uncomfortable
precision, almost none.

Note what the definition does not mention: souls, quantum mechanics,
consciousness, or the truth about determinism. AND is *apparent* —
defined relative to what an observer can predict — which is exactly what
makes it measurable, and measurability is the entire premise.

Now the sentence that must be said with total clarity, because every
hostile reader arrives with its refutation pre-loaded, aimed at a claim
this book does not make:

**The physics of Chapter 2 contributes a license, never a number.**

The staircase does not cause your Tuesday. The ceiling F ≤ 1/2 does not
govern wages, and 8/17 at nine particles implies nothing about nine
senators. Anyone who tells you this book derives economics from quantum
mechanics has not read this paragraph, and you may return them to it.
What the physics contributes is one thing, and it is not small: it
guarantees the *possibility class is open*. Before Chapter 2, "agents
whose actions are partly independent of circumstance" was a hypothesis a
determinist could dismiss with borrowed authority. After Chapter 2, it
is a standing possibility of the universe, priced and bounded, that no
one can strike from the table. Everything measured in the rest of this
book lives on that table — and lives or dies by its own evidence, in its
own units, exactly as the survival of chemistry does not depend on
re-proving atoms in every reaction.

One question remains before the measuring starts: why did settling the
physics matter, if the numbers never transfer? Because of what the
alternative licenses. If agents were rocks *to every possible observer*
— if the universe published a complete state from which every action
followed — then nothing could be stolen from them, and the theft this
book prices would be a category error, like robbing gravity. The
license says no such publication is forced. The ledger itself is
narrower than the license and survives either way: it is defined in a
seat, from what an observer with incomplete information can predict
(Part III), and a deterministic agent with private knowledge scores on
it exactly as a stochastic one does. What the license removes is the
dismissal — that the whole ledger is about nothing. It converts every
coercion from a neutral arrangement of matter into a *possible taking*,
and possible takings can be measured, audited, and charged for. That conversion is the door. The
rest of the book walks through it.

---



# PART II — ONE AGENT: THE ANATOMY OF FREEDOM

# Chapter 4. The Leaf and the Timetable

## §1. The idea, in plain words

The two axioms say what this book assumes. One further decision, made in
this chapter, says how it measures — and everything measured afterward
stands on it: **freedom needs two rulers, not one.**

The obvious single ruler — call it unpredictability — asks: after seeing
someone's circumstances, how much doubt remains about what they will do?
It sounds right. It is measurable. And it fails, in a way so instructive
that the failure became the foundation. Because two very different
things score high on unpredictability: a person steering their own life,
and a dropped leaf tumbling in the wind. And two very different things
score low: a coerced person, and a competent one in a world where the
right move is obvious.

So this chapter splits the measurement in two. The first ruler,
*independence*, keeps the old question: how little do circumstances
predict your actions? The second, *aim*, asks the question the leaf
fails: how much do your actions have to do with what actually comes
next? Freedom, as this book will use the word from here on, means scoring
on both rulers at once — and the entire book is a map of what that
double score costs, who pays it, and who takes it.

## §2. The story: the harbor

Stand on a harbor wall in a stiff wind and watch three people.

The **ferry captain** runs the posted schedule. Weather within limits,
she sails at the top of the hour to the island and back, the same
crossing she has made four thousand times. And note something easily
missed: she is never *wrong*. Her seamanship is real and her crossings
are flawless. But anyone holding the timetable and a weather report can
predict her whole day without watching her once. Her poverty is not
error. It is that everything she does was already written in her
circumstances.

The **lost tourist** is her opposite. He has no destination, no map he
trusts, and he wanders the quays turning wherever the crowd or a smell
or a seagull suggests. Nobody can predict his next turn — not you, and
not really him. By the single ruler, he is the freest person on the
harbor. And he is going nowhere. His unpredictability is genuine, and
it serves nothing.

Then the **sailor** casts off — heading upwind. Watch him closely,
because his behavior is strange by both of the other standards. He does
not do what the wind says: he tacks, cutting angles the gusts never
dictated, sometimes turning *toward* rough water. An observer reading
only the wind and the harbor cannot call his moves. But neither is he
wandering: every strange angle serves the same unwavering destination,
and he arrives. The wind pushed everyone on that water today; the
captain's route was written by it and the timetable, the tourist
scattered on it, and the sailor *used* it — visible in his wake as the
only track that disagreed with the wind and still ended at the chosen
port.

Independence without aim is the tourist. Aim without independence is
the captain. The sailor is what the two rulers, together, are built to
find.

## §3. The theorems

Three results fence the space the two rulers draw. Stated here in words;
formally in §4; proofs in the theorem file.

**Theorem 1 (The sage ceiling — Axiom 1, made quantitative). [PROVEN]** *Even a perfect agent —
complete knowledge of its own future, unlimited deliberation — cannot
reach total independence. Its remaining predictability equals exactly
what its environment already knew about that future.* You can never
rationally be less predictable than your world is informative; ignoring
a genuinely telling circumstance is not freedom but error. Every
environment posts a ceiling, and the ceiling belongs to the environment. Cybernetics reached a neighboring sentence fifty years earlier — Conant and Ashby's good-regulator theorem (1970), that every competent regulator must carry a model of what it regulates — and Theorem 1 is in its spirit: the sage's predictability is the model it cannot help carrying. The difference is the quantity measured. Conant and Ashby bound the regulator's structure; Theorem 1 prices its independence.

**Theorem 2 (Complementarity). [PROVEN]** *The environment's information
about the future is a fixed pot, split exactly two ways: it is
simultaneously the ceiling on the captain's aim and the floor under
the sailor's predictability.* One quantity, two debts. (The partition above is a statement about information
specifically; if aim is scored by raw success rate instead, the two
quantities no longer sum to one — the audit is printed in §5.)

**Proposition 3 (Starved is not free). [PROVEN]** *Strip an agent of
deliberation and its unpredictability rises — toward the leaf.* On the
single ruler, the most deprived agent scores as the most free. This
inversion is why the single ruler is not merely imprecise but dangerous,
and Chapter 7 will show it is exploitable.

## §4. The mathematics

The two rulers, built from plain parts.

*Doubt is counted in bits.* One bit is one fair coin-flip of remaining
uncertainty; three bits, three coin-flips. The standard name for
counted doubt is *entropy*, written H.

**Ruler one — independence.** Let A be the action taken and E the
circumstances an observer sees. H(A|E) counts the observer's remaining
doubt about A *after* seeing E. Scale it by the doubt a total stranger
would have (log₂ of the number of possible actions) and it lands on a
0-to-1 dial:

    δ_A = H(A|E) / log₂|A|

δ_A = 0: the captain — circumstances leave no doubt. δ_A = 1: the
tourist — circumstances say nothing.

**Ruler two — aim.** Let F be the future the agent is steering toward —
a state of the world the action is a bet on (where the fish are, what
the weather does, what the market will come to want), never an outcome
the action itself produces. F is exogenous to A everywhere in this
book; what that rules out, and why the audit of Chapter 13 needs it, is
said there. One more thing aim is not: a success rate. Information is
blind to relabeling — an agent who always does the opposite of what the
future calls for tracks it perfectly and fails every time — so aim
measures the capacity to track the future, not whether the tracking
was used well. The theorems of this book are about that capacity; a
success score adds a decoding the rulers do not see. For the agents of
this book the two move together, because every agent here is built to
seek reward and so decodes in its own favor — the perverse case is an
agent who knows the future and chooses to lose. Where the book prices a
loss of aim as a loss, that is the agent it has in mind.
The information the action carries about that future — written I(A;F),
the number of bits of doubt about F that watching A removes — measures
whether behavior is *about* anything. Scaled the same way:

    aim = I(A;F) / H(F)

The tourist: δ_A = 1, aim = 0. The captain in fair weather: δ_A = 0,
aim = 1. The sailor lives where both are high — and Theorems 1 and 2
say exactly how high both can simultaneously be.

**Theorem 1, formally.** For an agent with full knowledge of F and
ample deliberation, the acted policy is A = F, so H(A|E) = H(F|E), and

    δ_A(sage) = H(F|E) / log₂|A| .

The sage's ceiling is the environment's ignorance of the future — one
line, once the definitions exist. **Theorem 2** follows by splitting
H(F) = H(F|E) + I(F;E): the second term is what the vane can capture
(its aim ceiling) and the first is what the sage cannot shed (its
predictability floor). The two debts sum to the whole pot.

## §5. The model, and its audits

The world: a future F with n equally likely possibilities; an
environment signal that reveals F with probability 1−s; a knowledge
signal that reveals F with probability e; an agent acting on the exact
Bayesian posterior, with deliberation controlled explicitly. All
quantities computed by exact enumeration — no simulation, no fitted
parameters. (The agent is the standard bounded-rational one — a Bayesian posterior sharpened by a single deliberation parameter, the form Ortega and Braun derived from information-processing costs in 2013 — so nothing in the engine's driver is this book's invention. What the book adds is the second ruler held up to a driver already standard in its field.)

Audits, as the opening pages promised. Theorem 1 was machine-checked on five
hundred randomized worlds — arbitrary priors, arbitrary asymmetric
channels — with worst-case error at the limit of computer arithmetic.
Theorem 2 was checked the same way (no violations; equality exactly
where the proof says) and additionally stress-tested at alphabet sizes
up to 64. The complementarity identity is information-specific: re-run
with raw success rate in place of I(A;F), the two quantities no longer
sum to one, and no result in this book leans on the version that fails.
Proposition 3 is an exact limit of the model class and was replicated
under a second, independent model of deliberation in Chapter 7's
machinery — where the *direction* of the starved agent's drift turns out
to depend on what a mind falls back on when thought is taken, a fork
with consequences of its own.

## §6. The code

- `code/delta_A_v1.py` — both rulers computed across the full
  (education × noise) landscape; the four corner characters of this
  chapter appear as exact values.
- `code/verify_theorems.py` — the five-hundred-world checks of
  Theorems 1 and 2.
- `code/dichotomy_scaling_and_audits.py` — Theorem 2 at alphabet sizes
  16–64 on randomized channels; the success-rate audit.
- Formal statements and proofs: `docs/THEOREMS_v1.md`.


# Chapter 5. The Gate

## §1. The idea, in plain words

Here is the finding of this chapter in one sentence: **learning buys you
no independence at all — none — until what you know beats what your
surroundings already tell you; and the moment it does, independence
arrives all at once.**

The natural assumption — the one most readers will bring, because it
was brought here first too — is the opposite: the comfortable belief that every bit of education makes a person a bit
freer, smoothly, like filling a glass. The mathematics refused it. What it
handed back instead was a threshold: a gate. Below the gate, education
changes what you know but not what you do, because acting on weak
knowledge against a clear world is simply a mistake, and rational people
don't make it. Above the gate, your own knowledge outranks the world,
and your behavior stops being readable from your circumstances.

Education here means more than school. It is whatever leaves a person
knowing something their surroundings do not announce: a class, a
trade, an hour alone with a problem, years among the people they live
with. The gate does not ask where the knowledge came from. It asks how
often it is right.

One consequence deserves its own paragraph, because it runs against
instinct. *The clearer and more stable a person's world, the higher
their gate.* Someone whose environment is orderly, legible, fully
administered — where the "right" move is always obvious from the
situation — needs *more* education before any of it purchases
independence, not less. Order is not neutral. Order raises the bar.

## §2. The story: the intersection

Imagine learning to drive in a city where every intersection has a
working traffic light. You are given driving lessons — theory, judgment,
the physics of wet roads. Are you freer for it? Watch your actual
behavior: at every light you do what the light says, exactly like every
driver who never took your lessons. Your knowledge is real, but the
world is so legible that following it is always the right call. Anyone
watching the lights can predict you perfectly. Your lessons bought you
nothing visible — yet.

Now the storm knocks the lights out. Suddenly the intersection says
nothing, and the drivers split: most freeze or follow the car in front —
still readable, now from each other. But the driver whose training
finally *exceeds* what the intersection offers makes her own call —
yield here, roll there — and for the first time, watching the
intersection tells you nothing about her. Same driver, same lessons.
The lessons crossed the gate only when the world stopped answering
first. That is the whole theorem, lived: education pays nothing until
it wins the argument with your surroundings — and a world of perfect
traffic lights is a world where almost no one's education ever wins.

One more turn at the same intersection. The lights are out and her
training is good — but the two kinds of mistake are not priced alike.
If she follows the car in front and it goes badly, she has a dented
bumper and company. If she makes her own call and it goes badly, she
loses the car, and with it the job the car gets her to. At those
prices she follows the car in front, and she is right to. What decides
it is not what she knows. It is what one mistake of her own would cost
her, set against a mistake made in company: her **mistake budget**.
The theorem below gives the number. In a world that is right half the
time, lessons open the gate once they are right more than fifty times
in a hundred. Let her own mistake cost ten times the shared one, and
the same lessons must be right ninety-five times in a hundred before
she acts on them. Her lessons did not get worse. The price of using
them went up.

## §3. The theorem

**Theorem 5 (Activation threshold).** *In the model of §5, with
environment reliability 1−s and education fidelity e, a rational agent's
independence δ_A is exactly zero whenever e < 1−s, and strictly positive
whenever e > 1−s. The gate sits at*

    e* = 1 − s

*and its location does not depend on how finely the future is divided
(proven and verified for every alphabet size tested, 4 through 64).*
**[PROVEN]** 

Below the gate, the agent's behavior has a name in economics: an informational cascade (Banerjee 1992; Bikhchandani, Hirshleifer and Welch 1992) — the rational discarding of a private signal when the public one is more reliable. Cascade theory studies the sequence of such decisions and how fragile it is. Theorem 5 is in its spirit and asks a different question: where the threshold sits, as a race between two reliabilities — and finds the answer indifferent to how finely the future is divided.

In words: education fidelity plus environmental noise must exceed one.
Your knowledge and your world are in a reliability race, and only the
winner steers you.

**Theorem 5b (The mistake-budget gate). [EXACT]** *The gate above
assumed a mistake costs the same whichever way you make it. Let a
self-directed mistake cost κ times a conformist one — the arithmetic
of living without a buffer, where one wrong bet of your own means
eviction — and the gate moves to*

    e*(κ) / (1 − e*(κ)) = κ(1−s)/s + (κ−1)(1 − 1/n),

*recovering e\* = 1−s exactly at κ = 1 and rising with κ.* The second
term is the case where both sources are wrong — paid once by the
conformist, κ times by the self-directed — and it keeps the number of
options in the formula: more ways to be wrong, a higher gate. At κ = 10 in a half-noisy world, the gate sits at 0.936
with two options, 0.947 with eight, and under 0.95 with any number:
near-perfect knowledge required before independence is rational. The consequence deserves
plain statement: **a person can stand well above the education gate
and remain rationally conformist — for want of a mistake budget.**
Environments that permit mistakes are not a kindness; they are a
precondition. And a mistake budget, like time, is a resource that can
be taken: a zero-buffer life is a welded gate wearing different
clothes. The gate assumes
the agent knows its own reliability. With noisy self-knowledge, the
mistake ratio that maximizes a population's *per-decision accuracy* is
one where the population sits at its gate; below one where most sit
above it (a margin silences people who should act); and without bound
where most sit below it and do not know it — there, the
accuracy-optimal rule is that nobody acts on their own judgment. That
last case is the shared-tutor town of Chapter 11: the most accurate
town per decision, and the one that starves. Accuracy and survival
part company exactly there, which is why Chapter 14's first rule —
past the gate — comes before its others, and why the κ a zero-buffer
life actually imposes, around ten, is justified by neither objective.
(Who gets to buy mistake budgets back, and at whose expense,
is Chapter 13's business. Organizations have long had words near this one — *slack*, in Cyert and March's behavioral theory of the firm (1963); *psychological safety*, in Edmondson's study of teams (1999) — and the mistake budget is in their spirit while being a sharper object: a ratio, κ, that moves a proven gate by a computable amount.)

## §4. The mathematics

Two quantities, built from plain parts.

*Independence*, δ_A, asks: after seeing your circumstances, how
uncertain does an observer remain about your action? Uncertainty is
measured in bits — one bit is one fair coin-flip of doubt. If your
circumstances pin your action completely, the observer holds zero bits
of doubt: δ_A = 0, the rock. If circumstances say nothing about your
action, doubt is maximal: δ_A = 1. (Formally: δ_A = H(A|E) / log₂|A|,
the conditional entropy of action given environment, scaled to [0,1].)

*The gate*, derived. Your environment E points at your future correctly
with probability (1−s) + s/n — right most of the time, uniformly
confused otherwise. Your education K points correctly with probability
e + (1−e)/n. When the two disagree, a rational agent asks: which source
is more likely to be right, given exactly this disagreement? Bayes'
rule makes it a ratio of the two channels' odds:

    follow K  ⟺  [e + (1−e)/n] / [(1−e)/n]  >  [(1−s) + s/n] / [s/n]
              ⟺  n·e/(1−e)  >  n·(1−s)/s
              ⟺  e·s > (1−s)(1−e)
              ⟺  e + s > 1.

Four lines. Notice the alphabet size n cancels — the gate does not care
how complicated the future is, only who is more reliable about it.
Below the gate the agent follows E everywhere (δ_A = 0 identically);
above it, the agent defects to its own knowledge wherever the two
disagree, and δ_A jumps.

*The mistake-budget gate*, derived the same way. On a disagreement the
posterior's weights on the environment's future, on knowledge's, and
on neither stand in the
proportion 1 + n·(1−s)/s to 1 + n·e/(1−e) to n − 2. Acting with the
environment costs 1 when it is wrong; acting on knowledge, κ:

    follow K  ⟺  κ·[1 + n·(1−s)/s + n − 2]  <  1 + n·e/(1−e) + n − 2
              ⟺  e/(1−e)  >  κ·(1−s)/s + (κ−1)(1 − 1/n).

**Theorem 5c (The gate for any environment). [PROVEN]** *Drop the
symmetry. Let the environment be any channel at all, and for a given
signal let q_max be the posterior weight it puts on its favorite future
and q_k the weight it puts on the future the agent's own knowledge
names. The same four lines give the gate for that signal and that
disagreement:*

    e*  =  (q_max − q_k) / (q_max + (n−1)·q_k),

*which is 1−s in the symmetric world and in general a threshold per
signal — a surface, not a number — with the same knife-edge character
everywhere: below it the agent follows the environment; above it the
agent defects.* Checked against 215,000 Bayesian decisions on random
channels with zero disagreements. Chapter 15's "gate, generalized" is
closed by this line; what the symmetric world hid was only that the
threshold depends on how confidently the environment is pointing.

Two audits, because this book audits itself. The gate was re-derived
under a deliberately hostile redefinition of "buys nothing" (requiring
substantial, not merely nonzero, independence): the location moved by
less than one part in a thousand. And the smooth-education belief was
hunted across thousands of randomized worlds before its death was
accepted: the threshold appeared in every one. **[EXACT]**

## §5. The model

Everything above was computed in the simplest world that contains the
question. A future F: one of n possibilities, all equally likely.
An environment signal E: reveals F with probability 1−s, otherwise says
something uniformly random. An education signal K: reveals F with
probability e, otherwise uniformly random, independent of E given F.
(Where the education was acquired does not enter; only how often it is
right.) The agent sees both signals, computes the exact Bayesian posterior over
F, and acts on it (hurried agents were also computed via a softmax
deliberation parameter; the gate result quoted here is for ample
deliberation). Every number is exact enumeration over all cases — no
simulation, no sampling, no fitted parameters anywhere.

What the small world does and does not license: the *location* formula
e* = 1−s is proven in this class; the *existence and knife-edge
character* of the gate, per decision, survived every generalization
tried — alphabet sizes to 64, asymmetric randomized channels, hostile
redefinitions. One thing does not travel, and Theorem 5c says why: on a
channel whose signals point with different confidence, each decision
has its own threshold, and a population's activation against education
is a staircase of small steps rather than one cliff — the sharp
*aggregate* dead zone is a feature of worlds where every signal is
equally reliable. Constants are class properties; the per-decision gate
is not; the aggregate cliff is.

## §6. The code

- `code/verify_theorems.py` — the conjecture hunt that killed smooth
  education and exposed the threshold (runs in seconds).
- `code/delta_A_v1.py` — the two-axis landscape where the dead zone is
  first visible as the black region below the diagonal.
- `code/dichotomy_scaling_and_audits.py` — the gate at n = 16, 32, 64:
  zero below, ~0.93–0.95 above, at the predicted location every time.
- `code/mistake_budget_T18.py` — Theorem 5b in 196 worlds.
- Theorem 5's formal statement and proof: `docs/THEOREMS_v1.md`.
Reproduction: Python 3, numpy. No further dependencies.



# Chapter 6. The Frontier, and the Plateau

## §1. The idea, in plain words

Chapter 4 gave freedom two rulers: independence — how little your
circumstances predict you — and aim — how much your actions serve where
you're going. This chapter asks the natural next question: how well can
anyone score on *both at once*? Score everyone in the world on the two
rulers and plot them as points: somewhere out there is an outer edge,
the best simultaneous scores possible. That edge is called the
*frontier*, and this chapter maps it.

Two findings. First, the frontier has a hard trade built into it:
past a certain point, **every further unit of aim must be paid for in
visibility** — being more effective makes you more readable, at an
exact exchange rate. Second — and this is proven to exist, exactly —
there is a region whose existence is easy to doubt and no longer
possible to deny:
agents who are *perfectly* unreadable, circumstances predicting nothing
about them at all, whose actions nonetheless carry real information
about the future they are steering toward. Not much; the region is
narrow. But total
unreadability, with genuine aim inside it, is possible. This region
is the plateau, and the character who lives there is easiest to
meet at a card table.

## §2. The story: the card player

Watch a poker player — call her Ines — from the seat of someone trying
to read her.

A beginner is an open book: strong hand, big bet; weak hand, fold.
Read the bets, read the hand. The obvious fix — the one every beginner
is taught — is to mix it up: bluff sometimes, bet at random now and
then. That helps, but a patient observer still finds the pattern,
because "random now and then" still leans with the hand.

Ines does something stricter. She decides in advance what her betting
should look like *from the outside* — how often a raise, how often a
call, how often a fold — and she makes that outward pattern
**identical whatever the table shows**. Strong board or weak, early or
late: over her nights, her bets in any one visible situation are
spread exactly as they are in every other. To pull this off, when her
cards would push her one way more often than the pattern allows, she
uses chance — a private die — to pull her bets back until the outward
pattern is restored. Her randomness is not decoration on her
decisions; it is *shaped against what the table shows*, deliberately,
so that nothing the table shows predicts her. An observer with perfect
records of every visible card she ever sat behind can call her next
bet exactly as well as someone who never watched at all. What a bet
says once it is made is another matter: it carries a little about the
hand behind it, and that little is her winnings. The table can learn
from her bet. It can never see the bet coming.

Here is the strange part, and the theorem of this chapter: **Ines still
wins.** Not much — the discipline is expensive, because most of her
bets are spent maintaining the disguise rather than pressing her
advantages. But provably, exactly, more than chance — not more than
the captain who simply follows the table's tells, unless those tells
are noise more than half the time; the plateau's claim is information at zero
readability, not the best hand in the room. Perfect unreadability and
real winnings, together. That is the plateau.

And the plateau has an edge. If Ines wants to win *bigger*, she must
start pressing her good hands harder than her pattern allows — and
every extra dollar of expected winnings costs her a measurable amount
of readability. Tells are not a weakness of bad players. Past the
plateau, tells are the *price* of winning, posted by mathematics, and
no skill at any level makes the price go away.

## §3. The theorems

**Theorem 6 (The plateau). [PROVEN; edge OPEN]** *There exist
strategies with perfect independence — δ_A = 1 exactly, circumstances
predicting nothing — and strictly positive aim. The plateau extends at
least to c₀ — the aim of an agent who acts on the future exactly as
often as the world is wrong — and its exact edge is open; beyond the
edge, every additional unit of aim must be purchased with visibility.*
Full unreadability is never impossible; full aim is never unreadable
(Theorem 1's ceiling closes the far end). The trade is two-sided and
exact.

**A second refuted claim, kept. [REFUTED — kept]** The first printing
of this theorem put the plateau's edge at the end of Ines's simplest
strategy — follow the target a fraction λ of the time, compensate the
rest — and called that edge c₀: about five percent of full aim in the
reference world. It was the edge of that strategy, not of the plateau.
A later attack, mounted from a different direction — searching the
hidden strategies directly, as vertices of the set they live in, rather
than by gradient — found a strategy five times further out: *act on the
future whenever the world is wrong; scatter whenever it is right.* Its
aim has a closed form, printed in §4 — the aim of someone who follows
the future exactly as often as the environment errs — and an asymmetric
cousin goes further still. The plateau was five times wider than its
first estimate held. The old number is kept because the belief that
produced it — that hidden competence must be modest — is the natural
one, and it is wrong. 

Cryptographers hold the twin of this theorem under another name. Cachin's model of steganography (1998) asks how much hidden payload a message can carry while its visible statistics remain *perfectly* those of innocent cover text — and the plateau is that perfect-security case, with aim as the payload, the uniform action as the cover, and the whitening residual as the embedding. On this model class Theorem 6 is not merely in the spirit of steganographic capacity; it *is* that quantity. That is the strongest thing the book can say about any of its parts: the same arithmetic stands in another field, proved for another purpose, and agrees.

**A refuted conjecture, kept. [REFUTED — kept]** The natural first
belief — likely the reader's as well — was that the
frontier's best strategies were the simple ones — act on your knowledge
some fraction of the time, plain chance the rest. An optimizer owing no
loyalty to elegance found strategies strictly better. Chasing *why* produced Theorem 6: the
better strategies were Ines's kind — chance shaped against the visible
world, not sprinkled on top of it. The dead conjecture was the price of
the plateau's discovery, and both are printed.

**A sign worth remembering.** The plateau *widens* as the environment
grows noisier: c₀ rises with the chaos of the world. Storms are the
friend of whoever does not wish to be read. This sentence returns, at
the scale of a whole town, in Chapter 11.

## §4. The mathematics

The frontier, precisely: among all strategies available to an agent,
the set of best simultaneous scores —

    frontier = the maximal achievable pairs (aim, δ_A).

Ines's construction, in the model's terms. The agent knows its target F
and sees its circumstances E. It follows F with a fixed probability λ,
and with probability 1−λ draws its action from a *compensating*
distribution r_E — chosen, for each circumstance E, so that the overall
action pattern given E is exactly uniform: every action equally likely
from the observer's seat. Such a compensation exists whenever λ is
small enough; the exact limit is

    λ* = 1 / (n(1−s) + s)

where n is the number of options and 1−s the environment's reliability.
Up to λ\*, δ_A = 1 identically while aim grows with λ. Past λ\*, *this*
compensation is arithmetically impossible — the agent's pull toward F
exceeds what any redistribution can hide. But the plateau does not end
there; a different construction continues it. Let the agent act on F
exactly when the environment is wrong (F ≠ E), and when the environment
is right, scatter: the environment's own answer with probability q,
each other action with the remainder spread evenly. Choosing q so the
action pattern given E is exactly uniform gives q = λ* — the same
constant — and δ_A = 1 exactly with aim

    c₀ = 1 − h_n( s + (1−s)/n ) / log₂ n ,

where h_n(m) is the entropy of a row whose favored entry has probability
m. Read it as a sentence: the hidden agent's aim at the plateau is the
aim of someone who follows the future exactly as often as the world is
wrong. (In the reference world, 0.247 against the first printing's
0.052; equivalently, c₀ at noise s equals one minus the sage's
independence at noise 1−s.) The edge itself lies further out, and
the reason the first searches missed it is now understood: at perfect
unreadability the action pattern is pinned, so the edge is the
*minimum of a concave function over a polytope* — it sits at a vertex,
where smooth optimizers never look. Searching vertices directly finds
strategies at 0.335 in the reference world (0.311 at four options) —
a third of full aim with no readability at all — so c₀ is an exact
lower bound, the vertex search a numerical one, and the exact edge is
open (Chapter 15) — except at three options, where it is closed at
1 − 1/log₂3 ≈ 0.369, and at four, where the best strategy found,
(5 log₂5 + 9 log₂3 − 6)/64 ≈ 0.3105, is certified to lie within 0.0002
of the edge. The edge is not monotone in the number of options: lower
at four than at three, and higher again at five and at six. Past the edge,
readability begins, which is the
posted price of §2.

Note the ceiling formula's role: at full aim, Theorem 1 fixes
δ_A = H(F|E)/log₂|A| < 1. The frontier therefore runs from the plateau's
right edge (aim ≥ c₀, δ_A = 1) down to the sage point (aim = 1,
δ_A = the ceiling), and the exchange rate along the way is the price of
aim in visibility.

## §5. The model, and what it covers

Same world as Chapter 4; strategies unrestricted. What is proven: the
plateau's existence; a closed-form lower bound c₀ on its edge, reached
by an explicit strategy; and the two-sided trade. What is
open: the plateau's exact edge beyond four options, and the
frontier's exact shape from that edge to the sage point. An earlier
printing of this section claimed the best curve then known was within a part in a
thousand of the frontier. That was wrong near perfect unreadability —
by a factor of five — and the correction is kept in §3, with the
reason the first attack missed it: a search by gradient over a smooth
parametrization does not find strategies that live at the corners of
the feasible set; a search over the corners does. Both the gap and the
lesson are handed to the reader in Chapter 15. The frontier was then
re-attacked with the method that found the corpse — fix the visible
pattern of choices, search the strategies consistent with it at their
corners — and every point it returns is an exact strategy, hence a
certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997; 0.28 at δ_A = 1.00. The first
printing's curve lies below every one of these on the hidden side of
the sage point. The figure is redrawn accordingly (`figures/
the_plane_and_frontier_v2.png`), with the plateau's edge marked open. The plateau-widening
sign (c₀ rising with environmental noise) survives the correction and
strengthens — 0.10, 0.25, 0.46 as the world's noise rises through 0.3,
0.5, 0.7 in the reference world; constants, as always, travel only with
their class.

## §6. The code

- `code/frontier_attack.py` — the optimizer that killed the simple-
  strategy conjecture and the compensating construction that replaced
  it. (Its near-optimality claim is the second kept corpse.)
- `code/plateau_edge_T6prime.py` — the construction that widened the
  plateau, its closed form, and the search that found the asymmetric
  strategies beyond it.
- `code/rig/plateau_edge_vertex_search.py` — the edge as concave
  minimization over a polytope; successive linearization from random
  vertices; 0.335 at (6, 0.5), 0.311 at (4, 0.5).
- `code/rig/plateau_edge_bnb.py` — certified ceilings by
  branch-and-bound: the three-option edge closed, the four-option edge
  fenced.
- `code/frontier_polytope_attack.py` — the re-attack of the frontier by
  fixed choice pattern; every output point is an exact strategy.
- `code/figure_plane_and_frontier_v2.py` — the redrawn figure.
- `code/plateau_hit_rate_bound.py` — how often a hidden agent can be
  right, against the captain: more only when noise passes one half.
- `code/delta_A_v1.py` — the two-ruler landscape on which the plateau
  first appeared.
- Formal statements, the refutation record, and proofs:
  `docs/THEOREMS_v1.md`.


# Chapter 7. Cheap Theft

## §1. The idea, in plain words

This is the chapter where the book's title comes due — the price list
itself. So it begins by keeping the
promise of the front matter: *theft*, defined before the word does any
work.

An agent holds a position on the two rulers of Chapter 4, and its
resources — knowledge, time, privacy, the stability of its own hours,
the means to survive a mistake —
determine the best positions available to it: the frontier of
Chapter 6 — computed always at the system's *current* capacity, not at
nature's. (The relevant baseline for a worker at the Harbor Grill is
what the modern world's accumulated stability makes possible *now*,
not what a famine-stalked ancestor endured; a defense of theft that
appeals to the stone age has conceded the modern ledger.) **Theft is displacement by taking: any act by another party that
pushes an agent off its frontier, or pushes the frontier itself
inward, by taking or degrading one of the agent's own resources — so
that no position the agent could reach improves, and at least one
gets worse.** That is the entire definition. It names no villain. It is
the same kind of statement as "the dent is three millimeters deep."
Whether a given displacement was justified, paid for, or consented to
is a question for courts and philosophers. That it happened, and how
large it was — those are now questions for arithmetic.

Two things the definition does not call theft, said now so the word
stays sharp.

The first is a more legible world. A flawless neighbor (Chapter 10) or
a working traffic light (Chapter 5) also moves the frontier — but by
*reshaping* it: the independence ceiling falls while the competence
available to anyone who follows rises. Nothing was taken; something
was given. That is rivalry, priced in Chapter 10.

The second is a job that tells a person what to do. A script that must
be followed leaves no room for a judgment of one's own during the
hours it covers — a surgeon's checklist does exactly that, and robs no
one. So the test is not run on the hours of the job. It is run on the
whole life: the hours sold, and what the wage, the security and the
remaining time make possible outside them. A scripted job that pays
enough to steady the rest of a life widens that life's frontier while
it narrows the working day, and is not theft. A scripted job that also
takes the time, the stability and the margin for error a person would
need to do anything else narrows both, and is. The ledger keeps the
working day and the life in separate columns — the *task plane* and
the *life plane* — and calls theft only what shrinks the life.

The test has a second edge. A job can hand back every hour it promised
and still take what those hours were for. Put a worker on a complaints
line, with a script that forbids the one thing that would end each
call: giving the caller what the caller is owed. The firm keeps what it
did not concede. The cost of not conceding is paid by two people who
are not on its books — the caller, in time, and the worker, who absorbs
the caller's anger for a shift and goes home with the evening whole on
the clock and little left to spend in it. Hochschild named that work
*emotional labor* (1983), and three decades of studies find that
showing on script what one does not feel goes with exhaustion
(Hülsheger and Schewe 2011, ninety-five studies). The ledger books that
evening with the stolen hour, because the time gate of this chapter is
counted in thought, not in clock time. The surgeon's checklist and the
complaints script both leave no room for judgment while they run. They
differ twice: the checklist points the surgeon at what the patient
needs and the script points the worker away from what the caller
needs; and they differ in what is left of the worker when the shift
ends.

Two rules about baselines, because a displacement is always *from*
somewhere. First, every entry on the ledger is measured against a named
feasible alternative — the worker without the job, the same job
arranged differently — and the number changes with the baseline, so the
baseline is printed with the number. Second, identifying a loss is not
attributing it: that a worker's capacity fell under a practice does not
by itself say the practice caused the fall. Attribution needs the
practice compared with its alternative, and Chapter 13 does it three
ways: the same person followed across years, a city that changed its
scheduling law beside cities that did not, and stores assigned to
steadier schedules by lot.

And once theft has a size, it has a price list. This chapter computes
it: for every resource an agent holds, the exact yield of taking some.
The list has a headline, and it is the book's darkest finding:
**the most efficient theft of freedom never makes its victim
predictable — and never registers on the single ruler at all.**

## §2. The story: the manager who steals nothing

The Harbor Grill has a manager who has never taken a thing. Every hour
is paid to the cent. No till has ever come up short on his watch. Ask
an auditor: nothing is missing.

What he takes is the *shape* of his workers' time. The schedule posts
Sunday night for a week that starts Monday. Shifts move on a day's
notice. Slow afternoon? Workers sent home mid-shift, unpaid for the
hours that vanish. Busy evening? A text at four for a shift at six.
No worker can plan a class, a second job, a doctor's visit, a family
dinner, or an hour of quiet thought more than a day ahead — every plan is written in
pencil, and the eraser belongs to the manager. An auditor counting
objects and dollars finds a clean ledger. (The manager will get his
full say — the strongest defense his position affords — in Chapter 13.) What has been taken never
appears on any inventory, because what has been taken is *capacity*:
the ability to point one's hours at anything of one's own.

The mathematics says this theft leaves two kinds of victim, depending
on what a person's mind does when its planning time is taken away.

**Nadia's** mind, overloaded, spins loose. Her days shatter into
fragments; she starts things and abandons them, decides and
un-decides. Watch her and you can predict nothing — on the single
ruler, Nadia scores as remarkably *free*. What's gone is her aim.

**Tomas's** mind, equally overloaded, does the opposite: it hands the
wheel to whatever is directly in front of him. The order screen, the
line at the counter, the next text from the manager — each moment's
demand becomes his next act. He stays orderly, productive, even
competent. On any dashboard he scores *fine*. What's gone is
everything about his day that his situation didn't dictate.

Name the mechanism before the victims, because it is the chapter's
real subject: the schedule's chaos was not created by the manager — it
was *relocated* by him. Demand varies; that variance is a cost, and
someone must absorb it. A business can absorb it on its own books —
idle staff on slow days, overtime premiums on busy ones. Or it can
transfer the variance onto its workers' lives, where it destroys
planning, aim, and δ_A off any book anyone keeps. Call it what it is:
stochasticity transfer — the moving of variance from a party who
would have to account for it onto parties who cannot. (The manager
believes he has answers to all of this — that the transfer was priced
and agreed to — and his defense will be heard at full strength, and
answered, in Chapter 13.) Economics has watched this happen at national scale and given it a name — Hacker's *great risk shift* (2006): three decades of economic risk moving from institutions onto households. Stochasticity transfer is in that spirit and is the more general object — defined on any variance channel, inside a firm as readily as across an economy, and priced here by elasticity rather than described.

And an hour is not an hour. Thinking time has a gate of its own, twin
to Chapter 5's: until a person has had enough of it to out-think what
the situation in front of them already makes obvious, more time buys
nothing; just past that point it buys more than it ever will again;
and from there each added hour buys less. So the hours that matter
most are the first few past the gate — and those are the hours a moved
shift takes from someone with few to spare. In this chapter's model,
an hour taken from the time-poor destroys about seventy times the
agency of an hour taken from the time-rich, in proportion to what each
has, and nearer two hundred times hour for hour. The Grill's schedule
does not take the same thing from everyone it touches.

Two workers, opposite symptoms — one scattered, one on autopilot; you
know both, and may have been both — and neither was robbed, according
to every measure that doesn't use two rulers. That invisibility is not
an accident. It is, this chapter proves, exactly why this theft is the
cheap one.

## §3. The theorems

**Corollary 7.1 (Cheap theft). [EXACT]** *Destroying an agent's aim
while leaving its unpredictability intact is vastly cheaper than making
the agent readable — against agents of Ines's kind (Chapter 6), cheaper
by roughly a thousand to one, whatever the attacker wants.* The single
ruler cannot register the loss even in principle.

**Theorem 10 (The price list). [EXACT]** Computed as elasticities —
percentage of agency lost per percentage of resource taken, a form with
no units and no assumptions about the attacker's costs:
*(i)* against unreadable agents, only aim can be attacked at all;
*(ii)* agents near their education gate (Chapter 5) are the cheapest
to unmake — a small theft of knowledge, or a small *increase in how
predictable their world is*, drops them into the dead zone entirely,
at yields ten times any other entry on the list (on the independence
ruler; Chapter 10 prices what the second move gives back on the other);
*(iii)* a stolen hour is not a stolen hour: taken from someone with
few, its yield is roughly **seventy times** its yield against someone
with many in proportional terms (the elasticities), and nearer two
hundred times per unit of time taken.

**Theorem 16 (The two victims, and the time gate). [EXACT]** *Which
victim the theft produces — Nadia or Tomas — depends only on what an
overloaded mind falls back on: loose scatter, or the demand in front of
it. Both routes destroy agency at full cheap-theft efficiency.* And
thinking time has a gate of its own, twin to Chapter 5's: deliberation
buys zero independence until accumulated thought outweighs what the
situation already makes obvious — and then it activates all at once. The field has already measured the thing this gate formalizes: Mani, Mullainathan, Shafir and Zhao (2013) and Shah, Mullainathan and Shafir (2012) showed scarcity — of money, of time — taxing the deciding mind itself, not merely its options. The time gate is in the spirit of that finding and makes one claim it did not: that the tax arrives as a threshold, zero-then-jump, rather than a slope — which is exactly what the field audit of Chapter 15 can check. Placed inside the standard heterogeneous-agent macro model (Chapter 14 §5C), a threshold of the same kind is what makes a large monetary easing louder in output and quieter in balance sheets than any linear model of it reports — in the host where wages are sticky.

**Proposition 8 (Where an hour is worth most). [EXACT]** *Below the
time gate, extra thinking time buys nothing. Just past the gate, it
buys more than it ever will again. From there, each additional hour
buys less than the one before.* This is why clause (iii) lands where
it does: the most valuable hours anyone owns are the first few past
the gate — which are exactly the hours the time-poor lose first.

## §4. The mathematics

Elasticity, built from plain parts: if taking 1% of a resource costs
the victim 2% on an agency ruler, the elasticity is 2. It is a pure
ratio — no dollars, no assumed prices — so the price list holds for
*any* attacker, whatever their costs, because it ranks yields, not
expenses.

The list's dominant entries, from the computation: for agents on the
plateau, every resource attack (time, knowledge of the world) moves
the independence ruler by elasticity at most 0.009 while moving aim by
1.5 to 2.0 — the thousand-to-one of Corollary 7.1. Near the gate
e* = 1−s of Chapter 5, the independence ruler's elasticity against
education spikes to about 9, and against the world's predictability to
about 4.5. And aim's elasticity against time is 0.565 for a time-poor
agent versus 0.008 for a time-rich one — the seventy of clause (iii).
(Elasticities are proportional sensitivities; the return per *unit* of
time, dQ/dt = ε·Q/t, differs by about 190 between the same two agents,
because the time-poor agent's smaller budget is in the denominator.
"An hour returned" means the per-unit number.)

The time gate, precisely: model thought as consulting your own
knowledge in noisy steps, with the situation's suggestion available for
free. A single weak consultation loses the reliability race of
Chapter 5 and is rationally ignored; independence stays at exactly zero
until accumulated consultations outweigh the situation's reliability,
then jumps. The same inequality as the education gate — e + s > 1 —
with accumulated thought standing in for e. One law, two currencies.
Nothing in the model is clock time: it counts consultations. A person
handed the same hours with fewer consultations left in them has been
moved down the same curve as a person handed fewer hours.

## §5. The model, and what it covers

The price list was computed in the world of Chapters 4–6 by exact
enumeration; elasticities are unit-free but, like every constant in
this book, travel only with their model class — the *seventy* is real
in its world, and Chapter 13 is where the world is audited.

The two victims required a modeling choice this book declines to make:
what does an overloaded mind emit — loose scatter, or the demand in
front of it? Both versions were built and run. Cheap theft holds in
either. But an earlier result had to be narrowed by the comparison, and
the narrowing is printed: the first printing reported that
unreadable agents keep their unreadability when their time is stolen
(only their aim dies). That is true if a rushed mind emits scatter —
scatter is unreadable by nature. If instead a rushed mind does what the
situation suggests, the opposite happens: the unreadable agent, out of
time, becomes an open book. Which world a given person lives in is an
empirical question about minds, not mathematics, so the book keeps
both and labels each claim with the version it needs.

Nothing here requires the Harbor Grill's manager to have read
this book. Ordinary profit-seeking, ordinarily optimized — engagement
tested, schedules tuned, churn tolerated — discovers these high-yield
squares the way water discovers cracks. The list accuses no one of
understanding it. It predicts where extraction, wherever it optimizes,
will be found parked. Predictions can be checked.

## §6. The code

- `code/theft_equilibrium.py` — the elasticity price list, both agent
  types, all operating points.
- `code/iterative_time_T16.py` — the time gate and the Tomas version;
  `code/stealth_gates.py` — the Nadia version.
- `code/delta_A_v1.py` — Proposition 8's shape, visible in the
  deliberation sweep.
- Formal statements, the printed narrowing, and proofs:
  `docs/THEOREMS_v1.md`.


# PART III — WATCHERS: FREEDOM IS RELATIVE TO AN OBSERVER

# Chapter 8. The Watchers

## §1. The idea, in plain words

Every score in this book so far has carried a silent phrase, and this
chapter makes it speak. Unreadable — *to whom?* Independence was
defined as how little your circumstances predict you, but "your
circumstances" are not one thing: they are whatever a particular
watcher can see, and watchers see differently. Stated honestly, freedom
is always freedom *from someone's seat*: the same person, on the same
day, holds a different independence score for every watcher in their
life — and all of the scores are correct.

This is not a loophole in the framework. It is the framework refusing
to let anyone say "free" without saying
*from whose sight*. And taking that refusal seriously produced the
strangest exact result in this book: there is a way of watching that
makes the most unreadable person in the room the most readable one —
without changing anything the person does.

## §2. The story: three seats, and the learned conviction

Theo is one man with three watchers.

His **employer** sees his schedule, his badge swipes, his output. From
that seat, Theo is nearly a timetable: predictable to the minute,
independence close to zero. His **bank** sees his purchases and
payments — a different window, through which Theo is moderately
readable: the rent repeats, the groceries cycle, but Tuesday's detour
is invisible. His **neighbor** sees comings and goings and nothing
else; from her seat Theo is mostly mystery. Three watchers, three
scores, one man, one day — and no one of the three is wrong. Ask
"is Theo free?" and the honest answer is a question back: *from which
seat?*

Now bring back Ines from Chapter 6 — the card player whose private die
keeps her betting pattern identical whatever she holds — and seat a
fourth kind of watcher behind her: one who can see *the die itself*.
Here is the result that reverses the intuition: this watcher does not merely chip
away at her disguise. From this seat, Ines is more readable than a
beginner who never disguised anything — because her strategy was mostly
careful machinery built *around* the die, and once the die is seen, the
machinery is all that's left, and machinery is legible. The discipline
that made her the most unreadable player at the table makes her, under
this one gaze, the most readable. It does not take much: seeing barely
a third of her rolls already leaves her more exposed than the beginner.

And there is a second inhabitant of Ines's territory, whose version of
this story is quieter and worse. Elias plays no dice at all. He acts on
a conviction — a private theory about how things really work, reaching
past anything the table shows — and he acts on it consistently, not
even certain himself that it's true. To every ordinary watcher, Elias
is indistinguishable from noise: his moves track something no visible
circumstance contains. What looks like randomness is a hypothesis the
watcher doesn't hold. But note what this means: Elias has no die to
hide. His entire unreadability *is* the privacy of one idea. The
watcher who learns his theory doesn't reduce him to a beginner — she
reduces him to a wind-up toy, every future move written out in the one
sentence she acquired. For Ines, surveillance had to watch a coin,
roll after roll. For Elias, it only had to learn a conviction, once.

## §3. The theorems

**Theorem 9 (Watchers, and the inversion). [EXACT]** *Independence is
defined relative to a watcher's information: δ_A(𝒪) for a watcher who
sees 𝒪. An agent of Ines's kind is unreadable in full (δ_A = 1) to a
watcher who sees only circumstances — and, to a watcher who also sees
her source of chance, readable below the 0.75 of a fully open,
undisguised expert: at 0.29 for the strategy that follows the target a
fixed fraction of the time and compensates the rest, and at 0.65 for
the strategy that acts on the future where the world is wrong and
scatters where it is right (Chapter 6 §4; same coin model). The
crossover comes at roughly one third visibility of the source of
chance for the first strategy and seven tenths for the second.* Most
of the second strategy's unpredictability is the future itself, not a
coin, and the future is the one thing a watcher who buys the coin
still does not hold: chance spent where the world is wrong is chance
the watcher cannot buy.
Partial
watching costs her linearly — every additional fraction of the die
seen buys the watcher the same additional exposure.

**Corollary (Privacy is load-bearing). [EXACT]** *For unreadable
agents, the price list of Chapter 7 contains exactly one entry that
touches independence at all: visibility of their source of chance —
or, for Elias's kind, of their private hypothesis.* Privacy is not a
comfort of agency. It is the wall it stands on, and the only wall an
attacker needs.

**Theorem 9′ (The sandwich: what a watcher who holds the coin can and
cannot take). [PROVEN]** *For any agent whose action is a function of
the future, her circumstances, and a private coin that does not know
the future, a watcher who sees both circumstances and coin reads her
between two walls:*

    I(A;F | E)  ≤  H(A | E, R)  ≤  H(F | E).

*Upper wall: no agent, once her coin is watched, is ever less readable
than the open sage — Theorem 9's inversion is not a property of Ines's
strategy but of every strategy, with equality only for agents whose
actions are an invertible relabeling of the future. Lower wall: a
watched agent keeps at least the future-information her actions carry
beyond what circumstances already carry.* The proof is three lines —
the top because a function has no more uncertainty than its argument,
the bottom because the coin, knowing nothing of the future, cannot
subtract any of it — and it is the law behind the parenthetical above:
Ines's simplest strategy carries 0.09 of its independence as future
and reads at 0.29; the strategy that spends its chance where the world
is wrong carries 0.43 and reads at 0.65. A watcher who buys the coin
can strip everything *except* the part of you that was tracking the
future. That part is not for sale, because he does not hold the future
either.

## §4. The mathematics

The subscript, made explicit: for a watcher whose seat shows 𝒪,

    δ_A(𝒪) = H(A | 𝒪) / log₂|A| —

remaining doubt about the action, given everything that seat reveals.
Theo's three scores are this one formula at three values of 𝒪. All of
Chapters 4–7 used 𝒪 = circumstances; nothing there changes — it
acquires a label.

The inversion, by construction: Ines's strategy is λ-follow-the-target
plus compensation drawn from her die (Chapter 6, §4). Condition on the
die: the compensation — most of her behavior, since λ ≤ λ* is small —
becomes a fixed, known function; the only doubt left is the small
λ-weighted thread that tracks her target, and that thread is partially
pinned by circumstances too. Result: δ_A({circumstances, die}) = 0.29
in the model, versus 0.75 for the undisguised expert, whose behavior
at least tracks a future the circumstances don't fully reveal.
For partial visibility — the die seen with probability ρ — the score
is exactly the straight line between the two endpoints, hence the
early crossover at ρ ≈ 1/3.

Elias, in the model's terms: his conviction is a knowledge channel —
information about the future carried by neither the circumstances nor
any die. While private, it places him in Ines's corner of the two-ruler
plane (that corner was never about dice; it is about *acting on what
the watcher cannot see*). Disclosed, his behavior is a deterministic
function of known inputs: δ_A collapses not to 0.29 but toward zero.
Conviction buys deeper unreadability than chance, and pays more
completely when the wall falls.

## §5. The model, and what it covers

Computed in the world of Chapters 4–6 by exact enumeration; the
numbers 0.29, 0.75, and the one-third crossover are properties of that
world and travel only with it. What is class-robust: the existence of
the inversion, the linearity of partial watching, and the
single-entry structure of the corollary. The
"watcher" here is a bookkeeper — she conditions on what she sees and
recomputes her odds; she does not yet *learn over time* from Ines's
history. Watchers with memory, and what an agent's habits leak to
them across weeks, are the next chapter's machinery, and they sharpen
this one's moral considerably.

## §6. The code

- `code/theft_equilibrium.py` — the watcher computation: full and
  partial visibility of the source of chance; the inversion numbers
  and the straight line between them.
- `code/frontier_attack.py` — the construction whose machinery the
  inversion exposes.
- Formal statements and proofs: `docs/THEOREMS_v1.md`.


# Chapter 9. Habits and Coins

## §1. The idea, in plain words

Chapter 8's watchers held snapshots. This chapter gives them the thing
real watchers have: **memory.** A watcher with memory turns your past
into evidence against your future — every day you are observed, the
file on you thickens, and yesterday's you testifies about today's.
So the question sharpens from *can you be unreadable?* to the one that
decides lives: *can you stay unreadable, against someone who never
stops learning you?*

The answer has two parts. Part one: staying unreadable requires
genuinely fresh choices, made daily — choices no record contains and
no habit dictates. Count them the simplest way possible: in
**coin flips**. A choice between two options that nothing in your past
determines is one flip. Two flips can pick freely among four options;
three flips, among eight. The question "how spontaneous are you?"
becomes countable: *how many honest flips go into each of your
decisions?*

Part two is the chapter's finding, and it is stranger: **how many
flips you make matters less than what your flips are allowed to
decide.** Two people with identical habits and identical flips per day
can differ totally in what a lifelong file extracts from them. In one
arrangement, the file eventually wins no matter how many flips are
made. In the other, a known and modest number of flips — enough to
cover the day's real options — makes the file, however thick, worth
nothing at all.

## §2. The story: the courier's two wirings

Vera is a courier who carries things worth stealing — cash payrolls,
signed documents, small valuables. Her enemy is not the traffic; it is
anyone who can *predict her route*, because a predictable courier can
be waited for, and a courier who can be waited for gets robbed. Her
adversary is patient and keeps a file: every route she has ever
ridden, every departure time, every turn, for years. Vera has habits,
as everyone does — districts she knows best, hours her body prefers,
corners her hands take without asking. And she has her flips: each
morning, a few honest coin flips' worth of choices that nothing in her
file determines.

**The first wiring: flips decide the small things.** Vera's habits
pick the frame of the day — which district, which window of hours —
and her flips choose only within it: this alley or the next one, ten
minutes early or late. It feels unpredictable, and for the first two
weeks it is. Then the file catches the frame. Habits surface in any
honest record, and once the robber knows the frame, her flips are a
bird loose in a closed room — genuinely free, and only within walls he
has already mapped. He does not need her alley — robbers do not ambush alleys; they wait
at choke points. Knowing her district and her hour, he covers the one
bridge in, and catches her at whatever alley she flips. (If his
success *required* matching her exact alley, her inside-the-frame
flips would protect her about seven days in eight — which is exactly
why what matters is not how many flips you have, but which level of
choice they rule.) Here is the bitter part:
let this Vera flip *more* — twice as many flips, four times as many —
and her safety barely moves. Flips that only decide details inside a
habit-chosen frame are flips the file has already fenced in.

**The second wiring: flips decide the big things.** Same habits, same
number of flips — different jurisdiction. Now the flips choose the
frame itself. Her city has eight districts: three flips each morning
pick the district — any district, every morning, all eight genuinely
possible. Her habits still exist, but they are demoted to a lean: she
still *prefers* the riverside, and the preference now only tilts the
odds a little, the way a slightly bent coin still lands both ways.
The file still learns her lean — the robber truly comes to know that
she favors the riverside. And it buys him almost nothing, because the
flips, not the preference, pick the district. Knowing how her coin is
bent tells him how often she'll ride the riverside *across a year*;
it does not tell him where she'll be *today*, and today is when a
robbery has to happen.

Why "enough flips to cover the day's real options" is the magic
amount: one flip picks freely between 2, two flips among 4, three
among 8. If Vera's real choice each morning is among eight districts,
three honest flips *cover the menu* — every option stays genuinely
live every day, and the file's knowledge of her leanings changes the
long-run frequencies without ever pinning the day. Fewer flips than
the menu needs, and gaps appear that habit fills — and habit is what
the file owns. This is the exact sense of the chapter's constant:
in the model worlds, two to three flips per decision, given
jurisdiction over the big choices, made perfect knowledge of an
agent's habits predict her no better than total ignorance — to the
last decimal.

So the law of the chapter, plainly: **a watcher with memory does not
extract your flips. He extracts your wiring.** If your habits decide
the frame and your flips decide the details, the file wins — always,
eventually, at any number of flips. If your flips decide the frame
and your habits merely bend the coin, a modest number of honest flips
beats the deepest file ever kept.

## §3. The theorems

**Theorem 11 (The floor, and the two wirings). [EXACT floors; watched
decay verified by simulation with exact bookkeeping]**
*(i)* Against a learning watcher, unreadability decays from its
first-day value to a permanent floor — and the decay is fast: most of
what a file will ever extract, it extracts in the first ten to twenty
observations. First looks are the watcher's version of first hours
(Chapter 7): worth the most.
*(ii)* Under the first wiring (flips decide the small things), the floor sits permanently *below* the
exposure of someone who never disguised anything — Chapter 8's
inversion made chronic — at every coin size tested, for the strategy
that follows the target a fixed fraction of the time (the margin on
the wider plateau is Theorem 11′ (iii)). More coin does not
raise a gated floor.
*(iii)* Under the second wiring (flips decide the big things), the floor
rises with the number of flips, and once the flips are enough to name
a habit — three per decision, for this world's eight habits — it
reaches the first-day value
exactly: the file becomes information-theoretically worthless. Perfect
knowledge of Vera's habits predicts her no better than ignorance.
*(iv)* With no coin at all, both wirings are fully extractable.

**Theorem 11′ (The dichotomy, hardened). [EXACT; 3,372 wirings]**
*(i) The one-time-pad point is set by the number of habits. Under the second
wiring, perfect knowledge of the habit becomes worthless exactly when
the fresh key is at least as long as the habit — h ≥ log₂ (number of
habits). Three is log₂ 8, the model world's habit count; a thousand
habits need ten flips. (ii) The two wirings are the ends of one curve.
Index a wiring by its* reach *— how far the fresh bits can travel
across the choice space — and the floor depends on reach alone, is
non-decreasing in it, and is identical across habit-space sizes at
equal reach. A wiring drawn at random lands near the additive end:
gating is something a routine has to* do. *(iii) The gated inversion is
a margin, not a law. On the wider plateau — the strategy that spends
its chance where the world is wrong — a habit-reader has little left to
take, and the gated floor rises toward the open expert's exposure: at
four options in a half-noisy world it stays below by 0.07; in a
six-option world that is mostly right it crosses above, 0.564 against
0.538.* [REFUTED in one world of six; corpse kept.] *(iv) The exception is a coarse-habit effect, and it vanishes.
As the habit space refines, each habit's cell on the quantile axis
shrinks inside a single bin of every choice rule, the action becomes a
function of the future given the habit, and the gated floor converges
to one value for every number of fresh bits — the same value as with
no fresh bits at all — which is at most the open expert's exposure,
H(F|E), by the data-processing inequality, and strictly below it
whenever the policy maps two futures to one action.* [PROVEN; EXACT:
at a thousand habits the gated floor varies by 0.0015 across h in every
world, and no gated floor sits above the sage at 64 habits or more
anywhere in the sweep.] *Fresh bits inside a wide cell can push a
coarse habit's floor over the ceiling; a fine habit's cannot. The
inversion is universal for fine habits, at every h.*

**Theorem 20 (The inversion costs no theory). [EXACT floors; learned
to three decimals in 72 of 72 worlds]** *Any sufficiently flexible
learner — a sequence model of under a million parameters never told
that a habit exists, or a plain frequency table — reaches the exact
seed-known floor within five to ten observations, the same day the
perfect Bayesian does. The inversion of Theorems 9 and 11 is achieved
by every such watcher, on every wiring tested, at habit spaces of eight
and of a thousand. The habit space's size does not protect: a thousand
habits are read faster and further than eight, because finer habits
make each action more determinate. The one watcher who reads above the
floor is the one holding a confident wrong model of the wiring — who
reads worse than ignorance in 52 of 72 worlds.* The "strongest
watcher" of Theorem 11 is the floor's name, not its price.

**Result R6 (The pad is a race). [SIMULATION; existence results]**
*Theorem 11(iv) says that with no coin both wirings are fully
extractable. Let the coin instead be a* generator *— a deterministic
rule with k hidden bits whose outputs look fresh. The second wiring's
protection then lasts exactly as long as the watcher cannot acquire
those k bits within the watched lifetime. For a learner of under a
million parameters watching 512 days: an 8-bit generator is a habit —
the "worthless" file reads Vera at 0.34, below the gated floor, within
a week; a 12-bit one is a habit within a season; a 16-bit one is
half-read; a 32-bit one is still a coin. The watcher who* assumes *the
coin is fresh never moves: that is the price of assuming freshness,
and it is the whole gap. In the gated wiring, cracking the coin buys
almost nothing — the coin was never doing the work there.* One
training run per world, and the generators are the weakest kind; what
is established is that a watcher of this size *can* do it. A coin is a
word about the watcher.

## §4. The mathematics

Freshness, measured: h = honest flips per decision. The habits, measured: a
persistent pattern the watcher can learn — in the model, a fixed
personal offset drawn once and leaking slowly through behavior.

The two wirings, precisely. Gated: the flips select only within the
habit's cell — the learned offset chooses the region of the choice
space, and the flips pick details inside it. Wide: the flips select
over the whole choice space, and the offset only bends the odds among
outcomes. The watcher
runs honest bookkeeping — updating beliefs about the offset from every
observed action, by the standard rules of evidence — and his remaining
doubt about the next action is Vera's score, day by day.

Wiring two's endpoint has an ancestor cryptographers met in 1949 —
the one-time pad, the unbreakable code whose key is as fresh as the
message. The identity is the same: when the fresh key
is as large as the choice itself and ranges over all of it, knowing
the offset shifts *which* unpredictable thing happens but not *how
unpredictable* it is — Shannon's perfect-secrecy condition, restated
for behavior. The gated wiring can never satisfy it, because its key
is confined to a cell the watcher learns. The wiring dichotomy itself has an older ancestor in the same field: Kerckhoffs's principle (1883), that a cipher must survive the enemy knowing everything but the key. Wiring one keeps its secret in the habit structure, which a watcher learns; wiring two keeps it in the fresh bits, which a watcher cannot. The book's version is in that spirit and is tested rather than assumed — against a watcher who also sees outcomes.

## §5. The model, and what it covers

The floors — the permanent values — are exact enumeration. The decay
curves toward them average many simulated watched lifetimes, each with
exact belief-updates inside; with Theorem 20's learned watchers and
Result R6 they are this chapter's simulation-assisted results, and are
labeled accordingly. The specific
constants (the one-third, the "three fresh choices") are properties of
the model world and travel only with it — the three is log₂ 8, as
Theorem 11′ says. The dichotomy held its shape across every world size
and channel tested on the strategy this chapter was written for. On
the wider plateau found afterward it held at four options in a
half-noisy world (gated floors rising to 0.62–0.70 but staying below
the open expert; additive equality at three bits) and failed by 0.026
in a six-option world that is mostly right — the margin, and the
corpse, are printed in Theorem 11′(iii). The floors move with the
lower wall of Theorem 9′; where the wall is most of the ceiling, the
inversion has nowhere left to stand.

The watcher of
Theorem 11 is the strongest possible one — he knows the true structure
of Vera's behavior and updates perfectly. Theorem 20 ran the weak ones,
and they are not weaker at the floor: a sequence model told nothing,
and a frequency count, both arrive where he does, within days. What
had looked like a flattering idealization turned out to be the floor's
name. The only thing that protects a habit from a watcher is the
watcher's wrong theory of it, held firmly.

And one paragraph at the edge of the model, fenced. Where does the
coin come from? Inside the mathematics, h is simply given. Outside it,
your coin is your intake of the not-yet-filed: new experience, other
minds, imagination — the universe handing you inputs no watcher has
seen *yet*. A hypothesis-agent like Elias (Chapter 8) whose convictions
are updated by experiment has a coin exactly as large as his
experiments are fresh; a person whose inputs all arrive through
channels the watcher also reads has, whatever their inner life, a coin
of nearly zero. Whether any inside watcher could in principle capture
the whole stream — there being no seats outside the universe — is a
question this book flags, fences, and leaves standing. [SPECULATIVE]
Result R6 puts one number under that paragraph: a coin whose source a
watcher can learn is a habit one level up, and the file reopens.

## §6. The code

- `code/rig/watcher_tournament.py` — Theorem 20 and Result R6: the
  watcher zoo on every wiring, habit space and coin generator; results
  and lifetime curves in `code/rig/results/`.
- `code/rig/wiring_hardening_exact.py` — Theorem 11′: 3,372 exact
  floors across the span family and random wirings.
- `code/arms_race.py` — the learning watcher, both wirings, the decay
  and the floors.
- `code/dichotomy_scaling_and_audits.py` — the wirings across world
  sizes and randomized channels.
- `figures/stealth_floor.png` — the two floors against coin size; the
  wide wiring meeting the first-day line at three bits.
- Formal statements and proofs: `docs/THEOREMS_v1.md`.


# PART IV — TOWNS: FREEDOM IS SOCIAL

# Chapter 10. Neighbors

## §1. The idea, in plain words

No one lives on the harbor alone. The moment a second person appears,
something changes that no chapter so far has priced: *the neighbor's
actions become part of your circumstances.* You watch them — you
cannot help it; they are information, standing right there. And this
book keeps finding that information is never free to be near.

Two findings, and they cut in opposite directions. First: in a shared
world, your capacity for independence is not entirely yours. Every
person near you whose behavior visibly tracks the future you share
*consumes* some of your ceiling — because whatever their actions
reveal about the common future is something your circumstances now
tell any watcher about you. Freedom capacity, in a shared world, is a
commons. Second, and against the natural guess: ordinary, imperfect neighbors make your education gate
*easier* to cross, not harder — while one particular kind of neighbor,
the flawless and fully visible expert, does not raise your gate but
welds it shut entirely.

## §2. The story: three fields over

Your farm shares one future with the valley — same weather, same
river, same market. Consider three possible neighbors on the next
field, and what each one's presence does to *you*.

**Priya** farms the ordinary way: she reads the sky and the soil like
everyone, right more often than not, wrong in her own fashion. Living
beside her costs you something real: her plantings visibly track the
valley's shared future, so anyone watching your circumstances — which
now include Priya — learns more about what's coming for you both, and
your ceiling of independence drops by about a fifth. But here is the
turn the natural guess gets backwards: Priya makes your gate *easier*. Because she is
imperfect, she and the sky sometimes disagree — and every disagreement
is a crack of genuine ambiguity where even a little knowledge of your
own becomes the deciding vote. Beside an imperfect neighbor, modest
education starts paying almost immediately.

**Joss** is a Vera of farming — deliberately hard to read, his choices
tracking convictions and flips no file contains. He is expensive
company for any watcher and cheap company for you: his behavior leaks
little about the shared future, so your ceiling barely drops, and his
occasional divergences still crack open ambiguity that lowers your
gate. The unreadable neighbor consumes almost none of the commons.

Then there is **Aldo**, whom the valley takes for a sage. Start with
the Aldo of his reputation — never wrong, never hidden — because that
Aldo's arithmetic is exact, and it is the ceiling on what any real one
can do to you. Beside a flawless visible expert your ceiling of
independence is not lowered — it is *zero*: everything about the
valley's future is readable off his field, so everything you
rationally do is readable too. And your gate is not raised — it is
*welded*: no education, at any strength, can make your own knowledge
the deciding vote, because there is never a genuine ambiguity for it
to decide. Departing from a visible right answer is not independence;
it is error. Beside him, everyone becomes the ferry captain.

Now the Aldo who actually farms the next field. He is right about the
frost dates, about when the river is too high for the low field, about
the price of seed in spring — and so is everyone else; these are the
things the valley already knows. Where the year is strange — a late
blight, a market nobody has seen — he calls it with the same
confidence, and there he is right less often than you are. But a
strange year is hard to score: the harvest comes months later, tangled
with weather and luck, and nobody keeps the tally by kind of year. The
valley keeps one tally for Aldo, and it is a fine one, because most
years are ordinary and in ordinary years he is never wrong. So the
valley follows him in the strange years too. Chapter 11 runs this
valley as a town and counts what it costs: a record earned where the
answer was easy is spent where it is hard, and it lasts exactly as
long as nobody keeps the second tally.

Sit with the strangeness before the next chapter resolves it. This is
not a claim that experts are bad — the next town over will *starve*
for lack of them. It is a conservation statement with an uncomfortable
middle: every clearly right, clearly broadcast answer near you makes
your own independence both less possible and less *necessary* — and
"less necessary" is doing quiet, dangerous work in that sentence.
Whether a valley can live on answers alone, every gate welded and one
flawless field wearing the crown, is not a question about two
neighbors. It is a question about a fleet, and it has a number, and
the number is in Chapter 11.

## §3. The theorems

**Theorem 12 (The commons, and the welded gate). [EXACT]** *Your
independence ceiling falls with the legible competence of your
neighbors: from 0.77 alone, to 0.71 beside an unreadable neighbor, to
0.61 beside an ordinary one, to exactly 0 beside a flawless visible
expert. Your education gate moves the other way: 0.50 alone, 0.18
beside the unreadable, 0.01 beside the ordinary — and beside the
flawless expert, no education at any strength opens it.* Partial
legibility near you opens doors; perfect legibility welds them.
(The natural prediction — that legible neighbors raise the gate — runs
the other way; the refutation is kept.)

**Proposition 15 (Diminishing bites). [EXACT]** *Each additional
ordinary neighbor consumes less of your ceiling than the last: the
first costs 0.17, the second 0.13, the third 0.10, the fourth 0.08.*
Watchable neighbors overlap in what they reveal — so the first one
near you matters most, the social twin of "first looks are worth the
most" from Chapter 9.

## §4. The mathematics

Your circumstances, enlarged: with a neighbor whose action is visible,
the watcher's seat becomes 𝒪 = (your signals, their action), and both
your ceiling and your gate are recomputed against that richer seat
using the same formulas as Chapters 4–5.

The welded gate, in one paragraph: your rational action follows
whichever source wins the reliability race (Chapter 5). Beside Aldo,
the enlarged circumstances contain a *perfectly* reliable entry — his
action, which equals the future. A perfect entry cannot lose the race
to any education of fidelity less than perfect, in any situation, ever;
there are no disagreements left for your knowledge to referee. Hence
independence exactly zero and a gate no finite learning opens. Beside
Priya, her imperfection guarantees situations where the enlarged
circumstances *disagree internally* — and in exactly those situations,
the race is close and your own knowledge can win it at low fidelity.
That is why her presence lowers your gate to nearly nothing while
still costing you ceiling: the two effects are not opposites but two
faces of what her behavior reveals.

Diminishing bites, precisely: neighbors watching the same sky reveal
overlapping information about it; the second neighbor can only add
what the first did not already reveal. Shared-source information is
like light in a room — the second window brightens less than the
first.

## §5. The model, and what it covers

Computed by exact enumeration in the shared-future world: one common
future, each party with its own signal of it, the neighbor acting
first and visibly. The constants travel only with this class. Two
audits printed: the gate results were re-derived under a deliberately
stricter definition of "the gate opens" and did not move (the jump at
the threshold is discontinuous, so definitions cannot disagree); and
the natural prediction that legible neighbors would *raise* the gate
was refuted by the computation and is kept in the record — the
ambiguity-crack mechanism was found in the wreckage. What this
chapter leaves to the next: neighbors who react to *you*, crowding,
and learning across seasons — the towns of Chapter 11 have all three.

## §6. The code

- `code/neighbors_T12_P15.py` — the four neighbor types, the ceiling
  and gate numbers, and the erosion sequence.
- `code/dichotomy_scaling_and_audits.py` — the stricter-gate audit.
- Formal statements, the kept refutation, and proofs:
  `docs/THEOREMS_v1.md`.


# Chapter 11. The Fishing Town

## §1. The idea, in plain words

Chapter 10 left a question standing: can a community live on visible
right answers alone — every gate welded, one flawless expert wearing
the crown? The question needs communities that can *fail*, and a
way to count how often. So this chapter builds a town, feeds it or
starves it by exact arithmetic thousands of ways, and reads off what
made the difference.

The findings, in advance. What keeps a town alive is not how many
decision-makers it has, and not how skilled its best decision-maker
is. It is **how many genuinely different ways of being wrong it
contains.** Independence multiplies safety — literally, exponentially.
Sameness puts a floor under danger that no amount of skill or size can
break. And the strangest line-item on the town's books: its least
competent member, kept fed, is sometimes the only insurance policy
that pays.

## §2. The story: nine boats

Here is the town. Nine fishers. Every morning the fish are somewhere —
one of four grounds — and nobody knows which for certain. Each fisher
reads the water; each may also have education, years of learning how
fish actually move. If most boats find the fish, the town feasts.
Three missed days in a row is a famine. The town was run every way it
can be arranged. Five lessons came back. (Axiom 2 is what fails in this town, day
after day; independence is what contains the failure.)

**Lesson one. Nine okay heads beat one excellent head.** Give each
fisher modest skill: right 70% of days, judging alone. Now hire a
harbor master who is right 80% of days, and have everyone follow him.
The independent town finds the fish 90 days in 100; the harbor
master's town, 80 — and the independent town's famine risk is *six
times lower*. When independent fishers err, they err in different
directions and the majority still lands on the fish; when the master
errs, the whole fleet sails to one empty sea. There is power in the
people, and it is not a slogan: every two independent fishers added
cuts famine risk roughly in half, doubling and doubling again.

**Lesson two. Nine heads with one teacher are one head.** Now the
nastier town: nine fishers, all educated — by the same tutor. Each
still right 70% of days. But when the tutor's method fails, it fails
in all nine heads at once. This town's famine risk came out *exactly*
equal to a town with a single fisher. Not close. Equal. Nine boats,
nine engines, nine lifetimes of skill — one way of being wrong, and
therefore one head.

**Lesson three. Listen to the master — a little.** So should nobody
follow the harbor master? Every mixture was tried, and the safest town
of all has exactly *one* boat following him: it imports his higher
skill without creating a herd. Each additional follower makes the
town less safe, and at five of nine — the moment the followers become
a majority — the master decides every day, and nothing added after
matters. Centralized wisdom is medicine at a low dose and poison at a
herd dose. (The dose is this town's: a master far better than the room
earns a larger one, and a master who misleads earns none — §5.)

**Lesson four. Shared blind spots put a floor under your risk.**
Real tutors overlap; real weather fools whole fleets. Let the
fishers' training share a flaw — some days, everyone's education
points at the same mirage. Lesson one's exponential protection
survives, but only down to a floor: below it, adding fishers does
nothing, because the remaining risk is the risk they *share*. And the
floor punishes size. A town of nine barely feels a small shared flaw;
a town of thirty-one pays sixteen times over for the same flaw. Big
communities are not protected by being big — past modest size, their
safety is set almost entirely by what everyone has in common. To make
a big town safer, do not add heads. Subtract sameness.

**Lesson five. The wildcard.** One fisher ignores everything — the
master, the tutors, sometimes the birds themselves. He follows
hunches. He is right far less often, and on ordinary days he is a
small tax on the town's catch. But on mirage days — when every
trained head sails to the same empty sea — the wildcard is somewhere
else. In the shared-tutor town, each wildcard cuts the risk of
*total* failure about six-fold. He will never make the town rich:
wildcards insure subsistence, not prosperity. The town that keeps a
few eats less and starves never. And one warning the arithmetic
insists on: in a town whose fishers already err each in their own
way, the wildcard helps nothing and costs fish. He is insurance —
and insurance is only worth buying against a risk you actually share.

**Two more arrangements, run later, and exact.** *The sage's tally.*
Let three days in ten be hard — fog, a strange current — and let one
voice in the harbor be right on every plain day and on only half the
hard ones, where a single fisher manages 55 in a hundred. Keep one
tally per voice and his is the best record in town, 85 against 79, so
every boat follows him — and the famine rate doubles. Everything he
was right about, the town already knew; every day on which following
him made a difference was a hard one. Keep two tallies, plain days and
hard days, and he is followed where he is right and nowhere else. And
where the fog cannot be seen from the shore, no fisher can be talked
out of him: behind the sage each boat is right 85 mornings in a
hundred, reading for itself 79, and what is better for each boat is
worse for the town. Only where the boats that find the fish must share
them does the herd stop itself — at two boats of the nine.
*The boat that stays in.* Let sailing cost something, and let a
fisher's reading be clear some mornings and murky others. A fisher
with a murky reading and a costly trip stays ashore, and he is right
to. With four boats in ten staying in, the town starves 98 seasons in
a hundred where it starved 7: the doubtful boats had been landing four
boatloads in ten, and the town was living on them. Nor does his own
hunger bring him out. His one boatload turns a bad day into a good one
about one morning in four in a town of nine boats, and eight in a
hundred in a town of ninety-nine: the larger the town, the less it is
any one fisher's to save.

> **Lesson six. The town that watched itself. [SIMULATION — this
> lesson only.]** Every number in lessons one through five was exact
> arithmetic. This lesson's town *learns*, which is too tangled for
> exact enumeration, so its results come from many simulated
> town-lifetimes with honest bookkeeping inside each: strong evidence,
> not proof, and boxed so you always know which is which.
>
> The natural prediction, before any of this was built, was that a
> living town would fix itself: let fishers watch each other's
> results, and a master-following fleet converts into the distributed
> fleet that survives. The living town was built twice, in two worlds
> that differ by one fact: whether crowding costs anything. The first
> is the **glass sea**, named for what it lacks — friction. Nothing a
> boat does on it leaves a mark on any other boat's catch: fish are
> infinite, so every boat on the right ground catches its fill no
> matter how many boats are already there. There, honest
> ledgers *harden* the herd: each fisher correctly learns the master
> (80%) beats his own reading (70%), and the sharper the fishers
> reason, the more completely they herd — above ninety percent at the
> coldest reasoning. Watching results cannot save the glass-sea town,
> because results teach each fisher that the herd is smart; they
> cannot teach him that the herd is fragile. The second world is the
> **real sea** — real because every ground that has ever been fished
> works this way: fish are finite, and boats on the same ground split
> the catch. There the herd dissolves. Not from wisdom; from hunger: nine boats split one
> ground's catch nine ways, while the stubborn fisher who trusted her
> own reading and was right eats alone. Hub-following falls to about
> half and *stays there even among the coldest reasoners* — it is the
> balance point of a real game, not noise — while the town's accuracy
> rises and its famine risk is cut in half.
>
> The prediction, scored: as literally stated (results alone convert
> the fleet), refuted by the glass sea; with one condition added — that
> fishing a crowded ground costs something — confirmed. The missing
> mechanism is the one any fisher would name first: *wouldn't they
> realize they are overfishing one spot, and move?* The mechanism in
> one line: the glass sea is a chorus, where everyone can sing the
> same note and no note is worth less; the real sea is a potluck,
> where a dish everyone brings feeds no one. Herding survives wherever
> joining the crowd costs nothing. And one thought, flagged as
> interpretation only: ask which of your own economies are glass seas
> — a fishery punishes crowding automatically; an information feed
> does not.

Six lessons, one town, two axioms. Nothing about human nature was
assumed; nothing about politics. Yet the reader has noticed the town
has opinions — about newsrooms and central banks, about school systems
teaching one method to a nation, about the strange usefulness of
stubborn people. The town is not shy. How far its opinions travel is
the next, carefully fenced chapter.

## §3. The theorems

**Theorem 13 (Survival structure). [EXACT]** *(i)* Famine probability
falls exponentially in the number of independent educated fishers
(roughly halving per two added). Nine independent 70%-fishers beat one
80% authority six-fold on famine and outright on daily success.
*(ii)* Fishers sharing one competence source have the famine risk of a
single fisher, exactly, at any headcount. *(iii)* Safety against
hub-following is a dose curve whose optimum moves with the expert's
margin: one follower when he is 80–85% against 70% readers, two at
90%, a bloc at 99%; at the printed accuracies, a benefit at one,
worsening after, saturating exactly at bloc majority. *(iv)* Wildcards cut
total-failure risk multiplicatively where blind spots are shared, and
strictly hurt where they are not.

**S1 (The living town). [SIMULATION]** *Observation alone locks the
herd (rational result-watching converges to hub-following); finite
resources convert it (interior mix, higher accuracy, famine halved).*
Lesson six, boxed above; scripts in §6.

**S2 (The town under stress). [SIMULATION]** *Across 972 towns —
master accuracy, misdirection, slumps, readers' bad weeks, shared
blindness, a sea with memory — the best dose of following stays below
the herd line in 240 of the 243 towns whose readers share no blindness
and whose master is right at most nine days in ten, and moves to the
bloc where the readers share a blindness or the master is nearly never
wrong.* The all-readers town is safe only while its
errors are independent across readers and across days; that
independence is the theorem's premise and the thing to be protected.

**S3 (The town that stops reading). [SIMULATION]** *Where reading is a
skill that fades with disuse and returns with use, the town has one
long-run state, reached from a town of readers and from a broadcast
town alike: the slacker the crowding and the faster the fading, the
nearer that state is to everyone following and no one able to read.*
No point of no return; a slope with one bottom.

**Theorem 14 (The correlation floor). [EXACT]** *With a shared flaw
striking all trained heads together some fraction of days, the
exponential of 13(i) survives only down to a floor set by that
fraction — and the same small flaw that costs a town of nine a factor
of 1.3 costs a town of thirty-one a factor of 16.* Correlation taxes
scale specifically; past modest size, decorrelation is worth more
than growth.

**Theorem 21 (The public-signal window). [EXACT]** *Give every fisher,
beside a private reading right with probability p, one signal all can
see, right with probability a. A fisher who reasons correctly follows
the public signal against a disagreeing reading exactly when a > p —
and then the whole fleet sails on one signal. Whenever a lies above
each reader's accuracy and below the accuracy of the readers' majority,
every boat is right more often than before and the town goes hungry
more often than before.* In the printed town the window runs from 0.70
to 0.901, and famine jumps from 7 seasons in a hundred to 83 at its
lower edge. No master, no lie and no shared flaw is assumed: the
sameness is manufactured by each fisher's correct use of what everyone
can see.

**Theorem 22 (The borrowed record). [EXACT]** *Let some days be plain
and some hard. Let one voice be right on every plain day — when the
readers' majority is right too — and right less often than a single
reader on a hard one. A fisher who keeps one tally per voice finds
that voice's record better than his own whenever plain days are common
enough, and follows it; the town then fails on its hard days at the
voice's rate where it had failed at its majority's.* In the printed
town — three days in ten hard; a reader right nine plain days in ten
and 55 hard days in a hundred; the voice right on half the hard days —
his record is 85 against a reader's 79.5, every boat follows him, and
famine doubles, from 11 seasons in a hundred to 22.5. On plain days
the town's majority was right 999 times in a thousand: he was credited
for telling it what it knew. Two tallies — one for plain days, one for
hard — put him back where he is right and the town back at 11. And his
standing lasts in exact inverse proportion to the share of hard days
whose outcome anyone records against him: a reputation for never
being wrong ends at the first recorded miss — a week away when every
hard day is scored, seven seasons away when one in a hundred is.
Attacked after it was stated (`code/attack_T22_T23.py`), the theorem
came back sharper on one side and bounded on the other. It needs no
mistaken fisher: one who knows every number here and cannot tell a
hard morning from a plain one is right more often behind the voice
than reading — 85 against 79.5 — so following is each boat's best move
and the town's worst. And it is a theorem of the free answer. Where
the boats that find the fish must share them, joining the voice stops
paying once two boats are behind him — a third would land 0.109 of the
catch where a reader lands 0.111 — and famine stops at 14 seasons in a
hundred. The borrowed record rules where agreeing costs the agreer
nothing.

**Theorem 23 (The boat that stays in). [EXACT]** *Let a fisher's
reading be clear on some mornings and murky on others, and let sailing
cost something. He sails when the reading is worth the trip. Once a
trip costs more than a murky reading is worth, the murky boats stay in
— each for a sound private reason — and the town loses the boatloads
they were landing.* In the printed town a 70 percent reader is right
nine clear mornings in ten and four murky ones; with four boats in ten
ashore on any morning, famine goes from 7 seasons in a hundred to 98.
Covering the gap between what a doubtful trip costs and what it is
worth brings them back out — for under three percent of the catch when
the gap is a twentieth of a boatload. It is Theorem 5b in a boat: a
mistake budget is what keeps the doubtful boats on the water. A fisher
who counts his own hunger stays in all the same
(`code/attack_T22_T23.py`). Let a bad day cost him a boatload of his
own. His trip is then worth his catch plus his chance of saving the
day — 27 in a hundred in the printed town — and the murky boats stay
in above a trip cost of 0.51 where they had stayed in above 0.40; at
three boatloads of hunger, above 0.72. In a town of ninety-nine boats
that chance is 8 in a hundred and the line moves from 0.40 to 0.43.
His own hunger moves the line and does not remove it, and it moves it
less the larger the town.


These theorems have ancestors outside physics, and they should be named. Lesson one is Condorcet's jury theorem (1785) on independent fishers. Lesson two's collapse and Theorem 14's floor are in the spirit of what Ladha (1992), Boland (1989) and Berg (1993) proved for correlated jurors — and what ensemble learning proved again for correlated classifiers (Tumer and Ghosh 1996): a shared flaw sets a floor that no headcount breaks. The wildcard insurance of 13(iv) is ecology's insurance hypothesis (Yachi and Loreau 1999) — diversity as a buffer against a fluctuating world — and the collapse of a one-tutor town is the loss of what ecologists call response diversity (Elmqvist and colleagues 2003). What this chapter adds is the arrangement: the famine metric as survival over streaks, the shared-tutor identity N_eff = 1 exactly, and the dose curve of 13(iii) — which the jury literature, studying correlation rather than shared sources, does not contain. Theorem 21's upper edge is Condorcet's own number, the accuracy of the majority, and its mechanism stands near two modern results without being either: information cascades (Banerjee 1992; Bikhchandani, Hirshleifer and Welch 1992), where agents herd by watching one another's actions in turn, and the social value of public information (Morris and Shin 2002), where a public signal can lower welfare among agents who want to match one another. In the window nobody watches anybody and nobody wants to match: each fisher would follow the signal alone on the sea. Theorem 22 has an ancestor in the record of expert forecasting: Tetlock (2005) scored some twenty-seven thousand forecasts from 284 experts and found them barely better than guessing, no better than well-read amateurs, and worse than simple extrapolation rules. A doctorate, years of experience and access to classified information made virtually no difference. One thing predicted consistently, and it predicted the wrong way: the better known the forecaster, the further the stated odds sat from what happened. The theorem is in that spirit and adds the mechanism — one tally where two are needed — and the rate at which the standing decays once the second is kept. Theorem 23 is in the spirit of Olson's logic of collective action (1965) and of the threshold public-goods games of Palfrey and Rosenthal (1984), where each contributor weighs the chance that his own contribution decides the outcome — with this difference: what goes unsupplied here is not effort but doubtful judgment, and the boats that stay in are the careful ones.

## §4. The mathematics

Lesson one's engine is old and honorable: majorities of independent
voters. If each of nine fishers is right with probability 0.7,
*independently*, the chance that five or more are right is the sum of
the favorable cases — 0.901 — and the chance the majority fails on
any given day is 0.099. A famine needs three failures *in a row*; the
book computes that by simple bookkeeping over runs of days (a small
table tracking "how long is the current losing streak" — nothing
fancier), giving 0.074 per ninety-day season. The all-follow-the-
master town fails on exactly the days the master fails — 0.2 — and
its famine probability, 0.44, does not improve by one decimal if the
town grows, because it contains one way of being wrong.

The shared-tutor identity is bookkeeping of the same kind: nine
fishers with one tutor succeed and fail as one body, so every formula
reduces to the single-fisher case — headcount cancels out of its own
arithmetic. And the correlation floor: if a shared mirage strikes a
fraction ρ of days, the town's daily failure is at least ρ times the
mirage's failure rate no matter how large the majority — a floor that
size cannot touch, only sameness can lower.

The window is two lines of the same bookkeeping. A fisher whose
reading names one ground while the public signal names another weighs
a(1 − p) against (1 − a)p, and follows the signal exactly when a > p.
Once every fisher does, the town fails on the days the signal fails,
1 − a, where the reading town failed on the days its majority failed,
0.099. In the printed town the public signal is yesterday's ground, on
a sea that stays put from one day to the next with probability ρ, so
a = ρ + (1 − ρ)/4. Below ρ = 0.6 nobody consults yesterday and the
town is the reading town. From 0.6 to 0.868 everybody does, and famine
runs from 83 percent down to the reading town's 7.4. Only past 0.868 —
a sea steadier than the readers' majority is accurate — is yesterday
the better guide for the town as well as for the boat. The simulated
town (`code/rig/town_stress2.py`) lands on the exact figures: 55
percent at ρ = 0.7, 3 percent at 0.9. The window belongs to fishers
paid for being right whatever the company — the glass sea of lesson
six. Where a crowded ground pays less, §5's arithmetic applies with
the public signal in the master's place: with eight boats on
yesterday's ground at ρ = 0.7, reading pays 0.218 V against
following's 0.086 V, and the fleet cannot all sit on yesterday.

## §5. The model, and what it covers

The town is deliberately spare: days independent of each other, fish
placed fresh each morning, fishers deciding once per day, all famine
probabilities exact. Constants — the six-fold, the sixteen, the
"three flips" of the wider book — are properties of this town and
travel only with it; the *shapes* (the exponential, the identity, the
dose curve, the floor) held everywhere the town was varied.

The fishers of lessons one through five never learn, never crowd, and
never stay ashore. Each of those was then let in. Lesson six lets them
learn and crowd. S2 lets their errors persist, their masters mislead
and their sea remember. Theorem 21 lets them consult it. Theorem 22
gives them a sage they do not score where it matters. Theorem 23 lets
them stay ashore.

Theorem 13 is a
theorem about *readings*, not about who gives the orders. Nine
independent readings protect the town whoever dispatches the boats. A
harbor master who polls nine fishers and sends the fleet on their
majority inherits the same 0.074 in this model; a master who hedges
his own single signal gains nothing on the famine metric, because one
80% reading cannot put five boats on two grounds. Independence beats
the master only above a right-ground accuracy of about 0.63 (education
near one half in this town); below it, independent voting amplifies
error, and Chapter 14's first rule — past the gate — comes before all
the others. Whether readings stay
independent in a population that never acts on them is answered by the
living town, where that arrangement failed — fishers who could see the hub
stopped reading for themselves — and the link from acting to reading,
once a conjecture, is now a model with a result (S3 above, and
Chapter 15): give reading a skill that fades with disuse faster than
practice restores it, and a town with any slack in its crowding slides
to nine boats in ten behind the hub with its readers at chance, from
wherever it starts. And a fleet dispatched from the
center is, from the environment's seat, one free agent and, from the
dispatcher's seat, nine rocks: the most surveilled configuration this
book prices (Theorems 9 and 12).

The
town's survival is a *majority* game — enough boats on the right ground
— and Condorcet's logic is a majority-game logic. Much production is
not: a surgery, a flight, a chip succeeds only if every step does
(Kremer's O-ring, 1993), and there independent *execution* errors
multiply into near-certain failure — which is why such work is
standardized and scripted, correctly. The book's independence belongs
to the *readings* in such a task — the independent check, the second
pair of eyes, the inspector who does not share the team's blind spot —
not to the hands. Theorem 13 says nothing about conjunctive execution,
and the physics theorems of Chapter 2 are not production functions and
must not be borrowed as such in either direction.

The payoffs, exactly. The living town
de-herds because fishing a crowded ground pays less — but the right
inequality is not the naive one. When the reader and the master are
both right they share the ground, and the reader's choice changes the
town's total catch. With eight boats on the master and one deciding:
reading pays 0.70·(0.80·V/9 + 0.20·V) against following's 0.80·V/9 —
0.202 V against 0.089 V in the printed town — and because the reader
adds to the town's catch whenever the master is wrong, pooling any
share of the catch, up to all of it, leaves reading ahead (0.104 V
against 0.089 V at full pooling). What reverses the ranking is not
pooling but the master's margin: against a 99% master, following pays
at every pooling fraction. No winner-take-all is needed, only a
crowding penalty and a master who is merely better, not vastly so.
Which is also the correction to lesson three: one follower is the
optimum when the master is 80–85% against 70% readers; by 90% two
followers are safer, by 99% a bloc is — exactly computed, and the dose
is set by the expert's margin and by how his errors correlate, which
independent days cannot show — and which was therefore computed, town
by town (`code/rig/town_stress_T13.py`; the clean town reproduces the
exact numbers). A master who misdirects on one in ten of the days he
knows is still worth one boat, barely; at three in ten he is worth
none, at any accuracy up to ninety-nine percent: the margin that sets
the dose is the margin net of the lie. A master whose errors come in
slumps is worth no boat at eighty percent and one at ninety, and a
bloc behind him starves in as many as nineteen seasons of twenty. Readers whose
errors persist — bad weeks — lift the all-readers famine from seven
percent past fifty. If the master is spared the bad weeks his readers
have, the best dose rises to three boats — still under the herd line —
and even the bloc beats the town with no followers. Give the master
the same persistence and the book's ordering returns: all readers at
fifty-two percent, one follower best, the bloc at ninety-five. And
readers who share a blindness on three days in
ten are not nine readers: nothing under the herd line survives, and a
bloc behind a master whose errors are his own is the best arrangement
left — Theorem 14 seen from the other side. A sea that remembers
yesterday changed nothing, for fishers who do not consult yesterday;
fishers who do are Theorem 21, and inside its window no arrangement of
readers helps — only a following behind an honest master more accurate
than the sea. A master who fishes for himself, and misdirects once his
following is large enough to crowd his own catch, is worth exactly the
following that stays under that size: famine is certain above it and
unchanged below it, so the insurance a town can buy from him is capped
where misdirection begins to pay. The cap binds where it is needed.
Readers with bad weeks want three boats or more behind an honest
master; a master whose temptation begins at three leaves them two, and
famine at 28, 18 and 11 percent where his honest twin leaves 25, 6 and
none (`code/rig/town_stress2.py`). What the stress leaves standing is the
structure, not the headline: protection comes from errors that are
independent, and the channel worth following is whichever one's
errors are uncorrelated with the rest — sometimes the center's. "Keep
a few wildcards fed" — a transfer
to a few — and "fund mistake budgets" — lowering the price of one's
own wrong bet — touch neither the crowding penalty nor the margin.

The same paragraph in numbers: famine, in seasons of a hundred, by how many of the nine boats follow the master (`code/rig/results_town/`, `code/rig/results_town2/`; 20,000 simulated seasons a cell; readers right 70 days in a hundred). The self-serving master misdirects once more than two boats follow him.

| What is changed | None follow | 1 | 2 | 3 | 5 | All 9 | Best following |
|---|---:|---:|---:|---:|---:|---:|---|
| Nothing changed (master right 80) | 7 | 5 | 6 | 14 | 44 | 44 | one |
| Master right 90 | 7 | 3 | 2 | 3 | 8 | 8 | two |
| Master right 99 | 8 | 2 | 0.3 | 0.1 | 0 | 0 | four or more |
| Master misdirects, one known day in ten | 8 | 7 | 12 | 30 | 77 | 78 | one, barely |
| Master misdirects, three days in ten | 7 | 12 | 31 | 70 | 99 | 99 | none |
| The same, master right 99 | 7 | 8 | 15 | 37 | 85 | 85 | none |
| Master's errors come in slumps | 7 | 7 | 22 | 58 | 95 | 95 | none |
| The same, master right 90 | 8 | 4 | 10 | 31 | 72 | 72 | one |
| Readers have bad weeks; master does not | 51 | 40 | 29 | 26 | 44 | 45 | three |
| Readers and master both have bad weeks | 52 | 44 | 51 | 71 | 95 | 95 | one |
| Readers share a blindness, 3 days in 10 | 96 | 95 | 95 | 97 | 43 | 44 | five or more |
| The sea remembers yesterday | 8 | 5 | 6 | 14 | 44 | 44 | one |
| Self-serving master; readers' bad weeks | 52 | 39 | 28 | 100 | 100 | 100 | two |

## §6. The code

- `code/fishing_town_T13.py` — all five lessons: the town in every
  arrangement, every famine probability.
- `code/correlated_weather_T14.py` — the shared-mirage towns, the
  floors, and the scale tax.
- `figures/fishing_town.png`, `figures/correlated_weather.png` — the
  exponential, the dose curve, the floors, the wildcard's insurance.
- `code/living_town_S1.py`, `figures/living_town_S1.png` — lesson
  six: both seas, the learning fishers, the rationality controls.
- `code/rig/town_stress2.py` — fishers who consult yesterday's sea
  (Theorem 21, simulated beside its exact figures) and the master who
  misdirects when his following pays him to.
- `code/borrowed_record.py`, `code/stay_ashore.py` — Theorems 22 and
  23, with every table.
- `code/attack_T22_T23.py` — both theorems attacked after they were
  stated: the fisher who knows everything, the sea where the boats
  that are right share the fish, the fisher who counts his own hunger.
- Formal statements and proofs: `docs/THEOREMS_v1.md`.


# Chapter 12. A Conjecture, Fenced

## §1. The idea, in plain words

[SPECULATIVE — everything in this chapter is conjecture. Nothing later
in the book depends on it. It is included because it is beautiful and
because hiding it would be a different kind of dishonesty.]

Notice what the fishing town never mentioned: humans. Its five lessons
were proved about *things that know imperfectly, err inevitably, and
share a future* — any such things, made of anything, anywhere. The
theorems do not check your species at the door.

## §2. The conjecture

So here it is, stated once. Any advanced life, on any world, that
satisfies this book's two axioms — no perfect knowledge, mistakes
inevitable — will eventually stumble into distributed error
correction, the way chemistry on any world stumbles into the same
stable arrangements of matter — the same bonds, the same molecules,
found in steps, because matter keeps presenting the same structure to
whoever is looking. The survival arithmetic is the same on every
substrate for the same reason the arithmetic of bonds is. What humans call democracy
would then be one species' rough, early, still-changing implementation
of a universal discovery — the way human laboratories are one rough
implementation of the scientific method, which any curious species
must also eventually find. Not an invention. An *encounter*.

## §3. What supports it

Only this, but it is real: the mathematics of Chapters 4 through 11
truly is substrate-free. The exponential of independent heads, the
collapse of shared teachers, the poison of herd-following, the floor
of sameness, the insurance of wildcards — none of these mention
neurons, ballots, or flesh. A silicon fleet, a fungal network, a
civilization of tides would face the same arithmetic. When the same
theorem binds every possible student, it is not crazy to expect every
long-surviving student to have learned it. The conjecture also has a named ancestor, in whose spirit it is offered: Sen's observation (1999) that no famine has ever taken place in the history of the world in a functioning democracy — a survival filter noticed in the record before any theorem bound it. Chapter 11's arithmetic is one candidate for why. The fence stays.

## §4. What limits it

Nearly everything else. Humanity has met exactly one advanced species,
and it is itself — and the ballot boxes, the single feeds, and the
welded gates of the present moment suggest that species is still in
the early, clumsy chapters of the discovery. A sample of one, still mid-
experiment, proves nothing about the curriculum of the universe.
There is also a quieter limit, which surfaced while this book was being written:
whether any observer *inside* a universe can ever hold the whole of
what feeds another mind's choices — there being no seats outside —
is a question that touches this conjecture's edges and stays open at
its own address (Chapter 15).

## §5. Why print it at all

Because the alternative is worse. A book that computes for eleven
chapters and then pretends to have no view of what the computations
suggest is performing modesty, not practicing it. The honest posture
is the one this chapter takes: state the beautiful thing once, mark
it clearly as unproven, fence it so it cannot pretend to be a result,
and leave it where a future reader — or a future species — can test
it. Beauty is not evidence. It is, sometimes, a map of where evidence
would be worth looking for.

## §6. Pointers

- The substrate-free machinery this conjecture leans on:
  `docs/THEOREMS_v1.md`, Theorems 13–14.
- The fence's terms: the front matter's label definitions.
- The open questions at this conjecture's edges: Chapter 15.


# PART V — THE LEDGER

## Why the self-anointed rule

*This part in one paragraph.* Where nobody can check an answer,
whoever holds standing supplies it. That is how a self-anointed few
come to decide the largest parts of other people's lives — whose time
may be taken, what a fair schedule is, what consent is worth — and it
is arithmetic before it is anyone's grievance: Chapter 11 computed it.
The remedy is not a better few. It is a ruler in everyone's hands. The
chapters ahead hand it over: the ledger; the strongest defense of the
man it audits, and the four answers to it; a national survey, a law
and an experiment that already fill its first columns; and what the
arithmetic says to do.

Start with where the few do not rule. Nobody — no senator, no
billionaire, no committee of laureates — gets to dictate the speed of
light. Nobody rules by decree on the energy in a gallon of gasoline.
Where an answer can be checked by anyone holding an instrument,
authority serves the measurement: the powerful build their bridges and
their engines around the numbers like everyone else, and an
undergraduate with a good instrument can overrule a king.

Now where they do rule. Whose time may be taken, and at what price.
What a fair schedule is. What a worker's consent is worth. Which
communities may be hollowed and called efficient. How much sameness a
society can be fed. These govern most of most lives, and they have
been governed by whoever had the standing to declare — because nobody
could check.

How the standing is acquired is Theorem 22, and it needs no villain.
Chapter 11's town had a sage. On a plain day — seven days in ten — he
was always right, and so, 999 days in a thousand, was the town without
him: a plain day is one whose answer anyone can check. On a hard day
he was right half the time, which is worse than one fisher reading the
water for himself.
The town kept one tally for each voice, plain days and hard days
together, and on that tally the sage held the best record in the
harbor: 85 right in a hundred against a fisher's 79. So every boat
followed him, on the hard days as on the plain ones, and the famine
rate doubled. His record was earned on the days when following him
changed nothing, and spent on the days when it cost the town its
fish.

That is the pattern outside the town. A voice earns its record on the
questions anyone can check. It is then believed on the questions no
one can check, where it is right no more often than anyone else. And
its misses there never reach the record, because nobody is keeping
score. How long such standing lasts depends on one number: the share
of the hard calls that somebody scores. Score every hard day and the
sage's standing is gone in a week. Score one hard day in a hundred and
it outlasts seven seasons. Nobody has to be fooled for any of this. A
fisher who knows every number in the theorem, and cannot tell on a
given morning whether the day is plain or hard, still does better for
himself behind the sage — and the town still does worse.

The theorem also says where such a voice will be found. Where a shared answer pays less — a fishing ground, a claim, a
crowded trade — the herd stops itself at two boats in nine. Where an
answer can be held by everyone at no cost to any holder — a forecast,
a doctrine, a verdict on what is fair — nothing stops it. That is the
second list above, and it is why the self-anointed are found there and
not at the assay office. A fortune works the same way, and
faster. The prospector who strikes gold was right once, about gold;
the fortune then buys a say in how schools are run, how hours are
scheduled, how the rules of the claims office are written — matters on
which the strike is no evidence at all — and Chapter 13 gives that
purchase its name: premium rights. A gatekeeper works the same way,
and slower: the reviewer, the chair, the board that decides which
assumptions a field may question holds standing earned on the part of
the subject that can be checked, and spends it on the part that
cannot. The exhibit below is one such assumption, held for half a
century in the hardest science there is.

So the law, stated once: **an unmeasured domain is governed by
standing, a measured one by measurement, and standing gives way at
the rate the measuring spreads.** The history of science is the
history of domains crossing that line — the heavens, then matter, then
life, then mind — and at each crossing those who ruled by declaration
did not concede. They did not have to. The instrument passed into too
many hands. Historians of measurement have told this story from the other end: Porter's *Trust in Numbers* (1995) shows quantification arriving in a domain exactly when its experts can no longer be trusted on their word alone. This part is in that spirit, read forward — it brings the numbers to the domain that has resisted them longest. The mechanism and the rate are Theorem 22, exact; the reach across history is this part's argument, and the exhibit below is its first case. And a ruler kept by one office is a harbor master holding a ruler: Chapter 11's arithmetic applies to it unchanged. What carries a domain across is the instrument in many hands — which is why every file this part uses is public, every script is printed, and Proposition 13.1 states what an audited party can and cannot do to the record.

And before anyone answers that societies elect their authorities: the
largest study of whose preferences move American policy — Gilens and
Page (2014), nearly two thousand policy questions — found the average
citizen's preferences with near-zero independent influence on what was
enacted, and organized interests and economic elites with a great
deal. The reply of its critics (Bashir 2015; Enns 2015; Branham,
Soroka and Wlezien 2017) is that on about nine questions in ten the
middle and the affluent wanted the same thing, so the data cannot say
whose wish was granted — and that where the two parted, the affluent
side carried it 53 times in a hundred. Fifty-three sounds like a coin
toss. A coin toss between the household at the center of the income
ladder and a household a tenth of the way from its top, on questions
where the two want opposite things, is not what one household, one say
predicts. And the same reply prints a second count. Over those
twenty-two years a policy the affluent wanted and the middle opposed
became law 37 times in a hundred; a policy the middle wanted and the
affluent opposed, 26. Read that reply in this book's
units. Where the two agree and the affluent would have carried it
either way, the average citizen's agreement decided nothing: the match
is a coincidence, and nobody was answerable to anyone. Where they part
and the affluent side carries, the outcome is an imposition, bought in
the currencies of Chapter 13's premium rights.

And the agreement
itself is weaker evidence than it looks, because a preference can be
manufactured by dependence. Nearly three American households in five
hold some stock, most of them through retirement accounts, and the
holding is wide and thin. Among households that hold any, the typical
one in the lower half of incomes holds 12,600 dollars of it and the
typical one in the top tenth 608,000; the top tenth of households hold
88 percent of all of it, and the bottom half hold six tenths of one
percent (Survey of Consumer Finances, 2022; Federal Reserve,
Distributional Financial Accounts, mid-2026). Nor is the holding
chosen in the sense the word needs. The employer picks the plan and
its menu; since 2025 the law enrolls the workers of a newly created
plan unless they object; the fund follows an index; and the keeper of
the index decides what enters it. In 2026 one index shortened its
waiting rule from three months to fifteen trading days, a newly listed
company entered on the fifteenth, and the funds that track the index
had to buy some four billion dollars of its stock at whatever the
price stood. It fell 15 percent in the next six sessions.

A
household whose old age has been tied to the price of shares wants
what raises the price of shares, and its wanting it says as much about
its choosing as a signature that the rent predicted (Chapter 13, the
third answer). Hold the first ruler to the preference: if
circumstances predict it, it scored no independence, and "they wanted
the same thing" is the ferry captain agreeing with the timetable.
Elected is not the same as answerable, and agreeing is not the same as
choosing.

The chapters behind you were the crossing. Agency — how much of a
person's action is their own, what builds it, what destroys it, what
its destruction costs and who pays — has been given a measure. Gates,
floors, frontiers, famine arithmetic: none of it asked anyone's
permission, and none of it consulted anyone's values. The chapters
ahead do the bookkeeping that follows. And the reader should
understand exactly what changes at this line, because it is not that
the powerful become villains. It is quieter and larger than that:
**they lose the standing to call it opinion.** The manager, the fund,
the ministry — each may still argue their arrangement is justified.
But they must now argue it against a ledger, in a domain that has
crossed the line — where authority is a servant, and an ordinary
person with a good instrument can overrule a king.

This part of the book is that instrument, handed over.

## The law's own exhibit

Before the bookkeeping begins, one exhibit — because the law just
stated has a sharper corollary that the reader deserves to see
demonstrated in the hardest science there is: *an unmeasured quantity
does not stay neutral. It gets assumed.* It happened twice in this
book's own lineage, and the two cases should be kept apart.

The first paper's case is the fare itself. For half a century the third
exit from Bell's theorem was waved away on an assumption nobody had
computed: that as the experiments grew, the share of measurement
independence a local account must relax would climb toward all of
it — full conspiracy, the door welded shut. Hall priced the smallest
case in 2010 and found about a seventh. The general case stayed unpriced
for fifteen years, and the dismissal stood on the unmeasured column
the whole time. The staircase of Chapter 2 is that column, measured:
the fare climbs with every pair of particles and never passes one
half. The assumption was not wrong by a little. It was wrong at every
size, forever — and it had governed the reputation of an entire exit.

The second paper's case is a quantity in plain view. The Bell
experiments are among the most scrutinized measurements in the
history of physics — four decades, escalating rigor, Nobel
recognition. Through all of it, one quantity was never
bounded below the percent level: the total rate at which detector pairs
fire, summed over all outcomes, as the analyzer angles turn. Quantum
mechanics says that sum is flat. One solved class of local accounts
says it carries a fringe — up to twelve percent deep at full strength,
a strength the existing record already rules out; what survives are
mixtures in which that class carries at most about a seventh of the
detections — a fringe at the percent level or below — and below the
percent level the sum has never been bounded. And here is the reason
nobody settled it [PROVEN — the hiding theorem, arXiv:2608.18886]:
the fringe takes *identical values at the two relative angles the
canonical experiment compares.* Not approximately — harmonic by
harmonic, the same number on both sides — so the comparison every
textbook test was built around cancels it exactly. The standard
experiment is not lazy about this quantity; it is mathematically
blind to it. For forty years the sum was checked
at the percent level and assumed below it — and everything downstream
of the assumption was governed by that assumption rather than by a
measurement.

The second paper of this book's lineage ends by handing over the
instrument: a scan protocol, validated in simulation, runnable in
hours on standard hardware, that confines every factorizable apparatus
artifact to where it cannot imitate the signal, calibrates out the one
that does not factorize, and bounds the column either way: flat, and a
named family of local accounts is confined an order of magnitude below
where the record left it; a fringe surviving the calibrations, and the
apparatus has produced a joint dependence on both analyzers that no
single pair with fixed imperfections can. (The paper's newest result
says where, on the terrains it tested, the correlation must live if the
door is taken: in the pair's frozen offsets at creation, correlated
between the two stations — not in anything either station does alone.
That is the one place Bell's own argument reserves for it.) Whichever way it goes, note
what changed the moment the protocol existed: the quantity stopped
being a matter of assumption and became a matter of schedule. That is
the crossing this book keeps describing, performed in miniature, at the
bottom of physics, on the very experiments this book's license rests
on. And note, with equal care, what did *not* change: the license
itself. The door's price was fixed by counting, in Chapter 2, over
every account a local world could keep; the scan decides which of two
ledgers the surviving accounts settle in, and a flat result closes no
door — it moves the bill.

An ordinary person with a good instrument can overrule a king — or
forty years of everyone assuming the king was right.


# Chapter 13. The Ledger

## §1. The idea, in plain words

Everything before this chapter built an instrument. This chapter
points it at the world — and then lets the world's best lawyer answer
back.

The claim, plainly: the takings of Chapter 7 are real, measurable, and
currently *uncounted* — and what is uncounted is free, and what is
free gets taken without limit. Economics has a word for real costs
that one party imposes and nobody books: an externality. Pollution was
one, invisible to every ledger on Earth, until it was measured — and
the measuring, not the outrage, is what changed what could be argued.
This book's proposal is the same maneuver one rung up: displacement of
agency, priced and audited, entered on the books beside every other
cost of doing business.

Where would an auditor look? The price list of Chapter 7 says where
takings are cheap, so it says where takings will be found: scheduling
that fills every gap in a worker's week; products engineered for churn
and distraction; systems that make lives more predictable to their
operators; arrangements that hold whole populations just below their
education gates. The list knows no company's name. It predicts only
this: *wherever extraction optimizes, it will be found parked on these
squares.* Predictions can be checked.

## §2. The story: the manager's defense

Return to the Harbor Grill. Its manager has read Chapter 7 — the
chapter that used his schedule as its example of theft — and he has
come to defend himself, with the strongest argument his position
affords. It deserves to be heard at full strength:

*"I priced it in. The instability you call theft is reflected in the
wage — and my workers, knowing the schedule's nature, agreed to work
for that wage. A willing seller met a willing buyer. Where is your
theft in a signed agreement?"*

It is a serious argument. Here are the four answers, in ascending
order of force.

**First: the defense concedes the ledger.** Listen to what "I priced
it in" does — it admits the quantity exists. You cannot price a
fiction. Five minutes ago the position was that nothing was taken;
now the position is that something real was taken *and compensated*.
That is not a rebuttal of this book. That is this book winning its
central claim — the quantity is real and belongs on the books — after
which the argument is only about the price. Which is exactly where the
argument should live.

**Second: "priced in" is now an auditable claim — and flat prices
cannot match nonlinear harms.** The manager paid a wage: one number.
But Chapter 7's arithmetic says the harm is not one number — in its
model it is seventy times larger against the time-poor than the
time-rich, ten times larger near an education gate, and different
between two workers on identical pay. A single rate that never asks where each
worker stands can cover everyone only if it is set above the largest
harm — and then it overpays everyone else; set anywhere lower, the
most-displaced workers are underpaid and the books call it even. Either
way the common price is not the harm, and which of the two the manager
is doing cannot be read off the wage without the audit. Pricing without
measuring is not pricing. It is rounding — in the house's favor. And
the claim is testable: if instability were truly compensated, wages
would rise with schedule chaos. Where such labor markets have been
examined, the premium has been hard to find: irregular and on-call
schedules are most common in the lowest income bracket (Golden 2015),
and estimated wage differentials for job attributes of this kind are
unstable and often wrong-signed (Mas and Pallais 2017, reviewing them).
Workers have priced one piece of the schedule themselves: in Mas and
Pallais's hiring experiment, the average applicant gives up a fifth of
the wage to escape a schedule set by the employer on a week's notice —
which the authors attribute largely to aversion to the evenings and
weekends such schedules bring, not to unpredictability as such. So the
experiment prices the employer's control of the schedule, not the
uncertainty this chapter's ledger tracks; that price is unmeasured.
Whether payroll pays the instability back was then asked of a national
survey directly (§2D). At equal schooling and age, the households
whose hours the employer varies are paid less, not more — full-time
workers included — and in the year the same person's hours pass into
the employer's hands, household income does not rise. It was not
priced in. And where steadier schedules were assigned by lot, the
stores that gave them sold more. It was not even paying.

**Third — the deep one: the consent he cites was purchased with the
very currency he took.** An agreement's validity rests on the agency
of the person agreeing — the capacity to weigh alternatives, model
futures, negotiate. Those capacities are exactly what time poverty and
gate-proximity degrade; that is not sentiment, it is the price list.
So a feedback loop hides inside the defense: past displacement lowers
the price at which future displacement gets "accepted." And the book
can measure this with its own instrument — *apply the two rulers to
the act of signing itself.* If a watcher who knows only a worker's
circumstances — rent due, no savings, every other kitchen in town
running the same schedule — can predict the signature with near
certainty, then the signing scored an independence of nearly zero.
That alone decides nothing — Chapter 4 built the book on the fact that
one ruler cannot: a predictable yes to a generous offer is the ferry
captain, competent and unreadable to no one. The second reading is not
the signing's aim — a yes that everyone gives carries no information
about anything — but Chapter 7's quantity: the
contract's net displacement of the worker's frontier, against the
named baseline of the worker without it. A predictable yes to an
arrangement that expands the frontier is the captain sailing the
timetable; a predictable yes to one that contracts it is a person with
no port left to choose. The two readings together say how much
*choosing* was in the choice. The law's "voluntary" is a yes-or-no
box; measured independence is a dial; and the defense requires
confusing the two. The book need not claim the workers were coerced.
It invites the manager to publish both numbers.

**Fourth: even a perfect private price cannot settle the public
account.** Suppose the manager truly, individually, correctly
compensated every worker. The town's ledger still shows a loss,
because Chapter 11 priced what degraded, dependent decision-makers
cost *everyone else*: fewer independent heads, weaker error
correction, children raised below their parents' time floors —
displacement landing on people who never signed his agreement. A
factory paying its own workers a smoke premium has not settled the
neighborhood's account. Private wages cannot buy back a public
exponential. (Chapter 14 §5C runs it in the economists' own model:
scored one household at a time, cash is the better remedy; scored by
whether the town survives, it does nothing.) That is the textbook meaning of an externality — Pigou's divergence of private from social cost (1920), and the gap that Coase (1960) himself said bargaining closes only when bargaining is free, which here it is not — and the
reason this chapter's title is not "the wage" but "the ledger."

The manager's defense, answered in full: *it proves the quantity
exists, asserts a price it never computed, rests on consent its own
practice degrades, and settles with the only parties who signed —
who were never the only parties owed.* And notice what the book never
called him: evil. It called him **unaudited** — the one charge a
signature cannot answer.

It is also a charge only an audit can settle, and a small one has been
run. It begins with something one of his workers would tell the
auditor, because she knows what a spreadsheet does not. Nadia: *"Don't
ask whether my hours change. Ask who changes them. When I swap a
Thursday with Tomas, the week is still mine. When he moves it, the
week is his."* Two schedules can look the same on paper and be
opposite things to the person living them. The difference is whose
hand is on the eraser.

A national survey asks her question. Each autumn the Federal Reserve
asks some eleven thousand adults how they are managing, and asks the
employees among them whether their hours are normally the same, vary
at their own request, or vary on the employer's needs. Employees whose
hours vary at their own request are, on getting by and on savings, not
distinguishable from employees on fixed hours. Employees whose hours
the employer varies are more often just getting by and more often
behind on bills, and their households are paid less, not more. Among
them, the ones told three weeks ahead look like fixed-hours employees;
the ones told later do not. And when the same person is followed from
one year to the next, the strain is there in the year the employer
holds the schedule and not in the year he does not. A survey shows a
pattern, not a cause — so two tests that can show a cause were run, by
others. Seattle required its large retail and food chains to post
schedules two weeks ahead and to pay for late changes; set beside
workers at the same chains in twenty-four other cities, Seattle's had
fewer short-notice schedules, less hardship and better sleep. And one
national retailer assigned twenty-eight stores by lot, nineteen to
steadier schedules and nine to business as usual. The steadier stores
sold 7 percent more.

What the files show is what she said: the harm follows the hand on
the eraser, not the variation. The counts, the tests that were written
down before the files were opened, and what none of the three
measures — a time floor, a gate, aim — are in §2D.

## §2B. The ledger of imposition

One structural result belongs here, because it explains where the
takings pool. Model a hierarchy of bounded agents — an executive over
regionals over managers over workers — with *uncertainty* arriving at
the top (a demand that varies by some fraction of itself) and each
level able to absorb only what its resources allow, passing the
remainder down, where it lands *whole* on every person below. Hours
partition: if two of twenty shifts are cut, two people lose the hours.
Uncertainty does not: all twenty face *will it be me*, and when the
shortfall is a fraction of demand each worker's share of doubt is the
same whatever the headcount. The cascade is a theorem about the second
quantity, and that is the one this chapter prices.
Computed exactly [EXACT within model]: the executive's resources let
him cushion sixty percent of the uncertainty that reaches him, so only
forty percent of it goes downhill; a worker can cushion seven percent
of what reaches him, and the other ninety-three lands on his life as
it is. The worker faces less absolute variance than the executive did
— the cascade thins it on the way down — and still loses **ten times
more agency per person**, because the least capacity meets the
highest price per unit (the elasticities of Chapter 7). In the reference
cascade, the bottom layer bears 93.4% of all agency destroyed — a
*share*: how the gross loss distributes across the layers, measured
against a world with no shortfall. What part of it is a *taking* is a
different number, measured against the firm's cheapest feasible
arrangement of the same shortfall, and is stated below.
Imposition narrows going up and multiplies going down — not because
anyone at the top is a villain, but because passing variance downhill
is every bounded agent's path of least resistance. The cascade needs
no conspiracy. It needs only gravity. Two fairnesses the ledger owes
the firm, both printed. The firm is a filter: a worker inside the
hierarchy faces forty percent of the customers' raw unpredictability;
a solo artisan would face all of it — which is Coase's reason firms
exist, and the ledger's claim is only that what the firm *chooses* to
pass down is unpriced. And the broadcast is a scheduling rule, not a
law of nature: it is the un-tiered on-call pool, where every worker is
a candidate for every cut. Whether concentrating the same shortfall on a
small on-call tier does less damage depends on where the pool sits:
above the gate the time curve is concave and spreading a small cut
costs *less* (Jensen's inequality, the same seventy-fold of Chapter 7
working in reverse); near the gate, where a spread cut would drag the
whole pool toward the cliff, concentrating it on a tier *compensated
to stay above its own gate* costs less. Rule three of Chapter 14 is
stated with that boundary. And the two numbers of this section must be
kept apart: the 93.4% is a gross share, against no shortfall; the
*taking* is what the actual arrangement destroys beyond the firm's
cheapest feasible arrangement of the same shortfall — which, for a pool
well above its gate, can be nothing at all, and for a pool near it, is
the whole difference between the un-tiered pool and the paid tier. Management cybernetics drew this picture decades ago: Beer's viable system (1972; the variety engineering made explicit in 1979) has each level attenuate the variety it can and pass the rest, and Simon's architecture of complexity (1962) explains why hierarchies are built that way. Supply-chain theory knows the same algebra running the other direction — the bullwhip effect (Forrester 1961; Lee, Padmanabhan and Whang 1997), where demand variance amplifies *upstream* through orders. The ledger of imposition is in the spirit of both and differs from each in one word: it tracks uncertainty broadcast *downward* through authority, multiplied by headcount, and prices what it destroys.

The cascade, written out (`code/imposition_cascade_T17.py`). Uncertainty V arrives at the top. A person at level l faces v_l, absorbs what a capacity c_l allows, and passes the remainder whole to every person below; the agency lost is what is faced, times that level's elasticity ε_l (Chapter 7):

    v₁ = V,     v_(l+1) = v_l − min(v_l, c_l),     loss per person = ε_l · v_l

The reference cascade, each person at one level directing four at the next:

| Level | People | Uncertainty faced, each | Absorbed, each | Elasticity | Agency lost, each | Agency lost, level |
|---|---:|---:|---:|---:|---:|---:|
| Executive | 1 | 100 | 60 | 0.008 | 0.80 | 0.8 |
| Regional | 4 | 40 | 20 | 0.02 | 0.80 | 3.2 |
| Manager | 16 | 20 | 6 | 0.1 | 2.00 | 32.0 |
| Worker | 64 | 14 | 1 | 0.565 | 7.91 | 506.2 |

The worker's row is 93.4 percent of the last column, and 7.91 against 0.80 is the ten of the text. The capacities and elasticities are the model's constants; the two elasticities at the ends are Chapter 7's, time-rich and time-poor.

Two corollaries, tagged. First [ARGUMENT, anchored]: formally
universal rights bundle a nominal tier and a *responsiveness* tier
priced in exactly the currencies this ledger tracks — time past the
gate, mistake budget, protected privacy — so rights-effectiveness
inherits the ledger's distribution. The largest empirical study of
American policy responsiveness is evidence consistent with the
responsiveness tier being priced. Call them premium rights; their most
concrete instance is the purchased mistake budget — too big to fail is
the right to err, sold in tiers, socialized at the bottom. Second
[CONCEPT, modelable]: theft compounds. The frontier is defined at the
system's current capacity, and agents operating at their frontiers are
what expand it — so stolen agency doesn't just harm its victim today;
it forecloses the expansions the victim would have contributed to
everyone's tomorrow. A stolen hour is a stolen future at interest.

**[INTERPRETATION — a resonance, not a premise. The book's theorems
stand without this box.]**

**The same bookkeeping, at the bottom of physics.** Chapter 7 showed
that stochasticity is transferred, not destroyed: suppress the visible
signature of an imposition in one channel and the bill surfaces in
another, at an exchange rate you can compute. It is worth knowing that
this accounting pattern is not a metaphor this book invented. In the
physics this book's lineage rests on, the same structure appears as a
theorem-grade trade-off: within the solved family of local accounts
of the two-particle experiment, any account that hides its detection
signature — a specific modulation in the total coincidence rate —
below two percent must thereby pay at least 45% of the full
measurement-dependence price in that column; below one percent, 68%;
below half a percent, 80% [EXACT along the stated family, and a statement about that
family only: flat-rate accounts exist outside it at lower detector
efficiencies, so flatness alone forces no payment — arXiv:2608.18886,
§8–9]. Within the family, the bill never vanishes. It moves between
ledgers at a posted rate, and every
ledger it moves to has its own observable signature. When this part of
the book argues that destroyed agency, priced at zero, does not
thereby cease to exist but lands somewhere on someone — the reader
should know that the deepest physical theory in existence runs its books
the same way. That is a resonance, and this book claims it as nothing
more. But it is a well-earned one.

## §2C. What the market's eyes cannot see

The manager's defense rests, in the end, on a kind of evidence: the
record of what people chose, at what prices, under what circumstances.
Revealed preference. It is the evidence economics trusts most, and it
is worth asking, in this book's own units, what it can see.

The record is the joint pattern of action and circumstance — which
option was taken, and what the observable situation was. Call it
*choice data*. Chapter 4's first ruler is a function of choice data
alone: independence, δ_A, is identified by it exactly. The second
ruler is not.

**Theorem 19 (The hiding theorem, economic). [PROVEN by construction;
interval endpoints NUMERICAL]** *(i) Independence is identified by
choice data. (ii) Aim is not: for any fixed choice data, aim ranges
over an interval whose lower end reads the residual unpredictability
as noise and whose upper end reads it as hidden competence. (iii) The
interval is wide. Two exact pairs: uniform choice data — every option
equally likely in every circumstance — is produced by pure scatter at
aim zero and by Ines's plateau strategy at aim c₀, identically; and
choice data of the form "follow the room half the time, scatter
otherwise" is produced by a town of Tomases and Nadias at aim 0.07 —
and, identically, by the sage, acting on perfect knowledge of the
future through a half-reliable world, at aim 1.00. (iv) The standard
welfare measure of random-utility economics assigns every point of the
interval the same number: the destruction of aim is not mis-estimated
by that model; it is invisible to it. (v) Recording the realized future
beside the action — the state of the world the action was a bet on,
realized afterward and lying outside the audited party's control,
linked to what the person chose — collapses the interval to a point.*

Read (iii) again, slowly, because it is the chapter's thesis in one
line. The perfectly competent agent and the near-aimless town leave
the same fingerprint in every dataset economics calls revealed
preference. A market that scores only choices and prices cannot tell
the Harbor Grill's Nadia from a sage who happens to disagree with the
room, and it cannot tell the Grill's Tomas from a sage in a world the
room usually gets right. Whatever was done to them is, in that record,
indistinguishable from taste.

The column that sees it is the one the standard record omits: outcomes
linked to choices — the same person's actions and what their future
actually held. Panels that follow people over years are, in this
book's terms, the economic torus scan; cross-sections of choices and
prices are the four canonical angles. [The congruence, as a resonance
and nothing more: a quantity the canonical data cannot see — not
approximately but exactly, harmonic by harmonic, because the
comparison that data makes takes the same value on both sides —
together with the instrument that sees it. Chapter 2's sequel found the same shape at
the bottom of physics. The theorem here stands on its own arithmetic.]

## §2D. A column from public data

**[DATA — descriptive, not causal; each test below was written down
before the files it was run on were opened, or before it was
computed.]** One column of §4's audit
can be filled from a public file. Each autumn the Federal Reserve's
Survey of Household Economics and Decisionmaking asks some eleven
thousand adults how they are managing, and in each of its 2019 to 2023
files it asks employees whether their hours are normally the same,
vary at their own request, or vary on the employer's needs: the same
variability with a different hand on the eraser — the distinction this
chapter's ledger turns on, and one a wage statistic cannot see.

In the 2022 and 2023 files (11,503 employees), hours that vary on the
employer's needs become rarer at every step up in household income,
from 28 percent of employees in the lowest band to 11 in the highest.
At equal household income band, education, age, gender, race and
ethnicity, marital status and children, the employees whose hours the
employer varies are more often just getting by or worse (7 points),
more often without three months of savings (5), more often unable to
meet a four-hundred-dollar expense (3), and more often behind on bills
because income varied (11) than employees on fixed hours. Employees
whose hours vary at their own request are not distinguishable from
fixed-hours employees on the first three. And among those whose hours
the employer varies, the ones told three weeks ahead look like
fixed-hours employees; the ones told later do not.

That much was looked at freely, and a free look proves little. So
three statements were written down — the gap belongs to the employer's
control and not to variability; it is absent at three weeks' notice;
the lowest incomes carry it most — and run unchanged on the 2019, 2020
and 2021 files, which had not been opened (18,268 employees). All
three held. Employer-varied against self-varied hours: 7.5 points on
just getting by, 5.5 on bills, 2.4 on the four-hundred-dollar expense,
each distinguishable from zero, and 1.5 on the three-month fund, which
is not. Less than three weeks' notice against three weeks or more:
10.5 points on just getting by and 8.9 on bills, with the long-notice
group 2.4 points *below* fixed-hours employees on the first, a
difference not distinguishable from none. The share on employer-varied
hours fell at every step of household income, from 28 percent to 12.

Two further tests were written down before they were computed. The
survey re-interviews part of its panel, so one person can be followed
from one year to the next: 4,816 employees, 7,390 pairs of adjacent
years. In the year a person's hours are in the employer's hands, that
person is 3.0 points more likely to be just getting by and 6.1 points
more likely to be behind on bills because income varied than in the
year they are not; hours passing to the worker's own request bring
no change distinguishable from none on either; and the difference
between the two changes is itself distinguishable from zero on both
measures (5.6 and 3.8 points).
Nothing fixed about a person — schooling, temperament, the kind of
work chosen — can produce that. And holding industry fixed, across
twenty-four industry groups and all five years, removes less than a tenth
of the gap: these are not simply restaurant and retail jobs.

The first reply an economist makes to all of this is that it is what
a priced-in schedule would look like: if unstable hours were paid
more, then at equal income the worker on unstable hours would be the
worse off by construction. The reply has a consequence that can be
checked, and the check was written down before it was computed: the
pay should be higher. It is lower. At equal schooling, age, gender,
race and ethnicity, marital status and children, households whose
hours the employer varies sit a fifth of an income band below
households on fixed hours, and are 5 points less likely to reach fifty
thousand dollars a year; among full-time workers alone the gap is 0.15
of a band. And in the year the same person's hours pass into the
employer's hands, household income does not rise: no change
distinguishable from none, and the largest raise the files leave room
for is three hundredths of one band.

What the survey carries, and what it does not. Savings did not move
within the person: the four-hundred-dollar and three-month measures
show nothing in the year-to-year test, where strain and bills do.
Entering an employer-varied schedule is distinguishable from staying
out of one; leaving has the committed sign and is not distinguishable
from staying in. The strain estimate, though not the bills estimate,
loses its distance from zero when the survey's weights are dropped.
One thing the free look suggested did not survive: that income varies
as much under long notice as under short — in the unopened files it
varies less. The 2021 file alone shows the three-week break weakly,
and two of the three unopened years were pandemic years.
The year-to-year estimates are about half the size of the
cross-sectional ones, which is what either selection into jobs or
misreported schedule types would produce, and the survey cannot say
which: of those whose hours the employer varied in one year, half
report otherwise the next. A change of schedule usually arrives with a
change of job, and a household already in trouble may take the job on
offer; following a person removes what is fixed about them, not what
happens to them. Household income is a band, not a wage. And nothing
here measures a time floor, a gate, or aim.

What the survey says: a quantity the manager's defense treats as
priced moves with who holds the schedule, in the direction the ledger
gives, in data collected for another purpose. (`code/field/` and its
`results/`; `docs/SHED_PREREG_v0.1.md`, `v0.2`, `v0.3`. The
survey's files are public and are not redistributed with this book.)

Two designs that *can* attribute have been run, by others, and they
point the same way. When Seattle required its large retail and food
chains to post schedules two weeks ahead and to pay for late changes,
workers there were compared, before and after, with workers at the
same chains in twenty-four other metropolitan areas (Harknett,
Schneider and Irwin 2021). Relative to those cities, short-notice
schedules fell 11 points and unpaid last-minute changes 13 — and
material hardship fell 10 points and sound sleep rose 11. And when
twenty-eight stores of one national retailer were assigned by lot —
nineteen to steadier schedules, nine to business as usual — the
steadier stores' sales rose 7 percent over the thirty-five weeks of
the trial, and each hour of their labor brought in 5 percent more
(Williams, Lambert, Kesavan and colleagues 2018). That second result
answers a question the first two leave open: what steadiness costs to
provide. The experimenters put the added revenue at 2.9 million
dollars and the out-of-pocket cost at about 31,000. In that experiment
it paid for itself. And in a survey of 27,792 hourly workers at eighty of the country's
large retail and food-service companies, the schedule predicts
distress, poor sleep and unhappiness much more strongly than the wage
does
(Schneider and Harknett 2019). The instability was not priced in, and
it was not paying.

## §3. The claims, tagged

**The displacement claim. [EXACT, model class]** Theft has a size
(Chapter 7's definition), sizes add, and the price list ranks where
taking is cheap — with no assumptions about any taker's costs.

**The schedule-control column. [DATA — descriptive]** In a public
survey, financial strain moves with who holds the schedule and not with
whether hours vary; it is absent at three weeks' notice; it follows the
same person from year to year; and the households on such schedules
are paid less, not more (§2D). Association, tested out of sample
and within person; not attribution.

**The parking prediction. [CONJECTURE, testable]** Extraction that
optimizes — by design or by blind trial — will be found concentrated
on the high-yield squares: time of the time-poor, knowledge near
gates, legibility of the covert, sameness at scale. No conspiracy is
required or alleged: ordinary profit-seeking discovers cracks the way
water does.

**The audit program. [BEGUN]** Mapping the model's quantities onto
measurable life — schedule entropy, planning horizons, feed sameness,
gate proximity — and testing the parking prediction against data.
Three columns are filled in §2D, by a survey, a law and an experiment;
§4 specifies the rest, and Chapter 15 says what each remaining column
requires.

## §4. The mathematics

The auditable object: for a person or population, the displacement
Δ = (where their frontier position was, or would have been) minus
(where the practice under audit left it), on both rulers of
Chapter 4. The price list converts practices into predicted Δ per
unit of resource taken; the audit runs the arrow backward, from
observed lives to implied takings. Three quantities a field audit
would estimate, all with model definitions: a person's *time floor*
(hours past the time gate), their *gate distance* (education relative
to their world's predictability), and their *schedule entropy* (how
little of their coming hours is settled in advance), and their *mistake budget*
(the error one bad month can survive, Theorem 5b) — each an estimator
of position on the (aim, δ_A) plane of Chapter 4. The manager's defense, in
these terms, is the claim that his wage equals Δ times a fair price —
a claim with two free numbers in it that his ledger has never
contained.

**Proposition 13.1 (The ledger cannot be gamed into a better position).
[PROVEN]** *Let a ledger score a population on both rulers with the
future recorded. Let any party post-process the population's actions
using anything it sees — the actions, the circumstances, private noise
— but not the future. Then: (i) aim cannot be raised above what the
people and the room already jointly know; (ii) independence cannot be
raised at a better exchange rate than the frontier's; (iii) raising
independence by injected noise lands visibly inside the frontier; and
(iv) the information an action carries about the future* beyond *what
the circumstances already say — I(A;F|E), the lower wall of Theorem 9′
— cannot be raised at all.* A population already on its frontier cannot
be moved past it. A population inside the frontier *can* be moved
toward it by a processor who sees the circumstances, by this
construction: rewrite each action as a function of
the action, the circumstances and a private coin, and the recorded aim
rises from 0 to 0.46 while independence rises too, because the
circumstances knew the future and the rewrite laundered that knowledge
into the action column. What that rewrite cannot do is raise the
conditional information, which fell from 0.81 to 0.35 in the same
construction. So the conditional information is the *un-inflatable*
part of the record — the one number the audited party cannot make
larger — and an audit records it beside the two rulers as a check, not
in their place: on its own it scores the captain and the sage at their
independence and nothing more, and it cannot tell a Tomas from a Nadia,
which the two rulers can. (The population in the construction, with no
unconditional aim and full conditional information, is one whose
actions encode the future only in combination with the room — a
private channel disguised as noise; a population with no private
channel scores zero on it, which is why it is a check and not a ruler.)
Two more safeguards the audit needs. The action alphabet is quotiented by consequence: two labels
with identical effects on every future are one action, or an operator
can inflate independence for free by appending randomized choices that
decide nothing (one irrelevant bit lifts a sage's reading from 0.81 to
0.91 with aim unchanged). And life-plane futures that leave an outcome on a record are rare per
person — a night class, a treatment, a venture, a handful in a decade;
most of what a life is spent on leaves none — so their
information is estimated on cohorts facing shared exogenous shocks,
never on one worker's few decisions, where the finite-sample bias alone
exceeds the dial.
(Clause (i) is the data-processing inequality; (ii) the definition of
the frontier; (iii) Chapter 6's first kept corpse; (iv) data processing
conditional on E.)

The attack surface that remains, printed at full strength: the
immunity is against manipulating *actions*, not *definitions*. If the
audited party is allowed to define the future against which aim is
scored — its own targets, its own measures of success — or to define
which circumstances count as the room, then aim is measured against a
chosen mark and the proposition does not apply. The defense is
procedural, not mathematical, and it is the audit's first rule: **the
future must be an outcome the audited party does not choose, recorded
by someone it does not pay.** Its second rule: **the future must be one the audited party cannot
manufacture from the action.** The gaming it names: a piece-rate
escalator on which a worker's recorded outcome is a function of
compliance scores aim at 1.00 for a trapped worker, because control
reads as foresight. The column that defeats it is the one Chapter 4
defined — an exogenous future: what the economy came to want, what the
illness was, where demand sat — which a night class, a treatment or a
side business succeeded by *matching*, and which no employer's payout
schedule can write.

> **The audit, specified.** What the chapters above require of any
> field audit, collected in one place so that a reviewer can check the
> design against it rather than reconstruct it.
>
> *Quantities.* Two rulers per person or population — independence
> H(A|E)/log|A| and aim I(A;F)/H(F) (Chapter 4) — with the conditional
> information I(A;F|E) recorded beside them as the un-inflatable check
> (Proposition 13.1). Three estimators of position on the plane: time
> floor, gate distance, schedule entropy; a fourth, the mistake budget,
> where it can be had.
>
> *The future column.* (1) An outcome the audited party does not choose,
> recorded by someone it does not pay. (2) An outcome the audited party
> cannot manufacture from the action — the economy's demand, the
> illness, the market, never a payout schedule. (3) Life-plane futures
> estimated on cohorts facing shared exogenous shocks, never on one
> person's handful of decisions.
>
> *The action column.* (4) The alphabet quotiented by consequence: two
> labels with identical effects on every future are one action. (5)
> Hand-to-mouth status, where it is an outcome, measured as a band —
> liquid savings within a fortnight's income of the limit, as the field
> already measures it — never as the limit itself (Chapter 14 §5C).
>
> *The ledger's baseline.* (6) Every entry against a named feasible
> alternative (Chapter 7 §1); for a firm's shortfall, its cheapest
> feasible arrangement of the same shortfall, not a world without it.
> (7) Identifying a loss is not attributing it; a design that can tell
> cause from company is required before a practice is charged. (8) The
> line between taking and winning is borrowed from property and law,
> not drawn by the instrument.
>
> *What a design can resolve.* (9) Any comparison of instruments —
> time against money, stability against wages — must hold prices or
> model them; the ranking reversed between the two in Chapter 14 §5C.
> (10) One cross-section at survey scale can establish that the time tax
> arrives as a threshold; it cannot certify the threshold's sharpness
> finer than about a quarter of the free-time range (Chapter 15 §4).
> (11) Estimates are regime-specific: a response measured under one
> schedule regime does not carry to another. (12) Hand-to-mouth
> status is the least stable signature of the mechanism across the
> model's constants; the price of credit and the stock of wealth are
> the stable ones (Chapter 14 §5C), so a design that scores only
> hand-to-mouth status can miss a mechanism that is present.

## §5. What is established, and the applicability program

The constants are the model's; the shapes are what travel. What
the small worlds establish is what pollution science had at its
beginning: the quantity exists, the instrument works, and the
direction of every effect is proven. What the world has added so far
is in §2D: a national survey in which strain follows who holds the
schedule, a law whose passage lowered hardship, and an experiment in
which steadier schedules sold more. The section that grows from here — real cases run
through the instrument, of which the manager is the first — is the
Applicability program, and its cases must each be done with the same
care this one received: the defense at full strength first.

The rulers are
substrate-free; nothing in them distinguishes a person from a firm. A
company with a private model of the future and actions the regulator
cannot predict from public data has independence and aim relative to
the regulator's seat, and an audit that extracts its model — as any
action–outcome log does, by Theorem 11 — displaces it. The ledger
records that displacement like any other; an instrument that read only
one way would be a weapon. What keeps the books from cancelling to zero
is not a moral clause but arithmetic the ledger already carries: the
same unit of displacement destroys more agency the lower it lands
(Theorem 10), and it is multiplied by headcount (the cascade). A
regulator's displacement of one firm and a firm's displacement of a
thousand workers are both entries; they are not the same size — and a
firm's entry is not weighted one either: its workers ride in its boat,
so a displacement of the firm's model is weighted by everyone
downstream of it, and an audit that homogenizes an industry's models
is the regulator committing the sameness of Chapter 11 at the scale of
the economy. The audit this book proposes records outcomes beside
actions; it prescribes no method, for that reason. Two more things the
rulers never score, said plainly. They do not score an agent's targets:
an embezzler disguising routine around a private aim stands on the same
coordinate as Ines. The ledger catches him elsewhere — on *other*
agents' planes, where his takings land as displacements (Chapter 7) —
not by reading his; and it catches him only as a magnitude. A
displacement on a counterparty's plane looks the same whether it was
won by a better product or taken by a bribe, and a theft diffused to a
dollar apiece across millions of buffered people registers almost
nothing on any of their planes. The ledger measures how much was
displaced, against a named entitlement; what counted as *taking* rather
than *winning* was settled before the ledger opened, by property and by
law, and the book borrows that line rather than drawing it. And who counts at all is set by the survival metric
chosen, which Chapter 11 states.

## §6. The code, and the record

- `code/theft_equilibrium.py` — the price list underlying every
  answer above.
- `code/fishing_town_T13.py` — the public exponential of the fourth
  answer.
- `code/field/shed_first_look.py`, `shed_oos_test.py`,
  `shed_panel_test.py`, `shed_pay_test.py`, with
  `code/field/results/` — §2D: the free look, the out-of-sample test,
  the within-person test, the industry control and the pay test, each
  with its preregistration in `docs/`.
- The manager's example in its original form: Chapter 7, §2.
- Formal statements and proofs: `docs/THEOREMS_v1.md`.


# Chapter 14. What the Model Says to Do

## §1. The idea, in plain words

This book promised no opinions, and it will not start now. What
follows is not advice, and it is not a program. It is a list of what,
inside the mathematics, made agents capable and towns durable —
ranked by the same arithmetic that priced the thefts, with no moral
premise anywhere in the machinery. The reader may do with the list
what they wish. The chapter's real business comes after the list:
an observation about it, stated once, exactly, and not inflated.

## §2. The seven rules, each with its receipt

**Get people past their gates.** Education below the threshold buys
zero independence; just past it, the highest leverage in the entire
price list. A society that stops teaching at "almost enough" has paid
most of the cost of education and bought none of this particular
good. *(Chapter 5.)*

**Put floors under time, and start at the bottom.** An hour returned
to the time-poor yields on the order of a hundred times the agency of
an hour returned to the time-rich (seventy-fold in proportional terms,
nearer two-hundred-fold per hour), because the most valuable hours anyone
owns are the first few past the time gate — which are exactly the
hours the time-poor lose first. If a society can protect only one
thing, the arithmetic is not ambiguous about which. *(Chapter 7.)*

**Match the shortfall to where the pool sits.** When demand falls
short, hours partition but uncertainty broadcasts: an on-call pool of
everyone makes every worker face *will it be me*. Above the time gate,
spread the cut — the curve is concave there and a small shared loss
costs least. Near the gate, where a shared cut drags everyone toward
the cliff, concentrate it on a small on-call tier *paid enough to stay
above its own gate*. The un-tiered pool of workers already near their
gates — the arrangement the schedule data describe — is the worst of
the four. *(Chapters 7 and 13.)*

**Treat privacy as infrastructure, not amenity.** A few honest flips
per decision, given jurisdiction over the big choices, make the
deepest file worthless — provided the flips are flips: a coin whose
generator a watcher can learn is a habit one level up, and the file
reopens. Wired narrow, no amount of wildness helps.
The difference between those two arrangements is the difference
between a person and a file. *(Chapters 8–9.)*

**Subtract sameness.** Past modest size, a community's safety is set
by what its members share — one curriculum, one feed, one method —
not by its headcount. Nine heads with one teacher are one head.
To make a big town safer, diversify the teachers and break up the
mirrors. *(Chapter 11.)*

**Dose central wisdom by its margin.** Experts are medicine; blocs are
poison — when the expert is only somewhat better than the room. The
printed town was safest listening to its best-informed voice with
exactly one boat; a far better expert earns a larger dose, and the
rule is to set the dose by the margin — net of any misdirection — and
by how the expert's errors correlate, never by the expert's say-so, and never by a record that mixes plain
days with hard ones (Theorem 22):
the channel worth following is the one whose errors are independent of
the room's. *(Chapter 11.)*

**Keep a few wildcards fed.** They cost fish on ordinary days and are
the only boats on the water when every trained head sails to the same
mirage. They insure subsistence, never prosperity — and only in towns
that share blind spots, which is to say, in every real town.
*(Chapter 11.)*

## §3. The observation, stated once

Stand back from the list. Education for all. Rest for the overworked,
the poorest first. Privacy. Pluralism. Distrust of concentrated
authority. Shelter for the stubborn and strange.

The reader has seen this list before — on monuments, in scriptures,
in declarations written by people who never heard of a conditional
entropy. This book put no morality into the machine, and the machine
handed back a recognizable portrait of it anyway — as if what the
traditions call decency were survival arithmetic, learned the long way,
by trial and by grief. The reader holds the evidence and may judge it.

The observation is stated, and stops there. Perhaps morality is the
species' compressed memory of theorems it could not yet write down.
Perhaps the resemblance is partial coincidence. The one thing the
resemblance is not, any longer, is unarguable either way. It has
numbers now.

## §4. Where the list and the monuments disagree

A resemblance claimed by advocates should be audited like any other
claim, so here is the place the list and the monuments *disagree* —
printed, not hidden. Tradition praises the stubborn universally; the
arithmetic does not. The wildcard rule is conditional: where error
sources are already independent, wildcards help nothing and cost
fish. The model's shelter for the strange is insurance against shared
blindness, not reverence for strangeness itself — a colder and more
precise kindness than the monuments carve. Readers who find more
mismatches are doing exactly what the book asks; Chapter 15 is where
such findings belong.

## §5. What kind of claim this is

It does not say these rules are good. "Good" is a word the machinery
cannot produce; the machinery produces "survived" and "was capable,"
and the bridge from *is* to *ought* remains the reader's to walk, as
it has always been. What the chapter removes is something narrower
and arguably more valuable: the claim that such rules are *mere*
preference — soft sentiment against hard realism. Whatever else the
seven rules are, they are also engineering. The realist who dismisses
them now argues with arithmetic, not with tenderness.

## §5B. The ledger runs both ways

One direction, stated as arithmetic and nothing more. Everything in
this book that prices theft also prices gift: the same exponential
that made famine risk halve with every two independent fishers is,
read forward, the *return curve* on investing in other people's
independence. Helping a neighbor past their gate, funding a stranger's
mistake budget, defending someone else's privacy — in the town model
these are not charity; they are purchased survival for the helper,
because every genuinely independent head added protects everyone,
multiplicatively. An economy oriented around moving people to their
frontiers — and then past them, since reached frontiers expand the
capacity that defines the next ones — is not a utopia this book
proposes. It is a configuration this book's arithmetic prices, and
the gross return is positive and exponential. What the investment costs, and how much of the return
reaches the one who paid, depend on the case, and two cases are in
hand. Between two towns of readers that send each other their surplus,
famine falls twenty-fold for both: the return reaches the giver
(`code/two_towns_aid.py`). And where steadier schedules were assigned
by lot, the stores that gave them sold more (Chapter 13 §2D): there
the investment cost its maker less than nothing. What any society does with that line item was never
this book's to say.

One thing more belongs on this side of the rule, because it is where
the argument over any remedy will be fought. Which remedy helps
depends on how the score is kept, and there are three ways to keep it;
§5C runs all three inside the economists' own model. Count what each
household gets to consume, one household at a time, and cash wins
easily: a steadier schedule barely registers. Count the capacity to
plan, and the order reverses — time first, a steadier schedule second,
cash nowhere. Ask whether the town survives, and it reverses the same
way: the printed town starves in 11 seasons of a hundred with no
program, in 11 with the cash, in 4 with the steadier schedule, and in
fewer than one with the time. Which score to trust is a premise no
model supplies. It is the same bridge §5 left to the reader — and two
people can read the same three scores, choose differently, and each
say exactly what the other is protecting.

## §5C. Inside the economists' own model

**[NUMERICAL — a standard model with one block added; every constant
the model's; signs committed in writing before the runs.]** A mechanism
that lives only in its author's toy is a mechanism the field can
decline to read. So the time gate of Chapter 7, the schedule tax, and
the scarcity drain were given their simplest macroeconomic form — a
household whose capacity to plan recovers only with free time above a
threshold, and is drained by schedule entropy and by scarcity — and
placed inside the heterogeneous-agent model that is the working
instrument of modern macroeconomics: a one-asset HANK, in the family
of Kaplan, Moll and Violante (2018) and the sequence-space form of
Auclert, Bardóczy, Rognlie and Straub (2021), with sticky prices,
sticky wages, a central bank, a government budget, and markets that
clear. What is tested there is that reduced form, not Theorem 16
itself. The household's bandwidth is a state beside its
assets and skill; it degrades the household's own optimization in the
two faces the scarcity literature describes — noisier choices, a
shorter horizon — and it is fed by free time above the gate and
drained by schedule entropy and by scarcity itself. In the spirit of
Gabaix's sparse households and Sims's costly attention, with this
difference: the quality of the planner is a depletable stock that
other agents' decisions can draw down. Switch the two faces off and
what remains is the standard household on a discretized savings grid
with a small decision noise — it converges to the toolkit's own as the
grid is refined and the noise removed (wealth within 1.3%, consumption
within 0.1%, at the finest grid run). Every number below is the model
minus that control, each at its own general equilibrium, with the
fixed-price version printed beside it. (Code and receipts:
`code/rig/hank_port/`, `docs/RESULTS_HANK_v0.1.md`,
`docs/RESULTS_STRESS_2026-11-09.md`; the signs were committed in
writing before the runs, with one dated addendum — the forecast ruling
below.)

The section in six lines, for a reader who will not follow the model through:

1. The mechanism survives prices. With the drain on, households want a seventh fewer assets, and the interest rate that clears the market is a third higher.
2. A cut in interest rates moves output further in the drained economy where wages are sticky, and less far where households set their own hours.
3. The unpredictability a firm chooses for itself is more than the amount that is best for everyone, and a charge of half a percent of the wage bill per unit closes the gap.
4. In 688 economies drawn at random the interest-rate results hold in every one. The counts of households living hand to mouth depend on the constants.
5. Whether cash, time or a steadier schedule helps most depends on what is scored: consumption, the capacity to plan, or the town's survival.
6. All of it rests on one supposition, printed with its date: that a household does not foresee its own depletion.

The block, written out (`code/rig/hank_port/bw_hank.py`). A household's state is its bandwidth b, one of four levels from 0 to 3, its skill, and its assets. Write x for the depleted share of bandwidth. Bandwidth enters the household's problem in two places and nowhere else — the temperature of its logit choice of next period's assets, and the discount factor it plans with:

    x = 1 − b/3,     κ(b) = κ₀ + κ₁·x,     β(b) = β·(1 − τ·x)

Each quarter bandwidth can rise one level and can fall one level, the two draws independent (a household drawing both stays where it is):

    P(rise) = p↑  if  T̄ − N ≥ T_gate,  otherwise 0
    P(fall) = 1 − (1 − S·ω)(1 − d·[cash on hand < m])

N is hours worked, T̄ the time endowment of the household's skill group, S the schedule entropy set on the firm's side, ω that group's exposure to it, and the last factor the scarcity drain. The control economy sets κ₁ and τ to zero, which leaves bandwidth moving and changing nothing. The naive household solves its problem as if b were permanent; the sophisticated one forecasts the law above. Welfare is scored at β, never at β(b).

The printed constants, per quarter (`code/rig/hank_port/hank_ge.py`):

| Constant | Value | In the code |
|---|---|---|
| Noise floor, and noise added at empty bandwidth (κ₀, κ₁; utility units) | 0.005, 0.05 | `k_min`, `k_tax` |
| Horizon shortened at empty bandwidth (τ) | 0.0153, which is 6 percent a year | `tunnel` |
| Time endowment by skill, low to high (T̄); hours are 1 in the control | 1.80, 2.05, 2.30 | `Tbar` |
| Free time needed before bandwidth recovers (T_gate) | 1.0 | `T_gate` |
| Chance of recovering a level, past the gate (p↑) | 0.159 | `p_up` |
| Chance of losing a level per unit of schedule entropy, by skill (ω) | 0.102, 0.040, 0.021 | `omega` |
| Schedule entropy (S) | 1.0 | `S` |
| Scarcity drain, and the cash-on-hand line under which it applies (d, m) | 0.069, 0.6 | `s_scar`, `m_scar` |
| Hand to mouth: next period's assets within this distance of the borrowing limit | 0.15 | `htm_cut` |
| The host: real rate, bonds, markup, elasticity of substitution, skill | 0.5 percent a quarter; 1.4 times annual output; 1.2; 0.5; three states, persistence 0.966 | the toolkit's calibration |

At these constants the low-skill group's free time is 0.80, under the gate, and the middle group's is 1.05, just over it.

What survives prices. The channel cuts household asset demand by a
seventh at the standard model's prices; with the stock of bonds fixed,
the economy clears at a real rate a third higher — the mechanism is
transmitted into the interest rate, not washed out by it. A monetary
easing moves output 1.8 times as far on impact as in the control: a
population whose bottom optimizer is taxed is an economy with a
steeper spending response, which is the macroeconomist's own
quantity — in the host where wages are sticky and output is
demand-determined. In a second host, where each household sets its own
hours against a wage that clears, the same economy responds *less* than
the standard one (0.7 times), because the taxed optimizer's hours
answer the wage more sluggishly; the amplification is claimed for the
first host and not for the second, and the interest-rate result holds
in both. (That is for small easings. At a hundred basis points the two
economies of the second host respond alike, and at three hundred the
taxed one responds a fifth more; most of the departure from linearity
there is the lumpy choice of hours, which both share.) The fiscal
counterpart is smaller. A tax cut paid for with debt moves consumption
in both economies — neither household is the one that ignores such
cuts, and most of that distance is the standard model's own. The taxed
economy spends a quarter to two fifths more of the cut within the
year, more the longer repayment is deferred, and at fixed prices it
spends *less* of it in the quarter it arrives, because decision noise
blunts the constrained household's one-for-one spending
(`code/rig/hank_port/ricardian.py`). Schedule stability beats an equal-dollar transfer on
hand-to-mouth status, under a condition stated below; which of the two
leaves a household better off depends on how the score is kept, and is
taken up further down;
hand-to-mouth behavior persists after liquidity is repaired and
recedes only when the drain is, under the same condition; a firm's
privately optimal schedule entropy sits above the planner's,
and the two coincide exactly when the channel is off, so the wedge is
the externality and nothing else — a Pigou correction of half a
percent of the wage bill per unit of entropy closes it at the printed
constants. And the gate is live in the aggregate, in the first host:
an easing large enough to push hours through a population's time
threshold produces an output
response forty percent above its own linearization and a
balance-sheet repair cut nearly in half, while the linear version of
the same model, which is what the field computes, reports nothing at
the gate at all.

What holds across the model's constants, and what does not. The
numbers above come from one set of constants, and a reader is entitled
to ask how much of the section is that choice. So the constants were
drawn at random — eight hundred economies across the whole box of
noise, horizon, gate position, drains, debt, income risk, markup,
utility curvature and both forecasts; 688 solved
(`code/rig/hank_port/sweep_signs.py`) — and every signed claim was
scored in each. Three held in all 688: asset demand falls at fixed
prices; the real rate rises in general equilibrium; half the dose
gives less than the full one. A fourth — more schedule entropy raises
the rate further — held in all but five, each of the five a
sophisticated household and each within a hair of zero. A fifth held
in all but two of the 526 economies with the naive household:
stability adds more welfare to the taxed economy than to the
standard one by a wider margin than the equal-dollar transfer does —
the part of the gain that belongs to the mechanism, not the whole of
what a household gets.
The hand-to-mouth claims are the
ones that depend on the constants. With the naive household and the
curvature of the printed economy they hold in nearly every draw — the taxed economy has more
hand-to-mouth households in 97 of 100, the residual after liquidity
repair is positive in 98, stability beats the transfer on that count
in 88. With logarithmic utility, where the same decision noise is
larger against flatter stakes, they hold in about half the draws —
in seven of ten where the shortened horizon is large against the
noise, in three of ten where it is small. The reason is the one the
band already showed: the horizon
face pulls households toward the limit and the noise face scatters
them off it, and the count of households near the limit reports
whichever is winning. The mechanism's signature in the interest rate
and in the stock of wealth does not depend on that contest; its
signature on
balance sheets does, and a field design that measured only
hand-to-mouth status could find nothing, or the opposite sign, in an
economy where the mechanism is fully present. One in seven of the
drawn economies did not solve — the ones with little income risk and
much public debt, not the ones with unusual bandwidth constants — and
those are missing from every count here.

The same sweep as a table: the share of drawn economies, in a hundred, in which each signed claim holds (`code/rig/hank_port/results_sweep_fast/SWEEP_SUMMARY.md`; general equilibrium unless said).

| Signed claim | All 688 | Naive household, 526 | Sophisticated, 162 |
|---|---:|---:|---:|
| The real rate is higher under the tax | 100 | 100 | 100 |
| Asset demand is lower at fixed prices | 100 | 100 | 100 |
| Half the dose moves the rate less | 100 | 100 | 100 |
| More schedule entropy raises the rate | 99 | 100 | 97 |
| Stability beats the equal-dollar transfer on welfare | 94 | 99.6 | 74 |
| More low-skill households hand to mouth under the tax | 75 | 75 | 76 |
| The gap stays positive after liquidity is repaired | 75 | 74 | 77 |
| Stability beats the transfer on hand-to-mouth status | 51 | 64 | 10 |
| Time beats cash on hand-to-mouth status | 38 | 42 | 25 |
| Time beats cash on hand-to-mouth status, prices fixed | 20 | 22 | 17 |

What prices reverse. At fixed prices a cash transfer beats a time
transfer at lifting the time-poor out of hand-to-mouth status — the
cash removes the scarcity drain and does the time transfer's work; in
general equilibrium that advantage shrinks by two thirds and the
time transfer wins. The ranking of the two instruments is decided by
the price adjustment, which is a warning printed for the field audit:
a comparison that holds prices fixed can rank the arms wrongly. And in
the second host, where hours are the household's own, the cash wins on
the balance sheet in general equilibrium as well — the time transfer's
gain there is bandwidth, not hand-to-mouth status — so
the claim that time beats money at lifting households off the limit is
made for one host and withdrawn for the other — and across the drawn
economies of the first host it holds in two of five, so it is
withdrawn as a general claim altogether. What survives is that the two
instruments buy different things.

Where hours are the household's own, three more things the one-asset
host could not say. At the printed constants, nine in ten low-skill
households work below their own time gate in the control economy,
before any tax on bandwidth exists: the floor is sold for income, and the sale is not a symptom of
the tax but its precondition. A freed hour is kept, not sold back —
hours move by half a percent — and the share working below the gate
falls by fifteen points. And a cap on long shifts lowers output and
welfare in both economies and leaves the share below the gate where it
was: the instruments this book prices are stability and time, not
prohibition.

And a third host, for the objection that one asset is one too few:
two accounts, a liquid one and an illiquid one that pays more and
charges a fee to move — the structure the field uses for the wealthy
hand-to-mouth (`code/rig/hank_port/bw_two_asset.py`; fixed returns
unless said). There the head count of hand-to-mouth households barely
moves, 45 percent against 47, while its composition turns over: the
wealthy hand-to-mouth fall from 26 percent of households to 18 and the
poor hand-to-mouth rise from 19 to 29. Illiquid wealth falls by a
fifth and liquid by a seventh, and the liquid rate that clears its
market rises a point and a half a year. The shortened horizon does
this and the noise does not: the taxed household stops building the
asset that takes patience. Repairing liquidity widens the low-skill
gap, 16 points against 12. Time and stability lower low-skill
hand-to-mouth status and raise illiquid holdings; an equal-cost cash
transfer raises hand-to-mouth status in both economies and lowers
illiquid holdings.

The constants of this host were then drawn at random, as the first
host's were: three hundred economies over the bandwidth constants, the
income process, curvature, both returns, both fees and patience; 273
solved (`code/rig/hank_port/sweep_two_asset.py`). In every one of the
182 whose standard twin holds illiquid wealth worth a quarter's income
or more, illiquid wealth is lower under the tax — by a quarter at the
median — and half the dose does less; in all but one the wealthy
hand-to-mouth are fewer. Liquid wealth is lower, and the rate that
clears it higher, in six of seven. The poor hand-to-mouth are more
numerous in nine of ten and the head count is higher in five of
eight: the composition is the signature, the count is not. The
residual after liquidity repair is positive in five of six — nearly
always at the printed curvature, in three of five under logarithmic
utility. Stability raises low-skill illiquid holdings in 97 of 100,
and equal-cost cash lowers them in all but one. A time transfer does
its work only where it carries the household across the gate: where
it does, illiquid holdings rise in nine of ten; where it stops short,
in 2 of 71 — the time gate of Chapter 7, found again by a random
draw. In the other 91 economies the standard twin holds almost no
illiquid wealth. There is nothing there for the tax to remove, the
noise scatters households upward off the floor, and the signs fail;
they are mostly economies of logarithmic utility in which four
households in five already live hand to mouth, and they are printed
as the map's edge.

The same sweep as a table: the number of drawn economies in which each claim holds (`code/rig/hank_port/summarize_two_asset.py`). The middle column is the 182 whose standard twin holds illiquid wealth worth a quarter's income or more; the last is the 91 whose twin holds almost none.

| Claim, taxed economy against its standard twin | All 273 | Twin holds illiquid wealth, 182 | Twin holds almost none, 91 |
|---|---:|---:|---:|
| Illiquid wealth is lower | 240 | 182 | 58 |
| Half the dose moves it less, in the same direction | 231 | 182 | 49 |
| The wealthy hand to mouth are fewer | 240 | 181 | 59 |
| The poor hand to mouth are more numerous | 183 | 162 | 21 |
| Liquid wealth is lower and its clearing rate higher | 175 | 157 | 18 |
| The hand-to-mouth head count is higher | 123 | 114 | 9 |
| The low-skill gap stays positive after liquidity is repaired | 161 | 152 | 9 |
| Stability raises low-skill illiquid wealth | 189 | 176 | 13 |
| Equal-cost cash lowers low-skill illiquid wealth | 213 | 181 | 32 |
| A time transfer raises it, where the transfer clears the gate | 100 of 171 | 99 of 111 | 1 of 60 |
| A time transfer raises it, where the transfer stops short | 3 of 102 | 2 of 71 | 1 of 31 |

Which remedy helps depends on how the score is kept, and there are
three ways to keep it. The standard way counts what each household
gets to consume over its life, one household at a time. On that score
cash wins easily and a steadier schedule barely registers — at the
printed constants it is worth to the household what a fifth of one
percent of average income, paid in cash, is worth — because the only
harm this score can see in a drained mind is a slightly worse savings
plan, and slightly worse savings plans cost little (Cochrane 1989).
The second way counts the capacity to plan, which in this host is
bandwidth: the time transfer lifts the low-skill group's from 0.30 to
0.65, stability lifts it to 0.42, and cash leaves it where it was. The
third way asks whether the town survives. Put the same households in
Chapter 11's boats, on the supposition that a reader's accuracy rises
with bandwidth — a supposition with a measured direction: money
worries cost a mind, on the spot, about what a lost night's sleep
costs it (Mani and colleagues 2013), and factory workers paid early by
lot made fewer mistakes and turned out 7 percent more (Kaur and
colleagues 2024). The direction has been measured in a laboratory, at
a harvest and on a factory floor, and missed once, in a survey of
American households around payday (Carvalho, Meier and Wang 2016). The town starves in 11 seasons
of a hundred with no program, in fewer than one with the time
transfer, in 4 with stability, and in 11 with the cash, because moving
fish from one hold to another puts no boat on the fish
(`code/joined_three_rulers.py`). And when a quarter of the fleet reads
a little worse — right 60 times in a hundred where it was 70 — a
ledger that adds up boats one at a time records 3.6 percent less fish,
while the town's famine rate more than doubles. Across the drawn
economies the order holds: stability beats equal-cost cash on the
standard score in none of the 528 economies of the first host and 4 of
the 182 of the third, and on each of the other two scores in all but
one.

The standard score is the only one of the three that favors cash, and
the only one that counts each household as failing alone. Which score
to trust is a premise no model supplies, and the sizes are the models'
own; the working — the two-asset figures, every version of the
supposition, and what the earlier rankings "on welfare" in this
section do and do not measure — is in Appendix H.

And one supposition, made explicit because every model of this kind
carries it silently. The standard household knows its own mind
perfectly and never degrades. A household that *forecasts* its own
degradation — that plans around its future, more impatient selves —
saves to protect itself from them, and in that model the repairs lose
their effect or reverse it: a time transfer that lifts the group's
bandwidth by half leaves hand-to-mouth status where it was, and
schedule stability raises it. A household
that does not perceive the tunnel from inside, which is what the
scarcity literature describes, saves less when degraded and more
when repaired, and the repairs help. The two assumptions change
the sign of the policies in the model; the second is the one used, and
the first is printed beside it with the date on which the choice was
made. A second premise is printed with the first: welfare is scored at
the undegraded horizon — the degraded planner is a worse planner, not
a person with a new preference. Any criterion that honors the
shortened horizon as a preference scores the loss of bandwidth as a
gain, because a more impatient household reports less concern for
the hardship it is storing up; under such a criterion the planner's
schedule entropy rises above the firm's and the correction becomes a
subsidy to the drain. The Pigou result stands on the first criterion,
and whoever prefers the second must own what it implies: that
scarcity improves a life by that life's own lights. A model's
suppositions about what its agents know of themselves, and about how
their welfare is to be read, are not laundered into its conclusions
here; they are listed, and the reader can see which conclusions
depend on which.

A third supposition is the host's own and is left as found. Its
households' skill is a number drawn by chance and redrawn by chance;
nothing a household does, and nothing done for it, produces it. A
reader who takes this model's high earners for the talented is reading
a lottery, and so is a reader who takes them for the lucky: the model
cannot tell the two apart, because it has no account of where skill
comes from. The towns of Chapter 11 have one — a reader's accuracy
fades with disuse and returns with practice — and no chapter of this
book treats a capacity as issued at birth, or as equal at birth. Both
are suppositions, and neither is needed.

Two cautions from the same host, found by stressing it. Hand-to-mouth
status in every sentence above is a *band* — liquid savings within a
fortnight's income of the borrowing limit, as the field measures it —
and not the limit itself: noise moves households off the exact corner
into the band beside it, so counted at the corner the taxed economy
shows *less* hand-to-mouth than the standard one and the stability
result reverses; counted as the field counts, it holds. The same
result asks one more thing of the mechanism: that the degradation
touch the horizon or the attention and not the choice noise alone —
four microfoundations of the degraded optimizer were run at equal
footprint (noise, which is the rational-inattention solution;
tunneling; present bias; sparse attention), and every one amplifies
the monetary transmission in the first host, but under pure noise the
stability arm and the transfer arm tie. And the
economy's own transmission is a function of the schedule regime — the
monetary response is 1.4 times the standard model's at half the
printed entropy, 1.8 times at the printed one — so a response
estimated under one regime does not carry to another, which is the
economists' oldest objection to reduced forms (Lucas, 1976), returned
here against any audit that would estimate the mechanism's effects
from a single regime.

The constants are the model's. Every bandwidth parameter is a model constant rescaled from an
earlier toy; the gate's position was placed by hand; the magnitudes —
two to four points of hand-to-mouth status, under half a percent of
consumption, a real rate higher by a median of eight tenths of a
point a year across the drawn economies — are the model's and not the
field's. What the section
establishes: the mechanism is hosted by the standard model
without modification to the standard model, and what it does there
is computable, and it was computed.

## §6. The receipts

Every rule's derivation, by chapter above; every constant's model
class in `docs/THEOREMS_v1.md`; every computation in `code/`, with
the general-equilibrium host under `code/rig/hank_port/`.


# Chapter 15. What Each Open Question Requires

## §1. The rule of this chapter

Every question below is open for a stated reason: a proof nobody has
found, a computation larger than any yet run, or a measurement nobody
has taken. Each entry says which, and what closes it. Several entries
that stood here in earlier drafts were closed by doing the work, and
are kept as they were closed.

## §2. Proofs

**The exact frontier, and the plateau's edge.** The first curve for
the trade between aim and unreadability was printed as within a hair
of the truth. It was not: near perfect unreadability the plateau runs
at least five times further than that curve knew (Chapter 6, the
second kept corpse). The edge is now bounded below in closed form
(0.247 in the reference world) and, numerically, by a vertex search
(0.335) — the edge is a vertex of a polytope, which is why smooth
optimizers missed it twice — and above only crudely (0.56); the exact
edge, and the frontier's shape from the edge to the sage point, are
open. The vertex found at 0.335 recurred in fewer than one in a
thousand of 127,000 restarts, which says the landscape has many local
vertices and the true edge may be higher still. One case is now
closed and one is fenced, by branch-and-bound on the separable concave
objective (`code/rig/plateau_edge_bnb.py`). With three futures at a
coin-noisy room the edge is exactly 1 − 1/log₂3 ≈ 0.369 — every
future answered by an even split over two of the three actions — and
the search tree is exhausted. With four futures the edge is fenced to
the fourth decimal: the best vertex found, (5 log₂5 + 9 log₂3 − 6)/64
≈ 0.31054, against a certified ceiling of 0.31074 after four million
nodes. Vertices at more futures are floors, and the edge is not
monotone in the number of futures: 0.369 at three, 0.311 at four, at
least 0.357 at five — lower at four than on either side, with
certainty. At five the certified ceiling after eleven million nodes
is 0.469, so whether five sits above or below three is open. The
floors found at six and seven, 0.335 and 0.359,
continue the sawtooth, odd counts above even, without proving it. No
formula that only falls or only rises with the number of futures can
be the edge. For the reference world itself
the same tool does not bite: after nine million nodes its certified
ceiling at six futures is 0.641, looser than the crude 0.56 above.
What closes it: a bound that tightens faster than the corners
multiply. It is a problem in concave minimization over a polytope,
stated completely, with certified floors printed for whoever takes it
up.

**The inversion on the wider plateau** — posed here in one draft and
answered in the next, kept as a worked example of this list shrinking.
The inversion survives on the wider plateau (0.65 against the open
expert's 0.75) but the coin share a watcher needs rises from one-third
to seven-tenths, because those strategies spend their chance where the
world is wrong and the future is not for sale. The general law followed the same
day — Theorem 9′, the sandwich — and the entry is kept as what it is:
an open problem that lived for one draft.

**The gate, generalized — closed.** The threshold e + s > 1 was proven
for the symmetric worlds; for any channel the gate is a threshold per
signal, e* = (q_max − q_k)/(q_max + (n−1) q_k), by the same four lines
(Theorem 5c). Kept as a worked example of an entry that was open for
one draft.

**The wiring theorem, hardened — mostly closed.** The dichotomy is now
a one-parameter law: the floor depends only on how far the fresh bits
reach across the choice space, exactly, across every habit-space size
tested, and the one-time-pad point scales as the logarithm of the
habit count (Theorem 11′). The gated inversion's margin,
which fails in one world of six on the wider plateau, turned out to be
a coarse-habit effect: for fine habits the gated floor converges to a
value below the ceiling at every h (Theorem 11′(iv)). Open: the general
theorem for arbitrary habit structures, beyond the span family.

## §3. Models

**The living town, continued.** Chapter 11's sixth lesson built the learning town
and scored the standing prediction (refuted as stated; confirmed once
crowding costs something). Fishers who consult yesterday's sea are
Theorem 21; fishers who may stay ashore are Theorem 23. What remains
is the glass-sea reading — whether economies in which crowding costs
nothing really do lose their self-correction — and that is a
measurement: the same herd, observed where joining it is free and
where it is not.

**The clever weak watcher — closed.** Run on the rig: pattern-miners
with no model, and sequence models told nothing, reach the exact floor
within days on every wiring and habit space tested (Theorem 20). There
was no gap for cleverness to occupy; the entry is kept as what it was.

**Acting and reading — modeled, not proven.** Theorem 13 protects a
town through its independent readings, whoever dispatches; a
dispatcher who polls the fishers inherits it. Whether readings stay
independent in a population that never acts on them — whether
calibration requires one's own mistakes — was the conjecture. As a
model (`code/rig/living_town_skill.py`): let a fisher's accuracy fade
toward chance on days he follows and recover on days he acts on his
own reading. The natural expectation, a point of no return, fails: a
town of readers and a broadcast town reach the same long-run state,
and the refutation is kept. What exists instead is a slope: with the
strongest crowding the town keeps a third of its boats reading even
when fading outruns recovery tenfold, but their skill is at chance, so
the town *looks* plural and knows nothing the hub does not; with any
slack in the crowding, fading at a fifth of a percent a day against
recovery at half a percent carries the town from half-and-half to
seven boats in ten behind the hub, and a glass sea, three-quarters
herded to begin with, to nineteen in twenty. Two consequences. A head count of who follows cannot see the
loss — it shows on the aim ruler and not on the independence ruler,
which is the reason the book carries two. And because the state is an
attractor and not a trap, it moves when its causes move: crowding
restored or practice restored, the readers return. Whether human
calibration fades this way, and how fast, is a measurement, not a
theorem; the model says what would follow if it does.

**The masters who lie, and the days that remember — computed in
part.** Persistent error, strategic misdirection and shared blindness
are now in the town (S2, Chapter 11 §5): the dose rule survives as
"follow the channel whose errors are independent of the rest, in
proportion to its margin net of its lies," and the all-readers
headline is confined to readers whose errors are their own. Fishers
who use yesterday's sea are Theorem 21, and a master who misdirects
once his following pays him to is computed (Chapter 11 §5). Readers
who can tell are Theorem 22: they keep two tallies.

**The surveillance regress — measured, not closed.** Hypothesis; then
the method that updates hypotheses; then the method's inspiration —
each level of watching must acquire a new private top level. The race
between the fresh-input stream and the watcher's acquisition now has
one measured leg: a coin that is secretly a generator stays a coin only
while its hidden state exceeds what the watcher can learn in a lifetime
— between 12 and 32 bits for a million-parameter learner and the
weakest generators (Result R6). The general statement, for any
generator and any watcher, and what plays the generator's role for a
human mind, stay open. (Its
speculative capstone — whether any watcher inside a universe can hold
the whole of what feeds a mind — stays fenced where Chapter 12 left
it.)

**The household's knowledge of its own mind.** Chapter 14 §5C showed
that whether a household forecasts its own degradation erases or
reverses the bandwidth repairs in the standard macro model. The
scarcity literature says the tunnel is not seen from inside; whether
people are naive or sophisticated about their own bandwidth — and
whether the answer differs across the gate — is a measurable question
that no model can settle and that decides which of two economies the
world is.

**The bill's counterfactual.** Identifying a loss of aim is not
attributing it. Attribution takes a design: the same person across
time, a law that changes one place and not another, or assignment by
lot. All three now exist for schedules (Chapter 13 §2D). What no
dataset yet links is the schedule, the hours left over, and what the
person went on to do with them — the column that would put a number
on a time gate. It requires a panel that records all three; no public
one does.

**The leapfrog.** The frontier is defined at current system capacity;
agents who reach it expand the capacity, which relocates everyone's
frontier. A dynamic model of that recursion — growth as frontier
expansion, theft as compounding foreclosure — is the next model to
build. It needs one rule, for how a reached frontier moves the others;
the two towns of Chapter 14 §5B are its first data point; and it is
where this ledger meets the economists' oldest question on their own
ground.

**The isolations still assumed.** Each Part of this book removed an
isolation the Part before it had assumed — the unwatched agent, the
private error, the fixed accuracy, the private signal, the fixed
price, the household that fails alone — and in most cases the
conclusion changed with it (`docs/ISOLATION_AUDIT_v1.0.md` lists
them). Two more were computed as this list was being written. A town
with a neighbor: two towns of readers
that send each other their surplus cut famine from 7 seasons in a
hundred to a third of one, while two towns each behind its own master,
or both behind one, gain nothing — aid is worth what the sameness
between giver and receiver leaves it (`code/two_towns_aid.py`, exact).
And who is on call: selling the burden to the same few boats is better
for the town than drawing it by lot in most cases computed, because
spreading it wears down every reader's skill; the lot wins only where
skill fades slowly and an on-call day is half lost; and the boats that
sell end at chance, which the town's famine count does not see. The
expectation that such a trade would starve the town was refuted, and
is kept (`code/duty_trade_exact.py`). Still assumed, with what removing each takes: a
future that nobody's action moves (the leapfrog, above); an education
that arrives from nowhere and is independent of the world it is used
in (a model of who teaches, and what it costs them); an agent who
knows exactly how reliable its world and its own knowledge are
(Theorem 22 is the first case in which it does not); a watcher who is
not watched back (two-sided watching); a sea that is never fished down
(a stock the fleet draws on); a skill drawn by lot (skill produced by
time and teaching); uncertainty that travels down a hierarchy and
never back up (quits and slowdowns in the cascade). Each is a model to
build, not a measurement to wait for. One number would join the three
scores of Chapter 14: what a unit of the capacity to plan is worth in
consumption — this book's title, asked as a number. That one is a
measurement: the same people's judgments, scored under a steady
schedule and under a broken one. Seattle's law measured their sleep
and their hardship; nobody has yet scored their judgments.

## §4. Measurements

**The field audit.** Three of its columns are filled (Chapter 13 §2D):
strain follows who holds the schedule in a national survey, and
within the same person across years, and the households on such
schedules are paid less, not more; a scheduling law lowered hardship
where it passed and not elsewhere; steadier schedules, assigned by
lot, sold more. Not yet measured anywhere: a time floor, a gate
distance, aim. What a survey of them can resolve was computed before
any is run (`code/rig/audit_identification.py`): from one
cross-section with free time measured to a tenth of its range, a sharp
gate is told from a slope with near certainty at three thousand
workers, and a ramp a quarter of the range wide still reads as a gate
at ten thousand — the audit can establish that the tax arrives as a
threshold, not how sharp the threshold is. Any comparison of time
against money must hold prices or model them, because the ranking
reversed between the two in Chapter 14 §5C. What the audit requires is
not mathematics: a panel of a few thousand workers with schedules,
free hours and outcomes linked. It is the largest project the book
names, and the one on which its economic claims stand or fall.

**The price of subtracting sameness.** Decorrelation is worth more
than growth past modest size — but diversifying teachers and breaking
mirrors costs something, and that cost is a measurement no town can
supply: what a second curriculum, a second feed, a second method costs
to run. A ledger needs both columns.

**The neighbors' map.** A full accounting of where this framework's
pieces were anticipated — the mathematics of influence, of limited
attention, of unbreakable codes, of undiversifiable risk — is printed
as Appendix D, and the news is good: nearly every part of the engine
was built and tested elsewhere before this book borrowed it, which is
the best thing that can be said of any part. The configuration is
this book's. The ancestors are named in the chapters where their shapes
appear, with the difference stated each time, so that no reader
mistakes similarity for identity in either direction.

**The strongest standing attack, printed at full strength.** Any
quantum-scale slack, a critic will say, decoheres in the warm wet
brain long before it could steer a neuron, let alone a schedule:
the license may be real and the tenant impossible. The
response has two parts. First, the in-principle version of the attack
fails: classically chaotic systems amplify arbitrarily small
differences to macroscopic scale (Borel's electron at the edge of the
universe altering a billiard break within seconds), and the brain is
nothing if not nonlinear — so "too small to ever matter" is not a
theorem anyone holds. Second, and printed with equal weight:
amplification of noise is not harvesting of structure — chaos
amplifies thermal jitter as happily as quantum slack — so sensitivity
arguments establish possibility, never actuality. Whether any
biological mechanism exploits the licensed asymmetry is a genuinely
open empirical question, this list's deepest entry, and the book's
claims are built to survive either answer: the ledger of Parts II-V
measures apparent non-determinism relative to observers, and that
quantity exists and is stolen regardless of which microphysics feeds
it.

## §5. The oldest question

Untouched by any theorem in this book: whether the door the physics
left open has anyone walking through it. The staircase and its
ceiling license the possibility this book measures; they do not, and
cannot, certify the tenant. That question stands where it has always
stood — and for the first time in a century, it stands *open*, with
no one entitled to close it by authority.

## §6. The invitation

Every result herein reproduces from the scripts in the repository;
the corpses of the refuted conjectures are in there too, unembalmed.
Check the arithmetic. Break what you can. What survives the attack is
yours to use — that is the entire method, and perhaps the entire hope.

The invitation is not only to people who run scripts. The largest
measurement this book names is in no repository: who holds the
schedule, how much notice comes with it, what one mistake costs at the
bottom of a hierarchy, which records keep plain days and hard days in
one tally. Those are known first by the people living them — a
cashier, a nurse, a line cook, a manager — and they enter the record
when someone asks. So here is the instrument with the mathematics
taken out: five questions that anyone can put to a rule, a bill, a
workplace or a news report. None needs the mathematics. Each is what
the mathematics said to look at.

1. *Who holds the eraser?* Not whether the hours vary: who can change
   them, and on how much notice. (Chapters 7, 13.)
2. *What does one mistake cost here?* One bad month from ruin, a
   person rightly waits to be nearly certain before acting on what
   they know. (Chapter 5.)
3. *One ruler, or two?* Unpredictable is not free, and orderly is not
   fine: ask whose aim the hours serve. (Chapters 4, 7.)
4. *How many heads were there, really?* Three forecasts that began
   from one source are one forecast. (Chapter 11.)
5. *Which tally, and which score?* A record that mixes easy calls with
   hard ones flatters whoever made the easy ones; a remedy scored one
   household at a time has not been scored for the town.
   (Chapters 11, 14.)


# Coda. The Whole Argument, Walked Once

Fifteen chapters is a long walk, and the path turned many times. So
before the appendices, here is the entire argument again — every link
in one chain, each tagged with exactly what holds it, walked from the
particle to the monument without stopping.

**Link one: the staircase, and its ceiling.** Experiments violate
Bell's inequalities; something must give. If what gives is
measurement independence — the assumption that the universe does not
rig the questions to fit the answers — then the relaxation has an
exact minimum price: F = R/(2(R+1)), climbing a staircase with the
number of particles, toward a ceiling it can never reach. **F ≤ 1/2,
at every size, forever.** The universe's statistics never require
more than half of that independence to be given up. Total
determinism-by-conspiracy is never forced. [PROVEN — the published
record this book stands on.]

**Link two: the door is lawful.** Therefore a universe containing
apparent non-determinism — agents whose actions are partly
independent of their circumstances — is not a fantasy tolerated by
physics but a standing possibility priced by it. The sentence "your
freedom is an illusion, physics proved it" is revoked as *authority*;
what remains of it is an opinion, holding a price sheet it rarely
mentions. [PROVEN that the door is open; nothing yet about who walks
through.]

**Link three: congruence, claimed carefully.** Which exit did the
universe take? No one knows, and this book never pretends to. But
notice the asymmetry in what each exit must explain. Your daily
experience — that deliberation does something, that an hour of
thought changes the evening, that people surprise you in ways that
matter — proves nothing by itself. Yet the half-open exit
accommodates that experience at zero cost, while the closed exits
must explain all of it away, every day, in every life. A universe
that took the door is *congruent* with the existence you actually
have — and it is worth saying what that congruence consists of. This
exit requires no influence traveling faster than light. It requires
no endlessly multiplying unobservable worlds. It requires no cosmic
conspiracy reaching into every laboratory, and no daily
explaining-away of the lived experience that deliberation does
something. Every exit from the experiments carries a cost; the other
exits' costs are real but unpriced. This is the only exit whose cost
comes with a receipt — a posted, bounded price, never exceeding one
half. And the receipt has since acquired a property no other exit's
cost possesses: it is *collectible*. The sequel to the staircase
[arXiv:2608.18886] found the surviving local accounts' bill split
between two internal ledgers — measurement dependence and detection —
with an exact exchange rate between them along the solved family, and
posted a laboratory protocol whose outcome bounds that family either
way, an order of magnitude below where the record now leaves it — and
leaves the door's price exactly where Chapter 2 proved it. Not the
cheapest exit — the exits remain unranked, and the
surface prices trade-offs within the surviving accounts, never across
the exits. The only exit under audit. Congruent, priced, and
auditable: not proven, and this book never says otherwise. [FRAMING, not
a theorem.]

**Link four: the promotion.** And here the whole project turns. Once
AND is lawful rather than fanciful, it stops being a topic for
philosophy seminars and becomes a *quantity* — a thing that could be
present in degrees, and therefore measured, and therefore stolen.
Everything before this link was license. Everything after it is
measurement. This is also the answer owed to the second sentence of
Chapter 1: it matters whether you have free will, and this ledger is
the measure of how much. [The hinge — and the reason this book
did not begin measuring until the license was proven.]

**Link five: the two rulers.** Measured how? Not by unpredictability
alone — the harbor taught that. The ferry captain, flawless and
fully written by her timetable; the lost tourist, unreadable and
going nowhere; the sailor, tacking upwind, disagreeing with every
gust and arriving anyway. Freedom is the double score: independence
*and* aim. Every theorem in this book lives on the plane those two
rulers draw. [EXACT definitions; PROVEN fences — the sage ceiling,
the complementarity of what circumstances know.]

**Link six: the anatomy.** On that plane, agency turned out to have
load-bearing structure, none of it guessed in advance and some of it
found in the wreckage of refuted conjectures. The driver at the
darkened intersection: education buys nothing until it beats the
world — a gate, not a slope, sitting exactly at e + s > 1, higher
the more orderly the world. [PROVEN.] Ines at the card table:
perfect unreadability with real winnings exists — a plateau, wider
than this book first printed — and past its edge, tells are the posted
price of winning. [PROVEN; the edge itself OPEN.]
The manager who steals nothing: the cheapest theft of freedom
destroys aim and leaves unpredictability untouched, invisible to
the single ruler of unpredictability; and a stolen hour lands
on the order of a hundred times harder at the bottom of a time budget
than the top. [EXACT.]

**Link seven: the watchers.** Freedom carries a silent subscript —
*from whose seat* — and making it speak produced the strangest exact
result in the book: Theo with his three scores; Ines, inverted by the one
watcher who sees her die; Elias, whose unreadability is one private
conviction and who collapses completely the day it is learned. What
looks like noise may be a hypothesis the watcher doesn't hold — and
privacy is not agency's comfort but its wall. Against watchers with
memory, Vera showed the wall's engineering: it is not how many honest
flips you make, it is whether your flips rule the big choices or only
the details your habits already gave away. [EXACT; the two wirings
the ends of one curve across every world built.]

**Link eight: the towns.** Then freedom went social, and the commons
appeared. Priya, whose honest imperfection lowers her neighbors'
gates while consuming a bite of their ceilings; Aldo, never wrong and
never hidden, beside whom every gate welds and every ceiling falls to
zero. And the nine boats settled the question Aldo raised: nine okay
*readings* beat one excellent reading six-fold, whoever gives the
orders — the protection exponential in independent readings,
annihilated by sameness (nine fishers, one
tutor, exactly one head), dosed by hierarchy (at the printed margin,
one follower of the master: medicine; five: poison), floored by
whatever everyone shares, and insured, at the subsistence line only,
by the wildcard nobody respected; and one more thing counted — a
sage whose record was earned where the answer was easy and spent
where it was hard. [EXACT, every famine probability;
under masters who mislead, readers with bad weeks and shared
blindness the structure held and the headline numbers did not —
SIMULATION.]

**Link nine: the ledger.** A quantity that can be measured and taken
can be booked. Theft — displacement off the frontier or of it — is an
externality in the oldest sense: a real cost, imposed and uncounted,
and what is uncounted is free, and what is free gets taken without
limit. The manager came back with the strongest defense the position
affords — *I priced it in; they agreed* — and left with four answers,
the deepest being that the consent he cited was purchased with the
very currency he took. He was never called evil. He was called
unaudited, the one charge a signature cannot answer. And placed inside
the economists' standard model, with prices free to answer, the
mechanism was carried into the interest rate, not washed out — with
the premises it needs, what a household knows of its own mind and how
its welfare is read, printed beside its conclusions. Asked which
remedy helps, the same model gave opposite answers according to
whether a household's mistakes were counted as stopping at its own
door. [EXACT
instrument; testable parking prediction; NUMERICAL in a standard macro
host, constants the model's; the field audit begun — a survey, a
law, an experiment.]

**Link ten: the monuments.** And when the machine — two axioms, no
morality anywhere in it — was asked what made agents capable and
towns durable, it handed back: education for all; rest for the
overworked, the poorest first; privacy; pluralism; distrust of
concentrated authority; shelter for the stubborn and strange. The
list from the monuments, derived by arithmetic that never read them.
Perhaps morality is the species' compressed memory of theorems it
could not yet write down. The resemblance is no longer unarguable
either way. It has numbers now. [The observation, stated once, and
its printed mismatch beside it.]

That is the chain entire: a ceiling in the statistics of particles;
a door held lawfully open; a quantity promoted from philosophy to
measurement; an anatomy, a wall, a commons, a ledger; and at the end,
arithmetic shaking hands with the monuments. No link claims more
than its tag. Several links were bought with the corpses of assumptions
most readers will bring — corpses buried nowhere — they are in the appendix,
with the scripts, where you can dig them up and check the cause of
death yourself.

The universe declined, at every size priced, to demand the whole of
you. What you do above that floor was never this book's to say. What it cost, who paid, and who took — that, now, is
arithmetic.


---
# APPENDICES

The repository: <https://github.com/RandomInternetPreson/price-of-agency>; this draft, doi:10.5281/zenodo.24599088. Every path printed in this book — `code/`, `docs/`, `figures/`, `design/` — is a path inside it, and a claim is cited by the book's title, its draft number and that address.

A. The theorem file — docs/THEOREMS_v1.md, tags intact.

B. The self-administered referee report — docs/REFEREE_REPORT_v1.md.

C. Reproduction — code/ directory; every figure from a script. One command, `reproduce.py` at the top of the repository, re-runs the scripts and checks each number against the sentence of this book that prints it; its last report is REPRODUCE_REPORT.md.

D. The neighbors' map — docs/PRIOR_ART_MAP_v1.0.md (every citation verified against the record; thirty-four parts inherited, six arrangements the book's, three small results without ancestors). In brief: the agent is Ortega–Braun's bounded-rational one; the aim ruler is Sims's and Tishby–Polani's relevant information; the independence ruler is Shannon's equivocation, measured in the field by Song and colleagues; the frontier is in the spirit of the information bottleneck. Theorem 1 is in the spirit of Conant–Ashby; Theorem 5 of Bayes decision theory and informational cascades; the time gate of Wald and the scarcity literature; the mistake budget of organizational slack. Theorem 6 is Cachin's perfect steganographic security. Chapters 8–9 are Shannon (1949) and Kerckhoffs. Chapter 11 is Condorcet, the correlated-jury theorems, the insurance hypothesis, the ideal free distribution and producer–scrounger games. Part V is Pigou, Coase, Hacker's risk shift, Mas–Pallais, Porter, Beer and Simon, with the bullwhip effect as sibling. Three results found no ancestor — cheap theft as an information statement, noise-subsidized overshoot, and the nonmonotone escape gate — each small, each reproduced in the repository. The moiré mechanism's nearest picture, named in the paper itself, is the *supermeasured* account of Hance, Hossenfelder and Palmer (2022) — measurement dependence living in a non-trivial measure on the hidden variables rather than in a causal link — with Garza and Hance (2025) deriving such a measure for a different model; the mechanism is in that spirit, and whether it is supermeasured in their strict sense is left open there, as here. Chapter 14 §5C's host is the heterogeneous-agent New Keynesian model (Kaplan, Moll and Violante 2018; Auclert, Bardóczy, Rognlie and Straub 2021); the faces of its degraded optimizer are rational inattention (Sims 2003; Matějka and McKay 2015), tunneling (Mullainathan and Shafir 2013), present bias (Laibson 1997) and sparsity (Gabaix 2014); the objection it returns to reduced forms is Lucas's (1976).

E. The physics record: arXiv:2608.00124, v3 (the staircase, proven at every size and certified through n = 22; the ceiling F ≤ 1/2); arXiv:2608.18886, v7 (the exchange-rate surface, the hiding theorem, the protocol, the moiré mechanism and the structure of its floor-attaining census); Zenodo DOIs 10.5281/zenodo.21445609 (staircase) and 10.5281/zenodo.24053426 (CHSH scripts, offset banks, censuses — version 6.0 of the deposit whose concept record is 10.5281/zenodo.23537610). The book cites these versions; earlier versions are superseded on the points listed in docs/PAPER_SYNC_REPORT_v0.23.md.

F. Lexicon — docs/LEXICON_v1.0.md.

G. The stress record — docs/STRESS_CAMPAIGN_v1.0.md (each objection, where it was run, what it did to the claim); docs/RESULTS_STRESS_2026-11-09.md; docs/RESULTS_HANK_v0.1.md and docs/HANK_PREREG_v0.1.md (signs committed before the runs, with the dated addendum).

H. Three rulers, and the assumptions of isolation — docs/RESULTS_THREE_RULERS_2026-11-10.md (the full working behind Chapter 14 §5C's three ways of keeping score); code/joined_three_rulers.py and code/results/joined_three_rulers.md, with the same three scores across the drawn economies (code/rig/hank_port/results_sweep_rulers/, results_two_asset_rulers/); code/two_towns_aid.py, code/duty_trade_exact.py, code/borrowed_record.py, code/stay_ashore.py, code/attack_T22_T23.py; docs/ISOLATION_AUDIT_v1.0.md (each assumption of isolation in the book's models: where a later Part removes it, what changed, and those still assumed).

I. A ruler for one schedule — web/calculator.html. One file, run on the reader's own device and sending nothing. It asks nine questions about a job. It answers how often that job's schedule lets a person be where they planned to be, at a family dinner as much as at a class, and how far two weeks' notice reaches beside a fixed schedule; and, in the model of Chapters 5 and 7, how many of ten thousand people on that schedule finish a course, every class of it, for how many it then changes what they do, and which change helps the most of them. Its counts are the most the schedule allows: the people in it can already pay for the course and chose it well. The model inside it is code/calculator_model.py, which checks itself against Theorems 5b and 16.
