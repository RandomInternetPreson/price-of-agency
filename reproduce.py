"""reproduce.py -- re-run the book's computations and check each number against the page that prints it.

    python reproduce.py              every script that finishes in under a minute (two or three minutes in all)
    python reproduce.py --all        adds the long exact searches (see --list for their times)
    python reproduce.py --list       what runs, what is read from files already in the repository, and what is not re-run
    python reproduce.py --only town  only the scripts whose name contains "town"

What it does. It copies code/ to a temporary folder, so that nothing in the repository is touched; runs each script there
with the Python that is running this file; reads the numbers the script prints; and compares each one with the number the
book prints. Every check carries the sentence of the book it is checking, word for word, and the run stops being a pass if
that sentence is no longer in the manuscript. A number passes when the script's value, rounded the way the book prints
it, is the book's number.

Three kinds of line come out:

    ran        a script was run here, now, and its number matched the book (or did not: FAIL)
    recorded   the number was read from a results file in the repository and matched against the book. Nothing was re-run:
               these are the runs that need a GPU, hours of processor time, or the Federal Reserve's survey files
    not run    listed with the reason and the command that runs it

Needs Python 3.9 or later with numpy, scipy and matplotlib:   pip install numpy scipy matplotlib
The report is printed and also written to REPRODUCE_REPORT.md beside this file.
"""
import os, re, sys, csv, glob, time, shutil, tempfile, platform, subprocess

ROOT = os.path.dirname(os.path.abspath(__file__))


# ------------------------------------------------------------------------------------------------ the book
def manuscript():
    mds = sorted(glob.glob(os.path.join(ROOT, 'docs', 'THE_PRICE_OF_AGENCY_unified_v0.*.md')), key=lambda p: [int(x) for x in re.findall(r'\d+', os.path.basename(p))])
    if not mds: raise SystemExit('no manuscript found in docs/')
    return mds[-1]


def squash(s): return re.sub(r'\s+', ' ', s).strip()


# ------------------------------------------------------------------------------------------------ reading a script's output
def g(pattern, nth=0, group=1):
    """the nth match of a pattern in what the script printed, as a number"""
    def get(out):
        hits = list(re.finditer(pattern, out, re.M))
        if len(hits) <= nth: raise LookupError('not printed: %s' % pattern)
        return float(hits[nth].group(group).replace(',', '').rstrip('%'))
    return get


def allof(pattern, group=1):
    def get(out):
        hits = [float(m.group(group)) for m in re.finditer(pattern, out, re.M)]
        if not hits: raise LookupError('not printed: %s' % pattern)
        return hits
    return get


def digits(printed):
    m = re.search(r'\d+(?:\.(\d+))?', printed.replace(',', ''))
    return len(m.group(1)) if (m and m.group(1)) else 0


WORDS = {'zero': 0, 'none': 0, 'no': 0, 'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5, 'six': 6, 'seven': 7, 'eight': 8, 'nine': 9, 'ten': 10, 'twenty': 20,
         'a week': 7, 'a third': 1 / 3, 'one third': 1 / 3, 'seven tenths': 0.7, 'halved': 0.5, 'doubles': 2, 'ninety-five': 95, 'fifty': 50, 'five hundred': 500, 'twenty-fold': 20,
         'six-fold': 6, 'ten times': 10, 'refuted': 0}


def eq(get, printed, scale=1.0, tol=None):
    """the script's value, times scale, rounds to what the book prints. A number in words is given with its tolerance."""
    def test(out):
        got = get(out) * scale
        if printed in WORDS:
            want = WORDS[printed]; t = tol if tol is not None else 0.5
        else:
            want = float(re.search(r'-?\d+(?:\.\d+)?', printed.replace(',', '')).group(0)); t = tol if tol is not None else 0.5 * 10 ** -digits(printed) + 1e-9
        return abs(got - want) <= t, _f(got), printed
    return test, printed


def within(get, lo, hi, printed):
    """every value the script prints for this lies in the range the book states"""
    def test(out):
        v = get(out); v = v if isinstance(v, list) else [v]
        return all(lo <= x <= hi for x in v), ', '.join(_f(x) for x in v[:6]), printed
    return test, printed


def holds(fn, shown, printed):
    """a statement the book makes in words, tested on the script's numbers"""
    def test(out):
        return bool(fn(out)), shown(out) if callable(shown) else shown, printed
    return test, printed


def _f(x): return ('%.4g' % x) if abs(x) >= 1e-3 or x == 0 else ('%.1e' % x)


# ------------------------------------------------------------------------------------------------ the checks
# (script, seconds it took on a 2026 laptop-class processor, [(where in the book, the book's sentence, [tests])])
def diff(a, b): return lambda out: a(out) - b(out)
def ratio(a, b): return lambda out: a(out) / b(out)


