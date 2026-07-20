# SMPT Elsevier Upload Checklist

> **Historical upload checklist, superseded.** The files and counts below refer
> to the 2026-06-20 draft, including a Figure 1 that is no longer used. Do not
> upload this package. The current formal Figure 1 is editable Draw.io artwork,
> and the new CAS checklist will be generated after the final numerical gates
> pass.

Target journal: *Simulation Modelling Practice and Theory*  
Publisher: Elsevier  
Prepared: 2026-06-21  
Submission-candidate release:
`https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`

## Ready Files

| Upload item | Local file | Status |
|---|---|---|
| Main manuscript PDF | `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.pdf` | Ready |
| Main manuscript TeX | `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex` | Ready |
| Bibliography | `verified_refs.bib` | Ready |
| Highlights | `docs/submission/smpt_highlights_2026-06-21.txt` | Ready |
| Cover letter draft | `docs/submission/smpt_cover_letter_draft_2026-06-21.md` | Needs author metadata |
| Declarations template | `docs/submission/smpt_declarations_template_2026-06-21.md` | Needs author metadata |
| Submission portal fields | `docs/submission/smpt_submission_portal_fields_2026-06-21.md` | Ready, except author-specific fields |
| Package manifest | `docs/submission/smpt_submission_package_manifest_2026-06-21.md` | Ready |
| Figure file inventory | `docs/submission/smpt_figure_file_inventory_2026-06-21.md` | Ready |

## Journal-Facing Checks Already Satisfied

- Abstract: exactly 250 words.
- Keywords: 7.
- Highlights: 5 items, each under 85 characters.
- Main manuscript includes a generative-AI declaration.
- Main manuscript includes data/code/release availability wording.
- All figures and tables are cited in the manuscript.
- Figure and table audits are documented under `docs/reviews/`.
- The manuscript compiles through XeLaTeX/BibTeX/XeLaTeX/XeLaTeX.
- The PDF is 23 A4 pages.

## Upload Order

1. Upload the main manuscript PDF.
2. Upload the TeX source and `verified_refs.bib` if the submission system asks
   for source files.
3. Upload highlights as a separate editable text file.
4. Upload the cover letter after author confirmation.
5. Upload declarations / CRediT / funding / competing-interest statements after
   author confirmation.
6. Upload figure files using the mapping in
   `smpt_figure_file_inventory_2026-06-21.md`.
7. Add the GitHub release URL as the data/code availability link.
8. Use `smpt_submission_portal_fields_2026-06-21.md` for title, abstract,
   keywords, highlights, data availability, and AI declaration fields.
9. Add an archival DOI only if the release has been mirrored to Zenodo, OSF, or
   another persistent archive.

## Must Be Filled By The Author Before Submission

- Author names, order, affiliations, emails, ORCID identifiers.
- Corresponding author and postal address if required.
- Confirmation that the manuscript is not under review elsewhere.
- Funding statement.
- Declaration of competing interests.
- CRediT roles.
- Acknowledgements, if any.
- Optional DOI/archive decision.
- Author artwork-policy decision for Figure 1: either recreate/export an
  author-approved non-AI artwork from the IoT draft, or confirm that the journal
  will accept the generated artwork with disclosure.

## Final Caution

The current review draft embeds an IoT-style generated PNG as Figure 1. Do not
upload it as final artwork unless the author has checked the journal policy and
decided to disclose that workflow. The safer route is to use it as a visual
guide and recreate/export author-approved artwork before formal submission.
