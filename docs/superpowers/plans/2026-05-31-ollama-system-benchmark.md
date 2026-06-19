# Ollama System Benchmark Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use
> superpowers:subagent-driven-development (recommended) or
> superpowers:executing-plans to implement this plan task-by-task. Steps use
> checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a reproducible single-GPU Ollama benchmark that records empirical
inference-service QoS metrics without changing the synthetic pricing model.

**Architecture:** Add an isolated `pricing_sim.system_benchmark` module for
stream parsing, concurrent load generation, GPU sampling, aggregation, and
artifact writing. Add a small CLI entry point. Keep empirical measurements
separate from the synthetic pricing artifacts until curve fitting is justified
by sufficient data.

**Tech Stack:** Python 3, requests, concurrent.futures, nvidia-smi, pytest.

---

### Task 1: Define Stream Parsing And Aggregation Contracts

**Files:**
- Create: `tests/test_system_benchmark.py`
- Create: `pricing_sim/system_benchmark.py`

- [x] Write failing tests for stream parsing, aggregation, and invalid load
  levels.
- [x] Run the focused tests and confirm failure because the module is absent.
- [x] Implement immutable benchmark configuration, stream parsing, percentile
  calculation, and summary aggregation.
- [x] Run the focused tests and confirm success.

### Task 2: Add Concurrent Ollama Load Generation

**Files:**
- Modify: `pricing_sim/system_benchmark.py`
- Create: `run_system_benchmark.py`

- [x] Implement one streamed request against the local Ollama API.
- [x] Sample GPU memory and utilization with `nvidia-smi`.
- [x] Execute fixed requests at concurrency levels `1`, `2`, `4`, and `8`.
- [x] Write raw JSONL, summary JSON, summary CSV, and metadata JSON artifacts.
- [x] Expose model, endpoint, concurrency, request count, output length, and
  timeout through the CLI.

### Task 3: Run And Audit The Single-GPU Benchmark

**Files:**
- Create: `artifacts/system/<run-id>/raw_requests.jsonl`
- Create: `artifacts/system/<run-id>/summary.json`
- Create: `artifacts/system/<run-id>/summary.csv`
- Create: `artifacts/system/<run-id>/metadata.json`

- [x] Warm up the cached 9B Ollama model.
- [x] Run the controlled load matrix.
- [x] Confirm that each load level has repeated requests.
- [x] Inspect completion rates, TTFT, TPOT, throughput, and sampled GPU metrics.

### Task 4: Add Bounded Manuscript Evidence

**Files:**
- Modify: `token_dynamic_pricing_game.tex`

- [x] Add a system-measurement subsection that states the backend, GPU,
  quantization, workload, and measured metrics.
- [x] Report empirical observations without claiming semantic-quality
  degradation or a calibrated replacement for the synthetic QoS function.
- [x] Compile the manuscript, scan warnings, run all tests, and inspect the
  affected PDF pages.