FAST = [
 ('code/verify_theorems.py', 4, [
    ('Chapter 4 §5', 'Theorem 1 was machine-checked on five hundred randomized worlds', [
        eq(g(r'T1 sage identity, (\d+) random'), 'five hundred'),
        holds(lambda o: g(r'max \|error\| = (\S+)')(o) < 1e-12, lambda o: 'largest error %s' % _f(g(r'max \|error\| = (\S+)')(o)), 'machine-checked')]),
    ('Chapter 4 §5', 'Theorem 2 was checked the same way (no violations; equality exactly where the proof says)', [
        eq(g(r'T2 complementarity, \d+ instances: violations = (\d+)'), 'no')])]),
 ('code/dichotomy_scaling_and_audits.py', 1, [
    ('Chapter 5 §6', 'the gate at n = 16, 32, 64: zero below, ~0.93–0.95 above, at the predicted location every time', [
        within(allof(r'below-gate (\S+)'), 0, 1e-6, 'zero below'),
        within(allof(r'above-gate (\S+)'), 0.925, 0.955, '0.93–0.95')]),
    ('Chapter 4 §5', 'additionally stress-tested at alphabet sizes up to 64', [
        within(allof(r'max T2 violation (\S+)'), -1, 1e-12, 'stress-tested')])]),
 ('code/mistake_budget_T18.py', 1, [
    ('Chapter 5 §3', 'At κ = 10 in a half-noisy world, the gate sits at 0.936 with two options, 0.947 with eight, and under 0.95 with any number', [
        eq(g(r'reference kappa=10 s=0\.5 n=2: gate (\S+);'), '0.936'), eq(g(r'reference kappa=10 s=0\.5 n=8: gate (\S+);'), '0.947'),
        within(g(r'reference kappa=10 s=0\.5 n=64: gate (\S+);'), 0.947, 0.95, 'under 0.95')]),
    ('Chapter 5 §2', 'the same lessons must be right ninety-five times in a hundred before she acts on them', [
        eq(g(r'n=8: gate \S+; the knowledge is then right (\S+)'), 'ninety-five', scale=100, tol=0.6),
        eq(g(r'n=64: gate \S+; the knowledge is then right (\S+)'), 'ninety-five', scale=100, tol=0.6)]),
    ('Chapter 5 §2', 'lessons open the gate once they are right more than fifty times in a hundred', [
        eq(g(r'reference kappa=1 s=0\.5 any n: gate (\S+)'), 'fifty', scale=100)]),
    ('Chapter 5 §6', 'Theorem 5b in 196 worlds', [
        eq(g(r'brute force, (\d+) worlds'), '196'),
        holds(lambda o: g(r'largest gap (\S+)')(o) < 1e-9, lambda o: 'largest gap between the formula and brute force %s' % _f(g(r'largest gap (\S+)')(o)), 'in 196 worlds')])]),
 ('code/calculator_model.py', 2, [
    ('Appendix I', 'The model inside it is code/calculator_model.py, which checks itself against Theorems 5b and 16', [
        holds(lambda o: all(abs(a - b) < 1e-4 for a, b in re.findall(r'gate by this model (\S+); Theorem 5b (\S+)', o) for a, b in [(float(a), float(b))]) and len(re.findall(r'Theorem 5b', o)) >= 4,
              'the model\'s one-glimpse gate equals Theorem 5b at four mistake ratios', 'Theorems 5b'),
        holds(lambda o: len(re.findall(r'^  T [0-4] .* same$', o, re.M)) == 5, 'independence and accuracy equal iterative_time_T16.py at 0 to 4 sittings', 'and 16')])]),
 ('code/mistake_ratio_noisy_self_knowledge.py', 45, [
    ('Chapter 5 §3', 'one where the population sits at its gate; below one where most sit above it (a margin silences people who should act); and without bound where most sit below it and do not know it', [
        holds(lambda o: all(0.95 <= float(a) and float(b) <= 1.05 for a, b in re.findall(r'at the gate, kappa\* between (\S+) and (\S+)', o)),
              lambda o: 'at the gate, the best ratio lies between ' + ' and '.join(re.findall(r'CHECK n=8: at the gate, kappa\* between (\S+) and (\S+)', o)[0]) + ' (eight options, noise 0.05 and 0.10)', 'one where the population sits at its gate'),
        holds(lambda o: re.findall(r'above the gate, kappa\* below 1 in (\d+) of (\d+)', o) == [('12', '12')] * 3, 'above the gate, the best ratio is below 1 in 12 of 12 populations, at 2, 8 and 64 options', 'below one where most sit above it'),
        holds(lambda o: re.findall(r'below the gate, kappa\* above 1 in (\d+) of (\d+) cells; at the top of the grid in (\d+) of (\d+)', o) == [('12', '12', '4', '6')] * 3,
              'below the gate, the best ratio is above 1 in 12 of 12 populations and at the top of the search (nobody acts) in every world once the noise reaches 0.3', 'without bound where most sit below it and do not know it')])]),
 ('code/delta_A_v1.py', 2, [
    ('Chapter 4 §4', 'δ_A = 0: the captain — circumstances leave no doubt. δ_A = 1: the tourist — circumstances say nothing.', [
        eq(g(r'rock .*delta_A = (\S+)'), 'δ_A = 0', tol=1e-9), eq(g(r'gas .*delta_A = (\S+)'), 'δ_A = 1', tol=1e-9)])]),
 ('code/plateau_hit_rate_bound.py', 2, [
    ('Chapter 6 §2', 'not more than the captain who simply follows the table\'s tells, unless those tells are noise more than half the time', [
        holds(lambda o: 'true in 42 of 42 worlds' in o and float(re.search(r'largest gap (\S+)', o).group(1)) < 1e-9,
              'the most a perfectly unreadable strategy can be right, by linear program in 42 worlds, exceeds the captain exactly when the noise is above one half', 'more than half the time')])]),
 ('code/frontier_attack.py', 7, [
    ('Chapter 6 §6', 'the optimizer that killed the simple- strategy conjecture', [
        holds(lambda o: g(r'max excess over candidate curve across all attacks: (\S+)')(o) > 0.01,
              lambda o: 'the optimizer beats the conjectured curve by %s' % _f(g(r'max excess over candidate curve across all attacks: (\S+)')(o)), 'killed')])]),
 ('code/theft_equilibrium.py', 1, [
    ('Chapter 7 §4', 'the independence ruler by elasticity at most 0.009 while moving aim by 1.5 to 2.0', [
        holds(lambda o: abs(max(abs(x) for x in allof(r'd/dlog (?:s_hat|t)\s+: comp\s+\S+\s+dA\s+(\S+)')(o)) - 0.009) < 5e-4,
              lambda o: 'largest %s' % _f(max(abs(x) for x in allof(r'd/dlog (?:s_hat|t)\s+: comp\s+\S+\s+dA\s+(\S+)')(o))), '0.009'),
        within(allof(r'd/dlog (?:s_hat|t)\s+: comp\s+(\S+)'), 1.45, 2.05, '1.5 to 2.0')]),
    ('Chapter 7 §4', 'education spikes to about 9, and against the world\'s predictability to about 4.5', [
        eq(g(r's=0\.3\):\n\s+d/dlog e\s+: comp\s+\S+\s+dA\s+(\S+)'), '9', tol=0.5),
        eq(g(r's=0\.3\):\n.*\n.*\n\s+d/dlog s\s+: comp\s+\S+\s+dA\s+(\S+)'), '4.5', tol=0.05)]),
    ('Chapter 7 §4', 'aim\'s elasticity against time is 0.565 for a time-poor agent versus 0.008 for a time-rich one', [
        eq(g(r'beta=6\.0, s=0\.5\):\n.*\n\s+d/dlog beta\s+: comp\s+(\S+)'), '0.565'),
        eq(g(r'e=0\.7, beta=20\.0, s=0\.5\):\n.*\n\s+d/dlog beta\s+: comp\s+(\S+)'), '0.008')]),
    ('Chapter 8 §4', 'Result: δ_A({circumstances, die}) = 0.29 in the model, versus 0.75 for the undisguised expert', [
        eq(g(r'delta_A\(O1=\{E,R\}\)\s+= (\S+)'), '0.29'), eq(g(r'sage ceiling H\(F\|E\)/log = (\S+)'), '0.75')])]),
 ('code/surveillance_T9_wider_plateau.py', 1, [
    ('Chapter 8 §3', 'at 0.29 for the strategy that follows the target a fixed fraction of the time and compensates the rest, and at 0.65 for', [
        eq(g(r'lambda\* policy.*?\s(\S+)\s+True'), '0.29'), eq(g(r'hand plateau policy.*?\s(\S+)\s+True'), '0.65')]),
    ('Chapter 8 §3', 'crossover comes at roughly one third visibility of the source of chance for the first strategy and seven tenths for the second', [
        eq(g(r'lambda\* policy.*True\s+(\S+)'), 'one third', tol=0.02), eq(g(r'hand plateau policy.*True\s+(\S+)'), 'seven tenths', tol=0.02)])]),
 ('code/wirings_T11_wider_plateau.py', 1, [
    ('Chapter 9 §5', 'half-noisy world (gated floors rising to 0.62–0.70 but staying below the open expert; additive equality at three bits)', [
        holds(lambda o: (lambda v: abs(min(v) - 0.62) < 0.005 and abs(max(v) - 0.70) < 0.005)([float(x) for x in re.findall(r'h=\d: (\S+) \(', o.split('hand plateau policy')[1].split('\n')[1])]),
              lambda o: 'gated floors ' + ', '.join(re.findall(r'h=\d: (\S+) \(', o.split('hand plateau policy')[1].split('\n')[1])), '0.62–0.70'),
        holds(lambda o: max(float(x) for x in re.findall(r'h=\d: (\S+) \(', o.split('hand plateau policy')[1].split('\n')[1])) < g(r'hand plateau policy.*floor <= sage (\S+)')(o),
              lambda o: 'open expert %s' % _f(g(r'hand plateau policy.*floor <= sage (\S+)')(o)), 'staying below the open expert'),
        holds(lambda o: (lambda m: m.group(1) == m.group(2))(re.search(r'h=3: (\S+) \(seed-unknown (\S+)\)', o.split('hand plateau policy')[1].split('\n')[2])),
              lambda o: 'at three bits the floor equals the first-day value, %s' % re.search(r'h=3: (\S+) \(', o.split('hand plateau policy')[1].split('\n')[2]).group(1), 'additive equality at three bits')])]),
 ('code/arms_race.py', 13, [
    ('Chapter 9 §3', 'More coin does not raise a gated floor.', [
        holds(lambda o: max(allof(r'^\s+\d\s+\S+\s+(\S+)\s+\S+\s+\S+\s*$')(o)[:4]) < 0.5, lambda o: 'gated floors ' + ', '.join(_f(x) for x in allof(r'^\s+\d\s+\S+\s+(\S+)\s+\S+\s+\S+\s*$')(o)[:4]) + ', all under one half', 'does not raise')])]),
 ('code/stealth_gates.py', 1, [
    ('Chapter 6 §4', '(In the reference world, 0.247 against the first printing\'s 0.052', [
        eq(g(r'^\s+1\.00\s+(\S+)\s+1\.0000'), '0.052')])]),
 ('code/iterative_time_T16.py', 1, [
    ('Chapter 7 §6', 'the time gate and the Tomas version', [
        holds(lambda o: g(r'T 0 delta_A (\S+)')(o) == 0 and g(r'T 1 delta_A (\S+)')(o) == 0 and g(r'T 2 delta_A (\S+)')(o) > 0.4,
              lambda o: 'independence 0, 0, then %s at the third step' % _f(g(r'T 2 delta_A (\S+)')(o)), 'the time gate')])]),
 ('code/neighbors_T12_P15.py', 1, [
    ('Chapter 10 §3', 'from 0.77 alone, to 0.71 beside an unreadable neighbor, to 0.61 beside an ordinary one, to exactly 0 beside a flawless visible expert', [
        eq(g(r'absent ceiling (\S+)'), '0.77'), eq(g(r'covert ceiling (\S+)'), '0.71'), eq(g(r'rock ceiling (\S+)'), '0.61'), eq(g(r'sage ceiling (\S+)'), 'exactly 0', tol=1e-12)]),
    ('Chapter 10 §3', 'first costs 0.17, the second 0.13, the third 0.10, the fourth 0.08', [
        eq(diff(g(r'k 0 ceiling (\S+)'), g(r'k 1 ceiling (\S+)')), '0.17'), eq(diff(g(r'k 1 ceiling (\S+)'), g(r'k 2 ceiling (\S+)')), '0.13'),
        eq(diff(g(r'k 2 ceiling (\S+)'), g(r'k 3 ceiling (\S+)')), '0.10'), eq(diff(g(r'k 3 ceiling (\S+)'), g(r'k 4 ceiling (\S+)')), '0.08')])]),
 ('code/fishing_town_T13.py', 1, [
    ('Chapter 11 §4', 'giving 0.074 per ninety-day season', [eq(g(r'^independent: (\S+)'), '0.074')]),
    ('Chapter 11 §4', 'its famine probability, 0.44, does not improve by one decimal if the town grows', [eq(g(r'^hub: (\S+)'), '0.44')]),
    ('Chapter 11 §3', 'Nine independent 70%-fishers beat one 80% authority six-fold on famine', [eq(ratio(g(r'^hub: (\S+)'), g(r'^independent: (\S+)')), 'six-fold')]),
    ('Chapter 11 §3', 'falls exponentially in the number of independent educated fishers (roughly halving per two added)', [
        holds(lambda o: (lambda v: all(0.45 < v[i + 1] / v[i] < 0.6 for i in range(len(v) - 1)))(allof(r'^N \d+ famine (\S+)')(o)),
              lambda o: 'each two fishers added multiply famine by ' + ', '.join('%.2f' % (b / a) for a, b in zip(allof(r'^N \d+ famine (\S+)')(o), allof(r'^N \d+ famine (\S+)')(o)[1:])), 'roughly halving per two added')]),
    ('Chapter 11 §3', 'a benefit at one, worsening after, saturating exactly at bloc majority', [
        holds(lambda o: (lambda v: v[1] < v[0] and v[1] < v[2] < v[3] < v[4] < v[5] and v[5] == v[9])(allof(r'^hub-followers \d (\S+)')(o)),
              lambda o: 'famine by followers 0 to 5: ' + ', '.join('%.3f' % x for x in allof(r'^hub-followers \d (\S+)')(o)[:6]) + '; unchanged from 5 to 9', 'a benefit at one')]),
    ('Chapter 11 §5, table', '| Nothing changed (master right 80) | 7 | 5 | 6 | 14 | 44 | 44 | one |', [
        holds(lambda o: [int(100 * allof(r'^hub-followers \d (\S+)')(o)[k] + 0.5) for k in (0, 1, 2, 3, 5, 9)] == [7, 5, 6, 14, 44, 44],
              lambda o: 'exact: ' + ' | '.join('%d' % int(100 * allof(r'^hub-followers \d (\S+)')(o)[k] + 0.5) for k in (0, 1, 2, 3, 5, 9)) + ' (the table is simulated; this is the exact computation)', '7 | 5 | 6 | 14 | 44 | 44')])]),
 ('code/correlated_weather_T14.py', 1, [
    ('Chapter 11 §4', 'a floor that size cannot touch, only sameness can lower', [
        holds(lambda o: all(f31 >= fl > 0 for f31, fl in zip(allof(r'N 31 famine (\S+)')(o)[1:], allof(r'floor: (\S+)')(o)[1:])),
              lambda o: 'thirty-one boats, shared mirage on 5, 15, 30 days in a hundred: famine ' + ', '.join(_f(x) for x in allof(r'N 31 famine (\S+)')(o)[1:]) + ' against floors ' + ', '.join(_f(x) for x in allof(r'floor: (\S+)')(o)[1:]), 'a floor')])]),
 ('code/living_town_S1.py', 40, [
    ('Chapter 11 §3', 'finite resources convert it (interior mix, higher accuracy, famine halved)', [
        eq(ratio(g(r'^B finite fish\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)'), g(r'^A infinite fish\s+\S+\s+\S+\s+\S+\s+\S+\s+\S+\s+(\S+)')), 'halved', tol=0.1),
        holds(lambda o: 0.2 < g(r'^B finite fish\s+\S+\s+(\S+)')(o) < 0.8, lambda o: 'share following the hub at the end: %s' % _f(g(r'^B finite fish\s+\S+\s+(\S+)')(o)), 'interior mix'),
        holds(lambda o: g(r'^B finite fish\s+\S+\s+\S+\s+\S+\s+(\S+)')(o) > g(r'^A infinite fish\s+\S+\s+\S+\s+\S+\s+(\S+)')(o), 'majority right more often with finite fish', 'higher accuracy')])]),
 ('code/borrowed_record.py', 1, [
    ('Chapter 11 §3', 'his record is 85 against a reader\'s 79.5, every boat follows him, and famine doubles, from 11 seasons in a hundred to 22.5', [
        eq(g(r'\| the sage \| (\S+)%'), '85'), eq(g(r'\| one reader \| (\S+)%'), '79.5'), eq(g(r'\| everyone reads \| \S+ \| (\S+)%'), '11'), eq(g(r'\| everyone follows the sage \| \S+ \| (\S+)%'), '22.5')]),
    ('Chapter 11 §3', 'the town\'s majority was right 999 times in a thousand', [eq(g(r'\| the readers\' majority \| \S+ \| (\S+)%'), '999', scale=10)]),
    ('Chapter 11 §3', 'put him back where he is right and the town back at 11', [eq(g(r'\| two tallies.*\| \S+ \| (\S+)%'), '11')]),
    ('Chapter 11 §3', 'a week away when every hard day is scored, seven seasons away when one in a hundred is', [
        eq(g(r'^\| 1 \| (\d+) \('), 'a week', tol=0.5), eq(g(r'^\| 0\.01 \| \S+ \((\S+) seasons\)'), 'seven')]),
    ('Chapter 11 §3', 'and famine stops at 14 seasons in a hundred', [eq(g(r'Followers by number.*? 2: (\S+)%'), '14')]),
    ('Part V, Why the self-anointed rule', '85 right in a hundred against a fisher\'s 79', [eq(g(r'\| the sage \| (\S+)%'), '85'), eq(g(r'\| one reader \| (\S+)%'), '79', tol=0.51)])]),
 ('code/attack_T22_T23.py', 1, [
    ('Chapter 11 §3', 'a third would land 0.109 of the catch where a reader lands 0.111', [
        eq(g(r'^\| 2 \| \S+ V \| \S+ V \| (\S+) V'), '0.109'), eq(g(r'^\| 2 \| \S+ V \| (\S+) V'), '0.111')]),
    ('Chapter 11 §3', '27 in a hundred in the printed town — and the murky boats stay in above a trip cost of 0.51 where they had stayed in above 0.40; at three boatloads of hunger, above 0.72', [
        eq(g(r'9 boats, 5 needed \| murky boats stay in \| (\S+)'), '27', scale=100), eq(g(r'9 boats, 5 needed \| murky boats stay in \| \S+ \| \S+ \| (\S+)'), '0.51'),
        eq(g(r'9 boats, 5 needed \| murky boats stay in \| \S+ \| (\S+)'), '0.40'), eq(g(r'9 boats, 5 needed \| murky boats stay in \| \S+ \| \S+ \| \S+ \| (\S+)'), '0.72')]),
    ('Chapter 11 §3', 'that chance is 8 in a hundred and the line moves from 0.40 to 0.43', [
        eq(g(r'99 boats, 55 needed \| murky boats stay in \| (\S+)'), '8', scale=100), eq(g(r'99 boats, 55 needed \| murky boats stay in \| \S+ \| \S+ \| (\S+)'), '0.43')])]),
 ('code/stay_ashore.py', 1, [
    ('Chapter 11 §3', 'ashore on any morning, famine goes from 7 seasons in a hundred to 98', [
        eq(g(r'^\| 0\.6 \| 0\.9 \| 0\.4 \| \S+ / (\S+)%'), '7'), eq(g(r'^\| 0\.6 \| 0\.9 \| 0\.4 \| \S+ / \S+ \| \S+ / (\S+)%'), '98')]),
    ('Chapter 11 §3', 'for under three percent of the catch when the gap is a twentieth of a boatload', [
        within(g(r'^\| 0\.6 \| 0\.9 \| 0\.4 \|.*\| (\S+)% \|$'), 2.0, 2.999, 'under three percent')])]),
 ('code/two_towns_aid.py', 1, [
    ('Chapter 14 §5B', 'famine falls twenty-fold for both', [eq(g(r'^\| 0 \| \S+ \| \S+ \| \S+ \| ×(\S+) lower'), 'twenty-fold', tol=1.5)]),
    ('Chapter 15 §3', 'cut famine from 7 seasons in a hundred to a third of one', [
        eq(g(r'^\| 0 \| (\S+)%'), '7'), eq(g(r'^\| 0 \| \S+ \| (\S+)%'), 'a third', tol=0.03)])]),
 ('code/duty_trade_exact.py', 1, [
    ('Chapter 15 §3', 'The expectation that such a trade would starve the town was refuted', [
        holds(lambda o: g(r'every party can be made whole and the town starves more often\): \*\*(\d+)\*\*')(o) == 0,
              lambda o: 'cases in which the trade pays every party and starves the town: %d of 48' % g(r'every party can be made whole and the town starves more often\): \*\*(\d+)\*\*')(o), 'refuted')]),
    ('Chapter 15 §3', 'selling the burden to the same few boats is better for the town than drawing it by lot in most cases computed', [
        holds(lambda o: g(r'specialization pays the town too\): \*\*(\d+)\*\*')(o) > 24, lambda o: 'the trade is better for the town in %d of 48 cases' % g(r'specialization pays the town too\): \*\*(\d+)\*\*')(o), 'in most cases computed')])]),
 ('code/joined_three_rulers.py', 1, [
    ('Chapter 14 §5C', 'the time transfer lifts the low-skill group\'s from 0.30 to 0.65, stability lifts it to 0.42, and cash leaves it where it was', [
        eq(g(r'^\| no program \|.*?\| (\S+) / '), '0.30'), eq(g(r'^\| time transfer.*?\| (\S+) / '), '0.65'), eq(g(r'^\| low-skill schedule entropy halved.*?\| (\S+) / '), '0.42'),
        holds(lambda o: abs(g(r'^\| cash, same cost as the time transfer.*?\| (\S+) / ')(o) - g(r'^\| no program \|.*?\| (\S+) / ')(o)) < 0.015,
              lambda o: 'with the cash %s' % _f(g(r'^\| cash, same cost as the time transfer.*?\| (\S+) / ')(o)), 'where it was')]),
    ('Chapter 14 §5C', 'The town starves in 11 seasons of a hundred with no program, in fewer than one with the time transfer, in 4 with stability, and in 11 with the cash', [
        eq(g(r'^\| no program \|.*\| (\S+)% \|$'), '11'), within(g(r'^\| time transfer.*\| (\S+)% \|$'), 0, 0.999, 'fewer than one'),
        eq(g(r'^\| low-skill schedule entropy halved.*\| (\S+)% \|$'), '4'), eq(g(r'^\| cash, same cost as the time transfer.*\| (\S+)% \|$'), '11')]),
    ('Chapter 14 §5C', 'records 3.6 percent less fish, while the town\'s famine rate more than doubles', [
        eq(g(r'^\| 0\.60 \| 0\.70 \| \S+ \| (\S+)%'), '3.6'), within(g(r'^\| 0\.60 \| 0\.70 \|.*×(\S+) \|$'), 2.0001, 99, 'more than doubles')])]),
 ('code/imposition_cascade_T17.py', 2, [
    ('Chapter 13 §2B', 'cascade, the bottom layer bears 93.4% of all agency destroyed', [eq(g(r'share of total agency loss borne by workers: (\S+)%'), '93.4')]),
    ('Chapter 13 §2B', '| Worker | 64 | 14 | 1 | 0.565 | 7.91 | 506.2 |', [
        eq(g(r'^\s+worker\s+64\s+(\S+)'), '14'), eq(g(r'^\s+worker\s+64\s+\S+\s+(\S+)'), '1'), eq(g(r'^\s+worker\s+64\s+\S+\s+\S+\s+(\S+)'), '7.91'), eq(g(r'^\s+worker\s+64\s+\S+\s+\S+\s+\S+\s+(\S+)'), '506.2')]),
    ('Chapter 13 §2B', '| Executive | 1 | 100 | 60 | 0.008 | 0.80 | 0.8 |', [
        eq(g(r'^executive\s+1\s+(\S+)'), '100'), eq(g(r'^executive\s+1\s+\S+\s+(\S+)'), '60'), eq(g(r'^executive\s+1\s+\S+\s+\S+\s+(\S+)'), '0.80')]),
    ('Chapter 13 §2B', 'ten times more agency per person', [eq(g(r'agency loss x(\S+)'), 'ten times')])]),
 ('code/rig/wiring_hardening_exact.py', 10, [
    ('Chapter 9 §3', '**Theorem 11′ (The dichotomy, hardened). [EXACT; 3,372 wirings]**', [eq(g(r'^(\d+) exact configurations'), '3,372')]),
    ('Chapter 9 §3', 'four options in a half-noisy world it stays below by 0.07; in a six-option world that is mostly right it crosses above, 0.564 against 0.538', [
        eq(g(r'^\s+\| 4 \| 0\.5 \| hand \| \+(\S+) \|'), '0.07'), eq(g(r'n=6 s=0\.3 hand m_S=8 h=2 gated: floor (\S+) vs sage'), '0.564'), eq(g(r'n=6 s=0\.3 hand m_S=8 h=2 gated: floor \S+ vs sage (\S+)'), '0.538')]),
    ('Chapter 9 §5', 'failed by 0.026 in a six-option world that is mostly right', [eq(g(r'^\s+\| 6 \| 0\.3 \| hand \| -(\S+) \|'), '0.026')])]),
 ('code/fringe_2608_18886.py', 1, [
    ('The paper the essay "The law\'s own exhibit" stands on (arXiv:2608.18886); the figure in the designed edition', 'arXiv:2608.18886', [
        holds(lambda o: abs(g(r'efficiency of the exact profile \| (\S+)')(o) - 0.801) < 5e-4, lambda o: 'efficiency %s against the paper\'s 0.801' % _f(g(r'efficiency of the exact profile \| (\S+)')(o)), 'arXiv:2608.18886'),
        holds(lambda o: abs(g(r'fringe, peak to peak over mean \| (\S+)')(o) - 0.124) < 5e-4, lambda o: 'fringe %s against the paper\'s 0.124' % _f(g(r'fringe, peak to peak over mean \| (\S+)')(o)), 'arXiv:2608.18886')])]),
]

