from pathlib import Path
import sys

import numpy as np
import pytest
from time import perf_counter, sleep

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))


def test_matching_pennies_equilibrium_is_mixed_and_has_low_regret():
    from pricing_sim.finite_game import enumerate_bimatrix_equilibria

    row = np.array([[1.0, -1.0], [-1.0, 1.0]])
    col = -row

    equilibria = enumerate_bimatrix_equilibria(row, col)
    best = min(equilibria, key=lambda item: item["restricted_max_regret"])

    assert np.allclose(best["row_mix"], [0.5, 0.5], atol=1e-7)
    assert np.allclose(best["col_mix"], [0.5, 0.5], atol=1e-7)
    assert best["restricted_max_regret"] <= 1e-8


def test_full_grid_selection_detects_profitable_action_outside_support():
    from pricing_sim.finite_game import (
        enumerate_bimatrix_equilibria,
        select_full_grid_equilibrium,
    )

    restricted_row = np.array([[2.0]])
    restricted_col = np.array([[3.0]])
    equilibria = enumerate_bimatrix_equilibria(restricted_row, restricted_col)
    row_full = np.array([[2.0], [2.7], [1.0]])
    col_full = np.array([[3.0, 2.0, 4.2]])

    selected = select_full_grid_equilibrium(
        equilibria,
        restricted_row,
        restricted_col,
        row_full,
        col_full,
    )

    assert selected["row_best_response_index"] == 1
    assert selected["col_best_response_index"] == 2
    assert selected["row_full_regret"] == pytest.approx(0.7)
    assert selected["col_full_regret"] == pytest.approx(1.2)
    assert selected["full_max_regret"] == pytest.approx(1.2)


def test_full_grid_selection_prefers_candidate_with_lower_external_regret():
    from pricing_sim.finite_game import select_full_grid_equilibrium

    row = np.array([[2.0, 0.0], [0.0, 1.0]])
    col = row.copy()
    candidates = [
        {
            "row_mix": np.array([1.0, 0.0]),
            "col_mix": np.array([1.0, 0.0]),
            "restricted_max_regret": 0.0,
            "method": "pure-a",
        },
        {
            "row_mix": np.array([0.0, 1.0]),
            "col_mix": np.array([0.0, 1.0]),
            "restricted_max_regret": 0.0,
            "method": "pure-b",
        },
    ]
    row_full = np.array([[2.0, 0.0], [0.0, 1.0], [2.1, 0.2]])
    col_full = np.array([[2.0, 0.0, 2.1], [0.0, 1.0, 0.2]])

    selected = select_full_grid_equilibrium(
        candidates, row, col, row_full, col_full
    )

    assert selected["method"] == "pure-b"
    assert selected["full_max_regret"] == 0.0


def test_large_game_with_pure_equilibria_skips_support_enumeration(monkeypatch):
    import nashpy as nash

    from pricing_sim.finite_game import enumerate_bimatrix_equilibria

    def fail_if_called(*args, **kwargs):
        raise AssertionError("support enumeration should not be called")

    monkeypatch.setattr(nash.Game, "support_enumeration", fail_if_called)
    equilibria = enumerate_bimatrix_equilibria(np.eye(10), np.eye(10))

    assert len(equilibria) == 10
    assert all(item["method"] == "pure_best_response" for item in equilibria)


def test_mixed_game_consumes_only_first_valid_equilibrium(monkeypatch):
    import nashpy as nash

    from pricing_sim.finite_game import enumerate_bimatrix_equilibria

    row_count, col_count = 6, 8
    row_phase = np.arange(row_count)[:, None] / row_count
    col_phase = np.arange(col_count)[None, :] / col_count
    row = np.sin(2.0 * np.pi * (row_phase + col_phase))
    col = -row
    def fail_if_called(*args, **kwargs):
        raise AssertionError("support enumeration should not be called")

    monkeypatch.setattr(nash.Game, "support_enumeration", fail_if_called)
    equilibria = enumerate_bimatrix_equilibria(row, col)

    assert equilibria
    assert any(
        "lemke_howson_label_0" in item["methods"] for item in equilibria
    )
    assert max(item["restricted_max_regret"] for item in equilibria) <= 1e-8


