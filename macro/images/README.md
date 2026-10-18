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

## Growth-synthesis diagnostic paths

`growth_path_diagnosis.pdf` is an original two-panel vector illustration.
There are no data inputs or estimated model responses. The benchmark is
Y(t)=100 exp(0.03 t). All changes occur at model date 10. The temporary path
multiplies the benchmark by 1-0.10 exp(-(t-10)/4) after that date (baseline
utilization 0.90, impact utilization 0.81, unchanged capacity). The lasting
level loss multiplies it by 0.90. The slower-trend path multiplies it by
exp(-0.015(t-10)), lowering growth from 3% to 1.5% without an initial jump.
The panels show log output relative to initial output and the percentage
deviation from the common benchmark. These are distinct constructed cases,
not an identified decomposition of observed GDP.

Regenerate with the uv-managed environment, numpy, and matplotlib:

```sh
.venv/bin/python macro/images/growth_path_diagnosis.py
```

The generator checks the initial paths, impact change, subsequent slopes,
and utilization recovery before saving the figure with embedded fonts and
without PDF creation/modification timestamps.

## Fluctuation impulse and propagation

`fluctuation_impulse_propagation.pdf` is an original two-panel vector figure
with no empirical inputs. It plots an innovation of -1 at period zero and zero
at all other dates, then x(t)=rho*x(t-1)+innovation(t), starting from zero,
for rho=0, 0.5, and 0.85. The lower panel holds the impact fixed and varies
persistence. These are constructed dynamics, not estimated structural impulse
responses. The dimensionless deviations are not percentages of GDP, and
periods are not assigned a calendar duration.

Regenerate with the uv-managed environment, numpy, and matplotlib:

```sh
.venv/bin/python macro/images/fluctuation_impulse_propagation.py
```

The generator checks the zero prehistory, common impact, geometric response,
and cumulative deviation before embedding fonts and omitting PDF timestamps.

## RBC responses from the solved local equilibrium

`rbc_impulse_responses.pdf` is an original six-panel vector plot of productivity,
output, consumption, investment, hours, and inherited capital. It uses the RBC
chapter's first-order equilibrium, not independently invented response curves.
There are no data inputs, parameter estimates, or claims of empirical fit.

Illustrative quarterly parameters are alpha=0.33, beta=0.99, delta=0.025,
sigma=1, phi=1, Abar=1, and steady hours=1/3. Chi is derived from the steady
labor condition. Both paths begin with the steady capital and a date-zero log
productivity innovation of 0.01; all later innovations are zero. The consumption
and capital policies are solved separately for rho_a=0.95 and rho_a=0, using
coefficient matching and the stable root shown in the chapter. Vertical units
are 100 times log deviations, approximately percentage changes; dates are quarters.

Regenerate with the uv-managed environment, numpy, and matplotlib:

```sh
.venv/bin/python macro/images/rbc_impulse_responses.py
```

The generator checks the original linear labor, resource, capital, and Euler
equations for both paths and confirms predetermined impact capital. It embeds
fonts and omits PDF timestamps. Independent numerical checks of the primitive
conditions, nonlinear error order, and exact special case are recorded in
`../DERIVATION_AUDIT.md`.

## New Keynesian responses from the solved local equilibrium

`nk_impulse_responses.pdf` is an original six-panel vector figure: output gap,
quarterly inflation, nominal and expected real rates, price level, and money.
It uses the analytic local equilibrium in Chapter 11, with beta=.99,
sigma=phi=1, alpha=1/3, goods elasticity=6, Calvo retention=.75,
phi_pi=1.5, phi_x=.125, rho_nu=.5, money curvature nu_m=2, and a single
initial log gross-rate intercept innovation of .001. Initial deviations are
zero; all later innovations vanish. There is no data, estimation, or empirical
calibration claim. Money accommodates the interest rule.

Regenerate from the repository root:

```sh
.venv/bin/python macro/images/nk_impulse_responses.py
```

The generator checks the original linear IS, Phillips, interest-rule and
money-demand equations, price accumulation, and coefficient matching. Rate
panels use 10,000 times quarterly log deviations (unannualized basis points);
other panels use 100 times log deviations. Dashed level lines show the
long-run price/money displacement. Fonts are embedded and PDF timestamps omitted.
Additional independent nonlinear checks are in `../scripts/verify_new_keynesian.py`.
