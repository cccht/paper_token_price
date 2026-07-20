from pathlib import Path
import sys
from types import SimpleNamespace

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def _small_grid() -> np.ndarray:
    return np.array([
        [0.35, 0.0, 0.80, 0.0],
        [0.55, 0.0, 1.00, 0.0],
        [0.35, 0.2, 0.80, 0.2],
        [0.55, -0.2, 1.00, -0.2],
    ])


def test_final_equilibrium_pipeline_reports_verified_uniform_and_dynamic_games():
    from experiments.run_final_spatiotemporal_equilibrium import run_equilibria

    result = run_equilibria(
        candidate_grid=_small_grid(),
        max_oracle_rounds=4,
        retail_base_grid=np.array([0.8]),
        dynamic_retail_slope_grid=np.array([-0.2, 0.0, 0.2]),
        route_beta_grid=np.array([2.0]),
    )

    assert result["metadata"]["load_source"] == "BurstGPT token profile"
    assert result["metadata"]["full_candidate_count"] == 4
    assert result["uniform"]["candidate_count"] == 2
    assert result["dynamic"]["candidate_count"] == 4
    for game in (result["uniform"], result["dynamic"]):
        assert game["full_grid_verified"]
        assert game["full_max_regret"] <= 1e-7
        assert game["relative_full_max_regret"] <= 1e-7
        assert np.isclose(game["expected_metrics"]["total_demand"], 1100.0)
        assert len(game["expected_profiles"]["aggregate_load"]) == 8
        assert len(game["row_support_vectors"]) == len(game["row_mix"])
        assert len(game["col_support_vectors"]) == len(game["col_mix"])
        assert game["maximum_joint_residual"] <= 1e-8
        assert game["active_profiles"]
        assert all(
            "intermediary_candidate" in profile
            for profile in game["active_profiles"]
        )
    assert set(result["comparison"]) >= {
        "aggregate_peak_load_change",
        "maximum_provider_utilization_change",
        "minimum_provider_qos_change",
        "system_profit_change",
    }


def test_final_equilibrium_artifact_has_reproducibility_manifest():
    from experiments.run_final_spatiotemporal_equilibrium import run_equilibria

    result = run_equilibria(
        candidate_grid=_small_grid(),
        max_oracle_rounds=4,
        retail_base_grid=np.array([0.8]),
        dynamic_retail_slope_grid=np.array([0.0]),
        route_beta_grid=np.array([2.0]),
    )

    manifest = result["metadata"]
    assert manifest["git_commit"]
    assert manifest["git_dirty"] is True
    assert manifest["command"].startswith("uv run")
    assert all(len(digest) == 64 for digest in manifest["source_sha256"].values())
    expected_sources = {
        "pricing_sim/peak_shaving_config.py",
        "pricing_sim/peak_shaving_equilibrium.py",
        "pricing_sim/peak_shaving_market.py",
        "pricing_sim/spatiotemporal_mechanism.py",
        "pricing_sim/spatiotemporal_game.py",
        "pricing_sim/intermediary_response.py",
        "pricing_sim/finite_game.py",
        "pricing_sim/bimatrix_solver.py",
        "pricing_sim/complementarity_solver.py",
        "pricing_sim/milp_equilibrium_solver.py",
        "experiments/equilibrium_cache.py",
        "experiments/equilibrium_run_support.py",
        "experiments/final_equilibrium_tools.py",
        "experiments/final_reproducibility.py",
        "experiments/peak_shaving_submission_tools.py",
        "experiments/run_spatiotemporal_mechanism_decomposition.py",
        "experiments/run_final_spatiotemporal_equilibrium.py",
    }
    assert expected_sources <= set(manifest["source_sha256"])
    assert manifest["scipy"]
    assert manifest["nashpy"]
    assert result["demand_spec"]["flexible_fraction"] == [0.0, 0.8]
    assert result["qos_calibration"]["threshold"] >= 1.0


def test_final_case_applies_sensitivity_overrides_without_changing_total_demand():
    from experiments.run_final_spatiotemporal_equilibrium import final_case

    config, game, calibration = final_case(
        capacity_scale=0.85,
        price_sensitivity_scale=1.2,
        migration_cost_scale=0.7,
        qos_threshold_shift=0.05,
    )

    assert np.allclose(config.firm_capacity, np.array([180.0, 72.0]) * 0.85)
    assert np.allclose(game.demand.price_sensitivity, [2.4, 6.0])
    assert np.allclose(game.demand.migration_cost, [1.4, 0.245])
    assert config.qos_threshold == calibration["threshold"] + 0.05
    assert np.isclose(game.demand.native_demand.sum(), 1100.0)


