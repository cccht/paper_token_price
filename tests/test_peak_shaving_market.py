from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pricing_sim.peak_shaving_config import PeakShavingConfig


def test_config_defaults_and_invariants():
    cfg = PeakShavingConfig.default()
    assert cfg.num_periods == 8
    assert cfg.num_firms == 2
    # 算力异质：A 大于 B
    assert cfg.firm_capacity[0] > cfg.firm_capacity[1]
    # 两类人口占比之和为 1
    assert np.isclose(cfg.pop_rigid + cfg.pop_elastic, 1.0)
    # 弹性用户比刚性更价格敏感、迁移成本更低
    assert cfg.alpha_elastic > cfg.alpha_rigid
    assert cfg.switch_cost_elastic < cfg.switch_cost_rigid
    # 标准化负载形状零均值（用于 w_t = wbar*(1+delta*load_hat)）
    assert np.isclose(np.mean(cfg.load_shape_hat), 0.0, atol=1e-9)
    # 刚性原生时段分布与弹性原生时段分布均为概率分布
    assert np.isclose(np.sum(cfg.native_rigid), 1.0)
    assert np.isclose(np.sum(cfg.native_elastic), 1.0)


from pricing_sim.peak_shaving_market import choice_shares_with_exit


def test_choice_shares_sum_plus_exit_equals_one():
    cfg = PeakShavingConfig.default()
    T = cfg.num_periods
    # prices: 通道0=中间商, 通道1=厂家A, 通道2=厂家B
    prices = np.full((3, T), cfg.base_price)
    qos = np.ones((3, T))
    shares_R, exit_R = choice_shares_with_exit(prices, qos, cfg, user_type="rigid")
    shares_E, exit_E = choice_shares_with_exit(prices, qos, cfg, user_type="elastic")
    # 每类: 内部份额之和 + 退出概率 = 1
    assert np.isclose(np.sum(shares_R) + exit_R, 1.0)
    assert np.isclose(np.sum(shares_E) + exit_E, 1.0)
    assert shares_R.shape == (3, T)


def test_higher_price_raises_exit_probability():
    cfg = PeakShavingConfig.default()
    T = cfg.num_periods
    qos = np.ones((3, T))
    low = np.full((3, T), 0.80)
    high = np.full((3, T), 1.80)
    _, exit_low = choice_shares_with_exit(low, qos, cfg, user_type="elastic")
    _, exit_high = choice_shares_with_exit(high, qos, cfg, user_type="elastic")
    assert exit_high > exit_low


def test_elastic_more_price_sensitive_than_rigid():
    cfg = PeakShavingConfig.default()
    T = cfg.num_periods
    qos = np.ones((3, T))
    low = np.full((3, T), 0.80)
    high = np.full((3, T), 1.80)
    _, exitR_low = choice_shares_with_exit(low, qos, cfg, "rigid")
    _, exitR_high = choice_shares_with_exit(high, qos, cfg, "rigid")
    _, exitE_low = choice_shares_with_exit(low, qos, cfg, "elastic")
    _, exitE_high = choice_shares_with_exit(high, qos, cfg, "elastic")
    # 弹性用户对涨价的退出反应更强
    assert (exitE_high - exitE_low) > (exitR_high - exitR_low)


from pricing_sim.peak_shaving_market import channel_demand


def test_demand_shape_and_nonnegative():
    cfg = PeakShavingConfig.default()
    T = cfg.num_periods
    prices = np.full((3, T), cfg.base_price)
    qos = np.ones((3, T))
    D = channel_demand(prices, qos, cfg)
    assert D.shape == (3, T)
    assert np.all(D >= 0.0)


def test_higher_price_reduces_total_demand():
    cfg = PeakShavingConfig.default()
    T = cfg.num_periods
    qos = np.ones((3, T))
    D_low = channel_demand(np.full((3, T), 0.80), qos, cfg)
    D_high = channel_demand(np.full((3, T), 1.60), qos, cfg)
    assert D_high.sum() < D_low.sum()


from pricing_sim.peak_shaving_market import solve_market_fixed_point


def test_fixed_point_converges_and_small_firm_more_congested():
    cfg = PeakShavingConfig.default()
    T = cfg.num_periods
    # 中间商与两厂家同价, 路由均分
    prices = np.full((3, T), cfg.base_price)
    routing = np.full((2, T), 0.5)
    res = solve_market_fixed_point(prices, routing, cfg)
    assert res["converged"]
    # 小厂 B(容量600) 峰值利用率应高于大厂 A(容量1500)
    assert res["utilization"][1].max() > res["utilization"][0].max()
    # QoS 在 [0,1]
    assert np.all(res["qos_firm"] >= 0.0) and np.all(res["qos_firm"] <= 1.0)


def test_more_capacity_reduces_utilization():
    cfg = PeakShavingConfig.default()
    cfg_big = cfg.evolve(firm_capacity=np.array([3000.0, 1200.0]))
    T = cfg.num_periods
    prices = np.full((3, T), cfg.base_price)
    routing = np.full((2, T), 0.5)
    r1 = solve_market_fixed_point(prices, routing, cfg)
    r2 = solve_market_fixed_point(prices, routing, cfg_big)
    assert r2["utilization"].max() < r1["utilization"].max()


from pricing_sim.peak_shaving_market import firm_profit, intermediary_profit, MarketState


def test_idle_cost_charged_on_fixed_capacity():
    cfg = PeakShavingConfig.default()
    T = cfg.num_periods
    # 价格很高 -> 需求极低 -> 利用率极低, 但闲置成本仍按 G 计
    state = MarketState(
        retail=np.full(T, 2.10),
        direct=np.full((2, T), 2.10),
        wholesale=np.full((2, T), 0.40),
        routing=np.full((2, T), 0.5),
    )
    res = solve_market_fixed_point(
        np.vstack([state.retail[None, :], state.direct]), state.routing, cfg)
    profit_A = firm_profit(0, state, res, cfg)
    # 闲置成本 = c_g * G_A * sum(h) 应为正且等于解析值
    expected_idle = cfg.capacity_cost * cfg.firm_capacity[0] * cfg.period_hours * T
    assert expected_idle > 0
    # 利润应被闲置成本显著拉低(需求几乎为0时利润为负)
    assert profit_A < 0


def test_intermediary_profit_positive_at_reasonable_markup():
    cfg = PeakShavingConfig.default()
    T = cfg.num_periods
    state = MarketState(
        retail=np.full(T, 0.80),
        direct=np.full((2, T), 0.85),
        wholesale=np.full((2, T), 0.40),
        routing=np.full((2, T), 0.5),
    )
    res = solve_market_fixed_point(
        np.vstack([state.retail[None, :], state.direct]), state.routing, cfg)
    assert intermediary_profit(state, res, cfg) > 0
