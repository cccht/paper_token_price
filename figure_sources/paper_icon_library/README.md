# Inference Pricing Paper Icon Library

This directory contains a curated IconPark library for the fixed-capacity
inference-pricing manuscript. It is a source collection for author-created
diagrams, not a new experimental result and not a reason to add entities that
are absent from the model.

## Contents

- `manifest.json`: 48 icon records with English and Chinese labels, manuscript
  meaning, source path, category, and priority.
- `upstream_svg/`: unchanged 48x48 SVG files from the pinned IconPark commit.
- `paper-icons.xml`: generated Draw.io custom library with local embedded SVGs.
- `LICENSE-APACHE-2.0.txt`: complete upstream licence.
- `MODIFICATIONS.md`: exact colour changes applied to generated derivatives.
- `../../figures/paper_icon_library_2026-07-10.svg`: vector contact sheet.
- `../../figures/paper_icon_library_2026-07-10.png`: review preview.
- `../../figures/paper_icon_library_2026-07-10.pdf`: printable contact sheet.

## Priority rule

- `core`: suitable for the main framework or a closely related method figure.
- `optional`: reserved for an applied IoT variant, supplementary workflow, or
  diagnostic diagram. Optional assets should not all appear in one figure.

The current manifest contains 30 core icons and 18 optional icons. The main
Figure 1 should use no more than the concepts needed to explain the model.
English preview labels use Times New Roman. Chinese labels use SimSun only as
a glyph fallback because Times New Roman does not contain Chinese characters.

## Draw.io use

In diagrams.net or Draw.io, choose **File > Open Library from > Device** and
select `paper-icons.xml`. Each item is an embedded SVG and does not require a
network request. The title contains both English and Chinese labels.

The library colours have fixed semantic roles:

| Category | Colour | Meaning |
|---|---|---|
| Market actors | `#24557A` | users, provider, intermediary, exit |
| LLM and IoT workloads | `#2A9D8F` | chat, code, agents, batch and optional devices |
| API and network flow | `#5B9BD5` | API, gateway, routing and switching |
| GPU serving and QoS | `#DE6B57` | compute, capacity, utilization, QoS and congestion |
| Pricing and market game | `#D49A16` | prices, demand shifting, transactions and profit |
| Simulation and verification | `#596579` | finite grids, fixed points, regret and checks |

Do not mix these assets with unrelated filled, isometric, photographic, or
cartoon icon families in the same manuscript figure.

## Rebuild

Run from the repository root:

```bash
uv run python figure_sources/build_paper_icon_library.py
```

The builder performs no download. It reads only the pinned SVG files already
stored in `upstream_svg/`.

## Source and licence

- Upstream: <https://github.com/bytedance/IconPark>
- Commit: `8dc132da4c85671ba6a5962c87aa2bdafbf158e9`
- SVG package metadata: `@icon-park/svg` 1.4.2
- Licence: Apache-2.0

Retain `LICENSE-APACHE-2.0.txt` and `MODIFICATIONS.md` when the editable asset
package is redistributed.