def test_equilibrium_pipeline_records_sensitivity_scenario():
    from experiments.run_final_spatiotemporal_equilibrium import run_equilibria

    result = run_equilibria(
        candidate_grid=_small_grid(),
        max_oracle_rounds=4,
        retail_base_grid=np.array([0.8]),
        dynamic_retail_slope_grid=np.array([0.0]),
        route_beta_grid=np.array([2.0]),
        capacity_scale=0.9,
        price_sensitivity_scale=1.1,
        migration_cost_scale=1.2,
        qos_threshold_shift=-0.05,
    )

    assert result["scenario"] == {
        "capacity_scale": 0.9,
        "price_sensitivity_scale": 1.1,
        "migration_cost_scale": 1.2,
        "qos_threshold_shift": -0.05,
    }
    assert np.allclose(result["model_config"]["capacity"], [162.0, 64.8])


def test_default_pipeline_uses_third_audit_enriched_grid(monkeypatch):
    import experiments.run_final_spatiotemporal_equilibrium as module

    monkeypatch.setattr(
        module,
        "third_audit_enriched_provider_candidate_grid",
        lambda: _small_grid(),
    )
    result = module.run_equilibria(
        max_oracle_rounds=4,
        retail_base_grid=np.array([0.8]),
        dynamic_retail_slope_grid=np.array([0.0]),
        route_beta_grid=np.array([2.0]),
    )

    assert result["metadata"]["full_candidate_count"] == 4


def test_parallel_pair_evaluation_matches_serial_evaluation():
    from experiments.final_equilibrium_tools import PairEvaluator
    from experiments.run_final_spatiotemporal_equilibrium import final_case

    config, game, _ = final_case()
    kwargs = {
        "grid": _small_grid(),
        "game": game,
        "config": config,
        "retail_base_grid": np.array([0.8]),
        "retail_slope_grid": np.array([0.0, 0.2]),
        "route_beta_grid": np.array([2.0]),
    }
    pairs = [(0, 0), (0, 1), (2, 3), (3, 2)]
    serial = PairEvaluator(**kwargs, parallel_workers=1).evaluate_many(pairs)
    parallel = PairEvaluator(**kwargs, parallel_workers=2).evaluate_many(pairs)

    for serial_record, parallel_record in zip(serial, parallel):
        for key in ("firm_A_profit", "firm_B_profit", "intermediary_profit"):
            assert np.isclose(serial_record[key], parallel_record[key])
        assert serial_record["result"]["intermediary_candidate"] == parallel_record[
            "result"
        ]["intermediary_candidate"]


def test_pair_cache_identity_ignores_parallel_worker_count(tmp_path):
    from experiments.run_final_spatiotemporal_equilibrium import run_equilibria

    kwargs = {
        "candidate_grid": _small_grid(),
        "max_oracle_rounds": 2,
        "retail_base_grid": np.array([0.8]),
        "dynamic_retail_slope_grid": np.array([0.0]),
        "route_beta_grid": np.array([2.0]),
        "pair_cache_dir": tmp_path,
    }
    serial = run_equilibria(**kwargs, parallel_workers=1)
    parallel = run_equilibria(**kwargs, parallel_workers=2)

    serial_cache = serial["metadata"]["pair_cache"]["dynamic"]
    parallel_cache = parallel["metadata"]["pair_cache"]["dynamic"]
    assert serial_cache["signature"] == parallel_cache["signature"]
    assert parallel_cache["loaded_pairs"] == serial_cache["stored_pairs"]


def test_pair_evaluator_has_explicit_cache_checkpoint_interval():
    from experiments.final_equilibrium_tools import PairEvaluator

    field = PairEvaluator.__dataclass_fields__["checkpoint_interval"]
    assert field.default == 8192


def test_pair_evaluator_uses_spawn_process_context(monkeypatch):
    import experiments.final_equilibrium_tools as module
    from experiments.run_final_spatiotemporal_equilibrium import final_case

    captured = {}

    class SerialExecutor:
        def __init__(self, *, max_workers, mp_context):
            captured["max_workers"] = max_workers
            captured["start_method"] = mp_context.get_start_method()

        def __enter__(self):
            return self

        def __exit__(self, *args):
            return False

        def map(self, function, iterable, chunksize):
            return map(function, iterable)

    monkeypatch.setattr(module, "ProcessPoolExecutor", SerialExecutor)
    config, game, _ = final_case()
    evaluator = module.PairEvaluator(
        grid=_small_grid(),
        game=game,
        config=config,
        retail_base_grid=np.array([0.8]),
        retail_slope_grid=np.array([0.0]),
        route_beta_grid=np.array([2.0]),
        parallel_workers=2,
    )

    evaluator.evaluate_many([(0, 0), (1, 1)])

    assert captured == {"max_workers": 2, "start_method": "spawn"}


def test_equilibrium_pipeline_reuses_vector_pair_cache(tmp_path):
    from experiments.run_final_spatiotemporal_equilibrium import run_equilibria

    kwargs = {
        "candidate_grid": _small_grid(),
        "max_oracle_rounds": 4,
        "retail_base_grid": np.array([0.8]),
        "dynamic_retail_slope_grid": np.array([0.0]),
        "route_beta_grid": np.array([2.0]),
        "pair_cache_dir": tmp_path,
    }
    first = run_equilibria(**kwargs)
    second = run_equilibria(**kwargs)

    assert first["metadata"]["pair_cache"]["dynamic"]["loaded_pairs"] == 0
    assert second["metadata"]["pair_cache"]["dynamic"]["loaded_pairs"] > 0
    assert second["metadata"]["pair_cache"]["dynamic"]["stored_pairs"] >= 1
    assert (tmp_path / "dynamic.pkl").exists()
    assert np.isclose(
        first["dynamic"]["expected_metrics"]["system_profit"],
        second["dynamic"]["expected_metrics"]["system_profit"],
    )


