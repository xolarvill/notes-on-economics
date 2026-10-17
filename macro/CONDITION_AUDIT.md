# Model conditions and teaching content: preservation

The layout may change; it must not reduce the model specification to a summary.
The live conditions below are full-width numbered cards, followed by the
existing explanations and derivations. Original course wording remains in
commented blocks within each chapter for comparison, including statements that
need theoretical qualification. These comments are not alternate active sources.

## Solow

Comparison source: `862ae0e^:macro/chapters/solow.tex`, the original
“Economic Environment and Specific Assumptions” section.

| Original condition or explanation | Live location and treatment |
| --- | --- |
| Two sectors; output divided into consumption and investment; saving equals investment | Card 01, with resource equations also in cards 02 and 08 |
| Many homogeneous households; imposed saving and consumption behavior | Card 02 explicitly restores homogeneity and the absence of household intertemporal optimization |
| Saving share in [0,1] | Card 02 preserves the full range, while identifying (0,1) as the interior benchmark used by later results |
| Many homogeneous firms using a common method; aggregate production | Card 03 restores common technology and aggregation; firms maximize profits, consistent with the original section's own final profit-maximization problem |
| Competition | Cards 03 and 07 state price-taking factor markets, marginal-product prices, and clearing explicitly |
| Inelastic labor, wage income, household ownership of capital, rental income | Cards 02 and 04 |
| Given initial capital and exponential depreciation | Card 04 includes initial stocks and both discrete and continuous capital laws |
| Net return equals rental price less depreciation | Card 04 restores the relation and maps original R to current q, avoiding confusion with a discrete gross return |
| Distribution of capital outside the aggregate question | Card 04 restores this with the common saving-share and no household-specific constraint qualifications |
| Labor and capital market-clearing equations | Card 07 restores both explicit supply-demand equalities |
| Technology free and publicly available | Card 05 states availability separately from its exogenous growth path |
| Continuous, differentiable, positive production with diminishing marginal products and constant returns | Card 06 states the restrictions explicitly, including positive-input domains |
| Labor-augmenting production and a stable capital-output ratio | Card 06; “Production and normalization” derives constant K/Y conditional on a balanced growth path, rather than asserting it from functional form alone |
| Hicks-neutral alternative | “Production and normalization” restores the alternative and the Cobb--Douglas conversion, including the growth-rate qualification |
| Constant-returns equation, scale intuition, and intensive normalization | Cards 06 and 08; “Production and normalization” retains the replication explanation and restores the original scale and omitted-factor motivations as interpretations |
| Inada restrictions, their limits, and Cobb--Douglas as a chosen form | Card 06 and “Production and normalization”; limits apply to marginal products, not output levels; convenience is distinguished from deduction |
| Profit maximization, factor prices, Euler exhaustion, zero profits | Cards 03 and 07 and the existing “Prices and market clearing” derivation |
| Main production, saving-investment, and capital equations | Card 08 gives all three together |

The original description of firms as non-optimizing conflicts with its own
profit-maximization equations. It remains in the comparison comments; the live
specification distinguishes imposed household saving from optimizing firms.
Likewise, the original Inada output-level limits remain only in the comparison
record; the live marginal-product limits retain the correction already discussed.

## Ramsey

Comparison source: the complete original course assumption block retained in
`chapters/ramsey.tex` before the live “Assumptions” section.

| Original condition | Live location and treatment |
| --- | --- |
| Same production environment as Solow, with labor-augmenting technology | Card 01 spells out the production properties instead of saying only “Solow properties” |
| Exogenous population growth, technology growth, and zero depreciation | Card 02 preserves the course benchmark and distinguishes it from general-delta formulas |
| Original technology-growth symbol a | Card 02 explicitly maps a to the unified g notation |
| Competitive firms, homogeneous technology, representative formulation | Card 05 states each separately; homogeneity is not treated as a synonym for competition |
| Hire labor and capital in competitive factor markets; Y=F(K,AL) | Cards 01 and 05, with the actual firm maximization problem |
| Firms owned by families; income accrues to owners | Cards 03 and 05 restore ownership explicitly, before explaining zero profits |
| Homogeneous families | Card 03 specifies many identical price-taking dynasties |
| Population of each family grows at n | Card 02 restores dynasty population growth and explains aggregation to L |
| One unit of labor per member | Card 02 |
| Household income includes labor income, capital income, and firm profit shares | Card 03 writes all three into the budget before imposing zero profits |
| Household maximizes utility | Card 04 states the objective and its budget and solvency constraints, including the population weighting convention |
| Discount factor beta=1/(1+rho) | Card 04 restores it next to continuous discounting and distinguishes the time conventions |
| No-Ponzi restriction and the refinancing discussion | Card 07 introduces the restriction; the immediately following solvency subsection retains the explicit formula and distinguishes solvency from transversality |

The modern CRRA objective, effective discount restriction, and planner-market
equivalence conditions introduced in the preceding revision remain explicit.
They are not attributed verbatim to the original course list or Ramsey's 1928
objective. All previously added modeling intuition and derivations remain.

## OLG

