# SMPT Full Figure Audit

> **Historical figure audit, superseded.** This report covers the old eight-
> figure manuscript and image-generated Figure 1. The current six-figure set
> remains an internal review artifact because its layout or plotting code
> received Codex assistance. Authors must independently rebuild Figures 1--6
> before submission; see `../submission/smpt_author_actions_2026-07-16.md`.

Date: 2026-06-21  
Manuscript: `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`  
PDF: `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`

## Scope

This audit checks all eight manuscript figures after the latest Figure 1 and
abstract revisions. The checks cover:

- figure numbering and in-text references;
- caption/content consistency;
- rendered PDF readability;
- source file existence;
- font embedding for vector figures;
- key numerical consistency against stored artifacts.

## Commands Used

```bash
pdftotext -layout peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_fig_audit_layout.txt
```

```bash
uv run python - <<'PY'
# Parse figure environments and labels from the TeX file.
# Render PDF pages containing figures through pdftoppm.
# Build tmp/figure_checks/current_smpt_figure_pages_contact_sheet_2026-06-21.png.
PY
```

```bash
pdffonts figures/peak_shaving_submission/vllm_qos_anchor.pdf
pdffonts figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf
pdffonts figures/peak_shaving_diagnostics/profit_components_and_regret.pdf
pdffonts figures/peak_shaving_submission/mixed_oracle_regret.pdf
pdffonts figures/peak_shaving_submission/parameter_sweep_qos.pdf
pdffonts figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf
pdffonts figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf
pdffonts figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf
```

## Figure Inventory

| Figure | Label | Source file(s) | PDF page | Role |
|---|---|---|---:|---|
| 1 | `fig:market_schematic` | `market_schematic_drawio_exact_2026-06-21.png` | 4 | Market structure and simulation workflow |
| 2 | `fig:vllm_qos_anchor` | `vllm_qos_anchor.pdf` | 10 | vLLM QoS-shape anchor |
| 3 | `fig:qos_profiles` | `qos_utilization_profiles.pdf` | 12 | Main QoS/utilization evidence |
| 4 | `fig:profit_regret` | `profit_components_and_regret.pdf` | 13 | Profit split and pure-snapshot regret boundary |
| 5 | `fig:mixed_oracle` | `mixed_oracle_regret.pdf` | 13 | Mixed finite-grid regret diagnostic |
| 6 | `fig:parameter_sweep` | `parameter_sweep_qos.pdf` | 15 | Nine-scenario parameter stress test |
| 7 | `fig:smpt_phase` | `smpt_phase_qos_gain.pdf`; `smpt_phase_profit_gain.pdf` | 16 | 25-point fixed-policy phase grid |
| 8 | `fig:mechanism` | `mechanism_diagnostics.pdf` | 17 | Mechanism diagnostics for surplus reallocation |

All eight figure labels are referenced in the manuscript text.

## Visual Review

| Figure | Visual result | Issues |
|---|---|---|
| 1 | The revised Draw.io-style schematic is readable in the compiled PDF. Users, API intermediary, providers, direct access, exit, fixed point, and finite-grid diagnostic are all visible. | No visible overlap. Submission risk remains: final journal artwork should be manually exported from Draw.io source rather than the earlier imagegen drafts. |
| 2 | Points, fitted curves, legend, and healthy boundary are readable. Caption states the measurement role and does not overclaim production calibration. | No visual issue. |
| 3 | Utilization and QoS panels are readable. The dashed threshold line is in the utilization panel and the caption correctly describes it as a utilization threshold where QoS degradation begins. | No visual issue. |
| 4 | Stacked profit bars and regret boundary panel are readable. Legend labels use Provider A/B rather than Firm A/B. | No visual issue. |
| 5 | Mixed-oracle regret line is readable, with the target line visible and not blocked. | No visual issue. |
| 6 | Both bar panels are readable; long scenario labels are compact but legible in the rendered PDF. | Minor style risk: x-axis labels are small, but still readable at A4 PDF size. |
| 7 | Heatmap values, axes, and color bars are readable. Caption clearly states fixed-policy scope and points to the restricted re-solve table. | No visual issue. |
| 8 | Four mechanism panels are readable; legend and grouped bars are clear. | No visual issue. |

## Font And Export Checks

- Vector PDF figures 2--8 embed `TimesNewRomanPSMT` as CID TrueType text.
- Figure 1 PNG was generated with Times New Roman font files and the `.drawio`
  source also uses `fontFamily=Times New Roman`.
- Figure 1 PNG dimensions: 1800 x 1080 RGB.
- Contact sheet for current PDF figure pages:
  `tmp/figure_checks/current_smpt_figure_pages_contact_sheet_2026-06-21.png`.

## Numerical Traceability

Key figure numbers match stored artifacts:

- Figure 2 uses `vllm_qos_anchor_summary.json` and `vllm_qos_anchor_points.csv`.
- Figure 3 uses `peak_shaving_time_profiles.csv`.
- Figure 4 and Figure 5 align with:
  - coarse regret below 5 after 22 rounds;
  - fine pure snapshot regret about 22.3 after 40 rounds;
  - mixed oracle final full-grid regret `0.20253154148201702`, reported as
    `0.203`;
  - mixed support `5 x 5`.
- Figure 6 aligns with `peak_shaving_parameter_sweep_summary.json`:
  - 9 scenarios;
  - QoS gain positive in 9/9 for both dynamic snapshots;
  - peak-utilization reduction positive in 9/9 for both dynamic snapshots;
  - minimum QoS gain `0.12626481590252547` for coarse and
    `0.12906940509820686` for fine.
- Figure 7 aligns with `smpt_phase_grid.csv`:
  - 25 rows;
  - positive QoS gains and peak-utilization reductions in the fixed-policy grid.
- Figure 8 aligns with `peak_shaving_mechanism_summary.csv` and
  `peak_shaving_parameter_sweep.csv`:
  - served volume `2610 -> 2865 / 3043`;
  - average paid price `0.761 -> 0.735 / 0.625`;
  - rigid exit probability `0.158 -> 0.145 / 0.119`;
  - elastic exit probability `0.087 -> 0.075 / 0.044`.

## Audit Judgment

No figure currently shows a blocking visual or numerical inconsistency in the
compiled PDF. The strongest remaining figure-related submission risk is Figure 1
artwork policy: it is conceptually aligned and editable as Draw.io, but the final
journal submission should use an author-approved Draw.io export and should not
use the earlier imagegen PNG drafts as final artwork.
