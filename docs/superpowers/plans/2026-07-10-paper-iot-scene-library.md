# Paper IoT Scene Library Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build 18 concrete, editable IoT scene assets from the manuscript's licensed IconPark component library.

**Architecture:** A scene manifest declares component icon IDs, positions, sizes, links, badges, and priority. A Python builder resolves components through the existing base manifest, generates one self-contained SVG per scene, emits a Draw.io custom library, and assembles a six-by-three review sheet in SVG, PNG, and PDF.

**Tech Stack:** Python 3.12, standard-library JSON/XML, CairoSVG, Pillow tests, the existing IconPark base library, Draw.io `mxlibrary` JSON.

---

### Task 1: Define the scene contract

**Files:**
- Create: `tests/test_paper_iot_scene_library.py`
- Create: `figure_sources/paper_iot_scene_library/manifest.json`

- [ ] Add failing tests for 18 unique scenes, valid component references, 480×300 SVG outputs, 18 Draw.io entries, and a nonblank contact sheet.
- [ ] Run the focused test file with WSL-local temporary variables and confirm expected missing-artifact failures.
- [ ] Add the exact 18-scene manifest with 15 core and 3 optional scenes.

### Task 2: Implement scene composition

**Files:**
- Create: `figure_sources/build_paper_iot_scene_library.py`
- Create: `figure_sources/paper_iot_scene_library/scenes/*.svg`

- [ ] Reuse the base builder's validated SVG theming and data-URI functions.
- [ ] Render a light spatial base, component panels, solid/dashed connectors, arrowheads, and short badges from manifest data.
- [ ] Write 18 independent SVG scene assets without network access.

### Task 3: Build reusable outputs

**Files:**
- Create: `figure_sources/paper_iot_scene_library/paper-iot-scenes.xml`
- Create: `figures/paper_iot_scene_library_2026-07-10.svg`
- Create: `figures/paper_iot_scene_library_2026-07-10.png`
- Create: `figures/paper_iot_scene_library_2026-07-10.pdf`

- [ ] Encode all scene SVGs as local Draw.io library entries.
- [ ] Compose a six-column, three-row bilingual contact sheet.
- [ ] Export vector SVG/PDF and a 3600-pixel-wide PNG preview.

### Task 4: Review and document

**Files:**
- Create: `figure_sources/paper_iot_scene_library/README.md`
- Modify: `README.md`

- [ ] Inspect the full-resolution preview for object ambiguity, weak visual hierarchy, clipping, and label overlap.
- [ ] Document the scene meanings, reuse boundary, Draw.io import procedure, and non-AI provenance.
- [ ] Record actual commands, failures, corrections, output paths, and validation results.

### Task 5: Final verification

**Files:**
- Inspect: all generated assets and focused tests.

- [ ] Rebuild without network access and run the focused pytest file.
- [ ] Confirm 18 manifest scenes, 18 SVGs, 18 Draw.io entries, zero remote references, embedded PDF fonts, and clean Git whitespace.
- [ ] Confirm no TeX, experiment data, or existing Figure 1 asset changed.

