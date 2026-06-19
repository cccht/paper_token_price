# PaperSpine Review Round 5

**Manuscript**: `token_dynamic_pricing_game.tex`

**Review date**: 2026-06-07

**Target**: SCI Q1 pre-submission readiness

**Review basis**: PaperSpine artifact check, integrity audit, citation support
bank check, LaTeX guard, structured-review prompt generation, and manual
theory--experiment--claim consistency review.

## Executive Decision

**Recommendation**: Minor-to-moderate revision before SCI Q1 submission.

The core method is now coherent enough for external review. The manuscript no
longer has the earlier fatal mismatch between theory and experiments: the
theory states finite-user PSNE existence, SUE fixed-point existence,
conditional SPE existence, and solver-based regret diagnostics; the numerical
experiments are reported as sampled wholesale-price and SLSQP-response
candidates, not as global Nash or global optimum certificates.

The practical positioning is also mostly correct. The paper now treats the
method as an offline mechanism simulator and strategy-screening tool. It does
not claim that vLLM measurements validate the full economic model, nor that
platform revenue maximization automatically improves user welfare. The user
protection and direct API experiments are correctly framed as constrained
regions where platform revenue and user-side inclusive value can improve
together.

For SCI Q1, the remaining risk is no longer "the paper has no theory" or "the
experiments do not match the model." The remaining risk is packaging: the paper
is long, table-heavy, and still reads partly like accumulated reviewer-response
material. A journal reviewer may accept the mechanism but ask for a cleaner
main-paper story, a tighter related-work gap, and a sharper separation between
main results and supplementary robustness checks.

## PaperSpine Process Status

| Check | Current status | Interpretation |
|---|---:|---|
| PaperSpine artifact check | PASS | Required local workflow artifacts are present. |
| Integrity audit | READY | Artifact chain, reasoning depth, evidence chain, and integrity patterns are clean. |
| Citation support bank | PASS | 60 candidate support rows; 48 recent rows. |
| LaTeX guard | 0 errors, 31 warnings | Warnings are `&` detections in longtable/symbol rows; no blocking LaTeX error. |
| Structured review dispatch | prompts generated | Independent sub-agent reviews were not run in this pass; this report is local editor synthesis. |

## Manuscript Scale Snapshot

| Item | Count |
|---|---:|
| Sections | 7 |
| Subsections | 14 |
| Subsubsections | 11 |
| Figures | 12 |
| Tables | 23 |
| `includegraphics` calls | 12 |
| Cited BibTeX keys | 34 |
| BibTeX entries | 55 |
| Missing citation keys | 0 |
| Manuscript characters | 61,750 |
| Abstract characters | 834 |

This scale is defensible for an internal draft, but it is heavy for a polished
SCI Q1 main manuscript. The likely editorial fix is not more experiments. It is
a main/supplement split and a clearer evidence hierarchy.

## Theory--Experiment Alignment

### Finding T1: Equilibrium claims now match the available theory

**Severity**: Resolved, monitor wording in English submission.

The manuscript now correctly separates four levels:

1. finite user-layer PSNE existence via Rosenthal potential;
2. logit SUE and QoS fixed-point existence;
3. conditional SPE existence under compactness, continuity, and quasi-concavity
   assumptions;
4. numerical `solver-based regret` as a candidate-equilibrium diagnostic.

This is the correct boundary. The paper should preserve this wording during
English translation. Do not compress it into "we find the Nash equilibrium" or
"global equilibrium is guaranteed."

### Finding T2: Middle-layer nonconvexity is acknowledged correctly

**Severity**: Resolved.

The manuscript states that broker profit can be nonconvex because of logit
demand, QoS feedback, and capacity constraints. It therefore reports
regret-bounded candidates rather than global Nash certificates. The profit
slice diagnostics support this statement.

### Finding T3: Direct API extension is realistic but not a full upper-level design

**Severity**: Moderate.

The direct API experiment is useful because real users can bypass an
intermediary and call the upstream API directly. The manuscript correctly
models this as an outside option and scans direct price--capacity settings.

