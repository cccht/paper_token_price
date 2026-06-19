# SMPT Experiment Completion Design

## Goal

Strengthen the peak-shaving paper for *Simulation Modelling Practice and Theory* by adding auditable simulation evidence that addresses the review log's main weaknesses: weak baselines, missing V&V diagnostics, structural ablations, re-solved sensitivity, and phase diagrams.

## Scope

This pass creates a new SMPT experiment bundle. It does not overwrite the existing `20260618`, `20260619`, or `20260619_submission` artifacts.

Outputs:

- `artifacts/peak_shaving/20260619_smpt/`
- `figures/peak_shaving_smpt/`
- manuscript table/figure references in the English SMPT draft
- README experiment log updates

## Evidence Rules

- Treat strong baselines and ablations as simulation diagnostics unless they run the same candidate-response solver.
- Label budgeted re-solved sensitivity as budgeted candidate response, not equilibrium proof.
- Keep vLLM measurements as QoS-shape anchors only.
- Do not claim production validation, continuous-space Nash equilibrium, or robust profit improvement.

## Experiment Blocks

1. Strong baselines:
   - optimal static pricing, using the existing congested uniform candidate-response artifact;
   - off-peak discount only;
   - peak surcharge only;
   - static pricing with QoS-aware routing;
   - admission-control diagnostic;
   - static pricing under capacity scaling.

2. Structural ablations:
   - remove outside option;
   - suppress direct-provider channel;
   - remove provider heterogeneity;
   - suppress time-flexible users;
   - fixed equal routing as a no-routing diagnostic.

3. Re-solved sensitivity:
   - budgeted fictitious-play re-solve for selected perturbations covering capacity, price sensitivity, flexible-user share, QoS threshold, and outside-option utility.

4. Verification and validation:
   - fixed-point residual traces for reported policies;
   - convergence iterations and final residuals;
   - local phase diagrams for QoS gain and profit gain.

## Files

- Create `experiments/peak_shaving_smpt_tools.py`.
- Create `experiments/run_peak_shaving_smpt_experiments.py`.
- Create `tests/test_peak_shaving_smpt_experiments.py`.
- Modify `peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex`.
- Modify `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex`.
- Modify `README.md`.

## Verification

- Unit tests for baseline/ablation helper logic.
- Run the SMPT experiment script under WSL.
- Confirm generated JSON/CSV/PDF artifacts exist.
- Compile main and supplement PDFs.
- Check logs for LaTeX errors, undefined references/citations, and overfull boxes.
