"""build_book.py -- the designed edition, built from the markdown manuscript.

    python design/build_book.py [docs/THE_PRICE_OF_AGENCY_unified_vX.YY.md]

The manuscript stays the source. This script (1) sets the plain-text formulas as mathematics (design/mathmap.py),
(2) reads the manuscript's own structure -- parts, chapters, the six numbered sections of each chapter -- and marks each
section as for every reader, machinery, receipts, or fenced, (3) writes design/book.tex against design/bookstyle.tex, and
(4) runs xelatex. Figures are placed by design/figures.py. Nothing here adds or changes a sentence of the book; the only
new words are the key to the page markings, the figure captions, and the labels in the margin.
"""
import os, re, sys, json, subprocess, glob

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, HERE)
import mathmap as MM
try:
    import figures as FIG
except Exception:                                   # the book builds without pictures
    FIG = None

PANDOC_IN = 'markdown-simple_tables-multiline_tables-grid_tables'          # pipe tables are the manuscript's tables
E, M, R, F = 'everyone', 'machinery', 'receipts', 'fenced'
PART_TITLES = {'I': 'The Verdict and the Appeal', 'II': 'One Agent: The Anatomy of Freedom',
               'III': 'Watchers: Freedom Is Relative to an Observer', 'IV': 'Towns: Freedom Is Social', 'V': 'The Ledger'}
VOCAB = {'PROVEN', 'EXACT', 'NUMERICAL', 'MC', 'SIMULATION', 'DATA', 'CONJECTURE', 'CONJECTURED', 'SPECULATIVE', 'REFUTED',
         'OPEN', 'ARGUMENT', 'CONCEPT', 'INTERPRETATION', 'FRAMING', 'BEGUN', 'SURFACE'}
NOTES = {M: r'\textbf{The machinery}\\for those who want it', R: r'\textbf{The receipts}\\for anyone who\\trusts nothing',
         F: r'\textbf{Fenced}\\a conjecture; nothing\\later depends on it'}
MAPCODE = {E: 0, M: 1, R: 2, F: 3}
PANEL = {E: 'panelplain', M: 'panelmach', R: 'panelrcpt', F: 'panelfence'}


def track_of(ch, sec):
    """Which kind of text a numbered section is. The book says it itself: '§1-2 are for every reader; §3 onward for those
    who want the machinery; §6 for anyone who trusts nothing.' Chapters 12-15 depart from the template and are listed."""
    if ch == 12:
        return R if sec == '6' else F
    if ch == 13:
        return {'1': E, '2': E, '2B': M, '2C': M, '2D': R, '3': M, '4': M, '5': M, '6': R}[sec]
    if ch == 14:
        return {'1': E, '2': E, '3': E, '4': E, '5': E, '5B': E, '5C': M, '6': R}[sec]
    if ch == 15:
        return {'1': E, '2': M, '3': M, '4': M, '5': E, '6': E}[sec]
    return {'1': E, '2': E, '3': M, '4': M, '5': M, '6': R}[sec]


# ------------------------------------------------------------------------------------------------ text helpers
def tex(s):
    out = []
    for c in s:
        out.append({'\\': r'\textbackslash{}', '&': r'\&', '%': r'\%', '#': r'\#', '_': r'\_', '$': r'\$', '{': r'\{', '}': r'\}',
                    '~': r'\textasciitilde{}', '^': r'\textasciicircum{}'}.get(c, c))
    return ''.join(out)


def breakable(s):
    """file paths and identifiers: allow a line break after / _ and ."""
    return re.sub(r'(/|\\_|(?<=\w)\.(?=\w))', r'\1\\allowbreak{}', tex(s))


def flat(inl):
    out = ''
    for x in inl:
        t = x['t']
        if t == 'Str': out += x['c']
        elif t in ('Space', 'SoftBreak'): out += ' '
        elif t in ('Strong', 'Emph'): out += flat(x['c'])
        elif t == 'Quoted': out += '“' + flat(x['c'][1]) + '”'
        elif t == 'Code': out += x['c'][1]
        elif t == 'Math': out += '$' + x['c'][1] + '$'
    return out


def Str(s): return {'t': 'Str', 'c': s}
def RawI(s): return {'t': 'RawInline', 'c': ['latex', s]}
def RawB(s): return {'t': 'RawBlock', 'c': ['latex', s]}
SP = {'t': 'Space'}


