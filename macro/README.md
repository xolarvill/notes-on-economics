# Editing and compiling the macro notes

Compile `macro.tex`. It is the single entry point and contains the shared
formatting, commands, table of contents, and file references. Chapter text is
kept in chapter files rather than mixed into the entry point.

## Writing and revision standards

Read [WRITING_GUIDE.md](WRITING_GUIDE.md) before revising or adding chapters.
It fixes the book's agreed style: reconstruct the raw modeling ideas and
questions, explain economic intuition throughout, connect mechanisms to social
and economic situations, specify conditions fully, and use visual structure to
make relationships apparent. Concise prose must retain detailed reasoning;
layout changes must preserve substantive content.

[AGENTS.md](AGENTS.md) directs future editing work to those standards.
[REVISION_PLAN.md](REVISION_PLAN.md) records the structure and revision history;
[CONDITION_AUDIT.md](CONDITION_AUDIT.md) records condition comparisons for growth,
RBC, and New Keynesian models. [DERIVATION_AUDIT.md](DERIVATION_AUDIT.md) separately maps the
restored mathematical routes and intermediate operations. The intended reader has completed intermediate macroeconomics;
the introduction is a bridge to graduate study, not a repeat of that course.

## File layout

| Location | Contents |
| --- | --- |
| `macro.tex` | Shared settings and document assembly |
| `frontmatter/` | Title page and preface |
| `parts/` | Six part introductions and the chapter order within each part |
| `chapters/` | One file for each of the 25 chapters |
| `styles/` | Reusable layouts, including the model-condition cards |
| `images/` | Figures and their recovery provenance |
| `legacy/` | Original aggregate-model material, excluded from the main PDF |
| `OUTLINE.md` | Readable outline with planned content marked |
| `WRITING_GUIDE.md` | Agreed writing and visual standards for the whole book |
| `AGENTS.md` | Entry instructions for future editors |
| `REVISION_PLAN.md` | Structure, revision decisions, and progress |
| `CONDITION_AUDIT.md` | Original-to-revised condition comparison |

Part I contains one chapter, Introduction, with four sections. Growth begins
in Part II, with growth facts, Harrod--Domar (Chapter 3), Solow (Chapter 4),
and Ramsey (Chapter 5). OLG and endogenous growth follow; Chapter 8 closes
Growth with model comparisons and concrete economic situations. Fluctuations
begins with a qualitative introduction in Chapter 9, before RBC in Chapter 10.
RBC retains the original fixed-capital route and develops capital accumulation,
explicit stochastic and nominal pricing, stepwise approximation, and a solved
first-order shock experiment. Its original course text remains as comments for comparison.
Chapter 11, *New Keynesian Model: Sticky Prices*, connects RBC to the NKDSGE
framework and develops the sticky-price benchmark with complete conditions, both course
pricing routes, natural benchmarks, monetary closure, a solved policy experiment,
and a final IS–LM / AD–AS bridge. Its complete original text remains in comments.
Run `.venv/bin/python macro/scripts/verify_new_keynesian.py` from the repository
root for independent nonlinear and local-equilibrium checks.
Chapter 12, *New Keynesian Model: Sticky Wages and Prices*, develops staggered
wages with ten detailed condition cards, the full
wage-choice derivation, and a solved joint price–wage system. Chapter 13 develops
labor-market measurement and a real continuous-time search-and-matching model,
with full conditions, wage bargaining, vacancy creation, nonlinear transition
experiments, and the planner/Hosios comparison. Its participation extension
is accounting rather than a solved participation-choice model. Chapter 14 closes Fluctuations with model
comparisons, economic situations, propagation, and diagnostic reasoning.
Chapter 15 opens Part IV with the analysis boundary and solved one-good trade
across dates. It develops full two-period conditions, external accounts and
valuation, income news and return effects, productive investment, finite and
infinite horizons, and a separate borrowing-ceiling model. Ten condition cards
and the detailed algebra remain visible. Chapter 17's planned outline includes
an IS–LM–BP / Mundell–Fleming bridge, with conditional diagrams and explicit
capital-flow, expectation, and exchange-rate-regime assumptions.
Run `.venv/bin/python macro/scripts/verify_intertemporal_trade.py` for direct
utility/project optimization, constrained choices, derivatives, telescoping,
annuity limits, and gross external-account reconciliation.
Run `.venv/bin/python macro/scripts/verify_sticky_wages.py` for wage primitives
and joint-equilibrium checks, and
`.venv/bin/python macro/scripts/verify_fluctuation_synthesis.py` for the new
memory and welfare calculations. Run
`.venv/bin/python macro/scripts/verify_labor_markets.py` for primitive Markov
transitions, direct bargaining and welfare optimization, joint equilibrium
checks, and independent dynamic asset valuations. The existing welfare derivation is included directly in
`chapters/monetary-policy.tex`.

## Headings and page starts

The notes retain the existing `article` class and its visual style:

- `\part` defines a part and belongs in its `parts/` file.
- `\section` defines a chapter and belongs at the start of its chapter file.
- `\subsection` defines a section within that chapter.
- `\subsubsection` defines a further subdivision.
- `\plannedsection` defines a planned chapter and marks its status.

A shared hook in `macro.tex` starts every chapter on a new page. Sections within
a chapter continue normally. Do not add chapter-boundary page breaks to the
chapter files; the shared rule handles both existing and planned chapters.

