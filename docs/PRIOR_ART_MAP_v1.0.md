# Prior-art map v1.0 — INTEGRATED into v0.17 (2026-10-24)
# Rulings (Aaron): keep every book term; name ancestors as "similar to / in the spirit of" with the difference stated in the same breath — context, never surrender of the term. Ortega–Braun named in Ch 4; Cachin at full strength in Ch 6; ecology named in Ch 11; Hacker in Ch 7; Sen in Ch 11/12.
# Original draft header follows.
#
# Prior-art map — DRAFT FOR AARON'S REVIEW v0.1
# Target: Appendix D (currently "in progress"); closes Ch 15 §4 "the neighbors' map"
# Status: INTEGRATED (see header). Verification in §8.

---

## §0. Polarity of this document (Aaron, 2026-10-24)

The book wants ancestors. Every piece that was already invented is a beam
someone else load-tested; the reader can trust the engine because its
parts are known to work. So the tags run the opposite way from a patent
application:

- **[INHERITED]** — the good outcome. The piece exists in a prior
  literature; the book uses it, names its source, and claims nothing.
- **[CONFIGURATION]** — the pieces are inherited; their *arrangement*
  here is not in the record. Claimed only as arrangement.
- **[NOVEL — cost]** — nothing found. The book pays for this: it must
  defend the result on its own arithmetic. Minimized, not sought.
