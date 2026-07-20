# Peak-Shaving Framework Draw.io Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build and verify an editable Draw.io framework figure for the fixed-capacity inference-pricing manuscript using the approved Streamline icon set.

**Architecture:** A small Python builder embeds local SVG assets into an `mxGraphModel`, creates two hand-positioned manuscript panels, and writes deterministic Draw.io XML. Pytest checks semantic nodes, connector types, embedded vector assets, and exported files; the Draw.io validator and rendered-image review cover layout risks.

**Tech Stack:** Python 3.12, `xml.etree.ElementTree`, pytest, Draw.io Desktop 30.3.6 portable CLI, Pillow, PDF command-line inspection.

---

### Task 1: Lock the semantic contract

**Files:**
- Create: `tests/test_peak_shaving_framework_drawio.py`

- [ ] **Step 1: Write a failing structure test**

  Parse the expected Draw.io output and assert the presence of the two panels,
  user groups, four channel outcomes, intermediary, two providers, simulation
  stages, and evidence block.

- [ ] **Step 2: Run the test and confirm the red state**

  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py::test_drawio_contains_required_market_and_solver_nodes -q
  ```

  Expected result: failure because
  `figure_sources/peak_shaving_framework_2026-07-11.drawio` does not yet exist.

### Task 2: Generate editable Draw.io XML

**Files:**
- Create: `figure_sources/build_peak_shaving_framework_drawio.py`
- Create: `figure_sources/peak_shaving_framework_2026-07-11.drawio`

- [ ] **Step 1: Implement the minimal builder**

  Add helpers for vertices, text, local SVG image cells, connectors, and
  waypoints. Build the market panel and simulation panel from the design spec.

- [ ] **Step 2: Generate the Draw.io source**

  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run python \
    figure_sources/build_peak_shaving_framework_drawio.py
  ```

- [ ] **Step 3: Run the structural tests**

  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py -q
  ```

  Expected interim result: semantic tests pass; export tests remain pending
  until Task 3 creates the image files.

### Task 3: Validate and export

**Files:**
- Create: `figures/peak_shaving_framework_2026-07-11.png`
- Create: `figures/peak_shaving_framework_2026-07-11.svg`
- Create: `figures/peak_shaving_framework_2026-07-11.pdf`

- [ ] **Step 1: Validate Draw.io structure**

  ```bash
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    --strict figure_sources/peak_shaving_framework_2026-07-11.drawio
  ```

- [ ] **Step 2: Export a clean PNG preview**

  ```bash
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    --no-sandbox --disable-update -x -f png --width 3000 --border 12 \
    -o figures/peak_shaving_framework_2026-07-11.png \
    figure_sources/peak_shaving_framework_2026-07-11.drawio
  ```

- [ ] **Step 3: Export SVG and PDF**

  ```bash
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    --no-sandbox --disable-update -x -e -f svg --embed-svg-images --border 12 \
    -o figures/peak_shaving_framework_2026-07-11.svg \
    figure_sources/peak_shaving_framework_2026-07-11.drawio
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    --no-sandbox --disable-update -x -e -f pdf --crop --border 12 \
    -o figures/peak_shaving_framework_2026-07-11.pdf \
    figure_sources/peak_shaving_framework_2026-07-11.drawio
  ```

### Task 4: Visual QA and documentation

**Files:**
- Modify: `README.md`
- Modify if required: `figure_sources/build_peak_shaving_framework_drawio.py`

- [ ] **Step 1: Inspect the full-resolution PNG**

  Check icon rendering, label clipping, connector routing, legend semantics,
  and panel balance. Make only targeted coordinate or style edits.

- [ ] **Step 2: Run final verification**

  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py -q
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    --strict figure_sources/peak_shaving_framework_2026-07-11.drawio
  git diff --check
  ```

- [ ] **Step 3: Update the experiment record**

  Record source icons, commands, output dimensions, validation results,
  visual corrections, and the boundary that TeX files were not changed.