LONG = [
 ('code/plateau_edge_T6prime.py', 165, [
    ('Chapter 6 §4', '(In the reference world, 0.247 against the first printing\'s 0.052', [
        eq(g(r'^ 6\s+0\.5\s+\S+\s+(\S+)'), '0.247'), eq(g(r'^ 6\s+0\.5\s+(\S+)'), '0.052'),
        holds(lambda o: abs(g(r'^ 6\s+0\.5\s+\S+\s+(\S+)')(o) - g(r'^ 6\s+0\.5\s+\S+\s+\S+\s+(\S+)')(o)) < 5e-5, 'the closed form and the computed value agree', 'In the reference world')]),
    ('Chapter 6 §5', '0.10, 0.25, 0.46 as the world\'s noise rises through 0.3, 0.5, 0.7 in the reference world', [
        eq(g(r'^ 6\s+0\.3\s+\S+\s+(\S+)'), '0.10'), eq(g(r'^ 6\s+0\.5\s+\S+\s+(\S+)'), '0.25'), eq(g(r'^ 6\s+0\.7\s+\S+\s+(\S+)'), '0.46')])]),
]

LONG += [
 ('code/frontier_polytope_attack.py', 300, [
    ('Chapter 6 §5', 'certified floor under the true frontier: aim at least 1.00 at δ_A = 0.75; 0.86 at δ_A = 0.80; 0.70 at δ_A = 0.85; 0.53 at δ_A = 0.93; 0.37 at δ_A = 0.98; 0.35 at δ_A = 0.99; 0.29 at δ_A = 0.997', [
        t for mu_line, d, a in ((r'fam b mu=1\.00', '0.75', '1.00'), (r'fam b mu=0\.90', '0.80', '0.86'), (r'fam b mu=0\.75', '0.85', '0.70'), (r'fam a mu=0\.25', '0.93', '0.53'),
                                (r'fam b mu=0\.25', '0.98', '0.37'), (r'fam a mu=0\.10', '0.99', '0.35'), (r'fam b mu=0\.10', '0.997', '0.29'))
        for t in (eq(g(mu_line + r'\s+delta_A=(\S+)'), 'δ_A = ' + d), eq(g(mu_line + r'\s+delta_A=\S+\s+aim_min=\S+\s+aim_max>=(\S+)'), a + ' at δ_A = ' + d if a != '1.00' else 'aim at least 1.00'))])]),
 ('code/hiding_theorem_econ.py', 400, [
    ('Chapter 13 §2C', 'is produced by a town of Tomases and Nadias at aim 0.07 — and, identically, by the sage, acting on perfect knowledge of the future through a half-reliable world, at aim 1.00', [
        eq(g(r'^\s+0\.50\s+\S+\s+(\S+)'), '0.07'), eq(g(r'^\s+0\.50\s+\S+\s+\S+\s+(\S+)'), '1.00')]),
    ('Chapter 13 §2C', 'is produced by pure scatter at aim zero and by Ines\'s plateau strategy at aim c₀, identically', [
        eq(g(r'aim_min \(noise reading, Nadia\)\s+= (\S+)'), 'zero', tol=1e-9),
        holds(lambda o: g(r'delta_A identified = (\S+)')(o) == 1.0, 'both produce choice data with independence 1.0000', 'identically')])]),
]