def to_tex_inline(inl):
    """render a list of inlines to LaTeX with pandoc"""
    doc = {'pandoc-api-version': API, 'meta': {}, 'blocks': [{'t': 'Plain', 'c': inl}]}
    return subprocess.run(['pandoc', '-f', 'json', '-t', 'latex'], input=json.dumps(doc), capture_output=True, text=True).stdout.strip()


# ------------------------------------------------------------------------------------------------ mathematics
def apply_math(md):
    lines = md.split('\n')
    # the indented formula blocks become placeholders
    text = md
    for i, (src, _) in enumerate(MM.DISPLAY):
        block = '\n'.join('    ' + l for l in src.split('\n'))
        assert text.count('\n\n' + block + '\n') == 1, f"formula block not found exactly once: {src[:50]!r}"
        text = text.replace('\n\n' + block + '\n', f'\n\nDISPLAYMATH{i:02d}X\n', 1)
    # chapter scopes
    marks = [(m.start(), m.group(1)) for m in re.finditer(r'^#{1,2} (Chapter \d+|Coda|APPENDICES|PART [IVX]+)', text, re.M)]
    bounds = {}
    for k, (pos, name) in enumerate(marks):
        end = marks[k + 1][0] if k + 1 < len(marks) else len(text)
        key = ('ch' + name.split()[1]) if name.startswith('Chapter') else {'Coda': 'coda', 'APPENDICES': 'appx'}.get(name)
        if key: bounds[key] = (pos, end)
    for key, old, new in MM.SPECIFIC:
        a, b = bounds[key]
        pat = re.compile(r'\s+(?:>\s+)?'.join(re.escape(w) for w in old.split(' ')))
        seg = text[a:b]; found = pat.findall(seg)
        assert len(found) == 1, f"[{key}] expected once, found {len(found)}: {old[:70]!r}"
        seg2 = pat.sub(lambda m: new, seg, count=1)
        delta = len(seg2) - len(seg); text = text[:a] + seg2 + text[b:]
        for k2, (a2, b2) in list(bounds.items()):
            if a2 >= b: bounds[k2] = (a2 + delta, b2 + delta)
            elif k2 == key: bounds[k2] = (a2, b2 + delta)

    def outside(text, fn):
        parts = re.split(r'(\$[^$\n]*\$|`[^`]*`)', text)
        return ''.join(fn(p) if i % 2 == 0 else p for i, p in enumerate(parts))
    for pat, rep_ in MM.GLOBAL:
        text = outside(text, lambda p: re.sub(pat, rep_, p))
    # "$x$ = 0.75" -> "$x = 0.75$"
    ops = '|'.join(re.escape(o) for o in MM.MERGE_OPS)
    text = re.sub(r'\$([^$\n]+)\$(\s+)(' + ops + r')\s+(\d+(?:[./]\d+)?)(?![\d])',
                  lambda m: f"${m.group(1)} {MM.MERGE_OPS[m.group(3)]} {m.group(4)}$", text)
    return text


# ------------------------------------------------------------------------------------------------ inline transforms
def tag_kind(tagtext):
    return 1 if len(tagtext) <= 26 else 2