The limitation is also clear: direct price and direct reserved capacity are
fixed or scanned, not jointly optimized in the upper-level platform problem.
For SCI Q1, keep calling it a "direct API outside-option extension." Do not
call it a full direct-channel mechanism design.

## Experimental Completeness

### Finding E1: The experiment set is now broad enough

**Severity**: Resolved.

The current experiments cover the key theoretical levers:

- wholesale price search;
- noncooperative intermediary price and capacity response;
- user migration through logit choice;
- QoS feedback and congestion;
- fixed-capacity ablation;
- demand pressure and QoS-threshold sensitivity;
- finite-user PSNE versus logit share comparison;
- user welfare and inclusive value;
- user-protected platform revenue maximization;
- direct API outside option;
- calibration-uncertainty scenario scans;
- vLLM-measured QoS substitution;
- measured-arrival replay;
- random-seed reproducibility.

This is enough to demonstrate the value of the theory as a simulation and
screening framework. Adding another small synthetic sweep would probably make
the paper harder to read without improving the core argument.

### Finding E2: Revenue and user experience are now handled honestly

**Severity**: Resolved, but protect the wording.

The paper now reports the uncomfortable but important result: unconstrained
revenue maximization can reduce inclusive value. It then shows that price
protection and direct API outside options can create constrained regions where
platform revenue, inclusive value, and QoS improve together.

This is exactly the claim that should be made:

> Under price-protection and sufficient direct-capacity constraints, platform
> revenue maximization can be compatible with better user-side inclusive value
> and QoS in the simulated market.

Do not make the stronger claim:

> Platform revenue maximization makes user experience better.

The latter is false under the manuscript's own experiments.

### Finding E3: vLLM experiments support QoS substitution, not economic validity

**Severity**: Moderate.

The vLLM measurements are useful because they show that the QoS degradation
curve can be replaced by measured backend profiles and that the mechanism still
produces low-regret candidates in controlled settings.

They do not validate user price elasticity, migration cost, willingness to pay,
intermediary cost, direct API preference, or production arrival traces. The
manuscript mostly says this. In the final version, keep the vLLM results as
system-pressure evidence, not as a production deployment proof.

### Finding E4: Calibration uncertainty is a scenario scan, not statistical inference

**Severity**: Moderate.

The 8-variant calibration uncertainty scan is valuable. It shows where
user-protection and direct API policies pass or fail. But it is not a
confidence interval, posterior uncertainty analysis, or distributionally robust
optimization result.

The current wording is acceptable because it describes the scan as
screening-style simulation. In English, use "one-at-a-time scenario
perturbations" or "calibration-stress scenarios" rather than "statistical
uncertainty quantification."

## Related Work and Novelty

### Finding R1: The gap is plausible, but some wording can still provoke reviewers

**Severity**: Moderate.

The related work now cites recent LLM serving, inference economics, pricing,
and Stackelberg-game papers. The novelty is not that nobody studies LLM pricing
or hierarchical games. The novelty is narrower:

> existing work rarely combines strategic intermediaries, cross-period capacity
> allocation, user migration, and endogenous measured-QoS feedback in one
> wholesale--retail--user response system.

This wording is safer than saying most prior pricing models ignore the whole
problem. A Q1 reviewer in pricing or operations research may push back hard if
the paper appears to dismiss nearby game-pricing literature too broadly.

### Finding R2: Citation bank is strong enough, but citation selection should stay lean

**Severity**: Minor.

The citation bank has enough recent support. The active manuscript uses 34
citation keys and has no missing keys. The final journal manuscript should not
cite all available support rows. Choose citations by function: serving systems,
dynamic pricing, congestion games, discrete choice, and recent LLM pricing.

## Structure and Presentation

### Finding S1: The main paper is over-packed

**Severity**: Major for journal packaging, not for method validity.

The paper has 12 figures and 23 tables. The results section now contains many
diagnostic and robustness experiments that are useful, but the main narrative
is getting buried.

