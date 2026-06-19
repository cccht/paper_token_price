from __future__ import annotations

from dataclasses import dataclass

import numpy as np

from .config import SimulationConfig
from .demand import DemandResult, compute_demand
from .qos import qos_factor


@dataclass(frozen=True)
class PolicyEvaluation:
    prices: np.ndarray
    demand: DemandResult
    utilization: np.ndarray
    qos: np.ndarray
    posted_bill: float
    effective_bill: float
    profit: float
    welfare: float
    profit_components: dict[str, float]
    welfare_components: dict[str, float]


def _profit_components(
    prices: np.ndarray,
    demand: DemandResult,
    qos: np.ndarray,
    config: SimulationConfig,
) -> dict[str, float]:
    hours = config.period_hours
    gross_revenue = prices * demand.total * hours
    revenue_qos = qos if config.billing_mode == "effective" else 1.0
    revenue = float(np.sum(gross_revenue * revenue_qos))
    wholesale_cost = float(np.sum(config.wholesale_price * demand.total * hours))
    churned = np.maximum(config.rigid_baseline - demand.rigid, 0.0)
    churn_cost = float(np.sum(churned * config.churn_future_cost * hours))
    qos_churn_cost = float(np.sum(
        (1.0 - qos) * demand.rigid * config.degrade_churn_factor * hours
    ))
    components = {
        "revenue": revenue,
        "wholesale_cost": -wholesale_cost,
        "rigid_churn_cost": -churn_cost,
        "qos_churn_cost": -qos_churn_cost,
    }
    if config.billing_mode == "sla_penalty":
        components["sla_penalty"] = -float(np.sum(
            (1.0 - qos) * gross_revenue * config.sla_penalty_rate
        ))
    return components


def _welfare_components(
    prices: np.ndarray,
    demand: DemandResult,
    qos: np.ndarray,
    profit: float,
    config: SimulationConfig,
) -> dict[str, float]:
    hours = config.period_hours
    rigid_surplus = np.maximum(config.rigid_wtp - prices, 0.0) * demand.rigid * qos * hours
    effective_price = prices + config.inconvenience_cost * (1.0 - config.native_period_distribution)
    utility = -config.price_sensitivity * (effective_price - config.posted_price_cap)
    utility += np.log(config.time_preference + 1e-10)
    flex_surplus = np.log(np.sum(np.exp(utility))) / config.price_sensitivity
    flex_surplus *= float(np.sum(demand.flexible)) * hours
    carbon_cost = config.carbon_rate * config.carbon_unit_cost * np.sum(demand.total) * hours
    return {
        "platform_profit": profit,
        "rigid_consumer_surplus": float(np.sum(rigid_surplus)),
        "flexible_consumer_surplus": float(flex_surplus),
        "carbon_externality": -float(carbon_cost),
    }


def evaluate_policy(prices: np.ndarray, config: SimulationConfig) -> PolicyEvaluation:
    values = np.asarray(prices, dtype=float)
    demand = compute_demand(values, config)
    utilization = demand.total / config.capacity
    qos = qos_factor(utilization, threshold=config.qos_threshold, strength=config.qos_strength)
    posted_bill = float(np.sum(values * demand.total * config.period_hours))
    effective_bill = float(np.sum(values * demand.total * qos * config.period_hours))
    profit_components = _profit_components(values, demand, qos, config)
    profit = float(sum(profit_components.values()))
    welfare_components = _welfare_components(values, demand, qos, profit, config)
    return PolicyEvaluation(
        prices=values,
        demand=demand,
        utilization=utilization,
        qos=qos,
        posted_bill=posted_bill,
        effective_bill=effective_bill,
        profit=profit,
        welfare=float(sum(welfare_components.values())),
        profit_components=profit_components,
        welfare_components=welfare_components,
    )
