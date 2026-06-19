# PaperSpine Review Round 4

**Manuscript**: `token_dynamic_pricing_game.tex`

**Review date**: 2026-06-06

**Review basis**: PaperSpine, PaperSpine Audit, LaTeX Guard, manual
theory-experiment-claim consistency review.

**Target**: SCI Q1-level submission readiness.

## Executive Decision

**Recommendation**: Major revision for SCI Q1, but no longer because the core
method is incoherent. The main remaining issues are evidence packaging,
calibration scope, and wording precision.

The newest draft fixes the most important previous weakness. It now contains a
parameter-source audit, calibration-uncertainty sweep, and measured-QoS
fixed-capacity stress baseline. These additions make the practical claim much
more defensible: the method is useful as an offline mechanism simulator and
strategy-screening tool, not as a production-ready automatic pricing engine.

The theory and experiments are now mostly aligned. The paper proves user-layer
PSNE existence, states a conditional SPE existence theorem, and reports
solver-based regret-bounded numerical candidates. The experiments test the
same levers that the theory introduces: wholesale price, retail response,
capacity allocation, user migration, QoS feedback, user protection constraints,
and direct API outside options.

For SCI Q1, the manuscript should still avoid one weak interpretation: the
new calibration sweep shows relative improvement against uniform retail, not
absolute production SLA satisfaction. In particular, a scenario with active
minimum QoS `0.8481` is improved relative to the uniform baseline, but it should
not be described as fully QoS-protected.

## PaperSpine Process Findings

### PS-1: Full PaperSpine artifact chain is still incomplete

**Severity**: Major for PaperSpine process; not a manuscript logic error.

`artifact_check.py` still reports `FAIL` because the project does not contain
the complete PaperSpine workflow artifacts:

- `paper_spine_config.json`
- `source_map.md`
- `reference_materials/source_index.md`
- `research_dossier.md`
- `citation_support_bank.md`
- `confirmed_motivation.md`
- `section_blueprints.md`
- `writing_rationale_matrix.md`
- `evidence_bank.md`
- `logic_transfer_audit.md`
- `latex_report.md`
- `final_artifact_manifest.md`
- `final_paper/main.tex`
- `final_paper/paper.pdf`

**Interpretation**: The current work is a PaperSpine-style audit and targeted
revision, not a complete PaperSpine rewrite/build workflow.

**Fix before final packaging**: Create at least `source_map.md`,
`evidence_bank.md`, `citation_support_bank.md`, and
`writing_rationale_matrix.md`. These are more valuable now than another small
experiment, because they link every claim to its actual artifact.

### PS-2: Integrity audit is blocked by missing workflow artifacts

**Severity**: Major for process traceability.

`integrity_audit.py` reports 14 findings and a blocked LaTeX gate. The blocker
is missing PaperSpine workflow artifacts, not a LaTeX compile failure.

### PS-3: LaTeX guard has no errors

**Severity**: Minor.

`latex_guard.py` reports:

- Errors: 0
- Warnings: 31

The warnings are `&` warnings in the symbol table and are false positives from
table separators.

## What Improved Since Round 3

### R1 fixed: Parameter-source audit now separates measured and synthetic inputs

The manuscript now explicitly states that vLLM measurements support QoS curves
and arrival-rate shape, while price sensitivity, migration cost, capacity cost,
QoS penalty, QoS feedback, and direct API preference remain synthetic or
assumed.

This is important because it prevents the paper from implying that vLLM
experiments validate the full economic model.

**Remaining nuance**: The arrival-rate input is better described as
`measurement-derived` rather than fully measured production demand. It is
constructed from controlled 8/16/32 rps measurements and resampled into the
paper's 8-period market. The current text already says it is not a production
trace, so this is acceptable.

### R2 fixed: Calibration uncertainty is now tested

The new calibration-uncertainty experiment evaluates 8 perturbation settings:

- low and high price sensitivity;
- high migration cost;
- high capacity cost;
- high QoS penalty;
- low QoS feedback;
- high demand;
- low direct API preference.

The verified CSV contains 16 rows:

- user-protected revenue policy: 6/8 variants pass the joint relative-improvement
  criterion;
- direct API user-choice policy: 5/8 variants pass the same criterion.