def test_previous_mixed_candidate_is_embedded_when_support_expands():
    from experiments.final_equilibrium_tools import _embed_mixed_candidate

    warm = _embed_mixed_candidate(
        old_rows=[2, 5],
        old_cols=[1, 4],
        new_rows=[2, 3, 5],
        new_cols=[1, 4, 7],
        row_mix=np.array([0.25, 0.75]),
        col_mix=np.array([0.6, 0.4]),
    )

    assert np.allclose(warm[0], [0.25, 0.0, 0.75])
    assert np.allclose(warm[1], [0.6, 0.4, 0.0])


def test_oracle_round_limit_keeps_support_and_mixture_aligned(monkeypatch):
    import experiments.final_equilibrium_tools as module

    class Evaluator:
        grid = np.array([[0.0], [1.0]])
        cache = {}

        def restricted_payoffs(self, rows, cols):
            return np.zeros((len(rows), len(cols))), np.zeros((len(rows), len(cols)))

        def full_deviation_payoffs(self, rows, cols):
            return np.zeros((2, len(cols))), np.zeros((len(rows), 2))

        def evaluate(self, row, col):
            state = SimpleNamespace(
                retail=np.ones(1), direct=np.ones((2, 1)),
                wholesale=np.ones((2, 1)), routing=np.full((2, 1), 0.5),
            )
            result = {
                "loads": np.ones((2, 1)),
                "utilization": np.ones((2, 1)),
                "qos_firm": np.ones((2, 1)),
                "demand": np.ones((3, 1)),
                "destination_demand_by_type": np.ones((2, 1)),
                "intermediary_candidate": {
                    "retail_base": 1.0, "retail_slope": 0.0, "route_beta": 0.0,
                },
                "intermediary_search": {
                    "method": "test", "function_evaluations": 1,
                    "successful_local_runs": 1,
                },
            }
            return {
                **{key: 1.0 for key in module.SCALAR_KEYS},
                "joint_residual": 0.0,
                "state": state,
                "result": result,
            }

    selected = {
        "row_mix": np.array([1.0]),
        "col_mix": np.array([1.0]),
        "row_restricted_regret": 0.0,
        "col_restricted_regret": 0.0,
        "restricted_max_regret": 0.0,
        "method": "test",
        "methods": ["test"],
        "row_expected_payoff": 1.0,
        "col_expected_payoff": 1.0,
        "row_best_response_index": 1,
        "col_best_response_index": 1,
        "row_best_response_payoff": 2.0,
        "col_best_response_payoff": 2.0,
        "row_full_regret": 1.0,
        "col_full_regret": 1.0,
        "full_max_regret": 1.0,
        "relative_full_max_regret": 1.0,
    }
    monkeypatch.setattr(module, "enumerate_bimatrix_equilibria", lambda *args, **kwargs: [{}])
    monkeypatch.setattr(module, "select_full_grid_equilibrium", lambda *args, **kwargs: selected)

    result = module.solve_candidate_game(
        Evaluator(), row_support=[0], col_support=[0], max_oracle_rounds=1
    )

    assert result["row_support_indices"] == [0]
    assert result["col_support_indices"] == [0]
    assert len(result["row_support_indices"]) == len(result["row_mix"])
    assert len(result["col_support_indices"]) == len(result["col_mix"])
    assert result["termination_reason"] == "oracle_round_limit"
    assert result["oracle_round_limit_reached"] is True
    assert result["full_grid_verified"] is False


def test_submission_runner_uses_latest_completed_active_support(tmp_path):
    from experiments.run_submission_spatiotemporal_equilibrium import (
        OUTPUT_PATH,
        _continuation_vectors,
    )

    older = tmp_path / "provider1370.json"
    latest = tmp_path / "provider4016.json"
    older.write_text(
        '{"dynamic":{"row_support_vectors":[[1,0,1,0]],'
        '"col_support_vectors":[[2,0,2,0]],"row_mix":[1],"col_mix":[1]}}',
        encoding="utf-8",
    )
    latest.write_text(
        '{"dynamic":{"row_support_vectors":[[3,0,3,0],[4,0,4,0]],'
        '"col_support_vectors":[[5,0,5,0],[6,0,6,0]],'
        '"row_mix":[0,1],"col_mix":[1,0]}}',
        encoding="utf-8",
    )

    vectors, seed = _continuation_vectors((latest, older))

    assert OUTPUT_PATH.name == "spatiotemporal_equilibrium_submission.json"
    assert seed == latest
    assert vectors == ([[4, 0, 4, 0]], [[5, 0, 5, 0]])