- **[RENAME?]** — a book coinage has an established name that could
  replace it. Ruling needed each time (gain: credibility; loss: the
  book's own vocabulary and whatever precision the coinage carried).

Divergence sentences are written to be *falsifiable*: a reader who knows
the ancestor should be able to check whether the stated difference is
real.

---

## §1. Foundations: axioms, the policy, the two rulers

### 1.1 Axiom 1 (no one has perfect knowledge) · Axiom 2 (circumstance predicts)
- **Simon (1955), "A behavioral model of rational choice," *QJE*
  69(1):99–118** — bounded rationality (the idea; the term is Simon
  1957, *Models of Man*). **[INHERITED]**
- **Hayek (1945), "The use of knowledge in society," *AER* 35:519** —
  knowledge is dispersed; no center holds it. **[INHERITED]**
- Divergence: none claimed. The axioms are the cheapest premises in the
  record; the book says so (Coda, "axiom load order").

### 1.2 The bounded-rational policy p(a|e,k) ∝ exp(β·P(F=a|e,k))
- **Ortega & Braun (2013), "Thermodynamics as a theory of decision-making
  with information-processing costs," *Proc. R. Soc. A* 469:20120683** —
  softmax/free-energy bounded rationality; β as inverse temperature =
  information-processing resource. **[INHERITED — exactly]**
- **Genewein, Leibfried, Grau-Moya & Braun (2015), "Bounded rationality,
  abstraction, and hierarchical decision-making: an information-theoretic
  optimality principle," *Frontiers in Robotics and AI* 2:27.** **[INHERITED]**
- Divergence: none in the policy. The book's β *is* their resource
  parameter; "time" in Ch 4–7 is the Ortega–Braun processing budget.
  **Action:** the book should say this in Ch 4 §4 in one sentence — it
  converts "our model" into "the standard bounded-rational agent."

### 1.3 The aim ruler, competence = I(A;F)/H(F)
- **Tishby & Polani (2011), "Information theory of decisions and actions,"
  in *Perception-Action Cycle* (Springer), pp. 601–636** — relevant
  information carried from world to action. **[INHERITED]**
- **Sims (2003), "Implications of rational inattention," *J. Monetary
  Econ.* 50:665** — agents pay for I(action; state) under a capacity
  constraint. **[INHERITED — one ruler]**
- Divergence (vs Sims): rational inattention has the aim ruler and no
  independence ruler; it cannot distinguish the ferry captain from the
  sailor. The capacity is an internal parameter, not a stealable resource.

### 1.4 The independence ruler, δ_A = H(A|E)/log₂|𝒜|
- **Song, Qu, Blumm & Barabási (2010), "Limits of predictability in human
  mobility," *Science* 327(5968):1018–1021** — conditional entropy of
  human behavior measured at scale; a ~93% *upper bound* on
  predictability (Fano), not an achieved forecast. **[INHERITED — the
  measurement precedent; field-audit anchor]**
- **Klyubin, Polani & Nehaniv (2005), "Empowerment: a universal
  agent-centric measure of control," *IEEE CEC* 1:128** — agency as a
  channel capacity from actions to future sensations. **[NEIGHBOR, not
  ancestor]**
- Divergence (vs empowerment): empowerment measures influence *over* the
  future; δ_A measures independence *from* circumstance. Orthogonal axes.
- **The pairing (aim × independence) as the definition of agency, and the
  frontier between them: [CONFIGURATION].** Closest relative is the
  information-bottleneck plane (next entry); no source found that places
  conditional-entropy-given-circumstance as the second axis of agency.

### 1.5 The frontier (Ch 6) as a Pareto curve in an information plane
- **Tishby, Pereira & Bialek (1999), "The information bottleneck
  method," *Proc. 37th Allerton Conf.*, 368–377** — trade-off curves
  between two mutual informations; Lagrangian λ. **[INHERITED — the
  genre]**
- Divergence: IB minimizes I(T;X) subject to I(T;Y); the book's frontier
  maximizes I(A;F) subject to a *floor* on H(A|E). It is a reverse /
  entropy-constrained bottleneck, which is why the exact curve is open
  (Ch 15 §2) and why Engine-1-style attacks are the right shape.

---

## §2. The one-agent theorems (Part II)

### 2.1 T1 sage ceiling, T2 complementarity
- **Data-processing inequality** (Cover & Thomas 2006, *Elements of
  Information Theory*, 2nd ed., Thm 2.8.1). T2 is the DPI plus T1's
  equality. **[INHERITED — exactly]**
- **Conant & Ashby (1970), "Every good regulator of a system must be a
  model of that system," *Int. J. Systems Science* 1:89.** T1 in
  cybernetic clothing: a perfectly competent agent's actions must carry
  the environment's information about the future; the sage cannot shed
  I(F;E). **[INHERITED — the reading]**
- **Ashby (1956), *An Introduction to Cybernetics*, ch. 11 (requisite
  variety).** **[INHERITED]**
- Divergence: none. The book should name Conant–Ashby in Ch 4 §3 — it is
  the fifty-year-old version of "the sage ceiling is set by the
  environment, not the agent."

### 2.2 T5 education gate (e* = 1−s), T18 mistake-budget gate, T16 time gate
- **Bayes decision theory** — the gate is a likelihood-ratio threshold;
  T18 is the cost-weighted threshold (asymmetric loss). Standard (e.g.
  Berger 1985, *Statistical Decision Theory and Bayesian Analysis*).
  **[INHERITED — exactly]**
- **Wald (1945), "Sequential tests of statistical hypotheses," *Ann.
  Math. Stat.* 16:117** — SPRT: evidence accumulates until it crosses a
  threshold; T16's time gate ("independence activates only when
  accumulated evidence beats the room") is an SPRT crossing.
  **[INHERITED — the mechanism]**
- **Banerjee (1992), "A simple model of herd behavior," *QJE* 107:797;
  Bikhchandani, Hirshleifer & Welch (1992), "A theory of fads, fashion,
  custom, and cultural change as informational cascades," *JPE*
  100:992.** Rational agents discard their private signal when the
  public signal dominates — the dead zone below the gate is an
  informational cascade, and T12's welded gate (perfectly legible
  competent neighbor) is a cascade in its pure form. **[INHERITED — the
  phenomenon]**
- Divergence (vs cascades): cascade models study the *sequence* of
  decisions and its fragility; the book studies the *threshold's
  location* as a function of the two channels' reliabilities (e + s > 1,
  n-independent) and its displacement by error costs (κ) and by time.
  The gate-as-reliability-race statement is the book's; the behavior
  below it is theirs.
