"""build_web.py -- the web edition, built from the same manuscript as the designed edition.

    python design/make_figures.py
    python design/build_web.py [docs/THE_PRICE_OF_AGENCY_unified_vX.YY.md]

Writes web/index.html with its pictures in web/fig/, and web/the_price_of_agency.html, which is the same page with the
pictures inside it: one file that can be sent, saved or opened with the network off.

The manuscript stays the source, and the page says what the printed pages say. What the designed edition marks with a rule
in the left column, the web edition folds: the text for every reader runs straight down the page, and the machinery, the
receipts and the fenced conjecture sit in drawers that open where they stand. The page asks the network for nothing --
no fonts, no scripts, no counters -- and a line in its head tells the browser to refuse if anything ever tries.

Needs pandoc; pdftocairo for the charts; xelatex for the seven drawings in design/fig/*.tex.
"""
import os, re, sys, json, subprocess, glob, html, base64, time, shutil, tempfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
WEB = os.path.join(ROOT, 'web')
sys.path.insert(0, HERE)
import mathmap as MM
import figures as FIG
import build_book as BB
from build_book import E, M, R, F, VOCAB, flat, tag_kind, strip_brackets, cut_at_bracket, track_of, PART_TITLES, REPO, DOI

NOTE = {M: 'The machinery, for those who want it', R: 'The receipts, for anyone who trusts nothing',
        F: 'Fenced: a conjecture, and nothing later depends on it'}
esc = html.escape


def RawI(s): return {'t': 'RawInline', 'c': ['html', s]}
def RawB(s): return {'t': 'RawBlock', 'c': ['html', s]}
def Str(s): return {'t': 'Str', 'c': s}
SP = {'t': 'Space'}


# ------------------------------------------------------------------------------------------------ inline transforms
def stamp(body): return RawI('<span class="stamp">%s</span>' % esc(body))


def fix_inlines(inl):
    """the tags printed beside claims become stamps; everything else is left to pandoc"""
    out = []; i = 0
    while i < len(inl):
        x = inl[i]; t = x['t']
        if t == 'Strong':
            s = flat(x['c']).strip()
            m = re.match(r'^\[(.+)\]$', s, re.S)
            if m and m.group(1).split()[0].strip('—;:,.') in VOCAB:                       # a tag standing alone
                if tag_kind(m.group(1)) == 1: out.append(stamp(m.group(1)))
                else: out += [RawI('<span class="tagnote">[')] + tagwords(strip_brackets(x['c'])) + [RawI(']</span>')]
                i += 1; continue
            m = re.match(r'^(.+?)\s*\[([^\[\]]+)\]$', s, re.S)
            if m and m.group(2).split()[0].strip('—;:,.') in VOCAB:                       # a bold lead ending in a tag
                out += [{'t': 'Strong', 'c': fix_inlines(cut_at_bracket(x['c']))}, SP]
                out.append(stamp(m.group(2)) if tag_kind(m.group(2)) == 1 else RawI('<span class="tagnote">[%s]</span>' % esc(m.group(2))))
                i += 1; continue
            out.append({'t': 'Strong', 'c': fix_inlines(x['c'])}); i += 1; continue
        if t == 'Emph':
            out.append({'t': 'Emph', 'c': fix_inlines(x['c'])}); i += 1; continue
        if t == 'Quoted':
            out.append({'t': 'Quoted', 'c': [x['c'][0], fix_inlines(x['c'][1])]}); i += 1; continue
        if t == 'Str':
            s = x['c']; w = s.lstrip('[').strip('—;:,.]')
            if s.startswith('[') and w in VOCAB:                                           # a tag in running text
                j = i; span = []
                while j < len(inl):
                    span.append(inl[j])
                    if inl[j]['t'] == 'Str' and ']' in inl[j]['c']: break
                    j += 1
                closed = j < len(inl); body = flat(span).strip()
                mm = re.match(r'^\[([^\[\]]+)\]([.,;:]?)$', body)
                if closed and mm and tag_kind(mm.group(1).rstrip('.')) == 1:
                    out.append(RawI('<span class="stamp">%s</span>%s' % (esc(mm.group(1).rstrip('.')), mm.group(2)))); i = j + 1; continue
                out += tagwords(span if closed else [x]); i = (j + 1) if closed else (i + 1); continue
        out.append(x); i += 1
    return out


def tagwords(span):
    """a long bracketed note: its tag words are set as small stamps, the rest is left as it is"""
    out = []
    for y in span:
        if y['t'] == 'Str':
            for k, p in enumerate(re.split(r'\b(' + '|'.join(sorted(VOCAB, key=len, reverse=True)) + r')\b', y['c'])):
                if p: out.append(RawI('<span class="tagword">%s</span>' % p) if k % 2 else Str(p))
        else:
            out += fix_inlines([y])
    return out


