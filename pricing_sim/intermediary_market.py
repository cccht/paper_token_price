from __future__ import annotations

from dataclasses import dataclass, field
import numpy as np
from scipy.special import expit


FIXED_POINT_MAX_ITERATIONS = 200
FIXED_POINT_TOLERANCE = 1e-9
QOS_DAMPING = 0.35


def _rigid_baseline() -> np.ndarray:
    return np.array([200, 150, 300, 600, 800, 900, 700, 250], dtype=float)


def _time_preference() -> np.ndarray:
    return np.array([0.30, 0.20, 0.50, 0.80, 1.00, 1.00, 0.90, 0.40], dtype=float)


def _native_period_distribution() -> np.ndarray:
    preference = _time_preference()
    return preference / np.sum(preference)


def _intermediary_capacity() -> np.ndarray:
    return np.array([1050.0, 1080.0, 1080.0], dtype=float)


def _brand_quality() -> np.ndarray:
    return np.array([1.04, 1.00, 0.96], dtype=float)


@dataclass(frozen=True)
class IntermediaryConfig:
    rigid_baseline: np.ndarray = field(default_factory=_rigid_baseline)
    time_preference: np.ndarray = field(default_factory=_time_preference)
    native_period_distribution: np.ndarray = field(default_factory=_native_period_distribution)
    intermediary_capacity: np.ndarray = field(default_factory=_intermediary_capacity)
    brand_quality: np.ndarray = field(default_factory=_brand_quality)
    period_hours: float = 3.0
    base_wholesale_price: float = 0.40
    base_retail_price: float = 0.80
    wholesale_lower_bound: float = 0.25
    wholesale_upper_bound: float = 0.90
    retail_lower_bound: float = 0.45
    retail_upper_bound: float = 2.10
    rigid_wtp: float = 1.80
    rigid_churn_rate: float = 5.0
    flexible_baseline: float = 400.0
    price_sensitivity: float = 3.5
    inconvenience_cost: float = 0.20
    market_growth: float = 1.2
    qos_threshold: float = 0.82
    qos_strength: float = 15.0
    qos_feedback_weight: float = 1.0
    capacity_cost: float = 0.015
    degrade_cost: float = 0.35
    optimizer_trials: int = 10
    optimizer_maxiter: int = 160
    num_players: int = 60
    random_seed: int = 42

    def __post_init__(self) -> None:
        rigid = np.asarray(self.rigid_baseline, dtype=float)
        preference = np.asarray(self.time_preference, dtype=float)
        native = np.asarray(self.native_period_distribution, dtype=float)
        capacity = np.asarray(self.intermediary_capacity, dtype=float)
        brand = np.asarray(self.brand_quality, dtype=float)
        if rigid.shape != preference.shape:
            raise ValueError("rigid_baseline and time_preference must match")
        if native.shape != preference.shape:
            raise ValueError("native_period_distribution and time_preference must match")
        if np.any(native < 0.0) or float(np.sum(native)) <= 0.0:
            raise ValueError("native_period_distribution must be non-negative with positive mass")
        if capacity.ndim != 1 or capacity.size == 0:
            raise ValueError("intermediary_capacity must be a non-empty vector")
        if brand.shape != capacity.shape:
            raise ValueError("brand_quality and intermediary_capacity must match")
        object.__setattr__(self, "rigid_baseline", rigid)
        object.__setattr__(self, "time_preference", preference)
        object.__setattr__(self, "native_period_distribution", native / float(np.sum(native)))
        object.__setattr__(self, "intermediary_capacity", capacity)
        object.__setattr__(self, "brand_quality", brand)

    @property
    def num_periods(self) -> int:
        return int(self.rigid_baseline.size)

    @property
    def num_intermediaries(self) -> int:
        return int(self.intermediary_capacity.size)

    @classmethod
    def default(cls, **overrides: object) -> "IntermediaryConfig":
        return cls(**overrides)


@dataclass(frozen=True)
class ThreeLayerResult:
    policy: str
    wholesale_prices: np.ndarray
    retail_prices: np.ndarray
    capacity: np.ndarray
    shares: np.ndarray
    demand: np.ndarray
    utilization: np.ndarray
    qos: np.ndarray
    platform_revenue: float
    intermediary_profit: float
    system_profit: float
    intermediary_components: dict[str, float]
    diagnostics: dict[str, float | int | bool | str]


def qos_factor(utilization: np.ndarray, config: IntermediaryConfig) -> np.ndarray:
    util = np.asarray(utilization, dtype=float)
    overload = np.maximum(util - config.qos_threshold, 0.0)
    return np.exp(-config.qos_strength * overload * overload)


def _default_capacity(config: IntermediaryConfig) -> np.ndarray:
    preference = config.time_preference / np.sum(config.time_preference)
    return config.intermediary_capacity[:, None] * preference[None, :]


def _choice_shares(
    retail: np.ndarray,
    qos: np.ndarray,
    config: IntermediaryConfig,
) -> np.ndarray:
    time_term = np.log(config.time_preference + 1e-10)[None, :]
    brand_term = np.log(config.brand_quality + 1e-10)[:, None]
    move_cost = config.inconvenience_cost * (1.0 - config.native_period_distribution)[None, :]
    utility = -config.price_sensitivity * (retail + move_cost - config.base_retail_price)
    utility += time_term + brand_term - config.qos_feedback_weight * (1.0 - qos)
    exp_utility = np.exp(utility - np.max(utility))
    return exp_utility / np.sum(exp_utility)


