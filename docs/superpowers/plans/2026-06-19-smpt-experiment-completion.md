# SMPT Experiment Completion Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:executing-plans or inline execution task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add SMPT-oriented baseline, ablation, sensitivity, and V&V evidence without overwriting existing artifacts.

**Architecture:** A small tested helper module evaluates reported policies and diagnostic variants. A runner script writes the experiment bundle, tables, and publication-style figures. The manuscript consumes the generated tables and figures cautiously.

**Tech Stack:** Python, NumPy, Matplotlib, existing `pricing_sim` modules, XeLaTeX.

---

### Task 1: Test SMPT Helper API

**Files:**
- Create: `tests/test_peak_shaving_smpt_experiments.py`

- [ ] Write tests for policy vector loading, price-shape transformations, baseline records, and phase-grid summaries.
- [ ] Run `uv run pytest tests/test_peak_shaving_smpt_experiments.py -q` and confirm it fails because the helper module does not exist.

### Task 2: Implement SMPT Helper Module

**Files:**
- Create: `experiments/peak_shaving_smpt_tools.py`

- [ ] Implement evaluated policy records with common metrics.
- [ ] Implement off-peak-discount-only and peak-surcharge-only transforms.
- [ ] Implement equal-routing and admission-control diagnostics.
- [ ] Implement fixed-point residual tracing.
- [ ] Implement compact phase-grid evaluation.
- [ ] Run the focused tests and confirm they pass.

### Task 3: Implement SMPT Runner

**Files:**
- Create: `experiments/run_peak_shaving_smpt_experiments.py`

- [ ] Write JSON/CSV outputs to `artifacts/peak_shaving/20260619_smpt/`.
- [ ] Write figures to `figures/peak_shaving_smpt/`.
- [ ] Include strong baselines, ablations, re-solved sensitivity, residual diagnostics, and phase diagrams.
- [ ] Run the runner and inspect summary output.

### Task 4: Update Manuscript and Supplement

**Files:**
- Modify: `peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex`
- Modify: `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex`

- [ ] Add SMPT baseline and V&V evidence to the manuscript.
- [ ] Add artifact map and reproduction command entries to the supplement.
- [ ] Preserve cautious claim boundaries.

### Task 5: Verify

**Files:**
- Modify: `README.md`

- [ ] Run focused tests.
- [ ] Run SMPT experiment script.
- [ ] Compile main and supplement.
- [ ] Check logs and PDF text.
- [ ] Record commands and results in README.
