# Artifact Manifest

## Manuscript Sources

- `peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex`: SMPT-targeted main paper.
- `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex`: Supplement.
- `verified_refs.bib`: Bibliography used by the manuscript.

## Simulation Code

- `pricing_sim/peak_shaving_config.py`: Simulation parameters.
- `pricing_sim/peak_shaving_market.py`: User choice, demand, QoS, profit.
- `pricing_sim/peak_shaving_equilibrium.py`: Intermediary response and provider candidate search.
- `experiments/peak_shaving_smpt_tools.py`: SMPT diagnostic helpers.
- `experiments/run_peak_shaving_smpt_experiments.py`: SMPT experiment bundle.
- `experiments/run_peak_shaving_smpt_vv_audit.py`: Damping and initialization V&V audit.

## Main Artifacts

- `artifacts/peak_shaving/20260618/`: Congested and uncongested baseline artifacts.
- `artifacts/peak_shaving/20260619/`: Mechanism diagnostics.
- `artifacts/peak_shaving/20260619_submission/`: Mixed-oracle, parameter sweep, price and QoS anchors.
- `artifacts/peak_shaving/20260619_smpt/`: SMPT baseline, ablation, phase-grid, residual, and restricted re-solve diagnostics.

## Figures

- `figures/peak_shaving_diagnostics/`: Mechanism and profile figures.
- `figures/peak_shaving_submission/`: Submission-strengthening figures.
- `figures/peak_shaving_smpt/`: SMPT baseline and phase-grid figures.

## Tests

- `tests/test_peak_shaving_smpt_experiments.py`: Regression tests for SMPT diagnostics.

## Non-Claims

The artifacts do not provide:

- real user price-elasticity calibration;
- production inference traces;
- multi-GPU production QoS validation;
- continuous-space equilibrium proof;
- full global uncertainty quantification.
