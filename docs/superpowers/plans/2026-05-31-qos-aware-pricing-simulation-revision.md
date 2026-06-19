# QoS-Aware Token Pricing Simulation Revision Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Deliver a reproducible Chinese working paper centered on a QoS-aware
dynamic-pricing game model, without LLM-serving experiments in the current
phase.

**Architecture:** Split the current monolithic simulation into a small
`pricing_sim` package with typed configuration, pure economic functions,
bounded-simplex projection, deterministic optimization, experiment runners,
and artifact reporting. Preserve `run_experiment.py` as a compatibility entry
point. Regenerate all numerical evidence before rewriting the manuscript.

**Tech Stack:** Python 3, NumPy, SciPy, Matplotlib, pytest, XeLaTeX.

---

### Task 1: Lock Down Canonical Model Contracts

**Files:**
- Create: `pricing_sim/__init__.py`
- Create: `pricing_sim/config.py`
- Create: `tests/test_config.py`

- [ ] Define immutable typed configuration objects for periods, demand, QoS,
  economics, optimizer settings, and experiment output paths.
- [ ] Add validation for compatible period lengths, feasible price bounds, and
  a posted-price cap inside the feasible interval.
- [ ] Add tests for the default configuration and invalid configurations.
- [ ] Run: `python -m pytest tests/test_config.py -q`
- [ ] Record the lack of Git commit support because the workspace is not a Git
  repository.

### Task 2: Implement Pure Demand, QoS, And Economics Functions

**Files:**
- Create: `pricing_sim/demand.py`
- Create: `pricing_sim/qos.py`
- Create: `pricing_sim/economics.py`
- Create: `tests/test_economics.py`

- [ ] Implement rigid demand, flexible demand, utilization, and QoS functions.
- [ ] Implement one canonical profit definition with explicit components.
- [ ] Implement one canonical welfare definition with explicit components.
- [ ] Add tests for vector shapes, QoS threshold behavior, profit component
  consistency, and welfare component consistency.
- [ ] Run: `python -m pytest tests/test_economics.py -q`

### Task 3: Replace Infeasible Price Normalization

**Files:**
- Create: `pricing_sim/projection.py`
- Create: `tests/test_projection.py`

- [ ] Implement bounded-simplex projection by bisection:
  `lower <= prices <= upper` and `mean(prices) == cap`.
- [ ] Add tests for ordinary vectors, clipped vectors, boundary caps, and
  randomized vectors.
- [ ] Require cap residual `<= 1e-8`.
- [ ] Run: `python -m pytest tests/test_projection.py -q`

### Task 4: Implement Reproducible Pricing Algorithms

**Files:**
- Create: `pricing_sim/optimize.py`
- Create: `tests/test_myopic_policy.py`
- Create: `tests/test_optimize.py`

- [ ] Implement uniform pricing.
- [ ] Implement deterministic multi-start QoS-aware optimization.
- [ ] Implement myopic optimization with degradation disabled during search
  and restored during evaluation.
- [ ] Report optimizer status, objective-evaluation count, and all constraint
  residuals.
- [ ] Add tests proving that every returned price vector is feasible and that
  myopic evaluation uses the actual QoS model.
- [ ] Run: `python -m pytest tests/test_myopic_policy.py tests/test_optimize.py -q`

### Task 5: Build Experiment Matrix And Artifact Reporting

**Files:**
- Create: `pricing_sim/experiments.py`
- Create: `pricing_sim/reporting.py`
- Create: `tests/test_experiments.py`
- Create: `artifacts/.gitkeep`

- [ ] Save raw experiment records as JSONL.
- [ ] Save summary tables as CSV and JSON.
- [ ] Save plot-ready records separately from rendered figures.
- [ ] Implement baseline, seed stability, price-cap, QoS-strength,
  QoS-threshold, capacity, elasticity, shift-cost, market-expansion,
  churn-cost, and QoS-feedback experiments.
- [ ] Add a smoke test using a reduced experiment grid.
- [ ] Run: `python -m pytest tests/test_experiments.py -q`

### Task 6: Replace Legacy Entry Point

**Files:**
- Modify: `run_experiment.py`

- [ ] Replace the monolithic implementation with a compatibility CLI that
  delegates to `pricing_sim.experiments`.
- [ ] Support `--smoke` and `--full` modes.
- [ ] Ensure full mode writes timestamped artifacts and regenerated plots.
- [ ] Run: `python run_experiment.py --smoke`

### Task 7: Run Verification And Full Numerical Experiments

**Files:**
- Create: `artifacts/raw/<run-id>/*.jsonl`
- Create: `artifacts/summaries/<run-id>/*.csv`
- Create: `artifacts/summaries/<run-id>/*.json`
- Create: `artifacts/plots/<run-id>/*.pdf`

- [ ] Run: `python -m pytest tests -q`
- [ ] Run: `python run_experiment.py --full`
- [ ] Verify every saved policy satisfies cap residual `<= 1e-8`.
- [ ] Verify repeated runs include seeds and optimizer diagnostics.
- [ ] Inspect generated summaries before using numerical claims.

### Task 8: Rewrite The Manuscript Around Verified Claims

**Files:**
- Modify: `token_dynamic_pricing_game.tex`
- Modify: `paper_refs.bib`

- [ ] Replace `revenue neutrality` with `average posted-price cap`.
- [ ] Replace uncalibrated answer-quality claims with stylized QoS language.
- [ ] Remove unsupported Nash uniqueness, monotonicity, strict-advantage,
  Pareto-improvement, and mechanism-design theorem claims.
- [ ] State the canonical equations exactly as implemented.
- [ ] Present algorithm pseudocode, diagnostics, ablations, and limitations.
- [ ] Move multi-platform competition to a clearly labeled appendix or future
  work section unless its model is repaired and separately verified.
- [ ] Replace manually typed metadata with verified bibliography entries.

### Task 9: Repeat Strict Review And PDF Validation

**Files:**
- Modify as needed: `token_dynamic_pricing_game.tex`

- [ ] Compile with Windows XeLaTeX so Chinese fonts are embedded.
- [ ] Scan the log for unresolved references, citations, and layout warnings.
- [ ] Render the PDF and inspect representative pages visually.
- [ ] Cross-check every manuscript number against generated summaries.
- [ ] Review the paper as a skeptical algorithm-paper reviewer.
- [ ] Revise and rerun validation until no known blocking issue remains.