# ------------------------------------------------------------------------------------------------ pictures
def tikz_preamble():
    style = open(os.path.join(HERE, 'bookstyle.tex'), encoding='utf-8').read()
    colors = '\n'.join(re.findall(r'^\\definecolor\{.*$', style, re.M))
    return (r'''\documentclass[border=3pt]{standalone}
\usepackage{amsmath,amssymb}\usepackage[sc]{mathpazo}\usepackage[no-math]{fontspec}
\setmainfont{TeX Gyre Pagella}[Ligatures=TeX]
\setsansfont{Fira Sans}[Scale=0.9,BoldFont={Fira Sans SemiBold},ItalicFont={Fira Sans Italic},BoldItalicFont={Fira Sans SemiBold Italic}]
\setmonofont{DejaVu Sans Mono}[Scale=0.78]
\usepackage{xcolor,graphicx,tikz}\usetikzlibrary{arrows.meta,calc,decorations.pathmorphing}
\newlength{\ledgertotal}\setlength{\ledgertotal}{1.36in}
''' + colors + '\n' + r'\newcommand{\tagword}[1]{{\upshape\sffamily\fontsize{7.4}{9}\selectfont\addfontfeature{LetterSpace=7}\bfseries #1}}' + '\n\\begin{document}\\fontsize{10}{13.2}\\selectfont\n')


def make_pictures():
    """every picture of the designed edition as an SVG beside the page: charts through pdftocairo, drawings through xelatex first"""
    out = os.path.join(WEB, 'fig'); os.makedirs(out, exist_ok=True)
    sizes = {}
    for fig in FIG.FIGURES:
        src = os.path.join(HERE, 'fig', fig['file']); stem = os.path.splitext(fig['file'])[0]; svg = os.path.join(out, stem + '.svg')
        if fig['file'].endswith('.tex'):
            with tempfile.TemporaryDirectory() as tmp:
                open(os.path.join(tmp, 'd.tex'), 'w', encoding='utf-8').write(tikz_preamble() + '\\input{%s}\n\\end{document}\n' % src.replace('\\', '/'))
                r = subprocess.run(['xelatex', '-interaction=nonstopmode', '-halt-on-error', 'd.tex'], cwd=tmp, capture_output=True, text=True, errors='replace')
                if r.returncode != 0: print(r.stdout[-1500:]); raise SystemExit('drawing failed: ' + fig['file'])
                subprocess.run(['pdftocairo', '-svg', os.path.join(tmp, 'd.pdf'), svg], check=True)
        else:
            if not os.path.exists(src): raise SystemExit('missing chart %s: run design/make_figures.py first' % fig['file'])
            subprocess.run(['pdftocairo', '-svg', src, svg], check=True)
        head = open(svg, encoding='utf-8').read(600)
        w, h = re.search(r'width="([\d.]+)(?:pt)?" height="([\d.]+)(?:pt)?"', head).groups(); sizes[fig['file']] = (float(w), float(h))
    return sizes


