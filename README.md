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
  * A common credential-pattern scan was run before commit; no repository secret
    values were found.
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
  wsl.exe -d Ubuntu-22.04 -- bash -lc 'cd /root/paper_code/0427_tokenrl/paper_token_cross_survey && GIT_TERMINAL_PROMPT=0 git push -u origin main'
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

### 2026-06-20 11:08 - Full-paper SMPT language polishing

* Goal: polish the English main manuscript for submission to Simulation Modelling
  Practice and Theory, focusing on academic English, terminology consistency,
  paragraph logic, and simulation-modelling style.
* Constraints:
  * Do not change technical meaning, numerical results, equations, table values,
    figure references, labels, citation keys, or bibliography style.
  * Do not add experiments, citations, or new claims.
  * Preserve the bounded interpretation: simulation mechanism evidence,
    finite-grid QoS protection, synthetic economic calibration, and non-robust
    profit improvement.
* Skills used:
  * `journal-adapt`: applied hard-preserve principles and journal-fit framing.
  * `nature-polishing`: applied research/methods paper, abstract, introduction,
    methods, results, discussion, conclusion, English, and generic-journal
    polishing rules.
  * `humanizer`: applied AI-pattern cleanup, including avoiding inflated
    significance language, filler transitions, negative parallelisms, and
    excessive hedging.
* Planned actions:
  * Rewrite the abstract as context/problem, objective, approach, results, and
    bounded implication.
  * Tighten the introduction and related-work transition around the simulation
    contribution.
  * Improve methods, V&V, experimental design, results, discussion, limitations,
    and conclusion for flow and reproducibility.
  * Compile, scan logs, extract PDF text, run focused tests, and push the result.
* Action:
  * Edited `peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex` for full-paper
    SMPT language polishing.
  * Expanded first-use abbreviations where needed, including artificial
    intelligence, GPU, API, QoS, SLA, and DOI in the manuscript flow.
  * Reworked the abstract, introduction, related-work positioning, computational
    implementation, verification/validation discussion, results interpretation,
    limitations, conclusion, and artifact statement without changing equations,
    table values, figure labels, citation keys, or bibliography style.
* Output:
  * `peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex`
  * `peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf`
  * `peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.pdf`
* Verification:
  * Consistency check:
    ```bash
    uv run python - <<'PY'
    import re, subprocess, pathlib, collections

    path = 'peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex'
    old = subprocess.check_output(['git', 'show', f'HEAD:{path}'], text=True)
    new = pathlib.Path(path).read_text()
    slash = chr(92)
    patterns = {
        'cite_keys': re.escape(slash + 'cite') + r'[{]([^}]*)[}]',
        'labels': re.escape(slash + 'label') + r'[{]([^}]*)[}]',
        'refs': re.escape(slash + 'ref') + r'[{]([^}]*)[}]',
        'numbers': r'(?<![A-Za-z])[-+]?[0-9]+(?:[.][0-9]+)?%?',
    }
    for name, pat in patterns.items():
        def items(text):
            out = []
            for match in re.findall(pat, text):
                if name == 'cite_keys':
                    out.extend(x.strip() for x in match.split(',') if x.strip())
                else:
                    out.append(match)
            return collections.Counter(out)
        a, b = items(old), items(new)
        print(name, 'unchanged' if a == b else 'changed', sum(a.values()))
    PY
    ```
    Result: citation keys unchanged (42), labels unchanged (28), refs
    unchanged (4), numeric tokens unchanged (279). An initial local regex
    version of this check failed before being corrected; it did not modify any
    files.
  * LaTeX build:
    ```bash
    xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex
    bibtex peak_shaving_dynamic_pricing_sci_en_2026-06-19
    xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex
    xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex
    xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex
    xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.tex
    ```
    Result: main manuscript compiled to 16 A4 pages; supplement compiled to 6
    A4 pages.
  * Log scan:
    ```bash
    LC_ALL=C grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined|Warning: Citation|Warning: Reference" \
      peak_shaving_dynamic_pricing_sci_en_2026-06-19.log \
      peak_shaving_dynamic_pricing_sci_en_supplement_2026-06-19.log || true
    ```
    Result: no undefined references/citations, no LaTeX errors, and no overfull
    boxes. One wider `/tmp` log-scan command timed out and one WSL call returned
    a transient `E_UNEXPECTED`; the final project-log scan succeeded.
  * PDF text check:
    ```bash
    pdftotext peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf /tmp/ps_full_polish_main.txt
    rg -n "Quality-of-Service Protection|application programming interface|markets for artificial intelligence services|quality-of-service|Verification, Validation|Profit improvement is not treated|continuous-space equilibrium|public repository|digital object identifier|AI-assisted" /tmp/ps_full_polish_main.txt
    ```
    Result: polished title, abbreviation expansion, validation section,
    profit-boundary wording, continuous-space boundary, repository statement,
    DOI statement, and AI declaration are present in the generated PDF.
  * Focused regression test:
    ```bash
    uv run pytest tests/test_peak_shaving_smpt_experiments.py -q
    ```
    Result: `9 passed in 1.42s`.
  * Language and diff checks:
    ```bash
    git diff --check
    rg -n "Furthermore|Moreover|Additionally|It is worth noting|not subtle|lesson is practical|highlight|underscore|pivotal|testament|as an AI|in conclusion,|delve|crucial|robust robust" peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex || true
    ```
    Result: no whitespace errors and no high-risk AI-style phrases from the
    scan list.
* Decision: keep this as the SMPT-polished full-paper version. The work remains
  a language and expression polish; no new experiments or claims were added.
* Status: verified locally and included in the SMPT language-polishing commit.

### 2026-06-20 11:54 - External SMPT polished draft review

* Goal: review the user-provided external draft
  `C:/Users/cccht/Downloads/peak_shaving_dynamic_pricing_SMPT_polished.tex`
  against the current repository manuscript for SMPT submission readiness.
* Context:
  * The external draft is a polished English LaTeX manuscript, not a simple
    line-level edit of the repository main manuscript.
  * Existing repository status already showed
    `peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf` as modified before this
    review; this review did not touch or revert that file.
* Skills used:
  * `nature-reviewer`: reviewer-style evidence and claim-risk assessment.
  * `nature-polishing`: structure, section-job, terminology, and journal-style
    assessment.
  * `humanizer`: AI-style phrase and rhythm scan.
* Commands:
  ```bash
  nl -ba /mnt/c/Users/cccht/Downloads/peak_shaving_dynamic_pricing_SMPT_polished.tex | sed -n "1,380p"
  uv run python - <<'PY'
  # Extract title, abstract, keywords, section headings, term counts, and compare
  # citation keys, labels, refs, and numeric tokens against the repository main tex.
  PY
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/ps_candidate_build -jobname=ps_candidate /mnt/c/Users/cccht/Downloads/peak_shaving_dynamic_pricing_SMPT_polished.tex
  cd /tmp/ps_candidate_build && BIBINPUTS=/root/paper_code/0427_tokenrl/paper_token_cross_survey: bibtex ps_candidate
  cd /root/paper_code/0427_tokenrl/paper_token_cross_survey
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/ps_candidate_build -jobname=ps_candidate /mnt/c/Users/cccht/Downloads/peak_shaving_dynamic_pricing_SMPT_polished.tex
  xelatex -interaction=nonstopmode -halt-on-error -output-directory=/tmp/ps_candidate_build -jobname=ps_candidate /mnt/c/Users/cccht/Downloads/peak_shaving_dynamic_pricing_SMPT_polished.tex
  LC_ALL=C grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined|Warning: Citation|Warning: Reference" /tmp/ps_candidate_build/ps_candidate.log /tmp/ps_candidate_xelatex5.log || true
  pdftotext /tmp/ps_candidate_build/ps_candidate.pdf /tmp/ps_candidate_final.txt
  ```
* Findings:
  * The external draft compiled cleanly after running BibTeX from the temporary
    build directory with `BIBINPUTS` pointing to the repository bibliography.
    Final PDF: 16 A4 pages.
  * The draft improves readability, section titles, abstract compactness, and
    discussion clarity.
  * It removes or compresses several repository evidence blocks: the standalone
    related-work section, standalone verification/validation section, SMPT
    baseline diagnostics, structural ablations, phase grid, restricted local
    re-solve, reproducibility/data-availability section, AI declaration, and
    the `20260619_smpt` artifact mapping.
  * Compared with the repository main tex, citation keys changed from 42 to 46:
    the external draft adds `allcott2011rethinking` and repeats three
    electricity-pricing references in the integrated literature paragraph.
  * Labels changed from 28 to 24, removing `sec:related`, `sec:vv`,
    `tab:smpt_baselines`, and `fig:smpt_phase`.
  * Numeric-token comparison changed from 279 to 255, mainly because evidence
    tables and sensitivity/diagnostic details were removed or condensed.
* Decision:
  * The external draft is stronger as a readable narrative draft.
  * It is weaker as a defensible SMPT submission package unless the removed
    verification, baseline, ablation, phase-grid, and artifact-availability
    evidence is restored.
  * Recommended use: selectively borrow its abstract, section-title rhythm, and
    discussion wording, but do not replace the current repository manuscript
    wholesale.
* Status: reviewed; no manuscript files were modified in this step.

### 2026-06-20 12:24 - Optimized manuscript copy and figure/table audit

* Goal:
  * Save the user-provided polished SMPT manuscript as a dated optimized version
    in the paper directory.
  * Audit every figure and table in that optimized version for references,
    captions, content consistency, necessity, and publication-format readiness.
* Source:
  * `C:/Users/cccht/Downloads/peak_shaving_dynamic_pricing_SMPT_polished.tex`
* Target:
  * `peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex`
* Context:
  * The repository already had modified `README.md` review notes and a modified
    `peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf` before this step.
  * This audit does not revert or overwrite the current repository main
    manuscript.
* Planned checks:
  * Compile the optimized manuscript with XeLaTeX and BibTeX.
  * Extract figure/table labels, captions, and in-text references.
  * Verify that included graphics files exist and inspect PDF/vector properties.
  * Compare captions and surrounding discussion against the reported numerical
    claims.
* Action:
  * Saved the external polished manuscript as
    `peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex`.
  * Preserved the source file contents initially by direct copy; SHA-256 matched
    the Downloads source before later mathematical additions.
  * Added in-paper formula and calculation details so the PDF is self-contained:
    QoS fixed-point iteration, intermediary channel QoS and profit, system
    profit, finite-grid provider payoff, pure-strategy Nash condition,
    pure/mixed regret, reported metrics, and demand-centroid shift.
  * Clarified why the paper reports finite-grid exploitability rather than a
    closed-form continuous-strategy Nash equilibrium.
  * Added explicit text references for every optimized-version figure/table and
    corrected the QoS-profile caption from a QoS threshold wording to the
    utilization threshold at which QoS degradation begins.
* Commands:
  ```bash
  cp -p /mnt/c/Users/cccht/Downloads/peak_shaving_dynamic_pricing_SMPT_polished.tex \
    peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex
  sha256sum /mnt/c/Users/cccht/Downloads/peak_shaving_dynamic_pricing_SMPT_polished.tex \
    peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_opt_math_build_20260620_1233 \
    -jobname=ps_optimized_math \
    peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex
  cd /tmp/ps_opt_math_build_20260620_1233
  BIBINPUTS=/root/paper_code/0427_tokenrl/paper_token_cross_survey: bibtex ps_optimized_math
  cd /root/paper_code/0427_tokenrl/paper_token_cross_survey
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_opt_math_build_20260620_1233 \
    -jobname=ps_optimized_math \
    peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_opt_math_build_20260620_1233 \
    -jobname=ps_optimized_math \
    peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex
  cp /tmp/ps_opt_math_build_20260620_1233/ps_optimized_math.pdf \
    peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.pdf
  ```
* Verification:
  * Optimized PDF generated successfully:
    `peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.pdf`, 17 A4 pages.
  * Final log scan found no undefined references/citations, no LaTeX errors, and
    no overfull boxes.
  * PDF text check confirms the following text entered the generated PDF:
    `finite-game equilibrium`, `pure-strategy Nash`, `closed-form Nash`,
    `exploitability certificate`, `reported indicators`, and
    `demand-centroid shift`.
  * Figure/table reference audit:
    all optimized-version figure/table labels are explicitly referenced in the
    manuscript: `fig:market_schematic`, `fig:vllm_qos_anchor`,
    `tab:uncongested`, `tab:congested`, `tab:evidence_boundary`,
    `fig:qos_profiles`, `fig:profit_regret`, `fig:mixed_oracle`,
    `fig:parameter_sweep`, and `fig:mechanism`.
  * Figure format audit:
    all included figures exist as vector PDF files. Most Matplotlib-generated
    figures still embed Type 3 fonts; `vllm_qos_anchor.pdf` has a crowded legend
    and `parameter_sweep_qos.pdf` has dense rotated x-axis labels. These are
    remaining production-quality issues if the figures are regenerated later.
* Decision:
  * Do not add a fake closed-form Nash derivation. The correct statement is a
    restricted finite-game equilibrium certificate with pure and mixed regret.
  * Keep the new equations in the optimized manuscript to make the PDF
    self-contained for reviewers.
* Status: verified locally; files are not yet committed.

### 2026-06-20 13:05 - SMPT theory-method internal reviewer audit

* Goal:
  * Review the optimized SMPT manuscript from a Simulation Modelling Practice
    and Theory reviewer perspective, focusing only on theory, simulation method,
    experiment design, and theory-experiment alignment.
* Input:
  * `peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex`
  * `peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.pdf`
* Action:
  * Used the `nature-reviewer` skill in a journal-specific internal-review mode.
  * Checked the optimized manuscript equations, solution-method wording,
    validation-anchor paragraph, congested/uncongested results, stress tests,
    limitations, and artifact-availability section.
  * Compared the optimized manuscript against SMPT's stated emphasis on
    modelling/simulation contributions, validation and verification methods,
    experimental design, and transparent model implementation.
* Read-only commands:
  ```bash
  nl -ba peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex | sed -n '45,470p'
  nl -ba peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex | sed -n '247,306p'
  rg -n "tab:smpt|fig:smpt|ablation|Validation|verification|20260619_smpt|supplement" \
    peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex \
    peak_shaving_dynamic_pricing_sci_en_2026-06-19.tex README.md
  ```
* Result:
  * Internal recommendation: major revision before SMPT submission.
  * Strongest current evidence: bounded QoS improvement in the congested
    fixed-capacity regime, supported by coarse/fine snapshots and a low-regret
    finite-grid mixed diagnostic.
  * Main remaining weaknesses: incomplete finite-grid specification in the main
    paper, missing/condensed V&V and SMPT baseline/ablation evidence in the
    optimized version, synthetic calibration limits, fixed-policy stress tests
    not being cross-parameter equilibrium re-solves, and figure typography
    issues.
* Decision:
  * Treat the current optimized manuscript as a strong middle draft, not as the
    final submission file.
  * The next revision should restore or integrate the full SMPT evidence layer
    from the repository manuscript: standalone V&V, baseline diagnostics,
    structural ablations, phase grid, restricted local re-solve, and artifact
    mapping to `20260619_smpt`.
* Status: reviewed; no manuscript files were modified in this step.

### 2026-06-20 13:18 - SMPT final manuscript integration plan

* Goal:
  * Convert the optimized SMPT manuscript into a final-submission candidate.
  * Preserve the improved English and self-contained equations from the
    optimized manuscript while restoring the SMPT evidence layer that reviewers
    need for theory-method credibility.
* Boundary:
  * No new core equilibrium experiment will be run in this step.
  * Existing JSON/CSV artifacts, tables, and figure data are treated as the
    source of record.
  * A new final TeX/PDF will be created instead of overwriting the optimized
    manuscript.
* Planned target:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
* Planned edits:
  * Add the `figures/peak_shaving_smpt/` graphics path.
  * Restore a standalone verification, validation, and credibility-boundary
    section.
  * Add a reproducibility/parameter-grid table in the main paper.
  * Integrate SMPT baseline diagnostics, structural ablations, the
    capacity--elasticity phase grid, and restricted local re-solve evidence.
  * Correct artifact availability so it points to the English supplement and
    the `20260619_smpt` artifact directory.
  * Recheck figure references, citation/reference status, LaTeX logs, PDF text,
    and figure font/readability issues.
* Actions completed so far:
  * Created `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex` from the
    optimized manuscript.
  * Added the missing demand-market-size equation, finite-grid table,
    verification/validation section, main-parameter table, SMPT baseline
    diagnostics, structural ablations, phase grid, restricted local re-solve
    table, updated limitations, and corrected artifact availability.
  * Updated Matplotlib figure scripts to embed TrueType fonts rather than Type 3
    fonts.
* Figure regeneration commands:
  ```bash
  uv run python experiments/build_peak_shaving_diagnostics.py
  uv run python experiments/run_peak_shaving_mixed_oracle.py
  # The full mixed-oracle command was stopped after exceeding 180 s; the existing
  # verified JSON trace was used to redraw only mixed_oracle_regret.pdf.
  uv run python - <<'PY'
  import json
  from pathlib import Path
  import matplotlib
  matplotlib.use("Agg")
  import matplotlib.pyplot as plt
  plt.rcParams.update({"font.family":"DejaVu Sans","pdf.fonttype":42,"ps.fonttype":42})
  result=json.loads(Path("artifacts/peak_shaving/20260619_submission/peak_shaving_mixed_oracle.json").read_text())
  xs=[r["oracle_round"] for r in result["trace"]]
  ys=[r["full_max_regret"] for r in result["trace"]]
  fig, ax=plt.subplots(figsize=(6.2,3.4))
  ax.plot(xs, ys, marker="o", color="#0072B2")
  ax.axhline(5.0, color="#666666", ls="--", lw=1, label="target < 5")
  ax.set_xlabel("Double-oracle round")
  ax.set_ylabel("Full-grid max regret")
  ax.grid(alpha=0.25)
  ax.legend(frameon=False)
  fig.tight_layout()
  fig.savefig("figures/peak_shaving_submission/mixed_oracle_regret.pdf")
  plt.close(fig)
  PY
  uv run python experiments/run_peak_shaving_parameter_sweep.py
  uv run python experiments/run_peak_shaving_smpt_experiments.py
  find figures/peak_shaving_diagnostics figures/peak_shaving_submission figures/peak_shaving_smpt \
    -name "*.pdf" -print0 | xargs -0 -I{} sh -c 'echo ==== {}; pdffonts "{}" | sed -n "1,8p"'
  ```
* Figure regeneration result:
  * `build_peak_shaving_diagnostics.py` succeeded with no validation warnings.
  * `run_peak_shaving_parameter_sweep.py` regenerated 27 rows and
    `parameter_sweep_qos.pdf`; both dynamic snapshots keep positive QoS gains
    and peak-utilization reductions in all 9 scenarios.
  * `run_peak_shaving_smpt_experiments.py` regenerated the SMPT bundle with 7
    baseline rows, 6 ablation rows, 25 phase-grid rows, and 5 restricted
    re-solve rows.
  * `pdffonts` confirms the final referenced figure PDFs now embed CID TrueType
    fonts; no remaining Type 3 figure fonts were observed.
* Final compile and verification commands:
  ```bash
  rm -rf /tmp/ps_smpt_final_build_20260620
  mkdir -p /tmp/ps_smpt_final_build_20260620
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_final_build_20260620 \
    -jobname=ps_smpt_final \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  cd /tmp/ps_smpt_final_build_20260620
  BIBINPUTS=/root/paper_code/0427_tokenrl/paper_token_cross_survey: bibtex ps_smpt_final
  cd /root/paper_code/0427_tokenrl/paper_token_cross_survey
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_final_build_20260620 \
    -jobname=ps_smpt_final \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_final_build_20260620 \
    -jobname=ps_smpt_final \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  cp /tmp/ps_smpt_final_build_20260620/ps_smpt_final.pdf \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" \
    /tmp/ps_smpt_final_build_20260620/ps_smpt_final.log /tmp/ps_smpt_final_xe3.log || true
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | grep -E "^(Pages|Page size):"
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_smpt_final_text.txt
  pdffonts peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  uv run python -m py_compile \
    experiments/build_peak_shaving_diagnostics.py \
    experiments/run_peak_shaving_mixed_oracle.py \
    experiments/run_peak_shaving_parameter_sweep.py \
    experiments/run_peak_shaving_smpt_experiments.py
  uv run pytest \
    tests/test_peak_shaving_smpt_experiments.py \
    tests/test_peak_shaving_submission_tools.py \
    tests/test_peak_shaving_measurement_anchor.py -q
  ```
* Final verification result:
  * Final PDF generated: `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`,
    21 A4 pages.
  * Final log scan found no undefined references/citations, no LaTeX errors, and
    no overfull boxes.
  * Figure/table label audit found 17 figure/table labels, no unreferenced
    labels, and no duplicate labels.
  * `pdftotext` confirms that the final PDF contains the finite-grid table,
    standalone V&V section, fixed-point verification table, SMPT baseline
    diagnostics, structural ablations, phase grid, restricted local re-solve,
    reproducibility/data-availability statement, and AI-assisted-technologies
    declaration.
  * Final PDF font scan found embedded Type 1/CID/TrueType fonts and no Type 3
    fonts in the generated figure layer.
  * Contact-sheet visual inspection did not show blank pages, missing figures,
    or obvious table overflow.
  * Targeted code checks passed: `15 passed in 2.11s`.
* Remaining boundary:
  * The manuscript is now a final-submission candidate, but a formal journal
    upload should still freeze the GitHub repository into a release or DOI.
  * The full mixed-oracle recomputation exceeded 180 s in this run, so only the
    previously verified mixed-oracle JSON trace was used for figure redrawing.
    No mixed-oracle numerical claim was changed.
  * The repository already had an unrelated modified
    `peak_shaving_dynamic_pricing_sci_en_2026-06-19.pdf` before this final-file
    integration; it was not reverted.
* Status: verified locally.

### 2026-06-20 13:12 - Chinese TeX translation for author review

* Goal:
  * Create a Chinese TeX translation of the final SMPT manuscript so the author
    can review the paper in Chinese.
* Input:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
* Planned output:
  * `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex`
  * `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf`
* Constraints:
  * Preserve formulas, numerical results, labels, figure/table structure,
    citations, and the stated evidence boundaries.
  * Use `ctexart` and XeLaTeX for Chinese compilation.
  * Do not overwrite the English final manuscript.
* Action:
  * Initialized and updated the lightweight `plan/` context for this longer
    writing task.
  * Created the Chinese TeX translation while preserving equations, numerical
    values, figure/table labels, citations, and artifact statements.
* Commands:
  ```bash
  rm -rf /tmp/ps_smpt_final_zh_build_20260620
  mkdir -p /tmp/ps_smpt_final_zh_build_20260620
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_final_zh_build_20260620 \
    -jobname=ps_smpt_final_zh \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  cd /tmp/ps_smpt_final_zh_build_20260620
  BIBINPUTS=/root/paper_code/0427_tokenrl/paper_token_cross_survey: bibtex ps_smpt_final_zh
  cd /root/paper_code/0427_tokenrl/paper_token_cross_survey
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_final_zh_build_20260620 \
    -jobname=ps_smpt_final_zh \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_final_zh_build_20260620 \
    -jobname=ps_smpt_final_zh \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  cp /tmp/ps_smpt_final_zh_build_20260620/ps_smpt_final_zh.pdf \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  grep -nE "undefined|Undefined|LaTeX Error|Overfull|Citation.*undefined|There were undefined" \
    /tmp/ps_smpt_final_zh_build_20260620/ps_smpt_final_zh.log \
    /tmp/ps_smpt_final_zh_xe3.log || true
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf | grep -E "^(Pages|Page size):"
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf /tmp/ps_smpt_final_zh_text.txt
  pdffonts peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  ```
* Verification:
  * Generated `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf`,
    22 A4 pages.
  * Final log scan found no undefined references/citations, no LaTeX errors,
    and no overfull boxes.
  * PDF text check confirms the Chinese title, abstract, V&V section,
    finite-grid discussion, SMPT baseline section, restricted local re-solve,
    reproducibility statement, and AI-assisted-technologies declaration.
  * Figure/table label audit found 46 labels, including 17 figure/table labels;
    no unreferenced figure/table labels and no duplicate labels were found.
  * PDF font scan shows embedded CID/Type 1C/TrueType fonts; no Type 3 fonts
    were observed.
* Status: verified locally; files are not yet committed.

### 2026-06-20 13:45 - Times New Roman figure typography pass

* Goal:
  * Regenerate all figures referenced by the final English and Chinese SMPT
    manuscripts with Times New Roman typography.
  * Adjust legends and annotations so labels do not obscure plotted lines or
    surrounding text.
* Figure scope:
  * `market_schematic.pdf`
  * `vllm_qos_anchor.pdf`
  * `qos_utilization_profiles.pdf`
  * `profit_components_and_regret.pdf`
  * `mixed_oracle_regret.pdf`
  * `parameter_sweep_qos.pdf`
  * `smpt_phase_qos_gain.pdf`
  * `smpt_phase_profit_gain.pdf`
  * `mechanism_diagnostics.pdf`
* Context:
  * `fc-match "Times New Roman"` resolves to the Windows font file
    `/mnt/c/Windows/Fonts/times.ttf` from WSL.
  * No system font installation or font configuration change is planned.
* Planned action:
  * Patch the relevant Matplotlib figure scripts to use an explicit Times New
    Roman font manager helper.
  * Move or simplify crowded labels/legends where needed.
  * Regenerate the figure PDFs and recompile the final English and Chinese
    manuscripts.
* Actions:
  * Added `experiments/plot_style.py` with an explicit Times New Roman font
    loader for `/mnt/c/Windows/Fonts/times.ttf` and related style variants.
  * Updated the peak-shaving figure scripts to use the shared Times New Roman
    style:
    `experiments/build_peak_shaving_diagnostics.py`,
    `experiments/build_peak_shaving_measurement_anchor.py`,
    `experiments/run_peak_shaving_mixed_oracle.py`,
    `experiments/run_peak_shaving_parameter_sweep.py`, and
    `experiments/run_peak_shaving_smpt_experiments.py`.
  * Adjusted crowded figure elements:
    market-schematic direct-API arrows now avoid the intermediary text,
    vLLM boundary text is moved into the legend, profit/regret legends are kept
    outside the plotting area, parameter-sweep labels are line-broken, and phase
    heatmap cell labels use contrast-aware colors.
* Commands:
  ```bash
  uv run python -m py_compile \
    experiments/plot_style.py \
    experiments/build_peak_shaving_diagnostics.py \
    experiments/run_peak_shaving_parameter_sweep.py \
    experiments/run_peak_shaving_mixed_oracle.py \
    experiments/run_peak_shaving_smpt_experiments.py \
    experiments/build_peak_shaving_measurement_anchor.py
  uv run python experiments/build_peak_shaving_diagnostics.py
  uv run python experiments/run_peak_shaving_parameter_sweep.py
  uv run python experiments/run_peak_shaving_smpt_experiments.py
  uv run python experiments/build_peak_shaving_measurement_anchor.py
  uv run python - <<'PY'
  import json
  from experiments.run_peak_shaving_mixed_oracle import plot_trace, OUT
  result = json.loads((OUT / "peak_shaving_mixed_oracle.json").read_text(encoding="utf-8"))
  plot_trace(result)
  PY
  ```
* Verification commands:
  ```bash
  python3 - <<'PY'
  from pathlib import Path
  import subprocess
  figs = [
      Path("figures/peak_shaving_diagnostics/market_schematic.pdf"),
      Path("figures/peak_shaving_submission/vllm_qos_anchor.pdf"),
      Path("figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf"),
      Path("figures/peak_shaving_diagnostics/profit_components_and_regret.pdf"),
      Path("figures/peak_shaving_submission/mixed_oracle_regret.pdf"),
      Path("figures/peak_shaving_submission/parameter_sweep_qos.pdf"),
      Path("figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf"),
      Path("figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf"),
      Path("figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf"),
  ]
  for fig in figs:
      out = subprocess.check_output(["pdffonts", str(fig)], text=True)
      assert "TimesNewRoman" in out, fig
      assert "Type 3" not in out, fig
  print("font_check=ok")
  PY
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_times_en_build_20260620 \
    -jobname=ps_smpt_times_en \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  cd /tmp/ps_smpt_times_en_build_20260620
  BIBINPUTS=/root/paper_code/0427_tokenrl/paper_token_cross_survey: bibtex ps_smpt_times_en
  cd /root/paper_code/0427_tokenrl/paper_token_cross_survey
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_times_en_build_20260620 \
    -jobname=ps_smpt_times_en \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_times_en_build_20260620 \
    -jobname=ps_smpt_times_en \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_times_zh_build_20260620 \
    -jobname=ps_smpt_times_zh \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  cd /tmp/ps_smpt_times_zh_build_20260620
  BIBINPUTS=/root/paper_code/0427_tokenrl/paper_token_cross_survey: bibtex ps_smpt_times_zh
  cd /root/paper_code/0427_tokenrl/paper_token_cross_survey
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_times_zh_build_20260620 \
    -jobname=ps_smpt_times_zh \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error \
    -output-directory=/tmp/ps_smpt_times_zh_build_20260620 \
    -jobname=ps_smpt_times_zh \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  uv run pytest \
    tests/test_peak_shaving_smpt_experiments.py \
    tests/test_peak_shaving_submission_tools.py \
    tests/test_peak_shaving_measurement_anchor.py -q
  ```
* Verification result:
  * All nine manuscript-referenced figure PDFs embed `TimesNewRomanPSMT` and no
    Type 3 fonts were observed.
  * Contact-sheet visual inspection confirmed that the revised legends and
    annotations no longer cover the main lines, bars, or diagram labels.
  * English final PDF regenerated:
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`, 21 A4 pages.
  * Chinese review PDF regenerated:
    `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf`, 21 A4 pages.
  * Final LaTeX log scan found no undefined references/citations, no LaTeX
    errors, and no overfull boxes for either PDF.
  * Targeted tests passed: `15 passed in 1.72s`.
* Status: verified locally; files are not yet committed.

### 2026-06-20 14:05 - Figure 3 and Figure 4 legend spacing refinement

* Goal:
  * Tighten the top legend spacing in Figure 3
    (`qos_utilization_profiles.pdf`) and Figure 4
    (`profit_components_and_regret.pdf`) after author review.
  * Keep Times New Roman figure typography and avoid covering plotted lines,
    bars, or subplot titles.
* Action:
  * Moved Figure 3's shared legend closer to the utilization panel.
  * Moved Figure 4's participant legend and target-regret legend into unused
    subplot space rather than above the figure, removing the excessive top gap
    while avoiding overlap with bars and the dashed target line.
  * Regenerated the diagnostic figures through
    `experiments/build_peak_shaving_diagnostics.py`.
* Commands:
  ```bash
  uv run python -m py_compile experiments/build_peak_shaving_diagnostics.py
  uv run python experiments/build_peak_shaving_diagnostics.py
  ```
* Verification:
  * Visual preview generated at `/tmp/ps_fig34_spacing_v2.png` confirmed that
    Figure 3 and Figure 4 legends are closer to the plots and do not cover the
    main lines, bars, dashed threshold, or subplot titles.
  * `pdffonts` confirms both regenerated figures still embed
    `TimesNewRomanPSMT` and no Type 3 fonts were observed.
  * Regenerated the final English and Chinese PDFs:
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` and
    `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf`, both 21 A4
    pages.
  * Final LaTeX log scan found no undefined references/citations, no LaTeX
    errors, and no overfull boxes for either PDF.
  * Targeted tests passed: `15 passed in 1.76s`.
* Status: verified locally; files are not yet committed.

### 2026-06-20 14:24 - Imagegen-inspired Figure 1 market structure redesign

* Goal:
  * Redesign Figure 1, the market-structure diagram, using an imagegen draft as
    the visual reference while keeping the manuscript figure reproducible and
    publication-ready.
* Input:
  * User-provided reference image:
    `C:/Users/cccht/AppData/Local/Temp/codex-clipboard-1bec61fd-c2ba-45be-86f1-5404b6d02c7c.png`
  * Caption requirement: users may buy through the API intermediary, connect
    directly to providers, or exit; the intermediary routes traffic between two
    providers based on prices and QoS.
* Action:
  * Generated an imagegen concept draft for a wide academic market-structure
    diagram.
  * Reimplemented the concept as a deterministic vector PDF in
    `experiments/build_peak_shaving_diagnostics.py` so text, arrows, fonts, and
    labels remain controllable in LaTeX.
  * Replaced `figures/peak_shaving_diagnostics/market_schematic.pdf` with a
    richer diagram: left user panel, center API intermediary, right Provider A/B
    panels, outside option, brokered purchase arrow, direct API dashed arrows,
    routed-traffic arrows, and QoS feedback arrows.
* Commands:
  ```bash
  uv run python -m py_compile experiments/build_peak_shaving_diagnostics.py
  uv run python experiments/build_peak_shaving_diagnostics.py
  pdffonts figures/peak_shaving_diagnostics/market_schematic.pdf
  pdftoppm -png -singlefile -r 170 \
    figures/peak_shaving_diagnostics/market_schematic.pdf \
    /tmp/ps_market_schematic_imagegen_style_v3
  ```
* Verification:
  * Visual preview `/tmp/ps_market_schematic_imagegen_style_v3.png` confirms the
    new Figure 1 structure and no obvious label collision across the main boxes,
    arrows, provider panels, or outside-option panel.
  * Figure 1 embeds `TimesNewRomanPSMT` and `TimesNewRomanPS-BoldMT`; no Type 3
    fonts were observed.
  * Regenerated the final English and Chinese PDFs:
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` and
    `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf`, both 21 A4
    pages.
  * Final LaTeX log scan found no undefined references/citations, no LaTeX
    errors, and no overfull boxes for either PDF.
  * Targeted tests passed: `15 passed in 1.74s`.
* Status: verified locally; files are not yet committed.

### 2026-06-20 20:58 - Figure 1 redraw from PDF reference

* Goal: Rebuild the manuscript Figure 1 market-structure diagram by using the
  user-provided `论文图.pdf` as the visual reference, while keeping the output as
  a reproducible vector figure.
* Context: The reference PDF uses a three-column layout: users on the left,
  cloud platform/API intermediary in the center, model/API suppliers on the
  right, and lower modelling/feedback bands for the pricing game and iterative
  equilibrium update.
* Input:
  * Reference PDF: `/mnt/c/Users/cccht/Desktop/论文图.pdf`
  * Rendered preview:
    `tmp/pdfs/reference_paper_figure_20260620-1.png`
  * Target figure:
    `figures/peak_shaving_diagnostics/market_schematic.pdf`
* Action:
  * Rendered the PDF reference with Poppler for visual inspection.
  * Decided to redraw the figure in Matplotlib rather than embedding the
    supplied PDF or a bitmap, so labels, fonts, arrows, and LaTeX scaling remain
    controllable.
* Command:
  ```bash
  pdfinfo /mnt/c/Users/cccht/Desktop/论文图.pdf
  mkdir -p tmp/pdfs
  pdftoppm -png -r 200 /mnt/c/Users/cccht/Desktop/论文图.pdf \
    tmp/pdfs/reference_paper_figure_20260620
  ```
* Result:
  * The reference PDF has one 960 x 540 pt page and was rendered successfully.
* Decision: Rework only `plot_market_schematic()` in
  `experiments/build_peak_shaving_diagnostics.py`; do not change numerical
  experiment outputs, other figures, or manuscript claims.
* Next: Use imagegen directly, then compile English and Chinese PDFs against the
  generated bitmap figure.
* Status: superseded after user clarified that Figure 1 should be generated with
  imagegen, not redrawn through Python.

### 2026-06-20 21:05 - Imagegen Figure 1 generation

* Goal: Generate Figure 1 with the built-in imagegen model using
  `论文图.pdf` as the visual reference, without using Python drawing code.
* Context: The required figure should show users, the API intermediary,
  inference providers, the time-of-use pricing game, and the iterative
  equilibrium diagnostic in a single market-structure schematic.
* Input:
  * Reference PDF: `/mnt/c/Users/cccht/Desktop/论文图.pdf`
  * Prompt source: verbal description extracted from the rendered reference
    preview and the manuscript caption for Figure 1.
* Action:
  * Used the built-in `image_gen.imagegen` tool to generate a 16:9 academic
    infographic.
  * Copied the generated PNG from the Codex generated-images directory into the
    manuscript figure directory.
  * Updated the English final, Chinese final, and optimized TeX manuscripts to
    reference the imagegen PNG directly.
* Command:
  ```powershell
  Copy-Item -LiteralPath `
    'C:\Users\cccht\.codex\generated_images\019ede62-cd93-7220-8ab0-3824ce48b294\ig_0a36fa88e496739e016a368fe5f5b0819192dd86b8ecb42538.png' `
    -Destination `
    '\\wsl.localhost\Ubuntu-22.04\root\paper_code\0427_tokenrl\paper_token_cross_survey\figures\peak_shaving_diagnostics\market_schematic_imagegen_2026-06-20.png'
  ```
* Output:
  * `figures/peak_shaving_diagnostics/market_schematic_imagegen_2026-06-20.png`
  * Updated TeX includes in:
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`,
    `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex`, and
    `peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex`.
* Result:
  * Visual preview confirms that the imagegen figure follows the supplied PDF's
    three-column layout and includes the modelling and feedback bands.
* Verification command:
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex >/tmp/ps_imagegen_final_en_xe1.log
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20 >/tmp/ps_imagegen_final_en_bib.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex >/tmp/ps_imagegen_final_en_xe2.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex >/tmp/ps_imagegen_final_en_xe3.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex >/tmp/ps_imagegen_final_zh_xe1.log
  bibtex peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20 >/tmp/ps_imagegen_final_zh_bib.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex >/tmp/ps_imagegen_final_zh_xe2.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex >/tmp/ps_imagegen_final_zh_xe3.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex >/tmp/ps_imagegen_opt_xe1.log
  bibtex peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20 >/tmp/ps_imagegen_opt_bib.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex >/tmp/ps_imagegen_opt_xe2.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex >/tmp/ps_imagegen_opt_xe3.log
  grep -nE "LaTeX Error|Undefined control sequence|undefined references|Citation .*undefined|Reference .*undefined|Overfull|Missing character" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log || true
  grep -nE "LaTeX Error|Undefined control sequence|undefined references|Citation .*undefined|Reference .*undefined|Overfull|Missing character" peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log || true
  grep -nE "LaTeX Error|Undefined control sequence|undefined references|Citation .*undefined|Reference .*undefined|Overfull|Missing character" peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.log || true
  pdfimages -list peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  pdfimages -list peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  pdftoppm -png -f 3 -l 3 -r 180 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    tmp/pdfs/final_en_imagegen_fig1_page
  pdftoppm -png -f 3 -l 3 -r 180 peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf \
    tmp/pdfs/final_zh_imagegen_fig1_page
  ```
* Verification result:
  * XeLaTeX/BibTeX compilation completed for the English final, Chinese final,
    and optimized manuscripts.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or missing-character warnings in the three checked logs.
  * `pdfimages` reports the imagegen Figure 1 on page 3 of both final PDFs, with
    an embedded image size of 1672 x 941 pixels at approximately 259 ppi.
  * Rendered page previews:
    `tmp/pdfs/final_en_imagegen_fig1_page-03.png` and
    `tmp/pdfs/final_zh_imagegen_fig1_page-03.png`.
  * Visual inspection confirms that the imagegen figure is embedded in both PDF
    manuscripts and that figure-caption placement is normal.
* Decision:
  * Keep the generated image as a project-local PNG and reference it directly
    from TeX.
  * Do not rerun the Python diagnostic-figure script for Figure 1 in this pass.
* Status: verified.

### 2026-06-20 21:18 - Figure 1 content-aligned imagegen revision

* Goal: Regenerate Figure 1 in the same visual style and overall structure as
  the supplied `论文图.pdf`, but make the content match the actual simulation
  model in the SMPT manuscript.
* Context: The prior imagegen version followed the three-column reference style
  but still contained some generic platform labels. The revised version should
  emphasize the paper's specific agents and equations: two heterogeneous
  providers, one API intermediary, time-rigid/time-flexible users, direct access,
  market exit, QoS fixed point, provider/intermediary best responses, and finite
  grid regret.
* Planned output:
  * New imagegen PNG under `figures/peak_shaving_diagnostics/`.
  * Updated Figure 1 include paths in the English final, Chinese final, and
    optimized manuscripts.
* Action:
  * Used the built-in `image_gen.imagegen` tool to create a content-aligned
    Figure 1 that preserves the supplied reference's three-column and lower-band
    layout.
  * Copied the generated image into the manuscript figure directory as a new
    versioned asset; the prior imagegen PNG was retained as a backup.
  * Updated the English final, Chinese final, and optimized manuscripts to use
    the model-aligned imagegen figure.
* Command:
  ```powershell
  Copy-Item -LiteralPath `
    'C:\Users\cccht\.codex\generated_images\019ede62-cd93-7220-8ab0-3824ce48b294\ig_0a36fa88e496739e016a36a7ae8bb48191acdc2cb1c075da41.png' `
    -Destination `
    '\\wsl.localhost\Ubuntu-22.04\root\paper_code\0427_tokenrl\paper_token_cross_survey\figures\peak_shaving_diagnostics\market_schematic_imagegen_model_aligned_2026-06-20.png'
  ```
* Output:
  * `figures/peak_shaving_diagnostics/market_schematic_imagegen_model_aligned_2026-06-20.png`
  * Updated include paths in:
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`,
    `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex`, and
    `peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex`.
* Verification command:
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex >/tmp/ps_model_aligned_en_xe1.log
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20 >/tmp/ps_model_aligned_en_bib.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex >/tmp/ps_model_aligned_en_xe2.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex >/tmp/ps_model_aligned_en_xe3.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex >/tmp/ps_model_aligned_zh_xe1.log
  bibtex peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20 >/tmp/ps_model_aligned_zh_bib.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex >/tmp/ps_model_aligned_zh_xe2.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex >/tmp/ps_model_aligned_zh_xe3.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex >/tmp/ps_model_aligned_opt_xe1.log
  bibtex peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20 >/tmp/ps_model_aligned_opt_bib.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex >/tmp/ps_model_aligned_opt_xe2.log
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex >/tmp/ps_model_aligned_opt_xe3.log
  grep -nE "LaTeX Error|Undefined control sequence|undefined references|Citation .*undefined|Reference .*undefined|Overfull|Missing character" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log || true
  grep -nE "LaTeX Error|Undefined control sequence|undefined references|Citation .*undefined|Reference .*undefined|Overfull|Missing character" peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log || true
  grep -nE "LaTeX Error|Undefined control sequence|undefined references|Citation .*undefined|Reference .*undefined|Overfull|Missing character" peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.log || true
  pdfimages -list peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  pdfimages -list peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  pdftoppm -png -f 3 -l 3 -r 180 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    tmp/pdfs/final_en_model_aligned_fig1_page
  pdftoppm -png -f 3 -l 3 -r 180 peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf \
    tmp/pdfs/final_zh_model_aligned_fig1_page
  ```
* Verification result:
  * English final, Chinese final, and optimized manuscripts compiled with
    XeLaTeX/BibTeX.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or missing-character warnings.
  * `pdfimages` reports the model-aligned Figure 1 on page 3 of the English and
    Chinese final PDFs, embedded as a 1536 x 1024 image at about 238 ppi.
  * Rendered page previews:
    `tmp/pdfs/final_en_model_aligned_fig1_page-03.png` and
    `tmp/pdfs/final_zh_model_aligned_fig1_page-03.png`.
  * Visual inspection confirms that the reference-style structure is preserved
    and the figure content now matches the manuscript's actual model objects.
* Status: verified.

### 2026-06-20 23:33 - Figure 1 manuscript-consistency audit

* Goal: Check whether the model-aligned imagegen Figure 1 matches the actual
  SMPT manuscript content.
* Context: The figure should explain the market structure and simulation
  workflow, not introduce entities or claims absent from the paper.
* Action:
  * Visually inspected
    `figures/peak_shaving_diagnostics/market_schematic_imagegen_model_aligned_2026-06-20.png`.
  * Compared figure labels and arrows against the English final manuscript's
    model, demand, QoS, profit, and solver sections.
* Command:
  ```bash
  sed -n "62,220p" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  sed -n "220,330p" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  sed -n "330,390p" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  rg -n "mixed-oracle|0\\.203|regret|fixed point|routing|QoS|capacity|outside option" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  ```
* Result:
  * Figure 1 is broadly consistent with the manuscript: the user types, outside
    option, API intermediary retail pricing/routing, provider capacity
    heterogeneity, QoS fixed point, profit accounting, finite-grid diagnostic,
    and mixed-oracle regret value all map to manuscript text.
  * Minor figure-level caveat: one small QoS-signal label is visually rendered
    like `q_{i,t}` rather than the manuscript's `q^I_t`/`q_{k,t}` notation; the
    surrounding label still conveys the intended QoS signal.
  * Incidental manuscript issues observed during the audit: the English final
    TeX currently has a duplicated `r_{m,t}` line near the routing-logit
    equation and a duplicated `\caption{Main simulation parameters...}` line in
    the main-parameter table. These are not caused by the figure, but should be
    cleaned before submission.
* Decision: The figure is suitable as a conceptual overview figure for author
  review. For a final submission version, a lower-text-density or manually
  typeset/vector version would further reduce notation and imagegen-text risks.
* Status: reviewed.

### 2026-06-21 00:52 - Draw.io Figure 1 exact-content rebuild

* Goal: Replace the imagegen-style Figure 1 draft with a Draw.io source diagram
  whose labels and symbols exactly match the SMPT manuscript model.
* Context: The user requested a fully conforming figure and explicitly asked to
  use the Draw.io skill. The figure must preserve the supplied reference's
  three-column structure while removing imagegen text ambiguity.
* Action:
  * Read the Draw.io skill workflow.
  * Rechecked the manuscript model and solver sections around Figure 1.
  * Checked for a local draw.io CLI through WSL and common Windows CLI names.
* Command:
  ```bash
  command -v drawio || true
  command -v draw.io || true
  ```
  ```powershell
  drawio --version
  draw.io --version
  "C:\Program Files\draw.io\draw.io.exe" --version
  "C:\Program Files (x86)\draw.io\draw.io.exe" --version
  ```
* Result:
  * No draw.io CLI was available on PATH or in the checked standard Windows
    locations. A broader recursive search over common installation roots timed
    out.
* Decision: Generate a standards-compliant `.drawio` XML source file and a
  matching preview PNG for review. Do not rely on imagegen text for the final
  labels.
* Generation command:
  ```bash
  uv run python -m py_compile experiments/build_market_schematic_drawio.py
  uv run python experiments/build_market_schematic_drawio.py
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio
  ```
* Output:
  * `experiments/build_market_schematic_drawio.py`
  * `figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio`
  * `figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png`
* Result:
  * The Draw.io source was generated successfully.
  * Draw.io structural validation returned `0 error(s)`. The reported overlap
    warnings are expected because the large colored panels intentionally contain
    inner cards and labels.
  * Visual preview was inspected locally. The final preview removes the
    imagegen label ambiguity and uses manuscript-aligned labels for user
    choice, intermediary pricing/routing, provider capacities/prices, QoS fixed
    point, profit, and finite-grid regret diagnostics.
* Limit:
  * The local draw.io desktop CLI is not currently available, so the PNG preview
    was generated from the same scripted layout rather than exported by draw.io
    CLI. The `.drawio` source itself is editable in draw.io.
* Status: preview_ready.

### 2026-06-21 01:20 - Draw.io Figure 1 manuscript integration check

* Goal: Make Figure 1 fully consistent with the SMPT manuscript and verify that
  the paper PDFs use the Draw.io-derived figure rather than the older imagegen
  schematic.
* Context: The user requested a fully conforming Draw.io version of the market
  structure figure. The figure needs to represent the manuscript's user choice,
  API intermediary routing, provider capacity/QoS, simulation fixed point, and
  finite-grid equilibrium diagnostic without inventing extra model entities.
* Action:
  * Tightened the mixed-oracle label box in
    `experiments/build_market_schematic_drawio.py` to avoid text touching the
    border after PDF scaling.
  * Rebuilt the `.drawio` source and preview PNG.
  * Switched Figure 1 includes in the English final, Chinese final, and
    optimized SMPT manuscripts to
    `market_schematic_drawio_exact_2026-06-21.png`.
* Command:
  ```bash
  uv run python -m py_compile experiments/build_market_schematic_drawio.py
  uv run python experiments/build_market_schematic_drawio.py
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio
  ```
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.tex
  ```
  ```bash
  rg -n "LaTeX Error|Undefined control sequence|Citation .* undefined|Reference .* undefined|There were undefined|Overfull|Package natbib Warning" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log
  rg -n "LaTeX Error|Undefined control sequence|Citation .* undefined|Reference .* undefined|There were undefined|Overfull|Package natbib Warning" \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log
  rg -n "LaTeX Error|Undefined control sequence|Citation .* undefined|Reference .* undefined|There were undefined|Overfull|Package natbib Warning" \
    peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.log
  ```
  ```bash
  pdftoppm -f 3 -l 3 -png -r 120 \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    tmp/pdfs/smpt_final_en_page3_drawio_check
  ```
* Output:
  * `figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio`
  * `figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
  * `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf`
  * `peak_shaving_dynamic_pricing_SMPT_optimized_2026-06-20.pdf`
  * `tmp/pdfs/smpt_final_en_page3_drawio_check-03.png`
* Result:
  * Script syntax check passed and the figure was regenerated.
  * Draw.io structural validation returned `0 error(s)`; warnings are expected
    containment warnings from outer panels enclosing inner cards.
  * All three manuscripts compiled successfully with XeLaTeX.
  * Log scans found no LaTeX errors, undefined references/citations, natbib
    warnings, or overfull boxes.
  * The rendered English PDF page confirms that Figure 1 uses the new
    Draw.io-derived schematic.
* Note:
  * An initial log-scan command failed because the `Overfull \hbox` regular
    expression was not escaped correctly. The corrected scans above were rerun
    and are the recorded verification evidence.
  * The figure is information-dense but readable as a full-width structural
    schematic. If a target journal asks for single-column print legibility, the
    same `.drawio` source can be split into two subfigures.
* Status: verified.

### 2026-06-21 01:45 - Electricity pricing structure benchmark and SMPT manuscript restructuring

* Goal: Align the SMPT submission manuscript with the structure commonly used
  in electricity real-time pricing, time-of-use pricing, and demand-response
  simulation papers.
* Context: The active goal requires searching electricity pricing papers,
  borrowing their organization style, and improving the manuscript's length,
  formula detail, and result presentation without adding unsupported claims.
* Action:
  * Used the literature-review workflow to scope electricity pricing and
    demand-response papers.
  * Queried Crossref for DOI/metadata checks on four additional electricity
    pricing papers.
  * Created a structure benchmark document:
    `docs/reviews/power_pricing_structure_benchmark_2026-06-21.md`.
  * Added verified references for Samadi et al. 2010, Yang et al. 2013,
    Yu and Hong 2016, and Srinivasan et al. 2017 to `verified_refs.bib`.
  * Restructured the English SMPT final manuscript by adding
    `Related Work and Modelling Positioning`, adding an algorithmic outline to
    the solver section, and rewriting the opening of `Experimental Design` to
    follow a scenario-baseline-metric-sensitivity sequence.
* Command:
  ```bash
  python3 - <<'PY'
  import json, urllib.parse, urllib.request
  queries = [
      "Optimal real-time pricing algorithm based on utility maximization for smart grid",
      "A game-theoretic approach for optimal time-of-use electricity pricing",
      "Supply-demand balancing for power management in smart grid: A Stackelberg game approach",
      "Game-Theory based dynamic pricing strategies for demand side management in smart grids",
  ]
  for q in queries:
      url = "https://api.crossref.org/works?rows=1&query.title=" + urllib.parse.quote(q)
      item = json.load(urllib.request.urlopen(url, timeout=20))["message"]["items"][0]
      print(item.get("DOI"), (item.get("title") or [""])[0])
  PY
  ```
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  ```
  ```bash
  rg -n "LaTeX Error|Undefined control sequence|Citation .* undefined|Reference .* undefined|There were undefined|Overfull|Package natbib Warning|Warning--" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.blg
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf - | \
    rg -n "Related Work and Modelling Positioning|Electricity dynamic pricing|Algorithmic outline|reporting logic commonly used" -C 1
  ```
* Output:
  * `docs/reviews/power_pricing_structure_benchmark_2026-06-21.md`
  * `verified_refs.bib`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
* Result:
  * Crossref returned DOI metadata for all four newly added electricity-pricing
    references.
  * BibTeX and three XeLaTeX passes completed successfully.
  * The PDF grew from 21 pages to 23 pages after adding the independent related
    work and modelling-positioning section.
  * Log scans found no LaTeX errors, undefined references/citations, natbib
    warnings, BibTeX warnings, or overfull boxes.
  * `pdftotext` confirmed the PDF contains the new related-work section,
    electricity dynamic-pricing positioning, algorithmic outline, and
    demand-response-style experimental-design opening.
* Decision:
  * Keep electricity pricing as a structural modelling analogue, not as a
    physical mechanism claim.
  * Continue to bound equilibrium language to finite grids and regret
    certificates.
  * Next: run reviewer-style checks and inspect all figures after the structural
    revision.
* Status: verified.

### 2026-06-21 02:05 - Reviewer pass, figure audit, and final build check

* Goal: Use reviewer-style checks after the electricity-pricing restructuring,
  inspect every main-text figure, fix actionable issues, and verify the SMPT
  final manuscript build.
* Context: The active goal requires using reviewer/polishing skills, continuing
  optimization after review, and carefully reading all figures until the paper
  can approach a submission-ready state.
* Action:
  * Used the nature-reviewer workflow as a bounded SMPT pre-submission review.
  * Created `docs/reviews/smpt_reviewer_round_2026-06-21.md`.
  * Generated a main-figure contact sheet for visual inspection:
    `tmp/figure_checks/main_figure_contact_sheet_2026-06-21.png`.
  * Rendered PDF pages 11--16 to inspect Figure 3, Figure 4, Figure 5,
    Figure 6, and Figure 7 in page context.
  * Fixed Figure 4 legend wording from `Firm A/B` to `Provider A/B` in
    `experiments/build_peak_shaving_diagnostics.py`.
  * Strengthened the abstract and keywords with explicit verification and
    validation wording for SMPT fit.
* Failed command:
  ```bash
  # Intended to generate a figure contact sheet, but the shell loop parsed paths
  # incorrectly and pdftoppm received empty file names.
  for spec in "vllm_qos_anchor figures/peak_shaving_submission/vllm_qos_anchor.pdf" ...; do
    set -- $spec
    pdftoppm -png -singlefile -r 140 "$path" "tmp/figure_checks/${name}"
  done
  ```
  Result: failed with `I/O Error: Couldn't open file ''`. This command was not
  used as evidence.
* Successful commands:
  ```bash
  pdftoppm -png -singlefile -r 140 figures/peak_shaving_submission/vllm_qos_anchor.pdf tmp/figure_checks/vllm_qos_anchor
  pdftoppm -png -singlefile -r 140 figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf tmp/figure_checks/qos_utilization_profiles
  pdftoppm -png -singlefile -r 140 figures/peak_shaving_diagnostics/profit_components_and_regret.pdf tmp/figure_checks/profit_components_and_regret
  pdftoppm -png -singlefile -r 140 figures/peak_shaving_submission/mixed_oracle_regret.pdf tmp/figure_checks/mixed_oracle_regret
  pdftoppm -png -singlefile -r 140 figures/peak_shaving_submission/parameter_sweep_qos.pdf tmp/figure_checks/parameter_sweep_qos
  pdftoppm -png -singlefile -r 140 figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf tmp/figure_checks/smpt_phase_qos_gain
  pdftoppm -png -singlefile -r 140 figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf tmp/figure_checks/smpt_phase_profit_gain
  pdftoppm -png -singlefile -r 140 figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf tmp/figure_checks/mechanism_diagnostics
  uv run python - <<'PY'
  # Builds tmp/figure_checks/main_figure_contact_sheet_2026-06-21.png
  PY
  ```
  ```bash
  pdftoppm -f 11 -l 16 -png -r 110 \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    tmp/page_checks/smpt_pages_11_16
  ```
  ```bash
  uv run python experiments/build_peak_shaving_diagnostics.py
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  ```
  ```bash
  uv run python - <<'PY'
  # Checks figure environments, labels, references, and included image files.
  PY
  ```
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  rg -n "LaTeX Error|Undefined control sequence|Citation .* undefined|Reference .* undefined|There were undefined|Overfull|Package natbib Warning|Warning--" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.blg
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf - | \
    rg -n "verification and validation|Related Work and Modelling Positioning|Electricity dynamic pricing|Algorithmic outline|Provider A|Provider B|continuous strategy space|Profit is not robust" -C 1
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | rg "Pages|Page size|PDF version"
  ```
* Output:
  * `docs/reviews/smpt_reviewer_round_2026-06-21.md`
  * `tmp/figure_checks/main_figure_contact_sheet_2026-06-21.png`
  * `tmp/page_checks/smpt_pages_11_16-11.png` through
    `tmp/page_checks/smpt_pages_11_16-16.png`
  * `figures/peak_shaving_diagnostics/profit_components_and_regret.pdf`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
* Result:
  * Reviewer pass found no immediate new experiment requirement that can be
    satisfied without collecting real traces or expanding the strategy space.
  * Figure inspection found no label-overlap or caption-distance issue in the
    rendered PDF pages. Figure 3 and Figure 4 captions are now visually close to
    their figures.
  * Figure 4 legend now uses `Provider A` and `Provider B`, matching manuscript
    terminology.
  * Figure-reference script reported 8 figure environments, 8 cited figure
    labels, 0 uncited figure labels, and all 9 included image files present.
  * Full BibTeX/XeLaTeX build completed successfully.
  * Log scans found no LaTeX errors, undefined references/citations, natbib
    warnings, BibTeX warnings, or overfull boxes.
  * `pdfinfo` reports 23 A4 pages.
* Remaining boundary:
  * The paper is stronger as a simulation modelling and mechanism-diagnostic
    manuscript, but it still should not be described as production-calibrated or
    as proving continuous-space equilibrium.
  * If the manuscript is moved into an Elsevier two-column or final journal
    template, all figures need another rendered-page inspection.
* Status: verified.

### 2026-06-21 02:30 - Humanized language pass and SMPT submission adaptation check

* Goal: Reduce AI-like phrasing, tighten long sentences, and record the current
  SMPT/Elsevier submission-format boundary.
* Context: After the electricity-pricing structure adaptation and reviewer
  pass, the manuscript still contained repeated connective and defensive terms
  such as `therefore`, `diagnostic`, `mechanism`, and `robust`.
* Action:
  * Used the `humanizer` skill to scan for AI-like vocabulary, repetitive
    connectors, inflated phrasing, and over-regular sentence structure.
  * Used the `nature-polishing` generic research fragments for discussion,
    conclusion, and journal-neutral academic prose.
  * Rewrote high-impact passages in the abstract, Introduction, Related Work,
    Solution Method, Results, Discussion, Limitations, Conclusion, and AI
    declaration.
  * Created
    `docs/reviews/smpt_submission_adaptation_checklist_2026-06-21.md`.
  * Checked whether the current WSL TeX environment has Elsevier's
    `elsarticle.cls`.
* Command:
  ```bash
  detex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex > tmp/smpt_final_text_for_language_check.txt
  uv run python - <<'PY'
  from pathlib import Path
  import re
  text = Path("tmp/smpt_final_text_for_language_check.txt").read_text(errors="ignore")
  for w in ["therefore","thus","accordingly","robust","diagnostic","boundary",
            "mechanism","highlight","underscores","crucial","comprehensive"]:
      c = len(re.findall(r"\b"+re.escape(w)+r"\b", text, flags=re.I))
      print(f"{w}:{c}")
  PY
  ```
  ```bash
  kpsewhich elsarticle.cls || true
  ```
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  ```
  ```bash
  rg -n "LaTeX Error|Undefined control sequence|Citation .* undefined|Reference .* undefined|There were undefined|Overfull|Package natbib Warning|Warning--" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.blg
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf - | \
    rg -n "verification and validation|QoS-protection instrument|not as a reliable profit-improvement mechanism|Related Work and Modelling Positioning|Provider A|Provider B|mixed check|full-grid maximum regret falls to 0.203" -C 1
  ```
* Output:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
  * `docs/reviews/smpt_submission_adaptation_checklist_2026-06-21.md`
* Result:
  * `therefore` count was reduced from 18 before the language pass to 2 after
    the pass.
  * `thus`, `accordingly`, `highlight`, `underscores`, `crucial`, and
    `comprehensive` are no longer present in the extracted manuscript text.
  * `diagnostic` was reduced from 23 to 8, with remaining uses retained only
    where it names a technical artifact or figure family.
  * Full BibTeX/XeLaTeX build completed successfully.
  * Log scans found no LaTeX errors, undefined references/citations, natbib
    warnings, BibTeX warnings, or overfull boxes.
  * PDF text extraction confirms the updated abstract phrasing, related-work
    section, `mixed check` wording, Figure 4 `Provider A/B` terms, and
    finite-grid regret result.
  * `elsarticle.cls` is not installed in the current WSL TeX environment, so
    this round keeps the verified generic article manuscript rather than
    migrating to an unbuildable Elsevier template.
* Decision:
  * Treat the current PDF as a submission-review manuscript rather than a final
    Elsevier production-template file.
  * Template migration should wait until `elsarticle.cls` is installed or a
    journal template package is provided.
* Status: verified.

### 2026-06-21 03:05 - Table reference, value, and rendered-page audit

* Goal: Audit all main-text tables after the SMPT restructuring and language
  pass, with special attention to value traceability, table references, captions,
  and rendered-page readability.
* Context: Previous rounds inspected figures. The active goal also requires
  forming a submission-ready manuscript, so the tables need the same evidence
  audit as the figures.
* Action:
  * Parsed all `table` and `figure` environments in
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`.
  * Compared key table values against JSON/CSV artifacts.
  * Created `docs/reviews/smpt_table_value_audit_2026-06-21.md`.
  * Rendered PDF pages 6--17 and created
    `tmp/table_checks/table_pages_contact_sheet_2026-06-21.png`.
  * Visually inspected the pages containing Table 7, Table 8, and Table 9.
  * Changed one remaining phrase from `admission-control diagnostic` to
    `admission-control check`.
* Command:
  ```bash
  uv run python - <<'PY'
  # Extract table labels/captions and check citation status.
  PY
  ```
  ```bash
  uv run python - <<'PY'
  # Compare Table 2, 4, 5, 7, 8, and 9 values against:
  # - artifacts/peak_shaving/20260618/peak_shaving_summary.json
  # - artifacts/peak_shaving/20260619_smpt/smpt_baselines.csv
  # - artifacts/peak_shaving/20260619_smpt/smpt_fixed_point_residuals.csv
  # - artifacts/peak_shaving/20260619_smpt/smpt_ablations.csv
  # - artifacts/peak_shaving/20260619_smpt/smpt_resolved_sensitivity.csv
  # - artifacts/peak_shaving/20260619_submission/peak_shaving_mixed_oracle.json
  PY
  ```
  ```bash
  pdftoppm -f 6 -l 17 -png -r 105 \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    tmp/table_checks/smpt_table_pages
  uv run python - <<'PY'
  # Build tmp/table_checks/table_pages_contact_sheet_2026-06-21.png
  PY
  ```
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  ```
  ```bash
  rg -n "LaTeX Error|Undefined control sequence|Citation .* undefined|Reference .* undefined|There were undefined|Overfull|Package natbib Warning|Warning--" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.blg
  ```
  ```bash
  uv run python - <<'PY'
  # Recheck table/figure citation status and figure include existence.
  PY
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf - | \
    rg -n "Table 7|Table 8|Table 9|admission-control check|Provider A|Provider B|Profit is not stable|verification and validation" -C 1
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | rg "Pages|Page size|PDF version"
  ```
* Output:
  * `docs/reviews/smpt_table_value_audit_2026-06-21.md`
  * `tmp/table_checks/table_pages_contact_sheet_2026-06-21.png`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
* Result:
  * The manuscript contains 9 table environments and all 9 table labels are
    cited in the main text.
  * The manuscript contains 8 figure environments and all 8 figure labels are
    cited in the main text.
  * All 9 included figure/image files exist on disk.
  * The value audit checked 74 table values against artifacts and found
    0 issues within manuscript rounding tolerance.
  * Rendered-page inspection found no clipped tables, missing captions, or
    unreadable table columns on pages 6--17.
  * Full BibTeX/XeLaTeX build completed successfully.
  * Log scans found no LaTeX errors, undefined references/citations, natbib
    warnings, BibTeX warnings, or overfull boxes.
  * `pdfinfo` reports 23 A4 pages.
* Status: verified.

### 2026-06-21 02:11 - Draw.io Figure 1 content-compliance revision

* Goal:
  * Make Figure 1 fully consistent with the SMPT manuscript model and show a
    draw.io-based preview for review.
* Context:
  * The manuscript defines two user types, an outside option, one API
    intermediary, two heterogeneous inference providers, a routing--QoS fixed
    point, and a finite-grid equilibrium diagnostic.
  * The previous Figure 1 already covered these entities, but the legend merged
    direct access and market exit, and the fixed-point band omitted an explicit
    routing step.
* Action:
  * Updated `experiments/build_market_schematic_drawio.py`.
  * Added `Routing r_m,t` to the simulation fixed-point band.
  * Split the legend into `Direct API access` and `Exit option`.
  * Changed the direct-access label to `direct-provider API option p^D_m,t`.
  * Added a white backing label so the dashed direct-access arrow does not
    obscure the text.
  * Updated the Figure 1 caption in
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex` so it describes
    both the market structure and the lower simulation/diagnostic bands.
* Command:
  ```bash
  uv run python -m py_compile experiments/build_market_schematic_drawio.py
  uv run python experiments/build_market_schematic_drawio.py
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  ```
* Input:
  * `experiments/build_market_schematic_drawio.py`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
* Output:
  * `figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio`
  * `figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
* Result:
  * One intermediate generation attempt failed with
    `NameError: name 'draw' is not defined` after adding the white label backing.
    The call was corrected to use the active `ImageDraw` object `d`.
  * Regeneration then succeeded.
  * Draw.io XML validation reported `0 error(s)`; overlap warnings are caused
    by the large dashed section panels containing their child cards.
  * XeLaTeX completed and produced a 23-page PDF.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or cross-reference rerun warning; only existing underfull bibliography
    line-width messages remained.
  * Visual inspection confirmed that the direct-access label, fixed-point boxes,
    legend, and provider/user/intermediary labels are readable and not blocked.
* Decision:
  * Keep this draw.io version as the active Figure 1 source and PNG preview for
    the SMPT manuscript.
* Next:
  * If the target submission system requires vector-only figures, export the
    `.drawio` source to PDF/SVG from draw.io desktop on the host machine because
    the WSL environment does not currently have the draw.io CLI installed.
* Status: verified.

### 2026-06-21 02:18 - SMPT submission package and abstract-length compliance

* Goal:
  * Continue moving the SMPT manuscript toward a formal submission package after
    the Figure 1 Draw.io revision.
* Context:
  * Official SMPT/Elsevier author guidance was checked for submission-facing
    requirements: abstract length, keyword count, highlights, editable
    equations/tables, figure/table citation, data availability, and AI
    declaration/artwork restrictions.
  * Local audit showed the active abstract had 288 words before this round,
    exceeding the 250-word guide limit.
* Action:
  * Compressed the abstract in
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex` without changing
    numerical results or the bounded QoS/profit claim.
  * Added a submission package under `docs/submission/`.
  * Added explicit author-input placeholders for funding, competing interests,
    CRediT roles, repository DOI, author metadata, and corresponding author.
  * Added a Figure 1 policy caution: the final source is editable Draw.io, but
    the author should manually review/export it before submission because
    Elsevier restricts AI-assisted artwork.
* Command:
  ```bash
  python3 - <<'PY'
  # Count abstract words, keyword count, highlight lengths, and submission files.
  PY
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_smpt_submission_pkg.txt
  rg -n "QoS-protection instrument|not as a reliable profit-improvement mechanism|Reproducibility, Data Availability|Declaration of Generative AI|Figure 1: Market structure and simulation workflow" \
    /tmp/ps_smpt_submission_pkg.txt
  rg -n "LaTeX Error|Undefined control sequence|Citation.*undefined|Reference.*undefined|There were undefined|Overfull|Rerun to get cross-references" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    /tmp/ps_smpt_submission_pkg_xelatex.log
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | rg "Pages|Page size|PDF version"
  ```
* Input:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
  * Official SMPT guide for authors:
    `https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors`
* Output:
  * `docs/submission/smpt_submission_package_manifest_2026-06-21.md`
  * `docs/submission/smpt_cover_letter_draft_2026-06-21.md`
  * `docs/submission/smpt_highlights_2026-06-21.txt`
  * `docs/submission/smpt_declarations_template_2026-06-21.md`
  * Updated `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
* Result:
  * Abstract word count is now `250`.
  * Keyword count is `7`.
  * Highlights file has 5 non-empty bullets; lengths are `72, 72, 69, 70, 73`,
    all within the 85-character Elsevier guidance.
  * Submission package files were created and are non-empty.
  * XeLaTeX completed and produced a 23-page A4 PDF.
  * PDF text contains the bounded QoS/profit conclusion, Figure 1 caption,
    reproducibility/data availability section, and AI-assisted technology
    declaration.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or cross-reference rerun warnings.
* Decision:
  * Treat the paper as scientifically close to submission-candidate status, but
    not yet a formal submission-ready package until author metadata,
    declarations, and repository/DOI information are supplied.
* Next:
  * Fill author-specific declarations and decide whether to migrate to an
    Elsevier template after `elsarticle.cls` is available.
* Status: verified.

### 2026-06-21 02:28 - Full current-PDF figure audit for SMPT draft

* Goal:
  * Re-audit every figure in the latest compiled SMPT manuscript after the
    Figure 1 and abstract revisions.
* Context:
  * The active PDF contains 8 figure environments.
  * Current figure pages are PDF pages 4, 10, 12, 13, 15, 16, and 17.
  * The user previously requested Times New Roman figure fonts and no label or
    line overlap.
* Action:
  * Parsed all figure environments, labels, captions, and included source files
    from `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`.
  * Rendered the current PDF pages containing Figures 1--8.
  * Built a contact sheet for visual inspection.
  * Opened high-resolution page renders for Figures 1, 2, 3, 4, 5, 6, 7, and 8.
  * Checked PDF figure fonts through `pdffonts`.
  * Checked key figure values against stored JSON/CSV artifacts.
* Command:
  ```bash
  pdftotext -layout peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_fig_audit_layout.txt
  ```
  ```bash
  uv run python - <<'PY'
  # Render figure pages with pdftoppm through subprocess and build
  # tmp/figure_checks/current_smpt_figure_pages_contact_sheet_2026-06-21.png
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
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  ```
* Input:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
  * `artifacts/peak_shaving/20260619_submission/*`
  * `artifacts/peak_shaving/20260619_smpt/*`
  * `artifacts/peak_shaving/20260619/peak_shaving_mechanism_summary.csv`
* Output:
  * `docs/reviews/smpt_full_figure_audit_2026-06-21.md`
  * `tmp/figure_checks/current_smpt_figure_pages_contact_sheet_2026-06-21.png`
  * `tmp/figure_checks/current_pdf_pages/figaudit_page_*.png`
* Result:
  * All eight figure labels are referenced in the manuscript text.
  * Figure pages were rendered from the current PDF: 4, 10, 12, 13, 15, 16, 17.
  * Visual inspection found no missing figure, wrong caption placement, clipped
    panel, label-line overlap, or mismatched figure order.
  * Figures 2--8 embed `TimesNewRomanPSMT`; Figure 1 uses Times New Roman in the
    PNG rendering script and in the `.drawio` source.
  * Key values checked against artifacts include: mixed regret `0.2025` reported
    as `0.203`; nine parameter scenarios; 25 phase-grid rows; served volume
    `2610 -> 2865 / 3043`; average paid price `0.761 -> 0.735 / 0.625`; exit
    probabilities `0.158 -> 0.145 / 0.119` and `0.087 -> 0.075 / 0.044`.
  * Recompiled the manuscript with XeLaTeX; output remains a 23-page A4 PDF.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or cross-reference rerun warnings. Existing bibliography underfull
    line-width warnings remain.
* Decision:
  * No figure-level blocking issue was found in the current compiled manuscript.
  * Remaining figure-related submission risk is policy/export related: Figure 1
    should be manually reviewed and exported from Draw.io desktop before formal
    Elsevier submission, and earlier imagegen PNG drafts should not be used as
    final artwork.
* Status: verified.

### 2026-06-21 02:36 - SMPT final-gate reviewer pass and repository wording fix

* Goal:
  * Run a final-gate reviewer-style audit after the latest figure audit and
    submission-package updates.
* Context:
  * The current manuscript is scientifically close to an SMPT submission
    candidate, but formal submission still requires author metadata,
    declarations, and a frozen data/code archive.
  * The manuscript previously said that the current artifact package was
    available in a public GitHub repository. Because the latest local TeX and
    submission package files are still uncommitted/unpushed, that wording was
    too strong.
* Action:
  * Used `nature-reviewer` as a reviewer-style gate.
  * Created a three-reviewer internal report with cross-review synthesis.
  * Verified that `https://github.com/cccht/paper_token_price.git` is reachable
    through `git ls-remote`.
  * Revised the manuscript reproducibility statement to say that the public
    repository exists, but formal submission should cite a frozen release or DOI
    containing the final manuscript, code, artifacts, and figures.
* Command:
  ```bash
  git ls-remote https://github.com/cccht/paper_token_price.git
  ```
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_smpt_final_gate.txt
  python3 - <<'PY'
  # Count abstract words and check final-gate report size.
  PY
  rg -n "public project repository|latest repository push|frozen release|living reproducibility package|Declaration of Generative AI|QoS-protection instrument" \
    /tmp/ps_smpt_final_gate.txt
  rg -n "LaTeX Error|Undefined control sequence|Citation.*undefined|Reference.*undefined|There were undefined|Overfull|Rerun to get cross-references" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    /tmp/ps_smpt_final_gate_xelatex.log
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | rg "Pages|Page size|PDF version"
  ```
* Input:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
  * `docs/submission/*`
  * `docs/reviews/smpt_full_figure_audit_2026-06-21.md`
* Output:
  * `docs/reviews/smpt_final_gate_reviewer_report_2026-06-21.md`
  * Updated `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
* Result:
  * GitHub remote is reachable and reports `main` / `HEAD`.
  * Final-gate reviewer report size: `10558` bytes.
  * Abstract remains exactly `250` words.
  * PDF text confirms the revised repository/frozen-release wording and AI
    declaration.
  * XeLaTeX produced a 23-page A4 PDF.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or cross-reference rerun warnings. Existing bibliography underfull
    line-width warnings remain.
* Decision:
  * The manuscript should be treated as a strong author-review candidate, not as
    a fully formal submission package, until the final repository release/DOI,
    author declarations, and Figure 1 author-approved Draw.io export are done.
* Status: verified.

### 2026-06-21 02:47 - SMPT submission package pre-commit verification

* Goal:
  * Verify the final SMPT manuscript, Draw.io figure assets, submission notes,
    and review records before committing the package to GitHub.
* Context:
  * The final English manuscript is
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`.
  * Figure 1 now uses the editable Draw.io-derived asset
    `figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio`
    and its PNG preview.
  * Temporary render checks, planning notes, and earlier imagegen concept images
    are intentionally ignored and are not part of the formal submission package.
* Commands:
  ```bash
  git status --short --ignored
  git diff --check -- . ":!*.pdf" ":!*.png" ":!*.jpg" ":!*.jpeg" ":!*.drawio"
  # A common credential-pattern scan was executed; the exact sensitive regex is
  # not printed in README to avoid future false-positive secret scans.
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_smpt_final_commit.txt
  rg -n "Market structure and simulation workflow|living reproducibility package|Declaration of Generative AI|QoS-protection instrument" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex /tmp/ps_smpt_final_commit.txt
  rg -n "LaTeX Error|Undefined control sequence|Citation.*undefined|Reference.*undefined|There were undefined|Overfull|Rerun to get cross-references" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    /tmp/ps_smpt_final_commit_xelatex1.log \
    /tmp/ps_smpt_final_commit_xelatex2.log \
    /tmp/ps_smpt_final_commit_xelatex3.log \
    /tmp/ps_smpt_final_commit_bibtex.log
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | rg "Pages|Page size|PDF version"
  ```
* Output:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
  * `docs/submission/smpt_highlights_2026-06-21.txt`
  * `docs/submission/smpt_cover_letter_draft_2026-06-21.md`
  * `docs/submission/smpt_declarations_template_2026-06-21.md`
  * `docs/submission/smpt_submission_package_manifest_2026-06-21.md`
  * `docs/reviews/smpt_full_figure_audit_2026-06-21.md`
  * `docs/reviews/smpt_final_gate_reviewer_report_2026-06-21.md`
* Result:
  * Sensitive scan returned no credential values.
  * Text-only `git diff --check` returned no whitespace errors.
  * XeLaTeX/BibTeX/XeLaTeX/XeLaTeX completed and produced a 23-page A4 PDF.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or cross-reference rerun warnings.
  * PDF text contains the Figure 1 caption, QoS-protection conclusion, repository
    frozen-release boundary, and generative-AI declaration.
  * Abstract word count remains exactly `250`.
  * Elsevier-style highlights: 5 lines with lengths `72`, `72`, `69`, `70`, and
    `73`, all below the 85-character limit.
* Decision:
  * Commit the final English SMPT manuscript, editable Draw.io source and preview,
    submission package notes, review/audit records, updated figure scripts, and
    regenerated publication figures.
  * Do not commit temporary render directories, planning scratch files, or earlier
    imagegen-only concept images.
* Status: verified locally before Git commit.

### 2026-06-21 02:50 - SMPT submission package GitHub publication

* Goal:
  * Publish the verified SMPT submission package and Draw.io figure assets to the
    project GitHub repository.
* Context:
  * The remote repository is `https://github.com/cccht/paper_token_price.git`.
  * The package commit follows the successful XeLaTeX/BibTeX verification and
    figure/submission audit recorded above.
* Commands:
  ```bash
  git commit -m "Prepare SMPT submission package"
  GIT_TERMINAL_PROMPT=0 git push origin main
  git rev-parse --short HEAD
  git ls-remote --heads origin main
  git status --short --ignored
  ```
* Output:
  * Commit: `2e5132e` (`Prepare SMPT submission package`).
  * Remote branch after push:
    `2e5132edfcf7e8e2858b8688cdcc576c9b2e7fd9 refs/heads/main`.
* Result:
  * Git commit succeeded: `40 files changed, 5324 insertions(+), 56 deletions(-)`.
  * Push succeeded from local `main` to remote `main`.
  * The working tree has no unstaged or untracked formal submission files after
    the package push; remaining reported paths are ignored local artifacts,
    caches, LaTeX auxiliaries, render scratch files, and early concept images.
* Decision:
  * Add this README publication record as a separate follow-up documentation
    commit. The formal package commit itself remains `2e5132e`.
* Status: package pushed; README publication note pending commit.

### 2026-06-21 02:56 - Final data-availability wording refresh

* Goal:
  * Remove stale wording that implied the final SMPT draft might still contain
    local revisions not pushed to GitHub.
* Context:
  * The SMPT package was pushed to `https://github.com/cccht/paper_token_price`
    in commit `2e5132e`, followed by the README publication note in `956c926`.
  * A frozen release or DOI is still not available and should remain a formal
    submission boundary.
* Action:
  * Updated `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex` so the
    data-availability paragraph says the current manuscript, code, figure
    scripts, and artifacts are available in the GitHub repository.
  * Updated the SMPT cover-letter draft with the real repository URL and
    `archival DOI pending` wording.
  * Updated the declarations template so only the DOI remains a true placeholder.
* Commands:
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_smpt_dataavail.txt
  rg -n "current manuscript, code, figure scripts|frozen as a versioned release|living reproducibility package|Declaration of Generative AI" \
    /tmp/ps_smpt_dataavail.txt
  rg -n "LaTeX Error|Undefined control sequence|Citation.*undefined|Reference.*undefined|There were undefined|Overfull|Rerun to get cross-references" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    /tmp/ps_smpt_dataavail_xelatex1.log \
    /tmp/ps_smpt_dataavail_xelatex2.log \
    /tmp/ps_smpt_dataavail_xelatex3.log \
    /tmp/ps_smpt_dataavail_bibtex.log
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | rg "Pages|Page size|PDF version"
  ```
* Result:
  * Manuscript and submission-package wording now match the current pushed
    repository state.
  * XeLaTeX/BibTeX/XeLaTeX/XeLaTeX completed successfully.
  * PDF text contains the revised GitHub repository statement, frozen-release
    boundary, living-repository warning, and generative-AI declaration.
  * PDF remains 23 A4 pages.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or cross-reference rerun warnings.
* Decision:
  * Preserve the warning that a formal submission should cite a frozen release or
    archival DOI.
* Status: verified.

### 2026-06-21 03:00 - Versioned GitHub release for SMPT package

* Goal:
  * Freeze the current SMPT submission-candidate package as a versioned GitHub
    release so it is easier to cite and audit than a moving branch.
* Context:
  * DOI archival release is still not available; Zenodo, OSF, or another archive
    would be needed for a persistent data identifier.
  * The GitHub release targets commit `2eda4c2`.
* Commands:
  ```bash
  GH_PROMPT_DISABLED=1 gh release view smpt-final-2026-06-21 --repo cccht/paper_token_price
  GH_PROMPT_DISABLED=1 gh release create smpt-final-2026-06-21 \
    --repo cccht/paper_token_price \
    --target 2eda4c220423638e2cc725413f239aa9d513c1ac \
    --title "SMPT final manuscript package (2026-06-21)" \
    --notes "Versioned package for the Simulation Modelling Practice and Theory submission candidate. Includes the final manuscript PDF, submission highlights, cover-letter draft, package manifest, and editable Figure 1 Draw.io source. DOI archival release is still pending." \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    docs/submission/smpt_highlights_2026-06-21.txt \
    docs/submission/smpt_cover_letter_draft_2026-06-21.md \
    docs/submission/smpt_submission_package_manifest_2026-06-21.md \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png
  GH_PROMPT_DISABLED=1 gh release view smpt-final-2026-06-21 \
    --repo cccht/paper_token_price \
    --json tagName,name,isDraft,isPrerelease,url,targetCommitish,assets
  ```
* Output:
  * Release URL:
    `https://github.com/cccht/paper_token_price/releases/tag/smpt-final-2026-06-21`
  * Release target:
    `2eda4c220423638e2cc725413f239aa9d513c1ac`
  * Assets:
    `market_schematic_drawio_exact_2026-06-21.drawio`,
    `market_schematic_drawio_exact_2026-06-21.png`,
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`,
    `smpt_cover_letter_draft_2026-06-21.md`,
    `smpt_highlights_2026-06-21.txt`, and
    `smpt_submission_package_manifest_2026-06-21.md`.
* Result:
  * Release created successfully.
  * Release is not a draft and not a prerelease.
* Action:
  * Updated the manuscript, cover-letter draft, and declarations template to cite
    the versioned release while keeping the DOI limitation explicit.
* Verification:
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_smpt_release.txt
  rg -n "smpt-final-2026-06-21|versioned reproducibility package|persistent data identifier|Declaration of Generative AI" \
    /tmp/ps_smpt_release.txt
  rg -n "LaTeX Error|Undefined control sequence|Citation.*undefined|Reference.*undefined|There were undefined|Overfull|Rerun to get cross-references" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    /tmp/ps_smpt_release_xelatex1.log \
    /tmp/ps_smpt_release_xelatex2.log \
    /tmp/ps_smpt_release_xelatex3.log \
    /tmp/ps_smpt_release_bibtex.log
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | rg "Pages|Page size|PDF version"
  ```
* Verification result:
  * PDF text contains the GitHub release tag, versioned-package wording,
    persistent-identifier boundary, and generative-AI declaration.
  * XeLaTeX/BibTeX/XeLaTeX/XeLaTeX completed successfully.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or cross-reference rerun warnings.
  * PDF remains 23 A4 pages.
* Follow-up publication commands:
  ```bash
  git commit -m "Reference SMPT release package"
  GIT_TERMINAL_PROMPT=0 git push origin main
  GH_PROMPT_DISABLED=1 gh release upload smpt-final-2026-06-21 \
    --repo cccht/paper_token_price \
    --clobber \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex \
    docs/submission/smpt_cover_letter_draft_2026-06-21.md \
    docs/submission/smpt_declarations_template_2026-06-21.md
  GH_PROMPT_DISABLED=1 gh release view smpt-final-2026-06-21 \
    --repo cccht/paper_token_price \
    --json tagName,name,isDraft,isPrerelease,url,targetCommitish,assets
  ```
* Follow-up publication result:
  * Git commit pushed: `8f3caee` (`Reference SMPT release package`).
  * Release URL remains:
    `https://github.com/cccht/paper_token_price/releases/tag/smpt-final-2026-06-21`.
  * Release assets now include 8 files:
    `market_schematic_drawio_exact_2026-06-21.drawio`,
    `market_schematic_drawio_exact_2026-06-21.png`,
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`,
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`,
    `smpt_cover_letter_draft_2026-06-21.md`,
    `smpt_declarations_template_2026-06-21.md`,
    `smpt_highlights_2026-06-21.txt`, and
    `smpt_submission_package_manifest_2026-06-21.md`.
  * The local `gh` version supports release creation, upload, list, download,
    and view, but not `gh release edit`; therefore release notes were not edited
    after the attachment refresh.
  * The release tag target remains the creation commit `2eda4c2`, while the
    release assets were refreshed after repository commit `8f3caee`. The assets,
    not the auto-generated source archive, should be used as the submission
    candidate package unless a new archival DOI/release is created later.
* Status: verified and published.

### 2026-06-21 03:08 - Clean submission-candidate release URL

* Goal:
  * Replace the earlier release URL with a cleaner submission-candidate tag whose
    repository source archive can point to the final documented state.
* Context:
  * The earlier release `smpt-final-2026-06-21` was useful for freezing assets,
    but its tag target remained `2eda4c2` while later documentation and
    data-availability wording were committed afterward.
  * A new release tag is reserved:
    `smpt-submission-candidate-2026-06-21`.
* Action:
  * Updated the final manuscript data-availability paragraph to cite
    `https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`.
  * Updated the cover-letter draft and declarations template with the same
    release URL.
  * Corrected the cover-letter and declarations manuscript title so it exactly
    matches the final TeX title.
  * Updated the submission package manifest and final-gate reviewer report
    addendum so the remaining repository risk is narrowed to DOI archiving, not
    absence of a versioned release.
* Commands:
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_smpt_candidate.txt
  rg -n "smpt-submission-candidate-2026-06-21|versioned reproducibility package|QoS-protection instrument|profit-improvement mechanism|Declaration of Generative AI" \
    /tmp/ps_smpt_candidate.txt
  rg -n "LaTeX Error|Undefined control sequence|Citation.*undefined|Reference.*undefined|There were undefined|Overfull|Rerun to get cross-references" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    /tmp/ps_smpt_candidate_xelatex1.log \
    /tmp/ps_smpt_candidate_xelatex2.log \
    /tmp/ps_smpt_candidate_xelatex3.log \
    /tmp/ps_smpt_candidate_bibtex.log
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | rg "Pages|Page size|PDF version"
  ```
* Result:
  * XeLaTeX/BibTeX/XeLaTeX/XeLaTeX completed successfully.
  * PDF text contains the new submission-candidate release tag, versioned-package
    wording, QoS/profit boundary, and generative-AI declaration.
  * PDF remains 23 A4 pages.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or cross-reference rerun warnings.
* Next:
  * Commit and push the URL/title/manifest updates.
  * Create the new GitHub release at the pushed commit and upload the final
    submission-candidate assets.
* Publication commands:
  ```bash
  git commit -m "Prepare SMPT submission candidate release"
  GIT_TERMINAL_PROMPT=0 git push origin main
  GH_PROMPT_DISABLED=1 gh release create smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --target 195c60bb9f9752ebd04e5024e209b4e60f5e59a9 \
    --title "SMPT submission-candidate package (2026-06-21)" \
    --notes "Versioned package for the Simulation Modelling Practice and Theory submission candidate. Includes the final manuscript PDF/TEX, highlights, cover-letter draft, declarations template, package manifest, and editable Figure 1 Draw.io source. This release is versioned for review; DOI archival release remains pending if required by the journal or authors." \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex \
    docs/submission/smpt_highlights_2026-06-21.txt \
    docs/submission/smpt_cover_letter_draft_2026-06-21.md \
    docs/submission/smpt_declarations_template_2026-06-21.md \
    docs/submission/smpt_submission_package_manifest_2026-06-21.md \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png
  GH_PROMPT_DISABLED=1 gh release view smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --json tagName,name,isDraft,isPrerelease,url,targetCommitish,assets
  ```
* Publication result:
  * Commit pushed: `195c60b` (`Prepare SMPT submission candidate release`).
  * Release URL:
    `https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`.
  * Release target:
    `195c60bb9f9752ebd04e5024e209b4e60f5e59a9`.
  * Release is not a draft and not a prerelease.
  * Release assets: final manuscript PDF/TEX, highlights, cover-letter draft,
    declarations template, package manifest, Draw.io source, and Figure 1 PNG
    preview.
* Status: verified and published.

### 2026-06-21 03:16 - Submission-candidate completion audit

* Goal:
  * Record a requirement-by-requirement audit for the active SMPT manuscript
    objective.
* Context:
  * The current submission candidate is versioned at
    `https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`.
  * Remaining non-automatable items are author metadata, declarations, and any
    DOI/archive decision.
* Action:
  * Added `docs/reviews/smpt_submission_candidate_completion_audit_2026-06-21.md`.
* Result:
  * The audit maps the requested electricity-pricing structure alignment,
    formula/detail improvements, results presentation, reviewer-style checks,
    figure audits, table audits, compilation evidence, SMPT package checks, and
    versioned release to concrete files and command evidence.
  * The audit classifies the manuscript and reproducibility package as a
    submission-candidate final draft for author review.
  * The audit keeps author-only submission fields separate rather than inventing
    them.
* Status: documented.

### 2026-06-21 03:18 - Elsevier upload checklist and standalone figure assets

* Goal:
  * Make the release closer to an actual Elsevier submission package by adding
    upload checklists, an author information form, and standalone figure files.
* Context:
  * The manuscript PDF already embeds all figures.
  * Formal submission systems often request figure files separately, so relying
    only on the compiled manuscript PDF is less convenient for final upload.
* Action:
  * Added `docs/submission/smpt_elsevier_upload_checklist_2026-06-21.md`.
  * Added `docs/submission/smpt_author_information_form_2026-06-21.md`.
  * Added `docs/submission/smpt_figure_file_inventory_2026-06-21.md`.
  * Updated `docs/submission/smpt_submission_package_manifest_2026-06-21.md` to
    reference the new submission files.
  * Uploaded `verified_refs.bib`, the three new submission files, and standalone
    Figure 2--8 PDF assets to the GitHub release.
* Verification:
  ```bash
  python3 - <<'PY'
  # Checked 18 expected manuscript, bibliography, submission, and figure files.
  PY
  rg -n "\| [1-8] \|" docs/submission/smpt_figure_file_inventory_2026-06-21.md
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --clobber \
    verified_refs.bib \
    docs/submission/smpt_author_information_form_2026-06-21.md \
    docs/submission/smpt_elsevier_upload_checklist_2026-06-21.md \
    docs/submission/smpt_figure_file_inventory_2026-06-21.md \
    figures/peak_shaving_submission/vllm_qos_anchor.pdf \
    figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf \
    figures/peak_shaving_diagnostics/profit_components_and_regret.pdf \
    figures/peak_shaving_submission/mixed_oracle_regret.pdf \
    figures/peak_shaving_submission/parameter_sweep_qos.pdf \
    figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf \
    figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf \
    figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf
  GH_PROMPT_DISABLED=1 gh release view smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --json tagName,url,targetCommitish,assets
  ```
* Result:
  * All 18 expected local files exist.
  * Figure inventory lists all 8 manuscript figures.
  * Release now contains 20 assets, including final manuscript PDF/TEX,
    bibliography, highlights, cover letter, declarations, package manifest,
    upload checklist, author information form, figure inventory, Draw.io source,
    Figure 1 PNG, and standalone Figure 2--8 PDF assets.
* Status: verified and release assets refreshed.

### 2026-06-21 03:22 - Bundled Elsevier upload archive

* Goal:
  * Provide a single compressed upload bundle for author-side inspection and
    Elsevier submission preparation.
* Context:
  * The release already contains individual manuscript, figure, and submission
    files.
  * A single zip package makes it easier to download and inspect the exact
    submission candidate without selecting assets one by one.
* Commands:
  ```bash
  rm -rf tmp/smpt_elsevier_upload_bundle_2026-06-21 tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  mkdir -p tmp/smpt_elsevier_upload_bundle_2026-06-21/{manuscript,figures,submission,reviews}
  # Copy final manuscript PDF/TEX, verified_refs.bib, submission docs, figure
  # files, and selected review/audit reports into the bundle directory.
  cd tmp && zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21
  unzip -l tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  python3 - <<'PY'
  # Verified required zip entries, figure-file count, and required manuscript /
  # bibliography / submission / review files.
  PY
  pdftotext tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_bundle_pdf.txt
  rg -n "smpt-submission-candidate-2026-06-21|QoS-protection instrument|profit-improvement mechanism|Declaration of Generative AI" \
    /tmp/ps_bundle_pdf.txt
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --clobber tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release view smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --json tagName,url,targetCommitish,assets
  ```
* Result:
  * Created `tmp/smpt_elsevier_upload_bundle_2026-06-21.zip` with 30 zip
    entries and size about 916 KB.
  * The zip contains `manuscript/`, `figures/`, `submission/`, and `reviews/`
    folders.
  * Required entries were present; no required file was missing.
  * Bundle PDF text contains the release tag, QoS/profit boundary, and
    generative-AI declaration.
  * Uploaded the zip to the release.
  * Release now contains 21 assets and includes
    `smpt_elsevier_upload_bundle_2026-06-21.zip`.
* Decision:
  * Keep the zip in ignored `tmp/` locally and publish it only as a release
    asset, not as a tracked repository file.
* Status: verified and release asset published.

### 2026-06-21 03:29 - Submission portal copy fields

* Goal:
  * Add a copy-ready file for Elsevier submission-system fields so the author
    does not need to extract title, abstract, keywords, highlights, data
    availability, and AI declaration from the TeX/PDF manually.
* Action:
  * Added `docs/submission/smpt_submission_portal_fields_2026-06-21.md`.
  * Updated `docs/submission/smpt_elsevier_upload_checklist_2026-06-21.md`.
  * Updated `docs/submission/smpt_submission_package_manifest_2026-06-21.md`.
  * Rebuilt `tmp/smpt_elsevier_upload_bundle_2026-06-21.zip` with the portal
    fields file included.
  * Uploaded the portal fields file, updated checklist, updated manifest, and
    rebuilt zip to the GitHub release.
* Verification:
  ```bash
  python3 - <<'PY'
  # Verified portal-field abstract word count, keyword count, and highlight
  # lengths.
  PY
  zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21
  python3 - <<'PY'
  # Verified required zip entries, including submission portal fields.
  PY
  unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --clobber \
    docs/submission/smpt_submission_portal_fields_2026-06-21.md \
    docs/submission/smpt_elsevier_upload_checklist_2026-06-21.md \
    docs/submission/smpt_submission_package_manifest_2026-06-21.md \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release view smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --json tagName,url,targetCommitish,assets
  ```
* Result:
  * Portal-field abstract count is 250 words under the local regex check.
  * Portal-field keywords: 7.
  * Portal-field highlights: 5, with lengths `72`, `72`, `69`, `70`, and `73`.
  * Rebuilt zip contains 31 entries and passes `unzip -t`.
  * Release now contains 22 assets and includes
    `smpt_submission_portal_fields_2026-06-21.md`.
* Status: verified and release assets refreshed.

### 2026-06-21 03:32 - Completion audit synchronized with final release assets

* Goal:
  * Synchronize the completion audit with the current release state after the
    upload bundle and submission portal fields were added.
* Action:
  * Updated
    `docs/reviews/smpt_submission_candidate_completion_audit_2026-06-21.md`.
* Result:
  * The audit now states that the release contains 22 assets, including the final
    manuscript PDF/TEX, bibliography, submission portal fields, upload checklist,
    author-information form, standalone figure files, and bundled upload zip.
  * The audit notes that these packaging additions do not change the manuscript's
    scientific claims or experimental evidence.
* Status: documented.

### 2026-06-21 14:17 - Figure 4 and Figure 8 caption correction

* Goal:
  * Correct the captions of Figure 4 and Figure 8 in the final SMPT manuscript
    after a manual caption-quality concern was raised.
* Context:
  * Figure 4 previously used the phrase `Profit distribution`, although the
    figure actually reports profit components and a pure-strategy regret
    boundary.
  * Figure 8 previously described the mechanism direction but did not explicitly
    name all four diagnostic panels.
* Action:
  * Updated `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`.
  * Reworded Figure 4 as profit components plus pure-strategy regret boundary.
  * Reworded Figure 8 to name average paid price, no-purchase probability,
    QoS-adjusted served volume, and population-weighted inclusive value.
* Command:
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | grep -E "Pages|Page size"
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_final_text_caption_fix_v2.txt
  grep -En "Figure 4|Figure 8|Profit components and pure-strategy regret boundary|Mechanism diagnostics in the congested regime|Profit distribution|single-snapshot convergence boundary|better coverage and user experience" /tmp/ps_final_text_caption_fix_v2.txt
  grep -En 'LaTeX Error|Undefined control sequence|Citation .* undefined|Reference .* undefined|There were undefined|Overfull \\hbox|Overfull \\vbox|Rerun to get cross-references' peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log || true
  pdftoppm -f 13 -l 13 -png -r 180 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/caption_visual_check/final_page
  pdftoppm -f 17 -l 17 -png -r 180 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/caption_visual_check/final_page
  ```
* Output:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
  * `tmp/caption_visual_check/final_page-13.png`
  * `tmp/caption_visual_check/final_page-17.png`
* Result:
  * Final PDF remains 23 A4 pages.
  * PDF text contains the corrected Figure 4 and Figure 8 captions.
  * Old phrases `Profit distribution`, `single-snapshot convergence boundary`,
    and `better coverage and user experience` are absent from the PDF text.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or unresolved cross-reference rerun warning.
  * Rendered-page inspection confirms that Figure 4 and Figure 8 captions are
    visually close to the figures and do not overlap plots or body text.
* Next:
  * Refresh the GitHub release manuscript PDF/TEX and upload bundle.
* Status: verified locally.

### 2026-06-21 14:19 - Release assets refreshed after caption correction

* Goal:
  * Ensure the GitHub release and upload bundle contain the corrected Figure 4
    and Figure 8 captions.
* Action:
  * Copied the rebuilt final PDF/TEX into the Elsevier upload bundle.
  * Rebuilt `tmp/smpt_elsevier_upload_bundle_2026-06-21.zip`.
  * Re-uploaded the final PDF, final TEX, and upload bundle zip to the GitHub
    release with `--clobber`.
* Command:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cd tmp && zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21 && cd ..
  unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --clobber \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release view smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --json tagName,url,targetCommitish,assets
  ```
* Result:
  * `unzip -t` reports no errors.
  * Release still contains 22 assets.
  * Refreshed release assets:
    * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
    * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
    * `smpt_elsevier_upload_bundle_2026-06-21.zip`
  * Release URL:
    `https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`
* Status: verified and release assets refreshed.

### 2026-06-21 14:57 - Figure 4 legend and Figure 8 panel-label repair

* Goal:
  * Fix the Figure 4 `Intermediary` legend color swatch being visually blocked
    or clipped.
  * Fix the Figure 8 panel labels/titles so panels 1, 3, and 4 are visibly
    identified in the manuscript PDF.
* Context:
  * Figure 4 and Figure 8 are generated by
    `experiments/build_peak_shaving_diagnostics.py`.
  * The requested changes affect figure layout only; they do not change
    simulation data, metrics, equations, captions, or manuscript claims.
* Planned action:
  * Move the Figure 4 participant legend outside the plotting area.
  * Add explicit panel letters and more robust title placement to Figure 8.
  * Regenerate the diagnostic figures, recompile the final SMPT manuscript, and
    visually inspect the rendered manuscript pages.
* Command:
  ```bash
  uv run python experiments/build_peak_shaving_diagnostics.py
  pdftoppm -png -singlefile -r 180 figures/peak_shaving_diagnostics/profit_components_and_regret.pdf tmp/figure_label_fix_checks/profit_components_and_regret
  pdftoppm -png -singlefile -r 180 figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf tmp/figure_label_fix_checks/mechanism_diagnostics
  pdftotext figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf - | grep -En "\(a\)|\(b\)|\(c\)|\(d\)|Average paid price|No-purchase|QoS-adjusted|Population-weighted"
  pdftotext figures/peak_shaving_diagnostics/profit_components_and_regret.pdf - | grep -En "Provider A|Provider B|Intermediary|Profit by market participant|Final stored max regret"
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf | grep -E "Pages|Page size"
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_final_text_figure_label_fix.txt
  grep -En "Figure 4|Figure 8|\(a\) Average paid price|\(b\) No-purchase probability|\(c\) QoS-adjusted served volume|\(d\) Population-weighted inclusive value|Intermediary" /tmp/ps_final_text_figure_label_fix.txt
  grep -En 'LaTeX Error|Undefined control sequence|Citation .* undefined|Reference .* undefined|There were undefined|Overfull \\hbox|Overfull \\vbox|Rerun to get cross-references' peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log || true
  pdftoppm -f 13 -l 13 -png -r 180 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/figure_label_fix_checks/final_page
  pdftoppm -f 17 -l 17 -png -r 180 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/figure_label_fix_checks/final_page
  ```
* Output:
  * `figures/peak_shaving_diagnostics/profit_components_and_regret.pdf`
  * `figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf`
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
  * `tmp/figure_label_fix_checks/final_page-13.png`
  * `tmp/figure_label_fix_checks/final_page-17.png`
* Result:
  * The diagnostic build completed with `validation_warnings: []`.
  * Figure 4 now uses a figure-level three-column participant legend; the
    `Intermediary` color swatch is no longer blocked in the rendered manuscript
    page.
  * Figure 8 now shows explicit `(a)`--`(d)` panel titles in the standalone
    figure and in the manuscript PDF.
  * The final PDF remains 23 A4 pages.
  * Log scan found no LaTeX errors, undefined references/citations, overfull
    boxes, or unresolved cross-reference rerun warning.
  * Rendered-page inspection of pages 13 and 17 confirms that the two reported
    visual issues are fixed.
* Next:
  * Refresh release assets and the upload bundle with the updated figure files.
* Status: verified locally.

### 2026-06-21 15:03 - Release assets refreshed after figure-label repair

* Goal:
  * Ensure the GitHub release and Elsevier upload bundle contain the repaired
    Figure 4 legend and Figure 8 panel titles.
* Action:
  * Copied the rebuilt final manuscript PDF/TEX and updated diagnostic figure
    PDFs into `tmp/smpt_elsevier_upload_bundle_2026-06-21`.
  * Rebuilt `tmp/smpt_elsevier_upload_bundle_2026-06-21.zip`.
  * Re-uploaded the final PDF, updated standalone figure PDFs, and upload bundle
    zip to the GitHub release with `--clobber`.
* Command:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp figures/peak_shaving_diagnostics/profit_components_and_regret.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cd tmp && zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21 && cd ..
  unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --clobber \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    figures/peak_shaving_diagnostics/profit_components_and_regret.pdf \
    figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf \
    figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release view smpt-submission-candidate-2026-06-21 \
    --repo cccht/paper_token_price \
    --json tagName,url,targetCommitish,assets
  ```
* Result:
  * `unzip -t` reports no errors.
  * Release still contains 22 assets.
  * Refreshed assets include:
    * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`
    * `profit_components_and_regret.pdf`
    * `mechanism_diagnostics.pdf`
    * `qos_utilization_profiles.pdf`
    * `smpt_elsevier_upload_bundle_2026-06-21.zip`
  * Release URL:
    `https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`
* Status: verified and release assets refreshed.

### 2026-06-21 15:09 - Synchronize English and Chinese final TeX manuscripts

* Goal:
  * Update the English and Chinese final SMPT TeX manuscripts after the Figure 4
    legend repair and Figure 8 panel-label repair.
* Context:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex` already uses the
    updated figure sources, but its Figure 8 caption should explicitly align
    with the `(a)`--`(d)` panel labels.
  * `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex` still contains
    older Figure 4 and Figure 8 captions.
* Planned action:
  * Update only figure captions and directly related explanatory wording in the
    final English and Chinese TeX files.
  * Do not change experiments, data artifacts, equations, tables, or numerical
    claims.
  * Recompile both PDFs and inspect the affected figure pages.
* Command:
  ```bash
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/ps_final_en_sync.txt
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf /tmp/ps_final_zh_sync.txt
  pdftoppm -r 180 -f 13 -l 13 -png peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/page_checks/en_fig4
  pdftoppm -r 180 -f 17 -l 17 -png peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/page_checks/en_fig8
  pdftoppm -r 180 -f 11 -l 11 -png peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf tmp/page_checks/zh_fig4
  pdftoppm -r 180 -f 15 -l 15 -png peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf tmp/page_checks/zh_fig8
  ```
* Output:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` (23 pages).
  * `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf` (21 pages).
  * Page-check renders:
    `tmp/page_checks/en_fig4-13.png`,
    `tmp/page_checks/en_fig8-17.png`,
    `tmp/page_checks/zh_fig4-11.png`,
    `tmp/page_checks/zh_fig8-15.png`.
* Result:
  * English Figure 4 caption now names Provider A, Provider B, and the
    intermediary, matching the visible legend.
  * English Figure 8 caption now maps panels `(a)`--`(d)` to the four displayed
    diagnostics.
  * Chinese Figure 4 and Figure 8 captions were synchronized with the same
    evidence interpretation.
  * PDF text checks found the new captions and no stale Figure 4/Figure 8 caption
    phrases.
  * LaTeX log checks found no LaTeX errors, undefined references/citations,
    overfull boxes, or final cross-reference rerun warnings. The Chinese build
    still reports the known non-fatal `fontspec` warnings for Fandol fonts.
  * A first log-scan shell command failed because `printf` interpreted a leading
    `--` as an option; the command was corrected and rerun successfully. This was
    a verification-script issue, not a manuscript build issue.
* Decision:
  * No experiment, data artifact, equation, table, or numerical claim was
    changed.
  * Refresh the English submission bundle and GitHub release assets because the
    final English PDF/TEX changed.
* Release refresh:
  * Command:
    ```bash
    cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
    cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
    (cd tmp && zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21)
    unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
    gh release upload smpt-submission-candidate-2026-06-21 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21.zip --clobber
    ```
  * Output:
    * `tmp/smpt_elsevier_upload_bundle_2026-06-21.zip` rebuilt and `unzip -t`
      reported no compressed-data errors.
    * GitHub release assets refreshed at
      `https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`.
    * Updated remote asset sizes:
      `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` = 551982 bytes,
      `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex` = 64717 bytes,
      `smpt_elsevier_upload_bundle_2026-06-21.zip` = 968674 bytes.
* Status: verified.

### 2026-06-21 15:52 - Figure 1/4/8 visual legend revision

* Goal:
  * Improve Figure 1 visual quality and make Figure 4/Figure 8 color meanings
    explicit in every relevant panel.
* Context:
  * The final English and Chinese SMPT manuscripts currently include
    `market_schematic_drawio_exact_2026-06-21.png` as Figure 1.
  * Figure 4 uses `profit_components_and_regret.pdf`; its left profit panel has
    a participant legend, but the right regret panel also needs color annotation.
  * Figure 8 uses `mechanism_diagnostics.pdf`; panel (b) has a user-type legend,
    while panels (a), (c), and (d) also need strategy color annotation.
* Planned action:
  * Update `experiments/build_market_schematic_drawio.py` to generate a cleaner,
    more publication-style market-structure diagram while preserving the same
    model content: users, outside option, API intermediary, providers, routing,
    direct access, QoS feedback, fixed point, and equilibrium diagnostic.
  * Update `experiments/build_peak_shaving_diagnostics.py` so Figure 4 and
    Figure 8 include non-overlapping legends/color annotations for all panels.
  * Regenerate figures, recompile English and Chinese PDFs, render affected
    pages, and refresh the English release bundle if verification passes.
* Boundary:
  * Do not change numerical data, experiment artifacts, equations, tables, or
    manuscript claims.
* Command:
  ```bash
  uv run python -m py_compile experiments/build_market_schematic_drawio.py experiments/build_peak_shaving_diagnostics.py
  uv run python experiments/build_market_schematic_drawio.py
  uv run python experiments/build_peak_shaving_diagnostics.py
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  bibtex peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  ```
* Output:
  * Updated Figure 1:
    `figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png`
    and editable source
    `figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio`.
  * Updated Figure 4:
    `figures/peak_shaving_diagnostics/profit_components_and_regret.pdf`.
  * Updated Figure 8:
    `figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf`.
  * Recompiled PDFs:
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` and
    `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf`.
* Result:
  * Figure 1 was redesigned as a cleaner market-and-simulation workflow diagram
    while preserving the paper's model content.
  * Figure 4 now annotates colors in both the profit-component panel and the
    regret panel.
  * Figure 8 now includes visible color legends for all panels: strategy colors
    in panels (a), (c), and (d), and user-type colors in panel (b).
  * `pdffonts` confirms Figure 4/Figure 8 still embed Times New Roman.
  * PDF text checks found Figure 1, Figure 4, and Figure 8 captions in both the
    English and Chinese PDFs.
  * LaTeX log checks found no LaTeX errors, undefined references/citations,
    overfull boxes, or final cross-reference rerun warnings. The Chinese build
    still reports the known non-fatal Fandol `fontspec` warnings.
  * Rendered page checks:
    `tmp/figure_revision_checks/page_en_fig1-04.png`,
    `tmp/figure_revision_checks/page_en_fig4-13.png`,
    `tmp/figure_revision_checks/page_en_fig8-17.png`,
    `tmp/figure_revision_checks/page_zh_fig1-03.png`,
    `tmp/figure_revision_checks/page_zh_fig4-11.png`, and
    `tmp/figure_revision_checks/page_zh_fig8-15.png`.
  * Draw.io XML parses successfully. The draw.io structural validator reports
    only expected container-overlap warnings because the top-level section boxes
    contain internal cards; it reports 0 errors.
  * Unrelated regenerated files `market_schematic.pdf` and
    `qos_utilization_profiles.pdf` were restored to avoid non-target diffs.
* Decision:
  * Keep the manuscript text unchanged because the figure captions already
    describe the visual encodings sufficiently.
  * Refresh the English release bundle with the updated Figure 1, Figure 4,
    Figure 8, final English PDF, and editable Figure 1 source.
* Release refresh:
  * Command:
    ```bash
    cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
    cp figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
    cp figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
    cp figures/peak_shaving_diagnostics/profit_components_and_regret.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
    cp figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
    (cd tmp && zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21)
    unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
    gh release upload smpt-submission-candidate-2026-06-21 \
      peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
      figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio \
      figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png \
      figures/peak_shaving_diagnostics/profit_components_and_regret.pdf \
      figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf \
      tmp/smpt_elsevier_upload_bundle_2026-06-21.zip \
      --clobber
    ```
  * Output:
    * `tmp/smpt_elsevier_upload_bundle_2026-06-21.zip` rebuilt and `unzip -t`
      reported no compressed-data errors.
    * Release URL:
      `https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`.
    * Refreshed remote asset sizes:
      `market_schematic_drawio_exact_2026-06-21.drawio` = 13028 bytes,
      `market_schematic_drawio_exact_2026-06-21.png` = 151658 bytes,
      `profit_components_and_regret.pdf` = 26516 bytes,
      `mechanism_diagnostics.pdf` = 43820 bytes,
      `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` = 530530 bytes,
      `smpt_elsevier_upload_bundle_2026-06-21.zip` = 927117 bytes.
* Status: verified and release assets refreshed.

### 2026-06-21 21:08 - Blue/yellow figure palette and in-figure annotation spacing

* Goal:
  * Review all figures used by the final English and Chinese SMPT manuscripts.
  * Prefer a blue/yellow visual palette across figures.
  * Move in-figure legends, node notes, and annotation labels closer to the
    plotted content where they were placed too far above the axes or figure
    body.
* Correction:
  * The requested "figure caption" spacing refers to in-figure annotations,
    legends, and node remarks, not LaTeX `\caption` spacing.
  * Do not change `\captionsetup` or TeX figure-caption spacing.
* Figure scope:
  * `market_schematic_drawio_exact_2026-06-21.png`
  * `vllm_qos_anchor.pdf`
  * `qos_utilization_profiles.pdf`
  * `profit_components_and_regret.pdf`
  * `mixed_oracle_regret.pdf`
  * `parameter_sweep_qos.pdf`
  * `smpt_phase_qos_gain.pdf`
  * `smpt_phase_profit_gain.pdf`
  * `mechanism_diagnostics.pdf`
* Planned action:
  * Update only figure-generation scripts and generated figure assets.
  * Recompile English and Chinese final PDFs.
  * Render all figure pages and check for distant legends, overlaps, and color
    inconsistency.
* Boundary:
  * No experiment data, numerical claims, equations, tables, or manuscript
    prose changes.
* Commands:
  ```bash
  uv run python -m py_compile experiments/build_market_schematic_drawio.py experiments/build_peak_shaving_diagnostics.py experiments/build_peak_shaving_measurement_anchor.py experiments/run_peak_shaving_mixed_oracle.py experiments/run_peak_shaving_parameter_sweep.py experiments/run_peak_shaving_smpt_experiments.py
  ```
  ```bash
  uv run python experiments/build_market_schematic_drawio.py
  ```
  ```bash
  uv run python - <<'PY'
  from experiments.build_peak_shaving_diagnostics import (
      FIG,
      build_records,
      plot_mechanism,
      plot_profit_regret,
      plot_qos_utilization,
      validate,
  )

  bundle = build_records()
  warnings = validate(bundle)
  plot_qos_utilization(bundle)
  plot_profit_regret(bundle)
  plot_mechanism(bundle)
  print({
      "validation_warnings": warnings,
      "figures": [
          str(FIG / "qos_utilization_profiles.pdf"),
          str(FIG / "profit_components_and_regret.pdf"),
          str(FIG / "mechanism_diagnostics.pdf"),
      ],
  })
  PY
  ```
  ```bash
  uv run python - <<'PY'
  import csv
  import json

  from experiments.build_peak_shaving_measurement_anchor import PROJECT_ROOT, plot_anchor
  from experiments.run_peak_shaving_mixed_oracle import plot_trace
  from experiments.run_peak_shaving_parameter_sweep import plot_sweep
  from experiments.run_peak_shaving_smpt_experiments import plot_phase

  root = PROJECT_ROOT
  submission = root / "artifacts" / "peak_shaving" / "20260619_submission"
  smpt = root / "artifacts" / "peak_shaving" / "20260619_smpt"
  fig_submission = root / "figures" / "peak_shaving_submission"

  summary = json.loads((submission / "vllm_qos_anchor_summary.json").read_text(encoding="utf-8"))
  with (submission / "vllm_qos_anchor_points.csv").open(newline="", encoding="utf-8-sig") as handle:
      points = list(csv.DictReader(handle))
  plot_anchor(summary["profiles"], points, fig_submission / "vllm_qos_anchor.pdf")

  oracle = json.loads((submission / "peak_shaving_mixed_oracle.json").read_text(encoding="utf-8"))
  plot_trace(oracle)

  sweep = json.loads((submission / "peak_shaving_parameter_sweep.json").read_text(encoding="utf-8"))
  plot_sweep(sweep)

  with (smpt / "smpt_phase_grid.csv").open(newline="", encoding="utf-8") as handle:
      phase_rows = list(csv.DictReader(handle))
  for row in phase_rows:
      for key in ("capacity_scale", "alpha_scale", "qos_gain", "peak_reduction", "profit_gain_pct"):
          row[key] = float(row[key])
  plot_phase(phase_rows)
  print({
      "figures": [
          str(fig_submission / "vllm_qos_anchor.pdf"),
          str(fig_submission / "mixed_oracle_regret.pdf"),
          str(fig_submission / "parameter_sweep_qos.pdf"),
          str(fig_submission / "smpt_phase_qos_gain.pdf"),
          str(fig_submission / "smpt_phase_profit_gain.pdf"),
      ]
  })
  PY
  ```
* Result:
  * Script syntax check passed.
  * Figure 1 Draw.io source and PNG were regenerated.
  * Diagnostic reconstruction reported `validation_warnings: []`.
  * Figures regenerated from existing JSON/CSV artifacts, without rerunning
    the core equilibrium searches.
* Follow-up adjustment:
  * The first regenerated Figure 3 placed the in-figure legend inside the top
    panel and overlapped the QoS-threshold dashed line.
  * The legend was moved to the upper axis boundary with near-zero visual gap,
    so it stays close to the plot without covering the threshold or line series.
* Final validation commands:
  ```bash
  uv run python -m py_compile experiments/build_peak_shaving_diagnostics.py
  ```
  ```bash
  uv run python - <<'PY'
  from experiments.build_peak_shaving_diagnostics import build_records, plot_qos_utilization, validate
  bundle = build_records()
  warnings = validate(bundle)
  plot_qos_utilization(bundle)
  print({"validation_warnings": warnings, "figure": "figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf"})
  PY
  ```
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  ```
  ```bash
  rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log || true
  ```
* Final result:
  * English PDF compiled successfully: `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`, 23 pages.
  * Chinese PDF compiled successfully: `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf`, 21 pages after layout reflow.
  * Error scan reported no LaTeX errors, undefined references/citations, or overfull boxes.
  * Visual page checks were performed on English figure pages 3, 4, 10, 12, 13, 15, 16, 17 and Chinese figure pages 2, 3, 8, 9, 10, 11, 13, 14, 15, 17.
  * In-figure legends and node annotations are now close to the corresponding plot/diagram content; no overlap with plotted lines, node text, or manuscript body text was observed.
* Release refresh commands:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/profit_components_and_regret.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_submission/vllm_qos_anchor.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_submission/mixed_oracle_regret.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_submission/parameter_sweep_qos.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  (cd tmp && zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21)
  unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --clobber \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png \
    figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf \
    figures/peak_shaving_diagnostics/profit_components_and_regret.pdf \
    figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf \
    figures/peak_shaving_submission/vllm_qos_anchor.pdf \
    figures/peak_shaving_submission/mixed_oracle_regret.pdf \
    figures/peak_shaving_submission/parameter_sweep_qos.pdf \
    figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf \
    figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  ```
* Release result:
  * `unzip -t` reported no errors.
  * Release assets refreshed at `https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`.
  * Refreshed asset sizes include: final English PDF = 531192 bytes, upload bundle = 928551 bytes, Figure 1 PNG = 151803 bytes, Figure 3 PDF = 27805 bytes, Figure 4 PDF = 26197 bytes.
* Status: verified.

### 2026-06-21 21:45 - SCI/Nature figure palette and Figure 8 panel labels

* Goal:
  * Replace the previous mostly yellow/blue figure palette with a more standard
    SCI/Nature-style palette.
  * Keep colors publication-safe and distinguishable in print: NPG-like navy,
    cyan, green, coral, and neutral gray.
  * Move Figure 8 panel labels `(a)`--`(d)` below the corresponding subplots
    instead of embedding them in the subplot titles.
* Scope:
  * Update only figure-generation scripts, generated figure files, compiled PDFs,
    README records, and release/upload assets.
  * Keep experiment data, numerical values, manuscript prose, equations, tables,
    and LaTeX caption spacing unchanged.
* Planned action:
  * Adjust Figure 1 Draw.io/PNG palette to softer NPG-style group colors.
  * Adjust all matplotlib figures from yellow/blue-only colors to Nature/NPG or
    Okabe-Ito style colors.
  * Regenerate figures from existing JSON/CSV artifacts without rerunning core
    equilibrium searches.
  * Recompile English and Chinese PDFs, then visually inspect Figure 8 and all
    affected figure pages.
* Commands:
  ```bash
  uv run python -m py_compile experiments/build_market_schematic_drawio.py experiments/build_peak_shaving_diagnostics.py experiments/build_peak_shaving_measurement_anchor.py experiments/run_peak_shaving_mixed_oracle.py experiments/run_peak_shaving_parameter_sweep.py experiments/run_peak_shaving_smpt_experiments.py
  ```
  ```bash
  uv run python experiments/build_market_schematic_drawio.py
  ```
  ```bash
  uv run python - <<'PY'
  from experiments.build_peak_shaving_diagnostics import (
      FIG,
      build_records,
      plot_mechanism,
      plot_profit_regret,
      plot_qos_utilization,
      validate,
  )

  bundle = build_records()
  warnings = validate(bundle)
  plot_qos_utilization(bundle)
  plot_profit_regret(bundle)
  plot_mechanism(bundle)
  print({
      "validation_warnings": warnings,
      "figures": [
          str(FIG / "qos_utilization_profiles.pdf"),
          str(FIG / "profit_components_and_regret.pdf"),
          str(FIG / "mechanism_diagnostics.pdf"),
      ],
  })
  PY
  ```
  ```bash
  uv run python - <<'PY'
  import csv
  import json

  from experiments.build_peak_shaving_measurement_anchor import PROJECT_ROOT, plot_anchor
  from experiments.run_peak_shaving_mixed_oracle import plot_trace
  from experiments.run_peak_shaving_parameter_sweep import plot_sweep
  from experiments.run_peak_shaving_smpt_experiments import plot_phase

  root = PROJECT_ROOT
  submission = root / "artifacts" / "peak_shaving" / "20260619_submission"
  smpt = root / "artifacts" / "peak_shaving" / "20260619_smpt"
  fig_submission = root / "figures" / "peak_shaving_submission"

  summary = json.loads((submission / "vllm_qos_anchor_summary.json").read_text(encoding="utf-8"))
  with (submission / "vllm_qos_anchor_points.csv").open(newline="", encoding="utf-8-sig") as handle:
      points = list(csv.DictReader(handle))
  plot_anchor(summary["profiles"], points, fig_submission / "vllm_qos_anchor.pdf")

  oracle = json.loads((submission / "peak_shaving_mixed_oracle.json").read_text(encoding="utf-8"))
  plot_trace(oracle)

  sweep = json.loads((submission / "peak_shaving_parameter_sweep.json").read_text(encoding="utf-8"))
  plot_sweep(sweep)

  with (smpt / "smpt_phase_grid.csv").open(newline="", encoding="utf-8") as handle:
      phase_rows = list(csv.DictReader(handle))
  for row in phase_rows:
      for key in ("capacity_scale", "alpha_scale", "qos_gain", "peak_reduction", "profit_gain_pct"):
          row[key] = float(row[key])
  plot_phase(phase_rows)
  PY
  ```
* Result:
  * Script syntax check passed.
  * Figure 1 Draw.io/PNG and all final matplotlib figures were regenerated from
    existing artifacts.
  * Diagnostic reconstruction reported `validation_warnings: []`.
  * Standalone visual inspection confirms that Figure 8 panel labels `(a)`--`(d)`
    now appear below their corresponding subplots.
* Build and visual validation commands:
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  ```
  ```bash
  rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log || true
  ```
  ```bash
  pdftoppm -png -singlefile -r 130 -f 17 -l 17 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/peak_shaving_npg_page_review_20260621/en_p17
  pdftoppm -png -singlefile -r 130 -f 15 -l 15 peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf /tmp/peak_shaving_npg_page_review_20260621/zh_p15
  ```
* Build result:
  * English PDF compiled successfully: `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`, 23 pages.
  * Chinese PDF compiled successfully: `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf`, 21 pages.
  * Error scan reported no LaTeX errors, undefined references/citations, or overfull boxes.
  * Page-level inspection confirms that Figure 8 panel labels are below each
    subplot in both English page 17 and Chinese page 15.
* Release refresh commands:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/profit_components_and_regret.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_submission/vllm_qos_anchor.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_submission/mixed_oracle_regret.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_submission/parameter_sweep_qos.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  (cd tmp && zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21)
  unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --clobber \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png \
    figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf \
    figures/peak_shaving_diagnostics/profit_components_and_regret.pdf \
    figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf \
    figures/peak_shaving_submission/vllm_qos_anchor.pdf \
    figures/peak_shaving_submission/mixed_oracle_regret.pdf \
    figures/peak_shaving_submission/parameter_sweep_qos.pdf \
    figures/peak_shaving_smpt/smpt_phase_qos_gain.pdf \
    figures/peak_shaving_smpt/smpt_phase_profit_gain.pdf \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  ```
* Release result:
  * `unzip -t` reported no errors.
  * Release assets refreshed at `https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`.
  * Refreshed asset sizes include: final English PDF = 530512 bytes, Figure 1 PNG = 151458 bytes, Figure 8 PDF = 43327 bytes, upload bundle = 927126 bytes.
* Status: verified.

### 2026-06-21 22:18 - Reference-image palette for Figure 6 and Figure 8

* Goal:
  * Fix the color mismatch in Figure 6 and Figure 8 by extracting the visual
    palette from the provided AgentThink-style reference image.
  * Preserve the existing data, axes, captions, and Figure 8 panel-label layout.
* Source image:
  * `C:/Users/cccht/AppData/Local/Temp/codex-clipboard-6c89779f-4bcb-4d84-bbbf-f41b9bc0351b.png`
* Extraction command:
  ```bash
  uv run python - <<'PY'
  from pathlib import Path
  from PIL import Image
  from collections import Counter
  import colorsys

  path = Path("/mnt/c/Users/cccht/AppData/Local/Temp/codex-clipboard-6c89779f-4bcb-4d84-bbbf-f41b9bc0351b.png")
  img = Image.open(path).convert("RGB")
  small = img.resize((max(1, img.width//2), max(1, img.height//2)))
  quant = small.quantize(colors=96, method=Image.Quantize.MEDIANCUT).convert("RGB")
  counts = Counter(quant.getdata())
  for rgb, count in counts.most_common():
      r, g, b = [v / 255 for v in rgb]
      h, s, v = colorsys.rgb_to_hsv(r, g, b)
      if s >= 0.23 and 0.35 <= v <= 1.0 and count >= 60:
          print(f"#{rgb[0]:02X}{rgb[1]:02X}{rgb[2]:02X}\tcount={count}\th={h:.3f}\ts={s:.2f}\tv={v:.2f}")
  PY
  ```
* Extracted reusable palette:
  * Coral red: `#F08080`
  * Bright coral: `#F77870`
  * Peach orange: `#EEA667`
  * Soft pink: `#F5B7BF`
  * Mint green: `#8EEB95`
  * Pale green: `#C7E6AD`
  * Aqua: `#A9E9E4`
  * Teal: `#73BDAB`
  * Sky blue: `#89C6CF`
  * Slate blue: `#577386`
  * Warm gray: `#A8A1A2`
* Figure palette decision:
  * Figure 6 grouped bars: dynamic coarse = `#F08080`, dynamic fine = `#73BDAB`.
  * Figure 8 strategy bars: uniform = `#89C6CF`, dynamic coarse = `#F08080`,
    dynamic fine = `#73BDAB`.
  * Figure 8 user-type bars: rigid = `#577386`, elastic = `#F08080`.
* Boundary:
  * Only Figure 6 and Figure 8 colors will be changed.
  * No model outputs, numerical claims, TeX captions, or experiment artifacts
    will be recalculated.
* Code changes:
  * `experiments/run_peak_shaving_parameter_sweep.py` now uses reference-derived
    coral/teal bars for Figure 6.
  * `experiments/build_peak_shaving_diagnostics.py` now uses reference-derived
    sky-blue/coral/teal strategy bars and slate/coral user-type bars for Figure 8.
* Verification commands:
  ```bash
  uv run python -m py_compile experiments/build_peak_shaving_diagnostics.py experiments/run_peak_shaving_parameter_sweep.py
  uv run python - <<'PY'
  import json
  from experiments.build_peak_shaving_diagnostics import FIG, build_records, plot_mechanism, validate
  from experiments.run_peak_shaving_parameter_sweep import FIG as SWEEP_FIG, plot_sweep

  bundle = build_records()
  warnings = validate(bundle)
  plot_mechanism(bundle)
  rows = json.loads((SWEEP_FIG.parent.parent / "artifacts" / "peak_shaving" / "20260619_submission" / "peak_shaving_parameter_sweep.json").read_text(encoding="utf-8"))
  plot_sweep(rows)
  print({
      "validation_warnings": warnings,
      "figures": [str(SWEEP_FIG / "parameter_sweep_qos.pdf"), str(FIG / "mechanism_diagnostics.pdf")],
  })
  PY
  mkdir -p /tmp/peak_shaving_ref_palette_review_20260621
  pdftoppm -png -singlefile -r 220 figures/peak_shaving_submission/parameter_sweep_qos.pdf /tmp/peak_shaving_ref_palette_review_20260621/fig06_parameter
  pdftoppm -png -singlefile -r 220 figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf /tmp/peak_shaving_ref_palette_review_20260621/fig08_mechanism
  ```
* Output:
  * `figures/peak_shaving_submission/parameter_sweep_qos.pdf`
  * `figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf`
  * `/tmp/peak_shaving_ref_palette_review_20260621/fig06_parameter.png`
  * `/tmp/peak_shaving_ref_palette_review_20260621/fig08_mechanism.png`
* Result:
  * `py_compile` succeeded.
  * Figure regeneration succeeded with `validation_warnings: []`.
  * Visual spot check confirms Figure 6 uses the reference-derived coral/teal
    pair and Figure 8 uses the reference-derived sky-blue/coral/teal plus
    slate/coral pair; panel labels remain below the subfigures.
* Manuscript rebuild commands:
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log || true
  ```
* Manuscript rebuild result:
  * English PDF rebuilt successfully: 23 pages, 530446 bytes.
  * Chinese PDF rebuilt successfully: 21 pages, 911497 bytes.
  * Hard log scan found no `LaTeX Error`, undefined control sequence,
    undefined reference/citation, or `Overfull` entries.
  * Existing `Underfull` and Fandol `fontspec` warnings remain unchanged and
    are not caused by this color update.
  * A first combined PowerShell-to-WSL verification command failed because the
    bash here-document delimiter was misparsed by the Windows shell wrapper;
    the same checks were rerun as direct staged WSL commands.
* PDF page spot-check command:
  ```bash
  mkdir -p /tmp/peak_shaving_ref_palette_review_20260621/final_pdf_pages
  pdftoppm -png -r 180 -f 15 -l 17 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/peak_shaving_ref_palette_review_20260621/final_pdf_pages/en
  pdftoppm -png -r 180 -f 13 -l 15 peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf /tmp/peak_shaving_ref_palette_review_20260621/final_pdf_pages/zh
  ```
* PDF page spot-check result:
  * English Figure 6 appears on page 15; English Figure 8 appears on page 17.
  * Chinese Figure 6 appears on page 13; Chinese Figure 8 appears on page 15.
  * The embedded manuscript pages show the updated reference-image palette, with
    legends visible and no panel-label overlap.
* Upload-bundle refresh command:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp figures/peak_shaving_submission/parameter_sweep_qos.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  (cd tmp && zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21 && unzip -t smpt_elsevier_upload_bundle_2026-06-21.zip)
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --clobber \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    figures/peak_shaving_submission/parameter_sweep_qos.pdf \
    figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  ```
* Release verification:
  * `mechanism_diagnostics.pdf` = 43361 bytes.
  * `parameter_sweep_qos.pdf` = 27104 bytes.
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` = 530446 bytes.
  * `smpt_elsevier_upload_bundle_2026-06-21.zip` = 926987 bytes.
* Status: verified.

### 2026-06-21 22:39 - Shared palette alignment for Figure 4, Figure 6, and Figure 8

* Goal:
  * Fix the remaining palette inconsistency across Figure 4, Figure 6, and
    Figure 8.
  * Use the same reference-image-derived family for policy and participant
    encodings in the three figures.
* Context:
  * Figure 6 and Figure 8 already use the reference-image palette introduced in
    the previous round.
  * Figure 4 still used the earlier NPG navy/cyan/coral/green combination in
    its profit-component and regret panels, which made the figure visually
    inconsistent with Figure 6 and Figure 8.
* Planned palette:
  * Policy snapshots: uniform = `#89C6CF`, dynamic coarse = `#F08080`,
    dynamic fine = `#73BDAB`.
  * Figure 4 profit participants: Provider A = `#89C6CF`, Provider B =
    `#73BDAB`, intermediary = `#F08080`.
  * User types in Figure 8: rigid = `#577386`, elastic = `#F08080`.
  * Reference/threshold lines: `#577386`.
* Boundary:
  * Only figure-generation scripts and generated figure/PDF assets will change.
  * No simulation data, equations, captions, manuscript wording, or claims will
    be changed.
* Action:
  * Added shared reference-palette constants in
    `experiments/build_peak_shaving_diagnostics.py`.
  * Updated Figure 4 profit-participant colors and pure-strategy regret colors
    to match the Figure 6/Figure 8 color family.
  * Updated Figure 8 to use the same shared policy and user-type color
    constants.
  * Replaced Figure 6 hard-coded colors with the same shared policy palette in
    `experiments/run_peak_shaving_parameter_sweep.py`.
* Figure regeneration command:
  ```bash
  uv run python -m py_compile experiments/build_peak_shaving_diagnostics.py experiments/run_peak_shaving_parameter_sweep.py
  uv run python - <<'PY'
  import json
  from experiments.build_peak_shaving_diagnostics import FIG, build_records, plot_mechanism, plot_profit_regret, validate
  from experiments.run_peak_shaving_parameter_sweep import FIG as SWEEP_FIG, plot_sweep

  bundle = build_records()
  warnings = validate(bundle)
  plot_profit_regret(bundle)
  plot_mechanism(bundle)
  rows = json.loads((SWEEP_FIG.parent.parent / "artifacts" / "peak_shaving" / "20260619_submission" / "peak_shaving_parameter_sweep.json").read_text(encoding="utf-8"))
  plot_sweep(rows)
  print({
      "validation_warnings": warnings,
      "figures": [
          str(FIG / "profit_components_and_regret.pdf"),
          str(SWEEP_FIG / "parameter_sweep_qos.pdf"),
          str(FIG / "mechanism_diagnostics.pdf"),
      ],
  })
  PY
  ```
* Figure regeneration result:
  * `py_compile` succeeded.
  * Figure regeneration succeeded with `validation_warnings: []`.
  * Updated figure assets:
    `figures/peak_shaving_diagnostics/profit_components_and_regret.pdf`,
    `figures/peak_shaving_submission/parameter_sweep_qos.pdf`, and
    `figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf`.
* Manuscript rebuild command:
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log || true
  ```
* Manuscript rebuild result:
  * English PDF rebuilt successfully: 23 pages, 530440 bytes.
  * Chinese PDF rebuilt successfully: 21 pages, 911487 bytes.
  * Hard log scan found no `LaTeX Error`, undefined control sequence,
    undefined reference/citation, or `Overfull` entries.
* Visual check command:
  ```bash
  mkdir -p /tmp/peak_shaving_fig468_palette_20260621/figures /tmp/peak_shaving_fig468_palette_20260621/pages
  pdftoppm -png -singlefile -r 220 figures/peak_shaving_diagnostics/profit_components_and_regret.pdf /tmp/peak_shaving_fig468_palette_20260621/figures/fig04_profit_regret
  pdftoppm -png -singlefile -r 220 figures/peak_shaving_submission/parameter_sweep_qos.pdf /tmp/peak_shaving_fig468_palette_20260621/figures/fig06_parameter
  pdftoppm -png -singlefile -r 220 figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf /tmp/peak_shaving_fig468_palette_20260621/figures/fig08_mechanism
  pdftoppm -png -r 180 -f 13 -l 17 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/peak_shaving_fig468_palette_20260621/pages/en
  pdftoppm -png -r 180 -f 11 -l 15 peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf /tmp/peak_shaving_fig468_palette_20260621/pages/zh
  ```
* Visual check result:
  * Figure 4, Figure 6, and Figure 8 now use the same reference-image-derived
    sky-blue/coral/teal family.
  * English page checks: Figure 4 on page 13, Figure 6 on page 15, Figure 8 on
    page 17.
  * Chinese page checks: Figure 4 on page 11, Figure 6 on page 13, Figure 8 on
    page 15.
  * Legends remain visible and do not overlap bars, panel labels, captions, or
    body text.
* Release refresh command:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp figures/peak_shaving_diagnostics/profit_components_and_regret.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_submission/parameter_sweep_qos.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  (cd tmp && zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21)
  unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --clobber \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    figures/peak_shaving_diagnostics/profit_components_and_regret.pdf \
    figures/peak_shaving_submission/parameter_sweep_qos.pdf \
    figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  ```
* Release verification:
  * `profit_components_and_regret.pdf` = 26207 bytes.
  * `parameter_sweep_qos.pdf` = 27104 bytes.
  * `mechanism_diagnostics.pdf` = 43361 bytes.
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` = 530440 bytes.
  * `smpt_elsevier_upload_bundle_2026-06-21.zip` = 926957 bytes.
* Status: verified.

### 2026-06-21 23:06 - Nature/NMI pastel palette trial for Figure 4, Figure 6, and Figure 8

* Goal:
  * Try the `nature-figure` skill palette on Figure 4, Figure 6, and Figure 8
    after the author requested a different color scheme.
  * Keep the three figures internally consistent while preserving all numerical
    values, axes, labels, captions, and manuscript claims.
* Figure contract:
  * Core conclusion: the same QoS-improvement and profit-boundary evidence
    should read as one coherent figure family.
  * Evidence chain: Figure 4 reports profit components and pure-strategy regret,
    Figure 6 reports local stress-test QoS/peak-utilization robustness, and
    Figure 8 reports mechanism diagnostics.
  * Archetype: quantitative grid / grouped-bar figure family.
  * Backend: Python/Matplotlib, because the current figure-generation scripts
    are Python scripts.
  * Export contract: keep vector PDF outputs for LaTeX; retain the existing
    Times New Roman figure typography required by earlier manuscript edits.
* Nature/NMI palette mapping:
  * `baseline_dark`: `#484878`
  * `baseline_mid`: `#7884B4`
  * `baseline_soft`: `#B4C0E4`
  * `ours_base`: `#E4CCD8`
  * `ours_large`: `#F0C0CC`
  * `neutral_dark`: `#606060`
* Planned palette:
  * Policy snapshots: uniform = `#7884B4`, dynamic coarse = `#E4CCD8`,
    dynamic fine = `#F0C0CC`.
  * Figure 4 profit participants: Provider A = `#B4C0E4`, Provider B =
    `#7884B4`, intermediary = `#E4CCD8`.
  * Figure 8 user types: rigid = `#484878`, elastic = `#F0C0CC`.
  * Reference/threshold lines: `#606060`.
* Boundary:
  * Only palette constants, regenerated figure assets, rebuilt PDFs, and release
    assets will change.
  * No experiment outputs, formulas, tables, captions, TeX prose, or research
    claims will be changed.
* Action:
  * Replaced the prior reference-image colors in
    `experiments/build_peak_shaving_diagnostics.py` with the Nature/NMI pastel
    mapping above.
  * Replaced the Figure 6 policy colors in
    `experiments/run_peak_shaving_parameter_sweep.py` with the same policy
    mapping.
  * Kept the existing Times New Roman figure typography and PDF export path to
    preserve compatibility with the current LaTeX manuscript.
* Figure regeneration command:
  ```bash
  uv run python -m py_compile experiments/build_peak_shaving_diagnostics.py experiments/run_peak_shaving_parameter_sweep.py
  uv run python - <<'PY'
  import json
  from experiments.build_peak_shaving_diagnostics import FIG, build_records, plot_mechanism, plot_profit_regret, validate
  from experiments.run_peak_shaving_parameter_sweep import FIG as SWEEP_FIG, plot_sweep

  bundle = build_records()
  warnings = validate(bundle)
  plot_profit_regret(bundle)
  plot_mechanism(bundle)
  rows = json.loads((SWEEP_FIG.parent.parent / "artifacts" / "peak_shaving" / "20260619_submission" / "peak_shaving_parameter_sweep.json").read_text(encoding="utf-8"))
  plot_sweep(rows)
  print({
      "validation_warnings": warnings,
      "figures": [
          str(FIG / "profit_components_and_regret.pdf"),
          str(SWEEP_FIG / "parameter_sweep_qos.pdf"),
          str(FIG / "mechanism_diagnostics.pdf"),
      ],
  })
  PY
  ```
* Figure regeneration result:
  * `py_compile` succeeded.
  * Figure regeneration succeeded with `validation_warnings: []`.
  * Updated figure assets:
    `figures/peak_shaving_diagnostics/profit_components_and_regret.pdf`,
    `figures/peak_shaving_submission/parameter_sweep_qos.pdf`, and
    `figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf`.
* Manuscript rebuild command:
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log || true
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  ```
* Manuscript rebuild result:
  * English PDF rebuilt successfully: 23 pages,
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` =
    530403 bytes.
  * Chinese PDF rebuilt successfully: 21 pages,
    `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf` =
    911458 bytes.
  * The log scan reported no `LaTeX Error`, undefined reference/citation,
    undefined control sequence, or `Overfull` matches for the two rebuilt
    manuscripts.
* Visual preview command:
  ```bash
  mkdir -p /tmp/peak_shaving_nature_palette_20260621/figures /tmp/peak_shaving_nature_palette_20260621/pages
  pdftoppm -png -singlefile -r 220 figures/peak_shaving_diagnostics/profit_components_and_regret.pdf /tmp/peak_shaving_nature_palette_20260621/figures/fig04_profit_regret
  pdftoppm -png -singlefile -r 220 figures/peak_shaving_submission/parameter_sweep_qos.pdf /tmp/peak_shaving_nature_palette_20260621/figures/fig06_parameter
  pdftoppm -png -singlefile -r 220 figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf /tmp/peak_shaving_nature_palette_20260621/figures/fig08_mechanism
  pdftoppm -png -r 180 -f 13 -l 17 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/peak_shaving_nature_palette_20260621/pages/en
  pdftoppm -png -r 180 -f 11 -l 15 peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf /tmp/peak_shaving_nature_palette_20260621/pages/zh
  ```
* Visual preview result:
  * Figure 4, Figure 6, and Figure 8 standalone previews were generated under
    `/tmp/peak_shaving_nature_palette_20260621/figures`.
  * English manuscript pages checked: Figure 4 on page 13, Figure 6 on page 15,
    and Figure 8 on page 17.
  * Chinese manuscript pages checked: Figure 4 on page 11, Figure 6 on page 13,
    and Figure 8 on page 15.
  * The Nature/NMI pastel scheme is readable and internally consistent across
    Figure 4, Figure 6, and Figure 8. It is visually softer than the prior
    reference-image palette; Figure 6 has lower color contrast, but the legend,
    bars, and axis labels remain legible in both manuscripts.
* Release refresh command:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp figures/peak_shaving_diagnostics/profit_components_and_regret.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_submission/parameter_sweep_qos.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cd tmp
  zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21
  unzip -t smpt_elsevier_upload_bundle_2026-06-21.zip
  cd ..
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --clobber \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    figures/peak_shaving_diagnostics/profit_components_and_regret.pdf \
    figures/peak_shaving_submission/parameter_sweep_qos.pdf \
    figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release view smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --json assets
  ```
* Release refresh result:
  * The zip integrity check passed.
  * Refreshed release assets:
    * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` = 530403 bytes.
    * `profit_components_and_regret.pdf` = 26202 bytes.
    * `parameter_sweep_qos.pdf` = 27089 bytes.
    * `mechanism_diagnostics.pdf` = 43349 bytes.
    * `smpt_elsevier_upload_bundle_2026-06-21.zip` = 926898 bytes.
* Final verification command:
  ```bash
  uv run python -m py_compile experiments/build_peak_shaving_diagnostics.py experiments/run_peak_shaving_parameter_sweep.py
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  if rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log; then
    exit 2
  fi
  unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  stat -c "%n %s" \
    figures/peak_shaving_diagnostics/profit_components_and_regret.pdf \
    figures/peak_shaving_submission/parameter_sweep_qos.pdf \
    figures/peak_shaving_diagnostics/mechanism_diagnostics.pdf \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  GH_PROMPT_DISABLED=1 gh release view smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --json assets
  ```
* Final verification result:
  * `py_compile`, both `latexmk` commands, and the zip integrity test succeeded.
  * The final log scan produced no hard-error, undefined-reference/citation, or
    overfull-box matches.
  * Local and remote release sizes match for the English PDF, Figure 4,
    Figure 6, Figure 8, and the upload bundle.
* Status: verified and release assets refreshed.

### 2026-06-21 23:18 - Figure 1 redraw and Figure 2/3 Nature palette alignment

* Goal:
  * Redraw Figure 1 as an editable draw.io market-structure schematic.
  * Align Figure 2 and Figure 3 colors with the Nature/NMI pastel palette used
    for Figure 4, Figure 6, and Figure 8.
* Context:
  * Figure 1 is cited as `market_schematic_drawio_exact_2026-06-21.png` in both
    the English and Chinese SMPT manuscripts.
  * Figure 2 is `vllm_qos_anchor.pdf`.
  * Figure 3 is `qos_utilization_profiles.pdf`.
* Figure contract:
  * Figure 1 should explain the model sequence: providers post prices, the
    intermediary routes by price and QoS, users choose direct/intermediary/exit
    options, and congestion updates QoS.
  * Figure 2 should anchor the QoS degradation shape without changing measured
    data or fitted values.
  * Figure 3 should keep the policy colors consistent with the current Nature
    palette family.
* Boundary:
  * Only figure source/style files, regenerated figure assets, rebuilt PDFs,
    README records, release assets, and a Git commit will change.
  * No experiment data, formulas, numerical claims, captions, or theoretical
    statements will be changed.
* Tool check:
  ```bash
  command -v drawio || command -v draw.io || true
  ```
* Tool check result:
  * WSL did not find a `drawio` or `draw.io` CLI.
  * Windows-side quick path checks also did not locate `draw.io.exe`.
  * Decision: create a standards-compliant `.drawio` source file for Figure 1
    and use an available local preview/export path if the draw.io CLI remains
    unavailable.
* Figure regeneration command:
  ```bash
  uv run python -m py_compile \
    experiments/build_market_schematic_drawio.py \
    experiments/build_peak_shaving_measurement_anchor.py \
    experiments/build_peak_shaving_diagnostics.py
  uv run python experiments/build_market_schematic_drawio.py
  uv run python experiments/build_peak_shaving_measurement_anchor.py
  uv run python - <<'PY'
  from experiments.build_peak_shaving_diagnostics import FIG, build_records, plot_qos_utilization, validate
  bundle = build_records()
  warnings = validate(bundle)
  plot_qos_utilization(bundle)
  print({"validation_warnings": warnings, "figure": str(FIG / "qos_utilization_profiles.pdf")})
  PY
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio
  ```
* Figure regeneration result:
  * `py_compile` succeeded for all three scripts.
  * Figure 1 draw.io source and PNG preview were regenerated:
    `market_schematic_drawio_exact_2026-06-21.drawio` and
    `market_schematic_drawio_exact_2026-06-21.png`.
  * Figure 2 was regenerated as `vllm_qos_anchor.pdf` and
    `vllm_qos_anchor.png`.
  * Figure 3 was regenerated as `qos_utilization_profiles.pdf` with
    `validation_warnings: []`.
  * The draw.io structural validator reported `0 error(s)` and expected overlap
    warnings from intentionally layered background containers and child nodes.
  * The measurement-anchor JSON timestamp changed during script execution and
    was restored because this task only changes figure styling, not data
    artifacts.
* Manuscript rebuild command:
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  if rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log; then
    exit 2
  fi
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  ```
* Manuscript rebuild result:
  * English PDF rebuilt successfully: 23 pages,
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` =
    524224 bytes.
  * Chinese PDF rebuilt successfully: 21 pages,
    `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf` =
    905290 bytes.
  * The log scan produced no hard-error, undefined-reference/citation, or
    overfull-box matches.
* Visual preview command:
  ```bash
  pdftoppm -png -r 180 -f 3 -l 14 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/fig123_pages/en
  pdftoppm -png -r 180 -f 3 -l 14 peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf /tmp/fig123_pages/zh
  ```
* Visual preview result:
  * English manuscript checked: Figure 1 on page 4, Figure 2 on page 10, and
    Figure 3 on page 12.
  * Chinese manuscript checked: Figure 1 on page 3, Figure 2 on page 9, and
    Figure 3 across pages 10--11 due normal float placement.
  * Figure 1 has no node-note overlap after moving the diagnostic-feedback
    label downward.
  * Figure 2 and Figure 3 now use the same Nature/NMI pastel family as Figures
    4, 6, and 8. The colors are softer than the previous NPG palette but remain
    legible in the compiled manuscripts.
* Release refresh command:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_submission/vllm_qos_anchor.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cd tmp
  zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21
  unzip -t smpt_elsevier_upload_bundle_2026-06-21.zip
  cd ..
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --clobber \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png \
    figures/peak_shaving_submission/vllm_qos_anchor.pdf \
    figures/peak_shaving_diagnostics/qos_utilization_profiles.pdf \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  ```
* Release refresh result:
  * The zip integrity test passed.
  * Refreshed release assets:
    * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` = 524224 bytes.
    * `market_schematic_drawio_exact_2026-06-21.drawio` = 16444 bytes.
    * `market_schematic_drawio_exact_2026-06-21.png` = 147664 bytes.
    * `vllm_qos_anchor.pdf` = 27319 bytes.
    * `qos_utilization_profiles.pdf` = 27795 bytes.
    * `smpt_elsevier_upload_bundle_2026-06-21.zip` = 911654 bytes.
* Final verification command:
  ```bash
  uv run python -m py_compile \
    experiments/build_market_schematic_drawio.py \
    experiments/build_peak_shaving_measurement_anchor.py \
    experiments/build_peak_shaving_diagnostics.py
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.drawio
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  if rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log; then
    exit 2
  fi
  unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  git diff --check
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  GH_PROMPT_DISABLED=1 gh release view smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --json assets
  ```
* Final verification result:
  * `py_compile`, both `latexmk` commands, the zip integrity test, and
    `git diff --check` succeeded.
  * The draw.io validator reported `0 error(s)`; overlap warnings are expected
    from the intentionally layered schematic containers.
  * The final log scan produced no hard-error, undefined-reference/citation, or
    overfull-box matches.
  * Local and remote release sizes match for the English PDF, Figure 1 draw.io
    source/PNG, Figure 2, Figure 3, and the upload bundle.
* Status: verified and release assets refreshed.

### 2026-06-22 13:31 - Figure 1 IoT-style direct image generation

* Goal:
  * Redraw Figure 1 as a more practice-facing IoT/network-topology style
    infographic while preserving the manuscript logic: brokered API access,
    direct provider access, outside option, API intermediary routing, fixed GPU
    serving capacity, QoS feedback, fixed-point simulation, and finite-grid
    diagnostics.
* Context:
  * The previous Draw.io Figure 1 was technically consistent but looked too
    schematic. The current request asks for a direct generated image with IoT
    icons, system logic, and connecting lines so the figure reads more like a
    practical inference-service application.
* Action:
  * Used the built-in image generation path because no callable `codexdraft`
    tool is exposed in the current Codex tool list.
  * Generated an IoT-style manuscript Figure 1 draft with edge devices, an API
    gateway/intermediary, cloud GPU inference providers, routed-load arrows,
    price/QoS feedback, direct API access, exit/no-purchase path, and lower
    simulation/diagnostic bands.
* Command:
  ```text
  image_gen built-in tool prompt:
  "Redraw the provided Figure 1 as a polished IoT/network-topology style
  scientific infographic while preserving the same technical logic..."
  ```
* Input:
  * Current Figure 1 preview:
    `figures/peak_shaving_diagnostics/market_schematic_drawio_exact_2026-06-21.png`.
* Output:
  * Generated source image under Codex imagegen storage:
    `C:\Users\cccht\.codex\generated_images\019ede62-cd93-7220-8ab0-3824ce48b294\ig_0e8b76a9e9bef4b8016a38c8428bb08191983d27aaea611766.png`.
  * Manuscript asset:
    `figures/peak_shaving_diagnostics/market_schematic_iot_imagegen_2026-06-22.png`.
* Asset integration command:
  ```bash
  cp /mnt/c/Users/cccht/.codex/generated_images/019ede62-cd93-7220-8ab0-3824ce48b294/ig_0e8b76a9e9bef4b8016a38c8428bb08191983d27aaea611766.png \
    figures/peak_shaving_diagnostics/market_schematic_iot_imagegen_2026-06-22.png
  chmod 644 figures/peak_shaving_diagnostics/market_schematic_iot_imagegen_2026-06-22.png
  ```
* TeX update:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex` now uses
    `market_schematic_iot_imagegen_2026-06-22.png` for Figure 1.
  * `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex` now uses
    `market_schematic_iot_imagegen_2026-06-22.png` for Figure 1.
* Asset check command:
  ```bash
  uv run python - <<'PY'
  from PIL import Image
  p = "figures/peak_shaving_diagnostics/market_schematic_iot_imagegen_2026-06-22.png"
  im = Image.open(p)
  print(p)
  print(im.size, im.mode)
  PY
  ```
* Asset check result:
  * `market_schematic_iot_imagegen_2026-06-22.png` = 1662 x 946 px, RGB.
* Compilation command:
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  if rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log; then
    exit 2
  fi
  ```
* Compilation result:
  * English PDF rebuilt successfully:
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` = 1,662,770 bytes.
  * Chinese PDF rebuilt successfully:
    `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf` = 2,043,846 bytes.
  * The log scan found no LaTeX hard error, undefined reference/citation, or
    overfull-box match.
* Visual preview command:
  ```bash
  mkdir -p /tmp/fig1_iot_pages
  pdftoppm -png -r 180 -f 4 -l 4 peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/fig1_iot_pages/en
  pdftoppm -png -r 180 -f 3 -l 3 peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf /tmp/fig1_iot_pages/zh
  ```
* Visual preview result:
  * English Figure 1 appears on page 4; Chinese Figure 1 appears on page 3.
  * The rendered pages show no figure overflow, caption collision, or obvious
    node overlap.
  * The new Figure 1 now visibly includes IoT/edge applications, a network
    gateway, cloud GPU providers, routed-load arrows, price/QoS feedback,
    direct API access, and exit/no-purchase logic.
* Submission-note update:
  * Updated the Figure 1 file inventory, submission package manifest, Elsevier
    upload checklist, and declarations template to state that the active Figure
    1 is an author-requested IoT imagegen draft and that formal Elsevier upload
    needs an explicit artwork-policy decision.
* Release refresh command:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/
  cp figures/peak_shaving_diagnostics/market_schematic_iot_imagegen_2026-06-22.png tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/
  cp docs/submission/smpt_figure_file_inventory_2026-06-21.md tmp/smpt_elsevier_upload_bundle_2026-06-21/submission/
  cp docs/submission/smpt_submission_package_manifest_2026-06-21.md tmp/smpt_elsevier_upload_bundle_2026-06-21/submission/
  cp docs/submission/smpt_elsevier_upload_checklist_2026-06-21.md tmp/smpt_elsevier_upload_bundle_2026-06-21/submission/
  cp docs/submission/smpt_declarations_template_2026-06-21.md tmp/smpt_elsevier_upload_bundle_2026-06-21/submission/
  cd tmp
  zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21
  unzip -t smpt_elsevier_upload_bundle_2026-06-21.zip
  cd ..
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --clobber \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf \
    figures/peak_shaving_diagnostics/market_schematic_iot_imagegen_2026-06-22.png \
    tmp/smpt_elsevier_upload_bundle_2026-06-21.zip \
    docs/submission/smpt_figure_file_inventory_2026-06-21.md \
    docs/submission/smpt_submission_package_manifest_2026-06-21.md \
    docs/submission/smpt_elsevier_upload_checklist_2026-06-21.md \
    docs/submission/smpt_declarations_template_2026-06-21.md
  ```
* Release refresh result:
  * Zip integrity test passed.
  * Refreshed release assets:
    * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` = 1,662,770 bytes.
    * `market_schematic_iot_imagegen_2026-06-22.png` = 1,369,526 bytes.
    * `smpt_elsevier_upload_bundle_2026-06-21.zip` = 3,415,218 bytes.
    * `smpt_figure_file_inventory_2026-06-21.md` = 2,365 bytes.
    * `smpt_submission_package_manifest_2026-06-21.md` = 6,511 bytes.
    * `smpt_elsevier_upload_checklist_2026-06-21.md` = 3,338 bytes.
    * `smpt_declarations_template_2026-06-21.md` = 3,632 bytes.
* Final verification command:
  ```bash
  uv run python - <<'PY'
  from PIL import Image
  p = "figures/peak_shaving_diagnostics/market_schematic_iot_imagegen_2026-06-22.png"
  im = Image.open(p)
  print(f"{p}\t{im.size[0]}x{im.size[1]}\t{im.mode}")
  PY
  rg -n "market_schematic_iot_imagegen_2026-06-22.png" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex \
    docs/submission/smpt_figure_file_inventory_2026-06-21.md \
    docs/submission/smpt_submission_package_manifest_2026-06-21.md
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  if rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log \
    peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log; then
    exit 2
  fi
  unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  git diff --check
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  GH_PROMPT_DISABLED=1 gh release view smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --json assets
  ```
* Final verification result:
  * `market_schematic_iot_imagegen_2026-06-22.png` is 1662 x 946 px, RGB.
  * Both active TeX files cite the new Figure 1 PNG.
  * Both `latexmk` commands succeeded.
  * The final log scan found no LaTeX hard error, undefined reference/citation,
    or overfull-box match.
  * Zip integrity test and `git diff --check` succeeded.
  * PDF page counts remain 23 pages for English and 21 pages for Chinese.
  * GitHub release contains the refreshed PDF, upload bundle, Figure 1 PNG, and
    updated submission markdown assets with matching byte sizes.
* Result:
  * Visual check: the generated draft adds IoT/edge devices, a network gateway,
    cloud/GPU provider blocks, and clearer practical-system routes while
    retaining the paper's modelling and simulation workflow.
* Decision:
  * Use the generated PNG as the active Figure 1 image for the English and
    Chinese SMPT drafts.
  * Keep the previous Draw.io files as editable backup assets rather than
    deleting them.
* Next:
  * Commit and push the local manuscript, Figure 1, README, and submission-note
    updates.
* Status: verified.

### 2026-06-27 19:28 - SMPT reviewer-driven manuscript tightening

* Goal:
  * Respond to the latest internal review of the SMPT manuscript by tightening
    the academic framing, model transparency, equilibrium-evidence hierarchy,
    and submission-readiness notes without adding experiments or changing
    numerical artifacts.
* Context:
  * The review concludes that the manuscript is one coherent LaTeX/PDF paper
    rather than two different papers, but still reads partly like a simulation
    report plus method-diagnostic note.
  * The recommended positioning is a bounded, synthetic-calibration mechanism
    simulation: finite-grid evidence supports QoS protection under fixed GPU
    serving capacity, while profit improvement is not robust.
  * Elsevier's current SMPT guide page was checked again on 2026-06-27 through
    the official Elsevier guide search result. It reiterates that generative AI
    should not be used to create or alter submitted figures/artwork unless the
    use is part of the research method; therefore the current IoT imagegen
    Figure 1 remains an author-review draft, not a safe final artwork file.
* Action plan:
  * Compress the contribution statement into three academic contributions:
    simulation model, finite-grid regret diagnostic, and the QoS/profit
    separation.
  * Add a micro-level explanation of the user time-choice and replay-demand
    structure so the native-period distribution and logit choice are not read
    as duplicate time modelling.
  * Give the main QoS degradation function explicitly in the paper and define
    the interpretation of $q$ in utility, revenue, and congestion penalty terms.
  * Reframe the congested-result table as baseline, principal mixed diagnostic,
    and solver diagnostic snapshots rather than four equal equilibrium objects.
  * Replace ambiguous "SMPT baseline" wording with "service-management
    baseline" wording.
  * Strengthen validation and limitations language around synthetic
    calibration, vLLM measurement details, author metadata, persistent DOI, and
    AI artwork.
* Command:
  ```bash
  pwd
  uname -a || true
  git rev-parse --show-toplevel 2>/dev/null || true
  git status --short 2>/dev/null || true
  command -v uv || true
  uv --version || true
  sed -n "1,220p" ~/.codex/references/latex-paper.md
  ```
* Input:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
  * `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex`
  * Reviewer notes supplied in the Codex thread on 2026-06-27.
* Expected output:
  * Revised English SMPT TeX/PDF.
  * Necessary synchronized Chinese TeX/PDF wording edits.
  * Updated submission notes and README audit trail.
* Action:
  * Revised the English title, abstract, introduction contributions, model
    explanation, QoS function, profit-function interpretation, congested-result
    evidence hierarchy, vLLM validation notes, limitations, conclusion, artifact
    availability, and AI-assistance declaration.
  * Synchronized the same evidence-boundary and terminology changes in the
    Chinese TeX draft.
  * Replaced ambiguous "SMPT baseline" wording with "service-management
    baseline" in both drafts.
  * Reframed the congested-result table so the low-regret finite-grid mixed
    diagnostic is the main comparison against the uniform baseline, while coarse
    and fine pure snapshots are labelled as solver diagnostics.
* Verification command:
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex >/tmp/smpt_tighten_en_latexmk_20260627_final.log
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex >/tmp/smpt_tighten_zh_latexmk_20260627_final.log
  rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/smpt_tighten_en_20260627.txt
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf /tmp/smpt_tighten_zh_20260627.txt
  rg -n "Stylized Simulation Study|synthetic-calibrated|Principal mixed diagnostic|Regret / system profit|service-management baseline|author-review draft|QoS-protection" /tmp/smpt_tighten_en_20260627.txt
  rg -n "风格化仿真研究|合成校准|主混合诊断|regret / 系统利润|服务管理基线|作者审阅草图|非 AI 图稿" /tmp/smpt_tighten_zh_20260627.txt
  ```
* Verification output:
  * English manuscript compiled to a 24-page A4 PDF:
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf`.
  * Chinese manuscript compiled to a 22-page A4 PDF:
    `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf`.
  * Log scan found no `LaTeX Error`, undefined control sequence, undefined
    reference/citation, or `Overfull` warning in the two active logs.
  * PDF text extraction confirmed the revised title/framing, synthetic
    calibration wording, principal mixed diagnostic, regret/system-profit row,
    service-management baseline wording, QoS-protection framing, and AI artwork
    warning entered the compiled outputs.
  * English abstract word-count check initially failed twice because of
    PowerShell quoting and LaTeX-regex escaping in the checker command; the
    corrected string-split checker returned 210 words, below the 250-word
    Elsevier guide limit.
* Release refresh command:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  rm -f tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  cd tmp
  zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21
  unzip -t smpt_elsevier_upload_bundle_2026-06-21.zip >/tmp/smpt_bundle_unzip_test_20260627.log
  cd ..
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --clobber peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  ```
* Release refresh output:
  * Rebuilt upload bundle:
    `tmp/smpt_elsevier_upload_bundle_2026-06-21.zip` (3.3 MB).
  * `unzip -t` reported no compressed-data errors.
  * GitHub release `smpt-submission-candidate-2026-06-21` was refreshed with
    the revised English PDF, revised English TeX, and rebuilt upload bundle.
* Decision:
  * Keep the current numerical artifacts unchanged.
  * Treat the manuscript as a bounded, synthetic-calibrated mechanism simulation
    paper rather than a production forecast or robust profit-improvement paper.
  * Leave `Anonymous Author` unchanged until the real author metadata is
    supplied.
  * Keep the current Figure 1 as an author-review draft only; formal Elsevier
    submission still needs author-approved non-AI artwork or journal clearance.
* Next:
  * Add real author metadata, funding/declaration details, and a persistent
    artifact DOI before formal submission.
* Status: verified.

### 2026-07-10 01:11 - SMPT five-section manuscript restructuring

* Goal:
  * Restructure the SMPT manuscript so the numbered body uses only five main
    sections: introduction, related research review, methodology, experimental
    results, and conclusion/outlook.
* Context:
  * The previous draft was technically complete but still exposed too many
    internal diagnostic sections as main chapters.
  * The requested revision should improve readability without changing formulas,
    numerical values, citations, figures, tables, or experiment artifacts.
  * The language pass should avoid uncommon sentence structures and unnecessary
    specialist wording.
* Action plan:
  * Keep the abstract, keywords, reproducibility statement, AI statement, and
    bibliography outside the five counted main sections.
  * Fold simulation model, solver diagnostics, verification/validation, and
    experimental design into `Methodology`.
  * Fold mechanism discussion, limitations, and future work into
    `Conclusion and Outlook`.
  * Convert former subsection headings into shorter paragraph-level headings
    where navigation is still useful.
  * Apply `nature-polishing` and `humanizer` guidance: preserve evidence
    boundaries, use direct sentences, reduce inflated wording, and keep terms
    consistent.
* Command:
  ```bash
  pwd
  uname -a || true
  git rev-parse --show-toplevel 2>/dev/null || true
  git status --short 2>/dev/null || true
  command -v uv || true
  uv --version || true
  command -v python || true
  python --version || true
  command -v git || true
  git --version || true
  rg -n '^\\(section|subsection|subsubsection)\\*?\\{' peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex
  ```
* Input:
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
  * `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex`
* Expected output:
  * Revised English and Chinese TeX/PDF files with five numbered main sections.
  * No changed numerical claim, formula, table value, figure file, citation, or
    experiment artifact.
* Action:
  * Reorganized the English body into five numbered sections:
    `Introduction`, `Related Research Review`, `Methodology`,
    `Experimental Results`, and `Conclusion and Outlook`.
  * Reorganized the Chinese body into five numbered sections:
    `引言`、`相关研究综述`、`方法论`、`实验结果`、`总结展望`.
  * Converted the previous internal diagnostic sections into paragraph-level
    headings inside methodology, results, and conclusion/outlook.
  * Generated a new final-style framework figure directly with the built-in
    imagegen model rather than Draw.io, Python, SVG, or manual drawing.
  * Replaced Figure 1 in both English and Chinese TeX files with the new
    framework figure.
* Imagegen prompt summary:
  * Use case: academic infographic framework diagram.
  * Layout: wide 16:9, clean white background, final manuscript style.
  * Main blocks: `Users`, `Inference market`, `Simulation loop`, and
    `Diagnostics and findings`.
  * Required model content: time-rigid/time-flexible users, API intermediary,
    direct provider access, exit, Provider A with higher capacity, Provider B
    with lower capacity, fixed GPU capacity, price and traffic arrows,
    price-shape/user-choice/routing/load-QoS fixed-point loop, finite-grid
    regret, QoS protection, and profit boundary.
  * Style constraints: Nature/Elsevier-like blue, teal, muted orange, and grey
    palette; crisp lines; legible short labels; no equations, no citations, no
    extra terms, no decorative background.
* Output:
  * `figures/framework_imagegen_final_2026-07-10.png`
  * Image size: 1672 x 941 px, RGB.
  * The image is referenced by both active SMPT TeX drafts as Figure 1.
* Decision:
  * Keep the generated image as the current author-review framework figure for
    the final-style draft.
  * Because the figure was created with imagegen, the existing AI-artwork
    declaration remains necessary before any Elsevier submission.
* Verification command:
  ```bash
  chmod 644 figures/framework_imagegen_final_2026-07-10.png
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex >/tmp/smpt_final_structure_en_20260710.log
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex >/tmp/smpt_final_structure_zh_20260710.log
  rg -n "LaTeX Error|Undefined control sequence|Reference .* undefined|Citation .* undefined|Overfull" peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.log peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.log
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  pdfinfo peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf /tmp/smpt_final_structure_en_20260710.txt
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.pdf /tmp/smpt_final_structure_zh_20260710.txt
  rg -n "Introduction|Related Research Review|Methodology|Experimental Results|Conclusion and Outlook|Framework of the fixed-capacity inference-service simulation" /tmp/smpt_final_structure_en_20260710.txt
  rg -n "引言|相关研究综述|方法论|实验结果|总结展望|固定容量推理服务仿真框架" /tmp/smpt_final_structure_zh_20260710.txt
  ```
* Verification output:
  * English PDF compiled to 23 A4 pages.
  * Chinese PDF compiled to 20 A4 pages.
  * Log scan found no `LaTeX Error`, undefined control sequence, undefined
    reference/citation, or `Overfull` warning in the two active logs.
  * PDF text extraction confirmed the five numbered main sections in both
    languages.
  * PDF text extraction confirmed the new Figure 1 caption in both languages.
  * The new PNG is stored as a normal non-executable file:
    `-rw-r--r--`.
* Release refresh command:
  ```bash
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf
  cp peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex tmp/smpt_elsevier_upload_bundle_2026-06-21/manuscript/peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex
  cp figures/framework_imagegen_final_2026-07-10.png tmp/smpt_elsevier_upload_bundle_2026-06-21/figures/framework_imagegen_final_2026-07-10.png
  rm -f tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  cd tmp && zip -qr smpt_elsevier_upload_bundle_2026-06-21.zip smpt_elsevier_upload_bundle_2026-06-21
  unzip -t tmp/smpt_elsevier_upload_bundle_2026-06-21.zip >/tmp/smpt_bundle_unzip_test_20260710.log
  GH_PROMPT_DISABLED=1 gh release upload smpt-submission-candidate-2026-06-21 --repo cccht/paper_token_price --clobber peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex figures/framework_imagegen_final_2026-07-10.png tmp/smpt_elsevier_upload_bundle_2026-06-21.zip
  ```
* Release refresh output:
  * Rebuilt upload bundle:
    `tmp/smpt_elsevier_upload_bundle_2026-06-21.zip` (4.3 MB).
  * `unzip -t` reported no compressed-data errors.
  * GitHub release `smpt-submission-candidate-2026-06-21` was refreshed with
    the revised English PDF, revised English TeX, new framework figure, and
    rebuilt upload bundle.
* Status: verified.

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

## Experiment Log

### 2026-07-10 15:22 - Q1 dynamic-electricity-pricing framework-figure search

- Goal:
  * Identify high-impact Q1 papers on dynamic electricity pricing that contain
    market-structure, bilevel-game, demand-response, or simulation-workflow
    figures relevant to the manuscript's Figure 1.
- Context:
  * The current manuscript uses an imagegen framework figure that combines
    actors, simulation steps, diagnostics, and findings in one canvas.
  * The search was used to determine how Q1 papers separate market structure,
    information flow, and computational workflow.
- Action:
  * Applied the `superpowers:using-superpowers` workflow and the
    `nature-academic-search` multi-source-search workflow.
  * The academic-search MCP was unavailable, so the documented OpenAlex and
    Crossref fallback path was used together with publisher pages and author
    repository PDFs.
  * Checked original PDF pages for six framework examples from Applied Energy,
    Information Sciences, Nature Energy, and Electric Power Systems Research.
  * Used 2024 JCR Q1 as the strict "Q1" convention and kept the EPSR example in
    a separate high-relevance section because its 2024 JCR category is Q2.
  * The first documentation patch was rejected because its README context used
    the wrong bullet marker; no partial write occurred, and the patch was then
    reapplied against the actual file text.
- Command:
  ```bash
  uv run --no-project python /mnt/d/ccchtLinkData/UserProfile/.codex/skills/nature-academic-search/scripts/preflight.py
  uv run --no-project python /mnt/d/ccchtLinkData/UserProfile/.codex/skills/nature-academic-search/scripts/academic_search.py 'dynamic electricity pricing demand response framework' --limit 20 --sort cited_by_count
  uv run --no-project python /mnt/d/ccchtLinkData/UserProfile/.codex/skills/nature-academic-search/scripts/academic_search.py 'real-time electricity pricing demand response framework' --limit 20 --sort cited_by_count
  uv run --no-project python /mnt/d/ccchtLinkData/UserProfile/.codex/skills/nature-academic-search/scripts/academic_search.py 'dynamic tariff electricity market Stackelberg game' --limit 20 --sort cited_by_count
  pdfinfo /tmp/dynamic_pricing_frameworks/tang_2019_applied_energy.pdf
  pdfinfo /tmp/dynamic_pricing_frameworks/subramanian_2019_epsr.pdf
  pdfinfo /tmp/dynamic_pricing_frameworks/hong_2023_applied_energy.pdf
  pdfinfo /tmp/dynamic_pricing_frameworks/parag_2016_nature_energy.pdf
  pdftoppm -f 5 -l 5 -png -r 140 /tmp/dynamic_pricing_frameworks/tang_2019_applied_energy.pdf /tmp/dynamic_pricing_frameworks/tang_page
  pdftoppm -f 2 -l 2 -png -r 140 /tmp/dynamic_pricing_frameworks/subramanian_2019_epsr.pdf /tmp/dynamic_pricing_frameworks/subramanian_framework
  pdftoppm -f 6 -l 6 -png -r 140 /tmp/dynamic_pricing_frameworks/subramanian_2019_epsr.pdf /tmp/dynamic_pricing_frameworks/subramanian_elements
  pdftoppm -f 5 -l 6 -png -r 140 /tmp/dynamic_pricing_frameworks/hong_2023_applied_energy.pdf /tmp/dynamic_pricing_frameworks/hong_page
  ```
- Input:
  * Publisher metadata and DOI landing pages.
  * Public author manuscripts from PolyU, Southampton, Manchester, Missouri
    S&T, Aarhus, and the authors' own site.
- Output:
  * `docs/reviews/dynamic_electricity_pricing_frameworks_2026-07-10.md`
- Result:
  * The strongest content reference is Meng et al. (2023), Applied Energy,
    Fig. 1: a closed loop linking customer segmentation, customized demand
    models, multiple-pricing optimization, and prices.
  * The strongest hierarchy reference is Hong et al. (2023), Applied Energy,
    Fig. 1: an upper strategic decision layer and lower market/customer
    problems with explicit feedback.
  * The strongest visual simplification reference is Parag and Sovacool (2016),
    Nature Energy, Fig. 1: topology is expressed with nodes and links instead of
    decorative icons.
- Decision:
  * A final manuscript framework should use two panels: (a) market actors and
    information/traffic flows; (b) simulation and strategy-update loop.
  * QoS protection, regret, peak-utilization reduction, and the profit boundary
    are reported metrics, not market or mechanism nodes.
  * Do not copy or store the source figures in the repository; use the cited
    papers as structural references for a new original diagram.
- Verification command:
  ```bash
  git diff --check
  rg -n 'Meng et al.|Hong et al.|Feng et al.|Tang et al.|Parag and Sovacool|Subramanian et al.|双面板|2024 JCR Q1' docs/reviews/dynamic_electricity_pricing_frameworks_2026-07-10.md
  rg -o 'https://[^)]+' docs/reviews/dynamic_electricity_pricing_frameworks_2026-07-10.md
  curl -L --fail --silent --show-error --max-time 30 -o /dev/null -w '%{http_code}' '<each DOI or author-PDF URL>'
  ```
- Verification output:
  * `git diff --check` completed without whitespace errors.
  * The report contains all six strict-Q1 candidates, the EPSR boundary note,
    exact figure identifiers, and the two-panel recommendation.
  * Thirteen DOI/author-PDF endpoints returned HTTP 200.
  * The direct ScienceDirect PII URL returned HTTP 403 to command-line `curl`
    because of publisher anti-automation controls; its DOI returned HTTP 200,
    and the article page was readable through the browser search interface.
  * No manuscript TeX, figure asset, experiment data, or bibliography file was
    changed during this search.
- Status: verified.

### 2026-07-10 18:13 - 2026 electricity-pricing game-framework search

- Goal:
  * Find visually polished and explicitly layered game-theoretic electricity
    pricing framework figures published in 2026.
- Context:
  * This pass was limited to literature search, high-resolution figure
    screening, and local research archiving. No manuscript TeX or experiment
    file was to be changed.
  * Inclusion required pricing to be a game decision variable and the figure
    to expose a leader-follower, upper-lower, or market-aggregation-resource
    hierarchy.
- Action:
  * Used `superpowers:using-superpowers` and the
    `nature-academic-search` multi-source workflow.
  * Searched publisher pages for 2026 Stackelberg, Nash, cooperative, and
    hybrid-game electricity-pricing studies.
  * Downloaded publisher-hosted high-resolution figures and visually inspected
    their hierarchy, arrows, label density, style consistency, and readability.
  * Retained nine references and separated aesthetics-first examples from
    logic-first examples.
- Representative commands:
  ```bash
  curl -LfsS 'https://ars.els-cdn.com/content/image/1-s2.0-S2352467726000676-gr1_lrg.jpg' -o /tmp/game_pricing_2026/segan_cno_dynamic_pricing_2026_fig1_lrg.jpg
  curl -LfsS 'https://ars.els-cdn.com/content/image/1-s2.0-S0142061526002747-gr1_lrg.jpg' -o /tmp/game_pricing_2026/energy_multitimescale_game_2026_fig1.jpg
  curl -LfsS 'https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41598-026-36826-2/MediaObjects/41598_2026_36826_Fig1_HTML.png' -o /tmp/game_pricing_2026/srep_heterogeneous_2026_fig1.png
  file /tmp/game_pricing_2026/energy_multitimescale_game_2026_fig1.jpg
  ```
- Input:
  * Publisher article pages, DOI records, and publisher image endpoints.
  * The current manuscript's need for provider-intermediary-user pricing and
    feedback layers.
- Output:
  * `docs/reviews/game_theoretic_electricity_pricing_frameworks_2026_2026-07-10.md`
  * Local reference directory:
    `/root/paper_code/0427_tokenrl/paper_reference_figures/game_pricing_2026_2026-07-10/`
  * Local provenance and reuse-boundary file: `SOURCES.md`.
- Result:
  * Best single layered architecture: the 2026 Journal of Energy Storage VPP
    dynamic-storage-pricing paper, Fig. 1.
  * Best paired system/game reference: the 2026 Renewable Energy fair and
    adaptive P2P-pricing paper, Figs. 1-2.
  * Best end-to-end paper framework: the 2026 IJEPES multi-timescale bi-level
    game paper, Fig. 1.
  * Best exact dynamic-pricing logic: the 2026 Sustainable Energy, Grids and
    Networks charging-network-operator paper, Fig. 1.
- Decision:
  * A later original manuscript figure should combine market/aggregation/
    resource layering, information/physical separation, and explicit downward
    price/upward load feedback. Source icons and layouts must not be copied.
- Verification commands:
  ```bash
  file /root/paper_code/0427_tokenrl/paper_reference_figures/game_pricing_2026_2026-07-10/*.jpg
  for doi in '10.1016/j.renene.2026.125360' '10.1016/j.est.2026.121259' '10.1016/j.ijepes.2026.111832' '10.1016/j.renene.2025.123963' '10.1016/j.est.2026.120641' '10.1016/j.segan.2026.102185' '10.1016/j.epsr.2025.112676'; do curl -L --silent --show-error --max-time 30 -o /dev/null -w "$doi %{http_code}\n" "https://doi.org/$doi"; done
  rg -n 'Journal of Energy Storage|Renewable Energy|IJEPES|Sustainable Energy, Grids and Networks|2025.*2026|本地文件' docs/reviews/game_theoretic_electricity_pricing_frameworks_2026_2026-07-10.md
  git diff --check
  git status --short
  ```
- Verification output:
  * All nine archived figures were recognized as valid high-resolution JPEG
    files, ranging from 1721x1275 to 3591x1607 pixels and from 2368x2528 to
    3153x3298 pixels for the portrait layouts.
  * All seven principal DOI endpoints returned HTTP 200.
  * The report records both cases where the DOI year is 2025 but the formal
    issue date is in 2026.
  * `git diff --check` completed without whitespace errors.
  * Git status contains only README and review-report documentation changes;
    no TeX, manuscript figure asset, bibliography, or experiment file changed.
- Status: verified.

### 2026-07-10 19:38 - Inference-pricing framework ImageGen draft

- Goal:
  * Generate an original manuscript framework figure using the information/
    physical-layer composition of a selected 2026 Renewable Energy figure as
    visual inspiration.
- Context:
  * Reference image:
    `/root/paper_code/0427_tokenrl/paper_reference_figures/game_pricing_2026_2026-07-10/01_renewable_energy_adaptive_p2p_system_fig1.jpg`.
  * Manuscript source checked:
    `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`.
  * The reference is used only for high-level visual hierarchy; its electrical
    equipment, labels, icons, and exact layout will not be copied.
- Design:
  * Left panel: time-rigid and time-flexible users, channel choice, API
    intermediary, direct-provider paths, outside option, and provider pricing
    competition.
  * Right panel: a larger Provider A GPU cluster and a smaller Provider B GPU
    cluster, with fixed capacity, traffic, utilization, and QoS telemetry.
  * Bottom strip: price profiles, user choice, routing, GPU utilization, QoS
    fixed point, and payoff/regret diagnostics connected as a feedback loop.
  * Solid arrows denote request traffic; dashed arrows denote price and QoS
    information. No experimental result or profit-improvement claim is embedded
    in the framework.
- Tool:
  * Built-in ImageGen with the selected local image supplied as a composition
    and visual-style reference.
- Execution:
  * First built-in edit request used the selected reference image and the full
    manuscript-specific prompt.
  * A second edit request retried with a shorter prompt.
  * A third request used the built-in generation endpoint without uploading the
    reference image, while preserving the extracted composition in text.
- Result:
  * Both edit requests failed with `network error: error sending request for
    url (https://chatgpt.com/backend-api/codex/images/edits)`.
  * The generation request failed with `network error: error sending request
    for url (https://chatgpt.com/backend-api/codex/images/generations)`.
  * No image was returned or added to the manuscript assets.
- Decision:
  * Do not silently switch models or use a hand-drawn/Python substitute. The
    ImageGen CLI fallback requires an available `OPENAI_API_KEY` and explicit
    user approval.
- CLI fallback check:
  * The user explicitly approved continuing with the CLI fallback.
  * The WSL process reported `OPENAI_API_KEY=missing`; no API request was made,
    and no credential value was read, printed, or stored.
- Login-state retry:
  * At 2026-07-10 20:20 CST, the user reported that login had been refreshed.
  * `OPENAI_API_KEY` remained unavailable to the WSL process, so CLI fallback
    was still not eligible to run.
  * A new built-in ImageGen attempt was selected because it uses the Codex
    login state rather than the shell API-key variable.
- Next:
  * Inspect the generated author-review draft before replacing the manuscript
    asset or recompiling the paper.
- Successful retry:
  * After the Codex login state was refreshed, the built-in reference-image
    request completed successfully without `OPENAI_API_KEY`.
  * Built-in output:
    `/mnt/d/ccchtLinkData/UserProfile/.codex/generated_images/019f4ad0-229b-7352-b90f-706e510c875b/exec-c3282d1e-e981-4f2f-ad1b-9e44af18be61.png`.
  * Project copy:
    `figures/framework_imagegen_p2p_reference_2026-07-10.png`.
- Verification:
  * `file` identified the project copy as a 1693x929 RGB PNG.
  * Source and project-copy SHA-256 values both equal
    `f96d3a61555d8c31340146410ddb79ee73bc7586eaa3ef7f9b4ce6ea7e0c304b`.
  * The CLI fallback was not used; the WSL shell still had no
    `OPENAI_API_KEY`, which is expected because Codex login and API-key
    authentication are separate mechanisms.
- Status: verified.

### 2026-07-10 20:58 - Editable Draw.io reconstruction of the framework figure

- Goal:
  * Reconstruct the approved ImageGen framework as a fully editable Draw.io
    figure while preserving its three-part layout and manuscript semantics.
- Context:
  * Visual reference:
    `figures/framework_imagegen_p2p_reference_2026-07-10.png`.
  * The diagram must preserve two user types, four channel choices, one API
    intermediary, two capacity-heterogeneous providers, a GPU serving layer,
    and the simulation/diagnostic loop.
  * Icons must come from a consistent, openly licensed vector library rather
    than being cropped from published papers.
- Skills and sources:
  * Used `drawio-skill` for editable XML, structural validation, preview
    export, and final embedded exports.
  * Selected Font Awesome Free 7.3.0 SVG icons from the official repository;
    Font Awesome states that its Free SVG icons are licensed under CC BY 4.0.
  * BioIcons and the PLOS scientific-figure resource guide were reviewed, but
    their domain-specific assets were not mixed into the diagram because a
    single icon family gives better visual consistency for this computing
    architecture.
- Action:
  * Downloaded the selected Font Awesome Free 7.3.0 SVG files and retained the
    upstream licence and attribution comments.
  * Built the three-panel diagram with editable Draw.io cells and connectors;
    all labels use Times New Roman.
  * Embedded locally rendered 512-pixel transparent icon assets so the Draw.io
    file and its exports have no external image dependency.
  * Moved market-flow labels into fixed white-backed annotations and placed the
    two-way Nash-pricing arrow between Provider A and Provider B after two
    rendered-image inspection passes.
- Commands:
  ```bash
  uv run python figure_sources/build_inference_pricing_framework_drawio.py
  python /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figure_sources/inference_pricing_framework_2026-07-10.drawio
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    --no-sandbox --disable-update -x -e -f png --width 3000 --border 12 \
    -o figures/inference_pricing_framework_2026-07-10.drawio.png \
    figure_sources/inference_pricing_framework_2026-07-10.drawio
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    --no-sandbox --disable-update -x -e -f svg --embed-svg-images --border 12 \
    -o figures/inference_pricing_framework_2026-07-10.drawio.svg \
    figure_sources/inference_pricing_framework_2026-07-10.drawio
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    --no-sandbox --disable-update -x -e -f pdf --crop --border 12 \
    -o figures/inference_pricing_framework_2026-07-10.drawio.pdf \
    figure_sources/inference_pricing_framework_2026-07-10.drawio
  ```
- Outputs:
  * Editable `.drawio` source in `figure_sources/`.
  * Clean preview PNG and final embedded PNG/SVG/PDF in `figures/`.
  * Icon-source and licence record in `figure_sources/`.
- Result:
  * Draw.io structural validation reported `0 error(s), 0 warning(s)`.
  * The final embedded PNG is 3000x1659 pixels; the cropped PDF contains one
    page. PDF inspection confirms embedded Times New Roman regular and bold
    fonts.
  * Python XML parsing succeeded for the editable Draw.io source and exported
    SVG. The embedded PNG was reopened by Draw.io, recovered as editable XML,
    and passed the same structural validator.
  * Visual inspection found no clipped icons, overlapping node text, ambiguous
    Nash-pricing arrow, or missing traffic/information legend.
  * `xmllint` and ImageMagick `identify` were unavailable in the current WSL
    environment; equivalent XML, PNG, and PDF checks used Python, `file`,
    `pdfinfo`, and `pdffonts` without changing the system environment.
- Status: verified.

### 2026-07-10 16:40 - Aesthetic IoT framework-figure screening

- Goal:
  * Find visually polished IoT and smart-energy framework figures from Q1 or
    widely recognized high-impact journals before designing a new manuscript
    figure.
- Context:
  * The user limited this phase to search and screening. No new figure was to
    be generated, and the English and Chinese TeX files were left unchanged.
  * The prior search emphasized structural relevance; this pass additionally
    inspected the original high-resolution figures for visual quality.
- Action:
  * Used the `superpowers:using-superpowers` and `nature-academic-search`
    workflows, publisher article pages, DOI metadata, and publisher-hosted
    high-resolution images.
  * Visually inspected candidate figures from Applied Energy, Nature
    Communications, Nature Energy, Joule, Energy and Buildings, Renewable and
    Sustainable Energy Reviews, Sustainable Cities and Society, Energy and AI,
    and related venues.
  * Rejected candidates with mixed photo/clip-art styles, excessive crossing
    arrows, long labels, or poor readability after reduction.
  * Saved five selected reference images outside the Git repository, with a
    provenance and reuse-boundary note.
- Representative commands:
  ```bash
  curl -L -sS 'https://ars.els-cdn.com/content/image/1-s2.0-S0306261924012510-gr1_lrg.jpg' -o /tmp/iot_framework_search/dai_2024_applied_energy_fig1.jpg
  curl -L -sS 'https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41467-024-53352-9/MediaObjects/41467_2024_53352_Fig2_HTML.png' -o /tmp/iot_framework_search/li_2024_nature_communications_fig2.png
  curl -L -sS 'https://media.springernature.com/full/springer-static/image/art%3A10.1038%2Fs41560-018-0257-2/MediaObjects/41560_2018_257_Fig1_HTML.png' -o /tmp/iot_framework_search/wang_2018_nature_energy_fig1.png
  curl -L -sS 'https://ars.els-cdn.com/content/image/1-s2.0-S2542435121002907-fx1_lrg.jpg' -o /tmp/iot_framework_search/langevin_2021_joule_graphical_abstract.jpg
  curl -L -sS 'https://ars.els-cdn.com/content/image/1-s2.0-S0378778824011836-ga1_lrg.jpg' -o /tmp/iot_framework_search/toderean_2025_ijepes_graphical_abstract.jpg
  ```
- Input:
  * Publisher pages and high-resolution image endpoints for the selected
    papers.
  * The manuscript's current market actors and simulation-loop requirements.
- Output:
  * Updated `docs/reviews/dynamic_electricity_pricing_frameworks_2026-07-10.md`
    with an aesthetic-IoT screening section.
  * Local reference directory:
    `/root/paper_code/0427_tokenrl/paper_reference_figures/iot_frameworks_2026-07-10/`.
  * Local provenance file: `SOURCES.md` in that directory.
- Result:
  * Best market-structure reference: Dai et al. (2024), Applied Energy,
    Fig. 1, with Smart Homes, Microgrids, and DSO as three visually coherent
    tiers.
  * Best IoT-layer reference: Li et al. (2024), Nature Communications,
    Fig. 2, with end, edge, and cloud layers.
  * Best price-response reference: Wang (2018), Nature Energy, Fig. 1, with
    devices, homes, neighbourhood, and grid feedback.
  * Joule and Energy and Buildings examples were retained as layout-density
    references rather than direct content templates.
- Decision:
  * The later original figure should combine the three-tier clarity of Dai et
    al. with the spatial hierarchy of Li et al. and the price-response semantics
    of Wang, while using the restrained spacing of the Joule example.
  * Source figures remain local research references and will not be placed in
    manuscript assets or redistributed as original work.
- Next:
  * Await user approval before drafting an original image-generation prompt.
- Verification commands:
  ```bash
  file /root/paper_code/0427_tokenrl/paper_reference_figures/iot_frameworks_2026-07-10/*
  for doi in '10.1016/j.apenergy.2024.123868' '10.1038/s41467-024-53352-9' '10.1038/s41560-018-0257-2' '10.1016/j.joule.2021.06.002' '10.1016/j.enbuild.2024.115067'; do curl -L --silent --show-error --max-time 30 -o /dev/null -w "$doi %{http_code}\n" "https://doi.org/$doi"; done
  git diff --check
  git status --short
  ```
- Verification output:
  * All five local files were recognized as valid JPEG or PNG images. Their
    dimensions range from 950x1085 to 3219x1268 pixels.
  * All five DOI endpoints returned HTTP 200.
  * `git diff --check` completed without whitespace errors.
  * Git status contains only the pre-existing README/report documentation
    changes from this literature-search task; no TeX or manuscript figure file
    was modified.
- Status: verified.

### 2026-07-10 21:59 - 计算机论文图标来源与许可审计

- 目标：
  * 核对小红书和哔哩哔哩中计算机论文框架图常用的图标来源，并判断哪些来源适合公开、可编辑的 Draw.io 论文资产。
- 背景：
  * 当前 Figure 1 使用 Font Awesome Free，许可清楚，但视觉更接近通用 UI 图标；用户希望了解计算机论文作者实际使用的图标来源。
  * 本轮只做检索和许可审计，不修改 Draw.io、TeX 或论文图。
- 操作：
  * 使用独立的有头 Chrome 配置访问已登录的小红书，检索“计算机论文 图标”“论文 icon 网站”“科研框架图 图标素材”“计算机顶会 绘图 图标”和“物联网 论文 绘图 图标”。
  * 交叉检查哔哩哔哩中的科研绘图经验，并回到 IconPark、Tabler、Material Design Icons、Font Awesome、Remix Icon、Streamline、Flaticon、Icons8、Iconfinder、IconScout 和 Iconfont 官方页面核对许可。
  * Chrome 在本地独立用户目录中持久化登录状态；没有读取、导出或写入 Cookie、令牌及其他凭据。
- 输入：
  * 社交平台的公开绘图经验帖、素材库官方许可页面，以及当前 Figure 1 的图标来源记录。
- 输出：
  * `docs/reviews/computer_paper_icon_sources_2026-07-10.md`。
- 初步结果：
  * 社区中出现最多的是 Flaticon、Iconfont、Iconfinder、IconPark、Icons8 和 IconScout，但高频使用不等于许可适合公开源文件。
  * 对本论文而言，Apache-2.0 的 IconPark 是下一版 Draw.io 的首选；商业或混合许可素材应逐项核验，不能直接从帖子或预览图复制。
- 决策：
  * 本轮不改图。后续如重绘，优先采用单一 IconPark 图标家族，并保留版本、来源和许可记录。
- 下一步：
  * 用户确认下一版视觉方向后，再考虑把当前 Font Awesome 图标替换为 IconPark；本轮不修改论文资产。
- 验证命令：
  ```bash
  git diff --check
  rg -n -i '(xsec_token|access_token|refresh_token|web_session|authorization)=[^[:space:]]+' \
    docs/reviews/computer_paper_icon_sources_2026-07-10.md
  rg -o 'https://[^) ]+' docs/reviews/computer_paper_icon_sources_2026-07-10.md | sort -u | wc -l
  test -d /mnt/c/Users/cccht/AppData/Local/Temp/codex-xhs-browser-profile
  pgrep -af 'remote-debugging-port=9223'
  ```
- 验证结果：
  * `git diff --check` 无输出，未发现空白错误。
  * 新报告中的敏感参数赋值形式扫描无匹配；报告仅保留不含登录参数的公开页面链接。
  * 报告包含 25 个去重后的公开链接。
  * 独立 Chrome 配置目录存在，远程调试端口对应的有头 Chrome 进程仍在运行；未读取任何 Cookie 文件内容。
  * 本轮未修改 Draw.io、TeX、参考文献、实验数据或论文图。
- 状态：verified。

### 2026-07-12 18:10 - 扩大中间商响应空间并全量重求均衡

- 目标：消除旧中间商有限响应集对 13.03% 峰值降幅、17.08% 最大利用率降幅和 $0.888\rightarrow0.976$ 最低 QoS 改善的条件性限制；在扩大后的响应空间内重新求解统一定价与分时定价博弈，并重做偏离和稳健性检查。
- 背景：16:45 的专项复审发现旧响应集只有 18 个候选点，且主动态策略对应的中间商路由灵敏度为 $\beta=4.0$，正文误写为 1.5。固定服务商策略下扩大搜索后，中间商收益在更高 $\beta$ 处继续增加，说明旧上界会约束最优响应。
- 计划：
  * 比较宽离散全集、连续多起点优化和带边界审计的混合求解，记录精度、边界命中和单策略对耗时。
  * 先写失败测试，再实现扩展中间商响应、搜索诊断和候选参数序列化。
  * 在 225 个服务商候选策略上重新求解统一与动态有限博弈，扫描所有对最终支持集的单边偏离，并执行离网局部偏离检查。
  * 重算关键参数和结构敏感性；结果稳定后再更新图表、英文终稿和 claim--evidence 审计。
- 验收：中间商搜索不再被未报告的旧上界截断；所有使用中的固定点满足既定容差；服务商有限网格 regret 和离网 regret 明确报告；所有摘要数字均来自新工件；LaTeX、回归测试和图文一致性检查通过。
- 当前输入：`pricing_sim/spatiotemporal_game.py`、`experiments/final_equilibrium_tools.py`、`experiments/run_final_spatiotemporal_equilibrium.py`、`artifacts/peak_shaving/20260712_final/spatiotemporal_equilibrium.json`。
- 红灯测试：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_intermediary_response_optimizer.py \
    tests/test_final_spatiotemporal_equilibrium.py -q
  ```
  * 新增的两项中间商连续响应测试按预期因 `pricing_sim.intermediary_response` 尚不存在而失败。
  * 三项既有均衡流水线测试因该命令未注入仓库未声明的 `nashpy` 而失败；这是测试环境缺少可选运行依赖，不作为功能红灯。后续命令固定使用 `uv run --no-project --with numpy --with scipy --with nashpy`。
- 已实现：
  * 新增 `pricing_sim/intermediary_response.py`，在零、适中和近确定性三个路由区域分别进行确定性粗定位与 L-BFGS-B 局部优化；零售基价默认覆盖完整价格区间，零售斜率扩展到 $[-1,1]$，路由灵敏度扩展到 $[0,10^6]$。
  * 搜索工件记录粗定位点数、局部优化成功数、函数评估次数、参数边界命中和近确定性路由，且用显式数值并列最优规则选择较小的路由灵敏度。
  * 保留旧有限网格接口作为回归模式；默认终稿均衡改用连续多起点中间商响应，统一定价场景只把零售斜率约束为 0。
  * `active_profiles` 现在保存所有正概率均衡剖面的服务商策略、中间商参数、收益、固定点 residual 和搜索诊断，避免正文参数与工件脱节。
- 阶段验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with numpy --with scipy --with nashpy python -m pytest \
    tests/test_intermediary_response_optimizer.py \
    tests/test_spatiotemporal_game.py \
    tests/test_final_spatiotemporal_equilibrium.py -q
  ```
  * 结果为 `10 passed in 6.08s`。
  * 主动态旧策略对上的中间商收益由旧 18 点网格约 157.17 提升到约 181.56；另一极端服务商组合的最优响应为 $\beta\approx0$，说明三区域搜索确实覆盖了不同响应类型。
- 并行基准与修复：
  * 同一批 8 个策略对串行耗时 15.142 s，8 进程耗时 3.000 s，服务商收益、中间商收益和所选 $\beta$ 的校验和逐项一致。
  * 线程池在超过 60 s 后仍未完成，因线程争用由本任务主动中断，退出码为 130；后续不使用线程池。
  * 加入进程池后新增串并行一致性测试。首次结构回归中有 1 项失败：线程限制被写在 `command` 字段前，违反既有 `uv run` 前缀断言。现已把 `OMP_NUM_THREADS`、`OPENBLAS_NUM_THREADS` 和 `MKL_NUM_THREADS` 独立记录在 `environment` 字段。
- 首次全量重算失败与修复：
  * 225 点主均衡运行到约 18 分钟后，进程池子任务已结束，但主进程持续停留在单核受限博弈求解，未生成新工件。本任务主动中断自有进程，退出码为 130；旧工件未覆盖。
  * 根因是 `pricing_sim/finite_game.py` 在找到有效均衡后仍完整消费 Nashpy 0.0.43 的 `support_enumeration`。本地实现会遍历全部等规模支持组合；随机和退化 `10×10` 矩阵均超过 8 s 门限，而随机 `10×10` 的第一个均衡约 0.03 s 即可得到。
  * 新增两项红灯测试，分别要求有纯均衡时不得调用支持枚举，以及大矩阵无纯均衡时不得消费第二个混合候选；修复前两项均按预期失败。
  * 修复后先以 $O(mn)$ 扫描全部纯策略纳什均衡。不存在纯均衡时，最大维度不超过 8 才完整枚举混合均衡；更大受限博弈停止于第一个有效混合候选。该变更消除了“找到纯均衡后仍穷举全部混合支持”的无界耗时。
  * `tests/test_finite_game.py` 修复后为 `5 passed in 0.32s`。
- 第二次全量重算失败与修复：
  * 根因修复后的第二次运行顺利完成统一定价博弈，并在动态博弈中完成 6 轮、缓存 3102 个策略对；随后停在无纯均衡的 `6×8` 受限子博弈。任务再次主动中断，退出码为 130，未写入不完整工件。
  * 证据表明“维度不超过 8 即完整支持枚举”的门限仍不可靠：退化的 `6×8` 收益矩阵同样可能产生大量混合支持。
  * 将红灯测试改为 `6×8` 无纯均衡矩阵，要求只消费第一个有效混合候选；旧实现按预期在请求第二个候选时失败。
  * 最终规则改为：全部检查纯策略均衡；若不存在纯均衡，则不论矩阵规模，只接受支持枚举返回的第一个有效混合均衡。该规则保证混合候选数量有界，但不声称枚举了全部受限混合均衡。
  * 修复后的有限博弈、连续中间商响应、时空市场和最终流水线测试合计 `16 passed in 5.71s`。
  * 下一次长运行将在每轮全偏离扫描后把本地策略对缓存写入 `/tmp` 临时检查点；该临时文件不作为论文工件，不写入仓库。
- 第三次全量重算诊断与最终混合求解修复：
  * 第三次运行写入了统一 45 对、动态 3102 对的 `/tmp` 检查点，并复现了前 6 轮相同支持路径；在 `6×8` 无纯均衡子博弈中，首个支持枚举均衡本身仍未在 30 s 内返回。任务主动中断，退出码为 130，已完成收益缓存保留。
  * 从检查点重建出真实 `5×6`、`6×7` 和 `6×8` 受限收益矩阵。前两者最终由 Lemke--Howson 标签 0 给出有效均衡；实际 `6×8` 上标签 0、1、2、3、6--12 均在约 1 ms 内给出 restricted regret 不高于 $2.3\times10^{-13}$ 的有效均衡，标签 5 和 13 超过 5 s，首个顶点枚举候选约 0.10 s。
  * 最终实现不再调用支持枚举：先完整扫描纯策略均衡；若不存在纯均衡，则在独立 `fork` 进程中运行固定标签 0 的 Lemke--Howson，5 s 超时后强制终止，并要求返回候选的 restricted regret 不高于 $10^{-7}$。失败时明确报错，不再无界等待。
  * 实际 `6×8` 矩阵通过新实现于约 0.25 s 返回，restricted regret 为 0；相关回归合计 `16 passed in 5.83s`。
- 225 点扩展响应均衡与服务商边界诊断：
  * 从 3102 对检查点恢复后，动态 double oracle 在第 8 轮收敛；共评估 3537 个策略对，full-grid regret 为 $1.14\times10^{-13}$，最大 joint residual 为 $1.00\times10^{-9}$。统一博弈为纯策略，动态博弈为 4×4 个正概率组合的混合策略。
  * 相对统一定价，动态策略的聚合峰值降幅为 4.688%，最大服务商利用率降幅为 15.406%，最低 QoS 增加 0.07263，服务商与中间商利润之和增加 4.018%。这些数字取代旧响应集下的 13.03%、17.08% 和 $0.888\rightarrow0.976$，但尚不是终稿数字。
  * 全缓存 3537 对中，3 个非活跃策略对命中 $\beta=10^6$。固定零售参数将 $\beta$ 从 $10^3$ 扫到 $10^9$ 时，中间商收益变化不超过约 $7.1\times10^{-10}$，路由最大概率为 0.9999999992；因此这些是近确定性路由平台，不是收益仍随上界增加的截断。
  * 定向服务商边界诊断评估 239 个候选、1896 个策略对，耗时 395.884 s，最大 residual 为 $9.99\times10^{-10}$。服务商 A 的最佳边界偏离为 $(0.25,0,0.6,0)$，绝对 regret 49.887、相对 regret 6.036%；服务商 B 的最佳偏离为 $(0.25,0.6,0.6,0.2)$，绝对 regret 3.655、相对 regret 0.483%。当前 225 点结果因此明确不满足投稿门禁。
  * 新增 `expanded_provider_candidate_grid()`：批发基价取 $\{0.25,0.575,0.90\}$，直连基价取 $\{0.45,0.60,1.10,1.60\}$，两类斜率均取 $\{-0.6,-0.4,-0.2,0,0.2,0.4,0.6,0.8\}$，共 768 点。旧 `fine_candidate_grid()` 保留供历史回归。
  * 扩展网格、有限博弈、中间商响应、时空市场、主流水线和敏感性测试合计 `23 passed in 6.05s`。
  * 阶段工件：`artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_equilibrium.json` 与 `expanded_provider_boundary_diagnostic.json`。
- 768 点主均衡运行与混合求解器架构修复：
  * 768 点统一博弈在 3 轮内完成。动态博弈前 6 轮累计缓存 13,743 个策略对；第 6 轮完成 `9×9` 受限收益矩阵后，固定标签 0 的 Lemke--Howson 返回无效候选，主作业按设计报错退出，正式 JSON 未写入，检查点完整保留。
  * 从检查点重建真实 `9×9` 矩阵。标签 0、4、5、9、13 返回无效候选；标签 1、7、8、10、11、15--17 超过 5 s；标签 2、3、6、12、14 在约 1 ms 内给出 restricted regret 不高于 $1.14\times10^{-13}$ 的均衡；首个顶点枚举候选约 2.39 s、regret 为 $2.27\times10^{-13}$；支持枚举约 7.26 s 后未找到候选。诊断 shell 因末尾条件表达式返回退出码 1，但各子求解结果已完整输出。
  * 单标签架构由 `pricing_sim/bimatrix_solver.py` 取代。新求解器在独立进程中并行运行最多 8 个 Lemke--Howson 标签和一个顶点枚举，统一 5 s 总门限；超时进程终止，所有返回候选均需通过 restricted regret $\le10^{-7}$ 的校验，再按 full-grid regret 选择。
  * 实际 `9×9` 矩阵在 5.02 s 内得到一个去重均衡候选；标签 2、3、6 和顶点枚举交叉返回同一策略，restricted regret 为 $1.14\times10^{-13}$。相关测试新增“标签 0 无效时必须由其他标签恢复”，合计 `24 passed in 6.18s`。
- 768 点扩展服务商策略域结果与高斜率诊断：
  * 动态博弈在 8 轮内完成，评估 16,018 个去重策略对，full-grid regret 为 $2.27\times10^{-13}$；统一博弈评估 95 对并收敛到纯策略。相对统一定价，动态策略的聚合峰值变化为 $-11.524\%$，最大利用率变化为 $-17.575\%$，最低 QoS 增加 0.07779，服务商与中间商合计利润增加 $0.246\%$。
  * 动态均衡中服务商 A 的批发价格斜率 0.8 占 57.4% 概率，说明 768 点网格的斜率上界仍可能约束结果，不能把该工件作为终稿主证据。
  * 高斜率保护诊断评估 140 个候选、1,375 个策略对，耗时 273.679 s。服务商 A 在斜率 1.5 处获得最佳偏离，绝对 regret 为 13.472、相对 regret 为 1.585%；斜率 2.0 和 3.0 的收益均下降。服务商 B 未发现正 regret。该结果说明收益峰值位于原网格外，但未持续向更高斜率增长。
  * 新增 `guard_enriched_provider_candidate_grid()`，在 768 点基础网格上加入低价格区域的 1.0、1.2、1.5、2.0 和 3.0 高斜率保护层，共 892 个唯一策略。相关回归合计 `25 passed in 6.39s`。
- 892 点服务商策略域与连续中间商响应的全量重求解：
  * 执行命令：
    ```bash
    TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
      --with numpy --with scipy --with nashpy \
      python -m experiments.run_final_spatiotemporal_equilibrium
    ```
  * 从精确迁移的 768 点收益缓存继续计算；最终动态缓存含 26,214 个去重策略对，正式工件为 `artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_equilibrium_provider892.json`。最后一次续算耗时 250.464 s，工件时间为 2026-07-12 21:45:15 +08:00。
  * 统一定价博弈为纯策略，full-grid regret 为 0；动态博弈为 8×8 支持的混合策略，full-grid regret 为 $2.27\times10^{-13}$、相对 regret 为 $2.61\times10^{-16}$，最大 routing--QoS residual 为 $9.98\times10^{-10}$。
  * 动态支持中的最大批发价格斜率为 1.5；保护层中的 2.0 和 3.0 未进入支持集。服务商 A 在 1.5 上的概率为 0.4001，服务商 B 在 1.5 上的概率为 0.0332，因此还需针对 1.5 周围及 3.0 之外执行连续或离网偏离诊断，但原 0.8 上界截断已解除。
  * 64 个正概率联合剖面的中间商搜索均完成 3 次局部优化；零售基价和零售斜率均未命中有效边界。21 个剖面选择 $\beta=0$，占联合概率 0.3099；这是路由无差异端点，不是高端截断。其余剖面的最大 $\beta$ 为 2595.87，远低于 $10^6$ 上界，28 个剖面处于近确定性路由平台。
  * 相对统一定价，动态策略的聚合峰值变化为 $-12.851\%$，最大服务商利用率变化为 $-17.532\%$，最低 QoS 增加 0.06855（相对 $+7.703\%$），跨时段移动比例增加 0.01610。服务商与中间商合计利润增加 $0.726\%$；该指标不是社会福利，也不支持稳健利润提升主张。
  * 上述数字目前只证明 892 点有限服务商策略域内的低 regret 结果。域外偏离、关键参数全量重求解、图表和正文尚未更新，因此状态保持 `in_progress`。
- 892 点域外偏离诊断红灯：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy --with scipy --with nashpy \
    python -m pytest tests/test_final_offgrid_diagnostic.py -q
  ```
  * 结果为 `4 failed`，退出码 1。失败分别来自缺少宽域候选生成器，以及旧入口不接受均衡路径和并行工作进程参数；符合本轮先定义新诊断契约的预期。
  * 新契约要求读取 892 点连续中间商响应工件，服务商基价覆盖模型完整价格边界，两个斜率覆盖 $[-4,4]$，并同时包含活跃支持点、Latin-hypercube 全局样本和逐轴边界保护点。
  * 实现后将候选设计、带签名临时缓存和混合期望收益汇总拆到 `experiments/offgrid_diagnostic_tools.py`；入口脚本只负责工件验证、场景重建和元数据。两个文件均低于 300 行，所有函数均不超过 50 行。
  * 定向回归命令覆盖域外诊断、中间商响应、主均衡、有限博弈、时空市场和策略网格，结果为 `27 passed in 6.65s`。
  * 真实连续响应烟雾测试使用 1 个对手支持点、1 个 Latin-hypercube 样本及结构保护点，共计算 20 个策略对；20 个固定点全部收敛，最小成功局部优化数为 3，最大 residual 为 $9.50\times10^{-10}$，缓存序列化和并行汇总均正常。该烟雾测试不用于论文结论。
  * 正式宽域审计中，服务商 A 已完成 658 个候选、5,264 个“候选 × 对手混合支持”策略对。只读缓存复算发现局部保护候选 $(0.2825,1.0,0.6,0.2)$ 的期望收益为 872.524，比当前混合均衡收益 870.169 高 2.355，相对 regret 为 0.271%。八个活跃支持策略的收益复算误差不超过 $3.41\times10^{-13}$，因此该偏离不是数值汇总误差。892 点结果尚未通过域外门禁，需等待服务商 B 审计后共同扩充策略集并重求。
  * 正式命令于 2026-07-12 22:41:53 +08:00 完成，退出码 0，wall time 2,572.66 s、最大常驻内存 324,552 KB。服务商 B 完成 662 个候选、5,296 个策略对，最佳候选为其活跃支持点，regret 仅 $1.14\times10^{-13}$。
  * 两位服务商的全部候选固定点均收敛，最大 residual 分别为 $9.999\times10^{-10}$ 和 $9.998\times10^{-10}$。A 的最高偏离在全部八个对手支持剖面上均有 3 次成功中间商局部优化，最大 $\beta$ 为 5913.58，未命中 $10^6$ 高端边界；因此该正 regret 是服务商策略分辨率问题。
  * 个别非最优宽域候选只有 2 次成功局部优化，且某些非最优剖面位于近确定性路由平台。正式工件保留最小成功次数和最大 $\beta$，终稿不会以这些非最优点形成经济结论。
  * 正式输出：`artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_offgrid_diagnostic_provider892.json`，SHA-256 为 `d97cef59d423f7e2ef72256576396dad9491135364b4ba5ed3209cb303ccfee2`；两位服务商临时缓存各约 27 MB，不纳入仓库。
  * 工件生成后重跑域外诊断测试，结果为 `4 passed in 0.71s`。
  * 新增二维参数平面加密红灯测试，首次运行因 `_pairwise_refinement` 尚不存在得到 `1 failed, 4 passed`；实现后为 `5 passed in 0.38s`。加密围绕第一阶段最高收益点，对六组参数对采用域宽 1.25%、2.5% 和 5% 的对称步长。
  * 二维加密新增 A 的 228 个候选、1,824 个策略对和 B 的 160 个候选、1,280 个策略对，wall time 778.79 s。A 的最高偏离更新为 $(0.2825,1.0,0.579375,0.4)$，绝对/相对 regret 为 4.929/0.566%；B 的最高偏离为 $(0.25,0.4,0.55875,0.4)$，绝对/相对 regret 为 3.304/0.441%。两者均来自 `pairwise_refinement`，所有对应内层优化均有 3 个成功局部起点。
  * 更新后的正式域外工件包含 A 的 886 个候选、7,088 个策略对和 B 的 822 个候选、6,576 个策略对；SHA-256 为 `29f448ddf8f84cb02f24dc6631a17365722671d0db90afafbd66aabc30334920`。892 点均衡因此明确未通过最终域外门禁。
  * 新增 `audit_enriched_provider_candidate_grid()`：A 区域加密低批发基价、0.8--1.2 批发斜率、0.559--0.621 直接基价和 0.2--0.4 直接斜率；B 区域覆盖 0--0.6 批发斜率、0.538--0.600 直接基价和 0.3--0.6 直接斜率。该对称策略集共 1,370 个唯一候选，完整包含旧 892 点。网格测试先因缺失函数失败，实现后为 `7 passed in 4.76s`。
  * 新增向量键收益缓存与并行检查点。红灯为缺少缓存模块和 `PairEvaluator` 回调的 `2 failed`；实现后缓存单元测试与管线重复运行测试为 `3 passed in 0.61s`。缓存签名包含场景、中间商响应规格、需求/QoS 输入和核心评价源码，候选索引变化时按四参数向量精确重映射。
  * 将旧 892 点的 26,214 个动态收益和 95 个统一收益迁移到 `/tmp/peak_shaving_audit_enriched_equilibrium/`；在 1,370 点新网格上精确映射回 26,214 对。相关均衡、缓存、网格、中间商、固定点和有限博弈回归合计 `32 passed in 11.46s`。
  * 1,370 点主均衡首次续算运行 4,780.84 s 后，在第六次受限混合求解时报错 `bounded mixed-solver ensemble returned no valid restricted equilibrium`，退出码 1；未写出不完整 JSON。此前统一博弈已完成，动态收益缓存从 26,214 增至 44,742 对，原子检查点完整保留。失败属于受限双矩阵求解器，不是 fixed-point 或中间商优化失败。
  * 缓存重放将首次失败定位为 12×12 受限矩阵。全部 24 个 Lemke--Howson 标签在原支付尺度下均未返回有效策略；顶点枚举在 116.90 s 后返回 restricted regret $1.14\times10^{-13}$ 的有效 8×8 支持均衡。曾据此把门限从 60 s 提高到 300 s，相关红灯/回归为 `1 failed` 后 `10 passed`。
  * 从 12×12 支持续跑后又新增 5,428 个支付至 50,170 对，并在 14×14 受限矩阵再次失败，wall time 1,979.57 s。通过缓存中完整行/列覆盖直接恢复 14 个行支持和 14 个列支持，无需重算支付。
  * 对 14×14 支付分别做正仿射归一化后，前 8 个 Lemke--Howson 标签全部返回有效均衡；全部 28 个标签中 22 个有效，原支付 regret 为 0 至 $2.27\times10^{-13}$。正仿射变换保持每位玩家的最佳响应与纳什均衡不变，返回策略仍在原支付上验算。
  * 新增“求解器调用 Nashpy 前必须归一化”和“有效 Lemke 候选必须终止慢顶点分支”红灯。旧实现分别报无有效均衡和耗时 0.527 s 超过 0.4 s 门禁；修复后有限博弈、缓存和管线测试为 `12 passed in 0.92s`。
  * 最终混合求解器将每位玩家支付独立缩放到 $[0,1]$，只把归一化 regret 不超过 $10^{-10}$ 的快速候选作为提前停止信号，并在原始支付上继续执行 $10^{-7}$ 的正式过滤。14×14 真实失败矩阵现在 0.354 s 内返回，原支付 restricted regret 为 0；门限回调到 120 s 作为顶点后备，不再依赖不断加时。
  * 从 14×14 支持继续后，动态缓存增至 63,705 对并在 19×19 受限矩阵失败，wall time 3,410.93 s。完整 38 标签诊断在 2.11 s 内发现标签 29 的 11×11 支持均衡，原支付 regret 为 $1.14\times10^{-13}$；前 8 个标签无有效候选。新增高编号标签红灯后，将 Lemke--Howson 覆盖扩展为完整 $m+n$ 标签、上限 64；真实 19×19 矩阵现于 1.07 s 返回，相关测试 `13 passed in 0.92s`。
  * 从 19×19 支持继续后，动态缓存增至 71,802 对，并在 22×22 受限矩阵再次失败，wall time 2,173.71 s。说明仅靠 Nashpy 标签与顶点分支仍不足，且继续增加超时没有依据。
  * Fischer--Burmeister 互补原型首次命令因输出文件名引号错误在执行前报 `SyntaxError`，未启动优化；修正后从上一均衡嵌入启动，30 次函数评估得到原支付 regret $7.29\times10^{-7}$ 的近似候选。清理两个约 $10^{-8}$ 的伪概率后，在识别出的 11×11 支持上解线性无差异方程；支持概率均为正、外部动作松弛分别至少 0.00249/0.00227，原支付 regret 为 $8.41\times10^{-12}$。
  * 新增 `pricing_sim/complementarity_solver.py`：Nashpy 全部候选无效时，使用上一轮混合概率的扩展 warm start 求 Fischer--Burmeister 互补残差，再按多个阈值识别支持并线性精修。备用候选仍由原支付 $10^{-7}$ 门禁过滤；不会以残差或优化器 `success` 代替 regret。
  * 新增互补备用与混合概率嵌入红灯，旧实现分别因缺少参数和函数得到 `2 failed`；实现后定向测试 `2 passed`。真实 22×22 矩阵现于 0.231 s 返回 11×11 精修支持，原支付 regret 为 $2.27\times10^{-13}$；相关均衡、缓存、网格、固定点和域外诊断回归合计 `38 passed in 11.08s`。
  * 从 19×19 检查点重放后，受限支持依次扩展到 20×20、21×21、22×22、23×23 和 24×24；对应 full-grid regret 依次为 1.457、1.091、0.260、0.0731 和 0.0195。动态缓存增至 78,536 个策略对，随后在加入列策略 268 后的 24×25 受限博弈失败；正式 1,370 点 JSON 未写入。
  * 24×25 的 Fischer--Burmeister 最小二乘虽然报告成功，但归一化 regret 仍为 $2.73\times10^{-5}$，原支付 regret 为 0.00822。其 12 个主要行支持近似满足无差异条件，而 13 个正概率列动作仍有 $1.1\times10^{-5}$ 至 $4.8\times10^{-5}$ 的收益差。逐阈值线性精修、单列剔除和单行加入均不能同时满足正概率与支持外最优响应条件，确认问题是非线性最小二乘停在近似驻点，而不是支持阈值误选。
  * Nashpy 的全部 Lemke--Howson 与顶点分支在 120.65 s 内未返回任何 24×25 候选。随后将归一化支付上的 Nash 互补条件写成混合整数线性可行性问题：二元变量标识支持动作，正概率动作强制收益松弛为零，所有动作收益不超过各自均衡值。由于支付已缩放到 $[0,1]$，big-M 精确取 1；返回策略仍在原支付矩阵上验算。
  * 一次性 HiGHS 原型在 0.91 s 内找到 11×11 支持均衡，归一化 regret 为 $3.33\times10^{-16}$、原支付 regret 为 $3.41\times10^{-13}$。据此新增 `pricing_sim/milp_equilibrium_solver.py`，仅在 warm-start 互补解失败时先于慢 Nashpy 分支调用；无 warm start 时仍保留原快速 Lemke--Howson 首选路径。
  * MILP 回退红灯测试先按预期因进入 Nashpy 分支失败；实现后的目标测试为 `1 passed in 0.23s`。真实 24×25 矩阵通过正式接口在 3.92 s 内返回，方法标记为 `highs_milp_complementarity`，原支付 regret 为 $3.41\times10^{-13}$。
  * 完整定向回归命令：
    ```bash
    TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
      --with pytest --with numpy --with scipy --with nashpy \
      python -m pytest \
      tests/test_finite_game.py \
      tests/test_equilibrium_cache.py \
      tests/test_peak_shaving_submission_tools.py \
      tests/test_intermediary_response_optimizer.py \
      tests/test_spatiotemporal_game.py \
      tests/test_final_spatiotemporal_equilibrium.py \
      tests/test_final_offgrid_diagnostic.py -q
    ```
    结果为 `39 passed in 11.29s`。4 条警告均为 Python 3.12 对多线程父进程调用 `fork()` 的弃用提示；数值断言全部通过，进程启动方式将在终稿工程清理阶段单独审计。
  * 1,370 点正式续算命令从 19×19 支持向量和 78,536 对缓存启动，wall time 4:39.06、最大常驻内存 2,946,580 KB，退出码 0。第 7 轮的 24×25 MILP 均衡仍有 full-grid regret 0.1073，加入新的列最佳响应后，第 8 轮 24×26 受限博弈达到 full-grid regret $3.41\times10^{-13}$；最终正概率支持为 11×11，共存储 79,882 个策略对。
  * 正式工件为 `artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_equilibrium_provider1370.json`，SHA-256 为 `2794c2647b31ac1aa9d644799555bbeaf12d49433f5372457e221800c6e49cb6`。统一博弈 full-grid regret 为 0；动态/统一最大 joint residual 分别为 $9.93\times10^{-10}$ 和 $7.98\times10^{-10}$，全部需求守恒为 1100（浮点误差小于 $5\times10^{-13}$）。
  * 相对统一定价，动态均衡的聚合峰值变化为 $-12.997\%$，最大服务商利用率变化为 $-15.182\%$，最低 QoS 从 0.88992 提升到 0.95521，跨时段移动比例增加 0.01554。服务商与中间商利润之和变化为 $-0.594\%$，因此新结果仍只支持 QoS/拥塞主张，不支持利润改善。
  * 121 个正概率联合剖面的中间商局部搜索均有 3 次成功运行，零售基价和斜率均未命中边界；41 个剖面命中的是允许的 $\beta=0$ 下端，联合权重 0.3377。最大正 $\beta$ 为 48,728，远低于 $10^6$ 上界；没有活跃剖面命中高端截断。
  * 将域外审计默认输入、输出和缓存从 `provider892` 切换到 `provider1370`。对应红灯先因旧默认文件名得到 `1 failed`，实现后 `tests/test_final_offgrid_diagnostic.py` 为 `5 passed in 0.38s`。
  * 新 1,370 点均衡的正式域外审计已完成 A 方 733 个全局/一维保护候选和 172 个二维加密候选。512 个 Latin-hypercube 点未发现正偏离，但局部保护先发现 `[0.25,0.8,0.538125,0.3]` 的 regret 0.211；二维加密进一步在 `[0.25,0.1,0.5175,0.3]` 发现绝对/相对 regret 12.291/1.445%。该候选在 11 个对手支持剖面上全部固定点收敛，每个中间商求解均有 3 个成功局部起点，最大 residual 为 $8.78\times10^{-10}$。因此 1,370 点结果尚未通过域外门禁；B 方审计仍在运行，当前结果不进入论文。
  * 完整 A/B 域外审计 wall time 为 1:21:09、最大常驻内存 409,376 KB，退出码 0。A 共评估 905 个候选/9,955 个策略对；B 共评估 902 个候选/9,922 个策略对。两侧全部固定点收敛，最大 residual 均低于 $10^{-9}$；少数非最优候选只有 2 次成功中间商局部运行或命中 $\beta=10^6$ 平台，但两侧最高偏离均有 3 次成功局部运行且最大 $\beta$ 分别仅为 6,004 和 870。
  * B 的最高偏离为 `[0.26625,1.5,0.55875,0.2]`，绝对/相对 regret 为 7.574/1.000%。活跃支持收益复算误差 A/B 分别不超过 $3.41\times10^{-13}$ 和 $2.27\times10^{-13}$，排除了混合权重汇总错误。
  * 正式工件为 `artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_offgrid_diagnostic_provider1370.json`，SHA-256 为 `8e097f4bd303e9c3f87c0e87eae210a9908d6bee2d08fe35d0b8bb6a979a89a7`；其记录的均衡 SHA-256 与 `provider1370` 主工件一致。
  * 新增 `second_audit_enriched_provider_candidate_grid()`。A 区域对称覆盖批发基价 0.25--0.26625、批发斜率 0--0.3、直连基价 0.48656--0.55875 和直连斜率 0.1--0.4；B 区域覆盖批发基价 0.25--0.2825、批发斜率 1.3--1.8、直连基价 0.538125--0.579375 和直连斜率 0.1--0.5。新网格共 2,380 个唯一策略，完整包含旧 1,370 点并新增 1,010 点。
  * 第二层网格和主入口测试先分别因缺少构造器、入口仍使用旧网格而失败；实现后完整求解器、缓存、策略网格、中间商响应、时空市场、主均衡和域外诊断回归为 `41 passed in 6.86s`。4 条警告仍是 Python 3.12 的 `fork()` 弃用提示。
  * 2,380 点续算成功按向量映射旧 79,882 对缓存，并从旧 11×11 正概率支持启动。首轮完整扫描结束于 102,102 对；随后 double oracle 逐轮扩展支持，第 11 轮结束于 149,311 对，第 12 轮运行中缓存达到 151,360 对。
  * 长作业在 wall time 4:52:42 后被系统以退出码 137 终止，正式 `provider2380` JSON 未生成。内核 `dmesg` 明确记录 `global_oom`，被杀主进程匿名 RSS 约 3.4 GiB；当时动态缓存文件为 777 MiB。数值求解和固定点没有报错，最近一次原子检查点完整保留。
  * 根因是 `ProcessPoolExecutor` 默认 `fork`：16 个工作进程在父进程已加载大型 Python 对象缓存后创建，持续运行中的写时复制放大内存。此前 Python 3.12 的 4 条弃用警告正对应这一风险。仅降低 worker 数不能消除大型父缓存继承，下一步改为 `spawn` 上下文并以可导入模块入口续算。
  * 新增进程上下文红灯，旧实现因 `ProcessPoolExecutor` 缺少 `mp_context` 按预期失败；修复后显式使用 `multiprocessing.get_context("spawn")`。目标测试确认 spawn 调用，实际串并行支付与中间商候选保持一致，且不再产生 Python 3.12 的 fork 警告。
  * 新增正式模块入口 `experiments/run_submission_spatiotemporal_equilibrium.py`：优先读取已完成 `provider2380`，否则读取 `provider1370` 的正概率支持作为续算种子；记录准确命令、入口源码哈希和种子工件哈希；仅在完整结果返回后用临时文件替换正式 JSON。
  * 入口与 spawn 测试先因模块缺失失败，实现后 3 项目标测试通过；有限博弈、缓存、策略网格、中间商响应、时空市场、主均衡和域外诊断完整回归为 `43 passed in 7.74s`，不再有 multiprocessing 警告。
- 下一步：使用正式模块入口从 151,360 对缓存恢复第 12 轮，确认 spawn 下内存稳定并继续至 full-grid regret 通过门禁。
- 状态：in_progress。

### 2026-07-14 09:09 - 修正后离网偏差审计续跑

- 目标：确认 719 个审计自适应服务商候选得到的混合均衡，在预先声明的有界连续价格参数域内不存在超过 `0.5%` 的相对有利偏差。
- 操作：复核独立进程、子进程、日志、缓存和退出文件；不修改模型、中间商响应、候选生成或离网审计源码。
- 命令：
  ```bash
  pid=$(cat /tmp/peak_shaving_submission_offgrid.pid)
  ps -o pid,ppid,stat,etime,%cpu,%mem,cmd -p "$pid"
  tail -30 artifacts/peak_shaving/20260712_expanded_response/submission_offgrid_interior_seed_detached.log
  find /tmp/peak_shaving_submission_offgrid -maxdepth 2 -type f -printf '%T@ %s %p\n' | sort -n | tail -20
  ```
- 输出：服务商 A 的 `1,031/1,031` 个全局守卫候选、共 `26,806` 个策略对已经评估；随后启动 16 个局部精化进程。主进程及工作进程均存活，退出文件尚未生成，新缓存 `firm_A.pkl` 为 140,574,752 bytes。
- 结果：审计仍在运行，当前没有 traceback 或异常退出证据；不得引用目录中修正前生成的 JSON 作为本轮结果。
- 决策：等待 A/B 两方审计全部结束后，先核对正式均衡 SHA-256、两方绝对/相对 regret、固定点收敛和来源哈希。两方 relative off-grid regret 均不高于 `0.5%` 才进入全剖面中间商与固定点审计，否则将偏差策略加入候选集并继续重求。
- 下一步：完成离网门禁后，依次运行 676 个活跃剖面的固定点多起点审计和中间商 differential-evolution 全局性审计。
- 状态：in_progress。

### 2026-07-12 16:45 - 终稿可信度、现实性与文字准确性专项复审

- 目标：按 SMPT 审稿标准重新检查 7 月 12 日英文稿的模型可信度、有限均衡证据、现实幅度和文字准确性；不把低 residual 或零 finite-grid regret 等同于外部有效性。
- 范围：只读检查 TeX/PDF、`artifacts/peak_shaving/20260712_final/`、时空博弈代码、Git 公开状态和 BurstGPT/vLLM 原始工件；本轮未重求完整 provider game，未修改主 TeX、核心代码或正式 JSON/CSV。
- 使用技能：`nature-reviewer`，按三位侧重点不同的审稿人和交叉综合输出；语言检查同时参考 `nature-polishing` 与 `humanizer` 的 claim 精度和常见 AI 痕迹规则。
- 外部核对：
  * BurstGPT 官方仓库确认 `BurstGPT_1.csv` 为 1,429.7k 行，并说明时间戳校准到未公开身份的 local time zone。
  * OpenAI Batch API 证明异步推理工作负载真实存在，但其 24 小时窗口不能校准本文 48% 可移动需求或 6 小时时移假设。
  * Faruqui--Sergici 的电力实验综述和 Allcott 的小时定价研究用于判断 13.03% 降峰的现实量级；结论是方向合理，但对普通 TOU 偏高且不能直接迁移为推理平台预测。
- 只读审计命令：
  ```bash
  git remote -v
  git rev-parse HEAD
  git ls-remote origin refs/heads/main
  jq '.dynamic.trace, .dynamic.expected_metrics, .dynamic.expected_profiles' \
    artifacts/peak_shaving/20260712_final/spatiotemporal_equilibrium.json
  jq '.rows' \
    artifacts/peak_shaving/20260712_final/spatiotemporal_sensitivity.json
  uv run --no-project --with numpy --with scipy python - <<'PY'
  # Fixed-profile provider-slope and expanded-intermediary response checks.
  PY
  uv run --no-project --with numpy --with scipy python - <<'PY'
  # Sixty-four random initialisations of the main routing--QoS fixed point.
  PY
  uv run --no-project python - <<'PY'
  # BurstGPT zero-response-row share and exclusion comparison.
  PY
  ```
- 关键发现：
  * **正文事实错误：** 第 4.2 节写中间商 `routing sensitivity=1.5`，但当前评价函数复现主剖面时返回 4.0；由工件中八时段 routing、wholesale 和 QoS 反推也全部为 4.0。
  * **中间商策略域截断：** 原 `beta` 候选为 `{1.5,4.0}` 且主结果命中上界。固定服务商主剖面并扩大中间商网格后，利润由 `157.170` 提高到 `169.909`，最佳点再次命中 `beta=6`；固定 retail `(0.95,0.3)` 时利润在 `beta=0--20` 持续上升。完整 provider game 必须在更宽 follower response 下重求。
  * **服务商边界风险：** 九个重求解中服务商 B 的 wholesale/direct slope 分别有 6/7 次命中 0.4 上界。本轮测试的 12 个 `0.45--0.8` slope 组合未发现 B 的正收益偏离，但不构成连续最佳响应证明。
  * **主固定点局部稳定：** 64 个随机 QoS/路由初值全部在 56 轮内收敛；最大 residual `9.97e-10`，终值坐标最大跨度 `2.05e-9`。这只支持主剖面的数值稳定，不是唯一性定理。
  * **行为现实性有限：** 总需求的 48% 可移动；统一/动态价格下分别有 31.28%/32.95% 的全部需求跨时段移动，相当于 65.16%/68.65% 的可移动质量。该设定适合离线或后台任务，不适合解释全部交互式请求。
  * **QoS 术语过强：** 测量横轴实际为 concurrency/224，而仿真横轴为 load/capacity；阈值 1.000 命中拟合约束下界，只有三个低于单位 QoS 的点。应称 shape anchor 或 normalized load index，不宜称真实 utilisation calibration。
  * **BurstGPT failure 行影响很小：** 25,443 条零 response-token 记录占 1.780%；排除后八时段平均 token share 最大变化仅 `2.19e-5`，峰值时段不变。
  * **公开声明不准确：** `origin/main` 与本地 HEAD 均为 `0941d97...`，但 7 月 12 日终稿、代码和工件尚未被 Git 跟踪或推送；正文当前不能声称 final files 已在公开仓库。
- 文字审查：英文整体直接、清楚且无明显 AI 排比；需修正 `route_beta`、公开仓库、`calibrate`、`normalised utilisation`、`system profit`、`game converged`、`best candidate` 和 `complete finite grids` 等事实或证据强度表述，并补充 logit 随机效用假设。
- 输出：`docs/reviews/smpt_final_credibility_reality_language_audit_2026-07-12.md`。
- 定向回归：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy --with scipy --with nashpy \
    --with matplotlib --with pillow pytest -q -s \
    tests/test_final_qos_calibration.py \
    tests/test_final_spatiotemporal_equilibrium.py \
    tests/test_final_offgrid_diagnostic.py \
    tests/test_final_spatiotemporal_sensitivity.py \
    tests/test_final_manuscript_20260712.py
  git diff --check
  ```
  结果：`15 passed in 4.11s`；`git diff --check` 无输出。测试证明现有工件与既有测试仍一致，但不会解除本轮发现的策略域截断和正文事实错误。
- 决策：本记录取代 13:40 条目中的 `verified_submission_candidate` 判断。当前状态为 **major_revision_required**；先扩大中间商响应并重求全部核心结果，再恢复终稿门禁。
- 下一步：修正工件序列化与正文自动一致性测试，扩大/连续优化中间商响应，重求主均衡和九个场景；随后增加 flexible share、capacity ratio、shift window 与日级负载敏感性。
- 状态：analysis_complete_major_revision_required。

### 2026-07-12 16:20 - 终稿图统一为克制 SCI 配色

- 目标：减少终稿图中过多的黄、青、绿、红类别色，使所有定量图和 Figure 1 使用统一、低饱和且色盲友好的期刊配色；不修改数据、线型、图注或论文结论。
- 图形契约：
  * 主结论仍由 aggregate peak、provider utilisation、QoS、regret 和 sensitivity 面板分别承担，不删除证据面板。
  * 定量图使用主蓝 `#3C5488`、同系次蓝 `#6F83B5`、低饱和砖红 `#A86464` 和中性灰 `#7A7A7A`；浅蓝 `#B8C4D9` 只作同系填充。
  * uniform 固定为灰、dynamic 固定为主蓝；Provider A 为主蓝、Provider B 为砖红。敏感性图仅使用 baseline 灰和其余场景主蓝，不再按参数类别使用彩虹式分组色。
  * Figure 1 的面板填充改为浅蓝灰与浅砖红，保留 Streamline 物联网图标原有局部色彩，避免损失设备辨识度。
- TDD 红灯：
  ```bash
  uv run --no-project --with pytest --with numpy --with matplotlib --with pillow \
    pytest -q -s tests/test_final_submission_figures.py \
    tests/test_final_framework_drawio.py
  ```
  结果：`2 failed, 6 passed`。失败分别来自数据图尚无统一 `SCI_PALETTE`，以及旧 Draw.io 面板仍含 `#667085` 等旧色，符合本轮预期。
- 生成命令：
  ```bash
  uv run --no-project --with numpy --with matplotlib --with pillow \
    python -m experiments.build_final_submission_figures
  uv run --no-project python \
    figure_sources/build_final_spatiotemporal_framework_drawio.py
  uv run --no-project python \
    /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figure_sources/spatiotemporal_pricing_framework_final_2026-07-12.drawio --strict
  ```
  * Draw.io 严格验证为 `0 error(s), 0 warning(s)`。
  * 使用 Draw.io 30.3.6 重新导出 3200 px PNG、内嵌图标 SVG 和 PDF；CLI 的 D-Bus 提示不影响导出，三个目标文件均成功生成。
  * Draw.io PDF 默认为 1.7；为兼容当前 XeLaTeX/xdvipdfmx，使用 Ghostscript `/prepress` 设置转换为 PDF 1.5。
- 定向验证：同一测试命令重跑后为 `8 passed in 1.60s`。新增断言禁止旧亮色 `#E64B35/#00A087/#F2B701/#4DBBD5/#91D1C2` 回流，并约束 sensitivity 只含主蓝和灰。
- 视觉检查：逐一查看五张定量图和 Figure 1 的原始分辨率 PNG，并再次检查 PDF 第 4、8、9、10、11 页。未发现标签遮挡、颜色误映射、裁切、低对比文字或图注错位。
- 编译命令：
  ```bash
  latexmk -g -norc -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-12.tex
  ```
  结果：15 页 PDF 成功生成；日志无 LaTeX Error、undefined citation/reference、overfull、underfull 或其他 warning。
- 影响范围：仅修改终稿绘图脚本、Figure 1 生成器、图形产物、两组图形测试和 README；实验 JSON/CSV、表格数字、正文技术含义及参考文献均未改变。
- 状态：verified。

### 2026-07-12 13:40 - 路线 C：守恒需求博弈重算与英文终稿

- 目标：将已经验证的 origin--destination 守恒需求接入服务商、中间商、路由和 QoS 联合博弈，重新生成均衡、敏感性、图表和五章英文终稿。
- 原则：旧 `2026-07-11` TeX 和旧 mixed-oracle 数字仅作为历史版本；新稿不得引用 P0 修复前的支付矩阵或把 fixed-policy 机制实验称为 Nash equilibrium。
- 实施顺序：先以失败测试定义时空市场状态和利润行为，再实现联合求解与有限策略支付评估；随后运行标准双矩阵求解、完整候选偏离检查和参数重求解，最后重写论文并编译审计。
- 主要输入：BurstGPT 8 时段 token profile、现有 vLLM TTFT-SLA 测量点、225 点服务商策略候选集，以及路线 C 的合成对照负载。
- 预期输出：`artifacts/peak_shaving/20260712_final/`、终稿数据图、英文终稿 TeX/PDF、claim--evidence 审计和投稿前内部审稿报告。
- TDD 进展：新增时空联合市场测试，红灯为 4 个缺失模块失败；实现后 `4 passed`。新增有限双矩阵测试，修复 Nashpy 在退化 `1×1` 博弈上不必要的 Lemke--Howson 枚举后，与市场测试合计 `7 passed`。
- QoS 同函数校准：使用两个 Qwen2.5/vLLM profile 的 10 个 TTFT-SLA 点拟合主仿真的阈值指数函数。无约束最小二乘会给出 `threshold=0.600`，与两个 profile 在 `u<=1` 时 SLA 全为 1 的事实冲突，因此加入 `threshold>=1` 的测量约束。最终 pooled fit 为 `threshold=1.0000`、`strength=0.5747`、RMSE `0.0561`；留一模型外测 RMSE 为 `0.0454/0.1046`。
- 已生成：`artifacts/peak_shaving/20260712_final/qos_calibration.json` 与 `qos_calibration_points.csv`。
- 最终有限博弈：
  ```bash
  uv run --no-project --with numpy --with scipy --with nashpy \
    python -m experiments.run_final_spatiotemporal_equilibrium
  ```
  * uniform game 为完整 9 点零斜率限制，dynamic game 为完整 225 点线性价格形状。
  * uniform active profile 为双方 `(0.575,0,0.6,0)`；dynamic active profile 为服务商 A `(0.575,0.2,0.6,0.2)`、服务商 B `(0.575,0.4,0.6,0.4)`。
  * dynamic double oracle 评估 2,445 个去重策略对，full-grid regret 由 `44.284 -> 20.561 -> 0`；uniform 在第 2 轮达到 0。
  * dynamic/uniform 最大联合 routing--QoS residual 分别为 `6.63e-10/6.56e-10`，总需求均为 1100。
  * dynamic 相对 uniform：aggregate peak `-13.03%`，maximum provider utilisation `-17.08%`，minimum QoS `0.888 -> 0.976`，system profit `+9.25%`。
- 网格外诊断：
  ```bash
  uv run --no-project --with numpy --with scipy \
    python -m experiments.run_spatiotemporal_offgrid_diagnostic
  ```
  * seed 为 20260712；每位服务商 512 个 Latin-hypercube 候选，连同 incumbent 各评估 513 个候选。
  * 两位服务商的 sampled off-grid regret 均为 0；全部 joint fixed point 收敛，最大 residual 小于 `1e-9`。
  * 本轮耗时约 `160.05s`。该结果只作为抽样诊断，不写成 continuous-space Nash proof。
- 九组完整参数重求解：
  ```bash
  uv run --no-project --with numpy --with scipy --with nashpy \
    python -m experiments.run_final_spatiotemporal_sensitivity
  ```
  * capacity `0.85/1.15`、price sensitivity `0.8/1.2`、migration cost `0.7/1.3` 和 QoS threshold `-0.05/+0.05` 均重新求 uniform/dynamic equilibrium。
  * 九组的 uniform/dynamic full-grid regret 全部为 0，最大 residual 为 `9.87e-10`，总需求全部为 1100。
  * aggregate peak 变化范围为 `-14.31%` 至 `-4.23%`；maximum utilisation 为 `-19.27%` 至 `-10.49%`；minimum QoS 为 `+0.0540` 至 `+0.0958`。
  * system profit 为 `-37.43%` 至 `+9.41%`，因此终稿不声称稳定利润提升。
  * 完整运行耗时约 `1390.38s`。
- 固定政策机制分解：
  ```bash
  uv run --no-project --with numpy --with scipy \
    python -m experiments.run_final_mechanism_decomposition
  ```
  * dynamic temporal-only 相对 neither：aggregate peak `-42.015`、maximum utilisation `-0.2254`、minimum QoS `+0.0698`。
  * dynamic spatial-only：aggregate peak 严格为 0、maximum utilisation `-0.1017`、minimum QoS `+0.0377`。
  * combined 结果不等于两个单独效果相加，因此正文将其解释为带 QoS 反馈的固定政策分解，不写成可加因果效应。
- 终稿图表：
  ```bash
  uv run --no-project --with numpy --with matplotlib --with pillow \
    python -m experiments.build_final_submission_figures
  ```
  * 输出 `figures/peak_shaving_final_20260712/` 下五组数据图的 PDF/PNG，以及 editable Draw.io framework 的 PDF/SVG/PNG。
  * 所有数据图使用 Times New Roman、同一 Nature 风格色板、面板标记置于图下；逐图目视检查未发现标签遮挡、曲线遮挡或裁切。
  * Figure 1 的源文件为 `figure_sources/spatiotemporal_pricing_framework_final_2026-07-12.drawio`，使用本地嵌入的 Streamline CC BY 4.0 图标。Draw.io 严格检查为 0 error、0 warning。
- 英文终稿：
  * 新稿为 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-12.tex`，只保留 Introduction、Related research、Methodology、Experimental results、Conclusion and outlook 五个编号章节。
  * 公式补齐 channel price 映射、OD 守恒、routing、QoS、联合 residual、线性价格、利润、候选集、intermediary response、bimatrix payoff 和两方 regret。
  * PDF 内给出 BurstGPT 八时段向量、vLLM 并发档位、每档请求数、warm-up、固定 prompt、输出长度、seed、驱动和运行时版本。
  * 摘要为 227 词，关键词 7 个；新增 `peak_shaving_dynamic_pricing_SMPT_highlights_2026-07-12.txt`，5 条均为 60--77 字符。
  * claim--evidence 审计和三审稿人内部报告分别为 `docs/reviews/smpt_final_claim_evidence_audit_2026-07-12.md`、`docs/reviews/smpt_final_internal_review_2026-07-12.md`。
- SMPT 官方格式核对：2026-07-12 查阅 <https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors>。当前摘要、关键词、Highlights、可编辑公式/表格和 LaTeX 源文件符合入口要求；该刊为 single-anonymized review，真实作者、单位、通讯信息仍须作者填写。
- 失败与修复记录：
  * Nashpy 在退化 `1x1` 支持上不必要地进入 Lemke--Howson；改为 support enumeration 无有效结果时才 fallback。
  * 第一次直接运行 figure builder 因包导入方式报告 `ModuleNotFoundError`；改用 `python -m experiments.build_final_submission_figures`。
  * 一次英式拼写修改引入绘图缩进错误；定向测试前定位并修复，全部图重新生成。
  * framework 初始 PDF 1.7 使当前 `xdvipdfmx` segmentation fault；用 Ghostscript 转为 PDF 1.5 后稳定编译。
  * pytest 默认 fd capture 受当前临时目录影响，在退出时报告 `FileNotFoundError` 且未运行测试；关闭 capture 的 `-s` 方式稳定执行。
  * Ruff 唯一报告为 Draw.io 入口在 `sys.path` 设置后的 `E402`；在该局部导入增加说明性 `noqa` 后通过。
  * 行内 BurstGPT 八维向量触发一条 underfull box；改为独立公式后编译日志无 warning。
- 最终回归：
  ```bash
  uv run --no-project --with pytest --with numpy --with scipy \
    --with matplotlib --with nashpy --with pillow pytest -q -s \
    tests/test_peak_shaving_market.py \
    tests/test_peak_shaving_equilibrium.py \
    tests/test_peak_shaving_measurement_anchor.py \
    tests/test_peak_shaving_smpt_experiments.py \
    tests/test_peak_shaving_submission_tools.py \
    tests/test_peak_shaving_consistency.py \
    tests/test_spatiotemporal_mechanism.py \
    tests/test_spatiotemporal_decomposition_experiment.py \
    tests/test_burstgpt_load_anchor.py \
    tests/test_spatiotemporal_game.py \
    tests/test_finite_game.py \
    tests/test_final_qos_calibration.py \
    tests/test_final_spatiotemporal_equilibrium.py \
    tests/test_final_offgrid_diagnostic.py \
    tests/test_final_spatiotemporal_sensitivity.py \
    tests/test_final_mechanism_decomposition.py \
    tests/test_final_submission_figures.py \
    tests/test_final_framework_drawio.py \
    tests/test_final_manuscript_20260712.py
  ```
  结果：`74 passed in 227.61s`。修改 Python 文件的 Ruff 结果为 `All checks passed!`。
- 最终编译：
  ```bash
  latexmk -g -norc -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-12.tex
  ```
  * 输出 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-12.pdf`，15 页、A4、PDF 1.5、389686 bytes。
  * 日志无 LaTeX Error、undefined citation/reference、overfull、underfull 或其他 warning；所有 PDF 字体嵌入。
  * 逐页视觉抽查覆盖标题页、框架图、公式、参数表和六张结果图，未发现遮挡、裁切或孤立图题。
  * SCI 配色更新后的最终 TeX/PDF SHA-256 分别为 `af2f14cb58b9209c8a2253f91d44140e2b3683b03bb0502087ece93891ed28cb` / `0e125d5e8605aead7b5d703cdea248db0c3149a3858426f9ebdee1dd117cf267`。
- 投稿边界：实验与正文一致性已达到 submission-candidate 状态；经济行为参数仍为 synthetic，单卡 QoS 和平均日负载限制已经写入正文。实际上传前还需作者补齐姓名、单位、通讯作者、资金、利益冲突、CRediT、致谢，并建议生成干净 commit 与 Zenodo/OSF DOI。
- 当前状态：verified_submission_candidate。

### 2026-07-12 11:32 - 路线 C：计算修复与机制分解原型

- 目标：按已确认的路线 C，先修复影响支付矩阵和 V&V 的计算问题，再建立可分别启用时间迁移与跨服务商/渠道选择的最小机制分解原型。
- 背景：深层复核表明当前 QoS 改善来自 provider-level capacity balancing，而不是 aggregate temporal peak shaving；现有摘要和百分比在修复、重求解前均不作为最终结论。
- 计划：
  * 用失败测试覆盖批发内部转移守恒、QoS-adjusted average paid price 和联合 routing--QoS 固定点。
  * 最小修改核心支付与求解逻辑，并运行现有回归测试。
  * 用失败测试定义显式 uniform/peak-only/off-peak-only/symmetric TOU 基函数。
  * 建立守恒的 origin--destination 时间迁移函数和 temporal/spatial 四格机制指标原型。
  * 只运行受控原型；本阶段不覆盖旧 JSON/CSV、图表或 TeX，也不继续语言润色。
- 验收：内部批发转移严格抵消；最终 joint residual 达到报告容差；论文指标只有一个实现；时间流量逐 origin 守恒；四种价格基函数语义由测试验证；新工件包含代码/配置来源信息。
- 环境：当前位于 WSL 原生仓库，使用 `/root/.local/bin/uv` 和 WSL Python。工作区已有用户的论文、图表和审稿记录改动，核心 `pricing_sim` 文件当前无未提交差异；不建立会遗漏这些文件的独立 worktree。
- 基线测试：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy --with scipy --with matplotlib \
    pytest -q -s tests/test_peak_shaving_market.py \
    tests/test_peak_shaving_smpt_experiments.py \
    tests/test_peak_shaving_submission_tools.py
  ```
  结果：`23 passed in 1.35s`。
- P0 红灯测试：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy --with scipy --with matplotlib \
    pytest -q -s tests/test_peak_shaving_consistency.py
  ```
  结果：3 个预期失败。内部转移不守恒使零成本场景的系统利润比外部收入少 `0.679836`；当前平均支付价格与 QoS-adjusted 权重结果相差 `0.0005743`；joint solver 没有返回 `joint_residual`。
- P0 修复：
  * 新增唯一的 per-provider wholesale settlement 计算，服务商批发收入和中间商批发成本读取同一结算数组。
  * `average_paid_price` 统一按 `demand × QoS` 的完成服务量加权。
  * joint solver 同时迭代 QoS 和 routing，不再结束后固定 routing 重算 QoS；结果返回 joint/qos/routing residual、迭代数和收敛标志，未收敛候选不会进入中间商最优响应。
- P0 绿灯验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy --with scipy --with matplotlib \
    pytest -q -s tests/test_peak_shaving_market.py \
    tests/test_peak_shaving_smpt_experiments.py \
    tests/test_peak_shaving_submission_tools.py \
    tests/test_peak_shaving_consistency.py
  ```
  结果：`26 passed in 0.56s`。
- 机制原型红灯与绿灯：
  * 价格基函数、origin--destination 守恒流、nested 渠道分配、QoS 固定点和 12 单元实验入口均先得到预期失败，再逐项实现。
  * 新增定向回归后，6 个相关测试文件合计 `31 passed in 0.66s`。
- 受控实验命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with numpy --with scipy \
    python -m experiments.run_spatiotemporal_mechanism_decomposition \
    --load-source synthetic
  ```
- 受控实验输出：
  * `artifacts/peak_shaving/20260712_route_c/spatiotemporal_mechanism_decomposition.json`
  * `artifacts/peak_shaving/20260712_route_c/spatiotemporal_mechanism_decomposition.csv`
  * 共 3 种价格结构 × 4 种机制开关 = 12 行，全部 fixed-point converged；总原生需求在所有单元均为 `1100`。
- 初步结果：
  * `symmetric_tou + temporal_only` 相对同政策 neither：aggregate peak `-28.473`，maximum provider utilization `-0.0983`，minimum QoS `+0.1015`。
  * `asymmetric_capacity_balance + spatial_only`：aggregate peak 变化约 `0`，maximum provider utilization `-0.2021`，minimum QoS `+0.1075`。
  * `asymmetric_capacity_balance + combined`：aggregate peak `+2.6023`，maximum provider utilization `-0.1970`，minimum QoS `+0.1075`。
  * 原型在固定总需求下复现了两种不同机制：对称 TOU 可产生真实时序削峰；异质服务商的高峰折价/加价组合可在不降低总峰值时缓解 provider hotspot。该结果支持路线 C 的研究问题，但当前仍是 synthetic controlled prototype，不是均衡、真实轨迹或投稿结论。
- BurstGPT 锚点：
  * 固定官方提交 `d895a53bb7b8ec137d0d2fe203b335835a78c10a`，原始 CSV 为 `50,853,373` bytes，SHA-256 为 `46fc9480ef0b748ecb2b51d512ff08c196b031782cbe6f78e28044d768e86d5a`。
  * 首次 Python 流式下载在 `13,631,488` bytes 停止增长，进程持续等待 socket；本轮主动中断，没有把部分文件当作输入。
  * 新增 partial-cache 红灯测试后，下载器改为断点续传、低速退出/重试和精确 Content-Length 门禁；从已有位置续传成功。
  * 读取 `1,429,737` 行，跳过 0 行；去除首尾日后使用 59 个完整日。request/token share 之和分别为 `1.0/1.0000000000000002`，load-shape 均值为 `-1.11e-16`、最大绝对值为 `1.0`。
  * 派生文件保存在 `data/processed/burstgpt_d895a53b_8period/`；原始 50.85 MB CSV 只缓存于 `/tmp`。来源、许可、处理步骤和时区边界写入该目录 README。
- BurstGPT 四格实验：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with numpy --with scipy \
    python -m experiments.run_spatiotemporal_mechanism_decomposition \
    --load-source burstgpt
  ```
  * 12 个单元全部收敛，总需求均为 `1100`。
  * `symmetric_tou + temporal_only`：aggregate peak `-43.253`（`-18.13%`），maximum provider utilization `-0.1493`，minimum QoS `+0.5159`。
  * `asymmetric_capacity_balance + spatial_only`：aggregate peak 不变，maximum provider utilization `-0.2314`（`-28.09%`），minimum QoS `+0.5274`。
  * `asymmetric_capacity_balance + combined`：aggregate peak `-4.676`（`-1.96%`），maximum provider utilization `-0.2211`，minimum QoS `+0.5270`。
- 最终工件校验：
  * synthetic JSON/CSV：`ce939f6f8ca8604dcf2cc4cf869e3aaf42645f2e065b4b9c3a6a516e4798169b` / `9e28e3aa88bb8335d177f9d3f937b144c6a8d9fe296f45050b4d113fcfb5b8c5`。
  * BurstGPT JSON/CSV：`f6b85c99ce2610da515634a1274a4e05a543ec64c860df4746bb7c523c261320` / `0b648ff5c75e1aa60a608f281ded701dd6f592c3732af8c713e279ad2831c5c1`。
  * manifest 记录 commit、dirty status、完整行为参数、机制开关、实际命令和全部输入源 SHA-256；BurstGPT 工件同时包含聚合脚本指纹。
  * 核验命令使用 `jq -e` 检查每个 JSON 的 12 个实验单元、收敛标志和 `|total_demand-1100|<1e-9`，再用 `sha256sum` 核对两个 JSON、两个 CSV 和两个 BurstGPT 派生文件。结果：所有条件成立；实际需求范围为 synthetic `[1100,1100]`、BurstGPT `[1099.9999999999998,1100]`。
- 最终代码验证：
  * Ruff 对本轮全部修改 Python 文件输出 `All checks passed`；`compileall` 无输出且退出码为 0。
  * 包含两个旧慢速 `solve_firm_nash` 测试和 joint residual 工件记录测试的最终完整相关回归为 `44 passed in 224.49s`。
  * 旧 cross-seed 测试单独为 `1 passed in 137.73s`，但当前 seed 参数不参与确定性网格搜索，因此该结果只表示重复执行一致，不能作为随机稳健性证据。
- 审计输出：`docs/reviews/route_c_evidence_update_2026-07-12.md`。
- 论文状态：旧 TeX 和旧 mixed/参数工件未修改，且因 P0 改变支付矩阵而不再代表当前代码。路线 C 的机制与真实负载原型已验证；新主稿仍阻塞于 conserved demand 接入服务商博弈、重新求均衡和 QoS 直接校准。
- 状态：verified_prototype / equilibrium_rerun_pending。

### 2026-07-12 00:50 - 峰谷定价主机制深层复核

- 目标：在既有 Q1 就绪度审计基础上，重新计算主 mixed profile 的时间迁移、全市场峰值、服务商负载和有限博弈均衡，判断论文的“削峰”叙事是否由实验支持。
- 输入：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex`、统一定价工件、225 点 mixed-oracle 工件，以及当前市场、需求和求解器实现。
- 方法：逐一重算 mixed 支持集的 25 个策略组合；分别汇总 `maximum provider utilization` 和 `aggregate peak load`；计算刚性/弹性需求质心、渠道需求和服务商负载；使用 Nashpy/Lemke--Howson 独立求解 5×5 受限双矩阵博弈，并对完整 225 点候选集做偏离扫描。
- 核心发现：
  * 当前 mixed profile 将最低服务商 QoS 从 `0.7565` 提高到 `0.9699`，并将最高服务商利用率从 `0.7822` 降到约 `0.7030`。
  * 全市场峰值请求量却从 `222.11` 增至 `262.43`，增加 `18.15%`；刚性和弹性需求质心只分别移动 `+0.00216/+0.00215` 个时段。
  * mixed 支持组合中，QoS 优于统一定价的概率质量为 1.0，全市场峰值低于统一定价的概率质量为 0。
  * 第 6 时段大服务商 A 负载增加 `38.87%`，小服务商 B 负载下降 `10.14%`；A 直连需求增加 `49.65%`。当前 QoS 改善主要来自跨服务商/直连渠道容量均衡，不是时间削峰。
  * 主稿中的 `peak utilization` 是最拥塞服务商--时段利用率，不等于全市场时序峰值；摘要、题名和结论当前混用了两者。
- 模型复核：
  * 当前 channel×period logit 没有原生时段到目标时段的守恒流量，不能直接识别需求迁移；时间偏好还同时进入 period utility、native distribution 和 rigid baseline。
  * `discount_only_params()` 保留负 slope，实际对应高峰折扣/低谷加价；`peak_only_params()` 的正 slope 同时包含高峰加价和低谷折扣。现有单边价格基线名称与实现不符。
  * TeX 称 `load_shape_hat` 来自 rigid-demand baseline，代码实际从 `time_preference` 生成。
  * 旧 cross-seed 工件报告相对标准差 `4.31e-4`；当前网格求解器忽略 seed/n_starts，seed 0/1/2 得到完全相同的系统利润 `1139.4043677649`。工件缺少 commit/config/code hash，存在版本漂移。
- 独立有限博弈求解：
  * Nashpy support enumeration 识别到退化并返回 0 个解；对支付做正仿射缩放后，Lemke--Howson 得到一个 2×2 受限混合解。
  * 对完整 225 点网格评估 896 个去重策略对，耗时 `229.1 s`；row/column regret 分别为 `1.84e-10` 和 `3.67e-9`。
  * 独立解的最低 QoS、最高服务商利用率、系统利润分别为 `0.9693`、`0.7038`、`1732.58`；全市场峰值仍增加 `18.04%`，弹性需求质心只移动 `+0.0011`。
  * 结论：当前有限博弈的求解误差可以明显降低，但更强的均衡证据不会自动证明时间削峰；修复支付和联合固定点后仍须全量重跑。
- 外部门槛：SMPT 官网强调模型开发、计算实现、V&V 和真实数据透明度；BurstGPT 可提供真实 Azure OpenAI 到达轨迹；AAAI 2026 PriLLM 已提供 data-calibrated Stackelberg routing 定价基线，当前稿的合成校准和比较实验仍需加强。
- 决策建议：不再继续整篇语言润色。优先选择“时序迁移与跨服务商容量均衡分解”路线：真实轨迹原生到达、守恒时间迁移、渠道选择、路由和退出分别建模，并用 temporal-only/spatial-only/combined 因子实验识别机制。
- 输出：`docs/reviews/peak_shaving_mechanism_reaudit_2026-07-12.md`。
- 影响：本轮没有修改核心代码、JSON/CSV 工件、论文图或 TeX；Nashpy 仅通过 `uv run --with nashpy` 临时加载，没有修改项目依赖文件。
- 状态：analysis_complete；等待用户确认重构路线后再实施。

### 2026-07-12 00:15 - SMPT/SCI Q1 投稿就绪度复审

- 目标：按 SCI Q1 仿真建模论文标准复审当前英文稿的实验、理论计算、语言和投稿就绪度，不以“可以上传投稿系统”代替科学质量判断。
- 输入：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex`、当前 PDF、峰谷定价核心代码、混合 oracle/参数扫描/vLLM 工件、既有 SMPT 审稿记录。
- 期刊基准：SMPT 官网要求论文对建模与仿真作出显著贡献，并明确覆盖实验设计、敏感性分析、比较程序和 verification/validation；本轮据此提高外部有效性与数值校核门槛。
- 当前判断：major revision；语言接近投稿稿，但实验和计算一致性尚未达到 Q1 终稿门槛。
- 新发现的阻塞问题：
  * 服务商批发收入按 `sum(r_m w_m q_m)` 计算，中间商批发成本按 `sum(r_m w_m) sum(r_m q_m)` 计算；两者一般不相等，内部转移支付不守恒，并进入中间商最优响应。
  * 论文定义的平均支付价格按 QoS 调整后服务量加权，SMPT 工件代码按原始需求量加权，公式与图表生成口径不一致。
  * 联合路由--QoS 求解器内部计算联合残差，但不返回该残差或联合收敛标志；最终又在固定路由下重算 QoS。当前 V&V 表只证明固定路由 QoS 残差，不足以证明最终状态满足联合固定点。
- 证据边界：当前混合 oracle 在 225 点有限网格上达到最大 regret `0.203`，但未做网格外连续/随机最佳响应搜索；9 场景和 25 点扫描为固定策略，5 个重求解场景仅使用 5 个候选和 4 轮响应。
- 外部有效性：经济参数全部为 synthetic calibration；QoS 锚点只有单张 RTX 4090、两个小模型、短输出和少量并发点；同质容量消融中 QoS 优势反转。
- 定量复核：在当前混合支持状态上，批发内部转移差额的期望约为 `-0.0101`，约占已报告系统利润 `-0.00058%`；当前状态下数值很小，但修正会改变中间商目标函数，不能据此免除全量重跑。
- 测试命令：
  ```bash
  uv run --no-project --with pytest --with numpy --with scipy --with matplotlib \
    pytest -q tests/test_peak_shaving_market.py \
    tests/test_peak_shaving_submission_tools.py \
    tests/test_peak_shaving_smpt_experiments.py
  ```
- 首次结果：pytest 输出捕获临时文件在退出时丢失，`FileNotFoundError`，未执行测试。
- 修复后命令：
  ```bash
  uv run --no-project --with pytest --with numpy --with scipy --with matplotlib \
    pytest -q -s tests/test_peak_shaving_market.py \
    tests/test_peak_shaving_submission_tools.py \
    tests/test_peak_shaving_smpt_experiments.py
  ```
- 修复后结果：`23 passed in 1.18s`。现有测试未覆盖内部转移守恒、公式/工件指标一致性或联合固定点残差，因此通过结果不能解除上述阻塞。
- 输出：`docs/reviews/smpt_q1_readiness_audit_2026-07-12.md`。
- 报告检查：包含总体结论、3 份侧重点不同的内部审稿意见、交叉综合、P0--P2 修改门槛和复核命令；`git diff --check` 无空白错误。
- 状态：verified。

### 2026-07-11 23:34 - 扩展英文稿相关工作与电力定价定位

- 目标：扩展 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex` 第 2 节，评述既有研究，重点说明电力动态定价如何构成本研究的方法基础，以及该基础不能直接覆盖推理服务市场的原因。
- 输入：当前英文终稿、`verified_refs.bib` 中已核验的电力定价与推理服务文献，以及出版社页面可核对的摘要和研究边界。
- 文献核对：使用 Springer 的 Schweppe spot-pricing 图书页和 Faruqui--Sergici 实验综述页，以及 ScienceDirect 的 Allcott、Yu--Hong、Srinivasan 等论文页面核对研究对象、实验结论和适用边界。未增加新的参考文献条目。
- 修改：按推理服务系统研究、电力定价经济与实证基础、电力定价博弈模型、向推理服务迁移时的缺口四部分组织；相关工作由约 384 词扩展至 1157 词。
- 评述重点：
  * 区分系统内部调度研究与市场层价格、路由、切换和退出问题。
  * 用电力定价研究说明时变价格、用户异质性和峰值响应的理论与实证基础，并引用已有 15 项实验综述中的峰值削减区间。
  * 评述 utility、TOU game 和 Stackelberg 模型的贡献，同时指出单一 utility/retailer、物理供需平衡和跨市场弹性校准不能直接覆盖推理服务。
  * 明确本研究的价格函数仍为线性时序形状；有限网格离散的是函数参数，regret 只约束有限候选博弈。
  * 新增 `Table 1`，比较电力定价、经验需求响应、博弈模型、拥塞/平台研究与本文模型之间的继承关系和缺口。
- 语言要求：使用直接、常见的学术英语句式；每段只承担一个论点；避免文献罗列、夸大创新和生僻术语。
- 编译命令：
  ```bash
  latexmk -g -norc -xelatex -interaction=nonstopmode -halt-on-error -synctex=1 \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex
  ```
- 验证结果：强制全量编译成功，PDF 为 25 页、506006 bytes、A4、PDF 1.5；仍为五个一级章节。日志无 LaTeX error、未定义控制序列、未定义引用/文献、multiply-defined 标签或 overfull box；既有窄表保留 underfull box 提示。
- 页面检查：抽检 PDF 第 2--4 页；四个相关工作子节、经验百分比、线性价格与有限网格说明、文献定位表及其正文引用均可见。表格采用左对齐段落列，未发生遮挡、越界或拆分。
- 影响：未修改公式、实验数据、求解器、图、参考文献库或论文结论；PDF 比上一版增加 1 页。
- 状态：verified。

### 2026-07-11 23:13 - 英文期刊匹配与 SMPT 投稿结构适配

- 目标：比较英文期刊匹配度，并将 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex` 进一步适配目标期刊的结构与投稿规范。
- 候选：Simulation Modelling Practice and Theory（SMPT）、Future Generation Computer Systems、Electronic Commerce Research and Applications、Computers & Industrial Engineering。
- 决策：继续以 SMPT 为首选。当前稿件的核心证据是仿真模型、固定点、有限网格 regret、验证/校核和证据边界；这与 SMPT 对计算机系统、云/边缘环境、智能体、仿真实验设计及 verification/validation 的 scope 最一致。其他候选更依赖系统原型、真实工作负载、商业实证或更强的工业优化新方法。
- 官方依据：
  * 期刊主页与 scope：`https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory`。
  * 作者指南：`https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors`。
  * 当前官网指标：CiteScore 9.8，Impact Factor 4.6；期刊采用 single-anonymized review。
  * 摘要不超过 250 词；关键词 1--7 个；正文采用编号章节；highlights 为 3--5 条、每条不超过 85 个字符；数据可用性声明为必需项。
- 近期样本：检查了 2025--2026 年 SMPT 中的 MASS-GT、serverless scaling、sparse-data supply-chain simulation、GIS-integrated agent-based simulation、edge--fog--cloud optimization 和 IoT task-offloading 论文页面。高频结构为问题与缺口、模型/框架、实验设计、量化结果、验证边界和结论/局限。
- 模板检查：`kpsewhich elsarticle.cls` 和 `kpsewhich elsarticle-num.bst` 均无输出，本机 TeX Live 未安装 Elsevier 模板。未执行全局安装；保留可编译的通用单栏 `article` 类，并按 SMPT 指南实施结构、摘要、关键词、编号引用和声明要求。
- 修改：
  * 标题改为 `Simulation-based analysis of time-of-use pricing for fixed-capacity inference services`。
  * 摘要重写为目的--模型--验证--量化结果--证据边界顺序，最终为 239 词；保留全部关键数值。
  * 保持 Introduction、Related work、Methodology、Experimental results、Conclusion and outlook 五个主章节，将 24 个内联小标题改为编号子节或子子节。
  * 统一为美式英语，保持图中 `utilization` 等术语一致。
  * 数据声明改为简洁 GitHub 指向；生成式 AI 声明按 Elsevier 推荐结构明确 OpenAI Codex 的用途、作者复核和责任。
  * 新增 `peak_shaving_dynamic_pricing_SMPT_highlights_2026-07-11.txt`：5 条 highlights，每条 63--76 个字符，均低于 85 字符上限。
- 编译命令：
  ```bash
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/plugins/cache/openai-bundled/latex/0.2.4/scripts/compile_latex.py \
    /root/paper_code/0427_tokenrl/paper_token_cross_survey/peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex \
    --compiler texlive --engine xelatex --json

  latexmk -g -norc -xelatex -interaction=nonstopmode -halt-on-error -synctex=1 \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex
  ```
- 结果：2026-07-11 23:26 强制全量编译成功，PDF 为 24 页、499874 bytes、A4、PDF 1.5。日志无 LaTeX error、未定义控制序列、未定义引用/文献、multiply-defined 标签或 overfull box；仅保留表格中的 underfull box 警告。
- 页面检查：首页标题、摘要、关键词和引言布局正常；第二页 Related work 的编号层级清晰。PDF 文本包含五个主章节、数据声明和生成式 AI 声明，不含已移出的逐项脚本清单。
- 结构检查：`abstract_words=239`、`main_sections=5`、`inline_paragraphs=0`、`highlights=5`；五条 highlights 为 61--74 个字符，均低于 85 字符上限。
- 未解决：`Anonymous Author` 必须在投稿前替换为真实作者、单位和通讯作者信息；SMPT 为 single-anonymized review。GitHub release 尚无持久 DOI，正式投稿前宜归档至 Zenodo 或同类数据仓库。
- 状态：verified。

### 2026-07-11 23:05 - 精简论文可复现性声明并新建当日英文稿

- 目标：新建 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex`，将正文中的模块、实验脚本、工件目录和补充材料路径清单移出论文，改为简洁的 GitHub 数据与代码可用性声明。
- 背景：完整的代码入口、实验记录和工件映射已在本 README 中维护；在论文正文重复逐文件清单影响结论部分的阅读节奏。
- 输入：`peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`。
- 输出：当日英文 TeX 及编译 PDF；旧版 TeX 和 PDF 保持不变。
- 验证：检查被删除路径不再进入新 TeX/PDF，GitHub 仓库与 release 链接仍存在，并运行 XeLaTeX 完整编译和日志扫描。
- 修改：删除正文中的 3 个核心模块、9 个实验入口、诊断脚本、工件子目录、补充材料和 Figure 1 源文件路径；以三句 `Data and code availability` 声明替代，并保留 GitHub 仓库、版本化 release 和 README 复现入口。
- 编译命令：
  ```bash
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/plugins/cache/openai-bundled/latex/0.2.4/scripts/compile_latex.py \
    /root/paper_code/0427_tokenrl/paper_token_cross_survey/peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex \
    --compiler texlive --engine xelatex --json
  ```
- 结果：编译成功，新 PDF 为 23 页、497374 bytes；日志无 LaTeX error、未定义引用/文献或 overfull box。PDF 文本包含 GitHub 数据声明，不再包含逐项脚本和工件路径。
- 状态：verified。

### 2026-07-11 21:35 - 最终框架图插入中英文论文

- 目标：将已验证的 Draw.io 框架图作为 Figure 1 插入英文 SMPT 投稿稿和中文审阅稿。
- 输入：
  * `figures/peak_shaving_framework_2026-07-11.pdf`：论文引用的 PDF 1.3 矢量兼容版本。
  * `figure_sources/peak_shaving_framework_2026-07-11.drawio`：可编辑源文件。
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`。
  * `peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex`。
- 最终修改：
  * 中英文 TeX 均将旧的 `framework_imagegen_final_2026-07-10.png` 替换为 `peak_shaving_framework_2026-07-11.pdf`。
  * 更新中英文图注，使两层结构、实线/虚线语义和有限网格证据边界与图中内容一致。
  * 在图注中加入 Streamline Ultimate Color 图标的 CC BY 4.0 署名。
  * 更新生成式 AI 与 AI 辅助技术声明，删除“当前 Figure 1 仍需替换”的过时表述，并如实说明可编辑矢量图及 AI 辅助检查边界。
  * 在工件说明中补充 Draw.io 源文件、生成器、PDF 1.3 兼容导出和图标许可位置。
- PDF 兼容性诊断：
  * Draw.io 原始 PDF 为 1.7；TeX Live 2022 的 `xdvipdfmx` 目标版本为 PDF 1.5，首次英文编译因此发生 segmentation fault，`latexmk` 退出码为 12。
  * 使用 Ghostscript 生成 PDF 1.3 兼容版本，保留矢量文字、线条和 Times New Roman 嵌入字体：
  ```bash
  gs -q -dNOPAUSE -dBATCH -dSAFER -sDEVICE=pdfwrite \
    -dCompatibilityLevel=1.3 -dPDFSETTINGS=/prepress \
    -dEmbedAllFonts=true -dSubsetFonts=true \
    -sOutputFile=/tmp/peak_shaving_framework_pdf13.pdf \
    figures/peak_shaving_framework_2026-07-11.pdf
  ```
  * 调试期间测试了 PDF、PNG 和 4:4:4 JPEG 三种嵌入路径。预览工具曾在 1075×1521 图像上显示黑块，但像素审计表明实际 Poppler 输出正常；缩放副本与 Ghostscript 渲染也均正常。因此，终稿恢复使用 PDF 1.3 矢量版本，PNG、SVG 和 JPEG 作为备用导出保留。
- 集成测试：
  * 新增 `tests/test_peak_shaving_framework_tex_integration.py`，检查中英文 Figure 1 引用、图注语义、图标许可、源文件位置、AI 声明和 PDF 1.3 版本门禁。
  * 红灯阶段在 TeX 尚未切换到最终图时得到 `1 failed, 3 passed`；修改后单文件测试为 `4 passed`。
  * 最终联合测试命令与结果：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py \
    tests/test_peak_shaving_framework_tex_integration.py -q
  ```
  * 结果：`14 passed in 0.18s`。
- 最终编译：
  ```bash
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/plugins/cache/openai-bundled/latex/0.2.4/scripts/compile_latex.py \
    /root/paper_code/0427_tokenrl/paper_token_cross_survey/peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex \
    --compiler texlive --engine xelatex --json
  ```
  ```bash
  python3 /mnt/d/ccchtLinkData/UserProfile/.codex/plugins/cache/openai-bundled/latex/0.2.4/scripts/compile_latex.py \
    /root/paper_code/0427_tokenrl/paper_token_cross_survey/peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex \
    --compiler texlive --engine xelatex --json
  ```
  * 英文 PDF：24 页，500255 bytes；中文 PDF：20 页，876863 bytes；两者均为 PDF 1.5 输出。
  * 日志未发现 `LaTeX Error`、未定义控制序列、未定义引用/文献、multiply-defined 标签或 overfull box。
  * 保留的非阻塞警告为原稿已有的 underfull box，以及中文稿 Fandol 字体的 CJK script 警告。
- 页面核验：
  * Figure 1 位于英文第 4 页和中文第 3 页。
  * 使用 Poppler 以 130 dpi 渲染后，英文页黑像素比例为 `1.2010%`、近白像素比例为 `83.4408%`；中文页分别为 `0.9253%` 和 `83.8006%`。等比例预览确认图标、公式、直线/直角连线、色块和图注均完整。
  * `git diff --check` 通过。
- 状态：verified。

### 2026-07-11 14:35 - 平行公式标签间距修正

- 目标：修正作者指出的公式重叠问题。
- 诊断：用户临时截图文件已失效；检查 3200 px 正式图后，发现直连渠道的 $p^D_{m,t},q_{m,t}$ 与 $D^D_{m,t}$ 标签间距不足，中间商路由需求与批发价格/QoS 标签也接近上下标的实际高度。
- 原因：公式从普通文本改为 HTML 上下标后，字形实际高度增加，但平行箭头仍沿用旧的 21--41 个 Draw.io 单位间距。
- 修改范围：只调整对应箭头的垂直锚点，将公式轨道间距统一提高到至少 40 个 Draw.io 单位；保持箭头水平，不修改节点、公式内容、颜色或论文逻辑。
- 验证方式：新增平行公式轨道最小间距测试，重新导出 PNG、SVG、PDF，并进行全分辨率视觉检查。
- 红灯测试：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py::test_parallel_formula_labels_have_vertical_clearance -q
  ```
  * 初次运行得到 `1 failed`；服务商 A 的直连价格/QoS 与直连需求公式中心线仅相差 27.8 个单位，低于 40 单位门槛。
- 修复：
  * 将服务商 A 的四条公式轨道依次对齐到 170、212、255 和 297，间距为 42--43 个单位。
  * 将服务商 B 的四条公式轨道依次对齐到 380、422、464 和 506，间距均为 42 个单位。
  * API 中间商框高度由 180 增至 200 个单位，为服务商 B 的路由和批发信号提供空间；框内图标与文字内容不变。
  * 重新计算所有受影响的入口/出口锚点，公式箭头仍保持水平，两端高度误差不超过 0.5 个单位。
- 最终验证：完整测试为 `10 passed`；Draw.io 严格检查为 `0 error(s), 0 warning(s)`；PNG、SVG、PDF 已重新导出。
- 视觉检查：3200 px 正式图中未再发现上下标相碰、公式标签重叠、箭头倾斜或节点遮挡。
- 状态：verified。

### 2026-07-11 13:44 - 求解器到证据框箭头水平对齐

- 目标：修正作者指出的残余倾斜箭头。
- 诊断：用户临时截图文件已失效；检查当前正式图后，唯一仍明显倾斜的前向流程箭头是 `Fictitious play / Double oracle` 到 `Evidence reported`。
- 修改范围：仅调整证据框入口锚点，使其与求解器节点中心保持同一水平线；不移动节点、不修改公式、颜色、市场逻辑或实验结论。
- 验证方式：新增几何锚点回归检查，重新导出 PNG、SVG、PDF，并运行完整测试与 Draw.io 严格结构验证。
- 红灯测试：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py::test_solver_to_evidence_arrow_is_horizontal -q
  ```
  * 初次运行得到 `1 failed`；求解器出口高度为 182.5，证据框原入口高度为 222.5，两端相差 40 个 Draw.io 单位。
- 修复：将证据框入口锚点从 `entryY=0.5` 调整为 `entryY=0.373`，两端高度差降至 0.005 个单位，箭头成为水平直线。
- 最终验证：完整测试为 `9 passed`，Draw.io 严格检查为 `0 error(s), 0 warning(s)`；PNG、SVG、PDF 已重新导出。
- 视觉检查：所有前向流程箭头均为水平或垂直直线；仅固定点返回迭代保留直角折线。
- 状态：verified。

### 2026-07-11 13:22 - 框架图字体层级与公式排版

- 目标：修正作者指出的字体、字号和公式展示问题，不改变已确认的市场结构、求解逻辑与箭头布局。
- 当前审计：
  * Draw.io 源中有 28 处 `fontSize=13`、10 处 `fontSize=14`，主要位于箭头标签、服务商公式、用户说明和图例。
  * 公式仍使用 `w_A,t`、`p^D_A,t` 等普通文本写法，缩放到论文版心后上下标关系不清楚。
  * 全图已使用 Times New Roman，但字号层级不足以保证单栏或双栏 PDF 中的公式可读性。
- 修改目标：
  * 所有可见文字不低于 16 pt；服务商内部公式和价格公式使用 18 pt；节点标题使用 22 pt 左右；两块面板标题使用 26--28 pt。
  * 数学变量使用 Times New Roman 斜体，服务商、时段和渠道索引使用 HTML `<sub>`，直连与中间商渠道标记使用 `<sup>`。
  * 路由流量、直连需求、批发价格、直连价格和 QoS 信号改用与主稿一致的数学记号，而不是含糊的普通英文标签。
  * 保留当前水平直线与固定点直角反馈，不增加新节点或改变论文结论。
- 验证方式：新增公式 HTML 结构、Times New Roman 和最小字号测试；重新导出 PNG、SVG、PDF，并检查字体嵌入、公式裁切和标签遮挡。
- TDD 红灯：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py::test_provider_notation_matches_manuscript \
    tests/test_peak_shaving_framework_drawio.py::test_visible_text_uses_times_new_roman_and_readable_sizes -q
  ```
  * 初次运行得到 `2 failed`：公式仍是普通下划线/脱字符文本，且最小可见字号只有 13 pt。
- 修改：
  * 生成器新增统一数学变量格式，将变量设为 Times New Roman 斜体，并使用 HTML 上下标输出 $G_A$、$w_{A,t}$、$p^D_{A,t}$、$D^D_{A,t}$、$r_{A,t}D^I_t$、$u_{A,t}$ 和 $q_{A,t}$ 等记号。
  * 直连需求箭头不再写普通英文 `direct demand`，而是分别标注 $D^D_{A,t}$ 和 $D^D_{B,t}$；价格/QoS 虚线分别标注对应的 $p$、$w$ 与 $q$。
  * 所有可见文字提升到 16 pt 以上；服务商价格、容量、利用率和 QoS 公式为 18 pt；节点标签为 18 pt；主体标题为 22 pt；面板标题为 27/28 pt。
  * 放大后严格校验首次发现 3 处文本框边界相交：市场标题与容量关系，以及两个服务商标题与价格公式。调整文本框位置和高度后警告归零。
- 最终验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py -q
  uv run python /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figure_sources/peak_shaving_framework_2026-07-11.drawio --strict
  pdffonts figures/peak_shaving_framework_2026-07-11.pdf
  ```
  * 完整测试为 `8 passed`；严格结构检查为 `0 error(s), 0 warning(s)`。
  * 字号分布由 13--24 pt 调整为 16--28 pt，公式测试确认不再出现 `w_A,t`、`p^D_A,t` 等普通文本记号。
  * 生成器压缩为 296 行，低于项目 300 行上限；该调整只删除多余空行，不改变图形输出。
  * PDF 嵌入 Times New Roman regular、bold、italic 和 bold italic 四种字形；四种字体均为嵌入子集并包含 Unicode 映射。
  * 最终 PNG 为 3200×1921；SVG 可解析；PDF 为 1 页。
  * 全图预览未发现上下标裁切、公式错位、文字越界或标签遮挡。市场结构、有限网格求解顺序和证据边界均未改变。
  * 本轮未修改中英文 TeX、实验数据或论文结论。
- 状态：verified。

### 2026-07-11 12:50 - 必要折线策略与连接端点对齐

- 目标：落实作者补充要求：箭头以直线为主，节点避让或返回迭代时允许使用直角折线。
- 制图规则：
  * 同层级、同方向的请求流、路由流、价格/QoS 信号和求解步骤优先使用水平或垂直直线。
  * 仅当直线会经过节点、造成语义误读或用于明确的返回迭代时使用直角折线；不使用圆角折线。
- 修改：
  * 重新计算连接锚点，将直连 A、直连 B、中间商零售信号、中间商路由以及两家服务商返回的批发价格/QoS 信号全部水平对齐。
  * 当前图不需要新增市场层折线；唯一保留的直角折线仍是固定点到 QoS 依赖用户选择的返回迭代。
  * 两轮预览确认水平信号线没有经过中间商、退出节点、服务商内部公式或图标。
- 输出：继续覆盖 `peak_shaving_framework_2026-07-11.drawio` 及对应 PNG、SVG、PDF，文件名不变。
- 验证：定向测试 `7 passed`；Draw.io 严格检查为 `0 error(s), 0 warning(s)`；PNG 为 3200×1921。
- 状态：verified。

### 2026-07-11 12:12 - 框架图直线化与论文语义复核

- 目标：
  * 根据作者反馈，将框架图中的前向请求流、价格/QoS 信号和求解步骤尽量改为直线箭头。
  * 重新核对 Figure 1 与主稿的市场顺序、固定点计算和有限网格证据边界，避免图形为了美观改变论文含义。
- 论文语义核对：
  * 两个固定容量服务商同时选择批发和直连价格形状，且 $G_A>G_B$。
  * API 中间商观察批发价格和 QoS，在有限响应网格中选择零售价格与路由参数。
  * 时间刚性和时间弹性用户在“渠道—时段”组合与退出选项之间进行 logit 选择；“刚性”表示迁移成本较高，不表示完全不能迁移。
  * 服务商负载由直连需求和中间商路由需求共同构成，负载决定利用率，利用率通过 sigmoid 退化函数决定 QoS。
  * 每个候选价格组合内计算用户选择与路由—QoS 固定点，再选择中间商最优响应并形成服务商收益矩阵；虚拟博弈和双重 oracle 只给出有限候选集上的 regret 诊断。
  * 证据输出继续限定为有限网格 regret、QoS 保护方向和利润边界，不表示连续策略空间 Nash 证明或稳健利润提升。
- 布局决策：
  * 重新对齐直连 A、API 中间商、直连 B 和退出四条通道，使其分别与对应目标形成直线或短对角线。
  * 所有前向求解步骤保持水平直线；仅“QoS 依赖的选择与固定点迭代”保留一条返回箭头。
- 验证方式：新增直线连接器回归测试，重新运行 Draw.io 严格结构验证、PNG 全分辨率检查和三格式导出检查。
- TDD 红灯：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py::test_forward_connectors_are_straight \
    tests/test_peak_shaving_framework_drawio.py::test_solver_sequence_matches_the_manuscript \
    tests/test_peak_shaving_framework_drawio.py::test_connectors_preserve_market_and_feedback_semantics -q
  ```
  * 初次运行得到 `3 failed`：连接器仍为 `orthogonalEdgeStyle`，固定点反馈仍指向中间商响应，且求解节点仍使用较宽泛的旧名称。
- 修改：
  * 生成器将普通连接器统一为 `edgeStyle=none;rounded=0`，因此用户流、直连流量、中间商路由、价格/QoS 信号、服务商内部计算链和所有前向求解步骤均为直线。
  * 仅 `solver_feedback` 使用正交返回路径；其目标从“中间商响应”改为“渠道—时段 logit 选择”，表示 QoS 对用户选择与需求的反馈。
  * 渠道节点按“直连 A—中间商—直连 B—退出”重新对齐；服务商 A、服务商 B 和退出节点与对应流量线保持水平或短对角关系。
  * 求解链改为“服务商价格形状候选—中间商响应网格—渠道/时段 logit 选择—联合路由/QoS 固定点—中间商最优响应与服务商收益矩阵—虚拟博弈/双重 oracle—证据报告”。
  * 第一轮直线化预览中，服务商 B 的直连价格/QoS 虚线擦过退出节点；最终将该虚线移到直连需求线上方，不再经过任何节点。
- 最终生成与验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run python \
    figure_sources/build_peak_shaving_framework_drawio.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py -q
  uv run python /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figure_sources/peak_shaving_framework_2026-07-11.drawio --strict
  ```
  * 完整测试为 `7 passed`；新增测试确认除固定点反馈外的全部连接器无折点，并检查求解链文本与主稿一致。
  * Draw.io 严格检查为 `0 error(s), 0 warning(s)`。
  * 最终 PNG 为 3200×1921、RGB、非隔行；SVG 可解析；PDF 为 1 页。
  * 两轮全图视觉检查确认节点、标题、公式和箭头没有遮挡；前向箭头均为直线，唯一折线路径是明确标注的固定点返回迭代。
  * 本轮未修改中英文 TeX、实验数据或论文结论；更新后的三个导出文件继续使用原文件名，便于后续替换 Figure 1。
- 状态：verified。

### 2026-07-11 11:55 - Streamline 图标版 Draw.io 论文框架图

- 目标：
  * 使用已核验的 Streamline Ultimate Color SVG 素材重绘论文 Figure 1。
  * 生成可编辑 Draw.io 源文件以及 PNG、SVG、PDF 投稿预览。
- 论文逻辑：
  * 上层展示异质用户与物联网负载、渠道—时段选择、中间商、直连渠道、退出选项、两家固定容量服务商及利用率—QoS 反馈。
  * 下层展示价格形状网格、中间商响应、用户选择、路由—QoS 固定点、收益矩阵、虚拟博弈、双重 oracle 和证据边界。
  * 实线仅表示请求或流量；虚线仅表示价格、QoS 或求解反馈。
- 设计与计划：
  * `docs/superpowers/specs/2026-07-11-peak-shaving-framework-drawio-design.md`
  * `docs/superpowers/plans/2026-07-11-peak-shaving-framework-drawio.md`
- 输入：
  * `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`
  * `figure_sources/iot_icon_candidates/streamline_ultimate_color/`
- 输出目标：
  * `figure_sources/peak_shaving_framework_2026-07-11.drawio`
  * `figures/peak_shaving_framework_2026-07-11.png`
  * `figures/peak_shaving_framework_2026-07-11.svg`
  * `figures/peak_shaving_framework_2026-07-11.pdf`
- 验证方式：pytest 语义检查、Draw.io 严格结构验证、PNG 全分辨率检查、SVG/PDF 解析和 `git diff --check`。
- TDD 红灯：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py::test_drawio_contains_required_market_and_solver_nodes -q
  ```
  * 结果：`1 failed`；失败原因为目标文件 `figure_sources/peak_shaving_framework_2026-07-11.drawio` 尚不存在，符合新增框架图的预期红灯。
- Draw.io 生成：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run python \
    figure_sources/build_peak_shaving_framework_drawio.py
  uv run python /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figure_sources/peak_shaving_framework_2026-07-11.drawio --strict
  ```
  * 第一轮结构校验报告 2 个顶栏重叠警告：主标题分别与容量关系和请求流图例相交。
  * 缩短并左移主标题后，严格校验为 `0 error(s), 0 warning(s)`。
  * 第一轮导出中，Draw.io 30.3.6 未渲染采用 Base64 数据 URI 的内嵌图标；最小复现确认同一 SVG 改为 URL 编码数据 URI 后能够显示。生成器已统一采用 URL 编码，不依赖外部图像路径。
  * 第二轮视觉检查发现服务商公式沿用了内部 ID 的小写 `a/b`。新增记号一致性测试并确认红灯后，将图中文字统一为论文使用的 `A/B`，包括 `w_{A,t}`、`p^D_{A,t}`、`u_{A,t}`、`q_{A,t}` 及服务商 B 的对应记号。
- 最终导出：
  ```bash
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    -x -f png -e --width 3200 --border 12 \
    -o figures/peak_shaving_framework_2026-07-11.png \
    figure_sources/peak_shaving_framework_2026-07-11.drawio \
    --disable-update --no-sandbox
  uv run python /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/repair_png.py \
    figures/peak_shaving_framework_2026-07-11.png
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    -x -f svg -e --embed-svg-images --border 12 \
    -o figures/peak_shaving_framework_2026-07-11.svg \
    figure_sources/peak_shaving_framework_2026-07-11.drawio \
    --disable-update --no-sandbox
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    -x -f pdf -e --border 12 \
    -o figures/peak_shaving_framework_2026-07-11.pdf \
    figure_sources/peak_shaving_framework_2026-07-11.drawio \
    --disable-update --no-sandbox
  ```
- 最终验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_peak_shaving_framework_drawio.py -q
  file figure_sources/peak_shaving_framework_2026-07-11.drawio \
    figures/peak_shaving_framework_2026-07-11.{png,svg,pdf}
  ```
  * 定向测试为 `5 passed`；覆盖必要节点、市场与求解连线、实线/虚线语义、论文公式记号、24 个以上本地嵌入 SVG 以及三个导出格式。
  * PNG 为 3200×1921、RGB、非隔行；SVG 可解析且内嵌图标；PDF 1 页、185507 字节。
  * Draw.io 严格结构验证为 `0 error(s), 0 warning(s)`。
  * 全分辨率视觉检查未发现图标缺失、文字裁切、节点遮挡或箭头穿过标题。上层的市场机制与下层的有限网格诊断分区清楚，颜色分别承担主体和证据类型的区分，不依赖单一黄蓝配色。
- 边界：本轮先交付框架图供作者审阅，不修改中英文 TeX、实验数据或论文结论。
- 状态：verified。

### 2026-07-10 23:39 - 参考图风格的彩色线稿图标素材

- 目标：
  * 只获取与用户参考图一致的彩色线稿图标，不绘制框架图，不修改论文和既有图。
  * 覆盖论文中的物联网终端、市场主体、API 路由、GPU 容量、QoS、动态价格和仿真证据。
- 风格判断：
  * 参考图的主要特征是深色粗轮廓、白灰主体和黄/蓝/红/绿等低饱和填色，而不是 3D emoji。
  * 最终采用 Streamline Ultimate Color，同一图标系列可覆盖服务器、数据库、芯片和网络等技术对象，避免混合多个画风。
- 来源与许可：
  * 官方仓库：<https://github.com/webalys-hq/streamline-vectors>
  * 固定提交：`52d750c9ce051e51cb181b7a78932120c48541d0`
  * 来源目录：`ultimate/colors`
  * 许可：CC BY 4.0；使用时需署名 Streamline 并链接 <https://streamlinehq.com>。
- 命令：
  ```bash
  git ls-remote https://github.com/webalys-hq/streamline-vectors.git HEAD
  git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/webalys-hq/streamline-vectors.git \
    /tmp/streamline-vectors-20260710
  git -C /tmp/streamline-vectors-20260710 sparse-checkout add ultimate/colors
  curl -fsSL https://creativecommons.org/licenses/by/4.0/legalcode.txt \
    -o figure_sources/iot_icon_candidates/streamline_ultimate_color/LICENSE-CC-BY-4.0.txt
  ```
- 输出：
  * `figure_sources/iot_icon_candidates/streamline_ultimate_color/svg/`：48 个原始 SVG，共六类，每类 8 个。
  * `figure_sources/iot_icon_candidates/streamline_ultimate_color/SOURCES.tsv`：本地文件、上游路径和论文用途的逐项映射。
  * `figure_sources/iot_icon_candidates/streamline_ultimate_color/ATTRIBUTION.md`：可用于论文或图注的署名文本。
  * `figure_sources/iot_icon_candidates/streamline_ultimate_color/LICENSE-CC-BY-4.0.txt`：CC BY 4.0 法律文本。
  * `figure_sources/iot_icon_candidates/streamline_ultimate_color/SHA256SUMS.txt`：素材校验和。
- 失败与修复：
  * 第一次校验和清单从项目根目录生成，文件名带有完整素材目录前缀；进入素材目录执行 `sha256sum -c` 时，48 个路径被重复拼接并全部报告 `No such file or directory`。
  * SVG 解析和上游逐字节比对在同一次检查中均已通过，因此问题只在校验和清单的相对路径。
  * 修复方式是在素材目录中以 `svg/` 为根重新生成清单：
    ```bash
    cd figure_sources/iot_icon_candidates/streamline_ultimate_color
    find svg -type f -name '*.svg' -print0 | sort -z | \
      xargs -0 sha256sum > SHA256SUMS.txt
    sha256sum -c SHA256SUMS.txt
    ```
  * 第二次检查将“每个图标都有彩色填充”设为硬断言，`flow_split.svg` 因为是纯黑分流箭头而触发失败。逐项诊断确认其来源、轮廓和 SVG 结构均正常；这是同一官方系列中的连接符号，不是损坏或混入的素材。最终检查改为 48 个文件均具深色轮廓，47 个对象图标含彩色填充，分流箭头允许仅使用轮廓。
- 当前验证：
  * 素材数和清单数均为 48；六类各 8 个。
  * 48 个 SVG 均可解析，均含 `viewBox`，未发现脚本、事件处理器或远程资源引用。
  * 48 个本地 SVG 与固定上游提交中的源文件逐字节一致。
  * 子目录 48 项校验和及候选素材总目录 148 项校验和全部通过。
  * 48 个文件均含深色轮廓，其中 47 个对象图标含多色填充；`flow_split.svg` 是唯一的纯轮廓连接符号。
  * 敏感信息扫描无匹配，`git diff --check` 无输出，跟踪中的 TeX 改动数为 0。
  * 临时预览确认图标具有参考图所需的深色轮廓、浅色主体和多色填充；预览未写入论文目录。
  * 本任务未修改 TeX、实验结果、Figure 1 或论文结论。
- 下一步：由作者从该素材集中选择框架图实际使用的图标，再单独设计 Figure 1。
- 状态：verified。

### 2026-07-10 23:13 - 只获取具体物联网图标原文件

- 目标：
  * 按用户最新要求停止场景组合，只收集更具体、彩色、具有物联网设备感的图标原文件。
- 范围调整：
  * 不继续修改复合场景，不重绘 Figure 1，不修改 TeX。
  * 已生成的场景素材暂时保留，不擅自删除；本阶段只新增候选图标和许可记录。
- 来源：
  * Microsoft Fluent Emoji：MIT，固定提交 `62ecdc0d7ca5c6df32148c169556bc8d3782fca4`。
  * 3dicons：CC0 1.0，固定提交 `8884d59e68a7bae0e0e2163af5b6c2ad992c01c8`。
- 选择：
  * Fluent Emoji 36 个概念，每个保留 3D PNG 和彩色 SVG。
  * 3dicons 20 个动态彩色透明 PNG。
  * 两套素材分目录保存，不在本阶段混合或合成。
- 输出清单：
  * `figure_sources/iot_icon_candidates/SOURCES.tsv`
  * `figure_sources/iot_icon_candidates/README.md`
- 下一步：
  * 人工浏览两个独立素材目录，后续再决定采用哪一个图标家族；本阶段不组合或插入论文图。
- 获取命令：
  ```bash
  git ls-remote https://github.com/microsoft/fluentui-emoji.git HEAD
  git ls-remote https://github.com/realvjy/3dicons.git HEAD
  git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/microsoft/fluentui-emoji.git /tmp/fluentui-emoji-20260710
  git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/realvjy/3dicons.git /tmp/3dicons-20260710
  ```
- 获取过程：
  * 第一次批量提取在 Fluent `chart_increasing` 的按需 blob 获取阶段中断，目录当时只有 26 个 PNG、25 个 SVG，并留下一个零字节文件；未继续把该状态记录为成功。
  * 单独读取相同上游路径成功，确认清单路径正确。随后改为逐文件临时写入、成功后替换，并对 Git blob 和 CDN 下载各重试最多三次。
  * 重试后失败数为 0，零字节和 `.part` 文件均为 0。
- 输出：
  * `figure_sources/iot_icon_candidates/fluentui_emoji/3d_png/`：36 个 256×256 RGBA PNG。
  * `figure_sources/iot_icon_candidates/fluentui_emoji/color_svg/`：36 个原始彩色 SVG。
  * `figure_sources/iot_icon_candidates/fluentui_emoji/LICENSE-MIT.txt`。
  * `figure_sources/iot_icon_candidates/3dicons/color_png/`：20 个 400×400 RGBA PNG。
  * `figure_sources/iot_icon_candidates/3dicons/LICENSE-CC0.txt`。
  * `figure_sources/iot_icon_candidates/SHA256SUMS.txt`：92 个图标文件的校验和。
- 验证命令：
  ```bash
  file figure_sources/iot_icon_candidates/fluentui_emoji/3d_png/*.png
  file figure_sources/iot_icon_candidates/3dicons/color_png/*.png
  uv run python -c "from pathlib import Path; from xml.etree import ElementTree; [ElementTree.fromstring(p.read_text(encoding='utf-8')) for p in Path('figure_sources/iot_icon_candidates/fluentui_emoji/color_svg').glob('*.svg')]"
  cd figure_sources/iot_icon_candidates && sha256sum -c SHA256SUMS.txt --quiet
  ```
- 验证结果：
  * 原始图标总数为 92：Fluent Emoji 36 个 3D PNG + 36 个彩色 SVG，3dicons 20 个彩色 PNG。
  * 36 个 Fluent SVG 均通过 XML 解析，未发现远程脚本或图像引用。
  * Fluent 的 72 个文件与固定提交逐字节一致；3dicons 的 20 个下载 URL 与固定提交中的元数据全部一致。
  * 所有 PNG 均带透明通道，尺寸分别稳定为 256×256 和 400×400；零字节文件为 0。
  * `SHA256SUMS.txt` 在素材目录中验证通过。首次从仓库根目录运行导致相对路径假失败，修正工作目录后退出码为 0。
  * 本阶段没有生成联系表、复合场景或新论文图，也没有修改 TeX、实验数据和既有 Figure 1。
- 状态：verified。

### 2026-07-10 22:58 - 具体物联网复合场景素材库

- 目标：
  * 根据用户提供的彩色物联网参考风格，把单体图标进一步组合成可直接表达论文语义的设备与流程场景。
- 设计边界：
  * 保留现有 48 个基础 IconPark 图标库，不覆盖已有 SVG 或 Draw.io 库。
  * 新增 18 个 480×300 复合场景，覆盖终端负载、API 网关、中间商路由、大小服务商集群、GPU/QoS 和仿真诊断。
  * 只使用本地 IconPark SVG 和原创排版、连线与底板，不使用 ImageGen，不复制参考图中的具体图标。
- 计划：
  * `docs/superpowers/specs/2026-07-10-paper-iot-scene-library-design.md`
  * `docs/superpowers/plans/2026-07-10-paper-iot-scene-library.md`
- 输入：
  * 用户提供的视觉参考图，仅用于提取“彩色设备组合、空间层次、明确箭头和短标记”的风格特征。
  * `figure_sources/paper_icon_library/manifest.json` 及其 48 个本地 IconPark SVG。
- 下一步：
  * 根据联系表选择 8–12 个场景重组 Figure 1；本任务暂不替换现有论文图。
- 红灯测试：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_paper_iot_scene_library.py -q
  ```
  * 初次运行得到 5 个预期失败，原因是场景清单、独立 SVG、Draw.io 库、联系表和说明文件尚未生成。
  * 写入清单后，场景范围测试首先通过：18 个唯一场景、四组数量正确、15 个 `core` 和 3 个 `optional`，所有组件 ID 均存在于基础库。
- 生成命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run python \
    figure_sources/build_paper_iot_scene_library.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest \
    tests/test_paper_iot_scene_library.py -q
  ```
- 输出：
  * `figure_sources/paper_iot_scene_library/manifest.json`：18 个场景的对象、位置、颜色、连线、短标记和优先级。
  * `figure_sources/paper_iot_scene_library/scenes/`：18 个独立 480×300 SVG。
  * `figure_sources/paper_iot_scene_library/paper-iot-scenes.xml`：18 项 Draw.io 自定义场景库。
  * `figure_sources/paper_iot_scene_library/README.md`：场景用途、导入方法、许可和非生成式来源说明。
  * `figures/paper_iot_scene_library_2026-07-10.svg`、`.png` 和 `.pdf`：六列三行双语联系表。
- 视觉检查：
  * 用户终端场景分别显示交互窗口、手机、时钟、代码终端、日程和批任务；可选物联网场景显示多设备、摄像头和智能体。
  * 市场层分别显示 API 网关、中间商双服务商分流、大小 GPU 集群、服务商直连和退出选项。
  * GPU/QoS 与仿真层分别显示请求、利用率、QoS 反馈、拥塞边界、分时价格、路由分流、固定点和 regret。
  * 全分辨率检查未发现对象裁切、场景越界、箭头穿过主体、标题遮挡或中文缺字。
- 验证命令：
  ```bash
  file figures/paper_iot_scene_library_2026-07-10.{svg,png,pdf} \
    figure_sources/paper_iot_scene_library/paper-iot-scenes.xml
  pdfinfo figures/paper_iot_scene_library_2026-07-10.pdf
  pdffonts figures/paper_iot_scene_library_2026-07-10.pdf
  jq '.scenes | length' figure_sources/paper_iot_scene_library/manifest.json
  find figure_sources/paper_iot_scene_library/scenes -type f -name '*.svg' | wc -l
  sed -e 's/^<mxlibrary>//' -e 's#</mxlibrary>$##' \
    figure_sources/paper_iot_scene_library/paper-iot-scenes.xml | jq 'length'
  rg -l '<script|href="https?://' figure_sources/paper_iot_scene_library
  git diff --check
  ```
- 验证结果：
  * 定向测试为 `5 passed`。
  * PNG 为 3600×2050、RGB、非隔行；SVG 可解析；PDF 为 1 页、107530 字节。
  * PDF 嵌入 Times New Roman regular/bold 和 SimSun 字体。
  * 场景清单、独立 SVG 和 Draw.io 库条目数均为 18，远程脚本或图像引用为 0。
  * 生成脚本为 244 行，构建过程不访问网络，`git diff --check` 无输出。
  * 本任务未修改 TeX、实验数据、既有 Figure 1 或论文结论。
- 状态：verified。

### 2026-07-10 22:30 - 论文专用 IconPark 图标素材库

- 目标：
  * 建立一套覆盖论文市场主体、物联网工作负载、API 路由、GPU 服务、定价博弈、QoS 和仿真验证的可编辑图标库。
- 背景：
  * 用户确认采用全文核心版，并要求增加备用素材。
  * 当前 Figure 1 使用 Font Awesome Free；本任务先建立独立 IconPark 库，不直接替换现有图或 TeX。
- 设计：
  * 固定使用 IconPark 官方提交 `8dc132da4c85671ba6a5962c87aa2bdafbf158e9` 和 Apache-2.0 许可。
  * 选择 48 个 SVG，分为六类，每类 8 个；通过 `core` 和 `optional` 控制正文使用范围。
  * 生成原始 SVG、Draw.io 自定义库、PNG/PDF 联系表、语义清单和许可说明。
- 计划：
  * `docs/superpowers/specs/2026-07-10-paper-icon-library-design.md`
  * `docs/superpowers/plans/2026-07-10-paper-icon-library.md`
- 命令：
  ```bash
  git ls-remote https://github.com/bytedance/IconPark.git HEAD
  git clone --depth 1 --filter=blob:none --sparse \
    https://github.com/bytedance/IconPark.git /tmp/iconpark-src-20260710
  git -C /tmp/iconpark-src-20260710 sparse-checkout set packages/svg source types
  ```
- 当前结果：
  * 上游 HEAD 确认为 `8dc132da4c85671ba6a5962c87aa2bdafbf158e9`。
  * 官方 `@icon-park/svg` 包版本为 `1.4.2`，包元数据声明 `Apache-2.0`。
  * 本地稀疏检出包含 2662 个源 SVG，可从中按论文语义筛选，不需要复制整个图标仓库。
  * 首次运行 `uv run pytest tests/test_paper_icon_library.py -q` 时，pytest 在停止 fd 捕获时出现 `FileNotFoundError`，尚未进入预期的红灯断言。
  * 调查发现当前 WSL 会话的 `TEMP` 和 `TMP` 指向 Windows 挂载目录。Python `TemporaryFile` 在该目录中解除链接后可读写，但后续 `truncate` 失败；pytest 的 fd 捕获使用了同一路径。
  * 使用命令级 `TMPDIR=/tmp TEMP=/tmp TMP=/tmp` 后，临时文件探针通过，测试稳定得到 5 个预期失败，原因均为图标库产物尚未生成。未修改全局环境变量。
- 失败与诊断命令：
  ```bash
  uv run pytest tests/test_paper_icon_library.py -q
  uv run python -c "import tempfile; f=tempfile.TemporaryFile(mode='w+b'); f.write(b'x'); f.seek(0); print(f.read()); f.truncate()"
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run python -c "import tempfile; f=tempfile.TemporaryFile(mode='w+b'); f.write(b'x'); f.seek(0); print(f.read()); f.truncate(); print('truncate=ok')"
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest tests/test_paper_icon_library.py -q
  ```
- 下一步：
  * 根据预览选择 Figure 1 实际使用的核心图标；本任务不自动替换现有论文图。
- 生成命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run python figure_sources/build_paper_icon_library.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest tests/test_paper_icon_library.py -q
  ```
- 输出：
  * `figure_sources/paper_icon_library/manifest.json`：48 项语义清单，其中 30 项为 `core`，18 项为 `optional`。
  * `figure_sources/paper_icon_library/upstream_svg/`：48 个未经修改的 IconPark 源 SVG。
  * `figure_sources/paper_icon_library/paper-icons.xml`：可从 Draw.io 打开的自定义库，包含 48 个本地嵌入 SVG 条目。
  * `figure_sources/paper_icon_library/README.md`、`LICENSE-APACHE-2.0.txt` 和 `MODIFICATIONS.md`：使用说明、完整许可和派生修改说明。
  * `figures/paper_icon_library_2026-07-10.svg`、`.png` 和 `.pdf`：双语素材联系表。
- 视觉检查：
  * 第一轮发现 Times New Roman 不包含中文字形，中文标签显示为方框。
  * 字体探针确认 SimSun 可用；最终版本将英文固定为 Times New Roman，中文标签与双语标题中的中文部分单独使用 SimSun。
  * 第二轮全分辨率检查未发现图标裁切、卡片越界、标签遮挡或颜色混乱。六类素材均能区分，`core` 使用实线卡片，`optional` 使用浅灰虚线卡片。
- 验证命令：
  ```bash
  file figures/paper_icon_library_2026-07-10.{svg,png,pdf} \
    figure_sources/paper_icon_library/paper-icons.xml
  pdfinfo figures/paper_icon_library_2026-07-10.pdf
  pdffonts figures/paper_icon_library_2026-07-10.pdf
  sed -e 's/^<mxlibrary>//' -e 's#</mxlibrary>$##' \
    figure_sources/paper_icon_library/paper-icons.xml | jq 'length'
  find figure_sources/paper_icon_library/upstream_svg -type f -name '*.svg' | wc -l
  rg -l '<image|<script|href="https?://' figure_sources/paper_icon_library/upstream_svg
  git diff --check
  ```
- 验证结果：
  * 定向测试为 `5 passed`。
  * PNG 为 3200×2240、RGB、非隔行；SVG 可解析；PDF 为 1 页、120835 字节。
  * PDF 嵌入 Times New Roman regular/bold 和 SimSun 字体，没有依赖读者机器的中文字体回退。
  * Draw.io 30.3.6 的本地应用源码确认 `mxlibrary` 的 `data`、`w`、`h`、`title` 图像条目格式；生成库包含 48 个可解码 SVG 数据 URI。
  * 本地源文件数和清单条目数均为 48，未发现远程图像、脚本或远程 `href` 引用。
  * 生成脚本为 237 行，`git diff --check` 无输出。
  * 未修改 TeX、实验数据、现有 Figure 1 或论文结论。
- 状态：verified。
### 2026-07-13 15:35 - 第三轮服务商连续域偏离修正

- 目标：扩大服务商策略空间并全量重求均衡，避免主结果依赖旧的有限响应集。
- 背景：2,380 点候选集上的有限博弈达到零网格 regret，但独立连续域偏离审计未通过。
- 输入：
  * `spatiotemporal_equilibrium_provider2380.json`；
  * `spatiotemporal_offgrid_diagnostic_provider2380.json`。
- 已核对结果：
  * 服务商 A 的最佳偏离为 `[0.25, 0.55, 0.538125, 0.2]`，absolute regret 为 `10.2273`，relative regret 为 `1.2205%`；
  * 服务商 B 的最佳偏离为 `[0.25, 0.70, 0.538125, 0.4]`，absolute regret 为 `3.2937`，relative regret 为 `0.4445%`；
  * 所有偏离评估的最大联合固定点残差低于 `1.0e-9`，不能把偏离解释为数值未收敛。
- 决策：在保留前两轮全部候选的基础上，新增覆盖低批发基价、中等批发斜率、低直连基价及直连斜率交互的第三轮局部网格；完成重求后再次运行独立连续域偏离审计。
- 内存控制：缓存改为流式 `pickle.dump/load`，加载时逐项转移旧向量键记录，避免同时保留完整文件字节、旧映射和新映射；检查点间隔由 1,024 对提高到 8,192 对。确认内存峰值受控后，正式求解恢复为 16 个单线程工作进程。
- 缓存失配记录：首次 4,016 点续算因旧缓存签名错误地包含 `parallel_workers`，在并行度由 16 改为 8 后未能复用旧记录；运行在动态阶段写入 400 对后停止。针对这一问题新增回归测试，红灯结果为 `1 failed`，确认仅改变执行并行度会改变缓存签名。
- 修复：缓存身份只包含场景、模型和中间商响应参数，不再包含并行进程数；并行度仍完整记录在工件元数据中。
- 修复验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    --with numpy --with scipy --with nashpy pytest \
    tests/test_equilibrium_cache.py \
    tests/test_peak_shaving_submission_tools.py \
    tests/test_final_spatiotemporal_equilibrium.py -q
  ```
  * 结果为 `23 passed`；同一小型博弈在 1 和 2 个工作进程下得到相同缓存签名，第二次运行完整复用第一次记录。
- 正式续算命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with numpy --with scipy --with nashpy \
    python -m experiments.run_submission_spatiotemporal_equilibrium
  ```
- 4,016 点运行诊断：首个 8,192 对动态检查点约耗时 40 分钟，速度约为 `3.4 pairs/s`。按当前支持规模估算首轮全扫描约需 13 小时，且每个新增支持都需要继续扩展交叉评估；该方案被判定为不适合持续迭代的笛卡尔穷举。
- 方法调整：停止 4,016 点进程并保留完整的 8,592 对原子缓存。正式入口改为审计驱动自适应候选集：旧均衡正概率支持、统一定价基线、三轮偏离局部层和边界守卫进入有限博弈；随后仍以独立连续域 Latin-hypercube、轴向守卫和 pairwise refinement 作为必须通过的外部偏离审计。
- 证据边界：该流程支持“自适应有限候选集内的低 regret，并通过所声明连续域偏离审计”，不支持连续策略空间纳什均衡证明。
- 自适应网格实现：读取 `provider2380` 的两方正概率支持向量作为继续点，与统一策略、低/中/高斜率审计层及边界守卫去重合并；当前基线得到 40 个参考支持、726 个唯一候选和 12 个统一定价候选。
- 定向验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    --with numpy --with scipy --with nashpy pytest \
    tests/test_peak_shaving_submission_tools.py \
    tests/test_final_spatiotemporal_equilibrium.py -q
  uv run --no-project --with ruff ruff check \
    experiments/peak_shaving_submission_tools.py \
    experiments/run_submission_spatiotemporal_equilibrium.py
  ```
  * 结果为 `22 passed`，Ruff 为 `All checks passed!`。
- 新的稳定输出名为 `spatiotemporal_equilibrium_submission.json`；候选数量和参考工件哈希写入元数据，不再把可能继续扩展的候选数编码进文件名。
- 长作业记录：自适应续算依次写入 `9,464` 和 `17,656` 对检查点；约两小时后交互执行会话终止，未生成正式 JSON。日志无 traceback，`dmesg` 无 OOM 记录，内存始终有约 11 GiB 可用，因此判断为外层执行会话生命周期结束，而非数值或资源失败。
- 恢复策略：保留 `17,656` 对原子缓存，使用独立进程组运行相同模块，并单独记录 PID、退出码和日志；不修改模型、候选集、随机种子或容差。
- 后续审计入口统一：off-grid、intermediary globality、fixed-point multistart、mechanism decomposition、mixed distribution、parameter sensitivity 和 LaTeX macro builder 全部改为读取稳定的 `spatiotemporal_equilibrium_submission.json`；输出文件同样使用 `submission` 后缀。
- 路径回归测试先以 `7 failed, 17 passed` 确认旧 `provider2380` 常量仍存在，修改后运行：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    --with numpy --with scipy --with nashpy pytest \
    tests/test_final_offgrid_diagnostic.py \
    tests/test_submission_intermediary_audit.py \
    tests/test_submission_fixed_point_audit.py \
    tests/test_submission_mechanism_decomposition.py \
    tests/test_submission_mixed_distribution.py \
    tests/test_submission_spatiotemporal_sensitivity.py \
    tests/test_submission_result_macros.py -q
  ```
  * 结果为 `24 passed`，相关脚本 Ruff 检查为 `All checks passed!`。
- 自适应基线结果：独立进程退出码为 `0`，生成 `spatiotemporal_equilibrium_submission.json`。动态博弈含 726 个候选，在第 15 个 oracle 轮次以 `regret_tolerance` 结束；absolute regret 为 `2.27e-13`，relative regret 为 `2.72e-16`，最大联合固定点残差为 `1.00e-9`，共评估 47,520 个策略对。
- 新结果相对统一定价：aggregate peak load 下降 `12.259%`，maximum provider utilization 下降 `16.015%`，minimum provider QoS 从 `0.8899` 提高到 `0.9590`，aggregate market-side profit 下降 `2.809%`。这些数值尚未写入论文，需等待连续域偏离审计。
- 收敛说明：动态 regret 并非单调下降，第 2--3、7--8 和 9--10 轮出现回升；论文不得描述为单调收敛。动态混合均衡有 26×26 个正概率剖面，有限候选集内已验证，但不等同连续策略空间均衡。
- 中间商边界诊断：动态剖面中零售基价/斜率边界质量均为 0；route-beta 边界质量为 `28.74%`，near-deterministic routing 质量为 `24.91%`。因此 route beta 仍只能解释为路由饱和参数，不能当作稳定经济弹性估计。
- off-grid 执行优化：首次运行完成服务商 A 的 48 个候选后暂停并保留缓存。原工具每 16 个候选重写完整缓存，改为每 64 个候选检查点，并改用流式 `pickle.dump/load`；模型、候选设计、随机种子和评价函数均未改变。
- off-grid 优化验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    --with numpy --with scipy pytest tests/test_final_offgrid_diagnostic.py -q
  uv run --no-project --with ruff ruff check \
    experiments/offgrid_diagnostic_tools.py \
    experiments/run_spatiotemporal_offgrid_diagnostic.py
  ```
  * 结果为 `5 passed`，Ruff 为 `All checks passed!`；恢复后首先完成 64/1,031 个服务商 A 候选和 1,664 个策略对，确认旧缓存被复用。
- 连续域偏离审计结果：服务商 A/B 分别评估 1,208/1,191 个候选和 31,408/30,966 个策略对；relative off-grid regret 分别为 `0.4864%` 和 `0.2714%`，均低于预先设定的 `0.5%` 门槛。所有联合固定点均收敛，最大残差低于 `1.0e-9`。该结果是有界采样与局部 refinement 诊断，不是连续策略空间证明。
- 覆盖率修正：新混合均衡需要 266 个最高权重剖面才能覆盖 80% 概率质量，旧默认上限 192 只能覆盖 `70.97%`。新增红灯测试确认函数此前会静默接受不足覆盖（`1 failed`）；审计默认上限提高到 320，覆盖不足时现在直接报错。
- 剖面审计并行：中间商 differential-evolution 全局性审计和固定点随机初始化审计按剖面并行，最多使用 16 个单线程进程；每个剖面的 seed 仍由原顺序确定，不改变搜索设计。
- 首次覆盖率修复验证中，`10 passed`，但 Ruff 报告 13 个 `E402`，原因是 BLAS 单线程环境必须在 NumPy/SciPy 导入前设置；随后为这些延迟导入添加局部 `noqa`，不移动环境设置。
- 中间商全局性反例：80% 质量审计中的 4 个剖面出现 `0.44%--0.56%` 的 follower 利润改进，均位于 `route_beta=0` 且更优零售斜率约为 0.275 的内部盆地。新增针对 provider vectors `[0.315,0.8,0.579375,0.4]` / `[0.25,1.1,0.55875,0.3]` 的回归测试，原搜索利润为 `295.3283`，低于独立搜索的约 `296.973`，红灯结果为 `1 failed`。
- 求解器修正：中间商 coarse slope seeds 从 `(-0.6,0,0.6)` 扩展为 `(-0.6,0,0.3,0.6)`，专门覆盖审计发现的低-beta内部正斜率盆地。该变更会使旧均衡缓存失效，必须重新求均衡和全部后续审计。
- 求解器修正验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    --with numpy --with scipy --with nashpy pytest \
    tests/test_intermediary_response_optimizer.py -q
  uv run --no-project --with ruff ruff check \
    pricing_sim/intermediary_response.py \
    tests/test_intermediary_response_optimizer.py
  ```
  * 结果为 `3 passed`，Ruff 为 `All checks passed!`；反例候选利润超过 `296.9`、route beta 仍为 0、零售斜率进入 `(0.2,0.35)`。
- 决策：修正改变 follower 最优响应和服务商收益矩阵，不能局部替换四个剖面。归档修正前均衡、off-grid、固定点和全局性审计工件后，从当前正概率支持重建全部缓存并重新求均衡。
- 归档：修正前四个工件分别保存为 `*_pre_interior_seed.json`；原 252 MB 主缓存移动到 `/tmp/peak_shaving_audit_enriched_equilibrium_pre_interior_seed/`，新求解使用空缓存，防止语义不同的 follower 响应记录被误复用。
- 重求状态：统一子博弈完成 95 对缓存；动态受限 26×26 支持完成 676 对，正在对 726 个自适应候选重新执行全偏离扫描。
- 修正后均衡：独立进程退出码为 `0`，动态收益矩阵从空缓存重建 36,712 对；以旧 26×26 正概率支持为起点，首个 oracle 轮次对全部 `719` 个候选的 full-grid regret 即为 `0`，无新增支持。`metadata.full_candidate_count`、`metadata.candidate_design.candidate_count`、`provider_strategy_grid.candidate_count` 和 `dynamic.candidate_count` 四处数量一致；修正前自适应基线的候选数为 `726`，不得用于本轮正式结果。
- 有限候选收益复核：动态工件中 A 的 expected/best-response payoff 均为 `836.8918216596169`，B 的两项均为 `741.148569466216`；两方 full regret 均为 0，`full_grid_verified=true`，求解方法记录为 `highs_milp_complementarity`。
- 续算种子追溯：正式工件在覆盖前从稳定输出路径读取种子，因此元数据中的路径仍显示 `spatiotemporal_equilibrium_submission.json`；记录的种子 SHA-256 `351ba43ca53fce19cce6a1ed111ebafdc02c04aec62dfb7135c0ec8992cb6122` 与归档文件 `spatiotemporal_equilibrium_submission_pre_interior_seed.json` 完全一致。正式工件本身的 SHA-256 为下述 `b00a61...`。
- 修正后主指标：aggregate peak load 下降 `12.2548%`，maximum provider utilization 下降 `16.0808%`，minimum provider QoS 从 `0.8899` 提高到 `0.9592`，aggregate market-side profit 下降 `2.8041%`。相对修正前，主指标变化均小于 `0.001` 的绝对量级，但这些新值仍需重新通过 off-grid、follower globality 和 fixed-point 审计。
- 混合期望口径：主表的动态 aggregate peak `197.048` 是剖面级实现峰值的概率期望 $E[\max_t L_t]$；期望时段曲线的最高点为 `194.845`，即 $\max_t E[L_t]$。同理，主表最大利用率 `1.2172` 是 $E[\max_{m,t}u_{m,t}]$，而期望利用率曲线的最大值为 `1.1978`。终稿必须在指标定义、表题和图注中明确区分，不能用图中曲线峰值直接复述主表数值。
- 图 1 证据标签复核：当前导出仍含 `Finite-grid price competition`、`Nashpy restricted equilibrium` 和 `Full 225-point deviation scan`，与修正后的连续多起点中间商响应、HiGHS MILP 互补求解和 719 点审计自适应候选扫描不一致。最终候选数稳定后必须更新 Draw.io 源和三种导出格式，旧图不得用于终稿。
- 修正后中间商边界质量：零售基价和零售斜率的边界质量均为 0；route-beta 边界质量为 `28.9007%`，其中几乎全部来自下界 0，达到上界附近的质量仅为 `0.0128%`；near-deterministic routing 质量为 `25.0939%`。route beta 只能作为路由饱和控制量，不解释为可外推的经济弹性。
- 新均衡 SHA-256 为 `b00a61ad53110b324578326e2d816db73a6c6aafda54cf27ba58f318047f18e0`；旧审计因均衡和中间商响应源码哈希均变化而失效，不得继续引用。
- 来源哈希复核：逐项重算正式均衡元数据中的 10 个 SHA-256，`spatiotemporal_mechanism.py`、`spatiotemporal_game.py`、`intermediary_response.py`、有限博弈与均衡工具、两个均衡入口、QoS 校准工件和 BurstGPT 派生负载均与当前文件完全一致，无源码漂移。
- 修正后离网审计重新从空缓存运行；旧缓存移动到 `/tmp/peak_shaving_submission_offgrid_pre_interior_seed/`，新缓存为 `/tmp/peak_shaving_submission_offgrid/`，避免复用中间商搜索语义不同的剖面结果。
- 实际执行命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy --with scipy \
    python -m experiments.run_spatiotemporal_offgrid_diagnostic
  ```
  * 独立进程的 PID、退出码和日志分别写入 `/tmp/peak_shaving_submission_offgrid.pid`、`/tmp/peak_shaving_submission_offgrid.exit` 和 `artifacts/peak_shaving/20260712_expanded_response/submission_offgrid_interior_seed_detached.log`。
  * 2026-07-14 08:43 检查时，服务商 A 的全局守卫已完成 `768/1,031` 个候选和 `19,968` 个策略对；16 个单线程工作进程持续运行，缓存为 100 MB，尚未生成本轮正式 JSON。
  * 2026-07-14 09:03 尝试只读加载 187 MB 的主策略对 pickle 以重构支持收益，Python 进程未返回退出码，系统 swap 显示已满；未修改缓存或工件。随后确认 off-grid 主进程和 16 个 worker 仍正常运行。决定不再在长审计期间展开该大对象，支持收益一致性改用正式工件已记录的期望收益、最佳响应收益和 regret 字段验证。
- 全剖面审计升级：修正后动态混合均衡有 676 个正概率剖面，覆盖 80% 质量需要 274 个。为避免只审计高概率子集，中间商独立全局搜索和固定点随机初始化审计的默认覆盖率从 `0.8` 提高到 `1.0`，剖面安全上限从 320 提高到 1,000；正式运行将检查全部 676 个活跃剖面。
  * 红灯命令：
    ```bash
    TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
      --with numpy --with scipy pytest \
      tests/test_submission_intermediary_audit.py \
      tests/test_submission_fixed_point_audit.py -q
    ```
    结果为 `2 failed, 10 passed`，失败原因为全覆盖默认常量尚未实现。
  * 实现后同一测试为 `12 passed`；相关脚本与测试的 Ruff 检查为 `All checks passed!`。
- 审计来源追踪：中间商全局性审计现记录自身脚本、`intermediary_response.py`、`spatiotemporal_game.py` 和 `peak_shaving_market.py` 的 SHA-256；固定点审计记录自身脚本及固定点相关实现的 SHA-256。新增测试先以 `2 failed, 12 passed` 确认帮助函数不存在，实现后为 `14 passed`，Ruff 为 `All checks passed!`。
- 论文数字防混用门禁：`build_submission_result_macros.py` 现在要求 off-grid、中间商和固定点审计中的 `equilibrium_sha256` 与当前正式均衡完全一致。测试先以 `2 failed, 2 passed` 失败，实现后为 `4 passed`，Ruff 通过。用当前尚未重跑完的旧审计实测时命令以退出码 `1` 拒绝生成宏，并准确报告旧哈希 `351ba43...` 与当前哈希 `b00a61...` 不一致。
- 派生工件来源追踪：混合结果分布与固定政策机制分解现记录自身脚本、服务商价格展开、联合市场、需求分配和利润实现的 SHA-256。新增测试先以 `2 failed, 5 passed` 失败，实现后为 `7 passed`，Ruff 为 `All checks passed!`。
- 敏感性入口追踪：每个重求场景和总摘要现额外记录 `run_submission_spatiotemporal_sensitivity.py` 的 SHA-256。新增测试先以 `1 failed, 3 passed` 失败，实现后为 `4 passed`，Ruff 为 `All checks passed!`。
- SMPT 官方格式复核（2026-07-14）：期刊 Guide for Authors（`https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors`）说明采用 single-anonymized review，标题页需作者、单位和通讯作者信息；摘要不超过 250 词，关键词 1--7 个，Highlights 为 3--5 条且每条不超过 85 个字符。当前 `Anonymous Author` 只能作为内部占位，正式投稿前必须由作者提供真实信息。
- 验收标准：有限候选博弈达到设定 regret 容差，且两家服务商的连续域 relative off-grid regret 均不高于 `0.5%`；未满足时继续扩展，不更新论文主结果。
- 下一步：先运行网格覆盖红灯测试，再实现第三轮候选网格和新的可追溯输出文件。
- 红灯测试：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    --with numpy --with scipy pytest \
    tests/test_peak_shaving_submission_tools.py::test_third_audit_grid_covers_mid_slope_interaction_region -q
  ```
  * 退出码为 `4`；测试收集阶段按预期因 `third_audit_enriched_provider_candidate_grid` 尚未实现而失败。
  * 默认求解入口与新输出名的两项红灯测试随后以 `2 failed`、退出码 `1` 失败，分别确认入口仍调用第二轮网格且正式文件名仍为 `provider2380`。
- 实现验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    --with numpy --with scipy --with nashpy pytest \
    tests/test_equilibrium_cache.py \
    tests/test_peak_shaving_submission_tools.py \
    tests/test_final_spatiotemporal_equilibrium.py -q
  uv run --no-project --with ruff ruff check \
    experiments/equilibrium_cache.py experiments/final_equilibrium_tools.py \
    experiments/peak_shaving_submission_tools.py \
    experiments/run_final_spatiotemporal_equilibrium.py \
    experiments/run_submission_spatiotemporal_equilibrium.py
  ```
  * 结果为 `22 passed`，Ruff 为 `All checks passed!`；第三轮网格含 `4,016` 个唯一策略。
- 状态：in_progress。

### 2026-07-14 09:34 - 终稿 claim--evidence 映射

- 目标：在实验重跑期间锁定终稿数字的来源、计算次序和允许的结论边界，避免 225 点旧结果进入新稿。
- 操作：新增 `docs/reviews/smpt_submission_evidence_map_2026-07-14.md`，逐项映射有限均衡、混合期望、离网审计、中间商审计、固定点审计、敏感性、机制分解和混合分布工件。
- 输出：已记录 719 候选、26×26 正概率混合剖面、36,712 个已评价策略对、当前主指标及待完成门禁；明确区分 $E[\max X]$ 与 $\max E[X]$。
- 结果：当前只把正式均衡工件中的字段标为已锁定；off-grid、follower globality、fixed-point 和 sensitivity 仍标为待完成，不进入论文结论。
- 决策：最终 TeX 将通过机器生成宏引用通过哈希门禁的正式工件，并删除 225 点网格、Nashpy 正式求解、纯策略和有限中间商响应等旧表述。
- 下一步：等待 B 方离网搜索完成；若 relative regret 接近 `0.5%` 门槛，将继续加入审计发现的偏差区域并使用独立随机种子复核。
- 状态：in_progress。

### 2026-07-14 10:13 - 论文数字质量门禁

- 目标：防止仅通过均衡 SHA-256 检查、但科学质量未达到预设阈值的审计工件进入 LaTeX 数字宏。
- 操作：为 `build_submission_result_macros.py` 增加 off-grid、intermediary globality 和 fixed-point multistart 三类质量检查。
- 红灯命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    pytest tests/test_submission_result_macros.py -q
  ```
  * 结果为 `3 failed, 4 passed`；现有生成器未拒绝超阈值审计。
- 实现阈值：relative off-grid regret `<=0.5%`；独立中间商搜索 relative gain `<=0.1%`；审计残差 `<=1e-8`；固定点 QoS/路由跨度 `<=1e-7`；固定点所有起点必须收敛。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    pytest tests/test_submission_result_macros.py -q
  uv run --no-project --with ruff ruff check \
    experiments/build_submission_result_macros.py \
    tests/test_submission_result_macros.py
  ```
- 结果：`7 passed`，Ruff 为 `All checks passed!`。
- 决策：正式宏只有在审计哈希和质量门禁同时通过时生成；缺失的可选审计仍不生成对应宏。
- 下一步：继续等待修正后 B 方离网搜索完成。
- 状态：verified。

### 2026-07-14 11:18 - 扩展响应空间终稿化续算

- 目标：继续完成修正后有限候选均衡的连续域偏离审计，并据此判断是否需要第四轮候选扩展；未锁定最终均衡前不更新论文主结果。
- 环境：当前项目位于 WSL 原生路径 `/root/paper_code/0427_tokenrl/paper_token_cross_survey`；`uv 0.10.9`、WSL Python `3.12.13` 和 Git `2.34.1` 均来自 Linux 工具链。
- 检查命令：
  ```bash
  cat /tmp/peak_shaving_submission_offgrid.exit 2>/dev/null || true
  ps -eo pid,ppid,stat,etime,pcpu,pmem,cmd | \
    rg 'run_spatiotemporal_offgrid_diagnostic|peak_shaving_submission_offgrid'
  tail -30 \
    artifacts/peak_shaving/20260712_expanded_response/submission_offgrid_interior_seed_detached.log
  ```
- 结果：PID `298786` 的独立审计进程仍正常运行；服务商 A 已完成 1,031 个全局候选和 177 个局部候选，服务商 B 已完成 1,023 个全局候选，正在计算局部成对细化。16 个单线程 worker 持续占用 CPU，退出码文件和正式 JSON 尚未生成。
- 决策：保持当前均衡源码和哈希链不变。正式 JSON 写出后检查两方 relative off-grid regret、最佳偏离向量、固定点收敛、残差和局部搜索成功次数；若结果接近预设 `0.5%` 门槛，则把审计发现的局部区域加入候选集并使用独立随机种子复核。
- 下一步：等待 B 方局部细化完成并解析正式工件。
- 状态：in_progress。

### 2026-07-14 11:34 - 第三轮候选集离网审计结论

- 实际命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy --with scipy \
    python -m experiments.run_spatiotemporal_offgrid_diagnostic
  ```
- 输出：`spatiotemporal_offgrid_diagnostic_submission.json`，SHA-256 为 `8b4ffa3bd5057988f548b3282eb3f2e1df39ef8432b1611d1159f747d2ba3f8b`；记录的均衡 SHA-256 与当前 `b00a61...` 工件一致，独立进程退出码为 `0`。
- 服务商 A：评估 1,208 个候选和 31,408 个策略对；最佳偏离为 `(0.25, 0.25, 0.5278125, 0.2)`，absolute regret 为 `4.07366`，relative regret 为 `0.486760%`。
- 服务商 B：评估 1,197 个候选和 31,122 个策略对；最佳偏离为 `(0.25, 1.05, 0.5278125, 0.4)`，absolute regret 为 `1.96053`，relative regret 为 `0.264526%`。
- 数值质量：两方所有联合固定点均收敛，最大残差低于 `1.0e-9`；活跃支持收益重构误差低于 `6e-13`；每个策略对至少有 2 个成功的中间商局部优化起点。
- 判断：结果形式上通过预设 `0.5%` 门槛，但 A 方仅留约 `0.0132` 个百分点余量，且最佳偏离来自候选集之外的局部 refinement。将其直接表述为稳定的有限策略近似证据并不稳妥。
- 决策：进入第四轮审计自适应扩展，把 A/B 最佳偏离及其局部邻域加入候选集，重求完整有限博弈；最终 off-grid 复核使用不同随机种子，避免把同一采样设计当作独立证据。
- 状态：verified，触发 candidate expansion。

### 2026-07-14 11:40 - 第四轮候选扩展与来源追踪

- 归档：第三轮正式均衡、离网审计和运行日志分别复制为 `*_pre_fourth_grid.json` / `*_pre_fourth_grid.log`；均衡和离网工件 SHA-256 仍分别为 `b00a61...` 与 `8b4ffa...`，未删除或覆盖旧证据。
- 红灯测试：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest --with numpy \
    pytest tests/test_peak_shaving_submission_tools.py::\
test_adaptive_audit_grid_covers_fourth_audit_deviation_neighbourhoods -q
  ```
  * 结果为 `1 failed`；719 点集合缺少最新 A/B 离网最佳偏离及其邻点。
- 实现：在线性价格形状不变的前提下，增加 A 方低斜率邻域和 B 方中高斜率邻域；审计中心显式记录为 `(0.25, 0.25, 0.5278125, 0.2)` 与 `(0.25, 1.05, 0.5278125, 0.4)`。以当前 52 个正概率支持向量构建时，候选数从 719 增至 788。
- 可复现性：均衡元数据现覆盖模型配置、市场/固定点、中间商响应、缓存、有限博弈、互补条件和 HiGHS MILP 求解实现的完整源码 SHA-256，并记录 NumPy、SciPy 与 Nashpy 版本。`candidate_design` 同时记录第四轮方法、两个审计中心、参考支持数和最终候选数。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    --with numpy --with scipy --with nashpy pytest \
    tests/test_equilibrium_cache.py tests/test_peak_shaving_submission_tools.py \
    tests/test_final_spatiotemporal_equilibrium.py -q
  uv run --no-project --with ruff ruff check \
    experiments/peak_shaving_submission_tools.py \
    experiments/final_reproducibility.py \
    experiments/run_submission_spatiotemporal_equilibrium.py \
    tests/test_peak_shaving_submission_tools.py \
    tests/test_final_spatiotemporal_equilibrium.py
  ```
- 结果：`25 passed`；Ruff 为 `All checks passed!`。
- 下一步：复用语义未变的 36,712 个策略对缓存，完整扫描 788 个候选并重求有限混合均衡。
- 状态：verified，ready_to_resolve。

### 2026-07-14 12:23 - 第四轮有限候选均衡

- 实际命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with numpy --with scipy --with nashpy \
    python -m experiments.run_submission_spatiotemporal_equilibrium
  ```
- 输出：`spatiotemporal_equilibrium_submission.json`，SHA-256 为 `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`；独立进程退出码为 `0`。
- 求解过程：从第三轮 26×26 正概率支持开始，788 点完整偏离扫描在第 1 轮复现 A 方约 `0.4868%` 的偏离收益；随后扩展受限支持并重算。第 6 轮 full-grid absolute regret 降至 `1.14e-13`，relative regret 为 `1.36e-16`，终止原因为 `regret_tolerance`。
- 计算规模：动态博弈最终评价 46,381 个唯一策略对；受限集合含 29 个 A 方和 31 个 B 方策略，其中最终正概率支持仍为 26×26，共 676 个活跃混合剖面。统一定价限制含 12 个候选。
- 主结果：剖面级期望峰值从 `224.5689` 降至 `196.9028`（`-12.3196%`）；剖面级期望最大利用率从 `1.45048` 降至 `1.22278`（`-15.6985%`）；剖面级期望最低 QoS 从 `0.889917` 提高至 `0.958589`；市场侧总利润从 `1978.4907` 降至 `1922.9347`（`-2.8080%`）。
- 来源复核：工件记录 20 个源码/输入 SHA-256，逐项与当前文件一致；记录环境为 Python `3.12.13`、NumPy `2.4.4`、SciPy `1.17.1`、Nashpy `0.0.43`。
- 判断：该工件通过声明有限候选集内的完整 regret 验证，但仍不能替代连续策略空间检验；论文数字继续保持冻结，等待独立种子 off-grid 审计。
- 状态：verified finite-game result。

### 2026-07-14 12:25 - 最终离网复核配置

- 目标：用不同于第三轮的随机设计复核 788 点有限均衡，降低单次 Latin-hypercube 样本偶然遗漏有利偏离的风险。
- 红灯：新增测试要求每家默认 1,024 个 Latin-hypercube 样本、随机种子 `20260714` 和独立缓存目录；实现前因常量不存在而 `1 failed`。
- 实现：`run_spatiotemporal_offgrid_diagnostic.py` 的正式默认值改为 1,024 点、种子 `20260714`，缓存目录改为 `/tmp/peak_shaving_submission_offgrid_fourth_grid/`；搜索域和局部 refinement 设计不变。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    --with numpy --with scipy pytest tests/test_final_offgrid_diagnostic.py -q
  uv run --no-project --with ruff ruff check \
    experiments/offgrid_diagnostic_tools.py \
    experiments/run_spatiotemporal_offgrid_diagnostic.py \
    tests/test_final_offgrid_diagnostic.py
  ```
- 结果：`5 passed`；Ruff 为 `All checks passed!`。
- 下一步：启动独立缓存的最终连续域偏离审计；两方 relative regret 仍以 `0.5%` 为正式门禁，并同时检查固定点收敛、残差和活跃支持收益重构误差。
- 状态：verified，ready_to_audit。

### 2026-07-14 12:38 - SMPT 英文终稿结构与方法重写

- 目标：在最终审计运行期间建立当天英文终稿，删除旧 225 点、纯策略和有限中间商响应叙述；保持五个编号章节。
- 输出：新建 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex`，未覆盖 7 月 12 日稿。
- 结构：保留 Introduction、Related research、Methodology、Experimental results、Conclusion and outlook 五个编号章节；声明和数据可用性使用非编号标题。
- 理论改动：补充两阶段随机效用解释、OD 质量守恒、联合路由--QoS 固定点、三类线性价格形状、利润与批发转移守恒、混合结果期望口径、纳什最优响应条件、Fischer--Burmeister 互补方程、完整候选 regret 和有界离网搜索域。
- 方法改动：明确服务商价格函数是线性的，离散对象是四个价格系数；最终集合为 788 个审计自适应候选。中间商在 `[0.45,2.10]×[-1,1]×[0,10^6]` 内连续多起点优化，不再描述为有限网格。
- 结果改动：主表更新到 `d3717445...` 均衡；峰值、利用率和 QoS 明确采用剖面级极值的期望，并与期望曲线的极值区分。旧机制分解和旧敏感性数字已从新稿删除，保留工件通过后插入标记。
- 语言处理：按 `nature-polishing` 的 research/full-paper/English/generic 路由重组段落，再按 `humanizer` 规则减少模板化贡献排比、夸张词、连续转折和不必要术语。技能清单引用的共享 `_shared` 四个核心文件在本机技能目录中缺失，已使用可读取的本地核心与各章节规则，没有假装加载缺失文件。
- 编译命令：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：退出码 `0`，生成 15 页 A4 PDF；无 undefined citation/reference 和 LaTeX Error。候选集表格出现 `0.697 pt` overfull，已将该表局部字号降为 `\footnotesize`，等待下一次编译复核。当前结果图仍来自旧工件，所以该 PDF 只用于中间排版检查，不是可投稿版本。
- 离网审计状态：独立种子正式运行已启动，PID `1174681`；每家 1,024 个 LHS 样本，A 方候选总数为 1,544，正在运行。
- 下一步：等待 off-grid 门禁；随后依次完成全剖面 follower/fixed-point 审计、机制分解、敏感性、终稿图和最终语言审查。
- 状态：in_progress。

### 2026-07-14 12:45 - 终稿框架图更新与导出

- 目标：使论文框架图与 788 候选有限混合均衡、连续中间商响应和独立 off-grid 审计一致，并生成可编辑与投稿用格式。
- TDD：先将 `tests/test_final_framework_drawio.py` 更新为当天路径，并要求图中包含 `Audit-adaptive linear`、`Bounded continuous`、`Complementarity mixed equilibrium`、`Full 788-candidate regret` 与 `Bounded off-grid search`；生成前测试因新 Draw.io 文件不存在而失败。
- 实现：更新 `figure_sources/build_final_spatiotemporal_framework_drawio.py`，生成 `figure_sources/spatiotemporal_pricing_framework_final_2026-07-14.drawio`。市场层保持需求时移、渠道选择、中间商路由、服务商容量与 QoS 的因果顺序；求解层改为审计自适应线性价格候选、联合路由--QoS 固定点、连续中间商响应、互补条件混合均衡、完整候选 regret 和有界离网搜索。
- 结构校验：
  ```bash
  uv run --no-project python \
    /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figure_sources/spatiotemporal_pricing_framework_final_2026-07-14.drawio --strict
  ```
  * 结果：`0 error(s), 0 warning(s)`。
- 导出命令：
  ```bash
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    -x -f png -e --width 3200 --border 12 \
    -o figures/peak_shaving_final_20260714/spatiotemporal_pricing_framework.png \
    figure_sources/spatiotemporal_pricing_framework_final_2026-07-14.drawio \
    --disable-update --no-sandbox
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    -x -f svg -e --embed-svg-images --border 12 \
    -o figures/peak_shaving_final_20260714/spatiotemporal_pricing_framework.svg \
    figure_sources/spatiotemporal_pricing_framework_final_2026-07-14.drawio \
    --disable-update --no-sandbox
  xvfb-run -a /tmp/drawio-portable-30.3.6/opt/drawio/drawio \
    -x -f pdf -e --border 12 \
    -o figures/peak_shaving_final_20260714/spatiotemporal_pricing_framework.pdf \
    figure_sources/spatiotemporal_pricing_framework_final_2026-07-14.drawio \
    --disable-update --no-sandbox
  ```
- 验证：PNG 为 `3200×1921` RGB；SVG 可解析；PDF 为单页。全分辨率视觉检查未发现图标丢失、文字裁切、公式重叠或斜向流程箭头。第一次 pytest 因其临时捕获文件被清理而异常退出，关闭捕获后复核：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    pytest -s tests/test_final_framework_drawio.py -q
  uv run --no-project --with ruff ruff check \
    figure_sources/build_final_spatiotemporal_framework_drawio.py \
    tests/test_final_framework_drawio.py
  ```
  * 结果：`5 passed`；Ruff 为 `All checks passed!`。
- 论文接入：当天英文稿的图 1 已显式引用新 PDF；旧定量结果图暂未切换，等待最终审计和重建图表后统一更新 `graphicspath`。
- PDF 兼容性：Draw.io 初始导出为 PDF 1.7，`xdvipdfmx` 在嵌入第 4 页时报告目标 PDF 1.5 不兼容并退出。保留 `/tmp/spatiotemporal_pricing_framework_pdf17.pdf` 后执行：
  ```bash
  gs -sDEVICE=pdfwrite -dCompatibilityLevel=1.5 -dPDFSETTINGS=/prepress \
    -dNOPAUSE -dQUIET -dBATCH \
    -sOutputFile=figures/peak_shaving_final_20260714/spatiotemporal_pricing_framework.pdf \
    /tmp/spatiotemporal_pricing_framework_pdf17.pdf
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
  * 结果：图文件为 PDF 1.5；论文编译退出码 `0`，15 页 PDF 已更新。第 4 页渲染抽检未发现图文遮挡、裁切或比例异常；日志无 overfull box、undefined citation/reference 或 LaTeX Error。
- 状态：verified framework figure and TeX integration；quantitative figures in_progress。

### 2026-07-14 12:48 - 全活跃剖面固定点多起点审计启动

- 目标：对 788 候选混合均衡中的全部 676 个正概率动态剖面进行独立初始化复核，判断联合路由--QoS 固定点是否对初值敏感。
- 设计：每个剖面使用 32 组独立随机 QoS 与路由初值；要求全部起点收敛、最大残差不高于 `1e-8`，并检查 QoS 与路由终点跨度是否不高于 `1e-7`。默认 `maximum_profiles=1000`、`minimum_coverage=1.0`，因此覆盖全部概率质量。
- 预检查：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy pytest -s \
    tests/test_submission_fixed_point_audit.py -q
  uv run --no-project --with ruff ruff check \
    experiments/run_submission_fixed_point_audit.py \
    tests/test_submission_fixed_point_audit.py
  ```
  * 结果：`5 passed`；Ruff 为 `All checks passed!`。
- 正式命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy \
    python -m experiments.run_submission_fixed_point_audit
  ```
- 第一次启动：曾以默认 16 个工作进程后台启动，shell PID 为 `1244808`。进程在环境初始化后消失，未留下退出码，日志只有 uv 环境提示，正式 JSON 时间戳未变化；该次运行判定为失败。系统当时 4 GiB swap 已使用 3.9 GiB，故不在并行 off-grid 审计期间再次扩展进程数。
- 重启命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy python -c \
    'import json; from experiments.run_submission_fixed_point_audit import \
    OUTPUT_PATH, run_audit; result = run_audit(parallel_workers=1); \
    result["metadata"]["execution_override"] = \
    "parallel_workers=1 due concurrent off-grid audit"; \
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")'
  ```
- 运行状态：单工作进程复核已在受管终端会话中完成。该配置只改变任务调度，不改变起点、固定点迭代、容差或结果定义。
- 结果：输出 SHA-256 为 `cd4122f2c2523a451900357a9f0ede9bfde9dba7f3ee07b0f4e342d7c7421dd0`，记录的均衡 SHA-256 与 `d3717445...` 一致。共审计 676 个剖面，覆盖概率质量 `1.0000000000000002`；全部 21,632 个起点收敛。最大残差为 `9.99955e-10`，最大 QoS 跨度为 `9.70091e-10`，最大路由跨度为 `2.06860e-9`。
- 判断：通过 `1e-8` 残差与 `1e-7` 终点跨度门禁。该结果支持“在已审计活跃剖面与 32 个随机初值下未发现多固定点”，但仍不是解析唯一性证明。
- 状态：verified。

### 2026-07-14 12:57 - 终稿图表来源门禁与全覆盖要求

- 目标：禁止当天定量图和 LaTeX 结果宏混入旧 225 点或旧均衡的派生工件，并要求 follower/固定点审计覆盖全部混合概率质量。
- 图表红灯：新增测试要求输出目录为 `peak_shaving_final_20260714`、均衡为 `spatiotemporal_equilibrium_submission.json`，并要求每个依赖工件记录的 equilibrium/baseline SHA-256 与当前均衡文件一致。实现前因仍指向 `20260712_final` 且缺少来源校验而 `2 failed`。
- 图表实现：`build_final_submission_figures.py` 现读取 788 候选均衡及 submission 后缀的 distribution、mechanism、sensitivity、off-grid、fixed-point 和 intermediary 工件。任何来源哈希不一致都会停止生成。利润图标签统一为 `Market-side profit`；求解诊断预留有限候选 regret、相对 off-grid regret 及固定点/follower 门禁比值三个面板。文件保持 300 行。
- 图表定向验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with matplotlib --with numpy pytest -s \
    tests/test_final_submission_figures.py::\
test_submission_figure_paths_do_not_use_legacy_final_directory \
    tests/test_final_submission_figures.py::\
test_dependent_artifact_must_match_current_equilibrium_hash -q
  uv run --no-project --with ruff ruff check \
    experiments/build_final_submission_figures.py \
    tests/test_final_submission_figures.py
  ```
  * 结果：`2 passed`；Ruff 为 `All checks passed!`。完整图生成测试等待 final off-grid、固定点、follower、机制和敏感性工件齐备后执行。
- 结果宏红灯：新增参数化测试，将 follower 或固定点覆盖率设为 `0.999`；旧门禁未拒绝，结果为 `2 failed`。
- 结果宏实现：新增 `MIN_ACTIVE_PROFILE_COVERAGE=1-1e-9`。`build_submission_result_macros.py` 现在除数值误差门禁外，还拒绝未覆盖全部活跃混合概率质量的 follower 和固定点审计。
- 结果宏验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    pytest -s tests/test_submission_result_macros.py -q
  uv run --no-project --with ruff ruff check \
    experiments/build_submission_result_macros.py \
    tests/test_submission_result_macros.py
  ```
  * 结果：`9 passed`；Ruff 为 `All checks passed!`。
- 决策：最终 TeX 的关键结果将由通过全部来源和质量门禁后的 `submission_result_macros.tex` 提供；当前手工数字仅作为运行中稿，不作为最终来源。
- 状态：verified provenance and coverage gates；full figure build pending。

### 2026-07-14 13:10 - 机制分解修正、混合分布与 follower 审计

- 机制问题：旧分解在 `spatial_enabled=False` 时只固定用户渠道份额，中间商仍按价格和 QoS 动态路由，因此 `neither` 和 `temporal_only` 并未真正关闭服务商间空间响应。
- TDD：先新增测试，要求关闭空间响应后中间商路由严格等于两家服务商固定容量占比；实现前因缺少固定路由求解入口而 `1 failed`。随后新增 uniform/dynamic 按机制配对测试；实现前因缺少 `_policy_comparisons` 而 `1 failed`。
- 修正：仅修改 submission 机制分解，不改变主均衡代码。空间响应关闭时，用户渠道份额固定为 `(0.12,0.50,0.38)`，中间商路由固定为容量占比 `(0.7143,0.2857)`，再求 QoS 固定点；空间响应开启时仍联合求路由与 QoS。输出新增每种机制下 dynamic minus uniform 的政策对比。
- 验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy pytest -s \
    tests/test_submission_mechanism_decomposition.py \
    tests/test_spatiotemporal_mechanism.py \
    tests/test_spatiotemporal_game.py -q
  uv run --no-project --with ruff ruff check \
    experiments/run_submission_mechanism_decomposition.py \
    tests/test_submission_mechanism_decomposition.py
  uv run --no-project --with numpy \
    python -m experiments.run_submission_mechanism_decomposition
  ```
  * 结果：相关回归测试 `12 passed`，新增分解测试单独复核为 `5 passed`；Ruff 通过；8 个分解行全部收敛。最终工件 SHA-256 为 `785cefa88ef0c74fb9bcc0c036eabd61bb6a8d454e78cab47a22672bb57ab265`，均衡来源哈希匹配。
- 机制结果：temporal-only 的峰值/最大利用率变化为 `-13.0305%/-13.0305%`，最低 QoS 变化为 `+0.04077`；spatial-only 为约 `0%/-9.6244%/+0.04359`；combined 为 `-12.3196%/-15.6985%/+0.06867`。但相对容量比例固定路由，combined 的最大利用率和最低 QoS 不如 temporal-only，说明内生空间替代仍向小服务商分配了过多流量。
- 写作决策：标题与正文中的 `provider balancing` 改为中性的 `provider substitution`。正文同时报告“动态相对统一定价的空间改善”和“相对容量比例控制仍存在失衡”，不再把空间响应单向描述为 QoS 改善机制。
- 混合分布：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with numpy \
    python -m experiments.build_submission_mixed_distribution
  ```
  * 输出 SHA-256 为 `404e0a39c047354fcc908756b8aa3579ee9d24e8eac46e4ea262451062c2182a`；676 个剖面概率和为 1，期望指标最大重构误差为 `6.82e-13`。这些分位数描述混合策略结果分布，不是置信区间。
- 图表：使用当天均衡重建 `input_calibration`、`equilibrium_profiles` 和 `mechanism_decomposition` 的 PDF/PNG。曲线图的每个面板均有独立图例，图例位于折线上方；面板说明位于横轴标题下方且无重叠。框架图相应改为 `spatial provider substitution`，Draw.io 严格校验 `0 error(s), 0 warning(s)`，测试 `5 passed`。
- follower 审计预检查：`tests/test_submission_intermediary_audit.py` 为 `9 passed`，Ruff 通过。正式全覆盖审计已用 8 个工作进程启动，每个活跃剖面使用 SciPy differential evolution 与 polishing；门禁为最大相对利润改进不高于 `0.1%` 且最大固定点残差不高于 `1e-8`。
- 状态：mechanism/distribution/figures verified；intermediary audit in_progress。

### 2026-07-14 13:16 - 混合结果分布入稿与文献元数据复核

- 目标：让读者看到混合均衡下结果的离散程度，并复核当天修改后的参考文献与 PDF 版面。
- 论文修改：在 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 中新增活跃策略对结果分布表。表内给出聚合峰值、最大服务商利用率、最低 QoS 和市场侧合计利润的加权第 5、50、95 百分位；正文明确这些分位数描述 676 个正概率策略对上的均衡随机化，不是统计置信区间。最低活跃剖面 QoS 为 `0.893`，略高于统一定价均衡的 `0.890`。
- 求解图处理：旧 `solver_diagnostics` 图仍包含早期三轮轨迹和旧离网格数据，已从当天 TeX 中移除。只有最终 off-grid 与中间商全局性审计通过并重建图后才会重新插入，避免图文来源不一致。
- 文献核验：依据 AAAI 官方论文页，将 PriLLM 条目标题修正为正式标题 `Pricing Online LLM Services with Data-Calibrated Stackelberg Routing Game`；依据 NBER 官方页面补充工作论文 DOI `10.3386/w34608`。未改变正文引用标记或参考文献样式。
- 编译命令：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 `0`，BibTeX 与 XeLaTeX 自动完成，生成 15 页 A4、PDF 1.5 文件。日志无 overfull box、undefined citation/reference 或 LaTeX Error；只保留候选集表格和一处正文的 underfull hbox 提示。
- 视觉抽检：将第 9--12 页以 130 dpi 渲染后检查。表 5、图 2--4 无文字裁切、图例遮挡或面板标签重叠。第 4.5 节目前仅有敏感性设计说明，尚无最终结果，须等待全量重求解后补入。
- 决策：当前 PDF 是已验证的运行中稿，不是投稿终稿；敏感性、off-grid 和中间商全局性门禁仍未完成。
- 状态：verified manuscript build；numerical audits in_progress。

### 2026-07-14 13:20 - 敏感性全量重求解的并行与恢复门禁

- 目标：在不改变八个敏感性场景和求解定义的前提下，使全量重求解能够分批运行，并防止恢复时混入其他均衡版本的场景工件。
- 红灯测试：新增测试要求 `run_sensitivity` 将显式工作进程数传给 `run_equilibria`，并要求汇总函数拒绝 baseline SHA-256 不匹配的单场景文件。实现前分别因缺少 `output_dir/parallel_workers` 参数和 `collect_sensitivity_summary` 而失败，结果为 `2 failed`。
- 实现：`run_submission_spatiotemporal_sensitivity.py` 新增场景级 `parallel_workers` 与 `output_dir` 参数；新增经 baseline SHA-256 校验的 `collect_sensitivity_summary`。每个场景仍使用同一 788 候选集、连续中间商响应和最多 100 轮 oracle，只改变任务调度与工件汇总方式。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy --with scipy --with nashpy \
    pytest -s tests/test_submission_spatiotemporal_sensitivity.py -q
  uv run --no-project --with ruff ruff check \
    experiments/run_submission_spatiotemporal_sensitivity.py \
    tests/test_submission_spatiotemporal_sensitivity.py
  ```
- 结果：`6 passed`；Ruff 为 `All checks passed!`。运行器为 266 行，未超过项目文件长度门禁。
- 决策：当前 off-grid 使用 16 个工作进程，中间商审计使用 8 个工作进程，且 swap 仅剩约 75 MiB；因此不同时启动敏感性正式运行。待两项审计结束后按场景分批运行，并从通过哈希校验的单场景文件生成最终摘要。
- 状态：verified runner；full sensitivity run pending resources。

### 2026-07-14 13:28 - 敏感性构图字段与 vLLM 误差条修正

- 目标：在最终敏感性工件生成前验证图表字段契约，并使五次重复的 QoS 误差条与论文中的统计名称一致。
- 敏感性图红灯：`_summary_row` 输出 `maximum_provider_utilization_change_percent` 和 `minimum_provider_qos_change`，而 `_resolved_sensitivity` 读取不存在的缩写字段。新增真实字段名回归测试后，旧实现以 `KeyError: 'max_provider_utilization_change_percent'` 失败。
- 敏感性图修正：图 5 构建器改为读取汇总工件的正式字段名。该修改只修正图表接口，不改变场景、指标或均衡计算。
- QoS 误差条红灯：原始聚合文件使用 `1.96 × standard error`，但每个并发水平只有 5 次重复。新增测试要求最终图将该半宽换算为自由度 4 的 Student-$t$ 半宽，旧实现因缺少换算常量而失败。
- QoS 图修正：最终构图阶段使用比例 `2.7764451051977987 / 1.96` 换算误差条。均值、归一化利用率、QoS 曲线拟合参数和均衡输入均未改变，因此无需重算主均衡。英文方法部分已补充 `$t_{0.975,4}=2.776$`，图 2 题注改为 `Student-t 95% confidence intervals`。
- 生成命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with matplotlib --with numpy python -c \
    'from experiments.build_final_submission_figures import BURST, \
    CALIBRATION_ARTIFACT, FIGURE_DIR, _input_calibration, _read_csv, \
    _read_json; data={"burst_profile": _read_csv(BURST / \
    "burstgpt_8period_load_profile.csv"), "qos_calibration": \
    _read_json(CALIBRATION_ARTIFACT / "qos_calibration.json")}; \
    _input_calibration(data, FIGURE_DIR)'
  ```
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with matplotlib --with numpy pytest -s \
    tests/test_final_submission_figures.py::\
test_sensitivity_figure_accepts_submission_summary_field_names \
    tests/test_final_submission_figures.py::\
test_qos_error_bars_convert_five_repeat_normal_intervals_to_student_t -q
  uv run --no-project --with ruff ruff check \
    experiments/build_final_submission_figures.py \
    tests/test_final_submission_figures.py
  ```
- 结果：`2 passed`；Ruff 为 `All checks passed!`；图构建器保持 300 行。重建 PNG 为 `2592×990`，PDF 为单页 1.4。全分辨率抽检未发现误差条、图例、曲线或面板标签遮挡。
- 状态：verified。

### 2026-07-14 13:32 - 全活跃剖面中间商全局性审计

- 目标：用独立随机全局优化器复核主均衡中连续中间商响应，覆盖全部正概率服务商策略对。
- 正式命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with numpy --with scipy python -c \
    'import json; from experiments.run_submission_intermediary_audit import \
    OUTPUT_PATH, run_audit; result = run_audit(parallel_workers=8); \
    result["metadata"]["execution_override"] = \
    "parallel_workers=8 during concurrent off-grid audit"; \
    OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8")'
  ```
- 来源验证：工件 SHA-256 为 `140dac3c76871eaf175c07c623af46c500c8b5fdd17f763f60cadc1dfcd30fa9`；记录和实际均衡 SHA-256 均为 `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`。
- 覆盖：676 个正概率剖面全部复核，覆盖概率质量 `1.0000000000000002`。每个剖面使用 SciPy differential evolution，`maxiter=35`、`popsize=8`，随后进行局部 polishing。
- 结果：最大绝对利润改进为 `0.1026781`，最大相对改进为 `0.0002916833`，低于预设 `0.001` 门禁。最大联合固定点残差为 `9.99968e-10`，低于 `1e-8` 门禁。最差剖面权重为 `0.0001867`。
- 优化器状态：381/676 个运行满足差分进化停止判据；295 个达到迭代上限。后者相对存储解的最大改进仅 `3.1551e-10`，没有实质性遗漏。所有 676 个候选利润均为有限值，且没有剖面超过 `0.1%` 改进门禁。
- 论文更新：数值均衡检查加入覆盖率、最大相对改进、残差和迭代上限说明；明确该结果是全活跃剖面数值复核，不是解析全局最优证明。
- 决策：当前中间商响应通过投稿门禁。最终 solver diagnostics 可使用 `0.0292%` follower 改进值；仍需等待独立 provider off-grid 审计。
- 状态：verified。

### 2026-07-14 13:35 - GitHub 可用性声明与第一批敏感性启动

- 目标：核对论文 Data and code availability 与远端仓库的真实状态，并在资源释放后启动全量敏感性重求解。
- GitHub 检查：
  ```bash
  gh auth status
  git ls-remote --heads origin
  gh repo view cccht/paper_token_price \
    --json nameWithOwner,isPrivate,url,defaultBranchRef,pushedAt
  git ls-tree -r --name-only origin/main
  ```
- GitHub 结果：`gh` 已以 `cccht` 登录；远端为公开仓库 `https://github.com/cccht/paper_token_price`，默认分支 `main`。远端和本地 HEAD 均为 `0941d97af4afa33a0b150a77bfada33ef779c9ed`，但 7 月 14 日文件尚未提交，远端树中没有 `20260712_expanded_response`、`peak_shaving_final_20260714` 或当天 TeX。第一次 `gh repo view` 使用本机旧版不支持的 `visibility` 字段而失败，改用 `isPrivate` 后成功。
- 决策：当前论文中的公开仓库地址有效，但“最终机器可读工件已经公开”尚未成立。投稿前须审查 diff、仅暂存本任务文件、提交并推送，再保留最终 Data and code availability 表述；在此之前不宣称终稿已公开归档。
- 第一批敏感性命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with numpy --with scipy --with nashpy python -c \
    'from experiments.run_submission_spatiotemporal_sensitivity import \
    run_sensitivity; run_sensitivity(scenario_names=["capacity_low"], \
    parallel_workers=4)'
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with numpy --with scipy --with nashpy python -c \
    'from experiments.run_submission_spatiotemporal_sensitivity import \
    run_sensitivity; run_sensitivity(scenario_names=["capacity_high"], \
    parallel_workers=4)'
  ```
- 资源设计：两个场景各使用 4 个工作进程，与仍在运行的 16 进程 off-grid 审计合计使用 24 个工作核心；每个场景使用独立缓存目录和独立 JSON 输出，不共享可写文件。
- 运行状态：`capacity_low` 与 `capacity_high` 均已启动。`capacity_low` 的 95 个统一定价策略对已完成，动态博弈待继续；`capacity_high` 正在运行。
- 稿件复编译：中间商审计段落和 Student-$t$ 图注加入后执行 `latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex`，退出码 `0`，当前 PDF 为 16 页；日志无 overfull box、undefined citation/reference 或 LaTeX Error。
- 状态：GitHub availability audited；sensitivity wave 1 in_progress。

### 2026-07-14 13:43 - 定价规则、模型代码对应与主稿复编译

- 目标：消除“线性价格”与价格边界截断之间的表述歧义，并逐式核对方法章节和正式求解代码。
- 候选集核对：最终工件中的 788 个系数向量产生 788 个不同的 16 期批发价与直连价组合，没有因截断形成重复的实际价格剖面。第四轮构造所用的前序均衡含 52 个正概率支持条目、48 个不同向量。固定的确定性格点并集包含 770 个向量，另有 18 个只由前序审计均衡延续得到的向量；从归档的 `spatiotemporal_equilibrium_submission_pre_fourth_grid.json` 重新构造后，与正式工件的 788×4 候选数组逐元素完全一致。最终 off-grid 审计通过后再将表 2 改成这一可枚举定义，避免在审计未结束时冻结错误的候选集说明。
- 术语修正：英文主稿和框架图将 `linear price shapes` 改为 `bounded linear price rules`。正文明确价格先按负载的线性函数生成，再由 `clip` 施加价格上下界，因此边界期可能出现平段。该表述与 `spatiotemporal_price_shapes` 的实现一致。
- 模型代码核对：检查 `spatiotemporal_mechanism.py`、`spatiotemporal_game.py`、`peak_shaving_market.py` 和 `run_final_spatiotemporal_equilibrium.py`。需求迁移、渠道 softmax、连续中间商响应、联合 QoS/路由固定点、批发内部转移和三方利润与式 (1)--(18) 一致。正文补充需求和容量是每期归一化平均率，`h=3` 将平均率换成利润核算中的期间总量。
- 固定点证据：主稿加入多起点审计结果。676 个正概率剖面各使用 32 个初值，共 21,632 次求解；全部收敛，最大残差为 `9.99955e-10`，不同初值所得 QoS 和路由的最大跨度分别为 `9.70091e-10` 和 `2.06860e-9`。正文明确这只说明未观察到多解，不构成唯一性证明。
- 框架图更新：重新生成并导出 `spatiotemporal_pricing_framework.pdf/png/svg`，将图内术语统一为 bounded linear price-rule competition。Draw.io 结构验证为 5 个测试通过，PDF 经 Ghostscript 转为 1.5，图形逻辑和公式未改变。
- 编译命令：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 `0`，生成 16 页 A4、PDF 1.5 文件；日志没有 LaTeX Error、undefined citation/reference 或 overfull box。候选集表格仍有 underfull hbox，待最终 off-grid 结果确定后与表格的精确定义一起处理。
- 状态：manuscript build verified；provider off-grid 与 sensitivity wave 1 in_progress。

### 2026-07-14 13:51 - 主结果图补充实际终端价格路径

- 目标：让读者从论文 PDF 直接看到价格信号，而不是只看到价格作用后的负载、利用率和 QoS。
- 红灯测试：新增 `test_equilibrium_figure_reports_uniform_and_dynamic_end_user_prices`，要求主结果图同时绘制统一/动态的 API 中间商价格和直连价格。实现前因缺少 `_plot_end_user_prices` 而失败，结果为 `1 failed`。
- 实现：图 3 从横向三面板改为 `2×2`。新增面板 (b) 绘制概率加权的实际终端价格路径；原利用率和 QoS 面板顺延为 (c)、(d)。统一定价下两个服务商的直连价格重合，因此用一条虚线表示。正文补充动态终端价格在第 2--3 期最低、第 6 期最高，并说明固定需求下的迁移由同一价格路径内的相对差异驱动。
- 代码结构：价格面板和 SCI 调色板放入现有 `plot_style.py`；`build_final_submission_figures.py` 保持 300 行，未新增独立构图模块。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with matplotlib --with numpy pytest -q \
    tests/test_final_submission_figures.py::\
test_equilibrium_figure_reports_uniform_and_dynamic_end_user_prices \
    tests/test_final_submission_figures.py::\
test_final_figures_use_one_restrained_sci_palette
  uv run --no-project --with ruff ruff check \
    experiments/plot_style.py experiments/build_final_submission_figures.py \
    tests/test_final_submission_figures.py
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：回归测试 `2 passed`，Ruff 为 `All checks passed!`，LaTeX 退出码 `0`。主稿仍为 16 页，日志没有 LaTeX Error、undefined citation/reference 或 overfull box。
- 视觉检查：新 PNG 为 `2592×2015`。独立图和 PDF 第 11 页均已检查，图例、曲线、坐标标签和 `(a)--(d)` 面板说明没有遮挡或裁切。
- 状态：verified。

### 2026-07-14 13:57 - SMPT 最新作者指南与求解可扩展性说明

- 目标：按期刊当前官方要求复核投稿结构，并补足应用型仿真论文的实现与可扩展性说明。
- 官方来源：检查 Elsevier/ScienceDirect 的 `Simulation Modelling Practice and Theory: Guide for Authors`（2026-07-14 访问）。期刊要求应用论文透明呈现模型开发、计算实现、数学/可扩展性问题和基于真实数据的 verification/validation；摘要不超过 250 词；关键词 1--7 个；Highlights 为 3--5 条且每条不超过 85 个字符；图稿须单独提交并在正文引用；研究数据须存入相关仓库并链接，无法共享时须说明原因。
- 审稿与作者信息：期刊采用 single-anonymized review，因此正式投稿主稿必须包含作者姓名、单位、通讯作者和联系方式。当前 `Anonymous Author` 只能作为内部占位符，作者信息仍为 `AUTHOR_INPUT_NEEDED`，未擅自填写。
- 图像政策：Elsevier 不允许用生成式 AI 创建或修改投稿图像。当天正式框架图是可编辑 Draw.io 矢量图并使用 CC BY 4.0 图标，没有使用生成式图像模型；主稿继续保留这一事实说明。
- AI 声明：章节标题改成官方建议的 `Declaration of generative AI and AI-assisted technologies in the manuscript preparation process`，正文改为官方责任句式，并如实列明 Codex 用于语言、内部检查、代码测试和 LaTeX 排版检查。
- 可扩展性：方法部分新增 double-oracle 完整偏离扫描的上界 `K(s_A+s_B)`，并说明签名缓存避免构造完整 `K^2` 收益矩阵。结果部分记录最终动态博弈只评估 `46,381/788^2=7.47%` 的有序策略对。
- 运行时间来源：最终续算日志创建于 `2026-07-14 11:38:33.214825 +08:00`，完成于 `12:21:19.367023 +08:00`。该次 16 进程运行从签名缓存加载 36,712 对，新计算 9,669 对，wall time 为 `2566.15 s`（42.8 min）。论文明确这是续算时间，不是从零运行时间，也不包含独立 off-grid 与固定点审计。
- 英语一致性：图 2 横轴从 `Normalized concurrency` 改为 `Normalised concurrency`，与正文采用的 British English 一致；重建图 2 后 Ruff 通过。
- 编译验证：执行 `latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex`，退出码 `0`，生成 17 页、PDF 1.5 文件。日志没有 LaTeX Error、undefined citation/reference 或 overfull box；仍只有待重写候选集表和一处公式行的 underfull 提示。
- 整稿视觉检查：将 17 页 PDF 以 70 dpi 全页渲染并生成三列联系表。未发现空白页、图表断裂、孤立标题、文字裁切或图例遮挡。第 4.5 节仍只有敏感性设计和结果占位，是当前唯一明显的未完成版面；不使用旧敏感性数据填充。
- 决策：最终提交前还必须提供真实作者信息，并将当天最终代码和工件推送到公开仓库；最好再创建带 DOI 的长期数据版本。未完成这些条件前不宣称投稿包完整。
- 状态：guide audited；manuscript updated；author metadata and persistent data release pending。

### 2026-07-14 14:03 - 模型单位、随机性与语言边界复核

- 目标：消除归一化模型中容易被误读为真实 GPU 数量或美元利润的量纲歧义，并说明随机效用的实际计算方式。
- 单位修正：方法部分明确需求和容量是每期平均服务率，`G_A=180`、`G_B=72` 是服务率单位，不是物理 GPU 数量；`h=3` 只在利润核算时将平均率转成期间总量。价格、容量成本、退化成本和利润均为归一化货币单位，不对应美元或其他真实货币。主结果表和混合分布表的题注同步标明利润单位。
- 离散选择尺度：两个 type-I extreme-value 随机效用项的尺度归一化为 1，因此价格敏感度 `alpha` 和迁移成本 `kappa` 都相对于该效用尺度解释。该设定与代码中的标准 softmax 一致。
- 随机性说明：用户与时段选择直接计算 logit 概率，没有对个体用户或效用冲击做 Monte Carlo 抽样。给定策略和求解设置，市场状态是确定的；随机种子只用于 off-grid Latin-hypercube 和多起点数值审计。
- 语言处理：将两处超过 30 词的技术句拆分，删除未使用的 `assumption` 定理环境；数字、术语和证据强度不变。
- 编译命令：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：退出码 `0`，17 页、PDF 1.5；日志没有 LaTeX Error、undefined citation/reference 或 overfull box。
- 状态：verified。

### 2026-07-14 14:08 - 终稿证据映射更新到 788 候选基准

- 目标：清除 `smpt_submission_evidence_map_2026-07-14.md` 中仍指向上一轮 719 候选均衡的过期数字和审计状态。
- 更新：基准 SHA-256 改为 `d3717445...aae2f`；候选数、求解方法、46,381 个策略对、主结果、利润单位和 `788^2` 证据边界全部与当前正式均衡同步。
- 审计状态：中间商全局性与固定点多起点标为已验证，并写入 676 剖面覆盖、`0.0292%` 最大 follower 改进和 21,632 次多起点收敛。机制分解与混合结果分布标为已重建。最终 provider off-grid 和八个敏感性场景仍标为运行中。
- 验证：重新扫描证据映射文件，不再出现 `719`、旧 36,712 对、旧主结果或“待 676 个活跃剖面全量重跑”等过期文字。
- 状态：evidence map current；off-grid and sensitivity pending。
### 2026-07-14 14:11 - 最终均衡元数据路径审计

- 目标：核对扩大响应空间后的最终均衡工件及其下游审计是否具有可追溯的基线关系。
- 背景：独立 provider off-grid 审计与容量敏感性全量重求解正在运行，当前基线 SHA-256 为 `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`。
- 操作：只读检查 `spatiotemporal_equilibrium_submission.json`、`final_reproducibility.py`、`run_submission_spatiotemporal_sensitivity.py` 和缓存签名实现。
- 命令：
  ```bash
  sed -n '1,260p' experiments/final_reproducibility.py
  python - <<'PY'
  import json
  from pathlib import Path
  artifact = json.loads(Path('artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_equilibrium_submission.json').read_text())
  print(json.dumps(artifact['metadata'], indent=2))
  PY
  ```
- 输入：最终 788 候选均衡工件及当前求解代码。
- 输出：确认数值工件包含完整源码哈希和缓存签名；发现 `metadata.continuation_seed.path` 仍指向已被第四轮结果覆盖的主文件，而记录的 `b00a61...` SHA-256 对应保留的 pre-fourth 工件。
- 结果：这是元数据路径一致性问题，不影响已核对的均衡数值；若现在修改主工件，会改变正在运行审计所绑定的基线哈希。
- 决策：保持运行中基线不变。off-grid 和八个敏感性场景结束后，使用显式元数据迁移更新 continuation 路径，并同步所有下游工件的基线 SHA-256；迁移前后必须核对数值载荷不变。
- 下一步：继续监控三项运行；完成后先执行审计门禁，再处理元数据和稿件结果段。
- 状态：in_progress

### 2026-07-14 14:13 - 启动价格敏感度全量重求解

- 目标：并行推进八场景敏感性中的价格敏感度低值与高值场景，同时保持 off-grid 和容量场景运行。
- 背景：机器有 32 个逻辑处理器；原有 off-grid、`capacity_low`、`capacity_high` 合计使用 24 个 worker，检查时约有 8.0 GiB 可用内存。
- 操作：分别以 4 个 worker 启动 `price_sensitivity_low`（比例 0.8）和 `price_sensitivity_high`（比例 1.2）。每个场景使用独立签名缓存和独立 JSON 输出。
- 命令：
  ```bash
  /root/.local/bin/uv run --no-project --with numpy --with scipy --with nashpy python -c 'import json; from experiments.run_submission_spatiotemporal_sensitivity import run_sensitivity; result=run_sensitivity(scenario_names=["price_sensitivity_low"], parallel_workers=4); print(json.dumps(result["rows"], indent=2), flush=True)'
  /root/.local/bin/uv run --no-project --with numpy --with scipy --with nashpy python -c 'import json; from experiments.run_submission_spatiotemporal_sensitivity import run_sensitivity; result=run_sensitivity(scenario_names=["price_sensitivity_high"], parallel_workers=4); print(json.dumps(result["rows"], indent=2), flush=True)'
  ```
- 输入：当前 SHA-256 为 `d3717445...aae2f` 的 788 候选基线均衡、连续中间商响应和对应参数扰动。
- 输出：任务会写入 `/tmp/peak_shaving_submission_sensitivity/price_sensitivity_low/`、`price_sensitivity_high/`，完成后生成两个 `sensitivity_*_submission.json`。
- 结果：两项任务均已进入 uniform game 计算并写出首个 9-pair 缓存检查点；当前系统 load average 为 `29.08/25.67/24.44`，可用内存约 8.0 GiB，未发生异常退出。
- 决策：不再增加并行场景，保持总 worker 数约 32；待 off-grid 释放 16 个 worker 后再启动迁移成本和 QoS 阈值场景。
- 下一步：监控各缓存检查点与退出状态，逐场景执行 regret、固定点残差和基线哈希门禁。
- 状态：in_progress

### 2026-07-14 14:17 - 中间商策略类与数值精度边界修订

- 目标：避免把连续中间商搜索误写成任意时段响应，也避免用有限收益矩阵的极低 regret 掩盖 follower 数值误差。
- 操作：摘要和引言将中间商响应明确为连续优化的三参数价格与路由规则；方法部分说明该策略类不含逐时段独立零售价和路由份额；结果部分说明 `1.14e-13` regret 以存储收益矩阵为条件，实际精度由 follower 审计的 `0.0292%` 最大相对改进限定；局限段同步写入该参数化边界。
- 命令：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 输出：更新 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex/.pdf`。
- 结果：LaTeX 退出码 `0`，PDF 17 页、PDF 1.5；摘要 197 词，低于期刊 250 词上限。日志没有 LaTeX Error、undefined citation/reference 或 overfull box；候选集表和统一均衡公式行仍有 underfull 提示，待 off-grid 结果通过后随精确候选表一并处理。
- 决策：后续所有“continuous intermediary response”表述都限定为声明的三参数策略类；不把 follower 优化误差与 provider finite-game regret 混为同一精度指标。
- 下一步：等待运行中审计检查点；随后加入独立 provider off-grid 结果和全量敏感性结果。
- 状态：verified

### 2026-07-14 14:21 - 价格形状与水平/混合余项分解

- 目标：判断主均衡差异究竟来自日内价格斜率，还是来自动态博弈同时改变的价格基准水平与均衡组合。
- 方法：对 676 个动态正概率服务商剖面保持各价格基准、路由参数和混合概率不变，仅将两家服务商的批发/直连斜率及中间商零售斜率归零，然后重解联合市场固定点。按 `dynamic-uniform = (dynamic-flattened) + (flattened-uniform)` 分解每项指标。
- TDD 记录：首次普通 pytest 因并行任务期间的 pytest 临时捕获文件 `FileNotFoundError` 未进入测试；改用 `-s` 后得到预期红灯 `3 failed`（实现模块尚不存在）。实现后首次回归为 `1 failed, 2 passed`，原因是测试夹具只提供两项而生产函数固定检查四项指标；补齐夹具后为 `3 passed`。该环境性捕获问题未通过修改系统或 `/tmp` 配置规避。
- 命令：
  ```bash
  /root/.local/bin/uv run --no-project --with pytest --with numpy \
    pytest -q -s tests/test_submission_price_shape_decomposition.py
  /root/.local/bin/uv run --no-project --with ruff ruff check \
    experiments/run_submission_price_shape_decomposition.py \
    tests/test_submission_price_shape_decomposition.py
  /root/.local/bin/uv run --no-project --with numpy --with scipy \
    python -m experiments.run_submission_price_shape_decomposition
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 输出：新增 `price_shape_decomposition_submission.json`、实验脚本和 3 项回归测试；主稿方法部分新增分解恒等式，结果部分新增表 6 与解释。
- 结果：动态 flattened 值为峰值 `224.585`、最大利用率 `1.4512`、最低 QoS `0.8864`、市场侧利润 `1725.006`。形状项分别为 `-27.6821`、`-0.2284`、`+0.0722`、`+197.9284`；level/mix 余项分别为 `+0.0160`、`+0.0007`、`-0.0036`、`-253.4844`。676 个剖面全部收敛，最大残差 `9.98e-10`，分解恒等误差为 0；统一价格 flattening 复核误差为 0。
- 验证：最终测试 `3 passed`，Ruff `All checks passed!`。LaTeX 退出码 `0`，18 页、PDF 1.5；最终日志无 LaTeX Error、undefined citation/reference 或 overfull box。PDF 第 13--14 页已按 120 dpi 检查，表格、正文与图 4 无裁切或重叠。
- 决策：主文可写“拥塞与 QoS 差异几乎全部由时段价格形状项解释”；利润净下降来自更大的 level/mix 负余项。该结果只称 fixed-profile accounting decomposition，不称重新求得的均衡反事实。
- 下一步：provider off-grid 已推进到 firm A 的 `960/1544` 个全局候选；继续等待四个敏感性场景的下一缓存检查点。
- 状态：verified

### 2026-07-14 14:29 - 价格形状分解改为实际均价守恒

- 目标：消除 coefficient-base flattening 在价格裁剪后可能改变实际时段均价的问题，使“形状项”不混入每条价格序列的平均水平变化。
- 方法修正：主诊断对每个活跃剖面的每条已实现 wholesale、direct 和 intermediary retail 序列分别取八时段算术均值并展开为常数序列；route beta 与混合权重不变。原 coefficient-base flattening 继续存入工件作为辅助结果，但不作为主文表 6 的定义。
- TDD：新增 `test_mean_flattened_schedule_preserves_each_price_series_mean`，实现前按预期因 `_mean_flattened_schedule` 不存在而失败；实现后完整文件 `4 passed`，Ruff 通过。
- 命令：
  ```bash
  /root/.local/bin/uv run --no-project --with pytest --with numpy \
    pytest -q -s tests/test_submission_price_shape_decomposition.py
  /root/.local/bin/uv run --no-project --with ruff ruff check \
    experiments/run_submission_price_shape_decomposition.py \
    tests/test_submission_price_shape_decomposition.py
  /root/.local/bin/uv run --no-project --with numpy --with scipy \
    python -m experiments.run_submission_price_shape_decomposition
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：mean-flattened 动态值为峰值 `225.434`、最大利用率 `1.3540`、最低 QoS `0.9178`、市场侧利润 `1815.433`。主形状项为 `-28.5311`、`-0.1312`、`+0.0408`、`+107.5015`；level/mix 余项为 `+0.8651`、`-0.0965`、`+0.0279`、`-163.0575`。形状解释略多于全部 aggregate-peak 降幅，并解释约 58% 的最大利用率下降和 59% 的 QoS 增加。
- 诚实性修正：上一条 14:21 记录中的“QoS/利用率几乎全部由形状解释”仅对应 coefficient-base 辅助定义，现已被本条实际均价守恒结果取代；主稿与证据映射不再使用该过强结论。
- 验证：两种 flattening 的 676 个剖面均全部收敛；mean-preserving 最大残差 `9.99e-10`，统一策略均值 flattening 误差为 0，分解恒等误差为 0。主稿编译退出码 `0`，18 页、PDF 1.5，最终日志无 LaTeX Error、undefined citation/reference 或 overfull box；第 13--14 页重新渲染检查无裁切和重叠。
- 下一步：继续等待独立 off-grid 和四个全量敏感性场景；完成后更新最终结果图、宏和结论。
- 状态：verified

### 2026-07-14 14:35 - 2026 年预印本核验与并行求解状态

- 目标：核实相关工作中两篇 2026 年预印本的书目信息，并确认最终 off-grid 与四个敏感性场景没有异常退出。
- 文献核验：直接读取 arXiv 官方页面 `2604.16802` 和 `2603.00356`。前者为 Yan、Yorulmaz、Zhou 与 Basar 的 *A Stackelberg Game Framework with Drainability Guardrails for Pricing and Scaling in Multi-Tenant GPU Cloud Platforms*，2026-04-18 提交；后者为 Cunningham 的 *Token Management in Multi-Tenant AI Inference Platforms*，2026-02-27 提交。题名、作者、年份和主稿中将二者分别定位为定价/扩容博弈与推理容量管理工作的表述一致；二者仍按 arXiv 预印本引用，不改写为正式期刊论文。
- 文献命令：通过浏览工具打开 `https://arxiv.org/abs/2604.16802` 和 `https://arxiv.org/abs/2603.00356`，以官方摘要页为事实源。
- 求解检查：轮询 `capacity_low`、`capacity_high`、`price_sensitivity_low` 和 `price_sensitivity_high` 四个会话；价格敏感度两场景均已完成 dynamic 初始 `676` 对缓存。容量场景及价格场景的 worker 均保持运行。
- off-grid 状态：检查进程和 `submission_offgrid_fourth_grid_detached.log`。最终审计父进程已运行约 2 小时，16 个 worker 仍在计算；最近持久化进度为 firm A global guard 的 `1024/1544` 个候选，即 `26,624` 个支持策略--候选组合。退出标记尚未生成，未观察到 traceback 或进程异常。
- 资源状态：off-grid 16 个 worker 与四个敏感性场景各 4 个 worker 合计使用约 32 个计算 worker。当前不再启动新场景，避免在现有满载下增加内存和调度竞争。
- 决策：只记录运行状态，不把缓存检查点视为审计通过。off-grid 完成后必须核对基线 SHA-256、相对 regret、固定点收敛和残差门槛，再决定是否扩大候选集并重求均衡。
- 下一步：继续监控 off-grid；释放 16 个 worker 后启动迁移成本和 QoS 阈值的四个剩余敏感性场景。
- 状态：in_progress

### 2026-07-14 14:38 - 7 月 14 日终稿结构门禁测试

- 目标：为当天终稿建立可执行的 SMPT 结构与证据门禁，避免实验结束后漏插结果图、遗留占位符或回退到旧主结果。
- 操作：新增 `tests/test_final_manuscript_20260714.py`，检查五个且仅五个编号章节、摘要/关键词/Highlights 限制、最终六张图的存在与正文引用、引文键、旧数值清除以及生产预测/连续策略证明的 claim 边界。
- 命令：
  ```bash
  /root/.local/bin/uv run --no-project --with pytest --with numpy \
    pytest -q -s tests/test_final_manuscript_20260714.py
  ```
- 初次结果：`3 failed, 3 passed`。其中一项是测试对现有边界句的字面匹配过严，不是主稿缺陷；将检查改为接受正文已有的 `production forecast` 和 `continuous-space equilibrium` 明确边界后重跑。
- 当前结果：`2 failed, 4 passed`，退出码 `1`。两个保留红灯与当前真实未完成项一致：尚未插入 `solver_diagnostics.pdf` 和 `resolved_sensitivity.pdf`，且 TeX 仍有 `FINAL_SENSITIVITY_RESULTS` 注释占位。五章节、期刊字数限制、引文和 claim 边界已通过。
- 决策：不通过删除测试或填入未经审计的旧结果消除红灯。待 off-grid 和九组共同候选集重求解通过门禁后，生成两张图并替换结果占位，再要求该文件全部通过。
- 状态：expected_red；blocked_by_running_experiments

### 2026-07-14 14:45 - 788 候选集精确清单与 PDF 内重建说明

- 目标：修正主稿候选集表将所有正概率支持条目等同于新增候选的问题，并让读者只依据 PDF 即可重建最终有限策略集。
- TDD：新增 `tests/test_submission_candidate_manifest.py`。首次用 `pytest` 入口执行时，uv 临时环境没有把仓库根目录放入模块搜索路径，得到三项 `ModuleNotFoundError: No module named 'experiments'`；改用规范的 `python -m pytest` 后得到预期红灯，即三项均因构建模块尚不存在而失败。
- 实现：新增 `experiments/build_submission_candidate_manifest.py`。脚本只读 pre-fourth 与最终均衡工件，重建七个确定性组成部分和前一混合解的活跃支持，然后与最终 `candidate_grid` 逐元素比较。没有修改运行中的均衡、off-grid 或敏感性代码。
- 命令：
  ```bash
  /root/.local/bin/uv run --no-project --with pytest --with numpy \
    python -m pytest -q -s tests/test_submission_candidate_manifest.py
  /root/.local/bin/uv run --no-project --with ruff ruff check \
    experiments/build_submission_candidate_manifest.py \
    tests/test_submission_candidate_manifest.py
  /root/.local/bin/uv run --no-project --with numpy \
    python -m experiments.build_submission_candidate_manifest
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 输出：新增 `candidate_manifest_submission.json`。清单绑定最终 SHA-256 `d3717445...aae2f` 和真实 pre-fourth seed SHA-256 `b00a61ad...18e0`。
- 结果：pre-fourth 解有 52 个正概率支持条目和 48 个不同向量；七个确定性组成部分依次新增 `12, 378, 120, 64, 27, 100, 69` 个，累计 770；延续支持只新增 18 个，最终为 788。重建数组与最终工件逐元素相同。测试 `3 passed`，Ruff `All checks passed!`。
- 论文修改：表 2 现在报告每个组成部分的精确系数集合、新增唯一数和累计数；正文列出全部 18 个 continuation-only 向量。证据映射同步指向该清单。
- 编译与视觉检查：首次编译发现 wholesale-base 行 `1.53 pt` overfull，拆分为按坐标给值后重新编译，退出码 `0`，18 页且无 overfull。PDF 第 6--7 页按 110/130 dpi 检查，表格、18 个向量、公式和后续正文没有裁切、遮挡或次序错位。
- 状态：verified

### 2026-07-14 14:55 - 理论公式与 Python 实现逐项审计

- 目标：从审稿人视角核对 OD 守恒、两阶段选择、路由、QoS 固定点、利润会计、Nash 条件和 off-grid 定义是否与正式实现一致。
- 操作：逐段比对主稿方法部分与 `spatiotemporal_mechanism.py`、`spatiotemporal_game.py`、`peak_shaving_market.py`、`peak_shaving_equilibrium.py`、`intermediary_response.py` 和 `offgrid_diagnostic_tools.py`；新增 `docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md`。
- 结果：没有发现公式方向、负载分配、QoS 反馈、利润求和或双矩阵最佳响应计算错误。固定点存在性命题的连续映射和紧凸域条件成立，但只支持存在性；正文继续明确不证明唯一性或迭代全局收敛。
- 文字修正：首次出现时完整定义 `phi_k` 与 `H_k`，并写明 `phi_R=H_R=0`；将 seed 说明改为“市场份额不做个体 Monte Carlo，seed 用于独立数值审计和 vLLM 协议”，避免与后文 seed 42 冲突；精简 AI 声明中的重复项目。
- 排版修正：将统一均衡的四元组改为独立显示公式，清除最后一处 underfull。执行：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 `0`，18 页；最终日志没有 LaTeX Error、undefined citation/reference、overfull 或 underfull box。
- 仍有限制：路由 QoS 权重 `eta=3` 是实现中的固定默认值而非独立配置字段，但主稿参数表已明示该值；当前运行绑定的源码哈希保持不变，不在求解过程中重构核心模型代码。
- 状态：verified；off-grid and sensitivity gates pending

### 2026-07-14 14:59 - 投稿证据自动门禁

- 目标：防止“工件文件存在”被误当作“数值证据通过”，并将最终图、宏和论文结果绑定到可执行的统一门槛。
- TDD：新增 `tests/test_submission_evidence_gates.py`。实现前运行得到预期 `7 failed`，全部原因是 `experiments.submission_evidence_gates` 尚不存在；实现后覆盖有效工件、过高 off-grid regret、过高残差、活跃支持复算误差、无成功局部优化、过期基准哈希和过高有限 regret。
- 实现：新增 `experiments/submission_evidence_gates.py`。off-grid 门槛为两方相对 regret 不高于 `0.5%`、联合残差不高于 `1e-8`、支持收益复算误差不高于 `1e-6`、每个偏差组合至少有一次成功局部优化；敏感性门槛为基准 SHA 一致、候选数 788、两种定价博弈均完成全候选扫描、绝对 regret 不高于 `1e-7`、残差不高于 `1e-8`。
- 命令：
  ```bash
  /root/.local/bin/uv run --no-project --with pytest \
    python -m pytest -q -s tests/test_submission_evidence_gates.py
  /root/.local/bin/uv run --no-project --with ruff ruff check \
    experiments/submission_evidence_gates.py \
    tests/test_submission_evidence_gates.py
  ```
- 结果：测试 `7 passed`；Ruff `All checks passed!`。最终主入口将在 off-grid 和八个敏感性工件全部生成后写出 `submission_evidence_gate_report.json`；当前未运行主入口，避免把预期缺失状态写成正式报告。
- 决策：`build_final_submission_figures.py` 和结果宏只能在门禁报告 `passed=true` 后执行；若任一检查失败，先扩展/重求或修复工件，不能人工改写 JSON 结果。
- 状态：verified；awaiting artifacts

### 2026-07-14 15:04 - 长时求解监控与 QoS 区间复核

- 目标：确认最终 provider off-grid 审计与首批四个全量敏感性场景仍在有效推进，并复核图 2 的五次重复测量区间换算。
- 运行检查：读取 `/tmp/peak_shaving_final_offgrid.exit`、`submission_offgrid_fourth_grid_detached.log`、四个 uv 会话、进程树和缓存时间。off-grid 退出标记仍未生成；firm A global guard 最近持久化到 `1216/1544` 个候选，即 `31,616` 个候选--支持组合。容量与价格敏感度四个场景的父进程和各 4 个 worker 均在运行，dynamic 初始 `676` 对缓存均已生成。
- 资源：32 个计算 worker 保持满载，load average 约 `33.3`；可用内存约 `7.5 GiB`，swap 已使用约 `3.9/4.0 GiB`。在 off-grid 释放 16 个 worker 前不启动剩余四个场景。
- QoS 区间复核：`pricing_sim/vllm_study.py` 将每个五次重复点保存为 `1.96\,s/\sqrt{5}`；`build_final_submission_figures.py` 再乘以 `t_{0.975,4}/1.96=2.776445/1.96`。图中误差线因此等于 `t_{0.975,4}s/\sqrt{5}`，与正文所述 Student-t 95% 区间一致，无需改动数据或绘图逻辑。
- 实际命令：
  ```bash
  ps -eo pid,ppid,stat,etime,pcpu,pmem,args
  find /tmp/peak_shaving_submission_offgrid_fourth_grid -maxdepth 2 -type f
  find /tmp/peak_shaving_submission_sensitivity -maxdepth 3 -type f
  free -h
  uptime
  ```
- 决策：缓存文件和活跃进程只证明作业仍在运行，不计为证据门禁通过。继续保持求解源码及基准工件不变，待正式 JSON 生成后逐字段验收。
- 下一步：off-grid 完成后立即检查两方 relative regret、残差、活跃支持收益复算误差和局部优化成功次数；通过后启动迁移成本与 QoS 阈值四个剩余场景。
- 状态：in_progress

### 2026-07-14 15:08 - continuation 元数据处理决策

- 发现：基准工件 `spatiotemporal_equilibrium_submission.json` 的 `metadata.continuation_seed.path` 保留了续算时的目标文件名，但其 SHA-256 `b00a61ad...18e0` 实际对应已保存的 `spatiotemporal_equilibrium_submission_pre_fourth_grid.json`。这是路径字段的历史记录问题，不是候选向量或结果数值错误。
- 复核：`candidate_manifest_submission.json` 已记录正确 seed 路径与同一 `b00a61ad...18e0` 哈希，并从该 seed 重建七个确定性候选组成和 18 个 continuation-only 向量；重建结果与最终 788 个候选逐元素相同。
- 决策：不改写已被 fixed-point、intermediary、mechanism、mixed-distribution、price-shape、off-grid 和敏感性作业绑定的 `d3717445...aae2f` 原始基准工件。机器可读候选清单作为路径勘误和候选集重建来源；最终数据说明将提示这一点。该处理保留历史输出和现有哈希链，避免无数值收益的级联元数据重写。
- 验证命令：
  ```bash
  jq '.metadata.continuation_seed' artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_equilibrium_submission.json
  jq '.metadata, .verification' artifacts/peak_shaving/20260712_expanded_response/candidate_manifest_submission.json
  sha256sum artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_equilibrium_submission.json
  ```
- 下一步：在最终 evidence map 和 Data and code availability 中以简短说明连接原始基准与候选清单，不在论文正文展开内部文件历史。
- 状态：verified

### 2026-07-14 15:10 - QoS 负载代理与自然英语修正

- 目标：避免把 vLLM 实验的归一化并发数误写成 GPU 硬件利用率，并去除摘要中的内部审计式术语。
- 论文修改：摘要将 `audit-adaptive set` 改为“declared set ... expanded through repeated deviation checks”；方法部分明确以 `concurrency/224` 作为模型负载比 $u$ 的经验代理，并说明它不是 GPU hardware utilisation 测量；结果段统一写为 `normalised concurrency`；图 2 题注明确误差线是跨五次重复的 repeat-level Student-$t$ 95% 区间。
- 技术影响：不改变 QoS 函数、参数拟合、图中横坐标、均衡工件或任何结果数字。该修改只收紧测量解释，并使摘要用语更接近常规学术英语。
- 命令：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.pdf -
  /root/.local/bin/uv run --no-project --with pytest --with numpy \
    python -m pytest -q -s tests/test_final_manuscript_20260714.py
  ```
- 验证：LaTeX 退出码 `0`，18 页、PDF 1.5；日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。PDF 文本包含新的候选集、经验负载代理和 repeat-level Student-$t$ 表述。
- 门禁：终稿结构测试仍为预期 `2 failed, 4 passed`。失败项仅是尚未生成的 `solver_diagnostics.pdf`、`resolved_sensitivity.pdf` 和 `FINAL_SENSITIVITY_RESULTS` 占位；未使用旧结果绕过测试。
- 状态：verified；final evidence still in_progress

### 2026-07-14 15:13 - 主结果现实量级边界

- 目标：让读者直接从论文正文看到动态策略没有消除过载，并把仿真峰值降幅放回已有电力定价证据的量级中解释。
- 修改：主结果段新增“expected profile-level maximum utilisation 仍为 `1.223>1`，因此只缓解而未消除 modelled overload”；解释段将 `12.32%` 与 Faruqui and Sergici 汇总的 household TOU `3--6%` 和 critical-peak `13--20%` 并列，并明确该比较只是定位合成拥塞案例的量级，不构成 inference-user response 的实证验证。
- 命令：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.pdf -
  ```
- 验证：编译退出码 `0`，18 页；日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。PDF 文本已包含 `reduces rather than eliminates modelled overload` 及电力试验量级边界。
- 影响：不改变模型、实验或结论；降低将合成结果误读为现实预测的风险。
- 状态：verified

### 2026-07-14 15:14 - 线性价格规则与强化学习定位

- 目标：回应“线性定价为何使用网格”和“为何不使用强化学习”的潜在审稿疑问，同时保持相关研究与方法说明简洁。
- 相关研究：新增需求响应强化学习综述和 actor--critic 动态定价文献，说明 RL 适合未知响应下的序列策略搜索，但本研究关心竞争服务商的 Nash 稳定性与可检查的单边偏离，因此直接求解使用可解释线性规则的 provider game。
- 方法澄清：有限候选集离散的是 $(\bar w,\delta^w,\bar p^D,\delta^D)$ 四个规则系数，不是八个时段价格；每个候选仍通过线性规则和 clip 运算生成完整八时段价格表。表 2 的 `audit-adaptive/Audit-local` 改为更自然的 `expanded through deviation checks/Deviation-local`。
- 命令：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  pdftotext peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.pdf -
  ```
- 验证：编译退出码 `0`，18 页、PDF 1.5；日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。新增文献、方法澄清与表题均进入 PDF。
- 状态：verified

### 2026-07-14 15:15 - 最终图目录去旧版本

- 目标：防止后续新增 `includegraphics` 时从旧的 `peak_shaving_final_20260712` 目录静默选图。
- 修改：主稿 `graphicspath` 改为 `figures/peak_shaving_final_20260714/`，文末修订注释同步为 verified 2026-07-14 artifacts。正文当前显式图路径和图文件均未变化。
- 命令：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 验证：编译退出码 `0`，18 页；日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。
- 状态：verified

### 2026-07-14 15:17 - 摘要与 Highlights 限制复核

- 复核：英文摘要为 201 词；关键词 7 个；Highlights 5 条，长度分别为 `73/76/75/64/68` 个字符，均低于期刊 85 字符限制。
- 修改：将 `continuous intermediary policy` 收紧为 `bounded continuous intermediary rule`，并将口语色彩较强的 `cut expected peak` 改为 `reduce expected peak`。
- 命令：
  ```bash
  awk '{print length($0), $0}' \
    peak_shaving_dynamic_pricing_SMPT_highlights_2026-07-14.txt
  ```
- 状态：verified

### 2026-07-14 15:17 - 电力定价量级来源复核

- 目标：核验正文新增的 household TOU 与 critical-peak pricing 百分比，避免依赖二手记忆。
- 来源：Faruqui and Sergici, *Household Response to Dynamic Pricing of Electricity: A Survey of 15 Experiments*, *Journal of Regulatory Economics* 38, 193--225 (2010), DOI `10.1007/s11149-010-9127-y`。出版社元数据与作者公开摘要均确认 15 个实验及对应区间。
- 结果：原文报告 TOU peak-demand reduction 为 `3--6%`，critical-peak pricing 为 `13--20%`；论文中的量级比较准确，无需改数值。
- 检索：出版社 DOI 元数据、作者 SSRN 页面与期刊书目信息；检索日期 2026-07-14。
- 状态：verified

### 2026-07-14 15:19 - Figure 2/3 Times New Roman 重建

- 发现：`input_calibration.pdf` 与 `equilibrium_profiles.pdf` 仍嵌入旧版 `DejaVuSans Type 3`；`mechanism_decomposition.pdf` 和框架图已使用 Times New Roman。绘图代码已配置 Times New Roman，问题来自前两张图未按最新环境重建。
- 操作：只读取已验证的 BurstGPT CSV、QoS calibration JSON 和 `d3717445...aae2f` 均衡工件，调用当前 `_input_calibration` 与 `_equilibrium_profiles` 生成器，重建对应 PDF/PNG；未读取或修改运行中的 off-grid 与敏感性缓存。
- 命令：
  ```bash
  /root/.local/bin/uv run --no-project --with numpy --with matplotlib \
    python -c '<load verified inputs and rebuild Figure 2/3>'
  pdffonts figures/peak_shaving_final_20260714/input_calibration.pdf
  pdffonts figures/peak_shaving_final_20260714/equilibrium_profiles.pdf
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 输出：Figure 2 PNG 为 `2503x787`，Figure 3 PNG 为 `2524x1652`；PDF 均为单页、PDF 1.4。Figure 2/3 PDF SHA-256 分别为 `40498954...a8a400` 和 `712634e8...a314`。
- 字体验证：两个独立 PDF 只嵌入 `TimesNewRomanPSMT` CID TrueType；重编译主 PDF 不再含 DejaVu 字体。全文 PDF SHA-256 为 `ab68543e...d22ca`。
- 视觉检查：全分辨率检查误差条、图例、曲线、坐标标题和底部面板标注，无裁切或遮挡。LaTeX 编译退出码 `0`，18 页；日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。
- 状态：verified

### 2026-07-14 15:21 - Figure 2 模型名标签

- 目标：用读者可识别的模型名替代内部测量 profile 标识。
- 修改：Figure 2(b) 图例由 `vllm-0.5b/vllm-3b` 改为 `Qwen2.5-0.5B/Qwen2.5-3B`；数据、误差线、颜色、曲线和面板位置不变。
- 命令：
  ```bash
  /root/.local/bin/uv run --no-project --with ruff \
    ruff check experiments/build_final_submission_figures.py
  /root/.local/bin/uv run --no-project --with numpy --with matplotlib \
    python -c '<rebuild Figure 2 from verified inputs>'
  pdffonts figures/peak_shaving_final_20260714/input_calibration.pdf
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 验证：Ruff `All checks passed!`；绘图脚本为 300 行。独立 PDF 文本包含两个 Qwen2.5 模型名，只嵌入 Times New Roman；视觉检查无图例遮挡。主稿编译退出码 `0`，18 页且日志无错误、未定义引用或 box warning。
- 哈希：Figure 2 PDF `fed27c66...bb92a`；主 PDF `3c33f2e7...48392`。
- 状态：verified

### 2026-07-14 15:23 - capacity_low 会话 SIGTERM 与恢复决策

- 现象：轮询 `capacity_low` 长时会话时返回退出码 `143`，对应进程收到 `SIGTERM`。场景正式 JSON 尚未生成；另外三个敏感性场景和 off-grid 作业仍在运行。
- 触发条件：该会话已运行约 1 小时 43 分，完成 uniform 与 dynamic 初始收益缓存后处于全候选重求阶段；会话此前没有 stderr/stdout 异常。
- 排查：PID `1369974/1370005` 已不存在；`dmesg`、kernel journal 和 `systemd-oomd` 均无 OOM、segfault 或 kill 记录；当前可用内存约 `7.8 GiB`，memory pressure 为 0。缓存可完整反序列化，uniform/dynamic 分别含 `95/676` 条记录，签名为 `9d5fb5f2...e3058` 与 `6ae4dc65...e2a4`。
- 判断：可确认的直接原因是外部 SIGTERM，没有证据表明模型、固定点、求解器或缓存损坏；系统日志不足以识别信号发送者，因此不把具体来源写成事实。
- 恢复方案：保持源码、参数和缓存不变，从签名校验缓存重启同一 `capacity_low` 场景；改用独立日志、PID 与退出码文件监控。若再次在相近阶段收到 SIGTERM，再比较运行时和父进程托管方式，之后才考虑会话层修复。
- 状态：failed；recovery_in_progress

### 2026-07-14 15:24 - capacity_low 后台恢复方式测试

- 测试：尝试以 `nohup` 后台 wrapper 启动同一缓存恢复，并要求写入 PID、日志和退出码。
- 实际结果：启动命令本身退出码为 `0` 并返回 PID `1709207`，日志只写入 uv 的 `--no-project` 提示；`exec_command` 返回后 wrapper 与子进程均被会话托管层清理，退出码文件来不及生成。没有第二个 `capacity_low` 求解进程残留。
- 判断：该现象发生在工具会话边界，不是模型或求解器错误；`nohup` 在此执行环境中不能作为持久化方案。
- 决策：不重复该方案。改用保持打开的统一长时会话，在会话内部写独立 PID、日志和退出码；继续复用已验证的 `95/676` 对缓存。
- 状态：failed_recovery_method；next_method_selected

### 2026-07-14 15:25 - capacity_low 缓存恢复会话

- 操作：以统一长时会话重新运行完全相同的 `capacity_low` 命令，设置 `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`，继续使用 `/tmp/peak_shaving_submission_sensitivity/capacity_low/` 的签名缓存。
- 会话：session `49534`，wrapper PID `1712399`；独立日志为 `sensitivity_capacity_low_detached.log`，退出码文件为 `/tmp/peak_shaving_capacity_low_submission.exit`。
- 启动验证：日志写入 `starting submission sensitivity: capacity_low`；4 个 multiprocessing worker 均保持运行，未发现重复 `capacity_low` 场景；退出码仍为 pending。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
  OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
  /root/.local/bin/uv run --no-project --with numpy --with scipy --with nashpy \
    python -c '<run_sensitivity capacity_low with parallel_workers=4>'
  ```
- 决策：观察该会话是否越过上次全候选重求阶段。正式 JSON 生成并通过 hash/regret/residual 门禁前，状态保持 in_progress。
- 状态：recovery_in_progress

### 2026-07-14 15:29 - price_sensitivity_low 会话 SIGTERM 与恢复方案

- 现象：长时会话 `49388` 返回退出码 `143`，即 `price_sensitivity_low` 进程收到 `SIGTERM`；正式场景 JSON 尚未生成，日志未出现 Python traceback 或数值求解异常。
- 现场：`capacity_high`、`price_sensitivity_high`、恢复后的 `capacity_low` 以及 off-grid 作业仍在运行；系统可用内存约 `7.5 GiB`，swap 已使用约 `3.9/4.0 GiB`。现有信息只能确认外部终止，不能确认信号发送者或具体系统原因。
- 缓存：`/tmp/peak_shaving_submission_sensitivity/price_sensitivity_low/` 仍存在，将由原脚本重新校验签名并复用；不修改模型、参数、候选集、随机种子或求解代码。
- 决策：沿用 `capacity_low` 的长时统一会话方案恢复该场景，并限制 BLAS 线程。若再次收到 `SIGTERM`，记录发生阶段并在 off-grid 释放资源后串行恢复，避免扩大内存与 swap 压力。
- 状态：failed；recovery_pending

### 2026-07-14 15:30 - price_sensitivity_low 缓存恢复会话

- 操作：在长时统一会话中重新运行相同的 `price_sensitivity_low` 场景，继续使用原签名缓存，并设置 `OMP_NUM_THREADS=OPENBLAS_NUM_THREADS=MKL_NUM_THREADS=1`。
- 会话：session `23679`，wrapper PID `1724297`；日志为 `sensitivity_price_sensitivity_low_detached.log`，退出码文件为 `/tmp/peak_shaving_price_sensitivity_low_submission.exit`。
- 启动验证：uv/Python 进程保持运行，日志进入 `starting submission sensitivity: price_sensitivity_low`，退出码为 pending；未发现重复运行的旧场景进程。
- 状态：recovery_in_progress

### 2026-07-14 15:32 - capacity_high 会话 SIGTERM 与延迟恢复

- 现象：原 `capacity_high` 长时会话 `38309` 返回退出码 `143`，正式场景 JSON 尚未生成；进程列表中该场景已退出，未见 Python traceback。
- 共同特征：`capacity_low`、`price_sensitivity_low` 和 `capacity_high` 三个早期会话均被外部 `SIGTERM` 终止，但各自已完成的签名缓存仍保留。当前证据不足以判断为内存回收、会话寿命限制或其他外部信号来源。
- 资源决策：当前 off-grid 使用 16 个 worker，`price_sensitivity_high`、恢复后的 `capacity_low` 和 `price_sensitivity_low` 各使用 4 个 worker。由于 swap 约为 `3.9/4.0 GiB`，暂不立即增加新的 4-worker 作业。
- 下一步：off-grid 完成并释放资源后，从 `/tmp/peak_shaving_submission_sensitivity/capacity_high/` 复用签名缓存恢复同一场景；正式 JSON 和证据门禁通过前不使用该场景结果。
- 状态：failed；recovery_deferred

### 2026-07-14 15:37 - 终稿语言与理论表述预审

- 范围：在最终 off-grid 和敏感性数值尚未写入前，对英文主稿的摘要、引言、相关研究、方法、结果解释与结论进行轻量语言扫描和公式--文字复核。
- 结果：有限候选集明确离散四个线性规则系数，而非逐时段价格；Nash 条件、全候选 regret、bounded off-grid 检查和连续策略证明之间的界限保持一致。未发现新的公式/实现矛盾。
- 语言：`therefore/thus/however/moreover` 的正文出现次数为 `8/1/1/0`，未形成机械连接词堆积；`robust` 未使用。自动长句列表主要来自 LaTeX 表格和公式，未据此机械改写正文。
- 决策：待最终数值段和两张诊断图插入后，再用 reviewer/polishing/humanizer 流程做整稿润色，避免重复改写造成段落不一致。
- 状态：pre_review_verified

### 2026-07-14 15:52 - 独立 off-grid 审计阶段检查

- 进度：`firm_A/global_guard` 已完成 `1544/1544` 个候选，对应其 26 个对手支持策略的 `40,144` 个组合；缓存 `firm_A.pkl` 已更新并约为 `211 MB`。
- 运行状态：16 个 worker 持续计算，流程已进入 A 方最优全局偏离点附近的 pairwise refinement。该阶段首批尚未写出检查点，因此没有提前读取或报告 regret。
- 完整性边界：正式结果仍须包含 A 方 refinement、B 方 global guard 与 refinement，并由最终 JSON 绑定 `d3717445...aae2f` 基线、788 候选、1,024 样本、独立 seed、收敛残差和支持收益误差。
- 状态：in_progress

### 2026-07-14 16:17 - Provider A off-grid 搜索完成

- 全局阶段：`1544/1544` 个候选、`40,144` 个与 B 方支持混合策略的组合已完成。
- 局部阶段：围绕全局最佳候选生成的 pairwise refinement 为 `176/176` 个候选、`4,576` 个组合，缓存 `firm_A_refinement.pkl` 已更新。
- 运行状态：A 方两个阶段均正常结束，程序已切换到 Provider B 并重新创建 worker pool。最终 regret、最佳向量、残差和支持收益误差仍以两方完成后写出的正式 JSON 为准。
- 状态：firm_A_search_done；firm_B_in_progress

### 2026-07-14 16:18 - 前轮 off-grid 最佳偏离纳入检查

- 检查：前一版 719 候选审计的 A/B 最佳偏离向量 `(0.25, 0.25, 0.5278125, 0.2)` 与 `(0.25, 1.05, 0.5278125, 0.4)` 在当前 788 候选集中的索引分别为 `73` 和 `530`。
- 含义：第四候选集确实吸收了前轮发现的主要遗漏响应；当前独立 seed 的 1,024 点搜索用于检验进一步的离网格收益，而不是重复忽略已知偏离。
- 状态：verified

### 2026-07-14 16:27 - Provider B off-grid 首个检查点

- 进度：B 方独立候选设计去重后包含 `1,533` 个全局/边界候选；首批 `64/1533` 已完成，对应 `1,664` 个与 A 方 26 个支持策略的组合。
- 缓存：`firm_B.pkl` 已生成并约为 `8.7 MB`；A 方两个缓存保持不变。
- 资源：16 个 off-grid worker 与三个 4-worker 敏感性重求同时运行；系统可用内存约 `8.3 GiB`，没有新增异常退出。
- 状态：firm_B_global_in_progress

### 2026-07-14 17:27 - 监控等待会话 SIGTERM 边界

- 现象：仅执行 `sleep 480` 后读取日志的短期监控会话返回退出码 `143`，未执行实验代码或写入实验工件。
- 核对：off-grid 主进程和三个敏感性主进程均仍存活，worker 持续运行，缓存与退出码文件状态正常；B 方仍为 `448/1533`。
- 结论：本次 143 只影响监控等待命令，不属于求解失败，也不改变任何数值或源码哈希。后续改用更短监控窗口。
- 状态：monitor_only_failure；experiments_healthy

### 2026-07-14 17:35 - Provider B off-grid 三分之一里程碑

- 进度：`firm_B/global_guard` 已完成 `512/1533` 个候选，对应 `13,312` 个与 A 方支持混合策略的组合；`firm_B.pkl` 约为 `70 MB`。
- 检查：批次以原子缓存替换方式连续写入，16 个 worker 保持活跃；A 方已完成缓存未变化。
- 状态：firm_B_global_in_progress

### 2026-07-14 17:37 - 两个敏感性长会话再次 SIGTERM

- 现象：`price_sensitivity_high` 原会话和恢复后的 `capacity_low` 会话均返回退出码 `143`；两者没有生成正式场景 JSON，也没有 Python traceback。`price_sensitivity_low` 与 off-grid 主进程仍正常运行。
- 现场：终止后系统可用内存约为 `9.0 GiB`；kernel journal 同时段出现多条 WSL `p9handler.cpp:1378 (LookupFid) Invalid argument`，但没有能将该日志与两个 SIGTERM 建立因果关系的发送者记录，因此只保留为同时发生的环境现象。
- 损失范围：两个场景均未达到 `PairEvaluator` 默认每 `8192` 个新组合的首次中间检查点，现有签名缓存仍停留在初始 uniform/dynamic 扫描；基线、源码和已完成缓存未损坏。
- 决策：不在 off-grid 仍占用 16 个 worker 时再次并发恢复。待剩余敏感性会话停止后，以测试保护把敏感性运行的检查点间隔改为 `1024` 个组合，并在 off-grid 释放资源后降低并发场景数逐项恢复。该调整只影响故障恢复粒度，不改变模型、候选集、收益或门禁。
- 状态：failed；recovery_redesign_pending

### 2026-07-14 18:07 - Provider B off-grid 半程检查

- 进度：`firm_B/global_guard` 已完成 `768/1533` 个候选，对应 `19,968` 个组合，已超过全局阶段一半；缓存约为 `105 MB`。
- 并发：off-grid 16 个 worker 与 `price_sensitivity_low` 4 个 worker 继续运行；后者仍未达到默认 `8192` 对首次检查点。
- 状态：firm_B_global_in_progress；price_sensitivity_low_in_progress

### 2026-07-14 18:34 - B 方 1024 候选与敏感性首次恢复检查点

- off-grid：`firm_B/global_guard` 已完成 `1024/1533` 个候选，对应 `26,624` 个组合，达到全局阶段约三分之二。
- 敏感性：`price_sensitivity_low` 写入 `dynamic cache checkpoint: 8868 pairs`；该数等于原有 `676` 对加默认间隔的 `8,192` 个新组合，缓存更新为约 `47 MB`。
- 恢复意义：即使该长会话后续再次收到外部 SIGTERM，也可从 8,868 对继续，不再丢失此前约 2.8 小时的完整偏离计算。
- 状态：firm_B_global_in_progress；price_sensitivity_low_checkpointed

### 2026-07-14 19:14 - Provider B off-grid 全局阶段末段

- 进度：`firm_B/global_guard` 已完成 `1344/1533` 个候选，对应 `34,944` 个组合，只剩 `189` 个候选；缓存约为 `183 MB`。
- 敏感性：`price_sensitivity_low` 继续从已写入的 8,868 对检查点之后计算，源码保持不变。
- 状态：firm_B_global_final_stretch

### 2026-07-14 19:43 - Provider B off-grid 全局扫描完成

- 结果：`firm_B/global_guard` 的 `1533/1533` 个候选全部完成，共评估 `39,858` 个与 A 方支持策略的组合；缓存约为 `209 MB`。
- 下一阶段：程序已进入 B 方最佳全局候选附近的 pairwise refinement；待首批完成后记录局部候选总数。
- 状态：firm_B_global_done；firm_B_refinement_in_progress

### 2026-07-14 20:02 - 最终独立 off-grid 审计通过

- 输出：`spatiotemporal_offgrid_diagnostic_submission.json`，SHA-256 `d0cc2107867fe89ad83df16301134655dcc7671e62cbcfa3b6bde7e3cacaab04`；作业退出码 `0`。
- 绑定：基线 SHA-256 为 `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`，候选数 `788`，每方 Latin-hypercube 样本 `1024`，独立 seed `20260714`，16 个 worker。
- Provider A：绝对/相对 off-grid regret 为 `3.344718/0.400246%`；最佳向量 `(0.25, 0.35, 0.538125, 0.2)`，来源为 pairwise refinement；评估 `1720` 个候选、`44,720` 个组合。
- Provider B：绝对/相对 off-grid regret 为 `3.511301/0.473311%`；最佳向量 `(0.2825, -0.15, 0.5278125, 0.5)`，来源为 pairwise refinement；评估 `1699` 个候选、`44,174` 个组合。
- 数值质量：两方 `all_joint_converged=true`；最大 joint residual 分别为 `9.99970e-10/9.99977e-10`；最大 active-support payoff error 均为 `4.54747e-13`；每个组合至少 `2` 次局部优化成功。
- 门禁：两方相对 regret 均低于预先设定的 `0.5%` 数值充分性阈值，`validate_offgrid` 返回 `passed=true`。B 方结果接近门槛，正文必须报告精确值并继续声明这不是连续策略空间均衡证明。
- 决策：不在结果出来后移动预设门槛，也不把 0.4--0.47% 描述为零 regret。该审计足以支持有限候选均衡的局部离网格充分性表述，但不支持连续均衡证明。
- 状态：verified

### 2026-07-14 20:03 - capacity_high 低并发场景数恢复

- 操作：off-grid 释放资源后，从 `/tmp/peak_shaving_submission_sensitivity/capacity_high/` 的签名缓存恢复同一场景，使用 16 个 worker；与仍运行的 `price_sensitivity_low` 4 个 worker 合计 20 个。
- 会话：session `7503`，wrapper PID `2853667`；日志为 `sensitivity_capacity_high_detached.log`，退出码文件为 `/tmp/peak_shaving_capacity_high_submission.exit`。
- 约束：模型、候选集、随机性、求解器与缓存签名不变；仅提高单场景 worker 数并减少同时运行的场景数。源码在旧版敏感性会话结束前保持不变。
- 状态：recovery_in_progress

### 2026-07-14 20:06 - Figure 4 求解诊断图与 WSL 临时目录排查

- 生成：从已验证的 `d3717445...aae2f` 均衡、`d0cc2107...aab04` off-grid、固定点审计和中间商全局性审计重建 `solver_diagnostics.pdf/png`；不读取未完成的敏感性结果。
- 首轮视觉问题：面板说明与横轴标题重叠；第二轮通过过度下移造成大面积空白并触发 `tight_layout` warning。最终改为 figure-level 固定底部说明区，三幅面板无刻度、标题或图例遮挡。
- 最终图：PNG `2572x888`；PDF 仅嵌入 `TimesNewRomanPSMT` CID TrueType，SHA-256 `374efe55f7eacd78e7c680f3957a615d450362784e03b168e507882b0d022660`。绘图脚本保持 `300` 行，Ruff 通过。
- 测试环境失败：首次 pytest 沿继承的 Windows `TEMP/TMP=/mnt/c/Users/.../Temp` 创建捕获文件，出现 `FileNotFoundError`，与 WSL p9 临时路径风险一致。设置 `TMPDIR=/tmp TEMP=/tmp TMP=/tmp` 后测试可正常收集。
- 定向测试：`tests/test_final_submission_figures.py` 为 `2 failed, 6 passed`；两个失败均因 `spatiotemporal_sensitivity_submission.json` 尚未生成，其余图形路径、配色、哈希拒绝和字段适配测试通过。该失败保持为最终敏感性门禁。
- 规则：新增项目 `AGENTS.md`，要求实验、测试和图形构建显式使用 WSL `/tmp`，避免 Windows 挂载临时目录。
- 状态：solver_figure_verified；full_figure_suite_pending_sensitivity

### 2026-07-14 20:09 - off-grid 结果写入英文终稿

- 修改：在 Section 4.3 插入两方 off-grid 候选数、绝对/相对 regret、最佳遗漏向量、收敛残差和支持收益误差；加入 Figure 4 `solver_diagnostics.pdf`。正文明确 `0.400%/0.473%` 低于预设 `0.5%` 门禁但并非零，也不是连续策略均衡证明。
- 图形复核：最终采用 figure-level 面板说明与固定底部空间；全分辨率 PNG 和编译 PDF 第 13 页均无面板说明、横轴标题、旋转刻度、图例或正文重叠。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp latexmk -xelatex \
    -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with pytest \
    pytest -q tests/test_final_manuscript_20260714.py
  ```
- 编译：退出码 `0`，18 页、PDF 1.5；最终日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。PDF 文本包含两个相对 regret 和连续策略边界。
- 测试：主稿测试 `2 failed, 4 passed`；仅缺最终 `resolved_sensitivity.pdf` 和仍保留的 `FINAL_SENSITIVITY_RESULTS` 占位门禁，off-grid 图引用、五章结构、引用和 claim 边界均通过。
- 状态：offgrid_section_verified；sensitivity_section_pending

### 2026-07-14 20:10 - provenance-linked 结果宏

- 生成：`submission_result_macros.tex` 从当前均衡、最终 off-grid、中间商全局性审计和固定点多起点审计读取数值，并逐项检查基线 SHA-256、off-grid 0.5% 门禁、中间商 0.1% 门禁、残差、端点跨度和 active-profile coverage。
- 输出：包含 788 候选、46,381 个动态组合、主结果、两方 off-grid regret、固定点跨度和中间商审计增益；SHA-256 `3d0eaae544e460d51335870b1013d335dd64788a5e26692271da13970fbb330a`。
- 测试：`tests/test_submission_result_macros.py` 为 `9 passed`。
- 状态：verified

### 2026-07-14 20:14 - 全量敏感性恢复与检查点改造准备

- 目标：完成容量、价格敏感度、迁移成本和 QoS 阈值共八个扰动场景的 788 候选共同策略集全量重求解，并逐场通过有限 regret 与固定点残差门禁。
- 运行状态：`price_sensitivity_low` 使用 4 个 worker，已持久化 `8,868` 个动态策略对；`capacity_high` 使用 16 个 worker，从原签名缓存继续计算。两个 wrapper、Python 主进程及全部 worker 均处于运行态，退出码文件尚未生成。
- 资源检查：WSL 内存约 `15 GiB`，检查时可用约 `9.9 GiB`；swap 已使用约 `3.9/4.0 GiB`。当前不再启动第三个敏感性场景。
- 源码约束：旧进程运行期间不修改 `run_submission_spatiotemporal_sensitivity.py`、`run_final_spatiotemporal_equilibrium.py`、`final_equilibrium_tools.py` 或 `equilibrium_run_support.py`，避免正式工件记录的源码哈希与实际加载版本不一致。
- 后续实现：两项旧进程结束后，先写失败测试，要求 submission 敏感性入口将缓存检查点间隔显式设为 `1,024`；随后只修改持久化频率并执行定向测试与 Ruff。该改动不改变模型、候选集、随机性、收益或证据门禁。
- 状态：in_progress

### 2026-07-14 20:18 - 数据声明逐工件核对

- 核对：正式均衡 JSON 含 `git_commit`、`git_dirty`、环境、命令和源码 SHA-256；off-grid、固定点与中间商审计 JSON 含基线哈希、源码 SHA-256、命令及各自数值设置，但不重复 Git 字段。
- 修改：将主稿 Data and code availability 中“所有最终工件均包含 Git 与 dirty flag”的泛化表述改为逐类陈述；同步把理论—实现审计中的 off-grid 状态更新为已通过。
- 影响：不改变模型、实验结果、引用或正在运行的敏感性源码，仅收紧可复现性声明。
- 状态：verified_by_field_inspection

### 2026-07-14 20:20 - 数据声明改写编译验证

- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp latexmk -xelatex \
    -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 输出：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.pdf`，18 页，399,478 bytes，PDF 1.5。
- 结果：退出码 `0`；日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull；`pdftotext` 确认修正后的 Git/worktree 与审计工件说明进入 PDF。
- 状态：verified

### 2026-07-14 20:24 - SMPT 官方投稿指南复核

- 来源：Elsevier/ScienceDirect 官方 `Simulation Modelling Practice and Theory - Guide for Authors`，2026-07-14 访问。
- 已核对：摘要 201 词（上限 250）；关键词 7 个（要求 1--7）；5 条 Highlights 均为 64--76 字符（要求 3--5 条、每条不超过 85 字符）；五个编号章节；公式和表格可编辑；图表均在正文引用。
- 期刊匹配：官方范围要求应用论文透明呈现模型开发、实现、数值问题以及基于真实数据的 verification/validation。当前稿已给出模型链、求解审计、BurstGPT 负载形状和 vLLM QoS 形状锚点，同时明确经济参数仍为 synthetic calibration。
- 投稿阻塞：SMPT 使用 single-anonymized review 并要求完整 title page；当前 `Anonymous Author` 仅适合作为内部占位。作者、单位、邮政地址、通讯作者、ORCID、competing interests、Funding 和 CRediT 必须由作者提供。
- 文件：更新 `docs/reviews/smpt_submission_adaptation_checklist_2026-06-21.md`，保留官方模板迁移、冻结 GitHub release/Zenodo 和敏感性门禁为待办。
- 状态：content_format_checked；author_metadata_blocked

### 2026-07-14 20:27 - 正文数字与路由边界审计

- 对照工件：`spatiotemporal_equilibrium_submission.json`、`mixed_outcome_distribution_submission.json`、`mechanism_decomposition_submission.json` 和 `price_shape_decomposition_submission.json`。
- 一致性：主表的 8 个指标、676 个活跃剖面分位数、temporal/spatial/combined 三组机制变化和四项价格形状分解均与 JSON 一致，未发现旧版本数字。
- 新诊断：动态活跃剖面中，`beta=0` 下边界占 `29.0017%` 概率质量，接近 `10^6` 上边界占 `0.0134%`；标记为至少一个时段近确定性路由的剖面占 `24.8983%`。
- 修改：在 Section 4.2 报告四舍五入后的 `29.0%`、`0.013%` 和 `24.9%`，并明确 `beta` 是数值路由控制量而非估计的经济弹性；同步更新 claim--evidence 表。
- 状态：verified_by_artifact_comparison

### 2026-07-14 20:31 - 敏感性缓存检查点 TDD 红灯

- 测试改动：`test_run_sensitivity_forwards_parallel_workers` 现在要求 submission 敏感性入口传入 `checkpoint_interval=1024`；新增 `test_equilibrium_pipeline_records_cache_checkpoint_interval`，要求均衡元数据记录实际检查点间隔。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy --with scipy --with nashpy pytest -q \
    tests/test_submission_spatiotemporal_sensitivity.py::test_run_sensitivity_forwards_parallel_workers \
    tests/test_final_spatiotemporal_equilibrium.py::test_equilibrium_pipeline_records_cache_checkpoint_interval
  ```
- 结果：预期 `2 failed`，退出码 `1`。失败原因分别为缺少传入的 `checkpoint_interval` 和 `run_equilibria` 尚不接受该参数，证明测试覆盖目标行为。
- 约束：测试文件不参与正在运行作业的数值计算或源码哈希；生产源码仍保持不变。两个旧进程结束后再进入 green 阶段。
- 状态：red_verified；implementation_waiting_for_old_processes

### 2026-07-14 20:39 - Figure 1 正文字号与终稿编译复核

- 目标：提高 Figure 1 在 A4 正文宽度下的小字可读性，同时保持既有节点、直线/直角连线和模型逻辑不变。
- TDD：先在 `tests/test_final_framework_drawio.py` 增加缩放后字号门禁；红灯定位到用户说明、公式、求解步骤和证据标签仅为 16--17 pt。随后将这些源图字号分别提高到 18--19 pt，并让带标签的连线显式使用 18 pt。
- 图形验证：重新生成 Draw.io 源图后，严格结构校验为 `0 errors, 0 warnings`，Figure 1 测试为 `6 passed`，相关 Python 文件 Ruff 检查通过。
- 导出故障：首次复用桌面 Draw.io 配置导出时出现 `UnknownVizError` 并挂起；中断该任务自身会话后退出码为 `130`，旧正式图未被覆盖。改用独立 `--user-data-dir` 并关闭 GPU 后，PNG、SVG 和 PDF 均成功导出。
- 正式图：PNG 为 `3200x1918`；PDF 为单页 PDF 1.5，并嵌入 Times New Roman regular、italic、bold 和 bold italic。PNG/SVG/PDF SHA-256 分别为 `49b3a1d2...ca1`、`65d61792...497`、`0c623b65...938`。
- 编译故障：新增中间商边界比例段落的首次写入含一个反斜杠转义形成的退格控制字符，且百分号未转义；XeLaTeX 以 `Text line contains an invalid character` 失败，退出码 `12`。已按原句精确替换为合法的 `\\beta` 与 `\\%`，控制字符扫描不再检出异常字节。
- 最终命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp latexmk -xelatex \
    -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 最终结果：退出码 `0`，18 页、399,922 bytes、PDF 1.5；日志无 LaTeX Error、undefined citation/reference、overfull、underfull 或 invalid character。第 4 页 180 dpi 渲染抽检显示框架图无节点、公式、连线或图注重叠。
- 状态：verified

### 2026-07-14 20:45 - capacity_high 首个恢复检查点与新文献核验

- 敏感性进度：`capacity_high` 已写入 `dynamic cache checkpoint: 8868 pairs`；缓存从初始 676 对增长至约 47 MB。该场景与 `price_sensitivity_low` 均已有可恢复的 8,868 对动态缓存，退出码文件仍为 pending，20 个 worker 保持活跃。
- 文献核验：通过 AAAI 正式论文页确认 PriLLM 的题名、作者、卷期、页码和 DOI；通过 NBER 确认 working paper 34608；通过 arXiv 原始记录确认 `2604.16802`、`2603.00356` 和 `2502.07736` 的题名、作者及版本状态；通过 Springer 正式论文页确认 Faruqui--Sergici 的 3--6%/13--20% 区间；通过 KDD 官方论文列表和 BurstGPT 官方仓库确认 DOI `10.1145/3711896.3737413`。
- 文本完整性：全仓库文本控制字符扫描发现证据映射表的 `beta` 条目残留一个退格字符；已修复为合法的 `\\beta`，复扫无异常字符。英文 TeX 正文不受影响。
- 结论：已核对的新近关键引用均真实存在且当前出版状态与 `verified_refs.bib` 一致。`yan2026stackelberg` 与 `cunningham2026token` 仍按 arXiv 预印本引用，不升级为正式发表。
- 状态：checkpointed；references_verified

### 2026-07-14 20:49 - 三审稿人终稿审查与方法透明度改写

- skill：按 `nature-reviewer` 的三审稿人结构完成理论/博弈、实验/验证、贡献/语言三路审查；按 `nature-polishing` 的 research、全章节、英文、generic SCI 规则检查段落职责；按 `humanizer` 扫描宣传词、机械连接词、否定排比和 em dash。skill manifest 声明的 `_shared/core` 四个文件在当前安装路径缺失，已记录该加载边界，其余路由片段正常读取。
- 审稿输出：新增 `docs/reviews/smpt_final_three_reviewer_audit_2026-07-14.md`。三位审稿人的当前推荐均为大修；共同实质门禁是八场景敏感性、混合均衡分支审计和最终投稿元数据/模板。
- 方法改写：把“第四候选集”等内部版本词改为 `candidate-expansion audit`；说明 18 个延续向量的来源；公开多候选时按 full-candidate regret、restricted regret 和 combined provider payoff 选择；明确求解器不穷举所有混合均衡；将 0.5 秒 TTFT 写为预设诊断阈值而非通用生产 SLO。
- 编译命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp latexmk -xelatex \
    -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 `0`，18 页、400,259 bytes；日志无 LaTeX Error、undefined citation/reference、overfull、underfull 或 invalid character。
- 主稿测试：`2 failed, 4 passed`。两个失败仍精确对应未生成的 `resolved_sensitivity.pdf` 与 `FINAL_SENSITIVITY_RESULTS` 占位；本轮新增透明度文本、五章结构、当前图表和引用检查均通过。
- 状态：reviewed；language_and_method_edits_verified；sensitivity_gate_pending

### 2026-07-14 20:54 - 混合均衡分支审计 TDD 与正式运行

- 目标：检查冻结的最终受限收益矩阵是否因互补系统初值不同而恢复出多个低 regret 混合均衡分支，并量化分支间主结果差异。
- 红灯：新增 `tests/test_submission_equilibrium_branch_audit.py` 后，修正测试导入路径，测试按预期因 `experiments.run_submission_equilibrium_branch_audit` 不存在而 collection error，退出码 `2`。
- 实现：新增只读脚本 `experiments/run_submission_equilibrium_branch_audit.py`，从签名匹配的 baseline pair cache 重建最终受限矩阵与全候选偏离矩阵；提供受限/full regret、混合分支聚类和独立乘积分布结果加权函数。
- 测试修正：首轮 green 中 3 项通过、1 项失败；失败来自测试对 `0.10/0.15/0.30/0.45` 权重的手算期望写错，正确峰值/QoS 为 `142/0.69`。修正测试期望后为 `4 passed`。
- 质量检查：Ruff 通过；脚本为 300 行，radon 最高复杂度 B(6)，没有超过项目函数复杂度门禁。
- 正式运行：使用报告解、均匀初值和 seed `20260715` 的 64 个独立 Dirichlet 初值，共 66 个初值；读取 `/tmp/peak_shaving_audit_enriched_equilibrium/dynamic.pkl`，不写入或修改敏感性缓存。运行时单进程约占一个 CPU 核。
- 状态：tests_verified；branch_audit_in_progress

### 2026-07-14 20:58 - 混合均衡分支审计通过并进入统一门禁

- 输出：`equilibrium_branch_audit_submission.json`，SHA-256 `2b2f46438dbc2572e55bb2635ecfe81e704d39736015d1c15a69a590889b39ce`；绑定 baseline SHA-256 `d3717445...aae2f` 与 cache SHA-256 `3b3276b2...d657`。
- 结果：66 个初值中 65 个返回有效受限均衡；`dirichlet_000` 未返回有效解。其余 65 个全部在 `1e-6` 概率容差下聚为同一分支，并恢复 26-by-26 活跃支持。
- 数值：恢复分支的 full-candidate regret 为 `1.136868e-13`，相对值 `1.360434e-16`；峰值、最大利用率、最低 QoS 和市场侧利润与 baseline 的差异分别为 `0/0/-3.33e-16/-4.55e-13`。
- 证据门禁：为 `submission_evidence_gates.py` 增加 branch gate，要求 baseline 哈希、788 候选、至少 64 个成功初值、单一恢复分支和不高于 `1e-7` 的 full-candidate regret。门禁测试先红后绿，最终 `tests/test_submission_evidence_gates.py` 为 `12 passed`。
- 当前总门禁：手动运行 evidence gates 的退出码为 `1`；off-grid 和 equilibrium-branch 均通过，失败项精确为八个敏感性 JSON 尚未生成。这是预期的未完成状态，不是新数值失败。
- 论文同步：Section 4.3 已报告 65/66、多初值同一分支、full-candidate regret 与“不穷举所有均衡”的边界；证据映射、理论一致性审计和三审稿人报告均同步更新。
- 验证：分支审计与门禁测试合计 `16 passed`；XeLaTeX 退出码 `0`，18 页、400,868 bytes，日志无 LaTeX Error、undefined citation/reference、overfull、underfull 或 invalid character。
- 状态：verified；sensitivity_only_gate_pending

### 2026-07-14 21:04 - 终稿图形逐图视觉与字体复核

- 范围：逐张检查 Figure 2 `input_calibration.pdf`、Figure 3 `equilibrium_profiles.pdf` 和 Figure 5 `mechanism_decomposition.pdf`；Figure 1 与 Figure 4 已在前序编译页检查中通过。
- 视觉结果：三张图均使用一致的低饱和蓝灰、深蓝与红棕配色；子图编号、图例、误差棒、数值标签、轴标题和曲线之间无重叠。Figure 3(b) 图例信息较密，但仍完整位于画布内且可辨认。
- 字体：`pdffonts` 确认 Figure 2--5 均嵌入 Times New Roman；逐图 180 dpi 渲染未发现裁切或空白面板。
- 辅助命令失败：尝试使用 `montage` 和 `identify` 生成联系表时返回 `command not found`。该失败不影响正式图或论文编译；未为此安装 ImageMagick，改为逐图原分辨率审阅。
- 敏感性状态：`price_sensitivity_low` 与 `capacity_high` 的 Python 主进程及 20 个 worker 均在运行，两个退出码文件仍为 pending；两场景各保留 8,868 对恢复检查点。检查时 WSL 可用内存约 9.7 GiB，memory/io PSI 的 10/60/300 秒均值为 0。
- 决策：`price_sensitivity_low` 第二检查点写出前不终止或提速；暂不启动第三个场景。
- 状态：figures_verified；sensitivity_in_progress

### 2026-07-14 21:07 - 图表与正文集成回归测试

- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy --with matplotlib --with scipy --with nashpy \
    pytest -q tests/test_final_submission_figures.py \
    tests/test_final_framework_drawio.py \
    tests/test_peak_shaving_framework_tex_integration.py
  ```
- 结果：`2 failed, 16 passed`，退出码 `1`。两个失败均来自 `spatiotemporal_sensitivity_submission.json` 尚不存在；框架图结构、字体、TeX 引用和已有正式图测试全部通过。
- 决策：保持这两个失败作为终稿敏感性工件门禁；八场景全量重求解完成前不生成占位 JSON，也不弱化测试。
- 状态：existing_figures_verified；final_sensitivity_figure_blocked_by_expected_gate

### 2026-07-14 21:08 - 英文连接词去机械化与编译验证

- 范围：按 `nature-polishing` 与 `humanizer` 的语言检查规则，复核引言、相关研究、方法和机制解释中的机械连接词；保持公式、参数、引用、结果数字和证据边界不变。
- 首次修改失败：一个大补丁因 QoS 校准段落的上下文未精确匹配而被 `apply_patch` 拒绝；文件未发生部分修改。随后按实际源文拆分为小补丁完成修改。
- 修改：将重复的 `therefore/thus/however` 改为直接的因果陈述或删除无必要连接词；全文这五个重点扫描词中仅保留一处语义必要的 `therefore`，`thus/however/moreover/furthermore` 均为 0。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp latexmk -xelatex \
    -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：退出码 `0`，18 页、400,797 bytes；日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。
- 状态：verified

### 2026-07-14 21:09 - price_sensitivity_low 检查点提速恢复

- 检查点：4-worker 运行写出第二个动态缓存检查点，共 `17,060` 个策略对；缓存大小 `90,698,749` bytes，SHA-256 `d84afffdc181b3b534e32386ca70387b2de307d90fe7e2f52855533b6bab1102`。
- 操作：向本任务启动的旧进程组发送 `SIGTERM`；全部进程在 2 秒内退出。退出时 Python `resource_tracker` 报告 5 个待清理 semaphore，这是多进程中断清理提示，不涉及已持久化 pair cache。终止后缓存大小、修改时间和 SHA-256 均未变化。
- 恢复命令：使用相同生产源码、相同场景与相同签名缓存，将 `parallel_workers` 从 4 调整为 12；日志追加写入 `sensitivity_price_sensitivity_low_detached.log`，未覆盖原检查点记录。
- 运行确认：12 个计算 worker 和 1 个 resource tracker 均已启动；与 `capacity_high` 合计 28 个计算 worker。检查时可用内存约 9.3 GiB，memory PSI 为 0。
- 决策：继续等待两个场景完成，不再增加并发，也不启动第三场景。
- 状态：resumed_from_verified_checkpoint；in_progress

### 2026-07-14 21:10 - 标题、摘要、贡献与结论主张一致性检查

- 检查：逐段对照题名、201 词摘要、Introduction 贡献段、Interpretation and evidence limits 与 Conclusion and outlook。
- 结果：各处均把结论限定为合成经济校准、固定总需求和 788 候选有限博弈下的服务质量效应；均未声称生产预测、连续策略空间均衡证明、社会福利改善或稳健利润提升。
- 理论复核：市场固定点存在性命题的定义域、连续映射与 Brouwer 条件相符；内部批发结算守恒命题与两条利润式中的正负转移项逐项对应。两个证明均未越界声称唯一性或迭代全局收敛。
- 决策：本阶段不再增加防御性限制句，避免影响正文可读性；待八场景结果完成后只按工件更新摘要、敏感性段和结论。
- 状态：verified_by_manual_theory_and_claim_review

### 2026-07-14 21:12 - 2024 年电力动态定价文献补充

- 来源核验：通过 ScienceDirect 正式论文页核对 El-Afifi et al., *Energy Conversion and Management: X* 24 (2024) 100815，DOI `10.1016/j.ecmx.2024.100815`；核对 Fraija et al., *Smart Energy* 14 (2024) 100139，DOI `10.1016/j.segy.2024.100139`。
- 修改：在 electricity-pricing 综述中加入近期博弈论分时定价工作；在强化学习段加入容量与市场约束下的价格生成规则，并保持与本文“竞争服务商单边偏离稳定性”问题的区别。`verified_refs.bib` 增加两个已核验条目。
- 编译：`latexmk -xelatex` 首轮因新引用进入 aux 出现暂时 undefined citation，随后自动执行 BibTeX 和后续 XeLaTeX；最终退出码 `0`。
- 输出：19 页、402,676 bytes、PDF 1.5；最终日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull，两个新引用均存在于 aux 与 bbl。
- 状态：verified

### 2026-07-14 21:14 - 数据锚点与正文结果一致性回归

- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with pytest --with numpy --with scipy --with pandas \
    --with matplotlib --with nashpy pytest -q \
    tests/test_peak_shaving_consistency.py \
    tests/test_final_qos_calibration.py \
    tests/test_burstgpt_load_anchor.py \
    tests/test_submission_result_macros.py
  ```
- 结果：`17 passed in 2.83s`，退出码 `0`。
- 覆盖：BurstGPT 派生负载、vLLM QoS 拟合、需求与支付守恒、正式工件绑定和 TeX 结果宏；未读取或写入正在运行的敏感性 pair cache。
- 状态：verified

### 2026-07-14 21:16 - 图表孤儿引用修复

- 检查：解析主稿中的全部 `fig:`、`tab:` 标签与 `\includegraphics` 路径。
- 发现：Figure 5 `fig:mechanism_decomposition` 和参数表 `tab:parameters` 紧邻相关讨论，但正文未用编号显式引用；其余图表均有引用，五个正式图文件全部存在。
- 修改：在机制分解结果段加入 Figure 5 引用；在验证与校准段加入参数表引用。不改变图、表、数字或解释范围。
- 验证：重新编译退出码 `0`，19 页、402,713 bytes；孤儿标签检查无输出；最终日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。
- 状态：verified

### 2026-07-14 21:18 - 本轮实验与审计代码静态检查

- 命令：使用 `uv run --no-project --with ruff ruff check` 检查最终均衡、submission 敏感性、分支/固定点/中间商审计、机制与价格形状分解、证据门禁、正式图生成、结果宏、核心时空博弈模块及对应测试。
- 结果：`All checks passed!`，退出码 `0`。
- 说明：检查为只读；仍未修改两个运行进程正在加载的生产源码。检查点间隔测试继续保持已记录的 red 状态，待旧进程结束后实施。
- 状态：verified

### 2026-07-14 21:18 - 非活动审计脚本复杂度重构

- 发现：radon 门禁扫描报告 7 个 C 级代码块，涉及 6 个函数；其中 3 个位于当前敏感性进程正在加载的核心模块，暂不修改。其余 4 个位于结果宏、固定点审计、中间商审计和机制分解脚本。
- 修改前基线：四个对应测试文件为 `28 passed in 1.46s`。
- 修改：将审计质量判断、并行任务执行、元数据构造、汇总统计和单机制聚合拆为小函数；数据字段、数值算法、随机种子、命令记录和工件格式保持不变。
- 修改后验证：同一组测试为 `28 passed in 0.93s`；Ruff 为 `All checks passed!`；radon 的 `-n C` 无输出，45 个代码块平均复杂度 A(2.76)。四个文件分别为 173、242、298 和 252 行。
- 待办：`run_equilibria`、`PairEvaluator.evaluate_many` 与 `expected_outcome` 的复杂度重构必须等两个旧源码进程结束后再做，并与 1,024 间隔检查点改造一起执行完整缓存回归。
- 状态：partial_quality_gate_verified；active_core_refactor_deferred

### 2026-07-14 21:19 - Figure 1 图标许可与署名复核

- 核对：Figure 1 图注已署名 Streamline Ultimate Color 并链接 CC BY 4.0；主稿 AI 声明说明该图为可编辑 Draw.io 矢量图，未使用生成式图像模型创建或修改。
- 本地证据：`LICENSE-CC-BY-4.0.txt`、`ATTRIBUTION.md`、`SOURCES.tsv` 与素材 SVG 均存在；署名文件记录上游仓库和固定提交 `52d750c9ce051e51cb181b7a78932120c48541d0`。许可与署名文件 SHA-256 分别为 `9ba9550a...9411` 和 `a570b47e...12ce`。
- 结果：版权来源、许可条件和投稿图注一致，无需改图或正文。
- 状态：verified

### 2026-07-14 21:20 - GitHub 数据可用性地址匿名访问检查

- 本地：`origin` 的 fetch/push 均为 `https://github.com/cccht/paper_token_price.git`，当前分支 `main`，HEAD `0941d97`。
- 匿名检查：使用 `GIT_TERMINAL_PROMPT=0`、空 credential helper 和空 askpass 执行 `git ls-remote`，成功读取远端 HEAD 与 `refs/heads/main`，二者均为 `0941d97af4afa33a0b150a77bfada33ef779c9ed`。
- 边界：仓库地址与公开读取已验证；本轮未提交的终稿、审计和敏感性工件尚未出现在远端。完成全部证据门禁前不提交或发布新的 release。
- 状态：repository_publicly_readable；current_work_unpublished

### 2026-07-14 21:22 - 审计工件完整依赖哈希 TDD

- 问题：行为不变重构使固定点、中间商和机制分解工件记录的脚本哈希与当前源码不再相同；进一步检查发现旧 `_source_hashes` 还遗漏了实际导入的本地依赖。
- 红灯：扩展三个 provenance 测试，要求覆盖 `run_final_spatiotemporal_equilibrium.py`、`final_equilibrium_tools.py`、`run_submission_intermediary_audit.py` 和 `peak_shaving_equilibrium.py` 等直接依赖。定向测试按预期为 `3 failed`，退出码 `1`。
- 实现：补齐三个脚本的 `source_sha256` 路径集合，不改变数值函数、参数、随机种子或输出字段。
- 绿灯：结果宏及三个审计测试文件合计 `28 passed in 0.80s`；Ruff 通过；radon 未报告 C 级函数。
- 工件边界：现有三个 JSON 仍记录重构前哈希，发布前必须按新脚本重跑固定点审计、中间商审计和机制分解，再重建结果宏与相关图。当前不占用 28-worker 敏感性资源。
- 状态：provenance_code_verified；formal_artifact_regeneration_pending

### 2026-07-14 21:23 - 本轮文本与补丁卫生检查

- 命令：对本轮论文、参考文献、README、审计脚本与测试运行 `git diff --check`，并扫描 Git 冲突标记和 ASCII 非法控制字节。
- 结果：无尾随空格错误、无非法控制字符；`experiments/run_multiplatform.py` 的纯等号行是历史输出分隔符，不属于冲突标记，且不在本轮修改范围。
- 状态：verified

### 2026-07-14 21:24 - 八场景定义与正文一致性复核

- 对照：submission 敏感性 `SCENARIOS`、evidence gate 场景清单和 Methodology 第 415 行。
- 结果：容量缩放 `0.85/1.15`、价格敏感度缩放 `0.8/1.2`、迁移成本缩放 `0.7/1.3`、QoS 阈值平移 `-0.05/+0.05` 完全一致；八个场景名称与门禁名称一一对应。
- 求解范围：每场景使用相同 788 候选集，分别重求 uniform 与 dynamic 有限博弈及连续中间商响应；正文已明确仅 baseline 执行连续 off-grid 搜索。
- 状态：verified

### 2026-07-14 21:30 - capacity_high 第二恢复检查点

- 监控：每 30 秒只读检查缓存时间戳与退出文件，21:29:34 检测到 `capacity_high` 新写入。
- 结果：动态 pair cache 从 8,868 增至 `17,060` 对，文件大小 `90,699,795` bytes；日志无异常，退出码仍为 pending。
- 并发：`capacity_high` 保持 16 个 worker；`price_sensitivity_low` 保持 12 个 worker，后者仍使用 17,060 对的最近检查点继续计算。
- 决策：保持总计 28 个计算 worker，不启动第三场景。
- 状态：checkpointed；in_progress

### 2026-07-14 21:31 - SMPT Highlights 复核

- 文件：`peak_shaving_dynamic_pricing_SMPT_highlights_2026-07-14.txt`。
- 结果：共 5 条，长度分别为 73、76、75、64 和 68 字符，满足 Elsevier 每条不超过 85 字符的要求；主张与当前 12.32% 峰值变化、QoS 改善和 -2.81% 市场侧利润变化一致。
- 边界：未提前写入八场景稳健性、生产预测或连续策略均衡主张。
- 状态：verified

### 2026-07-14 21:31 - 三审稿人报告状态同步

- 文件：`docs/reviews/smpt_final_three_reviewer_audit_2026-07-14.md`。
- 更新：将混合均衡分支恢复审计标为已完成；补入两篇 2024 电力定价文献与全部图表交叉引用/图标许可检查；删除已完成的分支阻塞项。
- 当前门禁：八场景全量敏感性、重构后审计工件再生成、核心复杂度与检查点回归、作者元数据/Elsevier 模板、最终 release/DOI。
- 结论：综合推荐保持 `Major revision`，未提前改为可投稿。
- 状态：review_log_current

### 2026-07-14 21:32 - SMPT 投稿适配清单同步

- 文件：`docs/reviews/smpt_submission_adaptation_checklist_2026-06-21.md`。
- 修改：PDF 页数更新为 19；删除重复的 `elsarticle.cls` 检查行；将匿名 GitHub 可读性、混合分支已通过、八场景仍运行和重构后审计工件需再生成写入当前状态。
- 保留阻塞：真实作者/单位/通讯信息、Funding、CRediT、competing interests、ORCID 和 Elsevier 官方模板不得由工具推测。
- 状态：checklist_current

### 2026-07-14 21:33 - 19 页 PDF 末页视觉抽检

- 操作：以 160 dpi 渲染第 18--19 页并逐页检查新增参考文献、DOI/URL 换行、页边距和页脚。
- 结果：所有条目完整，无裁切、重叠或页脚冲突；第 19 页留白来自参考文献自然结束，不是缺失内容。
- 状态：verified

### 2026-07-14 21:35 - evidence gate 增加源码哈希一致性

- 红灯：新增 `validate_source_hashes` 测试后，因函数不存在按预期 `1 failed`，退出码 `1`。
- 实现：总门禁新增固定点、中间商和机制分解三个 provenance 检查；逐个验证记录路径位于仓库内、文件存在且当前 SHA-256 与工件一致。
- 绿灯：`tests/test_submission_evidence_gates.py` 为 `13 passed in 0.08s`；Ruff 通过；radon 无 C 级函数。
- 当前总门禁：命令退出码 `1`，报告 `passed=false`。off-grid 与 equilibrium branch 通过；失败项精确为 3 个审计源码哈希不一致和 8 个敏感性场景文件缺失。
- 输出：更新 `submission_evidence_gate_report.json`，gate script SHA-256 `2e77a1776f0205a71372f6c3f337f0d8b15330d3386e8f6a560e579744b5ddba`。
- 状态：gate_behavior_verified；expected_failures_11

### 2026-07-14 21:39 - 扩展响应空间数值源码冻结前核验

- 目标：在后续代码质量重构前，为基线和八场景全量重求保留可检出的精确数值源码快照。
- 操作：仅暂存正式基线 `metadata.source_sha256` 覆盖的源码、输入数据和 submission sensitivity 入口；论文、README、审稿记录、图表及实验输出均未加入本次暂存。
- 核验：逐项计算 20 个基线来源文件的工作区 SHA-256 与 Git 暂存区 blob SHA-256，并与正式基线工件比较。
- 结果：`SOURCE_COUNT=20 WORK_MISMATCH=0 INDEX_MISMATCH=0`。
- 输入边界：BurstGPT 8-period CSV 保留原始 CRLF 字节；其 SHA-256 为 `acc1f4952fffa35df7b72f80f734c1de6d566cce9514839f3b6b5600b0ad3ab3`。由 CRLF 触发的 `git diff --cached --check` 尾随空白提示不作格式化处理，以免改变输入哈希和在途 pair cache 签名。
- 提交：`6f483084178c3934d1340ba95cd469ae9dd1141d`（`Freeze expanded-response numerical source`），仅含上述暂存范围；未推送远端。
- 提交后验证：从该提交逐项读取 20 个来源 blob 并重新计算 SHA-256，结果为 `COMMIT_MISMATCH=0`。
- 下一步：保持该冻结源码运行全部八个敏感性场景；数值核心重构延后到场景工件生成后，并以此提交作为结果来源快照。
- 状态：verified；source_frozen

### 2026-07-14 21:44 - 终稿英文句长检查命令修复

- 目标：按 `nature-polishing` 与 `humanizer` 规则检查超过 30 词的英文句子。
- 失败：首次把含撇号的正则表达式直接嵌入 shell 单引号命令，Bash 在 `)` 处报语法错误，退出码 `2`，未生成或修改论文文件。
- 修复：先用 `detex -l` 输出到 `/tmp/peak_shaving_final_detex.txt`，再通过 `uv run --no-project python` 读取临时文本并统计句长。
- 结果：检测到的 407 个句段中有 7 个超过 30 词；其中 6 个由 `detex` 将标题、公式或相邻段落拼接造成。唯一明确的正文长句是离网格搜索的 32 词句子。
- 状态：verified；one_sentence_revision_required

### 2026-07-14 21:46 - 英文术语与长句定向润色

- 修改：将摘要中的 `continuously optimises` 改为“在有界连续参数域上优化”；首次展开 L-BFGS-B、SLA 和 RMSE；把 32 词的离网格搜索句拆为两句。公式、数字、引用键和证据边界均未改变。
- 审稿记录：修正三审稿人综合意见中已过时的“混合均衡分支仍待完成”，明确该门禁已通过，当前主要实质门禁为八场景全量敏感性。
- 编译命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp latexmk -xelatex \
    -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：退出码 `0`；生成 19 页、402,909 bytes 的 PDF。日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。
- 语言扫描：除一处有逻辑必要的 `therefore` 外，未发现所列 AI 高频连接词、宣传性词汇或 Unicode em dash。
- 状态：verified

### 2026-07-14 21:48 - GPU 可用性与求解器适配检查

- 用户要求：可使用 GPU 的计算优先使用 GPU 加速。
- 硬件检查：`nvidia-smi` 在 WSL 中识别到 NVIDIA GeForce RTX 4090，驱动 596.21，显存 24,564 MiB；检查时占用 6,093 MiB、GPU 利用率 1%。
- Python 检查：PyTorch 2.11.0+cu130 可用，`torch.cuda.is_available()` 为 `True`，CUDA 版本 13.0；CuPy、JAX 和 jaxlib 未安装。首次通过 heredoc 调用的 PyTorch 探针只返回 uv 警告、未返回探针字段，随后改用 `uv run --no-project python -c`，退出码 `0` 并取得上述结果。
- 适配结论：当前 pair evaluator 使用 NumPy、SciPy L-BFGS-B 和 8 时段固定点迭代，没有等价的 CUDA 后端。工作负载由大量小数组、优化器回调和分支构成，不能通过设备切换直接获得可靠加速。
- 决策：不终止已运行至 17,060/46,381 pair 检查点的两个 CPU 场景，也不在证据生成中引入未经等价性测试的新 GPU 实现。后续仅对可批处理环节先做 CPU/GPU 数值等价和计时测试，确认更快后才启用。
- 状态：gpu_available；current_solver_cpu_only_by_design

### 2026-07-14 21:51 - 敏感性场景源码哈希门禁 TDD

- 问题：场景门禁已检查 baseline SHA-256、788 候选、全候选 regret 和固定点残差，但未检查每个场景工件的 `metadata.source_sha256`。
- 红灯：新增陈旧源码哈希测试后，门禁未抛出异常，定向测试按预期为 `1 failed in 0.42s`，退出码 `1`。
- 实现：`validate_sensitivity_scenario` 现在调用通用 `validate_source_hashes`，并在通过结果中记录 provenance 检查摘要。
- 绿灯：`tests/test_submission_evidence_gates.py` 为 `14 passed in 0.51s`；Ruff 为 `All checks passed!`；radon 未报告 C 级代码块。
- 当前总门禁：重新运行后仍按预期退出码 `1`，失败项精确保持为 3 个待重建审计工件和 8 个尚未生成的敏感性场景；off-grid 与 equilibrium branch 通过。门禁脚本 SHA-256 更新为 `595ff0186f2ff8a7b9fe5f4ee159c63d0502d80c53e40b59258a44567781111e`。
- 状态：gate_behavior_verified；expected_failures_11

### 2026-07-14 21:56 - 下一波敏感性缓存签名核验

- 目标：确认 `capacity_low` 与 `price_sensitivity_high` 的早期缓存可由冻结源码安全接续。
- 方法：按 `run_equilibria` 的场景字典、连续中间商响应配置和八个缓存来源文件重新计算 uniform/dynamic 签名；只读反序列化本地可信 pickle，不调用会弹出记录的缓存加载函数。
- 结果：四个缓存均为 format version 1，且签名全部匹配当前冻结源码。`capacity_low` 已有 95 个 uniform 和 676 个 dynamic pair；`price_sensitivity_high` 已有 63 个 uniform 和 676 个 dynamic pair。
- 决策：当前两组结束后优先启动这两个场景，以复用已验证缓存；仍保持最多两个全量场景并行。
- 状态：verified；next_wave_ready

### 2026-07-14 21:57 - 九场景 TeX 表生成器 TDD

- 目标：让主稿中的全量敏感性数字直接由唯一 summary JSON 生成，避免人工转录。
- 红灯：新增九行顺序、标签、来源哈希和计数测试；生成模块尚不存在时按预期 `2 failed in 0.26s`，退出码 `1`。
- 实现：新增 `experiments/build_submission_sensitivity_table.py`。生成器固定 baseline 加八扰动的顺序，要求 788 个候选与九个场景，逐行报告两种价格制度中的最大有限 regret、最大固定点残差、峰值/利用率/QoS/利润变化，并在 TeX 注释中写入 summary SHA-256。
- 绿灯：`tests/test_submission_sensitivity_table.py` 为 `2 passed in 0.17s`；Ruff 通过；radon 无 C 级代码块。实现文件 106 行，测试文件 68 行。
- 边界：正式 summary 尚未生成，因此当前不创建正式表文件，也不把 `\\input` 加入主稿。
- 状态：generator_verified；formal_table_pending

### 2026-07-14 22:00 - SMPT 官方投稿要求复核

- 来源：Elsevier/ScienceDirect 官方 [SMPT Guide for Authors](https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors)，2026-07-14 在线复核。
- 已满足：摘要不超过 250 词且无引用；关键词 7 个；正文分级编号；公式和表格可编辑；图表均需正文引用并单独提供；Highlights 为 3--5 条且每条不超过 85 字符；生成式 AI 使用声明位于参考文献之前。
- 图像政策：官方不允许用生成式 AI 创建或修改投稿图。最终 Figure 1 为 Draw.io 可编辑矢量图，使用有 CC BY 4.0 署名的 Streamline 图标；当前声明与实际制作过程一致。
- 新确认的阻塞：期刊采用 single-anonymized review，正式 title page 必须有作者、单位、完整邮政地址和通讯作者信息；`Anonymous Author` 仅能用于内部审阅。研究数据适用 Option C，需要相关仓储链接和文内引用，或说明无法共享的原因。
- 决策：最终数值门禁通过后建立 GitHub 冻结 release，并优先连接 Zenodo DOI；作者、Funding、CRediT、competing interests 和 ORCID 继续等待真实信息，不作推测。
- 状态：official_requirements_verified；metadata_and_repository_pending

### 2026-07-14 22:02 - 英式英语一致性检查

- 工具边界：当前 WSL 未安装 `aspell`、`hunspell` 或 `codespell`；未为单次文案检查增加系统或项目依赖。
- 替代检查：扫描 utilisation/utilization、optimisation/optimization、behaviour/behavior、modelling/modeling、normalised/normalized、licence/license 等英美变体。
- 结果：正文采用英式拼写；检测到的 `center` 来自 LaTeX 环境，`Color` 来自 `Streamline Ultimate Color` 品牌名，不作修改。
- 修改：将引言中一处 `continuously optimises` 改为明确的“在有界连续域上优化”，与摘要和方法对策略空间的描述一致。
- 编译：再次运行 `latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex`，退出码 `0`；PDF 为 19 页、402,965 bytes，日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。
- 状态：verified；dictionary_spellchecker_unavailable

### 2026-07-14 22:06 - 主稿引用键与占位符检查

- 结果：主稿共有 57 次引用、38 个不同引用键；`verified_refs.bib` 中 68 个条目。缺失引用键为 0，重复 BibTeX 键为 0。
- 共享库边界：30 个未引用条目来自仓库共用参考文献库，BibTeX 不会把它们写入本稿参考文献列表，不影响当前 PDF。
- 永久链接检查：38 个被引条目中，只有 McFadden 1974、Anderson et al. 1992、Train 2009 和 Fudenberg--Tirole 1991 没有 DOI/URL 字段；它们是经典书籍或书章，不视为链接缺失错误。
- 已知占位：仅剩 `Anonymous Author` 和敏感性结果注释。前者等待真实作者元数据，后者等待九场景全量重求；未发现其他 TODO/TBD/FIXME/PLACEHOLDER。
- 状态：verified；known_placeholders_2

### 2026-07-14 22:07 - 证据映射 provenance 状态纠正

- 文件：`docs/reviews/smpt_submission_evidence_map_2026-07-14.md`。
- 修改：加入数值源码冻结提交 `6f483084178c3934d1340ba95cd469ae9dd1141d` 与 20 个来源 blob 零差异核验；把机制分解状态拆为“数值内容仍绑定基线”和“重构后 provenance 工件待重建”。
- 待办：固定点、中间商和机制分解三个工件必须按完整依赖哈希清单重跑后，才能由最终证据门禁接受。
- 状态：evidence_map_current

### 2026-07-14 22:11 - 近期推理市场文献出版状态复核

- 已正式发表：PriLLM 为 AAAI 2026 论文，BurstGPT 为 KDD 2025 论文；BibTeX 含正式 DOI、卷期或页码。
- 报告/预印本：Demirer et al. 为 NBER working paper；Bergemann et al.、Yan et al. 和 Cunningham 为明确标注 `arXiv preprint` 的条目。
- 结果：正文仅使用 `recent studies`、`work` 和 `models` 等中性描述，没有把预印本写成已同行评审共识；参考文献字段已按官方要求标明预印本状态。
- 状态：verified

### 2026-07-14 22:26 - 长检查点块活性核验

- 现象：`capacity_high` 与重启后的 `price_sensitivity_low` 自 17,060-pair 检查点后超过一小时尚未写入下一 8,192-pair 检查点。
- 检查：读取两个进程组中 28 个 `spawn_main` worker 的 `/proc/<pid>/stat`，比较 10 秒内累计 user+system CPU jiffies。
- 结果：`start_jiffies=19141804`、`end_jiffies=19173532`、`delta_10s=31728`，系统 `CLK_TCK=100`。所有 worker 仍在持续计算；日志无异常，内存 PSI 仍为 0。
- 决策：不重启，不丢弃本块未落盘进度。下一场景仅在当前任一场景完成或写入可恢复检查点后启动。
- 状态：active_compute_verified

### 2026-07-14 22:33 - 两场景第三恢复检查点

- `price_sensitivity_low`：22:27:01 写入 25,252 个 dynamic pair，缓存 134,251,312 bytes。
- `capacity_high`：22:30:32 写入 25,252 个 dynamic pair，缓存 134,252,779 bytes。
- 进度参考：两者均达到 25,252 records，相当于基线最终 46,381 个已评估 pairs 的 54.44%；场景自身的最终 pair 数仍由其 double-oracle 路径决定。uniform 缓存已在早期阶段完成或可恢复。
- 决策：保持 12+16 worker。当前 28 个计算 worker 已接近 32 个逻辑处理器的有效上限，不为 `price_sensitivity_low` 增加 worker，以免降低总体吞吐。
- 状态：checkpointed；in_progress

### 2026-07-14 22:40 - 理论公式与冻结实现定向复核

- 范围：复核 `spatiotemporal_mechanism.py`、`peak_shaving_market.py`、`peak_shaving_equilibrium.py` 与英文主稿方法部分的对应关系。
- 结果：时间迁移质量守恒、两阶段 logit 选择、中间商路由、服务商负载、QoS 退化、联合固定点和三方利润的符号、参数位置及单位解释均与主稿一致，未发现需要修改冻结数值源的新问题。
- 证据边界：Brouwer 论证只保证声明域内至少存在一个固定点；32 初值数值审计未观察到多分支，但不构成解析唯一性证明。有限候选 regret 与 off-grid 检查也不构成连续策略空间均衡证明。
- 运行状态：22:36 检查时，`price_sensitivity_low` 与 `capacity_high` 的退出哨兵均未生成；两个进程组最近检查点均为 25,252 records。以基线最终 46,381 个已评估 pairs 为参照是 54.44%，不是场景固定完成比例。
- 决策：保持冻结源码和 12+16 worker，不启动第三个场景，不为当前 SciPy/Python 回调求解器引入未经等价性验证的 GPU 路径。
- 状态：verified；sensitivity_in_progress

### 2026-07-14 22:45 - 灵敏度表版面门禁修复

- 预检：用九场景测试数据生成临时 TeX 表并在 A4、10 pt、2.5 cm 页边距下独立编译。首次编译退出码 `0`，但日志出现 `Overfull \\hbox (27.42676pt too wide)`。
- 红灯：测试新增局部列间距要求后，`tests/test_submission_sensitivity_table.py` 按预期为 `1 failed, 1 passed`，退出码 `1`。
- 修复：生成器在表环境内设置 `\\tabcolsep=3pt`。该设置只影响此表，保留原始文字和可编辑 LaTeX 数值，不缩放整张表。
- 绿灯：定向测试 `2 passed`；临时 TeX 重新编译后无 overfull、underfull、LaTeX Error 或 undefined control sequence；Ruff 通过，radon 无 C 级代码块。
- 边界：测试数字仅位于 `/tmp` 临时文件，未写入论文或正式工件。正式表仍等待九场景 summary。
- 状态：verified；table_layout_ready

### 2026-07-14 22:47 - 普通科研英语复核与终稿预门禁

- 语言检查：对 25--40 词句段做 `detex` 扫描；多数命中由标题或公式拼接产生。将“多个数值候选的选择规则”和“有限博弈 regret 与 follower audit 的精度边界”各拆为两个短句，算法顺序、阈值和数字未改变。
- 编译命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp latexmk -xelatex \
    -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 `0`；PDF 为 19 页、402,932 bytes，日志无 LaTeX Error、undefined citation/reference、overfull 或 underfull。
- 终稿测试：`tests/test_final_manuscript_20260714.py` 为 `4 passed, 2 failed`。两个失败精确对应尚未生成并引用的 `resolved_sensitivity.pdf` 以及仍保留的 `FINAL_SENSITIVITY_RESULTS` 注释，属于九场景完成前的预期红灯。
- 命令边界：本次组合 shell 命令末尾为 `pdfinfo`，因此外层退出码显示 `0`；pytest 子命令本身返回失败。后续门禁命令将显式保留测试退出状态。
- 状态：latex_verified；final_gate_expected_red

### 2026-07-14 22:48 - 线性分时价格方向审计

- 输入：正式基线工件 `spatiotemporal_equilibrium_submission.json`，只读检查 dynamic mixed equilibrium 的正概率支持和 676 个活跃联合剖面。
- 服务商 A：26 个正概率策略；概率加权系数均值为 `(0.270812, 0.640114, 0.549157, 0.302764)`；批发斜率零质量为 2.773%，负斜率质量为 0。
- 服务商 B：26 个正概率策略；概率加权系数均值为 `(0.252020, 0.434409, 0.536780, 0.479631)`；批发斜率零质量为 29.936%，负斜率质量为 0。
- 中间商：概率加权零售价基价为 0.657762，斜率为 0.188472；活跃剖面的零售价斜率范围为 `[0.069344, 0.292035]`，零斜率和负斜率概率质量均为 0。`beta=0` 的质量为 29.002%，该边界已在正文单独披露。
- 结论：主结果确实来自随归一化负载形状上升的线性分时价格规则，而不是反向价格或逐时段网格价格。正文已明确混合分布及均值的描述性边界，无需修改冻结数值源。
- 状态：verified

### 2026-07-14 22:52 - A4 PDF 图表视觉抽检

- 页码定位：通过 `pdftotext -layout` 确认 Figure 1 位于第 4 页，Tables 2--3 位于第 7、9 页，Figures 2--5 位于第 10、12、13、14 页。
- 失败：尝试用 ImageMagick `montage` 和 `identify` 生成接触表时，WSL 返回 `command not found`；未安装系统包，也未修改环境。
- 替代检查：用 `pdftoppm -r 120` 在 `/tmp` 生成七页 PNG，并逐页按原始分辨率检查。
- 结果：框架图节点和直角连线无重叠；图 2--5 的图例、面板标识、误差线、阈值线和坐标文字可读；候选集表与参数表未越界；正文、图题和相邻段落无遮挡。Figure 4(c) 的斜置标签较紧但仍可辨识，当前不需要重绘。
- 字体：`pdffonts` 确认五张正式图均嵌入 `TimesNewRomanPSMT`；框架图同时嵌入 Times New Roman 的常规、粗体、斜体和粗斜体字形。
- 边界：Figure 6 尚待九场景 summary 生成，未纳入本次视觉检查。
- 状态：verified；figure6_pending

### 2026-07-15 15:50 - WSL 重启中断与持久缓存恢复

- 现象：继续任务后发现旧的两个退出哨兵仍为 pending，但相关进程、`/tmp/peak_shaving_submission_sensitivity` 和 25,252-pair 检查点均不存在，也没有生成场景正式 JSON。
- 触发条件：`uptime -s` 显示当前 WSL 实例于 `2026-07-15 14:31:35` 重新启动；旧缓存位于易失的 `/tmp`，因此 WSL 生命周期结束时被清除。
- 影响：`price_sensitivity_low` 与 `capacity_high` 的 54.44% 中间进度不能恢复，也不能计入论文证据；冻结基线、代码提交、正式工件和日志均未丢失。
- 来源复核：HEAD 仍为 `6f483084178c3934d1340ba95cd469ae9dd1141d`。20 个基线来源文件对正式工件和冻结提交均为零哈希差异，灵敏度入口也与冻结提交一致：`SOURCE_COUNT=20 WORK_MISMATCH=0 COMMIT_MISMATCH=0 SENSITIVITY_MATCH=true`。
- 存储修正：新缓存根目录为 `/root/.cache/peak_shaving_submission_sensitivity`，位于 WSL 持久文件系统；根文件系统可用空间约 464 GiB。`/tmp` 只继续用于 Python 临时文件。
- 重启命令边界：用冻结入口分别调用 `run_sensitivity(..., cache_root=Path("/root/.cache/peak_shaving_submission_sensitivity"))`；`price_sensitivity_low` 使用 12 worker，`capacity_high` 使用 16 worker，线程库均限制为 1。
- 启动结果：两个独立进程组已运行，退出哨兵 pending；15:50 已分别写入 63-pair uniform 检查点。正式日志为 `sensitivity_price_sensitivity_low_persistent.log` 和 `sensitivity_capacity_high_persistent.log`。
- 检查失败与修正：首次只读 pickle 计数误用键 `entries`，返回 `KeyError`；检查结构后改用实际键 `records`，两份缓存均为 format version 1、63 条记录。
- 状态：restarted_from_zero；persistent_checkpointing_active

### 2026-07-15 15:54 - Figure 6 场景标签与顺序门禁

- 问题：预设横轴用 `Price`、`Move` 和 `QoS` 表示价格敏感度、迁移成本和 QoS 阈值，可能被误读为价格水平、迁移量和 QoS 本身。
- 红灯：测试先要求明确标签常量，模块尚未导出该常量时按预期返回 `ImportError`，定向测试退出码 `1`。
- 修复：标签改为 `Price sens.`、`Mig. cost` 和 `QoS thr.`；Figure 6 同时要求输入行严格遵循 baseline 加八扰动的正式 `SCENARIO_ORDER`，顺序错误直接失败。
- 绿灯：标签定向测试通过；Ruff 为 `All checks passed!`，radon 未报告 C 级代码块。图生成器保持 300 行，没有超过项目文件上限。
- 边界：正式 Figure 6 仍不生成，直到九场景 summary 通过证据门禁。
- 状态：verified；figure6_generator_ready

- 完整图生成测试：`tests/test_final_submission_figures.py` 为 `7 passed, 2 failed`，退出码 `1`。两个失败均由正式 `spatiotemporal_sensitivity_submission.json` 尚不存在触发；生成器没有回退到旧敏感性文件或测试数据，符合当前证据门禁设计。

### 2026-07-15 15:56 - 八场景验证队列

- 目的：当前两组结束后自动继续其余六组，同时保证失败场景不会被跳过。
- 队列脚本：`/root/.cache/peak_shaving_submission_sensitivity/run_validated_branch.sh`，属于本机运行控制文件，不进入论文仓库或正式源码哈希。`bash -n` 语法检查通过。
- 价格分支：等待并验证 `price_sensitivity_low`，随后以 12 worker 顺序运行并验证 `price_sensitivity_high`、`migration_cost_low`、`qos_threshold_low`。
- 容量分支：等待并验证 `capacity_high`，随后以 16 worker 顺序运行并验证 `capacity_low`、`migration_cost_high`、`qos_threshold_high`。
- 单场景门禁：baseline SHA-256 必须匹配；源码哈希必须匹配当前冻结文件；候选数必须为 788；uniform/dynamic 均须 full-grid verified、regret 不高于 `1e-7`、最大联合残差不高于 `1e-8`。
- 运行结果：两个 supervisor 进程已启动，日志分别为 `sensitivity_price_branch_queue.log` 与 `sensitivity_capacity_branch_queue.log`，当前均处于等待首场景状态。
- 失败行为：当前首场景退出码非零时分支写入非零 queue exit 并停止；后续场景的运行或验证命令受 `set -euo pipefail` 约束，任一失败即停止，不继续生成剩余结果。
- 状态：active；validated_sequential_queue

### 2026-07-15 15:57 - 首个持久 dynamic 检查点

- `price_sensitivity_low`：uniform 63 records，dynamic 676 records；format version 1；dynamic cache 3,594,084 bytes。
- `capacity_high`：uniform 63 records，dynamic 676 records；format version 1；dynamic cache 3,594,099 bytes。
- 资源：可用内存约 11 GiB，swap 余量约 3.2 GiB，memory PSI 的 10/60/300 秒均为 0。
- 解释：676 records 是基线 26-by-26 正概率支持笛卡尔积的首个 dynamic 状态；后续 double oracle 在周期检查点或求解阶段边界写入同一持久缓存。
- 状态：checkpointed；in_progress

### 2026-07-15 16:04 - 持久缓存运行活性核验

- 方法：比较两个计算进程组全部进程在 10 秒内的 `/proc/<pid>/stat` user+system CPU jiffies。
- 结果：`start_jiffies=1522768`、`end_jiffies=1553339`、`delta_10s=30571`，`CLK_TCK=100`，相当于该窗口持续使用约 30.6 个逻辑核心。
- 资源：两个进程组常驻内存约 1.23/1.55 GiB；系统可用内存约 11 GiB，memory PSI 为 0。
- 结论：任务处于正常计算状态，不是日志停滞或死锁；保持当前 12+16 worker。
- 状态：active_compute_verified

### 2026-07-15 16:45 - capacity_high 持久检查点

- `capacity_high` 于 16:44:32 将 dynamic cache 从 676 扩展到 8,868 records，文件大小 47,146,726 bytes；相当于基线最终已评估 pairs 的 19.12%，仅作进度参照。
- cache format version 为 1，签名为 `eb5d70d540b153d90c3ab1b109d7c7b298eb2bb297771625194221dc2aef2fae`；日志记录与 pickle 计数一致。
- `price_sensitivity_low` 仍为 676 records，两个退出哨兵均为 pending；保持当前并发，不启动额外场景。
- 状态：checkpointed；in_progress

### 2026-07-15 17:02 - price_sensitivity_low 持久检查点

- `price_sensitivity_low` 于 17:02:08 将 dynamic cache 从 676 扩展到 8,868 records，文件大小 47,146,306 bytes；相当于基线最终已评估 pairs 的 19.12%，仅作进度参照。
- cache format version 为 1，签名为 `ba8bf820468f2b59930b93c8da3ea691abbb50f1b34c224c01eb9759b41fcd70`；日志记录与 pickle 计数一致。
- 当前两场景均为 8,868 records；退出哨兵 pending，验证队列尚未进入下一场景。
- 状态：checkpointed；in_progress

### 2026-07-15 17:40 - capacity_high 第二持久检查点

- `capacity_high` 于 17:39:44 将 dynamic cache 扩展到 17,060 records，文件大小 90,699,795 bytes；相当于基线最终已评估 pairs 的 36.78%，仅作进度参照。
- format version 1 与场景签名 `eb5d70d...2fae` 均保持不变；日志和 pickle 计数一致。
- `price_sensitivity_low` 仍为 8,868 records；两分支均继续运行。
- 状态：checkpointed；in_progress

### 2026-07-15 18:11 - price_sensitivity_low 第二持久检查点

- `price_sensitivity_low` 于 18:10:37 将 dynamic cache 扩展到 17,060 records，文件大小 90,698,749 bytes；相当于基线最终已评估 pairs 的 36.78%，仅作进度参照。
- format version 1 与签名 `ba8bf820...fcd70` 保持不变；日志和 pickle 计数一致。
- 当前两个场景均为 17,060 records，两个退出哨兵仍为 pending。
- 状态：checkpointed；in_progress

### 2026-07-15 18:34 - capacity_high 第三持久检查点

- `capacity_high` 于 18:33:11 将 dynamic cache 扩展到 25,252 records，文件大小 134,252,779 bytes；相当于基线最终已评估 pairs 的 54.44%，仅作进度参照。
- format version 1 与场景签名保持不变；该进度现已位于 WSL 持久缓存，而非易失 `/tmp`。
- `price_sensitivity_low` 仍为 17,060 records；退出哨兵均为 pending。
- 状态：checkpointed；in_progress

### 2026-07-15 19:17 - price_sensitivity_low 第三持久检查点

- `price_sensitivity_low` 于 19:16:28 将 dynamic cache 扩展到 25,252 records，文件大小 134,251,312 bytes；相当于基线最终已评估 pairs 的 54.44%，仅作进度参照。
- format version 1 与场景签名保持不变；日志和 pickle 计数一致。
- 两个场景现在均已在持久缓存中达到并超过此前易失缓存的最高进度。
- 状态：checkpointed；in_progress

### 2026-07-15 19:18 - capacity_high 第四持久检查点

- `capacity_high` 于 19:17:28 将 dynamic cache 扩展到 33,444 records，文件大小 177,804,527 bytes；相当于基线最终已评估 pairs 的 72.11%，仅作进度参照。
- format version 1、场景签名和日志计数一致；场景最终评估数取决于后续 oracle 偏离集合，不能由基线 46,381 机械外推。
- 状态：checkpointed；in_progress

### 2026-07-15 20:00 - capacity_high 阶段边界检查点与进度定义修正

- `capacity_high` 于 19:58:51 写入 40,300 records，文件大小 214,254,572 bytes；format version 1、场景签名 `eb5d70d...2fae` 和日志计数一致。
- 发现：该次增量为 6,856，而非固定 8,192，说明缓存还会在 double-oracle 阶段边界写入。不同敏感性场景的支持扩展路径不同，最终 evaluated-pair 数不必等于基线的 46,381。
- 修正：将本轮及昨日 README 中的百分比统一改为“相对基线最终已评估 pair 数的进度参照”，不再表述为场景完成比例。
- 完成标准：只接受场景进程退出码 0、正式 JSON 写入、baseline/source 哈希匹配、788 候选、uniform/dynamic full-grid verified、regret 不高于 `1e-7` 和残差不高于 `1e-8`。
- 状态：checkpointed；progress_semantics_corrected

### 2026-07-15 20:03 - capacity_high oracle 尾部

- 缓存于 20:02:34 增至 41,063 records；日志依次记录 40,300、41,062 和 41,063，说明求解已进入新增偏离与受限博弈更新交替进行的尾部阶段。
- 决策：不再为单 pair 阶段写入逐条登记；该场景后续只以进程退出码、正式 JSON 和证据门禁判定完成。
- `price_sensitivity_low` 仍在 25,252-record 计算块中。
- 状态：in_progress；awaiting_formal_artifact

### 2026-07-15 20:19 - price_sensitivity_low 第四检查点与 capacity_high 继续扩展

- `price_sensitivity_low` 于 20:18:04 写入 33,444 records，文件大小约 170 MiB；日志确认该阶段写入成功。
- `capacity_high` 的 oracle 尾部继续写入 42,584 和 42,585 records，当前文件约 216 MiB；退出哨兵仍为 pending。
- 两次通过 `uv run` 只读反序列化两份较大 pickle 的探针只返回 uv warning，没有返回预期计数，也没有错误文本；该探针不作为验证证据。随后直接检查日志和文件时间戳，二者状态正常。
- 决策：运行中不再频繁反序列化大型缓存。最终只读取写完的正式 JSON，并由门禁验证。
- 状态：checkpointed；in_progress

### 2026-07-15 21:10 - 两场景进入扩展 oracle 尾部

- `price_sensitivity_low` 于 21:10:03 写入 40,300 records，开始从大块 pair evaluation 转入新增偏离与交叉项的阶段更新。
- `capacity_high` 于 21:09:17 已扩展到 51,675 records；自 40,300 后持续以新增候选偏离和交叉项成对写入，尚未退出。
- 解释：两个扰动场景均需要比基线更多的已评估策略对，进一步证明场景进度不能用基线 46,381 作为固定终点。
- 论文边界：在正式 JSON、full-candidate regret 与 residual 门禁通过前，不把支持扩展规模解释为经济结果或稳健性证据。
- 状态：in_progress；oracle_support_expanding

### 2026-07-15 21:14 - worker 池状态复核

- 触发：一次 `ps` 聚合在 pool 切换瞬间看到价格进程组较多历史子进程，生命周期平均 CPU 和共享页 RSS 求和不适合作为瞬时资源指标。
- 复核：10 秒 `/proc` jiffies 增量为价格组 9,446、容量组 17,477，总计 26,923（`CLK_TCK=100`）。检查末端分别为 12 和 16 个活跃 `spawn_main` worker，另有父进程与 resource tracker。
- 资源：系统实际已用内存约 8 GiB、可用约 7.1 GiB，memory full pressure 为 0；没有持续的 worker 泄漏或内存停顿证据。
- 决策：保持 12+16 worker，不依据 `ps` 生命周期平均值调整并发。
- 状态：active_compute_verified

### 2026-07-15 22:46 - capacity_high 正式完成并通过门禁

- 输出：`sensitivity_capacity_high_submission.json`，生成时间 `2026-07-15T22:44:07+08:00`，SHA-256 `0a2a065ab6dc937cf2c56ab32363e3b65365d5663e3f4a0d4ae819c875446be2`。
- 来源：baseline SHA-256 为 `d371744...aae2f`，候选数 788；provenance 门禁检查 20 个来源文件，全部匹配冻结源码。
- 数值门禁：uniform regret `0`、残差 `6.07e-10`；dynamic regret `2.27e-13`、残差 `9.95e-10`；均为 full-grid verified。dynamic 评估 65,919 pairs，正概率支持 10-by-10，停止原因为 `regret_tolerance`。
- 结果：相对该场景统一定价，aggregate peak `-12.9523%`，maximum provider utilisation `-8.4640%`，minimum provider QoS `+0.029145`，market-side profit `+27.6953%`。
- 解释边界：QoS 与峰值方向仍为改善，但利润符号与 baseline 的 `-2.81%` 相反，支持“利润效应不稳健”的结论；单个扰动尚不能代表全部八场景。
- 队列：容量分支已验证该工件并自动启动 `capacity_low`，16 worker；其 uniform 持久缓存已写入 95 records。
- 状态：verified；scenario_1_of_8

### 2026-07-14 23:15 - Figure 6 场景标签语义修正

- 问题：预设标签 `Price`、`Move` 和 `QoS` 容易被理解为价格水平、迁移量和 QoS 结果，而实际扰动对象分别是价格敏感度、迁移成本和 QoS 阈值。
- 红灯：测试先要求公开并锁定九个精确标签；常量尚不存在时按预期因 `ImportError` 失败，退出码 `1`。
- 修复：新增 `SENSITIVITY_LABELS`，改为 `Price sens.`、`Mig. cost` 和 `QoS thr.`；图中数据字段、顺序、颜色和数值均未改变。实现文件为 298 行，未超过 300 行门禁。
- 绿灯：定向标签与图生成测试 `1 passed`；Ruff 通过。完整图测试为 `6 passed, 2 failed`，两个失败只因正式 `spatiotemporal_sensitivity_submission.json` 尚未生成，符合当前门禁状态；radon 无 C 级函数。
- 状态：label_logic_verified；formal_sensitivity_artifact_pending

### 2026-07-14 23:27 - Figure 6 场景顺序门禁

- 风险：绘图器此前按 JSON 行位置赋予横轴标签，但未核对 `scenario` 字段；行被重排时会静默错标。
- 红灯：新增逆序九场景测试后，绘图器未抛出异常，定向测试按预期失败，退出码 `1`。
- 修复：Figure 6 与 TeX 表共同使用 `SCENARIO_ORDER`；绘图前逐行核对场景名，顺序或名称不一致即拒绝生成。
- 绿灯：正确顺序和逆序拒绝两项测试均通过；Ruff 通过，radon 无 C 级函数。绘图文件保持 300 行，满足文件长度门禁。
- 状态：verified；figure_table_order_locked

### 2026-07-15 23:33 - 双分支持久计算检查

- `price_sensitivity_low` 已写入 55,441 个 dynamic cache records；最近检查点时间为 23:28:22，退出哨兵仍为 pending。
- `capacity_low` 已写入 8,868 个 dynamic cache records；最近检查点时间为 23:32:28，容量队列继续使用 16 workers。
- 进程复核：价格分支 supervisor、12-worker 求解进程组与容量分支 supervisor、16-worker 求解进程组均存活；没有重复启动同一场景。
- 一次仅执行 `sleep` 和状态读取的监控 shell 曾以退出码 `143` 结束。该会话不持有缓存、不参与求解，计算进程组与正式工件不受影响；后续改用新的只读状态检查。
- GPU 决策：当前算法由 SciPy L-BFGS-B、NumPy 和大量 8-period Python fixed-point 回调组成，仓库没有经过数值等价验证的 CUDA 实现。为保持冻结来源哈希与结果可比性，本轮继续使用 CPU；不把可用 RTX 4090 强行用于不适配的细粒度求解。
- 完成判据保持不变：退出码 0、正式场景 JSON、20 个冻结来源哈希匹配、788 个候选、full-grid verified，以及 regret/residual 门禁全部通过。
- 状态：in_progress；scenario_1_of_8_verified

### 2026-07-15 23:41 - 终稿结构、语言与资源门禁复核

- 结构：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 仍只有五个编号主章节；数据/代码可用性与 AI 使用声明为不编号投稿声明。
- 测试：运行 `TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run pytest -q tests/test_final_manuscript_20260714.py`，结果为 `4 passed, 2 failed`。两个失败分别要求正式 `resolved_sensitivity.pdf` 与删除 `FINAL_SENSITIVITY_RESULTS` 占位，均是八场景完成前有意保留的终稿红灯。
- 语言：高频 AI 模板词扫描无命中，英式 `modelling` 未与美式 `modeling` 混用；保守句长扫描未发现超过 30 个词的正文句子。57 个引用位置对应 38 个唯一 BibTeX key，缺失 key 为 0。
- skill：已加载 `nature-reviewer`、`nature-polishing` 的 research/section/English/generic 片段及 `humanizer`。`nature-polishing/manifest.yaml` 指向的四个 `../_shared/core/` 文件在当前 skill 安装中不存在，命令返回 `No such file or directory`；本轮不声称使用这些缺失片段。
- 资源：价格和容量进程组分别有 12 与 16 个活跃 workers；约 10 GiB 内存可用，CPU 和 memory pressure 的 10/60/300 秒平均值均为 0。保持现有并发。
- 决策：敏感性完成前不修改摘要与结论数字，不用已完成的单个 `capacity_high` 场景概括八场景范围。
- 状态：audit_recorded；formal_sensitivity_pending

### 2026-07-15 23:42 - capacity_high 解释层一致性检查

- 输入：`sensitivity_capacity_high_submission.json`；该工件此前已通过来源、候选、regret 与 fixed-point 门禁。
- 操作：只读检查 uniform/dynamic 混合概率质量、总需求、价格/QoS/路由范围，以及三方利润与 `aggregate market-side profit` 的加总关系。
- 结果：两种策略的概率质量均为 `1.0`；总需求分别为 `1100.0` 和 `1100.0000000000005`。利润分项加总误差分别为 `0` 和 `-4.55e-13`。
- 范围：动态期望零售价 `[0.5447, 0.7110]`、直连价格 `[0.45, 0.7402]`、批发价格 `[0.25, 0.3445]`、路由份额 `[0.4050, 0.5950]`；均位于声明边界内。QoS 最大值为 `1+2e-16`，属于浮点舍入。
- 决策：该场景 `+27.6953%` 的利润变化不是概率未归一、需求不守恒或利润漏加造成；仍只作为利润符号敏感的单场景证据。
- 状态：verified；accounting_and_bounds_consistent

### 2026-07-15 23:43 - TeX 自包含性与均衡表达复核

- 标签：主稿共有 46 个标签，全部唯一；不存在引用到缺失标签的情况。当前 5 张正式图和 6 张表均有正文引用。
- 公式：Nash 部分已给出两方最佳响应不等式、支持互补条件、Fischer--Burmeister 数值系统、双方 full-candidate regret 与 double-oracle 停止条件。该内容足以解释有限候选混合均衡如何定义和计算。
- 边界：正文没有把上述数值系统写成连续策略解析证明，也没有声称枚举所有双矩阵均衡；与 branch multistart 和 off-grid 审计范围一致。
- 编译日志：未检出 `LaTeX Warning`、undefined reference/citation、overfull 或 underfull box。
- 决策：不为形式完整性增加不受证据支持的连续空间均衡定理；保留现有有限博弈定义、存在性范围和数值证书。
- 状态：verified；self_contained_theory_and_cross_references

### 2026-07-15 23:45 - 八场景验证后自动收尾

- 目标：避免长时间计算结束后遗漏场景验证、汇总顺序或 Figure 6 生成，同时不触碰冻结数值源码。
- 新增仓库外运维脚本：`/root/.cache/peak_shaving_submission_sensitivity/finalize_validated_sensitivity.sh`。脚本不属于正式来源清单，不进入论文工件 provenance。
- 流程：等待 `price_branch_queue.exit` 与 `capacity_branch_queue.exit`；若 supervisor 无哨兵退出或任一分支非零则停止。两个分支均成功后，重新验证八个正式场景，原子写入九行汇总，再生成可编辑 LaTeX 表与 `resolved_sensitivity.pdf/.png`。
- 验证：`bash -n /root/.cache/peak_shaving_submission_sensitivity/finalize_validated_sensitivity.sh` 返回 0；独立 finalizer PID 为 `100187`，日志为 `sensitivity_finalization.log`，退出哨兵为 `sensitivity_finalization.exit`。
- 边界：该脚本不自动改摘要、结果解释或结论；正文仍须在九场景数据审阅后人工写入，并重新执行完整证据与 LaTeX 门禁。
- 状态：in_progress；automated_post_validation_ready

### 2026-07-15 23:47 - 冻结数值来源复杂度复核

- 首次审计命令误写了不存在的 `pricing_sim/spatiotemporal_market.py`，AST 检查以 `FileNotFoundError` 退出；该失败不作为复杂度结论。随后改为直接读取基准工件记录的来源清单。
- 正确范围：20 个来源条目中有 18 个 Python 文件。`experiments/final_equilibrium_tools.py` 为 310 行；12 个既有函数超过 50 个源码行。
- radon：7 个函数为 C/D，包括 `run_equilibria` C(19)、`PairEvaluator.evaluate_many` C(15)、`enumerate_bimatrix_equilibria` D(22) 和 `adaptive_audit_provider_candidate_grid` D(30)。
- 决策：这些函数是已冻结并产生基准与敏感性工件的既有代码。计算途中进行结构重构会使来源哈希和全部场景 provenance 失效，因此本轮不修改数值来源。可信度继续由冻结 commit、逐文件 SHA-256、回归测试、finite regret、fixed-point residual 和独立审计建立。
- 后续：全量结果完成后，区分“投稿数值来源冻结”与“后续行为不变的工程重构”；不得用未重跑的工件为重构后源码背书。
- 状态：recorded；pre_existing_complexity_debt

### 2026-07-16 00:06 - price_sensitivity_low 扩展检查点

- `price_sensitivity_low` 于 2026-07-15 23:57:00 将 dynamic cache 扩展至 58,445 records，文件大小 310,710,407 bytes；日志按 58,444/58,445 的 oracle 阶段边界成对写入。
- `capacity_low` 仍在 8,868 records 后的大块计算中；12/16-worker 两个进程组没有退出信号。
- `price_sensitivity_low.exit`、两个 branch queue exit 和 `sensitivity_finalization.exit` 均为 pending；正式场景工件仍只有已验证的 `capacity_high`。
- 文件命名决策：新英文终稿只在全部门禁通过后按实际完成日期创建，不把 2026-07-14 候选稿直接改称终稿。
- 状态：checkpointed；scenario_1_of_8_verified

### 2026-07-16 00:15 - 长轮询退出与计算存活复核

- 一次只读 `sleep/status` 长轮询在约 211 秒后以退出码 `143` 结束；没有输出场景错误，也不持有 pair cache。后续不再使用长 `write_stdin` 轮询，改为独立短状态命令。
- 直接进程复核：价格求解 PID `23324`、price/capacity supervisors `24917/24918` 和 finalizer `100187` 均存活；四个退出哨兵仍为 pending。
- `price_sensitivity_low` 于 00:07:06 写入 59,944 records，文件大小 318,678,430 bytes；`capacity_low` 仍在 8,868 records 后的大块计算中。
- 影响：监控退出不影响求解、持久缓存、正式工件或自动收尾流程。
- 状态：monitor_failure_isolated；compute_in_progress

### 2026-07-16 00:19 - 禁用长等待监控并确认新检查点

- 再次尝试 120 秒只读 `sleep/status`，工具层在约 70 秒后以退出码 `143` 终止；该会话仍不属于求解进程组。由此确认当前工具环境不适合长等待会话，后续仅在自动续轮时执行瞬时检查。
- 存活复核：价格求解 PID `23324`、两个 supervisors `24917/24918` 和 finalizer `100187` 均存活。
- 实际进展：`price_sensitivity_low` 于 00:18:48 将 dynamic cache 写入 61,441 records，文件大小 326,635,971 bytes；日志记录 61,440/61,441 阶段边界。
- `capacity_low` 仍在 8,868 records 后的大计算块中，尚无错误或正式退出信号。
- 状态：checkpointed；long_polling_disabled

### 2026-07-16 00:21 - 敏感性完成后的审计流水线

- 新增仓库外脚本：`/root/.cache/peak_shaving_submission_sensitivity/run_post_sensitivity_audits.sh`；该脚本不进入正式数值来源清单。
- 触发条件：仅在 `sensitivity_finalization.exit=0` 后执行。finalizer 无哨兵退出或返回非零时，下游任务停止并写入 `post_sensitivity_audits.exit` 非零状态。
- 计算顺序：并行重建 12-worker 固定点多初值审计和 16-worker 中间商 differential-evolution 审计；同时重建固定策略机制分解。完成后串行运行完整 submission evidence gate、结果宏、全部正式图和相关定向测试。
- 验证：`bash -n /root/.cache/peak_shaving_submission_sensitivity/run_post_sensitivity_audits.sh` 返回 0；独立 PID `103484` 已运行，当前日志仅为 `waiting for sensitivity finalizer`。
- 资源边界：等待阶段不启动审计 workers；只有两个敏感性分支释放 CPU 后才使用 12+16 workers，不与当前求解竞争。
- 状态：in_progress；post_sensitivity_pipeline_ready

### 2026-07-16 00:22 - 下游审计失败路径修正

- 风险：初版脚本在机制分解或固定点审计先失败时可能提前返回，使另一个后台审计继续运行，而总哨兵已写为失败。
- 修正：三个子任务启动后临时关闭 `errexit`，始终收集机制分解、固定点审计和中间商审计的退出码，等待全部子进程结束后再统一判定；任一非零则拒绝继续 evidence gate。
- 验证：修正后 `bash -n` 返回 0。本机未安装 `shellcheck`，因此未声称通过 shellcheck。
- 进程：旧等待器 PID `103484` 在尚未触发审计计算时停止；新等待器 PID `103601` 已独立运行并重新进入 `waiting for sensitivity finalizer`。
- 状态：verified_wait_state；failure_cleanup_improved

### 2026-07-16 00:25 - 九场景结论事实提取器

- 目标：由通过门禁的九行敏感性汇总计算可直接核对的结论事实，避免手工抄写范围、方向和利润符号时出错；不自动生成论文解释性措辞。
- TDD 红灯：首个测试因未加入项目根目录而得到 3 个 `No module named 'experiments'`，属于测试夹具错误。修正 `sys.path` 后，3 个失败均准确指向 `experiments.build_submission_sensitivity_claims` 尚不存在。
- 实现：新增 `experiments/build_submission_sensitivity_claims.py`，锁定 baseline + 八扰动的九场景顺序和 788 候选范围，输出峰值/利用率/QoS 的最小值、最大值与全方向检查，利润正/零/负场景数，以及最大 finite regret 和 fixed-point residual。
- 边界：工件明确声明范围只适用于共同有限候选集和八个局部扰动，不是连续参数域或生产保证。输出绑定汇总 JSON 的 SHA-256。
- 绿灯：`tests/test_submission_sensitivity_claims.py` 为 `3 passed in 0.03s`；Ruff 为 `All checks passed!`；radon 所有函数为 A 级。实现 113 行，测试 89 行。
- 自动化：claims 生成器及其测试已加入 post-sensitivity 流水线。旧等待器 `103601` 在等待状态停止，新 PID `103917` 已独立运行。
- 状态：verified；formal_summary_pending

### 2026-07-16 00:25 - capacity_low 第二持久检查点

- `capacity_low` 于 00:21:22 将 dynamic cache 从 8,868 扩展至 17,060 records，文件大小 90,697,194 bytes；首个长块已正常完成。
- `price_sensitivity_low` 当前为 61,441 records；两个 branch、sensitivity finalizer 与 post-sensitivity audit 的五个退出哨兵均为 pending。
- 决策：保持 12+16 workers，不调整并发或重启场景。
- 状态：checkpointed；scenario_1_of_8_verified

### 2026-07-16 00:27 - claims 纳入正式证据门禁

- TDD：为 `submission_evidence_gates.py` 增加有效 claims、过期 summary SHA 和人工篡改范围三类测试。实现前定向测试为 `2 failed`，均因 `validate_sensitivity_claims` 尚不存在。
- 实现：新增 `SENSITIVITY_SUMMARY_PATH` 与 `SENSITIVITY_CLAIMS_PATH`；完整 gate 读取正式九场景汇总和 claims，验证源 SHA，并用同一确定性函数重算整个 claims 结构。
- 结构修正：首次实现使 gate 文件达到 310 行，超过 300 行门禁。将结构校验移至 claims 模块并在 gate 中显式别名导入后，claims/gate 分别为 134/290 行。
- 绿灯：`tests/test_submission_sensitivity_claims.py` 与 `tests/test_submission_evidence_gates.py` 合计 `18 passed in 0.05s`；Ruff 通过；radon 未报告 C 级函数。
- 作用：九场景范围、方向一致性、利润符号计数及最大 regret/residual 现在属于正式 submission evidence gate，而非旁路统计。
- 状态：verified；claims_gate_integrated

### 2026-07-16 00:28 - 完整证据门禁只读预演

- 命令：在内存中调用 `build_gate_report()`，不执行 `main()`，因此不覆盖正式 `submission_evidence_gate_report.json`。
- 当前结果：`passed=false`，3 项检查通过、11 项失败。已通过项为 off-grid、equilibrium branch 和 `capacity_high`。
- 预期失败：三个审计工件来源 SHA 过期；其余七个敏感性场景正式 JSON 缺失；九场景 summary/claims 尚未生成。
- 结论：新增 claims gate 没有引入意外失败，也没有发现新的数值门禁问题。当前失败集合与执行计划逐项一致。
- 状态：expected_red_gate；pipeline_consistent

### 2026-07-16 00:30 - claims 数值噪声与有限性门禁

- 风险：原实现会把 `-1e-12%` 视为峰值改善，且 NaN regret 可能绕过最大值统计；这会使“所有场景方向一致”对数值噪声过敏。
- 红灯：新增两个边界测试后，方向测试错误返回 `all_improve=true`，非有限 regret 测试未抛异常，得到预期 `2 failed`。
- 修复：定义 `EFFECT_TOLERANCE=1e-9`；峰值/利用率下降或 QoS 上升只有超过该阈值才计为改善。uniform/dynamic regret 通过统一有限性检查后再计算最大值。
- 绿灯：claims 与 evidence gate 测试合计 `20 passed in 0.05s`；Ruff 通过；claims/gate 为 131/290 行，radon 无 C 级函数。
- 状态：verified；noise_aware_claims

### 2026-07-16 00:31 - 冻结来源复核与 price_sensitivity_low 新检查点

- 来源复核：基准工件记录的 20 个来源文件均存在；工作树 SHA 与记录差异 0，冻结 commit `6f483084178c3934d1340ba95cd469ae9dd1141d` blob SHA 差异 0。
- sensitivity runner：当前 SHA-256 为 `199af66c39047feb506a6cdbb2a69139cfd3daa0b3582bab1fc7afaf9999c867`，与 `capacity_high` 正式工件记录一致。
- 结论：新增 claims 与 evidence gate 工作没有修改数值来源，也不会使正在运行场景的 provenance 失效。
- 进展：`price_sensitivity_low` 于 00:30:54 写入 62,936 records；退出哨兵仍为 pending。`capacity_low` 保持 17,060 records。
- 状态：source_freeze_verified；compute_in_progress

### 2026-07-16 00:32 - claim--evidence 映射状态同步

- 更新 `docs/reviews/smpt_submission_evidence_map_2026-07-14.md`，增加 2026-07-16 进展日期。
- 参数敏感性行现区分 `capacity_high` 已通过和其余七场景运行/排队，不再沿用“八场景全部进行中”的旧状态。
- 新增 `sensitivity_claims_submission.json` 证据行，明确正式工件等待九场景 summary，范围仅为九场景数值事实并绑定 summary SHA。
- 待完成门禁同步为其余七场景、九场景 summary/claims 和结构重算门禁；不改变任何已锁定基准数值。
- `git diff --check` 对相关审计、claims、gate、测试和 README 均通过。
- 状态：audit_map_updated；formal_sensitivity_pending

### 2026-07-16 00:33 - claims 生成代码 provenance

- 风险：仅绑定 summary SHA 可以证明输入，但不能直接追踪范围统计由哪一版生成器和场景顺序定义产生。
- 红灯：测试要求 metadata 含两个来源 SHA 后，因 `source_sha256` 缺失得到预期失败。
- 修复：claims metadata 记录 `build_submission_sensitivity_claims.py` 与 `build_submission_sensitivity_table.py` 的 SHA-256；evidence gate 通过重建整个 claims 工件间接核对二者。
- 绿灯：claims 与 gate 测试合计 `20 passed in 0.05s`；Ruff 通过；claims/gate 为 143/290 行，radon 无 C 级函数。
- 状态：verified；claims_provenance_complete

### 2026-07-16 00:44 - price_sensitivity_low 扩展至 64,429

- `price_sensitivity_low` 于 00:43:38 将 dynamic cache 写入 64,429 records，文件大小 342,519,324 bytes；日志记录 64,428/64,429 oracle 阶段边界。
- 场景与 price branch 退出哨兵仍为 pending，不能据配对数判断已完成。
- `capacity_low` 当前保持 17,060 records；两个分支继续运行。
- 状态：checkpointed；scenario_1_of_8_verified

### 2026-07-16 01:00 - 均衡比较与 off-grid 措辞收紧

- 范围：仅修改 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 中不依赖待完成敏感性数字的解释性句子；未修改公式、表格数值、实验脚本或冻结数值来源。
- 修改：将“policy reduces overload”改为“time-varying equilibrium reduces overload”，明确结果是两个均衡制度的模型内比较；删除“improve spatial allocation”这一超出利用率/QoS 指标直接含义的概括。
- 诚实度：off-grid 的 `0.5%` 门槛统一称为 `declared numerical-adequacy threshold`，不再使用可能暗示预注册的 `prespecified`。vLLM 的 `0.5 s` TTFT 阈值仍保留 `prespecified`，因为它属于测量协议中的预先诊断设定。
- 验证：待敏感性计算释放 CPU 后，与最终数字插入一起运行 TeX 定向测试、全文语言扫描和 LaTeX 编译。
- 状态：prose_updated；numerical_results_unchanged

### 2026-07-16 01:02 - SMPT 官方投稿规则复核

- 来源：重新读取 Elsevier/ScienceDirect 的 *Simulation Modelling Practice and Theory* Guide for Authors；只以期刊官方页面为依据。
- 已符合：摘要不超过 250 词、1--7 个关键词、3--5 条且每条不超过 85 字符的 Highlights、连续编号的可编辑公式、可编辑 LaTeX 表格、正文交叉引用和独立图文件。
- 图像政策：官方仍不允许用生成式 AI 创建或修改投稿图像。当前正式框架图为 Draw.io 矢量图，其余正式图由数据脚本生成；早期 image-generation 图片不得进入投稿包。
- 仍需人工信息：single-anonymized title page 需要真实作者、单位、完整地址和通讯作者；Funding、CRediT、competing interests 与 ORCID 不能推测。
- 数据政策：该刊采用 Option C，需要将研究数据存入相关仓储并在正文引用、链接，或解释无法共享的原因。GitHub 尚无持久标识符，最终仍需 release 与 Zenodo DOI 或等效仓储记录。
- 状态：journal_requirements_reverified；metadata_and_persistent_repository_pending

### 2026-07-16 01:03 - 稿件措辞修改后的定向红灯复核

- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run pytest -q tests/test_final_manuscript_20260714.py
  ```
- 结果：退出码 `1`，`4 passed, 2 failed in 0.04s`。
- 失败范围：一项要求 `resolved_sensitivity.pdf` 已生成并被正文引用；另一项要求删除 `FINAL_SENSITIVITY_RESULTS` 占位。两项均是八场景通过门禁前有意保留的终稿红灯。
- 结论：均衡比较与 off-grid 措辞修改未引入新的结构、图表或数值一致性失败。
- 状态：expected_red；final_sensitivity_pending

### 2026-07-16 01:04 - price_sensitivity_low 扩展至 65,920

- `price_sensitivity_low` 于 00:59:23 将 dynamic cache 写入 65,920 records，文件大小 350,445,307 bytes。
- 写入后求解器启动了新的 12-worker 偏差扫描，说明 65,920 不是可据以判定完成的固定数量；场景退出与正式 JSON 仍为 pending。
- `capacity_low` 保持 17,060 records，并继续执行当前 16-worker 大批次；无错误或退出信号。
- 状态：checkpointed；scenario_1_of_8_verified

### 2026-07-16 01:08 - 正式图源配色与视觉抽检

- 图源：检查 `experiments/plot_style.py`、`experiments/build_final_submission_figures.py` 和 `figure_sources/build_final_spatiotemporal_framework_drawio.py` 的颜色常量与调用位置。
- 配色：数据图统一使用 `#3C5488`、`#6F83B5`、`#A86464`、`#7A7A7A` 和 `#B8C4D9`；框架图复用同一主色并只加入浅背景色。未发现未受控的彩虹色图或渐变色图。
- 视觉：打开 Figure 1 及 Figures 2--5 的 PNG 导出逐一检查。框架图的直线/直角连接、公式、节点和图标无可见重叠；数据图的图例、曲线、误差条、阈值线和下置 `(a)--(d)` 子图说明均可辨认。
- 字体：数据图使用 Times New Roman 并以 PDF type 42 字体输出；框架图同时保留 Draw.io、SVG 和 PDF 可编辑/矢量源。
- 待验：Figure 6 生成器复用同一调色板且已锁定场景顺序，但正式九场景数据尚未生成，因此当前不声称 Figure 6 视觉门禁通过。
- 状态：figures_1_to_5_visually_verified；figure_6_pending

### 2026-07-16 01:11 - capacity_low 扩展至 25,252

- `capacity_low` 完成第二个 8,192-pair dynamic 批次，持久缓存从 17,060 扩展至 25,252 records。
- `price_sensitivity_low` 继续执行 65,920 records 之后的新偏差扫描；两个场景均无退出或错误哨兵。
- 决策：保持 12+16 workers 和当前冻结求解路径，不在批次中途调整并发、代码或缓存签名。
- 状态：checkpointed；scenario_1_of_8_verified

### 2026-07-16 01:13 - 终稿过期数值门禁消除误报

- 问题：`tests/test_final_manuscript_20260714.py` 全局禁止字符串 `13.03`，但现稿中 `13.03%` 是合法的 temporal-only 固定策略机制分解结果，只是与旧候选集主结果数值巧合。
- 影响：敏感性占位删除后，原测试会把合法机制结果误判为 stale main result，并可能诱导错误删除论文证据。
- 修正：停止全局禁止 `13.03`；继续禁止旧主结果中的 `17.08`、`0.888` 和 `0.976`，并新增测试要求 temporal-only 机制段保留 `13.03%`。
- 边界：未修改论文数字、实验脚本、工件或冻结来源。
- 验证：定向稿件测试为 `5 passed, 2 failed in 0.04s`；新增机制数值测试通过，两项失败仍仅为 Figure 6 和敏感性占位的预期红灯。相关文件 `git diff --check` 通过。
- 状态：test_gate_fixed_and_verified；expected_final_reds_remain

### 2026-07-16 01:14 - price_sensitivity_low 扩展至 67,409

- `price_sensitivity_low` 于 01:11:35 将 dynamic cache 从 65,920 扩展至 67,409 records，随后启动新的 12-worker 偏差扫描。
- 解释：上一轮混合博弈仍加入了新的支持策略，因此必须继续检查全部 788 个候选；不按与其他场景相近的配对数提前截断。
- `capacity_low` 同期保持 25,252 records 并继续当前大批次。
- 状态：checkpointed；finite_regret_pending

### 2026-07-16 01:16 - 敏感性表图双引用终稿门禁

- 风险：原终稿测试要求 Figure 6 和占位删除，但未要求机器生成的九行敏感性 LaTeX 表进入正文；自动汇总成功后仍可能人工漏插表格。
- 新增门禁：`Fully re-solved sensitivity and profit variation` 小节必须输入 `submission_sensitivity_table.tex`，并在同一小节引用 `tab:resolved_sensitivity` 和 `fig:resolved_sensitivity`。
- 当前预期：正式汇总尚未生成，因此该测试应与 Figure 6/占位测试一起保持红灯，直到全部八个场景通过。
- 验证：定向测试为 `5 passed, 3 failed in 0.05s`；三个失败逐项对应 Figure 6、九行表/表图引用和敏感性占位，没有额外失败。
- lint：首次运行 `uv run ruff` 因无项目环境中未安装 `ruff` 而得到 `Failed to spawn: ruff`；改用 `uv run --no-project --with ruff ruff check tests/test_final_manuscript_20260714.py` 后返回 `All checks passed!`。
- 状态：expected_red_verified；lint_verified；formal_sensitivity_pending

### 2026-07-16 01:20 - Figure 6 临时版式预检

- 目标：在正式九场景数据完成前，仅检查 `resolved_sensitivity` 的 2x2 布局、九个横轴标签、Times New Roman 字体、SCI 配色和下置子图说明。
- 操作：使用 `SCENARIO_ORDER` 和明确标记为测试用途的合成行调用 `_resolved_sensitivity`，输出到 `/tmp/peak_shaving_figure6_layout/`；未写入仓库图目录或论文工件。
- 输出：临时 PNG 为 2500x1696，另有矢量 PDF。视觉检查未见场景标签、坐标轴或 `(a)--(d)` 说明重叠；baseline 为灰色，其余场景为统一蓝色。
- 证据边界：临时柱高不属于实验结果，不能引用或复制到正文。正式 Figure 6 仍由通过门禁的 `spatiotemporal_sensitivity_submission.json` 生成并再次视觉审查。
- 状态：layout_only_verified；formal_figure_6_pending

### 2026-07-16 01:22 - 九行敏感性表宽度红灯

- 预检：用与正式表相同的九行、七列结构在 A4、2.3 cm 页边距下生成 `/tmp/peak_shaving_sensitivity_table_layout/table_test.tex` 并运行 XeLaTeX。
- 结果：编译成功，但日志报告 `Overfull \\hbox (7.04762pt too wide)`；原 `\\tabcolsep=3pt` 不满足终稿无 overfull 门禁。
- TDD 红灯：测试先要求 `\\tabcolsep=2.25pt`，实现前结果为 `1 failed, 1 passed`，失败只指向生成器仍输出 `3pt`。
- 实现：将生成表的 `\\tabcolsep` 从 `3pt` 调整为 `2.25pt`。该值减少 9 pt 总列间距，保留 `scriptsize` 字号，并给原 7.05 pt 超宽留出少量余量。
- 绿灯：表格单测 `2 passed in 0.02s`；独立 XeLaTeX 预检未检出 overfull、underfull、LaTeX warning 或 undefined 项；Ruff 与 `git diff --check` 通过。
- 冻结边界：基准工件记录的 20 个数值来源重新逐项计算 SHA-256，工作树差异为 0。表生成器不属于冻结数值来源，正在运行的敏感性 provenance 未失效。
- 状态：layout_fixed_and_verified；numerical_source_freeze_intact

### 2026-07-16 01:26 - 双分支计算与 GPU 路径复核

- `price_sensitivity_low` 的 dynamic cache 于 01:23:34 更新至 366,265,105 bytes；`capacity_low` 保持 134,248,496 bytes，并继续执行尚未完成的 16-worker 批次。
- 进程核验显示两个进程组共有 28 个数值 worker，连同协调进程合计占用约 30.8 个逻辑核；两组 worker 均处于运行状态，无错误或退出哨兵。
- 当前求解器由 NumPy/SciPy 的大量固定点与 L-BFGS-B 小任务组成，仓库没有经过结果一致性验证的 CUDA 实现。中途改用 GPU 会改变求解路径和 provenance，且不能保证加速，因此继续使用已冻结的 12+16 CPU 多进程配置。
- 正式工件仍只有 `sensitivity_capacity_high_submission.json`；其余场景在完整验证前不进入论文数字或结论。
- 状态：compute_healthy；gpu_path_not_validated；scenario_1_of_8_verified

### 2026-07-16 01:27 - Elsevier CAS 2.4 模板预检

- 来源：从 Elsevier 官方 SMPT Guide for Authors 链接下载 `els-cas-templates.zip` 至 `/tmp`，SHA-256 为 `36d97da01c6bbd134f315bff6c3de553735e2550444a6ddd4f869ddc67a20757`；包版本为 CAS 2.4（2024-05）。未将模板文件写入仓库。
- 检查：官方包提供 `cas-sc.cls`、`cas-dc.cls`、`cas-common.sty` 和 `cas-model2-names.bst`。原始 `cas-sc-template.tex` 可编译，但空示例在 `\maketitle` 处报告 `Overfull \\hbox (117.0831pt too wide)`。
- 排除：在 `/tmp` 的副本中填入非空题名、作者、单位、摘要、关键词和 Highlights，并移除空邮箱、网址、脚注、CRediT 与第二作者字段；XeLaTeX 和 pdfLaTeX 均可生成 PDF，但相同的 117.0831 pt `\maketitle` 溢出仍存在。因此不能把该警告简单归因于匿名元数据占位。
- 定位：打开 `\overfullrule` 并渲染标题页后，标记位于 `ARTICLE INFO` 与 `ABSTRACT` 的分栏交界。CAS 2.4 的 `cas-common.sty` 用 `\hbox_to_wd:nn {\z@} {\box \g_stm_key_box}` 将约 `0.25\textwidth` 的关键词盒叠放在零宽盒中；117.0831 pt 正是该内部覆盖盒的宽度。因此这是类文件实现产生的固定诊断，不表示题名、关键词或摘要超出页面。
- 其他模板噪声：示例正文保留的空 `\label{}` 会产生重复标签，空参考文献会产生 natbib 警告；正式迁移时不会复制这些示例内容。
- 决策：CAS 正式迁移保持 pending。先完成数值与正文证据门禁，再用实际稿件内容定位标题页溢出；真实作者元数据仍由作者提供，不进行推测。
- 状态：template_package_verified；title_page_layout_pending

### 2026-07-16 01:28 - 现稿静态结构与隔离编译检查

- 范围：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex`；未替换终稿敏感性占位，也未使用未验证场景数字。
- 静态检查：摘要 205 词；关键词 7 个；五条 Highlights 分别为 73、76、75、64、68 个字符，符合 SMPT 当前数量和长度要求。
- 交叉引用：共 46 个标签，无重复标签、未定义引用或未被正文引用的图表标签。正文 57 次 citation 调用涉及 38 个唯一键，均存在于 `verified_refs.bib`。
- 命令：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    -outdir=/tmp/peak_shaving_tex_preflight_20260716 \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：退出码 0，生成 19 页 A4 PDF；最终日志未检出 overfull、underfull、LaTeX warning、undefined citation/reference 或 LaTeX error。
- 边界：该结果只验证当前通用 article 稿的结构与排版。Figure 6、九行敏感性表和占位删除仍是三个预期终稿红灯；CAS 标题页适配另行处理。
- 状态：current_manuscript_compiles_cleanly；final_sensitivity_pending

### 2026-07-16 01:31 - 近期相关工作官方来源复核

- 范围：核对英文稿实际引用且年份较新的 LLM 定价、GPU 平台和电力动态定价条目；不根据搜索摘要新增引用。
- AAAI：官方 Proceedings 页面确认 `guo2026prillm` 的题名、三位作者、2026 年、40(20)、17005--17013 和 DOI `10.1609/aaai.v40i20.38748` 均与 `verified_refs.bib` 一致。
- arXiv：官方摘要页确认 `yan2026stackelberg` 为 arXiv:2604.16802（2026-04-18 提交），`cunningham2026token` 为 arXiv:2603.00356（2026-02-27 提交）；题名和作者均与 BibTeX 一致。`bergemann2025menu` 的 arXiv:2502.07736 题名和作者一致，当前版本为 2026-03-09 的 v2，但首发年份仍为 2025。
- NBER：官方页面确认 `demirer2025emerging` 为 Working Paper 34608，DOI `10.3386/w34608`。
- 电力定价：ScienceDirect 官方页面确认 `fraija2024dynamic` 发表于 *Smart Energy* 14 (2024), article 100139，DOI `10.1016/j.segy.2024.100139`，并确实使用 RL 调整受市场和容量约束的动态价格生成规则。
- 结果：上述条目无需修改；本轮没有改变引用键、引文位置或参考文献格式。
- 状态：recent_references_verified；bibliography_unchanged

### 2026-07-16 05:29 - 敏感性自动收尾管线预检

- 检查：复核 `finalize_validated_sensitivity.sh` 与 `run_post_sensitivity_audits.sh` 的等待条件、失败码传播、正式工件存在性检查和后续审计顺序。
- 门禁顺序：两个场景分支均以 queue sentinel 为 0 后，finalizer 才逐场景调用增强版证据门禁并原子替换九场景 summary；随后生成表格和 Figure 6。post 管线只在 finalizer sentinel 为 0 后重建固定点、中间商和机制分解工件，再运行 claims、总证据门禁、宏、全图和定向测试。
- 风险判断：表格和图本身不是原子替换，但后续集成严格依赖 finalizer 成功 sentinel 和文件非空检查，因此失败时不会被当作正式结果使用。数值源和正在运行的分支未改动。
- 命令：`bash -n /root/.cache/peak_shaving_submission_sensitivity/finalize_validated_sensitivity.sh /root/.cache/peak_shaving_submission_sensitivity/run_post_sensitivity_audits.sh`
- 结果：退出码 0。
- 状态：finalizer_syntax_verified；post_pipeline_order_verified；waiting_for_scenarios

### 2026-07-16 05:28 - 敏感性 claims 工件范围统一

- 发现：`build_submission_sensitivity_claims.py` 的机器可读 metadata 仍使用 `fully re-solved local perturbations`，比主稿已收紧的“有限博弈重求并扫描全部声明单边偏差”更容易被误解为完整构造 $788^2$ 支付矩阵。
- 修改：scope 改为 `baseline and eight local finite-game re-solves`；interpretation boundary 继续明确共同有限候选集、局部扰动、非连续域保证和 baseline-only 的独立审计。
- TDD：先修改期望字符串，定向测试按预期失败，退出码 1；修改 builder 后，`tests/test_submission_sensitivity_claims.py` 为 `5 passed`。
- 静态检查：`uv run --no-project --with ruff ruff check experiments/build_submission_sensitivity_claims.py tests/test_submission_sensitivity_claims.py` 退出码 0，`All checks passed!`。
- 边界：该 builder 不属于正在运行场景的 20 个冻结数值来源；正式 claims 尚未生成，post 管线将自动记录修改后的 builder SHA。
- 状态：machine_claim_scope_precise；post_builder_ready

### 2026-07-16 05:31 - 长任务进度检查

- `capacity_low`：动态支付缓存由 66,665 继续增至 72,605 对，16 个 worker 正常进入下一批次；尚无场景 `.exit`，不能提取或引用正式均衡结果。
- `price_sensitivity_high`：动态支付缓存由 17,060 增至 25,252 对，12 个 worker 持续高 CPU；没有失败 sentinel 或异常退出迹象。
- 资源：监督分支、finalizer 和 post-audit waiter 均存活；不重启、不修改冻结数值源，继续以 `.exit=0` 和增强证据门禁作为唯一完成条件。
- 状态：capacity_low_cache_advancing；price_high_batch_running；no_new_formal_scenario

### 2026-07-16 05:34 - 统一价格基线的均衡身份统一

- 审稿发现：统一价格结果来自 12 个零斜率候选构成的受限博弈；原方法与结果解释已说明，但摘要、分解记号和结论仍使用简写 `uniform-price equilibrium`，脱离上下文时可能被误读为完整 788 规则博弈中的另一均衡。
- 修改：摘要和结论改为 `equilibrium under the uniform-price restriction`；分解记号、价格解释和机制比较同步区分受限统一价格均衡与时变价格有限博弈均衡。数值和表格未改。
- TDD：新增 `test_uniform_baseline_is_identified_as_a_restricted_equilibrium`，修改前按预期失败，退出码 1；修改后与摘要长度门禁为 `2 passed`。完整静态稿件门禁为 `24 passed, 3 deselected`。
- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 退出码 0；PDF 为 22 页，SHA-256 为 `51f0dd8e5670c199d318d056ffb19a1413edcf912ca92c324b1a74c211b85fdd`，日志无 error、未定义引用/文献、overfull 或 underfull box。
- 视觉判断：新增页来自 Section 5 移至整页开头，最后一页仍有 3 条完整参考文献；没有孤立标题或只含一行的尾页。保留自然分页，不通过压缩字号或负间距追求页数。
- 状态：uniform_restriction_explicit；baseline_identity_consistent；latex_verified

### 2026-07-16 05:38 - SMPT 作者指南格式规则复核

- 官方来源：`https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors`，本次复核摘要、关键词、Highlights、公式、图像与 AI 声明条款。
- 当前限制：摘要不超过 250 词；关键词 1--7 个；Highlights 3--5 条且每条不超过 85 字符。当前主稿摘要 218 词、关键词 7 个，Highlights 5 条且长度门禁通过。
- 公式与表格：公式为可编辑 LaTeX、连续编号，表格为 TeX 文本，符合指南；没有把数学式或表格栅格化为图片。
- AI 条款：指南仍禁止使用生成式或 AI-assisted 工具制作投稿 artwork。当前主稿声明和作者行动清单继续要求作者独立重建 Figures 1--6；内部审阅图不能直接上传。
- 决策：内部测试中的 250/7/5/85 门限与当前官方页面一致，无需改动。
- 状态：smpt_format_limits_reverified；artwork_block_remains

### 2026-07-16 05:40 - 敏感性表题的有限博弈范围

- 发现：正式表格 builder 的 caption 仍写 `Fully re-solved sensitivity results`，与 claims metadata 和主稿收紧后的计算范围不一致。
- 修改：表题改为 `Finite-game sensitivity results on the common 788-candidate set`，并明确每个场景重求两类政策博弈且检查全部声明的单边服务商偏差。regret、残差和指标单位说明保持不变。
- TDD：先增加新表题、单边偏差和禁止旧短语的断言，修改前定向测试按预期失败，退出码 1；修改后 `tests/test_submission_sensitivity_table.py` 为 `2 passed`。
- 静态检查：对应 builder 与测试的 Ruff 检查为 `All checks passed!`。
- 编辑记录：首次补丁因 Python 源码中 LaTeX 反斜杠为双字符而未匹配，文件未部分写入；使用原样补丁后成功。
- 状态：sensitivity_caption_scope_precise；table_builder_ready

### 2026-07-16 01:35 - 旧 225 候选审计的版本边界

- 问题：三份 2026-07-12 审计仍保留 `13.03%`、`17.08%`、`0.888 -> 0.976`、225 候选和旧九场景结论。它们记录了后续扩大响应空间的修复动机，但标题中的“终稿/就绪度”可能使复核者误当当前证据。
- 处理：在 `smpt_final_claim_evidence_audit_2026-07-12.md`、`smpt_final_credibility_reality_language_audit_2026-07-12.md` 和 `smpt_q1_readiness_audit_2026-07-12.md` 顶部加入历史审计标记；保留原文，不删除或改写旧实验记录。
- 当前事实源：`docs/reviews/smpt_submission_evidence_map_2026-07-14.md` 与 `artifacts/peak_shaving/20260712_expanded_response/*_submission.json`。扫描确认所有包含旧主结果的 review 文件均已标记。
- 验证：相关 Markdown 与 README 通过 `git diff --check`。
- 状态：historical_evidence_marked；current_evidence_source_unambiguous

### 2026-07-16 01:36 - Figures 1--5 矢量与字体门禁

- 对五个正式 PDF 运行 `pdfinfo`、`pdffonts` 和 `pdfimages -list`；每个文件均为单页 PDF。
- Figure 1 嵌入 Times New Roman regular/bold/italic/bold-italic，Figures 2--5 嵌入 Times New Roman regular；字体均为 embedded/subset CID TrueType。
- 五个 PDF 的 image object 列表均为空，说明曲线、文字、箭头和图标保持矢量，不依赖低分辨率位图。Figure 1 同时保留 Draw.io/SVG 源，数据图由脚本重建。
- 边界：该门禁不包括尚未生成正式数据版的 Figure 6；Figure 6 必须在九场景 summary 完成后重复相同检查。
- 状态：figures_1_to_5_vector_verified；figure_6_pending

### 2026-07-16 01:38 - 投稿证据脚本复杂度与 lint

- 检查文件：敏感性运行/汇总、claims、敏感性表、evidence gate 和最终图生成器，以及对应测试。
- 文件规模：核心脚本分别为 266、143、107、290 和 300 行，均不超过项目 300 行上限。
- 命令：
  ```bash
  uv run --no-project --with radon radon cc -s -n C <submission scripts>
  uv run --no-project --with ruff ruff check <submission scripts and tests>
  ```
- 结果：Radon 未输出 C 级或更高复杂度函数；Ruff 返回 `All checks passed!`。敏感性运行器 SHA-256 仍为 `199af66c39047feb506a6cdbb2a69139cfd3daa0b3582bab1fc7afaf9999c867`。
- 状态：code_audit_verified；numerical_source_unchanged

### 2026-07-16 01:39 - price_sensitivity_low 完成与独立验证

- 正式工件：`artifacts/peak_shaving/20260712_expanded_response/sensitivity_price_sensitivity_low_submission.json`，大小 510,592 bytes，SHA-256 `c1335d1d7614515dd91ef0fa3dfe22c9cd0d34684de04240c44279361614db07`；场景退出码为 0。
- provenance：基准 SHA-256 为 `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`；20 个来源文件均存在且当前 SHA 无差异；候选数为 788，场景参数为 price sensitivity scale `0.8`，其他三个扰动为基准值。
- 数值门禁：uniform/dynamic full-candidate regret 分别为 0 和 `2.2737e-13`；最大联合残差为 `9.4470e-10/9.9192e-10`；两者均 `full_grid_verified=true`，以 `regret_tolerance` 结束且未达到 oracle round limit。
- 结果：相对同场景 uniform 均衡，aggregate peak `-12.5737%`，maximum provider utilisation `-18.2534%`，minimum provider QoS `+0.06735`，aggregate market-side profit `-39.7940%`。dynamic 评估 71,122 个唯一策略对，活跃支持为 21-by-21。
- 结构检查：混合概率与 441 个活跃剖面权重和均为 1；最大路由和误差 `8.88e-16`；市场侧利润分量会计误差 `1.36e-12`；中间商基价、斜率、beta、QoS 和候选系数均在声明边界内。
- 审计脚本失败记录：第一次附加检查误用不存在的 `probability` 键；第二次误把二维列表当字典读取。检查 `active_profiles` 与 `expected_profiles` 的真实结构后，改用 `weight` 和递归列表展开，第三次检查通过。两次失败均未修改工件或数值代码。
- 调度：price branch 已独立验证该场景并自动启动 `price_sensitivity_high`，仍使用 12 workers。
- 结论边界：这是 8 个扰动中的第 2 个已验证场景；九场景 summary 尚未生成，不在论文中提前声称方向稳健。
- 状态：scenario_2_of_8_verified；price_sensitivity_high_running

### 2026-07-16 01:42 - sensitivity finalizer 与 post-audit 预检

- finalizer：等待两个 branch 的退出哨兵并核对 supervisor PID；按 `SCENARIOS` 固定顺序重新验证八个场景；summary 先写 `.tmp` 再用 `os.replace` 原子替换；随后生成九行 LaTeX 表和 Figure 6，并检查四个输出非空。
- post-audit：等待 finalizer 成功后并行重建固定点多初值和中间商 differential-evolution 审计，同时重建机制分解；三者均成功后才生成 claims、运行完整 evidence gate、宏、全套图和定向测试。
- 环境风险复核：仓库没有 `pyproject.toml`，但 `uv run pytest --version` 返回 `pytest 9.1.0`，可解析到当前 WSL uv Python；post-audit 的测试入口可用。
- 当前未修改两个 `/root/.cache` 脚本。它们只协调已冻结代码与正式工件，不属于数值模型来源。
- 状态：automation_preflight_verified；waiting_for_remaining_scenarios

### 2026-07-16 01:47 - CAS 全文数字引用与视觉预检

- 问题：第一次实际全文 CAS 2.4 预检采用 `cas-model2-names.bst` 的作者年份标签，多篇引用展开为完整作者列表，造成大范围 overfull 与 PDF annotation 越界；另一次预检因模板不接受 `[H]` 浮动选项以退出码 12 失败。这两项均发生在 `/tmp` 模板副本，未修改仓库主稿。
- 修正：将临时副本的浮动选项机械替换为 `[htbp]`，并显式加入 `\usepackage[numbers]{natbib}`。使用 Elsevier CAS 2.4 类文件和当前完整正文重新运行 `latexmk -g -xelatex`。
- 命令：
  ```bash
  TEXINPUTS=/tmp/elsevier_cas_template_check/els-cas-templates: \
  BSTINPUTS=/tmp/elsevier_cas_template_check/els-cas-templates: \
  latexmk -g -xelatex -interaction=nonstopmode -halt-on-error \
    -outdir=/tmp/peak_shaving_cas_full_build_numeric \
    /tmp/peak_shaving_SMPT_CAS_full_preflight.tex
  ```
- 结果：退出码 0，生成 17 页、429,790 bytes 的 CAS PDF；最终日志无 undefined citation/reference、LaTeX error、annotation 越界或正文 overfull。数字引用正常显示为 `[n]`。
- 残余诊断：`\maketitle` 仍有已定位到 CAS `ARTICLE INFO` 零宽覆盖盒的 117.0831 pt 固定 overfull；正文中概率加权系数长句有两条 underfull，参考文献中的超长 MLSys URL 有一条 underfull。前者是类文件内部实现，后两者需在正式模板迁移时处理。
- 视觉检查：渲染全部 17 页为 90 dpi PNG，并逐页抽检标题页、参数表、主结果表、Figures 2--5、讨论和结论。图表未越界，数字引用不再挤压正文，单栏版式可读。Figure 6 和九场景表仍未进入临时稿，因此不能视为最终模板验证。
- 工具失败：尝试用 `montage` 生成联系表时返回 `montage: command not found`；改为直接检查独立页面，不安装系统级依赖。
- 状态：cas_numeric_citation_verified；full_template_migration_pending_final_sensitivity_and_metadata

### 2026-07-16 01:50 - 投稿检查表事实同步

- 修正：SMPT 适配检查表中的摘要词数由旧记录 201 更新为静态检查所得 205；仍低于官方 250 词上限。
- 模板状态：用 CAS 2.4 实际全文预检结果替换旧的 `elsarticle.cls` 缺失说明，记录 `[H]` 不兼容、数字 natbib 修复、17 页输出、类文件固定 overfull 和三条剩余 underfull 的来源。
- 审计命令失败：第一次用 `jq` 读取基准均衡时误用不存在的 `oracle_history` 键，返回 `Cannot iterate over null`。检查顶层字段后改读 `uniform.trace` 和 `dynamic.trace`，确认动态六轮 regret 为 `4.074, 1.586, 1.197, 1.734, 0.0295, 1.14e-13`，与正文一致。
- 边界：只更新投稿记录和只读核对；未修改主稿、数值脚本或工件。
- 状态：submission_checklist_current；baseline_trace_reverified

### 2026-07-16 01:54 - CAS 剩余正文断行修复预检

- 临时修正：在 `/tmp` CAS 全文副本中把两组概率加权四元系数拆为独立句，并加载 TeX Live 已提供的 `xurl` 以允许 MLSys 长 URL 在更多位置断行。
- 命令：
  ```bash
  TEXINPUTS=/tmp/elsevier_cas_template_check/els-cas-templates: \
  BSTINPUTS=/tmp/elsevier_cas_template_check/els-cas-templates: \
  latexmk -g -xelatex -interaction=nonstopmode -halt-on-error \
    -outdir=/tmp/peak_shaving_cas_full_build_numeric_xurl \
    /tmp/peak_shaving_SMPT_CAS_full_preflight.tex
  ```
- 结果：退出码 0，17 页 PDF；三条 underfull 全部消失。最终日志只保留 CAS 类文件标题信息盒产生的固定 117.0831 pt overfull 和随附 empty-anchor 警告，无正文 overfull、undefined citation/reference、LaTeX error 或 annotation 越界。
- 决策：最终 CAS 匿名稿加入 `xurl` 并采用拆句版本；不修改第三方类文件来压制内部模板诊断。
- 状态：cas_content_boxes_clean_in_preflight；formal_cas_file_pending

### 2026-07-16 01:57 - 终稿语言一致性与摘要数据边界

- 拼写审计：当前英文稿仍有 23 处 `utilisation`、11 处 `normalised`、4 处 `optimisation`，以及少量 `behaviour`、`discretisation`、`randomisation` 等英式拼写；正式图轴使用 `utilization` 和 `normalized`。当天日期终稿将统一为美式英语，期刊正式名称 *Simulation Modelling Practice and Theory* 除外。
- 数据措辞：摘要的 `derived from 1,429,737 BurstGPT records` 容易让读者理解为全部记录均直接进入日内均值。元数据表明脚本读取 1,429,737 行，但均值只使用去掉首尾不完整日后的 59 个完整日。终稿改为 `uses 59 complete days from the 1,429,737-record BurstGPT trace`。
- 术语修正清单：将结果小节中的 `main policy effect` 改为 `main equilibrium comparison`，把机制段的 `policy difference`/`time-varying policy` 改为 `equilibrium difference`/`time-varying equilibrium`，避免把双方内生均衡误写成外生政策评估。
- 边界：上述修改只进入敏感性完成后新建的终稿，不回写已归档的 2026-07-14 候选版本。
- 状态：final_language_changes_locked；awaiting_sensitivity_results

### 2026-07-16 02:02 - 正式图轴美式英语门禁

- TDD：新增测试要求最终图生成器和共享价格轴样式不再包含 `Normalised concurrency`、`Provider utilisation`、`Max. utilisation change` 或 `Normalised end-user price`，并要求对应美式拼写存在。
- 首次测试异常：普通 Pytest 捕获模式在收集阶段因捕获临时文件消失而报 `FileNotFoundError`，没有执行断言。使用 `-s` 禁用捕获后得到有效红灯：`1 failed`，准确命中 `Normalised concurrency`。复现后确认当前桌面 shell 继承的 `TEMP`/`TMP` 指向不存在的 Windows 路径 `/mnt/c/Users/cccht/AppData/Local/Temp`；显式设置 `TMPDIR=/tmp TEMP=/tmp TMP=/tmp` 后普通捕获模式正常。已排除 Pytest、测试代码和正在运行计算删除临时文件。
- 实现：只替换 `experiments/build_final_submission_figures.py` 和 `experiments/plot_style.py` 中五处轴标签字符串；未改变数据、坐标、图例、颜色或数值生成逻辑。
- 验证：
  ```bash
  uv run pytest -q -s \
    tests/test_final_submission_figures.py::test_final_figure_labels_use_american_english
  uv run --no-project --with ruff ruff check \
    experiments/build_final_submission_figures.py experiments/plot_style.py \
    tests/test_final_submission_figures.py
  ```
- 结果：测试 `1 passed`，Ruff `All checks passed!`，相关文件 `git diff --check` 通过。正式 Figures 2--6 等九场景数据完成后由 post-audit 流程统一重建；当前 PDF 图文件尚未提前覆盖。
- 自动化核验：post-audit 脚本本来就为测试命令显式设置三个临时目录变量，因此无需修改其测试入口。使用相同环境再次执行普通 `pytest -q` 得到 `1 passed`。
- 数值边界：两处图脚本不在基准工件记录的 20 个冻结数值来源中，敏感性 provenance 不受影响。
- 表格扩展：敏感性 LaTeX 表生成器仍有 caption 与列标题两处 `utilisation`。先增加断言并得到 `1 failed` 红灯，再改为 `utilization`；定向表格与图标签测试合计 `3 passed`，Ruff 和 `git diff --check` 通过。第一次补丁因反斜杠转义导致上下文匹配失败，检查原行后用保留原始反斜杠的补丁重试成功，未产生半成品修改。
- 状态：figure_language_source_fixed；formal_figure_rebuild_pending

### 2026-07-16 02:06 - 旧投稿包清单防误用标记

- 发现：`docs/submission/` 下的 2026-06-21 package manifest 和 upload checklist 仍把 2026-06-20 的 23 页、8 图稿及早期 imagegen Figure 1 标为可上传，与当前五章稿、6 图设计和非生成式 Draw.io Figure 1 不一致。
- 处理：在两份历史文件顶部加入 `Historical ... superseded` 标记，明确禁止作为当前上传清单，并指向当前期刊适配检查表与证据映射表。历史内容保留用于追踪，不伪装成当前状态。
- 扩展检查：cover letter、declarations template、figure inventory、portal fields 和旧 highlights 同样包含旧题名、outside option、225 候选或旧 release。前四份 Markdown 已加历史警告；旧 highlights 首行加入 `HISTORICAL - DO NOT SUBMIT`，确保它不再满足可直接上传文本的形式。作者信息表仍保留为空白输入表，不填猜测信息。
- 旧审计扫描：另有 `peak_shaving_mechanism_reaudit_2026-07-12.md`、`peak_shaving_sci_readiness_audit_2026-06-19.md`、`smpt_table_value_audit_2026-06-21.md`、`smpt_submission_readiness_2026-06-19.md` 和 `smpt_full_figure_audit_2026-06-21.md` 保留 225 候选旧数字但未标版本。五份文件已加历史标记并指向当前证据源；当前适配检查表仅因 CAS 的 `117.0831` 含有字符串 `17.08` 被扫描误命中，不属于旧结果。
- 后续：八场景和 post-audit 门禁通过、当天 CAS 匿名稿生成后，再重写当前 package manifest、figure inventory 和 upload checklist。
- 验证：相关 Markdown 与 README 运行 `git diff --check`。
- 状态：stale_submission_package_quarantined；current_package_pending

### 2026-07-16 02:10 - SMPT 引用顺序与 CAS 参考文献样式

- 官方规则复核：SMPT Guide for Authors 要求正文用方括号数字，并按首次出现顺序编号；初投可接受一致的参考文献字段/标点样式，录用后再由出版社统一。
- 发现：`numbers` 与通用 CAS `cas-model2-names.bst` 组合虽然不再展开作者，但参考文献仍按作者字母排序，正文首组系统文献显示为 `[36,21,2,24,38]`，不满足本刊的出现顺序要求。
- 临时修正：保留 `\usepackage[numbers]{natbib}`，将 `/tmp` 全文预检稿的 bibliography style 改为 `unsrtnat`；同时保留 `xurl` 和已验证的长句拆分。
- 结果：`latexmk -g -xelatex` 退出码 0，生成 18 页 CAS PDF；正文首组引用改为 `[1,2,3,4,5]`。最终日志只有 CAS 标题信息盒的固定 117.0831 pt overfull 和 empty-anchor 警告，无正文 overfull/underfull、undefined citation/reference、LaTeX error 或 annotation 越界。
- 决策：正式 CAS 匿名稿使用 `numbers` + `unsrtnat`。不使用作者排序的 `cas-model2-names` 数字模式。
- 状态：smpt_reference_order_verified；formal_cas_file_pending

### 2026-07-16 02:18 - SMPT 投稿图像政策边界复核

- 目标：核对当前 Draw.io 框架图和确定性数据图是否满足 SMPT 对生成式与 AI 辅助图像的限制。
- 官方依据：SMPT Guide for Authors 的 `Generative AI and Figures, images and artwork` 条款明确写明，投稿稿件不得使用 generative AI 或 AI-assisted tools 创建或修改图像；只有当该工具属于研究设计或研究方法时才有例外。本研究的框架排版与结果绘图不属于该例外。
- 发现：Figure 1 虽为可编辑 Draw.io 矢量图且未调用 image-generation 模型，但布局生成器接受过 Codex 辅助；Figures 2--6 的绘图脚本也曾由 Codex 创建或修改。矢量格式、确定性数据来源和可编辑性不能替代该政策要求。
- 处理：把当前 Figures 1--6 统一降为内部审阅图源；更新期刊适配检查表、证据映射和候选稿 AI 声明，删除“未用生成式模型即可投稿”的含混判断。
- 作者动作：正式上传前，作者须在不使用生成式或 AI 辅助图像工具的条件下独立重建六张图，并逐图确认数据、标签、图注、字体、配色和可访问性；完成后记录重建人、日期及文件校验值。当前图源可用于内容核对，但不能直接进入 SMPT 上传包。
- 数值边界：该合规修正不修改实验脚本、工件、表格、公式或论文结论，不影响正在运行的八场景 provenance。
- 状态：figure_policy_blocker_identified；author_rebuild_required_before_submission

### 2026-07-16 02:19 - 图像声明后的候选稿编译与预期红灯

- 首次命令失败：在创建 `/tmp/peak_shaving_tex_preflight_policy` 前把标准输出重定向到该目录，shell 返回 `No such file or directory`，LaTeX 与 Pytest 均未启动。创建隔离目录后重跑。
- 第二个命令错误：静态测试入口误写为不存在的 `tests/test_submission_manuscript.py`，Pytest 退出码为 4 且未收集测试。通过 `rg --files tests` 定位到实际入口 `tests/test_final_manuscript_20260714.py` 后更正。
- 编译命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp latexmk -xelatex \
    -interaction=nonstopmode -halt-on-error \
    -outdir=/tmp/peak_shaving_tex_preflight_policy \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 0，生成 19 页 A4 PDF。最终 LaTeX 日志无 overfull、underfull、undefined citation/reference、LaTeX warning 或 error；`latexmk` 综合输出中的未定义引用来自首轮编译，不属于最终状态。
- 正确测试命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest -q \
    tests/test_final_manuscript_20260714.py \
    tests/test_submission_sensitivity_table.py \
    tests/test_final_submission_figures.py
  ```
- 测试结果：15 passed，5 failed。五个红灯均对应尚未完成的正式敏感性 summary：缺少 Figure 6、敏感性表未嵌入、占位注释仍在，以及最终图生成器两项测试找不到 `spatiotemporal_sensitivity_submission.json`。未发现图像声明引起的结构或排版回归。
- 状态：review_draft_compiles；five_expected_sensitivity_failures

### 2026-07-16 02:20 - 审稿记录版本与图像结论同步

- 修正 `smpt_final_three_reviewer_audit_2026-07-14.md`：保留 Figure 1 的结构、字体和矢量技术检查，但删除“可编辑 Draw.io 即可投稿”的隐含判断；新增作者独立重建 Figures 1--6 的共同阻塞项。
- 标记 `smpt_final_internal_review_2026-07-12.md` 为历史审稿。该文件基于旧 225 候选和旧敏感性结论，不能覆盖当前 788 候选 submission 工件及最新图像政策边界。
- 当前审稿事实源保持为 `smpt_submission_evidence_map_2026-07-14.md`、`smpt_final_three_reviewer_audit_2026-07-14.md` 和正式 submission JSON；历史记录不删除。
- 状态：review_history_disambiguated；figure_policy_consistent

### 2026-07-16 02:22 - 基线测试门禁与检查点测试规格修正

- 首轮基线测试：候选清单、主均衡、离网格、分支、固定点、中间商、机制分解、结果宏和主稿共得到 59 passed、10 failed。失败中 6 项因普通 `uv run pytest` 环境缺少 `nashpy`，3 项是等待敏感性表/Figure 6 的预期红灯，1 项要求 `run_equilibria(checkpoint_interval=...)`，但冻结入口没有该参数。
- 依赖复核命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project \
    --with numpy --with scipy --with nashpy --with pytest \
    pytest -q tests/test_final_spatiotemporal_equilibrium.py
  ```
- 复核结果：12 passed、1 failed，只剩检查点参数测试。实现中的 `PairEvaluator.checkpoint_interval` 已显式固定为 8192，缓存日志按该间隔写入；正式工件通过 source SHA-256 固定这一本体来源。
- 决策：不在八场景运行期间修改 `run_final_spatiotemporal_equilibrium.py` 或缓存模块，因为它们属于 20 个冻结数值来源，任何改动都会使基准及敏感性 provenance 失效。把测试改为核验冻结实现的显式 8192 默认值，不新增未使用的运行参数，也不改数值路径。
- 验证：带显式 NumPy/SciPy/Nashpy/Pytest 依赖重跑后为 `13 passed`；修改后的测试通过 Ruff。`run_final_spatiotemporal_equilibrium.py`、`final_equilibrium_tools.py` 和 `equilibrium_run_support.py` 的当前 SHA-256 仍逐项等于基准工件记录值。
- 状态：baseline_equilibrium_tests_pass；checkpoint_test_aligned_with_frozen_source

### 2026-07-16 02:24 - 主结果现实机制与均衡措辞修正

- 摘要把 `derived from 1,429,737 BurstGPT records` 改为 `uses 59 complete days from the 1,429,737-record BurstGPT trace`，准确区分原始行数与实际进入日内均值的完整日数量。
- Section 4.2 标题由 `main policy effect` 改为 `main comparison`；正文将 `both policies`、`policy difference` 和 `time-varying policy` 分别改为 `both equilibria`、`equilibrium difference` 和 `time-varying equilibrium`，避免把内生博弈结果误写为外生政策处理效应。
- 在 Table 4 后明确：uniform aggregate peak 为 224.569，低于两家合计容量 252，但 provider B 的 utilization 达 1.450。基准拥塞是异质容量和流量分配造成的服务商局部热点，不是市场总容量不足。
- 同步对修改句采用美式 `utilization/normalized/modeled/summarizes`；其余全文拼写在当天 CAS 终稿中统一处理。
- 数值边界：只增加已有工件可直接验证的解释，没有修改表值、图值、模型或求解代码。
- 数值复核：基准工件给出 combined capacity `252.0`、uniform aggregate peak `224.56887629495142` 和 uniform maximum provider utilization `1.4504804430618476`，与新增解释一致。
- 编译：隔离 `latexmk -xelatex` 退出码 0，仍为 19 页 A4；最终日志无 overfull、underfull、undefined citation/reference、LaTeX warning 或 error。摘要静态计数为 212 词，低于 250 词上限。
- 测试命令失败：两次尝试调用不存在的定向测试节点 `test_manuscript_uses_the_final_artifact_language` 和 `test_manuscript_uses_submission_equilibrium_vocabulary`，Pytest 均退出 4 且未运行测试。检查文件内实际节点后，改跑章节数、摘要/关键词/Highlights 限制和 claim boundary 三项测试，结果为 `3 passed`。
- 状态：equilibrium_language_precise；provider_hotspot_mechanism_explicit；compile_verified

### 2026-07-16 02:27 - 英文主稿美式拼写与语言门禁

- `nature-polishing` 路由：`research / abstract+intro+methods+results+discussion+conclusion+title / English / generic-SMPT`。已读取研究论文、各章节、英文句法和 generic journal 规则；manifest 指向的四个 `_shared/core` 文件在本机技能包中不存在，首次读取返回 `No such file or directory`，没有假装加载。
- 句法扫描：普通正文未发现超过 30 词的句子；`moreover`、`furthermore`、`additionally`、`crucial`、`robust`、`demonstrates` 和 `establishes` 均为 0 次。现稿不需要为了“去 AI 化”大幅重写已经直接的句子。
- 机械统一：将 `utilisation/normalised/optimisation/behaviour/discretisation/randomisation/stylised/realised` 等 23 类英式拼写统一为美式写法；关键词改为 `simulation modeling`。未改变期刊正式名称 *Simulation Modelling Practice and Theory*。
- 编译：隔离 `latexmk -xelatex` 退出码 0，生成 19 页 A4 PDF；最终日志无 overfull、underfull、undefined citation/reference、LaTeX warning 或 error。
- 验证：章节数、摘要/关键词/Highlights、引用键和 claim boundary 四项测试 `4 passed`；相关测试 Ruff 通过，相关文件 `git diff --check` 通过。
- 状态：american_english_consistent；language_static_gates_pass

### 2026-07-16 02:28 - 当前版作者投稿动作表

- 新建 `docs/submission/smpt_author_actions_2026-07-16.md`，替代已标记为历史版本的 2026-06-21 上传清单作为当前作者输入入口。
- 内容：真实作者/机构/通讯信息、Funding、competing interests、CRediT、致谢、Git release、持久 DOI，以及 Figures 1--6 的作者独立重建记录。
- 图像记录为每张图预留重建文件、重建人/日期、SHA-256 和数据/标签/图注确认，不预先勾选，不把当前 AI 辅助内部图源写成投稿合规图。
- 状态：author_action_template_current；all_author_attestations_pending

### 2026-07-16 02:29 - BurstGPT 与 vLLM 锚点独立重算

- 测试：`tests/test_burstgpt_load_anchor.py` 与 `tests/test_final_qos_calibration.py` 在显式 NumPy/SciPy/Pytest 环境下为 `4 passed`。
- BurstGPT 派生工件：8 个 token-share 均值之和为 `1.0000000000000002`，最小/最大份额为 `0.013196/0.216925`；metadata 记录 59 个完整日、1,429,737 行和 0 跳过。原始 50,853,373-byte CSV 当前不在 `/tmp`，本轮未执行原始轨迹全量重聚合，也未声称完成该步骤。
- vLLM 重算：10 个 QoS 均值点，各 5 次重复；未加权 nonlinear least squares 得到 threshold `1.0000000000000002`、strength `0.5747078848823926`、RMSE `0.056074294670863147`，与正式 calibration JSON 在 `1e-12` 内一致。两组 profile RMSE 为 `0.07095/0.03542`，leave-one-model-out test RMSE 为 `0.04543/0.10464`。
- 文字修正：Methodology 明确十个均值点采用未加权非线性最小二乘，并指出 QoS threshold 估计落在预设下界。该事实限制了锚点外推强度，但不改变当前拟合参数或正在运行的 sensitivity provenance。
- 状态：external_anchor_recalculation_pass；qos_fit_boundary_disclosed

### 2026-07-16 02:30 - capacity_low 新动态检查点

- `capacity_low` 于 02:28:06 写入 214,248,170-byte `dynamic.pkl`；队列日志记录 `dynamic cache checkpoint: 40300 pairs`，较上一检查点 33,444 增加 6,856 对。
- 只读反序列化确认缓存 `records` 数为 40,300，签名容器可正常读取。`price_sensitivity_high` 当前仍为 676 对并处于首个大批次。
- 两个进程组合计继续占用约 30 个逻辑核，可用内存约 10 GiB；没有新失败或退出哨兵。
- 状态：capacity_low_progress_confirmed；two_scenarios_running

### 2026-07-16 02:31 - CAS 类文件本地依赖审计

- `kpsewhich` 结果：TeX Live 可找到 `unsrtnat.bst` 和 `xurl.sty`，但没有 `cas-sc.cls` 与 `cas-common.sty`。此前 CAS 预检依赖 `/tmp/elsevier_cas_template_check/els-cas-templates` 的显式 `TEXINPUTS`。
- 官方包 README 标明版本 2.4，`cas-sc.cls`/`cas-common.sty` 为 2024-05-04 版本，并允许按 LaTeX Project Public Licence 1.2/1.3c 或更高版本分发。
- 决策：八场景与正文门禁完成后，在正式投稿目录中加入官方未修改的 `cas-sc.cls`、`cas-common.sty` 和版本/许可说明，再从仓库内执行干净编译；不复制示例 PDF、图片或无关模板资产。
- 状态：cas_runtime_dependency_identified；vendor_step_pending_final_package

### 2026-07-16 02:32 - 可迁移需求比例与无效参数说明

- 参数表将 `Flexible fraction` 改为更准确的 `Reallocatable fraction`。主设计中 flexible population share 为 0.6，且该组的可重排比例为 0.8，因此进入时间选择的总需求比例为 `0.6 x 0.8 = 0.48`。
- Section 4.6 明确这代表 batch-like demand 占比较高的市场，不能外推到以交互请求为主的服务；最大时间窗口仍为两个三小时时段。
- 参数表注明 `kappa_R` 在 `phi_R=0` 时不参与需求计算。保留数值 2 以完整记录配置，但不把它解释为有效的刚性用户迁移成本。
- 编译首次出现 `Overfull \\hbox (15.86804pt too wide)`，定位到参数表的完整解释单元格。将表内 basis 缩为 `Synthetic; inactive for R`；`phi_R=0` 已在方法正文定义，含义不变。
- 复编：退出码 0，19 页 A4；最终日志不再有 overfull/underfull、undefined citation/reference、LaTeX warning 或 error，`git diff --check` 通过。
- 状态：behavioral_scope_explicit；inactive_rigid_migration_cost_disclosed；table_layout_verified

### 2026-07-16 02:35 - vLLM 服务端启动参数边界

- 仓库日志 `docs/vllm-system-benchmark.md` 保存 0.5B 服务端命令：`--dtype auto`、`--max-model-len 2048`、`--gpu-memory-utilization 0.75`。两个 study metadata 的 served-model 记录均显示 `max_model_len=2048`。
- 新证据：同一实验时段的 Codex 执行日志在 `2026-05-31T13:44:51.875Z` 保存了精确 3B 命令，包含 `--dtype auto`、`--max-model-len 2048` 和 `--gpu-memory-utilization 0.75`。这不是根据 0.5B 配置推测所得。
- 边界：3B study artifact 仍未嵌入完整命令，因此 `docs/vllm-system-benchmark.md` 和主稿将执行日志标为补充旁证，不把它误写为工件字段。
- 主稿 Methodology 和三审稿人内部报告同步更新。单 GPU、短生成和小模型的外推限制不变。
- 状态：vllm_launch_provenance_recovered_from_contemporaneous_log；artifact_boundary_disclosed

### 2026-07-16 02:38 - vLLM 参数修订后的稿件验证

- 目标：确认 3B 服务端启动参数出处的修订没有引入 LaTeX 或稿件结构回归。
- 操作：更新 `docs/vllm-system-benchmark.md`、英文主稿和三审稿人内部报告；重新编译 2026-07-14 英文候选稿，并运行该版本的静态稿件测试。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 10 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run --no-project \
    --with pytest --with numpy --with scipy --with nashpy \
    pytest -q tests/test_final_manuscript_20260714.py
  rg -n "Overfull|Underfull|undefined|LaTeX Warning|LaTeX Error|Emergency stop|Fatal error" \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.log
  git diff --check -- docs/vllm-system-benchmark.md \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex \
    docs/reviews/smpt_final_three_reviewer_audit_2026-07-14.md README.md
  ```
- 输出：PDF 为 19 页 A4，SHA-256 为 `2d19a8cc0b44312f5218bcca4c4b0c2d39888cc850ed1ade2879ea6e3099dca6`；最终日志扫描无命中，`git diff --check` 无输出。
- 测试：`5 passed, 3 failed`。三项失败仅对应尚未生成的最终敏感性表、Figure 6 和 `FINAL_SENSITIVITY_RESULTS` 占位符，需等待八个正式场景全部通过后由既定流水线消除；本阶段不把它们记为通过。
- 状态：latex_verified；vllm_provenance_text_verified；final_sensitivity_in_progress

### 2026-07-16 02:45 - 中间商理论目标与数值响应分离

- 目标：消除把多起点局部优化返回值直接写成精确全局 `argmax` 的理论歧义。
- 修改：Eq. (18) 的 $b^*$ 仅表示中间商理论最优响应目标；算法返回值改记为 $\widehat b$，服务商支付矩阵也显式由 $\widehat b$ 生成。有限候选 regret 现限定为对存储数值支付矩阵的验证，不再写成对精确 follower game 的无条件证书。
- 同步：`docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md` 和 `docs/reviews/smpt_submission_evidence_map_2026-07-14.md` 已采用同一证据边界。摘要、结果和结论数字均未改变。
- 语言：修正残留的 `utilised`、`Behavioural`、`normalisation`、`optimiser`、`summarises` 和 `discretises`，统一为美式拼写。
- 回归：为理论目标/数值返回值分离和美式拼写新增两项静态测试。首轮定向测试因遗漏 `summarises` 失败，修正 `summarizes/discretizes` 后复测为 `4 passed, 6 deselected`。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run --no-project \
    --with pytest --with numpy --with scipy --with nashpy \
    pytest -q tests/test_final_manuscript_20260714.py \
    -k 'intermediary_target or american_spelling or claim_boundaries or exactly_five'
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 10 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 输出：定向测试通过；PDF 为 19 页 A4，SHA-256 为 `ff6da876301e8ce96a1c4273c769a163c701e5daa486e621a51444f73361e183`；最终 LaTeX 日志没有 overfull/underfull、未定义引用或错误。
- 敏感性状态：仍只有 `capacity_high` 和 `price_sensitivity_low` 两个正式场景通过，未提前生成跨场景结论。
- 状态：follower_target_and_numerical_response_distinguished；language_regression_verified；sensitivity_2_of_8_verified

### 2026-07-16 02:50 - 数值方法引用审计

- 目标：补齐可复现数值流程的原始算法出处，并核对近期推理市场文献元数据。
- 核验：正文 38 个原 citation key 均存在于 `verified_refs.bib`。Crossref/官方 arXiv 元数据确认 PriLLM 的 AAAI 论文、NBER Working Paper 34608、arXiv:2604.16802 和 arXiv:2603.00356 的题名、作者与年份一致。
- 新增引用：McKay et al. (1979) 的 Latin hypercube、Fischer (1992) 的 Fischer--Burmeister 方法、Byrd et al. (1995) 的 L-BFGS-B，以及 Storn and Price (1997) 的 differential evolution。四个 DOI 均通过 Crossref 返回正式元数据。
- 修改：在中间商优化、互补方程、off-grid 采样和活跃剖面独立搜索首次出现处加入对应 citation，不改变算法、参数或结果。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run --no-project \
    --with pytest pytest -q tests/test_final_manuscript_20260714.py \
    -k 'citations_resolve or intermediary_target or american_spelling'
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 10 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：定向测试 `3 passed, 7 deselected`；BibTeX 最终日志没有缺失或重复条目警告；LaTeX 最终日志没有未定义 citation/reference、版面溢出或错误。PDF 仍为 19 页，SHA-256 为 `39d8ee90f755c0b48ddd7cb8a1aaaec0ece67b10db2d127757f500bb59bea2f0`。
- 计算状态：两个敏感性分支共 36 个相关进程，采样时总 CPU 约 `3109%`；正式完成数仍为 2/8。
- 状态：numerical_method_citations_verified；recent_reference_metadata_checked；sensitivity_running

### 2026-07-16 02:53 - PDF 语言与版面抽检

- 语言检查：`therefore/thus/additionally/furthermore/moreover` 的正文总命中分别为 `2/1/0/0/0`；`robust` 为 0。`mechanism`、`diagnostic` 和 `boundary` 的命中主要来自方法名、节标题或证据限制，没有继续做同义词轮换。
- 失败记录：首次 `pdftotext | python -c` 长句扫描因 shell 引号嵌套错误退出。修正引号后命令可运行，但 PDF 文本会把表格、公式和图内文字拼成“句子”，所得 `41` 个大于 30 词的计数不能作为正文句长证据，因此不据此改写。
- 版面操作：用 `pdftoppm -jpeg -r 85` 渲染 19 页。尝试用 `montage` 生成联系表失败，原因是系统未安装 ImageMagick；未安装新系统依赖，改为直接检查代表性单页。
- 视觉结果：标题页、两项命题、候选集宽表、$b^*/\widehat b$ 记号、参数表、Figures 2--5、结果表和声明页均未发现文字越界、公式重叠、图注遮挡或页脚碰撞。Section 4.5 仍因最终敏感性待生成而偏短，这会在 Figure 6 和结果表插入后消失。
- 图像政策：视觉清晰不改变合规结论。当前 Figures 1--5 仍仅供内部审阅，Figure 6 尚未生成；六图都须由作者独立重建后才能投稿。
- 历史文档：为 `smpt_final_gate_reviewer_report_2026-06-21.md` 增加 superseded 标记，并修正 `smpt_full_figure_audit_2026-06-21.md` 顶部说明，防止旧的“无图像阻塞”判断进入当前投稿包。
- 敏感性状态：正式完成数仍为 2/8。
- 状态：generic_pdf_layout_checked；historical_artwork_claims_quarantined；author_figure_rebuild_required

### 2026-07-16 02:55 - 基准证据链回归

- 目标：在敏感性计算继续运行时，确认基准均衡、结果宏、混合结果分布和三类数值审计没有被论文与引用修改影响。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    /root/.local/bin/uv run --no-project \
    --with pytest --with numpy --with scipy --with nashpy --with matplotlib \
    pytest -q \
      tests/test_submission_evidence_gates.py \
      tests/test_submission_result_macros.py \
      tests/test_submission_mixed_distribution.py \
      tests/test_submission_price_shape_decomposition.py \
      tests/test_submission_mechanism_decomposition.py \
      tests/test_submission_equilibrium_branch_audit.py \
      tests/test_submission_fixed_point_audit.py \
      tests/test_submission_intermediary_audit.py \
      tests/test_final_spatiotemporal_equilibrium.py
  ```
- 结果：`68 passed in 4.56s`。
- 来源冻结：独立重算基准工件记录的 20 个 `source_sha256`，当前工作树 `mismatch_count=0`。论文、README、引用和测试修改没有改变冻结数值实现。
- 敏感性进度：`capacity_low` 已写入 44,105 个动态缓存对，`price_sensitivity_high` 已写入 8,868 个；完成标准仍是正式 `.exit=0`、submission JSON 和门禁通过，而不是缓存对数。
- 状态：baseline_evidence_regression_verified；frozen_numerical_sources_unchanged；sensitivity_running

### 2026-07-16 02:57 - 日边界条件显式化

- 发现：`conserved_temporal_flows` 用 `max(0, origin-H)` 和 `min(T, origin+H+1)` 截断可行目的时段，不把一天末尾与下一天开头循环连接。此前公式的有限窗口可以推知这一点，但正文没有直接说明。
- 修改：Section 3.2 明确可行目的地与 $\mathcal T$ 取交集，迁移窗口不跨日回绕；Section 4.6 将“不允许相邻日期之间迁移”列为模型边界。未改变 OD 概率、需求质量或任何结果。
- 回归：新增静态边界测试；与理论记号、拼写和 claim 边界测试合并运行，结果为 `4 passed, 7 deselected`。
- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 退出码 0；PDF 19 页，SHA-256 为 `3cd58017fc53a5cf287987f83ba91730d028e624cc9e1dd845ec570088243244`，最终日志无版面溢出、未定义引用或错误。
- 状态：temporal_boundary_reproducible；theory_code_audit_updated；numerical_results_unchanged

### 2026-07-16 02:59 - 竞争结果与审计覆盖解释

- 结果逻辑：正文明确统一价格结果只是在零斜率限制下的均衡，因此在允许斜率策略后不必保持稳定。这解释了动态混合均衡的期望终端价格为何在每个时段都低于统一价格，但不额外声称囚徒困境或福利效应。
- 时间机制：动态与统一均衡的 temporally moved fraction 为 `0.327/0.313`，仅增加 1.38 个百分点。正文据此说明 12.32% 的降峰主要依赖迁移目的地重排，而不是迁移总量大幅增加。
- 数值边界：明确 differential-evolution follower audit 与固定点多初值 audit 覆盖 676 个正概率剖面，不覆盖全部 46,381 个缓存支付对。证据映射表同步更新，避免把活跃支持审计外推为全支付矩阵全局性证明。
- 回归：新增 audit coverage 静态检查；相关定向测试 `5 passed, 7 deselected`。
- 编译：退出码 0；PDF 19 页，SHA-256 为 `e6de8ded7403a88d533bc6d2c4f75061db5abccfa6a4239d283fbb73cf46148a`；最终日志无 overfull/underfull、未定义引用或错误。
- 敏感性状态：正式完成数仍为 2/8。
- 状态：competition_interpretation_clarified；movement_amount_vs_destination_explained；active_profile_audit_scope_disclosed

### 2026-07-16 03:01 - 公开仓库状态与 Data availability 修正

- 事实核对：本地 `main`/HEAD 为 `6f483084178c3934d1340ba95cd469ae9dd1141d`，远端 `origin/main` 为 `0941d97af4afa33a0b150a77bfada33ef779c9ed`，远端是本地历史祖先；当前工作树还有 155 个已修改或未跟踪路径，最终 788 候选稿和新工件尚未发布。
- 修改：审阅稿不再声称当前 submission artifacts 已在公开仓库中。Data and code availability 改为正在组装版本化公开发布，并明确投稿前须用 release tag 和持久归档标识替换临时句子。
- 约束：未在敏感性运行期间创建大范围提交或推送；最终 release 只能在八场景、后处理门禁、CAS 稿和文件范围审查完成后建立。
- 回归：新增未发布归档声明测试；相关定向测试 `6 passed, 7 deselected`。
- 编译：退出码 0；PDF 19 页，SHA-256 为 `9da1db3c9292c3a6c47b9818996c71d7c04eb23b2215e03de8c6d431b7f1e8f2`；最终日志无 overfull/underfull、未定义引用或错误。
- 敏感性状态：正式完成数仍为 2/8。
- 状态：data_availability_matches_remote_state；release_pending_final_gates；no_premature_publication_claim

### 2026-07-16 03:07 - 敏感性设计范围与结构比例说明

- 目标：避免把八个参数场景误读为覆盖异质性结构和参数交互的全局稳健性实验。
- 代码核对：`final_case` 对两家容量共同乘以同一 scale，对两类价格敏感度和迁移成本也分别共同乘以同一 scale。容量比 `G_A/G_B=2.5`、价格敏感度比 `alpha_F/alpha_R=2.5` 因而保持不变。刚性类型满足 `phi_R=H_R=0`，其迁移成本不进入实际时移流量；迁移成本场景只改变弹性类型的计算分配。
- 论文修改：Section 3 明确八个场景是 local one-factor-at-a-time re-solves，报告共同缩放方式、保持不变的比例和不估计参数交互的边界；Section 4.6 同步说明这些实验不能代表其他异质性结构或全参数空间。
- 审计同步：更新 `smpt_submission_evidence_map_2026-07-14.md` 和 `smpt_final_three_reviewer_audit_2026-07-14.md`，将最终允许 claim 限定为局部参数水平敏感性。
- 回归：新增 `test_sensitivity_scope_is_local_and_preserves_structural_ratios`。首轮测试发现新增公式中的 `\\alpha_F` 因补丁转义丢失反斜杠；修复后定向测试通过。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run --no-project \
    --with pytest pytest -q tests/test_final_manuscript_20260714.py \
    -k 'sensitivity_scope or exactly_five or claim_boundaries or temporal_boundary or numerical_audit_coverage or data_availability'
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 10 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：`6 passed, 8 deselected`；PDF 为 20 页 A4，SHA-256 为 `b802b9e8da7665aa26b73597036b12920537383b1fa6693d0df69cf57cfd11fb`。最终日志无 overfull/underfull、未定义引用或 LaTeX 错误，`git diff --check` 无输出。
- 敏感性状态：正式通过仍为 2/8；`capacity_low` 和 `price_sensitivity_high` 正在全量计算。
- 状态：local_sensitivity_scope_explicit；structural_ratios_preserved；latex_and_regression_verified

### 2026-07-16 03:12 - V&V 术语与共同候选集边界

- 目标：按仿真期刊语义区分模型校核、输入锚定和市场层外部验证，并约束敏感性结论的策略空间范围。
- 修改：关键词中的 `verification and validation` 改为 `model verification`。Section 3 将 OD 守恒、会计抵消、固定点残差和 regret 归为 model verification；BurstGPT 与单 GPU vLLM 数据只称 empirical input anchoring，并明确 simulated market outcomes are not externally validated。
- 候选集边界：baseline 执行有界 off-grid search，八个扰动场景只在共同 788-rule set 内重求，不做 scenario-specific off-grid expansion。Section 4.6、证据映射和三审稿人报告均明确其均衡证书对共同有限集合有条件，不能外推连续策略邻域。
- 回归：新增 `test_verification_is_not_presented_as_market_level_validation` 和 `test_sensitivity_equilibria_remain_conditional_on_common_candidate_set`。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run --no-project \
    --with pytest pytest -q tests/test_final_manuscript_20260714.py \
    -k 'verification_is_not or sensitivity_equilibria or sensitivity_scope or abstract_keywords or claim_boundaries'
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 10 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：`5 passed, 11 deselected`；PDF 为 20 页 A4，SHA-256 为 `f9555f8c4cfb8a811d38bce97d3bdb8cbe7078ff1f102798a8bd1453f39c67d8`。最终日志无 overfull/underfull、未定义引用或 LaTeX 错误，相关 `git diff --check` 通过。
- 计算状态：正式完成仍为 2/8；两个分支持续占用约 30 个 CPU 核心，未发现可验证的 CUDA 加速路径。
- 状态：verification_and_input_anchoring_distinguished；no_external_market_validation_claim；scenario_certificates_finite_set_conditional

### 2026-07-16 03:15 - 固定点选择规则与公式自包含检查

- 理论问题：命题 1 只证明市场固定点存在，不能直接把中间商利润写成与固定点选择无关的唯一函数，也不能由紧域自动声称实际数值目标的全局 `argmax` 已存在且唯一。
- 修改：Eq. (18) 前明确 `Pi_I(i,j,b)` 取声明的 unit-QoS/equal-routing 初值、阻尼和容差返回的数值固定点；不收敛评估不作为响应候选。`b*` 只表示最大值可达到时的理想目标，`b-hat` 仍是支付矩阵使用的多起点数值返回值；不新增解析存在性或唯一性 claim。
- 自包含性：在首次出现处定义路由价格/QoS 权重 `beta/eta`、QoS threshold/strength `u-bar/zeta`、成本系数 `c_G/c_q` 和均衡收益 `v_A/v_B`。PDF 不再要求读者到参数表或代码中反查这些符号。
- 容量说明：正文明确 `(180,72)` 是 normalized service-rate stress case，不由 RTX 4090 测量换算，也不表示物理 GPU 数量。
- 回归：扩展中间商理论/数值响应测试，并新增公式符号和容量校准边界测试。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run --no-project \
    --with pytest pytest -q tests/test_final_manuscript_20260714.py \
    -k 'model_equation_symbols or intermediary_target or capacity_stress or verification_is_not or sensitivity_equilibria or sensitivity_scope'
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 10 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：`6 passed, 12 deselected`；PDF 为 20 页 A4，SHA-256 为 `4024ea544199b84c2fa6f70634b699165491b121dee790b5a460ce644103158f`。最终日志无 overfull/underfull、未定义引用或 LaTeX 错误，相关 `git diff --check` 通过。
- 敏感性进度：正式通过仍为 2/8；`capacity_low` 已写入 47,139 个缓存对，完成仍以 `.exit=0`、正式 JSON 和独立门禁为准。
- 状态：fixed_point_selection_rule_disclosed；ideal_vs_numerical_follower_target_explicit；equations_self_contained

### 2026-07-16 03:19 - 混合统计量与价格系数解释复核

- 数字重算：正式均衡工件给出动态 `min(E[q])=0.9590676577`，而主表统计量为 `E[min(q)]=0.9585889872`。两者在三位小数都显示为 `0.959`，但不是同一运算顺序。
- 修改：结果段用四位小数写明期望 QoS 曲线最低值 `0.8899 -> 0.9591`，并单列剖面级 `E[min(q)]=0.9586`，明确二者在舍入前不同。证据映射增加对应条目。
- 经济解释：由于无 outside option 且总需求守恒，`alpha_k` 改称 utility price coefficient；正文说明它改变 period--channel 备选项的分配，不是总市场需求的 own-price elasticity。参数表同步改名，敏感性场景仍保持既有数值和代码标识。
- 回归：新增混合 QoS 极值顺序和价格系数含义测试。除等待 Figure 6/敏感性表/占位替换的三项门禁外，当前稿件静态测试为 `17 passed, 3 deselected`。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run --no-project \
    --with pytest pytest -q tests/test_final_manuscript_20260714.py \
    -k 'not submission_figures_exist_and_are_referenced and not resolved_sensitivity_table_and_figure_are_both_integrated and not submission_text_has_no_result_placeholders_or_stale_main_values'
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 10 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：PDF 20 页 A4，SHA-256 为 `976b63e81454d74f6e08d3546de028e6867f4917f2533ed5317249a775476a95`；LaTeX 日志和 `git diff --check` 均无异常。
- 状态：mixed_extrema_order_explicit；price_coefficient_not_market_elasticity；manuscript_static_gate_17_of_20

### 2026-07-16 03:22 - 价格系数术语收束与主稿复编译

- 目标：消除正文中残留的 `price sensitivity`，避免将固定总需求 logit 模型中的效用价格系数误写为市场需求弹性。
- 修改：实验设置中的合成参数边界改为 `utility price coefficients`；展望改为通过受控工作负载实验估计效用价格系数和迁移成本。相关工作、敏感性设计、参数表与局限性现在使用同一术语。
- 定向测试：除等待 Figure 6、敏感性表和结果占位替换的三项门禁外，结果为 `17 passed, 3 deselected`。
- 编译命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 10 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 0；PDF 为 20 页 A4，SHA-256 为 `b0e17048f98c94915eeb1e692ab1755138b8945f7b62e15ac99dc951d172f6cc`。
- 日志检查：首个 `rg` 正则扫描因 `\\hbox` 转义被解析为无效正则而失败；随后改用 `rg -F` 固定字符串扫描，LaTeX error、未定义引用/引用文献和 overfull box 均为零匹配。`git diff --check` 无输出。
- 敏感性进度：正式通过仍为 2/8；`capacity_low` 已推进到至少 48,653 个动态缓存对，`price_sensitivity_high` 仍在计算。两分支约占用 28 个并行工作进程；求解器没有已验证的 CUDA 路径。
- 状态：utility_price_coefficient_consistent；latex_verified；sensitivity_in_progress

### 2026-07-16 03:29 - 敏感性展示术语与排队模型边界

- 展示一致性：预审自动生成的敏感性表和 Figure 6 时发现展示标签仍写作 `Price sensitivity`。只将表格标签改为 `Utility coefficient`、图中标签改为 `Utility coeff.`；场景 ID、参数、求解器、缓存和数值逻辑均未修改。
- TDD：先扩展 `test_price_coefficient_is_not_presented_as_total_demand_elasticity`，测试按预期失败；修改 `build_submission_sensitivity_table.py` 与 `build_final_submission_figures.py` 后，结果为 `1 passed, 19 deselected`。
- 现实性审计：模型允许 `u>1`，但用约化 QoS 曲线表示超过固定服务率参考值后的质量下降，没有模拟服务积压或跨时段 queue carryover。因此 `1.223` 等利用率是服务压力指标，不是队列稳定性结果。
- 论文修改：在 QoS 方程后说明 `G_m` 的服务率参考含义与不截断需求的设定；在 Section 4.6 明确无 interperiod backlog 和无 queue-stability claim。证据映射与三审稿人报告同步更新。
- TDD：新增 `test_utilization_above_one_is_not_presented_as_queue_stability`；测试先失败，正文修改后与价格系数测试合并结果为 `2 passed, 19 deselected`。排除等待 Figure 6、敏感性表和占位替换的三项门禁后，完整稿件静态检查为 `18 passed, 3 deselected`。
- 编译：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 10 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：退出码 0；PDF 20 页，SHA-256 为 `2cb82d1c6a63d12e298388c061634f2f124c38fa225acde2382ee5c9317018a6`。固定字符串日志扫描无 LaTeX error、未定义引用或 overfull box；PDF 文本已检出新增边界句。
- 状态：sensitivity_labels_semantically_correct；queue_dynamics_boundary_disclosed；numerical_source_unchanged

### 2026-07-16 03:33 - 并行入口与检查点回归审计

- 发现：`test_run_sensitivity_forwards_parallel_workers` 同时要求不存在于 `run_equilibria` 签名中的 `checkpoint_interval=1024`，而 `test_pair_evaluator_has_explicit_cache_checkpoint_interval` 明确规定当前冻结实现的默认值为 8192。冻结提交中的两项断言互相冲突。
- 复现命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run --no-project \
    --with pytest pytest -q \
    tests/test_submission_spatiotemporal_sensitivity.py::test_run_sensitivity_forwards_parallel_workers
  ```
- 复现结果：失败，`KeyError: 'checkpoint_interval'`。正在运行的两个场景分支继续使用冻结数值源码；未修改 runner、`PairEvaluator`、缓存签名或求解器。
- 修正：从 worker 转发测试中删除无关的 1024 断言，检查点默认值继续由独立测试锁定为 8192。缓存写入采用临时文件后原子替换，并在每批缺失候选评估结束时强制写入；成功完成的正式场景不受该测试修正影响。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 15 \
    /root/.local/bin/uv run --no-project --with pytest --with numpy \
    --with scipy --with nashpy pytest -q \
    tests/test_final_spatiotemporal_equilibrium.py \
    tests/test_equilibrium_cache.py \
    tests/test_submission_spatiotemporal_sensitivity.py
  ```
- 结果：`21 passed in 4.27s`。数值源码未变，测试职责现在分别覆盖并行 worker 转发、8192 默认间隔、并行中途/批末检查点以及串并行缓存签名一致性。
- 决策：不在八场景运行期间把间隔改为 1024；否则场景工件结束时记录的源码哈希将不再对应实际加载执行的代码。
- 状态：stale_test_assertion_fixed；checkpoint_interval_8192_verified；frozen_numerical_provenance_preserved

### 2026-07-16 03:39 - Figure 6 分组布局预审

- 目标：在正式九场景汇总生成前验证长标签、面板说明和图例不会重叠，不使用虚拟预览支持任何论文结论。
- 预览：用九行虚拟数值将 `_resolved_sensitivity` 输出到 `/tmp/resolved_sensitivity_preview_v1` 至 `v5`。前三版依次暴露斜标签与面板说明重叠、两行英文标签横向重叠、参数符号下的幅度字符串相连；这些版本均未写入正式 `figures/`。
- 最终布局：将八个扰动按四个参数分组。横轴为 `Base`、$G$、$\alpha$、$\kappa$、$\bar u$；每个参数用蓝色 `Lower` 与红色 `Higher` 并列，baseline 为灰色。每个面板都显示三色图例，`(a)--(d)` 说明位于横轴下方且不与标签相交。精确扰动幅度留给最终 LaTeX caption。
- 配色：继续使用统一 SCI palette：neutral `#7A7A7A`、primary `#3C5488`、contrast `#A86464`。未修改任何数值或正式图。
- 回归：布局改动后旧测试因引用已删除的 `SENSITIVITY_COLORS`/`SENSITIVITY_LABELS` 失败 2 项；恢复三色常量并将测试迁移到 `SENSITIVITY_FACTOR_LABELS` 后，定向结果为 `5 passed, 26 deselected`。
- 进度：`capacity_low` 已推进到至少 51,675 个动态缓存对；正式完成仍为 2/8。
- 状态：figure6_preview_visually_clean；panel_legends_repeated；formal_figure_waits_for_validated_data

### 2026-07-16 03:43 - 机制分解非可加性与未扫描参数边界

- 机制解释：temporal-only、spatial-only 和 combined 都在固定价格剖面下重新求解渠道选择、路由和 QoS，因此三组差值不是可相加的因果分量。Section 4.4 已用直接句子替换“each pathway explains part”的模糊表述，证据映射同步限定。
- 敏感性边界：Section 4.6 新增未扫描项，包括 flexible/reallocatable population shares、channel preferences、QoS choice/routing weights、QoS curvature 和 cost coefficients。八场景完成后仍不能把结果外推到这些维度。
- Figure 6 回归：旧图接口测试先出现 2 个失败（删除的 `SENSITIVITY_COLORS` 与 `SENSITIVITY_LABELS`）；恢复三色常量、迁移到五组 `SENSITIVITY_FACTOR_LABELS` 后，相关图与语言测试为 `5 passed, 26 deselected`。
- 稿件门禁：等待三项敏感性集成门禁之外，结果为 `18 passed, 3 deselected`。
- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 退出码 0；PDF 20 页，SHA-256 为 `dbbd3895613860f74ddd34827482bc06a0063c53e049d890239095ed3d05b7b8`。日志无 error、未定义引用、overfull 或 underfull box。
- 状态：mechanism_comparisons_nonadditive；unvaried_parameters_disclosed；manuscript_verified

### 2026-07-16 03:47 - 后处理测试环境与 Figure 6 门禁预检

- 环境探测：裸 `uv run python -c 'import ... nashpy'` 因当前无项目解释器缺少 `nashpy` 而退出 1。该命令不是正式后处理命令，先用于判断等待脚本是否存在依赖风险。
- 实际验证：按后处理脚本原样使用裸 `uv run pytest` 运行固定点、中间商、机制和 evidence-gate 测试，结果 `34 passed`；sensitivity claim/table 测试结果 `7 passed`。这些测试不依赖 `nashpy`，因此无需终止或重启已等待的后处理进程。
- Figure 6：分组布局的灰/蓝/红三色常量、五个参数标签、场景顺序拒绝和表格生成器均已定向验证。一次组合 `-k` 误选了仍应等待的“正式表和图已集成”测试，出现预期的 1 个失败；改用明确节点后结果 `6 passed`。
- 术语门禁：`submission_sensitivity_table.tex` 的单元测试新增 `Utility coefficient -20%` 断言，结果 `2 passed`，防止后处理重新引入 total-demand elasticity 的错误暗示。
- 运行进度：`capacity_low` 已推进到至少 53,183 个动态缓存对；`price_sensitivity_high` 的 12 个 worker 持续高负载运行。
- 状态：post_pipeline_environment_verified；expected_integration_gate_preserved；figure6_generation_tests_ready

### 2026-07-16 03:52 - 投稿证据回归与基线审计范围

- 回归范围：对候选清单、均衡分支、缓存、共同候选集敏感性、固定点、中间商响应、机制分解、claim 表、LaTeX 表和终稿图生成器执行组合回归。
- 结果：`91 passed, 2 deselected in 4.04s`。两项 deselected 均依赖尚未生成的正式九场景敏感性汇总，不是既有证据失败。
- 审计边界：更新 claim 构建器和证据映射，明确 differential-evolution follower audit、固定点多初值 audit 和 bounded off-grid search 只覆盖 baseline，不外推到八个敏感性均衡。
- Figure 6 字体预检：Times 配置的第六版虚拟布局导出成功，PDF 字体为嵌入式 `TimesNewRomanPSMT` 与 `STIXGeneral`。虚拟数值只用于排版检查，不进入正式图或论文结论。
- 状态：broad_evidence_regression_passed；baseline_only_independent_audits_explicit；formal_sensitivity_outputs_pending

### 2026-07-16 03:59 - SMPT 官方规则复核与最新主稿编译

- 期刊依据：SMPT Guide for Authors 要求应用型论文透明呈现模型开发、实现、数值问题以及 verification/validation；摘要不超过 250 词，关键词 1--7 个，Highlights 为 3--5 条且每条不超过 85 个字符，审稿方式为 single anonymized。
- 图像政策：期刊专属 Guide 仍禁止 generative AI 或 AI-assisted tools 创建或修改投稿图像。Elsevier 较新的通用政策允许特定解释性图和可复现数据图，但两者当前存在文本冲突。投稿动作表继续采用更严格的期刊专属规则，并新增官方链接与编辑部书面确认选项。
- 稿件门禁：等待 Figure 6、敏感性表和结果占位替换的三项门禁之外，`tests/test_final_manuscript_20260714.py` 为 `18 passed, 3 deselected`。
- 编译命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 15 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 0；PDF 为 21 页 A4，SHA-256 为 `ab4b53b9dc64ced40fdb98bc6e1713601e7dc621adcc533fd34f1d5e84472d6e`。日志无 LaTeX error、未定义引用/文献、overfull 或 underfull box；`git diff --check` 无输出。
- 运行状态：`capacity_low` 与 `price_sensitivity_high` 继续以 16/12 个 CPU worker 计算；正式完成数仍为 2/8，未修改冻结数值源码。
- 状态：journal_policy_conflict_documented；manuscript_static_gate_passed；sensitivity_in_progress

### 2026-07-16 04:05 - 语言量化与近期参考文献复核

- 语言门禁：摘要为 211 词，关键词 7 个；5 条 Highlights 的字符数为 `73/82/75/66/68`，均满足期刊上限。高频模板词和 humanizer 词表扫描未发现宣传式表达、破折号滥用或常见 AI 连接词堆叠。
- 术语修改：`simulation modeling` 统一为期刊题名采用的 `simulation modelling`；摘要的 `capacity-heterogeneous providers` 改为 `providers of different capacities`；引言的模糊短语 `token contracts` 改为与所引文献更一致的 `token-based capacity control`。
- 文献复核：在 NBER、AAAI 和 arXiv 主页面核对了 `demirer2025emerging`、`guo2026prillm`、`bergemann2025menu`、`yan2026stackelberg` 和 `cunningham2026token` 的题名、作者、年份/提交日期和标识符，未发现虚构或错配。正文不把预印本写成已正式录用论文。
- 回归：不依赖正式 Figure 6 的稿件静态门禁仍为 `18 passed, 3 deselected`；相关 Figure 6、claim 和 manuscript 文件的 Ruff 检查为 `All checks passed!`。
- 状态：language_constraints_passed；recent_references_primary_source_checked；technical_meaning_preserved

### 2026-07-16 04:10 - 21 页审阅稿视觉检查

- 首次联系表命令调用 ImageMagick `montage` 失败，错误为 `montage: command not found`。未安装新系统软件，随后使用环境已有的 `ffmpeg` 将选定页面合成为 `/tmp/smpt_pdf_review_20260716/contact.png`。
- 视觉范围：检查第 4、10、12--16 和 21 页，覆盖 Figure 1、参数表、主结果表、Figures 3--5、敏感性占位与限制段。未发现图内遮挡、图注错位、表格越界、正文重叠或不可辨认的面板标注。
- 当前排版问题：第 21 页只有参考文献末条，视觉上偏空。敏感性表与 Figure 6 尚未插入，且最终稿还要迁移到 Elsevier CAS 模板，因此不在通用 article 审阅稿中提前调整参考文献字号或分页。
- 图形对象：`pdfimages -list` 未列出嵌入位图对象；当前 Figures 1--5 仍为矢量输出。该技术检查不替代 SMPT 的 AI 图像政策门禁。
- 复编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error` 退出码 0；PDF 21 页 A4，SHA-256 为 `39c970279661d1f2e7894b766cfdd808c5e7ebcd51d92f8dac11b137090cb171`。日志中 error、未定义引用/文献、overfull 和 underfull 均为零。
- 状态：visual_review_passed；sparse_last_reference_page_deferred_to_cas；latex_verified

### 2026-07-16 04:14 - 敏感性运行 GPU 可用性复核

- 硬件：`nvidia-smi` 可见 `NVIDIA GeForce RTX 4090`，驱动 `596.21`，显存 `24564 MiB`；检查时 GPU 利用率为 1%。
- 运行时：当前敏感性解释器使用 NumPy `2.4.4` 和 SciPy `1.17.1`，数组模块为 `numpy`；`import cupy` 返回 `ModuleNotFoundError`。
- 决策：核心计算由 SciPy 的固定点与 L-BFGS-B/互补求解路径组成，没有已验证的 CUDA 后端。在场景运行期间引入 CuPy 或重写优化器会改变数值路径与来源哈希，因此不切换 GPU。两个分支继续使用 16 和 12 个 CPU worker。
- 状态：gpu_visible_but_no_validated_solver_path；cpu_parallelism_retained；numerical_provenance_preserved

### 2026-07-16 04:20 - 五章英文标题自然化

- 修改：保持五个编号主章节不变，将 `Related research` 改为更常见的 `Related work`，将 `Conclusion and outlook` 改为 `Conclusions and future work`。未新增 Discussion 或其他主章节。
- TDD：先修改五章结构测试，定向测试按预期失败，差异定位到旧的两个标题；随后修改 TeX，定向测试 `1 passed`，不依赖正式敏感性输出的完整稿件门禁为 `18 passed, 3 deselected`。
- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error` 退出码 0；PDF 21 页 A4，SHA-256 为 `d94d919a0eea8f9e3223303caf98b6db7d74fa9c06eb17bf8269cdcd05db3697`。日志无 error、未定义引用/文献、overfull 或 underfull box。
- 状态：five_section_structure_preserved；section_titles_naturalized；latex_verified

### 2026-07-16 04:27 - 小节标题去内部报告化

- 修改：将 `Data anchors, parameter design, and verification` 改为 `Data inputs, parameter design, and model verification`，将 `Load and QoS anchors` 改为 `Load and QoS inputs`，将结果中的敏感性与边界小节改为 `Sensitivity analysis` 和 `Interpretation and limitations`。
- 约束：只修改标题和对应测试定位字符串；正文内容、公式编号、数据、引用和章节数量均未改变。
- 回归：不依赖正式敏感性输出的稿件门禁为 `18 passed, 3 deselected`；`git diff --check` 无输出。
- 编译：退出码 0；PDF 21 页 A4，SHA-256 为 `5a7416c25d98c921d9eba71788d7e9e22ecd2722b21abe83f8260b49f565a742`。日志无 error、未定义引用/文献、overfull 或 underfull box。
- 状态：subsection_titles_simplified；technical_content_unchanged；latex_verified

### 2026-07-16 04:30 - 已完成敏感性场景来源复核

- 命令：使用 `validate_sensitivity_scenario` 和冻结 baseline SHA 再次验证 `capacity_high` 与 `price_sensitivity_low`。
- 结果：两者均为 `passed=true`，来源文件数均为 20；uniform/dynamic 最大 regret 分别不高于 `0/2.27e-13`，最大联合残差分别不高于 `9.95e-10` 和 `9.92e-10`。
- 工件哈希：`capacity_high` 为 `0a2a065ab6dc937cf2c56ab32363e3b65365d5663e3f4a0d4ae819c875446be2`；`price_sensitivity_low` 为 `c1335d1d7614515dd91ef0fa3dfe22c9cd0d34684de04240c44279361614db07`。
- 进度：`capacity_low` 已写入至少 59,195 个动态支付对；正式通过仍为 2/8。
- 状态：completed_scenarios_revalidated；provenance_unchanged；remaining_scenarios_running

### 2026-07-16 04:35 - 电力层级博弈文献定位补强

- 官方核对：ScienceDirect 页面确认 Wang、Han、Bao 的三层 Stackelberg 虚拟电厂研究发表于 `Sustainable Energy, Grids and Networks` 46 (2026), 102245，DOI 为 `10.1016/j.segan.2026.102245`。
- 论文修改：Related work 新增一句说明该研究包含配电系统运营者、虚拟电厂和用户三层交互，并用固定点求解；紧接着指出其约束和结果属于电力调度，不包含本文的双推理服务商竞争、API 中间商、直购渠道和内生 QoS。
- 目的：补入 2026 年电力层级博弈进展，同时避免用“现有电力模型都只有单一零售商”这类过度概括。
- 验证：五章结构与引用解析测试 `2 passed`；编译退出码 0，PDF 21 页 A4，SHA-256 为 `354da79d16238b95d0e7104b3a25a6ce12d98318b9307871c3213372646ec2a0`。日志无 error、未定义引用/文献、overfull 或 underfull box。
- 状态：electricity_game_positioning_updated；recent_primary_source_verified；latex_verified

### 2026-07-16 04:42 - 引言贡献段自然化

- 修改：将内部审计式短语 `auditable bounded price rules` 改为 `a declared set of bounded price rules`；贡献段按模型、求解和数据输入重新连句，并把 `measured QoS-shape anchor` 改为更自然的 `measured QoS curve`。
- 边界：仍明确 observed load shape、measured QoS curve 与 synthetic economic parameters 的区别；未新增模型、证据或贡献 claim。
- 验证：不依赖正式敏感性输出的稿件门禁为 `18 passed, 3 deselected`。LaTeX 编译退出码 0，PDF SHA-256 为 `48e68fe734b6c78088008f64d67463cac44b366dfd897b827c657206c6d12073`；日志门禁和 `git diff --check` 均通过。
- 状态：introduction_prose_naturalized；claim_scope_preserved；latex_verified

### 2026-07-16 04:47 - 纳什条件与数值求解关系说明

- 目标：回应“论文是否需要推导纳什均衡”的理论完整性问题，同时避免把有限候选集数值均衡写成连续价格空间的闭式解。
- 修改：在式 (16)--(17) 的双矩阵纳什互补条件后补充说明：每个收益矩阵元素都包含中间商数值响应和市场固定点，因此这些条件不能导出闭式 tariff；本文求解的是已声明有限博弈的数值均衡。
- 编辑记录：第一次 `apply_patch` 因 JavaScript 字符串解释 LaTeX 反斜杠而未通过补丁校验，未改动文件；改用原始字符串后成功应用。
- 定向验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest -q \
    tests/test_final_manuscript_20260714.py::test_intermediary_target_is_distinguished_from_numerical_response \
    tests/test_final_manuscript_20260714.py::test_nash_conditions_explain_why_no_closed_form_tariff_is_claimed
  ```
- 结果：`2 passed in 0.02s`。
- 稿件门禁：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest -q \
    tests/test_final_manuscript_20260714.py \
    --deselect tests/test_final_manuscript_20260714.py::test_submission_figures_exist_and_are_referenced \
    --deselect tests/test_final_manuscript_20260714.py::test_resolved_sensitivity_table_and_figure_are_both_integrated \
    --deselect tests/test_final_manuscript_20260714.py::test_submission_text_has_no_result_placeholders_or_stale_main_values
  ```
- 结果：`19 passed, 3 deselected in 0.04s`；三项暂缓测试仅等待正式敏感性表、Figure 6 和结果占位替换。
- 编译证据：最近一次 XeLaTeX 编译退出码 0，21 页 PDF SHA-256 为 `f8e44f92e802c745bfa10d557710f39638a409658c168518cfc7f20598e42349`；日志无 error、未定义引用/文献、overfull 或 underfull box。
- 状态：nash_conditions_complete_for_declared_finite_game；closed_form_not_claimed；sensitivity_integration_pending

### 2026-07-16 04:53 - 两阶段需求分配说明与理论审计同步

- 修改：在渠道需求式后明确 destination choice 与 conditional channel choice 是同一守恒 OD 流量的两个分配阶段，不是两个相加的需求来源。该句只澄清模型顺序，不改变效用、份额、需求或结果数值。
- 审计：`docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md` 同步记录该解释，并记录纳什互补条件不能从含数值中间商响应和固定点的收益元素中导出闭式 tariff。
- 编辑记录：第一次更新审计文档时，JavaScript 模板字符串中的 Markdown 反引号触发语法错误，补丁未执行；重新构造补丁后成功，未造成部分写入。
- 稿件门禁：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run pytest -q \
    tests/test_final_manuscript_20260714.py \
    --deselect tests/test_final_manuscript_20260714.py::test_submission_figures_exist_and_are_referenced \
    --deselect tests/test_final_manuscript_20260714.py::test_resolved_sensitivity_table_and_figure_are_both_integrated \
    --deselect tests/test_final_manuscript_20260714.py::test_submission_text_has_no_result_placeholders_or_stale_main_values
  ```
- 结果：`20 passed, 3 deselected in 0.07s`；新增测试固定“一份守恒流量、两阶段分配”的说明。
- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 退出码 0；PDF 为 21 页 A4，SHA-256 为 `245c368bf84fed90fd0ce04dd99be0600831fa810f29af8b29a3a29893c8ad4a`。日志无 LaTeX error、未定义引用/文献、overfull 或 underfull box；相关文件 `git diff --check` 无输出。
- 状态：sequential_choice_clarified；duplicate_demand_interpretation_removed；latex_verified

### 2026-07-16 05:02 - 仿真 verification/validation 方法学定位

- 文献核验：通过期刊正式页面核对 Sargent, *Verification and Validation of Simulation Models*, *Journal of Simulation* 7(1), 12--24 (2013)，DOI `10.1057/jos.2012.20`，并加入 `verified_refs.bib`。
- 论文修改：Related work 明确区分 model verification 与针对观测系统的 validation。守恒、会计抵消、残差和 regret 被归入 verification；BurstGPT 与 vLLM 只提供经验输入，不能验证市场层输出。
- 目的：强化 SMPT 的建模与仿真定位，同时阻止把数值一致性测试写成现实有效性证据。
- 验证：不依赖正式敏感性输出的稿件门禁为 `20 passed, 3 deselected`；新增引用已进入 BibTeX 且最终编译日志无 undefined citation。
- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 退出码 0；PDF SHA-256 为 `945150e8bf5beda2f4b4262c7961173a6d2c91d5f2b5ec060bce4cea57e2b7d5`。最终日志无 LaTeX error、未定义引用/文献、overfull 或 underfull box；相关文件 `git diff --check` 无输出。
- 状态：simulation_vv_positioning_added；market_validation_not_claimed；latex_verified

### 2026-07-16 05:10 - 敏感性场景参数身份门禁

- 审查发现：场景工件已保存 `capacity_scale`、`price_sensitivity_scale`、`migration_cost_scale` 和 `qos_threshold_shift`，但原 `validate_sensitivity_scenario` 只检查基准 SHA、来源、候选数、regret 和残差，未核对场景名与四个参数。
- TDD：新增“`capacity_low` 工件若写入 `capacity_scale=1.15` 必须拒绝”的测试；修改门禁前按预期失败，错误为 `Failed: DID NOT RAISE ValueError`。随后门禁从唯一事实源 `SCENARIOS` 构造完整期望参数并要求工件 `scenario` 精确匹配。
- 边界：只修改证据验证层，不修改市场模型、求解器、场景定义或正在执行的数值路径；场景工件的 20 个冻结来源中不包含该门禁文件。
- 验证：新测试与有效工件测试为 `2 passed`；证据门禁与敏感性 runner 组合测试为 `22 passed in 0.50s`。完成的 `capacity_high` 与 `price_sensitivity_low` 在新门禁下再次通过，full regret 和残差保持不变。
- 静态检查：首次 `uv run ruff` 因项目环境未安装 ruff 退出 2，错误为 `Failed to spawn: ruff`；改用 `uv run --no-project --with ruff ruff check ...` 后为 `All checks passed!`。
- 状态：scenario_identity_gate_added；completed_artifacts_revalidated；numerical_solver_unchanged

### 2026-07-16 05:18 - 共同策略空间门禁

- 审查发现：旧门禁要求 `full_candidate_count=788`，但没有逐元素比较场景候选向量，也没有核对中间商响应的 method、uniform search spec 和 dynamic search spec。仅有相同数量不足以支持“共同候选集”表述。
- TDD：分别篡改候选向量和中间商 method 的两个测试先因接口尚不存在而失败，均为 `TypeError: unexpected keyword argument 'expected_baseline'`。随后增加 baseline strategy contract 比较，忽略只影响计算吞吐的 `parallel_workers`，严格比较候选数组和两类响应搜索规则。
- 运行行为：实际门禁在 baseline SHA 与正式均衡工件匹配时自动读取该 baseline contract；测试也可显式传入 baseline。该修改不进入市场求解或支付计算。
- 验证：两个篡改测试与有效工件测试为 `3 passed`；证据门禁与敏感性 runner 组合测试为 `24 passed in 0.40s`。`capacity_high` 和 `price_sensitivity_low` 均在增强门禁下通过，来源数仍为 20。Ruff 为 `All checks passed!`。
- 状态：common_candidate_vectors_verified；continuous_follower_contract_verified；completed_artifacts_revalidated

### 2026-07-16 05:25 - 场景级需求守恒与博弈规模门禁

- 审查发现：敏感性验证器尚未检查 uniform/dynamic 的实际候选数和 `expected_metrics.total_demand`。这会使“共同 788 候选动态博弈、12 候选统一定价限制、无市场退出”的场景级证据不完整。
- TDD：将 uniform 候选数改为 11、将 dynamic 总需求改为 1099 的两个测试先按预期失败，均为 `Failed: DID NOT RAISE ValueError`。随后增加 uniform=12、dynamic=788 的规模检查，以及两游戏总需求相等并与 baseline 1100 一致的 `1e-8` 容差门禁；非有限总需求也会被拒绝。
- 验证：定向结果 `3 passed`；证据门禁与敏感性 runner 组合结果 `26 passed in 0.45s`；Ruff 为 `All checks passed!`。完成的两个正式场景再次通过增强门禁。
- 状态：scenario_mass_conservation_gated；game_sizes_gated；completed_artifacts_revalidated

### 2026-07-16 05:29 - 已完成敏感性证据映射同步

- `capacity_high`：65,919 个动态支付对，10-by-10 活跃支持；峰值、最大利用率、最低 QoS 和市场侧利润变化为 `-12.9523%/-8.4640%/+0.029145/+27.6953%`。
- `price_sensitivity_low`：71,122 个动态支付对，21-by-21 活跃支持；对应变化为 `-12.5737%/-18.2534%/+0.067348/-39.7940%`。
- 文档：`docs/reviews/smpt_submission_evidence_map_2026-07-14.md` 已同步两场景和增强门禁。由于仅完成 2/8，本轮仍不形成跨扰动方向、范围或利润符号结论。
- 状态：two_completed_scenarios_documented；cross_scenario_claim_withheld

### 2026-07-16 05:33 - Highlights 策略边界措辞

- 修改：将 `continuous intermediary response` 改为 `bounded three-parameter intermediary response`，避免 Highlights 脱离正文后被理解为逐时段任意连续响应。
- 验证：SMPT 摘要、关键词和 Highlights 门禁 `1 passed`；五条字符数为 `73/83/75/66/68`，均不超过 85。
- 状态：highlight_scope_precise；journal_length_limit_passed

### 2026-07-16 05:40 - 线性价格规则自包含说明

- 发现：TeX 已给出三组线性时段价格式，但只说负载形状“centered and scaled”，没有写出精确变换；参数表也遗漏服务商 posted wholesale/direct price 的 clip 边界。
- 修改：正文新增 $\bar\nu=T^{-1}\sum_t\nu_t$ 与 $\ell_t=(\nu_t-\bar\nu)/\max_s|\nu_s-\bar\nu|$，定义 `clip(x,a,b)=min(max(x,a),b)`，并在参数表加入批发价 `[0.25,0.90]` 与直售/零售价 `[0.45,2.10]`。这些值与冻结实现一致。
- 边界：只增加 PDF 可见的计算定义，不改变价格候选、边界、收益或实验结果。
- 验证：不依赖正式敏感性输出的稿件门禁为 `21 passed, 3 deselected`。XeLaTeX 编译退出码 0，21 页 PDF SHA-256 为 `d6430595e00bc74e277ab8e3d3bb67cdea4bf69626fe1a2dc3b4e6f7581b3d17`；日志无 error、未定义引用/文献、overfull 或 underfull box，相关文件 `git diff --check` 无输出。
- 状态：price_rule_formula_self_contained；posted_bounds_visible_in_pdf；latex_verified

### 2026-07-16 05:45 - 联合固定点更新式进入主稿

- 修改：在联合 QoS--routing 固定点部分新增目标映射 $\mathcal F(q,r)=(Q(u(q,r)),R(w,q))$ 和阻尼迭代 $(q^{n+1},r^{n+1})=(1-\lambda)(q^n,r^n)+\lambda\mathcal F(q^n,r^n)$，并保留原有初值、$\lambda=0.35$、200 次上限和 `1e-9` 停止残差。
- 目的：使读者只看 PDF 即可知道固定点如何计算，而不需要从代码推断“damping”的具体含义。
- 验证：不依赖正式敏感性输出的稿件门禁为 `22 passed, 3 deselected`。编译退出码 0，21 页 PDF SHA-256 为 `f9a59325815d00f79f9b895db8142fc04de7c971aa31d19bbe0a38ca8cfeea52`；日志无 error、未定义引用/文献、overfull 或 underfull box，相关文件 `git diff --check` 无输出。
- 状态：joint_iteration_explicit；pdf_method_self_contained；latex_verified

### 2026-07-16 05:06 - 方法公式与参数表 PDF 视觉核验

- 输入：最近一次成功编译的 21 页英文主稿 PDF，重点检查第 5--7 页与第 10--11 页。
- 检查内容：联合 QoS--routing 固定点迭代、负载形状归一化、三类线性价格规则、`clip` 定义、利润式、候选集构造表、主参数表与期望指标定义。
- 结果：公式、编号、正文和表格均未出现重叠、裁切、遮挡或越界；新增固定点更新式与价格边界在 PDF 中完整可见。候选集构造表信息密度较高，但在 A4 单栏页面中仍可辨读。
- 决策：不为视觉原因改变冻结数值定义或表格内容；正式敏感性结果生成后再对新增表格和 Figure 6 做同样的逐页检查。
- 状态：method_pages_visually_verified；sensitivity_visual_audit_pending

### 2026-07-16 05:12 - OD 概率定义域与稿件测试修正

- 审稿发现：正文说明迁移窗口在日边界截断，但原 Eq. (3) 没有在公式内明确窗口外概率为零。数值实现已正确截断，问题仅影响 PDF 的理论自包含性。
- TDD：先在 `test_temporal_boundary_condition_is_explicit` 中要求分母含 $s\in\mathcal T$ 且分段式含 `otherwise`。修改 TeX 前定向测试按预期失败，退出码 1；加入分段概率定义后，相关三项测试为 `3 passed`。
- 测试修正：发现两个 verification/validation 测试函数同名，后定义覆盖前定义。第二个测试已重命名，完整静态稿件门禁由此前实际执行的 22 项增至 `23 passed, 3 deselected`；三项 deselection 仍只对应尚未生成的正式敏感性表、Figure 6 和占位文字替换。
- 技能记录：`nature-polishing` 的 manifest 引用四个未随本机技能包提供的 `_shared/core` 文件，首次批量读取因此失败。随后只读取包内实际存在的 core、research、全章节、English 和 generic journal fragments，并同时执行 `nature-reviewer` 与 `humanizer` 的非编造、证据边界和语言模式检查。
- 编辑记录：第一次公式补丁因匹配片段从原长段落中部开始而未应用，文件没有部分写入；缩小上下文后成功。
- 编译：
  ```bash
  latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：退出码 0，21 页 PDF SHA-256 为 `ad994283144be1cd9811012c5fdd9d2926258b01e106a0ee29c64445b9a868b2`；日志无 LaTeX error、未定义引用/文献、overfull 或 underfull box。第 5 页视觉复核确认分段式、公式编号及相邻正文无重叠或裁切；相关文件 `git diff --check` 无输出。
- 状态：od_probability_domain_explicit；shadowed_test_restored；latex_verified

### 2026-07-16 05:19 - 平坦负载边界与敏感性求解范围措辞

- 代码核对：`build_burstgpt_load_anchor._normalized_shape` 在负载形状的最大绝对离差为零时返回全零信号；原正文只给出非零分母公式。主稿现将 $d_\nu$ 和 $\ell_t$ 写成分段定义，与实现一致。
- 证据措辞：将敏感性场景的“complete finite-candidate re-solves”改为“重求有限博弈并检查全部声明的单边服务商偏差”，并明确无需构造全部 $788^2$ 支付单元。该说法对应 double-oracle 的全候选 regret 证书，不再暗示完整支付矩阵已经计算。
- 语言：将中间商支付计算的 47 词长句拆为两句，保留初始 QoS、初始路由、阻尼和容差，不改变计算定义。`detex` 长句扫描未发现其他超过 35 词的普通叙述句；输出中的其余命中均由公式边界合并造成。
- TDD：新增两个边界断言后，修改前定向测试为 `2 failed`；完成 TeX 改写后为 `2 passed`。不依赖正式敏感性输出的完整门禁为 `23 passed, 3 deselected`。
- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 退出码 0；21 页 PDF SHA-256 为 `6137466663e110e0f5a5ef161c7927800bd8fcc02e2e2a346e8a204e96a4db07`。日志无 error、未定义引用/文献、overfull 或 underfull box，第 6 页视觉检查无重叠或裁切，相关文件 `git diff --check` 无输出。
- 状态：flat_load_signal_defined；finite_game_scope_precise；language_scan_clean

### 2026-07-16 05:24 - 21 页全稿视觉与字体审计

- 操作：以 55 dpi 渲染全部 21 页并生成 4-by-6 接触表，检查标题页、五个编号章节、公式页、表格、五张现有图和参考文献分页。
- 结果：未发现孤立章节标题、异常大面积空白、浮动体断裂、图表越界、正文遮挡或不协调分页。第 21 页仅含参考文献末尾，页面下半部留白属于文末自然结束，不作人为填充。
- 字体：`pdffonts` 显示正文、数学字体和图内 Times New Roman 字体均为 `emb=yes`、`sub=yes`；图表文字与正文均可嵌入输出。数学扩展字体 `CMEX10` 的 Unicode 映射为 `uni=no`，但其字体已嵌入，公式显示正常。
- 临时输出：接触表位于 `/tmp/smpt_full_contact/contact.png`，不进入仓库或投稿包。
- 状态：full_pdf_layout_checked；fonts_embedded；formal_figure6_pending

### 2026-07-16 05:23 - 2026 年相关工作元数据复核

- 范围：复核正文实际引用的两篇 2026 年正式论文和两篇 2026 年预印本，未改动引用顺序或正文技术判断。
- 正式论文：Elsevier ScienceDirect 页面确认 Wang et al. 载于 *Sustainable Energy, Grids and Networks* 46, 102245，DOI `10.1016/j.segan.2026.102245`；AAAI 官方页面确认 Guo et al. 载于 AAAI 40(20), 17005--17013，DOI `10.1609/aaai.v40i20.38748`。
- 预印本：arXiv 官方页面确认 Yan et al. 为 `arXiv:2604.16802`，Cunningham 为 `arXiv:2603.00356`。题名、作者、年份和正文对其研究范围的概述均与 `verified_refs.bib` 一致。
- 决策：四个条目无需修改；正文继续将后两项表述为模型/预印本工作，不暗示同行评审状态。
- 状态：recent_references_verified；bibliography_unchanged

### 2026-07-16 05:44 - 源码级有限博弈措辞门禁

- 目标：避免正文之外的 TeX 修订注释仍把有限候选集证据写成 `fully re-solved`，使源码审查与正文证据边界一致。
- TDD：在 `test_sensitivity_equilibria_remain_conditional_on_common_candidate_set` 中增加全稿禁用断言；修改前定向测试按预期失败，唯一命中位于 `\end{document}` 后的修订注释。
- 修改：将该注释改为 `verified finite-game evidence`。正在运行且属于场景 provenance 的 `run_submission_spatiotemporal_sensitivity.py` 及 20 个冻结数值源均未修改；历史 runner 和历史工件也保持不变。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp /root/.local/bin/uv run pytest -q tests/test_final_manuscript_20260714.py::test_sensitivity_equilibria_remain_conditional_on_common_candidate_set
  ```
- 修改前结果：`1 failed`，退出码 `1`；失败原因与预期一致。修改后验证见后续记录。
- 修改后验证：定向测试 `1 passed`；不依赖正式敏感性输出的主稿门禁为 `24 passed, 3 deselected`。三项 deselection 仍仅对应最终敏感性表、Figure 6 和占位段落。
- 一致性：`git diff --check` 对 TeX、测试和 README 无输出。
- 状态：finite_game_wording_gated；static_manuscript_checks_passed

### 2026-07-16 05:48 - 支付 oracle 与部分矩阵表述修正

- 审稿发现：正式动态博弈只计算均衡支持及全候选偏差扫描所需的 46,381 个支付对，占 $788^2$ 完整矩阵的 7.47%。正文多处 `stored finite payoff matrix` 会错误暗示完整支付矩阵已经物化。
- TDD：先增加禁用三种 `stored ... payoff matrix` 表述并要求 `numerical payoff oracle`；定向测试按预期失败。修改正文后，另一个历史测试因仍强制要求旧表述而失败，说明测试语义也需同步更新。
- 修改：摘要改为 `declared finite game`；相关研究、求解方法、数值检查和局限性统一说明通过数值支付 oracle、缓存支付评价和全部声明候选偏差扫描验证所报混合剖面。完整矩阵的 7.47% 计算比例保持原样。
- 编译：XeLaTeX 成功生成 22 页 A4 PDF；摘要 222 词；当前 PDF SHA-256 为 `ae509ac5aa616358143513a18c975c1f13ecfb6c2dae67efff508eb77ae67604`。
- 验证：不依赖正式敏感性输出的主稿门禁为 `24 passed, 3 deselected`；LaTeX 日志无 error、未定义引用/文献、overfull 或 underfull，`git diff --check` 无输出。PDF 仍为 22 页，SHA-256 未变。
- 状态：payoff_oracle_wording_verified；static_manuscript_checks_passed；latex_verified

### 2026-07-16 05:53 - 数值审计随机性与搜索设置进入 PDF

- 审稿发现：vLLM 测量和 off-grid 审计的 seed 已在主稿中，但固定点多初值、混合均衡分支多初值和中间商差分进化的 seed/搜索设置只存在代码与 JSON，读者无法仅凭 PDF 精确复现这些诊断。
- TDD：新增 `test_numerical_audit_randomness_and_search_settings_are_visible`，要求两个 active-profile 审计都显示 `20260713`，并要求 `20260715`、35 代、差分进化 `popsize` 倍数 8 及 $10^{-8}$ 绝对/相对容差。正文修改前及首次漏写差分进化 seed 时，定向测试均按预期为 `1 failed`。
- 修改：在 Numerical equilibrium checks 中补入上述设置；说明固定点审计对每个 profile 使用 `20260713 + profile index`，混合分支的 64 个 Dirichlet 初值使用 seed `20260715`。数值、算法实现和冻结工件均未改变。
- 验证：定向测试 `1 passed`；不依赖正式敏感性输出的主稿门禁增至 `25 passed, 3 deselected`。XeLaTeX 成功生成 22 页 A4 PDF，SHA-256 为 `aafd1d04c51bb54676aaf2a347059655f5101b1e3f946afc5daac7abc42e273a`；日志无 error、未定义引用/文献、overfull 或 underfull，相关文件 `git diff --check` 无输出。
- 视觉复核：以 120 dpi 检查新增文字所在的第 14--15 页。差分进化设置、固定点 seed 和 Dirichlet seed 均完整可读，分页自然；Figure 4、图注和 Section 4.4 标题没有遮挡、裁切或孤立。
- 状态：audit_settings_visible_in_pdf；static_manuscript_checks_passed；latex_verified

### 2026-07-16 05:58 - 证据映射的部分支付矩阵语义同步

- 发现：`smpt_submission_evidence_map_2026-07-14.md` 的动态均衡、regret 和方法同步项仍写成 `stored ... payoff matrix`，与主稿已公开的 46,381/622,944 个必要支付对矛盾。
- TDD：新增文档一致性测试，禁用 `stored finite/numerical payoff matrix` 与旧的 `generated by the numerical intermediary response` 句式，并要求 `cached numerical payoff evaluations`。修改前定向测试按预期为 `1 failed`。
- 修改：证据映射现将均衡对象写为声明的有限服务商博弈，将数值对象写为缓存支付评价与全部声明候选偏差扫描；不改变基线工件、regret 或支持集。
- 验证：定向测试 `1 passed`；不依赖正式敏感性输出的稿件与文档门禁增至 `26 passed, 3 deselected`，相关文件 `git diff --check` 无输出。
- 状态：evidence_map_scope_verified；static_manuscript_checks_passed

### 2026-07-16 06:02 - Humanizer 语言模式复核

- 范围：标题、摘要、Highlights 和约 8,903 个英文正文词；按 `humanizer` 的宣传性语言、模糊归因、机械连接词、规则三段式、负向排比和 AI 高频词清单扫描。
- 结果：`moreover/furthermore/additionally/in addition/robust/novel/crucial/notably/importantly` 均为 0；未命中 `it is worth noting`、`plays a crucial role`、`delve`、`landscape`、`groundbreaking`、`novel framework`、`robust improvement`、`this study demonstrates` 等库存句式。`mechanism`、`diagnostic` 和 `boundary` 分别出现 7/5/6 次，均用于技术定义或限制，不作机械替换。
- 决策：不为追求低词频改动必要的博弈、仿真和审计术语；当前语言保持直接、常用句法和审慎语气。
- 状态：humanizer_scan_clean；no_language_edit_required

### 2026-07-16 06:06 - 总证据报告加入数值质量门禁

- 发现：`submission_evidence_gate_report.json` 原先对 fixed-point、intermediary 和 mechanism decomposition 只调用来源哈希验证；数值质量由后续宏/绘图步骤间接拦截，单独读取报告时证据范围不完整。
- TDD：先加入三个独立验证器的正常与失败用例，覆盖基准 SHA、active-profile 概率质量、全部初值收敛、残差、QoS/路由跨度、中间商相对收益改进、8 个 policy--mechanism 行及其概率质量。实现前为 `12 failed, 19 passed`。
- 实现：`submission_evidence_gates.py` 新增 `validate_fixed_point_audit`、`validate_intermediary_audit` 和 `validate_mechanism_audit`；总报告直接调用数值与 provenance 组合门禁。阈值与宏生成器一致：残差 `1e-8`、固定点跨度 `1e-7`、中间商相对改进 `0.1%`、active-profile 覆盖至少 `1-1e-9`。
- 验证：`tests/test_submission_evidence_gates.py` 为 `31 passed in 0.32s`；Ruff 为 `All checks passed!`，相关文件 `git diff --check` 无输出。该改动只读取工件，不修改求解器、场景参数或冻结来源。
- 状态：dependent_audit_quality_gated；post_pipeline_ready

### 2026-07-16 06:08 - capacity_low 正式场景独立核验

- 完成信号：容量分支日志记录 `validated queued scenario: capacity_low`，随后自动启动 `migration_cost_high`；队列场景由分支 supervisor 统一写最终 queue sentinel，因此没有单独 `.exit` 文件。
- 工件：`sensitivity_capacity_low_submission.json`，SHA-256 `b7cbb9a7ecc63e208076b2bb8badc4e86cf8f9c4ada4e5c98e2cdbed4a2266b7`。
- 门禁：场景参数为容量共同缩放 `0.85`；共同策略契约、12/788 候选数、20 个来源哈希、1100 需求守恒、全候选扫描均通过。动态 regret `1.1369e-13`，最大联合残差 `9.9726e-10`，计算 75,564 个支付对，支持为 15-by-15。
- 结果：相对统一定价限制，aggregate peak `-12.6859%`、maximum provider utilization `-21.0308%`、minimum QoS `+0.142075`、aggregate market-side profit `+4.2850%`。
- 决策：正式敏感性进度为 3/8。利润在已完成场景中已有正负两种符号，但五个场景未完成前仍不生成范围、方向稳定性或符号计数结论。
- 状态：capacity_low_verified；sensitivity_progress_3_of_8；cross_scenario_claim_withheld

### 2026-07-16 06:10 - 新门禁对真实依赖审计的预期红灯

- 操作：用当前 baseline SHA-256 分别调用 `validate_fixed_point_audit`、`validate_intermediary_audit` 和 `validate_mechanism_audit` 读取现有三个 submission JSON。
- 结果：三项均在进入数值质量判断前因 runner 来源 SHA-256 不匹配而被拒绝：`run_submission_fixed_point_audit.py`、`run_submission_intermediary_audit.py` 和 `run_submission_mechanism_decomposition.py` 的当前源码均晚于现有工件。
- 解释：这是已知且需要保留的 provenance 红灯，说明历史数值不能被新总报告直接复用。PID 100187 的 finalizer 与 PID 103917 的 post-sensitivity waiter 均存活；后者将在八场景完成后重建三项，再执行新数值门禁、宏、图和测试。
- 资源：当时约 11 GiB 可用内存、466 GiB 可用磁盘，无 OOM 或磁盘风险。
- 状态：stale_dependent_artifacts_rejected；post_rebuild_required；waiters_alive

### 2026-07-16 06:13 - 混合分布 provenance 纳入总门禁

- 发现：`mixed_outcome_distribution_submission.json` 的来源清单包含已重构的 `run_submission_intermediary_audit.py`，但原 post waiter 不重建该工件；Table 5 的 676 个 active-profile 分位数因此仍是旧 provenance。
- TDD：新增 distribution 正常与失败用例，覆盖基准 SHA、`[0.05,0.50,0.95]` 分位点、1/676 个 uniform/dynamic 活跃剖面、概率质量、全部固定点收敛、`1e-8` 残差和期望指标重构误差。实现前为 `6 failed, 30 passed`。
- 实现：总门禁新增 `validate_distribution_audit` 和 `DISTRIBUTION_PATH`；实现后证据门禁与分布单测为 `40 passed in 0.44s`，Ruff clean。对当前工件实测时，门禁按预期拒绝旧 runner SHA。
- 收尾安排：新增缓存区等待脚本 `complete_submission_after_post.sh`。它不接触求解器；只在原 post attempt 和 finalizer 结束后重建 mixed distribution，再重跑 sensitivity claims、总证据报告、结果宏、全部图及九组相关测试。
- 验证：`bash -n` 通过。首次以普通 `nohup` 启动的 PID `142604` 被命令会话清理，未写 exit sentinel；随后用独立 session 重启。当前 PID `142689` 的 PPID 为长期 shell `700`，PGID/SID 均为 `142689`，日志已写入 `waiting for post-sensitivity audit attempt`。最终状态将写入 `submission_completion.exit`。
- 状态：distribution_quality_gated；supplemental_completion_waiter_alive

### 2026-07-16 06:17 - ARTIFACT_MANIFEST 切换到 7 月终稿证据线

- 发现：原 `ARTIFACT_MANIFEST.md` 仍把 6 月主稿、旧 peak-shaving 模块和 `20260618/20260619*` 目录列为正式投稿证据，与当前 788 候选有限博弈不一致。
- 修改：manifest 现记录 7 月五章英文主稿、Highlights、baseline SHA、数值源码冻结提交、BurstGPT/vLLM 输入锚点、spatiotemporal 模块、正式 evidence JSON、敏感性生成状态、测试门禁和 author-only 图像政策事项。
- 边界：明确 `20260712_expanded_response` 中的早期扩展、interrupted logs 和 diagnostics 只是研究历史；只有列出的 submission 工件可进入 claim。三项已知 stale provenance 工件标为 scheduled for rebuild，敏感性状态标为 3/8，未写成已冻结 archive。
- 验证：旧 6 月主稿、旧 artifact 目录和旧测试入口在 manifest 中均无命中；baseline 路径、冻结 commit、3/8 状态和四个待重建工件均可检索，`git diff --check` 无输出。
- 状态：artifact_manifest_current；archive_not_frozen

### 2026-07-16 06:22 - 复现与数据可用性文档切换到当前有限博弈

- 发现：`REPRODUCIBILITY.md` 和 `DATA_AVAILABILITY.md` 仍给出 6 月实验、旧 TeX 和旧图目录；`requirements.txt` 也漏掉正式均衡/敏感性 runner 导入的 Nashpy。
- 依赖修改：在 `requirements.txt` 增加 `nashpy>=0.0.43`，其余依赖不变。项目没有 `pyproject.toml` 或 `uv.lock`，因此未运行 `uv lock/uv sync`；改用实际的 `uv run --no-project --with-requirements requirements.txt` 验证。
- 文档修改：复现指南现包含输入锚点、788 候选 baseline、八场景重求、四类依赖审计、总证据门禁、图表和当前 TeX 编译命令。明确 baseline runner 依赖已审计 continuation seed，是声明有限博弈的复现，不是从空策略空间独立发现候选集；同时说明 CPU 并行和无 GPU 求解路径。
- 数据边界：当前工作树未冻结、未完整推送且无 DOI；raw BurstGPT 不再分发，vLLM 只锚定单 GPU QoS 形状，经济参数仍为 synthetic design。
- 验证：requirements 环境解析为 Python 3.12.13、NumPy 2.4.4、SciPy 1.17.1、Nashpy 0.0.43、Matplotlib 3.10.8、Pytest 9.1.0；证据门禁与分布测试 `40 passed`。两个文档无 6 月路径/旧 TeX/旧 runner 命中，相关文件 `git diff --check` 无输出。
- 状态：reproducibility_docs_current；nashpy_dependency_declared；archive_pending

### 2026-07-16 06:12 - 混合策略分位数改为离散逆 CDF

- 审计发现：`mixed_outcome_distribution_submission.json` 描述的是有限个活跃策略对上的离散概率分布，旧 `weighted_quantile` 却在相邻结果值之间线性插值，会生成没有对应策略剖面的中间分位值。均值、均衡、regret 和主结果不受影响，但 Table 5 的 5/50/95 分位数需按离散分布重建。
- TDD：将权重为 `(0.1,0.8,0.1)`、取值为 `(1,2,10)` 的期望分位数固定为 `(1,2,10)`，并增加累计概率边界用例。修改前定向测试按预期为 `1 failed, 2 passed, 2 deselected`，旧函数返回 `(1,1.5,6)`。
- 实现：`weighted_quantile` 现返回最小满足累计概率不低于目标概率的观测值，即离散经验分布的广义逆；同时拒绝非有限取值、非有限权重和区间外分位点。
- 验证：完整分布单测 `5 passed`。首次 Ruff 命令因 `requirements.txt` 不含开发工具而以 exit code 2 失败；随后使用 `uv run --no-project --with-requirements requirements.txt --with ruff ruff check ...`，结果为 `All checks passed!`。
- 后续：PID `142689` 的补充收尾流水线会在敏感性结束后按修正定义重建分布、证据报告、宏、图和相关测试；当前旧分布工件不进入终稿。
- 论文同步：结果段现明确分位数是累计概率达到目标水平时的最小已观测 profile 值。新增静态测试修改前按预期失败，正文补充定义后为 `1 passed, 29 deselected`。
- 状态：discrete_quantile_definition_verified；distribution_rebuild_pending

### 2026-07-16 06:15 - 788 候选集清单进入总证据门禁

- 审计发现：`candidate_manifest_submission.json` 能从前一轮正概率支持逐元素重建当前 788 条候选规则，但旧清单只记录 baseline/continuation seed 的输入哈希，没有生成源码哈希，也未由 `submission_evidence_gate_report.json` 检查。
- TDD：增加生成器来源记录断言、正常门禁，以及 baseline 哈希、逐元素匹配、候选数、八组件增量计数和 continuation seed 文件变化的失败用例。实现前定向结果为 `7 failed, 2 passed, 35 deselected`。
- 实现：清单现记录生成时间、复现命令、生成器与候选网格源码 SHA-256；总门禁新增 `validate_candidate_manifest`，核对 baseline、continuation seed、来源、逐元素匹配、788 总数及组件累计计数。
- 重建：运行 `uv run --no-project --with-requirements requirements.txt python -m experiments.build_submission_candidate_manifest`，得到清单 SHA-256 `d52024b85559f54b87842207e887f3595078d8eee1df89a35794b016393a2bb6`。独立门禁返回 `passed=true`、`source_count=2`、`candidate_count=788`。
- 验证：候选清单与证据门禁定向测试 `9 passed, 35 deselected`；Ruff `All checks passed!`；相关文件 `git diff --check` 无输出。该步骤只读取冻结 baseline 与 continuation seed，不改变任何支付、策略或场景计算。
- 状态：candidate_manifest_provenance_verified；candidate_manifest_gate_passed

### 2026-07-16 06:16 - 分位数与候选清单组合回归

- 测试：运行候选清单、总证据门禁、混合分布和主稿静态测试；除等待正式敏感性表、Figure 6 和占位段落替换的三项外，结果为 `76 passed, 3 deselected in 0.55s`。
- 编译：`latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 成功生成 22 页 A4 PDF，SHA-256 `10a9f36338300e5374372012ac7d0767d0b843b35625f64ed177ffa37e10e99e`。
- 日志更正：首次合并日志扫描中的 `rg` 反斜线转义有误，出现 `regex parse error`，因此未将该次扫描视为验证。随后以简化模式重新扫描 `LaTeX Error`、未定义命令/引用/文献及全部 overfull/underfull，退出码 0 且无命中。
- PDF 抽检：第 13 页的离散分位数定义、Table 4 和 Table 5 均完整可读，无重叠、裁切或异常分页。Table 5 的数值仍来自待重建的旧分位数工件，最终流水线完成后必须同步替换，不将当前表作为终稿值。
- 状态：combined_regression_passed；latex_verified；mixed_quantile_values_pending_rebuild

### 2026-07-16 06:19 - 理论、实现与混合聚合链复核

- 核对范围：OD 时间流、两阶段 logit、价格/QoS 路由、服务商负载、阈值 QoS、联合固定点、有界线性价格、三方利润、批发转移抵消、中间商三参数响应、双矩阵 Nash 条件、全候选 regret、混合 profile 权重与逐时段期望。
- 结果：上述公式符号、方向、边界、阻尼、容差和聚合权重均与当前实现一致。活跃策略对使用 $x_i y_j$，profile-level 极值与逐时段曲线分开计算；未发现新的核心公式或主结果错误。
- 文档问题：理论一致性审计仍有“存储支付矩阵”的旧措辞，并把八个敏感性场景写得像已经全部完成。新增静态门禁修改前按预期为 `1 failed, 30 deselected`。
- 修正：审计文档现使用“缓存的必要支付评价”，说明只计算支持与偏差扫描所需单元；补入离散逆 CDF、候选清单来源门禁和当前 `3/8` 进度。修正后定向测试 `1 passed, 30 deselected`，`git diff --check` 无输出。
- 边界：本轮未修改冻结数值源码、baseline 或正在运行的场景；中间商全局最优、连续服务商均衡和市场层外部验证仍不成立。
- 状态：theory_code_aggregation_consistent；audit_wording_current；sensitivity_progress_3_of_8

### 2026-07-16 06:21 - 相关研究关键比较句在线核验

- 范围：电力定价基础中的 Faruqui--Sergici、Allcott、El-Afifi 和 2026 三层 VPP Stackelberg 工作，以及推理市场中的 PriLLM、GPU pricing/scaling 和 token-pool 工作。
- 一手来源：AAAI 官方页面确认 PriLLM 的题名、作者、卷期、页码、DOI 和 2026-03-14 发表日期；arXiv 原页确认 `2604.16802` 与 `2603.00356` 的作者、提交日期和摘要内容。ScienceDirect 出版页面支持按用户消费/负载贡献调整 on-peak/shoulder 价格的概括。
- 电力结果：出版机构摘要确认 Allcott 的受试家庭峰时节电且平均谷时用电未增加；Faruqui--Sergici 的 `3--6%` TOU 与 `13--20%` CPP 范围由论文引用链和公开全文索引交叉确认；2026 VPP 工作的三层 Stackelberg 与复合映射 fixed-point 表述相符。
- 决策：相关研究现有比较句与引用对象一致，不为增加文献数量修改主稿，也不把预印本写成已同行评议期刊论文。`verified_refs.bib` 中 AAAI 条目继续使用正式 DOI，两个 2026 GPU/token 条目保持 arXiv 类型。
- 状态：key_literature_claims_verified；no_citation_edit_required

### 2026-07-16 06:23 - 离散混合分布正式重建并进入 Table 5

- 运行：为避免影响 28 路敏感性求解，使用 `nice -n 15 taskset -c 31 env TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with-requirements requirements.txt python -m experiments.build_submission_mixed_distribution`，只在一个 CPU 核上重算 1 个 uniform 与 676 个 dynamic 活跃剖面的固定点。
- 工件：`mixed_outcome_distribution_submission.json`，SHA-256 `01928471487d034bc386d3f6577b4e4e561932a75883dda936d362af419f543f`。门禁返回 `passed=true`、`source_count=6`；概率质量为 1，全部剖面收敛，最大残差 `9.9997e-10`，最大期望重构误差 `6.8212e-13`。
- 数值修正：离散逆 CDF 下，Table 5 更新为 peak `(194.639,195.162,202.729)`、maximum utilization `(0.933,1.289,1.390)`、minimum QoS `(0.916,0.953,1.000)`、market-side profit `(1849.373,1934.681,1979.354)`。均值、主表、regret 和结论均未改变。
- TDD：新增从 provenance-linked JSON 构造四行期望文本的主稿测试；更新前按预期为 `1 failed, 31 deselected`，更新后组合回归为 `75 passed, 3 deselected`。Ruff 为 `All checks passed!`。
- 编译与视觉：XeLaTeX 生成 22 页 A4 PDF，SHA-256 `5c94fd2f99d728e6a2fe370d93137dcf548475f578a99aad7524105d6b9bf78b`；日志无 error、未定义引用/文献或 overfull/underfull。第 13 页的新 Table 5 无重叠、裁切或异常分页。
- 状态：mixed_distribution_gate_passed；table5_artifact_bound；latex_verified

### 2026-07-16 06:28 - QoS 误差条统计定义复核

- 来源定义：`pricing_sim/vllm_study.py` 将聚合 CSV 中的 `ttft_sla_0_5_rate_ci95` 定义为 $1.96s/\sqrt{n}$；当前测量每个并发点有 $n=5$ 次重复。最终绘图使用比例 $t_{0.975,4}/1.96=2.776445/1.96$ 将该已存半宽换算为小样本 Student-$t$ 95% 区间。
- 数值核对：唯一具有非零方差的 QoS 点为 Qwen2.5-0.5B、并发 384；样本标准差 `0.0079336313`，聚合半宽 `0.0069541344`，由此得到标准误 `0.0035480278`。最终半宽 `0.0098509043` 同时等于 `0.0069541344 * (2.776445/1.96)` 和 `2.776445 * 0.0079336313 / sqrt(5)`。
- 结论：不存在重复乘以 Student-$t$ 临界值的问题。主稿 Figure 2 图注所写的“five repeats, repeat-level Student-$t$ 95% confidence intervals”与最终绘图实现一致；旧 measurement-anchor 单图仍显示原始正态近似半宽，但不作为终稿 Figure 2。
- 运行状态：敏感性分支仍为 3/8；`price_sensitivity_high` 的 12 个 worker 与 `migration_cost_high` 的 16 个 worker 均持续运行并占用 CPU，finalizer、post waiter 和 supplemental waiter 均存活。
- 状态：qos_error_bar_definition_verified；no_numerical_change；sensitivity_workers_healthy

### 2026-07-16 06:31 - 输入不确定性定义进入 PDF

- 审稿缺口：BurstGPT 绘图使用 `numpy.std(..., ddof=0)`，旧正文未说明分母；vLLM 图虽写明五次重复的 Student-$t$ 区间，但未说明它不是请求级二项不确定性。
- TDD：新增 `test_input_uncertainty_statistics_are_defined_in_the_manuscript`。修改前定向测试按预期为 `1 failed`；正文补充后，与 BurstGPT、QoS calibration 和误差条换算测试合并为 `6 passed in 1.04s`。
- 修改：方法段现说明 Figure 2(a) 是 59 个保留日的总体标准差、分母为 59；Figure 2(b) 的区间只概括五次重复之间的变化，不代表单个请求层面的二项误差。
- 编译：`nice -n 15 taskset -c 31 latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 退出码 0。PDF 为 22 页 A4，SHA-256 `36447465bf1bbd16b1492b9126bb481c5a7c95a41cc25da8a4ca96afbd38b244`；日志无 LaTeX error、未定义引用/文献、overfull 或 underfull box。
- PDF 文本核对：两项统计边界均可从编译 PDF 检索；相关文件 `git diff --check` 无输出。
- 状态：input_uncertainty_scope_visible；targeted_tests_passed；latex_verified

### 2026-07-16 06:34 - 候选价格表唯一性与参数表同步门禁

- 候选展开审计：从正式 baseline 的 788 个系数向量出发，使用最终 BurstGPT 负载信号、批发价界和直售价界展开 16 维价格表。结果为 788 个唯一向量、788 个唯一的截断后价格表组合、0 个重复组；因此正文“each producing a distinct bounded price profile”与实际策略对象一致。
- 新增门禁：`test_parameter_table_matches_the_executed_final_case` 直接读取 `final_case()`、`routing_from_beta` 默认参数和 `IntermediarySearchSpec`，并与 Table 3 的 16 行参数逐项比较。覆盖时段、总需求、人口比例、可迁移比例、价格系数、迁移成本、移动窗口、容量、QoS 参数、两类 QoS 权重、渠道偏好、固定份额、成本和全部价格/搜索边界。
- 测试过程：首次运行因静态测试文件没有项目导入路径而失败；加入仓库根目录后，第二次暴露 tuple/list 测试类型假设；修正测试表示后结果为 `1 passed in 0.38s`。两次失败均来自新测试装配，不是参数或论文数值差异。
- 数值边界：未修改 `run_final_spatiotemporal_equilibrium.py`、20 个冻结来源、baseline 或正在运行的敏感性场景。
- 状态：realized_candidate_schedules_unique；parameter_table_code_bound；frozen_sources_unchanged

### 2026-07-16 06:41 - 价格形状分解纳入总证据门禁

- 发现：Table 7 与结果讨论依赖 `price_shape_decomposition_submission.json`，但 `submission_evidence_gate_report.json` 原先没有读取该工件。这使价格形状主张缺少与其他结果相同的统一拒绝条件。
- 工件预审：baseline SHA-256 一致，生成器与四个模型依赖的 5 个源码哈希全部匹配；uniform/dynamic 分别覆盖 1/676 个剖面，概率质量为 1，全部固定点收敛，动态最大残差 `9.9884e-10`，四个分解行的恒等误差均为 0。
- TDD：新增正常路径、8 种破坏性路径和总报告接线测试。实现前为 `10 failed`；新增 `validate_price_shape_audit` 后为 `10 passed, 40 deselected`，完整证据门禁与分解回归为 `54 passed in 0.44s`。
- 门禁内容：检查 baseline/source SHA、profile count、概率质量、固定点收敛、残差、uniform flattening 误差、四项指标集合，以及 overall/shape/remainder 的逐行算术重构和恒等误差。
- 真实工件：独立调用返回 `passed=true`、`source_count=5`、`row_count=4`。Ruff 为 `All checks passed!`，相关文件 `git diff --check` 无输出。
- 流水线影响：未修改任何等待脚本。post/supplemental 管线原本就调用总证据报告，因此将在最终收尾时自动执行新增门禁。
- 状态：price_shape_gate_passed；combined_report_extended；running_solvers_unchanged

### 2026-07-16 06:47 - 基准均衡工件加入独立完整性门禁

- 发现：总证据报告此前把正式 baseline SHA-256 作为派生工件的关联锚点，但没有直接验证 baseline 自身的场景、候选网格、均衡质量、主表算术和图表输入结构。
- TDD：增加真实工件正常路径、10 种破坏性路径和总报告接线测试。破坏项覆盖 788 候选数、baseline 场景、候选网格唯一性、全候选 regret、联合残差、1100 需求守恒、三方利润恒等式、比较值重构、8 时段 profile 维度和 1/676 个活跃剖面。实现前为 `12 failed`，实现后定向结果为 `12 passed, 50 deselected`。
- 实现：`submission_evidence_gates.py` 新增 `validate_equilibrium`，并在所有派生审计之前运行。门禁还核对 20 个冻结来源 SHA、统一/动态 12/788 候选游戏、支持概率质量、支持维度、活跃剖面残差和 peak-to-average 算术。
- 统计边界：动态混合均衡的 profile-level extrema 是 $\mathbb{E}[\max X]$ 或 $\mathbb{E}[\min X]$，而 Figure 3 使用 period-wise expected profiles；因此只对可线性重构的总需求建立曲线--指标恒等式。主稿方法段、结果段和 Figure 3 图注已明确两者区别。
- 验证：真实 baseline 返回 `passed=true`、`source_count=20`；uniform/dynamic full regret 分别为 `0` 和 `1.1369e-13`，最大联合残差分别为 `7.9772e-10` 和 `9.9997e-10`。证据门禁与价格形状组合回归为 `66 passed in 0.50s`，Ruff 为 `All checks passed!`，相关文件 `git diff --check` 无输出。
- 运行状态：长时间敏感性分支仍为 3/8，`price_sensitivity_high` 与 `migration_cost_high` 持续计算；本次只修改审计代码、测试和文档，没有改变冻结数值来源或运行中的求解。
- 状态：baseline_equilibrium_gate_passed；combined_report_starts_from_baseline；sensitivity_progress_3_of_8

### 2026-07-16 06:50 - BurstGPT 与 vLLM 输入锚点纳入总证据门禁

- 目标：使摘要和方法中的输入数据陈述与总证据报告直接关联，而不把输入锚定误写成市场输出的 external validation。
- TDD：新增真实输入正常路径、8 种破坏性路径和总报告接线测试。实现前为 `10 failed`；实现后定向结果为 `10 passed, 62 deselected`。
- BurstGPT 门禁：核对 baseline 所存处理后 CSV SHA、固定 source commit 与原始 SHA 声明、1,429,737 行、0 跳过、59 个完整日、8 个连续时段、请求/Token 份额和为 1，以及 normalized token load 的零均值和单位最大绝对偏差。
- QoS 门禁：核对 calibration JSON 的 4 个来源 SHA、10 个测量点、两个 profile 各 5 点、每点 5 次重复、数值范围、优化成功、约束阈值、正退化强度、RMSE 不高于 0.1、两项 leave-one-profile-out 误差，以及 baseline 内嵌的 threshold/strength 与拟合值一致。
- 验证：真实输入返回 `passed=true`，BurstGPT 为 8 periods/59 days，QoS 为 10 points/4 source hashes。总证据、价格形状、BurstGPT 和 QoS 组合回归为 `80 passed in 0.59s`；Ruff clean，`git diff --check` 无输出。
- 当前总报告：baseline、input anchors、candidate manifest、off-grid、branch、distribution、price-shape 和 3 个已完成敏感性场景通过；3 个待重建依赖审计和 5 个未完成场景仍按预期使 `passed=false`。没有写入新的正式报告文件。
- 运行状态：`migration_cost_high` 已推进到 8,868 个动态支付对；`price_sensitivity_high` 仍处于 33,444 后的下一批计算。约 10 GiB 可用内存、466 GiB 可用磁盘，29 个 worker 持续运行。
- 状态：input_anchor_gate_passed；market_output_external_validation_absent；sensitivity_progress_3_of_8

### 2026-07-16 06:57 - 结果段诊断数值改为工件绑定门禁

- 审计：主表、参数表和混合分位数已有 JSON/配置绑定测试，但策略支持、路由边界、double-oracle 轨迹、需求质心、固定点与中间商审计、off-grid 搜索、branch multistart、机制分解和价格形状分解仍依赖人工抄写。
- 新增：`test_final_manuscript_20260714.py` 加入四组工件驱动检查。它们从正式 baseline、off-grid、branch、fixed-point、intermediary、mechanism 和 price-shape JSON 重构正文应出现的自然语言数值及表格行。
- 测试修正：首轮暴露两处测试表达假设错误，即正文将 65 写作 `Sixty-five`，且 A/B 偏差数共用一次 `deviations`。另一次失败来自 Python `:g` 对 0.5278125 的六位截断。均修正测试生成逻辑，没有为迎合测试修改论文语言或数字。
- 覆盖：统一策略向量和中间商响应、26-by-26 正概率支持、系数均值、beta 上下界概率质量、near-deterministic routing 质量、六轮 regret、46,381 支付对、柔性需求质心、21,632 固定点初值、66-start branch audit、off-grid 候选和最优向量、DE 成功/截断数量、三类机制比较、动态路由与 QoS，以及 Table 7 四行分解恒等式。
- 验证：新增四组测试为 `4 passed`；除等待 sensitivity table/Figure 6/占位段替换的三项外，完整主稿静态回归为 `36 passed, 3 deselected in 0.40s`。Ruff clean，相关文件 `git diff --check` 无输出。
- 状态：diagnostic_prose_artifact_bound；manuscript_non_sensitivity_gates_passed；three_sensitivity_gates_pending

### 2026-07-16 07:02 - 敏感性场景补齐均衡输出完整性门禁

- 缺口：单场景门禁原先只检查共同策略契约、来源、12/788 候选数、full-candidate regret、联合残差与总需求；被破坏的利润恒等式、comparison 字段、逐时段 profile 或 active-profile 列表仍可能通过。
- TDD：将测试夹具升级为含完整指标、8 时段 profile、支持概率、active profile 和 comparison 的小型均衡对象；增加利润、比较算术、profile 长度和 active-profile 数四种破坏性用例。实现前为 `4 failed, 3 passed`，实现后为 `7 passed`。
- 实现：每个 sensitivity game 现在复用 baseline 的利润会计、peak-to-average、profile 维度/有限值、需求重构和支持概率门禁。应有 active-profile 数由正概率 row support 与 column support 的乘积计算，不假定所有场景都是 676。
- 真实回测：`capacity_high`、`capacity_low`、`price_sensitivity_low` 均通过加强门禁；其 uniform/dynamic active-profile 数分别为 `1/100`、`1/225` 和 `1/441`。
- 验证：证据门禁与价格形状组合回归为 `80 passed in 0.60s`，Ruff clean，相关文件 `git diff --check` 无输出。运行中的 supervisor 会在后续场景结束时自动使用加强后的验证器。
- 语言审计：按 nature-polishing 的 `research + full sections + English + generic` 路径和 humanizer 规则复核。普通叙述句未发现超过 30 词者，宣传式 AI 高频词与长破折号均无命中；`utilization` 的高频来自统一指标名，因此不做同义词替换。skill 清单中的四个 `_shared/core` 文件本机缺失，已使用可用的本地 core、section、language 和 journal fragments；本轮无需修改正文。
- 状态：sensitivity_outcome_integrity_gated；three_completed_scenarios_revalidated；language_scan_clean

### 2026-07-16 07:05 - 九场景 summary 与底层工件建立逐行门禁

- 缺口：`collect_sensitivity_summary()` 会从 baseline 和八个场景重算九行，但旧总门禁只让 claims 与 summary 自洽，没有再次验证 summary 是否仍等于底层工件。
- TDD：新增正常路径、summary 行篡改、baseline SHA 错误、scenario definitions 变更、runner 来源 SHA 错误和总报告接线，共 6 项。实现前为 `6 failed`，实现后为 `6 passed, 76 deselected`。
- 实现：`validate_sensitivity_summary` 核对 baseline SHA、788 候选数、九场景数量、中间商响应方法、完整场景定义及 summary runner 来源哈希；随后用 `_summary_row` 从 baseline 和八个已通过单场景门禁的 JSON 精确重构九行并逐项比较。
- 证据顺序：单场景 provenance/numerics → 九行 summary 重构 → summary SHA 绑定的 range/direction/profit-sign claims → TeX table 与 Figure 6。任何中间层变化都会使最终总报告失败。
- 验证：证据门禁、sensitivity runner、claims、table 和 price-shape 组合回归为 `99 passed in 0.63s`；Ruff clean，相关文件 `git diff --check` 无输出。
- 状态：sensitivity_summary_artifact_linked；claims_chain_complete_pending_eight_runs

### 2026-07-16 07:09 - 候选策略域与主稿逐项绑定

- 核对：从 `candidate_manifest_submission.json` 读取八个组件的 added/cumulative counts，并把正文列出的 18 个 continuation-only 向量解析为数值集合后比较。组件计数、52 个 support entries、48 个 distinct vectors、18 个新增向量及全部向量均一致。
- 测试设计：向量按浮点数比较，不把 `1` 与 `1.0` 的显示差异当成内容错误。首次字符串测试因此失败一次，改为解析 LaTeX 数组后通过；论文无需修改。
- 回归调度：两次使用 `taskset -c 31` 的低优先级主稿回归被同核敏感性 worker 长时间抢占，工具调用返回时测试仍在运行。只终止本轮产生的两个重复 Pytest 进程组，没有触碰 PGID 24917/24918 的求解器；随后取消单核绑定重跑。
- 验证：主稿非敏感性门禁为 `37 passed, 3 deselected in 0.40s`，显式 `PYTEST_EXIT=0`。三个 deselected 仍仅对应最终 sensitivity table、Figure 6 和占位段替换。
- 状态：candidate_domain_manuscript_bound；duplicate_test_processes_cleared；solver_processes_untouched

### 2026-07-16 07:15 - 终稿图件矢量、字号与图标来源复核

- 范围：逐张视觉检查当前 Figure 1--5；Figure 6 仍等待八个共同候选集场景全部通过后生成。现有图未发现文字、标注、曲线或图例遮挡，面板标识均位于各子图下方。
- 导出检查：五个正式 PDF 均为单页；`pdfimages -list` 显示 0 个栅格对象。四张 Matplotlib 图只嵌入 `TimesNewRomanPSMT`，框架图嵌入 Times New Roman regular/bold/italic，所有字体均为 embedded/subset。对应 PNG 为 360 dpi；框架图另有可编辑 Draw.io 和 SVG 源。
- 正文字号：A4 正文宽约 465 pt；框架 PDF 原宽 1,368 pt，缩放比例约 0.340。Draw.io 最小字号为 16 pt，因此正文中的理论最小字号约 5.44 pt；其余定量图最小图例字号缩放后约 5.7--6.5 pt，满足密集期刊图常用的 5--7 pt 下限。
- 来源门禁：`test_final_framework_drawio.py` 新增对嵌入 SVG 内容哈希的检查。每个 Draw.io 图标必须匹配固定 Streamline 素材库的 `SHA256SUMS.txt`；测试同时要求署名包含固定提交 `52d750c...`、CC BY 4.0 名称和完整许可文本。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s uv run --no-project \
    --with pytest --with pillow pytest -q tests/test_final_framework_drawio.py
  uv run --no-project python \
    /mnt/d/ccchtLinkData/UserProfile/.codex/skills/drawio-skill/scripts/validate.py \
    figure_sources/spatiotemporal_pricing_framework_final_2026-07-14.drawio --strict
  uv run --no-project --with ruff ruff check tests/test_final_framework_drawio.py
  ```
- 结果：`7 passed in 0.34s`；Draw.io 为 `0 error(s), 0 warning(s)`；Ruff 为 `All checks passed!`。本轮未重绘或改动任何结果图数据。
- 运行状态：敏感性场景仍为 3/8；`price_sensitivity_high` 已写入 40,301 个动态缓存条目，`migration_cost_high` 已写入 8,868 个，两个 supervisor 及三个收尾 waiter 均存活。
- 状态：figure_1_to_5_qa_verified；icon_provenance_hash_gated；figure_6_pending

### 2026-07-16 07:22 - 离网 regret 定义、混合策略时序与期刊规则复核

- 理论缺口：结果段给出 provider A/B 的 `0.400%/0.473%` relative off-grid regret，但方法段原先没有定义分母；混合均衡也没有说明抽样发生在日内还是日前。
- TDD：新增 `test_offgrid_relative_regret_and_mixed_strategy_timing_are_defined`。修改正文前定向运行按预期为 `1 failed`；补充公式和时序解释后为 `1 passed`。
- 公式：若 $\widehat v_m^{\mathrm{off}}$ 是有界搜索找到的最大偏离收益，$v_m$ 是有限博弈均衡收益，则正文现定义 $\epsilon_m^{\mathrm{off}}=\widehat v_m^{\mathrm{off}}-v_m$ 和 $\rho_m^{\mathrm{off}}=\epsilon_m^{\mathrm{off}}/\max\{|v_m|,1\}$；0.5% 门禁作用于 $\rho_m^{\mathrm{off}}$。
- 时序：正文现明确每个服务商在一个模拟日开始前独立抽取一条完整日内价格规则，不在每个时段重新抽取。该混合分布是博弈均衡对象，不是确定性 tariff 建议。
- 回归：一次未精确排除等待项的运行得到 `2 failed, 38 passed, 1 deselected`；两项失败分别是 Figure 6 尚不存在和敏感性占位符尚未替换。按三个等待项的精确测试名排除后为 `38 passed, 3 deselected in 0.45s`；Ruff clean，`git diff --check` 无输出。
- 编译：
  ```bash
  nice -n 15 timeout 180s latexmk -xelatex -interaction=nonstopmode \
    -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
  结果为 22 页 A4、PDF 1.5，SHA-256 `4b5fb961...f179`；日志无 LaTeX error、未定义引用/文献、overfull 或 underfull。新增定义和混合策略时序可从 PDF 文本检索。
- 期刊规则：2026-07-16 重新核对 SMPT 官方 Guide for Authors。当前摘要低于 250 词、关键词为 7 个、五个编号主章节符合格式要求。官方仍要求 title-page 作者/机构/通讯信息、3--5 条且每条不超过 85 字符的独立 Highlights、利益冲突与基金声明、生成式 AI 声明，以及 Option C 数据仓储链接或不能共享的理由。
- Highlights：正式根目录文件 `peak_shaving_dynamic_pricing_SMPT_highlights_2026-07-14.txt` 已有 5 条，长度为 66--83 字符并由测试约束。旧 225 点 Highlights 明确指向该文件；`docs/submission` 中仅保留同文副本，不作为第二套主张来源。
- 仍需作者完成：真实作者与机构、通讯作者、Funding、competing interests、CRediT、数据发布/DOI，以及不使用 AI 辅助图像工具独立重建并核对六张投稿图。
- 状态：offgrid_metric_defined；mixed_strategy_timing_explicit；official_guide_rechecked；author_actions_pending

### 2026-07-16 07:29 - 原生需求、移动指标与需求质心定义补全

- 自包含性审计：正文此前报告了柔性需求的 destination centroid，但只在实现中按 `sum(t * demand_t) / sum(demand_t)` 计算，没有给出论文定义。原生需求、peak-to-average ratio 和 temporally moved fraction 也已在本轮前一步补为显式公式。
- TDD：新增 `test_flexible_destination_centroid_is_defined`。修改正文前定向结果按预期为 `1 failed`；补充公式、1-based 时段约定及方向解释后为 `1 passed`。
- 正文：方法段现定义
  `C_k = sum_t t E[D_tilde_{k,t}] / sum_t E[D_tilde_{k,t}]`，并说明较低值表示更早的平均目的时段。该定义与 `spatiotemporal_mechanism.py` 及正式 baseline 工件的计算一致。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s uv run --no-project --with pytest \
    pytest -q tests/test_final_manuscript_20260714.py \
    --deselect tests/test_final_manuscript_20260714.py::test_submission_figures_exist_and_are_referenced \
    --deselect tests/test_final_manuscript_20260714.py::test_resolved_sensitivity_table_and_figure_are_both_integrated \
    --deselect tests/test_final_manuscript_20260714.py::test_submission_text_has_no_result_placeholders_or_stale_main_values
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s uv run --no-project --with ruff \
    ruff check tests/test_final_manuscript_20260714.py
  nice -n 15 timeout 180s latexmk -xelatex -interaction=nonstopmode \
    -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：非敏感性主稿门禁为 `40 passed, 3 deselected in 0.46s`；Ruff 为 `All checks passed!`。PDF 为 22 页 A4、PDF 1.5，SHA-256 为 `4218d098cc51aacaa0a774935bf4daf944475bb013cabe8b426a8b6bb79a2ef4`；日志无 LaTeX error、未定义引用/文献、overfull 或 underfull，新增公式与解释已进入 PDF 文本。
- 运行状态：两条敏感性 supervisor 和三个收尾 waiter 均存活；本次只修改主稿、稿件测试和实验记录，没有改变冻结数值来源或运行中的求解。
- 状态：reported_metrics_self_contained；manuscript_non_sensitivity_gates_passed；sensitivity_progress_3_of_8

### 2026-07-16 07:34 - 中间商重优化对服务商支付的后验检查

- 审稿问题：现有 globality audit 只以中间商自身利润改善率作为门禁。中间商目标近似持平并不必然意味着服务商支付也近似不变，尤其是接近确定性路由时。
- 操作：只读加载正式 baseline 与 `intermediary_globality_audit_submission.json`，分别在 676 个正概率剖面上重算 stored candidate 和 independent differential-evolution candidate，共 1,352 次联合市场固定点；没有写入正式工件，也没有修改运行中的求解器或冻结数值来源。
- 结果：1,352 次计算全部收敛。按均衡剖面概率加权后，服务商 A/B 的收益变化为 `-0.01412/+0.01342`，加权绝对变化为 `0.03780/0.03510`，相对其期望收益均很小。最大单剖面变化发生在 `(625,112)`：A 为 `+57.1321`（`+6.916%`），B 为 `-52.9505`（`-7.415%`），但该剖面概率质量仅为 `0.0001867`。对应中间商利润改善为 `0.10268`。
- 判断：这不改变“已评估数值支付矩阵上的有限博弈均衡”结论，也没有证明重优化响应下的全候选 regret。它揭示了一个需要单独记录的 follower-response 非唯一性/近平台区间：小的中间商目标误差可伴随较大的低概率单剖面服务商支付变化。
- 决策：等待自动 post-sensitivity 管线重建正式中间商审计后，再生成带来源哈希的派生支付敏感性工件、测试和正文限制说明；当前不修改等待脚本，避免让正在运行的收尾链读取半成品。
- 审稿记录：已同步更新 `smpt_final_three_reviewer_audit_2026-07-14.md`、`smpt_submission_evidence_map_2026-07-14.md` 和 `smpt_theory_code_consistency_audit_2026-07-14.md`。这些文件明确区分“加权主运行指标稳定”与“原混合策略在重优化活跃支付矩阵上的非零 regret”。
- 文献复核：再次读取 AAAI、ScienceDirect 和 arXiv 一手页面，确认 PriLLM、三层 VPP Stackelberg、GPU pricing/scaling 与 token-pool 四条 2026 引用的题名、作者、年份和发表状态仍与 `verified_refs.bib` 一致，本轮无需修改参考文献。
- 状态：follower_payoff_sensitivity_identified；weighted_effect_small；formal_artifact_pending_post_rebuild

### 2026-07-16 07:42 - 候选曲线唯一性与非收敛对象表述复核

- 候选域检查：从正式 baseline 的 788 个四系数向量重建每个候选的 8 时段批发价与直售价，在 `1e-12` 精度下得到 788 个不同的 16 维实现价格曲线；截断算子没有把不同向量压成重复曲线。因此主稿中 `each producing a distinct bounded price profile` 有数值依据。
- 文字问题：参数段原句 `A candidate is excluded if the joint fixed point fails` 容易被理解为删除服务商价格候选。实现实际是在每次中间商搜索中丢弃固定点未收敛的 response evaluation；服务商 788 候选集合不因此缩减。
- 修改：参数段改为 `Within an intermediary search, a response evaluation is discarded if its joint fixed point does not converge.`；方法段中更完整的非收敛边界保持不变。
- 测试：稿件测试增加禁止旧歧义句和要求新句的断言；与需求质心测试合计 `2 passed in 0.13s`，Ruff 为 `All checks passed!`，相关文件 `git diff --check` 无输出。
- 对比基线判断：2026-06-19 的 service-management/SMPT baselines 属于已废弃的旧需求模型和 225 候选阶段，不能与当前 788 候选守恒 OD 模型并列。终稿继续使用统一价格受限均衡作为公平基线，机制分解用于区分 temporal 与 spatial response，不混入版本不一致的旧结果。
- 运行状态：`price_sensitivity_high` 已保存 43,345 个动态支付对，`migration_cost_high` 已保存 17,060 个；两组 worker 继续运行。
- 状态：candidate_profiles_unique；response_failure_scope_precise；stale_baselines_excluded

### 2026-07-16 07:50 - 均衡符号与主求解器设置写入 PDF

- 记号审计：补定义全博弈策略数 `n_A=n_B=788`、概率单纯形和 regret 式中的单位向量。将 QoS 函数 `Q(u)` 与结果指标原先共用的 `Q` 拆开；报告量现记为 `L_peak`、`u_max`、`q_min` 和期望市场侧利润，peak-to-average ratio 同步使用 `L_peak`。
- 中间商优化器：正文现报告三类区域共 36 个粗起点之外的核心设置，即每个 L-BFGS-B 局部运行最多 250 次迭代、每次最多 30 个 line-search steps、相对目标下降容差 `1e-10`、投影梯度容差 `1e-8`，以及绝对/相对并列容差 `tau_I=max(1e-8,1e-10 max(|Pi_I|,1))`。
- 混合互补求解器：正文现报告 Fischer--Burmeister bounded least-squares 的 5,000 次函数评估上限、三项 `1e-13` 终止容差、五个支持概率阈值 `1e-5` 至 `1e-9`，以及归一化支付下 `1e-9` 的 support-polish regret 门限。
- TDD：四组新增稿件测试均先在缺少定义/设置时失败，补充正文后通过。完整非敏感性稿件门禁为 `44 passed, 3 deselected in 0.50s`；三个 deselected 仍只对应正式 sensitivity 表、Figure 6 和占位段替换。Ruff 为 `All checks passed!`。
- 编译：
  ```bash
  nice -n 15 timeout 180s latexmk -xelatex -interaction=nonstopmode \
    -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：23 页 A4、PDF 1.5，SHA-256 `942fcc30999b6aeaebd7becb6adfb4a5bc5f9a1d9d5c28c70a37602c7a8503b8`；日志无 LaTeX error、未定义引用/文献、overfull 或 underfull。逐页渲染检查新增求解器段和需求质心页，未见公式、正文、页码或标题重叠。
- 状态：finite_game_notation_complete；primary_solver_settings_reported；latex_verified

### 2026-07-16 07:52 - 数值审计门槛与经济显著性分离

- 问题：方法和结果将离网格相对 regret 的 `0.5%` 门槛及中间商相对利润改进的 `0.1%` 门槛称为 numerical adequacy/audit threshold，但没有明确说明它们不是经济显著性界线。
- TDD：新增 `test_numerical_audit_gates_are_not_economic_significance_thresholds`。正文修改前定向测试按预期为 `1 failed`；补充边界说明后为 `1 passed in 0.02s`。
- 修改：方法段现将两个阈值定义为预先声明的数值报告门槛，并明确它们不是经济显著性判据。有限候选、离网格与 follower-response 的证据范围不变。
- 回归与编译：非敏感性主稿门禁为 `45 passed, 3 deselected in 0.48s`。`latexmk -xelatex` 成功生成 23 页 A4、PDF 1.5，SHA-256 为 `a8daf5f20534c2a02fbc95bc35c3024d2009c543e4ad6b76304dda6c034b8f09`；日志未发现 LaTeX error、未定义引用/文献、overfull 或 underfull，新增句已从 PDF 文本检索确认。
- 运行状态：两个敏感性 supervisor 及三个收尾 waiter 均存活；`price_sensitivity_high` 已保存 43,345 个动态支付对，`migration_cost_high` 已保存 17,060 个。RTX 4090 利用率约 1%，但现有 SciPy 固定点、优化与 bimatrix 求解没有经过验证的 CUDA 路径，本轮保持冻结 CPU 数值实现。
- 状态：numerical_gate_semantics_explicit；sensitivity_progress_3_of_8

### 2026-07-16 07:55 - 离散选择异质性边界补充

- 审稿问题：两阶段 logit 已在方法中声明独立 type-I extreme-value 冲击和类型级参数，但 Limitations 没有直接说明该设定排除了相关偏好与用户级系数异质性；两个请求类型共用同一原生日内形状的限制也只出现在模型定义中。
- TDD：新增 `test_discrete_choice_heterogeneity_boundary_is_explicit`。正文修改前为 `1 failed`，在限制段加入三项明确边界后为 `1 passed in 0.02s`。
- 修改：Limitations 现说明每一请求类型内部使用共同系数、冲击相互独立、未表示相关偏好或用户级系数异质性，并指出两类请求共用同一原生日内负载形状。现有模型、参数、工件和结论均未改变。
- 运行状态：`price_sensitivity_high` 动态缓存已推进到 44,864 个支付对；`migration_cost_high` 仍在 17,060 后的大批次计算，所有 supervisor/waiter 保持存活。
- 状态：choice_model_scope_explicit；sensitivity_progress_3_of_8

### 2026-07-16 07:58 - 支付矩阵归一化公式补全

- 复现性问题：正文原先只称混合互补求解器使用 positive affine normalization，没有说明代码中的精确变换和常数矩阵分支。
- TDD：新增 `test_payoff_normalization_is_defined_for_regular_and_constant_matrices`。补公式前为 `1 failed`；首次补充后测试因断言使用 `applied` 而正文使用 `applies` 仍失败，修正测试的文字假设后为 `1 passed in 0.11s`。
- 修改：方法段现给出逐服务商支付矩阵的 min--max 归一化：非恒定矩阵映射为 `(U-min U)/(max U-min U)`，恒定矩阵映射为零矩阵；同时说明前者保持 best-response 顺序，后者表示该玩家对策略无差异。公式与 `pricing_sim/bimatrix_solver.py::_positive_affine_normalize` 一致。
- 状态：payoff_normalization_self_contained；solver_reproducibility_improved

### 2026-07-16 07:59 - 分时价格与实时反馈的边界明确

- 术语风险：`time-varying/dynamic pricing` 容易被理解为根据当天已实现负载在线更新的反馈控制；当前模型实际使用固定 BurstGPT 平均负载信号生成日前八时段价格表。
- TDD：新增 `test_price_rules_are_day_ahead_schedules_not_real_time_feedback`，并扩展离散选择限制测试以覆盖观测与调整假设。正文修改前为 `2 failed`，补充说明后为 `2 passed in 0.02s`。
- 修改：价格规则段现明确其为 day-ahead time-of-use schedules，不随 realized within-day demand 更新；Limitations 现说明用户与中间商无观测误差或调整延迟地响应模型价格和 QoS。本文没有因此声称实时定价、在线学习或强化学习控制。
- 综合验证：非敏感性主稿为 `48 passed, 3 deselected in 0.47s`，Ruff 与 `git diff --check` 均通过。`latexmk -xelatex` 成功生成 23 页 A4 PDF，SHA-256 `464377e6d74f46d61211804fbad72e439a4eacb7337b79bbcfeff890045490d7`；日志无 LaTeX error、未定义引用/文献、overfull 或 underfull。逐页渲染检查第 7、9、18 页，新增价格时序、支付归一化公式和行为限制未造成公式或正文重叠。
- 状态：day_ahead_policy_scope_explicit；information_delay_omitted_explicitly

### 2026-07-16 08:01 - 模型参数定义域补全

- 理论自包含性：效用和 OD 公式原先通过参数表隐含使用正总需求、非负份额、有效移动比例、整数移动窗口、非负成本/权重及正渠道偏好，但没有在公式附近逐项声明。
- TDD：新增 `test_model_parameter_domains_are_explicit`。正文修改前为 `1 failed`，补齐定义域后为 `1 passed in 0.02s`。
- 修改：方法段现声明 `N>0`、非负且归一化的 `gamma/nu`、`phi in [0,1]`、非负整数 `H`、`kappa>=0`、`b_c>0`、`alpha>=0`、`omega_q>=0`、`G_A>G_B>0`、正 QoS threshold/strength 以及非负容量/退化成本。扩展测试曾因新增的容量断言按预期再次失败，补齐剩余定义域后恢复为 `1 passed in 0.02s`。这些条件与已执行配置一致，不改变模型或实验输出。
- 状态：parameter_domains_explicit；theory_self_containment_improved

### 2026-07-16 08:06 - 统一价格连续基价临时诊断首次启动失败

- 目标：检查仅含 12 个零斜率候选的统一价格受限均衡，是否在连续批发/直售基价域内存在明显遗漏偏离；该检查只写 `/tmp`，不属于正式投稿工件。
- 首次命令：通过 `uv run ... python - <<'PY'` 从标准输入启动 4-worker `PairEvaluator`，计划使用 512 点二维 Latin hypercube、`9x13` 粗网格和 `17x17` 局部网格，服务商斜率与中间商零售价斜率固定为零。
- 失败：退出时抛出 `concurrent.futures.process.BrokenProcessPool`。子进程采用 `spawn`，试图重新导入 `/root/paper_code/0427_tokenrl/paper_token_cross_survey/<stdin>`，因该路径不存在而失败；没有完成任何正式结果，也没有修改仓库数值文件。
- 修复决策：将同一临时诊断放到 `/tmp` 的具名 Python 文件，并使用 `if __name__ == "__main__"` 后重启。运行中的敏感性 supervisor 与 waiter 未受影响。
- 第二次启动：`py_compile` 成功，但直接执行 `/tmp/uniform_offgrid_diagnostic_20260716.py` 立即报 `ModuleNotFoundError: No module named 'experiments'`，因为 Python 将脚本目录 `/tmp` 而非仓库根加入模块搜索路径。后续启动显式设置 `PYTHONPATH=/root/paper_code/0427_tokenrl/paper_token_cross_survey`；该错误同样未产生数值结果或修改仓库工件。
- 状态：failed_expected_infrastructure_issue；retry_with_importable_temp_script

### 2026-07-16 08:10 - 固定容量成本的策略作用说明

- 审稿问题：利润式包含容量持有成本，但在固定容量设计中该项对同一服务商的所有价格策略都是常数。若不说明，读者可能误认为该参数改变了价格最佳响应。
- TDD：新增 `test_fixed_capacity_cost_role_in_strategy_and_accounting_is_explicit`。正文修改前为 `1 failed`，补充策略与会计作用后为 `1 passed in 0.02s`。
- 修改：利润定义后现说明容量成本改变服务商与市场侧利润的报告水平，但不改变 best-response order。退化成本仍随流量和 QoS 变化并进入策略权衡。
- 临时诊断：具名 `/tmp` 脚本已用显式 `PYTHONPATH` 成功进入计算阶段，4 个低优先级 worker 正在处理统一基价全局搜索；尚无可解释结果。
- 状态：fixed_capacity_cost_role_explicit；uniform_baseline_offgrid_running

### 2026-07-16 08:11 - temporal-only 控制的目的时段效用补全

- 复现性问题：正文说明关闭空间响应时固定渠道份额和容量比例路由，但未说明 `allocate_spatiotemporal_demand` 此时如何形成目的时段效用。
- TDD：扩展 temporal-only 机制测试。补充前为 `1 failed`，正文写入控制定义后为 `1 passed in 0.02s`。
- 修改：机制分解段现说明 spatial-off 时用 `(0.12,0.50,0.38)` 固定份额加权三条渠道效用；spatial-on 时使用 Eq. (destination value) 的 log-sum inclusive value。由此 Figure 5 的 temporal-only/spatial-only 控制可仅凭 PDF 与参数表重建。
- 回归修复：首次完整非敏感性回归为 `2 failed, 48 passed, 3 deselected`。两项失败均因旧测试仍要求不带定义域的 `alpha/bar_u/zeta/c_G/c_q` 原句；更新断言检查更严格的新定义后为 `50 passed, 3 deselected in 0.63s`。Ruff 与 `git diff --check` 均通过。
- 编译与视觉检查：`latexmk -xelatex` 成功生成 23 页 A4、PDF 1.5，SHA-256 `12ea66726249a57408ad9cb9d0f7124bdde3ac0bdb3f0f8facee5d3e45f46fb0`；日志无 LaTeX error、未定义引用/文献、overfull 或 underfull。渲染检查第 5、8、17 页，参数域、固定容量成本和机制控制段均无公式、表格或正文重叠。
- 状态：mechanism_control_utility_explicit；decomposition_reproducibility_improved

### 2026-07-16 08:16 - 主比较的策略处理范围明确

- 解释风险：统一与分时博弈的差别同时覆盖服务商批发/直售斜率和中间商零售斜率；若结果段不直说，12.32% 峰值变化可能被误读为只改变一条 posted price 的因果处理。
- TDD：扩展统一基线定位测试。正文修改前为 `1 failed`，加入结果段范围说明后为 `1 passed in 0.03s`。
- 修改：Section 4.2 现明确统一受限博弈把全部服务商斜率和中间商零售斜率固定为零，分时博弈允许两层价格形状变化；主比较不是其余决策固定的一价-at-a-time 实验。
- 术语统一：Table 3 第三列表头由 `Dynamic` 改为 `Time-varying`，与题名、caption、正文和日前分时定位一致；工件绑定表格测试增加正向/禁止旧表头断言，定向结果为 `1 passed in 0.14s`。
- 临时统一基线搜索进度：服务商 A 已完成 384/630 个全局零斜率候选；缓存按 baseline SHA 与响应设置签名，尚未形成结论。
- 状态：comparison_policy_scope_explicit；causal_overinterpretation_reduced

### 2026-07-16 08:21 - 统一价格 12 候选基线发现重大离散化缺口

- 触发：正式 off-grid 工件只检查 788 候选分时均衡，没有检查仅含 12 个零斜率候选的统一价格基线。为验证基线公平性，启动不写仓库工件的二维连续基价临时搜索；服务商斜率和中间商零售斜率均固定为零，中间商仍使用正式连续多起点响应。
- 初步结果：服务商 A 的 630 个全局候选已经完成。当前最佳偏离由正式统一策略 `(0.575,0,0.600,0)` 移至约 `(0.5708546,0,0.6342739,0)`，A 利润从 `944.2488` 升至 `1052.3974`；绝对改进 `108.1486`，相对原收益约 `11.45%`。联合固定点残差为 `8.05e-10`。局部网格和服务商 B 尚在运行，因此这些数值只作预警，不进入论文。
- 判断：这不是轻微 off-grid 误差。当前 12-rule 统一结果不能继续作为可信的连续统一价格均衡；以它为分母的 `12.32%` 峰值、`15.70%` 最大利用率和 `0.890→0.959` QoS 比较均待更新。可以准确称为 12-candidate finite benchmark，但该定位不足以支撑当前主比较的投稿强度。
- 决策：不终止正在运行的动态 788 候选敏感性，因为其动态均衡仍可复用。待当前八场景任务结束后，扩展统一零斜率候选集并对 baseline 与八个扰动分别重求统一有限博弈、执行二维离网格检查、重建 comparison/summary/claims/table/Figure 6 和主稿数字。正式门禁必须把统一基线 regret 与来源哈希纳入。
- 状态：major_uniform_baseline_gap_identified；main_comparison_numbers_provisional；temporary_A_search_continuing

### 2026-07-16 08:43 - 统一价格二维临时诊断完成

- 目的：完成旧统一价格基线的两方零斜率离网格预检查，并据此决定是否需要正式扩展候选集。该诊断文件只存于 `/tmp`，不作为论文证据。
- 实际命令：
  ```bash
  PYTHONPATH=/root/paper_code/0427_tokenrl/paper_token_cross_survey \
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    nice -n 15 uv run --no-project --with numpy --with scipy --with nashpy \
    python /tmp/uniform_offgrid_diagnostic_20260716.py
  ```
- 搜索域：两家服务商均固定批发与直售价斜率为零；每方使用 512 点二维 Latin hypercube、`9x13` 粗网格和围绕全局最佳点的 `17x17` 局部网格，共评估 918 个候选。中间商沿用正式统一价格 continuous-multistart 响应，并固定零售斜率为零。
- 服务商 A：旧策略为 `(0.575,0,0.600,0)`，旧收益 `944.248812`；临时最佳偏离为 `(0.574917,0,0.613649,0)`，收益 `1054.144932`，绝对 regret `109.896120`，相对 regret `11.6385%`。
- 服务商 B：旧策略同为 `(0.575,0,0.600,0)`，旧收益 `875.193127`；临时最佳偏离为 `(0.497813,0,0.766250,0)`，收益 `918.326807`，绝对 regret `43.133679`，相对 regret `4.9285%`。
- 数值核验：两方共 1,836 个候选全部返回收敛的联合固定点；最大联合残差 `9.99881e-10`，每个候选至少有 2 个成功局部响应起点。输入 baseline SHA-256 为 `d3717445...a2f`；临时 JSON SHA-256 为 `d1385eef...b4b`。
- 判断：两方均存在远高于数值门槛的遗漏偏离，旧 12-candidate uniform game 不能作为投稿级比较基线。旧 `12.32%`、`15.70%`、`0.890->0.959` 和 `-2.81%` 均保持 provisional。
- 后续设计：在当前八场景动态任务结束后，建立同一确定性空间填充零斜率候选集。计划集合由旧 12 个锚点、512 点固定种子 Latin hypercube、`9x13` 全域粗网格及围绕上述 A/B 临时最佳偏离的两个 `9x9` 局部网格组成，去重后为 800 个统一价格规则；与原 788 个动态候选取并集后预计为 1,576 个共同动态候选。baseline 与八个扰动均在这一共同集合上重求统一博弈，并把新增零斜率候选纳入动态博弈的全候选偏离检查；若出现正 regret，则续解动态均衡。正式工件需绑定候选集哈希、来源哈希、两方全候选 regret、独立二维离网格 regret 和固定点残差。上述数量须在实现测试和工件重建后再次确认。
- 状态：temporary_uniform_diagnostic_verified；formal_uniform_resolve_required；not_submission_evidence

### 2026-07-16 09:59 - `migration_cost_high` 动态敏感性场景通过

- 场景：迁移成本系数放大至基准值的 `1.3` 倍；使用冻结的 788 个服务商候选和 continuous-multistart 中间商响应，从正式 baseline 动态活跃支持续算。
- 实际命令由 `sensitivity_capacity_branch_queue.log` 记录：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 \
    OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    uv run --no-project --with numpy --with scipy --with nashpy python -c \
    "from experiments.run_submission_spatiotemporal_sensitivity import run_sensitivity; ..."
  ```
- 动态求解：评估 41,062 个支付对，A/B 正概率支持均为 26；全候选 absolute regret `2.27374e-13`，relative regret `2.71193e-16`，最大联合固定点残差 `9.99740e-10`。
- 条件比较：相对旧 12-candidate 统一基线，聚合峰值 `-11.8059%`、最大服务商利用率 `-15.8246%`、最低服务商 QoS `+0.0682831`、市场侧利润 `-2.78508%`。由于统一基线已确认存在离散化缺口，这四个比较值只用于缓存阶段审计，不进入最终论文。
- 验证：分支内的场景门禁和 20 个来源哈希全部通过；工件为 `sensitivity_migration_cost_high_submission.json`，SHA-256 `7b3d7ea9...8ea8`。
- 调度：capacity 分支已自动进入 `qos_threshold_high`；总进度由 3/8 更新为 4/8。冻结数值源未修改。
- 状态：dynamic_scenario_verified；conditional_comparison_provisional；sensitivity_progress_4_of_8

### 2026-07-16 11:45 - `price_sensitivity_high` 动态敏感性场景通过

- 场景：两类请求的价格敏感度均放大至基准值的 `1.2` 倍；继续使用冻结的 788 候选动态策略域和 continuous-multistart 中间商响应。
- 动态求解：评估 70,380 个支付对，A/B 正概率支持均为 16；全候选 absolute regret `2.27374e-13`，relative regret `2.94802e-16`，最大联合固定点残差 `9.99649e-10`。
- 条件比较：相对旧 12-candidate 统一基线，聚合峰值 `-11.9181%`、最大服务商利用率 `-12.2915%`、最低服务商 QoS `+0.0558747`、市场侧利润 `+24.2879%`。利润符号与其他场景不同，但统一基线尚未扩展，因此这些幅度和符号都不能作为最终稳健性结论。
- 验证：分支场景门禁通过；动态与统一全候选 regret、固定点残差、活跃剖面计数和 20 个来源哈希均符合冻结设置。工件 `sensitivity_price_sensitivity_high_submission.json` 的 SHA-256 为 `2a762e85...6dfa`。
- 调度：price 分支已自动进入 `migration_cost_low`；总进度由 4/8 更新为 5/8。缓存中的 70,380 个动态支付对将在 1,576 候选共同策略域重算时按向量复用。
- 状态：dynamic_scenario_verified；profit_claim_provisional；sensitivity_progress_5_of_8

### 2026-07-16 16:04 - WSL 非正常重启后的敏感性续算

- 现象：目标续跑恢复后，原 supervisor PID `24917/24918` 及 finalizer/post waiter 均不存在；日志停在 `migration_cost_low=676` 和 `qos_threshold_high=25,252`，且没有对应场景完成或 `.exit` 哨兵。
- 原因证据：`dmesg -T` 显示 WSL 于 15:45 重新初始化，并在 15:47 报告 system journal 因 unclean shutdown 被替换。没有 OOM kill、Python traceback 或求解器失败记录；本次中断属于 WSL 实例级重启。
- 缓存审计：两份 `dynamic.pkl` 均可完整反序列化，记录数分别为 676 和 25,252，签名分别为 `4c0b19...9324` 与 `edca6b...675d`；两个场景目录均无遗留 `.tmp` 文件。原子检查点有效，只有最近一次检查点之后尚未写入的计算需要重做。
- 恢复命令：
  ```bash
  bash /root/.cache/peak_shaving_submission_sensitivity/run_validated_branch.sh \
    price_branch 12 price_sensitivity_low migration_cost_low qos_threshold_low
  bash /root/.cache/peak_shaving_submission_sensitivity/run_validated_branch.sh \
    capacity_branch 16 capacity_high qos_threshold_high
  ```
- 恢复结果：已完成的 `price_sensitivity_low` 与 `capacity_high` 门禁重新通过；新 supervisor PID 为 3994/4053，求解进程 PID 为 4028/4082。`migration_cost_low` 与 `qos_threshold_high` 均从向量缓存加载后进入续算，没有重算已完成的五个场景。
- 收尾恢复：将缓存目录调度脚本中的旧 supervisor/finalizer PID 更新为本次恢复 PID，不改变仓库数值源码。新 sensitivity finalizer、post-audit waiter 和 completion waiter 的 PID 分别为 4346、4392、4411；它们会等待两个分支成功哨兵后重建 summary/table/Figure 6、审计和最终派生输出。
- 后续：在自动收尾链结束前保持数值源码冻结；若再次发生 WSL 实例重启，则仍以原子缓存记录数和成功哨兵为恢复依据。
- 状态：infrastructure_restart_recovered；atomic_caches_verified；sensitivity_progress_5_of_8

### 2026-07-16 16:24 - 将恢复链改为 detached 编排

- 二次调度问题：Codex 任务续转会关闭附着的统一执行 session。16:04 启动的 Bash supervisor/finalizer/waiter 因此退出，但其正在运行的 `uv`/Python 子进程被 PID 1 接管，`migration_cost_low` 与 `qos_threshold_high` 求解没有停止。
- 当前孤儿求解：外层 `uv` PID 为 4018/4072，Python PID 为 4028/4082；它们继续使用 PGID 3994/4053 和原缓存，28 个 worker 保持运行。不能直接再启动同名场景，否则会重复并发写同一缓存。
- 修复：新增缓存目录脚本 `/root/.cache/peak_shaving_submission_sensitivity/resume_pipeline_after_wsl_20260716.sh`。它先等待现有 PID 4018/4072 退出，再验证对应场景工件；只有验证失败时才按原缓存补跑。随后运行 `qos_threshold_low`，写出原分支哨兵，并串行调用 sensitivity finalizer、post-audit 和 completion 链。
- 启动命令：
  ```bash
  nohup setsid bash \
    /root/.cache/peak_shaving_submission_sensitivity/resume_pipeline_after_wsl_20260716.sh \
    >> artifacts/peak_shaving/20260712_expanded_response/resume_pipeline_after_wsl_20260716.log \
    2>&1 < /dev/null &
  printf '%s\n' "$!" \
    > /root/.cache/peak_shaving_submission_sensitivity/resume_pipeline_after_wsl_20260716.pid
  ```
- 验证：`bash -n` 退出码为 0；detached 主进程 PID 7426，PGID/SID 均为 7426，两个子控制器 PID 为 7427/7430。进程使用 `nohup` 且不依赖 Codex 统一执行 session，后续任务续转不会再移除调度链。
- 边界：该脚本只存在于缓存目录，不进入论文源码或数值来源哈希；没有修改算法、参数、候选集或已有工件。正式统一基线修复仍等待这一旧阶段链结束。
- 状态：detached_resume_verified；duplicate_cache_writers_avoided；sensitivity_progress_5_of_8

### 2026-07-16 17:13 - WSL 恢复后的新检查点验证

- 结果：`qos_threshold_high` 从重启前的 25,252 对推进到 33,444 对；`migration_cost_low` 从 676 对推进到 8,868 对。两份缓存均由恢复后的 worker 原子替换，说明旧记录加载、缺失对识别和续算写回均正常。
- 运行状态：detached 主控 PID 7426 与两个子控制器保持存活；孤儿求解 PID 4018/4072 继续由 PID 1 托管。28 个 worker 持续运行，未发现并发缓存写入、`.tmp` 残留或 traceback。
- 判断：16:24 的 detached 恢复方案现已由实际新检查点验证，不再只是语法和进程层检查。继续等待三个剩余场景和自动收尾链。
- 状态：post_restart_checkpoint_verified；atomic_resume_verified；sensitivity_progress_5_of_8

### 2026-07-16 18:54 - `qos_threshold_high` 动态敏感性场景通过

- 场景：将 QoS 阈值相对基准上移 `0.05`；继续使用冻结的 788 个动态候选和 continuous-multistart 中间商响应。
- 实际核验命令：
  ```bash
  uv run --no-project python -c "import json; ..."
  sha256sum \
    artifacts/peak_shaving/20260712_expanded_response/sensitivity_qos_threshold_high_submission.json
  cat /root/.cache/peak_shaving_submission_sensitivity/capacity_branch_queue.exit
  ```
- 动态求解：评估 53,971 个支付对，A/B 正概率支持均为 24，共 576 个正概率联合剖面；全候选 absolute regret `6.82121e-13`，relative regret `8.29639e-16`，最大联合固定点残差 `9.98403e-10`。
- 条件比较：相对旧 12-candidate 统一基线，聚合峰值 `-12.8669%`、最大服务商利用率 `-12.0871%`、最低服务商 QoS `+0.0477097`、市场侧利润 `+3.05711%`。统一基线存在已证实的二维离网格缺口，因此这些比较值只用于旧阶段缓存审计。
- 验证：场景门禁通过，统一有限博弈 regret 为 `0`，统一最大联合残差 `9.38081e-10`，20 个来源哈希通过；容量分支退出哨兵为 `0`。工件 `sensitivity_qos_threshold_high_submission.json` 的 SHA-256 为 `020855ce...1309`。
- 调度：detached 恢复主控 PID 7426 仍存活，容量分支已经结束；price 分支继续等待 `migration_cost_low`，随后将自动运行 `qos_threshold_low` 和旧阶段收尾链。总进度由 5/8 更新为 6/8，冻结数值源未修改。
- 状态：dynamic_scenario_verified；conditional_comparison_provisional；capacity_branch_verified；sensitivity_progress_6_of_8

### 2026-07-16 18:57 - 800 条统一价格规则的确定性设计预校验

- 目的：在不修改冻结数值源码的前提下，消除正式统一候选扩展中的随机种子和局部网格范围歧义，并复核预计候选数。
- 实际命令：
  ```bash
  uv run --no-project --with scipy python - <<'PY'
  # Construct anchors, a seeded 2-D Latin hypercube, the global lattice,
  # and two local lattices; then report disjoint increments and SHA-256.
  PY
  ```
- 定义：Latin-hypercube 使用 seed `20260716`，在批发基价 `[0.25,0.90]` 与直售基价 `[0.45,2.10]` 上取 512 点；全域格为 `9x13`。两个 `9x9` 局部格分别以临时最佳偏离 `(0.5749170633,0.6136488523)` 和 `(0.4978125,0.76625)` 为中心，每个维度的半宽为完整定义域跨度的 `5%`。
- 结果：组件的新增唯一规则数依次为旧锚点 `12`、Latin-hypercube `512`、全域格 `114`、A 局部格 `81`、B 局部格 `81`，累计恰为 `800`。全域格与旧锚点有 3 个重合；两个局部格与此前组件无重合。
- 检查：所有规则的两个斜率均严格为零，基价同时触及四个完整边界，两个诊断中心均存在。排序后的 `800x4` 浮点数组字节 SHA-256 为 `51608022...a5e6`。
- 边界：这是候选设计的只读预校验，不是均衡、regret 或投稿证据。正式实现仍需先写失败测试，并在旧阶段收尾链结束后由源码与候选清单重新生成和绑定哈希。
- 状态：uniform_design_deterministic；candidate_count_prevalidated；implementation_pending

### 2026-07-16 19:06 - 扩展 baseline 的隔离缓存预计算启动

- 目的：利用旧阶段 `migration_cost_low` 只占用 12 个 worker 的空闲算力，提前计算 800 条统一规则与 1,576 条共同规则 baseline 所需的支付对；正式源码和 submission JSON 继续冻结。
- 隔离实现：缓存目录新增一次性脚本 `/root/.cache/peak_shaving_uniform_expansion_baseline/precompute_augmented_baseline.py`。它读取旧 baseline 的 26/26 个正概率支持，在内存中重建已预校验的 800 条统一规则及其与旧 788 条动态规则的并集，只写 `/root/.cache/peak_shaving_uniform_expansion_baseline/{uniform,dynamic}.pkl` 和非正式 `precompute_result.json`。
- 实际命令：
  ```bash
  PYTHONPATH="$PWD" uv run --no-project --with numpy --with scipy \
    --with nashpy python -m py_compile \
    /root/.cache/peak_shaving_uniform_expansion_baseline/precompute_augmented_baseline.py
  nohup setsid env PYTHONPATH="$PWD" TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    nice -n 10 /root/.local/bin/uv run --no-project --with numpy \
    --with scipy --with nashpy python \
    /root/.cache/peak_shaving_uniform_expansion_baseline/precompute_augmented_baseline.py \
    >> /root/.cache/peak_shaving_uniform_expansion_baseline/precompute.log 2>&1 \
    < /dev/null &
  ```
- 启动验证：脚本编译退出码为 0；detached PID/PGID/SID 均为 `19800`，nice 为 `10`，使用 16 个 worker。旧敏感性缓存由另一组 PID 和目录写入，不存在同一文件并发写入。
- 输入绑定：旧 baseline SHA-256 为 `d3717445...aae2f`；800 规则数组 SHA-256 为 `51608022...a5e6`；1,576 规则并集 SHA-256 为 `01db2a6b...8f4d`；动态初始正概率支持为 26/26。
- 复用依据：支付缓存签名只绑定场景、连续中间商响应、游戏类型、市场数值源码和输入数据，不绑定候选索引；正式 runner 实现后可按精确策略向量重映射这些缓存。正式工件仍须由仓库源码重新运行、写入来源哈希并通过全部门禁，本次预计算结果不能直接引用。
- 独立签名核验：使用 `cache_signature`、默认 `IntermediarySearchSpec`、baseline 场景参数和正式 `evaluation_cache_sources` 重新计算 uniform 身份，得到 `46a6ee54...d20d`；与 `uniform.pkl` 内记录完全一致。候选源码扩展不会改变该签名，正式 runner 可直接加载。
- 首轮进展：800 规则统一博弈完成默认三点支持的全候选扫描并原子保存 4,791 对；加入下一轮受限支付后缓存为 4,792 对。首轮纯解的 A/B absolute regret 为 `103.4856/51.5743`，最佳响应分别为 `(0.55804564,0,0.57801058,0)` 与 `(0.4896875,0,0.76625,0)`。该轮尚非最终均衡，只证明扩展 oracle 正在吸收旧基线遗漏响应。
- 状态：isolated_precompute_running；official_artifacts_unchanged；numerical_sources_frozen

### 2026-07-16 19:42 - 共同候选设计的 TDD 红灯

- 目标：在正式候选源码仍冻结时，先锁定 800 条统一规则和 1,576 条共同规则的可复现 contract；测试覆盖确定性、完整基价边界、两个诊断中心、组件增量和排序数组 SHA-256。
- 修改：新增 `tests/test_submission_candidate_design.py`，预期接口为 `common_uniform_candidate_components`、`common_uniform_provider_candidate_grid` 和 `augmented_submission_provider_candidate_grid`。测试要求统一组件新增数为 `12/512/114/81/81`，统一数组哈希为 `51608022...a5e6`，共同数组哈希为 `01db2a6b...8f4d`。
- 首次命令：
  ```bash
  uv run pytest -q tests/test_submission_candidate_design.py
  ```
- 首次结果：pytest 未进入收集，退出时因桌面环境把 `TEMP/TMP` 指向 Windows 临时目录而抛出 `FileNotFoundError`；没有测试结果，也没有修改数值工件。
- 修复与实际红灯：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run pytest -q tests/test_submission_candidate_design.py
  ```
  显式加入仓库根导入路径后，第一轮结果为预期的 `3 failed in 0.13s`，三项均因 `experiments.submission_candidate_design` 尚不存在而失败。随后增加候选构造元数据、正式 runner 的不可覆盖归档种子，以及 equilibrium、sensitivity、off-grid 和 branch-audit 的持久缓存约束；最终复跑结果为 `8 failed in 0.86s`。新增失败分别对应元数据接口尚不存在、归档常量尚不存在、三个默认路径仍位于 `/tmp`，以及 branch audit 仍指向旧 `audit_enriched` 缓存。红灯均与待实现 contract 一一对应。
- 计算进展：扩展统一博弈第 5 轮已把缓存从 `8,771` 对推进到 `10,359` 对并进入下一轮；旧 `migration_cost_low` 仍在当前完整扫描。两条任务均无 traceback。
- 决策：等待旧动态敏感性恢复链完成后再实现新模块并转绿，避免改变旧场景绑定的数值源码；测试文件本身不属于旧工件的来源哈希。
- 状态：candidate_design_tests_red；numerical_sources_frozen；isolated_precompute_running

### 2026-07-16 20:13 - 扩展候选清单的 TDD 红灯

- 目标：在覆盖旧工件前，先固定扩展 candidate manifest 的稳定续算种子和外层组件计数。
- 修改：`tests/test_submission_candidate_manifest.py` 的 seed 改为待建立的 `pre_uniform_expansion/spatiotemporal_equilibrium_submission.json`；最终候选数改为 `1,576`，组件新增数改为 `800/378/120/64/27/100/69/18`，累计数改为 `800/1,178/1,298/1,362/1,389/1,489/1,558/1,576`，来源哈希要求新增 `submission_candidate_design.py`。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run pytest -q tests/test_submission_candidate_manifest.py
  ```
- 结果：首次运行因旧测试缺少显式仓库根导入而得到 3 个 `ModuleNotFoundError`；修正测试夹具后为预期的 `3 failed in 0.20s`，三项均准确失败于 `pre_uniform_expansion` 归档尚不存在。
- 静态检查：首次执行 `uv run ruff check ...` 因项目环境内没有 `ruff` 可执行文件而未启动；改用 `uv run --no-project --with ruff ruff check tests/test_submission_candidate_design.py tests/test_submission_candidate_manifest.py` 后得到 `All checks passed!`。
- 判断：不能为转绿而提前复制仍可能被旧收尾链更新的工件。归档必须等待八个旧动态场景及其派生审计全部完成，再以哈希清单一次性冻结。
- 状态：candidate_manifest_tests_red；archive_pending_old_pipeline；numerical_sources_frozen

### 2026-07-16 20:25 - 九场景统一价格离网格审计的 TDD 红灯

- 目标：为扩展后的统一价格受限均衡建立独立二维遗漏响应检查，并把 baseline 与八个单因素扰动全部纳入，而不是只审计 baseline 动态博弈。
- 预声明设计：每方至少使用 seed `20260718` 的 1,024 点二维 Latin hypercube，加入活跃支持和完整基价边界 guard；围绕全局阶段最佳点再使用半宽为完整域 `2.5%` 的 `17x17` 局部格。所有服务商斜率和中间商零售斜率保持为零。
- 修改：新增 `tests/test_submission_uniform_offgrid_audit.py`，锁定零斜率与边界校验、非零斜率支持拒绝、289 点局部格、九场景清单、持久缓存路径和输出文件名。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run pytest -q tests/test_submission_uniform_offgrid_audit.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run --no-project --with ruff ruff check \
    tests/test_submission_uniform_offgrid_audit.py
  ```
- 结果：pytest 为预期的 `4 failed in 0.13s`，分别因 `uniform_offgrid_diagnostic_tools.py` 和 `run_submission_uniform_offgrid_audit.py` 尚不存在；Ruff 为 `All checks passed!`，无 diff whitespace 错误。
- 门禁边界：正式工件需对九个场景逐方报告 relative regret、活跃支持支付重构误差、联合固定点收敛与最大残差；`0.5%` 仍只是预声明数值报告门槛，不是经济显著性标准，也不构成连续策略均衡证明。
- 状态：uniform_offgrid_tests_red；nine_scenario_scope_locked；implementation_pending_old_pipeline

### 2026-07-16 20:28 - follower 重优化服务商支付审计的 TDD 红灯

- 目标：把 07:34 的临时后验检查转为来源绑定的正式工件，避免用“中间商利润近似不变”替代“服务商支付近似不变”。
- 修改：新增 `tests/test_submission_intermediary_payoff_sensitivity.py`。纯汇总 contract 要求完整覆盖正概率支持笛卡尔积，分别报告服务商 A/B 的概率加权有符号变化、加权绝对变化、最大单剖面绝对变化，以及原混合策略在 independent-global follower response 活跃支付矩阵上的 regret。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run pytest -q \
    tests/test_submission_intermediary_payoff_sensitivity.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run --no-project --with ruff ruff check \
    tests/test_submission_intermediary_payoff_sensitivity.py
  ```
- 结果：pytest 为预期的 `3 failed in 0.04s`，均因 `build_submission_intermediary_payoff_sensitivity.py` 尚不存在；Ruff 为 `All checks passed!`。
- 解释边界：active-support regret 只检查原混合策略在正概率支持对应的重优化支付子矩阵上是否仍为互为最佳响应，不是对全部 1,576 个候选的 follower-reoptimized regret。正式正文必须保留这一区分。
- 状态：provider_payoff_sensitivity_tests_red；active_support_scope_explicit；implementation_pending_old_pipeline

### 2026-07-16 20:30 - SMPT 当前投稿规则与 Figure 1 来源链复核

- 目标：复核目标期刊当前 Guide for Authors，确认生成式图像限制是否影响最终六图，并区分历史 imagegen 草图与当前 Figure 1 蓝图的实际来源。
- 官方来源：[SMPT Guide for Authors](https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors)，访问日期 2026-07-16。指南确认 single-anonymized review、至少两名审稿人、可编辑源文件、摘要不超过 250 词、1--7 个英文关键词、独立 Highlights 文件、Option C 数据存储与链接，以及正式 title page 的作者、机构和通讯信息要求。
- 图像硬约束：期刊专属指南明确禁止使用 generative AI 或 AI-assisted tools 创建或修改投稿图像；仅当相关工具属于研究设计或方法时例外。本研究的框架布局和数据图制作不属于该例外，因此当前六图仍只作为内部审阅蓝图，作者必须在不使用生成式或 AI 辅助绘图工具的流程中独立重建并核验。
- Figure 1 链路：主稿实际引用 `figures/peak_shaving_final_20260714/spatiotemporal_pricing_framework.pdf`。构建脚本 `figure_sources/build_final_spatiotemporal_framework_drawio.py` 从 `figure_sources/iot_icon_candidates/streamline_ultimate_color/svg/` 嵌入原始 SVG；上游固定为 Streamline commit `52d750c9ce051e51cb181b7a78932120c48541d0`，许可为 CC BY 4.0，逐文件来源、SHA-256、许可文本和署名均已保存。
- 排除项：历史 `market_schematic_iot_imagegen_2026-06-22.png` 与 `framework_imagegen_p2p_reference_2026-07-10.png` 均不在当前 TeX 或最终 Figure 1 构建链中。该结论只排除沿用 imagegen 位图的风险；当前 Draw.io 布局和构建脚本曾接受 Codex 辅助，不能据此直接上传。
- 文档更新：在 `docs/submission/smpt_author_actions_2026-07-16.md` 补充 Figure 1 的固定来源、许可、署名和独立重建检查项；在 `docs/reviews/smpt_submission_adaptation_checklist_2026-06-21.md` 同步素材与制作过程的证据边界。
- 计算状态：旧 `migration_cost_low` 的 12 个 worker 与扩展 baseline 的 16 个低优先级 worker 均持续运行；扩展 uniform 缓存已推进到至少 23,776 个支付对，系统可用内存约 10 GiB，未发现 traceback 或重复缓存写入。
- 状态：journal_rules_reverified；figure1_asset_chain_non_imagegen；author_independent_rebuild_still_blocking；numerical_sources_frozen

### 2026-07-16 20:36 - 共同候选证据门禁的 TDD 红灯

- 目标：把 `800` 条统一规则和 `1,576` 条共同服务商规则传播到证据门禁、九场景表格与敏感性 claims contract，防止新均衡生成后仍被旧 `12/788` 检查误判或错误标注。
- 修改：更新 `tests/test_submission_evidence_gates.py` 的合成 baseline、off-grid、branch、candidate-manifest 和 sensitivity fixtures；新增 `GateThresholds` 必须声明 `uniform_candidate_count=800`、`provider_candidate_count=1576` 的测试，并要求 baseline 活跃剖面数由各自报告的正概率混合支持推导，不能继续硬编码旧 uniform `1` 与 dynamic `676`。同步更新 `tests/test_submission_sensitivity_table.py` 和 `tests/test_submission_sensitivity_claims.py`，并要求表注写出 common `1,576`-candidate set。
- 实际命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run --no-project --with ruff ruff check \
    tests/test_submission_evidence_gates.py \
    tests/test_submission_sensitivity_table.py \
    tests/test_submission_sensitivity_claims.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run pytest -q \
    tests/test_submission_evidence_gates.py \
    tests/test_submission_sensitivity_table.py \
    tests/test_submission_sensitivity_claims.py
  ```
- 结果：Ruff 为 `All checks passed!`，`git diff --check` 无输出；pytest 为预期的 `27 failed, 63 passed in 0.66s`。首个失败直接显示当前 `GateThresholds` 仍为 `12/788`，其余失败来自 evidence gate、sensitivity table 和 claims builder 仍拒绝 `1,576`，与待修改实现逐项对应。新增的两个定向 contract 测试复跑为 `2 failed in 0.45s`，分别失败于旧候选数和旧 baseline 活跃剖面硬编码。
- 边界：本轮只修改测试和 README；`submission_evidence_gates.py`、表格/claims builders、数值 runner 与工件均未修改。旧敏感性恢复链继续使用冻结源码。
- 调度修正：检查 detached 收尾脚本后发现它会运行上述三份既有测试。为避免新 contract 在旧数值阶段制造非数值失败，已将三份测试恢复为旧阶段 contract，并把四项扩展红灯迁移到独立的 `tests/test_submission_augmented_evidence_contract.py`；该文件不在旧收尾脚本的测试清单中。
- 修正验证：旧阶段三文件测试恢复为 `89 passed in 0.65s`；独立扩展测试为预期的 `4 failed in 0.40s`，分别锁定 `800/1,576` 门禁、由正概率混合支持推导活跃剖面数、`1,576` 表注和 `1,576` claims 元数据。四文件 Ruff 通过，`git diff --check` 无输出。
- 状态：expanded_evidence_contract_red_isolated；old_pipeline_test_contract_green；numerical_sources_frozen

### 2026-07-16 20:43 - 扩展图表与五章主稿的独立 TDD 红灯

- 目标：在数值实现解冻前固定最终展示 contract，同时避免修改旧恢复链会运行的既有 figure/manuscript 测试。
- 修改：新增 `tests/test_submission_augmented_figure_contract.py`，要求最终图表 builder 接入九场景统一离网格工件和 follower 重优化服务商支付工件，并把 Figure 1 蓝图的有限候选标签改为 `1,576`。新增 `tests/test_submission_augmented_manuscript_contract.py`，要求五章主稿输入生成结果宏与敏感性表、插入 resolved Figure 6、移除占位注释与旧 `788/12` scope、区分九场景统一二维离网格和 baseline 动态四维离网格，并删除五个 provisional 主比较值。
- 实际命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run pytest -q \
    tests/test_submission_augmented_figure_contract.py \
    tests/test_submission_augmented_manuscript_contract.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run --no-project --with ruff ruff check \
    tests/test_submission_augmented_figure_contract.py \
    tests/test_submission_augmented_manuscript_contract.py
  ```
- 结果：pytest 为预期的 `6 failed in 0.99s`。失败分别对应两个新审计路径尚不存在、Figure 1 仍写 `788`、主稿尚未输入宏和敏感性表、候选 scope/审计边界尚未更新，以及旧 `12.32/15.70/0.890/0.959/2.81` 仍存在。Ruff 通过，`git diff --check` 无输出。
- 调度边界：这两个新测试文件不在旧 sensitivity finalizer、post-audit 或 completion 脚本的测试列表中，不会影响冻结阶段收尾。
- 状态：augmented_figure_contract_red；augmented_manuscript_contract_red；old_pipeline_isolated

### 2026-07-16 20:46 - 旧 migration-low 全扫描完成并进入混合求解

- 目标：确认 WSL 恢复后的第七个旧敏感性场景没有停滞，并持续监控与 `800/1,576` 候选扩展预计算并行时的资源安全性。
- 旧场景进度：`migration_cost_low` 的持久 `dynamic.pkl` 已记录 `40,300` 个全候选支付对，随后写入 `40,301` 检查点并进入受限支持混合均衡求解；父进程 PID `4028` 下观察到 12 个活跃 `multiprocessing` 子进程，未发现 traceback，正式 JSON 尚未写出。
- 扩展预计算：`/root/.cache/peak_shaving_uniform_expansion_baseline/precompute.log` 再次确认 uniform `800`、共同候选 `1,576`，SHA-256 分别为 `516080224c67b6f7ab111e69f17d2a73801a6728f16c73336893f4729cfaa5e6` 与 `01db2a6b2ef32af4413f880f3317eae0076daf79c1c381aa43d65a054ac78f4d`；uniform 缓存推进到至少 `28,478` 个支付对。
- 资源：`free -h` 显示 15 GiB 内存中约 10 GiB 可用，swap 约 3.2 GiB 可用；两个任务仍分别保持 12 workers 和低优先级 16 workers，没有触发资源干预。
- 决策：继续等待旧场景写出并通过来源绑定验证；在 `submission_completion.exit=0` 前保持数值实现冻结，也不启动重复 writer 或正式增强 baseline runner。
- 状态：migration_low_full_scan_done；restricted_equilibrium_running；augmented_uniform_precompute_28478；numerical_sources_frozen

### 2026-07-16 20:58 - 两类新增审计纳入独立证据 contract

- 目标：要求最终总门禁不仅接受 `800/1,576` 候选 scope，还必须显式验证九场景统一价格离网格工件和 follower 重优化后的服务商支付敏感性工件。
- 修改：扩展旧收尾链不会执行的 `tests/test_submission_augmented_evidence_contract.py`。新增路径 contract；统一离网格验证必须绑定 baseline SHA、seed `20260718`、每方至少 1,024 个样本、九场景顺序与逐方 regret/固定点/支持支付检查；服务商支付验证必须绑定 baseline SHA、完整活跃概率质量和联合固定点残差。active-support regret 暂不设经济阈值，只要求作为有限诊断如实报告。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run pytest -q tests/test_submission_augmented_evidence_contract.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run --no-project --with ruff ruff check \
    tests/test_submission_augmented_evidence_contract.py
  git diff --check -- tests/test_submission_augmented_evidence_contract.py
  ```
- 结果：pytest 为预期的 `7 failed in 0.41s`；原四项仍对应候选数、活跃剖面推导、敏感性表和 claims，新增三项对应路径/验证器尚未实现。Ruff 为 `All checks passed!`，diff 检查无输出。
- 状态：augmented_evidence_contract_7_red；new_audits_gate_locked；old_pipeline_isolated

### 2026-07-16 21:03 - 增强 baseline 动态缓存复用审计

- 目标：判断旧 `788` baseline 的已验证支付记录能否按策略向量精确映射到新 `1,576` 网格，减少完全相同的 follower 求解，同时不跨场景复用支付。
- 检查：当前 baseline 工件记录旧动态缓存 signature `74a4b267965b0691584e1c0c7eee90cb52d4504412b5c2b9bf4d345b43712694`、`46,381` 个支付对；但 WSL 恢复后对应 `/tmp/peak_shaving_audit_enriched_equilibrium/dynamic.pkl` 已不存在。持久目录中现有 `dynamic.pkl` 均属于容量、价格敏感性、迁移成本或 QoS 阈值扰动场景。
- 决策：不同参数场景改变支付 oracle 身份，不能迁移为 baseline 记录。增强 baseline 的动态阶段必须重新评价所需支付对；不使用场景不匹配的缓存加速。
- 状态：baseline_cache_unavailable_after_wsl；cross_scenario_cache_reuse_rejected；dynamic_recompute_required

### 2026-07-16 21:05 - 八个同场景缓存可按精确向量扩展复用

- 代码核对：`cache_signature` 绑定场景参数、连续 follower response 规范、定价/固定点源码、QoS 校准和 BurstGPT 输入；`write_vector_pair_cache` 以两方完整四维策略向量为键，`load_vector_pair_cache` 只把新网格中逐元素存在的向量对映射回索引。
- 结论：同一敏感性场景从旧 `788` 子集扩到新 `1,576` 超集时，持久缓存可安全载入旧子集上已经计算的支付；新加入的统一规则、与动态规则的交叉对及 oracle 新支持仍由求解器重新评价。不同敏感性场景之间仍禁止复用。
- 影响：等待旧第七、第八场景完成不仅保留历史审计，也为正式共同候选重求提供合法的同场景 warm cache。baseline 的旧 `/tmp` 动态缓存已丢失，仍需完整重算。
- 状态：same_scenario_vector_cache_reuse_valid；expanded_pairs_still_recomputed；baseline_exception_retained

### 2026-07-16 21:08 - 旧证据归档门禁收紧

- 修改：缓存区 `archive_pre_uniform_expansion.sh` 的 required 清单扩为 baseline、八个敏感性场景、九场景汇总、总证据报告、生成表格与结果宏；归档 Python 阶段新增 `submission_evidence_gate_report.json` 的 `passed=true` 强制检查，并在任一工件记录的来源 SHA-256 与当前仓库文件不一致时立即退出。
- 原子性：全部检查仍发生在 `pre_uniform_expansion.staging` 内，只有成功后才移动到最终归档目录；大体积 pair cache 仍不进入提交证据归档。
- 验证：`bash -n /root/.cache/peak_shaving_submission_sensitivity/archive_pre_uniform_expansion.sh` 返回 0。脚本尚未执行，继续等待 `submission_completion.exit=0`。
- 状态：archive_requires_all_eight_scenarios；gate_and_source_hashes_enforced；execution_pending_completion

### 2026-07-16 21:26 - migration-cost-low 正式旧场景验证通过

- 工件：`sensitivity_migration_cost_low_submission.json`，SHA-256 `1e865053957a54662f163aced27360c472d85a1308cd5e6a9868ef88d5a31967`，大小 730,199 bytes。
- 参数与来源：迁移成本共同缩放为 `0.7`，其余三项保持 baseline；20 个来源哈希、共同策略契约、需求守恒和工件 baseline SHA 均通过独立 `validate_sensitivity_scenario` 检查。控制器也随后记录 `validated orphan-completed scenario: migration_cost_low`。
- 数值门禁：动态博弈使用 45,624 个支付对，6 个 oracle rounds 后以 `regret_tolerance` 终止；full regret `2.2737e-13`，relative regret `2.7275e-16`，最大联合残差 `9.9928e-10`，正概率支持为 `26x26`。旧统一限制 full regret 为 0，残差 `6.6362e-10`。
- 历史比较：相对旧 12 条统一限制，aggregate peak `-13.0433%`、maximum provider utilization `-14.7122%`、minimum QoS `+0.061800`、aggregate market-side profit `+2.9089%`。这些数值只进入 `pre_uniform_expansion` 历史归档，不进入扩展统一基线后的正文。
- 调度：恢复控制器已自动启动第八个场景 `qos_threshold_low`（12 workers）；其统一限制缓存已推进到 95 个支付对。
- 状态：migration_cost_low_verified；old_sensitivity_progress_7_of_8；qos_threshold_low_running；historical_comparison_withheld

### 2026-07-16 21:38 - `800` 条统一规则预计算阶段结束

- 运行证据：增强 baseline 日志在 uniform 缓存 `43,246` 个支付对后切换为 `dynamic cache checkpoint: 676 pairs`，说明 `run_equilibria` 已结束 `800` 条零斜率规则的双重 oracle 阶段，并开始以旧动态正概率支持的 `26x26` 笛卡尔积评价 `1,576` 条共同候选。
- 边界：runner 只会在 uniform 与 dynamic 两阶段都结束后原子写出 `precompute_result.json`；当前尚无该文件，因此不报告或推断 uniform regret、正概率支持和市场指标。`43,246` 仅是缓存规模，不是活跃剖面数。
- 缓存：`uniform.pkl` 约 220 MiB，新增 `dynamic.pkl` 约 3.5 MiB；系统约 11 GiB 可用内存。旧 `qos_threshold_low` 同时完成初始 `676` 个动态支付对并进入旧 `788` 网格全偏差扫描。
- 状态：augmented_uniform_phase_finished；augmented_dynamic_phase_started；precompute_result_pending；qos_low_full_scan_running

### 2026-07-16 22:31 - 两条动态扫描完成首个可恢复大块

- 增强 baseline：`1,576` 候选动态缓存从初始 `676` 推进到 `8,868` 个支付对，于 22:21 写出首个 `8,192` 对增量检查点。
- 旧第八场景：`qos_threshold_low` 的 `788` 候选动态缓存同样从 `676` 推进到 `8,868`，于 22:30 原子写出。
- 资源：两个进程分别保持 16 与 12 workers；检查点前约 10 GiB 内存可用，未见 traceback、worker 丢失或缓存回退。
- 决策：继续按相同 worker 数推进。两个持久缓存均已越过仅有初始支持矩阵的状态，WSL 中断时可从当前向量键记录恢复。
- 状态：augmented_dynamic_checkpoint_8868；qos_low_checkpoint_8868；recovery_state_persisted

### 2026-07-16 23:38 - 两条动态扫描推进到 17,060 对

- 目标：刷新第八个旧敏感性场景与 `800/1,576` 增强 baseline 预计算的实时状态，并确认原父 PID 未出现在沙箱 PID 命名空间时并非任务退出。
- 实际命令：
  ```bash
  tail -n 60 artifacts/peak_shaving/20260712_expanded_response/sensitivity_price_branch_queue.log
  tail -n 35 /root/.cache/peak_shaving_uniform_expansion_baseline/precompute.log
  find /root/.cache/peak_shaving_submission_sensitivity -maxdepth 3 -type f -mmin -90 -printf '%TY-%Tm-%Td %TH:%TM:%TS %s %p\n'
  find /root/.cache/peak_shaving_uniform_expansion_baseline -maxdepth 2 -type f -mmin -90 -printf '%TY-%Tm-%Td %TH:%TM:%TS %s %p\n'
  ps -p 7426,24917,19800,142689 -o pid,ppid,stat,etime,%cpu,%mem,rss,cmd
  ps --ppid 7427,19811 -o pid,ppid,stat,etime,%cpu,%mem,rss,cmd
  ps --ppid 37072 -o pid,ppid,stat,etime,%cpu,%mem,rss,cmd
  free -h
  ```
- 结果：`qos_threshold_low` 与增强 baseline 的动态缓存均从 `8,868` 推进到 `17,060` 个支付对。宿主进程核对显示旧场景保持 12 个约 100% CPU 的 worker，增强 baseline 保持 16 个约 100% CPU 的低优先级 worker；控制器 PID `7426` 与预计算 PID `19800` 仍存活。
- 资源：15 GiB 内存中约 9.1 GiB 可用，swap 约 3.5 GiB 可用。日志未见 traceback；第八场景正式 JSON、增强 `precompute_result.json` 和总完成哨兵仍未出现。
- 决策：继续运行现有 worker，不启动重复 writer。等待第八场景验证和旧后处理全部完成后执行来源绑定归档，再解冻数值源码并实现正式共同候选集。
- 状态：old_sensitivity_progress_7_of_8；qos_low_checkpoint_17060；augmented_dynamic_checkpoint_17060；final_artifacts_pending；numerical_sources_frozen

### 2026-07-17 00:18 - 增强 baseline 动态缓存推进到 25,252 对

- 目标：持续监测第八个旧敏感性场景和增强 baseline 预计算，并核对跨日运行后的 worker 与资源状态。
- 实际命令：
  ```bash
  tail -n 30 artifacts/peak_shaving/20260712_expanded_response/sensitivity_price_branch_queue.log
  tail -n 30 /root/.cache/peak_shaving_uniform_expansion_baseline/precompute.log
  ps -p 7426,19800,37054,37072,19811 -o pid,ppid,stat,etime,%cpu,%mem,rss,cmd
  ps --ppid 37072 -o pid,ppid,stat,etime,%cpu,%mem,rss,cmd
  ps --ppid 19811 -o pid,ppid,stat,etime,%cpu,%mem,rss,cmd
  free -h
  rg -n 'Traceback|ERROR|Exception|Killed|BrokenProcessPool' artifacts/peak_shaving/20260712_expanded_response/sensitivity_price_branch_queue.log
  rg -n 'Traceback|ERROR|Exception|Killed|BrokenProcessPool' /root/.cache/peak_shaving_uniform_expansion_baseline/precompute.log
  ```
- 结果：增强 baseline 动态缓存已从 `17,060` 推进到 `25,252` 个支付对；第八场景 `qos_threshold_low` 最近持久检查点仍为 `17,060`。增强 baseline 的 16 个低优先级 worker 与旧场景的 12 个 worker 均保持运行，错误关键字扫描无命中。
- 资源：15 GiB 内存中约 9.6 GiB 可用，swap 约 3.8 GiB 可用。第八场景正式 JSON、增强 `precompute_result.json` 和总完成哨兵均未出现。
- 决策：保持现有并行度并继续检测；只在完整旧流水线写出成功哨兵后执行历史证据归档和数值源码解冻。
- 状态：old_sensitivity_progress_7_of_8；qos_low_checkpoint_17060；augmented_dynamic_checkpoint_25252；workers_healthy；final_artifacts_pending

### 2026-07-17 00:50 - 第八场景动态缓存推进到 25,252 对

- 持续检测：`sensitivity_price_branch_queue.log` 在 00:50 前写出 `dynamic cache checkpoint: 25252 pairs`；增强 baseline 同期保持 `25,252` 个支付对。
- 运行边界：`sensitivity_qos_threshold_low_submission.json`、`precompute_result.json` 和 `submission_completion.exit` 仍未生成，因此这里只确认可恢复缓存推进，不解释均衡或市场指标。
- 决策：保持 12+16 worker 并继续等待下一批次；不启动重复任务，不解冻旧数值源码。
- 状态：old_sensitivity_progress_7_of_8；qos_low_checkpoint_25252；augmented_dynamic_checkpoint_25252；recovery_state_persisted

### 2026-07-17 00:56 - 增强 baseline 动态缓存推进到 33,444 对

- 持续检测：增强 baseline 的 `precompute.log` 写出 `dynamic cache checkpoint: 33444 pairs`；第八场景同期保持 `25,252` 个支付对。
- 边界：增强 `precompute_result.json` 尚未生成，当前仍只记录缓存规模，不报告 regret、支持集或市场结果。
- 状态：qos_low_checkpoint_25252；augmented_dynamic_checkpoint_33444；final_artifacts_pending

### 2026-07-17 01:46 - 增强 baseline 动态缓存推进到 41,636 对

- 持续检测：增强 baseline 从 `33,444` 完成一个标准 `8,192` 对批次并写出 `41,636` 检查点；16 个低优先级 worker 仍全部处于运行态。
- 边界：第八场景同期保持 `25,252`；增强预计算仍未写出结果文件，不能据此判断最终候选支持或 regret。
- 状态：qos_low_checkpoint_25252；augmented_dynamic_checkpoint_41636；precompute_still_running

### 2026-07-17 01:53 - 第八场景动态缓存推进到 33,444 对

- 持续检测：`qos_threshold_low` 从 `25,252` 完成一个 `8,192` 对批次并写出 `33,444` 检查点；增强 baseline 同期保持 `41,636`。
- 边界：两个正式结果文件和总完成哨兵仍未出现，数值结论继续保留。
- 状态：old_sensitivity_progress_7_of_8；qos_low_checkpoint_33444；augmented_dynamic_checkpoint_41636

### 2026-07-17 02:30 - 增强 baseline 动态缓存推进到 49,828 对

- 持续检测：增强 baseline 完成下一批 `8,192` 个支付对，检查点由 `41,636` 推进到 `49,828`；第八场景同期保持 `33,444`。
- 解释边界：该缓存规模已经超过旧 `788` 候选 baseline 的 `46,381` 对，但新求解使用 `1,576` 条共同候选，因此不能把跨过旧规模解释为收敛或结果改善。
- 状态：qos_low_checkpoint_33444；augmented_dynamic_checkpoint_49828；precompute_still_running

### 2026-07-17 02:48 - 第八场景完成一轮全候选扫描并继续扩张

- 持续检测：`qos_threshold_low` 依次写出 `40,300` 和 `40,301` 个支付对；随后 12 个 worker 被重新创建并保持约 100% CPU，表明全候选偏差扫描后新增响应对并进入下一轮评价。
- 边界：场景正式 JSON 尚未生成，不能把 `40,301` 解释为最终收敛；增强 baseline 同期保持 `49,828`。
- 状态：old_sensitivity_progress_7_of_8；qos_low_oracle_expansion_after_40301；augmented_dynamic_checkpoint_49828

### 2026-07-17 03:12 - 第八场景继续 oracle 扩张，增强 baseline 到 58,020 对

- 第八场景：`qos_threshold_low` 在 `40,301` 后依次写出 `41,824` 与 `43,345` 个支付对，说明新增响应后的偏差评价仍在继续。
- 增强 baseline：完成一个标准 `8,192` 对批次，由 `49,828` 推进到 `58,020`。
- 边界：两条流水线仍无最终结果文件或成功哨兵；这些数值只表示签名绑定缓存的可恢复规模。
- 状态：qos_low_checkpoint_43345；augmented_dynamic_checkpoint_58020；both_running

### 2026-07-17 03:32 - 第八场景推进到 46,381 对并继续 oracle 迭代

- 轨迹：`qos_threshold_low` 在 `43,345` 后依次写出 `44,864`、`46,380` 和 `46,381` 个支付对；完整轨迹显示每轮全候选扫描后新增一个响应并重新评价。
- 进程核对：`46,381` 后 12 个新 worker 已重新创建并满载运行，因此该数值不是结束标志。增强 baseline 同期保持 `58,020`。
- 状态：old_sensitivity_progress_7_of_8；qos_low_oracle_continues_after_46381；augmented_dynamic_checkpoint_58020

### 2026-07-17 03:56 - 第八场景继续到 49,409 对，增强 baseline 到 66,212 对

- 第八场景：`qos_threshold_low` 在 `46,381` 后完成下一轮扫描并依次写出 `47,895/47,896`、`49,408/49,409`；每个 `+1` 后均重新启动 12 个 worker，oracle 迭代仍未结束。
- 增强 baseline：完成一个 `8,192` 对批次，由 `58,020` 推进到 `66,212`。
- 边界：两个正式结果文件仍未生成，不报告均衡或经济指标。
- 状态：qos_low_oracle_continues_after_49409；augmented_dynamic_checkpoint_66212；both_running

### 2026-07-17 04:34 - 两条动态缓存继续扩张

- 第八场景：`qos_threshold_low` 由 `49,409` 继续推进到 `50,920`、`52,429` 和 `53,935` 个支付对，oracle 仍未结束。
- 增强 baseline：由 `66,212` 完成一个 `8,192` 对批次并推进到 `74,404`。
- 边界：持续检测未见正式结果文件或完成哨兵，旧数值源码保持冻结。
- 状态：qos_low_checkpoint_53935；augmented_dynamic_checkpoint_74404；both_running

### 2026-07-17 05:09 - `800/1,576` 增强 baseline 预计算完成并独立验证

- 输出：`/root/.cache/peak_shaving_uniform_expansion_baseline/precompute_result.json`，SHA-256 `a12e57db80f50a2f9293b04adaa6042ac2a393d577f26fb6828520bda532d60b`，大小约 909 KiB。预计算进程正常退出，日志错误关键字扫描无命中。
- 缓存与数值门禁：uniform 记录 `43,246` 对、full regret `2.2737e-13`、最大联合残差 `9.9739e-10`；dynamic 记录 `81,276` 对、full regret `1.1369e-13`、最大联合残差 `9.9997e-10`。两者均以 `regret_tolerance` 终止。
- 候选验证：uniform 与共同候选分别为 `800x4` 和 `1,576x4`，全体向量唯一，uniform 是严格子集；数组 SHA-256 分别为 `516080224c67b6f7ab111e69f17d2a73801a6728f16c73336893f4729cfaa5e6` 与 `01db2a6b2ef32af4413f880f3317eae0076daf79c1c381aa43d65a054ac78f4d`，与预定 contract 一致。
- 来源与概率验证：19 个记录来源哈希与当前文件全部匹配。uniform 活跃支持为 `10x10`，dynamic 为 `26x26`；报告活跃剖面数分别为 100 和 676，概率质量分别为 `1.0000000000000002` 和 `1.0`，与混合支持笛卡尔积一致。
- 检查失败与修复：首次独立 Python 检查因把 `numpy.int64` 直接传给 `json.dumps` 而退出；改为显式转换原生 `int` 后重跑返回 0。该失败只影响检查输出，不修改工件或缓存。
- 预计算比较：相对扩展 uniform 均衡，dynamic 的 aggregate peak 为 `-12.5045%`、maximum provider utilization 为 `-10.8438%`、minimum QoS 为 `+0.057405`、aggregate market-side profit 为 `+2.2329%`。这些是待正式 runner 复现的预计算值，不在当前阶段写入正文。
- 元数据边界：底层 `run_equilibria` 工件尚无正式 `candidate_design` 元数据；归档完成后由正式 submission runner 复用持久缓存、补齐构造哈希和命令 provenance，再生成正文依赖工件。
- 状态：augmented_precompute_verified；formal_runner_pending_old_archive；preliminary_metrics_withheld

### 2026-07-17 05:16 - 第八场景完成，但旧总证据门禁未通过

- 第八场景工件：`sensitivity_qos_threshold_low_submission.json`，SHA-256 `8f223eb195d960f01b8315781933593b5dddf1afe441e40859cfd203a7a3f804`，大小 638,515 bytes。20 个来源哈希与 baseline 绑定验证通过。
- 数值门禁：uniform 使用 95 个支付对、full regret 为 0、最大联合残差 `5.0697e-10`；dynamic 使用 59,206 个支付对、full regret `3.4106e-13`、relative regret `4.0019e-16`、最大联合残差 `9.9786e-10`，以 `regret_tolerance` 终止，正概率支持为 `24x24`。
- 历史比较：相对旧 12 条统一限制，aggregate peak `-11.9723%`、maximum provider utilization `-18.7302%`、minimum QoS `+0.086396`、aggregate market-side profit `-2.7679%`。这些值只进入 `pre_uniform_expansion` 历史归档，不进入扩展统一基线后的正文。
- 九场景汇总：9 行齐全，最大 dynamic full regret `6.8212e-13`，最大联合残差 `9.9997e-10`。`price_branch_queue.exit` 与 `submission_completion.exit` 都写为 0，但 `submission_evidence_gate_report.json` 的 `passed=false`，因此禁止归档。
- 后处理失败：fixed-point 和 intermediary audit 通过 heredoc 的 `<stdin>` 启动，`multiprocessing spawn` 因无法导入 `<stdin>` 失败；claims 与最终 figure builder 直接执行脚本路径，引发 `ModuleNotFoundError: No module named 'experiments'`。Bash 函数位于 `||` 条件链中，`set -e` 未在中间失败处终止，后续 132 个测试通过覆盖了函数返回值，最终误写成功哨兵。
- 当前修复命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    uv run --no-project --with numpy \
    python -m experiments.run_submission_fixed_point_audit
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 \
    uv run --no-project --with numpy --with scipy \
    python -m experiments.run_submission_intermediary_audit
  ```
- 调度：两项 676 活跃剖面审计各使用 16 workers 并行重跑。重建 claims、总门禁、结果宏和图表前等待两项均成功；总门禁 `passed=true` 前不执行归档。
- 状态：old_sensitivity_progress_8_of_8；qos_low_verified；completion_sentinel_false_positive；post_audits_rerunning；archive_blocked_by_gate

### 2026-07-17 05:28 - 旧后处理证据修复并通过总门禁

- fixed-point audit：通过模块入口重建 676 个活跃剖面，概率覆盖 `1.0000000000000002`，每剖面 32 个初始化全部收敛；最大残差 `9.9996e-10`、最大 QoS span `9.7009e-10`、最大 routing span `2.0686e-9`。工件 SHA-256 为 `170be9b447ddddf9ca5057d72a9fc3f134a8e50fc12cf2edbb6e60841020ff9b`。
- intermediary audit：通过模块入口重建 676 个活跃剖面，概率覆盖 `1.0000000000000002`；最大绝对利润改进 `0.1026781`、最大相对改进 `0.0002916833`、最大联合残差 `9.9997e-10`，381 个 optimizer run 报告成功终止。工件 SHA-256 为 `8fe58efe6e528b1d7ac89cf6fb1509db9f4d96f171478361edb599c8871a1d94`。
- 来源验证：两项工件各记录 6 个来源哈希，均与当前源码匹配。随后以 `python -m experiments.build_submission_sensitivity_claims` 生成缺失 claims。
- 总门禁：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run --no-project --with numpy --with scipy --with nashpy \
    python -m experiments.submission_evidence_gates
  ```
  返回 0，`submission_evidence_gate_report.json` 为 `passed=true`、`failures=[]`，fixed-point、intermediary、八个敏感性场景、九场景汇总和 claims 均通过。
- 派生输出：以模块入口重建 `submission_result_macros.tex` 和 5 组 PDF/PNG 图表。随后运行旧后处理测试集，结果为 `132 passed in 2.69s`。
- 状态：old_evidence_gate_passed；post_audits_rebuilt；derived_outputs_rebuilt；archive_ready

### 2026-07-17 05:29 - 旧 `pre_uniform_expansion` 证据归档完成

- 命令：
  ```bash
  bash /root/.cache/peak_shaving_submission_sensitivity/archive_pre_uniform_expansion.sh
  cd artifacts/peak_shaving/20260712_expanded_response/pre_uniform_expansion
  sha256sum -c SHA256SUMS
  ```
- 输出：`artifacts/peak_shaving/20260712_expanded_response/pre_uniform_expansion/`。归档元数据绑定旧 baseline SHA-256 `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`，归档内证据门禁为 `passed=true`、`failures=[]`。
- 完整性：`SHA256SUMS` 列出的 37 个文件全部返回 `OK`。来源联合快照包含 221 条来源记录和 33 个唯一来源，`all_recorded_hashes_match_current=true`，无不匹配项。
- 核对命令修正：首次按旧预期查找 `MANIFEST.json` 与 `SOURCE_HASH_VERIFICATION.json` 失败；归档脚本实际文件名为 `archive_metadata.json` 与 `source_hash_union_snapshot.json`。改用实际字段 `entries` 和 `all_recorded_hashes_match_current` 后验证通过。
- 决策：旧 `788/12` 历史证据已经稳定归档，数值源码解冻。后续正式工件必须使用 `800/1,576` 共同候选集，不覆盖归档目录。
- 状态：pre_uniform_expansion_archived；archive_checksums_verified；source_snapshot_verified；numerical_sources_unfrozen

### 2026-07-17 05:31 - 正式 `800/1,576` 候选设计与 runner contract 实现

- 实现：新增 `experiments/submission_candidate_design.py`，固定 12 个旧 uniform anchors、512 点二维 Latin hypercube、`9x13` 全局 lattice 和两个 `9x9` 局部 lattice；去重后的分量增量为 `[12, 512, 114, 81, 81]`，共 800 条零斜率规则。与旧动态候选超集合并后共 1,576 条规则。
- 正式 runner：continuation seed 只读取 `pre_uniform_expansion/spatiotemporal_equilibrium_submission.json`，pair cache 固定为 `~/.cache/peak_shaving_uniform_expansion_baseline`，并记录候选构造元数据及新模块来源哈希。
- 相关路径：敏感性默认缓存改为 `~/.cache/peak_shaving_submission_sensitivity`；baseline 动态离网格缓存改为 `~/.cache/peak_shaving_submission_offgrid`；branch audit 读取增强 baseline 的持久 `dynamic.pkl`。
- manifest：uniform 组件改为完整 800 条规则，seed 指向旧归档，重建使用增强候选模块，来源集合新增 `submission_candidate_design.py`。
- 验证：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run --no-project --with ruff ruff check \
    experiments/submission_candidate_design.py \
    experiments/run_submission_spatiotemporal_equilibrium.py \
    experiments/build_submission_candidate_manifest.py \
    experiments/run_submission_spatiotemporal_sensitivity.py \
    experiments/run_spatiotemporal_offgrid_diagnostic.py \
    experiments/run_submission_equilibrium_branch_audit.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run pytest -q tests/test_submission_candidate_design.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp \
    uv run pytest -q tests/test_submission_candidate_manifest.py
  ```
- 结果：Ruff 为 `All checks passed!`；候选设计 `8 passed`。manifest 为 `1 failed, 2 passed`，唯一失败是当前正式 equilibrium 工件仍为旧 788 网格，尚未与重建的 1,576 网格逐元素一致；组件计数与来源哈希已通过。
- 状态：candidate_design_green；formal_runner_ready；manifest_exact_match_pending_formal_baseline

### 2026-07-17 05:34 - 正式增强 baseline 与候选 manifest 生成并验证

- 正式工件：`spatiotemporal_equilibrium_submission.json`，SHA-256 `70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`。记录 21 个来源哈希，全部与当前文件匹配；continuation seed 绑定旧归档 SHA `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`。
- 缓存复用：uniform 加载并保留 43,246 对，dynamic 加载并保留 81,276 对，没有新增 follower 评价。dynamic 在第一轮 full-grid scan 即以 full regret `1.1369e-13` 达到容差。
- 候选与支持：uniform 为 800 条、100 个活跃剖面（`10x10`）；dynamic 为 1,576 条、676 个活跃剖面（`26x26`）。最大联合残差分别为 `9.9739e-10` 与 `9.9997e-10`。
- 正式比较：aggregate peak `-12.5045%`、maximum provider utilization `-10.8438%`、minimum QoS `+0.057405`、aggregate market-side profit `+2.2329%`。这些值已由正式 baseline 复现，但仍等待八场景、统一离网格和总门禁后写入正文。
- 预计算一致性：candidate grid、dynamic、comparison 和模型输入逐字段一致。uniform 唯一差异是 `trace.evaluated_pairs`：预计算从空缓存逐轮增长，正式重建一开始即载入完整 43,246 对；移除该缓存规模诊断字段后 uniform 对象逐字段一致。
- manifest：正式重建 1,576 条候选并与工件逐元素匹配，组件累计计数为 `800,1178,1298,1362,1389,1489,1558,1576`。候选与 manifest 合并测试为 `11 passed in 0.94s`。
- 状态：formal_augmented_baseline_verified；candidate_manifest_exact_match；formal_sensitivity_pending

### 2026-07-17 05:55 - 八场景正式重算启动并完成首个 uniform 扩张块

- 调度：两个并行队列各使用 16 workers。队列 A 为 capacity low/high 与 price-sensitivity low/high；队列 B 为 migration-cost low/high 与 QoS-threshold low/high。不同场景使用独立缓存目录和工件路径。
- runner 验证：`tests/test_submission_spatiotemporal_sensitivity.py` 为 `6 passed`。两队列启动后分别从 capacity-low 和 migration-low 的旧同场景向量缓存继续，而非从零重算。
- 首个检查点：capacity-low uniform 先写出 103 对，随后推进到 `4,863/4,864`；migration-low 先写出 96 对，随后推进到 `4,856/4,857`。该轨迹表示扩展 800 候选 uniform game 完成偏差块并各新增一个响应。
- 资源：两个队列各保持 16 个约 100% CPU 的 worker，可用内存约 8.5 GiB，未见错误或 worker 退出。
- 状态：formal_capacity_low_uniform_4864；formal_migration_low_uniform_4857；sensitivity_queues_running

### 2026-07-17 07:38 - 首批正式场景 uniform 缓存越过 30,000 对

- capacity-low：uniform double-oracle 缓存推进到 `30,112/30,113` 个支付对。
- migration-low：uniform 缓存推进到 `30,105` 个支付对；最近完整 `+1` 检查点为 `28,542/28,543`。
- 运行状态：两个场景均持续以 16 workers 运行，检查点从旧同场景缓存连续增长，未见 traceback、缓存回退或正式工件提前写出。
- 边界：仍处于 800 候选 uniform 阶段，不报告场景比较指标；场景 dynamic 阶段和其余六个场景尚待队列顺序执行。
- 状态：formal_capacity_low_uniform_30113；formal_migration_low_uniform_30105；sensitivity_queues_running

### 2026-07-17 08:55 - migration-low 完成 uniform 并进入扩展 dynamic

- migration-low uniform：最后检查点为 `42,529` 个支付对，随后阶段切换，说明 800 候选 uniform double-oracle 已结束。
- migration-low dynamic：旧归档场景的 45,624 个完整策略向量对被持久缓存精确复用；首个新增 `8,192` 对批次后写出 `53,816` 检查点。
- capacity-low：同期仍在 uniform 阶段，最近检查点为 `51,785`。不同参数场景的支持扩张轮次与最终缓存规模不同，不强行对齐。
- 运行状态：两个队列继续各使用 16 workers，未见错误；migration-low 长批次完成后正常写回并切换阶段，排除停滞判断。
- 状态：formal_migration_low_uniform_finished；formal_migration_low_dynamic_53816；formal_capacity_low_uniform_51785

### 2026-07-17 11:19 - 首批正式场景持续扩张与资源复查

- capacity-low uniform：缓存持续推进到 `81,358` 个支付对；该数值只表示已评价集合，不能据此推算 oracle 轮数或终止原因。
- migration-low dynamic：继 `53,816` 后完成两个 `8,192` 对批次，推进到 `62,008` 和 `70,200`；下一块仍在计算。
- 健康检查：两个队列各有 16 个运行态 worker，总 CPU 约 3,152%；15 GiB 内存中约 5.6 GiB 可用，swap 约 3.2 GiB 可用。未触发并行度调整。
- 状态：formal_capacity_low_uniform_81358；formal_migration_low_dynamic_70200；sensitivity_queues_healthy

### 2026-07-17 12:13 - capacity-low 进入 dynamic，migration-low dynamic 到 86,600 对

- capacity-low：uniform 最终缓存为 `81,358` 对；随后从旧同场景 dynamic 的 `75,564` 对精确复用，并完成首个 `8,192` 对增量块到 `83,756`。
- migration-low：dynamic 从 `70,200` 继续写出 `78,392`、`86,584` 和 `86,600`。`86,584` 是标准批次边界，后续 16 对表示新 oracle 支持扩张。
- 结论边界：两个首批场景均已完成 800 候选 uniform 阶段，但 dynamic 仍在运行，正式场景工件尚未生成。
- 状态：formal_capacity_low_uniform_finished；formal_capacity_low_dynamic_83756；formal_migration_low_dynamic_86600

### 2026-07-17 12:35 - 正式敏感性持续检测与后续审计准备

- 检查点：capacity-low dynamic 缓存在 12:02 更新为 445,255,569 bytes；migration-low dynamic 在 12:28 更新为 472,963,524 bytes，对应后者已越过此前的 88,176 对检查点并继续计算。正式场景工件尚未改写，因此不提前报告场景指标。
- 运行状态：两个队列各有 16 个运行态 worker，总 CPU 接近 32 核满载；可用内存约 5.6 GiB，swap 可用约 2.6 GiB。未见 worker 退出或异常输出。
- 监控清理：终止一个由早先只读错误扫描遗留、阻塞在 `/proc/1543014/fd/1` 的 `rg` 进程；该进程不属于实验队列，实验 parent/worker 未受影响。
- 后续准备：读取 uniform off-grid 与 intermediary provider-payoff 的契约测试，计划只新增与当前来源哈希隔离的候选设计和纯汇总模块；在八场景完成前不修改敏感性 runner、候选设计或数值核心文件，也不启动额外重计算。
- 状态：formal_sensitivity_queues_healthy；audit_contract_reviewed；numerical_sources_frozen_during_run

### 2026-07-17 12:38 - uniform off-grid 与 provider-payoff 审计契约实现

- 新增 `experiments/uniform_offgrid_diagnostic_tools.py`：在完整二维价格边界上组合活跃支持、每个 provider 1,024 点独立 Latin hypercube、边界守卫，并在当前最佳点周围构造有界 `17x17`、半宽 2.5% 的零斜率局部格点。
- 新增 `experiments/run_submission_uniform_offgrid_audit.py`：显式声明 baseline 加八个敏感性场景，随机种子为 20260718，持久缓存根目录为 `~/.cache/peak_shaving_uniform_offgrid`。当前只实现 runner，未与仍占满 32 核的敏感性队列并发执行。
- 新增 `experiments/build_submission_intermediary_payoff_sensitivity.py`：在完整活跃剖面矩阵上比较 stored 与 independent-global intermediary response 下的 provider payoff，报告加权有符号/绝对变化、最大剖面变化和 active-support regret；边界明确限定为活跃剖面，不冒充全 1,576 偏差审计。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run pytest -q \
    tests/test_submission_uniform_offgrid_audit.py \
    tests/test_submission_intermediary_payoff_sensitivity.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run --no-project --with ruff ruff check \
    experiments/uniform_offgrid_diagnostic_tools.py \
    experiments/run_submission_uniform_offgrid_audit.py \
    experiments/build_submission_intermediary_payoff_sensitivity.py
  ```
- 结果：契约测试 `7 passed in 93.77s`；Ruff 三个文件均为 `All checks passed!`；文件长度分别为 192、176、249 行，`git diff --check` 通过。测试耗时较长来自 `nice -n 19` 下与双 16-worker 队列共享 CPU，不是测试计算量异常。
- 状态：uniform_offgrid_contract_green；provider_payoff_contract_green；audit_execution_pending_formal_sensitivities

### 2026-07-17 13:59 - 首个正式敏感性场景验证与增强证据门迁移

- 场景完成：`sensitivity_migration_cost_low_submission.json` 于 12:48 生成，SHA-256 为 `c186d72b729031f874d23c96fc3b5a00f976b88572240e32f5f519d9307dd2a8`；B 队列随后自动进入 migration-cost-high。
- 候选与缓存：uniform/dynamic 候选数为 `800/1,576`，评价对数为 `42,529/92,116`；活跃支持为 `9x9/26x26`。
- 数值验证：uniform/dynamic full regret 为 `1.1369e-13/2.2737e-13`，最大联合 residual 为 `9.9928e-10`；20 个来源哈希全部匹配当前文件，正式 baseline SHA-256 精确匹配 `70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`。`validate_sensitivity_scenario` 返回 `passed=true`。
- 场景比较：aggregate peak `-13.0813%`、maximum provider utilization `-11.5249%`、minimum QoS `+0.060297`、aggregate market-side profit `+1.9171%`。该行只进入场景汇总候选，不单独外推。
- 门禁迁移：`GateThresholds` 改为 uniform `800`、provider `1,576`；baseline 活跃剖面数改由正概率 row/column mixes 计算。新增九场景 uniform off-grid 与 provider-payoff sensitivity 验证路径；candidate manifest 累计计数同步为 `800, 1178, 1298, 1362, 1389, 1489, 1558, 1576`。
- 初次测试：增强门禁相关测试为 `5 failed, 9 passed`。失败分为两类：uniform off-grid 合成工件不含 dynamic optimizer 专用的 `minimum_successful_local_runs`；旧 sensitivity table/claims 测试夹具仍声明 788。
- 修复与复验：uniform 门禁仅检查既定的 regret、residual、support-payoff error 和 convergence，dynamic 四维门禁继续要求 local-run；测试夹具同步到 1,576。复验命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 10 \
    uv run pytest -q \
    tests/test_submission_augmented_evidence_contract.py \
    tests/test_submission_sensitivity_table.py \
    tests/test_submission_sensitivity_claims.py
  ```
- 结果：`14 passed in 7.46s`；相关 Ruff 为 `All checks passed!`，`git diff --check` 通过。
- 状态：formal_migration_cost_low_verified；augmented_evidence_contract_green；remaining_sensitivities_running

### 2026-07-17 14:11 - 正式 baseline 宏、图表契约与论文主体迁移

- 图表后处理：`build_final_submission_figures.py` 新增九场景 uniform off-grid 与 intermediary provider-payoff 工件路径。solver-diagnostics 的 off-grid 面板区分 uniform 九场景最大 regret 和 baseline dynamic 四维 regret；门禁比值面板新增 provider-payoff fixed-point residual。framework blueprint 标签改为 `Full 1,576-candidate regret`。
- 图表契约验证：`tests/test_submission_augmented_figure_contract.py` 与 price-shape 注册测试共 `3 passed in 8.88s`，相关 Ruff 通过。图表尚未重建，因为两个新审计工件尚未运行。
- 门禁回归：把旧合成夹具的 `12/788`、manifest 累计计数和故障注入值同步到正式 `800/1,576`。首次全门禁回归为 `1 failed, 81 passed`，唯一失败是测试仍查找旧字典字面量；更新为当前三元组注册结构后定向测试通过。
- 正式宏：从当前 baseline 工件重建 `submission_result_macros.tex`，包括 peak reduction `12.50%`、maximum-utilization reduction `10.84%`、minimum QoS `0.901 -> 0.959`、market-side profit `+2.23%`、uniform/dynamic 候选 `800/1,576` 和动态评价对 `81,276`。宏回归为 `9 passed in 0.71s`。
- 论文迁移：摘要、候选构造表、finite-game 维度、uniform 混合支持、主结果表、缓存说明、审计边界和结论改用正式 baseline 与生成宏。旧 `788/12` 及 `12.32/15.70/0.890/0.959/2.81` 文本已从主 tex 清除；利润叙述修正为 provider A 下降、provider B 与 intermediary 上升、baseline market-side profit 上升。
- 论文增强契约初检：`2 failed, 11 passed`。宏单测缺少新增的 provider-B 字段，已修复并复验；剩余一个缺口是正式 `submission_sensitivity_table.tex` 与 `resolved_sensitivity.pdf` 尚未接入，必须等待全部九场景工件生成，未使用旧工件规避测试。
- 编译命令：
  ```bash
  nice -n 10 latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 0，生成 23 页 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.pdf`，文件大小 425,875 bytes；XeLaTeX/BibTeX/xdvipdfmx 全流程完成。
- 状态：formal_baseline_macros_verified；manuscript_baseline_migrated；latex_verified；sensitivity_table_and_figure_pending

### 2026-07-17 14:23 - 正式 baseline 利润方向一致性修正

- 持续检测：capacity-low dynamic 与 migration-cost-high uniform 仍在大批次计算，两个队列无错误输出；14:23 可用内存约 5.5 GiB、swap 可用约 2.7 GiB。
- 稿件检查：引言遗留了“aggregate market-side profit falls in the main case”，与正式 baseline 的 `+2.2329%` 相反；正文结果表、解释与结论已经使用正式上升方向。
- 操作：将引言改为 `rises in the main case`，并在 `test_submission_augmented_manuscript_contract.py` 增加旧下降表述不得出现的回归断言。
- 边界：价格形状分解表仍绑定旧 equilibrium SHA-256，相关分量不根据新 baseline 手工推算；等待正式分解工件重建后统一替换。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run pytest -q \
    tests/test_submission_augmented_manuscript_contract.py::test_manuscript_removes_provisional_old_comparison_values
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run --no-project --with ruff ruff check \
    tests/test_submission_augmented_manuscript_contract.py
  git diff --check -- \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex \
    tests/test_submission_augmented_manuscript_contract.py README.md
  ```
- 验证结果：定向稿件契约 `1 passed in 2.29s`；Ruff `All checks passed!`；`git diff --check` 退出码 0。
- 新检查点：migration-cost-high uniform 于 14:23 写回 `23,062` 对；capacity-low dynamic 仍在同一大批次，无异常输出。
- 状态：baseline_profit_direction_consistent；price_shape_refresh_pending；formal_migration_cost_high_uniform_23062

### 2026-07-17 14:28 - 当前提交材料迁移到 800/1,576 正式范围

- 目标：清除当前提交材料中仍指向旧 `12/788` 设计、`12.32%` 峰值变化和 `-2.81%` 利润变化的内容；带有明确历史状态的审稿记录保持不变。
- 操作：更新 `ARTIFACT_MANIFEST.md` 与 `REPRODUCIBILITY.md`，记录完整 800-rule uniform 子集、1,576-rule common set、100/676 活跃剖面及新增的九场景 uniform off-grid/provider-payoff 审计；旧 SHA 绑定的审计明确标为待 provenance rebuild。
- 提交材料：`simpat_highlights_final_2026-07-16.txt` 改为正式 baseline 的 `12.50%` peak reduction、`+2.23%` market-side profit，并移除旧 price-shape 百分比；作者检查单同步候选范围与实际 Highlights 文件名。
- 回归保护：增强证据契约新增当前提交文档范围、baseline 数值及 Highlights 每行不超过 85 字符的断言。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run pytest -q \
    tests/test_submission_augmented_evidence_contract.py::test_current_submission_docs_use_augmented_scope_and_baseline_results
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run --no-project --with ruff ruff check \
    tests/test_submission_augmented_evidence_contract.py
  awk 'length($0)>85 {print NR ":" length($0) ":" $0; bad=1} END {exit bad}' \
    docs/submission/simpat_highlights_final_2026-07-16.txt
  git diff --check -- ARTIFACT_MANIFEST.md REPRODUCIBILITY.md \
    docs/submission/simpat_highlights_final_2026-07-16.txt \
    docs/submission/smpt_author_actions_2026-07-16.md \
    tests/test_submission_augmented_evidence_contract.py README.md
  ```
- 验证结果：定向契约 `1 passed in 3.88s`；Ruff `All checks passed!`；Highlights 行长与 `git diff --check` 均退出码 0。
- 运行进展：capacity-low dynamic 于 14:29 写回 `108,332` 对，缓存增至 575,909,562 bytes；两队列随后继续保持 16-worker 计算。
- 状态：submission_docs_augmented_scope_verified；formal_capacity_low_dynamic_108332

### 2026-07-17 14:32 - 旧终审测试迁移到正式候选与审计契约

- 操作：`test_final_submission_figures.py` 的正式候选数改为 1,576，并把 `uniform_offgrid`、`provider_payoff_sensitivity` 纳入图表输入集合；framework 期望标签改为 `Full 1,576-candidate regret`。
- 稿件契约：有限博弈维度改为 1,576，敏感性边界改查九场景 uniform-price off-grid、baseline 四维 off-grid 与 common finite rule set。
- 保留项：`test_submission_candidate_design.py` 中旧动态候选集合的 `(788, 4)` 夹具描述候选并集的历史组成，仍是构造 1,576 最终集合的有效输入，不做修改。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run pytest -q \
    tests/test_final_manuscript_20260714.py::test_finite_game_simplex_and_unit_vectors_are_defined \
    tests/test_final_manuscript_20260714.py::test_sensitivity_equilibria_remain_conditional_on_common_candidate_set \
    tests/test_submission_augmented_figure_contract.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run --no-project --with ruff ruff check \
    tests/test_final_submission_figures.py \
    tests/test_final_framework_drawio.py \
    tests/test_final_manuscript_20260714.py
  git diff --check -- tests/test_final_submission_figures.py \
    tests/test_final_framework_drawio.py \
    tests/test_final_manuscript_20260714.py README.md
  ```
- 验证结果：定向稿件与增强图形契约 `4 passed in 0.84s`；Ruff `All checks passed!`；`git diff --check` 退出码 0。依赖新审计工件的完整 figure 测试留待工件重建后执行。
- 新检查点：migration-cost-high uniform 于 14:33 写回 `25,416` 对；capacity-low dynamic 继续计算 108,332 后的新批次。
- 状态：legacy_final_tests_scope_verified；formal_migration_cost_high_uniform_25416

### 2026-07-17 14:35 - 终审稿件测试移除旧主结果硬编码

- 操作：把旧 `12.32/15.70/0.890/0.959/2.81` 从“必须存在”改为“必须不存在”，并要求主稿输入 `submission_result_macros.tex`。
- QoS 契约：期望曲线与剖面级最低值改为检查正式 uniform 起点和 `DynamicMinimumQoS` 生成宏，保留“取期望与取极值不交换”的表述检查。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run pytest -q \
    tests/test_final_manuscript_20260714.py::test_submission_text_has_no_result_placeholders_or_stale_main_values \
    tests/test_final_manuscript_20260714.py::test_mixed_qos_extrema_are_not_conflated_after_rounding
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run --no-project --with ruff ruff check \
    tests/test_final_manuscript_20260714.py
  git diff --check -- tests/test_final_manuscript_20260714.py README.md
  ```
- 验证结果：定向测试 `2 passed in 8.21s`；Ruff `All checks passed!`；diff 检查退出码 0。
- 状态：manuscript_result_contract_macro_bound_verified

### 2026-07-17 14:38 - 完整稿件契约初检与失败分流

- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 19 \
    uv run pytest -q tests/test_final_manuscript_20260714.py
  ```
- 结果：`8 failed, 45 passed in 7.94s`，退出码 1。
- 正式工件待办：2 项失败来自 `submission_sensitivity_table.tex`/`resolved_sensitivity.pdf` 尚未生成与接入；1 项来自机制和 price-shape 工件仍绑定旧 baseline SHA-256。
- 测试迁移待办：其余失败来自旧的 676 剖面措辞、理论审计 `3/8` 断言、主结果手写字面量、uniform 纯策略假设，以及 restricted-shape LaTeX 字符串位置错误。
- 决策：敏感性与依赖审计失败保持红色；迁移其余测试，并扩展结果宏覆盖主表剩余手写字段。
- 状态：full_manuscript_contract_red_expected；five_legacy_assertions_to_migrate

### 2026-07-17 14:47 - 主结果表完整宏绑定与稿件契约收敛

- TDD 红灯：先扩展 `test_submission_result_macros.py`，要求峰均比、移动比例变化、provider A/B 与 intermediary 利润及变化率均由宏生成；首次定向测试为 `1 failed in 4.34s`，缺少 `UniformPeakToAverage`。
- 实现：`build_submission_result_macros.py` 新增上述机器派生宏，主结果表移除 `1.637/1.432/0.0137/844.748/835.666/320.483/345.410` 及三项利润变化率的手写值。baseline-only 宏通过 `build_macros(equilibrium)` 显式生成；旧 SHA dependent audits 未被载入。
- 终审测试迁移：uniform 由旧纯策略假设改为核对 `10x10` 正概率支持及加权系数均值；动态审计改核对正式 full regret/evaluated pairs；combined 机制值改由正式 baseline 宏引用；restricted shape 与审计覆盖措辞同步当前正文。
- 中间复验：宏及六项稿件契约为 `2 failed, 13 passed`；失败来自零系数格式 `0`/`0.0000` 与 combined 值改用宏后的旧字面量断言。修正格式化和宏断言后，两项定向复验 `2 passed in 15.68s`。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 19 \
    uv run pytest -q tests/test_submission_result_macros.py \
    tests/test_final_manuscript_20260714.py::test_numerical_audit_coverage_boundary_is_explicit \
    tests/test_final_manuscript_20260714.py::test_theory_audit_matches_the_partial_payoff_and_sensitivity_status \
    tests/test_final_manuscript_20260714.py::test_main_result_table_matches_the_submission_equilibrium_artifact \
    tests/test_final_manuscript_20260714.py::test_strategy_support_and_solver_trace_match_the_equilibrium_artifact \
    tests/test_final_manuscript_20260714.py::test_demand_and_numerical_audit_prose_matches_artifacts \
    tests/test_final_manuscript_20260714.py::test_mechanism_and_price_shape_prose_matches_artifacts
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 19 \
    uv run pytest -q tests/test_final_manuscript_20260714.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 19 \
    latexmk -xelatex -interaction=nonstopmode -halt-on-error \
    peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 验证结果：宏与迁移契约最终定向复验通过；完整稿件契约由 `8 failed, 45 passed` 收敛到 `2 failed, 51 passed in 0.50s`，仅剩正式敏感性表和 Figure 6 未接入；Ruff 与 diff 检查通过。XeLaTeX 退出码 0，23 页 PDF 为 425,864 bytes。
- 运行进展：migration-cost-high uniform 于 14:43 写回 `27,766` 对；capacity-low dynamic 继续计算 108,332 后的下一批，32 个 worker 健康。
- 状态：main_table_fully_macro_bound；latex_verified；only_sensitivity_integration_tests_red

### 2026-07-17 14:49 - 终审 Highlights 门禁切换到实际提交文件

- 操作：`test_final_manuscript_20260714.py` 的 `HIGHLIGHTS` 路径由旧的根目录草稿切换到 `docs/submission/simpat_highlights_final_2026-07-16.txt`，确保 3--5 条与每条 85 字符门禁检查实际上传文件。
- 运行进展：migration-cost-high uniform 于 14:47 写回 `28,550` 对；capacity-low dynamic 继续 108,332 后的大批次。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 19 \
    uv run pytest -q \
    tests/test_final_manuscript_20260714.py::test_abstract_keywords_and_highlights_meet_smpt_limits
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp nice -n 19 \
    uv run --no-project --with ruff ruff check \
    tests/test_final_manuscript_20260714.py
  git diff --check -- tests/test_final_manuscript_20260714.py README.md
  ```
- 验证结果：实际提交 Highlights 门禁 `1 passed in 12.81s`；Ruff 与 diff 检查通过。
- 状态：final_highlights_gate_path_verified

### 2026-07-17 15:00 - 正式敏感性队列持续检测

- Queue A：capacity-low dynamic 维持 `108,332` 对后的下一大批次，16 workers 的 CPU 合计约 1,565%，无异常输出。
- Queue B：migration-cost-high uniform 从 `28,550` 继续写回到 `30,113` 和 `31,673` 对，缓存于 15:00 增至 168,358,620 bytes；支持扩张与偏差扫描持续推进。
- 资源：两组各 17 个子进程，系统可用内存约 5.2 GiB、swap 可用约 2.7 GiB，未调整并行度。
- 状态：formal_capacity_low_dynamic_running；formal_migration_cost_high_uniform_31673；sensitivity_queues_healthy

### 2026-07-17 15:49 - 两场景继续支持扩张

- capacity-low dynamic：从 `116,540` 依次推进到 `117,328`、`118,904` 和 `120,480` 对；后两轮各新增完整的 1,576 对候选规模扫描，随后均继续重建 16-worker 池，尚未满足停止条件。
- migration-cost-high uniform：从 `31,673` 继续推进到 `44,078` 对，多次出现支持扩张后的 `+1` 检查点；尚未切换 dynamic。
- 健康状态：两组各 17 个子进程，CPU 合计持续接近 32 核满载；可用内存约 4.9 GiB、swap 可用约 2.7 GiB，无错误输出或新正式场景工件。
- 状态：formal_capacity_low_dynamic_120480；formal_migration_cost_high_uniform_44078；sensitivity_queues_healthy

### 2026-07-17 16:41 - migration-cost-high 进入 dynamic

- Queue B：migration-cost-high uniform 最终缓存为 `44,078` 对；随后复用/扩张 dynamic 缓存并写回 `49,254` 对，正式场景仍在运行。
- Queue A：capacity-low dynamic 从 `120,480` 继续按 1,576 对整轮扫描推进到 `129,936` 对，仍未满足终止条件。
- 进程复核：Queue A 在 worker 池切换瞬间短暂显示 46 个子进程；20 秒后恢复为两组各 17 个子进程，CPU 合计约 31 核，确认不是进程泄漏。
- 资源：可用内存约 4.8 GiB、swap 可用约 2.7 GiB；无错误输出，新正式场景工件尚未生成。
- 状态：formal_capacity_low_dynamic_129936；formal_migration_cost_high_uniform_finished；formal_migration_cost_high_dynamic_49254

### 2026-07-17 17:00 - 两项 dynamic 敏感性持续运行

- capacity-low dynamic：从 `129,936` 继续按 1,576 对整轮扫描推进到 `133,088` 对，worker 池每轮正常重建，正式场景工件仍未改写。
- migration-cost-high dynamic：uniform 已固定为 `44,078` 对；dynamic 当前在 `49,254` 对后的大批次中持续运行。
- 健康状态：两组各 17 个子进程、CPU 接近 32 核满载；可用内存约 4.8 GiB、swap 可用约 2.7 GiB，无错误输出。
- 状态：formal_capacity_low_dynamic_133088；formal_migration_cost_high_dynamic_49254；sensitivity_queues_healthy

### 2026-07-17 17:26 - 投稿证据映射迁移到 800/1,576 正式基线

- 目标：避免 `smpt_submission_evidence_map_2026-07-14.md` 继续把旧 12/788 候选和 SHA-256 `d3717445...aae2f` 描述为当前投稿事实源。
- 操作：将基准切换到 SHA-256 `70a3b640...ed226`，同步 800/1,576 候选、10-by-10/26-by-26 支持、43,246/81,276 个评价对及正式主结果；把仍绑定旧基准的 off-grid、固定点、中间商、分支、机制、价格形状和分布工件标为待重建。
- 敏感性状态：只把已通过正式门禁的 `migration_cost_low` 记为当前证据；其统一/动态评价对为 42,529/92,116，峰值、最大利用率、最低 QoS 和市场侧利润变化分别为 `-13.0813%/-11.5249%/+0.0603/+1.9171%`。其余 7 个场景仍为运行中或排队。
- 运行进展：Queue B 于 17:21 写回 `migration_cost_high` dynamic 的 57,446 对检查点；Queue A 于 17:18 更新 `capacity_low` dynamic 缓存。按上一检查点和每轮 1,576 对增量推算为 136,240 对，但对应终端行已被消费，因此该数只作运行监测，不作正式证据。
- 校验命令：
  ```bash
  sha256sum \
    artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_equilibrium_submission.json \
    artifacts/peak_shaving/20260712_expanded_response/sensitivity_migration_cost_low_submission.json
  jq '{baseline_sha:.metadata.baseline_equilibrium.sha256, uniform_pairs:.uniform.evaluated_pairs, dynamic_pairs:.dynamic.evaluated_pairs, comparison:.comparison}' \
    artifacts/peak_shaving/20260712_expanded_response/sensitivity_migration_cost_low_submission.json
  rg -n '12-candidate|当前 `uniform` 仅|complete `788\^2`|d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f' \
    docs/reviews/smpt_submission_evidence_map_2026-07-14.md
  awk '/[[:blank:]]$/ {print NR ":" $0}' \
    docs/reviews/smpt_submission_evidence_map_2026-07-14.md
  ```
- 验证结果：两个正式工件的实际 SHA-256 分别为 `70a3b640...ed226` 与 `c186d72b...dd2a8`；结构化字段与文档更新值一致；旧正式基线字面量、旧 12-candidate 描述、`788^2` 表述和行尾空白均未检出。
- 回归保护：`test_current_evidence_map_uses_augmented_baseline_and_sensitivity_status` 固定新基线 SHA、800/1,576 候选范围、`migration_cost_low` 的 1/8 正式状态，并禁止旧 12-candidate 现状措辞；定向测试 `1 passed in 3.46s`，Ruff 为 `All checks passed!`。
- 失败记录：首次 `rg` 复核把含 Markdown 反引号的表达式放在双引号中，shell 尝试执行 `uniform` 与 `788^2` 并返回两条 `command not found`；该命令为只读且未改动文件，随后改用单引号复核通过。
- 下一步：继续监测两条敏感性队列；每个场景重写后立即校验基准 SHA、来源哈希、候选数、regret、残差、支持与比较算术。
- 状态：evidence_map_augmented_baseline_synced；formal_sensitivity_1_of_8_verified；sensitivity_queues_healthy

### 2026-07-17 17:34 - Manifest 与理论审计移除旧阶段现状

- 目标：修复 `ARTIFACT_MANIFEST.md` 顶部仍把 `d3717445...aae2f` 和 3/8 敏感性写成当前状态、理论一致性审计仍把 788/12 与旧 6/8 写成当前状态的问题。
- TDD 红灯：先扩展当前提交文档与理论审计契约；首次运行按预期为 `2 failed in 16.39s`，分别缺少新 baseline SHA 和新敏感性状态。
- 实现：Manifest 改为 SHA-256 `70a3b640...ed226`、新阶段 1/8、当前 Highlights 路径和两个保留红灯；理论审计改为 800/1,576 正式基准、`migration_cost_low` 已验证、其余 7 个运行或排队，并把旧基准 off-grid、分支、固定点、中间商和分布审计明确标为待重建。
- 中间复验：理论审计契约通过；Manifest 断言因目标短语跨 Markdown 换行而失败，结果为 `1 failed, 1 passed in 4.33s`。将断言改为两个稳定片段后复验通过。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 19 \
    uv run pytest -q \
    tests/test_submission_augmented_evidence_contract.py::test_current_submission_docs_use_augmented_scope_and_baseline_results \
    tests/test_final_manuscript_20260714.py::test_theory_audit_matches_the_partial_payoff_and_sensitivity_status
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 19 \
    uv run --no-project --with ruff ruff check \
    tests/test_submission_augmented_evidence_contract.py \
    tests/test_final_manuscript_20260714.py
  git diff --check -- ARTIFACT_MANIFEST.md README.md \
    tests/test_submission_augmented_evidence_contract.py \
    tests/test_final_manuscript_20260714.py
  ```
- 验证结果：最终定向测试 `2 passed in 3.78s`；Ruff `All checks passed!`；diff 和理论审计行尾空白检查通过。
- 完整契约尝试：随后以 `timeout 60s nice -n 19 uv run pytest -q tests/test_submission_augmented_evidence_contract.py` 运行整个增强证据契约；在两个 16-worker 队列占满 CPU 时未产生测试输出并以退出码 124 超时。该结果不视为通过或断言失败；定向文档契约仍为绿色，完整文件待敏感性队列释放核心后重跑。
- 运行进展：两条敏感性队列仍各有 17 个子进程；A 保持 137,816 对后的下一轮，B 保持 57,446 对后的大批次，无错误输出。
- 状态：artifact_manifest_current；theory_audit_current；documentation_contract_verified；sensitivity_queues_healthy

### 2026-07-17 18:00 - 正式敏感性小时状态

- Queue A：`capacity_low` dynamic 从 137,816 继续完成 139,392、140,968 和 142,544 对检查点；每轮均完整增加 1,576，随后正常重建 16-worker 池，尚未满足停止条件。
- Queue B：`migration_cost_high` dynamic 保持 57,446 对后的长批次，16 个 worker 持续高 CPU，无错误输出或正式工件改写。
- 正式证据：仍只有 `migration_cost_low` 通过新 800/1,576 基线门禁，进度为 1/8；未用缓存中间状态推断跨场景结论。
- 文档：当前 evidence map、Artifact Manifest 和理论一致性审计已统一到 SHA-256 `70a3b640...ed226` 与 1/8 状态，定向契约通过；旧基准只作为 continuation seed 或历史工件出现。
- 验证限制：完整 `tests/test_submission_augmented_evidence_contract.py` 在 `nice -n 19` 下因 32 核满载于 60 秒超时，退出码 124；未发现残留 pytest 进程，待数值队列释放核心后重跑。
- 资源：两组各 17 个子进程；最近可用内存约 4.5 GiB、swap 可用约 2.7 GiB；敏感性缓存约 3.9 GiB，根文件系统可用约 458 GiB。
- 下一步：继续等待场景终止或缓存写回；场景工件一旦改写，立即执行 baseline SHA、20 个来源哈希、800/1,576 候选、regret、residual、support、demand 与 comparison 算术验证。
- 状态：formal_capacity_low_dynamic_142544；formal_migration_cost_high_dynamic_57446；formal_sensitivity_1_of_8_verified；sensitivity_queues_healthy

### 2026-07-17 18:59 - capacity-low 正式通过并切换 capacity-high

- 场景完成：Queue A 在 dynamic 缓存依次推进到 144,120、145,696、147,272、148,848、150,424、152,000、152,788 和 153,576 对后，输出 `finished capacity_low: regret=1.137e-13, peak=-13.36%`；正式工件于 18:57:01 改写。
- 工件：`sensitivity_capacity_low_submission.json` 的 SHA-256 为 `42ba10d78be4ff65e04c4a3996dca21fc62c6bf61c49484bc240e8c57ac5cf5b`，记录的 baseline SHA-256 精确匹配 `70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`。
- 候选与求解：uniform/dynamic 为 800/1,576 候选、81,358/153,576 个评价对、18-by-18/15-by-15 正概率支持；full regret 为 `3.4106e-13/1.1369e-13`，dynamic relative regret 为 `1.2034e-16`，最大联合 residual 为 `9.9930e-10`，两场需求均为 1,100。
- 场景比较：aggregate peak `-13.3577%`、maximum provider utilization `-10.9106%`、minimum QoS `+0.066191`、aggregate market-side profit `-9.1390%`。与 `migration_cost_low` 的利润正向结果不同，因此当前两场已说明利润方向不能提前概括为一致。
- 正式门禁命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 \
    uv run python -c "import hashlib,json; from pathlib import Path; from experiments.submission_evidence_gates import validate_sensitivity_scenario; root=Path('.'); out=root/'artifacts/peak_shaving/20260712_expanded_response'; baseline_path=out/'spatiotemporal_equilibrium_submission.json'; artifact_path=out/'sensitivity_capacity_low_submission.json'; baseline=json.loads(baseline_path.read_text()); artifact=json.loads(artifact_path.read_text()); expected_hash=hashlib.sha256(baseline_path.read_bytes()).hexdigest(); print(json.dumps(validate_sensitivity_scenario('capacity_low', artifact, expected_hash=expected_hash, expected_baseline=baseline), indent=2))"
  ```
- 门禁结果：退出码 0，`passed=true`；20/20 来源哈希匹配，uniform/dynamic accounting、profile、support、regret、residual、需求守恒和 comparison 算术全部通过；活跃剖面数为 324/225。
- 队列接续：Queue A 自动进入 `capacity_high`，已写回 uniform `71` 对并启动 16-worker 批次；Queue B 保持 `migration_cost_high` dynamic 73,830 对后的批次。
- 文档同步：evidence map、Artifact Manifest 与理论一致性审计更新为正式 2/8；相应回归契约同步要求 `migration_cost_low`、`capacity_low` 和其余 6 场状态。
- 文档验证：三个定向契约 `3 passed in 2.07s`，Ruff `All checks passed!`；tracked diff 与两份 untracked 审计文档的行尾空白检查通过。
- 下一步：继续监测 `capacity_high` 与 `migration_cost_high`；CPU 释放后复验文档回归契约。
- 状态：formal_capacity_low_verified；formal_sensitivity_2_of_8_verified；formal_capacity_high_uniform_71；formal_migration_cost_high_dynamic_73830

### 2026-07-17 19:30 - 新场景续算与 worker 池瞬时重叠

- Queue A：`capacity_high` uniform 从 71 对推进到 4,831、5,628、5,629、7,220、7,221、8,799 和 8,800 对；小幅 `+1` 检查点来自支持扩张后的新增配对补齐。
- Queue B：`migration_cost_high` dynamic 从 73,830 推进到 82,022 和 82,038 对；后一个 `+16` 检查点同样发生在支持扩张后。
- 瞬时资源峰值：B 连续写回后短暂保留 54 个子进程，与 A 的 17 个子进程叠加；可用内存最低约 1.1 GiB。未主动终止进程，继续观察 30 秒后 B 自动恢复为 17 个子进程。
- 恢复验证：A/B 子进程 RSS 合计约 791/1,222 MiB，可用内存回升至约 4.8 GiB；swap 使用量由约 1.3 GiB 短暂增至 1.4 GiB，但 `vmstat 1 3` 后两次采样均为 `si=0, so=0`，没有持续换页或 OOM 信号。
- 决策：保持每队列 16 workers，不中断已持久化续算；继续监测下一次池切换，若可用内存持续低于 512 MiB 或进程数继续增长再采取保护措施。
- 状态：formal_capacity_high_uniform_8800；formal_migration_cost_high_dynamic_82038；worker_pool_overlap_recovered；sensitivity_queues_healthy

### 2026-07-17 19:36 - migration-cost-high 正式通过并切换 qos-threshold-low

- 场景完成：Queue B 在 dynamic 缓存从 82,038 补齐到 82,826 对后输出 `finished migration_cost_high: regret=2.274e-13, peak=-12.00%`；正式工件于 19:34:37 改写。
- 工件：`sensitivity_migration_cost_high_submission.json` 的 SHA-256 为 `b79656ec996e727bbe8242c39c9b7152a4246884b3255c2e933a7749b5247200`，记录的 baseline SHA-256 精确匹配 `70a3b640...ed226`。
- 候选与求解：uniform/dynamic 为 800/1,576 候选、44,078/82,826 个评价对、10-by-10/26-by-26 正概率支持；两场 full regret 均为 `2.2737e-13`，dynamic relative regret 为 `2.7119e-16`，最大联合 residual 为 `9.9974e-10`，需求守恒为 1,100。
- 场景比较：aggregate peak `-12.0043%`、maximum provider utilization `-10.5939%`、minimum QoS `+0.055292`、aggregate market-side profit `+2.1446%`。
- 正式门禁命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 \
    uv run python -c "import hashlib,json; from pathlib import Path; from experiments.submission_evidence_gates import validate_sensitivity_scenario; out=Path('artifacts/peak_shaving/20260712_expanded_response'); baseline_path=out/'spatiotemporal_equilibrium_submission.json'; artifact_path=out/'sensitivity_migration_cost_high_submission.json'; baseline=json.loads(baseline_path.read_text()); artifact=json.loads(artifact_path.read_text()); expected_hash=hashlib.sha256(baseline_path.read_bytes()).hexdigest(); print(json.dumps(validate_sensitivity_scenario('migration_cost_high', artifact, expected_hash=expected_hash, expected_baseline=baseline), indent=2))"
  ```
- 门禁结果：退出码 0，`passed=true`；20/20 来源哈希匹配，uniform/dynamic accounting、profile、support、regret、residual、需求守恒和 comparison 算术全部通过；活跃剖面数为 100/676。
- 队列接续：Queue B 自动进入 `qos_threshold_low`，uniform 初始检查点为 103 对；Queue A 的 `capacity_high` uniform 已推进到 10,388 对并继续运行。
- 文档同步：evidence map、Artifact Manifest 与理论一致性审计更新为正式 3/8；回归契约同步要求三项已验证场景与其余 5 场状态。
- 文档验证：三个定向契约 `3 passed in 0.43s`，Ruff `All checks passed!`；tracked diff 与两份审计文档的行尾空白检查通过。
- 下一步：验证文档契约后继续监测 `capacity_high` 与 `qos_threshold_low`。
- 状态：formal_migration_cost_high_verified；formal_sensitivity_3_of_8_verified；formal_capacity_high_uniform_10388；formal_qos_threshold_low_uniform_103

### 2026-07-17 20:00 - 正式敏感性小时状态

- 正式进度：`migration_cost_low`、`capacity_low` 与 `migration_cost_high` 已通过新 800/1,576 基线门禁，当前为 3/8；其余 5 个场景尚未完成，不报告跨场景稳健性。
- Queue A：`capacity_high` uniform 从 10,388 依次推进到 11,973、11,974、13,557、13,558、15,139、15,140、16,719、17,508 和 17,509 对，支持扩张与偏差扫描持续运行。
- Queue B：`qos_threshold_low` uniform 从 103 进入首批 4,863/4,864 对，随后推进到 6,456/6,457 对；旧阶段 dynamic 缓存保留，等待 uniform 完成后续接。
- 资源：两组各 17 个子进程；此前 B 的 54 子进程池重叠未复发。最近可用内存约 5.0 GiB、swap 可用约 2.6 GiB，未见持续换页。
- 文档与验证：3/8 状态已同步到 evidence map、Artifact Manifest、理论一致性审计和回归契约；三个定向契约与 Ruff 已通过。完整增强证据契约仍待 CPU 释放后重跑。
- 下一步：继续监测 `capacity_high` 与 `qos_threshold_low`；任一场景完成后立即执行正式门禁并同步状态。
- 状态：formal_sensitivity_3_of_8_verified；formal_capacity_high_uniform_17509；formal_qos_threshold_low_uniform_6457；sensitivity_queues_healthy

### 2026-07-17 21:00 - 正式敏感性小时状态

- 正式进度：仍为 3/8；`capacity_high` 与 `qos_threshold_low` 正在运行，另外三个场景排队。
- Queue A：`capacity_high` uniform 从 17,509 继续推进到 19,083、19,871 和 20,658 对；20:08 后进入较大的评价批次，16 个 worker 持续高 CPU，尚未写回下一检查点。
- 21:00 后阶段确认：上述长批次完成了 uniform 求解，A 随后复用旧阶段 dynamic 缓存并写回 74,111 对；`capacity_high` 已进入 dynamic，但整个场景尚未完成。
- Queue B：`qos_threshold_low` uniform 从 6,457 继续推进到 8,047、8,048、9,636、9,637、11,223、11,224、12,808、12,809、14,391、14,392、15,972、15,973、17,551、18,340、18,341、19,916 和 19,917 对。
- 健康状态：两组各 17 个子进程，未复发 worker 池长时间重叠；最近可用内存约 3.7 GiB、swap 可用约 2.7 GiB，无错误输出或持续换页。
- 决策：A 当前轮次较长但所有 worker 持续计算，不中断；继续等待实际检查点或场景完成。
- 状态：formal_sensitivity_3_of_8_verified；formal_capacity_high_uniform_20658_finished；formal_capacity_high_dynamic_74111；formal_qos_threshold_low_uniform_21491；sensitivity_queues_healthy

### 2026-07-17 22:00 - 正式敏感性小时状态

- 正式进度：仍为 3/8；`capacity_high` 与 `qos_threshold_low` 正在运行，其余 3 个场景继续排队，未将旧日期同名工件计入正式证据。
- Queue A：`capacity_high` 已完成 uniform 阶段；dynamic 在 21:43 将检查点从 74,111 推进到 82,303 对，单批新增 8,192 对，随后继续下一批计算。
- Queue B：`qos_threshold_low` uniform 从 21,491 依次推进到 23,062、23,063、24,632、24,633、26,200、26,201、27,766、28,548、28,549、30,111、30,112、31,672、31,673、33,231、33,232、34,788、35,566 和 35,567 对。
- 健康状态：两组均保持 17 个子进程；最近 worker 合计 CPU 各约 1,550%，可用内存约 3.7 GiB。监测到少量瞬时 swap-in，但复核未出现持续 swap-out、进程退出或错误输出。
- 决策：不启动会争抢 CPU 的完整测试和后续审计，也不改动敏感性来源哈希覆盖的求解源码；继续等待实际检查点或场景完成。
- 下一步：任一场景工件改写后，立即执行 baseline SHA、20 个来源哈希、800/1,576 候选、regret、residual、support、demand 和 comparison 算术门禁。
- 状态：formal_sensitivity_3_of_8_verified；formal_capacity_high_dynamic_82303；formal_qos_threshold_low_uniform_35567；sensitivity_queues_healthy

### 2026-07-17 23:00 - 正式敏感性小时状态

- 正式进度：仍为 3/8；`capacity_high` 与 `qos_threshold_low` 持续运行，其余 3 个场景排队，尚无新的正式场景工件改写。
- Queue A：`capacity_high` dynamic 在 22:29 将检查点从 82,303 推进到 90,495 对，再次完整新增 8,192 对；随后继续下一批计算。
- Queue B：`qos_threshold_low` uniform 从 35,567 依次推进到 37,120、37,121、38,672、39,447、39,448、40,996、40,997、42,543、42,544、44,088、44,089、45,631、46,402、46,403、47,942、48,712、49,482 和 50,252 对；截至 23:00，旧 dynamic 缓存的修改时间仍未变化，不能认定阶段已切换。
- Worker 池：B 在 22:43 和 22:52 两次短暂只剩 resource tracker，均在约 15 秒内自动恢复为 16 个 worker 加 tracker；没有出现持续进程增长或阶段失败。
- 资源：两组均保持 17 个子进程，worker 合计 CPU 各约 1,550%；最近可用内存约 3.2 GiB。监测到零星少量 swap-in，但没有持续 swap-out 或 OOM 信号。
- 决策：保持两队现有 16-worker 配置并继续续算；不运行会争抢 CPU 的完整测试或后续审计。
- 下一步：场景工件一旦改写，立即执行正式门禁并同步 evidence map、Artifact Manifest、理论一致性审计和回归契约。
- 状态：formal_sensitivity_3_of_8_verified；formal_capacity_high_dynamic_90495；formal_qos_threshold_low_uniform_50252；sensitivity_queues_healthy

### 2026-07-18 00:00 - 正式敏感性小时状态

- 正式进度：仍为 3/8；`capacity_high` 与 `qos_threshold_low` 正在运行，其余 3 个场景排队，尚无新的正式场景工件改写。
- Queue A：`capacity_high` dynamic 在 23:16 将检查点从 90,495 推进到 98,687 对，单批新增 8,192 对；随后继续下一批计算。
- Queue B：`qos_threshold_low` uniform 最终于 50,252 对结束；23:47 后切入 dynamic 并复用已有缓存，首个新检查点为 67,398 对。该场景尚未完成，不能提前计入正式证据。
- 健康状态：两组均保持 17 个子进程，worker 合计 CPU 各约 1,545%；最近可用内存约 3.3 GiB。Swap 使用量有波动，但连续采样 `si=0, so=0`，未见持续换页、进程退出或错误输出。
- 决策：继续保持两队 16-worker 续算；仅更新实验记录，不运行完整测试或后续审计。
- 下一步：继续监测 A/B dynamic；任一正式场景工件改写后立即执行 baseline SHA、来源哈希、候选规模、regret、residual、support、demand 和 comparison 门禁。
- 状态：formal_sensitivity_3_of_8_verified；formal_capacity_high_dynamic_98687；formal_qos_threshold_low_uniform_50252_finished；formal_qos_threshold_low_dynamic_67398；sensitivity_queues_healthy

### 2026-07-18 01:00 - 正式敏感性小时状态

- 正式进度：仍为 3/8；`capacity_high` 与 `qos_threshold_low` 仍在 dynamic 阶段运行，其余 3 个场景排队，尚无新的正式场景工件改写。
- Queue A：`capacity_high` dynamic 从 98,687 依次推进到 106,879、106,895、107,683、109,259、110,835、112,411、113,987 和 115,563 对；其中 `+16` 和 `+788` 检查点来自支持扩张后的补齐批次。
- Queue B：`qos_threshold_low` dynamic 从 67,398 推进到 75,590 对；随后继续下一批长批次计算，尚未写回新的 cache。
- 监控命令：会话轮询 `71703`/`53295`，并使用 `stat -c '%y %s %n' ...`、`ps --ppid ...`、`free -m` 和 `vmstat 1 3` 复核 cache、worker 数、内存和换页状态。
- 健康状态：两组均保持 17 个子进程；最近可用内存约 2.4 GiB。`vmstat` 实时样本显示 swap-out 持续为 0，仅有低速瞬时 swap-in，未见 OOM、进程退出或错误输出。
- 决策：继续保持两队 16-worker 续算；不启动会争抢 CPU/IO 的完整测试、后续审计或图表重建。
- 下一步：继续监测 A/B dynamic；任一正式场景工件改写后立即执行 baseline SHA、20 个来源哈希、800/1,576 候选、regret、residual、support、demand 和 comparison 算术门禁。
- 状态：formal_sensitivity_3_of_8_verified；formal_capacity_high_dynamic_115563；formal_qos_threshold_low_dynamic_75590；sensitivity_queues_healthy

### 2026-07-18 02:00 - 正式敏感性小时状态

- 正式进度：仍为 3/8；`capacity_high` 与 `qos_threshold_low` 仍在 dynamic 阶段运行，其余 3 个场景排队，尚无新的正式场景工件改写。
- Queue A：`capacity_high` dynamic 从 115,563 依次推进到 117,139、118,715、120,291、121,867、123,443 和 125,019 对；检查点保持 `+1,576` 的补齐节奏。
- Queue B：`qos_threshold_low` dynamic 从 75,590 推进到 83,782 对；该长批次确认完成并写回 cache，随后继续下一批计算。
- 监控命令：继续轮询会话 `71703`/`53295`，并使用 `stat -c '%y %s %n' ...`、`ps --ppid ...`、`free -m` 和 `vmstat 1 3` 复核 cache、worker 数、内存和换页状态。
- 健康状态：两组均保持 17 个子进程；最近可用内存约 2.6 GiB。一次瞬时 swap-out 后连续复核恢复为 `so=0`，后续实时样本只见低速 swap-in 或无换页，未见 OOM、进程退出或错误输出。
- 决策：继续保持两队 16-worker 续算；不启动会争抢 CPU/IO 的完整测试、后续审计或图表重建。
- 下一步：继续监测 A/B dynamic；任一正式场景工件改写后立即执行 baseline SHA、20 个来源哈希、800/1,576 候选、regret、residual、support、demand 和 comparison 算术门禁。
- 状态：formal_sensitivity_3_of_8_verified；formal_capacity_high_dynamic_125019；formal_qos_threshold_low_dynamic_83782；sensitivity_queues_healthy

### 2026-07-18 02:45 - capacity-high 正式通过并切换 price-sensitivity-low

- 场景完成：Queue A 在 `capacity_high` dynamic 从 132,899 补齐到 133,687 对后输出 `finished capacity_high: regret=2.274e-13, peak=-12.98%`；随后自动进入 `price_sensitivity_low`，uniform 初始检查点为 71 对。
- 工件：`sensitivity_capacity_high_submission.json` 的 SHA-256 为 `7124aa36ae11e6bd1eb9525e8fe70c59671abd1dcce8e11634985b0d9429a301`，记录的 baseline SHA-256 精确匹配 `70a3b640...ed226`。
- 候选与求解：uniform/dynamic 为 800/1,576 候选、20,658/133,687 个评价对、13-by-13/43-by-43 正概率支持；两场 full regret 均为 `2.2737e-13`，dynamic relative regret 为 `2.9725e-16`，最大联合 residual 为 `9.9544e-10`，需求守恒为 1,100。
- 场景比较：aggregate peak `-12.9817%`、maximum provider utilization `-7.6212%`、minimum QoS `+0.027873`、aggregate market-side profit `+0.4854%`。
- 正式门禁命令：使用 `validate_sensitivity_scenario('capacity_high', ...)` 绑定当前 baseline SHA；退出码 0，`passed=true`，20/20 来源哈希、候选规模、regret、residual、需求守恒和 comparison 算术均通过。
- 补充提取：首次补充数值提取命令因 `native_demand` 为嵌套 list 而退出码 1；改用递归 `total(...)` 后退出码 0，并得到上述 demand、support 和 comparison 数值。
- 并发事件：Queue B 在 `qos_threshold_low` dynamic 写回 100,166 与 100,182 对后短暂出现 54 个子进程，可用内存最低约 598 MiB；15 秒复查自动恢复为 17 个子进程，可用内存回升到约 4.8 GiB，实时 `vmstat` 未出现持续 swap-out。
- 文档同步：Artifact Manifest、evidence map、理论一致性审计和回归契约更新为正式 4/8；剩余 `price_sensitivity_low`、`price_sensitivity_high`、`qos_threshold_low` 与 `qos_threshold_high` 仍在运行或排队。
- 下一步：继续监测 Queue A 的 `price_sensitivity_low` 与 Queue B 的 `qos_threshold_low`；任一场景完成后立即执行同一正式门禁。
- 状态：formal_capacity_high_verified；formal_sensitivity_4_of_8_verified；formal_price_sensitivity_low_uniform_71；formal_qos_threshold_low_dynamic_100182；worker_pool_overlap_recovered

### 2026-07-18 03:00 - 4/8 状态同步与定向验证

- 正式进度：`migration_cost_low`、`capacity_low`、`migration_cost_high` 与 `capacity_high` 已通过新 800/1,576 基线门禁，当前为 4/8；其余 4 个场景仍在运行或排队，不报告跨场景范围或方向稳定性。
- Queue A：`price_sensitivity_low` uniform 从 71 推进到 4,831 和 4,832 对，16 个 worker 继续运行。
- Queue B：`qos_threshold_low` dynamic 从 100,182 推进到 101,758 对，16 个 worker 继续运行。
- 文档验证：`git diff --check -- README.md ARTIFACT_MANIFEST.md docs/reviews/smpt_submission_evidence_map_2026-07-14.md docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md tests/test_submission_augmented_evidence_contract.py` 退出码 0；`TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run pytest tests/test_submission_augmented_evidence_contract.py -q` 为 `9 passed in 0.79s`。
- Ruff 状态：`uv run ruff check tests/test_submission_augmented_evidence_contract.py` 退出码 2，错误为 `Failed to spawn: ruff`；`uv run python -m ruff check ...` 退出码 1，错误为 `No module named ruff`。未临时安装依赖，暂不声称 Ruff 通过。
- 健康状态：两组均保持 17 个子进程；最近可用内存约 4.5 GiB，实时 `vmstat` 样本 `so=0`，未见 OOM、进程退出或错误输出。
- 决策：保持两队 16-worker 续算；Ruff 待 CPU 释放或环境补齐后再复验，当前以 whitespace 和定向 pytest 作为文档同步验证。
- 下一步：继续监测 `price_sensitivity_low` 与 `qos_threshold_low`；任一正式场景完成后执行 baseline SHA、20 个来源哈希、800/1,576 候选、regret、residual、support、demand 和 comparison 算术门禁。
- 状态：formal_sensitivity_4_of_8_verified；formal_price_sensitivity_low_uniform_4832；formal_qos_threshold_low_dynamic_101758；doc_contract_verified；ruff_unavailable

### 2026-07-18 04:00 - 正式敏感性小时状态

- 正式进度：仍为 4/8；`price_sensitivity_low` 与 `qos_threshold_low` 正在运行，`price_sensitivity_high` 和 `qos_threshold_high` 仍排队，不报告八场景范围或方向稳定性。
- Queue A：`price_sensitivity_low` uniform 从 4,832 依次推进到 6,424、6,425、8,015、8,016、9,604、10,398、10,399、11,984、11,985、13,568、13,569、15,150、15,151、16,730、16,731、18,308、18,309、19,884、19,885、21,458 和 21,459 对。
- Queue B：`qos_threshold_low` dynamic 从 101,758 依次推进到 103,334、104,910、106,486、108,062、109,638、111,214 和 112,790 对。
- 健康状态：两组均保持 17 个子进程；最近可用内存约 4.3 GiB。`vmstat` 实时样本保持 `so=0`，仅有低速瞬时 swap-in，未见 OOM、进程退出或错误输出。
- 文档状态：4/8 状态已同步到 README、Artifact Manifest、evidence map、理论一致性审计和定向回归契约；Ruff 仍因当前环境缺少 `ruff` 可执行文件和模块而未复验。
- 决策：保持两队 16-worker 续算；不启动完整测试、后续审计或图表重建。
- 下一步：继续监测 A/B；任一正式场景工件改写后立即执行 baseline SHA、20 个来源哈希、800/1,576 候选、regret、residual、support、demand 和 comparison 算术门禁。
- 状态：formal_sensitivity_4_of_8_verified；formal_price_sensitivity_low_uniform_21459；formal_qos_threshold_low_dynamic_112790；sensitivity_queues_healthy；ruff_unavailable

### 2026-07-18 04:45 - qos-threshold-low 正式通过并切换 qos-threshold-high

- 场景完成：Queue B 在 `qos_threshold_low` dynamic 从 119,094 补齐到 119,882 对后输出 `finished qos_threshold_low: regret=3.411e-13, peak=-12.35%`；随后自动进入 `qos_threshold_high`，uniform 初始检查点为 88 对。
- 工件：`sensitivity_qos_threshold_low_submission.json` 的 SHA-256 为 `4fc3ebbc7a1bef2ef977dcee70dbd404e52696b2b1e772aed6c054f84d5df437`，记录的 baseline SHA-256 精确匹配 `70a3b640...ed226`。
- 候选与求解：uniform/dynamic 为 800/1,576 候选、50,252/119,882 个评价对、30-by-34/42-by-35 正概率支持；uniform/dynamic full regret 为 `2.2737e-13/3.4106e-13`，dynamic relative regret 为 `4.0019e-16`，最大联合 residual 为 `9.9786e-10`，需求守恒为 1,100。
- 场景比较：aggregate peak `-12.3544%`、maximum provider utilization `-10.9019%`、minimum QoS `+0.053435`、aggregate market-side profit `-0.3160%`。
- 正式门禁命令：使用 `validate_sensitivity_scenario('qos_threshold_low', ...)` 绑定当前 baseline SHA；退出码 0，`passed=true`，20/20 来源哈希、候选规模、regret、residual、需求守恒和 comparison 算术均通过。
- 文档同步：Artifact Manifest、evidence map、理论一致性审计和回归契约更新为正式 5/8；剩余 `price_sensitivity_low`、`price_sensitivity_high` 与 `qos_threshold_high` 仍在运行或排队。
- 队列接续：Queue A 的 `price_sensitivity_low` uniform 已推进到 35,536 对并继续运行；Queue B 的 `qos_threshold_high` uniform 已写入 88 对并启动 16-worker 批次。
- 下一步：继续监测 Queue A 的 `price_sensitivity_low` 与 Queue B 的 `qos_threshold_high`；任一场景完成后立即执行同一正式门禁。
- 状态：formal_qos_threshold_low_verified；formal_sensitivity_5_of_8_verified；formal_price_sensitivity_low_uniform_35536；formal_qos_threshold_high_uniform_88

### 2026-07-18 05:00 - 正式敏感性小时状态

- 正式进度：`migration_cost_low`、`capacity_low`、`migration_cost_high`、`capacity_high` 与 `qos_threshold_low` 已通过新 800/1,576 基线门禁，当前为 5/8；其余 3 个场景仍在运行或排队，不报告八场景范围或方向稳定性。
- Queue A：`price_sensitivity_low` uniform 从 21,459 依次推进到 23,030、23,817、25,385、26,171、27,736、28,521、30,084、31,645、33,203、33,980、34,760、35,536、36,316、37,868、38,646、38,647、40,196 和 40,197 对。
- Queue B：`qos_threshold_low` dynamic 在 119,882 对正式完成并通过门禁；`qos_threshold_high` 随后开始，uniform 从 88 推进到 4,848 和 4,849 对。
- 文档验证：5/8 状态同步后，`git diff --check -- README.md ARTIFACT_MANIFEST.md docs/reviews/smpt_submission_evidence_map_2026-07-14.md docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md tests/test_submission_augmented_evidence_contract.py` 退出码 0；`TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run pytest tests/test_submission_augmented_evidence_contract.py -q` 为 `9 passed in 5.18s`。
- Ruff 状态：当前环境仍缺少 `ruff` 可执行文件和模块，沿用 03:00 记录的 `ruff_unavailable`，未临时安装依赖。
- 健康状态：两组均保持 17 个子进程；最近可用内存约 4.4 GiB。`vmstat` 实时样本保持 `so=0`，仅有低速瞬时 swap-in，未见 OOM、进程退出或错误输出。
- 决策：保持两队 16-worker 续算；不启动完整测试、后续审计或图表重建。
- 下一步：继续监测 `price_sensitivity_low` 与 `qos_threshold_high`；任一正式场景完成后执行 baseline SHA、20 个来源哈希、800/1,576 候选、regret、residual、support、demand 和 comparison 算术门禁。
- 状态：formal_sensitivity_5_of_8_verified；formal_price_sensitivity_low_uniform_40197；formal_qos_threshold_high_uniform_4849；sensitivity_queues_healthy；ruff_unavailable

### 2026-07-18 06:00 - 正式敏感性小时状态

- 正式进度：仍为 5/8；`price_sensitivity_low` 与 `qos_threshold_high` 正在运行，`price_sensitivity_high` 仍排队，不报告八场景范围或方向稳定性。
- Queue A：`price_sensitivity_low` uniform 从 40,197 依次推进到 41,745、43,291、44,835、46,377、47,917、49,455、50,991、52,525、54,056、54,824、55,592、55,593 和 57,120 对；dynamic cache 仍为旧时间戳，尚未切入正式 dynamic 阶段。
- Queue B：`qos_threshold_high` uniform 从 4,849 依次推进到 6,441、6,442、8,032、8,827、8,828、10,415、10,416、12,001、12,793、12,794、14,376、15,167、15,168、16,736、16,737、18,314、18,315、19,890、20,677、21,464、22,250 和 23,036 对。
- 健康状态：两组均保持 17 个子进程；最近可用内存约 4.7 GiB。`vmstat` 实时样本保持 `so=0`，仅有低速瞬时 swap-in，未见 OOM、进程退出或错误输出。
- 决策：保持两队 16-worker 续算；不启动完整测试、后续审计或图表重建。
- 下一步：继续监测 A/B；任一正式场景工件改写后立即执行 baseline SHA、20 个来源哈希、800/1,576 候选、regret、residual、support、demand 和 comparison 算术门禁。
- 状态：formal_sensitivity_5_of_8_verified；formal_price_sensitivity_low_uniform_57120；formal_qos_threshold_high_uniform_23036；sensitivity_queues_healthy；ruff_unavailable

### 2026-07-18 06:55 - price-sensitivity-low uniform 求解失败

- 目标：继续监测正式敏感性队列，并在场景完成后执行正式门禁。
- 操作：轮询 Queue A 会话 `71703` 与 Queue B 会话 `53295`，并用 `ps --ppid`、`stat -c '%y %s %n' ...`、`free -m` 复核 worker 数、缓存时间戳和内存状态。
- Queue A 进展：`price_sensitivity_low` uniform 从 57,120 继续推进到 65,493、67,008、68,521、70,031、70,782 和 71,540 对；`price_sensitivity_low/dynamic.pkl` 仍为 2026-07-16 旧缓存，当前运行未进入 dynamic。
- Queue B 进展：`qos_threshold_high` uniform 已结束并切入 dynamic；`qos_threshold_high/dynamic.pkl` 在 06:45 写入当前检查点，stdout 显示 `dynamic cache checkpoint: 62163 pairs`。旧 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 工件，未计入当前正式证据。
- 资源事件：Queue A 在 06:52 左右出现 worker 池重叠，子进程数从 17 升至 63；06:53 复查时可用内存降至 242 MiB，低于 512 MiB 保护线。准备发送 `SIGTERM` 前，Queue A 父进程已自行退出，`kill -TERM 1542276` 返回 `No such process`；随后可用内存恢复到约 8.7 GiB。
- 失败输出：Queue A 会话退出码 1，错误为 `RuntimeError: bounded mixed-solver ensemble returned no valid restricted equilibrium`，调用栈位于 `experiments/run_submission_spatiotemporal_sensitivity.py` -> `experiments/run_final_spatiotemporal_equilibrium.py` -> `experiments/final_equilibrium_tools.py` -> `pricing_sim/finite_game.py`。
- 工件状态：`sensitivity_price_sensitivity_low_submission.json` 与 `sensitivity_price_sensitivity_high_submission.json` 仍是 2026-07-16 旧工件，不能作为当前 800/1,576 基线的正式证据；当前只保留 `price_sensitivity_low/uniform.pkl` 检查点。
- 决策：暂不修改 `run_submission_spatiotemporal_sensitivity.py`、`run_final_spatiotemporal_equilibrium.py`、`final_equilibrium_tools.py` 或 `finite_game.py`，避免 Queue B 最终写工件时记录的源码哈希与实际加载代码不一致。先只读诊断 A 的受限混合求解失败；待 Queue B 完成或确认可用无源码改动恢复路径后，再重启 A。
- 下一步：继续监测 Queue B 的 `qos_threshold_high` dynamic；同时检查 A 的求解器失败是否已有不改源码的重跑参数或缓存恢复路径。
- 状态：formal_sensitivity_5_of_8_verified；formal_price_sensitivity_low_failed_uniform_solver；formal_qos_threshold_high_dynamic_62163；queue_b_running；source_patch_deferred

### 2026-07-18 07:05 - mixed-solver fan-out 触发 OOM 保护

- 目标：在不改源码的前提下尝试恢复 `price_sensitivity_low`，并继续保护 `qos_threshold_high` 运行队列。
- 首次恢复命令：
  ```bash
  env TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run python -c "import json; from experiments.run_submission_spatiotemporal_sensitivity import run_sensitivity; result=run_sensitivity(scenario_names=['price_sensitivity_low'], parallel_workers=4); print(json.dumps(result['rows'], indent=2), flush=True)"
  ```
- 首次恢复结果：退出码 1；子进程在 `pricing_sim/bimatrix_solver.py` 中导入 `nashpy` 失败，错误为 `ModuleNotFoundError: No module named 'nashpy'`。该命令未使用 `requirements.txt`，没有推进缓存或覆盖正式 artifact。
- 正确环境恢复命令：
  ```bash
  env TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -c "import json; from experiments.run_submission_spatiotemporal_sensitivity import run_sensitivity; result=run_sensitivity(scenario_names=['price_sensitivity_low'], parallel_workers=4); print(json.dumps(result['rows'], indent=2), flush=True)"
  ```
- 正确环境恢复结果：会话 `35759` 进入 `starting submission sensitivity: price_sensitivity_low`，但随后在受限混合求解阶段同时启动 62 个 fork 子进程；07:02 复查时可用内存降至 410 MiB，低于 512 MiB 保护线。
- 保护操作：对 A 恢复进程 PID `1431577` 和 wrapper PID `1431357` 发送 `SIGTERM`；A 会话退出码 143，内存恢复到约 12.5 GiB 可用。
- Queue B 影响：Queue B 会话 `53295` 在同一窗口退出码 137，符合 OOM kill 特征；`qos_threshold_high/dynamic.pkl` 仍停在 06:45 的 62,163-pair 当前检查点，`sensitivity_qos_threshold_high_submission.json` 仍是 2026-07-16 旧工件，当前场景未完成。
- 诊断：`bounded_mixed_candidates()` 当前会一次性启动最多 64 个 Lemke--Howson/vertex 子进程；即使外层 `parallel_workers=4`，受限混合求解阶段仍会出现 60+ 子进程驻留。继续原样重启不满足资源保护要求。
- 决策：停止所有长时敏感性队列，先给 mixed solver 增加小批次并发上限，使 64 个标签按受控批次运行并保留完整标签覆盖；修复后再从 `price_sensitivity_low` 和 `qos_threshold_high` 的签名缓存恢复。
- 当前缓存：`price_sensitivity_low/uniform.pkl` 为 2026-07-18 06:51、约 380 MB；`qos_threshold_high/dynamic.pkl` 为 2026-07-18 06:45、约 330 MB。两个当前正式 artifact 均未生成。
- 状态：formal_sensitivity_5_of_8_verified；price_sensitivity_low_solver_fanout_blocked；qos_threshold_high_oom_interrupted；source_patch_required

### 2026-07-18 07:08 - mixed-solver fan-out 保护补丁

- 目标：修复受限混合求解阶段一次性 fork 最高 64 个子进程的问题，同时保持 64 个 Lemke--Howson 标签和 vertex enumeration 的候选覆盖逻辑。
- 修改：`pricing_sim/bimatrix_solver.py` 新增 `MAX_PARALLEL_MIXED_SOLVER_PROCESSES = 8`，`bounded_mixed_candidates()` 改为只保留最多 8 个 active solver 子进程；子进程结束后再从待运行标签中补启动下一个任务。该修改不改变支付矩阵、regret 门禁、候选选择规则或 equilibrium definition。
- 测试：`tests/test_finite_game.py` 增加资源上限断言，并将高编号 Lemke 标签恢复测试压到 `MAX_PARALLEL_MIXED_SOLVER_PROCESSES = 2`，确认低并发上限下仍能扫描到 `lemke_howson_label_9`。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_finite_game.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_spatiotemporal_equilibrium.py -q
  git diff --check -- README.md pricing_sim/bimatrix_solver.py tests/test_finite_game.py
  uv run python -m py_compile pricing_sim/bimatrix_solver.py pricing_sim/finite_game.py tests/test_finite_game.py
  ```
- 验证结果：`tests/test_finite_game.py` 为 `12 passed in 1.16s`；`tests/test_final_spatiotemporal_equilibrium.py` 为 `13 passed in 2.42s`；whitespace check 和 py_compile 退出码均为 0。
- 决策：修复后不再同时启动两个 16-worker 长队列；先用受控求解器从 `price_sensitivity_low` 的 uniform 缓存恢复，并用资源采样确认 mixed-solver fan-out 不超过 8 个 active 子进程，再恢复 `qos_threshold_high`。
- 状态：mixed_solver_fanout_guard_verified；formal_sensitivity_5_of_8_verified；sensitivity_resume_pending

### 2026-07-18 07:20 - mixed-solver 标签时间片补丁

- 背景：active 子进程上限补丁避免了 OOM，但 `price_sensitivity_low` 仍在受限混合求解阶段失败；原因是前 8 个 Lemke--Howson 标签若长时间不返回，高编号标签无法在 120 秒窗口内启动。
- 修改：`pricing_sim/bimatrix_solver.py` 新增 `MIXED_SOLVER_LABEL_TIMEOUT_SECONDS = 10.0`。Vertex enumeration 分支保留完整 `MIXED_SOLVER_TIMEOUT_SECONDS = 120.0`；Lemke--Howson 标签按 10 秒时间片轮转，超时即终止该标签进程并启动下一个标签。总 active 子进程数仍不超过 `MAX_PARALLEL_MIXED_SOLVER_PROCESSES = 8`。
- 语义边界：该补丁仍不改变支付矩阵、payoff normalization、regret 门禁、MILP/互补回退或均衡定义；只改变 exact solver ensemble 的进程调度方式。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_finite_game.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_spatiotemporal_equilibrium.py -q
  git diff --check -- README.md pricing_sim/bimatrix_solver.py tests/test_finite_game.py
  uv run python -m py_compile pricing_sim/bimatrix_solver.py pricing_sim/finite_game.py tests/test_finite_game.py
  ```
- 验证结果：`tests/test_finite_game.py` 为 `12 passed in 0.86s`；`tests/test_final_spatiotemporal_equilibrium.py` 为 `13 passed in 2.60s`；whitespace check 和 py_compile 退出码均为 0。
- 决策：用该调度版本重新恢复 `price_sensitivity_low`，先不并行恢复 `qos_threshold_high`，避免再次把缓存恢复和 solver 诊断混在一起。
- 状态：mixed_solver_label_timeslice_verified；formal_sensitivity_5_of_8_verified；price_sensitivity_low_resume_pending

### 2026-07-18 07:45 - 42x50 restricted game MILP 修复

- 失败定位：运行时 wrapper 保存 `price_sensitivity_low` uniform 第 51 次受限博弈到 `/tmp/price_sensitivity_low_failed_restricted_game.npz`；矩阵规模为 `42 x 50`，有 warm initial candidate，原错误仍是 `bounded mixed-solver ensemble returned no valid restricted equilibrium`。
- 诊断结果：该矩阵无 pure equilibrium；现有归一化 MILP 在 30 s 内返回 `success=true`，但 raw mix 的原支付最大 restricted regret 为 `9.289e-4`，超过 `1e-7` 门禁；`_support_polish()` 正确拒绝该近似解。Nashpy vertex enumeration 单进程运行 87.77 s 后因 Qhull 高维 halfspace intersection 溢出失败。
- 关键原因：MILP 在 `[0,1]` 归一化支付上建模时，HiGHS 的绝对可行性误差会被原支付跨度放大；同一矩阵改用原支付尺度和 payoff span Big-M 后，30 s 内返回原支付最大 restricted regret `6.71e-12` 的有效解。
- 修改：`pricing_sim/milp_equilibrium_solver.py` 不再把 MILP 支付矩阵归一化；`_equilibrium_constraints()` 使用每位玩家原支付跨度作为 Big-M，`row_value`/`col_value` bounds 使用原支付最小值和最大值。若 `_support_polish()` 因退化返回 None，但 raw MILP mix 的原支付 regret 不超过 `MIP_RAW_REGRET_TOLERANCE = 1e-9`，则接受 raw mix。
- 测试：`tests/test_finite_game.py` 新增回归，强制 `_support_polish()` 返回 None，确认严格 raw MILP solution 不会被丢弃。
- 验证命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_finite_game.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_spatiotemporal_equilibrium.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt python - <<'PY'
  import json
  import numpy as np
  from pricing_sim.finite_game import enumerate_bimatrix_equilibria

  data = np.load('/tmp/price_sensitivity_low_failed_restricted_game.npz')
  equilibria = enumerate_bimatrix_equilibria(
      data['payoff_row'], data['payoff_col'], initial_candidate=None
  )
  print(json.dumps({
      'count': len(equilibria),
      'method': equilibria[0]['method'],
      'restricted_max_regret': equilibria[0]['restricted_max_regret'],
  }, indent=2))
  PY
  git diff --check -- README.md pricing_sim/bimatrix_solver.py pricing_sim/milp_equilibrium_solver.py tests/test_finite_game.py
  uv run python -m py_compile pricing_sim/bimatrix_solver.py pricing_sim/milp_equilibrium_solver.py pricing_sim/finite_game.py tests/test_finite_game.py
  ```
- 验证结果：`tests/test_finite_game.py` 为 `13 passed in 0.95s`；`tests/test_final_spatiotemporal_equilibrium.py` 为 `13 passed in 2.64s`；42×50 失败矩阵直接枚举返回 `highs_milp_complementarity`，restricted regret `3.3765e-11`；whitespace check 和 py_compile 退出码均为 0。
- 决策：该修复改变的是 MILP 数值尺度和退化 raw 解接收条件，不改变原支付 regret 门禁或均衡定义。接下来恢复 `price_sensitivity_low`，并继续只运行一个正式敏感性队列，避免再次触发内存竞争。
- 状态：price_sensitivity_low_restricted_game_fixed；mixed_solver_milp_original_scale_verified；formal_sensitivity_5_of_8_verified

### 2026-07-18 07:50 - price-sensitivity-low 修复后恢复检查点

- 操作：使用修复后的 `bimatrix_solver.py` 与 `milp_equilibrium_solver.py` 恢复 `price_sensitivity_low`，命令为：
  ```bash
  env TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -c "import json; from experiments.run_submission_spatiotemporal_sensitivity import run_sensitivity; result=run_sensitivity(scenario_names=['price_sensitivity_low'], parallel_workers=8); print(json.dumps(result['rows'], indent=2), flush=True)"
  ```
- 结果：恢复会话 `18725` 成功越过此前第 51 次 `42 x 50` 受限博弈失败点，并在 07:49 写入 `uniform cache checkpoint: 72290 pairs`。`price_sensitivity_low/uniform.pkl` 更新时间为 2026-07-18 07:49，大小约 384 MB。
- 资源：恢复期间保持单队列运行；pair-evaluation 阶段为 8 个 worker 加 resource tracker，未再出现 60+ solver 子进程；最近可用内存约 9.9 GiB。
- 当前阶段：`price_sensitivity_low` 仍处于 uniform，`price_sensitivity_low/dynamic.pkl` 仍是 2026-07-16 旧缓存，正式 `sensitivity_price_sensitivity_low_submission.json` 尚未改写。
- 决策：继续单队列监测，不恢复 `qos_threshold_high`，直到 `price_sensitivity_low` 完成 uniform 或进入稳定 dynamic 阶段。
- 状态：price_sensitivity_low_uniform_72290；restricted_game_failure_recovered；formal_sensitivity_5_of_8_verified

### 2026-07-18 08:00 - 正式敏感性恢复小时状态

- 正式进度：仍为 5/8；`price_sensitivity_low` 正在修复后单队列恢复，`price_sensitivity_high` 尚未运行，`qos_threshold_high` 因 07:02 OOM interruption 暂停等待恢复。
- Queue A：`price_sensitivity_low` 在 07:49 写入 `uniform cache checkpoint: 72290 pairs` 后继续运行；截至 08:00，仍为 8 个 pair-evaluation worker 加 resource tracker，尚未写入下一 checkpoint，也未切入 dynamic。`price_sensitivity_low/dynamic.pkl` 仍为 2026-07-16 旧缓存。
- Queue B：`qos_threshold_high` 当前未运行；可恢复缓存仍是 06:45 的 `dynamic cache checkpoint: 62163 pairs`，正式 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 旧工件，不能计入当前证据。
- 源码状态：本小时修改了 `pricing_sim/bimatrix_solver.py`、`pricing_sim/milp_equilibrium_solver.py` 和 `tests/test_finite_game.py`；后续新敏感性 artifact 会记录修复后的源码哈希。该差异已在 07:45 记录为 provenance 边界。
- 验证状态：本小时 `tests/test_finite_game.py`、`tests/test_final_spatiotemporal_equilibrium.py`、42×50 失败矩阵直接枚举、whitespace check 和 py_compile 均已通过；Ruff 仍沿用前述 `ruff_unavailable`，未临时安装依赖。
- 资源：最近采样显示 A 子进程数为 9，worker 合计 CPU 约 800%，可用内存约 9.3 GiB；swap 仍有历史占用但当前未见持续 OOM 或进程增长。
- 决策：继续只跑 `price_sensitivity_low`，不同时恢复 `qos_threshold_high`；待 A 完成 uniform 或进入稳定 dynamic 后，再按单队列或低并发恢复 B。
- 状态：formal_sensitivity_5_of_8_verified；price_sensitivity_low_uniform_72290_running；qos_threshold_high_paused_after_oom；solver_fix_verified

### 2026-07-18 08:45 - price-sensitivity-low 切入 dynamic

- 进展：`price_sensitivity_low` 在修复后的 uniform 阶段继续运行约 51 分钟后，切入当前 dynamic 阶段；stdout 显示 `dynamic cache checkpoint: 79314 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 08:40，大小约 422 MB，确认不再是 2026-07-16 旧缓存；`price_sensitivity_low/uniform.pkl` 最近检查点仍为 07:49 的 72,290 对。
- 工件：`sensitivity_price_sensitivity_low_submission.json` 仍为 2026-07-16 旧工件，当前场景尚未完成，不能计入正式 6/8。
- 资源：dynamic 初始批次保持 8 个 worker 加 resource tracker，最近可用内存约 8.8 GiB；未再出现 60+ mixed-solver fan-out 或 OOM。
- 决策：继续让 `price_sensitivity_low` 单队列运行，先确认 dynamic 后续 checkpoint 稳定；暂不恢复 `qos_threshold_high`。
- 状态：price_sensitivity_low_dynamic_79314；formal_sensitivity_5_of_8_verified；qos_threshold_high_paused_after_oom

### 2026-07-18 09:00 - 正式敏感性恢复小时状态

- 正式进度：仍为 5/8；`price_sensitivity_low` 正在 dynamic 阶段运行，`price_sensitivity_high` 尚未运行，`qos_threshold_high` 仍暂停等待恢复。
- Queue A：`price_sensitivity_low` dynamic 从 08:40 的 79,314 对 checkpoint 后继续运行；截至 09:00，仍为 8 个 worker 加 resource tracker，尚未写入下一 dynamic checkpoint，正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写。
- Queue B：`qos_threshold_high` 未恢复，仍只保留 06:45 的 62,163-pair dynamic checkpoint；旧 JSON 工件未计入正式证据。
- 资源：最近采样显示 A 子进程数为 9，可用内存约 9.4 GiB；swap 仍接近满载但无持续 swap-out 或 OOM。继续保持单队列，避免复现 07:02 的并发内存问题。
- 验证状态：本小时未新增源码修改；前述 finite-game、小规模 pipeline、42×50 失败矩阵直接枚举、whitespace 和 py_compile 验证仍是当前补丁依据。
- 下一步：继续等待 `price_sensitivity_low` dynamic 下一 checkpoint 或正式完成；完成后执行 baseline SHA、20 个来源哈希、800/1,576 候选、regret、residual、support、demand 和 comparison 算术门禁。
- 状态：formal_sensitivity_5_of_8_verified；price_sensitivity_low_dynamic_79314_running；qos_threshold_high_paused_after_oom

### 2026-07-18 09:25 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 在长批次后写入 `dynamic cache checkpoint: 87506 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 09:25，大小约 465 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 尚未改写，仍不计入 6/8。
- 资源：单队列继续运行，8 个 worker 加 resource tracker；最近可用内存约 9.1 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_87506；formal_sensitivity_5_of_8_verified

### 2026-07-18 10:00 - 正式敏感性恢复小时状态

- 正式进度：仍为 5/8；`price_sensitivity_low` 正在 dynamic 阶段运行，`price_sensitivity_high` 未运行，`qos_threshold_high` 仍暂停。
- Queue A：`price_sensitivity_low` dynamic 在 09:25 写入 87,506 对 checkpoint 后继续运行；截至 10:00 尚未写入下一 checkpoint，正式 JSON 工件仍未改写。
- Queue B：`qos_threshold_high` 未恢复，仍等待 A 完成或更明确的资源窗口。
- 资源：A 保持 8 个 worker 加 resource tracker；最近 worker 合计 CPU 约 798%，可用内存约 8.8 GiB。Swap 仍有历史占用，但没有 OOM、进程增长或错误输出。
- 决策：继续只跑 A，避免恢复 B 导致两个 dynamic 队列竞争内存；不启动完整测试、图表重建或后续审计。
- 下一步：等待 A 下一 checkpoint 或正式完成；完成后立刻执行正式门禁并更新 Artifact Manifest、evidence map、理论一致性审计和回归契约。
- 状态：formal_sensitivity_5_of_8_verified；price_sensitivity_low_dynamic_87506_running；qos_threshold_high_paused_after_oom

### 2026-07-18 10:15 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 95698 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 10:12，大小约 509 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 尚未改写，仍不计入 6/8。
- 资源：A 继续保持 8 个 worker 加 resource tracker；最近可用内存约 8.5 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_95698；formal_sensitivity_5_of_8_verified

### 2026-07-18 10:55 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 103890 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 10:53，大小约 552 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 6/8。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 8.3 GiB，未见 OOM 或进程增长。
- 决策：继续单队列运行 `price_sensitivity_low`，暂不恢复 `qos_threshold_high`，避免两个 dynamic 队列竞争内存。
- 状态：price_sensitivity_low_dynamic_103890；formal_sensitivity_5_of_8_verified

### 2026-07-18 11:00 - 正式敏感性恢复小时状态

- 正式进度：仍为 5/8；`price_sensitivity_low` 正在 dynamic 阶段运行，`price_sensitivity_high` 未运行，`qos_threshold_high` 仍暂停。
- Queue A：`price_sensitivity_low` dynamic 在 10:53 写入 103,890 对 checkpoint 后继续运行；截至 11:02 尚未写入下一 checkpoint，正式 JSON 工件仍未改写。
- Queue B：`qos_threshold_high` 未恢复，仍保留 06:45 的 62,163-pair dynamic checkpoint；旧 JSON 工件未计入当前正式证据。
- 资源：A 保持 8 个 worker 加 resource tracker；最近 worker 合计 CPU 约 798%，可用内存约 8.3 GiB。Swap 仍为历史占用，但没有 OOM、进程增长或错误输出。
- 决策：继续只跑 A，不恢复 B；下一步等待 A 下一 checkpoint 或正式完成。
- 状态：formal_sensitivity_5_of_8_verified；price_sensitivity_low_dynamic_103890_running；qos_threshold_high_paused_after_oom

### 2026-07-18 11:40 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 112082 pairs`，随后写入 `dynamic cache checkpoint: 112098 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 11:35，大小约 596 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 6/8。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 795%，最近可用内存约 8.1 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_112098；formal_sensitivity_5_of_8_verified

### 2026-07-18 11:50 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 113674 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 11:46，大小约 604 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 7.9 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_113674；formal_sensitivity_5_of_8_verified

### 2026-07-18 12:00 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 115250 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 11:56，大小约 613 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：11:56 曾短暂只剩 resource tracker，随后启动下一批 8 个 worker；11:57 采样显示新 worker 运行约 61 s、合计 CPU 约 798%，可用内存约 7.6 GiB，未见 OOM。
- 决策：该现象符合批次切换，不视为完成；继续等待后续 checkpoint 或正式 JSON 写出。
- 状态：price_sensitivity_low_dynamic_115250；formal_sensitivity_5_of_8_verified

### 2026-07-18 12:05 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 116826 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 12:04，大小约 621 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 7.3 GiB，swap 历史占用下降到约 3.0 GiB，未见 OOM。
- 状态：price_sensitivity_low_dynamic_116826；formal_sensitivity_5_of_8_verified

### 2026-07-18 12:15 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 118402 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 12:14，大小约 629 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；最近可用内存约 7.2 GiB，swap 约 2.9 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_118402；formal_sensitivity_5_of_8_verified

### 2026-07-18 12:30 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 119978 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 12:23，大小约 638 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 7.0 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_119978；formal_sensitivity_5_of_8_verified

### 2026-07-18 12:35 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 121554 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 12:32，大小约 646 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 796%，最近可用内存约 7.0 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_121554；formal_sensitivity_5_of_8_verified

### 2026-07-18 12:45 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 123130 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 12:41，大小约 655 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 6.9 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_123130；formal_sensitivity_5_of_8_verified

### 2026-07-18 12:55 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 124706 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 12:50，大小约 663 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 6.8 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_124706；formal_sensitivity_5_of_8_verified

### 2026-07-18 13:00 - price-sensitivity-low dynamic checkpoint

- 正式进度：仍为 5/8；`price_sensitivity_low` 正在 dynamic 阶段运行，`price_sensitivity_high` 未运行，`qos_threshold_high` 仍暂停。
- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 126282 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 12:59，大小约 671 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 6/8。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 6.8 GiB，未见 OOM 或进程增长。
- 决策：继续只跑 A，不恢复 B；下一步等待 A 后续 checkpoint 或正式完成。
- 状态：price_sensitivity_low_dynamic_126282；formal_sensitivity_5_of_8_verified；qos_threshold_high_paused_after_oom

### 2026-07-18 13:15 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 127858 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 13:10，大小约 680 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 6.9 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_127858；formal_sensitivity_5_of_8_verified

### 2026-07-18 13:25 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 129434 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 13:19，大小约 688 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 6.8 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_129434；formal_sensitivity_5_of_8_verified

### 2026-07-18 13:30 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 131010 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 13:29，大小约 696 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 6.8 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_131010；formal_sensitivity_5_of_8_verified

### 2026-07-18 13:40 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 132586 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 13:39，大小约 705 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；最近可用内存约 6.7 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_132586；formal_sensitivity_5_of_8_verified

### 2026-07-18 13:55 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 134162 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 13:48，大小约 713 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 6.8 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_134162；formal_sensitivity_5_of_8_verified

### 2026-07-18 14:00 - 正式敏感性恢复小时状态

- 正式进度：仍为 5/8；`price_sensitivity_low` 正在 dynamic 阶段运行，`price_sensitivity_high` 未运行，`qos_threshold_high` 仍暂停。
- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 135738 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 13:59，大小约 722 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 6/8。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 6.7 GiB，未见 OOM 或进程增长。
- 决策：继续只跑 A，不恢复 B；下一步等待 A 后续 checkpoint 或正式完成。
- 状态：price_sensitivity_low_dynamic_135738；formal_sensitivity_5_of_8_verified；qos_threshold_high_paused_after_oom

### 2026-07-18 14:10 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 137314 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 14:09，大小约 730 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；最近可用内存约 6.6 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_137314；formal_sensitivity_5_of_8_verified

### 2026-07-18 14:20 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 138890 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 14:18，大小约 738 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 797%，最近可用内存约 6.6 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_138890；formal_sensitivity_5_of_8_verified

### 2026-07-18 14:30 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 140466 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 14:28，大小约 747 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 6.6 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_140466；formal_sensitivity_5_of_8_verified

### 2026-07-18 14:40 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 142042 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 14:37，大小约 755 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：A 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 797%，最近可用内存约 6.5 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_low_dynamic_142042；formal_sensitivity_5_of_8_verified

### 2026-07-18 14:50 - price-sensitivity-low dynamic checkpoint

- 进展：`price_sensitivity_low` dynamic 写入 `dynamic cache checkpoint: 143618 pairs`。
- 缓存：`price_sensitivity_low/dynamic.pkl` 更新时间为 2026-07-18 14:47，大小约 764 MB。
- 工件：正式 `sensitivity_price_sensitivity_low_submission.json` 仍未改写，当前场景尚未完成。
- 资源：14:47 曾短暂只剩 resource tracker，随后启动下一批 8 个 worker；14:48 采样显示新 worker 运行约 59 s、合计 CPU 约 800%，可用内存约 6.5 GiB，未见 OOM。
- 决策：该现象符合批次切换，不视为完成；继续等待后续 checkpoint 或正式 JSON 写出。
- 状态：price_sensitivity_low_dynamic_143618；formal_sensitivity_5_of_8_verified

### 2026-07-18 14:55 - price-sensitivity-low 完成与门禁验证

- 运行结果：`price_sensitivity_low` 写入最终 `dynamic cache checkpoint: 144406 pairs`，随后 stdout 显示 `finished price_sensitivity_low: regret=2.274e-13, peak=-12.84%`；会话 `18725` 退出码为 0。
- 工件：`sensitivity_price_sensitivity_low_submission.json` 于 2026-07-18 14:52 改写，大小 1,015,876 bytes，SHA-256 `b9852e673b2cb0c31f389313addac41e53c9fc09cb6758356e08c1dfd42879d6`。
- 正式门禁命令：
  ```bash
  uv run --no-project --with-requirements requirements.txt python - <<'PY'
  import hashlib
  import json
  from pathlib import Path
  from experiments.submission_evidence_gates import validate_sensitivity_scenario

  out = Path('artifacts/peak_shaving/20260712_expanded_response')
  baseline_path = out / 'spatiotemporal_equilibrium_submission.json'
  artifact_path = out / 'sensitivity_price_sensitivity_low_submission.json'
  baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
  artifact = json.loads(artifact_path.read_text(encoding='utf-8'))
  expected_hash = hashlib.sha256(baseline_path.read_bytes()).hexdigest()
  print(json.dumps(validate_sensitivity_scenario(
      'price_sensitivity_low',
      artifact,
      expected_hash=expected_hash,
      expected_baseline=baseline,
  ), indent=2))
  PY
  ```
- 验证结果：`validate_sensitivity_scenario('price_sensitivity_low', ...)` 返回 `passed=true`；20/20 来源哈希、baseline SHA `70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`、共同 800/1,576 候选、需求守恒、比较算术和 residual 门禁均通过。
- 数值摘要：uniform/dynamic evaluated pairs 为 `72,290/144,406`；正概率支持为 `20-by-20/21-by-21`；uniform/dynamic full regret 为 `3.3765e-11/2.2737e-13`；最大 joint residual 为 `9.9962e-10`。
- 结果变化：峰值 `-12.8392%`，最大利用率 `-8.7991%`，最低 QoS `+0.0423`，市场侧利润 `-9.4905%`。
- 决策：当前正式敏感性从 5/8 更新为 6/8；剩余 `price_sensitivity_high` 和 `qos_threshold_high` 仍需重跑或恢复并通过同一门禁。
- 状态：price_sensitivity_low_verified；formal_sensitivity_6_of_8_verified；price_sensitivity_high_pending；qos_threshold_high_paused_after_oom

### 2026-07-18 14:57 - 6/8 证据文档与契约测试更新

- 修改：将 `ARTIFACT_MANIFEST.md`、`docs/reviews/smpt_submission_evidence_map_2026-07-14.md`、`docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md` 和 `tests/test_submission_augmented_evidence_contract.py` 从 5/8 更新到 6/8，并加入 `price_sensitivity_low` 的正式门禁数值。
- Provenance 边界：`price_sensitivity_low` 单场景工件记录的是当前修复后源码哈希并已通过场景门禁；但旧 baseline 工件自身记录的 `pricing_sim/bimatrix_solver.py` 哈希与当前修复后源码不一致，因此完整 combined evidence gate 仍有 baseline provenance 红灯，不能声称全门禁通过。
- 验证命令：
  ```bash
  git diff --check -- README.md ARTIFACT_MANIFEST.md docs/reviews/smpt_submission_evidence_map_2026-07-14.md docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md tests/test_submission_augmented_evidence_contract.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_augmented_evidence_contract.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_evidence_gates.py -q -k 'sensitivity_scenario or sensitivity_summary or sensitivity_claims or uniform_offgrid or provider_payoff'
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_evidence_gates.py -q
  ```
- 验证结果：diff check 退出码 0；augmented evidence contract 为 `9 passed in 0.23s`；敏感性相关 evidence gate 子集为 `6 passed, 76 deselected in 0.25s`。完整 `tests/test_submission_evidence_gates.py` 为 `11 failed, 71 passed`，失败均由 `pricing_sim/bimatrix_solver.py: source SHA-256 mismatch` 先触发的旧 baseline provenance mismatch 引起。
- 决策：6/8 单场景证据成立；后续不能生成 combined evidence report 或最终 claims，直到 baseline provenance 红灯通过重建或明确 reconciliation 处理。
- 状态：formal_sensitivity_6_of_8_verified；price_sensitivity_low_gate_passed；baseline_provenance_gate_red_after_solver_patch

### 2026-07-18 14:58 - qos-threshold-high 单队列恢复启动

- 目标：恢复剩余正式扰动场景 `qos_threshold_high`，使用修复后的受控 mixed-solver 与原签名缓存继续计算。
- 启动命令：
  ```bash
  env TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -c "import json; from experiments.run_submission_spatiotemporal_sensitivity import run_sensitivity; result=run_sensitivity(scenario_names=['qos_threshold_high'], parallel_workers=8); print(json.dumps(result['rows'], indent=2), flush=True)"
  ```
- 会话：session `41273`；stdout 已输出 `starting submission sensitivity: qos_threshold_high`。
- 恢复输入：`qos_threshold_high/uniform.pkl` 更新时间为 2026-07-18 06:00，大小约 122 MB；`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 06:45，大小约 330 MB。
- 工件边界：`sensitivity_qos_threshold_high_submission.json` 仍是 2026-07-16 旧工件，当前不能计入正式 7/8。
- 资源：启动前可用内存约 11.5 GiB；继续只跑一个长队列，不并行恢复 `price_sensitivity_high`。
- 状态：qos_threshold_high_resume_started；formal_sensitivity_6_of_8_verified；price_sensitivity_high_pending

### 2026-07-18 15:00 - qos-threshold-high 恢复小时状态

- 正式进度：仍为 6/8；`qos_threshold_high` 正在单队列恢复，`price_sensitivity_high` 尚未恢复。
- Queue Q：`qos_threshold_high` session `41273` 运行中；截至 15:03，仍为 8 个 worker 加 resource tracker，尚未写入新的 dynamic checkpoint。
- 缓存：`qos_threshold_high/dynamic.pkl` 仍停在 2026-07-18 06:45 的 62,163-pair checkpoint，正式 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 旧工件。
- 资源：worker 合计 CPU 约 800%，可用内存约 9.2 GiB，未见 OOM、进程增长或错误输出。
- 决策：继续只跑 Q，不并行恢复 `price_sensitivity_high`。
- 状态：qos_threshold_high_running_from_62163；formal_sensitivity_6_of_8_verified

### 2026-07-18 15:45 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 70355 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 15:44，大小约 374 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 7/8。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 8.7 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_70355；formal_sensitivity_6_of_8_verified

### 2026-07-18 16:00 - qos-threshold-high 恢复小时状态

- 正式进度：仍为 6/8；`qos_threshold_high` 正在 dynamic 阶段运行，`price_sensitivity_high` 尚未恢复。
- Queue Q：`qos_threshold_high` dynamic 在 15:44 写入 70,355 对 checkpoint 后继续运行；截至 16:02 尚未写入下一 checkpoint，正式 JSON 工件仍未改写。
- 资源：Q 保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 8.8 GiB，未见 OOM、进程增长或错误输出。
- 决策：继续只跑 Q，不并行恢复 `price_sensitivity_high`。
- 状态：qos_threshold_high_dynamic_70355_running；formal_sensitivity_6_of_8_verified

### 2026-07-18 16:35 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 78547 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 16:32，大小约 418 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 7/8。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 8.8 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_78547；formal_sensitivity_6_of_8_verified

### 2026-07-18 17:00 - qos-threshold-high 恢复小时状态

- 正式进度：仍为 6/8；`qos_threshold_high` 正在 dynamic 阶段运行，`price_sensitivity_high` 尚未恢复。
- Queue Q：`qos_threshold_high` dynamic 在 16:32 写入 78,547 对 checkpoint 后继续运行；截至 17:03 尚未写入下一 checkpoint，正式 JSON 工件仍未改写。
- 资源：Q 保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 8.7 GiB，未见 OOM、进程增长或错误输出。
- 决策：继续只跑 Q，不并行恢复 `price_sensitivity_high`。
- 状态：qos_threshold_high_dynamic_78547_running；formal_sensitivity_6_of_8_verified

### 2026-07-18 17:20 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 86739 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 17:19，大小约 461 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 7/8。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 8.6 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_86739；formal_sensitivity_6_of_8_verified

### 2026-07-18 18:00 - qos-threshold-high 恢复小时状态

- 正式进度：仍为 6/8；`qos_threshold_high` 正在 dynamic 阶段运行，`price_sensitivity_high` 尚未恢复。
- Queue Q：`qos_threshold_high` dynamic 在 17:19 写入 86,739 对 checkpoint 后继续运行；截至 18:02 尚未写入下一 checkpoint，正式 JSON 工件仍未改写。
- 资源：Q 保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 8.6 GiB，未见 OOM、进程增长或错误输出。
- 决策：继续只跑 Q，不并行恢复 `price_sensitivity_high`。
- 状态：qos_threshold_high_dynamic_86739_running；formal_sensitivity_6_of_8_verified

### 2026-07-18 18:05 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 94931 pairs`，随后写入 `dynamic cache checkpoint: 94947 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 18:06，大小约 505 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 7/8。
- 资源：18:06 采样显示 Q 仍为 8 个 worker 加 resource tracker；可用内存降至约 3.4 GiB，尚未出现 OOM 或进程增长，但需要加密监测。
- 决策：不启动其他队列；继续观察下一轮内存是否回落或进入危险区间。
- 状态：qos_threshold_high_dynamic_94947；formal_sensitivity_6_of_8_verified；memory_pressure_watch

### 2026-07-18 18:20 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 96523 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 18:17，大小约 513 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 7/8。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 8.7 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_96523；formal_sensitivity_6_of_8_verified

### 2026-07-18 18:30 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 98099 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 18:26，大小约 522 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 7/8。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 8.6 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_98099；formal_sensitivity_6_of_8_verified

### 2026-07-18 18:40 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 99675 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 18:36，大小约 530 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 7/8。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 8.6 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_99675；formal_sensitivity_6_of_8_verified

### 2026-07-18 18:42 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 100463 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 18:41，大小约 534 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍未改写，当前场景尚未完成。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 8.8 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_100463；formal_sensitivity_6_of_8_verified

### 2026-07-18 18:47 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 101251 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 18:46，大小约 538 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍未改写，当前场景尚未完成。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 8.5 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_101251；formal_sensitivity_6_of_8_verified

### 2026-07-18 18:55 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 102039 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 18:51，大小约 542 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍未改写，当前场景尚未完成。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 8.6 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_102039；formal_sensitivity_6_of_8_verified

### 2026-07-18 19:00 - qos-threshold-high 恢复小时状态

- 正式进度：仍为 6/8；`qos_threshold_high` 正在 dynamic 阶段运行，`price_sensitivity_high` 尚未恢复。
- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 102827 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 18:56，大小约 547 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍为 2026-07-16 旧工件，尚未改写，不能计入正式 7/8。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 8.3 GiB，未见 OOM 或进程增长。
- 决策：继续只跑 Q，不并行恢复 `price_sensitivity_high`。
- 状态：qos_threshold_high_dynamic_102827；formal_sensitivity_6_of_8_verified

### 2026-07-18 19:05 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 103615 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 19:02，大小约 551 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍未改写，当前场景尚未完成。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 795%，最近可用内存约 8.3 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_103615；formal_sensitivity_6_of_8_verified

### 2026-07-18 19:10 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 104403 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 19:07，大小约 555 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍未改写，当前场景尚未完成。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 792%，最近可用内存约 8.3 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_104403；formal_sensitivity_6_of_8_verified

### 2026-07-18 19:13 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 105191 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 19:12，大小约 559 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍未改写，当前场景尚未完成。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；最近可用内存约 8.2 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_105191；formal_sensitivity_6_of_8_verified

### 2026-07-18 19:20 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 105979 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 19:17，大小约 563 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍未改写，当前场景尚未完成。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 8.5 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_105979；formal_sensitivity_6_of_8_verified

### 2026-07-18 19:25 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 106767 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 19:22，大小约 568 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍未改写，当前场景尚未完成。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 8.5 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_106767；formal_sensitivity_6_of_8_verified

### 2026-07-18 19:30 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 107555 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 19:27，大小约 572 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍未改写，当前场景尚未完成。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 8.4 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_107555；formal_sensitivity_6_of_8_verified

### 2026-07-18 19:35 - qos-threshold-high dynamic checkpoint

- 进展：`qos_threshold_high` dynamic 写入 `dynamic cache checkpoint: 108343 pairs`。
- 缓存：`qos_threshold_high/dynamic.pkl` 更新时间为 2026-07-18 19:32，大小约 576 MB。
- 工件：正式 `sensitivity_qos_threshold_high_submission.json` 仍未改写，当前场景尚未完成。
- 资源：Q 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 797%，最近可用内存约 8.4 GiB，未见 OOM 或进程增长。
- 状态：qos_threshold_high_dynamic_108343；formal_sensitivity_6_of_8_verified

### 2026-07-18 19:40 - qos-threshold-high 完成与门禁验证

- 运行结果：`qos_threshold_high` 写入最终 `dynamic cache checkpoint: 109131 pairs`，随后 stdout 显示 `finished qos_threshold_high: regret=6.821e-13, peak=-12.78%`；会话 `41273` 退出码为 0。
- 工件：`sensitivity_qos_threshold_high_submission.json` 于 2026-07-18 19:37 改写，大小 770,797 bytes，SHA-256 `abc8956c89c7bf8792b3af9ee307366b7f9dfe74bab316f8f1967e89655d92b7`。
- 正式门禁命令：
  ```bash
  uv run --no-project --with-requirements requirements.txt python - <<'PY'
  import hashlib
  import json
  from pathlib import Path
  from experiments.submission_evidence_gates import validate_sensitivity_scenario

  out = Path('artifacts/peak_shaving/20260712_expanded_response')
  baseline_path = out / 'spatiotemporal_equilibrium_submission.json'
  artifact_path = out / 'sensitivity_qos_threshold_high_submission.json'
  baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
  artifact = json.loads(artifact_path.read_text(encoding='utf-8'))
  expected_hash = hashlib.sha256(baseline_path.read_bytes()).hexdigest()
  print(json.dumps(validate_sensitivity_scenario(
      'qos_threshold_high',
      artifact,
      expected_hash=expected_hash,
      expected_baseline=baseline,
  ), indent=2))
  PY
  ```
- 验证结果：`validate_sensitivity_scenario('qos_threshold_high', ...)` 返回 `passed=true`；20/20 来源哈希、baseline SHA `70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`、共同 800/1,576 候选、需求守恒、比较算术和 residual 门禁均通过。
- 数值摘要：uniform/dynamic evaluated pairs 为 `23,036/109,131`；正概率支持为 `6-by-6/24-by-24`；uniform/dynamic full regret 为 `1.1369e-13/6.8212e-13`；最大 joint residual 为 `9.9978e-10`。
- 结果变化：峰值 `-12.7809%`，最大利用率 `-11.1948%`，最低 QoS `+0.0583`，市场侧利润 `+1.4609%`。
- 决策：当前正式敏感性从 6/8 更新为 7/8；剩余 `price_sensitivity_high` 仍需重跑或恢复并通过同一门禁。
- 状态：qos_threshold_high_verified；formal_sensitivity_7_of_8_verified；price_sensitivity_high_pending

### 2026-07-18 19:40 - 7/8 证据文档与契约测试更新

- 修改：将 `ARTIFACT_MANIFEST.md`、`docs/reviews/smpt_submission_evidence_map_2026-07-14.md`、`docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md` 和 `tests/test_submission_augmented_evidence_contract.py` 从 6/8 更新到 7/8，并加入 `qos_threshold_high` 的正式门禁数值。
- 验证命令：
  ```bash
  git diff --check -- README.md ARTIFACT_MANIFEST.md docs/reviews/smpt_submission_evidence_map_2026-07-14.md docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md tests/test_submission_augmented_evidence_contract.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_augmented_evidence_contract.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_evidence_gates.py -q -k 'sensitivity_scenario or sensitivity_summary or sensitivity_claims or uniform_offgrid or provider_payoff'
  ```
- 验证结果：diff check 退出码 0；augmented evidence contract 为 `9 passed in 0.25s`；敏感性相关 evidence gate 子集为 `6 passed, 76 deselected in 0.25s`。
- 决策：7/8 单场景证据成立；最后剩余 `price_sensitivity_high` 继续按单队列恢复，完成前不生成 summary、claims 或 combined evidence report。
- 状态：formal_sensitivity_7_of_8_verified；price_sensitivity_high_pending；baseline_provenance_gate_red_after_solver_patch

### 2026-07-18 19:41 - price-sensitivity-high 单队列启动

- 目标：运行最后一个正式扰动场景 `price_sensitivity_high`，使用当前修复后源码与单队列 8 workers。
- 启动命令：
  ```bash
  env TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -c "import json; from experiments.run_submission_spatiotemporal_sensitivity import run_sensitivity; result=run_sensitivity(scenario_names=['price_sensitivity_high'], parallel_workers=8); print(json.dumps(result['rows'], indent=2), flush=True)"
  ```
- 会话：session `70679`；stdout 已输出 `starting submission sensitivity: price_sensitivity_high`。
- 旧缓存与工件：`price_sensitivity_high/uniform.pkl`、`dynamic.pkl` 和 `sensitivity_price_sensitivity_high_submission.json` 均为 2026-07-16 旧产物，当前不能计入正式 8/8；脚本会按签名决定是否复用。
- 资源：启动前可用内存约 11.9 GiB；继续只跑一个长队列。
- 状态：price_sensitivity_high_started；formal_sensitivity_7_of_8_verified

### 2026-07-18 19:43 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` 写入 `uniform cache checkpoint: 71 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 19:40，大小约 0.4 MB；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 含义：当前运行正在按新签名重建 uniform 阶段，不能把旧 `dynamic.pkl` 或旧 JSON 计入当前正式 8/8。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 9.8 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_71；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:00 - price-sensitivity-high 恢复小时状态

- 正式进度：仍为 7/8；最后剩余场景 `price_sensitivity_high` 正在 uniform 阶段运行。
- 进展：`price_sensitivity_high` 写入 `uniform cache checkpoint: 4831 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 20:01，大小约 30 MB；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 9.7 GiB，未见 OOM、进程增长或错误输出。
- 决策：继续单队列运行；完成前不生成 summary、claims 或 combined evidence report。
- 状态：price_sensitivity_high_uniform_4831；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:10 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 5628 pairs`、`6424 pairs` 和 `6425 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 20:04，大小约 34 MB；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 9.7 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_6425；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:15 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 8004 pairs` 和 `8005 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 20:10，大小约 43 MB；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 9.6 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_8005；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:18 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 9593 pairs` 和 `9594 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 20:16，大小约 51 MB；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；最近可用内存约 9.2 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_9594；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:22 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 11180 pairs` 和 `11181 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 20:22，大小约 59 MB；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；最近可用内存约 9.2 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_11181；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:30 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 12765 pairs` 和 `12766 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 20:28，大小约 68 MB；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 799%，最近可用内存约 9.2 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_12766；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:35 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 14348 pairs` 和 `14349 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 20:34，大小约 76 MB；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；最近可用内存约 9.2 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_14349；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:45 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 15929 pairs` 和 `15930 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 20:40，大小约 85 MB；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 797%，最近可用内存约 9.2 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_15930；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:50 - price-sensitivity-high uniform checkpoint

- 目标：继续检测最后一个正式扰动场景 `price_sensitivity_high` 的 uniform 阶段进展。
- 检查命令：
  ```bash
  date '+%F %T %Z'
  P=$(pgrep -f "/bin/python.*scenario_names=\['price_sensitivity_high'\]" | head -1); echo P_PID=${P:-none}
  if [ -n "$P" ]; then
    ps -o stat,%cpu,rss --no-headers --ppid "$P" | awk '{n++; cpu+=$2; rss+=$3; s[$1]++} END {print "P_children", n+0, "cpu", cpu+0, "rss_kb_sum", rss+0; for (k in s) print "P_stat", k, s[k]}'
  fi
  stat -c '%y %s %n' /root/.cache/peak_shaving_submission_sensitivity/price_sensitivity_high/uniform.pkl /root/.cache/peak_shaving_submission_sensitivity/price_sensitivity_high/dynamic.pkl artifacts/peak_shaving/20260712_expanded_response/sensitivity_price_sensitivity_high_submission.json 2>/dev/null
  free -m
  uv run --no-project --with-requirements requirements.txt python - <<'PY'
  import pickle
  from pathlib import Path

  p = Path('/root/.cache/peak_shaving_submission_sensitivity/price_sensitivity_high/uniform.pkl')
  with p.open('rb') as f:
      obj = pickle.load(f)
  print(len(obj['records']))
  PY
  ```
- 进展：`price_sensitivity_high/uniform.pkl` 当前内部 `records` 为 `17,509`，高于上次记录的 `15,930`。
- 缓存：`uniform.pkl` 更新时间为 2026-07-18 20:46，大小 93,069,050 bytes；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 9.1 GiB，未见 OOM 或错误输出。
- 决策：继续等待 uniform 阶段完成；完成前不把旧 dynamic 缓存和旧 JSON 计入正式 8/8。
- 状态：price_sensitivity_high_uniform_17509；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:52 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 19085 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 20:52，大小 101,446,834 bytes；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 798%，最近可用内存约 9.1 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_19085；formal_sensitivity_7_of_8_verified

### 2026-07-18 20:55 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 19873 pairs` 和 `19874 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 20:54，大小 105,640,032 bytes；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 816%，最近可用内存约 9.1 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_19874；formal_sensitivity_7_of_8_verified

### 2026-07-18 21:01 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 21447 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 21:00，大小 114,001,801 bytes；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 794%，最近可用内存约 9.3 GiB，未见 OOM 或进程增长。
- 决策：继续单队列运行；完成前不生成 summary、claims 或 combined evidence report。
- 状态：price_sensitivity_high_uniform_21447；formal_sensitivity_7_of_8_verified

### 2026-07-18 21:02 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 22234 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 21:02，大小 118,185,323 bytes；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 856%，最近可用内存约 9.3 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_22234；formal_sensitivity_7_of_8_verified

### 2026-07-18 21:06 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 23019 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 21:05，大小 122,358,241 bytes；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 800%，最近可用内存约 8.9 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_23019；formal_sensitivity_7_of_8_verified

### 2026-07-18 21:10 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 23804 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 21:08，大小 126,531,306 bytes；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 797%，最近可用内存约 9.2 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_23804；formal_sensitivity_7_of_8_verified

### 2026-07-18 21:12 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 24589 pairs` 和 `24590 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 21:11，大小 130,708,583 bytes；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：P 继续保持 8 个 worker 加 resource tracker；worker 合计 CPU 约 794%，最近可用内存约 9.0 GiB，未见 OOM 或进程增长。
- 状态：price_sensitivity_high_uniform_24590；formal_sensitivity_7_of_8_verified

### 2026-07-18 21:19 - price-sensitivity-high uniform checkpoint

- 进展：`price_sensitivity_high` uniform 写入 `uniform cache checkpoint: 26157 pairs`。
- 缓存：`price_sensitivity_high/uniform.pkl` 更新时间为 2026-07-18 21:18，大小 139,038,620 bytes；旧 `dynamic.pkl` 和旧 JSON 仍为 2026-07-16 工件。
- 资源：批次切换时曾短暂只看到 tracker；复查后 P 继续保持 8 个 worker 加 resource tracker，worker 接近满载，最近可用内存约 8.8 GiB，未见 OOM 或错误输出。
- 说明：当前有效运行从 2026-07-18 19:41 开始，旧 2026-07-16 结果因源码签名边界不能直接计入正式 8/8。
- 状态：price_sensitivity_high_uniform_26157；formal_sensitivity_7_of_8_verified

### 2026-07-18 21:28 - price-sensitivity-high 长批次诊断

- 现象：`price_sensitivity_high` 在 `uniform cache checkpoint: 26157 pairs` 后出现较长时间无新 stdout，但 8 个 worker 持续接近满载。
- 检查命令：
  ```bash
  rg -n "class PairEvaluator|checkpoint_interval|evaluate_many|evaluated_pairs|pair_cache|write_checkpoints|run_equilibria|candidate_count|maximum_joint_residual" experiments/run_final_spatiotemporal_equilibrium.py pricing_sim -g '*.py'
  sed -n '1,340p' experiments/equilibrium_run_support.py
  sed -n '1,360p' experiments/final_equilibrium_tools.py
  ```
- 诊断：`PairEvaluator.evaluate_many()` 使用 `ProcessPoolExecutor.map(..., chunksize=1)`，结果按输入顺序返回；若排在前面的 pair 较慢，后续已完成 pair 也不会马上进入 cache，因此 checkpoint 可能被单个慢 pair 阻塞。
- 约束：当前运行中不修改 Python 源码，避免最终工件记录的 source hash 与实际执行代码不一致。
- 决策：继续当前严格验证运行；若本轮失败或需要重启，再考虑把 `executor.map` 改为 `submit`/`as_completed`，使 checkpoint 不受输入顺序阻塞。
- 状态：price_sensitivity_high_long_batch_active；formal_sensitivity_7_of_8_verified

### 2026-07-18 21:35 - price-sensitivity-high 耗时来源补充

- 检查命令：
  ```bash
  rg -n "class IntermediarySearchSpec|def .*intermediary|minimize|timeout|maxiter|function_evaluations|successful_local_runs|evaluate_firm_pair_spatiotemporal" pricing_sim/intermediary_response.py pricing_sim/spatiotemporal_game.py pricing_sim/spatiotemporal_mechanism.py
  sed -n '1,320p' pricing_sim/intermediary_response.py
  sed -n '1,260p' pricing_sim/spatiotemporal_game.py
  rg -n "FIXED_POINT_MAX_ITER|FIXED_POINT_TOL|QOS_DAMPING" pricing_sim/peak_shaving_market.py pricing_sim/spatiotemporal_game.py tests -g '*.py'
  ```
- 诊断：每个 provider pair 会运行 deterministic multistart intermediary response；默认 3 个 route region，每个 region 一次 L-BFGS-B，本地优化上限为 `max_iterations=250`。
- 诊断：每次 objective evaluation 内部调用 spatiotemporal joint fixed point，`FIXED_POINT_MAX_ITER=200`、`FIXED_POINT_TOL=1e-9`、`QOS_DAMPING=0.35`。
- 含义：困难 pair 的耗时可能远高于 bimatrix solver 的单次 120s 边界；当前长批次更像是连续响应优化的尾部耗时，而不是 Nash solver 卡死。
- 决策：当前运行仍保持 8 worker 满载且内存稳定；不在运行中改源码，继续等待本批次完成。
- 状态：price_sensitivity_high_intermediary_tail_active；formal_sensitivity_7_of_8_verified

### 2026-07-18 21:43 - price-sensitivity-high 父进程内存检查

- 检查命令：
  ```bash
  P=$(pgrep -f "/bin/python.*scenario_names=\['price_sensitivity_high'\]" | head -1); echo P_PID=${P:-none}
  if [ -n "$P" ]; then
    ps -o pid,ppid,stat,etime,%cpu,rss,vsz,comm -p "$P" --ppid "$P"
  fi
  stat -c '%y %s %n' /root/.cache/peak_shaving_submission_sensitivity/price_sensitivity_high/uniform.pkl /root/.cache/peak_shaving_submission_sensitivity/price_sensitivity_high/dynamic.pkl artifacts/peak_shaving/20260712_expanded_response/sensitivity_price_sensitivity_high_submission.json 2>/dev/null
  free -m
  ```
- 结果：父进程 RSS 约 2.14 GiB，8 个 worker 各约 83 MiB；可用内存约 8.1 GiB，未见 OOM。
- 诊断：父进程内存偏高，符合 `executor.map` 顺序产出造成已完成结果暂存的可能性；目前 RSS 在相邻检查中基本稳定。
- 决策：暂不终止当前运行；若父进程 RSS 继续快速上涨并接近可用内存风险区，再停止并改为异步 `as_completed` 后重跑。
- 状态：price_sensitivity_high_parent_rss_stable；formal_sensitivity_7_of_8_verified

### 2026-07-18 21:50 - price-sensitivity-high 长批次继续运行

- 现象：自 2026-07-18 21:18 的 `uniform cache checkpoint: 26157 pairs` 后暂无新 checkpoint。
- 资源：父进程 RSS 约 2.16 GiB，8 个 worker 已运行约 32 分钟且继续接近满载；可用内存约 8.1 GiB，未见 OOM。
- 缓存：`uniform.pkl` 仍停在 2026-07-18 21:18，大小 139,038,620 bytes；`dynamic.pkl` 和最终 JSON 仍为旧工件。
- 判断：当前更像是 `executor.map` 的有序返回被慢前缀 pair 阻塞；父进程 RSS 缓慢上涨但仍稳定，暂不牺牲当前已算结果。
- 决策：继续等待；若 RSS 快速上涨或 worker 退出异常，再停止并修改回收逻辑后重跑。
- 状态：price_sensitivity_high_ordered_map_waiting；formal_sensitivity_7_of_8_verified

### 2026-07-18 22:01 - price-sensitivity-high 整点状态

- 进展：仍停留在 `uniform cache checkpoint: 26157 pairs`，暂无新 stdout。
- 资源：父进程 RSS 约 2.18 GiB；8 个 worker 已运行约 43 分钟且继续接近满载；可用内存约 7.9 GiB，未见 OOM。
- 缓存：`uniform.pkl` 更新时间仍为 2026-07-18 21:18，大小 139,038,620 bytes；`dynamic.pkl` 与最终 JSON 仍为 2026-07-16 旧工件。
- 判断：当前仍是有序 map 长批次等待；父进程 RSS 缓慢上涨但没有失控。
- 决策：继续等待当前批次；若到 22:18 仍无 checkpoint 且 RSS 继续上升，再重新评估是否终止并改异步结果回收。
- 状态：price_sensitivity_high_ordered_map_waiting_2201；formal_sensitivity_7_of_8_verified

### 2026-07-18 22:11 - price-sensitivity-high 进入 dynamic 阶段

- 进展：stdout 输出 `dynamic cache checkpoint: 78572 pairs`。
- 更正：结合 `uniform.pkl` 停在 2026-07-18 21:18、`dynamic.pkl` 于 2026-07-18 22:10 改写，可以判断 21:18 之后的长时间无 stdout 是 dynamic 阶段第一批任务，而不是 uniform 阶段继续卡住。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-18 22:10，大小 417,716,388 bytes；`uniform.pkl` 最终停在 2026-07-18 21:18，大小 139,038,620 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 2.62 GiB；8 个 worker 继续接近满载；可用内存约 7.4 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON，然后运行 `validate_sensitivity_scenario('price_sensitivity_high', ...)`。
- 状态：price_sensitivity_high_dynamic_78572；formal_sensitivity_7_of_8_verified

### 2026-07-18 22:18 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 78572 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-18 22:10，大小 417,716,388 bytes。
- 资源：父进程 RSS 约 2.63 GiB；8 个 worker 继续接近满载；可用内存约 7.8 GiB，未见 OOM。
- 判断：距上次 dynamic checkpoint 约 8 分钟，仍在正常长批次范围内。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_78572_waiting；formal_sensitivity_7_of_8_verified

### 2026-07-18 22:29 - price-sensitivity-high dynamic 长批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 78572 pairs`，最终 JSON 尚未改写。
- 资源：父进程 RSS 约 2.63 GiB；8 个 worker 继续接近满载；可用内存约 8.0 GiB，未见 OOM。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 22:10，大小 417,716,388 bytes。
- 判断：当前仍是 dynamic 阶段有序 map 长批次；内存稳定，继续等待比终止重跑更合理。
- 状态：price_sensitivity_high_dynamic_78572_waiting_2229；formal_sensitivity_7_of_8_verified

### 2026-07-18 22:38 - price-sensitivity-high dynamic 长批次继续

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 78572 pairs`，最终 JSON 尚未改写。
- 资源：父进程 RSS 约 2.64 GiB；8 个 worker 继续接近满载；可用内存约 8.0 GiB，未见 OOM。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 22:10，大小 417,716,388 bytes。
- 判断：第二个 dynamic 长批次仍在计算；资源稳定，继续等待。
- 状态：price_sensitivity_high_dynamic_78572_waiting_2238；formal_sensitivity_7_of_8_verified

### 2026-07-18 22:48 - price-sensitivity-high dynamic 长批次接近 40 分钟

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 78572 pairs`，最终 JSON 尚未改写。
- 资源：父进程 RSS 约 2.65 GiB；8 个 worker 继续接近满载；可用内存约 7.8 GiB，未见 OOM。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 22:10，大小 417,716,388 bytes。
- 判断：等待时间较长，但内存和 worker 状态稳定；当前终止会丢失 22:10 后未写入 cache 的计算。
- 决策：继续等待，不中断当前运行。
- 状态：price_sensitivity_high_dynamic_78572_waiting_2248；formal_sensitivity_7_of_8_verified

### 2026-07-18 22:56 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 86764 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-18 22:55，大小 461,266,755 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 2.77 GiB；8 个 worker 继续接近满载；可用内存约 7.4 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_86764；formal_sensitivity_7_of_8_verified

### 2026-07-18 23:02 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 86764 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-18 22:55，大小 461,266,755 bytes。
- 资源：父进程 RSS 约 2.78 GiB；8 个 worker 继续接近满载；可用内存约 7.4 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_86764_waiting_2302；formal_sensitivity_7_of_8_verified

### 2026-07-18 23:14 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 86764 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 22:55，大小 461,266,755 bytes。
- 资源：父进程 RSS 约 2.79 GiB；8 个 worker 继续接近满载；可用内存约 7.3 GiB，未见 OOM。
- 判断：当前仍是 dynamic 阶段长批次等待；资源稳定，继续运行。
- 状态：price_sensitivity_high_dynamic_86764_waiting_2314；formal_sensitivity_7_of_8_verified

### 2026-07-18 23:24 - price-sensitivity-high dynamic 长批次继续

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 86764 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 22:55，大小 461,266,755 bytes。
- 资源：父进程 RSS 约 2.79 GiB；8 个 worker 继续接近满载；available 内存约 7.3 GiB，未见 OOM。
- 判断：当前批次持续时间较长，但资源稳定；不终止当前运行。
- 状态：price_sensitivity_high_dynamic_86764_waiting_2324；formal_sensitivity_7_of_8_verified

### 2026-07-18 23:34 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 86764 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 22:55，大小 461,266,755 bytes。
- 资源：父进程 RSS 约 2.80 GiB；8 个 worker 继续接近满载；available 内存约 7.5 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_86764_waiting_2334；formal_sensitivity_7_of_8_verified

### 2026-07-18 23:41 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 86764 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 22:55，大小 461,266,755 bytes。
- 资源：主进程运行约 4 小时；父进程 RSS 约 2.80 GiB；8 个 worker 继续接近满载；available 内存约 7.5 GiB，未见 OOM。
- 判断：当前为长批次等待；系统资源稳定，不中断。
- 状态：price_sensitivity_high_dynamic_86764_waiting_2341；formal_sensitivity_7_of_8_verified

### 2026-07-18 23:43 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 94956 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-18 23:42，大小 504,817,597 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 2.92 GiB；8 个 worker 继续接近满载；available 内存约 7.4 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_94956；formal_sensitivity_7_of_8_verified

### 2026-07-18 23:49 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 94956 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 23:42，大小 504,817,597 bytes。
- 资源：父进程 RSS 约 2.92 GiB；8 个 worker 继续接近满载；available 内存约 7.1 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_94956_waiting_2349；formal_sensitivity_7_of_8_verified

### 2026-07-18 23:55 - price-sensitivity-high dynamic 内存状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 94956 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 23:42，大小 504,817,597 bytes。
- 资源：父进程 RSS 约 2.93 GiB；8 个 worker 继续接近满载；available 内存约 6.3 GiB，未见 OOM。
- 判断：`free` 较低但 `available` 仍足够；后续重点监控 `MemAvailable`，若接近 3 GiB 再重新评估是否中断重跑优化版。
- 状态：price_sensitivity_high_dynamic_94956_waiting_memory_watch；formal_sensitivity_7_of_8_verified

### 2026-07-19 00:02 - price-sensitivity-high 跨日状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 94956 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 23:42，大小 504,817,597 bytes。
- 资源：主进程运行约 4 小时 22 分钟；父进程 RSS 约 2.93 GiB；8 个 worker 继续接近满载；available 内存约 6.85 GiB，未见 OOM。
- 判断：运行已跨到 2026-07-19；当前仍是 dynamic 阶段长批次等待。
- 状态：price_sensitivity_high_dynamic_94956_waiting_0002；formal_sensitivity_7_of_8_verified

### 2026-07-19 00:10 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 94956 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 23:42，大小 504,817,597 bytes。
- 资源：主进程运行约 4 小时 30 分钟；父进程 RSS 约 2.94 GiB；8 个 worker 继续接近满载；available 内存约 6.95 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_94956_waiting_0010；formal_sensitivity_7_of_8_verified

### 2026-07-19 00:19 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 94956 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 23:42，大小 504,817,597 bytes。
- 资源：主进程运行约 4 小时 39 分钟；父进程 RSS 约 2.94 GiB；8 个 worker 继续接近满载；available 内存约 6.94 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_94956_waiting_0019；formal_sensitivity_7_of_8_verified

### 2026-07-19 00:29 - price-sensitivity-high dynamic 内存状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 94956 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-18 23:42，大小 504,817,597 bytes。
- 资源：父进程 RSS 约 2.95 GiB；8 个 worker 继续接近满载；`free` 内存约 130 MiB，但 available 内存约 6.9 GiB，未见 OOM。
- 判断：低 `free` 主要来自 Linux page cache，当前仍以 `MemAvailable` 为准；暂不中断。
- 状态：price_sensitivity_high_dynamic_94956_waiting_0029；formal_sensitivity_7_of_8_verified

### 2026-07-19 00:35 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 103148 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 00:35，大小 548,369,442 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.07 GiB；8 个 worker 继续接近满载；available 内存约 6.8 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_103148；formal_sensitivity_7_of_8_verified

### 2026-07-19 00:42 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 103148 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 00:35，大小 548,369,442 bytes。
- 资源：主进程运行约 5 小时 2 分钟；父进程 RSS 约 3.07 GiB；8 个 worker 继续接近满载；available 内存约 6.74 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_103148_waiting_0042；formal_sensitivity_7_of_8_verified

### 2026-07-19 00:49 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 103148 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 00:35，大小 548,369,442 bytes。
- 资源：主进程运行约 5 小时 9 分钟；父进程 RSS 约 3.07 GiB；8 个 worker 继续接近满载；available 内存约 6.75 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_103148_waiting_0049；formal_sensitivity_7_of_8_verified

### 2026-07-19 00:56 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 103148 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 00:35，大小 548,369,442 bytes。
- 资源：主进程运行约 5 小时 16 分钟；父进程 RSS 约 3.08 GiB；8 个 worker 继续接近满载；available 内存约 7.17 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_103148_waiting_0056；formal_sensitivity_7_of_8_verified

### 2026-07-19 01:04 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 103148 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 00:35，大小 548,369,442 bytes。
- 资源：主进程运行约 5 小时 24 分钟；父进程 RSS 约 3.08 GiB；8 个 worker 继续接近满载；available 内存约 7.16 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_103148_waiting_0104；formal_sensitivity_7_of_8_verified

### 2026-07-19 01:11 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 103148 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 00:35，大小 548,369,442 bytes。
- 资源：主进程运行约 5 小时 31 分钟；父进程 RSS 约 3.09 GiB；8 个 worker 继续接近满载；available 内存约 7.16 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_103148_waiting_0111；formal_sensitivity_7_of_8_verified

### 2026-07-19 01:19 - price-sensitivity-high dynamic 状态

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 103148 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 00:35，大小 548,369,442 bytes。
- 资源：主进程运行约 5 小时 39 分钟；父进程 RSS 约 3.09 GiB；8 个 worker 继续接近满载；available 内存约 7.14 GiB，未见 OOM。
- 判断：长批次持续，但资源稳定；不终止当前运行。
- 状态：price_sensitivity_high_dynamic_103148_waiting_0119；formal_sensitivity_7_of_8_verified

### 2026-07-19 01:28 - price-sensitivity-high dynamic checkpoint 与混合求解

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 111340 pairs` 和 `111356 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 01:27，大小 592,005,856 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：主进程 RSS 约 3.22 GiB；后续出现多个大 RSS 子进程，推断为混合均衡求解阶段的 fork 子进程；available 内存约 4.15 GiB，未见 OOM。
- 判断：动态 pair evaluation 已继续推进，当前很可能进入 restricted mixed-equilibrium 求解或后续 full-deviation 批次准备；RSS 会因 fork 继承地址空间而高估实际独占内存。
- 决策：继续运行，密切监控 `MemAvailable` 和最终 JSON 是否改写。
- 状态：price_sensitivity_high_dynamic_111356; formal_sensitivity_7_of_8_verified

### 2026-07-19 01:30 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 111356 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 01:27，大小 592,005,856 bytes。
- 资源：前一轮大 RSS fork 子进程已退出，当前回到 8 个正常 worker；父进程 RSS 约 3.22 GiB；available 内存约 7.1 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_111356_waiting_0130；formal_sensitivity_7_of_8_verified

### 2026-07-19 01:38 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 111356 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 01:27，大小 592,005,856 bytes。
- 资源：后续批次已运行约 9 分钟；父进程 RSS 约 3.22 GiB；8 个 worker 继续接近满载；available 内存约 7.1 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_111356_waiting_0138；formal_sensitivity_7_of_8_verified

### 2026-07-19 01:40 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 112932 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 01:39，大小 600,384,446 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.22 GiB；8 个 worker 继续接近满载；available 内存约 7.1 GiB，未见 OOM。
- 判断：本次增量约 1,576 pairs，符合一轮 full-grid deviation 扫描的规模特征。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_112932；formal_sensitivity_7_of_8_verified

### 2026-07-19 01:47 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 112932 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 01:39，大小 600,384,446 bytes。
- 资源：后续批次已运行约 8 分钟；父进程 RSS 约 3.23 GiB；8 个 worker 继续接近满载；available 内存约 7.1 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_112932_waiting_0147；formal_sensitivity_7_of_8_verified

### 2026-07-19 01:49 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 114508 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 01:48，大小 608,762,870 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.25 GiB；8 个 worker 继续接近满载；available 内存约 7.05 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_114508；formal_sensitivity_7_of_8_verified

### 2026-07-19 01:56 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 114508 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 01:48，大小 608,762,870 bytes。
- 资源：后续批次已运行约 7.5 分钟；父进程 RSS 约 3.26 GiB；8 个 worker 继续接近满载；available 内存约 7.05 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_114508_waiting_0156；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:00 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 116084 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 01:58，大小 617,141,378 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.29 GiB；8 个 worker 继续接近满载；available 内存约 7.02 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_116084；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:09 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 117660 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 02:07，大小 625,519,852 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.32 GiB；8 个 worker 继续接近满载；available 内存约 7.0 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_117660；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:17 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 119236 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 02:16，大小 633,898,195 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.35 GiB；8 个 worker 继续接近满载；available 内存约 6.95 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_119236；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:23 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 119236 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 02:16，大小 633,898,195 bytes。
- 资源：后续批次已运行约 6.5 分钟；父进程 RSS 约 3.35 GiB；8 个 worker 继续接近满载；available 内存约 6.94 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_119236_waiting_0223；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:27 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 120812 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 02:26，大小 642,276,665 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.38 GiB；8 个 worker 继续接近满载；available 内存约 6.92 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_120812；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:33 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 120812 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 02:26，大小 642,276,665 bytes。
- 资源：后续批次已运行约 7 分钟；父进程 RSS 约 3.38 GiB；8 个 worker 继续接近满载；available 内存约 6.9 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_120812_waiting_0233；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:35 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 122388 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 02:35，大小 650,655,007 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.42 GiB；8 个 worker 继续接近满载；available 内存约 6.88 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_122388；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:41 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 122388 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 02:35，大小 650,655,007 bytes。
- 资源：后续批次已运行约 6.7 分钟；父进程 RSS 约 3.42 GiB；8 个 worker 继续接近满载；available 内存约 6.86 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_122388_waiting_0241；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:45 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 123964 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 02:44，大小 659,033,387 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.44 GiB；8 个 worker 继续接近满载；available 内存约 6.84 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_123964；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:51 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 123964 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 02:44，大小 659,033,387 bytes。
- 资源：后续批次已运行约 7 分钟；父进程 RSS 约 3.45 GiB；8 个 worker 继续接近满载；available 内存约 6.84 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_123964_waiting_0251；formal_sensitivity_7_of_8_verified

### 2026-07-19 02:55 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 125540 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 02:54，大小 667,411,871 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.47 GiB；8 个 worker 继续接近满载；available 内存约 6.81 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_125540；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:01 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 125540 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 02:54，大小 667,411,871 bytes。
- 资源：后续批次已运行约 7 分钟；父进程 RSS 约 3.48 GiB；8 个 worker 继续接近满载；available 内存约 6.8 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_125540_waiting_0301；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:03 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 127116 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 03:02，大小 675,790,286 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.51 GiB；8 个 worker 继续接近满载；available 内存约 6.78 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_127116；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:09 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 127116 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 03:02，大小 675,790,286 bytes。
- 资源：后续批次已运行约 7 分钟；父进程 RSS 约 3.51 GiB；8 个 worker 继续接近满载；available 内存约 6.76 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_127116_waiting_0309；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:12 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 128692 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 03:12，大小 684,168,812 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.54 GiB；8 个 worker 继续接近满载；available 内存约 6.75 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_128692；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:18 - price-sensitivity-high dynamic 后续批次

- 进展：dynamic 阶段仍停留在 `dynamic cache checkpoint: 128692 pairs`，最终 JSON 尚未改写。
- 缓存：`dynamic.pkl` 更新时间仍为 2026-07-19 03:12，大小 684,168,812 bytes。
- 资源：后续批次已运行约 6.5 分钟；父进程 RSS 约 3.54 GiB；8 个 worker 继续接近满载；available 内存约 6.74 GiB，未见 OOM。
- 决策：继续等待 dynamic 阶段完成。
- 状态：price_sensitivity_high_dynamic_128692_waiting_0318；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:22 - price-sensitivity-high dynamic checkpoint

- 进展：dynamic 阶段写入 `dynamic cache checkpoint: 130268 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 03:21，大小 692,547,369 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：父进程 RSS 约 3.57 GiB；8 个 worker 继续接近满载；available 内存约 6.70 GiB，未见 OOM。
- 判断：本次继续增加约 1,576 pairs，符合连续 full-grid deviation 扫描模式。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_130268；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:27 - price-sensitivity-high 用户状态核验

- 目标：回应当前正在运行的实验及长时间未结束的原因，并确认运行状态。
- 命令：
  ```bash
  date '+%F %T %Z'
  ps -o pid,ppid,stat,etime,%cpu,rss,vsz,comm -p 2565619 --ppid 2565619 | sed -n '1,24p'
  stat -c '%y %s %n' /root/.cache/peak_shaving_submission_sensitivity/price_sensitivity_high/dynamic.pkl artifacts/peak_shaving/20260712_expanded_response/sensitivity_price_sensitivity_high_submission.json 2>/dev/null
  free -m
  ```
- 进展：当前有效运行是 `price_sensitivity_high`，父进程已运行约 7 小时 47 分钟；不是单次有效运行连续两天。
- 缓存：最近有效 checkpoint 仍为 `dynamic cache checkpoint: 130268 pairs`；`dynamic.pkl` 更新时间为 2026-07-19 03:21，大小 692,547,369 bytes。
- 工件：正式输出 `sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，不能计入当前 8/8。
- 资源：8 个 worker 均接近 100% CPU；父进程 RSS 约 3.57 GiB；available 内存约 6.70 GiB，当前没有 OOM 或退出迹象。
- 判断：运行慢的直接原因是 dynamic 阶段在持续加入支持策略并反复扫描全网格 deviation；每轮 checkpoint 只增加约 1,576 pairs，终止条件取决于 regret gate，不是固定总量。
- 决策：继续监控；只有 stdout 出现 `finished price_sensitivity_high`、JSON 更新时间更新，并通过 `validate_sensitivity_scenario('price_sensitivity_high', ...)` 后，才更新正式 8/8 证据。
- 状态：price_sensitivity_high_dynamic_130268_waiting_0327；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:33 - price-sensitivity-high dynamic checkpoint

- 进展：stdout 写入 `dynamic cache checkpoint: 131844 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 03:31，大小 700,926,024 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：8 个 worker 继续接近满载；父进程 RSS 约 3.60 GiB；available 内存约 6.67 GiB，未见 OOM。
- 判断：较上一 checkpoint 增加约 1,576 pairs，证明当前批次继续推进。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_131844；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:42 - price-sensitivity-high dynamic checkpoint

- 进展：stdout 写入 `dynamic cache checkpoint: 133420 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 03:41，大小 709,304,604 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：8 个 worker 继续接近满载；父进程 RSS 约 3.63 GiB；available 内存约 6.63 GiB，未见 OOM。
- 判断：较上一 checkpoint 增加约 1,576 pairs，运行节奏仍一致。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_133420；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:51 - price-sensitivity-high dynamic checkpoint

- 进展：stdout 写入 `dynamic cache checkpoint: 134996 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 03:50，大小 717,683,051 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：8 个 worker 继续接近满载；父进程 RSS 约 3.66 GiB；available 内存约 6.59 GiB，未见 OOM。
- 判断：较上一 checkpoint 增加约 1,576 pairs，运行仍在推进。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_134996；formal_sensitivity_7_of_8_verified

### 2026-07-19 03:59 - price-sensitivity-high dynamic checkpoint

- 进展：stdout 写入 `dynamic cache checkpoint: 136572 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 03:59，大小 726,061,413 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：8 个 worker 继续接近满载；父进程 RSS 约 3.69 GiB；available 内存约 6.57 GiB，未见 OOM。
- 判断：较上一 checkpoint 增加约 1,576 pairs，运行仍在推进。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_136572；formal_sensitivity_7_of_8_verified

### 2026-07-19 04:09 - price-sensitivity-high dynamic checkpoint

- 进展：stdout 写入 `dynamic cache checkpoint: 138148 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 04:08，大小 734,440,047 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：8 个 worker 继续接近满载；父进程 RSS 约 3.73 GiB；available 内存约 6.51 GiB，未见 OOM。
- 判断：较上一 checkpoint 增加约 1,576 pairs，运行仍在推进。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_138148；formal_sensitivity_7_of_8_verified

### 2026-07-19 04:19 - price-sensitivity-high dynamic checkpoint

- 进展：stdout 写入 `dynamic cache checkpoint: 139724 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 04:18，大小 742,818,542 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：8 个 worker 继续接近满载；父进程 RSS 约 3.76 GiB；available 内存约 6.50 GiB，未见 OOM。
- 判断：较上一 checkpoint 增加约 1,576 pairs，运行仍在推进。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_139724；formal_sensitivity_7_of_8_verified

### 2026-07-19 04:28 - price-sensitivity-high dynamic checkpoint

- 进展：stdout 写入 `dynamic cache checkpoint: 141300 pairs`。
- 缓存：`dynamic.pkl` 更新时间为 2026-07-19 04:27，大小 751,197,047 bytes。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 仍为 2026-07-16 旧 JSON，当前不能计入正式 8/8。
- 资源：8 个 worker 继续接近满载；父进程 RSS 约 3.79 GiB；available 内存约 6.46 GiB，未见 OOM。
- 判断：较上一 checkpoint 增加约 1,576 pairs，运行仍在推进。
- 决策：继续等待 dynamic 阶段完成并写出最终 JSON。
- 状态：price_sensitivity_high_dynamic_141300；formal_sensitivity_7_of_8_verified

### 2026-07-19 04:37 - price-sensitivity-high 正式完成

- 目标：完成最后一个正式敏感性场景 `price_sensitivity_high`，并将正式进度从 7/8 推进到 8/8。
- 命令：
  ```bash
  env TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -c "import json; from experiments.run_submission_spatiotemporal_sensitivity import run_sensitivity; result=run_sensitivity(scenario_names=['price_sensitivity_high'], parallel_workers=8); print(json.dumps(result['rows'], indent=2), flush=True)"
  ```
- 输出：stdout 写入 `dynamic cache checkpoint: 142876 pairs`，随后输出 `finished price_sensitivity_high: regret=2.274e-13, peak=-11.98%`，会话退出码为 0。
- 工件：`sensitivity_price_sensitivity_high_submission.json` 更新时间为 2026-07-19 04:37，大小 455,394 bytes，SHA-256 为 `ff73e94eaebace997531c03f4304ce79f3aee860a089f2708bb1267b9f8e46a7`。
- 指标：uniform/dynamic evaluated pairs 为 `26,157/142,876`；support 为 `5-by-5/16-by-16`；dynamic full regret 为 `2.2737367544323206e-13`；最大 joint residual 为 `9.99648919197682e-10`；峰值变化为 `-11.982843172521866%`。
- 判断：当前有效运行自 2026-07-18 19:41 左右启动，约 8 小时 56 分钟完成；此前 2026-07-16 旧 JSON 仅为历史工件，未计入本轮正式证据。
- 状态：price_sensitivity_high_completed；formal_sensitivity_8_of_8_pending_validation

### 2026-07-19 04:38 - price-sensitivity-high 单场景门禁验证

- 命令：
  ```bash
  uv run --no-project --with-requirements requirements.txt python - <<'PY'
  import hashlib, json
  from pathlib import Path
  from experiments.submission_evidence_gates import validate_sensitivity_scenario
  out = Path('artifacts/peak_shaving/20260712_expanded_response')
  baseline_path = out / 'spatiotemporal_equilibrium_submission.json'
  artifact_path = out / 'sensitivity_price_sensitivity_high_submission.json'
  baseline = json.loads(baseline_path.read_text(encoding='utf-8'))
  artifact = json.loads(artifact_path.read_text(encoding='utf-8'))
  expected_hash = hashlib.sha256(baseline_path.read_bytes()).hexdigest()
  print(json.dumps(validate_sensitivity_scenario(
      'price_sensitivity_high',
      artifact,
      expected_hash=expected_hash,
      expected_baseline=baseline,
  ), indent=2))
  PY
  ```
- 结果：`passed=true`；provenance `passed=true`；`source_count=20`；uniform/dynamic full regret 分别为 `1.1368683772161603e-13` 和 `2.2737367544323206e-13`；active profile counts 为 `25/256`。
- 决策：`price_sensitivity_high` 可计入本轮正式 8/8 敏感性证据。
- 状态：price_sensitivity_high_validated；formal_sensitivity_8_of_8_verified

### 2026-07-19 04:39 - 九场景 summary、claims 与 sensitivity table

- 目标：在 8/8 单场景门禁通过后，生成正式九行敏感性 summary、机器可读 claims 和 LaTeX 表格。
- 命令：
  ```bash
  uv run --no-project --with-requirements requirements.txt python - <<'PY'
  import json
  from experiments.run_submission_spatiotemporal_sensitivity import SUMMARY_PATH, collect_sensitivity_summary
  result = collect_sensitivity_summary()
  SUMMARY_PATH.write_text(json.dumps(result, indent=2), encoding='utf-8')
  print(json.dumps({
      'output': str(SUMMARY_PATH),
      'scenario_count': result['metadata']['scenario_count'],
      'baseline_sha256': result['metadata']['baseline_sha256'],
  }, indent=2))
  PY
  uv run --no-project --with-requirements requirements.txt python -m experiments.build_submission_sensitivity_claims
  uv run --no-project --with-requirements requirements.txt python -m experiments.build_submission_sensitivity_table
  sha256sum artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_sensitivity_submission.json artifacts/peak_shaving/20260712_expanded_response/sensitivity_claims_submission.json artifacts/peak_shaving/20260712_expanded_response/submission_sensitivity_table.tex
  ```
- 输出：`spatiotemporal_sensitivity_submission.json` 的 `scenario_count=9`，baseline SHA-256 为 `70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`。
- SHA-256：summary 为 `7bfbd0d471a73ffe23b50034c463b536c9ea0e601a86e7c6f59f8d8bbaa41626`；claims 为 `9d9bf3fd7d1b9689b82888fc365ce5f61f7d9e2b1882b6000cafe5b3fe15a558`；table 为 `203b1fc8199154c9ba63559d16ccb9bda8781e4327275efc6dd95f9d4f63ba98`。
- 结论：九场景有限候选敏感性 summary 已生成；峰值和最大利用率在九行中均下降，最低 QoS 均增加；市场侧利润不是稳健同号，9 行中 3 个为负、6 个为正。
- 状态：sensitivity_summary_claims_table_generated；formal_sensitivity_8_of_8_verified

### 2026-07-19 04:41 - 8/8 敏感性文档与测试验证

- 目标：同步正式 8/8 状态到证据文档和回归契约，并验证新生成 summary、claims 与 table 的生成器契约。
- 修改：更新 `ARTIFACT_MANIFEST.md`、`docs/reviews/smpt_submission_evidence_map_2026-07-14.md`、`docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md` 和 `tests/test_submission_augmented_evidence_contract.py`；把 sensitivity 状态从 7/8 更新到 8/8，并记录 `price_sensitivity_high`、summary、claims 与 table SHA。
- 命令：
  ```bash
  git diff --check -- README.md ARTIFACT_MANIFEST.md docs/reviews/smpt_submission_evidence_map_2026-07-14.md docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md tests/test_submission_augmented_evidence_contract.py
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_augmented_evidence_contract.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_evidence_gates.py -q -k 'sensitivity_scenario or sensitivity_summary or sensitivity_claims or uniform_offgrid or provider_payoff'
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 60s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_sensitivity_claims.py tests/test_submission_sensitivity_table.py tests/test_submission_spatiotemporal_sensitivity.py -q
  ```
- 结果：`git diff --check` 退出码 0；增强证据契约测试 `9 passed in 0.25s`；evidence gates 目标子集 `6 passed, 76 deselected in 0.28s`；summary/table/claims 相关测试 `13 passed in 0.23s`。
- 限制：未运行完整 combined evidence gate，因为当前已知 baseline artifact 的记录源码哈希仍不匹配求解器补丁后的 live worktree；该问题需要后续 baseline-dependent audit rebuild 处理。
- 状态：formal_sensitivity_8_of_8_verified；summary_claims_table_verified；combined_baseline_provenance_gate_still_pending

### 2026-07-19 12:10 - post-sensitivity figure/manuscript gate triage

- 目标：按 8/8 敏感性完成后的真实论文状态继续推进 Figure 6、主稿和派生审计门禁。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_submission_figures.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_manuscript_20260714.py -q
  ```
- 结果：figure builder 测试为 `2 failed, 8 passed`，失败原因是 `mixed_outcome_distribution_submission.json` 仍绑定旧 equilibrium SHA `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`，不匹配当前基准 `70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`；主稿测试为 `3 failed, 50 passed`，失败点是 Figure 6 和 sensitivity table 尚未接入，以及测试断言仍检查过时的 partial sensitivity 状态。
- 诊断：敏感性本身已经 8/8 通过；当前红灯转移到依赖当前基准的派生工件重建，包括 mixed distribution、mechanism decomposition、baseline off-grid、fixed-point audit、intermediary audit、uniform off-grid sensitivity 和 provider-payoff sensitivity。
- 决策：先重建可直接绑定当前基准的派生审计工件，再生成 `resolved_sensitivity.pdf/.png` 并接入主稿。
- 状态：post_sensitivity_rebuild_in_progress

### 2026-07-19 12:44 - baseline-dependent audit artifact rebuild

- 目标：在 8/8 敏感性验证后，按当前 baseline SHA `70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226` 重建 Figure 6 和主稿依赖的派生审计工件。
- 已完成命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -m experiments.build_submission_mixed_distribution
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -m experiments.run_submission_mechanism_decomposition
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -m experiments.run_submission_fixed_point_audit
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -m experiments.run_submission_intermediary_audit
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -m experiments.build_submission_intermediary_payoff_sensitivity
  ```
- 已完成输出：`mixed_outcome_distribution_submission.json` active profiles 为 `676`，maximum reconstruction error 为 `1.3642420526593924e-12`；`mechanism_decomposition_submission.json` 为 `8` rows 且 `all_converged=true`；`fixed_point_multistart_audit_submission.json` covered probability mass 为 `1.0000000000000002` 且 all starts converged；`intermediary_globality_audit_submission.json` covered probability mass 为 `1.0000000000000002`，maximum profit improvement 为 `0.10267809887176327`；`intermediary_payoff_sensitivity_submission.json` maximum active support regret 为 `1.1641169265477629`。
- 当前阻塞项：`spatiotemporal_offgrid_diagnostic_submission.json` 仍是 2026-07-14 旧工件，记录 equilibrium SHA 为 `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`，不能用于当前基准。
- 当前运行命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -c 'import json; from experiments.run_spatiotemporal_offgrid_diagnostic import OUTPUT_PATH, ROOT, run_offgrid_diagnostic; result = run_offgrid_diagnostic(parallel_workers=32); OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True); OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8"); print(json.dumps({"output": str(OUTPUT_PATH.relative_to(ROOT)), "firm_A_regret": result["players"]["firm_A"]["offgrid_regret"], "firm_B_regret": result["players"]["firm_B"]["offgrid_regret"]}, indent=2))'
  ```
- 当前进展：baseline off-grid 从默认 `16` worker 在 `firm_A/global_guard: evaluated 128/1544 candidates (3328 pairs)` 处 checkpoint 后，切换为 `32` worker 续跑；已确认缓存复用正常，并推进到 `firm_A/global_guard: evaluated 192/1544 candidates (4992 pairs)`。
- 决策：继续完成 baseline off-grid，随后运行 `run_submission_uniform_offgrid_audit`，再重跑 final figure 和 manuscript tests。
- 状态：baseline_offgrid_running_from_checkpoint

### 2026-07-19 13:52 - manuscript sensitivity integration during off-grid run

- 目标：在 baseline off-grid 长任务运行期间，先修正主稿 sensitivity 接入结构和过时测试断言。
- 修改：`tests/test_final_manuscript_20260714.py` 不再要求旧的“其余 5 个场景”表述，改为要求 theory audit 包含 8/8 个正式场景；`peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 在 sensitivity subsection 中接入 `submission_sensitivity_table.tex` 和 `resolved_sensitivity.pdf`。
- 命令：
  ```bash
  git diff --check -- README.md tests/test_final_manuscript_20260714.py peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：`git diff --check` 退出码 0。
- 当前 off-grid 进展：`firm_A/global_guard` 已推进到 `896/1544 candidates (23296 pairs)`；缓存 `~/.cache/peak_shaving_submission_offgrid/firm_A.pkl` 更新时间为 2026-07-19 13:49，大小约 `117M`。
- 限制：`resolved_sensitivity.pdf` 仍需等待 baseline off-grid 与 uniform off-grid 工件齐全后由 `experiments.build_final_submission_figures` 生成；当前不能运行 final figure/manuscript 通过性验证。
- 状态：manuscript_sensitivity_structure_updated；baseline_offgrid_running

### 2026-07-19 17:57 - baseline off-grid diagnostic completed

- 目标：为当前 baseline SHA 重建 `spatiotemporal_offgrid_diagnostic_submission.json`，解除 final figure gate 中旧 equilibrium SHA 绑定问题。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -c 'import json; from experiments.run_spatiotemporal_offgrid_diagnostic import OUTPUT_PATH, ROOT, run_offgrid_diagnostic; result = run_offgrid_diagnostic(parallel_workers=32); OUTPUT_PATH.parent.mkdir(parents=True, exist_ok=True); OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8"); print(json.dumps({"output": str(OUTPUT_PATH.relative_to(ROOT)), "firm_A_regret": result["players"]["firm_A"]["offgrid_regret"], "firm_B_regret": result["players"]["firm_B"]["offgrid_regret"]}, indent=2))'
  ```
- 输出：
  ```json
  {
    "output": "artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_offgrid_diagnostic_submission.json",
    "firm_A_regret": 3.34471800063875,
    "firm_B_regret": 3.51130144859178
  }
  ```
- 校验命令：
  ```bash
  jq '{generated_at:.metadata.generated_at,equilibrium_sha256:.metadata.equilibrium_sha256,samples:.metadata.samples_per_player,workers:.metadata.parallel_workers,firm_A:.players.firm_A.offgrid_regret,firm_B:.players.firm_B.offgrid_regret,firm_A_rel:.players.firm_A.relative_offgrid_regret,firm_B_rel:.players.firm_B.relative_offgrid_regret,firm_A_candidates:.players.firm_A.evaluated_candidates,firm_B_candidates:.players.firm_B.evaluated_candidates}' artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_offgrid_diagnostic_submission.json
  sha256sum artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_offgrid_diagnostic_submission.json
  ```
- 校验结果：`generated_at=2026-07-19T17:57:12+08:00`；`equilibrium_sha256=70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`；samples 为 `1024`；workers 为 `32`；evaluated candidates 为 firm A `1720`、firm B `1699`；relative regrets 为 firm A `0.004002458302554513`、firm B `0.004733110489296879`。
- SHA-256：`257c3906190d1441c23fcaa3a21f9fedac750e430177ad020811b697b6066b06`。
- 决策：baseline off-grid 已绑定当前 equilibrium SHA，可进入 uniform off-grid sensitivity audit 重建；随后再运行 final figure 和 manuscript gates。
- 状态：baseline_offgrid_verified；uniform_offgrid_pending

### 2026-07-19 17:58 - uniform off-grid audit started

- 目标：重建 `uniform_offgrid_audit_submission.json`，使 Figure 6 依赖的 uniform baseline sensitivity audit 与当前 equilibrium SHA 一致。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -c 'import json; from experiments.run_submission_uniform_offgrid_audit import OUTPUT_PATH, ROOT, run_uniform_offgrid_audit; result = run_uniform_offgrid_audit(parallel_workers=32); OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8"); print(json.dumps({"output": str(OUTPUT_PATH.relative_to(ROOT)), "scenario_count": result["metadata"]["scenario_count"]}, indent=2))'
  ```
- 当前输出：启动后前 30 秒暂无 stdout 批次进度。
- 决策：继续监控长任务；完成后记录 scenario count、metadata SHA 和文件 SHA，再运行 final figure gate。
- 状态：uniform_offgrid_running

### 2026-07-19 19:32 - uniform off-grid baseline scenario progress

- 目标：记录 `uniform_offgrid_audit` 在 baseline scenario 上的阶段性完成状态。
- 已观察输出：
  ```text
  firm_A/global_guard: evaluated 1042/1042 candidates (10420 pairs)
  firm_A/local_refinement: evaluated 289/289 candidates (2890 pairs)
  firm_B/global_guard: evaluated 1042/1042 candidates (10420 pairs)
  firm_B/local_refinement: evaluated 289/289 candidates (2890 pairs)
  ```
- 缓存：`~/.cache/peak_shaving_uniform_offgrid/baseline/firm_A.pkl`、`firm_A_local.pkl`、`firm_B.pkl` 和 `firm_B_local.pkl` 已生成或更新。
- 判断：baseline scenario 的 uniform off-grid 两个 firm 均已完成 global guard 和 local refinement；任务仍在运行，尚未写出最终 `uniform_offgrid_audit_submission.json`。
- 下一步：继续监控后续 8 个 sensitivity scenario，待命令完成后记录 artifact metadata 与 SHA。
- 状态：uniform_offgrid_baseline_scenario_done；uniform_offgrid_running

### 2026-07-19 22:25 - uniform off-grid capacity-low scenario progress

- 目标：记录 `uniform_offgrid_audit` 在 `capacity_low` scenario 上的阶段性完成状态。
- 已观察输出：
  ```text
  firm_A/global_guard: evaluated 1050/1050 candidates (18900 pairs)
  firm_A/local_refinement: evaluated 289/289 candidates (5202 pairs)
  firm_B/global_guard: evaluated 1050/1050 candidates (18900 pairs)
  firm_B/local_refinement: evaluated 289/289 candidates (5202 pairs)
  ```
- 缓存：`~/.cache/peak_shaving_uniform_offgrid/capacity_low/firm_A.pkl`、`firm_A_local.pkl`、`firm_B.pkl` 和 `firm_B_local.pkl` 已生成或更新。
- 判断：`capacity_low` scenario 的 uniform off-grid 两个 firm 均已完成 global guard 和 local refinement；任务仍在运行，尚未写出最终 `uniform_offgrid_audit_submission.json`。
- 下一步：继续监控剩余 sensitivity scenarios，待命令完成后记录 artifact metadata 与 SHA。
- 状态：uniform_offgrid_capacity_low_done；uniform_offgrid_running

### 2026-07-19 22:53 - uniform off-grid capacity-high scenario progress

- 目标：记录 `uniform_offgrid_audit` 在 `capacity_high` scenario 上的阶段性完成状态。
- 已观察输出：
  ```text
  firm_A/global_guard: evaluated 1035/1035 candidates (3105 pairs)
  firm_A/local_refinement: evaluated 289/289 candidates (867 pairs)
  firm_B/global_guard: evaluated 1035/1035 candidates (3105 pairs)
  firm_B/local_refinement: evaluated 289/289 candidates (867 pairs)
  ```
- 缓存：`~/.cache/peak_shaving_uniform_offgrid/capacity_high/firm_A.pkl`、`firm_A_local.pkl`、`firm_B.pkl` 和 `firm_B_local.pkl` 已生成或更新。
- 判断：`capacity_high` scenario 的 active opponent support 较小，pairs 明显少于 `capacity_low`，两个 firm 均已完成 global guard 和 local refinement；任务仍在运行，尚未写出最终 `uniform_offgrid_audit_submission.json`。
- 下一步：继续监控剩余 sensitivity scenarios，待命令完成后记录 artifact metadata 与 SHA。
- 状态：uniform_offgrid_capacity_high_done；uniform_offgrid_running

### 2026-07-20 01:41 - uniform off-grid price-sensitivity-low scenario progress

- 目标：记录 `uniform_offgrid_audit` 在 `price_sensitivity_low` scenario 上的阶段性完成状态，并确认任务已进入下一 sensitivity scenario。
- 已观察输出：
  ```text
  firm_A/global_guard: evaluated 1052/1052 candidates (21040 pairs)
  firm_A/local_refinement: evaluated 289/289 candidates (5780 pairs)
  firm_B/global_guard: evaluated 1052/1052 candidates (21040 pairs)
  firm_B/local_refinement: evaluated 289/289 candidates (5780 pairs)
  firm_A/global_guard: evaluated 64/1037 candidates (320 pairs)
  ```
- 缓存：`~/.cache/peak_shaving_uniform_offgrid/price_sensitivity_low/firm_A.pkl`、`firm_A_local.pkl`、`firm_B.pkl` 和 `firm_B_local.pkl` 已生成或更新；`~/.cache/peak_shaving_uniform_offgrid/price_sensitivity_high/firm_A.pkl` 已开始写入。
- 判断：`price_sensitivity_low` scenario 的两个 firm 均已完成 global guard 和 local refinement；任务已进入 `price_sensitivity_high`，该场景初始 pairs 数明显较低。
- 下一步：继续监控剩余 sensitivity scenarios，待命令完成后记录 artifact metadata 与 SHA，并运行 final figure 和 manuscript gates。
- 状态：uniform_offgrid_price_sensitivity_low_done；uniform_offgrid_running

### 2026-07-20 02:25 - uniform off-grid price-sensitivity-high scenario progress

- 目标：记录 `uniform_offgrid_audit` 在 `price_sensitivity_high` scenario 上的阶段性完成状态。
- 已观察输出：
  ```text
  firm_A/global_guard: evaluated 1037/1037 candidates (5185 pairs)
  firm_A/local_refinement: evaluated 289/289 candidates (1445 pairs)
  firm_B/global_guard: evaluated 1037/1037 candidates (5185 pairs)
  firm_B/local_refinement: evaluated 289/289 candidates (1445 pairs)
  ```
- 缓存：`~/.cache/peak_shaving_uniform_offgrid/price_sensitivity_high/firm_A.pkl`、`firm_A_local.pkl`、`firm_B.pkl` 和 `firm_B_local.pkl` 已生成或更新。
- 判断：`price_sensitivity_high` scenario 的 active opponent support 较小，两个 firm 均已完成 global guard 和 local refinement；任务仍在运行，尚未写出最终 `uniform_offgrid_audit_submission.json`。
- 下一步：继续监控剩余 sensitivity scenarios，待命令完成后记录 artifact metadata 与 SHA，并运行 final figure 和 manuscript gates。
- 状态：uniform_offgrid_price_sensitivity_high_done；uniform_offgrid_running

### 2026-07-20 03:39 - uniform off-grid migration-cost-low scenario progress

- 目标：记录 `uniform_offgrid_audit` 在 `migration_cost_low` scenario 上的阶段性完成状态。
- 已观察输出：
  ```text
  firm_A/global_guard: evaluated 1041/1041 candidates (9369 pairs)
  firm_A/local_refinement: evaluated 289/289 candidates (2601 pairs)
  firm_B/global_guard: evaluated 1041/1041 candidates (9369 pairs)
  firm_B/local_refinement: evaluated 289/289 candidates (2601 pairs)
  ```
- 缓存：`~/.cache/peak_shaving_uniform_offgrid/migration_cost_low/firm_A.pkl`、`firm_A_local.pkl`、`firm_B.pkl` 和 `firm_B_local.pkl` 已生成或更新。
- 判断：`migration_cost_low` scenario 的两个 firm 均已完成 global guard 和 local refinement；任务仍在运行，尚未写出最终 `uniform_offgrid_audit_submission.json`。
- 下一步：继续监控剩余 sensitivity scenarios，待命令完成后记录 artifact metadata 与 SHA，并运行 final figure 和 manuscript gates。
- 状态：uniform_offgrid_migration_cost_low_done；uniform_offgrid_running

### 2026-07-20 05:00 - uniform off-grid migration-cost-high scenario progress

- 目标：记录 `uniform_offgrid_audit` 在 `migration_cost_high` scenario 上的阶段性完成状态。
- 已观察输出：
  ```text
  firm_A/global_guard: evaluated 1042/1042 candidates (10420 pairs)
  firm_A/local_refinement: evaluated 289/289 candidates (2890 pairs)
  firm_B/global_guard: evaluated 1042/1042 candidates (10420 pairs)
  firm_B/local_refinement: evaluated 289/289 candidates (2890 pairs)
  ```
- 缓存：`~/.cache/peak_shaving_uniform_offgrid/migration_cost_high/firm_A.pkl`、`firm_A_local.pkl`、`firm_B.pkl` 和 `firm_B_local.pkl` 已生成或更新。
- 判断：`migration_cost_high` scenario 的两个 firm 均已完成 global guard 和 local refinement；任务仍在运行，尚未写出最终 `uniform_offgrid_audit_submission.json`。
- 下一步：继续监控剩余 QoS threshold sensitivity scenarios，待命令完成后记录 artifact metadata 与 SHA，并运行 final figure 和 manuscript gates。
- 状态：uniform_offgrid_migration_cost_high_done；uniform_offgrid_running

### 2026-07-20 06:24 - uniform off-grid qos-threshold-low scenario progress

- 目标：记录 `uniform_offgrid_audit` 在 `qos_threshold_low` scenario 上的阶段性完成状态。
- 已观察输出：
  ```text
  firm_A/global_guard: evaluated 1042/1042 candidates (10420 pairs)
  firm_A/local_refinement: evaluated 289/289 candidates (2890 pairs)
  firm_B/global_guard: evaluated 1042/1042 candidates (10420 pairs)
  firm_B/local_refinement: evaluated 289/289 candidates (2890 pairs)
  ```
- 缓存：`~/.cache/peak_shaving_uniform_offgrid/qos_threshold_low/firm_A.pkl`、`firm_A_local.pkl`、`firm_B.pkl` 和 `firm_B_local.pkl` 已生成或更新。
- 判断：`qos_threshold_low` scenario 的两个 firm 均已完成 global guard 和 local refinement；任务仍在运行，尚未写出最终 `uniform_offgrid_audit_submission.json`。
- 下一步：继续监控最后一个 `qos_threshold_high` scenario，待命令完成后记录 artifact metadata 与 SHA，并运行 final figure 和 manuscript gates。
- 状态：uniform_offgrid_qos_threshold_low_done；uniform_offgrid_running

### 2026-07-20 07:11 - uniform off-grid sensitivity audit completed

- 目标：完成 `uniform_offgrid_audit` 全部 9 个 scenario，生成与当前 baseline SHA 绑定的 Figure 6 uniform off-grid sensitivity artifact。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -c 'import json; from experiments.run_submission_uniform_offgrid_audit import OUTPUT_PATH, ROOT, run_uniform_offgrid_audit; result = run_uniform_offgrid_audit(parallel_workers=32); OUTPUT_PATH.write_text(json.dumps(result, indent=2), encoding="utf-8"); print(json.dumps({"output": str(OUTPUT_PATH.relative_to(ROOT)), "scenario_count": result["metadata"]["scenario_count"]}, indent=2))'
  ```
- 输出：
  ```json
  {
    "output": "artifacts/peak_shaving/20260712_expanded_response/uniform_offgrid_sensitivity_submission.json",
    "scenario_count": 9
  }
  ```
- 校验命令：
  ```bash
  jq '{generated_at:.metadata.generated_at,scenario_count:.metadata.scenario_count,workers:.metadata.parallel_workers,baseline_sha256:.metadata.baseline_sha256,source_sha256:.metadata.source_sha256}' artifacts/peak_shaving/20260712_expanded_response/uniform_offgrid_sensitivity_submission.json
  sha256sum artifacts/peak_shaving/20260712_expanded_response/uniform_offgrid_sensitivity_submission.json
  ```
- 校验结果：`generated_at=2026-07-20T07:11:51+08:00`；`scenario_count=9`；`parallel_workers=32`；`baseline_sha256=70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`。
- SHA-256：`abb58fe6b5e6eb8204e1089f4acb1f8fcb3b47df897d3878ec7c79fbe8768674`。
- 场景摘要：baseline firm A/B regret 为 `23.809526882714067` / `15.027428848422687`；capacity low 为 `14.733569013152419` / `16.168784754621925`；capacity high 为 `11.499437468910742` / `5.488913302839933`；price sensitivity low 为 `27.56727727973953` / `15.245976115477447`；price sensitivity high 为 `15.568018339247942` / `14.9813094420698`；migration cost low 为 `24.172800407820887` / `14.923636082989674`；migration cost high 为 `23.471436252668127` / `14.682505668595809`；QoS threshold low 为 `23.31755117894329` / `11.090608412656252`；QoS threshold high 为 `23.45502025189819` / `12.97456191146523`。
- 决策：uniform off-grid sensitivity artifact 已绑定当前 baseline SHA，可继续运行 final figure gate 和 final manuscript gate。
- 状态：uniform_offgrid_verified；final_figure_gate_pending

### 2026-07-20 07:16 - final figure gate stale key repair

- 目标：运行 final figure gate，确认 Figure 6 依赖的最终 artifact 是否已与当前 baseline SHA 对齐。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_submission_figures.py -q
  ```
- 结果：`1 failed, 9 passed`；唯一失败为 `test_final_figure_builder_uses_only_final_artifacts`，测试仍期望旧 key `provider_payoff_sensitivity`，而 `experiments/build_final_submission_figures.py`、工件路径和绘图逻辑均使用 `intermediary_payoff_sensitivity`。
- 修改：`tests/test_final_submission_figures.py` 将 expected data key 从 `provider_payoff_sensitivity` 调整为 `intermediary_payoff_sensitivity`。
- 决策：这是测试命名滞后，不改变 Figure builder 行为和 artifact 命名。
- 状态：final_figure_gate_retest_pending

### 2026-07-20 07:17 - final figure gate verified

- 目标：重跑 final figure gate，确认 Figure builder 与最终 artifact key 一致。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_submission_figures.py -q
  ```
- 结果：`10 passed in 2.25s`。
- 决策：final figure gate 已通过，可生成最终 `peak_shaving_final_20260714` figure PDF/PNG。
- 状态：final_figure_gate_verified；final_figures_build_pending

### 2026-07-20 07:18 - final submission figures rebuilt

- 目标：基于当前 final artifact 重建主稿引用的最终图表，特别是新增接入的 `resolved_sensitivity.pdf/.png`。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 nice -n 10 uv run --no-project --with-requirements requirements.txt python -m experiments.build_final_submission_figures
  ```
- 输出：生成 `figures/peak_shaving_final_20260714/input_calibration.pdf/.png`、`equilibrium_profiles.pdf/.png`、`mechanism_decomposition.pdf/.png`、`resolved_sensitivity.pdf/.png` 和 `solver_diagnostics.pdf/.png`。
- 文件检查：PDF 大小分别约 `31K`、`33K`、`26K`、`34K`、`33K`；PNG 大小分别约 `127K`、`331K`、`142K`、`208K`、`168K`。
- SHA-256：`resolved_sensitivity.pdf=f2d9ca1b2aa676b30da56f99efc78a3fa0ce3f4d451bf5894dff9e7dd4b833ce`；`solver_diagnostics.pdf=48510984cc5d912536b6718edb9ce0e97c2482c2d07c91ec34710746a4bbed53`。
- 决策：最终图表已生成，继续重跑 final figure gate 和 final manuscript gate。
- 状态：final_figures_rebuilt；final_gates_pending

### 2026-07-20 07:19 - final manuscript prose artifact sync

- 目标：重跑 final figure gate 和 final manuscript gate，确认主稿正文与当前 artifact 一致。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_submission_figures.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_manuscript_20260714.py -q
  ```
- 结果：final figure gate 为 `10 passed in 2.20s`；final manuscript gate 为 `2 failed, 51 passed`。
- 失败原因：主稿正文仍保留旧 artifact 数值，`spatiotemporal_offgrid_diagnostic_submission.json` 当前最大 active-support payoff error 为 `$6.82\times10^{-13}$`；`mechanism_decomposition_submission.json` 当前 spatial-only maximum provider utilization change 为 `4.32\%`，minimum QoS change 为 `0.0265`。
- 修改：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 同步上述三个正文数值。
- 状态：final_manuscript_gate_retest_pending

### 2026-07-20 07:20 - final manuscript gate verified

- 目标：重跑 final manuscript gate，确认主稿正文数值、图表引用和 sensitivity 接入均与当前 artifact 一致。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_manuscript_20260714.py -q
  ```
- 结果：`53 passed in 0.32s`。
- 决策：final manuscript gate 已通过，继续运行 whitespace diff check 和 LaTeX 编译验证。
- 状态：final_manuscript_gate_verified；latex_compile_pending

### 2026-07-20 07:21 - final manuscript latex compile verified

- 目标：验证主稿 LaTeX 能完整编译，并确认新增 sensitivity table 与 `resolved_sensitivity.pdf` 引用可解析。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 180s nice -n 10 latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 结果：编译退出码 0，生成 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.pdf`，共 24 页，大小约 `454K`。
- SHA-256：`43c5faff53551b7070605a2f3456964167f70833a1b06d74265e2f4cc6483821`。
- 编译警告：`submission_sensitivity_table.tex` 在 lines 9--24 有 `Overfull \hbox (2.95963pt too wide)`；未出现未定义引用或 fatal error。
- 决策：PDF 编译可用；该 overfull 警告较小，暂不影响当前验证结论。
- 状态：latex_compile_verified

### 2026-07-20 13:16 - full evidence gate audit found blocking evidence drift

- 目标：对最终 PDF、图表和主稿门禁通过后的投稿证据链做综合审查。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_evidence_gates.py -q
  ```
- 结果：`11 failed, 71 passed in 0.88s`。
- 主要失败：`spatiotemporal_equilibrium_submission.json` 记录的 solver 来源哈希与当前工作区源码不一致。`pricing_sim/bimatrix_solver.py` 记录 `90312a7fe9188adb6ab8a810ad05eafa75a81ca43342561c66c34e9bea1b3214`，当前为 `c79aec6bfd8c639f8698e20000d2094715862aae19d9a994891ce6f9a92dd687`；`pricing_sim/milp_equilibrium_solver.py` 记录 `db224d7a87a9b4b04dff63a8ae5579e2a6774b1d440a08631e8461c89780587f`，当前为 `f7a19c835e5c75c1d1a66566f401ef574f9018302b8a002dd3ddf8b09a435c0b`。
- 隔离诊断：在内存中仅把 artifact 的 `source_sha256` 临时替换为当前源码哈希后，`build_gate_report()` 仍返回 `passed=false`，失败项为 `uniform_offgrid: baseline/firm_A: relative off-grid regret exceeds the gate`、`equilibrium_branch: branch audit baseline SHA-256 does not match`、`price_shape_audit: dependent artifact equilibrium SHA-256 does not match`。
- 数值诊断：`uniform_offgrid_sensitivity_submission.json` 的 9 个场景、18 个 firm 均超过现有 `0.5%` relative off-grid regret 门槛，且 active-support payoff error 均超过 `1e-6`。baseline firm A/B 的 relative regret 分别为 `2.8185%` 和 `2.0997%`。
- 旧 SHA 诊断：`equilibrium_branch_audit_submission.json` 仍绑定旧 baseline SHA `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`；`price_shape_decomposition_submission.json` 仍绑定旧 equilibrium SHA `d37174453530ad67754da2303bc1e85374053efd53cec90d9824e65f5a3aae2f`。
- 决策：不能把当前论文状态声明为 full evidence gate passed。下一步先刷新可重建的派生审计文件；uniform off-grid 的门禁失败需要在论文中降级为诊断性证据，或重新设计并重求 uniform baseline/sensitivity 证据链。
- 状态：full_evidence_gate_blocked；derived_audit_refresh_pending

### 2026-07-20 13:20 - derived audits refreshed and manuscript reverified

- 目标：刷新可重建的旧 SHA 派生审计文件，并使主稿正文重新匹配当前 artifact。
- 命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt python -m experiments.run_submission_price_shape_decomposition
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 timeout 180s nice -n 10 uv run --no-project --with-requirements requirements.txt python -m experiments.run_submission_equilibrium_branch_audit
  ```
- 输出：`price_shape_decomposition_submission.json` 已绑定当前 equilibrium SHA `70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`，`all_converged=true`，`maximum_residual=9.9884045479115e-10`；`equilibrium_branch_audit_submission.json` 已绑定当前 baseline SHA，`successful_starts=66`，`branch_count=1`。
- SHA-256：`price_shape_decomposition_submission.json=b8e16bf9b944c5ea9984129b097ba1bed21a4db7bf643c6294c340cade4c21ad`；`equilibrium_branch_audit_submission.json=14d6882e2e67f31ed8804327a3dcf23d9bd1942c117bc6ecc9a0f03418c7b36a`。
- 测试：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_evidence_gates.py -q -k 'branch or price_shape'
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_manuscript_20260714.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_submission_figures.py -q
  ```
- 测试结果：branch/price-shape 证据门禁为 `14 passed, 68 deselected in 0.29s`；final manuscript gate 修正文稿数值后为 `53 passed in 0.31s`；final figure gate 为 `10 passed in 2.47s`。
- 主稿同步：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 将 branch restricted matrix 改为 `$26\times26$`，branch starts 改为 `66/66`，branch full-candidate regret 改为 `$3.41\times10^{-13}$`；Table~\ref{tab:price_shape_decomposition} 同步当前 price-shape components。
- LaTeX 编译：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 180s nice -n 10 latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 0，PDF 为 24 页，大小 `464272` bytes，SHA-256 `911b6b5c66e9442d85cd0bc2c3d029cb9428da3f53ede0d153c6cbd0fc3e2440`。仍有 `submission_sensitivity_table.tex` lines 9--24 的 `Overfull \hbox (2.95963pt too wide)` 警告。
- Full evidence gate 状态：官方 `tests/test_submission_evidence_gates.py -q` 仍为 `11 failed, 71 passed`，失败先触发当前 solver 源码与 equilibrium artifact 的来源哈希不一致；在仅内存替换 source hashes 的隔离诊断下，剩余失败降为 1 项，即 `uniform_offgrid: baseline/firm_A: relative off-grid regret exceeds the gate`。
- 决策：当前可验证部分是 final figure、final manuscript、branch/price-shape 派生审计和 LaTeX 编译；投稿前 full evidence gate 尚未通过，阻塞项为 solver provenance 漂移与 uniform off-grid 严格数值门禁。
- 状态：final_pdf_reverified；full_evidence_gate_blocked

### 2026-07-20 13:24 - academic plain-language polish planned

- 目标：根据反馈把英文主稿改得更接近正式学术论文，同时减少生硬、晦涩和连续否定的表达。
- 背景：上一轮已验证 final figure、final manuscript、branch/price-shape 派生审计和 LaTeX 编译；full evidence gate 仍因 solver provenance 与 uniform off-grid 门禁阻塞。
- 操作：只润色 `peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 的正文叙事、限制表述和段落连接；不新增参考文献，不改变 artifact 数值，不改实验结论。
- 命令：尚未运行修改后验证命令。
- 输入：用户反馈“贴近学术一些，不要用太过苦涩的词”。
- 输出：待生成。
- 决策：优先处理 abstract、introduction、related work positioning、results interpretation、limitations 和 conclusion；保留证据边界，但把连续的 `not/does not/cannot` 改写为范围限定或条件解释。
- 下一步：修改主稿并复跑 final manuscript gate 与 LaTeX 编译。
- 状态：in_progress

### 2026-07-20 13:28 - academic plain-language polish verified

- 目标：验证主稿学术化、清晰化润色后仍与 artifact 和 LaTeX 编译要求一致。
- 修改：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex` 润色 abstract、introduction、related work positioning、input interpretation、main comparison、numerical checks、limitations 和 conclusion。修改保留所有数值、公式、引用键和证据边界；未新增参考文献。
- 写作策略：将连续否定句改为范围限定和解释性表述，例如把 production 与 continuous-equilibrium 边界写成 calibrated simulation scope；把 limitations 段调整为研究范围说明，而不是审计式问题清单。
- 测试命令：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_final_manuscript_20260714.py -q
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 120s nice -n 10 uv run --no-project --with-requirements requirements.txt --with pytest python -m pytest tests/test_submission_augmented_manuscript_contract.py tests/test_submission_augmented_evidence_contract.py -q
  git diff --check -- peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex README.md tests/test_final_manuscript_20260714.py
  ```
- 测试结果：final manuscript gate 为 `53 passed in 0.40s`；augmented manuscript/evidence contracts 为 `13 passed in 0.30s`；`git diff --check` 无输出。
- LaTeX 编译：
  ```bash
  TMPDIR=/tmp TEMP=/tmp TMP=/tmp timeout 180s nice -n 10 latexmk -xelatex -interaction=nonstopmode -halt-on-error peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex
  ```
- 编译结果：退出码 0，PDF 为 24 页，大小 `464742` bytes，SHA-256 `0feb13e201466a6aca640b0d527be96c62795004ef52e6c16cc6e4ece37153b5`；TeX 源文件 SHA-256 `bba94b0354d6033dccb9b556383a213e85e774601f1bc52e2b198655366b18c5`。
- 编译警告：`submission_sensitivity_table.tex` lines 9--24 仍有 `Overfull \hbox (2.95963pt too wide)`；未出现 undefined references 或 fatal error。
- Full evidence gate 状态：本轮为语言润色，未改变 full evidence gate 的既有阻塞；solver provenance 与 uniform off-grid strict gate 仍需另行处理。
- 状态：academic_plain_language_polish_verified；full_evidence_gate_blocked
