from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.special import expit, logsumexp

from .peak_shaving_config import PeakShavingConfig


def _channel_brand(config: PeakShavingConfig) -> np.ndarray:
    # 通道顺序: [中间商, 厂家A, 厂家B]
    return np.concatenate([[config.intermediary_brand], config.firm_brand])


def _type_params(config: PeakShavingConfig, user_type: str):
    if user_type == "rigid":
        return config.alpha_rigid, config.switch_cost_rigid, config.native_rigid
    if user_type == "elastic":
        return config.alpha_elastic, config.switch_cost_elastic, config.native_elastic
    raise ValueError(f"unknown user_type {user_type}")


def _utilities(prices: np.ndarray, qos: np.ndarray, config: PeakShavingConfig, user_type: str) -> np.ndarray:
    alpha, switch_cost, native = _type_params(config, user_type)
    brand = _channel_brand(config)  # (3,)
    time_term = np.log(config.time_preference + 1e-10)[None, :]
    brand_term = np.log(brand + 1e-10)[:, None]
    # 迁移成本: 偏离原生时段分布的人口期望 switch_cost*(1-native_t)
    move_cost = switch_cost * (1.0 - native)[None, :]
    utility = -alpha * (prices + move_cost - config.base_price)
    utility = utility + time_term + brand_term - config.qos_feedback_weight * (1.0 - qos)
    return utility


def choice_shares_with_exit(prices: np.ndarray, qos: np.ndarray, config: PeakShavingConfig, user_type: str):
    """Return (shares (3,T), exit_prob scalar). Shares sum + exit_prob == 1."""
    utility = _utilities(prices, qos, config, user_type)
    flat = utility.ravel()
    all_u = np.concatenate([flat, [config.outside_utility]])
    m = np.max(all_u)
    exp_all = np.exp(all_u - m)
    denom = float(np.sum(exp_all))
    inside = (exp_all[:-1] / denom).reshape(utility.shape)
    exit_prob = float(exp_all[-1] / denom)
    return inside, exit_prob


def inclusive_value(prices: np.ndarray, qos: np.ndarray, config: PeakShavingConfig, user_type: str) -> float:
    utility = _utilities(prices, qos, config, user_type)
    flat = np.concatenate([utility.ravel(), [config.outside_utility]])
    return float(logsumexp(flat))


def _type_demand(prices: np.ndarray, qos: np.ndarray, config: PeakShavingConfig, user_type: str) -> np.ndarray:
    shares, _ = choice_shares_with_exit(prices, qos, config, user_type)
    # 弹性市场规模因子: 平均价低于基准时市场扩张
    avg_price = float(np.sum(shares * prices)) / max(np.sum(shares), 1e-12)
    growth = 1.0 + config.market_growth * max(config.base_price - avg_price, 0.0)
    flexible = config.flexible_baseline * growth * shares
    # 刚性/重放需求: 按渠道自身份额分配(修正口径, 无 J 放大)
    rigid_response = expit(config.rigid_churn_rate * (config.rigid_wtp - prices))
    rigid = config.base_rigid[None, :] * rigid_response * shares
    return flexible + rigid


def channel_demand(prices: np.ndarray, qos: np.ndarray, config: PeakShavingConfig) -> np.ndarray:
    """Total per-channel demand (3,T), population-weighted over the two user types."""
    dR = _type_demand(prices, qos, config, "rigid")
    dE = _type_demand(prices, qos, config, "elastic")
    return config.pop_rigid * dR + config.pop_elastic * dE


def type_channel_demand(prices: np.ndarray, qos: np.ndarray, config: PeakShavingConfig,
                        user_type: str) -> np.ndarray:
    """Per-channel demand (3,T) for ONE user type, population-weighted. Used by the
    P1 load-migration experiment to track rigid vs elastic centroid shifts."""
    weight = config.pop_rigid if user_type == "rigid" else config.pop_elastic
    return weight * _type_demand(prices, qos, config, user_type)


FIXED_POINT_MAX_ITER = 200
FIXED_POINT_TOL = 1e-9
QOS_DAMPING = 0.35


def qos_factor(util: np.ndarray, config: PeakShavingConfig, shape: str = "threshold") -> np.ndarray:
    u = np.asarray(util, dtype=float)
    ubar = config.qos_threshold
    if shape == "threshold":
        excess = np.maximum(u - ubar, 0.0)
        return np.exp(-config.qos_strength * excess * excess)
    if shape == "linear":
        ubar_low = 0.5
        c_lin = 1.0 / (1.0 - ubar_low)
        return np.clip(1.0 - c_lin * np.maximum(u - ubar_low, 0.0), 0.0, 1.0)
    if shape == "sigmoid":
        return 1.0 / (1.0 + np.exp(np.clip(30.0 * (u - ubar), -50, 50)))
    if shape == "sqrt":
        return np.clip(1.0 - 2.5 * np.sqrt(np.maximum(u - ubar, 0.0)), 0.0, 1.0)
    raise ValueError(f"unknown qos shape {shape}")


