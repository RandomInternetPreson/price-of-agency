"""make_index.py -- the index of the designed edition.

The index is read off the typeset pages: after the book is set, each page's text is searched for the patterns below and the
page numbers are written to <stem>_index.tex, which the next pass sets at the end of the book. So the index cannot disagree
with the pages, and an edit to the manuscript re-makes it.

ENTRIES is the whole editorial content: (heading, pattern[, 'cs']). A pattern is a regular expression matched against the
page's running text with line-end hyphens rejoined; 'cs' makes it case-sensitive (surnames). Words the book uses on nearly
every page (independence, aim, agency, theft, ledger) are indexed at the passages that define or turn on them, not at every
use. The theorems are listed separately, by number, at the pages where they are stated.
"""
import re, subprocess

ENTRIES = [
 # ---- the book's own terms
 ("agency, as independence with aim", r"two rulers|independence and aim|freedom two rulers"),
 ("aim (the second ruler)", r"second ruler|how much your actions serve|aim is not|destroying an agent.s aim"),
 ("apparent non-determinism", r"apparent non-?determinism"),
 ("audit, the field", r"field audit|an auditor|audit protocol|auditable"),
 ("axioms, the two", r"Axiom 1|Axiom 2|two axioms"),
 ("bandwidth", r"bandwidth"),
 ("baseline, named", r"named (feasible )?(baseline|alternative)|rules about baselines"),
 ("Bell's theorem; Bell experiments", r"Bell.s (theorem|inequalit)|Bell experiment|Bell angles", 'cs'),
 ("borrowed record, the", r"borrowed record|one tally|two tallies|sage.s tally"),
 ("cascade, informational", r"informational cascade"),
 ("cascade of imposition (hierarchy)", r"ledger of imposition|the cascade|hierarchy of bounded agents"),
 ("cash, time and steadier schedules compared", r"cash transfer|equal-?cost cash|time transfer|three ways to keep"),
 ("ceiling (one half)", r"never reach|ceiling it can|capped at one half|ceiling of this chapter"),
 ("choice data", r"choice data|revealed preference"),
 ("coin; fresh flips", r"honest flips|fresh (bits|key|coin|entropy)|where does the coin come from|a private die"),
 ("congruence", r"congruen"),
 ("consent", r"consent|willing seller|signed agreement"),
 ("correlation floor", r"correlation floor|shared (blind spots?|flaw|blindness)"),
 ("crowding; the real sea and the glass sea", r"glass sea|real sea|crowd(ed|ing) (ground|penalty)|crowding costs"),
 ("displacement", r"displacement by taking|net displacement|measurable displacement"),
 ("dose of following", r"best dose|herd dose|low dose|dose curve|dose is"),
 ("eraser, the", r"eraser"),
 ("exits from Bell's theorem", r"third exit|three exits|exits from Bell"),
 ("externality", r"externalit|Pigou correction"),
 ("famine", r"famine (risk|rate|probability) (falls|doubles|jumps|halve)|three missed days"),
 ("fenced conjecture, the", r"carefully fenced|A Conjecture, Fenced|fenced chapter"),
 ("fishing town, the", r"Here is the town|nine fishers|printed town"),
 ("forecast, naive and sophisticated household", r"naive household|sophisticated household|forecasts its own"),
 ("fringe, the hidden", r"fringe"),
 ("frontier, the", r"called the frontier|the frontier of Chapter 6|frontier has a hard trade|certified floor under the true frontier"),
 ("gate, the education", r"activation threshold|education gate|the gate sits|below the gate, education"),
 ("gate, the mistake-budget", r"mistake-?budget gate"),
 ("gate, the time", r"time gate"),
 ("habit; the watcher's file", r"habit seed|knows her habit|the file (catches|learns|reads)|deepest file"),
 ("hand-to-mouth households", r"hand-? ?to-? ?mouth"),
 ("HANK (heterogeneous-agent model)", r"HANK|heterogeneous-?agent"),
 ("harbor, the (tourist, captain, sailor)", r"lost tourist|ferry captain"),
 ("herd, the", r"the herd (stops|dissolves|line)|harden the herd|herd(ing)? survives|a herd"),
 ("hiding theorem (physics)", r"hiding theorem, arXiv|mathematically blind|mathematically incapable of seeing"),
 ("hiding theorem (economic)", r"hiding theorem, economic|market.s eyes cannot see"),
 ("hours partition, uncertainty broadcasts", r"hours partition"),
 ("independence (the first ruler)", r"first ruler|how little your circumstances predict|independence was defined"),
 ("Ines (the card player)", r"\bInes\b", 'cs'),
 ("inversion (the watcher who holds the coin)", r"the inversion|inverts her|surveillance inversion|gated inversion"),
 ("invitation, the; five questions", r"The invitation|five questions"),
 ("ledger, the", r"belongs on the books|ledger keeps|the ledger.s claim|ledger of Parts|ledger runs both ways"),
 ("license, never a number", r"a license, never a number|touch the license|the license itself|license under"),
 ("life plane and task plane", r"task plane|life plane"),
 ("living town, the", r"living town|town that watched itself"),
 ("manager's defense, the", r"manager.s defense|I priced it in"),
 ("master, the harbor", r"harbor master|follow(ing)? the master|the master decides"),
 ("measurement independence", r"measurement independence"),
 ("mistake budget", r"mistake budgets?"),
 ("monuments; the observation", r"monument"),
 ("Nadia and Tomas", r"\bNadia\b|\bTomas\b", 'cs'),
 ("notice, of a schedule", r"weeks? ahead|short-?notice|(a )?day.s notice|weeks.? notice"),
 ("one-time pad", r"one-?time-? ?pad"),
 ("opinions", r"no opinions|opinion, man|decline opinions|call it opinion"),
 ("plateau, the", r"This region is the plateau|That is the plateau|plateau has an edge|wider plateau|The plateau\b"),
 ("premium rights", r"premium rights"),
 ("preregistration", r"written down before|committed in writing|preregist"),
 ("price list, the", r"price list"),
 ("privacy", r"privacy"),
 ("public-signal window", r"public-?signal window|one signal all can see"),
 ("repository, the", r"The repository:|its repository"),
 ("rulers, the two", r"two rulers|one ruler,? or two|single ruler"),
 ("sage, the", r"sage point|the sage.s (tally|standing)|behind the sage|open sage"),
 ("schedule entropy", r"schedule entropy"),
 ("schedules, unstable", r"schedule posts|shape of his workers. time|steadier schedules|employer varies"),
 ("score, three ways to keep the", r"three ways to keep|how the score is kept|standard score"),
 ("staircase, the", r"staircase"),
 ("standing, law of", r"governed by standing|standing gives way|how long (the|such) standing"),
 ("steganography", r"steganograph"),
 ("stochasticity transfer", r"stochasticity transfer|stochasticity is transferred"),
 ("stock, who holds the", r"hold some stock|wide and thin"),
 ("superdeterminism", r"superdeterminis|rigged universe|determinism-? ?by-? ?conspiracy"),
 ("Survey of Household Economics and Decisionmaking", r"Survey of Household Economics|national survey"),
 ("tags (PROVEN, EXACT and the rest)", r"labels are printed beside|tags intact|each tagged"),
 ("theft, defined", r"Theft is displacement|word theft appears|theft, defined|theft has a size"),
 ("Theo (three seats); Elias", r"\bTheo\b|\bElias\b", 'cs'),
 ("time floor; time poverty", r"time floors?|time-?poor|time poverty"),
 ("unaudited", r"unaudited"),
 ("unmeasured quantity, law of the", r"unmeasured (quantity|column|domain)"),
 ("Vera (the courier)", r"\bVera\b", 'cs'),
 ("watchers", r"freedom from someone.s seat|from whose sight|learning watcher|watcher who (sees|holds|knows)"),
 ("wildcard, the", r"wildcards?"),
 ("wirings, the two", r"first wiring|second wiring|two wirings|gated wiring|additive wiring"),
 # ---- places, studies, people
 ("Auclert, Bardóczy, Rognlie and Straub", r"Auclert", 'cs'),
 ("Banerjee; Bikhchandani, Hirshleifer and Welch", r"Banerjee|Bikhchandani", 'cs'),
 ("Barnard and Sibly; Fretwell and Lucas", r"Barnard and Sibly|Fretwell", 'cs'),
 ("Beer; Simon", r"Beer.s viable|Simon.s architecture", 'cs'),
 ("Branham, Soroka and Wlezien; Bashir; Enns", r"Branham|Bashir", 'cs'),
 ("Cachin", r"Cachin", 'cs'),
 ("Coase", r"Coase", 'cs'),
 ("Cochrane", r"Cochrane", 'cs'),
 ("Condorcet", r"Condorcet", 'cs'),
 ("Cyert and March; Edmondson", r"Cyert|Edmondson", 'cs'),
 ("Forrester; Lee, Padmanabhan and Whang (bullwhip)", r"bullwhip"),
 ("Gabaix; Sims", r"Gabaix", 'cs'),
 ("Gilens and Page", r"Gilens", 'cs'),
 ("Golden", r"Golden 2015", 'cs'),
 ("Hacker (the great risk shift)", r"Hacker", 'cs'),
 ("Hall", r"\bHall\b", 'cs'),
 ("Harknett, Schneider and Irwin (Seattle)", r"Seattle", 'cs'),
 ("Kaplan, Moll and Violante", r"Kaplan", 'cs'),
 ("Kaur and colleagues; Carvalho, Meier and Wang", r"\bKaur\b|Carvalho", 'cs'),
 ("Kerckhoffs", r"Kerckhoffs", 'cs'),
 ("Kremer (O-ring)", r"Kremer", 'cs'),
 ("Mani, Mullainathan, Shafir and Zhao", r"\bMani\b|Mullainathan", 'cs'),
 ("Mas and Pallais", r"Pallais", 'cs'),
 ("Olson; Palfrey and Rosenthal", r"Olson|Palfrey", 'cs'),
 ("Ortega and Braun", r"Ortega", 'cs'),
 ("Pigou", r"Pigou", 'cs'),
 ("Porter (Trust in Numbers)", r"Porter", 'cs'),
 ("Schneider and Harknett", r"Schneider and Harknett", 'cs'),
 ("Shannon", r"Shannon", 'cs'),
 ("Tetlock", r"forecasts from 284 experts|Tetlock", 'cs'),
 ("Williams, Lambert, Kesavan and colleagues (the store trial)", r"assigned by lot|twenty-?eight stores"),
]


