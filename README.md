# Token-Service Cross-Period Pricing

This repository contains the simulation code, single-GPU measurements, and
Chinese manuscript for a QoS-aware token-service pricing study.

## Directory Layout

```text
.
├── token_dynamic_pricing_game.tex/.pdf  # active full Chinese manuscript
├── token_dynamic_pricing_game_sci_main.tex/.pdf
│                                           # SCI-style compressed main draft
├── token_dynamic_pricing_game_supplement.tex/.pdf
│                                           # supplementary material draft
├── verified_refs.bib                    # active bibliography
├── experiments/                         # reproducible experiment entrypoints
├── pricing_sim/                         # pricing-game simulation modules
├── tests/                               # regression tests
├── artifacts/                           # generated experiment outputs
├── figures/                             # figures referenced by the manuscript
├── figures_multi/                       # generated multi-platform figures
├── manuscripts/                         # legacy and translated manuscript files
├── latex_aux/                           # LaTeX auxiliary files moved out of root
├── references/legacy/                   # older bibliography files
├── docs/reviews/                        # manuscript review reports
├── figure_sources/                      # PPT/diagram source files
├── paper_rewriting_output/              # PaperSpine audit and traceability files
├── notes/                               # design notes and writing notes
└── YYYY-MM-DD/                          # dated manuscript snapshot folders
```

Keep the active manuscript and active bibliography in the project root. Put
experiment entrypoints in `experiments/`, generated LaTeX intermediates in
`latex_aux/`, old drafts in `manuscripts/`, review records in `docs/reviews/`,
and dated snapshots under `YYYY-MM-DD/`.

## Organization Record

### 2026-06-06

- Created an in-project dated archive workflow with
  `archive_daily_snapshot.py`.
- Created dated manuscript snapshots under `2026-06-06/snapshots/`.
- Moved legacy manuscript drafts and translated drafts into `manuscripts/`.
- Moved LaTeX auxiliary files and older build outputs into `latex_aux/`.
- Moved older bibliography files into `references/legacy/`.
- Moved manuscript review reports into `docs/reviews/`.
- Moved writing notes into `notes/`.
- Moved PPT, PowerShell, and Python figure source files into
  `figure_sources/`.
- Moved experiment and plotting entrypoints from the project root into
  `experiments/`.
- Updated experiment entrypoints so their default outputs still write under
  root-level `artifacts/`.
- Updated manuscript, README, benchmark docs, and targeted tests to reference
  the new `experiments/` paths.
- Updated the daily snapshot script so future snapshots include review records,
  benchmark docs, `archive_daily_snapshot.py`, `experiments/*.py`, `tests/*.py`,
  and reviewer-strengthening CSV/JSON artifacts.
- Added the PaperSpine-style manuscript audit report at
  `docs/reviews/paperspine_review_2026-06-06.md`.
- Added reviewer-strengthening sensitivity experiments for user-protection
  price caps and direct API price-capacity settings.
- Added calibration-uncertainty experiments, a parameter-source audit, and a
  measured-QoS fixed-capacity stress baseline.
- Updated the daily snapshot workflow to preserve calibration-uncertainty
  CSV/JSON artifacts together with manuscript-referenced figures.
- Added lightweight PaperSpine `source_map.md`, `evidence_bank.md`,
  `citation_support_bank.md`, `section_blueprints.md`,
  `writing_rationale_matrix.md`, `original_logic_map.md`, `rewrite_matrix.md`,
  and `logic_transfer_audit.md` traceability artifacts under
  `paper_rewriting_output/`.
- Added a PaperSpine final-paper mirror under
  `paper_rewriting_output/final_paper/` for audit tooling. The root manuscript
  remains the active source of truth.
- Updated the daily snapshot workflow to preserve nested PaperSpine markdown,
  JSON, LaTeX, BibTeX, and PDF traceability artifacts.

Root is now reserved for the active manuscript, active bibliography,
dependency file, project README, and snapshot utility.

### 2026-06-07

- Added the PaperSpine round-5 review report at
  `docs/reviews/paperspine_review_round5_2026-06-07.md`.
- Revised the active manuscript after the round-5 review without adding new
  experiment data.
- Tightened the abstract, narrowed the related-work gap, grouped the
  experiment narrative by evidence strength, and made the conclusion explicitly
  conditional on protected prices, sufficient direct capacity, and calibrated
  deployment data.
- Synchronized the PaperSpine final-paper mirror with the active manuscript.

### 2026-06-08

- Revised the active manuscript and simulation code in response to a strict
  reviewer critique on theory-experiment alignment.
- Replaced the aggregate migration-cost shortcut with a native-period
  distribution `native_period_distribution`, matching the paper's
  `\pi_t` formulation.
- Added a congestion-proxy no-QoS baseline so the comparison no longer treats
  congestion awareness as an all-or-nothing advantage.
- Increased middle-stage best-response sweeps and reran the main, SCI
  supplemental, realism, direct-API sensitivity, reviewer-response, and
  calibration-uncertainty experiment groups.
- Updated manuscript tables, discussion, conclusion, and artifact paths to the
  2026-06-08 rerun outputs.
- Added a SCI-style compressed main draft,
  `token_dynamic_pricing_game_sci_main.tex`, while keeping
  `token_dynamic_pricing_game.tex` as the full active source.
- Added `token_dynamic_pricing_game_supplement.tex` to preserve detailed
  simulation parameters, mechanism diagnostics, robustness sweeps, user
  protection, direct API sensitivity, calibration uncertainty, and measured-QoS
  stress evidence moved out of the compressed main draft.
- Updated `archive_daily_snapshot.py` so dated snapshots preserve the full
  manuscript, SCI main draft, supplement draft, their compiled PDFs, and figures
  referenced by any of the three TeX sources.
- Corrected the convergence-diagnostic paragraph in both the full manuscript
  and the compressed SCI draft so the reported objective evaluations, response
  rounds, regret values, and single-intermediary utilization match the 2026-06-08
  experiment artifacts.
- Revised `token_dynamic_pricing_game_sci_main.tex` against
  `review_report.md`: repositioned the theory around solver-based
  epsilon-Nash candidate responses, moved the inclusive-value drop into the
  main result narrative, contextualized the 93.92% gain against the weaker
  uniform baseline, added a QoS-threshold explanation, and strengthened
  cross-disciplinary readability and single-platform limitations.
- Added local review-response tracking at
  `docs/reviews/sci_main_review_response_check_2026-06-08.md`.
- Recorded the attempted `opencode` DeepSeekv4pro review and tool-side failure
  at `docs/reviews/deepseekv4pro_opencode_attempt_2026-06-08.md`.
- Completed the requested DeepSeek v4 review through
  `opencode-go/deepseek-v4-pro` and saved it as
  `docs/reviews/deepseekv4pro_opencodego_review_2026-06-08.md`.
- Added the follow-up response checklist at
  `docs/reviews/deepseekv4pro_response_check_2026-06-08.md`.
- Revised `token_dynamic_pricing_game_sci_main.tex` again after that review:
  platform-level optimization is now framed as candidate-set revenue ranking,
  the 13.61% QoS-aware increment is the primary result, 93.92% is explicitly a
  weak-baseline diagnostic, the QoS mechanism is described as threshold-type
  congestion control under the current function, the welfare table includes a
  diagnostic no-purchase probability, and public DeepSeek/OpenAI API prices are
  added only as a scale check rather than economic calibration.
- Created dated snapshots under `2026-06-08/snapshots/`.

### 2026-06-17 — Paper Polish & Figure Overhaul

- Replaced the four framework/schematic figures (Figures 1--4) with new
  versions from `ppt2pdf/`:
  * Figure 1 `three_layer_game_framework.pdf` ← `ppt2pdf/论文图.pages_3.pdf`
  * Figure 2 `api_market_topology.pdf` ← `ppt2pdf/论文图.pages_7.pdf`
  * Figure 3 `information_interaction.pdf` ← `ppt2pdf/论文图.pages_10.pdf`
  * Figure 4 `fixed_point_candidate_response.pdf` ← `ppt2pdf/论文图.pages_13.pdf`
- All four replacement PDFs were processed through `gs -dNoOutputFonts` to
  convert text to vector outlines, eliminating the CambriaMath mathematical
  symbol garbled-text issue that occurred when `xdvipdfmx` embedded the original
  font subsets.
- **Full manuscript humanization pass** — systematically removed AI-generated
  writing traces throughout the entire SCI main draft:
  * Replaced unnatural section heads: `机制直觉` → `机制说明`,
    `跨市场类比` → `与电力定价的类比`, `跨层二层基准` → `二层集中优化参照`,
    `有效性威胁` → `局限与注意事项`.
  * Removed AI-favored filler verbs and adverbs: `呈现` (present/morph),
    `构成了` (constitutes), `显著的` (significant), `明显` (obvious),
    `天然` (naturally), `随之产生` (emerged), `展现出` (revealed).
  * Removed AI meta-discourse markers: `需要强调的是`, `换言之`,
    `综合来看`, `进一步地`, `具体而言`, `系统研究表明`, `{现实意义：}`.
  * Replaced template sentence structures: `除A之外，另一个B是C`,
    `基于...视角...核心思想是`, `将A、B和C结合`.
  * Replaced `→` arrow chains with proper Chinese prose (e.g.,
    `批发价格→零售价格→...→利润` → `批发价格、零售价...直至利润`).
  * Tightened the abstract, introduction, problem description, contribution
    list, model description, discussion, and conclusion.
- **Figure caption trimming** — shortened all 20 figure captions to single-line
  titles. Descriptive content was already present in the surrounding body text
  and was deletable redundancy.
- **Figure 9 legend fix** — moved the legends in subpanels (a) and (c) of
  `three_layer_policy_detail` from the default top-left to below the plot area
  (`loc="upper center", bbox_to_anchor=(0.5, -0.18)`), regenerated via
  `experiments/pub_figures.py::plot_policy_detail()`.
- **GPT2Image prompt** — wrote a detailed diagram-generation prompt for
  Figure 4 (`fixed_point_candidate_response`) and saved it at
  `docs/gpt2image_prompt_fixed_point_candidate_response.md`.
- Compiled and verified: 34 pages, zero errors (only harmless PDF 1.7 version
  warnings from the three included vector figures).

- Added two-layer game baselines (`pricing_sim/two_layer_game.py`) for
  cross-layer comparison: Liu-inspired centralized dispatch and Yan-inspired
  two-layer Stackelberg (platform → users, no intermediaries).
- Added comparison experiment entrypoint
  (`experiments/run_two_layer_comparison.py`).
- Removed the public API price comparison table (Table 8) from the SCI main
  draft; the quantity-of-magnitude check is kept as a one-sentence note.
- Removed the experiment-file listing from Section 5.1 and replaced it with a
  cross-reference to the code-availability section.
- Fixed Figure 2 (three-layer policy detail):
  * First subplot: distinguished three retail-price lines with distinct colors
    (red/green/orange), markers (circle/triangle/diamond), and ±0.03 vertical
    offsets to prevent visual collapse.
  * Third subplot: added a twin-axis showing peak utilization (red) alongside
    QoS floor (green), with reference lines for the QoS threshold.
- Rewrote the abstract with three structured quantitative claims matching the
  two-layer and three-layer experiments.
- Rewrote the conclusion to align with the abstract: three-group result
  structure, consistent numbers, and a shared core insight about
  intermediaries as carriers of price discrimination, congestion control,
  and market coverage.
- Reran the full experiment (`--full`), cross-checked every table number
  against the fresh run, and corrected four stale values:
  * Fixed-point iterations: 31→33 (uniform), 30→32 (no-QoS), 3→2 (3L QoS).
  * Average retail prices in the welfare-diagnostics table and discussion
    text: 1.4926→1.5339 (no-QoS), 1.4852→1.6707 (3L QoS-aware).
- Updated artifact figures under `artifacts/intermediary/20260608-144953/`
  with the full-run regenerated plots.
- Updated this README with the current active-manuscript build command and
  the 2026-06-10 changelog.
- Translated the full SCI main draft into English and saved as
  `token_dynamic_pricing_game_sci_main_en.tex`. The English version uses the
  standard `article` class (submitters can switch to `elsarticle` for EJOR).
  Both Chinese and English versions share the same data, structure, and
  quantitative claims.
- Restored the Chinese version as the active `token_dynamic_pricing_game_sci_main.tex`
  after the English translation; all today's fixes (abstract, conclusion,
  convergence numbers, average retail prices, deleted API-price table, deleted
  experiment-file list) were reapplied to the restored Chinese source.
- Updated the manuscript-build section to document both Chinese and English
  compilation commands.
- Created a pre-edit dated backup snapshot under
  `2026-06-10/snapshots/182013/`.
- Added `experiments/build_reference_aligned_figures.py` to generate
  reference-aligned SCI main figures from existing CSV/JSON artifacts.
- Added generated PDF/SVG figures under `figures/reference_aligned/`.
- Expanded `token_dynamic_pricing_game_sci_main.tex` from 2 to 20 figure
  environments, matching the reference paper's figure count while keeping all
  numeric claims tied to existing experiment artifacts.
- Completed an opencode-go DeepSeek v4 Pro review of the reference-aligned
  figure revision and saved it at
  `docs/reviews/opencodego_reference_figures_review_2026-06-10.md`.
- Fixed the review's high-risk consistency issues in the SCI main draft:
  explicitly tabulated the two-layer centralized baseline behind the 4519.28
  value, revised the abstract/conclusion to +110.8%, moved manuscript figures
  into `figures/reference_aligned/`, added direct-API share/demand equations,
  and changed revision-history wording to neutral manuscript wording.
- Replaced SCI main Figure 2 and Figure 3 with Mermaid-rendered PNG assets:
  `figures/reference_aligned/information_interaction_mermaid.png` and
  `figures/reference_aligned/api_market_topology_mermaid.png`. The batch
  figure script no longer regenerates the old Matplotlib box diagrams for
  these two positions.
- Completed an `opencode-go/deepseek-v4-pro` review of the Mermaid Figure 2/3
  replacement and saved it at
  `docs/reviews/opencodego_mermaid_fig2_fig3_review_2026-06-10.md`. The review
  fixes were applied by marking upstream API supply as exogenous, removing the
  incorrect platform quota-allocation wording, routing QoS feedback through
  user utility, and recording the Mermaid CLI render commands.