# ------------------------------------------------------------------------------------------------ blocks
def fix_blocks(blocks, state):
    out = []
    for b in blocks:
        t = b['t']
        if t == 'Table':
            walk_table(b); out += [RawB('<div class="tablewrap">'), b, RawB('</div>')]; continue
        if t in ('Para', 'Plain'):
            c = b['c']
            if len(c) == 1 and c[0]['t'] == 'Str' and re.match(r'^DISPLAYMATH\d\dX$', c[0]['c']):
                texsrc = re.sub(r'\\\\\[\d+pt\]', r'\\\\', MM.DISPLAY[int(c[0]['c'][11:13])][1]).replace(r'\allowbreak', '')
                texsrc = re.sub(r'\\[Bb]igg?l', r'\\left', texsrc); texsrc = re.sub(r'\\[Bb]igg?r', r'\\right', texsrc)      # sized brackets, said the way a browser's math understands
                out += [RawB('<div class="dispmath">'), {'t': 'Plain', 'c': [{'t': 'Math', 'c': [{'t': 'DisplayMath'}, texsrc]}]}, RawB('</div>')]; continue
            if t == 'Para' and c and c[0]['t'] == 'Strong':
                s = flat(c[0]['c']).strip(); m = BB.CLAIM.match(s)
                if m:
                    label, name, tag = m.group(1), m.group(2), m.group(3)
                    state['claims'] += 1
                    tagh = '' if not tag else (' <span class="stamp">%s</span>' % esc(tag) if tag_kind(tag) == 1 else ' <span class="tagnote">[%s]</span>' % esc(tag))
                    out.append(RawB('<p class="claim" id="claim-%d"><span class="claim-label">%s</span> <span class="claim-name">%s</span>%s</p>'
                                    % (state['claims'], esc(label), esc(name), tagh)))
                    rest = c[1:]
                    while rest and rest[0]['t'] in ('Space', 'SoftBreak'): rest = rest[1:]
                    if rest: out.append({'t': 'Para', 'c': fix_inlines(rest)})
                    continue
                if s.startswith('Axiom 1.') and len(c) >= 3 and c[-1]['t'] == 'Strong':
                    a1 = flat(c[0]['c']).split('. ', 1)[1]; a2 = flat(c[-1]['c']).split('. ', 1)[1]
                    out.append(RawB('<div class="axioms"><p><span class="ax">Axiom 1</span>%s</p><p><span class="ax">Axiom 2</span>%s</p></div>' % (esc(a1), esc(a2)))); continue
            if t == 'Para' and len(c) == 1 and c[0]['t'] == 'Emph' and c[0]['c'] and c[0]['c'][0]['t'] == 'Quoted':
                out += [RawB('<div class="saying">'), {'t': 'Para', 'c': fix_inlines(c)}, RawB('</div>')]; continue
            out.append({'t': t, 'c': fix_inlines(c)})
            s = re.sub(r'\s+', ' ', flat(c))
            for fig in FIG.FIGURES:
                if fig.get('placed') or state['chapter'] != fig['chapter'] or fig['after'] not in s: continue
                n = state['fignum'][fig['chapter']] = state['fignum'].get(fig['chapter'], 0) + 1
                pre = str(fig['chapter']) if isinstance(fig['chapter'], int) else {'coda': 'C', 'appx': 'A', 'front': '0'}.get(fig['chapter'], fig['chapter'].replace('part', ''))
                w, h = state['sizes'][fig['file']]; stem = os.path.splitext(fig['file'])[0]
                out.append(RawB('<figure id="fig-%s-%d"%s><img src="fig/%s.svg" width="%d" height="%d" loading="lazy" alt="%s"><figcaption><span class="fignum">Figure %s.%d</span> %s</figcaption></figure>'
                                % (pre, n, ' class="wide"' if fig.get('wide') else '', stem, round(w * 4 / 3), round(h * 4 / 3), esc(fig['caption'], quote=True), pre, n, esc(fig['caption']))))
                fig['placed'] = True; state['figs_here'] += 1
            continue
        if t == 'BulletList':
            out.append({'t': t, 'c': [fix_blocks(item, state) for item in b['c']]}); continue
        if t == 'OrderedList':
            out.append({'t': t, 'c': [b['c'][0], [fix_blocks(item, state) for item in b['c'][1]]]}); continue
        if t == 'BlockQuote':
            out.append({'t': t, 'c': fix_blocks(b['c'], state)}); continue
        if t == 'HorizontalRule':
            continue
        out.append(b)
    return out


def walk_table(b):
    head, bodies = b['c'][3], b['c'][4]
    for row in head[1] + [r for body in bodies for r in body[3]]:
        for cell in row[1]:
            for blk in cell[4]:
                if blk['t'] in ('Para', 'Plain'): blk['c'] = fix_inlines(blk['c'])
    for cs in b['c'][2]: cs[1] = {'t': 'ColWidthDefault'}        # the browser sets the columns


