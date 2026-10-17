# Notes on Advanced Macroeconomics: Outline

Part I contains one Introduction chapter with four sections. Every chapter starts
on a new page; sections within a chapter continue normally. Chapters and sections
marked **planned** specify the scope of later writing.

`macro.tex` contains shared settings and assembles `frontmatter/` and `parts/`.
All chapter text is in `chapters/`, with one file per chapter. See `README.md`
for the file layout and editing conventions.

The original Classical / Keynesian chapters remain in `legacy/aggregate-models.tex`
outside the main PDF. The existing welfare derivation is in the Monetary Policy
chapter of Part V.

## Part I: Introduction

### 1. Introduction

- Growth, fluctuations, and their interaction
- From aggregate relations to individual decisions
- Reading a dynamic equilibrium
- Accounting and notation used in these notes

## Part II: Growth

### 2. Growth Facts and Growth Accounting

- Income levels, growth rates, and convergence
  - Which output, and per whom?
  - A level difference is not a growth-rate difference
  - What does convergence mean?
- Capital, labor, and productivity
  - From a production function to growth accounting
  - Labor productivity and finite-period contributions
  - What is inside the residual?
- From accounting to a growth model
  - Level accounting and joint determination
  - Connecting TFP to labor-augmenting technology

### 3. Harrod--Domar: Investment and Growth

- From a spending equilibrium to a growth problem
- Domar: demand must keep up with capacity
  - A flow affects demand; its accumulation affects capacity
  - Deriving the required investment path
- Harrod: which growth rate validates investment plans?
  - Actual and warranted growth
  - Why a deviation can amplify
  - Natural growth and the employment constraint
- Fixed proportions, compatibility, and the route to Solow

### 4. Solow Model

- From the growth question to the model
  - What if production can adjust?
  - Choose one adjustment mechanism
  - Close the system and choose a useful intensity
- Economic environment and assumptions
  - Complete conditions in eight full-width cards; original retained in TeX comments
  - Resources, timing, and behavior
  - Production and normalization
  - Prices and market clearing
- Solow model in discrete time
  - Deriving the law of motion
  - A steady state and the path toward it
  - What grows on a balanced growth path?
  - Saving, rebuilding, and conditional convergence
  - Local convergence speed
- Solow model in continuous time
  - The same mechanism with continuous adjustment
  - Local approximation and an exact Cobb--Douglas solution
- The Golden Rule and the cost of saving
- Extensions: which assumption needs to change?
  - Investment spending and productive capital
  - Accumulating human capital
  - Technology adoption and catch-up
  - Removing diminishing returns: the AK benchmark
  - Fixed land and the transition to modern growth

### 5. Ramsey Model

- From a saving rule to a saving decision
- Assumptions
  - Complete conditions in seven full-width cards; original retained in TeX comments
  - Notation, preferences, solvency, and transversality
- Solving the consumption--saving problem
  - The planner's problem and decentralization
  - Lagrangian: the adjacent-date trade-off
  - Hamiltonian: saving with continuous adjustment
  - Bellman and HJB: valuing the remaining opportunities
- Intertemporal equilibrium and economic adjustment
  - Steady state, phase diagram, and adjustment
- Linearization and the saddle path
  - The local system and its eigenvalues
  - The same restriction by undetermined coefficients
- Maximizing welfare
  - Consumption paths, Golden Rule, and consumption-equivalent welfare
- Taxation and capital accumulation
  - Consolidated budgets and real resource use
  - Lump-sum financing versus the capital income tax wedge
  - Steady states, transitions, and a numerical comparison

### 6. OLG Model

- From retirement needs to overlapping generations
  - Finite lives, continuing economies, and retirement assets
  - Market closure and contracts with future entrants
- Assumptions and the cohort timeline
  - Eight complete condition cards; original course conditions retained in comments
  - A cohort's lifetime versus a date's resource constraint
- Household optimization and life-cycle saving
  - Budgets, multipliers, and the Euler condition
  - CRRA saving, wage and return derivatives, and the log case
- Firm optimization and the return to ownership
  - Rental price, net return, gross payoff, and depreciation conventions
