from __future__ import annotations

import numpy as np


def qos_factor(
    utilization: np.ndarray,
    *,
    threshold: float,
    strength: float,
) -> np.ndarray:
    values = np.asarray(utilization, dtype=float)
    excess = np.maximum(values - threshold, 0.0)
    return np.exp(-strength * excess**2)