def test_mixed_solver_recovers_when_lemke_label_zero_is_invalid(monkeypatch):
    import nashpy as nash

    from pricing_sim.finite_game import enumerate_bimatrix_equilibria

    row = np.array([[1.0, -1.0], [-1.0, 1.0]])
    col = -row
    uniform = np.array([0.5, 0.5])

    def selective_lemke(self, initial_dropped_label):
        if initial_dropped_label < 2:
            return np.array([1.0]), np.array([1.0])
        return uniform, uniform

    def no_vertex_candidate(self):
        return iter(())

    def fail_support(*args, **kwargs):
        raise AssertionError("support enumeration should not be called")

    monkeypatch.setattr(nash.Game, "lemke_howson", selective_lemke)
    monkeypatch.setattr(nash.Game, "vertex_enumeration", no_vertex_candidate)
    monkeypatch.setattr(nash.Game, "support_enumeration", fail_support)
    equilibria = enumerate_bimatrix_equilibria(row, col)

    assert equilibria
    assert any(
        "lemke_howson_label_2" in item["methods"] for item in equilibria
    )
    assert max(item["restricted_max_regret"] for item in equilibria) <= 1e-8


def test_mixed_solver_timeout_covers_measured_twelve_by_twelve_vertex_case():
    from pricing_sim.bimatrix_solver import (
        MAX_LEMKE_LABELS,
        MAX_PARALLEL_MIXED_SOLVER_PROCESSES,
        MIXED_SOLVER_LABEL_TIMEOUT_SECONDS,
        MIXED_SOLVER_TIMEOUT_SECONDS,
    )

    assert MIXED_SOLVER_TIMEOUT_SECONDS >= 120.0
    assert MIXED_SOLVER_LABEL_TIMEOUT_SECONDS < MIXED_SOLVER_TIMEOUT_SECONDS
    assert 1 <= MAX_PARALLEL_MIXED_SOLVER_PROCESSES <= 8
    assert MAX_LEMKE_LABELS >= MAX_PARALLEL_MIXED_SOLVER_PROCESSES


def test_mixed_solver_normalizes_payoffs_before_calling_nashpy(monkeypatch):
    import nashpy as nash

    from pricing_sim.finite_game import enumerate_bimatrix_equilibria

    matching = np.array([[1.0, -1.0], [-1.0, 1.0]])
    row = 1000.0 + 100.0 * matching
    col = 5000.0 - 50.0 * matching
    uniform = np.array([0.5, 0.5])

    def scale_sensitive_lemke(self, initial_dropped_label):
        normalized = all(
            matrix.min() >= 0.0 and matrix.max() <= 1.0
            for matrix in self.payoff_matrices
        )
        return (uniform, uniform) if normalized else (np.array([1.0]), np.array([1.0]))

    monkeypatch.setattr(nash.Game, "lemke_howson", scale_sensitive_lemke)
    monkeypatch.setattr(nash.Game, "vertex_enumeration", lambda self: iter(()))
    equilibria = enumerate_bimatrix_equilibria(row, col)

    assert equilibria[0]["restricted_max_regret"] <= 1e-8


def test_valid_lemke_candidate_stops_slow_vertex_branch(monkeypatch):
    import nashpy as nash
    import pricing_sim.bimatrix_solver as solver

    from pricing_sim.finite_game import enumerate_bimatrix_equilibria

    matching = np.array([[1.0, -1.0], [-1.0, 1.0]])
    uniform = np.array([0.5, 0.5])

    monkeypatch.setattr(
        nash.Game,
        "lemke_howson",
        lambda self, initial_dropped_label: (uniform, uniform),
    )

    def slow_vertex(self):
        sleep(1.0)
        return iter(())

    monkeypatch.setattr(nash.Game, "vertex_enumeration", slow_vertex)
    monkeypatch.setattr(solver, "MIXED_SOLVER_TIMEOUT_SECONDS", 0.5)
    start = perf_counter()
    equilibria = enumerate_bimatrix_equilibria(matching, -matching)

    assert equilibria[0]["restricted_max_regret"] <= 1e-8
    assert perf_counter() - start < 0.4