- Capital accumulation and equilibrium dynamics
  - Young wealth versus aggregate saving
  - General implicit equilibrium and local stability
  - Log/Cobb--Douglas steady state and exact transition path
- Comparing Solow, Ramsey, and OLG
- Dynamic efficiency and intergenerational welfare
  - Cohort-weighted consumption and the Golden Rule
  - A feasible Pareto improvement from the same initial stock
  - An illustrative overaccumulation case and two-panel figure
  - Private discounting versus social cohort weights, including the initially old
- Population, pensions, and public debt
  - Support ratios and capital per worker
  - Pay-as-you-go budgets, saving, and transition conditions
  - Funded accounts and voluntary-saving offsets
  - Public debt portfolios, taxes, resource consolidation, and local crowding

### 7. Endogenous Growth and Resource Allocation

- From intermediate macroeconomics and Ramsey to a growth engine
  - Familiar claims, missing accumulation mechanisms, and endogenous saving versus growth
- AK: retain Ramsey's choice, change the return
  - Complete conditions and the inherited stock
  - Hamiltonian, growth, feasibility, and transversality
  - Level changes, permanent return changes, and a tax wedge
  - Private returns versus aggregate AK with a spillover
- Human capital: explain the reproducible composite
  - Complete two-sector conditions and the work--learning choice
  - Two shadow values and an interior balanced growth path
  - Joint reproducibility versus diminishing returns to one input
- Ideas: from a research share to innovation incentives
  - Nonrivality, production rights, and a complete expanding-variety experiment
  - Input demand, markups, wages, and patent profits
  - Free entry, household pricing, and endogenous research effort
  - Planner research as a transformed AK problem
- What changes when ideas become harder to find?
  - Scale effects and the research-technology assumption
  - Conditional semi-endogenous growth, levels, and transitions
- Allocation: more output from the same stocks
  - Full conditions for a static two-firm experiment
  - Efficient capital allocation, wedges, and a numerical comparison
- How to read an endogenous-growth claim
  - Model comparison and the distinction between levels, transitions, and growth

### 8. Growth Models: Mechanisms, Comparisons, and Reality

- A map of the questions, not a ranking of the models
  - Production, saving, and ownership compared with skills, ideas, and allocation
- A region builds factories: demand, capacity, and diminishing returns
  - Investment spending versus usable capacity; marginal versus total output
- Someone must save: from an investment target to household choices
  - Transition costs, Ramsey choices, OLG ownership, pensions, and welfare
- The next machine needs a skill; the next skill needs an idea
  - Training inputs, learning productivity, adoption, innovation, and research difficulty
  - Korea as a historical connection, with the limits of a model-based interpretation
- The same resources can produce more, but who gains?
  - Allocation, adjustment costs, distribution, and the distinction between output and welfare
- A growth slowdown: work backward from observations
  - Per-person accounting, competing diagnoses, and evidence that would distinguish them
  - Capacity versus utilization; temporary deviations, level losses, and slower trend growth
- A longer view: learning to exercise economic judgment
  - Binding constraints, changing complements, and learning from investment outcomes
  - Resources, financial claims, expectations, and institutional channels
  - Transition costs, repeatable opportunities, and conditional judgments
- What we carry into fluctuations
  - Inherited stocks, changing decisions, and the boundary between trends and model benchmarks

## Part III: Fluctuations

### 9. Understanding Economic Fluctuations

- Why study growth before fluctuations?
  - Analytical benchmarks, inherited stocks, and the interaction of growth with adjustment
- What exactly are we describing as a fluctuation?
  - Levels, growth rates, reference paths, and different meanings of an output gap
  - Breadth, duration, persistence, comovement, timing, and measurement
  - Business-cycle phases without a regular clock; recession dating and recovery
- Where can fluctuations come from?
  - Production, spending, finance, policy, news, uncertainty, and reallocation
  - Innovations, anticipation, exogeneity, and the distinction between shocks and residuals
- How does a disturbance become an aggregate movement?
  - Impulse, propagation, amplification, and stabilizing mechanisms
  - A one-period innovation with persistent responses; individual plans in equilibrium
- Do fluctuations belong to the short, medium, or long run?
  - Adjustment mechanisms, financial cycles, shock duration, and recovery time
  - Lasting effects, hysteresis, and the counterfactual growth path
