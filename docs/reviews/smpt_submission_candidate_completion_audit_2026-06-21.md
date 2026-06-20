# SMPT Submission-Candidate Completion Audit

Date: 2026-06-21  
Target journal: *Simulation Modelling Practice and Theory*  
Current manuscript: `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`  
Current release: `https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`

## Scope

This audit checks whether the requested manuscript work has reached a
submission-candidate state:

- use electricity dynamic-pricing papers as the structural template;
- optimize the manuscript's length, derivation detail, and results presentation;
- run reviewer-style checks and revise after them;
- inspect every figure for content and presentation problems;
- package a versioned submission candidate.

It does not fill author-only metadata such as author order, affiliations,
funding, competing interests, or CRediT roles.

## Requirement-by-Requirement Evidence

| Requirement | Evidence inspected | Status |
|---|---|---|
| Find electricity-related pricing papers and use their structure | `docs/reviews/power_pricing_structure_benchmark_2026-06-21.md` lists RTP/TOU/DR references, DOI checks, and the structural template. | Achieved |
| Align manuscript structure with electricity pricing / demand-response papers | Final manuscript sections follow motivation, related work, simulation model, solution method, V&V, experimental design, results, mechanism discussion, limitations, and conclusion. | Achieved |
| Keep the electricity analogy bounded | Final manuscript states that inference services are governed by GPU capacity, latency, completion, and routing rather than power-flow equations. | Achieved |
| Improve formula and derivation detail | Final TeX contains 19 displayed equation/align blocks covering utility, demand, load, QoS, profit, fixed-point evaluation, pure regret, and mixed regret. | Achieved |
| Improve results presentation | Final PDF contains 8 figures, 9 tables, baseline comparisons, regret diagnostics, SMPT baselines, ablations, stress tests, phase grid, local re-solve, and mechanism diagnostics. | Achieved |
| Use reviewer-style skills and revise after review | `docs/reviews/smpt_reviewer_round_2026-06-21.md` and `docs/reviews/smpt_final_gate_reviewer_report_2026-06-21.md` record reviewer-style critiques; later commits added release/package fixes and updated evidence boundaries. | Achieved |
| Inspect all figures carefully | `docs/reviews/smpt_full_figure_audit_2026-06-21.md` audits all 8 figures for reference order, caption/content consistency, visual readability, font/export checks, and numerical traceability. | Achieved |
| Ensure table values match artifacts | `docs/reviews/smpt_table_value_audit_2026-06-21.md` reports 74 checks and 0 issues. | Achieved |
| Compile the manuscript cleanly | Fresh XeLaTeX/BibTeX/XeLaTeX/XeLaTeX verification produced a 23-page A4 PDF with no LaTeX errors, undefined citations/references, overfull boxes, or rerun warnings in the checked logs. | Achieved |
| Meet core SMPT package constraints | Abstract is 250 words, keywords are 7, highlights are 5 lines under 85 characters, and data/AI declarations are present. | Achieved |
| Create a versioned submission package | GitHub release `smpt-submission-candidate-2026-06-21` exists, targets commit `195c60b`, is not draft/prerelease, and contains 8 submission assets. | Achieved |

## Remaining Author-Only Items

These items are not scientific-content blockers, but they are required before
pressing submit in Elsevier's system:

- final author names, order, affiliations, emails, ORCID identifiers, and
  corresponding author;
- confirmation that the manuscript is not under review elsewhere and has been
  approved by all authors;
- funding statement;
- declaration of competing interests;
- CRediT author contribution statement;
- acknowledgements, if any;
- persistent DOI if the authors choose to mirror the GitHub release to Zenodo,
  OSF, or another archive;
- author-approved export of Figure 1 from the Draw.io source before uploading
  final artwork.

## Judgment

The manuscript and reproducibility package are now a submission-candidate final
draft for author review. The remaining work is procedural and author-specific
rather than a missing modelling, experiment, figure, or manuscript-structure
component.
