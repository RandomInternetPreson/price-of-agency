# The designed edition

`book.pdf` is *The Price of Agency* set as a book (7 × 10 in). The markdown manuscript in `docs/` stays the source: the
designed edition is built from it by script, so a change to the manuscript is a change to one file.

    python design/make_figures.py                      # the charts (design/fig/*.pdf)
    python design/build_book.py                        # newest docs/THE_PRICE_OF_AGENCY_unified_v0.NN.md -> design/book.pdf
    python design/build_book.py --print                # the two-sided edition for paper -> design/book_print.pdf

Needs: pandoc, xelatex with tcolorbox and mathpazo, the fonts TeX Gyre Pagella, Fira Sans and DejaVu Sans Mono; Python with
numpy and matplotlib for the charts.

## How the pages are marked ("the ledger rule")
The book's chapters share one template, and the book says who each part is for: "§1–2 are for every reader; §3 onward for
those who want the machinery; §6 for anyone who trusts nothing." The design marks exactly that and nothing else.

| mark in the left column | what it is | where |
|---|---|---|
| none | the idea and the story, for every reader | §1–§2 of each chapter; Part I; the Part V essays; the Coda |
| single blue rule | the machinery: theorems, mathematics, models | §3–§5; Chapter 13 §2B–§2C, §3–§5; Chapter 14 §5C; Chapter 15 §2–§4 |
| double brass rule | the receipts: code, files, the public record | §6 of each chapter; Chapter 13 §2D; the appendices |
| dashed grey rule | the one fenced conjecture | Chapter 12 §1–§5 |

Single against double against dashed survives black-and-white printing. A strip on the outer edge of every marked page shows
where the machinery is when the book is flipped or its thumbnails are scrolled. Under each chapter title a strip lists the
chapter's sections with their pages. The book's tags ([PROVEN], [EXACT], …) are set as small stamps.

## Files
- `build_book.py` — reads the manuscript's own structure (parts, chapters, numbered sections), assigns each section its mark
  (`track_of`), writes `book.tex`, runs xelatex, and reports missing glyphs, overflowing lines and untranslated symbols.
- `mathmap.py` — the manuscript writes formulas in plain Unicode so it reads anywhere; this file is the complete translation
  into typeset mathematics. Each entry must be found exactly once, so an edited formula fails the build instead of silently
  printing untranslated. No entry changes a word of prose.
- `bookstyle.tex` — the page design. Contains no manuscript text.
- `make_figures.py` — twenty charts in one style, and the cover's drawing. Each function names its source: computed there with the book's own model
  and checked against a number the book prints, read from a results file in the repository, or copied from the text.
- `figures.py` — where each picture goes, and its caption.
- `fig/*.tex` — seven drawings (the three exits, the harbor, the two rulers, the intersection, two weeks of work, nine boats,
  the chain of the Coda). Drawings, not data. Vera's routes (Figure 9.1) are drawn by `make_figures.py`: 250 mornings under
  each wiring, the days per district taken from the figure of 2026-08-15, the curves drawn with a fixed seed.
- `samples/` — the three treatments tried on Chapter 5 before one was chosen (tinted bands, the ledger rule, two voices).

## What is not in the manuscript
The key to the page marks (in "How to read this book"), the two-line notes in the left column where a marked passage begins,
the "Story resumes: page N" pointers, the twenty-six figure captions, the words inside the figures, and the cover. Everything
else is the manuscript, word for word.

## The two editions
`book.pdf` is for screens: one-sided, with a cover. `book_print.pdf` is for paper: no cover, the text block moved 0.11 in away
from the spine, parts and chapters opening on right-hand pages, page numbers and the edge strips on the outer edge. The ledger
column is on the left of every page in both. One style file serves both (`\ifprinted` in `bookstyle.tex`).

## Tables, the index, the page behind the title
- A pipe table in the manuscript is set by `build_book.py` (`table_block`) in the small sans, its columns sharing the width by
  how much they hold, and kept on one page with the sentence that introduces it.
- `make_index.py` reads the index off the typeset pages: each heading has a pattern, each page's text is searched, and the page
  numbers are set by two further passes. The headings and patterns (`ENTRIES`) are the editorial content; words used on nearly
  every page are indexed where they are defined. The theorems are listed by number where they are stated.
- The page behind the title gives the repository's address (`REPO` in `build_book.py`), a citation line and the arXiv numbers.

## Ruled passages outside the numbered sections
Part I has no numbered sections. Its two passages of machinery (Chapter 2: the second paper, and the argument about a common
currency) are named in `build_book.py` (`RULED_PARAGRAPHS`) by their opening words and carry the blue rule.

## Where pictures sit
On story pages (no rule) a picture that does not fit where it is called moves to the top of the next page and the text runs
on. Inside a marked passage a picture stays where it is called. `wide=True` in `figures.py` lets a story-page picture take the
left column as well. Figures are numbered by chapter; V.1 and V.2 are in the essay that opens Part V, C.1 in the Coda.

## The web edition

`python design/build_web.py` writes `web/index.html` (pictures beside it in `web/fig/`) and `web/the_price_of_agency.html`
(the same page with the pictures inside it: one file, about 4 MB, that opens with the network off). It reads the same
manuscript through the same steps as the PDF: `mathmap.py` for the formulas, `track_of` for which sections are machinery,
receipts or fenced, `figures.py` for where each picture goes. The differences are in how the page is marked:

- The text for every reader runs straight down the page. Machinery and receipts are drawers (`<details>`), closed until
  opened, each with the rule the PDF gives it: blue, double brass. The drawer's handle names the section and says how
  many pictures are inside. The fenced chapter stands open, behind its dashed rule.
- A button opens or folds every drawer and keeps the reader's place. A link into a folded drawer opens it. Printing
  opens them all.
- Formulas are MathML, set by pandoc. Charts are the PDF's own, converted by `pdftocairo -svg`; the seven drawings are
  compiled alone by xelatex and converted the same way.
- The page loads nothing from the network: no fonts, no scripts, no counters. Its `Content-Security-Policy` line tells the
  browser to refuse any connection but the page's own pictures. Type falls back through Palatino to the reader's serif.
- There is no index and there are no page numbers; the contents and the browser's own search do that work.

`web/calculator.html` is written by hand and is not built from anything. It shares the page's look and its rule about the
network.
