# SMPT Figure File Inventory

Manuscript: `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`  
Release:
`https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`

## Figure Files

| Figure | Manuscript label | Upload file | Source / note |
|---:|---|---|---|
| 1 | `fig:market_schematic` | `figures/peak_shaving_diagnostics/market_schematic_iot_imagegen_2026-06-22.png` | IoT-style direct generated draft requested for author review; Draw.io backup source remains `market_schematic_drawio_exact_2026-06-21.drawio` |
| 2 | `fig:vllm_qos_anchor` | `figures/peak_shaving_submission/vllm_qos_anchor.pdf` | Controlled vLLM QoS-shape anchor |
| 3 | `fig:qos_profiles` | `figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf` | Congested utilization and QoS profiles |
| 4 | `fig:profit_regret` | `figures/peak_shaving_diagnostics/profit_components_and_regret.pdf` | Profit components and pure-snapshot regret |
| 5 | `fig:mixed_oracle` | `figures/peak_shaving_submission/mixed_oracle_regret.pdf` | Double-oracle finite-grid mixed diagnostic |
| 6 | `fig:parameter_sweep` | `figures/peak_shaving_submission/parameter_sweep_qos.pdf` | Nine-scenario parameter stress test |
| 7 | `fig:smpt_phase` | `figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf` and `figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf` | Two-panel fixed-policy phase grid assembled in LaTeX |
| 8 | `fig:mechanism` | `figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf` | Mechanism diagnostics |

## Audit Evidence

- Full figure audit: `docs/reviews/smpt_full_figure_audit_2026-06-21.md`.
- All eight figure labels are cited in the manuscript.
- Figures 2--8 use Times New Roman embedded in vector PDF files.
- Figure 1 currently uses a raster imagegen draft with IoT/edge, gateway,
  provider, direct-access, exit, and feedback elements added for author review.

## Submission Note

If the submission system requires one file per figure, upload the files listed
above. For Figure 7, upload both phase-grid PDFs and note that they form one
multi-panel figure in the manuscript.

Before formal Elsevier submission, Figure 1 needs an explicit artwork-policy
decision because the current active file is a generative-image draft. The safer
route is to use it as a visual guide and recreate/export an author-approved
vector or Draw.io artwork.
