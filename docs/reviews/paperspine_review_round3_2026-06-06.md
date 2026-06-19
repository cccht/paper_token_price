# PaperSpine Review Round 3

**Manuscript**: `token_dynamic_pricing_game.tex`

**Review date**: 2026-06-06

**Review basis**: PaperSpine Audit, LaTeX Guard, structured review prompt
generation, manual theory/experiment/claim consistency review.

**Target**: SCI Q1-level submission readiness.

## Executive Decision

**Recommendation**: Major revision, but the paper is now much closer to a
defensible submission draft than the previous round.

The newest manuscript has addressed the most important previous weakness:
platform revenue and user experience are no longer claimed to improve
unconditionally. The paper now shows that unconstrained revenue maximization
can reduce user inclusive value, while price-protected revenue maximization
and a sufficiently provisioned direct API outside option can improve platform
revenue, inclusive value, and QoS in the tested market.

The theoretical framing is also more honest. The manuscript proves user-layer
PSNE existence through a potential game, gives a user-layer SUE fixed-point
existence result, states conditional SPE existence under compactness,
continuity, quasi-concavity, and upper-hemicontinuity assumptions, and reports
numerical outcomes as solver-based regret-bounded candidates rather than global
nonconvex Nash certificates.

The remaining SCI Q1 risk is mainly external validity. The vLLM measurements
only calibrate QoS degradation. Demand elasticity, willingness to pay,
migration cost, intermediary cost, direct API preference, contract caps, and
retention effects remain synthetic. The current paper is useful as an offline
mechanism simulator and policy screening tool. It is not yet evidence that the
pricing policy can be directly deployed in a production API marketplace.

## PaperSpine Compliance

### PS-1: Full PaperSpine workflow remains incomplete

**Severity**: Major for PaperSpine process; not a LaTeX compilation error.

`artifact_check.py` reports `FAIL` because the complete PaperSpine chain is
missing. Missing files include:

- `paper_spine_config.json`
- `paper_spine_config.md`
- `source_map.md`
- `reference_materials/source_index.md`
- `research_dossier.md`
- `exemplar_learning_dossier.md`
- `style_profile.md`
- `sota_gap_map.md`
- `motivation_options_after_research.md`
- `citation_support_bank.md`
- `confirmed_motivation.md`
- `section_blueprints.md`
- `writing_rationale_matrix.md`
- `original_logic_map.md`
- `evidence_bank.md`
- `rewrite_matrix.md`
- `logic_transfer_audit.md`
- `latex_report.md`
- `final_artifact_manifest.md`
- `final_paper/main.tex`
- `final_paper/paper.pdf`

**Interpretation**: This round should be described as a PaperSpine-style audit,
not a completed PaperSpine rewrite/build workflow.

**Required before claiming full PaperSpine completion**: run or reconstruct the
full artifact chain, especially `source_map.md`, `citation_support_bank.md`,
`writing_rationale_matrix.md`, `evidence_bank.md`, and
`logic_transfer_audit.md`.

### PS-2: Integrity audit is blocked by missing workflow artifacts

**Severity**: Major for process traceability.

`integrity_audit.py` reports 14 findings and a blocked LaTeX gate because the
PaperSpine output directory does not contain the expected upstream artifacts.
This is a workflow completeness issue. It does not mean the current manuscript
fails to compile.

### PS-3: Structured review script output is not reliable for this draft

**Severity**: Minor.

`structured_review.py` generated reviewer prompts successfully under
`review_prompts/`. Its local structured review output also wrote
`paper_rewriting_output/structured_review.md`, but the generated report contains
placeholder text and an implausible low word-count finding for a 33-page
Chinese LaTeX manuscript.

**Interpretation**: The generated prompts are useful as review dimensions, but
the structured report should not be treated as an independent peer review.

### PS-4: LaTeX guard is clean on errors

**Severity**: Minor.

`latex_guard.py` reports:

- Errors: 0
- Warnings: 31

The warnings are unescaped `&` warnings on lines 55-92. These are table
separators inside the symbol table and are false positives.

## What Was Fixed Since The Previous Review

### R2 fixed: User-protection result is no longer a single point

The previous review flagged that user-protected revenue maximization depended
on one retail cap and one wholesale cap. The new manuscript now includes a
20-point price-cap sweep:

- Retail caps: `0.80, 0.82, 0.85, 0.90, 1.00`
- Wholesale caps: `0.60, 0.70, 0.80, 0.90`
- Artifact: `artifacts/review_strengthening/20260606-182705/user_protection_sweep.csv`
- Figure: `fig:user_protection_frontier`
- Table: `tab:user_protection_sweep`