- **[RENAME?]** "welded gate" ↔ "informational cascade." Recommend: keep
  "welded gate" as the book's image, print "informational cascade" in
  the same paragraph as the established name.
- **Mani, Mullainathan, Shafir & Zhao (2013), "Poverty impedes cognitive
  function," *Science* 341:976; Shah, Mullainathan & Shafir (2012), "Some
  consequences of having too little," *Science* 338:682; Mullainathan &
  Shafir (2013), *Scarcity* (Times Books).** The bandwidth tax: the
  optimizer itself is degraded by scarcity. Ancestor of P8, T10(iii),
  T16 time-theft, and the macro divergence claim G1. **[INHERITED — the
  phenomenon, with field evidence]**
- Divergence: scarcity research measures the tax; the book places it in
  an explicit information channel and derives a *gate* (zero-then-jump),
  not a slope, from it. Falsifiable: the field audit either finds the
  gate shape or it doesn't.
- **[RENAME?]** "mistake budget" ↔ **organizational slack** (Cyert &
  March 1963, *A Behavioral Theory of the Firm*; Bourgeois 1981, "On the
  measurement of organizational slack," *AMR* 6:29) and **psychological
  safety** (Edmondson 1999, "Psychological safety and learning behavior
  in work teams," *ASQ* 44:350). Recommend: keep "mistake budget" (it is
  a *ratio* κ, more precise than slack), cite both as the organizational
  literature's names for the resource.

### 2.3 T6 covert plateau, Cor 7.1 cheap theft, P7, the whitening residual
- **Cachin (1998/2004), "An information-theoretic model for
  steganography," *Information Hiding 1998* (LNCS 1525); *Information
  and Computation* 192:41 (2004).** ε-secure steganography: the
  stego-text distribution is within relative entropy ε of the cover
  distribution while carrying payload; *perfectly* secure at ε = 0. T6's
  plateau — δ_A = 1 exactly with aim c₀ > 0 — is the ε = 0 case: the
  aim is the payload, the uniform action distribution is the cover, the
  "whitening residual" is the embedding. (Cachin, Definition 1; the
  plateau is his perfect-security case, which is sharper than
  "indistinguishable.") **[INHERITED — exactly, and this is the most
  valuable single inheritance in the map]**
- **Lampson (1973), "A note on the confinement problem," *CACM* 16:613**
  — covert channels. **[INHERITED — the lineage]**
- **Brunton & Nissenbaum (2015), *Obfuscation: A User's Guide for
  Privacy and Protest* (MIT Press).** Obfuscation as noise-adding
  resistance — Ch 9's additive mixing in civic form. **[INHERITED]**
- Divergence: steganography assumes the warden sees only the channel;
  the book's watcher may buy the coin (T9). "Cheap theft" (Cor 7.1) —
  that the dominant attack on a covert agent is to make its
  unpredictability *useless* rather than *readable* — has no
  steganographic analogue found (the warden wants to detect, not to
  degrade payload utility). **[NOVEL — cost]** Note the ancestor of the
  *phenomenon* is the bandwidth tax (2.2); the information-theoretic
  statement is the book's.
- **4b noise-subsidized overshoot** — raw H(A|E) exceeding the sage
  ceiling as a symptom of error. No source found. **[NOVEL — cost;
  small]** Defended by exact enumeration in the repo.

### 2.4 P8 front-loaded returns, T10 elasticity price list
- Elasticities are standard; the coercer's "derived playbook" is a
  best-response computation. **[INHERITED — method]**
- **Tambe (2011), *Security and Game Theory* (Cambridge UP)** —
  Stackelberg security games: a defender randomizes, an attacker
  observes and best-responds. The theft equilibrium of T10 is this
  structure with agency as the contested resource. **[INHERITED — the
  genre]**
- Divergence: security games price *patrols*; the book prices *attacks
  on the agent's own information resources* (time, education, privacy)
  and finds cheap theft dominant ~10³:1. The dominance ratio is a model
  constant with a passport; the *ordering* is the claim.

---

## §3. Watchers and wirings (Part III)

### 3.1 T9 observer-relativity; surveillance inversion
- **Shannon (1949), "Communication theory of secrecy systems," *Bell
  Syst. Tech. J.* 28:656.** Equivocation H(M|C): unpredictability is
  always *relative to an observer's information*. T9's definition
  δ_A(𝒪) = H(A|𝒪)/log|𝒜| is Shannon's equivocation normalized.
  **[INHERITED — exactly]**
- Divergence: the *inversion* — a surveilled covert agent being more
  predictable than an overt sage (0.291 < 0.753) — follows from the
  plateau's construction (deterministic residual machinery) and has no
  found analogue. **[CONFIGURATION]**
- **Scott (1998), *Seeing Like a State* (Yale UP)** — legibility as the
  state's project. The book's "legible" is Scott's word. **[INHERITED —
  vocabulary]**

