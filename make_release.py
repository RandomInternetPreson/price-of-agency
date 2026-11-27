"""make_release.py -- assemble the public copy of this repository from the working copy.

    python make_release.py            writes release/the_price_of_agency_<draft>/  and the files to upload beside it
    python make_release.py --draft    the same, without insisting on a LICENSE file (for looking at, not for publishing)

The working copy holds everything: every earlier draft, the handoff notes between sessions, the task ledger, the pitch,
the chapter drafts. The public copy holds what the book prints and stands on: the book, the code, the theorem file, the
referee report, the figures, and the records the book cites. Working notes stay in the working copy. This script is
that rule written out as a list, so that what becomes public is decided once and not file by file on the day.

What it does:
  1. copies the public files into a fresh folder (the lists are below; nothing is copied that is not on them);
  2. checks that every path the manuscript prints exists in the copy;
  3. checks that no public file points at a file that was left out, and that none contains a private marker
     (a personal e-mail address, the working notes' private headings);
  4. requires LICENSE files, unless --draft;
  5. writes, beside the folder, the files a deposit wants: the two PDFs, the one-file web edition, the calculator,
     and a zip of the folder.

It changes nothing in the working copy and publishes nothing. The folder it writes is what a new repository's first commit
would hold.
"""
import os, re, sys, glob, shutil, zipfile, fnmatch

ROOT = os.path.dirname(os.path.abspath(__file__))

# ---- top level: files and whole folders
TOP_FILES = ['README.md', 'CITATION.cff', 'reproduce.py', 'REPRODUCE.bat', 'REPRODUCE_REPORT.md', 'make_release.py', '.gitignore', '.gitattributes']
LICENSE_FILES = ['LICENSE', 'LICENSE.md', 'LICENSE-TEXT.md', 'LICENSE-CODE.md', 'LICENSE-CODE', 'LICENSE-TEXT']
FOLDERS = ['code', 'figures', 'design', 'web']
SKIP = ['.venv', '.venv_reproduce', '__pycache__', '*.pyc', '*.aux', '*.log', '*.out', 'RESULTS_TO_SEND']
# design/samples holds the three page designs that were compared before one was chosen: working material
SKIP_PATHS = ['design/samples']

# ---- docs/: named one by one. The newest manuscript is added automatically.
DOCS = [
    'THEOREMS_v1.md',                      # Appendix A: every claim, its tag, its proof, and the refutation record
    'REFEREE_REPORT_v1.md',                # Appendix B
    'PRIOR_ART_MAP_v1.0.md',               # Appendix D
    'LEXICON_v1.0.md',                     # Appendix F
    'STRESS_CAMPAIGN_v1.0.md',             # Appendix G
    'RESULTS_STRESS_2026-11-09.md',        # Appendix G
    'RESULTS_HANK_v0.1.md',                # Appendix G
    'HANK_PREREG_v0.1.md',                 # Appendix G: signs committed before the runs
    'RESULTS_THREE_RULERS_2026-11-10.md',  # Appendix H
    'ISOLATION_AUDIT_v1.0.md',             # Chapter 15 §3
    'PAPER_SYNC_REPORT_v0.23.md',          # Chapter 2's record of what was checked against the two papers
    'SHED_PREREG_v0.1.md', 'SHED_PREREG_v0.2.md', 'SHED_PREREG_v0.3.md',   # Chapter 13 §2D: written before each test was run
    'RESULTS_2026-10-24_v1.0.md', 'RESULTS_2026-10-24_rig_v1.0.md', 'RESULTS_2026-11-08_tournament_v1.0.md',   # the results records the code's own notes cite
]
# Left out, and why. Listed so that the choice can be read and changed; nothing here is needed by the book.
LEFT_OUT = {
    'the earlier drafts of the manuscript and the scripts that made each from the last': ['THE_PRICE_OF_AGENCY_unified_v0.*.md (all but the newest)', 'integrate_v0*.py'],
    'chapter drafts, superseded by the manuscript': ['CH*.md', 'CODA_*.md', 'PART_V_INTRO_*.md', 'BOOK_DRAFT.md', 'BOOK_OUTLINE.md', 'FISHING_TOWN_design.md'],
    'notes between working sessions, the task ledger and the pitch': ['HANDOFF_*.md', 'TASKS.md', 'PITCH.md', 'AA_EDITS_REPORT_*.md', 'RIG_JOBS_*.md', 'READTHROUGH_*.md', 'PUBLISHING_*.md'],
    'process reports superseded by later ones': ['IMPACT_MAP_*.md', 'INTEGRATION_REPORT_*.md', 'CHSH_INTEGRATION_REPORT_*.md', 'PAPER_SYNC_REPORT_v0.16.md', 'PAPER_AUDIT_v0.22.md', 'HANK_PORT_PLAN_v0.1.md'],
    'adversarial reviews and the steelman, written as working papers and not yet read for public tone': ['ADVERSARY_REVIEW_*.md', 'MACRO_STEELMAN_v1.0.md'],
}
PRIVATE_MARKERS = [r'@gmail\.', r'@yahoo\.', r'@hotmail\.', r'@outlook\.', r'@proton', r'DEAD-MAN', r'dead[- ]man switch', r'claude\.ai/code/session', r'/tmp/claude-', r'C:\\Users\\']


