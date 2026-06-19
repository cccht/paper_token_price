# opencode-go DeepSeek v4 Pro Review: Reference-Aligned Figure Revision

Date: 2026-06-10

Target file: `token_dynamic_pricing_game_sci_main.tex`

Reviewer model: `opencode-go/deepseek-v4-pro`

Scope: review the revised SCI main draft after expanding the manuscript to 20
figure environments in response to the reference paper's figure structure.

## Main Findings

### Critical / High Risk

1. The abstract and conclusion cite a two-layer Stackelberg baseline of
   `4519 -> 9525 (+111%)`, but the SCI main text did not define or tabulate the
   `4519` baseline. The value is present in
   `artifacts/two_layer_comparison/cross_layer_summary.csv` as
   `two_layer_centralized`, so the manuscript needs explicit provenance.

2. Several figures were referenced through timestamped artifact paths. The
   reviewer flagged this as a portability risk for journal submission, even
   though local compilation succeeds.

3. The abstract presents platform revenue gain and inclusive-value improvement
   side by side. The inclusive-value gain is small in absolute terms, so the
   wording should make the user-experience improvement conditional and modest.

4. The section title `审稿回应实验` exposes revision history and should be
   changed to a neutral final-manuscript title.

### Major / Moderate Issues

1. The two-layer Stackelberg baseline should be defined as platform-to-user,
   no-intermediary optimization, with objective, solver, and metrics reported.

2. The direct-API extension should give the expanded logit share and demand
   equations, not only describe them in prose.

3. Solver-based regret should be reported as a numerical stability diagnostic,
   ideally with a relative scale against intermediary profit.

4. The profit-slice and finite-user bridge figures are useful, but claims based
   on them should remain local and diagnostic.

5. The direct-API sensitivity figure caption should mention the scanned price
   and capacity ranges.

### Reviewer Judgment

The reviewer did not recommend moving directly to English polishing before
fixing the baseline provenance, portability, and wording issues above.

## Executor Notes

- The reported `hyperref` issue in the opencode output was a false positive:
  the source already contains `\usepackage{hyperref}`.
- Local verification before this review showed 20 figure environments, 20
  existing `includegraphics` targets, no LaTeX guard errors, and a successful
  XeLaTeX/BibTeX build.

## Follow-up Fixes Applied

- Added an explicit two-layer centralized optimization baseline table to the
  SCI main draft, sourcing the `4519.28` value from
  `artifacts/two_layer_comparison/cross_layer_summary.csv`.
- Revised the abstract and conclusion from `+111%` to `+110.8%`, and clarified
  that the comparison is against a two-layer centralized optimization baseline.
- Reworded the user-protection claim as a price-freezing protection result with
  a modest inclusive-value gain.
- Copied manuscript figures from timestamped artifact directories into
  `figures/reference_aligned/` and updated the manuscript figure paths.
- Added direct-API utility, share, and demand equations.
- Renamed the revision-history section title to a neutral final-manuscript
  title.
- Added a relative-scale explanation for solver-based regret.