def _firm_loads(demand: np.ndarray, routing: np.ndarray) -> np.ndarray:
    """demand (3,T) channels=[I,A,B]; routing (2,T) sums to 1 per period.
    Firm load = direct demand + routed intermediary demand."""
    intermediary = demand[0]            # (T,)
    direct = demand[1:]                 # (2,T) = [A,B]
    routed = routing * intermediary[None, :]   # (2,T)
    return direct + routed              # (2,T)


def solve_market_fixed_point(prices: np.ndarray, routing: np.ndarray, config: PeakShavingConfig,
                             qos_shape: str = "threshold") -> dict:
    """prices (3,T) channels=[I,A,B]; routing (2,T). Returns demand, firm loads,
    utilization, firm QoS, channel QoS, converged, iterations."""
    T = config.num_periods
    G = config.firm_capacity[:, None]   # (2,1)
    qos_firm = np.ones((2, T))
    converged = False
    iterations = 0
    for iterations in range(1, FIXED_POINT_MAX_ITER + 1):
        # channel QoS: 中间商通道的QoS是其路由组合的加权; 厂家直连通道用各自QoS
        qos_channel = np.vstack([
            np.sum(routing * qos_firm, axis=0)[None, :],  # 中间商通道
            qos_firm,                                      # A, B 直连
        ])
        demand = channel_demand(prices, qos_channel, config)
        loads = _firm_loads(demand, routing)
        util = loads / np.maximum(G, 1e-8)
        target = qos_factor(util, config, qos_shape)
        residual = float(np.max(np.abs(target - qos_firm)))
        if residual <= FIXED_POINT_TOL:
            converged = True
            break
        qos_firm = QOS_DAMPING * target + (1.0 - QOS_DAMPING) * qos_firm
    qos_channel = np.vstack([np.sum(routing * qos_firm, axis=0)[None, :], qos_firm])
    demand = channel_demand(prices, qos_channel, config)
    loads = _firm_loads(demand, routing)
    util = loads / np.maximum(G, 1e-8)
    return {
        "prices": prices, "routing": routing, "demand": demand,
        "loads": loads, "utilization": util, "qos_firm": qos_firm,
        "qos_channel": qos_channel, "converged": converged, "iterations": iterations,
    }


@dataclass(frozen=True)
class MarketState:
    retail: np.ndarray      # (T,) 中间商零售价
    direct: np.ndarray      # (2,T) 厂家直连价 [A,B]
    wholesale: np.ndarray   # (2,T) 厂家批发价 [A,B]
    routing: np.ndarray     # (2,T) 路由权重, 每时段和为1

    def channel_prices(self) -> np.ndarray:
        return np.vstack([self.retail[None, :], self.direct])  # (3,T)


def wholesale_settlement_by_firm(
    state: MarketState,
    res: dict,
    config: PeakShavingConfig,
) -> np.ndarray:
    """Completed intermediary traffic settled with each provider."""
    routed = state.routing * res["demand"][0][None, :]
    completed = routed * res["qos_firm"]
    return config.period_hours * np.sum(state.wholesale * completed, axis=1)


def firm_profit(idx: int, state: MarketState, res: dict, config: PeakShavingConfig) -> float:
    h = config.period_hours
    demand = res["demand"]            # (3,T)
    qos_firm = res["qos_firm"]        # (2,T)
    direct_demand = demand[1:][idx]   # (T,)
    routed = state.routing[idx] * demand[0]   # (T,)
    qos_m = qos_firm[idx]
    wholesale_rev = float(wholesale_settlement_by_firm(state, res, config)[idx])
    # 直连收入
    direct_rev = float(np.sum(state.direct[idx] * direct_demand * qos_m * h))
    # 闲置成本: 按固定算力计(无论是否用满)
    idle_cost = float(config.capacity_cost * config.firm_capacity[idx] * h * config.num_periods)
    # QoS 退化成本(对该厂家承载的总量)
    total_served = routed + direct_demand
    degrade_cost = float(np.sum(config.degrade_cost * (1.0 - qos_m) * total_served * h))
    return wholesale_rev + direct_rev - idle_cost - degrade_cost


def intermediary_profit(state: MarketState, res: dict, config: PeakShavingConfig) -> float:
    h = config.period_hours
    demand = res["demand"]
    intermediary_demand = demand[0]      # (T,)
    qos_channel = res["qos_channel"][0]  # 中间商通道QoS (T,)
    retail_rev = float(np.sum(state.retail * intermediary_demand * qos_channel * h))
    wholesale_cost = float(np.sum(wholesale_settlement_by_firm(state, res, config)))
    degrade_cost = float(np.sum(config.degrade_cost * (1.0 - qos_channel) * intermediary_demand * h))
    return retail_rev - wholesale_cost - degrade_cost


def system_profit(state: MarketState, res: dict, config: PeakShavingConfig) -> float:
    return (sum(firm_profit(i, state, res, config) for i in range(config.num_firms))
            + intermediary_profit(state, res, config))
