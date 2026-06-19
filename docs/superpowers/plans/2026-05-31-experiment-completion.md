# Experiment Completion Implementation Plan

**Goal:** Add empirical QoS calibration, billing ablations, stronger baselines,
scalability measurements, and fairness summaries.

**Architecture:** Keep the canonical simulation stable. Add focused pure
helpers and a supplemental experiment runner that writes auditable CSV and
JSON artifacts.

**Tech Stack:** Python 3, NumPy, SciPy, pytest.

---

### Task 1: Add empirical QoS calibration

- [ ] Add failing tests for aggregate loading, fitted QoS points, and RMSE.
- [ ] Implement `pricing_sim/calibration.py`.
- [ ] Run focused tests.

### Task 2: Add explicit billing models

- [ ] Add failing tests for effective, full, and SLA-penalty billing.
- [ ] Extend `SimulationConfig` and `pricing_sim/economics.py`.
- [ ] Run focused tests.

### Task 3: Add supplemental experiments

- [ ] Add failing tests for rule-baseline feasibility, billing ablations,
  scalability records, and fairness records.
- [ ] Implement `pricing_sim/supplemental_experiments.py`.
- [ ] Add `run_supplemental_experiments.py`.
- [ ] Run focused tests.

### Task 4: Execute and verify

- [ ] Run all tests.
- [ ] Run supplemental experiments against existing 0.5B and 3B vLLM
  aggregates.
- [ ] Inspect generated artifacts.
- [ ] Revise manuscript tables, claims, and limitations.
- [ ] Compile and review the PDF.