### 3.2 T11 sustainable stealth floor; the architecture dichotomy
- **Shannon (1949), perfect secrecy / one-time pad** — T11(iii)'s "at
  h = 3, δ_∞ = δ_A(seed unknown) exactly" is Shannon's perfect-secrecy
  condition: fresh key entropy ≥ message entropy makes the key
  worthless to the observer. The book already calls it "one-time-pad
  equality"; it should cite the source. **[INHERITED — exactly]**
- **Unicity distance (Shannon 1949, §16)** — T11(i)'s "the observer
  extracts the seed within ~10–20 steps" is a unicity-distance
  computation on the habit seed. **[INHERITED — the mechanism]**
- **Kerckhoffs (1883), "La cryptographie militaire," *Journal des
  sciences militaires* 9:5–38 and 161–191** — security must reside in
  the key, not the system (his second principle).
  The architecture dichotomy is Kerckhoffs's principle for behavior:
  *gated* mixing puts the secret in the habit structure (which the
  watcher learns); *additive* mixing puts it in the fresh bits.
  **[INHERITED — the principle]**
- **Dwork, McSherry, Nissim & Smith (2006), "Calibrating noise to
  sensitivity in private data analysis," *TCC 2006* (LNCS 3876)** —
  differential privacy: privacy purchased with calibrated randomness; a
  per-query budget ε is the cousin of the per-action entropy rate h.
  **[INHERITED — the genre]**
- Divergence: cryptography protects a *message* from a passive
  eavesdropper; the book protects a *behavioral stream* from an adaptive
  Bayesian observer who also sees the outcomes. The dichotomy's
  statement — which wiring protects and which surrenders *for
  arbitrary habit structures* — is open (Ch 15 §2) and claimed only on
  the tested class. **[CONFIGURATION]**

---

## §4. Towns (Part IV)

### 4.1 T12 neighbor coupling; P15 submodular erosion
- Informational cascades (2.2). **[INHERITED]**
- **Fujishige (1978), "Polymatroidal dependence structure of a set of
  random variables," *Information and Control* 39:55** — entropy is
  submodular; P15 ("each additional legible neighbor consumes less") is
  submodularity of conditional information. **[INHERITED — exactly]**
- Divergence: the nonmonotone escape gate (partial legibility *opens*
  the gate, perfect legibility welds it) — no source found.
  **[NOVEL — cost; small]**

### 4.2 T13 fishing town: Condorcet exponential, homogeneity collapse, wildcards
- **Condorcet (1785), *Essai sur l'application de l'analyse à la
  probabilité des décisions rendues à la pluralité des voix*.** The
  survival exponential is the Jury Theorem on independent 0.7-fishers.
  **[INHERITED — exactly]**