def newest_manuscript():
    mds = sorted(glob.glob(os.path.join(ROOT, 'docs', 'THE_PRICE_OF_AGENCY_unified_v0.*.md')), key=lambda p: [int(x) for x in re.findall(r'\d+', os.path.basename(p))])
    return os.path.basename(mds[-1])


def skipped(rel, name):
    return any(fnmatch.fnmatch(name, pat) for pat in SKIP) or any(rel == p or rel.startswith(p + '/') for p in SKIP_PATHS)


def copy_tree(src, dst, rel):
    n = 0
    for name in sorted(os.listdir(src)):
        r = rel + '/' + name
        if skipped(r, name): continue
        a, b = os.path.join(src, name), os.path.join(dst, name)
        if os.path.isdir(a):
            n += copy_tree(a, b, r)
        else:
            os.makedirs(dst, exist_ok=True); shutil.copy2(a, b); n += 1
    return n


def main(argv):
    draft = '--draft' in argv
    ms = newest_manuscript(); version = re.search(r'(v0\.\d+)', ms).group(1)
    out_root = os.path.join(ROOT, 'release'); name = 'the_price_of_agency_' + version; out = os.path.join(out_root, name)
    if os.path.isdir(out): shutil.rmtree(out)
    os.makedirs(out)
    problems = []; count = 0

    for f in TOP_FILES:
        if os.path.exists(os.path.join(ROOT, f)): shutil.copy2(os.path.join(ROOT, f), os.path.join(out, f)); count += 1
        else: problems.append('missing at the top level: ' + f)
    licenses = [f for f in LICENSE_FILES if os.path.exists(os.path.join(ROOT, f))]
    for f in licenses: shutil.copy2(os.path.join(ROOT, f), os.path.join(out, f)); count += 1
    if not licenses and not draft: problems.append('no LICENSE file. Without one nobody may reuse the text or the code. Add the license files, or run with --draft to look at the folder.')
    for d in FOLDERS: count += copy_tree(os.path.join(ROOT, d), os.path.join(out, d), d)
    os.makedirs(os.path.join(out, 'docs'))
    for f in DOCS + [ms]:
        src = os.path.join(ROOT, 'docs', f)
        if os.path.exists(src): shutil.copy2(src, os.path.join(out, 'docs', f)); count += 1
        else: problems.append('listed for docs/ and not found: ' + f)

    # every path the book prints is in the copy
    book = re.sub(r'\s+', ' ', open(os.path.join(out, 'docs', ms), encoding='utf-8').read())
    cited = set(re.findall(r'`((?:docs|code|figures|design|web)/[^`]*)`', book)) | set(re.findall(r'(?<![`\w/])((?:docs|code|figures|design|web)/[\w./-]+\.(?:md|py|png|json|csv|npy))', book))
    for p in sorted(cited):
        q = p.replace(' ', '').rstrip('.,;')
        if not os.path.exists(os.path.join(out, q)): problems.append('the book prints a path that is not in the public copy: ' + q)

    # no public file points at a file that was left out; none carries a private marker
    kept_docs = set(os.listdir(os.path.join(out, 'docs'))); all_docs = set(os.listdir(os.path.join(ROOT, 'docs')))
    dangling = {}; marked = []
    for base, _, files in os.walk(out):
        for f in files:
            if not f.endswith(('.md', '.py', '.txt', '.bat', '.tex', '.html', '.cff', '.csv', '.json')): continue
            p = os.path.join(base, f); rel = os.path.relpath(p, out).replace(os.sep, '/')
            try: text = open(p, encoding='utf-8', errors='replace').read()
            except Exception: continue
            for m in set(re.findall(r'docs/([\w.\-]+\.(?:md|py))', text)):
                if m in all_docs and m not in kept_docs and rel != 'make_release.py': dangling.setdefault(m, []).append(rel)
            for pat in PRIVATE_MARKERS:
                if re.search(pat, text) and rel != 'make_release.py': marked.append('%s contains %s' % (rel, pat))
    for m in marked: problems.append('private marker: ' + m)

    # the files a deposit wants, beside the folder
    extras = [('design/book.pdf', 'The_Price_of_Agency_%s.pdf' % version), ('design/book_print.pdf', 'The_Price_of_Agency_%s_print_two-sided.pdf' % version),
              ('web/the_price_of_agency.html', 'The_Price_of_Agency_%s_web_edition.html' % version), ('web/calculator.html', 'who_holds_the_eraser_calculator.html')]
    for src, dst in extras:
        if os.path.exists(os.path.join(out, src)): shutil.copy2(os.path.join(out, src), os.path.join(out_root, dst))
        else: problems.append('not built yet: ' + src)
    zpath = os.path.join(out_root, name + '_repository.zip')
    with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
        for base, _, files in os.walk(out):
            for f in sorted(files):
                p = os.path.join(base, f); z.write(p, os.path.join(name, os.path.relpath(p, out)))

    size = sum(os.path.getsize(os.path.join(b, f)) for b, _, fs in os.walk(out) for f in fs)
    print('%s: %d files, %.1f MB, in release/%s/' % (name, count, size / 1e6, name))
    print('beside it: ' + ', '.join(d for _, d in extras) + ', ' + os.path.basename(zpath))
    print('\nleft out of docs/ (%d files):' % (len(all_docs) - len(kept_docs)))
    for why, pats in LEFT_OUT.items(): print('  - %s: %s' % (why, ', '.join(pats)))
    unlisted = [f for f in sorted(all_docs - kept_docs) if not any(fnmatch.fnmatch(f, pat.split(' ')[0]) for pats in LEFT_OUT.values() for pat in pats)]
    if unlisted: print('  - left out and not on any list above (decide): ' + ', '.join(unlisted))
    if dangling:
        print('\npublic files that mention a file left out (the mention stays; the file does not):')
        for m, where in sorted(dangling.items()): print('  - docs/%s, mentioned in %s%s' % (m, ', '.join(sorted(set(where))[:4]), ' and others' if len(set(where)) > 4 else ''))
    if problems:
        print('\nNOT READY:'); [print('  - ' + p) for p in problems]; return 1
    print('\nready: nothing the book prints is missing, and no private marker was found.' + (' (draft: no license files yet)' if draft and not licenses else ''))
    return 0


if __name__ == '__main__':
    sys.exit(main(sys.argv[1:]))
