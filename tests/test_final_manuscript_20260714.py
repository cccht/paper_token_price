import json
import inspect
from pathlib import Path
import re
import sys


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
MANUSCRIPT = ROOT / "peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex"
HIGHLIGHTS = ROOT / "docs/submission/simpat_highlights_final_2026-07-16.txt"
SENSITIVITY_TABLE_BUILDER = ROOT / "experiments/build_submission_sensitivity_table.py"
FIGURE_BUILDER = ROOT / "experiments/build_final_submission_figures.py"
EVIDENCE_MAP = ROOT / "docs/reviews/smpt_submission_evidence_map_2026-07-14.md"
THEORY_AUDIT = ROOT / "docs/reviews/smpt_theory_code_consistency_audit_2026-07-14.md"
DISTRIBUTION = (
    ROOT
    / "artifacts/peak_shaving/20260712_expanded_response"
    / "mixed_outcome_distribution_submission.json"
)
EQUILIBRIUM = (
    ROOT
    / "artifacts/peak_shaving/20260712_expanded_response"
    / "spatiotemporal_equilibrium_submission.json"
)
SUBMISSION_ARTIFACT_DIR = EQUILIBRIUM.parent
OFFGRID = SUBMISSION_ARTIFACT_DIR / "spatiotemporal_offgrid_diagnostic_submission.json"
BRANCH_AUDIT = SUBMISSION_ARTIFACT_DIR / "equilibrium_branch_audit_submission.json"
FIXED_POINT_AUDIT = SUBMISSION_ARTIFACT_DIR / "fixed_point_multistart_audit_submission.json"
INTERMEDIARY_AUDIT = SUBMISSION_ARTIFACT_DIR / "intermediary_globality_audit_submission.json"
MECHANISM_AUDIT = SUBMISSION_ARTIFACT_DIR / "mechanism_decomposition_submission.json"
PRICE_SHAPE_AUDIT = SUBMISSION_ARTIFACT_DIR / "price_shape_decomposition_submission.json"
CANDIDATE_MANIFEST = SUBMISSION_ARTIFACT_DIR / "candidate_manifest_submission.json"
RESULT_MACROS = SUBMISSION_ARTIFACT_DIR / "submission_result_macros.tex"


def _source() -> str:
    return MANUSCRIPT.read_text(encoding="utf-8")


def _latex_scientific(value: float, digits: int = 2) -> str:
    mantissa, exponent = f"{value:.{digits}e}".split("e")
    return rf"${mantissa}\times10^{{{int(exponent)}}}$"


def _compact_decimal(value: float) -> str:
    return f"{value:.7f}".rstrip("0").rstrip(".")


def test_manuscript_has_exactly_five_numbered_sections():
    sections = re.findall(r"^\\section\{([^}]+)\}", _source(), flags=re.MULTILINE)

    assert sections == [
        "Introduction",
        "Related work",
        "Methodology",
        "Experimental results",
        "Conclusions and future work",
    ]


def test_abstract_keywords_and_highlights_meet_smpt_limits():
    source = _source()
    abstract = source.split(r"\begin{abstract}", 1)[1].split(
        r"\end{abstract}", 1
    )[0]
    abstract_words = re.findall(r"[A-Za-z0-9][A-Za-z0-9.-]*", abstract)
    keywords = source.split(r"\textbf{Keywords:}", 1)[1].split("\n", 1)[0]
    keyword_count = len([item for item in keywords.split(";") if item.strip()])
    highlights = HIGHLIGHTS.read_text(encoding="utf-8").splitlines()

    assert len(abstract_words) <= 250
    assert 1 <= keyword_count <= 7
    assert 3 <= len(highlights) <= 5
    assert all(len(line) <= 85 for line in highlights)


def test_submission_figures_exist_and_are_referenced():
    source = _source()
    figures = re.findall(r"\\includegraphics(?:\[[^]]+\])?\{([^}]+)\}", source)
    expected = [
        "figures/peak_shaving_final_20260714/spatiotemporal_pricing_framework.pdf",
        "figures/peak_shaving_final_20260714/input_calibration.pdf",
        "figures/peak_shaving_final_20260714/equilibrium_profiles.pdf",
        "figures/peak_shaving_final_20260714/solver_diagnostics.pdf",
        "figures/peak_shaving_final_20260714/mechanism_decomposition.pdf",
        "figures/peak_shaving_final_20260714/resolved_sensitivity.pdf",
    ]

    assert figures == expected
    for figure in figures:
        assert (ROOT / figure).exists()
    for label in re.findall(r"\\label\{(fig:[^}]+)\}", source):
        assert source.count(rf"\ref{{{label}}}") >= 1


