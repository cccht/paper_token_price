from __future__ import annotations

import numpy as np
from scipy.optimize import least_squares

from .bimatrix_solver import _positive_affine_normalize

SUPPORT_THRESHOLDS = (1e-5, 1e-6, 1e-7, 1e-8, 1e-9)
POLISHED_REGRET_TOLERANCE = 1e-9


def _regret(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    row_mix: np.ndarray,
    col_mix: np.ndarray,
) -> float:
    row_values = payoff_row @ col_mix
    col_values = row_mix @ payoff_col
    return float(max(
        np.max(row_values) - row_mix @ row_values,
        np.max(col_values) - col_values @ col_mix,
        0.0,
    ))


def _fb_residual(
    vector: np.ndarray, payoff_row: np.ndarray, payoff_col: np.ndarray
) -> np.ndarray:
    rows, cols = payoff_row.shape
    row_mix = vector[:rows]
    col_mix = vector[rows:rows + cols]
    row_slack = vector[-2] - payoff_row @ col_mix
    col_slack = vector[-1] - row_mix @ payoff_col
    row_fb = np.sqrt(row_mix**2 + row_slack**2) - row_mix - row_slack
    col_fb = np.sqrt(col_mix**2 + col_slack**2) - col_mix - col_slack
    return np.r_[row_fb, col_fb, row_mix.sum() - 1.0, col_mix.sum() - 1.0]


def _initial_vector(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    initial_candidate: tuple[np.ndarray, np.ndarray] | None,
) -> np.ndarray:
    rows, cols = payoff_row.shape
    if initial_candidate is None:
        row_mix = np.full(rows, 1.0 / rows)
        col_mix = np.full(cols, 1.0 / cols)
    else:
        row_mix = np.clip(np.asarray(initial_candidate[0], dtype=float), 0.0, None)
        col_mix = np.clip(np.asarray(initial_candidate[1], dtype=float), 0.0, None)
        if row_mix.shape != (rows,) or col_mix.shape != (cols,):
            raise ValueError("initial mixed candidate has incompatible dimensions")
        row_mix /= row_mix.sum()
        col_mix /= col_mix.sum()
    return np.r_[
        row_mix,
        col_mix,
        np.max(payoff_row @ col_mix),
        np.max(row_mix @ payoff_col),
    ]


def _support_polish(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    row_guess: np.ndarray,
    col_guess: np.ndarray,
) -> tuple[np.ndarray, np.ndarray] | None:
    for threshold in SUPPORT_THRESHOLDS:
        row_support = np.flatnonzero(row_guess > threshold)
        col_support = np.flatnonzero(col_guess > threshold)
        if not len(row_support) or not len(col_support):
            continue
        row_block = payoff_row[np.ix_(row_support, col_support)]
        col_block = payoff_col[np.ix_(row_support, col_support)]
        row_system = np.block([
            [row_block, -np.ones((len(row_support), 1))],
            [np.ones((1, len(col_support))), np.zeros((1, 1))],
        ])
        col_system = np.block([
            [col_block.T, -np.ones((len(col_support), 1))],
            [np.ones((1, len(row_support))), np.zeros((1, 1))],
        ])
        col_solution = np.linalg.lstsq(
            row_system, np.r_[np.zeros(len(row_support)), 1.0], rcond=None
        )[0][:-1]
        row_solution = np.linalg.lstsq(
            col_system, np.r_[np.zeros(len(col_support)), 1.0], rcond=None
        )[0][:-1]
        if np.min(row_solution) < -1e-10 or np.min(col_solution) < -1e-10:
            continue
        row_mix = np.zeros(payoff_row.shape[0])
        col_mix = np.zeros(payoff_row.shape[1])
        row_mix[row_support] = np.clip(row_solution, 0.0, None)
        col_mix[col_support] = np.clip(col_solution, 0.0, None)
        row_mix /= row_mix.sum()
        col_mix /= col_mix.sum()
        if _regret(payoff_row, payoff_col, row_mix, col_mix) <= POLISHED_REGRET_TOLERANCE:
            return row_mix, col_mix
    return None


def complementarity_candidate(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    initial_candidate: tuple[np.ndarray, np.ndarray] | None,
) -> tuple[np.ndarray, np.ndarray] | None:
    row = _positive_affine_normalize(payoff_row)
    col = _positive_affine_normalize(payoff_col)
    initial = _initial_vector(row, col, initial_candidate)
    size = row.shape[0] + row.shape[1]
    result = least_squares(
        _fb_residual,
        initial,
        args=(row, col),
        bounds=(np.r_[np.zeros(size), 0.0, 0.0], np.r_[np.ones(size), 1.0, 1.0]),
        xtol=1e-13,
        ftol=1e-13,
        gtol=1e-13,
        max_nfev=5000,
    )
    row_mix = np.clip(result.x[:row.shape[0]], 0.0, None)
    col_mix = np.clip(result.x[row.shape[0]:size], 0.0, None)
    row_mix /= row_mix.sum()
    col_mix /= col_mix.sum()
    return _support_polish(row, col, row_mix, col_mix)
