# New user-game figure contract

Backend: existing Python/matplotlib workflow. New outputs only; no legacy figure or result overwritten.

1. Same-price before/after: demonstrate the measured reduction in cost and peak after individual best responses, with the same final price mixture on both sides. Load panel leads; cost decomposition and absolute utility/bill/regret panels support it. Original schedule is not Nash. Expected peaks and maxima of expected loads are different estimands.
2. Fair tariff comparison: both regimes contain user and manufacturer equilibria. Mean user utility falls under TOU in all five predeclared cohorts. Show bills, manufacturer profit, all 240 expected utility changes, and five paired cohort differences. Retain harms rather than selecting only winners.
3. Individual choices: retain the predeclared first flexible user, and add the smallest-ID actual time switcher as an explicitly post-hoc mechanism example without filtering on gains. Curves include the deviating user's own load at the destination. No invented gain curve.
4. Convergence: representative highest-probability price pair. Plot potential, regret, and unsmoothed average utility. Potential convergence does not imply monotone average utility.
5. Provider load and quality: same-price before/after per-resource outcomes, fixed scales across manufacturers, reference rather than hard capacity.
6. Framework: application icons at left, feasible time choice and an actual individual utility curve in the center, two competing manufacturers at right. An intermediary is not an evaluated player in this model.

Quantitative figures are 7.15 inches wide, vector PDF/SVG with editable text plus 400 dpi PNG. No error bars for exact mixed-strategy expectations. Five seeds are synthetic instances, not a real-market confidence interval. All plotted data come from the complete predeclared experiment, with input and script hashes in manifests; no results are tuned after inspection.
