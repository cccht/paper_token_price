from pathlib import Path
import sys

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import expand_price, FirmParams


def test_delta_zero_gives_uniform_price():
    cfg = PeakShavingConfig.default()
    p = expand_price(base=0.80, delta=0.0, config=cfg, lower=0.45, upper=2.10)
    assert np.allclose(p, 0.80)


def test_positive_delta_raises_peak_price():
    cfg = PeakShavingConfig.default()
    p = expand_price(base=0.80, delta=0.3, config=cfg, lower=0.45, upper=2.10)
    peak_t = int(np.argmax(cfg.load_shape_hat))   # 负载最高时段
    trough_t = int(np.argmin(cfg.load_shape_hat)) # 负载最低时段
    assert p[peak_t] > p[trough_t]


def test_firm_params_roundtrip():
    fp = FirmParams(wbar=0.40, delta=0.2, pdbar=0.85, delta_d=0.1)
    vec = fp.to_vector()
    fp2 = FirmParams.from_vector(vec)
    assert np.allclose(vec, fp2.to_vector())
    assert vec.shape == (4,)


from pricing_sim.peak_shaving_equilibrium import (
    routing_from_beta, intermediary_best_response,
)
from pricing_sim.peak_shaving_market import MarketState, solve_market_fixed_point, intermediary_profit


def test_routing_prefers_cheaper_firm():
    cfg = PeakShavingConfig.default()
    T = cfg.num_periods
    w = np.vstack([np.full(T, 0.40), np.full(T, 0.60)])  # 厂家A便宜, B贵
    qos = np.ones((2, T))
    routing = routing_from_beta(w, qos, route_beta=3.0, config=cfg)
    assert np.all(routing[0] > routing[1])               # 更多流量给便宜的A
    assert np.allclose(routing.sum(axis=0), 1.0)


def test_intermediary_best_response_improves_profit():
    cfg = PeakShavingConfig.default()
    T = cfg.num_periods
    wA = np.full(T, 0.40); wB = np.full(T, 0.45)
    pdA = np.full(T, 0.85); pdB = np.full(T, 0.88)
    w = np.vstack([wA, wB]); pd = np.vstack([pdA, pdB])
    # 一个朴素初始: 零售加成固定, 路由均分
    naive = MarketState(retail=np.full(T, 0.80), direct=pd, wholesale=w, routing=np.full((2, T), 0.5))
    res0 = solve_market_fixed_point(naive.channel_prices(), naive.routing, cfg)
    p0 = intermediary_profit(naive, res0, cfg)
    best_state, best_res = intermediary_best_response(w, pd, cfg, n_starts=4)
    p1 = intermediary_profit(best_state, best_res, cfg)
    assert p1 >= p0 - 1e-6


from pricing_sim.peak_shaving_equilibrium import solve_firm_nash


def test_firm_nash_reaches_stable_profit():
    # 验收门是"经济量(系统利润)稳定", 而非参数范数收敛到求解器精度以下。
    # 用两次不同 max_sweeps 求解, 系统利润应几乎一致(参数微抖动不影响经济结论)。
    cfg = PeakShavingConfig.default()
    r_short = solve_firm_nash(cfg, max_sweeps=8, n_starts=3, seed=0)
    r_long = solve_firm_nash(cfg, max_sweeps=15, n_starts=3, seed=0)
    assert np.isfinite(r_short["system_profit"])
    assert len(r_long["firm_params"]) == 2
    rel = abs(r_long["system_profit"] - r_short["system_profit"]) / abs(r_long["system_profit"])
    assert rel < 0.05, f"system profit not stable across sweep budgets: rel={rel}"


def test_firm_nash_cross_seed_stability():
    cfg = PeakShavingConfig.default()
    profits = []
    for seed in (0, 1, 2):
        r = solve_firm_nash(cfg, max_sweeps=15, n_starts=3, seed=seed)
        profits.append(r["system_profit"])
    profits = np.array(profits)
    # 跨种子相对标准差应较小(<5%), 证明均衡稳定而非随机
    rel_std = np.std(profits) / np.mean(profits)
    assert rel_std < 0.05, f"cross-seed rel_std too high: {rel_std}"
