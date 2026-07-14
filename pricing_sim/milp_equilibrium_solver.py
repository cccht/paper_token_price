from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import Bounds, LinearConstraint, milp
from scipy.sparse import lil_matrix

from .bimatrix_solver import _positive_affine_normalize
from .complementarity_solver import _support_polish

MIP_TIME_LIMIT_SECONDS = 120.0


@dataclass(frozen=True)
class _VariableLayout:
    row_mix: slice
    col_mix: slice
    row_value: int
    col_value: int
    row_active: slice
    col_active: slice
    count: int


def _variable_layout(rows: int, cols: int) -> _VariableLayout:
    row_mix = slice(0, rows)
    col_mix = slice(rows, rows + cols)
    row_value = rows + cols
    col_value = row_value + 1
    row_active = slice(col_value + 1, col_value + 1 + rows)
    col_active = slice(row_active.stop, row_active.stop + cols)
    return _VariableLayout(
        row_mix,
        col_mix,
        row_value,
        col_value,
        row_active,
        col_active,
        col_active.stop,
    )


def _equilibrium_constraints(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    layout: _VariableLayout,
) -> LinearConstraint:
    rows, cols = payoff_row.shape
    count = 2 + 3 * rows + 3 * cols
    matrix = lil_matrix((count, layout.count))
    lower = np.full(count, -np.inf)
    upper = np.full(count, np.inf)
    index = 0
    matrix[index, layout.row_mix] = 1.0
    lower[index] = upper[index] = 1.0
    index += 1
    matrix[index, layout.col_mix] = 1.0
    lower[index] = upper[index] = 1.0
    index += 1
    for row_index in range(rows):
        matrix[index, layout.row_value] = 1.0
        matrix[index, layout.col_mix] = -payoff_row[row_index]
        lower[index] = 0.0
        index += 1
        matrix[index, layout.row_value] = 1.0
        matrix[index, layout.col_mix] = -payoff_row[row_index]
        matrix[index, layout.row_active.start + row_index] = 1.0
        upper[index] = 1.0
        index += 1
        matrix[index, layout.row_mix.start + row_index] = 1.0
        matrix[index, layout.row_active.start + row_index] = -1.0
        upper[index] = 0.0
        index += 1
    for col_index in range(cols):
        matrix[index, layout.col_value] = 1.0
        matrix[index, layout.row_mix] = -payoff_col[:, col_index]
        lower[index] = 0.0
        index += 1
        matrix[index, layout.col_value] = 1.0
        matrix[index, layout.row_mix] = -payoff_col[:, col_index]
        matrix[index, layout.col_active.start + col_index] = 1.0
        upper[index] = 1.0
        index += 1
        matrix[index, layout.col_mix.start + col_index] = 1.0
        matrix[index, layout.col_active.start + col_index] = -1.0
        upper[index] = 0.0
        index += 1
    return LinearConstraint(matrix.tocsr(), lower, upper)


def milp_equilibrium_candidate(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
) -> tuple[np.ndarray, np.ndarray] | None:
    row = _positive_affine_normalize(payoff_row)
    col = _positive_affine_normalize(payoff_col)
    layout = _variable_layout(*row.shape)
    integrality = np.zeros(layout.count)
    integrality[layout.row_active] = 1.0
    integrality[layout.col_active] = 1.0
    result = milp(
        np.zeros(layout.count),
        integrality=integrality,
        bounds=Bounds(np.zeros(layout.count), np.ones(layout.count)),
        constraints=_equilibrium_constraints(row, col, layout),
        options={"time_limit": MIP_TIME_LIMIT_SECONDS, "mip_rel_gap": 0.0},
    )
    if not result.success or result.x is None:
        return None
    row_mix = np.clip(result.x[layout.row_mix], 0.0, None)
    col_mix = np.clip(result.x[layout.col_mix], 0.0, None)
    row_mix /= np.sum(row_mix)
    col_mix /= np.sum(col_mix)
    return _support_polish(row, col, row_mix, col_mix)
