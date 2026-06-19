# vLLM Reliability Study Design

## Goal

Strengthen the single-GPU vLLM evidence without downloading additional model
weights. The study must separate controlled concurrency microbenchmarks from
arrival-rate experiments and preserve enough metadata for independent audit.

## Scope

- Reuse `Qwen/Qwen2.5-0.5B-Instruct` from the local Hugging Face cache.
- Repeat critical concurrency levels five times in randomized order.
- Add a deterministic mixed-length workload.
- Add deterministic Poisson arrival schedules.
- Persist request timing, GPU time-series samples, scan order, and runtime
  metadata.
- Aggregate repeated scans with mean, sample standard deviation, and 95%
  confidence intervals.

Larger model validation remains a separate phase because it requires an
explicit model download and disk-space confirmation.

## Components

- `pricing_sim/vllm_study.py`: pure study-design and aggregation helpers.
- `pricing_sim/vllm_benchmark.py`: request execution with optional request
  specifications, optional Poisson schedule, and auditable samples.
- `run_vllm_study.py`: execute the predefined reliability study and write
  machine-readable artifacts.

## Interpretation Boundary

The controlled scan tests whether queueing congestion exists. The Poisson
study checks whether the same pattern appears under arrival-rate load. Neither
study estimates user price elasticity or automatically calibrates the
synthetic QoS proxy.

