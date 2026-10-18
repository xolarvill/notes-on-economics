# Mathematical derivations: restoration and granularity

The standard is concise prose and fully visible mathematics. A correct final
formula or a named theorem is not a substitute for the intermediate operations.
This audit is distinct from `CONDITION_AUDIT.md`: a complete specification does
not imply that the original derivation paths have been preserved.

Comparison sources:

- Solow: `862ae0e^:macro/chapters/solow.tex`.
- Ramsey: `ca1b9ac^:macro/chapters/ramsey.tex`.
- OLG: `c861908^:macro/chapters/olg.tex`.
- RBC: `f54f5c9:macro/chapters/rbc.tex`; the complete course text is archived in comments.
- Endogenous growth had only an outline before its recent development; its
  calculations need the same granularity, but are not recoveries of old proofs.

Preserve valid theoretical qualifications. Correct signs, time indices,
normalization, and endpoint restrictions before restoring a route; do not
restore incorrect expressions merely to reproduce the old number of lines.
All condition cards, intuition, examples, figures, and table formatting remain.

## Ramsey: restored routes

| Route | Operations now visible |
| --- | --- |
| Two-period choice | Separate asset budgets, elimination, chain-rule derivative, geometry, and individual Lagrangian derivatives |
| Two dates to T dates | Individual budgets, discounted summation, cancellation of intermediate assets, present-value constraint, adjacent first-order conditions, and their ratio |
| Sequential finite-horizon method | Each asset's two budget appearances, both discounted multiplier terms, and the last valid Euler comparison; fixed terminal asset is not an interior choice |
| Infinite production economy | Full derivatives of consumption and next capital, cancellation of beta powers, multiplier substitution, and CRRA powers; infinite TVC distinguished from finite zero terminal assets |
| Hamiltonian | Utility normalization, present-value augmented objective, integration by parts with the boundary term, interior variations, present-value costate, current-value conversion by product rule, and CRRA Euler algebra |
| Bellman | Splitting the infinite sum into current and continuation utility; full policy chain rule, explicit bracket cancellation, next-date envelope condition, and Euler substitution |
| Exact log/Cobb--Douglas rule | Value-function substitution, optimization, both logarithms expanded, coefficient and constant matching, and saving/consumption rules |
| HJB | Short-interval accumulation, discount and value expansions, subtraction/division/limit, full optimal-control chain rule, cancellation, and the costate along the path |
| Linearization | Four Jacobian entries, zero constants, determinant expansion, eigenvectors, both exponential modes, stable-mode restriction, integration, and half-life logarithms |
| Original second-order method | Differentiate capital motion, substitute consumption motion, construct the second-order ODE, differentiate an exponential guess, and recover the characteristic polynomial; retain the policy-slope method as an additional route |
| Welfare and taxation | CRRA/log consumption-equivalent algebra, household-government budget cancellations, private after-tax Euler, tax steady state and derivative, initial-consumption perturbation, and numerical stock calculation |

## Solow: restored calculations

- Factor-price first-order derivatives, the scale derivative behind Euler's
  theorem, factor exhaustion, and differentiation of the intensive production function.
- Exact next-date normalization, subtraction over a common denominator,
  steady-state rearrangement, Cobb--Douglas powers, and the level elasticity.
- Explicit iterations, relative deviations, logarithmic target times and
  half-lives, integer dates, and the distinction between a local model and
  the nonlinear path.
- Product/quotient rules for effective-worker capital, separation and
  integration of the local ODE, and an integrating-factor solution of the
  exact Cobb--Douglas transformed ODE, including its initial condition.
- Golden Rule powers and saving share; resource cost under imperfect capital
  conversion; collection of powers in the augmented human-capital example.

## OLG: restored calculations

- Individual Lagrangian derivatives and elimination of both multipliers;
  CRRA powers, intermediate saving ratios, full return-derivative chain rule,
  and the log case's rearrangement.
- Firm derivatives before normalization, liquidation/resource accounting,
  division by next-period cohort size, implicit differentiation of the
  capital law, steady-state powers, and the exact log transition.
- Reciprocal powers for the stationary return, each inequality in the
  dynamic-inefficiency threshold, and matching Solow/Ramsey stock comparisons.
- Aggregate planner derivatives with cohort sizes, within-cohort cancellation,
  stationary social multiplier weights, PAYG cross-multiplication, and
  debt-financed asset clearing/differentiation.

