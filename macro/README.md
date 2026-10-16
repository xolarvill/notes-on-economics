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
| `chapters/` | One file for each of the 21 chapters |
| `images/` | Figures and their recovery provenance |
| `legacy/` | Original aggregate-model material, excluded from the main PDF |
| `OUTLINE.md` | Readable outline with planned content marked |

Part I contains one chapter, Introduction, with four sections. Growth begins
in Part II. The existing welfare derivation is included directly in
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

## Compile

From this directory, with the installed TeX Live toolchain:

```sh
latexmk -norc -pdf -interaction=nonstopmode -halt-on-error macro.tex
```

Compile the entry point rather than individual chapter files. It supplies all
shared definitions and resolves chapter, equation, and part references.
