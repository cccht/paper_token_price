# Artifact Manifest

## Status

This manifest describes the July 2026 SMPT submission line. It is an internal-review
manifest, not a frozen archive. As of 2026-07-19, all eight local sensitivity
perturbations have passed the augmented common-candidate gates. The dependent audit
rebuild remains pending.

The formal baseline is
`artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_equilibrium_submission.json`
(SHA-256 `70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`).
Its numerical outputs remain the baseline for current scenario gates. The live worktree
now includes solver robustness patches used by resumed sensitivity artifacts, so the
baseline artifact's recorded source hashes no longer pass the current combined
provenance gate until the baseline-dependent audit rebuild is reconciled. The former
SHA-256 `d3717445...aae2f` is retained only as the continuation seed for the
uniform-candidate expansion.

## Manuscript Sources

- `peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex`: five-section English review manuscript.
- `docs/submission/simpat_highlights_final_2026-07-16.txt`: five journal highlights.
- `verified_refs.bib`: bibliography used by the manuscript.
- `docs/reviews/smpt_submission_evidence_map_2026-07-14.md`: claim-to-artifact map and evidence limits.
- `docs/submission/smpt_author_actions_2026-07-16.md`: author-only items required before upload.

## External Input Anchors

- `data/processed/burstgpt_d895a53b_8period/`: eight-period load shape derived from 59 complete BurstGPT days.
- `artifacts/peak_shaving/20260712_final/qos_calibration.json`: pooled vLLM QoS-shape fit and measurement provenance.

These inputs anchor only the mean intraday load shape and the reduced-form QoS shape.
They do not calibrate market demand, price response, capacity, or cost parameters.
The combined evidence report validates the load-profile SHA recorded by the baseline,
the pinned BurstGPT commit and raw-file checksum declaration, 1,429,737 processed rows,
59 complete days, eight normalized periods, the QoS artifact's four source hashes,
ten measurement points with five repeats, fit quality, and the two QoS parameters used
by the baseline.

## Numerical Model

- `pricing_sim/spatiotemporal_game.py`: conserved origin--destination demand, routing, QoS, and accounting.
- `pricing_sim/spatiotemporal_mechanism.py`: response switches and outcome summaries.
- `pricing_sim/intermediary_response.py`: bounded three-parameter intermediary optimization.
- `pricing_sim/finite_game.py`: restricted-game construction and full-candidate deviation scans.
- `pricing_sim/complementarity_solver.py`: Fischer--Burmeister mixed-equilibrium solver.
- `experiments/run_final_spatiotemporal_equilibrium.py`: baseline finite-game solve.
- `experiments/run_submission_spatiotemporal_sensitivity.py`: eight common-candidate local re-solves.
- `experiments/submission_evidence_gates.py`: provenance and numerical submission gates.

## Formal Evidence

All paths below are under `artifacts/peak_shaving/20260712_expanded_response/`.

- `candidate_manifest_submission.json`: source-hashed, gate-checked reconstruction of the exact 1,576-rule provider candidate set and its complete 800-rule zero-slope subset.
- `spatiotemporal_equilibrium_submission.json`: uniform restriction and time-varying finite-game outcomes; the combined evidence report validates its 20 source hashes, baseline scenario, exact 1,576-vector candidate grid, 800/1,576 game sizes, full-candidate regret, joint residuals, demand conservation, profit and comparison arithmetic, eight-period profile dimensions, and the probability masses of 100/676 active profiles.
- `uniform_offgrid_sensitivity_submission.json`: nine-scenario bounded off-grid search over the two-dimensional zero-slope domain; scheduled for the post-sensitivity rebuild.
- `spatiotemporal_offgrid_diagnostic_submission.json`: baseline four-dimensional bounded provider off-grid search; scheduled for provenance rebuild.
- `equilibrium_branch_audit_submission.json`: 66-start restricted-equilibrium branch audit; scheduled for provenance rebuild.
- `fixed_point_multistart_audit_submission.json`: active-profile fixed-point initialization audit; scheduled for provenance rebuild.
- `intermediary_globality_audit_submission.json`: active-profile differential-evolution audit; scheduled for provenance rebuild.
- `intermediary_payoff_sensitivity_submission.json`: active-profile provider-payoff sensitivity to the independently optimized intermediary responses; generated after the intermediary audit.
- `mixed_outcome_distribution_submission.json`: source-hashed active-profile discrete weighted quantiles; scheduled for provenance rebuild.
- `mechanism_decomposition_submission.json`: fixed-policy temporal/spatial decomposition; scheduled for provenance rebuild.
- `price_shape_decomposition_submission.json`: source-hashed fixed-profile intraday price-shape decomposition; scheduled for provenance rebuild, after which the combined evidence report checks profile counts, probability mass, convergence, residuals, and four accounting identities.
- `sensitivity_*_submission.json`: one file per completed perturbation; each scenario gate checks the common strategy contract, source hashes, 800/1,576 game sizes, regret, residuals, demand conservation, profit and comparison arithmetic, eight-period profile dimensions, and the active-profile mass implied by its own positive supports.
- `spatiotemporal_sensitivity_submission.json`: nine-row sensitivity summary generated after all scenario gates passed; current SHA-256 is `7bfbd0d471a73ffe23b50034c463b536c9ea0e601a86e7c6f59f8d8bbaa41626`.
- `sensitivity_claims_submission.json`: ranges, directions, and profit-sign counts bound to the summary SHA-256; current SHA-256 is `9d9bf3fd7d1b9689b82888fc365ce5f61f7d9e2b1882b6000cafe5b3fe15a558`.
- `submission_evidence_gate_report.json`: combined provenance and numerical gate report.

Other JSON and log files in this directory record earlier candidate expansions,
interrupted runs, and diagnostics. They are research history, not manuscript claim sources.

## Figures

`figures/peak_shaving_final_20260714/` contains PDF and PNG review figures generated
from provenance-linked artifacts. `resolved_sensitivity.pdf` is created only after all
nine rows pass. The current figures are internal content blueprints. They are not
upload-ready because the target journal's artwork policy requires the authors to rebuild
and verify them without generative or AI-assisted image tools.

## Tests

The submission path is covered by `tests/test_submission_*.py`,
`tests/test_final_submission_figures.py`, and
`tests/test_final_manuscript_20260714.py`. The final manuscript tests intentionally keep
two red gates until the sensitivity table and Figure 6 are integrated.

## Evidence Boundaries

The listed artifacts do not establish:

- production demand or QoS forecasts;
- real inference-user price elasticity;
- multi-GPU or production-cluster validation;
- a continuous-provider-strategy Nash equilibrium;
- a globally optimal intermediary response;
- robust profit improvement, social welfare improvement, or global uncertainty coverage.
