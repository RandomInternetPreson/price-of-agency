# The Price of Agency

*Freedom, measured. Theft, priced. No opinions required.*

Aaron Alai, with Claude (Anthropic) as mathematical collaborator. Draft v0.50, November 2026. doi:[10.5281/zenodo.24599088](https://doi.org/10.5281/zenodo.24599088)

The book runs on two assumptions: no one has perfect knowledge, and mistakes are inevitable. From those it builds two
rulers for freedom (how little your circumstances predict you, and how much your actions have to do with what comes next),
measures what raises a person on both and what lowers them, and prices the lowering. Every claim carries a printed tag that
says what holds it up: a proof, an exact computation, a simulation, someone else's data, or a conjecture.

This repository is the book and everything it stands on: the text, every script, every results file, and the tools made
from it.

## Read it

| | |
|---|---|
| The designed edition, for a screen | [`design/book.pdf`](design/book.pdf) |
| The designed edition, for two-sided printing | [`design/book_print.pdf`](design/book_print.pdf) |
| The web edition, one file, works offline | [`web/the_price_of_agency.html`](web/the_price_of_agency.html) |
| The manuscript, plain text | [`docs/THE_PRICE_OF_AGENCY_unified_v0.50.md`](docs/THE_PRICE_OF_AGENCY_unified_v0.50.md) |

The book has two kinds of page. Sections 1 and 2 of every chapter are for every reader: an idea in plain words, then a
story. The sections after them are the machinery (theorems, mathematics, models) and the receipts (code and records). In the
PDF the machinery has a blue rule beside it and the receipts a double brass rule. In the web edition they are folded shut
and open where they stand. A reader can go from the first page to the last on the unruled text alone.

## Use it

[`web/calculator.html`](web/calculator.html), *Who holds the eraser?*, is a ruler for one schedule: yours. It asks nine
questions: how far ahead you know your hours, how often they are changed by a decision that is not freely yours, what one
mistake costs you, how much a shift leaves you for anything else. It answers in two parts. The first uses only your
answers: how often the schedule lets you be where you planned to be (a family dinner as much as a class), how many plans
you have to make to keep ten, and how far two weeks' notice reaches beside a fixed schedule. The second uses the book's
model: it puts ten thousand people on your schedule, signs them up for a course, and shows how many finish it (every
class, because that is who gets the certificate), for how many it then changes what they do, and which change would help
the most of them. Its counts are the most a job
allows: the people in it can already pay for the course and chose it well, and the page says so. It is
one file. It makes no network connection, and a line near the top of the file tells the browser to refuse any. The model
inside it is [`code/calculator_model.py`](code/calculator_model.py).

## Check it

```
python reproduce.py
```

On Windows, double-click `REPRODUCE.bat`. It needs Python 3 with numpy, scipy and matplotlib, and takes two or three minutes.

The command copies `code/` to a temporary folder, runs each script there, reads the numbers each one prints, and compares
them with the numbers the book prints. Every check quotes the sentence of the book it is checking. The report says, line by
line, which of three things happened:

- **ran**: the script was run on your machine just now and its number matched the book, or did not;
- **recorded**: the number was read from a results file in this repository and matched against the book. These are the runs
  that need a GPU, hours of processor time, or the Federal Reserve's survey files, and nothing was re-run;
- **not run**: listed with the reason and the command that runs it.

`python reproduce.py --all` adds the long exact searches (about fifteen minutes more). `python reproduce.py --list` shows
what each mode covers. Each run writes its report to [`REPRODUCE_REPORT.md`](REPRODUCE_REPORT.md); the one in the
repository is from a full run.

What it does not cover: numbers the book gives only in words inside a story, the second sweep of the household model,
and the learned-watcher tournament. The report's last section lists everything that was not re-run and how to run it.

The proofs are in [`docs/THEOREMS_v1.md`](docs/THEOREMS_v1.md), with the record of every claim that was refuted and what
replaced it. Refuted claims stay in the book, marked.

## The tags

| Tag | What holds the claim up |
|---|---|
| PROVEN | a proof short enough to check by hand |
| EXACT | exhaustive enumeration: no sampling, no approximation |
| NUMERICAL, MC, SIMULATION | computed with stated error, or by many simulated lifetimes |
| DATA | measured in the world by someone else and tabulated here |
| CONJECTURE, SPECULATIVE | not established, and marked so that it cannot pass for a result |
| REFUTED | believed, then killed; kept in the book with what killed it |

## What is where

| | |
|---|---|
| `docs/` | the manuscript, the theorem file, the preregistrations written before each test was run, and the results records |
| `code/` | one script for each computation, named for the theorem it establishes; exact unless its name or tag says otherwise |
| `code/rig/` | the long runs (GPU tournaments, stress simulations, the household model in general equilibrium), with their results |
| `code/field/` | the tests on the Federal Reserve's household survey, with their results. The survey files are public and are not copied here |
| `figures/` | the figures the scripts draw |
| `design/` | the designed edition: `build_book.py` makes the PDFs and `build_web.py` the web edition, both from the manuscript |
| `web/` | the web edition and the calculator |
| `reproduce.py` | the check described above |

To rebuild the editions from the manuscript (pandoc, xelatex and pdftocairo are needed):

```
python design/make_figures.py
python design/build_book.py            # design/book.pdf
python design/build_book.py --print    # design/book_print.pdf
python design/build_web.py             # web/index.html and web/the_price_of_agency.html
```

## What it stands on

Part I rests on two papers by the same author: *The Price of Locality* (arXiv:2608.00124; Zenodo
doi:10.5281/zenodo.21445609) and its sequel (arXiv:2608.18886). What the book takes from them is a license and never a
number: the universe is not incongruent with apparent non-determinism, the book's name for action that cannot be predicted
from its local circumstances. Chapter 2 gives both papers in one chapter, and the rest of the book can be read without
them.

## To challenge a claim

Run its script, or read its proof, and open an issue with what you found: a counterexample, a number that does not
reproduce, a model assumption that carries more than the book says it does. A claim that falls is marked REFUTED in the
next draft and stays in the book.

## To cite it

Aaron Alai, with Claude (Anthropic) as mathematical collaborator. *The Price of Agency: Freedom, measured. Theft, priced. No
opinions required.* Draft v0.50, 2026. https://github.com/RandomInternetPreson/price-of-agency ·
doi:10.5281/zenodo.24599088

[`CITATION.cff`](CITATION.cff) holds the same in machine-readable form.

## Licence

The text, figures and records may be copied, translated and built on, for any purpose, with credit: Creative Commons
Attribution 4.0 International ([`LICENSE-TEXT`](LICENSE-TEXT)). The code may be used for anything: MIT
([`LICENSE-CODE`](LICENSE-CODE)). [`LICENSE.md`](LICENSE.md) says which is which and how to give credit.