# ------------------------------------------------------------------------------------------------ the page
def build(md_path):
    md = open(md_path, encoding='utf-8').read()
    version = re.search(r'draft (v[\d.]+)', md).group(1)
    md = BB.apply_math(md).replace('\\allowbreak', '')          # a line-breaking hint for the typesetter, which a browser does not need
    ast = json.loads(subprocess.run(['pandoc', '-f', BB.PANDOC_IN, '-t', 'json'], input=md, capture_output=True, text=True).stdout)
    API = ast['pandoc-api-version']; blocks = ast['blocks']
    for fig in FIG.FIGURES: fig.pop('placed', None)
    sizes = make_pictures()

    # the outline, read the way the designed edition reads it
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
            chap = {'kind': 'chapter', 'num': 'coda', 'title': title.split('. ', 1)[1], 'label': 'coda', 'sections': [], 'part': None}; outline.append(chap); continue
        if title == 'APPENDICES':
            chap = {'kind': 'chapter', 'num': 'appx', 'title': 'Appendices', 'label': 'appx', 'sections': [], 'part': None}; outline.append(chap); continue
        m = re.match(r'^§(\w+)\.\s+(.*)$', title)
        if m and chap:
            chap['sections'].append({'sec': m.group(1), 'title': m.group(2), 'track': track_of(chap['num'], m.group(1)), 'label': f"{chap['label']}-s{m.group(1)}"})
        elif lvl == 2 and part and chap is None and title != 'How to read this book':
            part['essays'].append((title, 'sec-' + re.sub(r'\W+', '-', title.lower())))
    order = [o for o in outline if o['kind'] == 'chapter']

    out = []; state = {'chapter': None, 'fignum': {}, 'sizes': sizes, 'claims': -1, 'figs_here': 0}
    open_tags = []                                    # closing tags owed, innermost last
    body = []; seen_title = False; chap = None; summaries = []; cur = {'drawer': None}

    def close(to=0):
        while len(open_tags) > to: out.append(RawB(open_tags.pop()))

    def flush():
        nonlocal body
        if body:
            state['figs_here'] = 0; out.extend(fix_blocks(body, state)); body = []
            if cur['drawer'] is not None: cur['drawer'][1] += state['figs_here']

    for b in blocks:
        if b['t'] != 'Header':
            if seen_title: body.append(b)
            continue
        flush(); cur['drawer'] = None
        lvl, title = b['c'][0], flat(b['c'][2]).strip()
        if title == 'THE PRICE OF AGENCY' or lvl == 3: continue
        if title == 'How to read this book':
            seen_title = True; state['chapter'] = 'front'
            out.append(RawB('<section class="front" id="front-howto"><h2>How to read this book</h2>')); open_tags.append('</section>'); continue
        m = re.match(r'^PART ([IVX]+)\b', title)
        if m:
            close(); p = next(o for o in outline if o['kind'] == 'part' and o['num'] == m.group(1))
            lst = ''.join('<li><a href="#%s"><span class="n">%s</span>%s</a></li>' % (c['label'], c['num'], esc(c['title'])) for c in p['chapters'])
            out.append(RawB('<section class="part" id="%s"><header class="partopen"><p class="kicker">Part %s</p><h2>%s</h2><ol class="partlist">%s</ol></header>' % (p['label'], p['num'], esc(p['title']), lst)))
            open_tags.append('</section>'); state['chapter'] = 'part' + p['num']; chap = None; continue
        m = re.match(r'^Chapter (\d+)\.\s+(.*)$', title)
        if m or title.startswith('Coda.') or title == 'APPENDICES':
            key = int(m.group(1)) if m else ('coda' if title.startswith('Coda.') else 'appx')
            close(1 if (m and open_tags) else 0)             # a chapter closes everything inside its part; the coda and appendices close the part too
            chap = next(c for c in order if c['num'] == key); state['chapter'] = key
            top = ('Part %s. %s' % (chap['part']['num'], chap['part']['title'])) if chap['part'] else ('Coda' if key == 'coda' else '')
            numeral = '<span class="numeral" aria-hidden="true">%d</span>' % key if isinstance(key, int) else ''
            head = '<article class="chapter" id="%s"><header class="chapopen">%s<p class="kicker">%s</p><h2>%s</h2>' % (
                chap['label'], numeral, esc(top + (' · Chapter %d' % key if isinstance(key, int) else '')) if top else '', esc(chap['title']))
            if chap['sections']:
                head += '<nav class="route" aria-label="The sections of this chapter"><ol>' + ''.join(
                    '<li class="%s"><a href="#%s"><span class="n">§%s</span>%s</a></li>' % (s['track'], s['label'], s['sec'], esc(short(s['title']))) for s in chap['sections']) + '</ol></nav>'
            out.append(RawB(head + '</header>')); open_tags.append('</article>')
            if key == 'appx':
                out.append(RawB('<div class="ruled receipts"><p class="tracknote">%s</p>' % NOTE[R])); open_tags.append('</div>')
            continue
        m = re.match(r'^§(\w+)\.\s+(.*)$', title)
        if m and chap:
            close(2 if chap['part'] else 1)
            s = next(x for x in chap['sections'] if x['sec'] == m.group(1))
            if s['track'] == E:
                out.append(RawB('<section class="sec everyone" id="%s"><h3><span class="n">§%s</span>%s</h3>' % (s['label'], s['sec'], esc(s['title'])))); open_tags.append('</section>')
            else:
                summaries.append([len(out), 0, s]); cur['drawer'] = summaries[-1]
                out.append(None); open_tags.append('</div></details>')
            continue
        close(1)                                              # an essay that opens a part
        out.append(RawB('<section class="essay" id="%s"><h3 class="essayhead">%s</h3>' % ('sec-' + re.sub(r'\W+', '-', title.lower()), esc(title)))); open_tags.append('</section>')
    flush(); close()

    for k, nfig, s in summaries:                              # the drawer's handle says what is inside it
        pics = '' if not nfig else ' · %s' % ('one picture' if nfig == 1 else '%d pictures' % nfig)
        out[k] = RawB('<details class="sec %s" id="%s"%s><summary><h3><span class="n">§%s</span>%s</h3><span class="tracknote">%s%s</span></summary><div class="drawer">'
                      % (s['track'], s['label'], ' open' if s['track'] == F else '', s['sec'], esc(s['title']), NOTE[s['track']], pics))   # the fenced chapter is short and is all fence: it stands open

    for opening in BB.RULED_PARAGRAPHS:                       # Part I's two passages of machinery, named by their opening words
        hits = [k for k, b in enumerate(out) if b['t'] == 'Para' and flat(b['c']).lstrip().startswith(opening)]
        if len(hits) != 1: raise SystemExit(f'ruled paragraph not found exactly once: {opening!r} ({len(hits)})')
        k = hits[0]; out.insert(k + 1, RawB('</div>')); out.insert(k, RawB('<div class="ruled machinery"><p class="tracknote">%s</p>' % NOTE[M]))
    for k, b in enumerate(out):                               # the key to the markings, where the book explains its own structure
        if b['t'] == 'Para' and 'Every chapter is built the same way' in flat(b['c']):
            out.insert(k + 1, RawB(KEY)); break
    else:
        raise SystemExit('the paragraph that explains the chapter template was not found')
    missing = [f['after'][:50] for f in FIG.FIGURES if not f.get('placed')]
    if missing: raise SystemExit('FIGURES NOT PLACED: %s' % missing)

    r = subprocess.run(['pandoc', '-f', 'json', '-t', 'html', '--mathml', '--wrap=none'],
                       input=json.dumps({'pandoc-api-version': API, 'meta': {}, 'blocks': out}), capture_output=True, text=True)
    if r.stderr.strip(): print('pandoc:', r.stderr.strip()[:2000])
    body_html = r.stdout

    toc = ['<li class="tocfront"><a href="#front-howto">How to read this book</a></li>']
    for o in outline:
        if o['kind'] == 'part':
            toc.append('<li class="tocpart"><a href="#%s"><span class="n">Part %s</span>%s</a></li>' % (o['label'], o['num'], esc(o['title'])))
            toc += ['<li class="tocessay"><a href="#%s">%s</a></li>' % (lab, esc(t)) for t, lab in o['essays']]
        elif isinstance(o['num'], int): toc.append('<li class="tocchap"><a href="#%s"><span class="n">%d</span>%s</a></li>' % (o['label'], o['num'], esc(o['title'])))
        else: toc.append('<li class="tocfront"><a href="#%s">%s</a></li>' % (o['label'], 'Coda: ' + esc(o['title']) if o['num'] == 'coda' else 'Appendices'))
    year = time.strftime('%Y'); month = time.strftime('%B %Y')
    page = (PAGE.replace('@CSS@', CSS).replace('@JS@', JS).replace('@VERSION@', version).replace('@MONTH@', month).replace('@YEAR@', year)
            .replace('@REPO@', REPO).replace('@DOI@', DOI).replace('@TOC@', '\n'.join(toc)).replace('@BODY@', body_html))
    os.makedirs(WEB, exist_ok=True)
    open(os.path.join(WEB, 'index.html'), 'w', encoding='utf-8').write(page)

    def inline(m):
        data = open(os.path.join(WEB, 'fig', m.group(1)), 'rb').read()
        return 'src="data:image/svg+xml;base64,%s"' % base64.b64encode(data).decode()
    single = re.sub(r'src="fig/([\w.-]+\.svg)"', inline, page)
    open(os.path.join(WEB, 'the_price_of_agency.html'), 'w', encoding='utf-8').write(single)
    n_math = body_html.count('<math'); bad = len(re.findall(r'class="math (?:inline|display)"', body_html))
    print(f'web edition {version}: {len(page) // 1024} KB page + {len(FIG.FIGURES)} pictures; single file {len(single) // 1024} KB; '
          f'{n_math} formulas set, {bad} left as text; {len(summaries)} drawers')
    return version


