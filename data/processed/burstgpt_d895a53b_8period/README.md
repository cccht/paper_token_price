# BurstGPT eight-period load anchor

This directory contains a small derived intraday profile used to anchor the
spatiotemporal mechanism experiment. The raw trace is not copied into this
repository.

## Source

- Dataset: BurstGPT
- Repository: <https://github.com/HPMLL/BurstGPT>
- Pinned commit: `d895a53bb7b8ec137d0d2fe203b335835a78c10a`
- Raw file: `data/BurstGPT_1.csv`
- Raw SHA-256: `46fc9480ef0b748ecb2b51d512ff08c196b031782cbe6f78e28044d768e86d5a`
- Raw size: `50,853,373` bytes
- License: CC BY 4.0
- Citation: Yuxin Wang et al., "BurstGPT: A Real-World Workload Dataset to
  Optimize LLM Serving Systems," KDD 2025,
  <https://doi.org/10.1145/3711896.3737413>.

## Processing

The pinned CSV is streamed from the official repository to `/tmp`. Requests
are assigned to eight three-hour bins using `Timestamp mod 86400`. The first
and last days are excluded. Each remaining complete day is normalized to unit
request mass and unit token mass before the 59 daily profiles are averaged.
The normalized token load is centered to zero mean and divided by its maximum
absolute deviation.

```bash
TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy \
  python experiments/build_burstgpt_load_anchor.py
```

`burstgpt_8period_load_profile.csv` stores the day-normalized mean and standard
deviation for request and token shares. The JSON file records the source URL,
commit, checksum, row count, retained days, license, and aggregation rule.

## Boundary

This profile anchors only the intraday arrival shape. It does not estimate user
price elasticity, migration cost, market exit, provider capacity, or production
QoS. BurstGPT timestamps are calibrated to the source service's local time, but
the public file does not identify that time zone; period labels are therefore
relative positions within the recorded local day.
