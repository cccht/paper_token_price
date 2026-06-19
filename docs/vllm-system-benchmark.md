# Single-GPU vLLM System Benchmark

## Purpose

This benchmark measures overload behavior on a controllable vLLM backend.
It complements the Ollama external-validity check and does not claim semantic
quality degradation.

## Installation And Disk Usage

- Environment: `/root/.venvs/tokenrl-vllm`
- vLLM: 0.22.0
- PyTorch: 2.11.0+cu130
- GPU: NVIDIA GeForce RTX 4090
- Environment size: 8.6 GB on the WSL root filesystem
- vLLM cache: 28 MB on the WSL root filesystem
- FlashInfer cache: 40 MB on the WSL root filesystem
- WSL free space after installation: approximately 570 GB
- Model weights: reused from `D:\huggingface_cache`

No new Hugging Face model weights were downloaded for this benchmark.

## Server

```bash
export HOME=/root
export HF_HOME=/mnt/d/huggingface_cache
export HF_HUB_OFFLINE=1
export TRANSFORMERS_OFFLINE=1
export NO_PROXY=127.0.0.1,localhost
export no_proxy=127.0.0.1,localhost
unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy

/root/.venvs/tokenrl-vllm/bin/vllm serve Qwen/Qwen2.5-0.5B-Instruct \
  --host 0.0.0.0 \
  --port 8000 \
  --dtype auto \
  --max-model-len 2048 \
  --gpu-memory-utilization 0.75
```

## Overload Scan

Artifact directory: `artifacts/vllm/system/20260531-175235`

```powershell
python .\experiments\run_vllm_benchmark.py `
  --model 'Qwen/Qwen2.5-0.5B-Instruct' `
  --concurrency 64 96 112 128 144 160 192 224 256 384 512 `
  --requests-per-level 512 `
  --warmup-requests 2 `
  --max-tokens 256 `
  --prompt-repeat 1 `
  --timeout-seconds 120 `
  --gpu-sample-interval-seconds 0.05 `
  --output-root .\artifacts\vllm
```

Each level records 512 successful requests with 20 prompt tokens and 256
generated tokens per request. TTFT SLA rates count failed requests as SLA
violations.

## Interpretation Boundary

The overload scan identifies queueing growth and SLA degradation on one
single-GPU vLLM configuration. It does not establish a universal QoS curve.
Multi-model, multi-GPU, realistic arrival-trace, and repeated-run experiments
remain necessary before replacing the synthetic QoS proxy.

## Reliability Study

The reliability study reuses the cached 0.5B model and adds randomized repeated
scans, a mixed-length workload, Poisson arrival schedules, timestamped request
records, timestamped GPU samples, and uncertainty aggregation.

```powershell
python .\experiments\run_vllm_study.py `
  --model 'Qwen/Qwen2.5-0.5B-Instruct' `
  --concurrency 64 128 224 384 512 `
  --repeats 5 `
  --controlled-requests-per-level 512 `
  --auxiliary-requests 256 `
  --auxiliary-repeats 3 `
  --max-tokens 128 `
  --arrival-rate 8 16 32 `
  --output-root .\artifacts\vllm-study
```

The Poisson experiment remains a synthetic arrival process. It is not a
production trace replay and does not estimate user price elasticity.

## Second-Model Check

`Qwen/Qwen2.5-3B-Instruct` was downloaded to the existing Hugging Face cache
after disk-space confirmation. Its cache footprint is approximately 5.8 GB.
The repeated controlled scan is stored under:

```text
artifacts/vllm-study-qwen25-3b/20260531-214710
```

At 384 concurrent requests, mean TTFT reaches 0.539 seconds and the 0.5-second
TTFT SLA rate falls to 66.7 percent. This confirms the congestion pattern on a
second vLLM model but remains a single-GPU microbenchmark.

## Bounded Multi-Wave Batch Stress Test

`experiments/run_vllm_extreme.py` adds staged finite-batch stress tests with stop
conditions for GPU temperature, request failure rate, and free disk space.
Each concurrency level submits a bounded number of requests over multiple
waves. The test is not an open-loop steady-state workload. The script also
supports tokenizer-based prompt construction for long-context checks. The
initial 3B scan used a conservative 30 GiB disk threshold. Follow-up scans
used 10 GiB after confirming sufficient free space.

```bash
python experiments/run_vllm_extreme.py \
  --model Qwen/Qwen2.5-3B-Instruct \
  --endpoint http://192.168.110.16:8000 \
  --concurrency 32 64 128 \
  --request-multiplier 2 \
  --prompt-token-target 1536 \
  --max-tokens 128 \
  --min-free-disk-gib 10 \
  --safety-disk-path /mnt/d \
  --output-root artifacts/vllm-extreme-qwen25-3b-context-1536
```

Completed artifacts:

- `artifacts/vllm-extreme-qwen25-05b/20260601-095434`
- `artifacts/vllm-extreme-qwen25-3b/20260531-231707`
- `artifacts/vllm-extreme-qwen25-3b-high/20260601-093105`
- `artifacts/vllm-extreme-qwen25-3b-context-256/20260601-095143`
- `artifacts/vllm-extreme-qwen25-3b-context-768/20260601-095224`
- `artifacts/vllm-extreme-qwen25-3b-context-1536/20260601-095301`
- `artifacts/vllm-extreme-qwen25-05b-repeat-224/20260601-111400`
- `artifacts/vllm-extreme-qwen25-05b-repeat-224/20260601-111423`
- `artifacts/vllm-extreme-qwen25-05b-repeat-224/20260601-111436`

The 3B 768-concurrency level was stopped before artifact completion because
the multi-wave queue no longer added useful evidence. It is excluded from the
reported results.
The extreme runner now writes a root-level checkpoint after every completed
concurrency level, so a later interrupted level does not hide completed data.

## 0.5B 224-Concurrency Repeat Check

The original bounded multi-wave scan reported an unusually low 4537.94
tokens/s at 224 concurrency. Three independent reruns with 896 requests each
reported 8731.47, 12936.41, and 13193.75 tokens/s. The two warm-state reruns
average 13065.08 tokens/s. The original low value is retained as an artifact
but is not used as a stable-capacity estimate.