def _demand_from_shares(
    shares: np.ndarray,
    retail: np.ndarray,
    config: IntermediaryConfig,
) -> np.ndarray:
    period_share = np.sum(shares, axis=0)
    avg_price = float(np.sum(shares * retail))
    growth = 1.0 + config.market_growth * max(config.base_retail_price - avg_price, 0.0)
    flexible = config.flexible_baseline * growth * shares
    rigid_response = expit(config.rigid_churn_rate * (config.rigid_wtp - retail))
    rigid = config.rigid_baseline[None, :] * rigid_response * period_share[None, :]
    return rigid + flexible


def evaluate_three_layer_policy(
    wholesale: np.ndarray,
    retail: np.ndarray,
    capacity: np.ndarray,
    config: IntermediaryConfig,
    *,
    policy: str = "candidate",
) -> ThreeLayerResult:
    qos = np.ones_like(retail, dtype=float)
    shares = _choice_shares(retail, qos, config)
    demand = _demand_from_shares(shares, retail, config)
    converged = False
    iterations = 0
    for iterations in range(1, FIXED_POINT_MAX_ITERATIONS + 1):
        shares = _choice_shares(retail, qos, config)
        demand = _demand_from_shares(shares, retail, config)
        utilization = demand / np.maximum(capacity, 1e-8)
        target_qos = qos_factor(utilization, config)
        residual = float(np.max(np.abs(target_qos - qos)))
        if residual <= FIXED_POINT_TOLERANCE:
            converged = True
            break
        qos = QOS_DAMPING * target_qos + (1.0 - QOS_DAMPING) * qos
    if not converged:
        shares = _choice_shares(retail, qos, config)
        demand = _demand_from_shares(shares, retail, config)
    return _build_result(policy, wholesale, retail, capacity, shares, demand, qos, config, converged, iterations)


def _build_result(
    policy: str,
    wholesale: np.ndarray,
    retail: np.ndarray,
    capacity: np.ndarray,
    shares: np.ndarray,
    demand: np.ndarray,
    qos: np.ndarray,
    config: IntermediaryConfig,
    converged: bool,
    iterations: int,
) -> ThreeLayerResult:
    hours = config.period_hours
    utilization = demand / np.maximum(capacity, 1e-8)
    platform_revenue = float(np.sum(wholesale[None, :] * demand * qos * hours))
    retail_revenue = float(np.sum(retail * demand * qos * hours))
    wholesale_cost = platform_revenue
    capacity_cost = float(np.sum(config.capacity_cost * capacity * hours))
    qos_cost = float(np.sum(config.degrade_cost * (1.0 - qos) * demand * hours))
    components = {
        "retail_revenue": retail_revenue,
        "wholesale_cost": -wholesale_cost,
        "capacity_cost": -capacity_cost,
        "qos_degradation_cost": -qos_cost,
    }
    intermediary_profit = float(sum(components.values()))
    return ThreeLayerResult(
        policy, wholesale, retail, capacity, shares, demand, utilization, qos,
        platform_revenue, intermediary_profit, platform_revenue + intermediary_profit,
        components, {
            "converged": converged,
            "iterations": iterations,
            "objective_evaluations": 1,
            "min_qos": float(np.min(qos)),
            "max_utilization": float(np.max(utilization)),
        },
    )


def optimize_three_layer(
    config: IntermediaryConfig,
    *,
    qos_aware: bool = True,
    policy: str = "three_layer_qos_aware",
) -> ThreeLayerResult:
    from .three_stage_game import optimize_three_stage_stackelberg

    return optimize_three_stage_stackelberg(config, qos_aware=qos_aware, policy=policy)


def run_three_layer_smoke(config: IntermediaryConfig) -> dict[str, ThreeLayerResult]:
    full_capacity = _default_capacity(config)
    wholesale = np.full(config.num_periods, config.base_wholesale_price)
    retail = np.full((config.num_intermediaries, config.num_periods), config.base_retail_price)
    single_config = _single_config(config)
    single_capacity = _default_capacity(single_config)
    single_retail = np.full((single_config.num_intermediaries, single_config.num_periods), config.base_retail_price)
    direct = _direct_platform_accounting(
        evaluate_three_layer_policy(wholesale, retail, full_capacity, config, policy="direct_platform")
    )
    return {
        "uniform_retail": evaluate_three_layer_policy(wholesale, retail, full_capacity, config, policy="uniform_retail"),
        "direct_platform": direct,
        "single_intermediary": evaluate_three_layer_policy(wholesale, single_retail, single_capacity, single_config, policy="single_intermediary"),
        "no_qos_pricing": optimize_three_layer(config, qos_aware=False, policy="no_qos_pricing"),
        "three_layer_qos_aware": optimize_three_layer(config, qos_aware=True, policy="three_layer_qos_aware"),
    }


def _single_config(config: IntermediaryConfig) -> IntermediaryConfig:
    data = {**config.__dict__}
    data["intermediary_capacity"] = np.array([float(np.sum(config.intermediary_capacity))])
    data["brand_quality"] = np.array([1.0])
    return IntermediaryConfig.default(**data)


def _direct_platform_accounting(result: ThreeLayerResult) -> ThreeLayerResult:
    diagnostics = {**result.diagnostics, "accounting": "merged_retail_margin"}
    components = {
        "retail_revenue": 0.0,
        "wholesale_cost": 0.0,
        "capacity_cost": 0.0,
        "qos_degradation_cost": 0.0,
    }
    return ThreeLayerResult(
        result.policy,
        result.wholesale_prices,
        result.retail_prices,
        result.capacity,
        result.shares,
        result.demand,
        result.utilization,
        result.qos,
        result.system_profit,
        0.0,
        result.system_profit,
        components,
        diagnostics,
    )
