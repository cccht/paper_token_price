# Data Availability Statement

The working code repository is available at
<https://github.com/cccht/paper_token_price>. The current July 2026 manuscript,
common-candidate sensitivity results, and dependent audit rebuild have not yet been
frozen or fully pushed. A versioned release and persistent archive identifier will be
added before submission; the working repository URL is not a substitute for that
archive.

The formal internal-review artifacts are under:

- `data/processed/burstgpt_d895a53b_8period/`;
- `artifacts/peak_shaving/20260712_final/`;
- `artifacts/peak_shaving/20260712_expanded_response/`; and
- `figures/peak_shaving_final_20260714/`.

`ARTIFACT_MANIFEST.md` identifies which files support manuscript claims and which are
historical diagnostics or interrupted-run logs.

The raw BurstGPT trace is not redistributed. It is available from the official BurstGPT
repository under CC BY 4.0. The derived-data README records the pinned source commit,
raw-file SHA-256, file size, row count, retained days, license, and aggregation method.

The controlled vLLM measurements and fitted QoS points are retained as derived artifacts.
They cover two Qwen2.5 models on one RTX 4090 with five repeats per concurrency level.
They anchor only the shape of the reduced-form QoS function and do not constitute a
production workload or cluster validation.

The economic parameters are synthetic design values. The repository does not contain
observed inference-user price elasticity, consumer-surplus data, production API demand,
or multi-GPU production QoS measurements.