def fix_inlines(inl):
    """tags, code paths, long identifiers; recursive"""
    out = []
    i = 0
    while i < len(inl):
        x = inl[i]; t = x['t']
        if t == 'Strong':
            s = flat(x['c']).strip()
            m = re.match(r'^\[(.+)\]$', s, re.S)
            if m and m.group(1).split()[0].strip('—;:,.') in VOCAB:            # a tag standing alone
                body = m.group(1)
                if tag_kind(body) == 1:
                    out.append(RawI(r'\istamp{' + tex(body) + '}'))
                else:
                    inner = strip_brackets(x['c'])
                    if inner and inner[0]['t'] == 'Str' and inner[0]['c'].strip('—;:,.') in VOCAB:
                        inner = [RawI(r'\tagword{' + inner[0]['c'] + '}')] + inner[1:]
                    inner = fix_inlines(inner)
                    out += [RawI(r'{\sffamily\fontsize{8.6}{12.2}\selectfont\color{trackc}[')] + inner + [RawI(']}')]
                i += 1; continue
            m = re.match(r'^(.+?)\s*\[([^\[\]]+)\]$', s, re.S)
            if m and m.group(2).split()[0].strip('—;:,.') in VOCAB:            # a bold lead ending in a tag
                lead = cut_at_bracket(x['c'])
                out.append({'t': 'Strong', 'c': fix_inlines(lead)})
                body = m.group(2)
                out.append(SP)
                out.append(RawI((r'\istamp{' if tag_kind(body) == 1 else r'{\sffamily\fontsize{8.6}{12.2}\selectfont\color{trackc}[') + tex(body) + ('}' if tag_kind(body) == 1 else ']}')))
                i += 1; continue
            out.append({'t': 'Strong', 'c': fix_inlines(x['c'])}); i += 1; continue
        if t == 'Emph':
            out.append({'t': 'Emph', 'c': fix_inlines(x['c'])}); i += 1; continue
        if t == 'Quoted':
            out.append({'t': 'Quoted', 'c': [x['c'][0], fix_inlines(x['c'][1])]}); i += 1; continue
        if t == 'Code':
            out.append(RawI(r'\texttt{' + breakable(x['c'][1].replace('/ ', '/')) + '}')); i += 1; continue
        if t == 'Str':
            s = x['c']
            w = s.lstrip('[').strip('—;:,.]')
            if s.startswith('[') and w in VOCAB:                                 # a tag in running text: find its closing bracket
                j = i; span = []
                while j < len(inl):
                    span.append(inl[j])
                    if inl[j]['t'] == 'Str' and ']' in inl[j]['c']: break
                    j += 1
                closed = j < len(inl)
                body = flat(span).strip()
                mm = re.match(r'^\[([^\[\]]+)\]([.,;:]?)$', body)
                if closed and mm and tag_kind(mm.group(1).rstrip('.')) == 1:
                    out.append(RawI(r'\istamp{' + tex(mm.group(1).rstrip('.')) + '}' + mm.group(2)))
                    i = j + 1; continue
                for y in (span if closed else [x]):                              # long: letter-space the tag words, keep the rest
                    if y['t'] == 'Str':
                        pieces = re.split(r'\b(' + '|'.join(sorted(VOCAB, key=len, reverse=True)) + r')\b', y['c'])
                        for k, p in enumerate(pieces):
                            if not p: continue
                            out.append(RawI(r'\tagword{' + p + '}') if k % 2 else Str(p))
                    else:
                        out += fix_inlines([y])
                i = (j + 1) if closed else (i + 1); continue
            if ('/' in s or '_' in s) and len(s) > 14 and not s.startswith('$'):
                out.append(RawI(breakable(s))); i += 1; continue
        out.append(x); i += 1
    return out


def strip_brackets(inl):
    inl = json.loads(json.dumps(inl))
    for x in inl:
        if x['t'] == 'Str': x['c'] = x['c'].lstrip('['); break
    for x in reversed(inl):
        if x['t'] == 'Str': x['c'] = x['c'].rstrip(']'); break
    return inl


def cut_at_bracket(inl):
    out = []
    for x in inl:
        if x['t'] == 'Str' and x['c'].startswith('['): break
        out.append(x)
    while out and out[-1]['t'] in ('Space', 'SoftBreak'): out.pop()
    return out


RULED_PARAGRAPHS = ['The staircase was the first paper.', 'One argument, made by the author of the two papers']      # Chapter 2

CLAIMS = []                # every stated theorem, proposition, corollary and result, in order, for the index

CLAIM = re.compile(r'^((?:Theorem|Proposition|Corollary|Result|Lemma)(?:\s[0-9R][0-9.]*[a-z′]?)?|S[0-9]+)\s+\((.+?)\)\.(?:\s*\[(.+)\])?\s*$', re.S)