def test_mixed_solver_recovers_from_high_lemke_label(monkeypatch):
    import nashpy as nash
    import pricing_sim.bimatrix_solver as solver

    from pricing_sim.finite_game import enumerate_bimatrix_equilibria

    size = 6
    phase = np.arange(size)
    row = np.cos(2.0 * np.pi * (phase[:, None] - phase[None, :]) / size)
    col = -row
    uniform = np.full(size, 1.0 / size)

    def high_label_only(self, initial_dropped_label):
        if initial_dropped_label == 9:
            return uniform, uniform
        return np.array([1.0]), np.array([1.0])

    monkeypatch.setattr(nash.Game, "lemke_howson", high_label_only)
    monkeypatch.setattr(nash.Game, "vertex_enumeration", lambda self: iter(()))
    monkeypatch.setattr(solver, "MAX_PARALLEL_MIXED_SOLVER_PROCESSES", 2)
    equilibria = enumerate_bimatrix_equilibria(row, col)

    assert equilibria[0]["restricted_max_regret"] <= 1e-8
    assert "lemke_howson_label_9" in equilibria[0]["methods"]


def test_complementarity_fallback_polishes_warm_mixed_candidate(monkeypatch):
    import pricing_sim.finite_game as finite_game

    matching = np.array([[1.0, -1.0], [-1.0, 1.0]])
    warm = (
        np.array([0.500001, 0.499999]),
        np.array([0.499998, 0.500002]),
    )
    monkeypatch.setattr(
        finite_game,
        "bounded_mixed_candidates",
        lambda *args: (_ for _ in ()).throw(
            AssertionError("verified warm candidate should skip Nashpy")
        ),
    )

    equilibria = finite_game.enumerate_bimatrix_equilibria(
        matching,
        -matching,
        initial_candidate=warm,
    )

    assert equilibria[0]["method"] == "fischer_burmeister_support_polish"
    assert equilibria[0]["restricted_max_regret"] <= 1e-8


def test_milp_fallback_recovers_when_warm_complementarity_stalls(monkeypatch):
    import pricing_sim.finite_game as finite_game

    matching = np.array([[1.0, -1.0], [-1.0, 1.0]])
    warm = (
        np.array([0.75, 0.25]),
        np.array([0.25, 0.75]),
    )
    monkeypatch.setattr(
        finite_game,
        "complementarity_candidate",
        lambda *args: None,
    )
    monkeypatch.setattr(
        finite_game,
        "bounded_mixed_candidates",
        lambda *args: (_ for _ in ()).throw(
            AssertionError("MILP fallback should precede the bounded Nashpy ensemble")
        ),
    )

    equilibria = finite_game.enumerate_bimatrix_equilibria(
        matching,
        -matching,
        initial_candidate=warm,
    )

    assert equilibria[0]["method"] == "highs_milp_complementarity"
    assert np.allclose(equilibria[0]["row_mix"], [0.5, 0.5], atol=1e-8)
    assert np.allclose(equilibria[0]["col_mix"], [0.5, 0.5], atol=1e-8)
    assert equilibria[0]["restricted_max_regret"] <= 1e-8


def test_milp_fallback_accepts_strict_raw_solution_when_polish_is_degenerate(
    monkeypatch,
):
    import pricing_sim.milp_equilibrium_solver as milp_solver

    from pricing_sim.finite_game import _restricted_regret

    matching = np.array([[1.0, -1.0], [-1.0, 1.0]])
    row = 1000.0 + 100.0 * matching
    col = 5000.0 - 50.0 * matching
    monkeypatch.setattr(milp_solver, "_support_polish", lambda *args: None)

    row_mix, col_mix = milp_solver.milp_equilibrium_candidate(row, col)
    row_regret, col_regret = _restricted_regret(row, col, row_mix, col_mix)

    assert np.allclose(row_mix, [0.5, 0.5], atol=1e-8)
    assert np.allclose(col_mix, [0.5, 0.5], atol=1e-8)
    assert max(row_regret, col_regret) <= 1e-8
