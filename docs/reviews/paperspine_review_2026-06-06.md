# PaperSpine Review Report

**Manuscript**: `token_dynamic_pricing_game.tex`

**Review date**: 2026-06-06

**Skill basis**: PaperSpine / PaperSpine Audit. This review uses the
PaperSpine audit logic of motivation control, evidence chain, claim boundary,
LaTeX safety, and artifact completeness. It does not run the full PaperSpine
rewrite workflow.

## Executive Decision

**Current recommendation**: Major revision before SCI Q1 submission.

The manuscript is materially stronger than a pure simulation paper: it contains
a clear three-stage game, conditional equilibrium theory, solver-based regret
diagnostics, multiple robustness checks, user welfare diagnostics, and a direct
API outside-option experiment. The main conclusion is now mostly consistent with
the theory and experiments: the method is positioned as an offline mechanism
simulator and strategy-screening tool, not a ready-to-deploy automatic pricing
system.

The remaining gap is not "more text". The gap is that several deployment-facing
claims rely on single-point parameter choices. For a SCI Q1 target, the paper
needs stronger evidence around user-protection constraints, direct API option
design, calibration uncertainty, and target-journal positioning.

## PaperSpine Compliance Findings

### PS-1: Full PaperSpine workflow artifacts are missing

**Severity**: Major for PaperSpine process; not a manuscript content error.

`paper-spine-audit` reports missing upstream artifacts:

- `paper_spine_config.json`
- `source_map.md`
- `research_dossier.md`
- `citation_support_bank.md`
- `confirmed_motivation.md`
- `section_blueprints.md`
- `writing_rationale_matrix.md`
- `evidence_bank.md`
- `logic_transfer_audit.md`

**Impact**: If the goal is to claim a complete PaperSpine rewrite/build
workflow, the current project is incomplete. If the goal is only peer review,
this is acceptable, but the report should say "PaperSpine-style audit" rather
than "complete PaperSpine workflow completed".

**Fix**: Before final submission polishing, run the full PaperSpine chain or
manually create equivalent artifacts:

- source map from manuscript claims to files/artifacts
- citation support bank for introduction, related work, and discussion claims
- writing rationale matrix explaining why each major section exists
- evidence bank linking each table/figure conclusion to CSV/JSON artifacts

### PS-2: Structured review script is unreliable for this Chinese LaTeX draft

**Severity**: Minor.

The generated `paper_rewriting_output/structured_review.md` reports a very low
word count and contains `[LLM: ...]` placeholders. This is a tool limitation for
Chinese LaTeX text extraction, not a real manuscript-length finding.

**Fix**: Do not use that generated file as reviewer evidence. Use it only as a
workflow trace.

### PS-3: LaTeX guard warnings are false positives in the nomenclature table

**Severity**: Minor.

`latex_guard.py` reports unescaped `&` warnings on lines 55-92. These are table
separators inside `longtable`, not actual LaTeX errors.

**Fix**: No manuscript change required unless the guard script is improved to
recognize tabular environments.

## Content Review Findings

### R1: The practical value claim is honest but still needs stronger calibration evidence

**Severity**: Major.

The discussion correctly says the method is an offline decision simulator rather
than a direct production pricing engine. This is good. However, the empirical
bridge still calibrates only the QoS degradation curve from controlled vLLM
measurements. Demand elasticity, willingness to pay, migration cost, direct API
preference, and intermediary cost remain synthetic.

**Evidence in manuscript**:

- `token_dynamic_pricing_game.tex:806` says vLLM measurements parameterize QoS.
- `token_dynamic_pricing_game.tex:957-959` correctly states production use
  still needs real trace and elasticity calibration.

**Risk**: Reviewers may accept the mechanism simulation but reject any strong
"real-world usefulness" framing if calibration uncertainty is not quantified.

**Fix**:

- Add a calibration-uncertainty experiment: vary `alpha`, `c_s`, `gamma`,
  `c_g`, `c_q`, demand scale, and direct API preference across plausible ranges.
- Report whether the user-protected policy and direct API option remain
  beneficial under those ranges.
- Add a table that separates "measured" inputs from "synthetic" inputs.

### R2: User-protected revenue maximization is currently a single policy point

**Severity**: Major.

The current result is useful: adding retail and wholesale caps yields higher
platform revenue than uniform pricing while improving inclusive value and QoS.
But it uses one retail cap (`0.82`) and one wholesale cap (`0.70`).

**Evidence in manuscript**:

- `token_dynamic_pricing_game.tex:869-883`

**Risk**: A reviewer can argue the result is parameter-picked. The paper should
show the tradeoff curve, not only one selected point.

**Fix**:

- Sweep retail caps, e.g. `0.80, 0.82, 0.85, 0.90, 1.00`.
- Sweep wholesale caps, e.g. `0.60, 0.70, 0.80, 0.90`.
- Plot platform revenue vs inclusive value vs active minimum QoS.
- Mark the chosen policy as one point on the Pareto frontier.

### R3: Direct API outside option needs price-capacity sensitivity

**Severity**: Major.

The direct API experiment is aligned with reality because users can choose
manufacturer/direct APIs. The result is promising: direct API share is about
25.20%, platform revenue and inclusive value both increase. But the direct
channel has fixed price and fixed capacity.

**Evidence in manuscript**:

- `token_dynamic_pricing_game.tex:889-903`

**Risk**: The paper correctly states this does not prove all direct API settings
improve experience. For SCI Q1, that caveat should be backed by a sensitivity
surface.