This materially strengthens the claim that user protection and direct API
outside options can enlarge the revenue-experience improvement region.

### R3 fixed: measured-QoS stress baseline now exposes the value of capacity adaptation

The new measured-QoS stress experiment compares fixed capacity and adaptive
capacity under vLLM-derived QoS profiles. It shows the mechanism more clearly
than the earlier vLLM tables:

- `vllm-0.5b`, demand `1.30`, capacity `0.85`:
  fixed capacity has active minimum QoS `0.9631` and system profit `11337.18`;
  adaptive capacity improves active minimum QoS to `0.999997` and system profit
  to `11839.77`.
- `vllm-3b`, demand `1.30`, capacity `1.00`:
  fixed capacity has higher system profit `11915.46`, while adaptive capacity
  has lower system profit `11819.42` but improves active minimum QoS from
  `0.9830` to `1.0000`.

This is exactly the right kind of evidence. It shows the method's value under
capacity pressure while avoiding the false claim that adaptive capacity always
raises profit.

## Remaining SCI Q1 Findings

### F1: The calibration sweep pass/fail definition needs one sentence of clarification

**Severity**: Major but easy to fix.

The code marks a scenario as improved when platform revenue gain, inclusive
value gain, and active minimum QoS gain are all non-negative relative to the
uniform-retail baseline. That is a relative-improvement criterion.

This creates a subtle wording risk. In the high-demand user-protected scenario,
active minimum QoS is `0.8481`. That is better than the corresponding uniform
baseline, but it is not a fully protected QoS state.

**Risk**: A reviewer may read "三项改善" as "QoS reaches acceptable SLA level".

**Fix**: Add one sentence near the calibration-uncertainty table:

> 这里的三项改善指相对统一零售基线同时改善平台收入、inclusive value和活跃最低QoS；它不是绝对SLA达标判据，因此高需求场景下的0.8481仍应解释为部分退化但优于基线。

### F2: The phrase "完整的三层博弈模型与条件性理论证明" still sounds slightly strong

**Severity**: Moderate.

The contribution section still says "完整的三层博弈模型与条件性理论证明".
The content itself is careful, but this phrase may invite theory reviewers to
expect stronger global claims.

**Fix**: Replace it with:

> 三层博弈模型、条件性均衡存在证明与regret-bounded数值候选

This better matches the theorem and numerical evidence.

### F3: Calibration uncertainty is still a scenario sweep, not statistical uncertainty

**Severity**: Moderate.

The new experiment is valuable, but it is not a confidence interval, posterior
uncertainty analysis, or production-calibrated parameter distribution. It is a
screening sweep over selected perturbations.

**Current manuscript status**: Mostly safe. The text uses "筛查型仿真" and says
real production use needs trace-driven replay and online experiments.

**Recommended refinement**: Keep the term "校准不确定性扫描", but avoid wording
that implies formal uncertainty quantification. If possible, add "one-at-a-time
scenario perturbation" in the English version.

### F4: Evidence packaging is now weaker than the actual evidence

**Severity**: Moderate.

The experiments are now broad, but the evidence is scattered across many CSV,
JSON, and figure directories. A reviewer or editor will not easily know which
artifact supports which claim.

**Fix**: Create an evidence map with columns:

| Claim | Manuscript location | Figure/Table | Source CSV/JSON | Script | Caveat |
|---|---|---|---|---|---|

Minimum rows should cover:

- base five-policy comparison;
- capacity ablation;
- user welfare diagnostic;
- user-protection price-cap sweep;
- direct API price-capacity sweep;
- parameter-source audit;
- calibration-uncertainty scan;
- measured-QoS stress baseline;
- measured-arrival replay.

### F5: Recent literature support is adequate, not yet strong

**Severity**: Moderate.

The bibliography contains 55 entries and the manuscript cites 34 keys. There
are no missing citation keys. However, only 18 entries are from 2023 or later,
and only 13 are from 2024 or later.

For SCI Q1, the introduction and related work should be checked against recent
2024--2026 work on:

- LLM inference serving and scheduling;
- inference marketplaces and API routing;
- dynamic pricing for cloud or AI services;
- Stackelberg resource allocation with congestion or QoS;
- user welfare constraints in platform pricing.