def test_resolved_sensitivity_table_and_figure_are_both_integrated():
    source = _source()
    result_section = source.split(
        r"\subsection{Sensitivity analysis}", 1
    )[1].split(r"\subsection{Interpretation and limitations}", 1)[0]

    assert (
        r"\input{artifacts/peak_shaving/20260712_expanded_response/"
        r"submission_sensitivity_table.tex}"
    ) in result_section
    assert r"\ref{tab:resolved_sensitivity}" in result_section
    assert r"\ref{fig:resolved_sensitivity}" in result_section


def test_citations_resolve_to_verified_bibliography():
    source = _source()
    bibliography = (ROOT / "verified_refs.bib").read_text(encoding="utf-8")
    cited = {
        key.strip()
        for group in re.findall(r"\\cite\{([^}]+)\}", source)
        for key in group.split(",")
    }
    available = set(re.findall(r"^@\w+\{([^,]+),", bibliography, flags=re.MULTILINE))

    assert cited <= available


def test_submission_text_has_no_result_placeholders_or_stale_main_values():
    source = _source()

    assert "FINAL_SENSITIVITY_RESULTS" not in source
    assert "17.08" not in source
    assert "0.888" not in source
    assert "0.976" not in source
    for obsolete in ("12.32", "15.70", "0.890", "0.959", "2.81"):
        assert obsolete not in source
    assert "submission_result_macros.tex" in source


def test_temporal_only_mechanism_value_is_not_treated_as_a_stale_main_result():
    source = _source()

    assert "temporal-only case reduces aggregate peak" in source
    assert "13.03\\%" in source
    assert "The three comparisons are not additive" in source
    assert "depend on the fixed channel shares and capacity-proportional routing" in source
    assert "fixed-share-weighted mean of the three channel utilities" in source


def test_claim_boundaries_remain_explicit():
    source = _source().lower()

    assert "synthetic economic calibration" in source
    assert "production forecast" in source
    assert "continuous-space equilibrium" in source
    assert "mixed distribution" in source


def test_uniform_baseline_is_identified_as_a_restricted_equilibrium():
    source = _source()

    assert source.count("equilibrium under the uniform-price restriction") >= 3
    assert "Relative to the uniform-price equilibrium" not in source
    assert "fixes all provider slopes and the intermediary retail slope at zero" in source
    assert "not an experiment that changes one posted price" in source


def test_destination_and_channel_choices_use_one_conserved_flow():
    source = _source()

    assert "two stages of one conserved flow, not two sources of demand" in source
    assert "conditional channel shares then allocate that same destination demand" in source


def test_price_shape_normalization_and_clip_bounds_are_self_contained():
    source = _source()

    assert r"d_\nu=\max_s|\nu_s-\bar\nu|" in source
    assert r"\ell_t=" in source
    assert r"0, & d_\nu=0" in source
    assert r"\operatorname{clip}(x,a,b)=\min\{\max\{x,a\},b\}" in source
    assert "Wholesale/direct posted-price bounds" in source
    assert r"$[0.25,0.90]/[0.45,2.10]$" in source


def test_price_rules_are_day_ahead_schedules_not_real_time_feedback():
    source = _source()

    assert "day-ahead time-of-use schedules" in source
    assert "fixed BurstGPT mean load signal" in source
    assert "do not update from realized within-day demand" in source


def test_joint_fixed_point_iteration_is_visible_in_the_pdf_source():
    source = _source()

    assert r"\mathcal F(\boldsymbol q,\boldsymbol r)" in source
    assert r"(1-\lambda)(\boldsymbol q^{(n)},\boldsymbol r^{(n)})" in source
    assert r"+\lambda\mathcal F(\boldsymbol q^{(n)},\boldsymbol r^{(n)})" in source


def test_verification_is_not_presented_as_market_level_validation():
    source = _source()

    assert r"\cite{sargent2013verification}" in source
    assert "distinguish model verification from validation against an observed system" in source
    assert "they do not validate the market-level outcomes" in source


