# Peak-Shaving Framework Draw.io Design

## Goal

Create an editable manuscript framework figure that explains the paper's
market model and simulation method without requiring the reader to infer the
meaning of channels, feedback loops, or solver outputs.

## Evidence logic

The figure should communicate one conclusion: time-of-use price shapes affect
QoS through user choice, intermediary routing, fixed GPU capacity, and the
routing--QoS fixed point; the numerical evidence is bounded by finite-grid
regret and does not establish a continuous-space equilibrium.

## Layout

The figure uses a landscape page with two full-width panels:

```text
+--------------------------------------------------------------------------+
| (a) Market and serving mechanism                                         |
| Workloads -> channel-period choice -> intermediary -> Provider A (G_A)   |
|                       |               \-> Provider B (G_B)                |
|                       +-> direct A / direct B / outside option            |
|       solid: requests and traffic   dashed: price, QoS, solver feedback  |
+--------------------------------------------------------------------------+
| (b) Simulation and finite-grid diagnostics                               |
| price grids -> intermediary response -> user choice -> routing-QoS FP    |
| -> payoff matrix -> fictitious play / double oracle -> evidence reported |
+--------------------------------------------------------------------------+
```

## Required content

- Time-rigid users: interactive requests and higher migration cost.
- Time-flexible users: scheduled or shiftable workloads.
- Four channel outcomes: API intermediary, direct Provider A, direct
  Provider B, and outside option.
- Provider A and Provider B choose wholesale and direct price shapes; their
  fixed capacities satisfy `G_A > G_B`.
- The intermediary selects a retail price and routes by wholesale price and
  QoS.
- Provider load produces utilization, and utilization maps to QoS.
- The simulation pipeline includes candidate grids, intermediary response,
  logit choice, joint routing--QoS fixed point, provider payoff matrix,
  fictitious play, and double-oracle diagnostics.
- The evidence block names finite-grid regret, QoS protection, and the profit
  boundary without claiming a production forecast or continuous-space Nash
  proof.

## Visual system

- Use only the locally stored Streamline Ultimate Color SVG family.
- Keep SVG icons embedded as vector data in the Draw.io source.
- Use Times New Roman for all labels.
- Use white panels, dark outlines, and restrained cyan, yellow, coral, and
  green accents sampled from the icons.
- Use solid arrows only for requests/traffic and dashed arrows only for price,
  QoS, or numerical feedback.
- Keep labels outside arrow paths and avoid decorative backgrounds, gradients,
  shadows, and 3D effects.

## Outputs

- Editable source: `figure_sources/peak_shaving_framework_2026-07-11.drawio`
- Reproducible builder: `figure_sources/build_peak_shaving_framework_drawio.py`
- Preview: `figures/peak_shaving_framework_2026-07-11.png`
- Vector exports: `figures/peak_shaving_framework_2026-07-11.svg` and `.pdf`

The first delivery is a reviewable draft. The English and Chinese TeX files
remain unchanged until the author approves the diagram.

## Acceptance criteria

- Draw.io structural validator reports zero errors and warnings.
- Required market and solver nodes are present exactly once.
- Every connector has a valid source, target, and geometry.
- At least 20 local SVG icons are embedded; no remote image references exist.
- Exported PNG is nonblank, at least 2400 pixels wide, and visually readable.
- SVG and PDF exports parse successfully; the PDF contains one cropped page.
- Visual inspection finds no clipped labels, node overlap, edge-label overlap,
  or ambiguous arrow semantics.