def table_block(b):
    """a pipe table of the manuscript, set in the small sans as ruled rows; columns share the width by how much they hold.
    Each row is its own line of top-aligned boxes, so a long table can run over a page break between rows."""
    colspecs, head, bodies = b['c'][2], b['c'][3], b['c'][4]
    rows = [[c[4] for c in r[1]] for r in head[1]]; nhead = len(rows)
    for body in bodies: rows += [[c[4] for c in r[1]] for r in body[3]]
    cells = [[(blk[0]['c'] if blk else []) for blk in r] for r in rows]
    ncol = len(colspecs); right = [cs[0]['t'] == 'AlignRight' for cs in colspecs]
    need = []
    for j in range(ncol):
        body_len = max((len(flat(r[j])) for r in cells[nhead:]), default=1)
        head_word = max((len(w) for r in cells[:nhead] for w in flat(r[j]).split()), default=1)
        need.append(max(min(body_len, 44) if not right[j] else min(body_len, 12) + 1, head_word + 1, 5))
    avail = 1.0 - (ncol - 1) * 0.0255                      # 8pt between columns, as a share of the text block
    frac = [avail * x / sum(need) for x in need]
    lines = [r'\begin{booktable}']
    for i, r in enumerate(cells):
        tex_cells = [to_tex_inline(fix_inlines(c)) if c else '' for c in r]
        if i < nhead: tex_cells = [r'\textbf{%s}' % x for x in tex_cells]
        boxes = [r'\parbox[t]{%.4f\linewidth}{\%s\strut %s\strut}' % (frac[j], 'raggedleft' if right[j] else 'raggedright', x) for j, x in enumerate(tex_cells)]
        lines.append(r'\tablerow{' + r'\hspace{8pt}'.join(boxes) + '}' + (r'\tablerule' if i in (nhead - 1, len(cells) - 1) else r'\tablehair')
                     + (r'\nobreak' if i in (nhead - 1, nhead, len(cells) - 2) else ''))
    lines.append(r'\end{booktable}')
    return RawB('\n'.join(lines))


