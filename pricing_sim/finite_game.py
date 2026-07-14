from __future__ import annotations

import numpy as np

from .bimatrix_solver import bounded_mixed_candidates
from .complementarity_solver import complementarity_candidate
from .milp_equilibrium_solver import milp_equilibrium_candidate

PURE_BEST_RESPONSE_TOLERANCE = 1e-10
RESTRICTED_EQUILIBRIUM_TOLERANCE = 1e-7


def _normalize_mix(values: np.ndarray, expected_size: int) -> np.ndarray:
    mix = np.asarray(values, dtype=float)
    if mix.shape != (expected_size,) or not np.all(np.isfinite(mix)):
        raise ValueError("invalid mixed strategy returned by bimatrix solver")
    mix = np.clip(mix, 0.0, None)
    total = float(np.sum(mix))
    if total <= 0.0:
        raise ValueError("mixed strategy has zero probability mass")
    mix /= total
    mix[mix < 1e-12] = 0.0
    return mix / np.sum(mix)


def _restricted_regret(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    row_mix: np.ndarray,
    col_mix: np.ndarray,
) -> tuple[float, float]:
    row_values = payoff_row @ col_mix
    col_values = row_mix @ payoff_col
    row_current = float(row_mix @ row_values)
    col_current = float(col_values @ col_mix)
    return (
        max(float(np.max(row_values)) - row_current, 0.0),
        max(float(np.max(col_values)) - col_current, 0.0),
    )


def _append_candidate(
    candidates: list[dict],
    pair: tuple[np.ndarray, np.ndarray],
    method: str,
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
) -> None:
    try:
        row_mix = _normalize_mix(pair[0], payoff_row.shape[0])
        col_mix = _normalize_mix(pair[1], payoff_row.shape[1])
    except ValueError:
        return
    for candidate in candidates:
        if np.allclose(row_mix, candidate["row_mix"], atol=1e-9) and np.allclose(
            col_mix, candidate["col_mix"], atol=1e-9
        ):
            candidate["methods"].append(method)
            return
    row_regret, col_regret = _restricted_regret(
        payoff_row, payoff_col, row_mix, col_mix
    )
    candidates.append({
        "row_mix": row_mix,
        "col_mix": col_mix,
        "row_restricted_regret": row_regret,
        "col_restricted_regret": col_regret,
        "restricted_max_regret": max(row_regret, col_regret),
        "method": method,
        "methods": [method],
    })


def _pure_equilibria(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
) -> list[dict]:
    candidates: list[dict] = []
    row_best = np.max(payoff_row, axis=0)
    col_best = np.max(payoff_col, axis=1)
    for row_index in range(payoff_row.shape[0]):
        for col_index in range(payoff_row.shape[1]):
            if payoff_row[row_index, col_index] < (
                row_best[col_index] - PURE_BEST_RESPONSE_TOLERANCE
            ):
                continue
            if payoff_col[row_index, col_index] < (
                col_best[row_index] - PURE_BEST_RESPONSE_TOLERANCE
            ):
                continue
            row_mix = np.zeros(payoff_row.shape[0])
            col_mix = np.zeros(payoff_row.shape[1])
            row_mix[row_index] = 1.0
            col_mix[col_index] = 1.0
            _append_candidate(
                candidates,
                (row_mix, col_mix),
                "pure_best_response",
                payoff_row,
                payoff_col,
            )
    return candidates


