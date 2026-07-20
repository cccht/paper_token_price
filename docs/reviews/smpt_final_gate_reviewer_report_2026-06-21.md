# SMPT Final-Gate Reviewer Report

> **Historical review, superseded.** This report assesses the 2026-06-20
> manuscript and predates both the 788-candidate evidence and the current SMPT
> artwork-policy audit. Its statement that no figure-level blocker remained is
> no longer valid. Use `smpt_submission_evidence_map_2026-07-14.md`,
> `smpt_final_three_reviewer_audit_2026-07-14.md`, and
> `../submission/smpt_author_actions_2026-07-16.md` for the current gate.

Date: 2026-06-21  
Manuscript assessed: `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`  
Assessment mode: internal reviewer-style pre-submission gate  
Target: *Simulation Modelling Practice and Theory*

## Review Setup

- Input scope: full current SMPT manuscript, current PDF, submission package,
  table audit, full-figure audit, and reproducibility statements.
- Assessment boundary: this is an internal gate review. It does not replace the
  journal editor's decision and does not assume author metadata, funding,
  competing-interest, or DOI information that has not been supplied.
- Shared manuscript claim summary: the paper presents an auditable simulation
  model for time-of-use pricing in fixed-capacity LLM inference services. The
  supported claim is bounded: dynamic pricing protects QoS under congestion in
  finite-grid simulation evidence, while profit improvement is not robust.
- Visible evidence base:
  - formal user-choice, load, QoS, profit, and regret equations;
  - fixed-point verification and solver traces;
  - public price-scale anchors and controlled vLLM QoS-shape anchors;
  - congested and uncongested experiments;
  - service-management baselines, structural ablations, local parameter stress
    tests, phase grid, and restricted local re-solves;
  - full figure/table audits and artifact value checks.
- Missing materials affecting confidence:
  - production request traces;
  - real user price-elasticity calibration;
  - production-scale multi-GPU QoS curves;
  - continuous strategy-space equilibrium evidence;
  - author metadata, declarations, and frozen data/code DOI.

## Reviewer 1

- Overall assessment: The technical honesty of the manuscript is now strong for
  a simulation study. The paper no longer overstates profit improvement or
  continuous equilibrium. The main remaining scientific limitation is external
  validity, not internal presentation.
- Who would be interested in the results, and why: Readers interested in
  simulation modelling, service systems, AI infrastructure operations, and
  dynamic pricing would find the paper relevant because it joins pricing,
  routing, fixed capacity, QoS degradation, and user exit in one reproducible
  simulation workflow.
- Major strengths:
  - The model is sufficiently specified for a reader to follow the main
    computation from utility through QoS and profit.
  - The paper separates fixed-policy stress tests, restricted re-solves, and
    finite-grid mixed diagnostics instead of treating them as equivalent proof.
  - Verification and validation boundaries are explicit and fit SMPT's
    simulation-modelling expectations.
  - The figure and table audits reduce the risk of internal inconsistency.
- Major concerns:
  - The external calibration remains synthetic. Public API prices and vLLM
    single-GPU overload measurements are useful anchors but not market
    calibration.
  - The solution evidence remains finite-grid and low-dimensional. It does not
    establish a continuous-space Nash equilibrium.
  - The repository exists, but a final frozen release/DOI is still missing.
- Technical failings that need to be addressed before the case is established:
  - If the authors want to claim production validity, they need real request
    traces, production QoS curves, and user elasticity estimates.
  - If the authors want to claim equilibrium theory, they need a larger or
    continuous strategy-space analysis.
  - If the submission claims full reproducibility, the public repository must
    contain the final manuscript/artifacts and preferably a frozen DOI.
- Assessment against review axes:
  - Originality: credible as a simulation-model combination for LLM inference
    service pricing, not as a new game-theoretic theorem.
  - Scientific importance: field-relevant and timely; strongest for simulation
    modelling and AI service operations.
  - Technical soundness: internally sound for the bounded QoS claim.
  - Readability: much improved; the structure now follows a model--solver--V&V--
    results--boundary pattern.
- Recommendation posture: scientifically close to a submission candidate after
  author metadata and repository archiving are completed.

## Reviewer 2

- Overall assessment: The contribution is now narrower but more credible. The
  paper reads as a simulation-based mechanism study rather than an overbroad
  pricing claim. This is the right direction for SMPT.
- Who would be interested in the results, and why: Simulation and modelling
  readers would value the explicit model and diagnostics; AI service operations
  readers would value the QoS/profit separation.
- Major strengths:
  - The electricity pricing literature is used as a structural template without
    implying physical equivalence.
  - The Results section now has a clear evidence hierarchy: baseline, QoS
    profiles, regret checks, service-management baselines, ablations, stress
    tests, phase grid, and local re-solves.
  - The abstract satisfies the SMPT length boundary and still contains the main
    quantitative result.