def test_intermediary_target_is_distinguished_from_numerical_response():
    source = _source()

    assert r"b^*(i,j)\in\argmax" in source
    assert r"\widehat b(i,j)" in source
    assert r"U^A_{ij}=\Pi_A(i,j,\widehat b(i,j))" in source
    assert "declared finite game under the evaluated numerical payoffs" in source
    assert "starts from unit QoS and equal routing" in source
    assert "A nonconvergent evaluation is not admitted" in source
    assert "Within an intermediary search, a response evaluation is discarded" in source
    assert "A candidate is excluded if the joint fixed point fails" not in source
    assert "no analytical existence or uniqueness result is claimed" in source


def test_primary_intermediary_optimizer_settings_are_reported():
    source = _source()

    assert "allows at most 250 iterations" in source
    assert r"objective-reduction and projected-gradient tolerances are $10^{-10}$ and $10^{-8}$" in source
    assert "at most 30 line-search steps" in source
    assert r"\tau_I=\max\{10^{-8},10^{-10}\max(|\Pi_I|,1)\}" in source


def test_nash_conditions_explain_why_no_closed_form_tariff_is_claimed():
    source = _source()

    assert "these conditions do not yield a closed-form tariff" in source
    assert "equilibrium of the declared finite game is therefore obtained numerically" in source


def test_finite_game_simplex_and_unit_vectors_are_defined():
    source = _source()

    assert r"n_A=n_B=|\Sset|=1576" in source
    assert r"\Delta_n=\{\boldsymbol z\in\mathbb R_+^n" in source
    assert "corresponding unit vector" in source


def test_complementarity_solver_settings_are_reported():
    source = _source()

    assert "allows 5,000 function evaluations" in source
    assert r"three least-squares tolerances are $10^{-13}$" in source
    assert r"$10^{-5},10^{-6},10^{-7},10^{-8},10^{-9}$" in source
    assert r"normalized-game regret is at most $10^{-9}$" in source


def test_payoff_normalization_is_defined_for_regular_and_constant_matrices():
    source = _source()

    assert r"\widetilde U=" in source
    assert r"\frac{U-\min U}{\max U-\min U}" in source
    assert r"\max U>\min U" in source
    assert r"\boldsymbol 0, & \max U=\min U" in source
    assert "applies the following normalization separately to each provider's payoff matrix" in source


def test_manuscript_uses_american_spelling_except_journal_name():
    source = _source()
    british_variants = re.compile(
        r"\b(?:utilised|utilisation|behaviour|behavioural|normalisation|"
        r"optimiser|summarises|discretises)\b",
        flags=re.IGNORECASE,
    )

    assert not british_variants.search(source)


def test_temporal_boundary_condition_is_explicit():
    source = _source()

    assert "does not wrap across the day boundary" in source
    assert r"s\in\T:\,|s-o|\le H_k" in source
    assert r"0, & \text{otherwise}" in source
    assert "excludes movement across adjacent days" in source


def test_numerical_audit_coverage_boundary_is_explicit():
    source = _source()

    assert "all 676 positive-probability provider pairs" in source
    assert "rather than all cached pairs or every sensitivity equilibrium" in source
    assert "destination pattern matters more than the total amount moved" in source


def test_flexible_destination_centroid_is_defined():
    source = _source()

    assert r"C_k=" in source
    assert r"t\,\mathbb E[\widetilde D_{k,t}]" in source
    assert "period indices are one based" in source
    assert "lower value denotes an earlier average destination period" in source


def test_qos_function_and_reported_minimum_use_distinct_symbols():
    source = _source()

    assert r"q_{m,t}=Q(u_{m,t})" in source
    assert r"L_{\mathrm{peak}}&=\mathbb E" in source
    assert r"u_{\max}&=\mathbb E" in source
    assert r"q_{\min}&=\mathbb E" in source
    assert r"\overline{\Pi}_M&=\mathbb E" in source
    assert "Q&=\\mathbb E" not in source


def test_mixed_qos_extrema_are_not_conflated_after_rounding():
    source = _source()

    assert "expected QoS curves rises from 0.9012 to \\DynamicMinimumQoS{}" in source
    assert r"$\mathbb E[\min_{m,t}q_{m,t}]=\DynamicMinimumQoS$" in source
    assert "the values differ before rounding" in source


def test_data_availability_does_not_claim_an_unreleased_archive():
    source = _source()

    assert "have not yet been frozen or pushed" in source
    assert "persistent archive identifier" in source


def test_sensitivity_scope_is_local_and_preserves_structural_ratios():
    source = _source()

    assert "local, one-factor-at-a-time perturbations" in source
    assert r"preserves the baseline ratio $G_A/G_B=2.5$" in source
    assert r"preserving $\alpha_F/\alpha_R=2.5$" in source
    assert r"Because $\phi_R=H_R=0$" in source
    assert "it does not estimate interactions among parameters" in source
    assert "not alternative forms of market heterogeneity" in source
    assert "QoS choice and routing weights, QoS curvature, and cost coefficients are held fixed" in source


