from __future__ import annotations

from dataclasses import dataclass, field, replace

import numpy as np


def _base_rigid() -> np.ndarray:
    # 刚性需求基线：集中在下午高峰(第5-7时段)
    return np.array([200, 150, 300, 600, 800, 900, 700, 250], dtype=float)


def _time_preference() -> np.ndarray:
    return np.array([0.30, 0.20, 0.50, 0.80, 1.00, 1.00, 0.90, 0.40], dtype=float)


def _native_rigid() -> np.ndarray:
    # 刚性用户原生时段：强烈集中高峰
    pref = _time_preference() ** 2
    return pref / np.sum(pref)


def _native_elastic() -> np.ndarray:
    # 弹性用户原生时段：相对分散(接近均匀, 略偏白天)
    pref = np.sqrt(_time_preference())
    return pref / np.sum(pref)


def _load_shape_hat() -> np.ndarray:
    # 标准化负载形状(零均值), 用于 w_t = wbar*(1+delta*load_hat_t)
    pref = _time_preference()
    centered = pref - np.mean(pref)
    scale = np.max(np.abs(centered))
    return centered / scale  # 范围约[-1,1], 零均值


@dataclass(frozen=True)
class PeakShavingConfig:
    base_rigid: np.ndarray = field(default_factory=_base_rigid)
    time_preference: np.ndarray = field(default_factory=_time_preference)
    native_rigid: np.ndarray = field(default_factory=_native_rigid)
    native_elastic: np.ndarray = field(default_factory=_native_elastic)
    load_shape_hat: np.ndarray = field(default_factory=_load_shape_hat)
    firm_capacity: np.ndarray = field(default_factory=lambda: np.array([1500.0, 600.0]))
    firm_brand: np.ndarray = field(default_factory=lambda: np.array([1.0, 1.0]))  # 同质服务
    intermediary_brand: float = 1.05  # 聚合便利性略高
    period_hours: float = 3.0
    pop_rigid: float = 0.6
    pop_elastic: float = 0.4
    flexible_baseline: float = 400.0
    rigid_wtp: float = 1.80
    rigid_churn_rate: float = 5.0
    market_growth: float = 1.2
    base_price: float = 0.80
    price_lower: float = 0.45
    price_upper: float = 2.10
    wholesale_lower: float = 0.25
    wholesale_upper: float = 0.90
    alpha_rigid: float = 2.0
    alpha_elastic: float = 5.0
    switch_cost_rigid: float = 0.60
    switch_cost_elastic: float = 0.10
    qos_threshold: float = 0.82
    qos_strength: float = 15.0
    qos_feedback_weight: float = 1.0
    capacity_cost: float = 0.015     # 闲置/持有成本, 按固定算力计
    degrade_cost: float = 0.35
    outside_utility: float = 0.0
    random_seed: int = 42

    @property
    def num_periods(self) -> int:
        return int(self.base_rigid.size)

    @property
    def num_firms(self) -> int:
        return int(self.firm_capacity.size)

    @classmethod
    def default(cls, **overrides) -> "PeakShavingConfig":
        return cls(**overrides)

    def evolve(self, **overrides) -> "PeakShavingConfig":
        return replace(self, **overrides)
