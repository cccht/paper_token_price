from __future__ import annotations

from multiprocessing import get_context
import queue as queue_module
from time import monotonic, sleep
import warnings

import numpy as np

MIXED_SOLVER_TIMEOUT_SECONDS = 120.0
MAX_LEMKE_LABELS = 64
POLL_INTERVAL_SECONDS = 0.01
NORMALIZED_REGRET_TOLERANCE = 1e-10


def _positive_affine_normalize(payoff: np.ndarray) -> np.ndarray:
    values = np.asarray(payoff, dtype=float)
    span = float(np.max(values) - np.min(values))
    if span <= 0.0:
        return np.zeros_like(values)
    return (values - np.min(values)) / span


def _valid_solver_candidate(
    pair: tuple[np.ndarray, np.ndarray],
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
) -> bool:
    row_mix = np.asarray(pair[0], dtype=float)
    col_mix = np.asarray(pair[1], dtype=float)
    if row_mix.shape != (payoff_row.shape[0],) or col_mix.shape != (payoff_row.shape[1],):
        return False
    if not np.all(np.isfinite(row_mix)) or not np.all(np.isfinite(col_mix)):
        return False
    row_mix = np.clip(row_mix, 0.0, None)
    col_mix = np.clip(col_mix, 0.0, None)
    if np.sum(row_mix) <= 0.0 or np.sum(col_mix) <= 0.0:
        return False
    row_mix /= np.sum(row_mix)
    col_mix /= np.sum(col_mix)
    row_values = payoff_row @ col_mix
    col_values = row_mix @ payoff_col
    regrets = (
        np.max(row_values) - row_mix @ row_values,
        np.max(col_values) - col_values @ col_mix,
    )
    return max(regrets) <= NORMALIZED_REGRET_TOLERANCE


def _solver_worker(
    method: str,
    label: int | None,
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
    output_queue: object,
) -> None:
    import nashpy as nash

    try:
        game = nash.Game(payoff_row, payoff_col)
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            if method == "lemke_howson":
                pair = game.lemke_howson(initial_dropped_label=int(label))
                name = f"lemke_howson_label_{label}"
            else:
                pair = next(game.vertex_enumeration(), None)
                name = "vertex_enumeration_first"
        if pair is not None:
            output_queue.put((name, pair))
    except BaseException:
        return


def _drain(output_queue: object) -> list[tuple[str, tuple]]:
    output = []
    while True:
        try:
            output.append(output_queue.get_nowait())
        except queue_module.Empty:
            return output


def bounded_mixed_candidates(
    payoff_row: np.ndarray,
    payoff_col: np.ndarray,
) -> list[tuple[str, tuple[np.ndarray, np.ndarray]]]:
    """Run a bounded parallel ensemble of exact bimatrix solvers."""
    solver_row = _positive_affine_normalize(payoff_row)
    solver_col = _positive_affine_normalize(payoff_col)
    context = get_context("fork")
    output_queue = context.Queue()
    label_count = min(MAX_LEMKE_LABELS, sum(payoff_row.shape))
    specifications = [
        ("lemke_howson", label) for label in range(label_count)
    ] + [("vertex_enumeration", None)]
    processes = [
        context.Process(
            target=_solver_worker,
            args=(method, label, solver_row, solver_col, output_queue),
        )
        for method, label in specifications
    ]
    for process in processes:
        process.start()

    deadline = monotonic() + MIXED_SOLVER_TIMEOUT_SECONDS
    candidates: list[tuple[str, tuple[np.ndarray, np.ndarray]]] = []
    while monotonic() < deadline and any(process.is_alive() for process in processes):
        candidates.extend(_drain(output_queue))
        if any(
            method == "vertex_enumeration_first"
            or _valid_solver_candidate(pair, solver_row, solver_col)
            for method, pair in candidates
        ):
            break
        for process in processes:
            process.join(timeout=0.0)
        sleep(POLL_INTERVAL_SECONDS)
    for process in processes:
        if process.is_alive():
            process.terminate()
        process.join()
    sleep(POLL_INTERVAL_SECONDS)
    candidates.extend(_drain(output_queue))
    output_queue.close()
    return candidates
