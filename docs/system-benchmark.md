# Single-GPU Ollama System Benchmark

## Purpose

This benchmark measures operational inference-service QoS under controlled
single-GPU load. It does not replace the synthetic pricing model and does not
claim semantic-quality degradation.

## Environment

- Backend: Ollama 0.24.0
- GPU: NVIDIA GeForce RTX 4090, 24,564 MiB
- Model: `pdurugyan/qwen3.5-9b-deepseek-v4-flash-Q4_K_M:latest`
- Model format: GGUF, 9.0B parameters, Q4_K_M quantization

## Primary Run

Artifact directory: `artifacts/system/20260531-150455`

```powershell
python .\experiments\run_system_benchmark.py `
  --model 'pdurugyan/qwen3.5-9b-deepseek-v4-flash-Q4_K_M:latest' `
  --concurrency 1 2 4 8 `
  --requests-per-level 12 `
  --warmup-requests 2 `
  --max-tokens 128 `
  --prompt-repeat 1 `
  --timeout-seconds 120 `
  --output-root .\artifacts
```

The primary run uses 30 prompt tokens and records 48 successful requests.

## Prompt-Length Sensitivity

Artifact directory: `artifacts/system/20260531-150340`

```powershell
python .\experiments\run_system_benchmark.py `
  --model 'pdurugyan/qwen3.5-9b-deepseek-v4-flash-Q4_K_M:latest' `
  --concurrency 1 `
  --requests-per-level 6 `
  --warmup-requests 1 `
  --max-tokens 64 `
  --prompt-repeat 16 `
  --timeout-seconds 120 `
  --output-root .\artifacts
```

The sensitivity run uses 315 prompt tokens and records 6 successful requests.

## Interpretation Boundary

The measurements show queueing growth near backend saturation. They do not
justify replacing the synthetic QoS proxy with a universal fitted curve.
Multi-model, vLLM, multi-GPU, timeout-threshold, and real-arrival-trace
experiments remain future work.