The revised conclusion is properly bounded. It states that platform revenue and
user experience can improve together only in price-protected and QoS-feasible
regions. It also reports a failure boundary where higher revenue can coincide
with active QoS collapse.

This directly supports the user's requirement: platform income can be maximized
under user-protection constraints while user experience improves, but it is not
a universal property of unconstrained revenue maximization.

### R3 fixed: Direct API outside option now has sensitivity evidence

The previous review flagged that the direct API result used fixed price and
capacity. The new manuscript now includes a 16-point direct API sensitivity
scan:

- Direct prices: `0.75, 0.82, 0.90, 1.00`
- Direct capacities: `500, 1000, 1500, 2000`
- Artifact: `artifacts/review_strengthening/20260606-182705/direct_api_sensitivity.csv`
- Figure: `fig:direct_api_sensitivity`
- Table: `tab:direct_api_sensitivity`

The paper now states the realistic conclusion: a direct API is best understood
as a capacity-protected outside option. It can improve user inclusive value and
platform revenue when capacity is sufficient, but low direct capacity creates a
new congestion point.

This makes the direct API extension much more realistic.

### R4 improved: Conclusions no longer overstate practical readiness

The discussion now positions the method as:

- an offline mechanism simulator;
- a strategy-screening tool;
- a framework requiring trace-driven replay and online validation before
  production use.

This is the right level of claim. The manuscript no longer presents the method
as a deployable automatic pricing engine.

## Theory Review

### T1: User-layer PSNE proof is acceptable

The finite user game uses a Rosenthal-style potential construction. The claim
that a finite exact potential game admits at least one pure-strategy Nash
equilibrium is standard and appropriate.

**Current status**: acceptable.

**Remaining nuance**: The finite PSNE result supports the micro-level
congestion game. It does not by itself prove that the continuous logit demand
simulation is a finite-user PSNE. The manuscript now states this distinction,
which is important.

### T2: SUE fixed-point theorem is acceptable but conditional

The SUE fixed-point result uses a continuous self-map over
`[0,1]^{J x T}` and Brouwer's theorem. The additional uniqueness and convergence
condition based on a composite Lipschitz constant is also reasonable.

**Current status**: acceptable.

**Remaining nuance**: The paper should not imply uniqueness unless the
Lipschitz condition is verified. The current text says existence is guaranteed
and uniqueness requires an extra condition, so this is fine.

### T3: Three-layer SPE theorem is formally acceptable but assumption-heavy

The SPE proposition depends on quasi-concavity of each intermediary payoff and
upper-hemicontinuity of the middle-layer equilibrium correspondence. These are
standard sufficient conditions, but they are strong for the actual nonconvex
numerical model.

The manuscript handles this correctly by saying the theorem is conditional and
the numerical solution is only a sampled, solver-based regret-bounded candidate.

**Current status**: acceptable for an applied modeling paper.

**Q1 risk**: A theory-heavy reviewer may still view the theorem as somewhat
generic unless the paper adds a short table separating:

- assumptions used only for existence theory;
- assumptions actually verified numerically;
- assumptions left as modeling regularity conditions.

### T4: Nash terminology is now mostly controlled

The manuscript correctly limits "global Nash certificate" and does not claim
that SLSQP solves the full nonconvex game globally.

**Minor wording risk**: The phrase "完整的三层博弈模型与条件性理论证明" is acceptable
in Chinese, but for a strict venue the contribution could be safer if phrased
as "三层博弈模型、条件性均衡存在证明与regret-bounded数值候选".

## Experiment Review

### E1: Current experiment set is broad enough for a strong revision

The manuscript now includes:

- five baseline strategies;
- mechanism ablations;
- profit slice diagnostics;
- finite-user PSNE vs logit comparison;
- platform candidate count sweep;
- QoS threshold sensitivity;
- demand pressure tests;
- fixed-capacity ablation;
- vLLM QoS parameterization;
- vLLM pressure tests;
- user welfare diagnostics;
- user-protected revenue maximization;
- user-protection price-cap sweep;
- direct API option experiment;
- direct API price-capacity sensitivity;
- measured-arrival replay;
- random-seed robustness;
- platform reference search.

For a simulation-and-theory paper, this is now a serious experimental package.

### E2: Experiments support the theory's value, but only within the stated scope

The experiments do show the value of the theory:

- the Stackelberg structure exposes how wholesale prices transmit incentives;
- the user logit/QoS feedback explains demand migration and congestion relief;
- solver-based regret gives a stability diagnostic for intermediary response;
- user-protection constraints and direct API outside options show how to make
  revenue objectives compatible with user experience in selected regions.

The theory is not merely decorative. It directly determines the simulation
objects, diagnostics, and intervention knobs.

### E3: Calibration uncertainty remains the main empirical weakness

