# Mathematical derivations: restoration and granularity

The standard is concise prose and fully visible mathematics. A correct final
formula or a named theorem is not a substitute for the intermediate operations.
This audit is distinct from `CONDITION_AUDIT.md`: a complete specification does
not imply that the original derivation paths have been preserved.

Comparison sources:

- Solow: `862ae0e^:macro/chapters/solow.tex`.
- Ramsey: `ca1b9ac^:macro/chapters/ramsey.tex`.
- OLG: `c861908^:macro/chapters/olg.tex`.
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

## Remaining stages in this restoration

Solow, OLG, and the new endogenous-growth derivations are being expanded next.
Compilation and mathematical/layout verification are recorded after the stages
have actually passed; the table above describes the routes written in source.