def test_parameter_table_separates_verification_from_market_validation():
    source = _source()

    assert "mixed-strategy equilibrium; model verification" in source
    assert "Model verification is separate from empirical input anchoring" in source
    assert "The simulated market outcomes are not externally validated" in source
    assert "Validation is limited to" not in source


def test_capacity_stress_case_is_not_presented_as_hardware_calibration():
    source = _source()

    assert "asymmetric congestion stress case in normalized service-rate units" in source
    assert "It is not converted from the RTX 4090 measurements" in source
    assert "does not represent a count of physical GPUs" in source


def test_utilization_above_one_is_not_presented_as_queue_stability():
    source = _source()

    assert "permits $u_{m,t}>1$" in source
    assert "does not simulate queue carryover between periods" in source
    assert "not a queue-stability result" in source


def test_model_equation_symbols_are_defined_in_the_prose():
    source = _source()

    assert r"$\beta\ge0$ is the routing weight on wholesale price" in source
    assert r"$\eta\ge0$ is the routing weight on provider QoS" in source
    assert r"The threshold $\bar u>0$" in source
    assert r"$\zeta>0$ controls its rate" in source
    assert r"$c_G\ge0$ is the holding cost" in source
    assert r"$c_q\ge0$ is the degradation penalty" in source
    assert r"The scalars $v_A$ and $v_B$" in source


def test_model_parameter_domains_are_explicit():
    source = _source()

    assert r"$N>0$" in source
    assert r"$\gamma_k\ge0$" in source
    assert r"$\nu_o\ge0$" in source
    assert r"$\phi_k\in[0,1]$" in source
    assert r"$H_k\in\mathbb Z_{\ge0}$" in source
    assert r"$\kappa_k\ge0$" in source
    assert r"$b_c>0$" in source
    assert r"$\alpha_k\ge0$" in source
    assert r"$\omega_q\ge0$" in source
    assert r"$G_A>G_B>0$" in source
    assert r"$\bar u>0$" in source
    assert r"$\zeta>0$" in source
    assert r"$c_G\ge0$" in source
    assert r"$c_q\ge0$" in source


def test_fixed_capacity_cost_role_in_strategy_and_accounting_is_explicit():
    source = _source()

    assert "constant across that provider's price strategies" in source
    assert "changes reported profit levels but not best-response order" in source


def test_price_coefficient_is_not_presented_as_total_demand_elasticity():
    source = _source()
    table_builder = SENSITIVITY_TABLE_BUILDER.read_text(encoding="utf-8")
    figure_builder = FIGURE_BUILDER.read_text(encoding="utf-8")

    assert r"$\alpha_k\ge0$ is the price coefficient on utility" in source
    assert "changes allocation among period--channel alternatives" in source
    assert "not an own-price elasticity of total market demand" in source
    assert r"Utility price coefficient $\alpha_R/\alpha_F$" in source
    assert "Utility coefficient $-20\\%$" in table_builder
    assert "Utility coefficient $+20\\%$" in table_builder
    assert '"$\\\\alpha$"' in figure_builder
    assert 'label="Lower"' in figure_builder
    assert 'label="Higher"' in figure_builder


def test_discrete_choice_heterogeneity_boundary_is_explicit():
    source = _source()

    assert "independent shocks and common coefficients within each request type" in source
    assert "correlated preferences and user-level coefficient heterogeneity" in source
    assert "Both request types also share the same native intraday load shape" in source
    assert "without observation error or adjustment delay" in source


def test_native_demand_and_reported_movement_metrics_are_defined():
    source = _source()

    assert r"N_{k,o}=N\gamma_k\nu_o" in source
    assert r"R_P=L_{\mathrm{peak}}/(N/T)" in source
    assert (
        r"M=\mathbb E\!\left["
        r"\frac{\sum_{k,o}\sum_{t\ne o}F_{k,o,t}}{N}"
        in source
    )


def test_sensitivity_equilibria_remain_conditional_on_common_candidate_set():
    source = _source()

    assert "fully re-solved" not in source.lower()
    assert "stored finite payoff matrix" not in source.lower()
    assert "stored finite-game payoff matrix" not in source.lower()
    assert "stored numerical payoff matrix" not in source.lower()
    assert "numerical payoff oracle" in source
    assert "checks every declared unilateral provider deviation" in source
    assert "nine-scenario uniform-price off-grid audit" in source
    assert "baseline four-dimensional off-grid audit" in source
    assert "conditional on the common finite rule set" in source