def page_texts(pdf, npages):
    """the running text of each page, without the page head, with line-end hyphens rejoined"""
    out = []
    for p in range(1, npages + 1):
        t = subprocess.run(['pdftotext', '-f', str(p), '-l', str(p), '-x', '0', '-y', '58', '-W', '504', '-H', '630', pdf, '-'],
                           capture_output=True, text=True).stdout
        t = re.sub(r'(\w)-\n(\w)', r'\1\2', t).replace('’', "'").replace('‘', "'")
        out.append(re.sub(r'\s+', ' ', t))
    return out


def ranges(pages):
    """[3, 4, 5, 9] -> [(3, 5), (9, 9)]"""
    out = []
    for p in pages:
        if out and p == out[-1][1] + 1: out[-1] = (out[-1][0], p)
        else: out.append((p, p))
    return out


def compute(pdf, first_numbered_page, last_body_page):
    """returns [(heading, [printed page numbers])]; pages before the contents and the index's own pages are not searched"""
    n = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    texts = page_texts(pdf, min(n, last_body_page))
    res = []
    for e in ENTRIES:
        pat = re.compile(e[1], 0 if len(e) > 2 else re.I)
        hits = [i + 1 - (first_numbered_page - 1) for i, t in enumerate(texts) if i + 1 >= first_numbered_page + 1 and pat.search(t)]
        res.append((e[0], hits))
    return res


def to_tex(res, claims):
    """the index pages: the terms in two columns, then the theorems by number"""
    def link(a, b): return str(a) if a == b else '%d--%d' % (a, b)
    lines = [r'\indexopen']
    for head, pages in sorted(res, key=lambda x: re.sub(r'[^a-z]', '', x[0].lower())):
        if not pages: continue
        head_tex = head
        lines.append(r'\indexentry{%s}{%s}' % (head_tex, ', '.join(link(a, b) for a, b in ranges(pages))))
    lines.append(r'\indexclaims')
    for label, name, ref in claims:
        lines.append(r'\indexentry{%s\enspace %s}{\pageref{%s}}' % (label, name, ref))
    lines.append(r'\indexclose')
    return '\n'.join(lines) + '\n'
