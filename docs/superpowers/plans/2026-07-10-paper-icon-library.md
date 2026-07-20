# Paper Icon Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a 48-icon, IconPark-based asset library for the inference-pricing manuscript, including editable SVG sources, a Draw.io custom library, preview sheets, and complete licence provenance.

**Architecture:** A JSON manifest is the single source of truth. A focused Python builder validates the manifest and SVG sources, applies semantic colours only to generated derivatives, emits the Draw.io `mxlibrary`, and renders PNG/PDF contact sheets. Tests validate semantic coverage, source integrity, library structure, and nonblank outputs.

**Tech Stack:** Python 3.12, standard-library JSON/XML, CairoSVG, Pillow, pytest, IconPark SVG sources, Draw.io `mxlibrary` JSON.

---

### Task 1: Define the manifest contract

**Files:**
- Create: `tests/test_paper_icon_library.py`
- Create: `figure_sources/paper_icon_library/manifest.json`

- [x] Write tests requiring 48 unique IDs, six categories with eight entries each, valid priorities, existing source paths, and 48×48 SVG view boxes.
- [x] Run `uv run pytest tests/test_paper_icon_library.py -q` and confirm failure because the manifest and outputs do not yet exist.
- [x] Add the exact 48-entry manifest using only manuscript-relevant IconPark sources.

### Task 2: Preserve sources and provenance

**Files:**
- Create: `figure_sources/paper_icon_library/upstream_svg/*.svg`
- Create: `figure_sources/paper_icon_library/LICENSE-APACHE-2.0.txt`
- Create: `figure_sources/paper_icon_library/MODIFICATIONS.md`

- [x] Copy only the selected SVGs from IconPark commit `8dc132da4c85671ba6a5962c87aa2bdafbf158e9`, retaining source bytes unchanged.
- [x] Export the upstream Apache-2.0 licence and record that colour substitution occurs only in generated Draw.io/preview derivatives.
- [x] Run the source-integrity subset of `tests/test_paper_icon_library.py`.

### Task 3: Build the Draw.io library and contact sheets

**Files:**
- Create: `figure_sources/build_paper_icon_library.py`
- Create: `figure_sources/paper_icon_library/paper-icons.xml`
- Create: `figures/paper_icon_library_2026-07-10.png`
- Create: `figures/paper_icon_library_2026-07-10.pdf`

- [x] Implement manifest loading, SVG validation, semantic recolouring, embedded data URIs, `mxlibrary` generation, and a six-section contact sheet.
- [x] Run `uv run python figure_sources/build_paper_icon_library.py` and verify all four outputs are generated without downloading at build time.
- [x] Run `uv run pytest tests/test_paper_icon_library.py -q` and verify all tests pass.

### Task 4: Document use in the manuscript

**Files:**
- Create: `figure_sources/paper_icon_library/README.md`
- Modify: `README.md`

- [x] Document import steps, category meanings, core versus optional use, palette, licence, and the rule against mixing icon families.
- [x] Record source commit, executed commands, output paths, visual review, and test results in the root README experiment log.

### Task 5: Visual and structural verification

**Files:**
- Inspect: `figures/paper_icon_library_2026-07-10.png`
- Inspect: `figure_sources/paper_icon_library/paper-icons.xml`

- [x] Inspect the full-resolution PNG for clipping, label overlap, weak icon contrast, inconsistent visual weight, or ambiguous semantics.
- [x] Parse the `mxlibrary` JSON and every embedded SVG; verify 48 entries and no external URLs in icon payloads.
- [x] Run `file`, `pdfinfo`, `git diff --check`, the focused pytest file, and a sensitive-data scan before reporting completion.