def test_numerical_audit_randomness_and_search_settings_are_visible():
    source = _source()

    assert source.count("base seed was 20260713") >= 2
    assert "35 generations" in source
    assert "population multiplier of 8" in source
    assert "absolute and relative tolerances of $10^{-8}$" in source
    assert "Dirichlet generator used seed 20260715" in source


def test_numerical_audit_gates_are_not_economic_significance_thresholds():
    source = _source()

    assert "prespecified numerical reporting gates" in source
    assert "not criteria for economic significance" in source


def test_mixed_distribution_uses_a_discrete_quantile_definition():
    source = _source()

    assert "smallest observed profile value whose cumulative probability" in source


def test_mixed_distribution_table_matches_the_provenance_linked_artifact():
    source = _source()
    metrics = json.loads(DISTRIBUTION.read_text(encoding="utf-8"))["dynamic"][
        "metrics"
    ]
    labels = {
        "aggregate_peak_load": "Aggregate peak load",
        "maximum_provider_utilization": "Maximum provider utilization",
        "minimum_provider_qos": "Minimum provider QoS",
        "system_profit": "Aggregate market-side profit",
    }

    for key, label in labels.items():
        values = metrics[key]
        row = (
            f"{label} & {values['p05']:.3f} & {values['p50']:.3f} "
            f"& {values['p95']:.3f} \\\\"
        )
        assert row in source


def test_evidence_map_does_not_claim_a_stored_complete_payoff_matrix():
    source = EVIDENCE_MAP.read_text(encoding="utf-8").lower()

    assert "stored finite payoff matrix" not in source
    assert "stored numerical payoff matrix" not in source
    assert "generated by the numerical intermediary response" not in source
    assert "cached numerical payoff evaluations" in source


def test_theory_audit_matches_the_partial_payoff_and_sensitivity_status():
    source = THEORY_AUDIT.read_text(encoding="utf-8").lower()

    assert "stored finite payoff matrix" not in source
    assert "存储支付矩阵" not in source
    assert "缓存的必要支付评价" in source
    assert "离散逆 cdf" in source
    assert "1,576" in source
    assert "800" in source
    assert "70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226" in source
    assert "8/8 个新阶段扰动场景" in source
    for scenario in (
        "capacity_low",
        "capacity_high",
        "price_sensitivity_low",
        "price_sensitivity_high",
        "migration_cost_low",
        "migration_cost_high",
        "qos_threshold_low",
        "qos_threshold_high",
    ):
        assert scenario in source
    assert "其余 5 个场景" not in source
    assert "动态 788 候选" not in source
    assert "统一 12 候选" not in source
    assert "当前预校验不属于均衡证据" not in source


def test_input_uncertainty_statistics_are_defined_in_the_manuscript():
    source = _source()

    assert "population standard deviation across the 59 retained days" in source
    assert "uses a divisor of 59" in source
    assert "between-repeat variation, not request-level binomial uncertainty" in source


