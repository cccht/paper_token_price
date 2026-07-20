# SMPT Submission Portal Fields

> **Historical portal text, do not paste into Editorial Manager.** The title,
> abstract, keywords, highlights, 225-point results, outside-option statement,
> and release link below have all been superseded. Current portal fields will be
> generated only from the gated final manuscript.

Target journal: *Simulation Modelling Practice and Theory*  
Prepared: 2026-06-21  
Release:
`https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21`

Use this file to copy stable manuscript fields into the Elsevier submission
system. Author-specific fields are intentionally left out or marked separately
in `smpt_author_information_form_2026-06-21.md`.

## Article Type

Research article

## Title

A Simulation-Based Study of Time-of-Use Pricing for Fixed-Capacity Inference
Services: Provider Competition, QoS Protection, and the Profit Boundary

## Short Title

Time-of-Use Pricing for Fixed-Capacity Inference Services

## Abstract

Large language model (LLM) inference services operate under short-run fixed graphics processing unit (GPU) capacity, while time-varying arrivals can create costly off-peak idleness and peak quality-of-service (QoS) degradation. This paper develops an auditable simulation model to test whether time-of-use pricing can shift time-flexible inference demand away from congested periods and protect QoS without capacity expansion. The model combines two heterogeneous inference providers, one application programming interface (API) intermediary, time-rigid and time-flexible users, direct access, and an outside option. Provider prices use a low-dimensional time-shape family, and provider competition is approximated through fictitious play with finite-grid regret checks. Verification uses fixed-point residuals and solver traces; validation is bounded to public price scales and controlled vLLM overload measurements. In the congested uniform-pricing baseline, peak utilization is 0.782 and minimum QoS is 0.756. Dynamic coarse-grid and fine-grid snapshots reduce peak utilization to 0.706 and 0.666, respectively, and raise minimum QoS to 0.968 and 0.990. A double-oracle mixed-strategy check on the full 225-point grid gives a 5 x 5 support profile with maximum regret 0.203, expected peak utilization 0.703, and minimum QoS 0.970. Additional baselines and stress checks indicate that QoS gains are more reproducible than profit gains. Profit is unstable across solver objects: the coarse snapshot gives +9.3%, the fine snapshot gives -1.9%, and the low-regret mixed profile gives -2.8%. The results support time-of-use pricing as a QoS-protection instrument under fixed capacity, not as a reliable profit-improvement mechanism.

## Keywords

- inference-service simulation
- time-of-use pricing
- peak shaving
- fixed capacity
- QoS protection
- verification and validation
- finite-grid regret

## Highlights

- Simulates time-of-use pricing for fixed-capacity LLM inference services.
- Links user choice, API routing, capacity, and QoS feedback in one model.
- Mixed finite-grid check reaches max regret 0.203 on a 225-point grid.
- Dynamic prices improve congested QoS but do not robustly raise profit.
- Verification and stress tests define the simulation credibility boundary.

## Data And Code Availability

The code, simulation scripts, generated artifacts, and plotting pipeline used in
this study are available at https://github.com/cccht/paper_token_price. The
versioned submission-candidate release is available at
https://github.com/cccht/paper_token_price/releases/tag/smpt-submission-candidate-2026-06-21.
The archived release is available at [DOI, if created]. The manuscript
distinguishes synthetic calibration, public price anchors, and controlled vLLM
QoS-shape measurements.

## Declaration Of Generative AI And AI-Assisted Technologies

During manuscript preparation, AI-assisted tools were used for language
polishing, consistency checks, and internal reviewer-style checks. The authors
reviewed and edited the content as needed and remain responsible for the
simulation model, experimental artifacts, numerical results, interpretation, and
final text.

## Funding

Fill from `smpt_author_information_form_2026-06-21.md`.

## Declaration Of Competing Interests

Fill from `smpt_author_information_form_2026-06-21.md`.

## Author Contributions

Fill from `smpt_author_information_form_2026-06-21.md`.

## Suggested Reviewers

Not supplied. Add only real experts after author confirmation.
