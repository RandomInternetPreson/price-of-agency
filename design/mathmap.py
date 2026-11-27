"""mathmap.py -- where the manuscript's plain-text formulas are, and how each is set as mathematics.

The markdown manuscript writes formulas in Unicode ("δ_A = H(A|E) / log₂|A|") so that it reads anywhere. The designed edition
sets them as mathematics. This file is the whole translation: DISPLAY for the indented formula blocks, SPECIFIC for expressions
inside prose (each must be found exactly once in its chapter, so a change to the manuscript fails loudly here instead of
silently printing an untranslated formula), and GLOBAL for symbols that mean one thing everywhere.

No entry changes a word of prose."""

# ---- the indented formula blocks, by their exact text -----------------------------------------------------------------------
DISPLAY = [
 ("F = R / (2(R + 1)),   where R doubles with every second particle.",
  r"F = \frac{R}{2(R+1)}, \qquad \text{where } R \text{ doubles with every second particle.}"),
 ("δ_A = H(A|E) / log₂|A|", r"\delta_A = \frac{H(A \mid E)}{\log_2 |A|}"),
 ("aim = I(A;F) / H(F)", r"\text{aim} = \frac{I(A;F)}{H(F)}"),
 ("δ_A(sage) = H(F|E) / log₂|A| .", r"\delta_A(\text{sage}) = \frac{H(F \mid E)}{\log_2 |A|}\,."),
 ("e* = 1 − s", r"e^{\ast} = 1 - s"),
 ("e*(κ) / (1 − e*(κ)) = κ(1−s)/s + (κ−1)(1 − 1/n),", r"\frac{e^{\ast}(\kappa)}{1 - e^{\ast}(\kappa)} \;=\; \frac{\kappa(1-s)}{s} + (\kappa - 1)\Bigl(1 - \frac{1}{n}\Bigr),"),
 ("follow K  ⟺  κ·[1 + n·(1−s)/s + n − 2]  <  1 + n·e/(1−e) + n − 2\n"
  "          ⟺  e/(1−e)  >  κ·(1−s)/s + (κ−1)(1 − 1/n).",
  r"\begin{aligned}\text{follow } K \;&\Longleftrightarrow\; \kappa\Bigl[1 + \frac{n\,(1-s)}{s} + n - 2\Bigr] \;<\; 1 + \frac{n\,e}{1-e} + n - 2\\[4pt]"
  r"&\Longleftrightarrow\; \frac{e}{1-e} \;>\; \frac{\kappa(1-s)}{s} + (\kappa - 1)\Bigl(1 - \frac{1}{n}\Bigr).\end{aligned}"),
 ("follow K  ⟺  [e + (1−e)/n] / [(1−e)/n]  >  [(1−s) + s/n] / [s/n]\n"
  "          ⟺  n·e/(1−e)  >  n·(1−s)/s\n"
  "          ⟺  e·s > (1−s)(1−e)\n"
  "          ⟺  e + s > 1.",
  r"\begin{aligned}\text{follow } K \;&\Longleftrightarrow\; \frac{e + (1-e)/n}{(1-e)/n} \;>\; \frac{(1-s) + s/n}{s/n}\\[4pt]"
  r"&\Longleftrightarrow\; \frac{n\,e}{1-e} \;>\; \frac{n\,(1-s)}{s}\\[4pt]"
  r"&\Longleftrightarrow\; e\,s > (1-s)(1-e)\\[4pt]"
  r"&\Longleftrightarrow\; e + s > 1.\end{aligned}"),
 ("e*  =  (q_max − q_k) / (q_max + (n−1)·q_k),", r"e^{\ast} = \frac{q_{\max} - q_k}{q_{\max} + (n-1)\,q_k},"),
 ("frontier = the maximal achievable pairs (aim, δ_A).", r"\text{frontier} = \text{the maximal achievable pairs } (\text{aim}, \delta_A)."),
 ("λ* = 1 / (n(1−s) + s)", r"\lambda^{\ast} = \frac{1}{n(1-s) + s}"),
 ("c₀ = 1 − h_n( s + (1−s)/n ) / log₂ n ,", r"c_0 = 1 - \frac{h_n\bigl(s + (1-s)/n\bigr)}{\log_2 n}\,,"),
 ("I(A;F | E)  ≤  H(A | E, R)  ≤  H(F | E).", r"I(A;F \mid E) \;\le\; H(A \mid E, R) \;\le\; H(F \mid E)."),
 ("δ_A(𝒪) = H(A | 𝒪) / log₂|A| —", r"\delta_A(\mathcal{O}) = \frac{H(A \mid \mathcal{O})}{\log_2 |A|} \;\;\text{---}"),
 # Chapter 13 §2B, the cascade
 ("v₁ = V,     v_(l+1) = v_l − min(v_l, c_l),     loss per person = ε_l · v_l",
  r"v_1 = V, \qquad v_{l+1} = v_l - \min(v_l, c_l), \qquad \text{loss per person} = \varepsilon_l\, v_l"),
 # Chapter 14 §5C, the bandwidth block
 ("x = 1 − b/3,     κ(b) = κ₀ + κ₁·x,     β(b) = β·(1 − τ·x)",
  r"x = 1 - \frac{b}{3}, \qquad \kappa(b) = \kappa_0 + \kappa_1 x, \qquad \beta(b) = \beta\,(1 - \tau x)"),
 ("P(rise) = p↑  if  T̄ − N ≥ T_gate,  otherwise 0\n"
  "P(fall) = 1 − (1 − S·ω)(1 − d·[cash on hand < m])",
  r"\begin{aligned}P(\text{rise}) &= p_{\uparrow} \;\text{ if }\; \bar{T} - N \ge T_{\mathrm{gate}}, \;\text{ otherwise } 0\\[4pt]"
  r"P(\text{fall}) &= 1 - (1 - S\omega)\bigl(1 - d\,[\text{cash on hand} < m]\bigr)\end{aligned}"),
]