def test_parameter_table_matches_the_executed_final_case():
    from experiments.run_final_spatiotemporal_equilibrium import final_case
    from pricing_sim.intermediary_response import IntermediarySearchSpec
    from pricing_sim.peak_shaving_equilibrium import routing_from_beta

    source = _source()
    config, game, calibration = final_case()
    route_qos_weight = inspect.signature(routing_from_beta).parameters[
        "qos_weight"
    ].default
    search = IntermediarySearchSpec().to_dict(config)

    assert config.num_periods == 8
    assert config.period_hours == 3.0
    assert game.demand.native_demand.sum() == 1100.0
    assert game.demand.native_demand.sum(axis=1).tolist() == [440.0, 660.0]
    assert game.demand.flexible_fraction.tolist() == [0.0, 0.8]
    assert game.demand.price_sensitivity.tolist() == [2.0, 5.0]
    assert game.demand.migration_cost.tolist() == [2.0, 0.35]
    assert game.demand.max_shift.tolist() == [0, 2]
    assert config.firm_capacity.tolist() == [180.0, 72.0]
    assert config.qos_threshold == calibration["threshold"]
    assert config.qos_strength == calibration["strength"]
    assert game.demand.qos_weight == 1.0
    assert route_qos_weight == 3.0
    assert game.demand.channel_brand.tolist() == [1.05, 1.0, 1.0]
    assert game.fixed_channel_shares.tolist() == [0.12, 0.50, 0.38]
    assert config.capacity_cost == 0.015
    assert config.degrade_cost == 0.35
    assert (config.wholesale_lower, config.wholesale_upper) == (0.25, 0.90)
    assert (config.price_lower, config.price_upper) == (0.45, 2.10)
    assert tuple(search["retail_base_bounds"]) == (0.45, 2.10)
    assert tuple(search["retail_slope_bounds"]) == (-1.0, 1.0)
    assert tuple(search["route_beta_bounds"]) == (0.0, 1_000_000.0)

    for row in (
        r"Periods and period length & $T=8$, $h=3$ hours",
        r"Sum of native period rates & 1100 normalized units",
        r"Rigid/flexible population share & $0.4/0.6$",
        r"Reallocatable fraction $\phi_R/\phi_F$ & $0/0.8$",
        r"Utility price coefficient $\alpha_R/\alpha_F$ & $2/5$",
        r"Migration cost $\kappa_R/\kappa_F$ & $2/0.35$",
        r"Maximum shift $H_R/H_F$ & $0/2$ periods",
        r"Provider capacities $G_A/G_B$ & $180/72$ rate units",
        r"QoS threshold and strength & $1.000/0.5747$",
        r"QoS choice weight $\omega_q$ & 1",
        r"Routing QoS weight $\eta$ & 3",
        r"Channel preferences $(b_I,b_A,b_B)$ & $(1.05,1,1)$",
        r"Fixed shares when spatial response is off & $(0.12,0.50,0.38)$",
        r"Capacity/degradation cost & $0.015/0.35$",
        r"Wholesale/direct posted-price bounds & $[0.25,0.90]/[0.45,2.10]$",
        r"Intermediary $(\bar p^I,\delta^I,\beta)$ bounds & $[0.45,2.10]/[-1,1]/[0,10^6]$",
    ):
        assert row in source


def test_main_result_table_matches_the_submission_equilibrium_artifact():
    from experiments.build_submission_result_macros import equilibrium_macros

    source = _source()
    payload = json.loads(EQUILIBRIUM.read_text(encoding="utf-8"))
    macro_source = RESULT_MACROS.read_text(encoding="utf-8")

    assert "Metric & Uniform & Time-varying & Change" in source
    assert "Metric & Uniform & Dynamic & Change" not in source
    for name, value in equilibrium_macros(payload).items():
        assert rf"\newcommand{{\{name}}}{{{value}}}" in macro_source
    for row in (
        r"Aggregate peak load & \UniformAggregatePeak{} & \DynamicAggregatePeak{}",
        r"Aggregate peak-to-average ratio & \UniformPeakToAverage{} & \DynamicPeakToAverage{}",
        r"Maximum provider utilization & \UniformMaximumUtilisation{} & \DynamicMaximumUtilisation{}",
        r"Minimum provider QoS & \UniformMinimumQoS{} & \DynamicMinimumQoS{}",
        r"Temporally moved fraction & \UniformMovedFraction{} & \DynamicMovedFraction{}",
        r"Provider $A$ profit & \UniformProviderAProfit{} & \DynamicProviderAProfit{}",
        r"Provider $B$ profit & \UniformProviderBProfit{} & \DynamicProviderBProfit{}",
        r"Intermediary profit & \UniformIntermediaryProfit{} & \DynamicIntermediaryProfit{}",
        r"Aggregate market-side profit & \UniformMarketProfit{} & \DynamicMarketProfit{}",
    ):
        assert row in source


def test_candidate_table_and_continuation_vectors_match_the_manifest():
    source = _source()
    manifest = json.loads(CANDIDATE_MANIFEST.read_text(encoding="utf-8"))
    table = source.split(r"\label{tab:candidate_design}", 1)[1].split(
        r"\end{table}", 1
    )[0]
    labels = (
        "Uniform", "Mid-slope", "Wholesale-base", "Low-slope",
        "High-slope", "Boundary guards", "Deviation-local", "Continuation",
    )
    for label, component in zip(labels, manifest["components"]):
        row = next(line for line in table.splitlines() if line.startswith(label))
        assert (
            f"& {component['added_unique_count']} "
            f"& {component['cumulative_unique_count']} \\" in row
        )
    verification = manifest["verification"]
    assert (
        f"{verification['reference_support_entry_count']} support entries, "
        f"{verification['reference_unique_count']} distinct vectors, of which "
        f"{len(manifest['continuation_only_vectors'])} are new"
    ) in source
    continuation_block = source.split(
        "For completeness, the 18 continuation-only vectors", 1
    )[1].split(r"\end{center}", 1)[0]
    observed = {
        tuple(float(value) for value in match.split(","))
        for match in re.findall(r"\$\(([^)]+)\)\$", continuation_block)
    }
    expected = {
        tuple(float(value) for value in vector)
        for vector in manifest["continuation_only_vectors"]
    }
    assert observed == expected


