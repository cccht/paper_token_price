# Reproducibility Guide

This repository contains the simulation code, experiment scripts, artifacts, and
LaTeX sources for the SMPT-targeted manuscript:

> A Simulation-Based Study of Time-of-Use Pricing for Fixed-Capacity AI
> Inference Services: QoS Protection and the Profit Boundary

## Environment

The experiments are intended to run on Linux or WSL. The verified local
environment used WSL Ubuntu 22.04 and `uv 0.10.9`.

```bash
uv sync
uv run pytest tests/test_peak_shaving_smpt_experiments.py -q
```

If `uv sync` is not available for the local setup, install the Python packages
listed in `requirements.txt` in a clean Python 3.12 environment.

## Main SMPT Reproduction Commands

Run from the repository root:

```bash
uv run python experiments/run_peak_shaving_smpt_experiments.py
uv run python experiments/run_peak_shaving_smpt_vv_audit.py
uv run pytest tests/test_peak_shaving_smpt_experiments.py -q
```

The command writes:

- `artifacts/peak_shaving/20260619_smpt/peak_shaving_smpt_experiments.json`
- `artifacts/peak_shaving/20260619_smpt/smpt_baselines.csv`
- `artifacts/peak_shaving/20260619_smpt/smpt_ablations.csv`
- `artifacts/peak_shaving/20260619_smpt/smpt_phase_grid.csv`
- `artifacts/peak_shaving/20260619_smpt/smpt_fixed_point_residuals.csv`
- `artifacts/peak_shaving/20260619_smpt/smpt_vv_damping_initial.csv`
- `artifacts/peak_shaving/20260619_smpt/smpt_vv_damping_initial_summary.json`
- `artifacts/peak_shaving/20260619_smpt/smpt_resolved_sensitivity.csv`
- `figures/peak_shaving_smpt/smpt_baseline_comparison.pdf`
- `figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf`
- `figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf`

## Existing Submission Diagnostics

```bash
uv run python experiments/build_peak_shaving_diagnostics.py
uv run python experiments/run_peak_shaving_parameter_sweep.py
uv run python experiments/run_peak_shaving_mixed_oracle.py
uv run python experiments/build_peak_shaving_measurement_anchor.py
```

## Paper Build

```bash
xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex
bibtex peak_shaving_dynamic_pricing_sci_en_2026-06-19
xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex
xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex
xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex
```

## Claim Boundaries

The artifact supports a simulation-based mechanism analysis. It does not support
production prediction, calibrated user price elasticity, continuous-space Nash
equilibrium claims, or production-level QoS validation.