## CPU Reproducibility Bundle

Create a Python environment and install the CPU-side dependencies:

```powershell
python -m pip install -r requirements.txt
```

Run the economic simulation, supplemental experiments, calibration-uncertainty
checks, and test suite:

```powershell
python .\experiments\run_reproducibility_bundle.py
```

Use `--smoke` for a fast pipeline check with reduced trials and optimizer
iterations. The full command writes a timestamped bundle under
`artifacts/reproducibility`.

### 2026-06-18 — Corrected manuscript + new peak-shaving track

**(A) Corrected SCI main draft** `token_dynamic_pricing_game_sci_main_2026-06-18.tex/.pdf`
(18 pages, compiles clean). Fixes two modeling defects found in adversarial
review and re-runs all affected numbers:

- **M1 rigid-demand J-scaling fix.** The rigid/replay arrival term previously
  multiplied each intermediary by the whole-period aggregate share
  (`sum_k s[k,t]`), so total demand grew ~linearly with the number of
  intermediaries J. Corrected to per-channel own share. Effect: the earlier
  "more intermediaries → higher profit" result vanishes (uniform-retail J=3
  system profit 4911.97 → 2308.55, equal to J=1); QoS-aware gain at baseline
  demand falls from the headline +13.61% to +0.32%.
- **M3 outside-option fix.** User choice previously normalized over inside
  options only, so negative utilities never shed demand even while the paper
  reported a 62.69% "exit probability" (two mutually exclusive models). Added a
  no-purchase outside option so profit, inclusive value, and exit probability
  live in one consistent model.
- New corrected results (all re-run, real): QoS-awareness gain is **conditional**
  — ~+0.3% at baseline (uncongested) but +9.3%–+14.5% once demand scaling
  ρ≥1.3 pushes utilization toward capacity; price-protection contract yields a
  clean win-win (platform revenue 1501→1921, inclusive value 1.57→2.28, exit
  20.7%→10.2%).
- Switchable corrected simulator `pricing_sim/fixed_market.py` (fixes are
  independent on/off switches); fidelity check reproduces the original
  artifacts bit-for-bit when all switches are off.
- Experiment entrypoints: `experiments/run_reviewer_fixed_experiments.py`
  (baselines RAW/M1/M1+M3, smooth-QoS shapes) and
  `experiments/run_reviewer_fixed_regime.py` (demand-scale sweep, welfare
  tension). Artifacts under `artifacts/reviewer_fixed/20260618/`.
- Design + plan docs: `docs/superpowers/specs/2026-06-18-peak-shaving-dynamic-pricing-design.md`
  is the next-paper spec; the corrected-manuscript rationale is recorded in this
  changelog.

**(B) New peak-shaving dynamic-pricing track** (next paper, multi-firm).
Goal: with fixed GPU capacity, can time-of-day dynamic pricing migrate
time-elastic load from peak to off-peak. Two heterogeneous firms (large A=1500,
small B=600) deploying the same open-source model, one routing intermediary,
two user types (time-rigid vs time-elastic) with a no-purchase outside option.

- Modules:
  * `pricing_sim/peak_shaving_config.py` — two user types + heterogeneous firms.
  * `pricing_sim/peak_shaving_market.py` — two-type logit with outside option,
    corrected-allocation demand, firm-load QoS congestion fixed point, firm
    profit with idle cost (`c_g * G_m`, charged on fixed capacity), intermediary
    profit.
  * `pricing_sim/peak_shaving_equilibrium.py` — low-dim shape parameterization
    (each firm = 4 scalars: `wbar, delta, pdbar, delta_d`), logit routing,
    intermediary best response, M=2 firm Nash via damped best-response
    (damping=0.7). Firm and intermediary best-responses use coarse GRID search
    (see solver architecture note below), not gradient/Powell.
- Experiments: `experiments/run_peak_shaving_experiments.py` (uncongested P1–P5),
  `experiments/run_peak_shaving_congested.py` (congested regime), and
  `experiments/run_peak_shaving_robustness.py` (QoS shapes, u0, cross-seed).
  Artifacts under `artifacts/peak_shaving/20260618/`.
- Tests: `tests/test_peak_shaving_market.py` (10) and
  `tests/test_peak_shaving_equilibrium.py` (7); all 17 pass.