def short(title):
    for a, b in (('The idea, in plain words', 'The idea'), ('The model, and what it covers', 'The model'), ('The model, and its audits', 'The model'),
                 ('The code, and the record', 'The code')):
        if title == a: return b
    return 'The story' if title.startswith('The story:') else title


KEY = '''<aside class="key" aria-label="How this page is marked">
<p class="keyrow everyone"><span class="swatch"></span><span><b>No rule.</b> For every reader. This text runs straight down the page.</span></p>
<p class="keyrow machinery"><span class="swatch"></span><span><b>A blue rule.</b> The machinery: theorems, mathematics, models. Folded shut; it opens where it stands.</span></p>
<p class="keyrow receipts"><span class="swatch"></span><span><b>A double brass rule.</b> The receipts: code and records.</span></p>
<p class="keyrow fenced"><span class="swatch"></span><span><b>A dashed rule.</b> Fenced: the one conjecture, on which nothing later depends.</span></p>
</aside>'''

CSS = r'''
:root { --paper:#fff; --ink:#1a1a1a; --muted:#5b5b57; --hair:#cfcec9; --numeral:#a3a29d; --panel:#f4f3f0; --mach:#1c5cab; --rcpt:#8a5a14; --fence:#77766f;
  --serif:"Palatino Linotype",Palatino,"Book Antiqua","TeX Gyre Pagella","URW Palladio L",Georgia,serif;
  --sans:"Fira Sans",system-ui,-apple-system,"Segoe UI",Roboto,"Helvetica Neue",Arial,sans-serif;
  --mono:"DejaVu Sans Mono",ui-monospace,Menlo,Consolas,monospace;
  --ledger:8.5rem; --gap:1.6rem; --measure:36rem; color-scheme:light; }
* { box-sizing:border-box; }
html { background:var(--paper); scroll-padding-top:3.4rem; -webkit-text-size-adjust:100%; }
body { margin:0; background:var(--paper); color:var(--ink); font-family:var(--serif); font-size:1.125rem; line-height:1.58; }
.bar { position:sticky; top:0; z-index:5; background:rgba(255,255,255,.96); border-bottom:1px solid var(--hair); font-family:var(--sans); font-size:.82rem; }
.bar .in { max-width:calc(var(--ledger) + var(--gap) + var(--measure) + 2rem); margin:0 auto; padding:.5rem 1rem; display:flex; gap:1.1rem; align-items:center; }
.bar a { color:var(--ink); text-decoration:none; } .bar a:hover { text-decoration:underline; } .bar .t { font-weight:600; margin-right:auto; white-space:nowrap; overflow:hidden; text-overflow:ellipsis; }
.bar button { font:inherit; color:var(--ink); background:var(--paper); border:1px solid #9f9e99; border-radius:3px; padding:.22rem .6rem; cursor:pointer; white-space:nowrap; }
.bar button:hover { background:var(--panel); }
:focus-visible { outline:2px solid var(--mach); outline-offset:2px; }
.page { max-width:calc(var(--ledger) + var(--gap) + var(--measure) + 2rem); margin:0 auto; padding:0 1rem 5rem calc(1rem + var(--ledger) + var(--gap)); }
p { margin:0 0 .9rem; } a { color:var(--mach); text-underline-offset:.15em; }
h2 { font-weight:400; font-size:clamp(1.9rem,5vw,2.6rem); line-height:1.1; margin:0 0 1rem; letter-spacing:-.005em; }
h3 { font-size:1.22rem; line-height:1.25; margin:0 0 .7rem; font-weight:700; }
h3 .n, .route .n, .partlist .n, .toc .n { font-family:var(--sans); font-weight:400; color:var(--muted); margin-right:.55rem; font-size:.86em; }
.kicker, .tracknote, figcaption, .stamp, .tagnote, .tagword, .keyrow, .colophon, .route, .partlist, .toc { font-family:var(--sans); }
.kicker { font-size:.84rem; color:var(--muted); margin:0 0 .5rem; }
/* cover */
.cover { padding:5.5rem 0 3rem; }
.cover h1 { font-weight:400; font-size:clamp(3rem,10vw,5rem); line-height:1; margin:0 0 1.5rem; letter-spacing:-.015em; }
.cover .sub { font-style:italic; font-size:1.3rem; line-height:1.4; margin:0 0 3.2rem; }
.cover .by { font-family:var(--sans); font-size:1rem; margin:0; } .cover .with, .cover .draft { font-family:var(--sans); font-size:.86rem; color:var(--muted); margin:.15rem 0 0; }
.cover .draft { margin-top:1.6rem; }
/* contents */
.toc { margin:1rem 0 4rem; font-size:.95rem; }
.toc h2 { font-family:var(--serif); } .toc ol { list-style:none; margin:0; padding:0; } .toc a { color:var(--ink); text-decoration:none; display:block; padding:.16rem 0; } .toc a:hover { color:var(--mach); }
.toc .tocpart { margin-top:1.1rem; font-weight:600; } .toc .tocchap, .toc .tocessay { padding-left:1.2rem; } .toc .tocessay a { font-style:italic; } .toc .tocfront { margin-top:.9rem; }
.toc .tocchap .n { display:inline-block; min-width:1.5rem; margin-right:.3rem; }
/* openers */
.front, .part, .chapter { padding-top:3.2rem; }
.partopen { border-top:1px solid var(--ink); padding-top:1.2rem; } .partopen h2 { font-size:clamp(2.1rem,6vw,3rem); }
.partlist { list-style:none; margin:1.2rem 0 0; padding:0; font-size:.95rem; } .partlist a { color:var(--ink); text-decoration:none; display:block; padding:.14rem 0; } .partlist a:hover { color:var(--mach); }
.partlist .n { display:inline-block; min-width:1.5rem; }
.chapopen { position:relative; margin-bottom:1.6rem; }
.chapopen .numeral { position:absolute; right:calc(100% + var(--gap)); top:-.9rem; font-size:4.6rem; line-height:1; color:var(--numeral); font-weight:400; }
.route ol { list-style:none; margin:1.1rem 0 0; padding:0; display:flex; flex-wrap:wrap; gap:.35rem .5rem; font-size:.8rem; }
.route a { display:block; color:var(--ink); text-decoration:none; padding:.2rem .55rem .22rem .6rem; background:var(--panel); border-left:3px solid transparent; }
.route a:hover { background:#eae9e5; } .route .n { margin-right:.35rem; }
.route .machinery a { border-left-color:var(--mach); } .route .receipts a { border-left:5px double var(--rcpt); } .route .fenced a { border-left:3px dashed var(--fence); }
.essayhead { font-size:1.6rem; font-weight:400; margin-bottom:1rem; }
/* sections and drawers */
.sec { margin-top:2.2rem; }
details.sec { margin-top:1rem; padding-left:1.1rem; border-left:3px solid var(--mach); }
details.receipts, .ruled.receipts { border-left:5px double var(--rcpt); } details.fenced { border-left:3px dashed var(--fence); }
.ruled { padding-left:1.1rem; border-left:3px solid var(--mach); margin-top:1.2rem; margin-bottom:1.2rem; }
summary { cursor:pointer; list-style:none; padding:.45rem 0; display:flex; flex-wrap:wrap; align-items:baseline; gap:.2rem .9rem; }
summary::-webkit-details-marker { display:none; }
summary h3 { margin:0; font-size:1.08rem; } summary h3::before { content:"+"; font-family:var(--sans); font-weight:400; color:var(--muted); display:inline-block; width:1.1rem; }
details[open] > summary h3::before { content:"\2212"; }
summary:hover h3 { color:var(--mach); }
.tracknote { font-size:.8rem; color:var(--muted); margin:0; } .ruled > .tracknote { margin-bottom:.4rem; }
.drawer { padding:.5rem 0 .8rem; }
details.fenced > summary .tracknote { color:var(--fence); }
/* the furniture of the text */
.stamp { font-size:.68em; letter-spacing:.07em; border:1px solid currentColor; border-radius:2px; padding:.08em .38em .02em; white-space:nowrap; vertical-align:.12em; color:var(--muted); }
.tagnote { font-size:.84em; color:var(--muted); } .tagword { font-size:.82em; letter-spacing:.07em; }
.claim { margin:1.5rem 0 .35rem; } .claim-label { font-family:var(--sans); font-weight:600; font-size:.92rem; margin-right:.35rem; } .claim-name { font-weight:700; margin-right:.35rem; }
.axioms { margin:1.2rem 0; padding:.9rem 1.1rem; background:var(--panel); } .axioms p { margin:0; font-size:1.2rem; } .axioms p + p { margin-top:.4rem; }
.axioms .ax { font-family:var(--sans); font-size:.8rem; color:var(--muted); display:inline-block; min-width:4.6rem; }
.saying p { font-size:1.3rem; line-height:1.4; margin:1.4rem 0; }
blockquote { margin:1.1rem 0; padding:.8rem 1.1rem; background:var(--panel); } blockquote p:last-child { margin-bottom:0; }
a.uri { overflow-wrap:anywhere; } .dispmath mtd { math-style:normal; math-depth:0; }
code { font-family:var(--mono); font-size:.8em; overflow-wrap:anywhere; }
pre { overflow-x:auto; font-size:.86rem; line-height:1.45; padding:.2rem 0 .2rem 1.6rem; } pre code { font-size:1em; overflow-wrap:normal; }
.dispmath { margin:1rem 0; overflow-x:auto; overflow-y:hidden; padding:.15rem 0; } math { font-family:"Cambria Math","STIX Two Math","Latin Modern Math","TeX Gyre Pagella Math",math; font-size:1em; }
ul, ol { padding-left:1.4rem; margin:0 0 .9rem; } li { margin-bottom:.3rem; } li > p { margin-bottom:.4rem; }
figure { margin:1.8rem 0; } figure img { display:block; width:100%; height:auto; }
figure.wide { margin-left:calc(-1 * (var(--ledger) + var(--gap))); }
figcaption { font-size:.82rem; line-height:1.45; color:var(--muted); margin-top:.6rem; } .fignum { color:var(--ink); font-weight:600; margin-right:.3rem; }
.tablewrap { overflow-x:auto; margin:1.1rem 0 1.3rem; }
table { border-collapse:collapse; font-family:var(--sans); font-size:.82rem; line-height:1.4; font-variant-numeric:tabular-nums; min-width:100%; }
th, td { padding:.3rem .9rem .3rem 0; vertical-align:top; text-align:left; border-bottom:1px solid var(--hair); } th { font-weight:600; border-bottom:1px solid var(--ink); }
th:last-child, td:last-child { padding-right:0; } tbody tr:last-child td { border-bottom:1px solid var(--ink); }
.key { margin:1.2rem 0 1.4rem; } .keyrow { display:flex; gap:.9rem; font-size:.86rem; line-height:1.45; margin:0 0 .5rem; align-items:stretch; }
.keyrow .swatch { flex:0 0 1.2rem; min-height:1.6rem; } .keyrow.machinery .swatch { border-left:3px solid var(--mach); } .keyrow.receipts .swatch { border-left:5px double var(--rcpt); }
.keyrow.fenced .swatch { border-left:3px dashed var(--fence); } .keyrow.everyone .swatch { border-left:3px solid transparent; }
.colophon { margin:5rem 0 0; border-top:1px solid var(--hair); padding-top:1rem; font-size:.8rem; line-height:1.5; color:var(--muted); }
.colophon p { margin-bottom:.5rem; overflow-wrap:anywhere; } .colophon a { color:inherit; overflow-wrap:anywhere; }
@media (max-width:54rem) {
  :root { --ledger:0rem; --gap:0rem; } body { font-size:1.0625rem; }
  .chapopen .numeral { position:static; display:block; font-size:3.2rem; margin-bottom:.3rem; }
  figure.wide { margin-left:0; } .bar .hide-s { display:none; } .cover { padding-top:3.5rem; }
}
@media print {
  .bar { display:none; } body { font-size:10.5pt; } .page { max-width:none; padding:0; } details.sec, .ruled, figure, .claim { break-inside:auto; } figure, tr { break-inside:avoid; }
  .part, .chapter { break-before:page; } a { color:inherit; text-decoration:none; }
}
'''