- **Hong & Page (2004), "Groups of diverse problem solvers can
  outperform groups of high-ability problem solvers," *PNAS* 101:16385.**
  Nine 0.70s beating one 0.80. **[INHERITED]**
- **Hayek (1945)** again — distributed knowledge beats the center.
  **[INHERITED]**
- **Sen (1999), *Development as Freedom* (Knopf), Introduction p. 16;
  ch. 6 "The Importance of Democracy"; ch. 7 "Famines and Other
  Crises"** — verbatim (p. 16): "no famine has ever taken place in the
  history of the world in a functioning democracy."
  The fishing town's *famine* metric and Ch 12's fenced conjecture have
  Sen as their direct ancestor; he should be named in both. **[INHERITED
  — the metric and the thesis of Ch 12]**
- **Yachi & Loreau (1999), "Biodiversity and ecosystem productivity in a
  fluctuating environment: the insurance hypothesis," *PNAS* 96:1463** —
  diversity as insurance against environmental variance. T13(iv)
  wildcard insurance is the insurance hypothesis with fishers as
  species. **[INHERITED — exactly; and from the author's own first
  field]**
- **Elmqvist et al. (2003), "Response diversity, ecosystem change, and
  resilience," *Frontiers in Ecology and the Environment* 1:488** —
  response diversity: resilience comes from members that respond
  *differently* to the same shock. T13(ii)'s homogeneity collapse is
  the loss of response diversity. **[INHERITED]**
- **[RENAME?]** "wildcard insurance" ↔ "the insurance hypothesis."
  Recommend: keep "wildcard" as the character, cite Yachi–Loreau as the
  theorem's name in ecology.
- Divergence: the *homogeneity collapse to N_eff = 1 exactly* and the
  *nonmonotone centralization dose-response* (beneficial dip at one
  follower, poison at bloc majority) are computed structures not found
  in the jury-theorem literature, which studies correlation (next entry)
  rather than shared-source identity. **[CONFIGURATION]**

### 4.3 T14 correlation floor; scale tax
- **Ladha (1992), "The Condorcet Jury Theorem, free speech, and
  correlated votes," *AJPS* 36:617; Boland (1989), "Majority systems and
  the Condorcet jury theorem," *The Statistician* 38:181; Berg (1993),
  "Condorcet's jury theorem, dependency among jurors," *Social Choice
  and Welfare* 10:87.** Correlated voters degrade the jury theorem to a
  floor set by the correlation. T14(i)–(ii) is this result in the
  streak-Markov survival metric. **[INHERITED — exactly]**
- **Tumer & Ghosh (1996), "Error correlation and error reduction in
  ensemble classifiers," *Connection Science* 8:385; Krogh & Vedelsby
  (1995), "Neural network ensembles, cross validation, and active
  learning," *NIPS* 7.** Ensemble error floors under member correlation
  — the same theorem in machine learning. **[INHERITED]**
- **Markowitz (1952), "Portfolio selection," *J. Finance* 7:77; Sharpe
  (1964), "Capital asset prices," *J. Finance* 19:425** — undiversifiable
  (systematic) risk. Already flagged in THEOREMS as the echo. **[INHERITED]**
- Divergence: the *scale tax* framing (the same ρ costs 1.3× at N = 9
  and 16× at N = 31 — larger societies are bounded by correlation more
  than size) is the book's way of reading a known floor; the number is a
  passport, the direction is standard. **[INHERITED — reading ours]**

### 4.4 S1 the living town: observation locks the herd; finite fish convert it
- **Fretwell & Lucas (1969), "On territorial behavior and other factors
  influencing habitat distribution in birds. I. Theoretical
  development," *Acta Biotheoretica* 19(1):16–36** — the ideal free
  distribution: foragers spread until intake
  equalizes across patches. S1(ii)'s "crowded correct followers split
  nine ways" is an IFD. **[INHERITED — exactly]**