NOT_RUN = [
 ('code/rig/plateau_edge_vertex_search.py, plateau_edge_bnb.py', 'the edge of the plateau (Chapter 6 §6, Chapter 15 §2): 0.335 at six options and the certified ceilings',
  'these are searches, and the printed values are the best of long runs; a twenty-second run of the first finds 0.331, under the printed 0.335 as a floor should be',
  'python code/rig/plateau_edge_vertex_search.py 6 0.5 <restarts> <seconds>; the long runs\' outputs are in code/rig/results_exact/'),
 ('code/rig/watcher_tournament.py', 'the learned watchers of Chapter 9 (Theorem 20, Result R6)', 'needs a GPU; about an hour on six', 'see code/rig/README_RIG.md; results in code/rig/results/'),
 ('code/rig/town_stress_T13.py, town_stress2.py, living_town_skill.py', 'the towns under stress (S2, S3) and the table of Chapter 11 §5',
  'twenty thousand simulated seasons a cell, written for a GPU with PyTorch (they fall back to the processor, slowly)',
  'the launchers in code/rig/ (RUN_ALL.bat on Windows); the table is checked above against the results files'),
 ('code/rig/hank_port/', 'Chapter 14 §5C: the household model in general equilibrium, and its sweeps of 688 and 273 drawn economies', 'hours of processor time on many cores',
  'the launchers in code/rig/ (RUN_NIGHT.bat, RUN_DAY.bat, RUN_RULERS.bat, RUN_TWOASSET_RULERS.bat); the first sweep\'s table is checked above against its summary'),
 ('code/field/shed_*.py', 'Chapter 13 §2D: the Federal Reserve survey', 'needs the survey\'s public files, which are the Federal Reserve\'s to distribute and are not copied into this repository',
  'download the SHED public-use files for 2019 to 2023 from federalreserve.gov; each script\'s first lines say which files it takes (python code/field/shed_first_look.py public2022.csv public2023.csv); they also need pandas and statsmodels. The printed numbers are checked above against code/field/results/'),
]