The measured vLLM evidence calibrates QoS degradation only. The following inputs
are still synthetic:

- demand elasticity;
- willingness to pay;
- migration cost;
- intermediary capacity cost;
- QoS penalty cost;
- direct API preference;
- direct API capacity reservation policy;
- customer retention effect;
- contract/SLA penalty parameters.

This is the main reason the manuscript should not claim real-world deployment
validity yet.

**Recommended next experiment**: Add a calibration-uncertainty sweep that varies
`alpha`, `c_s`, `gamma`, `c_g`, `c_q`, demand scale, and direct API preference.
Report whether the user-protected and direct-API improvements survive across
the plausible parameter range.

### E4: vLLM results may look too easy

The vLLM pressure tables keep active minimum QoS near 1.0000 across several
settings. This supports the solver's congestion-avoidance behavior, but it can
also invite reviewer skepticism: if the measured QoS curve almost never binds,
the value of QoS-aware control is less visible.

**Recommended next experiment**:

- add a no-capacity-adaptation baseline under measured QoS;
- add a tighter-capacity or longer-context stress case;
- report QoS-curve fit uncertainty or confidence intervals.

### E5: Runtime reproducibility is good but environment sealing is incomplete

The repository contains scripts, artifacts, and tests. The new artifacts were
checked:

- `user_protection_sweep.csv`: 20 rows;
- `direct_api_sensitivity.csv`: 16 rows.

However, `pytest` was not available in the local environment during the previous
verification run. Python compile checks and manual test execution were used
instead.

**Recommended next step**: Add a short "CPU reproducibility" block in the
README with the exact Python version, installation command, and smoke commands.

## Claim Consistency Review

### Claims now supported by theory and experiments

- The user layer has a finite potential-game PSNE.
- The SUE-QoS feedback admits at least one fixed point under continuity.
- The three-layer game has conditional SPE existence under stated regularity
  assumptions.
- The numerical solution should be interpreted as a sampled, solver-based
  regret-bounded candidate.
- The base QoS-aware three-layer strategy improves system profit and QoS in the
  synthetic market.
- Unconstrained revenue maximization can reduce user inclusive value.
- Price-protected platform revenue maximization can improve platform revenue,
  inclusive value, and QoS in the tested market.
- A direct API outside option can improve user inclusive value when direct
  capacity is sufficient.
- Direct API capacity shortage can create new QoS failure points.
- The practical value is an offline simulation and policy-screening role, not
  direct production deployment.

### Claims that must remain bounded

- Do not claim global Nash equilibrium for the nonconvex numerical game.
- Do not claim production-ready pricing.
- Do not claim user experience always improves under platform revenue
  maximization.
- Do not claim any direct API option improves user experience.
- Do not claim vLLM calibration validates the full economic model.
- Do not claim the parameterized results generalize to all API marketplaces.

## Verdict For SCI Q1

The manuscript is now scientifically coherent and much more realistic than the
previous draft. It has a defensible theory-experiment connection and no longer
overstates the "platform revenue plus user experience" result.

For SCI Q1, I would still expect reviewers to ask for one more layer of
external-validity evidence. The most valuable addition is not another single
table. It is a measured-vs-synthetic parameter audit plus uncertainty
sensitivity.

## Highest-Impact Next Revisions

1. Add a measured/synthetic parameter table.

   The table should mark each model input as measured, calibrated, synthetic,
   or assumed. This will make the paper more honest and easier to defend.

2. Add a calibration-uncertainty sensitivity sweep.

   Vary demand elasticity, migration cost, intermediary costs, QoS penalty,
   demand scale, and direct API preference. Show where the user-protection and
   direct-API conclusions survive.

3. Add a measured-QoS stress baseline.

   Compare QoS-aware control against no capacity adaptation under measured QoS,
   ideally with a tighter-capacity or longer-context setting.

4. Create PaperSpine evidence artifacts.

   At minimum, create `source_map.md`, `evidence_bank.md`,
   `citation_support_bank.md`, and `writing_rationale_matrix.md`.

5. Tighten one contribution phrase.

   Replace "完整的三层博弈模型与条件性理论证明" with a more precise phrase such as
   "三层博弈模型、条件性均衡存在证明与regret-bounded数值候选".

## Final Editorial Judgment

The paper is no longer just a paper-only method. It has a real practical role:
offline simulation for API pricing, channel policy design, and direct API
capacity/price screening. But it is not yet a production pricing method because
key economic inputs are not calibrated from real users.

The current conclusion matches the theory and experiments. It is cautious
enough: the method can improve platform revenue and user experience together
only under explicit price/user-protection constraints and sufficient direct API
capacity. This should remain the central claim.