# ---- expressions inside prose: (chapter key, exact manuscript text, replacement) ---------------------------------------------
# A space in the manuscript text matches any run of whitespace, so line wrapping does not matter.
SPECIFIC = [
 # the formal passages of v0.44: single letters set as mathematics
 ("ch13", "Uncertainty V arrives at the top. A person at level l faces", "Uncertainty $V$ arrives at the top. A person at level $l$ faces"),
 ("ch14", "is its bandwidth b, one of four levels", "is its bandwidth $b$, one of four levels"),
 ("ch14", "Write x for the depleted share", "Write $x$ for the depleted share"),
 ("ch14", "N is hours worked,", "$N$ is hours worked,"),
 ("ch14", "S the schedule entropy set on the firm's side,", "$S$ the schedule entropy set on the firm's side,"),
 ("ch14", "as if b were permanent", "as if $b$ were permanent"),
 ("ch14", "by skill (ω) |", r"by skill ($\omega$) |"),
 ("ch14", "Schedule entropy (S) |", "Schedule entropy ($S$) |"),
 ("ch14", "applies (d, m) |", "applies ($d$, $m$) |"),
 # Chapter 2
 ("ch2", "precisely (√2 − 1)/3 — about", r"precisely $(\sqrt{2}-1)/3$ — about"),
 # Chapter 4
 ("ch4", "*entropy*, written H.", "*entropy*, written $H$."),
 ("ch4", "Let A be the action taken and E the circumstances an observer sees. H(A|E) counts the observer's remaining doubt about A *after* seeing E.",
         r"Let $A$ be the action taken and $E$ the circumstances an observer sees. $H(A \mid E)$ counts the observer's remaining doubt about $A$ *after* seeing $E$."),
 ("ch4", "(log₂ of the number of possible actions)", r"($\log_2$ of the number of possible actions)"),
 ("ch4", "δ_A = 0: the captain — circumstances leave no doubt. δ_A = 1: the tourist", r"$\delta_A = 0$: the captain — circumstances leave no doubt. $\delta_A = 1$: the tourist"),
 ("ch4", "Let F be the future the agent is steering toward", "Let $F$ be the future the agent is steering toward"),
 ("ch4", "F is exogenous to A everywhere", "$F$ is exogenous to $A$ everywhere"),
 ("ch4", "written I(A;F), the number of bits of doubt about F that watching A removes", "written $I(A;F)$, the number of bits of doubt about $F$ that watching $A$ removes"),
 ("ch4", "The tourist: δ_A = 1, aim = 0. The captain in fair weather: δ_A = 0, aim = 1.", r"The tourist: $\delta_A = 1$, aim $= 0$. The captain in fair weather: $\delta_A = 0$, aim $= 1$."),
 ("ch4", "For an agent with full knowledge of F and ample deliberation, the acted policy is A = F, so H(A|E) = H(F|E), and",
         r"For an agent with full knowledge of $F$ and ample deliberation, the acted policy is $A = F$, so $H(A \mid E) = H(F \mid E)$, and"),
 ("ch4", "H(F) = H(F|E) + I(F;E): the second term", r"$H(F) = H(F \mid E) \allowbreak + I(F;E)$: the second term"),
 ("ch4", "a future F with n equally likely possibilities; an environment signal that reveals F with probability 1−s; a knowledge signal that reveals F with probability e;",
         "a future $F$ with $n$ equally likely possibilities; an environment signal that reveals $F$ with probability $1-s$; a knowledge signal that reveals $F$ with probability $e$;"),
 ("ch4", "in place of I(A;F), the two", "in place of $I(A;F)$, the two"),
 # Chapter 5
 ("ch5", "with environment reliability 1−s and education fidelity e, a rational agent's independence δ_A is exactly zero whenever e < 1−s, and strictly positive whenever e > 1−s.",
         r"with environment reliability $1-s$ and education fidelity $e$, a rational agent's independence $\delta_A$ is exactly zero whenever $e < 1-s$, and strictly positive whenever $e > 1-s$."),
 ("ch5", "Let a self-directed mistake cost κ times a conformist one", r"Let a self-directed mistake cost $\kappa$ times a conformist one"),
 ("ch5", "*recovering e\\* = 1−s exactly at κ = 1 and rising with κ.* The second", r"*recovering $e^{\ast} = 1-s$ exactly at $\kappa = 1$ and rising with $\kappa$.* The second"),
 ("ch5", "proportion 1 + n·(1−s)/s to 1 + n·e/(1−e) to n − 2.", r"proportion $1 + n(1-s)/s$ to $1 + n\,e/(1-e)$ to $n - 2$."),
 ("ch5", "doubt: δ_A = 0, the rock.", r"doubt: $\delta_A = 0$, the rock."),
 ("ch5", "doubt is maximal: δ_A = 1. (Formally: δ_A = H(A|E) / log₂|A|, the conditional entropy of action given environment, scaled to [0,1].)",
         r"doubt is maximal: $\delta_A = 1$. (Formally: $\delta_A = H(A \mid E)/\log_2 |A|$, the conditional entropy of action given environment, scaled to $[0,1]$.)"),
 ("ch5", "Your environment E points at your future correctly with probability (1−s) + s/n —", "Your environment $E$ points at your future correctly with probability $(1-s) + s/n$ —"),
 ("ch5", "Your education K points correctly with probability e + (1−e)/n.", "Your education $K$ points correctly with probability $e + (1-e)/n$."),
 ("ch5", "Notice the alphabet size n cancels", "Notice the alphabet size $n$ cancels"),
 ("ch5", "Below the gate the agent follows E everywhere (δ_A = 0 identically);", r"Below the gate the agent follows $E$ everywhere ($\delta_A = 0$ identically);"),
 ("ch5", "A future F: one of n possibilities, all equally likely. An environment signal E: reveals F with probability 1−s, otherwise says something uniformly random. An education signal K: reveals F with probability e, otherwise uniformly random, independent of E given F.",
         "A future $F$: one of $n$ possibilities, all equally likely. An environment signal $E$: reveals $F$ with probability $1-s$, otherwise says something uniformly random. An education signal $K$: reveals $F$ with probability $e$, otherwise uniformly random, independent of $E$ given $F$."),
 ("ch5", "Bayesian posterior over F, and acts on it", "Bayesian posterior over $F$, and acts on it"),
 ("ch5", "formula e* = 1−s is proven", r"formula $e^{\ast} = 1-s$ is proven"),
 ("ch5", "the gate at n = 16, 32, 64:", "the gate at $n = 16, 32, 64$:"),
 # Chapter 6
 ("ch6", "The agent knows its target F and sees its circumstances E. It follows F with a fixed probability λ, and with probability 1−λ draws its action from a *compensating* distribution r_E — chosen, for each circumstance E, so that the overall action pattern given E is exactly uniform",
         r"The agent knows its target $F$ and sees its circumstances $E$. It follows $F$ with a fixed probability $\lambda$, and with probability $1-\lambda$ draws its action from a *compensating* distribution $r_E$ — chosen, for each circumstance $E$, so that the overall action pattern given $E$ is exactly uniform"),
 ("ch6", "where n is the number of options and 1−s the environment's reliability. Up to λ\\*, δ_A = 1 identically while aim grows with λ. Past λ\\*, *this*",
         r"where $n$ is the number of options and $1-s$ the environment's reliability. Up to $\lambda^{\ast}$, $\delta_A = 1$ identically while aim grows with $\lambda$. Past $\lambda^{\ast}$, *this*"),
 ("ch6", "the agent's pull toward F exceeds", "the agent's pull toward $F$ exceeds"),
 ("ch6", "Let the agent act on F exactly when the environment is wrong (F ≠ E),", r"Let the agent act on $F$ exactly when the environment is wrong ($F \ne E$),"),
 ("ch6", "the environment's own answer with probability q, each other action with the remainder spread evenly. Choosing q so the action pattern given E is exactly uniform gives q = λ* — the same constant — and δ_A = 1 exactly with aim",
         r"the environment's own answer with probability $q$, each other action with the remainder spread evenly. Choosing $q$ so the action pattern given $E$ is exactly uniform gives $q = \lambda^{\ast}$ — the same constant — and $\delta_A = 1$ exactly with aim"),
 ("ch6", "where h_n(m) is the entropy of a row whose favored entry has probability m.", "where $h_n(m)$ is the entropy of a row whose favored entry has probability $m$."),
 ("ch6", "equivalently, c₀ at noise s equals one minus the sage's independence at noise 1−s.)", "equivalently, $c_0$ at noise $s$ equals one minus the sage's independence at noise $1-s$.)"),
 ("ch6", "1 − 1/log₂3 ≈ 0.369, and at four, where the best strategy found, (5 log₂5 + 9 log₂3 − 6)/64 ≈ 0.3105, is certified",
         r"$1 - 1/\log_2 3 \approx 0.369$, and at four, where the best strategy found, $(5\log_2 5 + 9\log_2 3 - 6)/64 \approx 0.3105$, is certified"),
 ("ch6", "δ_A = H(F|E)/log₂|A| < 1. The frontier therefore runs from the plateau's right edge (aim ≥ c₀, δ_A = 1) down to the sage point (aim = 1, δ_A = the ceiling)",
         r"$\delta_A \allowbreak = H(F \mid E)/\log_2 |A| < 1$. The frontier therefore runs from the plateau's right edge (aim $\ge c_0$, $\delta_A = 1$) down to the sage point (aim $= 1$, $\delta_A =$ the ceiling)"),
 # Chapter 7
 ("ch7", "Near the gate e* = 1−s of Chapter 5", r"Near the gate $e^{\ast} = 1-s$ of Chapter 5"),
 ("ch7", "time, dQ/dt = ε·Q/t, differs", r"time, $dQ/dt = \varepsilon\,Q/t$, differs"),
 ("ch7", "with accumulated thought standing in for e.", "with accumulated thought standing in for $e$."),
 # Chapter 8
 ("ch8", "All of Chapters 4–7 used 𝒪 = circumstances;", r"All of Chapters 4–7 used $\mathcal{O} =$ circumstances;"),
 ("ch8", "since λ ≤ λ* is small", r"since $\lambda \le \lambda^{\ast}$ is small"),
 ("ch8", "Result: δ_A({circumstances, die}) = 0.29", r"Result: $\delta_A(\{\text{circumstances, die}\}) = 0.29$"),
 # Chapter 9
 ("ch9", "habit — h ≥ log₂ (number of habits). Three is log₂ 8,", r"habit — $h \ge \log_2(\text{number of habits})$. Three is $\log_2 8$,"),
 ("ch9", "varies by 0.0015 across h in every", "varies by 0.0015 across $h$ in every"),
 ("ch9", "universal for fine habits, at every h.*", "universal for fine habits, at every $h$.*"),
 ("ch9", "rule with k hidden bits whose", "rule with $k$ hidden bits whose"),
 ("ch9", "acquire those k bits within", "acquire those $k$ bits within"),
 ("ch9", "Freshness, measured: h = honest flips per decision.", "Freshness, measured: $h =$ honest flips per decision."),
 ("ch9", "the three is log₂ 8, as", r"the three is $\log_2 8$, as"),
 ("ch9", "Inside the mathematics, h is simply given.", "Inside the mathematics, $h$ is simply given."),
 # Chapter 10
 ("ch10", "becomes 𝒪 = (your signals, their action),", r"becomes $\mathcal{O} =$ (your signals, their action),"),
 # Chapter 11
 ("ch11", "beside a private reading right with probability p, one signal all can see, right with probability a. A fisher who reasons correctly follows the public signal against a disagreeing reading exactly when a > p — and then the whole fleet sails on one signal. Whenever a lies above",
          "beside a private reading right with probability $p$, one signal all can see, right with probability $a$. A fisher who reasons correctly follows the public signal against a disagreeing reading exactly when $a > p$ — and then the whole fleet sails on one signal. Whenever $a$ lies above"),
 ("ch11", "weighs a(1 − p) against (1 − a)p, and follows the signal exactly when a > p.", "weighs $a(1-p)$ against $(1-a)p$, and follows the signal exactly when $a > p$."),
 ("ch11", "town fails on the days the signal fails, 1 − a, where", "town fails on the days the signal fails, $1-a$, where"),
 ("ch11", "with probability ρ, so a = ρ + (1 − ρ)/4. Below ρ = 0.6 nobody", r"with probability $\rho$, so $a = \rho + (1-\rho)/4$. Below $\rho = 0.6$ nobody"),
 ("ch11", "reading pays 0.218 V against following's 0.086 V, and", r"reading pays $0.218\,V$ against following's $0.086\,V$, and"),
 ("ch11", "reading pays 0.70·(0.80·V/9 + 0.20·V) against following's 0.80·V/9 — 0.202 V against 0.089 V in the printed town",
          r"reading pays $0.70\,(0.80\,V/9 + 0.20\,V)$ against following's $0.80\,V/9$ — $0.202\,V$ against $0.089\,V$ in the printed town"),
 ("ch11", "(0.104 V against 0.089 V at full pooling)", r"($0.104\,V$ against $0.089\,V$ at full pooling)"),
 # Chapter 13
 ("ch13", "conditional on E.)", "conditional on $E$.)"),
 ("ch13", "H(A|E)/log|A| and aim I(A;F)/H(F) (Chapter 4)", r"$H(A \mid E)/\log |A|$ and aim $I(A;F)/H(F)$ (Chapter 4)"),
 # Chapter 15
 ("ch15", "the edge is exactly 1 − 1/log₂3 ≈ 0.369 —", r"the edge is exactly $1 - 1/\log_2 3 \approx 0.369$ —"),
 ("ch15", "(5 log₂5 + 9 log₂3 − 6)/64 ≈ 0.31054,", r"$(5\log_2 5 + 9\log_2 3 - 6)/64 \approx 0.31054$,"),
 ("ch15", "signal, e* = (q_max − q_k)/(q_max + (n−1) q_k), by", r"signal, $e^{\ast} = (q_{\max} - q_k)/(q_{\max} + (n-1)\,q_k)$, by"),
 ("ch15", "at every h (Theorem", "at every $h$ (Theorem"),
 # Coda, appendices
 ("coda", "exact minimum price: F = R/(2(R+1)), climbing", "exact minimum price: $F = R/(2(R+1))$, climbing"),
 ("appx", "certified through n = 22;", "certified through $n = 22$;"),
]