## Endogenous growth: newly expanded calculations

- AK Hamiltonian derivatives, consumption integration, capital integrating
  factor, evaluation of the integral, and the full candidate terminal value
  before imposing the restriction on initial consumption.
- Firm-specific spillover derivatives before symmetry; two-stock production
  derivatives, time-choice cancellation, equal shadow-value growth, the work
  fraction, and the balanced physical/human-capital ratio.
- Final-demand inversion, monopoly profit differentiation, input quantity and
  markup, wage and profit substitution, patent-value division, and the research
  labor equation.
- Planner input choice, elimination of research labor, transformed-state
  differentiation, optimizing growth conditions, and a common-denominator
  comparison of decentralized and planner growth.
- Log differentiation of semi-endogenous idea growth, chain rule and integration
  at fixed research labor, allocation multipliers, capital-share powers,
  explicit output aggregation, and private wedge derivatives.

## RBC: course routes preserved and the capital model completed

| Route | Visible intermediate operations |
| --- | --- |
| Nominal-bond household | Resources-minus-expenditure Lagrangian, both bond date contributions, substitution of marginal utility per currency unit, and expectation-preserving division |
| Labor and capital choice | Both CRRA/log derivatives, work derivative, MRS, Frisch elasticity, two-date capital payoff, real stochastic discount factor, and covariance pricing |
| Firm and aggregate accounts | Both input derivatives before capital normalization, factor-income exhaustion, household-to-resource cancellation, planner partial derivatives, and exact equilibrium list |
| Course fixed-capital limit | K=1 and no investment choice; Y=C under explicit zero depreciation/expenditure assumptions, fixed-factor income, full hours solution, and productivity elasticities |
| Capital and investment | Deterministic steady rental, output-capital ratio, expenditure shares, capital-hours ratio, hours and preference weight; current stock distinguished from next stock |
| Both original approximation routes | Taylor expansion of log(1+d), inverse exponential expansion, remainder order, exact production/price/labor log identities, weighted goods and capital sums |
| Expected Euler | Return expansion with beta*q rental weight, product before cancellation, removal of second-order terms inside conditional expectation, and the original expectation warning corrected explicitly |
| Exact special case | Full-depreciation/log saving rule through every-state cancellation, hours solution, feasibility, and expected terminal expression |
| General local solution | Labor substitution, all reduced coefficients, consumption-rule substitution, quadratic expansion and roots, stable selection, productivity-coefficient matching, and state transition |
| Shock experiment | Stated quarterly parameters and steady values, impact calculations, separately solved persistent and iid cases, resource-based investment response, and inherited-stock propagation |
| Original nominal attachment | Gross-rate and inflation definitions, nominal Euler expansion, first-order Fisher comparison, money-demand log algebra, and qualified nominal level rescaling |

Numerical verification covers 27 curvature/persistence combinations, primitive
derivatives, all resource accounts, and stable roots recovered independently
from finite differences of the nonlinear equations. Exact special-case saving
and hours are checked against direct numerical optimization. Exact resource
and stochastic Euler residuals fall quadratically when perturbations shrink.
The nominal/Fisher approximation has the same error-order check. All displayed
impact values are checked against the solved policies; the iid comparison
re-solves behavior and checks capital's predetermined timing. The figure
generator retains checks against the unreduced linear equations.

## Verification scope

Numerical checks independently evaluate finite budgets and Euler conditions,
Bellman identities and envelope derivatives, short-interval HJB residuals,
integration by parts including endpoints, the Ramsey Jacobian/eigenvectors,
tax perturbation signs, consumption-equivalent formulas, the exact Solow path,
OLG utility maximization and derivative formulas, debt steady states, AK
terminal expressions, human-capital costates, patent pricing and income
accounting, planner transformations, and efficient allocation.

All complete condition-card bodies and original course comment lines were
compared byte for byte with the pre-restoration source. They remain unchanged.
This record names the routes checked; it does not use total page count as
proof of preservation. Final rendering checks are recorded in REVISION_PLAN.md.

## New Keynesian: both pricing routes and unfinished calculations

Comparison source: `af17be9:macro/chapters/new-keynesian.tex`. Its complete
950-line text is recoverable from source comments; the independent checker
verifies the decoded source's SHA-256. Corrected classroom special cases are
retained visibly, not just stored as a backup.