def fix_blocks(blocks, state):
    """block-level transforms inside a section"""
    out = []
    for b in blocks:
        t = b['t']
        if t == 'Table':
            tb = table_block(b)
            if out and out[-1]['t'] == 'Para' and len(flat(out[-1]['c'])) < 330:    # a short sentence that introduces the table stays with its first rows
                out.insert(len(out) - 1, RawB(r'\tableneed{%dpt}' % (70 + 12 * (1 + len(flat(out[-1]['c'])) // 85))))
            else:
                out.append(RawB(r'\tableneed{60pt}'))
            out.append(tb); state['noindent'] = True; continue
        if t == 'Para' or t == 'Plain':
            c = b['c']
            if len(c) == 1 and c[0]['t'] == 'Str' and re.match(r'^DISPLAYMATH\d\dX$', c[0]['c']):
                k = int(c[0]['c'][11:13])
                out.append(RawB('\\begin{dispmath}' + MM.DISPLAY[k][1] + '\\end{dispmath}'))
                state['noindent'] = True; continue
            if t == 'Para' and c and c[0]['t'] == 'Strong':
                s = flat(c[0]['c']).strip(); m = CLAIM.match(s)
                if m:
                    label, name, tag = m.group(1), m.group(2), m.group(3)
                    kind = 0 if not tag else tag_kind(tag)
                    out.append(RawB(r'\claimhead{%s}{%s}{%s}{%d}' % (tex(label), tex(name), tex(tag or ''), kind)))
                    ref = 'claim-%d' % len(CLAIMS); CLAIMS.append((tex(label), tex(name), ref)); out.append(RawB(r'\label{%s}' % ref))
                    rest = c[1:]
                    while rest and rest[0]['t'] in ('Space', 'SoftBreak'): rest = rest[1:]
                    if rest: out.append({'t': 'Para', 'c': [RawI(r'\noindent ')] + fix_inlines(rest)})
                    continue
                if s.startswith('Axiom 1.') and len(c) >= 3 and c[-1]['t'] == 'Strong':
                    a1 = flat(c[0]['c']).split('. ', 1)[1]; a2 = flat(c[-1]['c']).split('. ', 1)[1]
                    out.append(RawB(r'\axioms{%s}{%s}' % (tex(a1), tex(a2)))); continue
            if t == 'Para' and len(c) == 1 and c[0]['t'] == 'Emph' and c[0]['c'] and c[0]['c'][0]['t'] == 'Quoted':
                s = flat(c[0]['c'])
                if len(s) < 90:
                    out.append(RawB(r'\saying{' + to_tex_inline(c[0]['c']) + '}')); continue
                out.append(RawB(r'\begin{quote}\itshape ' + to_tex_inline(fix_inlines(c[0]['c'])) + r'\end{quote}')); continue
            c2 = fix_inlines(c)
            pre = []
            if state.get('pending_note'):
                pre.append(RawI(r'\noindent\ledgerput{{\tracknotefont ' + state.pop('pending_note') + '}}')); state['noindent'] = False
            if state.get('noindent') and t == 'Para':
                pre.append(RawI(r'\noindent ')); state['noindent'] = False
            out.append({'t': t, 'c': pre + c2})
            if FIG:
                s = flat(c)
                for fig in FIG.FIGURES:
                    if fig.get('placed'): continue
                    if fig['after'] in re.sub(r'\s+', ' ', s) and state['chapter'] == fig['chapter']:
                        state['fignum'][fig['chapter']] = state['fignum'].get(fig['chapter'], 0) + 1
                        pre_ = str(fig['chapter']) if isinstance(fig['chapter'], int) else {'coda': 'C', 'appx': 'A', 'front': '0'}.get(fig['chapter'], fig['chapter'].replace('part', ''))
                        num = f"{pre_}.{state['fignum'][fig['chapter']]}"
                        macro = r'\booktikz' if fig['file'].endswith('.tex') else (r'\bookfigurewide' if fig.get('wide') and state['track'] == E else r'\bookfigure')
                        if state['track'] == E and not state.get('in_quote'): macro += 'float'       # story pages: the text runs on past a picture that has to wait for the next page
                        out.append(RawB('%s{%s}{%s}{%s}' % (macro, 'fig/' + fig['file'], num, fig['caption'])))
                        fig['placed'] = True; state['noindent'] = False
            continue
        if t == 'BulletList':
            out.append({'t': t, 'c': [fix_blocks(item, state) for item in b['c']]}); continue
        if t == 'OrderedList':
            out.append({'t': t, 'c': [b['c'][0], [fix_blocks(item, state) for item in b['c'][1]]]}); continue
        if t == 'BlockQuote':
            tr = state['track']; inner = fix_blocks(b['c'], state)
            if tr != E: out.append(RawB('\\end{%s}' % tr))
            out.append(RawB('\\begin{%s}' % PANEL[tr])); out += inner; out.append(RawB('\\end{%s}' % PANEL[tr]))
            if tr != E: out.append(RawB('\\begin{%s}[before skip=0pt]{}\\global\\firstsectfalse' % tr))
            continue
        if t == 'HorizontalRule':
            continue
        out.append(b)
    return out


# ------------------------------------------------------------------------------------------------ structure
REPO = 'https://github.com/RandomInternetPreson/price-of-agency'
DOI = '10.5281/zenodo.24599088'      # reserved on Zenodo for draft v0.50. A later draft is a new version there and gets its own: change it with the draft


def STEM(printed): return 'book_print' if printed else 'book'


def colophon_page(version, printed):
    """the page behind the title: where the files are, and how to cite the book"""
    import time
    lines = [r'\textbf{The Price of Agency.} Draft %s, %s.' % (version, time.strftime('%B %Y')),
             r'Every script, results file and preregistration named in this book is in its repository:\\ \url{%s}' % REPO,
             r'To cite it: Aaron Alai, with Claude (Anthropic) as mathematical collaborator, \textit{The Price of Agency: Freedom, measured. '
             r'Theft, priced. No opinions required.} Draft %s, %s. \url{%s} \ doi:%s' % (version, time.strftime('%Y'), REPO, DOI),
             r'\textcopyright\ %s Aaron Alai. The text and figures may be copied, translated and built on, for any purpose, with credit '
             r'(Creative Commons Attribution 4.0 International). The code may be used for anything (MIT).' % time.strftime('%Y'),
             r'The physics it stands on: arXiv:2608.00124 and arXiv:2608.18886.']
    if not printed: lines.append(r"The cover: two hundred and fifty mornings under Vera's second wiring (Chapter 9).")
    lines.append(r'Set in TeX Gyre Pagella and Fira Sans, and built from the manuscript by the scripts in \texttt{design/}.')
    return (r'\clearpage\thispagestyle{empty}\vspace*{\fill}' + '\n' + r'\noindent\parbox[b]{\textwidth}{\raggedright\sffamily\fontsize{7.8}{11.4}\selectfont\color{ink}' + '\n'
            + ('\\par\\vspace{7pt}\n').join(lines) + '}')


def build(md_path, printed=False):
    global API
    md = open(md_path, encoding='utf-8').read()
    version = re.search(r'draft (v[\d.]+)', md).group(1)
    md = apply_math(md)
    ast = json.loads(subprocess.run(['pandoc', '-f', PANDOC_IN, '-t', 'json'], input=md, capture_output=True, text=True).stdout)
    API = ast['pandoc-api-version']
    blocks = ast['blocks']

    # pass 1: the outline
    outline = []; part = None; chap = None
    for b in blocks:
        if b['t'] != 'Header': continue
        lvl, title = b['c'][0], flat(b['c'][2]).strip()
        m = re.match(r'^PART ([IVX]+)\b', title)
        if m:
            part = {'kind': 'part', 'num': m.group(1), 'title': PART_TITLES[m.group(1)], 'label': 'part' + m.group(1), 'chapters': [], 'essays': []}
            outline.append(part); chap = None; continue
        m = re.match(r'^Chapter (\d+)\.\s+(.*)$', title)
        if m:
            chap = {'kind': 'chapter', 'num': int(m.group(1)), 'title': m.group(2), 'label': 'ch' + m.group(1), 'sections': [], 'part': part}
            outline.append(chap); part['chapters'].append(chap); continue
        if title.startswith('Coda.'):
            chap = {'kind': 'chapter', 'num': 'coda', 'title': title.split('. ', 1)[1], 'label': 'coda', 'sections': [], 'part': None}
            outline.append(chap); continue
        if title == 'APPENDICES':
            chap = {'kind': 'chapter', 'num': 'appx', 'title': 'Appendices', 'label': 'appx', 'sections': [], 'part': None}
            outline.append(chap); continue
        m = re.match(r'^§(\w+)\.\s+(.*)$', title)
        if m and chap:
            sec = m.group(1)
            chap['sections'].append({'sec': sec, 'title': m.group(2), 'track': track_of(chap['num'], sec), 'label': f"{chap['label']}-s{sec}"})
        elif lvl == 2 and part and chap is None and title != 'How to read this book':
            part['essays'].append((title, 'sec-' + re.sub(r'\W+', '-', title.lower())))      # the essays that open a part, before its first chapter
    order = [o for o in outline if o['kind'] == 'chapter']

    def next_everyone(ch, sec_index):
        """label of the next place written for every reader after section sec_index of chapter ch"""
        for s in ch['sections'][sec_index + 1:]:
            if s['track'] == E: return s['label']
        k = outline.index(ch)                       # the next chapter, or the part that opens before it
        return outline[k + 1]['label'] if k + 1 < len(outline) else None

    def short(title):
        for a, b in (('The idea, in plain words', 'The idea'), ('The model, and what it covers', 'The model'), ('The model, and its audits', 'The model'),
                     ('The code, and the record', 'The code')):
            if title == a: return b
        if title.startswith('The story:'): return 'The story'
        return title

    # pass 2: emit
    out = []; state = {'track': E, 'chapter': None, 'fignum': {}}
    cur = {'open': None}

    def close_track():
        if cur['open'] and cur['open'] != E: out.append(RawB('\\end{%s}' % cur['open']))
        cur['open'] = None; state['track'] = E

    def open_track(tr, note):
        close_track()
        if tr != E: out.append(RawB('\\begin{%s}{%s}' % (tr, note)))
        cur['open'] = tr; state['track'] = tr

    i = 0; chap = None; body = []; seen_title = False

    def flush():
        nonlocal body
        if body: out.extend(fix_blocks(body, state)); body = []

    for b in blocks:
        if b['t'] != 'Header':
            if not seen_title: continue
            body.append(b); continue
        flush()
        lvl, title = b['c'][0], flat(b['c'][2]).strip()
        if title == 'THE PRICE OF AGENCY' or lvl == 3:
            continue
        if title == 'How to read this book':
            seen_title = True; state['chapter'] = 'front'
            out.append(RawB(r'\frontsect{How to read this book}{front-howto}')); continue
        m = re.match(r'^PART ([IVX]+)\b', title)
        if m:
            close_track(); p = next(o for o in outline if o['kind'] == 'part' and o['num'] == m.group(1))
            lst = ''.join(r'\partline{%s}{%s}{%s}' % (c['num'], tex(c['title']), c['label']) for c in p['chapters'])
            out.append(RawB(r'\renewcommand{\partlist}{%s}\partopen{%s}{%s}{%s}\renewcommand{\runninghead}{%s}' % (lst, p['num'], tex(p['title']), p['label'], tex(p['title']))))
            state['chapter'] = 'part' + p['num']; chap = None; continue
        m = re.match(r'^Chapter (\d+)\.\s+(.*)$', title)
        if m or title.startswith('Coda.') or title == 'APPENDICES':
            close_track()
            key = int(m.group(1)) if m else ('coda' if title.startswith('Coda.') else 'appx')
            chap = next(c for c in order if c['num'] == key); state['chapter'] = key
            top = ('Part %s. %s' % (chap['part']['num'], chap['part']['title'])) if chap['part'] else ('Coda' if key == 'coda' else '')
            numeral = str(key) if isinstance(key, int) else ''
            out.append(RawB(r'\chapteropen{%s}{%s}{%s}{%s}' % (tex(top), numeral, tex(chap['title']), chap['label'])))
            if chap['sections']:
                cells = []
                for k, s in enumerate(chap['sections']):
                    if k and k % 6 == 0: cells.append(r'\maprowbreak ')
                    cells.append(r'\mapcellbox{%d}{§\,%s}{%s}{%s}' % (MAPCODE[s['track']], s['sec'], tex(short(s['title'])), s['label']))
                out.append(RawB(r'\routemap{' + ''.join(cells) + '}'))
            if key == 'appx':
                open_track(R, ''); state['pending_note'] = NOTES[R]
                out.append(RawB(r'\setlength{\parskip}{7pt}\setlength{\parindent}{0pt}'))
            continue
        m = re.match(r'^§(\w+)\.\s+(.*)$', title)
        if m and chap:
            k = next(j for j, s in enumerate(chap['sections']) if s['sec'] == m.group(1)); s = chap['sections'][k]
            if s['track'] != cur['open']:
                note = ''
                if s['track'] != E:
                    note = NOTES[s['track']]
                    if s['track'] in (M, F):
                        nxt = next_everyone(chap, k)
                        if nxt: note += r'\\[3pt]{\color{muted}Story resumes:\\page~\pageref{%s}}' % nxt
                open_track(s['track'], note)
            out.append(RawB(r'\sect{§\,%s}{%s}{%s}' % (s['sec'], tex(s['title']), s['label']))); continue
        # an unnumbered section (the two essays that open Part V)
        close_track(); out.append(RawB(r'\plainsect{%s}{%s}' % (tex(title), 'sec-' + re.sub(r'\W+', '-', title.lower())))); continue
    flush(); close_track()

    # Part I has no numbered sections, so its two passages of machinery are named here by their opening words
    for opening in RULED_PARAGRAPHS:
        hits = [k for k, b in enumerate(out) if b['t'] == 'Para' and flat(b['c']).lstrip().startswith(opening)]
        if len(hits) != 1: raise SystemExit(f'ruled paragraph not found exactly once: {opening!r} ({len(hits)})')
        k = hits[0]
        out[k] = {'t': 'Para', 'c': [RawI(r'\rulednote{%s}' % NOTES[M])] + out[k]['c']}
        out.insert(k + 1, RawB(r'\end{ruled}')); out.insert(k, RawB(r'\begin{ruled}'))

    # the key to the page markings goes where the book explains its own structure
    for k, b in enumerate(out):
        if b['t'] == 'Para' and 'Every chapter is built the same way' in flat(b['c']):
            out.insert(k + 1, RawB(r'\pagekey')); break
    else:
        raise SystemExit('the paragraph that explains the chapter template was not found')

    body_tex = subprocess.run(['pandoc', '-f', 'json', '-t', 'latex', '--wrap=preserve'],
                              input=json.dumps({'pandoc-api-version': API, 'meta': {}, 'blocks': out}), capture_output=True, text=True).stdout
    # contents
    toc = [r'\frontsect{Contents}{front-toc}', r'\tocfront{How to read this book}{front-howto}']
    for o in outline:
        if o['kind'] == 'part':
            toc.append(r'\tocpart{%s}{%s}{%s}' % (o['num'], tex(o['title']), o['label']))
            toc.extend(r'\tocessay{%s}{%s}' % (tex(t), lab) for t, lab in o['essays'])
        elif isinstance(o['num'], int): toc.append(r'\tocchap{%d}{%s}{%s}' % (o['num'], tex(o['title']), o['label']))
        else: toc.append(r'\par\addvspace{13pt}\tocfront{%s}{%s}' % ('Coda: ' + tex(o['title']) if o['num'] == 'coda' else 'Appendices', o['label']))
    toc.append(r'\par\addvspace{13pt}\tocfront{Index}{index}')
    title_page = r'''\begin{titlepage}\thispagestyle{empty}COVERPAGE\vspace*{1.7in}
\noindent\hspace*{-\ledgertotal}\parbox[t]{\dimexpr\textwidth+\ledgertotal}{\raggedright
{\fontsize{44}{48}\selectfont The Price\\[4pt] of Agency}\par\vspace{0.42in}
{\fontsize{14}{20}\selectfont\itshape Freedom, measured. Theft, priced.\\No opinions required.}\par\vspace{2.6in}
{\sffamily\fontsize{11}{15}\selectfont Aaron Alai}\par\vspace{3pt}
{\sffamily\fontsize{9}{13}\selectfont\color{muted}with Claude (Anthropic) as mathematical collaborator}\par\vspace{0.5in}
{\sffamily\fontsize{8}{11}\selectfont\color{muted}Draft %s}}
COLOPHON
\end{titlepage}''' % version
    title_page = (title_page.replace('COVERPAGE', '' if printed else r'\coverpage\clearpage\thispagestyle{empty}')
                  .replace('COLOPHON', colophon_page(version, printed)))
    doc = (('\\def\\PrintEdition{1}' if printed else '') + '\\input{bookstyle}\n'
           '\\begin{document}\n\\pagenumbering{roman}\n' + title_page + '\n\\pagenumbering{arabic}\n' + '\n'.join(toc) + '\n\\clearpage\n' + body_tex + '\n\\IfFileExists{%s_index.tex}{\\input{%s_index}}{}\n\\end{document}\n' % (STEM(printed), STEM(printed)))
    open(os.path.join(HERE, STEM(printed) + '.tex'), 'w', encoding='utf-8').write(doc)
    if FIG:
        missing = [f['after'][:50] for f in FIG.FIGURES if not f.get('placed')]
        if missing: print('FIGURES NOT PLACED:', missing)
    return version


def check(version, printed=False):
    """report what the typesetter could not do"""
    log = open(os.path.join(HERE, STEM(printed) + '.log'), encoding='utf-8', errors='replace').read()
    miss = sorted(set(re.findall(r'Missing character: There is no (.) ', log)))
    over = [float(x) for x in re.findall(r'Overfull \\hbox \(([\d.]+)pt too wide\)', log)]
    undef = re.findall(r"Reference `([^']+)' on page", log)
    print(f"missing glyphs: {miss or 'none'}; overfull lines > 3pt: {sum(1 for x in over if x > 3)} (worst {max(over) if over else 0:.1f}pt); undefined references: {len(set(undef))}")
    body = open(os.path.join(HERE, STEM(printed) + '.tex'), encoding='utf-8').read()
    left = sorted(set(re.findall(r'[δλρκεΔ₂₀√≠𝒪⟺]', body)))
    print('untranslated symbols left in book.tex:', left or 'none')


if __name__ == '__main__':
    mds = sorted(glob.glob(os.path.join(ROOT, 'docs', 'THE_PRICE_OF_AGENCY_unified_v0.*.md')), key=lambda p: [int(x) for x in re.findall(r'\d+', os.path.basename(p))])
    args = [a for a in sys.argv[1:] if not a.startswith('--')]; printed = '--print' in sys.argv
    md_path = args[0] if args else mds[-1]
    open(os.path.join(HERE, STEM(printed) + '_index.tex'), 'w').write('')          # the index is made from this build's own pages, below
    version = build(md_path, printed)
    for _ in range(4 if printed else 3):          # print: one more pass, because which side a page is on settles after the page numbers do
        r = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', STEM(printed) + '.tex'], cwd=HERE, capture_output=True, text=True, errors='replace')
        if r.returncode != 0:
            print(r.stdout[-3000:]); raise SystemExit('xelatex failed')
    # the index: read off the pages just set, written out, and set by two more passes (it is the book's last section, so no page before it moves)
    import make_index as MI
    pdf = os.path.join(HERE, STEM(printed) + '.pdf')
    npages = int(re.search(r'Pages:\s+(\d+)', subprocess.run(['pdfinfo', pdf], capture_output=True, text=True).stdout).group(1))
    first = next(k for k in range(1, 12) if subprocess.run(['pdftotext', '-f', str(k), '-l', str(k), pdf, '-'], capture_output=True, text=True).stdout.strip().startswith('Contents'))
    entries = MI.compute(pdf, first, npages)
    open(os.path.join(HERE, STEM(printed) + '_index.tex'), 'w', encoding='utf-8').write(MI.to_tex(entries, CLAIMS))
    for _ in range(2):
        r = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', STEM(printed) + '.tex'], cwd=HERE, capture_output=True, text=True, errors='replace')
        if r.returncode != 0:
            print(r.stdout[-3000:]); raise SystemExit('xelatex failed (index)')
    print(f'index: {sum(1 for _, pg in entries if pg)} headings, {len(CLAIMS)} theorems and results')
    check(version, printed)
    print(f'built design/{STEM(printed)}.pdf from', os.path.basename(md_path))