# ---- symbols that mean one thing everywhere: (regular expression, replacement), applied outside mathematics and code ---------
GLOBAL = [
 (r"e \+ s > 1", r"$e + s > 1$"),
 (r"F ≤ 1/2", r"$F \\le 1/2$"),
 (r"I\(A;F\|E\)", r"$I(A;F \\mid E)$"),
 (r"H\(F\|E\)", r"$H(F \\mid E)$"),
 (r"δ_A\(𝒪\)", r"$\\delta_A(\\mathcal{O})$"),
 (r"δ_A", r"$\\delta_A$"),
 (r"𝒪", r"$\\mathcal{O}$"),
 (r"λ\*", r"$\\lambda^{\\ast}$"),
 (r"λ", r"$\\lambda$"),
 (r"c₀", r"$c_0$"),
 (r"κ₀", r"$\\kappa_0$"),
 (r"κ₁", r"$\\kappa_1$"),
 (r"β\(b\)", r"$\\beta(b)$"),
 (r"β", r"$\\beta$"),
 (r"τ", r"$\\tau$"),
 (r"ω", r"$\\omega$"),
 (r"T̄", r"$\\bar{T}$"),
 (r"T_gate", r"$T_{\\mathrm{gate}}$"),
 (r"p↑", r"$p_{\\uparrow}$"),
 (r"ε_l", r"$\\varepsilon_l$"),
 (r"\bv_l\b", r"$v_l$"),
 (r"\bc_l\b", r"$c_l$"),
 (r"κ", r"$\\kappa$"),
 (r"ρ", r"$\\rho$"),
 (r"Δ", r"$\\Delta$"),
 (r"q_max", r"$q_{\\max}$"),
 (r"q_k", r"$q_k$"),
 (r"N_eff", r"$N_{\\mathrm{eff}}$"),
 (r"1−s", r"$1-s$"),
]
# after the symbols: "$x$ = 0.75" becomes "$x = 0.75$"
MERGE_OPS = {"=": "=", "<": "<", ">": ">", "≤": r"\le", "≥": r"\ge", "≈": r"\approx"}
