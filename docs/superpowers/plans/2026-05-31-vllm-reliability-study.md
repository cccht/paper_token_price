# vLLM Reliability Study Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add reproducible repeated and arrival-rate vLLM experiments with
auditable artifacts and uncertainty summaries.

**Architecture:** Keep request execution in `vllm_benchmark.py`. Add pure study
helpers in `vllm_study.py` and a small CLI orchestrator in
`run_vllm_study.py`. Preserve existing single-scan compatibility.

**Tech Stack:** Python 3, requests, NumPy-free standard library statistics,
pytest, vLLM OpenAI-compatible API.

---

### Task 1: Pure study helpers

**Files:**
- Create: `pricing_sim/vllm_study.py`
- Test: `tests/test_vllm_study.py`

- [ ] Add failing tests for randomized orders, Poisson offsets, mixed request
  specifications, and uncertainty aggregation.
- [ ] Run `python -m pytest tests/test_vllm_study.py -q` and confirm failure.
- [ ] Implement the minimal pure helpers.
- [ ] Re-run the focused tests.

### Task 2: Auditable benchmark artifacts

**Files:**
- Modify: `pricing_sim/system_benchmark.py`
- Modify: `pricing_sim/vllm_benchmark.py`
- Modify: `run_vllm_benchmark.py`
- Test: `tests/test_system_benchmark.py`

- [ ] Add a failing test that requires `gpu_samples.jsonl`.
- [ ] Run the focused test and confirm failure.
- [ ] Persist timestamped GPU samples and request timestamps.
- [ ] Re-run the focused tests.

### Task 3: Reliability study CLI

**Files:**
- Create: `run_vllm_study.py`
- Modify: `docs/vllm-system-benchmark.md`

- [ ] Add the study orchestrator using the tested helpers.
- [ ] Document the exact local command and interpretation boundary.
- [ ] Run all tests.

### Task 4: Execute and report

- [ ] Start the local offline vLLM server.
- [ ] Run five randomized repeated scans plus mixed-length and Poisson studies.
- [ ] Inspect artifact completeness and aggregate statistics.
- [ ] Update manuscript tables, claims, and limitations.
- [ ] Compile the manuscript and perform completion verification.