To add a chapter, create its file in `chapters/` and add one `\input` entry to the
appropriate part file. Keep each active chapter referenced exactly once.
Chapter files use `% !TEX root = ../macro.tex` so editors can find the entry point.

## Equation, figure, and table numbering

The entry point resets all three counters at each top-level section (the
book's chapter) and prints chapter-local numbers: `(3.14)`, `Figure 3.1`, and
`Table 3.1`. Their sequences are independent; moving to the next part does not
reset chapter numbering. Keep equation labels and use `\eqref`, not literal numbers.

Every figure and table needs a numbered caption and a unique label immediately
after it. Put figure captions below the image and table captions above the
table. Shared caption styling uses small, centered text without first-line
indentation and a bold label. The caption block must not exceed the actual
image or table width; long captions wrap and remain centered within that width.
Retain explanatory notes, sources, and scope.
The shared caption hook resets both paragraph-indent settings before a caption
box opens; its local scope preserves the body's 2em indentation afterward.

For an existing in-place object, keep it and its caption in one minipage. Set
the local type **before** the image or table so hyperlink anchors point to the
object rather than below it:

```tex
\begin{center}
\begin{minipage}{\linewidth}
\captionsetup{type=figure,width=0.9\linewidth}
\centering
\includegraphics[width=0.9\linewidth]{example.pdf}
\caption{A short descriptive title.}
\label{fig:example}
\end{minipage}
\end{center}
```

Match the caption width to the image width in the same enclosing scope. For
side-by-side layouts, put the caption below the image inside its own column;
the reading guide in the adjacent column is not part of the image width.

For a table use `type=table` and wrap its caption, label, and `tabular` in
`threeparttable`, with the caption and label above `tabular`. The package
measures the typeset table, including column padding, and uses that width for
the caption. Keep the original surrounding line width and font size when
measuring, so existing paragraph-column widths remain unchanged. For example:

```tex
\begin{center}
\begin{minipage}{\linewidth}
\captionsetup{type=table}
\centering
\begin{threeparttable}
\caption{A short descriptive title.}
\label{tab:example}
\begin{tabular}{lc}
\tableheading{Variable} & \tableheading{Value}\\
Output & 1.0\\
\end{tabular}
\end{threeparttable}
\end{minipage}
\end{center}
```

Existing floating `figure` and `table` environments use ordinary `\caption`
and `\label` without a manual type. Do not force a floating layout solely to
obtain a caption or allow a caption to detach from its object.

## Table formatting

The shared `tabular` and `tabular*` hooks keep cell indentation at zero and
alternate body rows between a very light gray (3% black) and white. The header
remains white, and the first body row is gray. Each table restarts the pattern;
the settings remain local to the environment.

Wrap each nonempty header cell in `\tableheading{...}`. This makes its text
and any mathematical symbols bold without changing the body rows or their
column alignment. Keep existing column widths and all substantive content;
check the PDF if a longer bold heading changes the wrapping.

## Model-condition maps

`styles/model-setup.tex` supplies `modelsetup` and numbered `modelcondition`
cards. Preserve every substantive assumption and its qualifications when
changing the layout. Do not replace a specification by a summary or a reference
to another model merely to fit the cards on one page.

Use `\begin{modelsetup}[1]` for full-width conditions, as in Solow and Ramsey.
The default `\begin{modelsetup}` remains available for two columns when the
complete content fits naturally. Card titles group related conditions by
economic role; the number of cards follows the content.

```tex
\begin{modelsetup}[1]
\begin{modelcondition}{01}{Technology}
% State the complete technology assumptions and their equations here.
\end{modelcondition}
% Continue with the other conditions without deleting details to save space.
\end{modelsetup}
```

Each card stays intact; the layout can paginate between cards. Reserve enough
space for the heading and first card with `\Needspace`, rather than requiring
the whole specification to occupy one page. If a card becomes too long, split
it into meaningful conditions. Explanations and derivations follow the complete
specification; they do not substitute for omitted assumptions.

For the benchmark's timing, `\modelsequence{K_t,A_t,L_t}{Y_t\to C_t,I_t}{K_{t+1}}`
shows what is inherited, what happens during the period, and what becomes
available next period. Use it only when that sequence matches the model;
uncertainty or a different information structure needs an explicit alternative.
This layout leaves the existing three breakable note environments unchanged.

Solow, Ramsey, and OLG retain their original course condition blocks as TeX comments.
RBC retains its complete pre-revision text between `BEGIN ORIGINAL RBC COURSE TEXT`
and `END ORIGINAL RBC COURSE TEXT`.
Ramsey uses `BEGIN ORIGINAL COURSE ASSUMPTIONS`; Solow uses
`BEGIN ORIGINAL SOLOW COURSE ASSUMPTIONS`, each with a matching `END` marker. OLG uses
`BEGIN ORIGINAL OLG COURSE ASSUMPTIONS` and its matching end marker.
These are comparison records, not active alternate versions. Their labels
would conflict if both versions were typeset. See `CONDITION_AUDIT.md` for the
condition-by-condition restoration and the theoretical qualifications retained.

## Compile

From this directory, with the installed TeX Live toolchain:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error macro.tex
```

Compile the entry point rather than individual chapter files. It supplies all
shared definitions and resolves chapter, equation, and part references.