def enumerate_bimatrix_equilibria(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    initial_candidate: tuple[np.ndarray, np.ndarray] | None = None,
) -> list[dict]:
    """Return all pure equilibria or one bounded-time mixed equilibrium."""
    row = np.asarray(payoff_row, dtype=float)
    col = np.asarray(payoff_col, dtype=float)
    if row.ndim != 2 or col.shape != row.shape:
        raise ValueError("bimatrix payoffs must be aligned two-dimensional arrays")
    candidates = _pure_equilibria(row, col)
    if candidates:
        return candidates
    candidates = []
    if initial_candidate is not None:
        pair = complementarity_candidate(row, col, initial_candidate)
        if pair is not None:
            _append_candidate(
                candidates,
                pair,
                "fischer_burmeister_support_polish",
                row,
                col,
            )
    candidates = [
        candidate for candidate in candidates
        if candidate["restricted_max_regret"] <= RESTRICTED_EQUILIBRIUM_TOLERANCE
    ]
    if not candidates and initial_candidate is not None:
        pair = milp_equilibrium_candidate(row, col)
        if pair is not None:
            _append_candidate(
                candidates,
                pair,
                "highs_milp_complementarity",
                row,
                col,
            )
    if not candidates:
        for method, pair in bounded_mixed_candidates(row, col):
            _append_candidate(candidates, pair, method, row, col)
        candidates = [
            candidate for candidate in candidates
            if candidate["restricted_max_regret"] <= RESTRICTED_EQUILIBRIUM_TOLERANCE
        ]
    if not candidates and initial_candidate is None:
        pair = milp_equilibrium_candidate(row, col)
        if pair is not None:
            _append_candidate(
                candidates,
                pair,
                "highs_milp_complementarity",
                row,
                col,
            )
    if not candidates and initial_candidate is None:
        pair = complementarity_candidate(row, col, None)
        if pair is not None:
            _append_candidate(
                candidates,
                pair,
                "fischer_burmeister_support_polish",
                row,
                col,
            )
    if not candidates:
        raise RuntimeError(
            "bounded mixed-solver ensemble returned no valid restricted equilibrium"
        )
    return candidates


def default_support(size: int) -> list[int]:
    return sorted({0, size // 2, size - 1})


def serializable_selected(selected: dict) -> dict:
    output = {}
    for key, value in selected.items():
        if key in {"row_mix", "col_mix"}:
            continue
        if isinstance(value, np.generic):
            value = value.item()
        output[key] = value
    return output


def embed_mixed_candidate(
    old_rows: list[int],
    old_cols: list[int],
    new_rows: list[int],
    new_cols: list[int],
    row_mix: np.ndarray,
    col_mix: np.ndarray,
) -> tuple[np.ndarray, np.ndarray]:
    row_lookup = {index: probability for index, probability in zip(old_rows, row_mix)}
    col_lookup = {index: probability for index, probability in zip(old_cols, col_mix)}
    return (
        np.asarray([row_lookup.get(index, 0.0) for index in new_rows]),
        np.asarray([col_lookup.get(index, 0.0) for index in new_cols]),
    )


def select_full_grid_equilibrium(
    equilibria: list[dict],
    restricted_row: np.ndarray,
    restricted_col: np.ndarray,
    row_full_payoff: np.ndarray,
    col_full_payoff: np.ndarray,
) -> dict:
    """Select the restricted equilibrium with the lowest full-grid regret."""
    payoff_row = np.asarray(restricted_row, dtype=float)
    payoff_col = np.asarray(restricted_col, dtype=float)
    row_full = np.asarray(row_full_payoff, dtype=float)
    col_full = np.asarray(col_full_payoff, dtype=float)
    if row_full.shape[1] != payoff_row.shape[1]:
        raise ValueError("row full-payoff columns must match restricted columns")
    if col_full.shape[0] != payoff_row.shape[0]:
        raise ValueError("column full-payoff rows must match restricted rows")

    assessed = []
    for equilibrium in equilibria:
        row_mix = np.asarray(equilibrium["row_mix"], dtype=float)
        col_mix = np.asarray(equilibrium["col_mix"], dtype=float)
        row_current = float(row_mix @ (payoff_row @ col_mix))
        col_current = float((row_mix @ payoff_col) @ col_mix)
        row_values = row_full @ col_mix
        col_values = row_mix @ col_full
        row_best = int(np.argmax(row_values))
        col_best = int(np.argmax(col_values))
        row_regret = max(float(row_values[row_best]) - row_current, 0.0)
        col_regret = max(float(col_values[col_best]) - col_current, 0.0)
        scale = max(abs(row_current), abs(col_current), 1.0)
        assessed.append({
            **equilibrium,
            "row_expected_payoff": row_current,
            "col_expected_payoff": col_current,
            "row_best_response_index": row_best,
            "col_best_response_index": col_best,
            "row_best_response_payoff": float(row_values[row_best]),
            "col_best_response_payoff": float(col_values[col_best]),
            "row_full_regret": row_regret,
            "col_full_regret": col_regret,
            "full_max_regret": max(row_regret, col_regret),
            "relative_full_max_regret": max(row_regret, col_regret) / scale,
        })
    return min(
        assessed,
        key=lambda item: (
            item["full_max_regret"],
            item["restricted_max_regret"],
            -(item["row_expected_payoff"] + item["col_expected_payoff"]),
            item["method"],
        ),
    )
