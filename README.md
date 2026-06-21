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
