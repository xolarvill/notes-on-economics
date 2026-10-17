# Figure sources

## Recovered phase diagrams

Both images were extracted from the existing 63-page `macro/macro.pdf`,
preserved in Git as PDF blob `d858b27a0eefb8aaa289bd9a33add7eb5ff96922`.
Page numbers below count from the first PDF page, including the title page.

| File | Source PDF page | Dimensions |
| --- | --- | --- |
| `solow_phase_diagram.png` | 12 (also embedded identically on page 13) | 1194 × 858 pixels |
| `ramsey_phase_diagram.png` | 27 | 714 × 726 pixels |

The embedded images were recovered with `pypdf`, including their transparency,
and saved as lossless PNGs. They retain the images available in the old PDF;
they are not screenshots, redrawings, or replacements from the web. The original
standalone image files and their earlier provenance remain unavailable.

## OLG illustration generated from equations

`olg_capital_and_consumption.pdf` is an original vector figure, not a recovered
image. It plots the log/Cobb--Douglas capital map and stationary consumption
using alpha=0.25, beta=0.96, population factor N=1.02, and full depreciation.
There are no empirical inputs. Both curves and the capital markers are
computed from the equations stated in the OLG chapter.

Regenerate from the repository root with the uv-managed project environment:

```sh
.venv/bin/python macro/images/olg_capital_and_consumption.py
```

The generator requires numpy and matplotlib. It embeds fonts and omits PDF
creation/modification timestamps. Its parameters refer to the model's life-stage
period; they are not annual demographic or financial estimates.

## Endogenous-growth illustrations generated from equations

`endogenous_ak_paths.pdf` compares log-consumption paths in the optimizing AK
example: B=0.10 versus 0.12, depreciation=0.02, rho=0.04, theta=2, and baseline
initial capital=1. One comparison gives the baseline stock a 10% increase.
Each path starts with its stated parameters at date zero. Time is in model
units, and the figure is not an estimated event study.

`endogenous_allocation.pdf` plots the static two-firm output function
2*sqrt(k1)+sqrt(1-k1), with total capital fixed at one. It marks the efficient
allocation (0.8, 0.2) and the hypothetical wedge-distorted allocation (0.5, 0.5).
The loss is 1-3/sqrt(10), approximately 5.13% of efficient output.

Both are original vector PDFs generated without external data. From the
repository root, using numpy and matplotlib in the uv-managed environment:

```sh
.venv/bin/python macro/images/endogenous_growth_figures.py
```

The generator embeds fonts and omits PDF creation/modification timestamps.