JS = r'''
(function () {
  'use strict';
  var drawers = Array.prototype.slice.call(document.querySelectorAll('details.sec')), btn = document.getElementById('all'), open = false;
  function label() { btn.textContent = open ? 'Fold the machinery' : 'Open every drawer'; btn.setAttribute('aria-pressed', open ? 'true' : 'false'); }
  btn.addEventListener('click', function () {
    var y = window.scrollY, anchor = null, top = 0;                    // keep the reader's place while the page changes height
    var els = document.querySelectorAll('.chapopen, .sec, .partopen, .essay');
    for (var i = 0; i < els.length; i++) { var r = els[i].getBoundingClientRect(); if (r.top >= 0) { anchor = els[i]; top = r.top; break; } }
    open = !open; drawers.forEach(function (d) { d.open = open; }); label();
    if (anchor) window.scrollTo(0, window.scrollY + anchor.getBoundingClientRect().top - top); else window.scrollTo(0, y);
  });
  function reveal() {                                                  // a link into a folded drawer opens it
    var id = decodeURIComponent(location.hash.slice(1)); if (!id) return;
    var el = document.getElementById(id); if (!el) return;
    for (var p = el; p; p = p.parentElement) if (p.tagName === 'DETAILS') p.open = true;
    el.scrollIntoView();
  }
  window.addEventListener('hashchange', reveal); reveal();
  window.addEventListener('beforeprint', function () { drawers.forEach(function (d) { d.open = true; }); });
  label();
})();
'''