Comparison source: `b69162a:macro/chapters/olg.tex`, before the OLG revision.
Original conditions remain in a commented block before the live eight-card
specification. The rest of the original chapter remains recoverable in Git.

| Original material | Live location and treatment |
| --- | --- |
| Finite lives overlapping at a date | Modeling questions, cards 01 and 04, and the cohort timeline |
| “Meet only once” note | Blue note retains the contracting question but corrects the claim that overlapping generations preclude intertemporal allocation; capital saving does transfer consumption across a life |
| Solow, RCK, and OLG comparison | Full comparison section, with a table and equations under a common time, population, and depreciation convention |
| Aggregate consumption, population law, aggregate saving | Cards 01 and 07 explicitly retain the equations; a denotes saving per young person and mathematical A young asset purchases, avoiding confusion with national saving |
| Household objective and both budgets | Cards 05 and 07; household section retains both multipliers, all interior conditions, and the Euler derivation with a consistent multiplier sign |
| CRRA utility, saving formula, wage derivative, return derivative, all three curvature cases | Household section retains and expands every step; green note explains substitution and retirement-resource effects; the log limit is handled separately |
| Firm profit maximization and factor prices | Card 06 and firm section; aggregate inputs and per-worker prices are distinguished, and zero profits do not erase ownership income |
| Depreciation and R=f'(k) in the later course formulas | General delta is explicit throughout; R=f'(k) is retained as the full-depreciation special case, alongside the no-depreciation convention |
| Capital law, implicit saving-return feedback, unfinished general steady state | Capital section derives K_next=L*a from age-specific consumption; it separates young purchases from gross investment and net national saving, states the general scalar steady-state equation, and derives a conditional local slope |
| Green log example and explicit capital stock | The full log derivation, wage-saving rule, steady state, global positive-stock convergence, and exact log-deviation path remain; a green frame summarizes the mechanism |
| Solow Golden Rule and dynamic-efficiency comparison | Welfare section derives the correct stock exponents and conditional overaccumulation test; inefficiency is possible, not inevitable |
| Ramsey stationary Euler and no overaccumulation | Comparison uses the matching discrete dynasty objective and its finite-welfare restriction; it does not treat an Euler equation alone as a welfare theorem |
| OLG planner and social discounting | Welfare section keeps a planner formulation, distinguishes social cohort weights from private beta, includes the initially old, and derives the multiplier and stationary-return conditions |
| Golden Rule consumption and the Cobb--Douglas inefficiency inequality | General-delta age-weighted consumption, gross and net return tests, full-depreciation parameter threshold, numerical example, and a feasible all-cohort Pareto improvement |
| Summary of the three models | Comparison table and closing discussion retain the distinctions without treating finite lives alone as proof of inefficiency |
| Planned population, pension, and debt section | Expanded into support-ratio accounting, PAYG and funded budgets, saving responses and constraints, transition questions, debt financing and portfolio/resource consolidation |

The original two green calculation boxes become detailed mainline derivations
with green mechanism summaries, rather than disappearing. Additional blue
notes separate gross and net returns, young and national saving, and individual
versus social accounting. A red worked resource experiment establishes why
an overaccumulating path can permit a Pareto improvement. The complete
condition cards remain distinct from these callouts.

## Endogenous Growth and Resource Allocation

The original chapter (`8306854:macro/chapters/endogenous-growth.tex`) contained
only a planned outline: AK/human capital; ideas, innovation and incentives;
allocation and aggregate productivity. It contained no existing assumption
list, worked derivation, or callout to archive. All three topics are developed,
with explicit bridges from intermediate macroeconomics and the Ramsey chapter.

| Specification | Complete conditions and scope |
| --- | --- |
| Optimizing AK | Five cards specify continuous time, fixed population, ownership, one-good linear technology, CRRA choice, competitive returns, feasibility, transversality, positive growth and finite-welfare restrictions |
| AK spillover construction | Text states firm technology, common capital/knowledge spillover, price-taking behavior, labor clearing, symmetric aggregation, and the private/social return distinction; growing solutions are conditional on admissibility |
| Human capital | Four cards specify two inherited stocks, work and learning time, production, goods and skill laws, skill depreciation, objective, terminal conditions and interior balanced-path restrictions; arbitrary transitions are not claimed to be solved |
| Expanding varieties | Five cards specify fixed labor and population, patent ownership, final demand, flow intermediate resource costs, exclusive rights, symmetric monopoly, research labor, knowledge spillovers, free entry, asset pricing, household budgets and terminal restrictions |
| Semi-endogenous technology experiment | The altered research law, growing labor, and fixed positive research share are explicit; the earlier endogenous share is not carried over, and the calculation is not represented as the complete new competitive equilibrium |
| Static allocation | Three cards specify two firms, fixed complementary inputs and capital, technologies, competitive rental choice, rebated tax wedges and resource clearing; this is a one-date allocation comparison, not a standalone growth engine |

Symbols used for different technology coefficients are defined within each
experiment. Teaching simplifications are distinguished from the full Lucas
and Romer originals. The two original figures use only stated model equations
and hypothetical parameters; there are no empirical estimates in the examples.