- **Reproducibility (the prior versions' failure point) is solved.** With the
  grid solver the equilibrium is fully deterministic: cross-seed system-profit
  rel_std = **0.000000** (three seeds give 1139.40 identically), versus ±9% in
  prior versions. (An earlier Powell-based solver already reached rel_std=0.0004;
  the grid makes it exact.)
- **Uncongested-regime findings (grid solver, real output).** **P1 HOLDS and is
  robust**: elastic load migrates ~2.3x more than rigid (centroid shift +0.177 vs
  +0.077). But dynamic pricing does NOT raise profit here — at the grid optimum it
  is profit-neutral at zero elastic share (gain +0.00% at pe=0, which correctly
  resolves a Powell-era artifact that had shown a spurious +3.35%) and slightly
  *negative* as elastic share rises (pe=0.2/0.4/0.6/0.8 → -0.32%/-4.51%/-3.76%/
  -3.00%). **This reverses the earlier Powell-based "P5 gain rises with elastic
  share" claim, which was an optimizer artifact — recorded here as a correction.**
  P4 (small firm more dynamic) is indistinguishable at grid resolution
  (δ_A=δ_B=0.1995).
- **Honest note on the uncongested baseline:** peak utilization is only ~0.21–0.26,
  so the market is not congested and QoS≈1 regardless; peak-shaving/QoS effects
  are necessarily small here. The congested regime below is where the mechanism
  actually bites.
- **Congested-regime experiment (`experiments/run_peak_shaving_congested.py`,
  G=(300,120), sigmoid QoS, pop_elastic=0.6).** Calibration confirmed this
  capacity activates QoS degradation (uniform-pricing min QoS ~0.98 and peak
  utilization ~0.85). The congestion mechanism is now genuinely exercised, unlike
  the uncongested baseline.
- **Solver architecture fix (resolves the earlier congested-regime intractability).**
  The original nested-optimizer design (firm Powell over 4 scalars → intermediary
  Powell over 3 scalars → a routing loop that ran a *full* QoS fixed point inside
  each of 12 routing sweeps) compounded badly under congestion and timed out.
  Two changes fixed it: (1) `_solve_with_routing` now solves QoS and routing in
  ONE joint damped fixed point (~0.004s/call) instead of 12 nested full solves;
  (2) both `_firm_best_response` (3^4 grid) and `intermediary_best_response`
  (3x3x2 grid) are now coarse GRID searches rather than Powell/L-BFGS-B — bounded,
  predictable, parallel-friendly, and robust to the non-smooth QoS objective. A
  single congested firm best-response went from >115s (timeout) to ~18s. Task-7
  routing/best-response unit tests still pass.
- **Congested-regime findings — coarse vs refined Nash (IMPORTANT caveat).**
  * Coarse run (`peak_shaving_congested.py`, 3^4 firm grid, max_sweeps=3):
    appeared to show P2 (dynamic peak util 0.781 < uniform 0.853) and P3 (dynamic
    min QoS 1.000 > uniform 0.984) holding, with dynamic pricing lowering profit
    ~3.6%.
  * **Refined run (`peak_shaving_congested_refined.py`, delta/delta_d at 5 levels,
    max_sweeps=6) REVERSES this and exposes a non-convergence.** The dynamic-pricing
    firm Nash does NOT converge in the congested regime — best responses limit-cycle
    (sweep-to-sweep change oscillates 0.04→0.27→0.08→0.28, never < 3e-3). The
    "dynamic" iterate reported is therefore not an equilibrium, and at this
    resolution P2/P3 read False (dynamic peak util 0.711 > uniform 0.617; dynamic
    min QoS 0.964 < uniform 0.998). **Conclusion: the coarse run's P2/P3 "holds" was
    a grid artifact that masked the oscillation. The congested-regime equilibrium is
    currently NOT reliably solved.** Profit gain (−8.6%) and P1/P4 are likewise not
    trustworthy until convergence is achieved.
  * **This is the honest state**: the UNCONGESTED regime is fully solved
    (deterministic, rel_std=0, P1 robust, dynamic pricing profit-neutral-to-negative).
    The CONGESTED regime activates the QoS mechanism but the firm Nash limit-cycles
    at fine resolution — it needs either much stronger damping, many more sweeps
    (each ~100s here, so a converged run is a multi-hour job), or a different
    equilibrium solver (e.g. fictitious play with averaging, or a VI/complementarity
    formulation). Recorded as a scoped open problem, NOT masked.
  * Artifacts: `artifacts/peak_shaving/20260618/peak_shaving_congested.json`
    (coarse) and `peak_shaving_congested_refined.json` (refined, non-converged).
- **Fictitious-play solver resolves the limit cycle**
  (`experiments/run_peak_shaving_congested_fp.py`,
  `peak_shaving_congested_fp.json`). Replacing naive damped best-response with
  continuous fictitious play (each firm best-responds to the OTHER firm's running-
  AVERAGE strategy) damps the cycle: per-round change decays 0.225→0.075→0.038→…
  monotonically instead of oscillating 0.04→0.27→0.08→0.28. This is the correct
  equilibrium solver for this pricing game.
  * **With FP the congested regime is a WIN-WIN, reversing the naive-solver story.**
    P2 HOLDS (dynamic peak util 0.696 < uniform 0.782); P3 HOLDS (dynamic min QoS
    0.977 > uniform 0.757 — uniform pricing is genuinely congested here); P1 HOLDS
    (elastic shift +0.054 > rigid +0.045); and dynamic pricing RAISES system profit
    +10.2% (1964 vs 1783). When uniform pricing leaves the market badly congested
    (QoS 0.76), time-of-day dynamic pricing both protects QoS and earns more.
  * **Honest caveats**: (a) the uniform FP run converged (round-10 change 0.004) but
    the dynamic FP run did not fully converge (round-10 change 0.023, a mild residual
    wobble) — results are reported on the FP time-average (the standard FP solution
    object) but are approximate; (b) **P4 still fails and in the opposite direction**
    (δ_B=0.097 < δ_A=0.364) — the small firm uses *less* dynamic pricing here, so the
    "small firm more dynamic" hypothesis should be dropped or rethought, not claimed.
  * **Dynamic FP pushed to full convergence** (`run_fp_dynamic_converge.py`,
    regret-based stopping + per-round checkpointing, `peak_shaving_fp_dynamic_converged.json`).
    Using a regret criterion (max single-firm deviation gain from the time-average)
    instead of parameter drift, the dynamic equilibrium converges monotonically:
    max regret 133.6→63.7→43.6→…→4.98 over 22 rounds (CONVERGED at regret<5.0). The
    converged numbers confirm the win-win and sharpen the predictions:
    - System profit **1948.8 vs uniform 1783.2 → +9.3%** (win-win confirmed at a
      converged equilibrium, not just the time-average snapshot).
    - **P2 HOLDS**: dynamic peak util 0.706 < uniform 0.782.
    - **P3 HOLDS**: dynamic min QoS 0.968 vs uniform 0.756.
    - **P1 is weak at convergence**: elastic centroid 4.323 ≈ rigid centroid 4.374
      (shift difference negligible) — in the congested equilibrium the load-migration
      asymmetry essentially washes out, unlike the uncongested regime where it is
      robust. Report P1 as regime-dependent, not universal.
    - **P4 is decisively REJECTED and reversed**: at convergence δ_A=0.383 ≫
      δ_B=0.023 — the LARGE firm uses far more dynamic pricing, the small firm almost
      none. The "small firm more dynamic" hypothesis is false; the defensible
      finding is the opposite (large firm leads dynamic pricing).
  * **Grid-resolution robustness check (`FP_TAG=fine`, 3x5x3x5=225-point grid,
    resumable via checkpoint; `peak_shaving_fp_dynamic_fine_plateau.json`).** Re-running
    the dynamic FP at finer resolution overturns two of the coarse claims and confirms
    two:
    - **P2 (peak-shaving) ROBUST**: fine peak util 0.666 < uniform 0.782 (coarse 0.706).
    - **P3 (QoS protection) ROBUST**: fine min QoS 0.990 > uniform 0.756 (coarse 0.968).
    - **Profit gain NOT robust — the +9.3% does not survive.** Fine-grid profit is
      1749 vs uniform 1783 = **-1.9%** (coarse said +9.3%). The headline profit number
      flips sign with grid resolution, so dynamic pricing is best described as
      **near-profit-neutral**, not a profit win. The earlier "+10.2%/+9.3% win-win"
      was partly a coarse-grid artifact.
    - **P4 NOT robust — direction flips.** Fine grid gives δ_A=0.059, δ_B=0.278 (small
      firm more dynamic), the OPPOSITE of the coarse grid's δ_A≫δ_B. P4 must be dropped
      entirely in either direction; it is a grid artifact.
    - **The fine-grid FP did NOT converge (UPDATED after the full 40-round run).**
      Regret bottomed at ~14 around round 10, then DRIFTED UP to ~22 by round 40 — it
      never reached the <5 target and is diverging/plateauing high, not converging. So
      the coarse "regret 4.98 converged" was a coarse-grid artifact, and the congested
      equilibrium is NOT reliably solvable within this solver budget at fine resolution.
      Consequence: the congested-regime QUANTITATIVE numbers (profit, which firm is more
      dynamic) are untrustworthy; only the QUALITATIVE QoS-protection direction (peak
      shaved, min QoS lifted) holds across both grids. Reliable congested-equilibrium
      solving (stronger averaging, a VI/complementarity reformulation, or a much larger
      convergence budget) is required future work. Artifact:
      `peak_shaving_fp_dynamic_converged_fine.json` (a 40-round non-converged snapshot)
      and `peak_shaving_fp_dynamic_fine_plateau.json`.
- **HONEST combined story across regimes (after grid-robustness testing):** the
  ONLY resolution-robust claim is that time-of-day dynamic pricing **protects QoS
  under congestion** — both coarse and fine FP grids agree dynamic pricing shaves
  the peak (util 0.78→0.66-0.71) and lifts min QoS (0.76→0.97-0.99). Everything else
  is weaker than it first looked: the profit effect is **near-neutral** (coarse +9.3%,
  fine -1.9% (non-converged) — sign flips with resolution, so NOT a profit win); P1 (elastic migrates
  more) is robust uncongested but washes out at the congested equilibrium; P4
  (which firm is more dynamic) flips direction with grid resolution and must be
  dropped. The defensible paper claim is narrow and honest: **dynamic peak-shaving
  pricing is a reliable QoS-protection tool under congestion, at roughly neutral
  profit — not a profit-raising mechanism.** This is far less than the original
  hoped-for headline, but it is what survives adversarial robustness testing. The
  remaining work (finer-converged congested FP, a cleaner congested P1 probe, and a
  proper profit confidence interval across grids/seeds) would sharpen — but is
  unlikely to overturn — this QoS-protection-but-profit-neutral conclusion.
- **Progress + problem report and discussion draft written** for negotiator review:
  * `docs/进展与问题报告_2026-06-18.md` — full session history (审稿 → corrected
    manuscript → peak-shaving line), the five core problems (solver convergence,
    conclusion-flips-under-scrutiny, synthetic params, environment task-reaping,
    wrong P4 hypothesis), publishability assessment, and four open decisions.
  * `docs/削峰填谷_利润打平机制_discussion草稿.md` — Discussion-section draft
    explaining WHY profit is neutral: dynamic pricing redistributes surplus (peak
    price-up gains offset by demand driven away; trough discount volume offset by
    thin margins) rather than creating it; under fixed capacity + competition +
    exit options the QoS-improvement surplus flows to users, not firm profit. Framed
    as a policy-relevant finding (dynamic pricing is a QoS-protection tool, not a
    profiteering tool), not a negative result. To be folded into the peak-shaving
    paper's Discussion when that manuscript is drafted.
- **Peak-shaving manuscript drafted** (`peak_shaving_dynamic_pricing_2026-06-18.tex/.pdf`,
  8 pages, compiles clean: 0 undefined citations, 0 unresolved cross-refs). This is a
  NEW standalone paper for the multi-firm peak-shaving line (distinct from the
  three-layer-intermediary corrected manuscript). It writes up the honest,
  robustness-tested results: the model (heterogeneous two firms + routing
  intermediary + two user types + exit option + idle cost), the fictitious-play
  solver that resolved the limit cycle, the uncongested (P1 robust, profit neutral)
  and congested (QoS protection robust across grids, profit near-neutral with
  sign-flip) results, the "why profit breaks even" surplus-redistribution mechanism
  as the Discussion, and honest limitations (synthetic params, fine-grid FP not fully
  converged, dropped P4). All numbers trace to `artifacts/peak_shaving/20260618/`.

### 2026-06-19 — Peak-shaving final draft (humanized) + readiness assessment

No new experiments were run this day. Work was on the manuscript text and a critical
self-review. All numerical claims continue to trace to `artifacts/peak_shaving/20260618/`.

- **Final draft created**: `peak_shaving_dynamic_pricing_2026-06-19.tex/.pdf` (8 pages,
  compiles clean, 27 key numbers verified byte-identical to the 0618 source). Built from
  the 0618 manuscript, which already carries the corrected fine-grid FP numbers (the
  full 40-round run that showed non-convergence: regret bottomed ~14 at round 10 then
  drifted to ~22; congested fine-grid profit -1.9%, not the earlier -1.2% snapshot).
- **Full humanization (de-AI) pass** using the `humanizer` skill on every prose section
  (abstract, intro, model, solver, results, discussion, limitations, conclusion). Changes
  are STYLE ONLY — every number, conclusion, and honest caveat is preserved unchanged:
  * Cut em-dash (`——`) usage from ~15 to single digits.
  * Broke up mechanical parallelisms ("正向:…负向:…", "第一/第二/第三" enumerations) and
    formulaic closers ("这一发现与…预期相反，具有…含义").
  * Varied sentence rhythm; added measured first-person ("一开始我们猜…只能撤掉") for a
    researcher-thinking voice without sacrificing academic register.
  * Verified post-edit: all 27 key figures present, 5 honesty markers (未收敛/不作生产预测/
    靠不住/撤掉/被撤回) retained, LaTeX still compiles (exit 0).
- **Readiness assessment (recorded for the next work session).** Verdict: good as an honest,
  clean working draft; NOT yet submission-ready. Text is done; the scientific skeleton has
  three substantive gaps:
  * **Theory — too thin, one concept imprecise.** No formal proposition/proof anywhere
    (the three-layer paper had two). Two fixes identified: (a) formalize "profit breaks
    even" via an envelope-theorem first-order-effect-is-zero proposition under fixed
    capacity + fixed total demand; (b) **the congested limit cycle is most likely the
    signature of NO pure-strategy Nash equilibrium, i.e. a mixed-strategy equilibrium** —
    so the fictitious-play time-average should be reported as the marginal of a mixed
    equilibrium with exploitability (not parameter drift) as the convergence test. This
    REFRAMES the biggest weakness (non-convergence) into a self-consistent theoretical
    finding and is the single highest-value change.
  * **Method — the grid oracle is the weak point.** Regret magnitude depends on grid
    density (coarse 4.98 hid deviations the fine grid exposed at 22), so regret is not a
    resolution-independent number. Also the "QoS protection is robust" claim is mildly
    over-stated: both sides being compared are non-converged points, so it stands on the
    same shaky ground as the profit claim, just happens to agree in direction across two
    grids. And cross-parameter sensitivity (α, c_s, c_g) in the congested regime is still
    untested.
  * **Conclusion — lighter after honesty pass.** Of P1–P5 only the QoS-protection
    direction survives; the headline ("dynamic pricing doesn't profiteer") leans on the
    strong fixed-total-demand assumption; no real-data anchor (could pin 1–2 params to
    public DeepSeek/GLM API prices).
  * Priority order for next session: (1) reframe congested regime as mixed-strategy
    equilibrium w/ exploitability — highest value; (2) add the envelope-theorem
    proposition for profit-neutrality; (3) stop calling the QoS result uniquely "robust";
    (4) one congested-regime economic-parameter sweep; (5) real-price anchor.

- **Nature-style reviewer assessment by Codex (2026-06-19 13:45 CST).** Review-only
  pass using the local `nature-reviewer` and `ml-paper-writing` skills. No experiments,
  tests, or LaTeX compilation were run. Inputs reviewed: this README, the 0619
  peak-shaving TeX draft, compiled bibliography output, selected 20260618 JSON
  artifacts, and the peak-shaving model / solver / experiment code.
  * Commands:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl && pwd && uname -a || true && git rev-parse --show-toplevel 2>/dev/null || true && git status --short 2>/dev/null || true && command -v uv || true && uv --version || true'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && nl -ba peak_shaving_dynamic_pricing_2026-06-19.tex | sed -n "1,140p"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && nl -ba peak_shaving_dynamic_pricing_2026-06-19.tex | sed -n "141,280p"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && jq "." artifacts/peak_shaving/20260618/peak_shaving_summary.json | sed -n "1,220p"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && jq "." artifacts/peak_shaving/20260618/peak_shaving_fp_dynamic_converged_fine.json | sed -n "1,260p"'
    ```
  * Output: `docs/reviews/codex_nature_style_peak_shaving_review_2026-06-19.md`.
  * Result: the review agrees the topic and honesty are strong, but flags four
    submission-blocking issues: congested-regime QoS evidence still depends on
    non-converged / resolution-sensitive equilibrium objects; the utility equation
    and implementation need to be aligned; the profit-neutral mechanism needs a
    formal or diagnostic basis because demand is not strictly fixed in the code; and
    the peak-shaving paper needs a parameter / reproducibility supplement plus
    convergence and welfare diagnostics.
  * Status: recorded.

- **Optimization round started after Codex review (2026-06-19).** Goal: improve the
  0619 peak-shaving manuscript without running new experiments. Scope is limited to
  manuscript logic, evidence boundaries, equation/code consistency, and reproducibility
  documentation. Planned edits:
  * Reframe the congested-regime result as a shape-restricted fictitious-play
    time-average / snapshot rather than a fully established equilibrium claim.
  * Align the utility equation with the implemented generalized-cost form in
    `pricing_sim/peak_shaving_market.py`.
  * Replace "robust QoS protection" and "profit near zero" with more defensible
    wording: QoS-improvement direction is consistent across grids, while profit is
    not robustly positive and remains solver-sensitive.
  * Add a peak-shaving supplement with parameters, grid definitions, artifact mapping,
    and reproduction commands.
  * Status: in_progress.

- **Optimization round completed and compiled (2026-06-19 14:11 CST).** Revised the
  peak-shaving draft after the Codex review. No Python experiments were run; all
  numerical claims still trace to `artifacts/peak_shaving/20260618/`.
  * Manuscript edits:
    - Retitled the paper around QoS protection and profit boundaries rather than
      load migration as a full headline.
    - Rewrote the abstract, contribution list, solver section, results, discussion,
      limitations, and conclusion to avoid over-claiming.
    - Reframed the congested regime as a shape-restricted fictitious-play time-average
      / snapshot with explicit exploitability and grid-resolution boundaries.
    - Aligned the utility equation with the implemented generalized-cost form:
      migration cost is inside the price-like term scaled by user price sensitivity.
    - Added an evidence-boundary table separating converged baseline, coarse-grid
      diagnostic, and non-converged fine-grid snapshot.
  * Supplement added:
    - `peak_shaving_dynamic_pricing_supplement_2026-06-19.tex/.pdf`
    - Contains parameter table, grid definitions, artifact-to-number mapping,
      reproduction commands, and known limitations.
  * Commands:
    ```bash
    xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex
    bibtex peak_shaving_dynamic_pricing_2026-06-19
    xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex
    xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex
    xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex
    xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex
    ```
  * Verification:
    - Main PDF: `peak_shaving_dynamic_pricing_2026-06-19.pdf`, 9 pages.
    - Supplement PDF: `peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf`, 4 pages.
    - Final log scan found no undefined references/citations, no LaTeX errors, and
      no overfull boxes. Remaining fontspec CJK-script warnings are the same harmless
      Fandol font warnings seen in prior builds.
  * Status: verified.

- **Post-optimization Nature-style reassessment (2026-06-19 14:14 CST).** Review-only
  pass on the optimized peak-shaving manuscript and supplement. No Python experiments,
  citation lookups, or additional LaTeX compilation were run in this review pass.
  * Inputs:
    - `peak_shaving_dynamic_pricing_2026-06-19.tex`
    - `peak_shaving_dynamic_pricing_supplement_2026-06-19.tex`
    - latest README optimization record
    - compiled PDF metadata from the 14:11 CST build
  * Output:
    - `docs/reviews/codex_nature_style_peak_shaving_review_after_optimization_2026-06-19.md`
  * Result:
    - The reassessment finds the previous hard issues materially improved:
      claim strength, utility-equation alignment, evidence-boundary disclosure,
      and missing supplement.
    - The draft is still not submission-ready. Remaining blockers are:
      (1) the positive QoS claim is still qualitative and not yet a
      low-exploitability equilibrium property; (2) profit and surplus mechanism
      diagnostics are missing; (3) no real calibration or congested-regime economic
      parameter sweep is present; (4) related work remains too narrow; and
      (5) the paper needs figures for market structure, time profiles, and
      regret/convergence.
  * Priority next steps:
    1. Add exploitability/perturbation evidence for the QoS direction, or explicitly
       label the paper exploratory.
    2. Add mechanism diagnostics: demand by period/type/channel, exit, average price,
       served demand, profit components, and user welfare/inclusive value.
    3. Add three figures: market schematic, time-profile comparison, and regret trace.
    4. Expand related work beyond inference serving and electricity demand response.
    5. Add one real calibration anchor or congested-regime parameter sweep.
  * Status: recorded.

- **Reviewer-response enhancement started (2026-06-19 16:06 CST).** Goal:
  strengthen the 0619 peak-shaving manuscript against the latest three-reviewer
  summary: Reviewer 1 asks for firmer QoS evidence, Reviewer 2 asks for clearer
  generalization boundaries and literature positioning, and Reviewer 3 asks for
  figures plus mechanism diagnostics. This round is not a claim-expansion pass; it
  will add diagnostics and visual evidence only where the current artifacts support
  them.
  * Planned actions:
    - Build a diagnostic artifact from the existing 20260618 congested-regime
      outputs: time profiles, demand by type/channel, exit, inclusive value,
      served demand, average price, profit components, and final exploitability
      checks.
    - Generate manuscript-ready figures for market structure, QoS/utilization
      profiles, mechanism diagnostics, and convergence / exploitability boundaries.
    - Revise the main paper to connect those diagnostics to the QoS and profit
      mechanisms without overstating equilibrium strength.
    - Expand related-work positioning using only verified local references or
      explicitly checked sources.
    - Update the supplement with diagnostic provenance and figure/data mapping.
  * Commands already run for context:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pwd && uname -a && git rev-parse --show-toplevel 2>/dev/null || true && git status --short 2>/dev/null || true && command -v uv || true && uv --version || true'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && rg -n "2026-06-19|Experiment Log|实验记录|review|审稿|优化" README.md | tail -100'
    ```
  * Environment notes:
    - WSL distro: `Ubuntu-22.04`.
    - Project path: `/root/paper_code/0427_tokenrl/paper_token_cross_survey`.
    - `uv`: `/root/.local/bin/uv`, version `0.10.9`.
    - This subdirectory is not currently inside a Git worktree, so Git diff/status
      cannot be used as a change audit.
    - A parallel WSL read attempt returned `Wsl/Service/E_UNEXPECTED`; subsequent
      WSL checks succeeded, so the rest of the round will use serial WSL commands.
  * Status: in_progress.

- **Reviewer-response diagnostics generated (2026-06-19 16:06 CST).** Built
  mechanism diagnostics and manuscript-ready figures from existing 20260618
  congested-regime policy artifacts. This command reconstructs reported policy
  snapshots and does not run a new equilibrium search.
  * Command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run --with-requirements requirements.txt python experiments/build_peak_shaving_diagnostics.py'
    ```
  * Outputs:
    - `experiments/build_peak_shaving_diagnostics.py`
    - `artifacts/peak_shaving/20260619/peak_shaving_diagnostics.json`
    - `artifacts/peak_shaving/20260619/peak_shaving_mechanism_summary.csv`
    - `artifacts/peak_shaving/20260619/peak_shaving_time_profiles.csv`
    - `figures/peak_shaving_diagnostics/market_schematic.pdf`
    - `figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf`
    - `figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf`
    - `figures/peak_shaving_diagnostics/profit_components_and_regret.pdf`
  * Result:
    - Script exit status: success.
    - Validation warnings: none; reconstructed system profits match the existing
      reported artifacts within the script tolerance.
    - Key diagnostic pattern: compared with the uniform congested baseline,
      dynamic coarse and fine snapshots reduce peak utilization
      (`0.782 -> 0.706 / 0.666`) and raise the QoS-adjusted served volume
      (`2610 -> 2865 / 3043`), while average paid price falls
      (`0.761 -> 0.735 / 0.625`). This supports a QoS/coverage mechanism, not a
      robust profit-growth claim.
    - Exit probability also falls in the diagnostic snapshots
      (rigid `0.158 -> 0.145 / 0.119`, elastic `0.087 -> 0.075 / 0.044`), but the
      fine-grid snapshot remains non-converged (`maxregret=22.3029`), so these
      numbers must be labeled diagnostic rather than equilibrium estimates.
  * Figure check:
    - All four generated PDFs are one-page figures by `pdfinfo`.
  * Status: generated.

- **Reviewer-response manuscript revision compiled (2026-06-19 16:19 CST).**
  Revised the 0619 peak-shaving main paper and supplement to respond to the three
  reviewer summaries without broadening the claim beyond the available evidence.
  * Main-paper edits:
    - Added a literature-positioning subsection covering inference serving,
      dynamic pricing / congestion economics / revenue management, electricity
      demand response, LLM-service pricing, discrete choice, and platform markets.
    - Added four figures: market structure, QoS/utilization profiles, profit +
      regret boundary, and mechanism diagnostics.
    - Strengthened the QoS evidence discussion by tying it to the new time-profile
      figure while preserving the fine-grid non-convergence warning.
    - Added mechanism diagnostics showing that dynamic snapshots improve
      QoS-adjusted served volume and reduce exit, but also lower average paid price;
      this supports a QoS/coverage mechanism rather than a robust profit claim.
    - Updated code/artifact availability to include the 20260619 diagnostic outputs
      and figure directory.
  * Supplement edits:
    - Added S4, "机制诊断和图表来源", mapping the diagnostic JSON/CSV/figure outputs.
    - Added the diagnostic-generation command to the reproduction section.
    - Renumbered known limitations to S6.
  * Commands:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex && bibtex peak_shaving_dynamic_pricing_2026-06-19 && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && rg -n "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_2026-06-19.log || true && rg -n "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_supplement_2026-06-19.log || true && pdfinfo peak_shaving_dynamic_pricing_2026-06-19.pdf | rg "Pages|Page size" && pdfinfo peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf | rg "Pages|Page size"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_2026-06-19.pdf - | rg -n "文献位置|市场结构|拥塞区间的时段利用率|利润分布与收敛边界|机制诊断|QoS调整后的服务量|代码与工件可用性" && pdftotext peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf - | rg -n "机制诊断和图表来源|build_peak_shaving_diagnostics|validation warning|S6"'
    ```
  * Verification:
    - Main PDF: `peak_shaving_dynamic_pricing_2026-06-19.pdf`, 13 pages.
    - Supplement PDF: `peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf`, 4 pages.
    - Final log scan found no undefined references/citations, no LaTeX errors, and
      no overfull boxes. Remaining warnings are harmless Fandol CJK-script warnings
      and underfull boxes in long bibliography / path-heavy supplement rows.
    - `pdftotext` confirms that the literature positioning, four figure captions,
      mechanism-diagnostic text, code availability paragraph, supplement S4, and
      diagnostic command are present in the compiled PDFs.
  * Remaining evidence boundary:
    - The paper still cannot claim a fully established low-exploitability congested
      equilibrium because the fine-grid snapshot remains non-converged. The revised
      paper therefore keeps the QoS result as a cross-grid directional diagnostic.
  * Status: verified.

- **Submission-strengthening experiment round started (2026-06-19 18:17 CST).**
  Goal: address the remaining submission-readiness gaps identified after the
  16:19 revision by adding three evidence layers: a stronger mixed/average-strategy
  exploitability diagnostic for the congested fine-grid regime, a key-parameter
  robustness scan, and a real-world public API price calibration anchor.
  * Scope and design:
    - Mixed/average strategy: build a finite-grid double-oracle / empirical
      fictitious-play diagnostic using the existing congested fine-grid candidate
      set. The output will report full-grid best-response regret against the mixed
      profile. If the regret is not below the target, the paper will state the
      remaining boundary instead of claiming convergence.
    - Parameter scan: run a fixed-policy stress test around the reported uniform,
      dynamic-coarse, and dynamic-fine policy snapshots for capacity scale, price
      sensitivity, migration cost, and QoS threshold. This tests whether the QoS
      direction survives local parameter perturbations without pretending each
      point is a freshly solved equilibrium.
    - Real calibration anchor: verify public API pricing from official provider
      pages and add it as a scale anchor, not as a full demand calibration.
  * Planned files:
    - New tests under `tests/` for support selection, mixed-regret accounting, and
      parameter-scan scenario construction.
    - New experiment scripts under `experiments/`.
    - New artifacts under `artifacts/peak_shaving/20260619_submission/`.
    - New figures under `figures/peak_shaving_submission/`.
    - Revised main paper, supplement, and bibliography if the checked public
      pricing anchor requires updated access dates or citations.
  * Commands already run for context:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pwd && uname -a && git rev-parse --show-toplevel 2>/dev/null || true && git status --short 2>/dev/null || true && command -v uv || true && uv --version || true'
    ```
  * Environment notes:
    - WSL distro: `Ubuntu-22.04`.
    - Project path: `/root/paper_code/0427_tokenrl/paper_token_cross_survey`.
    - `uv`: `/root/.local/bin/uv`, version `0.10.9`.
    - This subdirectory is not a Git worktree, so Git cannot be used as the final
      diff audit.
  * Status: in_progress.

- **Submission-strengthening scripts and experiments generated (2026-06-19 18:31
  CST).** Added tested reusable tooling plus two new experiment entrypoints for
  the submission-readiness round.
  * New files:
    - `experiments/peak_shaving_submission_tools.py`
    - `experiments/run_peak_shaving_mixed_oracle.py`
    - `experiments/run_peak_shaving_parameter_sweep.py`
    - `tests/test_peak_shaving_submission_tools.py`
  * TDD commands:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run --with-requirements requirements.txt pytest tests/test_peak_shaving_submission_tools.py -q'
    ```
    - First run failed as expected with `ModuleNotFoundError:
      experiments.peak_shaving_submission_tools`.
    - After implementation: `4 passed`.
  * Static checks:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && wc -l experiments/peak_shaving_submission_tools.py experiments/run_peak_shaving_mixed_oracle.py experiments/run_peak_shaving_parameter_sweep.py && python -m py_compile experiments/peak_shaving_submission_tools.py experiments/run_peak_shaving_mixed_oracle.py experiments/run_peak_shaving_parameter_sweep.py'
    ```
    - File sizes: 85 / 175 / 145 lines.
    - `py_compile`: success.
  * Parameter-sweep command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run --with-requirements requirements.txt python experiments/run_peak_shaving_parameter_sweep.py'
    ```
    - Outputs:
      - `artifacts/peak_shaving/20260619_submission/peak_shaving_parameter_sweep.json`
      - `artifacts/peak_shaving/20260619_submission/peak_shaving_parameter_sweep.csv`
      - `artifacts/peak_shaving/20260619_submission/peak_shaving_parameter_sweep_summary.json`
      - `figures/peak_shaving_submission/parameter_sweep_qos.pdf`
    - Result:
      - 27 rows = 9 scenarios x 3 policy snapshots.
      - Dynamic coarse: QoS gain positive in 9/9, peak-utilization reduction
        positive in 9/9, profit gain positive in 9/9.
      - Dynamic fine: QoS gain positive in 9/9, peak-utilization reduction
        positive in 9/9, profit gain positive in only 1/9.
      - Minimum QoS gain over all tested perturbations remains positive
        (`0.126` coarse, `0.129` fine). This strengthens the QoS direction while
        preserving the "profit not robust" conclusion.
  * Mixed-oracle command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run --with-requirements requirements.txt python experiments/run_peak_shaving_mixed_oracle.py'
    ```
    - Outputs:
      - `artifacts/peak_shaving/20260619_submission/peak_shaving_mixed_oracle.json`
      - `figures/peak_shaving_submission/mixed_oracle_regret.pdf`
    - Result:
      - Full fine-grid candidate set: 225 strategies per firm.
      - Double-oracle support at termination: 5 x 5.
      - Evaluated pure-strategy pairs: 2225.
      - Final full-grid max regret: `0.2025`, well below the previous target of 5.
      - Expected mixed-profile metrics: system profit `1733.13`, peak utilization
        `0.7030`, minimum QoS `0.9699`.
    - Interpretation:
      - This provides a low-exploitability mixed/average-strategy diagnostic on the
        finite fine grid. It does not prove a continuous-strategy equilibrium, but
        it removes the earlier objection that the only fine-grid evidence was a
        high-regret single snapshot.
  * Status: generated.

- **Public API price anchor checked (2026-06-19 18:31 CST).** Verified current
  public API price references from official provider documentation and stored a
  machine-readable scale anchor.
  * Sources checked:
    - Z.AI official developer pricing: `https://docs.z.ai/guides/overview/pricing`
      — states prices are in USD per 1M tokens. Relevant GLM text prices include
      GLM-5 (`$1.0` input, `$3.2` output), GLM-4.7 (`$0.6` input, `$2.2` output),
      and GLM-4.7-FlashX (`$0.07` input, `$0.4` output).
    - DeepSeek official API pricing:
      `https://api-docs.deepseek.com/quick_start/pricing-details-usd` — reports
      deepseek-chat cache-miss input `$0.27` and output `$1.10`, and
      deepseek-reasoner cache-miss input `$0.55` and output `$2.19`, per 1M tokens.
    - OpenAI official GPT-4o model page:
      `https://developers.openai.com/api/docs/models/gpt-4o` — reports GPT-4o
      input `$2.50`, cached input `$1.25`, and output `$10.00`, per 1M tokens.
  * Files updated:
    - `verified_refs.bib`: updated DeepSeek/OpenAI access dates and added
      `zaiPricing2026`.
    - `artifacts/peak_shaving/20260619_submission/public_api_price_anchor.json`
  * Interpretation:
    - These prices provide an order-of-magnitude anchor for the normalized price
      unit used in the simulation. They do not estimate demand elasticity, migration
      cost, or the QoS-utilization curve.
  * Status: recorded.

- **Verification timeout recorded (2026-06-19 18:41 CST).** A broad targeted
  pytest command including older equilibrium tests exceeded the command timeout.
  The timeout came from the legacy `solve_firm_nash`-based tests, not from the new
  submission-strengthening utility tests.
  * Command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run --with-requirements requirements.txt pytest tests/test_peak_shaving_submission_tools.py tests/test_peak_shaving_market.py tests/test_peak_shaving_equilibrium.py -q'
    ```
  * Result:
    - Timed out after 184 seconds.
    - The still-running pytest process was terminated because it was started by
      this task and was consuming CPU.
  * Decision:
    - Continue with focused verification for the new utilities / scripts plus
      LaTeX compilation and log checks. Do not claim the full older equilibrium
      test file passes in this round.
  * Status: failed.

- **Submission-strengthening manuscript revision verified (2026-06-19 18:44 CST).**
  Integrated the mixed-oracle evidence, parameter stress test, and public API price
  anchor into the main paper and supplement.
  * Main-paper updates:
    - Abstract, contribution list, solver remark, congested-results table,
      evidence-boundary table, discussion, limitations, conclusion, and
      code/artifact availability were revised.
    - Added `mixed_oracle_regret.pdf` and `parameter_sweep_qos.pdf`.
    - Added official public API price anchor citations for Z.AI, DeepSeek, and
      OpenAI GPT-4o.
  * Supplement updates:
    - Added mixed-oracle, parameter-sweep, and public-price-anchor rows to the
      artifact mapping table.
    - Added S5, "投稿增强实验与校准锚点".
    - Added reproduction commands for the parameter sweep and mixed oracle.
    - Updated limitations to distinguish a high-regret fine-grid pure snapshot from
      the low-regret finite-grid mixed profile.
  * Verification commands:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && python -m py_compile experiments/peak_shaving_submission_tools.py experiments/run_peak_shaving_mixed_oracle.py experiments/run_peak_shaving_parameter_sweep.py && uv run --with-requirements requirements.txt pytest tests/test_peak_shaving_submission_tools.py tests/test_peak_shaving_market.py -q'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex && bibtex peak_shaving_dynamic_pricing_2026-06-19 && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && rg -n "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_2026-06-19.log peak_shaving_dynamic_pricing_supplement_2026-06-19.log || true && pdfinfo peak_shaving_dynamic_pricing_2026-06-19.pdf | rg "Pages|Page size" && pdfinfo peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf | rg "Pages|Page size"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_2026-06-19.pdf - | rg -n "双重oracle|0\\.203|参数压力测试|GLM-4\\.7|公开API|细网格混合" && pdftotext peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf - | rg -n "投稿增强实验|0\\.2025|public_api_price_anchor|run_peak_shaving_mixed_oracle|run_peak_shaving_parameter_sweep"'
    ```
  * Verification result:
    - Python focused tests: `14 passed`.
    - Main PDF: `peak_shaving_dynamic_pricing_2026-06-19.pdf`, 15 pages.
    - Supplement PDF: `peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf`, 5 pages.
    - Final log scan found no undefined references/citations, no LaTeX errors, and
      no overfull boxes.
    - `pdftotext` confirms the mixed-oracle result, parameter stress test, public API
      price anchor, and supplement S5 are present in the compiled PDFs.
  * Remaining verification boundary:
    - The older `tests/test_peak_shaving_equilibrium.py` file was not claimed as
      passing in this round because it timed out when included with broader tests.
    - The mixed-oracle result is a low-regret finite-grid mixed/average diagnostic,
      not a continuous-strategy equilibrium proof.
  * Status: verified.

- **Publication-polish pass started (2026-06-19 19:14 CST).** Continue optimizing
  the peak-shaving manuscript after the submission-strengthening experiments.
  * Goal:
    - Improve reviewer-facing readability without changing experimental values,
      artifacts, or claims beyond the verified evidence.
  * Scope:
    - Main manuscript abstract, congested-results wording, evidence-boundary table,
      discussion, limitations, conclusion, and small LaTeX/table defects.
    - Supplement is kept stable unless compilation or terminology consistency shows
      a concrete issue.
  * Constraints:
    - Preserve the mixed-oracle max regret (`0.203` in the paper, `0.2025` in the
      JSON artifact), parameter-sweep results, and public API price anchor.
    - Do not claim that the legacy `tests/test_peak_shaving_equilibrium.py` passed;
      it previously timed out.
  * Plan:
    1. Rebuild the abstract around question, method, evidence, boundary, and
       implication.
    2. Separate Results-style quantitative reporting from Discussion-style
       interpretation.
    3. Remove duplicated table rows and reduce internal-workshop phrasing.
    4. Recompile the paper and scan logs for undefined references, citation
       warnings, LaTeX errors, and overfull boxes.
  * Action completed before compilation (2026-06-19 19:21 CST):
    - Rewrote the main abstract around the sequence question, model, solver,
      QoS evidence, profit boundary, and calibration boundary.
    - Renamed the congested-results subsection to emphasize stronger QoS evidence
      and still-unstable profit evidence.
    - Harmonized "mixed oracle" wording in the main paper and supplement as
      finite-grid mixed-strategy diagnostics while preserving script/artifact names.
    - Replaced colloquial discussion phrasing with a clearer residual-reallocation
      mechanism explanation.
  * Verification commands (2026-06-19 19:22 CST):
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex >/tmp/ps_polish_main1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex >/tmp/ps_polish_main2.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex >/tmp/ps_polish_supp1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex >/tmp/ps_polish_supp2.log && rg -n "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_2026-06-19.log peak_shaving_dynamic_pricing_supplement_2026-06-19.log /tmp/ps_polish_main1.log /tmp/ps_polish_main2.log /tmp/ps_polish_supp1.log /tmp/ps_polish_supp2.log || true && pdfinfo peak_shaving_dynamic_pricing_2026-06-19.pdf | rg "Pages|Page size" && pdfinfo peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf | rg "Pages|Page size"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_2026-06-19.pdf - | rg -n "QoS保护证据|细网格混合诊断|混合策略诊断|重排剩余，而非创造新增供给|证据更充分|不是利润提升机制" | sed -n "1,120p"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf - | rg -n "混合策略诊断|peak_shaving_mixed_oracle|0\.2025|连续策略空间" | sed -n "1,120p"'
    ```
  * Verification result:
    - Main PDF regenerated: `peak_shaving_dynamic_pricing_2026-06-19.pdf`, 15 pages, A4.
    - Supplement PDF regenerated: `peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf`, 5 pages, A4.
    - Log scan returned no undefined references/citations, no LaTeX errors, and no overfull boxes.
    - `pdftotext` confirms the revised QoS/profit-boundary wording and mixed-strategy
      diagnostic labels are present in both PDFs.
  * Remaining boundary:
    - No Python experiment or legacy equilibrium test was rerun in this polish pass,
      because this step changed only manuscript prose and terminology labels.
  * Status: verified.

- **Q1 SCI calibration-anchor pass started (2026-06-19 20:02 CST).** Continue from
  the Q1-SCI target discussion by adding a real-measurement anchor where possible,
  rather than adding more synthetic-only experiments.
  * Goal:
    - Strengthen the manuscript for Q1 SCI review by connecting the synthetic
      QoS-utilization proxy to existing single-GPU Ollama/vLLM microbenchmark
      artifacts.
  * Context:
    - Existing documentation lists Ollama and vLLM single-GPU benchmark protocols
      under `docs/system-benchmark.md` and `docs/vllm-system-benchmark.md`.
    - Existing root artifacts include `artifacts/calibration_uncertainty/*/measured_qos_stress.csv`
      and vLLM/Ollama summary files.
  * Action:
    - Inspect benchmark scripts, tests, metadata, and measured QoS stress files.
    - Select one reproducible, current-root measurement bundle as a calibration
      anchor.
    - Add a manuscript/supplement statement that treats it as a bounded
      microbenchmark anchor, not as production trace calibration.
  * Command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pwd && uname -a && git rev-parse --show-toplevel 2>/dev/null || true && git status --short 2>/dev/null || true && command -v uv || true && uv --version || true && date "+%Y-%m-%d %H:%M %Z" && rg --files | rg "(benchmark|vllm|ollama|gpu|latency|qos|peak_shaving|README|pyproject|requirements|docs/)" | sed -n "1,240p"'
    ```
  * Initial observation:
    - The project is running in WSL at `/root/paper_code/0427_tokenrl/paper_token_cross_survey`.
    - `uv` is available at `/root/.local/bin/uv`, version `0.10.9`.
    - The subdirectory is not reported as a Git worktree by `git rev-parse`.
    - Existing benchmark artifacts are present in the current root, so this pass can
      prioritize integration and verification before deciding whether a fresh GPU
      run is necessary.
  * Implementation update (2026-06-19 20:09 CST):
    - Added `experiments/build_peak_shaving_measurement_anchor.py` to extract the
      two existing vLLM controlled-scan aggregates, fit the existing threshold-type
      QoS proxy, and render a publication PDF/PNG figure.
    - Added `tests/test_peak_shaving_measurement_anchor.py`.
    - Initial test attempt failed because `experiments` was not on `sys.path`.
      A second attempt exposed an external-path edge case in `Path.relative_to`.
      Both issues were fixed before generating the manuscript artifacts.
  * Commands:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run --with-requirements requirements.txt pytest tests/test_peak_shaving_measurement_anchor.py -q'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run --with-requirements requirements.txt python experiments/build_peak_shaving_measurement_anchor.py'
    ```
  * Output:
    - `artifacts/peak_shaving/20260619_submission/vllm_qos_anchor_summary.json`
    - `artifacts/peak_shaving/20260619_submission/vllm_qos_anchor_points.csv`
    - `figures/peak_shaving_submission/vllm_qos_anchor.pdf`
    - `figures/peak_shaving_submission/vllm_qos_anchor.png`
  * Result:
    - New unit test after fixes: `2 passed`.
    - 0.5B profile: max healthy concurrency `224`, fitted
      `qos_threshold=1.000`, `qos_strength=0.517`, `RMSE=0.068`, minimum observed
      TTFT-SLA rate `0.500`.
    - 3B profile: max healthy concurrency `224`, fitted `qos_threshold=1.058`,
      `qos_strength=0.942`, `RMSE=6.3e-10`, minimum observed TTFT-SLA rate `0.667`.
    - The anchor is used only as a controlled single-GPU QoS-shape reference, not as
      production trace calibration or user elasticity evidence.
  * Manuscript update:
    - Main paper now includes `vllm_qos_anchor.pdf` in the experiment setting section
      and clarifies the calibration boundary in the abstract and limitations.
    - Supplement now maps the anchor artifacts, reports the fitted parameters, and
      lists the reproduction command.
  * LaTeX issue and fix:
    - First supplement compile attempt stopped at the new anchor table because the
      supplement used `[H]` without loading the `float` package.
    - Fixed by adding `\usepackage{float}` to
      `peak_shaving_dynamic_pricing_supplement_2026-06-19.tex`.
  * Final verification commands (2026-06-19 20:13 CST):
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && python -m py_compile experiments/build_peak_shaving_measurement_anchor.py && uv run --with-requirements requirements.txt pytest tests/test_peak_shaving_measurement_anchor.py tests/test_calibration.py tests/test_vllm_plots.py -q && uv run --with-requirements requirements.txt python experiments/build_peak_shaving_measurement_anchor.py'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex >/tmp/ps_q1_main1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex >/tmp/ps_q1_main2.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex >/tmp/ps_q1_supp1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex >/tmp/ps_q1_supp2.log'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_2026-06-19.log peak_shaving_dynamic_pricing_supplement_2026-06-19.log /tmp/ps_q1_main2.log /tmp/ps_q1_supp2.log || true'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_2026-06-19.pdf /tmp/ps_main_q1_final.txt && pdftotext peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf /tmp/ps_supp_q1_final.txt'
    ```
  * Final verification result:
    - Python checks: `5 passed`.
    - Main PDF regenerated: `peak_shaving_dynamic_pricing_2026-06-19.pdf`, 16 pages, A4.
    - Supplement PDF regenerated: `peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf`, 5 pages, A4.
    - Final log scan returned no undefined references/citations, no LaTeX errors,
      and no overfull boxes.
    - `pdftotext` confirms the vLLM QoS anchor paragraph, figure caption, supplement
      table, reproduction command, and updated limitations are present in the PDFs.
  * Remaining boundary:
    - This pass did not rerun the GPU benchmark server. It reuses existing controlled
      vLLM artifacts and makes that provenance explicit.
    - The measurement anchor improves external validity for the QoS curve shape; it
      still does not calibrate demand elasticity, migration cost, or production traces.
  * Status: verified.

- **Submission-style manuscript polish started (2026-06-19 20:30 CST).** Polish
  the current peak-shaving manuscript so it reads more like a formal journal
  submission rather than an internal working draft.
  * Goal:
    - Improve submission readiness by tightening the title signal, abstract logic,
      introduction framing, section titles, solver description, Results/Discussion
      separation, limitations, and conclusion.
  * Context:
    - This is a prose and structure pass only.
    - Existing quantitative claims, citations, experiment artifacts, figures, tables,
      and calibration boundaries must remain unchanged unless a compile or consistency
      check exposes a concrete issue.
  * Action plan:
    - Apply `nature-polishing` with research-paper axes:
      abstract, introduction, results, discussion, conclusion, title, and methods-like
      reproducibility wording.
    - Replace informal or internal-draft wording with submission-style academic prose.
    - Preserve the current cautious claim: dynamic time-of-use pricing is supported as
      a QoS-protection mechanism, not as a robust profit-improvement mechanism.
  * Planned verification:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex >/tmp/ps_submit_main1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex >/tmp/ps_submit_main2.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex >/tmp/ps_submit_supp1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex >/tmp/ps_submit_supp2.log'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_2026-06-19.log peak_shaving_dynamic_pricing_supplement_2026-06-19.log /tmp/ps_submit_main2.log /tmp/ps_submit_supp2.log || true'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_2026-06-19.pdf /tmp/ps_submit_main.txt && pdftotext peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf /tmp/ps_submit_supp.txt'
    ```
  * Action completed (2026-06-19 20:36 CST):
    - Retitled the paper as `固定算力约束下推理服务的分时动态定价`.
    - Rewrote the abstract into a submission-style sequence:
      context, research question, model, solver, key QoS results, profit boundary,
      and calibration boundary.
    - Renamed and polished the introduction subsections:
      `研究问题与动机`, `竞争结构与异质算力`, and `相关文献与研究定位`.
    - Reframed the solver section around the low-dimensional pricing shape family,
      fictitious play, and low-exploitability diagnostics.
    - Renamed Discussion and Limitations to emphasize the QoS/profit boundary and
      explicit evidence limits.
    - Rewrote residual informal/internal-draft expressions without changing numeric
      claims, citations, labels, figures, or tables.
  * Verification commands (2026-06-19 20:36 CST):
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && rg -n "各有各|矛盾|摆在|不一样|一家独大|卡多|卡紧|对得上|没什么|真拥塞|上分时|显眼|明说|相对常规|会出问题|来回跳|好并行|成本会爆|栽跟头|悄悄|问的是|搭了|省下来的|为什么|护住|压住|白白|打到|翻成" peak_shaving_dynamic_pricing_2026-06-19.tex || true'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex >/tmp/ps_submit_main1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_2026-06-19.tex >/tmp/ps_submit_main2.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex >/tmp/ps_submit_supp1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_supplement_2026-06-19.tex >/tmp/ps_submit_supp2.log && grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_2026-06-19.log peak_shaving_dynamic_pricing_supplement_2026-06-19.log /tmp/ps_submit_main2.log /tmp/ps_submit_supp2.log || true && pdfinfo peak_shaving_dynamic_pricing_2026-06-19.pdf | grep -E "Pages|Page size" && pdfinfo peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf | grep -E "Pages|Page size"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_2026-06-19.pdf /tmp/ps_submit_main.txt && pdftotext peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf /tmp/ps_submit_supp.txt && grep -nE "固定算力约束下推理服务的分时动态定价|研究问题与动机|竞争结构与异质算力|相关文献与研究定位|局限性|分时定价更适合作为服务质量管理工具|vLLM QoS" /tmp/ps_submit_main.txt | sed -n "1,160p" && grep -nE "投稿增强实验|vLLM|0\\.2025|public_api_price_anchor|run_peak_shaving_mixed_oracle|run_peak_shaving_parameter_sweep" /tmp/ps_submit_supp.txt | sed -n "1,160p"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'grep -nE "虚拟博弈|exploitability|QoS改善|利润边界|剩余重排|新增供给|运营与监管" /tmp/ps_submit_main.txt | sed -n "1,160p"'
    ```
  * Verification result:
    - Informal-expression scan returned no remaining matches for the tracked phrases.
    - Main PDF regenerated: `peak_shaving_dynamic_pricing_2026-06-19.pdf`, 16 pages, A4.
    - Supplement PDF regenerated: `peak_shaving_dynamic_pricing_supplement_2026-06-19.pdf`, 5 pages, A4.
    - Log scan returned no undefined references/citations, no LaTeX errors, and no
      overfull boxes.
    - `pdftotext` confirms the new title, revised section headings, QoS/profit-boundary
      discussion, limitations wording, code-availability entry, and supplement
      calibration-anchor content are present in the generated PDFs.
  * Remaining boundary:
    - This pass did not add new experiments, references, or claims.
    - The manuscript is more submission-like, but target-journal adaptation still
      requires a named journal, word limits, article type, and reference style.
  * Status: verified.

- **English SCI middle-draft implementation started (2026-06-19 20:57 CST).** Execute
  the approved plan to produce an English SCI-style middle draft and a claim-evidence
  audit for the peak-shaving manuscript.
  * Goal:
    - Create an English manuscript draft suitable for close human review.
    - Audit whether the current experiments support each main claim.
    - Humanize the English scientific prose without adding experiments or expanding
      the evidence beyond the verified artifacts.
  * Scope:
    - Create `peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex`.
    - Create `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex`.
    - Create `docs/reviews/peak_shaving_sci_readiness_audit_2026-06-19.md`.
    - Update this README with actions, commands, outputs, and verification results.
  * Constraints:
    - Do not overwrite the Chinese manuscript.
    - Do not modify experiment scripts, JSON/CSV artifacts, figure data, or
      `verified_refs.bib`.
    - Do not claim production prediction, continuous-space Nash equilibrium, robust
      profit improvement, calibrated user elasticity, or production QoS calibration.
  * Skills used:
    - `nature-reviewer` for reviewer-style readiness assessment.
    - `nature-polishing` for English SCI structure and section logic.
    - `humanizer` for AI-writing-pattern checks.
    - `ara-rigor-reviewer` was requested in the plan but the local skill path is
      missing, so it is not used.
  * Initial environment command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pwd && uname -a || true && git rev-parse --show-toplevel 2>/dev/null || true && git status --short 2>/dev/null || true && command -v uv || true && uv --version || true && date "+%Y-%m-%d %H:%M %Z"'
    ```
  * Initial environment result:
    - WSL project path: `/root/paper_code/0427_tokenrl/paper_token_cross_survey`.
    - `uv`: `/root/.local/bin/uv`, version `0.10.9`.
    - Timestamp: `2026-06-19 20:57 CST`.
  * Drafting update (2026-06-19 20:57 CST):
    - Created `docs/reviews/peak_shaving_sci_readiness_audit_2026-06-19.md`.
    - Created `peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex`.
    - Created `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex`.
    - The English main draft follows a generic SCI article structure and keeps the
      paper's main claim bounded to finite-grid QoS protection under fixed capacity.
    - The English supplement maps parameters, grids, artifacts, submission-strengthening
      diagnostics, price/QoS anchors, reproduction commands, and known limitations.
  * Evidence-check correction notes (2026-06-19 21:06 CST):
    - A first read-only JSON check used the wrong artifact root
      `artifacts/peak_shaving/20260619` and failed with
      `FileNotFoundError: peak_shaving_summary.json`.
    - A second check used the correct artifact directories but assumed
      `peak_shaving_summary.json` had a `congested_uniform` key; the actual
      congested baseline is in
      `artifacts/peak_shaving/20260618/peak_shaving_congested_fp.json`.
    - A third check assumed older summary field names in
      `peak_shaving_parameter_sweep_summary.json` and failed with `KeyError: 'n'`.
    - A fourth check assumed `vllm_qos_anchor_summary.json["profiles"]` was a
      dictionary; it is a list of profile records.
    - These failures were in the read-only verification script, not in the
      experiment artifacts. The corrected artifact map was written into the
      English supplement.
  * Final read-only evidence check command (2026-06-19 21:06 CST):
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && python - <<"PY"
    import json
    from pathlib import Path
    base=Path("artifacts/peak_shaving/20260618")
    sub=Path("artifacts/peak_shaving/20260619_submission")
    congested=json.load(open(base/"peak_shaving_congested_fp.json"))
    coarse=json.load(open(base/"peak_shaving_fp_dynamic_converged.json"))
    fine=json.load(open(base/"peak_shaving_fp_dynamic_converged_fine.json"))
    mixed=json.load(open(sub/"peak_shaving_mixed_oracle.json"))
    sweep=json.load(open(sub/"peak_shaving_parameter_sweep_summary.json"))
    vllm=json.load(open(sub/"vllm_qos_anchor_summary.json"))
    uniform=congested["uniform"]
    def gain_pct(x):
        return 100*(x-uniform["system_profit"])/uniform["system_profit"]
    print("uniform_congested", round(uniform["peak_util"], 3), round(uniform["min_qos_firm"], 3), round(uniform["system_profit"], 3))
    print("dynamic_coarse", round(coarse["peak_util"], 3), round(coarse["min_qos"], 3), round(gain_pct(coarse["system_profit"]), 1))
    print("dynamic_fine", round(fine["peak_util"], 3), round(fine["min_qos"], 3), round(gain_pct(fine["system_profit"]), 1))
    me=mixed["expected_metrics"]
    reg=mixed["trace"][-1]["full_max_regret"]
    print("mixed", round(reg, 3), round(me["peak_utilization"], 3), round(me["minimum_qos"], 3), round(gain_pct(me["system_profit"]), 1))
    for label, block in sweep.items():
        print("sweep", label, block["scenarios"], block["qos_gain_positive"], block["peak_reduction_positive"], block["profit_gain_positive"], round(block["min_qos_gain"], 3))
    for block in vllm["profiles"]:
        print("vllm", block["profile"], int(block["capacity_concurrency"]), round(block["qos_threshold"], 3), round(block["qos_strength"], 3), round(block["min_observed_qos"], 3))
    PY'
    ```
  * Final evidence check result:
    ```text
    uniform_congested 0.782 0.756 1783.239
    dynamic_coarse 0.706 0.968 9.3
    dynamic_fine 0.666 0.99 -1.9
    mixed 0.203 0.703 0.97 -2.8
    sweep dynamic_coarse 9 9 9 9 0.126
    sweep dynamic_fine 9 9 9 1 0.129
    vllm vllm-0.5b 224 1.0 0.517 0.5
    vllm vllm-3b 224 1.058 0.942 0.667
    ```
  * Compile and verification command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_en_main1.log && bibtex peak_shaving_dynamic_pricing_sci_en_2026-06-19 >/tmp/ps_en_bib.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_en_main2.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_en_main3.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_en_supp1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_en_supp2.log'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_en_supp3.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_en_supp4.log && grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_sci_en_2026-06-19.log peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.log /tmp/ps_en_supp4.log || true && pdfinfo peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf | grep -E "^(Pages|Page size):" && pdfinfo peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf | grep -E "^(Pages|Page size):"'
    ```
  * Compile and verification result:
    - Main PDF regenerated: `peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf`,
      14 pages, A4.
    - Supplement PDF regenerated:
      `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf`, 4 pages,
      A4.
    - Log scan returned no undefined references/citations, no LaTeX errors, and no
      overfull boxes.
    - `pdftotext` confirms that the title, bounded finite-grid QoS claim,
      low-exploitability value, profit-improvement boundary, limitations, code and
      artifact availability, supplement diagnostics, vLLM anchor, and known
      boundaries are present in the PDFs.
  * Language scan command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && rg -n -i "therefore|thus|in addition|moreover|furthermore" peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex || true'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && rg -n -i "robust|mechanism|diagnostic|boundary" peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex'
    ```
  * Language scan result:
    - Mechanical connectors `therefore`, `thus`, `in addition`, `moreover`, and
      `furthermore` no longer appear in the English main or supplement.
    - Remaining matches for `mechanism`, `diagnostic`, and `boundary` are retained
      as technical terms in section titles, figure captions, artifact names, and
      evidence-limit wording.
  * Final completion-gate verification (2026-06-19 21:15 CST):
    - Command:
      Re-ran the full compile/log/PDF command recorded above with
      `/tmp/ps_en_gate_*` log files, then re-ran the same read-only JSON evidence
      check with compact `gate_metrics`, `gate_sweep`, and `gate_vllm` output.
    - Result:
      ```text
      Pages:           14
      Page size:       595.28 x 841.89 pts (A4)
      Pages:           4
      Page size:       595.28 x 841.89 pts (A4)
      gate_metrics 0.782 0.756 0.706 0.968 9.3 0.666 0.99 -1.9 0.203 0.703 0.97 -2.8
      gate_sweep 9 9 1
      gate_vllm [('vllm-0.5b', 224, 1.0, 0.517, 0.5), ('vllm-3b', 224, 1.058, 0.942, 0.667)]
      ```
    - No LaTeX error, undefined reference/citation, or overfull-box line was
      returned by the log scan.
  * Remaining boundary:
    - No new experiment was added or rerun.
    - The English draft is a generic SCI middle draft, not yet adapted to a named
      journal template, article type, word limit, or reference style.
    - The manuscript still supports a cautious simulation/mechanism paper; it does
      not support production prediction, continuous-space equilibrium proof, robust
      profit improvement, calibrated user elasticity, or production QoS calibration.
  * Status: verified.

- **SMPT target-journal adaptation started (2026-06-19 22:28 CST).** The target
  journal is now *Simulation Modelling Practice and Theory*.
  * Goal:
    - Use the supplied strict review log to reframe the English manuscript for SMPT.
    - Separate immediate manuscript/format fixes from experiments that still need
      to be added before a strong submission.
    - Keep all claims within the existing evidence; do not pretend that missing
      baselines, V&V diagnostics, or public artifact DOI already exist.
  * Sources:
    - User review log:
      `C:\Users\cccht\.codex\attachments\2dcfd4dd-9ef0-408a-a079-94508bda9e6c\pasted-text.txt`.
    - Official ScienceDirect journal page and Guide for Authors checked on
      2026-06-19. SMPT asks for original high-quality systems simulation and
      modelling papers, and application papers should make model development,
      implementation, mathematical/scalability issues, and validation/verification
      transparent.
    - Official guide constraints checked in this pass: abstract should be concise
      and factual; keywords must be 1 to 7; highlights are encouraged as a separate
      editable file; data availability and research-data linking need to be handled
      before final submission.
  * Skills used:
    - `journal-adapt` with a lightweight no-corpus path based on official guide
      requirements, the review log, and the CS/engineering base rules.
    - `nature-reviewer` to interpret the supplied review log as reviewer-facing
      risks rather than author wishful thinking.
  * Environment command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pwd && uname -a || true && git rev-parse --show-toplevel 2>/dev/null || true && git status --short 2>/dev/null || true && command -v uv || true && uv --version || true && date "+%Y-%m-%d %H:%M %Z"'
    ```
  * Environment result:
    - WSL project path: `/root/paper_code/0427_tokenrl/paper_token_cross_survey`.
    - `uv`: `/root/.local/bin/uv`, version `0.10.9`.
    - Timestamp: `2026-06-19 22:28 CST`.
  * Manuscript action:
    - Created `docs/reviews/smpt_submission_readiness_2026-06-19.md`.
    - Created `peak_shaving_dynamic_pricing_smpt_highlights_2026-06-19.txt`.
    - Retitled the English manuscript as a simulation-based study for fixed-capacity
      AI inference services.
    - Rewrote the abstract to 228 words and reduced keywords to 7.
    - Renamed core sections toward SMPT terminology:
      `Simulation Model`, `Model Implementation and Candidate-Response Solver`,
      `Verification and Validation`, `Experimental Design`, and
      `Mechanism and Profit-Boundary Discussion`.
    - Added bounded V&V wording based only on existing artifacts.
    - Added a reproducibility/data-availability boundary and an AI-assisted-writing
      declaration draft.
  * Format-check command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && python - <<"PY"
    import re
    from pathlib import Path
    s=Path("peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex").read_text()
    abs_text=re.search(r"\\begin\{abstract\}(.*?)\\end\{abstract\}", s, re.S).group(1)
    words=re.findall(r"[A-Za-z0-9]+(?:-[A-Za-z0-9]+)?", abs_text)
    kw_line=re.search(r"\\noindent\\textbf\{Keywords:\}(.*)", s).group(1)
    keywords=[x.strip() for x in kw_line.split(";") if x.strip()]
    print("abstract_words", len(words))
    print("keyword_count", len(keywords), keywords)
    for i,line in enumerate(Path("peak_shaving_dynamic_pricing_smpt_highlights_2026-06-19.txt").read_text().splitlines(),1):
        print("highlight", i, len(line), line)
    PY'
    ```
  * Format-check result:
    ```text
    abstract_words 228
    keyword_count 7 ['simulation modelling', 'inference service', 'dynamic pricing', 'QoS', 'peak shaving', 'finite-grid regret', 'sensitivity analysis']
    highlight 1 65 An auditable simulation model links AI inference pricing and QoS.
    highlight 2 66 Time-of-use pricing lowers peak utilization in congested settings.
    highlight 3 53 Finite-grid mixed diagnostics reduce regret to 0.203.
    highlight 4 56 QoS gains persist under local fixed-policy stress tests.
    highlight 5 57 Profit improvements are not robust across solver objects.
    ```
  * Compile and PDF-check command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_smpt_main1.log && bibtex peak_shaving_dynamic_pricing_sci_en_2026-06-19 >/tmp/ps_smpt_bib.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_smpt_main2.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_smpt_main3.log && grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_sci_en_2026-06-19.log /tmp/ps_smpt_bib.log /tmp/ps_smpt_main3.log || true && pdfinfo peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf | grep -E "^(Pages|Page size):"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf /tmp/ps_smpt_main.txt && grep -nE "Simulation-Based Study|Verification and Validation|Data Availability|Artifact Boundary|Declaration of Generative AI|AI-assisted|QoS-protection|0\.203" /tmp/ps_smpt_main.txt | head -80'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_smpt_supp1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_smpt_supp2.log && grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.log /tmp/ps_smpt_supp2.log || true && pdfinfo peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf | grep -E "^(Pages|Page size):"'
    ```
  * Compile and PDF-check result:
    - Main PDF regenerated: `peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf`,
      14 pages, A4.
    - Supplement PDF regenerated:
      `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf`, 4 pages,
      A4.
    - Log scans returned no undefined references/citations, no LaTeX errors, and no
      overfull boxes.
    - `pdftotext` confirms the SMPT-oriented title, `Verification and Validation`,
      `Reproducibility, Data Availability, and Artifact Boundary`, and
      `Declaration of Generative AI and AI-Assisted Technologies` are present in
      the generated PDF.
  * Remaining SMPT blockers:
    - Strong baselines are not yet implemented.
    - Structural ablations are not yet implemented.
    - Re-solved sensitivity / phase diagrams are not yet implemented.
    - Fixed-point residual and damping-sensitivity diagnostics are not yet reported.
    - Public repository DOI / archival data deposit is not yet available.
  * Status: verified for the current manuscript-adaptation pass; not yet final
    submission-ready.

- **SMPT experiment completion pass (2026-06-19 22:43 CST).** Add the baseline,
  ablation, phase-grid, restricted re-solve, and fixed-point residual diagnostics
  requested by the SMPT-oriented review.
  * Goal:
    - Move beyond language-only adaptation by generating additional auditable
      simulation evidence.
    - Keep new outputs separate from earlier artifacts.
    - Preserve claim boundaries: restricted local re-solve is not a full
      continuous-strategy equilibrium proof.
  * Plan/spec files:
    - `docs/superpowers/specs/2026-06-19-smpt-experiment-completion-design.md`
    - `docs/superpowers/plans/2026-06-19-smpt-experiment-completion.md`
  * TDD RED command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run pytest tests/test_peak_shaving_smpt_experiments.py -q'
    ```
  * TDD RED result:
    - Failed as expected with
      `ModuleNotFoundError: No module named 'experiments.peak_shaving_smpt_tools'`.
  * Implemented files:
    - `tests/test_peak_shaving_smpt_experiments.py`
    - `experiments/peak_shaving_smpt_tools.py`
    - `experiments/run_peak_shaving_smpt_experiments.py`
  * First runner attempt:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run python experiments/run_peak_shaving_smpt_experiments.py'
    ```
  * First runner result:
    - Failed by timeout after 304 seconds.
    - Cause: the first version reused the original coarse fictitious-play grid for
      five re-solved sensitivity scenarios, making the run too heavy.
    - Corrective action: replaced the heavy re-solve with a restricted local
      candidate re-solve over static, dynamic coarse/fine, off-peak-only, and
      peak-only shapes. This is reported as a diagnostic, not as an equilibrium
      proof.
  * Static-baseline correction:
    - A follow-up read showed `optimal_static_qos_routing` was accidentally
      evaluated with the active load-shape vector. The test
      `test_static_shape_reproduces_congested_uniform_baseline` now locks the
      correct static-shape evaluation to peak utilization `0.7822217827449163`
      and minimum QoS `0.756455957358171`.
  * Final test and experiment command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run pytest tests/test_peak_shaving_smpt_experiments.py -q && uv run python experiments/run_peak_shaving_smpt_experiments.py'
    ```
  * Final test and experiment result:
    ```text
    8 passed in 1.11s
    {
      "bundle": "artifacts/peak_shaving/20260619_smpt/peak_shaving_smpt_experiments.json",
      "baseline_rows": 7,
      "ablation_rows": 6,
      "phase_rows": 25,
      "resolved_rows": 5,
      "figures": [
        "figures/peak_shaving_smpt/smpt_baseline_comparison.pdf",
        "figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf",
        "figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf"
      ]
    }
    ```
  * Key results:
    - Baselines: static with QoS-aware routing has peak utilization `0.782`,
      minimum QoS `0.756`, and system profit `1783.24`.
      Off-peak-only discount reaches minimum QoS `0.833`; peak-only surcharge
      reaches `0.921`; dynamic coarse reaches `0.968`; dynamic fine reaches
      `0.990`.
    - Admission-control diagnostic: matching the dynamic coarse peak-utilization
      target requires a minimum admitted fraction of `0.902` and a mean admitted
      fraction of `0.974`.
    - Fixed-point residuals: static, off-peak-only, peak-only, dynamic coarse, and
      dynamic fine all converge with final residuals below `1e-9`; iterations are
      `52`, `32`, `34`, `33`, and `35`.
    - Ablations: QoS gain is material under baseline, no-outside-option,
      no-time-flexible-users, and equal-routing diagnostics; it nearly vanishes
      when the direct channel is suppressed and reverses under homogeneous
      capacity.
    - Fixed-policy phase grid: QoS gain and peak reduction are positive in all
      `25/25` grid points; minimum QoS gain is `0.094`; fixed-policy profit gain
      ranges from `+2.0%` to `+15.5%`.
    - Restricted local re-solve: QoS gain is positive in all five selected
      perturbation scenarios; profit is mixed (`+12.5%`, `-1.4%`, `-1.9%`,
      `+11.0%`, `+0.7%`), preserving the profit-boundary conclusion.
  * Manuscript updates:
    - Added `SMPT baseline diagnostics` and
      `Structural ablations and re-solved sensitivity` subsections.
    - Added Table `SMPT baseline diagnostics in the congested setting`.
    - Added fixed-policy phase-grid figure from `figures/peak_shaving_smpt/`.
    - Updated the V&V, limitations, artifact availability, and supplement artifact
      map.
  * Compile and PDF-check command:
    ```powershell
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_smpt2_main1.log && bibtex peak_shaving_dynamic_pricing_sci_en_2026-06-19 >/tmp/ps_smpt2_bib.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_smpt2_main2.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_smpt2_main3.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_smpt2_supp1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_smpt2_supp2.log'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_sci_en_2026-06-19.log peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.log /tmp/ps_smpt2_bib.log /tmp/ps_smpt2_main3.log /tmp/ps_smpt2_supp2.log || true && pdfinfo peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf | grep -E "^(Pages|Page size):" && pdfinfo peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf | grep -E "^(Pages|Page size):"'
    wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf /tmp/ps_smpt2_main.txt && pdftotext peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf /tmp/ps_smpt2_supp.txt && grep -nE "SMPT baseline diagnostics|Structural ablations|restricted local|phase grid|0\\.968|smpt_baselines|SMPT diagnostic artifact bundle|run_peak_shaving_smpt" /tmp/ps_smpt2_main.txt /tmp/ps_smpt2_supp.txt | head -100'
    ```
  * Compile and PDF-check result:
    - Main PDF regenerated: `peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf`,
      15 pages, A4.
    - Supplement PDF regenerated:
      `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf`, 5 pages,
      A4.
    - Log scans returned no undefined references/citations, no LaTeX errors, and no
      overfull boxes.
    - `pdftotext` confirms the new SMPT baseline diagnostics, structural ablations,
      restricted local re-solve, phase-grid figure, supplement artifact bundle, and
      SMPT runner command are present in the generated PDFs.
  * Remaining boundary:
    - The paper still lacks a public GitHub/Zenodo/OSF DOI.
    - The new re-solved sensitivity is restricted to a local candidate set, not a
      full continuous-strategy or full-grid re-solve.
    - Damping-factor and initial-condition audits for all candidate evaluations are
      still not fully reported.
  * Status: verified for the SMPT experiment-completion pass; public artifact
    deposit remains pending before formal submission.

### 2026-06-19 23:21 - SMPT GitHub-readiness and V&V completion pass

* Goal: close the remaining reproducibility and verification gaps for a
  Simulation Modelling Practice and Theory submission package, and prepare the
  project for publication in an existing GitHub repository.
* Context:
  * The user approved creating a GitHub-facing artifact package and asked to
    address the remaining defects.
  * The local Codex GitHub plugin exposes file and issue operations for existing
    repositories, but does not expose a create-repository operation.
  * The WSL environment does not currently provide the GitHub CLI (`gh`), so a
    new remote repository could not be created from this environment.
  * `paper_token_cross_survey` and `/root/paper_code/0427_tokenrl` are not
    currently Git working trees, so there is no local Git history to push.
* Actions:
  * Added GitHub-facing reproducibility documents:
    `REPRODUCIBILITY.md`, `DATA_AVAILABILITY.md`, `ARTIFACT_MANIFEST.md`,
    `CITATION.cff`, and `environment.yml`.
  * Added a V&V audit script:
    `experiments/run_peak_shaving_smpt_vv_audit.py`.
  * Extended the SMPT experiment helper with an explicit fixed-point residual
    trace over initial QoS and damping settings.
  * Updated the main manuscript and supplement to report the V&V audit boundary:
    `24/27` checked solver settings converged, all dynamic coarse/fine settings
    converged, and the only non-converged settings were uniform pricing with
    damping `0.5`.
* Commands:
  ```powershell
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run pytest tests/test_peak_shaving_smpt_experiments.py -q && uv run python experiments/run_peak_shaving_smpt_experiments.py && uv run python experiments/run_peak_shaving_smpt_vv_audit.py'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'git -C /root/paper_code/0427_tokenrl rev-parse --show-toplevel 2>/dev/null || true'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'git -C /root/paper_code/0427_tokenrl status --short 2>/dev/null || true'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_github_main1.log && bibtex peak_shaving_dynamic_pricing_sci_en_2026-06-19 >/tmp/ps_github_bib.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_github_main2.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_github_main3.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_github_supp1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_github_supp2.log'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_sci_en_2026-06-19.log peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.log /tmp/ps_github_bib.log /tmp/ps_github_main3.log /tmp/ps_github_supp2.log || true'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdfinfo peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf | grep -E "^(Pages|Page size):" && pdfinfo peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf | grep -E "^(Pages|Page size):"'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf /tmp/ps_github_main.txt && pdftotext peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf /tmp/ps_github_supp.txt && grep -nE "24 of 27|damping|initial|run_peak_shaving_smpt_vv_audit|REPRODUCIBILITY|Data Availability|smpt_vv_damping|restricted local|GitHub" /tmp/ps_github_main.txt /tmp/ps_github_supp.txt | head -120'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && uv run pytest tests/test_peak_shaving_smpt_experiments.py -q && test -s REPRODUCIBILITY.md && test -s DATA_AVAILABILITY.md && test -s ARTIFACT_MANIFEST.md && test -s CITATION.cff && test -s environment.yml && test -s peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf && test -s peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf && test -s artifacts/peak_shaving/20260619_smpt/smpt_vv_damping_initial.csv && rg -n "SMPT GitHub-readiness|Status: verified locally" README.md && (rg -n "REPLACE|TODO|TBD|PLACEHOLDER" REPRODUCIBILITY.md DATA_AVAILABILITY.md ARTIFACT_MANIFEST.md CITATION.cff environment.yml peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex || true)'
  ```
* Outputs:
  * `artifacts/peak_shaving/20260619_smpt/smpt_vv_damping_initial.csv`
  * `artifacts/peak_shaving/20260619_smpt/peak_shaving_smpt_experiments.json`
  * `figures/peak_shaving_smpt/smpt_baseline_comparison.pdf`
  * `figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf`
  * `figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf`
* Results:
  * Unit tests: `9 passed in 1.22s`.
  * SMPT experiment bundle regenerated successfully with `7` baseline rows, `6`
    ablation rows, `25` phase-grid rows, and `5` restricted local re-solve rows.
  * V&V audit generated `27` rows; `24` converged. Dynamic coarse and dynamic
    fine converged for all checked initial-condition/damping combinations.
  * GitHub remote creation remains blocked because no create-repository tool is
    available in the active plugin surface, `gh` is unavailable, and the project
    is not currently a Git repository.
  * Main PDF regenerated successfully: `peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf`,
    16 pages, A4.
  * Supplement PDF regenerated successfully:
    `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf`, 6 pages,
    A4.
  * Log scans returned no undefined references/citations, no LaTeX errors, and no
    overfull boxes.
  * `pdftotext` confirms the V&V audit, `24 of 27` convergence statement,
    restricted local re-solve boundary, reproducibility/data-availability text,
    and `run_peak_shaving_smpt_vv_audit.py` command are present in the generated
    PDFs.
  * Final gate check: `9 passed in 1.24s`; required manuscript PDFs,
    reproducibility documents, environment file, and V&V CSV are present and
    non-empty; no `REPLACE`, `TODO`, `TBD`, or `PLACEHOLDER` marker was found in
    the submission-facing files checked.
* Decision:
  * Treat the local package as GitHub-ready but not yet published.
  * Do not claim a public repository, DOI, or archived artifact until the user
    provides an existing `owner/name` repository or a GitHub CLI/authenticated
    remote workflow.
* Next:
  * If an existing GitHub repository is provided, use the GitHub plugin to upload
    the reproducibility files and create a submission-readiness issue.
  * Select a license before public release; `CITATION.cff` currently uses
    `NOASSERTION` rather than claiming an unapproved license.
* Status: verified locally; remote GitHub publication remains blocked on
  repository creation/authentication.

### 2026-06-19 23:53 - GitHub repository initialization attempt

* Goal: initialize a local Git repository for the SMPT-ready manuscript package
  and push it to `https://github.com/cccht/paper_token_price.git`.
* Context:
  * The user provided the standard GitHub empty-repository commands for
    `paper_token_price`.
  * The project README already has a title and experiment-log structure, so the
    default `echo "# paper_token_price" >> README.md` command was not run; adding
    that line at the end would make the README less clean.
* Action:
  * Prepare the existing manuscript, reproducibility documents, experiment code,
    artifacts, and figures for the first Git commit.
  * Add a root `.gitignore` for LaTeX build debris, Python caches, virtual
    environments, and local temporary files.
* Commands:
  ```powershell
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pwd && git status --short 2>/dev/null || true && git remote -v 2>/dev/null || true && command -v git && git --version && date +"%Y-%m-%d %H:%M %Z"'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && git init && git branch -M main && git add -A --dry-run | wc -l && git add -A --dry-run | sed -n "1,180p"'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && rg -n --hidden --glob "!.git/**" --glob "!*.pdf" --glob "!*.png" --glob "!*.vsdx" --glob "!*.pptx" --glob "!*.synctex*" "AKIA[0-9A-Z]{16}|OPENAI_API_KEY|ANTHROPIC_API_KEY|GITHUB_TOKEN|GH_TOKEN|sk-[A-Za-z0-9_-]{20,}|password\s*=|secret\s*=|api[_-]?key\s*=" . || true'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && git config user.name "cccht" && git config user.email "cccht@users.noreply.github.com" && git add -A && git status --short | sed -n "1,120p" && git commit -m "first commit"'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && git rm --cached -r --ignore-unmatch latex_aux "token_dynamic_pricing_game.synctex(busy)" "token_dynamic_pricing_game_sci_main.synctex(busy)" && git add .gitignore README.md && git commit --amend --no-edit && git status --short'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && git status --short && git rev-parse --short HEAD && git branch --show-current && git ls-files | wc -l && git ls-files | rg "synctex|latex_aux|\.aux$|\.log$" || true'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && git add README.md && git commit --amend --no-edit && git remote add origin https://github.com/cccht/paper_token_price.git && git remote -v && git push -u origin main'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'kill 2996360 2>/dev/null || true; sleep 1; ps -ef | grep "[g]it push" || true'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && GIT_TERMINAL_PROMPT=0 git push -u origin main'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && GIT_TERMINAL_PROMPT=0 git ls-remote --heads origin main || true'
  ```
* Result:
  * The target directory is `/root/paper_code/0427_tokenrl/paper_token_cross_survey`.
  * The directory was not yet a Git working tree.
  * Git is available in WSL: `git version 2.34.1`.
  * After adding `.gitignore`, the dry-run first commit contains `306` files
    rather than the initial `4543`; local dependency caches, dated archive
    snapshots, rewrite workspaces, LaTeX build debris, Python caches, and
    non-peak-shaving historical artifacts are excluded.
  * Lightweight credential scan found no typical API-key, GitHub-token,
    password, or cloud-secret pattern in submission-facing text files.
  * Local-only Git identity was configured for this repository:
    `cccht <cccht@users.noreply.github.com>`.
  * The initial commit was created with message `first commit`, then amended to
    remove `latex_aux/` and `*.synctex*` build debris from the tracked set.
  * The repository is on branch `main`, with `302` tracked files and no tracked
    `.aux`, `.log`, `latex_aux`, or `synctex` build artifacts. Use
    `git rev-parse --short HEAD` to check the current amended commit.
  * Remote `origin` was added as
    `https://github.com/cccht/paper_token_price.git`.
  * The first interactive HTTPS push hung waiting for credentials and was
    stopped. A non-interactive retry failed with:
    `fatal: could not read Username for 'https://github.com': terminal prompts disabled`.
  * GitHub plugin metadata confirms that `cccht/paper_token_price` exists,
    is public, and the plugin has repository permissions, but the exposed plugin
    tools do not provide a full Git push path for this binary-containing
    manuscript package.
  * `git ls-remote --heads origin main` returned no `main` reference, confirming
    that the local commit has not reached the remote repository yet.
* Next:
  * Authenticate Git from WSL, for example with GitHub CLI, Git Credential
    Manager, or a token-backed HTTPS remote, then rerun `git push -u origin main`.
  * Alternatively, provide a GitHub workflow that accepts the local commit
    bundle; the current plugin can update text files in an existing repository
    but is not sufficient for the full PDF/figure artifact upload.
* Status: local repository and first commit prepared; remote push blocked by
  missing Git HTTPS credentials in WSL.

### 2026-06-20 00:38 - GitHub CLI credential configuration attempt

* Goal: configure WSL Git credentials directly so the local `main` branch can be
  pushed to `https://github.com/cccht/paper_token_price.git`.
* Context:
  * WSL had no existing Git credential helper, no SSH private key, and no
    authenticated GitHub CLI session.
  * SSH authentication to `git@github.com` failed with `Permission denied
    (publickey)`.
  * The active GitHub plugin can inspect the repository and has repository
    permissions, but the plugin does not expose SSH-key management and is not a
    drop-in replacement for local `git push` credentials.
* Actions:
  * Installed GitHub CLI from the configured Ubuntu package source.
  * Tried `gh auth setup-git`; it correctly reported that no GitHub host was
    logged in.
  * Started GitHub device-flow authentication and opened
    `https://github.com/login/device` through Windows.
  * Polled GitHub for five minutes without printing or storing any token in the
    repository.
* Commands:
  ```powershell
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'apt-get update >/tmp/apt_update_gh.log && apt-get install -y gh >/tmp/apt_install_gh.log && gh --version | sed -n "1,3p"'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'gh auth status 2>&1 | sed -n "1,80p"'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'gh auth setup-git 2>&1 | sed -n "1,80p"; true'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'ssh -o BatchMode=yes -o StrictHostKeyChecking=accept-new -T git@github.com 2>&1 | sed -n "1,20p"'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'python3 - <<"...device-flow request omitted from README to avoid copying transient device_code..."'
  wsl.exe -d Ubuntu-22.04 -- bash -lc '/mnt/c/Windows/System32/cmd.exe /c start "" "https://github.com/login/device" >/tmp/open_github_device.log 2>&1 || true'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'python3 - <<"...device-flow polling omitted from README to avoid copying transient device_code..."'
  ```
* Results:
  * GitHub CLI installed: `gh version 2.4.0+dfsg1`.
  * `gh auth status`: `You are not logged into any GitHub hosts`.
  * `gh auth setup-git`: refused because no GitHub host is logged in.
  * Device-flow polling ended with
    `{"error": "timeout_waiting_for_authorization", "last_error": "authorization_pending"}`.
* Decision:
  * Do not store a token manually or fabricate credentials.
  * The repository is locally configured and ready, but completing GitHub auth
    requires the account owner to approve the GitHub device-flow page or provide
    a token through a secure channel.
* Next:
  * Rerun device-flow authentication and approve it in the browser, or provide a
    GitHub PAT with `repo` scope through a secure one-time channel.
  * After `gh auth status` reports a logged-in GitHub host, run
    `gh auth setup-git` and `git push -u origin main`.
* Status: blocked on GitHub account authorization.

### 2026-06-20 01:02 - GitHub authentication and first remote push

* Goal: complete GitHub authentication through an alternative route and push the
  local manuscript repository to `cccht/paper_token_price`.
* Context:
  * The first GitHub device-flow attempt succeeded only after adding
    `read:org`, but the Ubuntu-packaged `gh 2.4.0` did not provide a clean Git
    credential response for HTTPS pushes.
  * Global Git config contained a URL-specific helper installed by
    `gh auth setup-git`, but that old helper returned an unsupported `erase`
    operation path during failed pushes.
* Actions:
  * Re-ran GitHub device-flow login with `repo read:org`.
  * Verified that the stored GitHub token can access `cccht/paper_token_price`
    through the GitHub API and has repository push permission.
  * Configured a repository-local credential helper that reads the token from
    `~/.config/gh/hosts.yml` at Git credential time. The token is not stored in
    the repository and is not printed in logs.
  * Pushed the local `main` branch to GitHub.
* Commands:
  ```powershell
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && gh auth status 2>&1 | sed -n "1,80p"'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && printf "protocol=https\nhost=github.com\n\n" | git credential fill | awk -F= "/^password=/{print \"password_length=\" length(\$2)} /^username=/{print}" && GIT_TERMINAL_PROMPT=0 git push -u origin main'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && git ls-remote --heads origin main'
  ```
* Results:
  * GitHub login status reports `Logged in to github.com as cccht`.
  * Git credential fill returns `username=x-access-token` and a non-empty
    password without printing the token.
  * Push succeeded:
    `Branch 'main' set up to track remote branch 'main' from 'origin'.`
  * Remote branch confirmed:
    `ca720396616762c9ee35a59618b784d230c00baa refs/heads/main`.
* Decision:
  * Keep the repository-local helper because it avoids storing the token in Git
    config while bypassing the old `gh auth git-credential` behavior.
  * Do not amend the already-pushed first commit; record this successful
    authentication step as a normal follow-up commit.
* Next:
  * Commit and push this README authentication record.
  * Re-run the focused SMPT test after the README commit to confirm local
    research code is unchanged.
* Status: first remote push verified; README record pending commit.

### 2026-06-20 01:05 - SMPT manuscript fit polishing

* Goal: continue improving the English SMPT-targeted manuscript after the first
  GitHub push by making the paper read more clearly as a simulation-modelling
  contribution rather than as a narrow pricing-game report.
* Context:
  * The target journal remains Simulation Modelling Practice and Theory.
  * Elsevier's journal scope emphasizes original, high-quality work on systems
    simulation and modelling, with application papers making model development,
    computer implementation, V&V, experimental design, and applicability clear.
  * The current manuscript already contains these ingredients, but several parts
    are still distributed across the introduction, solver, V&V, and artifact
    sections.
* Actions planned:
  * Add explicit simulation research questions and clarify the paper's simulation
    contribution in the introduction.
  * Separate related-work positioning from the introduction narrative.
  * Retitle and sharpen model, implementation, and V&V sections to match SMPT
    expectations.
  * Add an experimental-design paragraph that names factors, baselines, output
    measures, and evidence layers.
  * Replace the old local-only data-availability sentence with the now-public
    GitHub repository URL while keeping the DOI limitation explicit.
* Command:
  ```powershell
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && git status --short && git rev-parse --short HEAD && git remote -v && date +"%Y-%m-%d %H:%M %Z"'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && rg -n -F "\\section" peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex && rg -n "RQ[0-9]|Related Work|Conceptual Simulation Model|Credibility Boundaries|github.com/cccht" peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex DATA_AVAILABILITY.md REPRODUCIBILITY.md'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_smpt_polish_main1.log && bibtex peak_shaving_dynamic_pricing_sci_en_2026-06-19 >/tmp/ps_smpt_polish_bib.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_smpt_polish_main2.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex >/tmp/ps_smpt_polish_main3.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_smpt_polish_supp1.log && xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex >/tmp/ps_smpt_polish_supp2.log'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" peak_shaving_dynamic_pricing_sci_en_2026-06-19.log peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.log /tmp/ps_smpt_polish_bib.log /tmp/ps_smpt_polish_main3.log /tmp/ps_smpt_polish_supp2.log || true'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdfinfo peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf | grep -E "^(Pages|Page size):" && pdfinfo peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf | grep -E "^(Pages|Page size):"'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && pdftotext peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf /tmp/ps_smpt_polish_main.txt && pdftotext peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf /tmp/ps_smpt_polish_supp.txt && grep -nE "RQ1|Related Work and Positioning|Conceptual Simulation Model|Verification, Validation, and Credibility Boundaries|https://github.com/cccht/paper_token_price|living reproducibility package|public repository" /tmp/ps_smpt_polish_main.txt /tmp/ps_smpt_polish_supp.txt | head -120'
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && python3 - <<"PY"
import re
text=open("peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex", encoding="utf-8").read().lower()
terms=["robust","therefore","thus","moreover","furthermore","additionally","highlight","underscore","crucial","important","novel","framework","mechanism","diagnostic","boundary","not only","it is worth noting"]
for term in terms:
    print(f"{term}: {len(re.findall(re.escape(term), text))}")
PY'
  ```
* Result:
  * Repository is on pushed commit `cc31c28` before this manuscript-polishing pass.
  * Remote origin is `https://github.com/cccht/paper_token_price.git`.
  * Main manuscript changes:
    - Added explicit simulation research questions RQ1--RQ3.
    - Split `Related Work and Positioning` into its own section.
    - Retitled the model, implementation, and V&V sections to better match an
      application-oriented simulation paper.
    - Added an experimental-design paragraph naming evidence layers and output
      measures.
    - Replaced the local-only artifact statement with the public GitHub
      repository URL while keeping the archival DOI boundary.
  * Companion-file changes:
    - Updated `DATA_AVAILABILITY.md`, `REPRODUCIBILITY.md`, and the supplement
      reproduction section to point to `https://github.com/cccht/paper_token_price`.
  * Compile result:
    - Main PDF regenerated: `peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf`,
      16 pages, A4.
    - Supplement PDF regenerated:
      `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf`, 6 pages,
      A4.
    - Log scans returned no undefined references/citations, no LaTeX errors, and
      no overfull boxes.
  * PDF text check confirms RQ1, `Related Work and Positioning`,
    `Conceptual Simulation Model`, `Verification, Validation, and Credibility
    Boundaries`, the GitHub URL, and the supplement repository statement are
    present in the generated PDFs.
  * Humanizer-style term scan found no high-risk filler such as `Furthermore`,
    `Moreover`, `Additionally`, `highlight`, `underscore`, or `It is worth
    noting`; repeated `diagnostic` and `boundary` terms are retained because they
    name the paper's solver and evidence-limit concepts.
* Status: verified locally; commit and push pending.

## Manuscript Build


Active manuscripts (share the same data, identical quantitative claims):

| File | Language | Target |
|------|----------|--------|
| `token_dynamic_pricing_game_sci_main.tex` | Chinese | Chinese journals |
| `token_dynamic_pricing_game_sci_main_en.tex` | English | EJOR / English SCI journals |
| `token_dynamic_pricing_game_supplement.tex` | Chinese | Supplementary material |

Compile with XeLaTeX and BibTeX:

```bash
# Chinese version
xelatex -interaction=nonstopmode token_dynamic_pricing_game_sci_main.tex
bibtex token_dynamic_pricing_game_sci_main
xelatex -interaction=nonstopmode token_dynamic_pricing_game_sci_main.tex
xelatex -interaction=nonstopmode token_dynamic_pricing_game_sci_main.tex

# English version
xelatex -interaction=nonstopmode token_dynamic_pricing_game_sci_main_en.tex
bibtex token_dynamic_pricing_game_sci_main_en
xelatex -interaction=nonstopmode token_dynamic_pricing_game_sci_main_en.tex
xelatex -interaction=nonstopmode token_dynamic_pricing_game_sci_main_en.tex
```

## GPU Measurements

GPU measurements are intentionally separate from the CPU bundle because they
require local model weights, an RTX 4090, and a running Ollama or vLLM server.
The exact commands and artifact directories are documented in:

- `docs/system-benchmark.md`
- `docs/vllm-system-benchmark.md`

The manuscript treats these measurements as congestion checks. They do not
constitute production-trace calibration or user price-elasticity estimation.