**Fix**: Build `citation_support_bank.md` with at least 60 candidate papers
before final English submission. Do not add citations only by keyword; map each
new reference to a specific claim.

## Theory Review

### T1: User-layer theory is coherent

The finite user game and Rosenthal-style potential proof are appropriate. The
manuscript correctly states that the finite PSNE result gives a micro-level
foundation and does not mean the continuous logit simulation enumerates user
PSNE.

### T2: SUE fixed-point result is acceptable

The Brouwer existence proof is standard. The uniqueness condition is stated as
an additional Lipschitz condition, not as an unconditional result. This is
properly bounded.

### T3: SPE theorem is conditional and should stay that way

The SPE theorem relies on quasi-concavity and upper-hemicontinuity assumptions.
The manuscript now admits that the numerical model can be nonconvex and uses
solver-based regret. This is acceptable for an applied modeling paper.

**Optional improvement**: Add a small table separating:

- assumptions used for theory;
- assumptions checked numerically;
- assumptions left as regularity conditions.

This would make the theory more transparent to reviewers.

## Experiment Review

### E1: Experimental coverage is now broad enough

The current package includes base comparisons, ablations, finite-user bridge,
profit slices, platform candidate sweeps, QoS threshold sensitivity, demand
stress, vLLM QoS calibration, welfare diagnostics, user-protection sweeps,
direct API sweeps, calibration uncertainty, measured-QoS stress, measured
arrival replay, random seeds, and reference platform search.

This is enough for a serious simulation-and-theory submission.

### E2: The experiments now prove the theory's value within the stated scope

The theory is not decorative. It defines the intervention levers and the
diagnostics:

- Stackelberg hierarchy explains platform-to-intermediary price transmission;
- intermediary Nash response motivates solver-based regret;
- user logit/QoS fixed point explains demand migration and congestion relief;
- direct API extension changes the user action set and tests outside-option
  effects;
- user-protection constraints expose the revenue-experience tradeoff.

### E3: The paper still does not prove production deployment readiness

This is not a flaw if the paper says it clearly. The newest discussion does say
it clearly. Do not weaken that caveat.

The correct claim is:

> The method is useful for offline policy screening and mechanism analysis.

The incorrect claim would be:

> The method is ready for direct production pricing.

## Claim Consistency Checklist

Supported by current theory and experiments:

- user-layer PSNE existence;
- user-layer SUE fixed-point existence;
- conditional SPE existence under regularity assumptions;
- solver-based regret-bounded numerical candidates;
- QoS-aware three-stage pricing improves system profit and QoS in the tested
  synthetic market;
- unconstrained platform revenue maximization can reduce user inclusive value;
- price-protected revenue maximization can improve platform revenue and user
  experience in selected regions;
- direct API outside option can improve inclusive value when capacity is
  sufficient;
- direct API capacity shortage or high demand can create new QoS failure
  points;
- measured QoS profiles validate the QoS hook, not the full economic model.

Must remain bounded:

- no global Nash certificate for the nonconvex numerical game;
- no production-ready pricing claim;
- no statement that platform revenue maximization always improves user
  experience;
- no statement that any direct API option improves user experience;
- no claim that calibration uncertainty is statistically quantified from real
  users.

## Priority Revision List

1. Add one clarification sentence that the 6/8 and 5/8 pass counts are based on
   relative improvement against uniform retail, not absolute SLA satisfaction.
2. Tighten the contribution phrase from "完整的三层博弈模型与条件性理论证明" to a
   more precise conditional-theory/regret-candidate phrase.
3. Create an evidence map linking every main claim to script, CSV/JSON, figure,
   and caveat.
4. Build a PaperSpine citation support bank for recent 2024--2026 literature.
5. Prepare an English SCI-target version after the evidence map is stable.

## Final Editorial Judgment

The paper now has a coherent scientific story:

1. The three-stage game is theoretically motivated.
2. The numerical solver is correctly bounded as a candidate-equilibrium solver.
3. The experiments show why price, capacity, QoS, user choice, and direct API
   options must be modeled together.
4. The practical claim is realistic: offline policy screening before
   production calibration.

The current manuscript is much stronger than a paper-only method. It still
needs evidence packaging and careful wording before SCI Q1 submission, but the
core direction is now defensible.
