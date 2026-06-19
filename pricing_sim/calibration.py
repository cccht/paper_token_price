from __future__ import annotations

import csv
from dataclasses import dataclass
from pathlib import Path

import numpy as np
from scipy.optimize import least_squares

from .qos import qos_factor


@dataclass(frozen=True)
class CalibrationResult:
    capacity_concurrency: float
    threshold: float
    strength: float
    rmse: float
    concurrency: np.ndarray
    utilization: np.ndarray
    observed_qos: np.ndarray
    fitted_qos: np.ndarray


def load_controlled_aggregate(source: Path) -> list[dict[str, float]]:
    with source.open(newline="", encoding="utf-8-sig") as handle:
        return [
            {
                "concurrency": float(row["concurrency"]),
                "observed_qos": float(row["ttft_sla_0_5_rate_mean"]),
            }
            for row in csv.DictReader(handle)
        ]


def _capacity_concurrency(points: list[dict[str, float]]) -> float:
    healthy = [row["concurrency"] for row in points if row["observed_qos"] >= 0.99]
    if not healthy:
        raise ValueError("at least one healthy concurrency point is required")
    return max(healthy)


def fit_qos_curve(points: list[dict[str, float]]) -> CalibrationResult:
    capacity = _capacity_concurrency(points)
    concurrency = np.array([row["concurrency"] for row in points], dtype=float)
    observed = np.array([row["observed_qos"] for row in points], dtype=float)
    utilization = concurrency / capacity

    def residuals(parameters: np.ndarray) -> np.ndarray:
        return qos_factor(utilization, threshold=parameters[0], strength=parameters[1]) - observed

    fitted = least_squares(residuals, x0=[1.0, 1.0], bounds=([1.0, 0.0], [2.0, 100.0]))
    threshold, strength = (float(value) for value in fitted.x)
    predicted = qos_factor(utilization, threshold=threshold, strength=strength)
    rmse = float(np.sqrt(np.mean((predicted - observed) ** 2)))
    return CalibrationResult(
        capacity,
        threshold,
        strength,
        rmse,
        concurrency,
        utilization,
        observed,
        predicted,
    )
