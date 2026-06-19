# QoS-Aware Token Pricing Simulation Revision Design

## 1. Objective

Revise the current token-pricing paper into a reproducible Chinese working
paper for a future computer-science algorithm submission.

Phase 1 covers numerical simulation only. It does not download language-model
weights, start an LLM serving backend, or claim that GPU load directly reduces
answer correctness. A future Phase 2 may add controlled serving experiments.

The Phase 1 paper studies:

> A QoS-aware constrained dynamic-pricing algorithm for inference services.
> Under an average posted-price cap, the algorithm shifts flexible demand
> across time periods and evaluates the resulting profit and service-quality
> trade-offs.

## 2. Scope

### 2.1 Included

- A single-platform multi-period simulation model.
- Explicit separation between demand, QoS, profit, welfare, and optimization.
- A feasible average posted-price constraint with numerical residual checks.
- Baselines: uniform pricing, myopic dynamic pricing, and QoS-aware dynamic
  pricing.
- Repeated runs, convergence diagnostics, ablations, and sensitivity analyses.
- Machine-readable raw results, summaries, plot data, and generated figures.
- Paper revision based only on regenerated evidence.
- A limited multi-platform appendix after the single-platform model is stable.

### 2.2 Excluded From Phase 1

- LLM downloads, vLLM deployment, Ollama benchmarks, and GPU-serving tests.
- Claims that high GPU utilization necessarily reduces semantic correctness.
- Unproven pure-strategy Nash existence or uniqueness claims.
- Unproven monotonicity, Pareto-improvement, or mechanism-design theorems.
- Quantitative policy recommendations based on uncalibrated parameters.

## 3. Terminology

Use consistent terminology throughout the code and paper:

| Term | Meaning |
| --- | --- |
| `average posted-price cap` | Constraint on the unweighted mean of posted period prices |
| `QoS factor` | Stylized multiplier representing effective service quality |
| `QoS-aware pricing` | Dynamic pricing optimized with the QoS factor enabled |
| `myopic pricing` | Prices optimized without QoS degradation, then evaluated under the actual QoS model |
| `uniform pricing` | Constant price equal to the posted-price cap |

Avoid using `revenue neutrality`, `降智`, and `Pareto improvement` unless a
future empirical or theoretical result justifies the stronger term.

## 4. Canonical Simulation Model

### 4.1 Inputs

The model receives:

- period count and duration;
- rigid baseline demand by period;
- flexible baseline demand;
- capacity;
- posted-price cap;
- wholesale cost;
- price bounds;
- flexible-user price sensitivity and time preferences;
- optional market-expansion coefficient;
- QoS threshold and QoS-degradation strength;
- optional churn-cost coefficients.

All inputs must be stored in a typed configuration object and serialized with
each experiment.

### 4.2 Demand

Rigid demand and flexible demand must be computed in separate functions.
Flexible demand may use time preference, price response, and optional market
expansion. The paper must state the exact same equations used by the code.

The baseline model does not feed QoS back into user utility. A QoS-feedback
variant is an ablation, not an implicit implementation detail.

### 4.3 QoS

The QoS factor is a stylized simulation function:

```text
q(u) = 1                              if u <= threshold
q(u) = exp(-strength * (u-threshold)^2) otherwise
```

The paper must describe this function as a parameterized QoS proxy. Phase 1
does not claim that it is empirically calibrated.

### 4.4 Profit And Welfare

Profit must have one canonical definition. Any churn costs or other penalties
must be explicitly included in both the code and paper.

Welfare must have one canonical definition with documented components. The
reported summary must include a component-level breakdown so that readers can
inspect which terms drive each result.

## 5. Optimization

### 5.1 Feasible Price Projection

Replace shift-then-clip normalization with a bounded-simplex projection:

```text
lower_bound <= p_t <= upper_bound
mean(p) == posted_price_cap
```

Every optimized result must report:

- mean posted price;
- cap residual;
- lower-bound residual;
- upper-bound residual;
- optimizer status;
- number of objective evaluations.

The acceptance threshold for the cap residual is `1e-8`.

### 5.2 Algorithms

Compare:

1. Uniform pricing.
2. Myopic dynamic pricing:
   optimize with QoS degradation disabled, then evaluate the returned prices
   with the actual QoS model.
3. QoS-aware dynamic pricing:
   optimize and evaluate with the actual QoS model.

Use deterministic seed control and repeated multi-start optimization.
The paper must not claim global optimality unless an exhaustive or certifying
method is added.

## 6. Experimental Matrix

### 6.1 Required Experiments

- Baseline comparison across all three algorithms.
- Seed stability with at least `10` seeds.
- Price-cap sensitivity.
- QoS-strength sensitivity.
- QoS-threshold sensitivity.
- Capacity sensitivity.
- Flexible-demand elasticity sensitivity.
- Shift-cost sensitivity.
- Market-expansion ablation including `growth = 0`.
- Churn-cost ablation.
- QoS-feedback ablation.

### 6.2 Required Evidence

Each experiment must save:

- full configuration;
- random seed;
- price vector;
- demand vectors;
- utilization vector;
- QoS vector;
- profit;
- welfare and welfare components;
- constraint residuals;
- optimizer diagnostics.

Summaries must report mean, standard deviation, minimum, and maximum where
repeated runs apply.

## 7. Artifact Layout

Create focused files instead of extending the existing monolithic script:

```text
paper_token_cross_survey/
  pricing_sim/
    config.py
    demand.py
    qos.py
    economics.py
    projection.py
    optimize.py
    experiments.py
    reporting.py
  tests/
    test_projection.py
    test_economics.py
    test_myopic_policy.py
    test_experiments.py
  artifacts/
    raw/
    summaries/
    plots/
```

Keep `run_experiment.py` as a compatibility entry point that delegates to the
new package. Preserve existing figures until regenerated replacements exist.

## 8. Paper Revision

Rewrite the paper around an algorithmic contribution:

1. Introduction.
2. Related work.
3. Problem definition and assumptions.
4. QoS-aware constrained pricing algorithm.
5. Numerical experiments.
6. Limitations and future system validation.
7. Conclusion.

Move the multi-platform model to an appendix until its wholesale-price model,
routing logic, and convergence diagnostics are aligned.

Replace strong unsupported claims with bounded statements:

- report empirical observations as observations;
- state sufficient conditions only when formally proved;
- label QoS parameters as synthetic;
- avoid causal claims about answer quality;
- avoid aggregate-welfare claims phrased as individual Pareto improvements.

## 9. Validation Gates

Before revising numerical claims in the paper:

1. Run unit tests.
2. Run the complete Phase 1 experiment matrix.
3. Verify every saved policy satisfies the cap residual threshold.
4. Regenerate tables and figures from saved artifacts.
5. Cross-check every number in the paper against generated summaries.
6. Compile the LaTeX manuscript with embedded Chinese fonts.
7. Inspect the PDF visually and scan the LaTeX log for unresolved warnings.
8. Verify cited metadata programmatically before submission.

## 10. Future Phase 2

After Phase 1 is stable, add a separate system-validation design:

- vLLM as the primary serving backend;
- Ollama only as an optional external-validity check;
- controlled load generation;
- TTFT, TPOT, throughput, tail latency, timeout, truncation, and task-success
  metrics;
- empirical fitting of a QoS curve;
- replacement of synthetic QoS parameters only after measurement.

Phase 2 is intentionally excluded from the current implementation plan.