| Route | Intermediate operations visible in the live chapter |
| --- | --- |
| CES expenditure minimum | Chain-rule derivative, multiplier FOC, demand, constraint substitution, dual index, and bill check |
| CES utility maximum | Separate multiplier, demand, basket substitution, shadow value, expenditure, and equivalence |
| Finite goods | 1/J derivative factor, demand with J, power collection, dual price index, equal-price units, and n-to-epsilon translation |
| Intertemporal household | Consumption/hours derivatives and both dates' bond/money contributions; multiplier substitutions and opportunity cost; face-value versus carrying-value bond budgets |
| Money approximation | Log opportunity cost, derivative 1/[i(1+i)], subtraction of reference, net-log versus gross-log conversion, and income-elasticity qualification |
| Firm cost | Conditional cost Lagrangian, MPN, inverse technology, total-cost derivative, and flexible-price profit chain rule |
| Calvo profit | Survival probability, owner SDF, demand derivative, every profit derivative, FOC rearrangement, weighted ratio, time-zero and general-date versions |
| Discount cancellation | Demand and SDF substitution, identified common current factor, both remaining beta^k factors, own-price cost response, and closed nonlinear reset equation |
| Taylor pricing | Constant and individual variable terms on LHS/RHS, exact cancellation of weight deviations, own-price correction, target and recursive expected reset relation |
| NKPC first route | CES price index, bivariate Taylor expansion, reset-relative-price identity, substitution into recursion, and Phillips coefficient |
| Original long-sum route | Price differences expanded into inflation sums, discount powers on each term, rearranged double series, two recursions, and explicit elimination |
| NKPC vintage route | Finite backward iteration with inherited remainder, geometric vintage limit, t and t+1 identities, target substitution, expanded coefficient cancellation, and inflation differences |
| Gap and benchmarks | Exact dispersion aggregation/recursion and first-order cancellation; wage and MPN substitution, natural level and deviation, alternative alpha=0 target route, and planner derivative |
| Dynamic IS | Exact stochastic Euler, product expansion, cancellation of constant, natural real rate, and explicit subtraction to the gap equation |
| Fixed-duration example | Three-date profit FOC, discount-normalized target average, exact CES aggregate, local average, and replacement-price inflation identity |
| Monetary equilibrium | Money demand separated from a quantity rule, price accumulation, rate rule, output-level/gap convention conversion, complete two-row reduced matrix |
| Determinacy | Trace/determinant, characteristic equation, unit-disk transformation, quadratic root test, expanded Taylor principle, forward iteration, and bounded-solution uniqueness |
| Shock solution | Phillips and IS coefficient substitutions, full denominator, positivity expansion, implied output/inflation recursions, real/nominal rates, accumulated prices, completed money path and innovation derivative |
| Persistence | Forward NKPC iteration and terminal restriction, technology-shock coefficient equations, contract indexation with adjusted prices and normalization, separate sticky-information interpretation |
| Intermediate bridge | Derived conditional IS and LM, full elimination to price-level AD, NKPC-to-AS transformation, intersection solution, and contrast with interest-rule demand in inflation space |

Run `.venv/bin/python macro/scripts/verify_new_keynesian.py` from the repository
root. It compares CES allocations and nonlinear Calvo pricing with direct
optimization; checks pricing and dispersion error orders, money derivatives,
1,215 parameter/eigenvalue cases, 100 reconstructed diagram intersections,
and the stochastic Euler approximation. The figure generator separately checks
every unreduced local equilibrium equation and all six plotted paths. These
checks concern algebra and the stated approximations, not empirical fit.

### IS–LM illustrations

The paired figures additionally show the same monetary expansion using a
linear intermediate goods/money specification and the derived conditional
Euler/MIU system. The new text explicitly collects the intermediate goods
equation into its inverse IS curve. A second pair holds money fixed while
expected future consumption changes, then replaces the money closure by a
Taylor-rule MP relation. Substituting the NKPC into the Taylor rule gives
its slope phi_x+phi_pi*kappa in interest-rate–gap space.
`images/islm_comparison.py` independently verifies every plotted intersection
against the underlying equations and checks the shift-arrow endpoints.
All pre-existing mathematical expressions, condition cards, and original
course comments remain unchanged.