Recommended split:

- Main paper: core model, equilibrium boundary, five-policy baseline,
  user-welfare diagnostic, user-protected policy, direct API outside option,
  one calibration-stress summary, one measured-QoS stress summary.
- Supplement: platform candidate-count sweep, full QoS-threshold sweep, full
  demand-scale sweep, all price-cap grid points, all direct price-capacity grid
  points, random seeds, artifact tables, and detailed vLLM benchmark records.

### Finding S2: Abstract is accurate but overloaded

**Severity**: Moderate.

The abstract is technically careful, including the global-Nash caveat and the
user-welfare tradeoff. The problem is density. It lists too many experiment
families. For SCI Q1, a compressed abstract should emphasize:

- three-layer wholesale--retail--user game;
- conditional theory and regret-bounded computation;
- baseline improvement in system profit and QoS;
- user-protection/direct-API result as constrained welfare-compatible revenue;
- limitation that results are simulation and measured-QoS supported, not
  production-calibrated.

### Finding S3: Conclusions are mostly aligned with evidence

**Severity**: Resolved, monitor in translation.

The conclusion now says the method is an offline simulator, not a production
pricing engine. It also states that revenue and user experience improve
together only under price protection, sufficient direct capacity, and controlled
price regions. This is consistent with the experiments.

## Scores

| Dimension | Score | Rationale |
|---|---:|---|
| Method completeness | 4.0/5 | Model, assumptions, algorithms, and regret diagnostics are now explicit. |
| Assumption justification | 4.0/5 | Synthetic economic parameters are disclosed; production calibration still absent. |
| Experimental design | 4.0/5 | Broad and aligned with model; now needs packaging rather than more sweeps. |
| Limitations acknowledgment | 4.5/5 | Strong caveats on global Nash, vLLM, calibration, and user welfare. |
| Contribution clarity | 4.0/5 | Clearer than before; related-work gap should remain precise. |
| Novelty | 3.8/5 | Strong integrated mechanism; not a wholly new theory class. |
| Evidence-to-claim strength | 4.0/5 | Claims mostly match evidence; external validity remains bounded. |
| Venue appropriateness | 3.8/5 | Potentially SCI Q1 after main/supplement split and cleaner framing. |
| Structure | 3.4/5 | Overloaded main text is the largest remaining weakness. |
| Figure/table integration | 3.5/5 | Valuable artifacts, but too many for the main manuscript. |

## Required Next Actions

1. Split main-text and supplementary experiments before submission.
2. Rewrite the related-work gap in the narrower form: intermediary strategy,
   capacity allocation, user migration, and endogenous QoS feedback jointly.
3. Shorten the abstract by grouping experiments instead of listing every sweep.
4. Keep the direct API claim as an outside-option extension, not a full
   direct-channel optimization model.
5. Add or keep a compact "Threats to validity" paragraph/table in the final
   English version, explicitly separating synthetic economics, measured QoS,
   and production deployment.
6. Preserve all conditional wording around Nash, regret, revenue-user
   compatibility, and vLLM evidence.

## Do Not Do

- Do not add more synthetic experiments unless they answer a specific reviewer
  objection.
- Do not claim a global Nash equilibrium or global optimum.
- Do not claim direct API always improves user experience.
- Do not claim platform revenue maximization automatically improves users.
- Do not claim vLLM validates the economic model.
- Do not describe calibration perturbations as formal statistical uncertainty.

## Final Judgment

The paper is now scientifically defensible as a simulation-backed mechanism
paper. Its strongest realistic value is not "automatic pricing for production."
Its value is that it gives platform operators a reproducible way to test how
wholesale prices, intermediary strategy, user migration, capacity allocation,
QoS degradation, price protection, and direct API outside options interact.

For SCI Q1, the next improvement should be editorial discipline: reduce the
main paper's experimental clutter, sharpen the novelty sentence, and keep the
claim boundaries exactly as strict as the theory and experiments allow.
