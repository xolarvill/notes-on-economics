# Editing and compiling the macro notes

Compile `macro.tex`. It is the single entry point and contains the shared
formatting, commands, table of contents, and file references. Chapter text is
kept in chapter files rather than mixed into the entry point.

## File layout

| Location | Contents |
| --- | --- |
| `macro.tex` | Shared settings and document assembly |
| `frontmatter/` | Title page and preface |
| `parts/` | Six part introductions and the chapter order within each part |
| `chapters/` | One file for each of the 22 chapters |
| `styles/` | Reusable layouts, including the model-condition cards |
| `images/` | Figures and their recovery provenance |
| `legacy/` | Original aggregate-model material, excluded from the main PDF |
| `OUTLINE.md` | Readable outline with planned content marked |

Part I contains one chapter, Introduction, with four sections. Growth begins
in Part II, with growth facts, Harrod--Domar (Chapter 3), Solow (Chapter 4),
and Ramsey (Chapter 5). The existing welfare derivation is included directly in
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

`styles/model-setup.tex` supplies a two-column `modelsetup` layout. Put one
short condition in each `modelcondition` card, with a sequence marker and a
meaningful title. A map distinguishes the environment, technology, agents,
given states, behavior, and equilibrium conditions; categories should follow
the model rather than a mandatory count of cards.

```tex
\begin{modelsetup}
\begin{modelcondition}{01}{Technology}
Constant returns in capital and effective labor.
\[
Y_t=F(K_t,A_tL_t).
\]
\end{modelcondition}
% Add the other short cards here.
\end{modelsetup}
```

Rows have matching heights. Each short card stays intact; the grid can paginate
between rows. Reserve space before the section heading with `\Needspace` when
the full overview should be visible together (Solow reserves 34 text lines).
Keep cards concise instead of forcing a long derivation into an unbreakable
box. Explain assumptions, notation, and derivations in the following prose.

For the benchmark's timing, `\modelsequence{K_t,A_t,L_t}{Y_t\to C_t,I_t}{K_{t+1}}`
shows what is inherited, what happens during the period, and what becomes
available next period. Use it only when that sequence matches the model;
uncertainty or a different information structure needs an explicit alternative.
This layout leaves the existing three breakable note environments unchanged.

The Ramsey chapter retains its original course assumption block as TeX comments,
between `BEGIN ORIGINAL COURSE ASSUMPTIONS` and `END ORIGINAL COURSE ASSUMPTIONS`.
The live six-card overview follows it. Compare or restore that block in place;
do not typeset both versions together, since their assumption labels coincide.

## Compile

From this directory, with the installed TeX Live toolchain:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error macro.tex
```

Compile the entry point rather than individual chapter files. It supplies all
shared definitions and resolves chapter, equation, and part references.