def test_strategy_support_and_solver_trace_match_the_equilibrium_artifact():
    source = _source()
    payload = json.loads(EQUILIBRIUM.read_text(encoding="utf-8"))
    uniform, dynamic = payload["uniform"], payload["dynamic"]
    uniform_means = []
    for side in ("row", "col"):
        vectors, mix = uniform[f"{side}_support_vectors"], uniform[f"{side}_mix"]
        assert sum(weight > 1e-12 for weight in mix) == 10
        uniform_means.append([
            sum(weight * row[i] for row, weight in zip(vectors, mix))
            for i in range(4)
        ])
    assert "over ten positive-probability strategies for each provider" in source
    for mean in uniform_means:
        text = ",".join("0" if abs(value) < 5e-8 else f"{value:.4f}" for value in mean)
        assert f"({text})" in source

    means, slope_ranges = [], []
    for side in ("row", "col"):
        vectors, mix = dynamic[f"{side}_support_vectors"], dynamic[f"{side}_mix"]
        means.append([sum(weight * row[i] for row, weight in zip(vectors, mix)) for i in range(4)])
        positive = [row for row, weight in zip(vectors, mix) if weight > 1e-12]
        slope_ranges.append((min(row[1] for row in positive), max(row[1] for row in positive)))
    assert f"range from {slope_ranges[0][0]:g} to {slope_ranges[0][1]:g}" in source
    assert f"range from {slope_ranges[1][0]:g} to {slope_ranges[1][1]:g}" in source
    for mean in means:
        assert "(" + ",".join(f"{value:.4f}" for value in mean) + ")" in source

    active = dynamic["active_profiles"]
    lower_mass = sum(row["weight"] for row in active if row["intermediary_candidate"]["route_beta"] <= 1e-8)
    upper_mass = sum(row["weight"] for row in active if row["intermediary_candidate"]["route_beta"] >= 999_000)
    deterministic_mass = sum(row["weight"] for row in active if row["search_diagnostics"]["routing_near_deterministic"])
    assert f"{100 * lower_mass:.1f}\\% of the profile probability mass" in source
    assert f"{100 * upper_mass:.3f}\\%" in source
    assert f"profiles with {100 * deterministic_mass:.1f}\\% probability mass" in source

    audit_paragraph = source.split("The augmented reconstruction", 1)[1].split(
        "\n\n", 1
    )[0]
    assert _latex_scientific(dynamic["full_max_regret"]) in audit_paragraph
    assert f"{dynamic['evaluated_pairs']:,} pairs" in audit_paragraph


def test_demand_and_numerical_audit_prose_matches_artifacts():
    source = _source()
    equilibrium = json.loads(EQUILIBRIUM.read_text(encoding="utf-8"))
    destinations = [
        equilibrium[name]["expected_profiles"]["destination_demand_by_type"][1]
        for name in ("uniform", "dynamic")
    ]
    centroids = [
        sum((index + 1) * value for index, value in enumerate(row)) / sum(row)
        for row in destinations
    ]
    assert f"centroid changes from {centroids[0]:.3f} to {centroids[1]:.3f}" in source

    fixed = json.loads(FIXED_POINT_AUDIT.read_text(encoding="utf-8"))
    starts = len(fixed["records"]) * fixed["metadata"]["starts_per_profile"]
    assert f"All {starts:,} runs converged" in source
    assert _latex_scientific(fixed["maximum_residual"]) in source
    assert _latex_scientific(fixed["maximum_qos_span"]) in source
    assert _latex_scientific(fixed["maximum_routing_span"]) in source

    branch = json.loads(BRANCH_AUDIT.read_text(encoding="utf-8"))
    metadata = branch["metadata"]
    assert metadata["successful_starts"] == metadata["total_starts"]
    assert f"All {metadata['total_starts']} starts returned a valid equilibrium" in source
    assert f"${branch['restricted_shape'][0]}\\times{branch['restricted_shape'][1]}$" in source
    assert f"{branch['branches'][0]['row_support_count']}-by-{branch['branches'][0]['col_support_count']} active support" in source