# ------------------------------------------------------------------------------------------------ numbers read from results files
def recorded_checks(book):
    """(where, the book's sentence, the file, [(ok, got, printed)])"""
    out = []

    def rd(*p): return open(os.path.join(ROOT, *p), encoding='utf-8').read()

    # Chapter 11 §5: the stress table, cell by cell, from the two results files
    t1 = list(csv.DictReader(open(os.path.join(ROOT, 'code', 'rig', 'results_town', 'town_stress_00.csv'))))
    t2 = list(csv.DictReader(open(os.path.join(ROOT, 'code', 'rig', 'results_town2', 'town_stress2.csv'))))

    def first(**kw):
        base = dict(q=0.8, p=0.7, rho_G=0.0, rho_err=0.0, c=0.0, rho_h=0.0, lie=0.0); base.update(kw)
        hit = [r for r in t1 if all(abs(float(r[k]) - v) < 1e-9 for k, v in base.items())]
        return [100 * float(hit[0]['famine_k%d' % k]) for k in range(10)]

    def second(q, Yc, rho_err):
        hit = [r for r in t2 if float(r['q']) == q and int(r['Yc']) == Yc and float(r['rho_err']) == rho_err and float(r['rho_G']) == 0 and int(r['mem']) == 0]
        return [100 * float(hit[0]['famine_k%d' % k]) for k in range(10)]

    def cell(x): return ('%.1f' % x).rstrip('0').rstrip('.') if 0 < x < 0.95 else '%d' % int(x + 0.5)
    rows = [("Nothing changed (master right 80)", first()), ("Master right 90", first(q=0.9)), ("Master right 99", first(q=0.99)),
            ("Master misdirects, one known day in ten", first(lie=0.1)), ("Master misdirects, three days in ten", first(lie=0.3)),
            ("The same, master right 99", first(q=0.99, lie=0.3)), ("Master's errors come in slumps", first(rho_h=0.5)), ("The same, master right 90", first(q=0.9, rho_h=0.5)),
            ("Readers have bad weeks; master does not", first(rho_err=0.5)), ("Readers and master both have bad weeks", first(rho_err=0.5, rho_h=0.5)),
            ("Readers share a blindness, 3 days in 10", first(c=0.3)), ("The sea remembers yesterday", first(rho_G=0.9)), ("Self-serving master; readers' bad weeks", second(0.8, 2, 0.5))]
    tests = []
    for name, f in rows:
        line = '| ' + name + ' | ' + ' | '.join(cell(f[k]) for k in (0, 1, 2, 3, 5, 9)) + ' |'
        tests.append((line in book, line, name))
    out.append(('Chapter 11 §5, table', 'famine, in seasons of a hundred, by how many of the nine boats follow the master', 'code/rig/results_town/town_stress_00.csv, code/rig/results_town2/town_stress2.csv', tests))

    # Chapter 14 §5C: the first sweep
    summ = rd('code', 'rig', 'hank_port', 'results_sweep_fast', 'SWEEP_SUMMARY.md')
    MAP = [('The real rate is higher under the tax', 'GE transmission: r_model > r_ctrl'), ('Asset demand is lower at fixed prices', 'asset demand falls at fixed prices'),
           ('Half the dose moves the rate less', 'dose: half dose gives smaller dr'), ('More schedule entropy raises the rate', 'P-E: dr*/dS > 0'),
           ('Stability beats the equal-dollar transfer on welfare', 'P-B GE: stability beats wage on welfare'), ('More low-skill households hand to mouth under the tax', 'HtM_low higher in model (GE)'),
           ('The gap stays positive after liquidity is repaired', 'P-C GE: residual > 0 after liquidity repair'), ('Stability beats the transfer on hand-to-mouth status', 'P-B GE: stability beats wage on HtM'),
           ('Time beats cash on hand-to-mouth status', 'P-A\' GE: time beats money'), ('Time beats cash on hand-to-mouth status, prices fixed', 'P-A\' PE: time beats money')]

    def pc(share, draws):
        # the summary prints shares to three decimals; the count of economies is recovered first, so that nothing is rounded twice
        count = int(share * draws + 0.5); p = 100.0 * count / draws
        return '100' if count == draws else (('%.1f' % p) if p >= 99.5 else '%d' % int(p + 0.5))
    tests = []
    for bookrow, key in MAP:
        m = re.search(r'^\| ' + re.escape(key) + r' \| (\S+) \((\d+)\) \| (\S+) \((\d+)\) \| (\S+) \((\d+)\) \|', summ, re.M)
        line = '| ' + bookrow + ' | ' + ' | '.join(pc(float(m.group(k)), int(m.group(k + 1))) for k in (1, 3, 5)) + ' |' if m else '(row missing from the summary)'
        tests.append((line in book, line, bookrow))
    out.append(('Chapter 14 §5C, table', 'the share of drawn economies, in a hundred, in which each signed claim holds', 'code/rig/hank_port/results_sweep_fast/SWEEP_SUMMARY.md', tests))

    # Chapter 13 §2D: the survey
    fl, oos, pan = rd('code', 'field', 'results', 'shed_first_look.md'), rd('code', 'field', 'results', 'shed_oos_test.md'), rd('code', 'field', 'results', 'shed_panel_test.md')

    def num(text, pat, grp=1): return float(re.search(pat, text, re.M).group(grp).replace(',', ''))

    def rec(where, sentence, f, items):
        tests = []
        for got, printed in items:
            want = float(re.search(r'-?\d[\d,]*(?:\.\d+)?', printed).group(0).replace(',', '')); d = digits(printed)
            tests.append((sentence in book and printed in sentence and abs(got - want) <= 0.5 * 10 ** -d + 1e-9, _f(got) if got < 1000 else '%d' % got, printed))
        out.append((where, sentence, f, tests))
    rec('Chapter 13 §2D', 'from 28 percent of employees in the lowest band to 11 in the highest', 'code/field/results/shed_first_look.md',
        [(num(fl, r'^\| Less than \$10,000 \| (\S+)%'), '28'), (num(fl, r'^\| \$150,000 or more \| (\S+)%'), '11')])
    rec('Chapter 13 §2D', 'more often just getting by or worse (7 points), more often without three months of savings (5), more often unable to meet a four-hundred-dollar expense (3), and more often behind on bills because income varied (11)',
        'code/field/results/shed_first_look.md',
        [(num(fl, r'^\| strained \| pooled \| \S+ \[.*?\] \| \+?(\S+) \['), '(7 points)'), (num(fl, r'^\| nofund3 \| pooled \| \S+ \[.*?\] \| \+?(\S+) \['), '(5)'),
         (num(fl, r'^\| cant400 \| pooled \| \S+ \[.*?\] \| \+?(\S+) \['), '(3)'), (num(fl, r'^\| billvar \| pooled \| \S+ \[.*?\] \| \+?(\S+) \['), '(11)')])
    rec('Chapter 13 §2D', 'and 2021 files, which had not been opened (18,268 employees)', 'code/field/results/shed_oos_test.md', [(num(oos, r'Pooled out-of-sample: (\d+) employees'), '18,268')])
    h1 = r'^\| %s \| pooled 2019–2021 \| \S+ \[.*?\] \| \S+ \[.*?\] \| \+?(\S+) \['
    rec('Chapter 13 §2D', '7.5 points on just getting by, 5.5 on bills, 2.4 on the four-hundred-dollar expense, each distinguishable from zero, and 1.5 on the three-month fund', 'code/field/results/shed_oos_test.md',
        [(num(oos, h1 % 'strained'), '7.5'), (num(oos, h1 % 'billvar'), '5.5'), (num(oos, h1 % 'cant400'), '2.4'), (num(oos, h1 % 'nofund3'), '1.5')])
    rec('Chapter 13 §2D', '4,816 employees, 7,390 pairs of adjacent years', 'code/field/results/shed_panel_test.md',
        [(num(pan, r'adjacent-wave pairs from (\d+) persons'), '4,816'), (num(pan, r'Sample: (\d+) adjacent-wave pairs'), '7,390')])
    rec('Chapter 13 §2D', 'person is 3.0 points more likely to be just getting by and 6.1 points more likely to be behind on bills', 'code/field/results/shed_panel_test.md',
        [(num(pan, r'^\| strained \| \+?(\S+) \['), '3.0'), (num(pan, r'^\| billvar \| \+?(\S+) \['), '6.1')])
    rec('Chapter 13 §2D', 'measures (5.6 and 3.8 points)', 'code/field/results/shed_panel_test.md',
        [(num(pan, r'^\| strained \| \S+ \[.*?\] \| \S+ \[.*?\] \| \+?(\S+) \['), '5.6'), (num(pan, r'^\| billvar \| \S+ \[.*?\] \| \S+ \[.*?\] \| \+?(\S+) \['), '3.8')])
    return out


