# SCI Readiness Audit for the Peak-Shaving Manuscript

> **Historical review, superseded.** This report evaluates the 225-candidate
> June draft. Its results and readiness judgment must not be applied to the
> current 788-candidate conserved-demand manuscript.

Date: 2026-06-19 20:57 CST

Scope: `peak_shaving_dynamic_pricing_2026-06-19.tex`,
`peak_shaving_dynamic_pricing_supplement_2026-06-19.tex`, README experiment log,
and the existing artifacts under `artifacts/peak_shaving/`.

Skills used: `nature-reviewer`, `nature-polishing`, and `humanizer`.
`ara-rigor-reviewer` was not used because its local skill path was missing in this
environment.

## Shared Manuscript Fact Base

The paper studies whether time-of-use dynamic pricing can shift time-flexible
inference demand away from congested periods when GPU serving capacity is fixed.
The model uses two heterogeneous inference providers, one API intermediary,
time-rigid and time-flexible users, direct-provider API options, and an outside
option. Provider pricing is restricted to a low-dimensional time-shape family and
is solved with fictitious play and finite-grid diagnostics.

The evidence supports a bounded claim: in the congested synthetic setting, dynamic
time-of-use pricing reduces peak utilization and improves the minimum QoS. The
evidence does not support a robust profit-improvement claim, a production
prediction, or a continuous-strategy equilibrium theorem.

## Claim-Evidence Map

| Claim in the English draft | Evidence source | Supported wording | Boundary |
|---|---|---|---|
| Time-of-use pricing can improve QoS under fixed GPU capacity in the congested setting. | `peak_shaving_congested_fp.json`, `peak_shaving_fp_dynamic_converged.json`, `peak_shaving_fp_dynamic_converged_fine.json`, `peak_shaving_mixed_oracle.json` | Supported as a synthetic finite-grid simulation result. | Do not generalize to production traces or continuous strategy spaces. |
| Uniform pricing creates congestion in the tightened-capacity setting. | `peak_shaving_congested_fp.json`: peak utilization `0.782`, minimum QoS `0.756` | Supported. | This is a designed congested stress setting. |
| Coarse and fine dynamic snapshots reduce peak utilization and improve minimum QoS. | Coarse: peak utilization `0.706`, minimum QoS `0.968`; fine snapshot: peak utilization `0.666`, minimum QoS `0.990` | Supported as snapshot evidence. | Fine-grid pure snapshot has high regret and is not a pure-strategy equilibrium certificate. |
| The double-oracle finite-grid mixed diagnostic reaches low exploitability. | `peak_shaving_mixed_oracle.json`: full-grid max regret `0.2025` (rounded to `0.203`), expected peak utilization `0.703`, minimum QoS `0.970` | Supported on the 225-point finite grid. | Not a continuous-space Nash equilibrium proof. |
| Local perturbations preserve the QoS direction. | `peak_shaving_parameter_sweep_summary.json`: QoS gain positive in `9/9`; peak-utilization reduction positive in `9/9` for both dynamic snapshots | Supported as fixed-policy stress evidence. | The sweep does not recompute equilibrium at each parameter point. |
| Profit improvement is not robust. | Coarse `+9.3%`, fine snapshot `-1.9%`, mixed profile about `-2.8%`; fine stress sweep positive in only `1/9` scenarios | Supported. | The paper should not claim dynamic pricing raises profit. |
| Public API prices anchor the price scale. | `public_api_price_anchor.json`; cited public pricing pages | Supported only as a scale check. | Not demand elasticity calibration. |
| vLLM measurements anchor the QoS curve shape. | `vllm_qos_anchor_summary.json`, `vllm_qos_anchor_points.csv` | Supported as controlled single-GPU threshold-shape evidence. | Not a production SLA curve; not multi-GPU, long-context, or user behavior calibration. |

## Reviewer-Style Assessment

### Reviewer 1: Technical soundness emphasis