def test_offgrid_and_intermediary_audit_prose_matches_artifacts():
    source = _source()
    offgrid = json.loads(OFFGRID.read_text(encoding="utf-8"))
    counts = [
        offgrid["players"][name]["evaluated_candidates"]
        for name in ("firm_A", "firm_B")
    ]
    assert (
        f"{counts[0]:,} deviations for provider A and {counts[1]:,} for provider B"
        in source
    )
    for player in ("firm_A", "firm_B"):
        values = offgrid["players"][player]
        assert f"{100 * values['relative_offgrid_regret']:.3f}\\%" in source
        vector = ",".join(_compact_decimal(value) for value in values["best_vector"])
        assert f"$({vector})$" in source
    support_error = max(
        values["maximum_active_support_payoff_error"]
        for values in offgrid["players"].values()
    )
    assert _latex_scientific(support_error) in source

    audit = json.loads(INTERMEDIARY_AUDIT.read_text(encoding="utf-8"))
    successful = sum(row["optimizer_success"] for row in audit["records"])
    unsuccessful = [row for row in audit["records"] if not row["optimizer_success"]]
    max_unsuccessful = max(row["relative_profit_improvement"] for row in unsuccessful)
    assert f"Of the {len(audit['records'])} runs, {successful} met" in source
    assert f"The other {len(unsuccessful)} reached" in source
    assert f"{audit['maximum_profit_improvement']:.4f}" in source
    assert f"{100 * audit['maximum_relative_profit_improvement']:.4f}\\%" in source
    assert _latex_scientific(max_unsuccessful) in source


def test_offgrid_relative_regret_and_mixed_strategy_timing_are_defined():
    source = _source()
    assert r"\epsilon_m^{\mathrm{off}}=\widehat v_m^{\mathrm{off}}-v_m" in source
    assert (
        r"\rho_m^{\mathrm{off}}="
        r"\epsilon_m^{\mathrm{off}}/\max\{|v_m|,1\}"
        in source
    )
    assert "draws one complete intraday price rule before the simulated day" in source
    assert "does not redraw a rule in each period" in source


def test_mechanism_and_price_shape_prose_matches_artifacts():
    source = _source()
    mechanism = json.loads(MECHANISM_AUDIT.read_text(encoding="utf-8"))
    comparisons = {row["mechanism"]: row for row in mechanism["policy_comparisons"]}
    temporal = comparisons["temporal_only"]
    spatial = comparisons["spatial_only"]
    assert f"{abs(temporal['aggregate_peak_load_change_percent']):.2f}\\%" in source
    assert f"{temporal['minimum_provider_qos_change']:.4f}" in source
    assert f"{abs(spatial['maximum_provider_utilization_change_percent']):.2f}\\%" in source
    assert f"{spatial['minimum_provider_qos_change']:.4f}" in source
    assert r"$\AggregatePeakChangePercent$\%" in source
    dynamic_rows = {
        row["mechanism"]: row for row in mechanism["rows"] if row["policy"] == "dynamic"
    }
    temporal_row = dynamic_rows["temporal_only"]
    combined_row = dynamic_rows["combined"]
    assert (
        f"from {temporal_row['maximum_provider_utilization']:.3f} in the "
        r"temporal-only control to \DynamicMaximumUtilisation{}"
    ) in source
    assert (
        f"from {temporal_row['minimum_provider_qos']:.3f} "
        r"to \DynamicMinimumQoS{}"
    ) in source
    assert f"{100 * combined_row['intermediary_weighted_route_to_A']:.1f}\\%" in source

    price_shape = json.loads(PRICE_SHAPE_AUDIT.read_text(encoding="utf-8"))
    components = {row["metric"]: row for row in price_shape["components"]}
    labels = {
        "aggregate_peak_load": ("Aggregate peak load", 3),
        "maximum_provider_utilization": ("Maximum provider utilization", 4),
        "minimum_provider_qos": ("Minimum provider QoS", 4),
        "system_profit": ("Aggregate market-side profit", 3),
    }
    for key, (label, digits) in labels.items():
        row = components[key]
        expected = (
            f"{label} & ${row['overall_change']:+.{digits}f}$ "
            f"& ${row['shape_change']:+.{digits}f}$ "
            f"& ${row['level_and_mix_remainder']:+.{digits}f}$"
        )
        assert expected in source
