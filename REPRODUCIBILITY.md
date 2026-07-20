# Reproducibility Guide

This repository contains the model, numerical experiments, artifacts, and LaTeX
sources for:

> Time-of-use pricing for fixed-capacity inference services: a simulation of
> temporal load shifting and provider substitution

Working repository: <https://github.com/cccht/paper_token_price>

The current July 2026 submission state has not yet been frozen or assigned a
persistent archive identifier. Use `ARTIFACT_MANIFEST.md` to distinguish formal
claim sources from historical diagnostics.

## Environment

Run commands from the repository root on Linux or WSL with Python 3.12 and `uv`.
The active finite-game runs use Python 3.12.13, NumPy 2.4.4, SciPy 1.17.1, and
Nashpy 0.0.43. Figure and test checks use Matplotlib 3.10.8 and Pytest 9.1.0.

```bash
uv run --no-project --with-requirements requirements.txt python -c \
  'import numpy, scipy, nashpy; print(numpy.__version__, scipy.__version__, nashpy.__version__)'
```

The provider-game solve is CPU-bound NumPy/SciPy work. The reported run uses
process-level CPU parallelism and one BLAS thread per worker; it does not use a GPU
solver path.

## Input Anchors

Rebuild the derived BurstGPT load profile from the pinned public source:

```bash
TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
uv run --no-project --with numpy \
python experiments/build_burstgpt_load_anchor.py
```

Rebuild the QoS fit from the recorded vLLM measurements:

```bash
TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
uv run --no-project --with numpy --with scipy \
python experiments/build_final_qos_calibration.py
```

The raw BurstGPT CSV is not redistributed. Its repository, pinned commit, checksum,
license, and aggregation rule are recorded in
`data/processed/burstgpt_d895a53b_8period/`.

## Baseline Finite Game

The formal baseline uses an audit-adaptive set of 1,576 bounded linear provider price
rules. Its complete zero-slope subset contains 800 rules and defines the uniform-price
comparison. The submission runner requires an existing audited equilibrium seed. The
pre-expansion equilibrium is retained separately as the continuation seed; the formal
`spatiotemporal_equilibrium_submission.json` records the expanded result and exact
candidate set. This reproduces the declared finite-game calculation; it is not an
independent rediscovery of the candidate set from an empty strategy space.

```bash
TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --no-project --with numpy --with scipy --with nashpy \
python -m experiments.run_submission_spatiotemporal_equilibrium
```

The signature-checked pair cache reduces runtime but does not change the declared
candidate set or stopping rule. Without a compatible cache, required provider pairs
are recomputed.

## Sensitivity Re-solves

The sensitivity runner jointly rebuilds the baseline row and eight local,
one-factor-at-a-time perturbations on the common 1,576-candidate set. Each uniform
comparison uses the complete 800-rule zero-slope subset:

```bash
TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
uv run --no-project --with numpy --with scipy --with nashpy \
python -m experiments.run_submission_spatiotemporal_sensitivity
```

This is a long CPU calculation. A scenario is accepted only after source hashes,
scenario identity, the shared strategy contract, 800/1,576 game sizes, demand
conservation, full-candidate regret, and joint fixed-point residual pass
`submission_evidence_gates.py`.

## Dependent Audits

After the baseline and sensitivity outputs are fixed, rebuild the numerical audits and
derived distributions:

```bash
TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy \
  python -m experiments.run_submission_fixed_point_audit
TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy --with scipy \
  python -m experiments.run_submission_intermediary_audit
TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy --with scipy \
  python -m experiments.build_submission_intermediary_payoff_sensitivity
TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy --with scipy \
  python -m experiments.run_submission_uniform_offgrid_audit
TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy \
  python -m experiments.run_submission_mechanism_decomposition
TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy \
  python -m experiments.build_submission_mixed_distribution
TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy \
  python -m experiments.run_submission_price_shape_decomposition
```

Then generate claims, run the combined gates, and rebuild tables and figures:

```bash
uv run --no-project python experiments/build_submission_sensitivity_claims.py
uv run --no-project --with numpy --with scipy --with nashpy \
  python -m experiments.submission_evidence_gates
uv run --no-project python experiments/build_submission_sensitivity_table.py
uv run --no-project python experiments/build_submission_result_macros.py
uv run --no-project --with matplotlib --with numpy --with scipy \
  python experiments/build_final_submission_figures.py
```

`submission_evidence_gate_report.json` must contain `"passed": true` before any
generated number is transferred into the final manuscript.

## Tests

```bash
TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
uv run --no-project --with-requirements requirements.txt pytest -q \
  tests/test_submission_*.py tests/test_final_submission_figures.py
```

The three sensitivity-dependent checks in
`tests/test_final_manuscript_20260714.py` remain red until the nine-row table,
Figure 6, and machine-derived result paragraph are integrated.

## Paper Build

```bash
latexmk -xelatex -interaction=nonstopmode -halt-on-error \
  peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
```

The review manuscript is still anonymous and uses a generic article class. Author
metadata and the journal-specific Elsevier package are prepared only after the evidence
gates pass.

## Claim Boundaries

The artifacts support a conserved-demand, synthetic-calibration mechanism simulation
on a declared finite provider strategy set. They do not support production prediction,
calibrated user price elasticity, a continuous-strategy equilibrium proof, global
intermediary optimality, robust profit improvement, or production-cluster QoS
validation.