- **Barnard & Sibly (1981), "Producers and scroungers: a general model
  and its application to captive flocks of house sparrows," *Animal
  Behaviour* 29:543** — producer–scrounger games have an *interior*,
  frequency-dependent equilibrium mix. S1(ii)'s persistent ~0.5
  hub-following equilibrium is a producer–scrounger equilibrium with
  the hub as producer. **[INHERITED — exactly]**
- **Arthur (1994), "Inductive reasoning and bounded rationality," *AER
  P&P* 84:406** (El Farol); **Challet & Zhang (1997), "Emergence of
  cooperation and organization in an evolutionary game," *Physica A*
  246:407** (minority game) — crowding cost punishes shared predictors
  and forces heterogeneity. S1(i)–(ii) together. **[INHERITED]**
- Divergence: the *glass sea* — zero crowding cost removes the only
  endogenous decorrelating force, leaving T14's floor uncorrected — is
  an interpretation on simulation, tagged as such in the book. The
  contrapositive of El Farol. **[CONFIGURATION — interpretation]**
- **Action:** these three are from the author's own field and should
  be named in Ch 11 Lesson Six; they turn "our simulation found" into
  "ecology has known since 1969."

---

## §5. The ledger (Part V)

### 5.1 Externality framing; the manager's defense
- **Pigou (1920), *The Economics of Welfare* (Macmillan)** —
  externalities; unpriced costs land on third parties. **[INHERITED]**
- **Coase (1960), "The problem of social cost," *J. Law & Econ.* 3:1** —
  the manager's "willing seller met a willing buyer." The book's fourth
  answer (private prices cannot settle public costs) is Coase's own
  transaction-cost caveat, not a refutation of him. **[INHERITED —
  including the defense]**
- **Hacker (2006), *The Great Risk Shift* (Oxford UP)** — variance
  transferred from institutions to households over three decades. This
  is **stochasticity transfer**, named and documented in economics
  before the book. **[INHERITED — the phenomenon; must be cited in Ch 7
  and Ch 13]**
- **[RENAME?]** "stochasticity transfer" ↔ "risk shift." Recommend:
  keep the book's term (it is defined on variance *channels* and
  applies inside a firm, not only to households' financial risk), and
  introduce it as "what Hacker called the risk shift, generalized."
- **Mas & Pallais (2017), "Valuing alternative work arrangements,"
  *AER* 107(12):3722–3759** — in a discrete-choice hiring experiment,
  the average worker gives up ~20% of wages to avoid an employer-set
  schedule on one week's notice. This is *experimental willingness to
  pay*, not observed market wages: the paper establishes that the
  schedule is a cost workers would pay to remove; it does **not**
  establish whether wages actually compensate it. That second question
  is exactly the parking prediction's open column. **[INHERITED — the
  valuation; the audit stays owed]** (Verification caught my draft
  overstating this; the manager's defense has *not* "already lost on
  data" — it has been priced by the workers and not yet checked against
  payroll.)
- **Schneider & Harknett (2019), "Consequences of routine work-schedule
  instability for worker health and well-being," *American Sociological
  Review* 84:82** — the Shift Project's flagship. **[INHERITED — the
  dataset and its first findings]**
- **Goodhart (1975), "Problems of monetary management: the U.K.
  experience," in *Papers in Monetary Economics* vol. I (Reserve Bank
  of Australia; reprinted in Goodhart 1984, *Monetary Theory and
  Practice*, Macmillan, pp. 91–121); Campbell (1979), "Assessing the
  impact of planned social change," *Evaluation and Program Planning*
  2(1):67–90 (the law is stated p. 85)** — metric gaming. Ancestor of the Ch 13 §4 inoculation queued in TASKS.
  **[INHERITED]**
