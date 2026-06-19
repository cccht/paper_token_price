# vLLM Extreme Capacity Implementation Plan

**Goal:** Add bounded RTX 4090 capacity scans and publish auditable artifacts.

**Architecture:** Extend the existing vLLM benchmark sampler with thermal and
power metrics. Add a separate extreme-scan CLI with automatic stop conditions
so existing reliability experiments remain reproducible.

---

### Task 1: Add safety telemetry

- [x] Add failing tests for thermal and power summaries.
- [x] Extend GPU samples and summaries.
- [x] Run focused tests.

### Task 2: Add bounded extreme-scan runner

- [x] Add failing tests for temperature, failure-rate, disk, and health stops.
- [x] Implement `pricing_sim/vllm_extreme.py`.
- [x] Implement `run_vllm_extreme.py`.
- [x] Verify a low-concurrency probe.

### Task 3: Execute staged experiments

- [x] Run a 3B upper-bound sweep.
- [x] Run sustained 3B repeats near the measured boundary.
- [x] Run long-context 3B scans.
- [x] Run the cached 0.5B cross-model check.
- [x] Attempt the cached 0.8B check and record its incomplete local processor
      snapshot as a compatibility limitation.

### Task 4: Report and verify

- [x] Inspect artifact completeness.
- [x] Update the manuscript and benchmark documentation.
- [x] Run all tests, compile the manuscript, and inspect the PDF.
