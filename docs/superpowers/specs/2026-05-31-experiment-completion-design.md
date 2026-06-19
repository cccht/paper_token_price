# Experiment Completion Design

## Goal

Complete the evidence needed for an algorithm-oriented computer-science paper
without downloading additional model weights.

## Scope

- Fit an empirical QoS curve from the existing repeated vLLM concurrency scans.
- Compare effective billing, full billing, and SLA-penalty revenue models.
- Add time-of-use and queue-aware rule baselines.
- Report a stronger best-observed multi-start reference without claiming a
  certified global optimum.
- Measure optimization runtime as the period count and multi-start count grow.
- Report rigid-user spending, surplus, and QoS disparity by price-sensitivity
  segment.
- Preserve the existing Poisson result as a finite-window burst-arrival stress
  test rather than a steady-state capacity result.

## Design

`pricing_sim/calibration.py` reads repeated vLLM aggregates and fits the
existing exponential QoS proxy to observed TTFT-SLA rates. The fit normalizes
concurrency by the first measured overloaded level and reports RMSE together
with every observed and fitted point.

`pricing_sim/economics.py` supports three explicit billing modes. The default
remains effective billing so existing results stay reproducible. Full billing
does not multiply revenue by QoS. SLA-penalty billing charges completed demand
and subtracts a configurable penalty for degraded service.

`pricing_sim/supplemental_experiments.py` generates separate machine-readable
tables for billing ablations, rule baselines, optimization scalability,
fairness segments, and empirical calibration. Supplemental experiments do not
silently alter the existing canonical matrix.

## Validation

- Add focused unit tests before implementation.
- Run the full test suite.
- Execute the supplemental experiment CLI.
- Check that every optimized policy satisfies the posted-price cap residual.
- Cross-check generated CSV files before revising manuscript claims.