**Fix**:

- Sweep direct API price, e.g. `0.75, 0.82, 0.90, 1.00`.
- Sweep reserved direct capacity, e.g. `500, 1000, 1500, 2000`.
- Report direct share, platform revenue, system profit, inclusive value,
  demand-weighted QoS, and active minimum QoS.
- Identify when the direct option helps and when it cannibalizes intermediary
  welfare or reduces system profit.

### R4: vLLM calibration validates the QoS hook, not the full economic model

**Severity**: Major.

The vLLM experiments are useful as a systems sanity check, but they do not
validate price elasticity or user migration. The manuscript says this, but the
experimental tables can make the result look stronger than it is because QoS
stays near 1.0000 across the vLLM parameterized runs.

**Evidence in manuscript**:

- `token_dynamic_pricing_game.tex:806-826`
- `token_dynamic_pricing_game.tex:909-926`

**Risk**: A systems or operations reviewer may ask why measured QoS profiles do
not produce more visible degradation differences.

**Fix**:

- Add confidence intervals for fitted QoS parameters.
- Include a stress case where the measured QoS curve actually bites: tighter
  capacity, larger demand scale, or longer context.
- Report the same policy under measured QoS but without capacity adaptation, so
  the value of the QoS-aware control is visible.

### R5: Conditional SPE theory is acceptable, but the paper should make the theorem boundary even more explicit

**Severity**: Moderate.

The theory no longer overclaims global Nash optimality. The conditional SPE
existence proposition is mathematically reasonable, and the numerical work is
framed as solver-based regret-bounded candidates.

**Evidence in manuscript**:

- `token_dynamic_pricing_game.tex:356-372`
- `token_dynamic_pricing_game.tex:458-474`
- `token_dynamic_pricing_game.tex:685`

**Risk**: Some reviewers may still object that the title and contribution text
sound like the full nonconvex game is solved.

**Fix**:

- In the contribution bullet, say "conditional existence theorem and
  regret-bounded numerical candidate" instead of "complete theory" if targeting
  a strict theory journal.
- Keep "Nash equilibrium" only for the finite user potential game and the
  conditional middle-layer game under stated assumptions.

### R6: Citation support is adequate but not PaperSpine-grade for SCI Q1

**Severity**: Moderate.

The manuscript has no missing BibTeX keys. The current TeX uses 34 citation
keys, and `verified_refs.bib` contains 55 entries. However, only 18 of 55 BibTeX
entries are from 2023 or later. PaperSpine's citation-bank standard expects a
larger recent candidate pool before final motivation and introduction writing.

**Risk**: For SCI Q1, the related-work section may be judged narrow if it does
not show the most recent work on LLM inference serving, dynamic pricing, API
marketplaces, and Stackelberg resource allocation.

**Fix**:

- Build `citation_support_bank.md` with at least 60 candidate papers.
- Prioritize 2023-2026 work on LLM serving systems, inference marketplaces,
  dynamic pricing, congestion pricing, and multi-agent Stackelberg games.
- Map each introduction/related-work claim to one or more support sentences.

### R7: Reproducibility is good, but the current runtime environment is not sealed

**Severity**: Moderate.

The repository has experiment scripts, artifacts, tests, and a CPU
reproducibility bundle. This is a strength. But the local environment used for
review did not have `pytest` installed even though `requirements.txt` lists it.

**Risk**: Reviewers may not reproduce results if the environment is underspecified.

**Fix**:

- Add an environment setup section with exact Python version and installation
  command.
- Consider `requirements-lock.txt` or `pyproject.toml`.
- Add a smoke command that does not require GPU:
  `python experiments/run_reproducibility_bundle.py --smoke`.
- State clearly which vLLM experiments require GPU and which CPU experiments
  reproduce the paper tables.

## Claim Consistency Check

### Supported claims

- The three-layer QoS-aware candidate improves system profit and QoS in the
  synthetic base case.
- The numerical result is a solver-based regret-bounded candidate, not a global
  nonconvex Nash certificate.
- Unconstrained platform revenue maximization can reduce user inclusive value.
- Adding user-protection constraints can improve inclusive value in the tested
  synthetic market.
- Adding a fixed direct API outside option can improve inclusive value in the
  tested parameterization.
- The method is best described as an offline mechanism simulator unless real
  production calibration is added.

### Claims that must stay bounded

- Do not claim the method is production-ready.
- Do not claim all users are better off under the unconstrained policy.
- Do not claim the direct API option always improves welfare.
- Do not claim global Nash equilibrium for the full nonconvex numerical game.
- Do not claim vLLM measurements validate demand elasticity or market behavior.

## Priority Revision Plan

1. Add user-protection cap sensitivity and Pareto frontier.
2. Add direct API price-capacity sensitivity.
3. Add calibration uncertainty for synthetic demand and vLLM QoS parameters.
4. Build PaperSpine citation support bank and strengthen recent related work.
5. Add source map/evidence bank linking every table and claim to artifact files.
6. Add a reproducibility checklist with CPU-only and GPU-required commands.

## Final Assessment

The paper is no longer merely a paper-only method. It has a usable simulation
engine and a defensible theoretical boundary. Its realistic role is an offline
decision-support simulator for token-service pricing and capacity policy.

For SCI Q1, the main remaining work is to show that the "platform revenue can
rise while user experience improves" conclusion is robust across constraints and
outside-option settings, not just one selected configuration.