- **Porter (1995), *Trust in Numbers* (Princeton UP)** — quantification
  arises where trust is absent; the Part V thesis ("domains believed
  subjective get governed by power instead of measurement") is Porter's
  thesis run forward. **[INHERITED — the thesis law has an ancestor]**

### 5.2 T17 the ledger of imposition (cascade)
- **Beer (1972), *Brain of the Firm* (Allen Lane); Beer (1979), *The
  Heart of Enterprise* (Wiley)** — the Viable System Model (1972); the
  explicit variety-engineering vocabulary — attenuators and amplifiers
  between recursion levels — is developed in 1979. T17's
  absorb-to-capacity-then-broadcast is Beer's variety engineering.
  **[INHERITED — the mechanism; cite both]**
- **Simon (1962), "The architecture of complexity," *Proc. Am. Phil.
  Soc.* 106:467** — hierarchy as near-decomposable variance structure.
  **[INHERITED]**
- **Lee, Padmanabhan & Whang (1997), "Information distortion in a supply
  chain: the bullwhip effect," *Management Science* 43:546; Forrester
  (1961), *Industrial Dynamics* (MIT Press)** — variance amplification
  along a chain. **[SIBLING — direction differs]**
- Divergence (vs bullwhip): the bullwhip amplifies demand variance
  *upstream* through ordering; T17 broadcasts unabsorbed variance
  *downstream* through authority, multiplied by branching. Same algebra,
  opposite direction, different channel; the 93.4% bottom-share is a
  passported constant.
- **[CONFIGURATION]** for the cascade; **[INHERITED]** for every part.

### 5.3 Ch 14 six rules
- **Edmondson (1999)** — environments that permit mistakes (Rule: floor
  the mistake budget). **[INHERITED]**
- **Hayek (1945), Sen (1999), Yachi–Loreau (1999)** — subtract sameness.
  **[INHERITED]**
- Rules are derived from the theorems; their ancestors are the theorems'
  ancestors. No rule is claimed as new policy.

### 5.4 Ch 12 fenced conjecture (democracy as convergent discovery)
- **Sen (1999)**; **Condorcet (1785)**; **Ladha (1992)**. The conjecture
  is the jury theorem with correlation, read as a survival filter. The
  fence stays. **[INHERITED — the shape; conjecture ours]**

### 5.5 The law's own exhibit (hiding theorem analogue)
- Own lineage (arXiv:2608.18886). Not prior art; recorded here only so
  Appendix D is complete.

---

## §6. Credibility ledger (the count)

| Tag | Entries |
|---|---|
| INHERITED (exactly or the mechanism) | 34 |
| CONFIGURATION (parts inherited, arrangement ours) | 6 |
| NOVEL — cost | 3 (cheap theft as information-theoretic statement; overshoot; nonmonotone escape gate) |
| RENAME? rulings | 5 (welded gate / cascade; mistake budget / slack; wildcard / insurance hypothesis; stochasticity transfer / risk shift; — plus "legible" already Scott's) |

Reading: the engine is almost entirely built from parts with names.
The three NOVEL entries are each small, each defended by exact
enumeration in the repo, and none is load-bearing for Part V.

---

## §7. Sentences in the manuscript that this map changes

- **Ch 15 §4 "the configuration is ours"** — survives, with the map as
  its receipt.
- **Ch 2 l.167 "does something no result in this lineage had done
  before"** — true as written (within the lineage); untouched.
- **Ch 4 §4** — add one sentence naming Ortega–Braun for the policy.
- **Ch 4 §3** — add Conant–Ashby to the sage-ceiling reading.
- **Ch 5** — add "informational cascade" beside "dead zone"; add the
  scarcity literature beside the time gate.
- **Ch 6** — add Cachin: the plateau *is* steganographic capacity.
- **Ch 7 / Ch 13** — add Hacker's risk shift where stochasticity
  transfer is introduced; add Mas–Pallais to the manager's defense *as
  the workers' own price for the schedule* (experimental WTP), with the
  payroll check left to the audit — never as "already lost on data."
- **Ch 9** — cite Shannon for "one-time-pad equality"; Kerckhoffs for
  the dichotomy.
- **Ch 11** — Condorcet, Ladha, Yachi–Loreau, Fretwell–Lucas,
  Barnard–Sibly, Sen.
- **Ch 13 §2B** — Beer / Simon for the cascade; bullwhip as sibling with
  direction stated.
- **Part V intro** — Porter for the thesis law.
- **Appendix D** — becomes this document, condensed to book register.

Each is one sentence or a parenthetical; none changes a result.

---

## §8. Verification status (2026-10-24)

Every citation above was checked by three independent passes against
DOI/Crossref records, publisher pages, or the primary text, for (a)
existence, (b) authors/year/venue/pages, (c) whether the work says what
is attributed to it.

**52 citations: 52 found; 0 unverified; 0 attributions wrong at the
level of the result.** Corrections folded in above:

| Item | What changed |
|---|---|
| Mas & Pallais 2017 | **Substantive.** The paper is an experiment measuring willingness-to-pay (~20% of wages to avoid employer-set schedules); it does *not* measure observed wage differentials. My draft's "actual jobs show little compensating differential" was wrong and is removed. The manager's defense has been priced by workers, not yet checked against payroll — which is the parking prediction, still owed. |
| Sen 1999 | My quotation was a hybrid of two passages; now verbatim (Intro p. 16) with ch. 6/7 named. |
| Cachin 1998/2004 | ε-security is bounded relative entropy; exact indistinguishability only at ε = 0 — which is the plateau's case. Inheritance sharpened, not weakened. |
| Shannon 1949 | Unicity distance confirmed in the paper (§14); perfect secrecy §10; equivocation §11–12. |
| Song et al. 2010 | 93% is an upper bound on predictability, not achieved accuracy. |
| Goodhart 1975 | Proper source: RBA *Papers in Monetary Economics* vol. I (1975/76), reprinted 1984. |
| Beer 1972 | Variety-engineering vocabulary is mainly *Heart of Enterprise* (1979); cite both. |
| Fretwell & Lucas 1969 | Title spelling ("behavior") and subtitle; pp. 16–36. |
| Kerckhoffs 1883 | Two-part pagination (5–38, 161–191). |
| Simon 1955 | Idea 1955; the term "bounded rationality" is 1957. |
| Mani et al. 2013 / Shah et al. 2012 | "Bandwidth tax" is the *Scarcity* book's term, not the papers'; the ~13-IQ-point figure is the authors' own gloss, not in the abstract. Attribute accordingly. |
| Dwork et al. 2006 | Paper defines ε-indistinguishability; the name "differential privacy" and "privacy budget" are later Dwork papers. Substance correct. |
| Pigou 1920 | Frames it as marginal social vs private net product; never uses the word "externality." |
| Tishby & Polani 2011 | "Relevant information" is a component; the chapter's headline construct is "information-to-go." |
| Ladha 1992 | Correlation *degrades* (bounded-correlation survival), does not destroy. Map wording already says degrade. |
| Tambe 2011 | Print 2011, ©2012; either defensible. |
| Berger 1985 | Standard content; section pinpoint still to add at integration. |
| Sen ch. 6 page | Chapter solid; p. ~152 from memory — check against edition at integration. |

---

## §9. Rulings needed from Aaron

1. The five RENAME? entries — keep the book's term + cite, or adopt the
   established name outright? (My default: keep + cite, every time.)
2. Steganography (2.3): print Cachin in Ch 6 at full strength ("the
   plateau is steganographic capacity") — this is the single biggest
   credibility gain in the map, and it costs the book nothing.
3. Ecology (4.2, 4.4): name Yachi–Loreau, Fretwell–Lucas, Barnard–Sibly
   in Ch 11 — your first field; the book currently doesn't say so.
4. Hacker's risk shift (5.1): cite in Ch 7 where stochasticity transfer
   is introduced, as the economics name for the phenomenon?
5. Sen (4.2): the famine metric and Ch 12 both owe him a sentence.
6. Any ancestor you know of that I missed — your private lexicon and
   the Gemini debates may hold names.