PAGE = r'''<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<!-- This page asks the network for nothing, and this line tells the browser to refuse if anything on it ever tries. -->
<meta http-equiv="Content-Security-Policy" content="default-src 'none'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; img-src 'self' data:; form-action 'none'; base-uri 'none'">
<meta name="referrer" content="no-referrer">
<meta name="author" content="Aaron Alai">
<meta name="description" content="The Price of Agency. Freedom, measured. Theft, priced. No opinions required.">
<title>The Price of Agency</title>
<style>@CSS@</style>
</head>
<body>
<div class="bar"><div class="in"><a class="t" href="#top">The Price of Agency</a><a href="#contents">Contents</a><a class="hide-s" href="calculator.html">A ruler for your own schedule</a><button type="button" id="all">Open every drawer</button></div></div>
<div class="page" id="top">
<header class="cover">
<h1>The Price<br>of Agency</h1>
<p class="sub">Freedom, measured. Theft, priced.<br>No opinions required.</p>
<p class="by">Aaron Alai</p>
<p class="with">with Claude (Anthropic) as mathematical collaborator</p>
<p class="draft">Draft @VERSION@, @MONTH@</p>
</header>
<nav class="toc" id="contents" aria-label="Contents">
<h2>Contents</h2>
<ol>
@TOC@
</ol>
</nav>
@BODY@
<footer class="colophon">
<p><b>The Price of Agency.</b> Draft @VERSION@, @MONTH@.</p>
<p>Every script, results file and preregistration named in this book is in its repository: <a href="@REPO@">@REPO@</a></p>
<p>To cite it: Aaron Alai, with Claude (Anthropic) as mathematical collaborator, <i>The Price of Agency: Freedom, measured. Theft, priced. No opinions required.</i> Draft @VERSION@, @YEAR@. @REPO@ &middot; doi:@DOI@</p>
<p>&copy; @YEAR@ Aaron Alai. The text and figures may be copied, translated and built on, for any purpose, with credit (<a href="https://creativecommons.org/licenses/by/4.0/">Creative Commons Attribution 4.0 International</a>). The code may be used for anything (MIT).</p>
<p>The physics it stands on: arXiv:2608.00124 and arXiv:2608.18886.</p>
<p>This page was built from the manuscript by <code>design/build_web.py</code>. It loads nothing from the network and keeps no count of its readers. <a href="calculator.html">A ruler for your own schedule</a> is the book&rsquo;s first instrument, and works the same way.</p>
</footer>
</div>
<script>@JS@</script>
</body>
</html>
'''

if __name__ == '__main__':
    mds = sorted(glob.glob(os.path.join(ROOT, 'docs', 'THE_PRICE_OF_AGENCY_unified_v0.*.md')), key=lambda p: [int(x) for x in re.findall(r'\d+', os.path.basename(p))])
    args = [a for a in sys.argv[1:] if not a.startswith('--')]
    build(args[0] if args else mds[-1])