- Why do fluctuations matter?
  - Missed opportunities, distribution, consumption risk, and welfare
  - The same output fall under supply, spending, or financing constraints
- What must a model of fluctuations explain?
  - Joint paths, conditional shock responses, identification, and the route to RBC and NK

### 10. Real Business Cycle Model

- From a growth path to changing opportunities
  - Modeling questions, uncertain productivity, hours choice, and propagation
- Complete conditions and the order of decisions
- Household choice: working now and transferring consumption
  - Nominal bonds, capital, conditional expectations, and risk pricing
- Firms, resource clearing, and the real equilibrium
  - Input derivatives, household accounts, and the planner comparison
- Recover the course's fixed-capital benchmark
  - Work incentives, wealth effects, and the log-utility case
- Capital accumulation and the deterministic reference
- Log-linearization: show the approximation in each equation
  - Both original routes, exact log identities, weighted sums, and expected Euler conditions
- Solve the model before drawing its responses
  - Exact full-depreciation case, coefficient matching, and stable selection
- A worked shock experiment and its economic meaning
  - Reoptimized persistence comparison, investment timing, and capital memory
- Retain nominal pricing without confusing it with real closure
  - Local Fisher comparison, optional money demand, and conditional neutrality
- What should an economist learn from the benchmark?
  - Joint-path evidence, identification, efficiency, and missing mechanisms

### 11. New Keynesian Model

- UMP of household
- PMP of firm
  - Price-setting behavioral equation
  - Philips curve
  - Dynamic IS curve
- Equilibrium of model
  - DNK with money supply rule
  - DNK with interest rate rule
- Analyze exogenous shocks
- Natural rates, output gaps, and model limits — **planned**

### 12. Sticky Wage Model

### 13. Labor Markets and Unemployment — **planned**

- Employment, unemployment, and participation
- Search, matching, and wage determination
- Adjustment and persistence

## Part IV: Open Economy

### 14. International Accounts and Intertemporal Trade — **planned**

- Trade balances, current accounts, and external wealth
- Consumption smoothing and international borrowing
- Investment and external adjustment

### 15. Trade and Relative Prices — **planned**

- Comparative advantage, trade gains, and trade costs
- Terms of trade and the real exchange rate
- Tradable goods, nontradable goods, and adjustment

### 16. Open Economy Fluctuations and Exchange Rates — **planned**

- The small open economy RBC model
- Capital flows, interest parity, and risk
- Nominal rigidities and exchange-rate regimes

## Part V: Money, Finance, and Macroeconomic Policy

### 17. Money, Banking, and Central Bank Operations — **planned**

- Money, payments, and financial claims
- Banks and balance sheets
- Implementing monetary policy

### 18. Financial Frictions and Aggregate Adjustment — **planned**

- Borrowing limits and collateral
- Intermediation and financial amplification
- Financial distress and policy intervention

### 19. Household Heterogeneity and Policy Transmission — **planned**

- Income risk, insurance, and precautionary saving
- Marginal propensities to consume and redistribution
- From representative to heterogeneous households

### 20. Monetary Policy

- Transmission and policy shocks — **planned**
- Rules, commitment, and discretion — **planned**
- The interest-rate lower bound and balance-sheet policies — **planned**
- Optimal monetary policy

### 21. Fiscal Policy — **planned**

- Government budgets, debt, and Ricardian equivalence
- Taxes, purchases, transfers, and public investment
- Fiscal multipliers and financing

### 22. Policy Interaction and Constraints — **planned**

- Fiscal and monetary regimes
- Debt sustainability and policy space
- Policy combinations in an open economy

## Part VI: Topics

### 23. The Dollar in the International Monetary System — **planned**

- History and measures of international currency use
- Network effects, invoicing, and safe assets
- Benefits, obligations, and the international balance sheet
- Global funding and policy spillovers
- Persistence, alternatives, and testable changes

### 24. China's Growth and Adjustment after the Pandemic — **planned**

- The baseline, timeline, and measurement
- Demand, consumption, and employment
- Property, balance sheets, and local public finance
- Population, productivity, and resource allocation
- External demand and policy alternatives