- Major concerns:
  - The manuscript still depends on synthetic demand and cost parameters.
  - The local parameter checks are useful but do not fully generalize across
    market structures, more providers, multiple intermediaries, or capacity
    expansion.
  - Formal submission materials remain incomplete without author declarations.
- Technical failings that need to be addressed before the case is established:
  - The paper should not imply that the public GitHub repository is an archival
    package unless the final version is pushed and frozen.
  - The cover letter must not claim production prediction or robust profit
    uplift.
  - The Figure 1 artwork should be exported from author-reviewed Draw.io source
    before formal Elsevier submission.
- Assessment against review axes:
  - Originality: moderate to strong within the niche of inference-service market
    simulation.
  - Scientific importance: strongest for a specialized simulation and
    infrastructure audience.
  - Technical soundness: adequate for bounded claims; weak for any broader
    equilibrium or production forecasting claim.
  - Readability: now suitable for close author review.
- Recommendation posture: proceed toward submission packaging, with metadata and
  artifact archiving as the main remaining gate.

## Reviewer 3

- Overall assessment: The manuscript is readable enough for an SMPT reviewer to
  understand what was simulated, why it matters, and what is not being claimed.
  The figures now support the story rather than merely decorating it.
- Who would be interested in the results, and why: Readers outside AI pricing
  but familiar with demand response, service systems, or capacity-constrained
  simulation can follow the analogy and the QoS/profit boundary.
- Major strengths:
  - Figure 1 now matches the actual market structure and simulation workflow.
  - Figures 3--8 form a coherent evidence chain: core QoS result, regret
    boundary, mixed diagnostic, parameter stress, phase grid, and mechanism.
  - Limitations are not hidden at the end; they are integrated into V&V,
    Results, Discussion, and Limitations.
- Major concerns:
  - Figure 1 is information-dense and should be checked after any Elsevier
    template conversion.
  - Some readers may still need a clear statement that the study is simulation
    evidence, not a production deployment study.
  - The manuscript is anonymous and lacks final title-page/declaration metadata.
- Technical failings that need to be addressed before the case is established:
  - No figure-level blocking issue remains in the current PDF.
  - The final repository archive and artwork export are procedural but important
    submission requirements.
- Assessment against review axes:
  - Originality: clear enough in the introduction and related work.
  - Interdisciplinary interest: present but bounded; most attractive to service
    systems and simulation readers.
  - Technical soundness: credible for the stated finite-grid simulation claim.
  - Readability: substantially improved, with remaining burden mainly in dense
    notation and figure complexity.
- Recommendation posture: suitable for final author review before formal
  submission-system preparation.

## Cross-Review Synthesis

- Consensus strengths:
  - The manuscript now has a defensible simulation-modelling spine.
  - The main QoS conclusion is supported by several bounded checks.
  - The profit boundary is honestly presented and should not be softened into a
    positive revenue claim.
  - Figures and tables are internally consistent with the text and artifacts.
- Consensus technical risks:
  - Real calibration is still missing.
  - Continuous-space equilibrium is not established.
  - The artifact repository needs a frozen release/DOI for strong reproducibility.
  - Formal author declarations remain incomplete.
- Where emphasis differs across reviewers:
  - Reviewer 1 prioritizes technical evidence and external validity.
  - Reviewer 2 prioritizes novelty, contribution scope, and submission packaging.
  - Reviewer 3 prioritizes readability, figures, and cross-field accessibility.
- Broad-interest/significance readout:
  - The paper is best positioned as an SMPT simulation-modelling paper on
    AI-service capacity management, not as a general pricing theorem or
    production deployment report.
- Most important issues before a strong submission:
  - Push/freeze the final code and artifact package.
  - Fill author-specific declarations.
  - Export author-approved Figure 1 artwork from Draw.io.
  - Keep all claims within finite-grid simulation evidence.

## Risk / Unsupported Claims

- Not supported: production prediction.
- Not supported: continuous-space Nash equilibrium.
- Not supported: robust profit improvement.
- Supported with boundary: finite-grid QoS protection under fixed capacity.
- Supported with boundary: vLLM QoS-shape anchor as validation-style evidence.
- Supported with boundary: fixed-policy parameter stress tests as local
  sensitivity checks, not re-solved equilibrium at every parameter point.

## Direct Fix Applied After This Review

The manuscript's reproducibility statement was revised to avoid claiming that the
current local submission package is already archived in the public repository.
It now states that the repository exists, but a formal submission should cite a
frozen release or archival DOI containing the final manuscript, code, artifacts,
and figures.

## Post-Release Addendum

After the review above, a versioned GitHub release was prepared for the
submission-candidate package:

`https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`

This resolves the reviewer concern that the package existed only as a moving
repository branch. It does not create a persistent DOI. The remaining procedural
items are author-specific: author metadata, funding and competing-interest
statements, CRediT roles, acknowledgements if any, and author-approved export of
Figure 1 from the Draw.io source before formal submission.
