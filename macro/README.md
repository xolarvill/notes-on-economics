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
[CONDITION_AUDIT.md](CONDITION_AUDIT.md) records the Solow, Ramsey, and OLG condition
comparisons. The intended reader has completed intermediate macroeconomics;
the introduction is a bridge to graduate study, not a repeat of that course.

## File layout

| Location | Contents |
| --- | --- |
| `macro.tex` | Shared settings and document assembly |
| `frontmatter/` | Title page and preface |
| `parts/` | Six part introductions and the chapter order within each part |
| `chapters/` | One file for each of the 24 chapters |
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
The existing welfare derivation is included directly in
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