# ------------------------------------------------------------------------------------------------ running
def run_script(work, script, limit):
    env = dict(os.environ, MPLBACKEND='Agg', PYTHONIOENCODING='utf-8', PYTHONUTF8='1')
    path = os.path.join(work, *script.split('/')); t0 = time.time()
    try:
        r = subprocess.run([sys.executable, os.path.basename(path)], cwd=os.path.dirname(path), env=env, capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=limit)
        return r.returncode, r.stdout, r.stderr, time.time() - t0
    except subprocess.TimeoutExpired as ex:
        return 124, (ex.stdout or b'').decode('utf-8', 'replace') if isinstance(ex.stdout, bytes) else (ex.stdout or ''), 'stopped after %d seconds' % limit, time.time() - t0


def main(argv):
    do_all = '--all' in argv; only = argv[argv.index('--only') + 1] if '--only' in argv else None
    plan = FAST + (LONG if do_all else [])
    if only: plan = [p for p in FAST + LONG if only in p[0]]
    md = manuscript(); book = squash(open(md, encoding='utf-8').read())
    if '--list' in argv:
        print('Runs by default (seconds are from one laptop-class processor):')
        for s, secs, checks in FAST: print('  %-44s %4d s   %d checks' % (s, secs, sum(len(c[2]) for c in checks)))
        print('Added by --all:')
        for s, secs, checks in LONG: print('  %-44s %4d s   %d checks' % (s, secs, sum(len(c[2]) for c in checks)))
        print('Read from results files in the repository (nothing re-run):')
        for where, sentence, f, tests in recorded_checks(book): print('  %-24s %2d checks from %s' % (where, len(tests), f))
        print('Not re-run by this command:')
        for s, what, why, how in NOT_RUN: print('  %s\n      %s. %s.\n      To run: %s' % (s, what, why, how))
        return 0

    lines = []; n_ok = n_bad = 0; failed = []

    def say(s=''):
        print(s, flush=True); lines.append(s)

    say('# Reproduction report'); say()
    say('Manuscript: `docs/%s`. Python %s on %s. %s.' % (os.path.basename(md), platform.python_version(), platform.system(), time.strftime('%Y-%m-%d')))
    say('A number passes when the value a script prints, rounded the way the book prints it, is the book\'s number.'); say()
    work = tempfile.mkdtemp(prefix='price_of_agency_')
    try:
        shutil.copytree(os.path.join(ROOT, 'code'), os.path.join(work, 'code'), ignore=shutil.ignore_patterns('.venv', '__pycache__', 'curves', '*.npz', '*.jsonl'))
        os.makedirs(os.path.join(work, 'figures')); os.makedirs(os.path.join(work, 'docs'))
        say('## Ran here'); say()
        for script, secs, checks in plan:
            rc, out, err, took = run_script(work, script, max(600, secs * 8))
            print('   (%s: %.0f s)' % (script, took), flush=True)
            if rc != 0:
                n_bad += 1; failed.append(script)
                say('**FAIL** `%s` did not finish (exit %d): %s' % (script, rc, squash(err)[-300:])); say(); continue
            say('`%s`' % script); say()
            for where, sentence, tests in checks:
                in_book = squash(sentence) in book
                for test, printed in tests:
                    try: ok, got, want = test(out)
                    except Exception as ex: ok, got, want = False, 'could not be read (%s)' % ex, printed
                    ok = ok and in_book and (printed in sentence)
                    n_ok += ok; n_bad += (not ok)
                    if not ok: failed.append('%s: %s' % (script, printed))
                    say('- %s  **%s** — computed %s. %s: “%s”%s' % ('ran ' if ok else 'FAIL', want, got, where, sentence, '' if in_book else '  [THIS SENTENCE IS NOT IN THE MANUSCRIPT]'))
            say()
        if not only:
            say('## Recorded: read from results files in the repository, not re-run'); say()
            for where, sentence, f, tests in recorded_checks(book):
                say('`%s` — %s: “%s”' % (f, where, sentence)); say()
                for ok, got, printed in tests:
                    n_ok += bool(ok); n_bad += (not ok)
                    if not ok: failed.append('%s: %s' % (f, printed))
                    say('- %s  **%s** — in the file: %s' % ('recorded' if ok else 'FAIL', printed, got))
                say()
            say('## Not re-run by this command'); say()
            if not do_all:
                for s, secs, checks in LONG: say('- `%s` — a long exact search (about %d minutes). Run `python reproduce.py --all`.' % (s, max(1, round(secs / 60))))
            for s, what, why, how in NOT_RUN: say('- `%s` — %s. Not re-run: %s. To run it: %s.' % (s, what, why, how))
            say()
    finally:
        shutil.rmtree(work, ignore_errors=True)
    say('## Result'); say()
    say('%d checks. %d match the book, %d do not.' % (n_ok + n_bad, n_ok, n_bad))
    for f in failed: say('- does not match: %s' % f)
    if not only:
        open(os.path.join(ROOT, 'REPRODUCE_REPORT.md'), 'w', encoding='utf-8', newline='\n').write('\n'.join(lines) + '\n')
        print('\nwritten to REPRODUCE_REPORT.md')
    return 0 if n_bad == 0 else 1


if __name__ == '__main__':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass
    sys.exit(main(sys.argv[1:]))
