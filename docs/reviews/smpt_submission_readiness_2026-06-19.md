# SMPT Submission Readiness and Revision Plan

> **Historical readiness plan, superseded.** The 225-point evidence and June
> manuscript named below are no longer the submission basis. Use the current
> adaptation checklist and 2026-07-14 evidence map instead.

Target journal: *Simulation Modelling Practice and Theory* (SMPT)

Date: 2026-06-19

## Source Basis

- User-provided strict review log:
  `C:\Users\cccht\.codex\attachments\2dcfd4dd-9ef0-408a-a079-94508bda9e6c\pasted-text.txt`
- Official journal scope and Guide for Authors checked on 2026-06-19:
  - https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory
  - https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors
- Current manuscript:
  `peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex`

## Journal Fit Judgment

The paper fits SMPT better than AI-algorithm or economics-theory venues if it is framed as:

> a simulation-based mechanism analysis of time-of-use pricing for fixed-capacity AI inference services.

The paper should not be framed as a new dynamic-pricing theory, a production predictor, or a continuous-space equilibrium result.

## Current Recommendation From Review Log

- Current status if submitted immediately: **Weak Reject**.
- Main reason: the manuscript remains closer to a synthetic mechanism demonstration than to a fully validated and reproducible simulation-modelling study.
- Highest-risk areas:
  - insufficient verification and validation;
  - weak baselines;
  - limited structural ablations;
  - local fixed-policy stress tests rather than re-solved sensitivity;
  - local artifact paths rather than a public repository / DOI;
  - SMPT formatting gaps.

## Immediate Manuscript Adaptation Done in This Pass

- Retitle the manuscript as a simulation-based study.
- Compress the abstract toward the SMPT 250-word limit.
- Reduce keywords to at most seven.
- Rename core sections toward SMPT terminology:
  - `Model` -> `Simulation Model`;
  - `Solution Method` -> `Model Implementation and Candidate-Response Solver`;
  - `Experimental Setup` -> `Experimental Design`;
  - `Mechanism Discussion` -> `Mechanism and Profit-Boundary Discussion`.
- Add a bounded `Verification and Validation` section based only on existing evidence.
- Add a more explicit reproducibility/data-availability boundary.
- Prepare a separate highlights draft.

## Evidence-Preserving Claim Rules

Keep:

- time-of-use pricing lowers peak utilization and raises minimum QoS in the congested synthetic setting;
- the finite-grid mixed diagnostic reaches full-grid maximum regret about 0.203 on the 225-point grid;
- local fixed-policy perturbations preserve QoS gains and peak-utilization reductions;
- profit improvement is not robust across solver objects.

Avoid:

- production validation;
- continuous-space Nash equilibrium proof;
- robust profit improvement;
- calibrated user price elasticity;
- claiming that vLLM measurements validate production QoS;
- claiming that local perturbation is global uncertainty quantification.

## Required Experiments Before A Strong SMPT Submission

Status after the SMPT experiment-completion pass:

1. Strong baselines:
   - optimal static pricing;
   - off-peak discount only;
   - peak surcharge only;
   - congestion-aware routing without dynamic pricing;
   - admission control or throttling;
   - small capacity scaling.

   Status: mostly completed as diagnostics in
   `artifacts/peak_shaving/20260619_smpt/smpt_baselines.csv` and the phase grid.
   Admission control is a diagnostic admitted-fraction calculation rather than a
   full profit model.

2. Structural ablations:
   - remove outside option;
   - remove direct-provider channel;
   - remove provider heterogeneity;
   - remove intermediary routing;
   - remove time-flexible users;
   - one-provider monopoly variant.

   Status: partially completed in
   `artifacts/peak_shaving/20260619_smpt/smpt_ablations.csv`. The one-provider
   monopoly variant is not implemented because the current simulator is
   structurally two-provider.

3. Re-solved sensitivity:
   - capacity scale;
   - price sensitivity;
   - flexible-user share;
   - QoS threshold;
   - outside-option utility.

   Status: completed as a restricted local candidate re-solve in
   `artifacts/peak_shaving/20260619_smpt/smpt_resolved_sensitivity.csv`. This is
   not a full continuous-strategy or full-grid re-solve.

4. Global sensitivity / phase diagrams:
   - elasticity vs flexible share;
   - capacity tightness vs QoS curvature;
   - outside utility vs competition intensity.

   Status: partially completed as a fixed-policy capacity-scale by
   price-sensitivity phase grid in
   `artifacts/peak_shaving/20260619_smpt/smpt_phase_grid.csv`. The other two
   phase diagrams remain future work.

5. Simulation verification:
   - fixed-point residual distributions;
   - iteration counts;
   - initial-condition sensitivity;
   - non-convergence handling;
   - damping-factor audit.

   Status: fixed-point residuals and iteration counts are completed for the main
   reported policy rows in
   `artifacts/peak_shaving/20260619_smpt/smpt_fixed_point_residuals.csv`.
   Initial-condition and damping-factor audits are still not fully reported.

6. Reproducibility:
   - public GitHub / Zenodo or OSF archive;
   - DOI;
   - environment file;
   - raw artifacts and figure scripts;
   - formal Data Availability Statement.

   Status: local artifact organization and reproduction commands are improved,
   but public repository DOI / archival deposit is still not completed.

## Submission Checklist

- Abstract <= 250 words.
- Keywords: 1 to 7.
- Highlights: 3 to 5 bullets, each <= 85 characters.
- Include explicit model development, implementation, verification, validation, and data availability statements.
- Include generative AI declaration if AI-assisted writing tools were used.
- Ensure all scientific figures are script-generated or otherwise copyright-compliant.

## Current Decision

The current revision is now a stronger SMPT-targeted working draft with added
baseline, ablation, phase-grid, residual, and restricted re-solve diagnostics.
It is still not final submission-ready until the public artifact deposit is
prepared and the authors decide whether to add the remaining global sensitivity
and damping/initialization audits.
