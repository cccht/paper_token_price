# Inference Pricing IoT Scene Library

This directory contains 18 concrete, multi-object scene assets for the
fixed-capacity inference-pricing manuscript. The scenes are designed for
framework diagrams that need visible devices, API routing, server capacity,
QoS state, and simulation diagnostics rather than isolated interface glyphs.

## Provenance

The scenes are not generated with ImageGen or another generative image model.
They are programmatically composed from the local IconPark base library at
commit `8dc132da4c85671ba6a5962c87aa2bdafbf158e9`, together with original SVG
panels, spatial bases, arrows, badges, and layout. The IconPark components are
distributed under Apache-2.0; see the complete licence and modification record
in `../paper_icon_library/`.

The user-provided reference image was used only to identify broad visual
properties: coloured devices, multi-object scenes, light spatial depth,
directional arrows, and short labels. No icon or layout was copied from it.

## Contents

- `manifest.json`: scene meaning, priority, component IDs, coordinates,
  connectors, and short badges.
- `scenes/*.svg`: 18 independent 480x300 SVG assets.
- `paper-iot-scenes.xml`: Draw.io custom library with embedded local SVGs.
- `../../figures/paper_iot_scene_library_2026-07-10.svg`: vector contact sheet.
- `../../figures/paper_iot_scene_library_2026-07-10.png`: review preview.
- `../../figures/paper_iot_scene_library_2026-07-10.pdf`: printable contact sheet.

## Draw.io use

Choose **File > Open Library from > Device** in Draw.io or diagrams.net, then
select `paper-iot-scenes.xml`. The scenes can be used as complete visual
objects. Use the base library in `../paper_icon_library/paper-icons.xml` when
individual components are needed.

## Manuscript use

- Use the user endpoint, intermediary routing, Provider A/B cluster, direct
  channel, outside option, QoS feedback, and fixed-point scenes for Figure 1.
- Keep applied IoT endpoints and the generic request stream optional because
  the current experiment is not calibrated to a specific IoT deployment.
- Do not place all 18 scenes in one figure. A typical framework should use
  8-12 scenes and rely on arrows and labels for the remaining relationships.
- The scene assets do not change the model boundary, evidence, or claims.

## Rebuild

Run from the repository root:

```bash
TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run python \
  figure_sources/build_paper_iot_scene_library.py
```

The builder performs no download and reads only local SVG components.

