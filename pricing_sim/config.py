from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np


def _rigid_baseline() -> np.ndarray:
    return np.array([200, 150, 300, 600, 800, 900, 700, 250], dtype=float)


def _time_preference() -> np.ndarray:
    return np.array([0.3, 0.2, 0.5, 0.8, 1.0, 1.0, 0.9, 0.4], dtype=float)


def _native_period_distribution() -> np.ndarray:
    preference = _time_preference()
    return preference / np.sum(preference)


@dataclass(frozen=True)
class SimulationConfig:
    rigid_baseline: np.ndarray = field(default_factory=_rigid_baseline)
    time_preference: np.ndarray = field(default_factory=_time_preference)
    native_period_distribution: np.ndarray = field(default_factory=_native_period_distribution)
    period_hours: float = 3.0
    capacity: float = 950.0
    wholesale_price: float = 0.40
    posted_price_cap: float = 0.80
    price_lower_bound: float = 0.45
    price_upper_bound: float = 2.10
    rigid_wtp: float = 1.80
    rigid_churn_rate: float = 5.0
    flexible_baseline: float = 400.0
    price_sensitivity: float = 3.5
    inconvenience_cost: float = 0.20
    market_growth: float = 2.5
    qos_threshold: float = 0.82
    qos_strength: float = 15.0
    qos_feedback_weight: float = 0.0
    churn_future_cost: float = 0.60
    degrade_churn_factor: float = 0.35
    billing_mode: str = "effective"
    sla_penalty_rate: float = 0.20
    enforce_bill_protection: bool = False
    bill_cap_ratio: float = 1.0
    carbon_rate: float = 0.20
    carbon_unit_cost: float = 0.05
    optimizer_trials: int = 40
    optimizer_maxiter: int = 800

    def __post_init__(self) -> None:
        rigid = np.asarray(self.rigid_baseline, dtype=float)
        preference = np.asarray(self.time_preference, dtype=float)
        native = np.asarray(self.native_period_distribution, dtype=float)
        if rigid.ndim != 1 or rigid.size == 0:
            raise ValueError("rigid_baseline must be a non-empty vector")
        if preference.shape != rigid.shape:
            raise ValueError("rigid_baseline and time_preference must have equal length")
        if native.shape != rigid.shape:
            raise ValueError("native_period_distribution and time_preference must have equal length")
        if np.any(native < 0.0) or float(np.sum(native)) <= 0.0:
            raise ValueError("native_period_distribution must be non-negative with positive mass")
        if not self.price_lower_bound <= self.posted_price_cap <= self.price_upper_bound:
            raise ValueError("posted_price_cap must be inside price bounds")
        if self.capacity <= 0 or self.period_hours <= 0:
            raise ValueError("capacity and period_hours must be positive")
        if self.billing_mode not in {"effective", "full", "sla_penalty"}:
            raise ValueError("billing_mode must be effective, full, or sla_penalty")
        if self.sla_penalty_rate < 0:
            raise ValueError("sla_penalty_rate must be non-negative")
        if self.bill_cap_ratio <= 0:
            raise ValueError("bill_cap_ratio must be positive")
        object.__setattr__(self, "rigid_baseline", rigid)
        object.__setattr__(self, "time_preference", preference)
        object.__setattr__(self, "native_period_distribution", native / float(np.sum(native)))

    @property
    def num_periods(self) -> int:
        return int(self.rigid_baseline.size)

    @classmethod
    def default(cls, **overrides: object) -> "SimulationConfig":
        return replace(cls(), **overrides)
