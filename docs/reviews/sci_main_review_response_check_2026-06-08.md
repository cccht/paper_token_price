# SCI Main Review-Response Check

**Manuscript checked**: `token_dynamic_pricing_game_sci_main.tex`

**Source review**: `review_report.md`

**Date**: 2026-06-08

## Summary

The first revision pass addresses the main review report by changing the SCI
main draft from a theorem-forward SPE narrative to a mechanism-simulation
paper centered on solver-based epsilon-Nash candidate responses and the user
welfare tension.

## Checklist

| Review issue | Current status | Evidence in manuscript |
|---|---|---|
| SPE theorem overclaim under nonconvex middle-stage profit | Addressed in narrative and theory positioning | Abstract; contribution 2; `sec:three_level_game`; Definition `def:solver_eps_nash`; Remark `rem:conditional_spe_boundary` |
| Regret-bounded candidate vs global Nash ambiguity | Addressed with solver-based epsilon-Nash candidate-response definition | Definition `def:solver_eps_nash`; `sec:fixed_point`; `sec:regret_definition`; conclusion |
| 93.92% profit improvement is over-weighted against a weak baseline | Addressed by foregrounding 13.61% vs no-QoS dynamic pricing and contextualizing 93.92% | Abstract; Table `tab:three_layer_baseline`; `sec:equilibrium_results`; conclusion |
| Inclusive value drop should be a core finding | Addressed by moving welfare diagnostics next to the main profit/QoS result | Table `tab:welfare_diagnostics`; text immediately after Table `tab:three_layer_baseline` |
| Negative inclusive value needs economic interpretation | Addressed with a note that the base logit model lacks an explicit no-purchase option | Paragraph before Table `tab:welfare_diagnostics` |
| QoS=1.0000 and peak utilization near 0.82 need explanation | Addressed as threshold-seeking under a soft QoS penalty, not a hard SLSQP utilization constraint | `sec:pricing_capacity_detail`, item (3) |
| Demand function's rigid and elastic components need clearer meaning | Addressed with an explanation of elastic demand, replay/rigid demand, sigmoid retention, and calibration boundary | Paragraph after Equation `eq:demand` |
| Attribution ablation has fixed-capacity baseline bias | Addressed by marking it as diagnostic rather than strict causal decomposition | Paragraph before Table `tab:attribution_ablation` |
| No-QoS baseline fairness | Partly addressed by keeping congestion-proxy baseline and emphasizing its implication | Paragraph before Table `tab:attribution_ablation` |
| Cross-disciplinary readability | Addressed with nontechnical mechanism intuition and electric-market analogy in the introduction | `sec:introduction`, mechanism and cross-market analogy paragraphs |
| Single-platform limitation | Addressed with explicit multi-platform competition effect directions | `sec:discussion`, validity threats paragraph |
| vLLM evidence overreach | Already bounded; retained | `sec:robustness_ablation`; `sec:discussion` |
| Direct API benefit overclaim | Already bounded; retained | `sec:realism_validation`; `sec:discussion` |

## Remaining Risks Before Journal Submission

- The manuscript is still a Chinese SCI-style draft. A real SCI submission will
  need an English version and target-journal formatting.
- The new solver-based epsilon-Nash definition improves honesty, but it does
  not provide a global nonconvex equilibrium certificate.
- No new production trace, real user elasticity, or public API price-data
  calibration was added in this pass.
- The attribution table remains diagnostic. A fully fair causal decomposition
  would require new controlled optimization experiments.