Overall assessment: The technical honesty is now substantially better than in an
early working draft. The strongest part is that the manuscript no longer hides
the high-regret fine-grid pure snapshot and uses a finite-grid mixed diagnostic
to support the QoS direction.

Major strengths:

- The QoS result is supported by several independent checks: coarse snapshot, fine
  snapshot, mixed finite-grid profile, parameter stress tests, and a controlled
  vLLM QoS-shape anchor.
- The profit result is reported conservatively, with sign changes across solver
  objects.
- Artifact provenance is strong enough for a reviewer to trace most numbers.

Major concerns:

- The mixed diagnostic is still limited to a 225-point candidate grid.
- The parameter sweep is a fixed-policy test, not a new equilibrium solve.
- The vLLM measurement anchor has a narrow hardware and workload scope.

Recommendation posture: technically plausible for a cautious simulation paper,
but not for a paper claiming a general equilibrium or production policy result.

### Reviewer 2: Originality and significance emphasis

Overall assessment: The contribution is credible but narrow. The paper is most
convincing when framed as a fixed-capacity inference-market simulation with a
QoS/profit trade-off, not as a broad pricing theory paper.

Major strengths:

- The problem framing is timely: fixed GPU capacity, daily demand shape, API
  intermediaries, and QoS degradation are realistic ingredients.
- The negative profit result is useful because it prevents the work from becoming
  a one-sided dynamic-pricing promotion.
- The paper is clearer when the main contribution is a bounded mechanism
  diagnosis rather than a general theorem.

Major concerns:

- The model remains synthetic and the demand-side parameters are not calibrated
  from real users.
- The literature positioning should stay modest and specific.
- Without a target journal, the broad-interest claim should remain restrained.

Recommendation posture: suitable for a field-facing SCI submission after English
polish and claim control; unlikely to satisfy very broad significance standards
without stronger real-data calibration.

### Reviewer 3: Readability and non-specialist access emphasis

Overall assessment: The manuscript has become readable, but it still risks
sounding machine-polished because the current Chinese draft repeats terms such
as "diagnostic", "boundary", "robust", and "therefore" too often. The English
middle draft should vary rhythm and avoid defensive phrasing in every paragraph.

Major strengths:

- The story is now easier to follow: fixed capacity, congestion, time-of-use
  prices, QoS improvement, and profit boundary.
- The figures support the core narrative.
- The limitations are visible rather than hidden.

Major concerns:

- Some terms need natural English equivalents, especially provider, API
  intermediary, fixed GPU serving capacity, time-flexible demand, and surplus
  reallocation.
- The abstract should not pack too many caveats into one paragraph.
- Results and Discussion should be kept separate: observed quantities in Results,
  interpretation and rival explanations in Discussion.

Recommendation posture: acceptable for human review once the English draft is
written in a less templated style.

## Cross-Review Synthesis

Consensus strengths:

- The QoS-improvement claim is now materially supported.
- The manuscript is honest about the lack of robust profit gain.
- The artifact trail is strong enough for a reproducibility-oriented reviewer.

Consensus technical risks:

- Synthetic economic calibration remains the main limitation.
- The finite-grid mixed diagnostic should not be oversold.
- The vLLM anchor only supports the shape of the QoS degradation proxy.

Most important issues to resolve in the English middle draft:

1. Use bounded claim language throughout the abstract, contributions, Results,
   Discussion, and Conclusion.
2. Replace AI-like repetitive transition words and rigid paragraph templates.
3. Keep "profit boundary" as a finding, not as an embarrassment.
4. State all calibration limits once clearly, then refer back rather than
   repeating defensive caveats in every paragraph.

## Unsupported Or Not-Assessable Claims To Avoid

- Dynamic pricing robustly increases profit.
- The mixed strategy is a continuous-space Nash equilibrium.
- The vLLM scan calibrates a production SLA curve.
- Public API prices calibrate user elasticity.
- The method is ready for deployment without production traces or online tests.
- The result generalizes to many providers, many intermediaries, long-term
  contracts, or dynamically adjustable capacity.
