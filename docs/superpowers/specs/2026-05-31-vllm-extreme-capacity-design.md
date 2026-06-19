# vLLM Extreme Capacity Design

## Goal

Measure the sustainable single-GPU capacity boundary of a personal RTX 4090
without deliberately triggering an out-of-memory failure.

## Scope

- Reuse cached Qwen models without downloading additional weights.
- Add temperature, power, GPU-memory, service-health, failure-rate, and disk
  safety checks.
- Run a staged capacity scan before longer sustained repeats.
- Add long-context scans after the stable capacity range is known.
- Preserve every request record, GPU sample, runtime configuration, and stop
  reason.

## Safety Limits

- Stop after a level if GPU temperature exceeds 82 C.
- Stop after a level if request failure rate exceeds 10 percent.
- Stop after a level if the vLLM health endpoint fails.
- Stop after a level if `/mnt/d` free space falls below 30 GiB.
- Keep `gpu-memory-utilization=0.75` so the experiment remains comparable to
  the existing repeated scans.

## Interpretation Boundary

The study measures the capacity of one RTX 4090 configuration. It does not
establish universal serving capacity, multi-GPU scaling, or production-trace
performance.

