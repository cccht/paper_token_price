from __future__ import annotations

import numpy as np


def project_bounded_mean(
    raw: np.ndarray,
    *,
    cap: float,
    lower: float,
    upper: float,
    tolerance: float = 1e-12,
) -> np.ndarray:
    if lower > upper or not lower <= cap <= upper:
        raise ValueError("cap must be inside valid bounds")
    values = np.asarray(raw, dtype=float)
    low_shift = lower - float(np.max(values))
    high_shift = upper - float(np.min(values))
    for _ in range(100):
        shift = (low_shift + high_shift) / 2.0
        projected = np.clip(values + shift, lower, upper)
        if abs(float(np.mean(projected)) - cap) <= tolerance:
            return projected
        if float(np.mean(projected)) < cap:
            low_shift = shift
        else:
            high_shift = shift
    return np.clip(values + (low_shift + high_shift) / 2.0, lower, upper)
