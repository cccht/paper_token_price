import numpy as np
import pytest

from pricing_sim.projection import project_bounded_mean


@pytest.mark.parametrize("cap", [0.45, 0.60, 0.80, 1.20, 2.10])
def test_projection_enforces_bounds_and_exact_mean(cap):
    raw = np.array([-1.0, 0.2, 0.5, 0.8, 1.1, 2.4, 3.0, 8.0])

    prices = project_bounded_mean(raw, cap=cap, lower=0.45, upper=2.10)

    assert np.all(prices >= 0.45)
    assert np.all(prices <= 2.10)
    assert abs(float(np.mean(prices)) - cap) <= 1e-8


def test_projection_rejects_cap_outside_bounds():
    with pytest.raises(ValueError, match="cap"):
        project_bounded_mean(np.array([0.5, 0.7]), cap=0.4, lower=0.45, upper=2.10)
