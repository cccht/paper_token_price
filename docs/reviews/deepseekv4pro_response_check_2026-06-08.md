# DeepSeek v4 Response Check

**Date**: 2026-06-08

**Reviewer input**: `docs/reviews/deepseekv4pro_opencodego_review_2026-06-08.md`

**Revised manuscript**: `token_dynamic_pricing_game_sci_main.tex`

## Response Summary

| Review issue | Response in manuscript | Status |
|---|---|---|
| Platform layer looked like weak random search in 8D space | Reframed platform layer as candidate-set revenue ranking rather than continuous Stackelberg leader optimum; added explicit nonconvex upper-level limitation and future optimization directions. | Addressed by claim tightening |
| 93.92% still visually dominated the results | Removed the absolute weak-baseline gain from the abstract, kept 13.61% as the primary QoS-aware increment, and removed bold emphasis from 93.92% in the main table. | Addressed |
| QoS mechanism may behave like a hard utilization threshold | Reworded QoS section to state that the code has no hard utilization constraint, but the current flat-below-threshold QoS function has the economic effect of threshold-type congestion control. | Addressed by boundary tightening |
| Attribution table could mislead readers into a causal 87.53% price contribution | Renamed the table and column as diagnostic, not causal; added explanation that the congestion-proxy result close to QoS internalization supports congestion-risk control rather than unique exact QoS-cost identification. | Addressed |
| Finite-user bridge L1 gap remains non-negligible | Added text that L1=0.1558 is not an exact validation of continuous SUE and that individual deployment needs option-level errors or larger finite populations. | Addressed by limitation |
| No public API price comparison | Added a public price scale-check table using official DeepSeek and OpenAI GPT-4o prices, with explicit warning that normalized prices are not economic calibration. | Addressed |
| Migration-cost aggregation still compresses heterogeneity | Added limitation after the aggregate switch-cost equation and again in validity threats; described grouped-logit extension. | Addressed by assumption boundary |
| Section headings still implied strict equilibrium | Changed headings and narrative from strict Stackelberg equilibrium toward Stackelberg-style candidate response and iterative calculation. | Addressed |
| Negative inclusive value may imply market exit | Added diagnostic no-purchase probabilities derived from inclusive value under a utility-zero outside option. | Addressed with derived diagnostic |
| Single-point numeric precision looks overstated | Added validity-threat statement that four-decimal profits/regrets are deterministic reproducibility diagnostics, not true market prediction precision. | Addressed by precision boundary |

## Remaining Honest Limits

- The manuscript still does not provide a continuous-space platform optimum.
- The current QoS function remains threshold-flat below the degradation point.
- The finite-user bridge is trend evidence, not a proof of accurate finite-to-SUE convergence at N=240.
- Public API prices only check scale; they do not calibrate user elasticity, cache-hit rates, token mix, or channel costs.

