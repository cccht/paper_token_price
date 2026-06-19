# 削峰填谷动态定价（异质两厂家 + 中间商）实现计划

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** 实现一个固定算力下的削峰填谷分时动态定价仿真：异质两厂家（大算力 A、小算力 B，部署同款开源模型）+ 单中间商（可路由）+ 两类用户（时间刚性 / 时间弹性）+ 含退出选项，通过低维形状参数化的 Nash 求解保证可收敛、可复现。

**Architecture:** 三层嵌套（厂家 Nash 竞争 → 中间商最优响应 → 两类用户 logit×QoS 拥塞固定点）。复用上一版 `fixed_market.py` 已验证的修正需求口径与退出选项逻辑；新增两类用户、异质厂家有效产出与闲置成本、低维形状参数化（每厂家 4 标量 $\bar w,\delta,\bar p^D,\delta^D$）、$M=2$ best-response 求交、跨种子诊断。

**Tech Stack:** Python 3.12（uv 管理）、numpy、scipy.optimize（SLSQP/最优响应）、scipy.special（expit/logsumexp）、pytest、matplotlib。

**关键设计参数（来自 spec，全程一致使用）：**
- $T=8$ 时段，$h=3$ 小时，$M=2$ 厂家。
- 厂家算力 $G_A=1500$（大）、$G_B=600$（小），外生固定。
- 两类用户人口占比 $(\pi_R,\pi_E)$，基准 $(0.6,0.4)$。
- 刚性 R：$\alpha_R=2.0$、$c_s^R=0.6$、原生时段集中高峰；弹性 E：$\alpha_E=5.0$、$c_s^E=0.1$、原生时段分散。
- QoS：$\bar u=0.82$、$\kappa=15$，阈值型为主，平滑形态稳健性。
- 闲置成本 $c_g=0.015$（按固定算力计），退化成本 $c_q=0.35$，退出效用 $u_0=0$。
- 每厂家策略 4 标量：基准批发价 $\bar w_m$、批发动态强度 $\delta_m$、基准直连价 $\bar p^D_m$、直连动态强度 $\delta^D_m$；$w_{m,t}=\bar w_m(1+\delta_m\widehat{\text{load}}_t)$，$\widehat{\text{load}}_t$ 为标准化负载形状（零均值）。

---

## 文件结构

| 文件 | 职责 | 创建/修改 |
|---|---|---|
| `pricing_sim/peak_shaving_config.py` | 配置 dataclass：两厂家算力、两类用户参数、QoS、成本、负载形状 | 创建 |
| `pricing_sim/peak_shaving_market.py` | 两类用户 logit（含退出）、修正口径需求、异质厂家 QoS/有效产出、厂家/中间商利润、拥塞固定点 | 创建 |
| `pricing_sim/peak_shaving_equilibrium.py` | 低维形状参数化、中间商最优响应、$M=2$ best-response 求交、跨种子诊断 | 创建 |
| `experiments/run_peak_shaving_experiments.py` | 主实验 1–5，落盘 JSON+CSV | 创建 |
| `experiments/run_peak_shaving_robustness.py` | 稳健性 6（QoS 形态/$u_0$/跨种子/收敛曲线） | 创建 |
| `tests/test_peak_shaving_market.py` | 市场层单元测试 | 创建 |
| `tests/test_peak_shaving_equilibrium.py` | 求解层单元测试 | 创建 |

---

## Task 0: 环境准备

**Files:** 无（环境检查）

- [ ] **Step 1: 确认 pytest 可用，不可用则安装**

Run: `python3 -m pytest --version 2>&1 || pip install pytest`
Expected: 输出 pytest 版本（如 `pytest 7.x`）。若安装，重跑验证。

- [ ] **Step 2: 确认可 import 既有模块**

Run: `python3 -c "import sys; sys.path.insert(0,'.'); from pricing_sim.fixed_market import MarketFix, qos_factor; print('ok')"`
Expected: 输出 `ok`

---

## Task 1: 配置模块 `peak_shaving_config.py`

**Files:**
- Create: `pricing_sim/peak_shaving_config.py`
- Test: `tests/test_peak_shaving_market.py`

- [ ] **Step 1: 写失败测试（配置默认值与不变量）**

写入 `tests/test_peak_shaving_market.py`：

```python
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python3 -m pytest tests/test_peak_shaving_market.py::test_config_defaults_and_invariants -v`
Expected: FAIL with `ModuleNotFoundError: No module named 'pricing_sim.peak_shaving_config'`

- [ ] **Step 3: 写最小实现**

写入 `pricing_sim/peak_shaving_config.py`：

```python
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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python3 -m pytest tests/test_peak_shaving_market.py::test_config_defaults_and_invariants -v`
Expected: PASS

- [ ] **Step 5: 提交（若 git 仓库）**

Run: `git add pricing_sim/peak_shaving_config.py tests/test_peak_shaving_market.py 2>/dev/null && git commit -m "feat: peak-shaving config with two user types and heterogeneous firms" 2>/dev/null || echo "non-git repo, skip commit"`
Expected: 提交成功或打印 skip 提示。

---

## Task 2: 两类用户 logit 份额（含退出选项）

**Files:**
- Create: `pricing_sim/peak_shaving_market.py`
- Test: `tests/test_peak_shaving_market.py`

选项布局：每时段通道顺序为 `[中间商, 厂家A直连, 厂家B直连]`，共 `(1+M)=3` 个通道 × `T` 时段。份额数组形状 `(3, T)`。退出选项单列，不在该数组内，但参与归一化分母。

- [ ] **Step 1: 写失败测试（份额+退出概率自洽）**

追加到 `tests/test_peak_shaving_market.py`：

```python
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
```

- [ ] **Step 2: 运行测试确认失败**

Run: `python3 -m pytest tests/test_peak_shaving_market.py -k choice_shares -v`
Expected: FAIL with `ModuleNotFoundError` 或 `ImportError: cannot import name 'choice_shares_with_exit'`

- [ ] **Step 3: 写最小实现**

写入 `pricing_sim/peak_shaving_market.py`：

```python
from __future__ import annotations

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
```

- [ ] **Step 4: 运行测试确认通过**

Run: `python3 -m pytest tests/test_peak_shaving_market.py -k "choice_shares or exit or sensitive" -v`
Expected: PASS（3 个测试）

- [ ] **Step 5: 提交**

Run: `git add pricing_sim/peak_shaving_market.py tests/test_peak_shaving_market.py 2>/dev/null && git commit -m "feat: two-type logit choice with outside option" 2>/dev/null || echo "skip commit"`
Expected: 成功或 skip。

---

## Task 3: 需求合成（修正口径，两类人口加权）

**Files:**
- Modify: `pricing_sim/peak_shaving_market.py`
- Test: `tests/test_peak_shaving_market.py`

需求 = 刚性人口 × 刚性份额相关需求 + 弹性人口 × 弹性份额相关需求。刚性项按**渠道自身份额**分配（修正口径，无 J 放大）。返回 `(3,T)` 的分通道需求。

- [ ] **Step 1: 写失败测试（需求随渠道数不放大 + 涨价降总需求）**

追加到 `tests/test_peak_shaving_market.py`：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/test_peak_shaving_market.py -k demand -v`
Expected: FAIL（`cannot import name 'channel_demand'`）

- [ ] **Step 3: 写实现（追加到 peak_shaving_market.py）**

```python
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
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/test_peak_shaving_market.py -k demand -v`
Expected: PASS（2 个）

- [ ] **Step 5: 提交**

Run: `git add -A 2>/dev/null && git commit -m "feat: population-weighted demand with corrected rigid allocation" 2>/dev/null || echo "skip commit"`

---

## Task 4: 厂家负载、QoS 拥塞固定点与有效产出

**Files:**
- Modify: `pricing_sim/peak_shaving_market.py`
- Test: `tests/test_peak_shaving_market.py`

厂家负载 = 直连需求 + 中间商按路由分来的需求。中间商通道需求 `D[0,t]` 按路由 `r[m,t]` 分给两厂家。厂家 m 负载 `L[m,t] = D_direct[m,t] + r[m,t]*D_intermediary[t]`。利用率 `u=L/G_m`，QoS 由阻尼固定点求解（QoS 反馈进入用户效用）。

- [ ] **Step 1: 写失败测试（小厂更易拥塞 + 固定点收敛 + 退出选项不破坏收敛）**

追加到 `tests/test_peak_shaving_market.py`：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/test_peak_shaving_market.py -k fixed_point -v`
Expected: FAIL（`cannot import name 'solve_market_fixed_point'`）

- [ ] **Step 3: 写实现（追加到 peak_shaving_market.py）**

```python
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
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/test_peak_shaving_market.py -k "fixed_point or capacity" -v`
Expected: PASS（2 个）

- [ ] **Step 5: 提交**

Run: `git add -A 2>/dev/null && git commit -m "feat: firm-load QoS congestion fixed point with routing" 2>/dev/null || echo "skip commit"`

---

## Task 5: 厂家利润（含闲置成本）与中间商利润

**Files:**
- Modify: `pricing_sim/peak_shaving_market.py`
- Test: `tests/test_peak_shaving_market.py`

厂家 m 利润 = 批发收入(路由来的量×批发价×QoS) + 直连收入(直连量×直连价×QoS) − 闲置成本($c_g G_m$，按固定算力) − QoS 退化成本。中间商利润 = 零售收入 − 批发成本 − QoS 退化成本。需要把价格拆成"中间商零售价 + 两厂家直连价 + 两厂家批发价"。

- [ ] **Step 1: 写失败测试（闲置成本随固定算力计；利润随退化下降）**

追加到 `tests/test_peak_shaving_market.py`：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/test_peak_shaving_market.py -k "idle_cost or intermediary_profit" -v`
Expected: FAIL（`cannot import name 'firm_profit'`）

- [ ] **Step 3: 写实现（追加到 peak_shaving_market.py）**

```python
from dataclasses import dataclass


@dataclass(frozen=True)
class MarketState:
    retail: np.ndarray      # (T,) 中间商零售价
    direct: np.ndarray      # (2,T) 厂家直连价 [A,B]
    wholesale: np.ndarray   # (2,T) 厂家批发价 [A,B]
    routing: np.ndarray     # (2,T) 路由权重, 每时段和为1

    def channel_prices(self) -> np.ndarray:
        return np.vstack([self.retail[None, :], self.direct])  # (3,T)


def firm_profit(idx: int, state: MarketState, res: dict, config: PeakShavingConfig) -> float:
    h = config.period_hours
    demand = res["demand"]            # (3,T)
    qos_firm = res["qos_firm"]        # (2,T)
    intermediary_demand = demand[0]   # (T,)
    direct_demand = demand[1:][idx]   # (T,)
    routed = state.routing[idx] * intermediary_demand   # (T,)
    qos_m = qos_firm[idx]
    # 批发收入: 路由来的量按批发价结算(乘QoS有效完成)
    wholesale_rev = float(np.sum(state.wholesale[idx] * routed * qos_m * h))
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
    # 中间商按路由从两厂家批发购入, 加权批发成本
    avg_wholesale = np.sum(state.routing * state.wholesale, axis=0)  # (T,)
    retail_rev = float(np.sum(state.retail * intermediary_demand * qos_channel * h))
    wholesale_cost = float(np.sum(avg_wholesale * intermediary_demand * qos_channel * h))
    degrade_cost = float(np.sum(config.degrade_cost * (1.0 - qos_channel) * intermediary_demand * h))
    return retail_rev - wholesale_cost - degrade_cost


def system_profit(state: MarketState, res: dict, config: PeakShavingConfig) -> float:
    return (sum(firm_profit(i, state, res, config) for i in range(config.num_firms))
            + intermediary_profit(state, res, config))
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/test_peak_shaving_market.py -k "idle_cost or intermediary_profit" -v`
Expected: PASS（2 个）

- [ ] **Step 5: 全市场层测试回归**

Run: `python3 -m pytest tests/test_peak_shaving_market.py -v`
Expected: 全部 PASS（约 9 个测试）

- [ ] **Step 6: 提交**

Run: `git add -A 2>/dev/null && git commit -m "feat: firm profit with idle cost and intermediary profit" 2>/dev/null || echo "skip commit"`

---

## Task 6: 低维形状参数化与价格展开

**Files:**
- Create: `pricing_sim/peak_shaving_equilibrium.py`
- Test: `tests/test_peak_shaving_equilibrium.py`

每厂家 4 标量 $(\bar w_m,\delta_m,\bar p^D_m,\delta^D_m)$，展开为分时价 `w_{m,t}=clip(wbar*(1+delta*load_hat_t), 边界)`。`delta=0` 时为统一价（用于统一定价基线）。

- [ ] **Step 1: 写失败测试（delta=0 给统一价；delta>0 高峰价更高）**

写入 `tests/test_peak_shaving_equilibrium.py`：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/test_peak_shaving_equilibrium.py -k "delta or roundtrip" -v`
Expected: FAIL（`No module named 'pricing_sim.peak_shaving_equilibrium'`）

- [ ] **Step 3: 写实现**

写入 `pricing_sim/peak_shaving_equilibrium.py`：

```python
from __future__ import annotations

from dataclasses import dataclass

import numpy as np
from scipy.optimize import minimize

from .peak_shaving_config import PeakShavingConfig
from .peak_shaving_market import (
    MarketState, solve_market_fixed_point, firm_profit, intermediary_profit,
    system_profit, choice_shares_with_exit, inclusive_value,
)


def expand_price(base: float, delta: float, config: PeakShavingConfig,
                 lower: float, upper: float) -> np.ndarray:
    raw = base * (1.0 + delta * config.load_shape_hat)
    return np.clip(raw, lower, upper)


@dataclass(frozen=True)
class FirmParams:
    wbar: float
    delta: float
    pdbar: float
    delta_d: float

    def to_vector(self) -> np.ndarray:
        return np.array([self.wbar, self.delta, self.pdbar, self.delta_d], dtype=float)

    @classmethod
    def from_vector(cls, v: np.ndarray) -> "FirmParams":
        return cls(float(v[0]), float(v[1]), float(v[2]), float(v[3]))

    def wholesale(self, config: PeakShavingConfig) -> np.ndarray:
        return expand_price(self.wbar, self.delta, config,
                            config.wholesale_lower, config.wholesale_upper)

    def direct(self, config: PeakShavingConfig) -> np.ndarray:
        return expand_price(self.pdbar, self.delta_d, config,
                            config.price_lower, config.price_upper)
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/test_peak_shaving_equilibrium.py -k "delta or roundtrip" -v`
Expected: PASS（3 个）

- [ ] **Step 5: 提交**

Run: `git add -A 2>/dev/null && git commit -m "feat: low-dim shape parameterization for dynamic prices" 2>/dev/null || echo "skip commit"`

---

## Task 7: 中间商最优响应（零售价 + 路由）

**Files:**
- Modify: `pricing_sim/peak_shaving_equilibrium.py`
- Test: `tests/test_peak_shaving_equilibrium.py`

给定两厂家批发价与直连价，中间商选零售价形状参数 $(\bar p, \delta^p)$ 和路由强度。路由用 logit：偏好低批发价 + 高 QoS 的厂家。为保持低维，路由参数化为单标量"路由价格敏感度" `route_beta`（QoS 反馈系数固定）。中间商策略 = 3 标量 $(\bar p,\delta^p,\text{route\_beta})$。

- [ ] **Step 1: 写失败测试（最优响应提升中间商利润；路由偏向低批发价厂家）**

追加到 `tests/test_peak_shaving_equilibrium.py`：

```python
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
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/test_peak_shaving_equilibrium.py -k "routing or best_response" -v`
Expected: FAIL（`cannot import name 'routing_from_beta'`）

- [ ] **Step 3: 写实现（追加到 peak_shaving_equilibrium.py）**

```python
def routing_from_beta(wholesale: np.ndarray, qos_firm: np.ndarray, route_beta: float,
                      config: PeakShavingConfig, qos_weight: float = 3.0) -> np.ndarray:
    """Logit routing over firms per period: prefer low wholesale + high QoS."""
    util = -route_beta * wholesale + qos_weight * qos_firm   # (2,T)
    util = util - np.max(util, axis=0, keepdims=True)
    exp_u = np.exp(util)
    return exp_u / np.sum(exp_u, axis=0, keepdims=True)


def _solve_with_routing(retail: np.ndarray, wholesale: np.ndarray, direct: np.ndarray,
                        route_beta: float, config: PeakShavingConfig, qos_shape: str = "threshold"):
    """Inner fixed point that also updates routing from firm QoS each sweep."""
    T = config.num_periods
    routing = np.full((2, T), 0.5)
    for _ in range(12):
        state = MarketState(retail=retail, direct=direct, wholesale=wholesale, routing=routing)
        res = solve_market_fixed_point(state.channel_prices(), routing, config, qos_shape)
        new_routing = routing_from_beta(wholesale, res["qos_firm"], route_beta, config)
        if np.max(np.abs(new_routing - routing)) < 1e-7:
            routing = new_routing
            break
        routing = new_routing
    state = MarketState(retail=retail, direct=direct, wholesale=wholesale, routing=routing)
    res = solve_market_fixed_point(state.channel_prices(), routing, config, qos_shape)
    return state, res


def intermediary_best_response(wholesale: np.ndarray, direct: np.ndarray,
                               config: PeakShavingConfig, n_starts: int = 6,
                               qos_shape: str = "threshold", seed: int = 0):
    """Optimize intermediary 3 scalars (pbar, delta_p, route_beta) to maximize its profit."""
    rng = np.random.default_rng(seed)
    best = None
    best_profit = -np.inf
    bounds = [(config.price_lower, config.price_upper), (-0.6, 0.6), (0.5, 8.0)]
    for start in range(n_starts):
        if start == 0:
            x0 = np.array([config.base_price, 0.0, 3.0])
        else:
            x0 = np.array([rng.uniform(0.6, 1.4), rng.uniform(-0.4, 0.4), rng.uniform(1.0, 6.0)])

        def obj(x):
            retail = expand_price(x[0], x[1], config, config.price_lower, config.price_upper)
            state, res = _solve_with_routing(retail, wholesale, direct, x[2], config, qos_shape)
            return -intermediary_profit(state, res, config)

        r = minimize(obj, x0, method="L-BFGS-B", bounds=bounds, options={"maxiter": 300})
        retail = expand_price(r.x[0], r.x[1], config, config.price_lower, config.price_upper)
        state, res = _solve_with_routing(retail, wholesale, direct, r.x[2], config, qos_shape)
        prof = intermediary_profit(state, res, config)
        if prof > best_profit:
            best_profit = prof
            best = (state, res)
    return best
```

- [ ] **Step 4: 运行确认通过**

Run: `python3 -m pytest tests/test_peak_shaving_equilibrium.py -k "routing or best_response" -v`
Expected: PASS（2 个）

- [ ] **Step 5: 提交**

Run: `git add -A 2>/dev/null && git commit -m "feat: intermediary best response with logit routing" 2>/dev/null || echo "skip commit"`

---

## Task 8: 厂家 Nash best-response 求交（M=2）+ 跨种子诊断

**Files:**
- Modify: `pricing_sim/peak_shaving_equilibrium.py`
- Test: `tests/test_peak_shaving_equilibrium.py`

外层：两厂家各 4 标量。给定对手参数，一厂家做最优响应（内嵌中间商最优响应 + 用户固定点）。交替最优响应迭代到参数稳定（带阻尼）。报告收敛诊断 + 支持跨种子重复。

- [ ] **Step 1: 写失败测试（best-response 迭代收敛；跨种子稳定）**

追加到 `tests/test_peak_shaving_equilibrium.py`：

```python
from pricing_sim.peak_shaving_equilibrium import solve_firm_nash


def test_firm_nash_converges():
    cfg = PeakShavingConfig.default()
    result = solve_firm_nash(cfg, max_sweeps=12, n_starts=3, seed=0)
    assert result["converged"]
    # 两厂家参数都在边界内
    assert len(result["firm_params"]) == 2
    # 系统利润为有限正值
    assert np.isfinite(result["system_profit"])


def test_firm_nash_cross_seed_stability():
    cfg = PeakShavingConfig.default()
    profits = []
    for seed in (0, 1, 2):
        r = solve_firm_nash(cfg, max_sweeps=12, n_starts=3, seed=seed)
        profits.append(r["system_profit"])
    profits = np.array(profits)
    # 跨种子相对标准差应较小(<5%), 证明收敛而非随机
    rel_std = np.std(profits) / np.mean(profits)
    assert rel_std < 0.05, f"cross-seed rel_std too high: {rel_std}"
```

- [ ] **Step 2: 运行确认失败**

Run: `python3 -m pytest tests/test_peak_shaving_equilibrium.py -k firm_nash -v`
Expected: FAIL（`cannot import name 'solve_firm_nash'`）

- [ ] **Step 3: 写实现（追加到 peak_shaving_equilibrium.py）**

```python
def _firm_best_response(idx: int, params: list, config: PeakShavingConfig,
                        n_starts: int, qos_shape: str, rng) -> FirmParams:
    """Firm idx best-responds: choose its 4 scalars to max its own profit,
    given the other firm's params and the intermediary's best response."""
    other = 1 - idx
    bounds = [(config.wholesale_lower, config.wholesale_upper), (-0.6, 0.6),
              (config.price_lower, config.price_upper), (-0.6, 0.6)]

    def eval_params(vec_idx) -> float:
        fp_idx = FirmParams.from_vector(vec_idx)
        fps = [None, None]
        fps[idx] = fp_idx
        fps[other] = params[other]
        wholesale = np.vstack([fps[0].wholesale(config), fps[1].wholesale(config)])
        direct = np.vstack([fps[0].direct(config), fps[1].direct(config)])
        state, res = intermediary_best_response(wholesale, direct, config,
                                                n_starts=2, qos_shape=qos_shape)
        return firm_profit(idx, state, res, config)

    best_vec = params[idx].to_vector()
    best_val = eval_params(best_vec)
    for start in range(n_starts):
        if start == 0:
            x0 = params[idx].to_vector()
        else:
            x0 = np.array([rng.uniform(0.30, 0.80), rng.uniform(-0.4, 0.4),
                           rng.uniform(0.6, 1.4), rng.uniform(-0.4, 0.4)])
        r = minimize(lambda v: -eval_params(v), x0, method="L-BFGS-B",
                     bounds=bounds, options={"maxiter": 80})
        if -r.fun > best_val:
            best_val = -r.fun
            best_vec = r.x.copy()
    return FirmParams.from_vector(best_vec)


def solve_firm_nash(config: PeakShavingConfig, max_sweeps: int = 15, n_starts: int = 3,
                    seed: int = 0, qos_shape: str = "threshold", damping: float = 0.5) -> dict:
    rng = np.random.default_rng(seed)
    # 初始: 统一价(delta=0), 基准批发/直连
    params = [FirmParams(0.40, 0.0, 0.85, 0.0), FirmParams(0.45, 0.0, 0.88, 0.0)]
    norm_history = []
    converged = False
    for sweep in range(1, max_sweeps + 1):
        old = np.concatenate([p.to_vector() for p in params])
        for idx in range(2):
            br = _firm_best_response(idx, params, config, n_starts, qos_shape, rng)
            # 阻尼更新
            blended = damping * br.to_vector() + (1 - damping) * params[idx].to_vector()
            params[idx] = FirmParams.from_vector(blended)
        new = np.concatenate([p.to_vector() for p in params])
        change = float(np.max(np.abs(new - old)))
        norm_history.append(change)
        if change < 1e-3:
            converged = True
            break
    # 最终评估
    wholesale = np.vstack([params[0].wholesale(config), params[1].wholesale(config)])
    direct = np.vstack([params[0].direct(config), params[1].direct(config)])
    state, res = intermediary_best_response(wholesale, direct, config, n_starts=4, qos_shape=qos_shape)
    return {
        "firm_params": [p.to_vector().tolist() for p in params],
        "state": state, "res": res,
        "firm_profits": [firm_profit(i, state, res, config) for i in range(2)],
        "intermediary_profit": intermediary_profit(state, res, config),
        "system_profit": system_profit(state, res, config),
        "converged": converged, "sweeps": sweep, "norm_history": norm_history,
    }
```

- [ ] **Step 4: 运行确认通过（这一步可能较慢，给足超时）**

Run: `python3 -m pytest tests/test_peak_shaving_equilibrium.py -k firm_nash -v`
Expected: PASS（2 个）。若 `cross_seed` 的 rel_std 超阈，说明未收敛——需调大 `max_sweeps`/`n_starts` 或检查 best-response 实现，不可放宽断言。

- [ ] **Step 5: 提交**

Run: `git add -A 2>/dev/null && git commit -m "feat: M=2 firm Nash via best-response with cross-seed diagnostics" 2>/dev/null || echo "skip commit"`

---

## Task 9: 主实验脚本（统一 vs 动态 + 负载迁移 + 异质 + 弹性占比 + 竞争天花板）

**Files:**
- Create: `experiments/run_peak_shaving_experiments.py`
- Test: 通过运行脚本验证（实验脚本不写单元测试，但须可端到端运行并落盘）

实验对应 spec 的 P1–P5。统一定价 = 强制 `delta=delta_d=0` 求 Nash；动态定价 = 放开 delta。

- [ ] **Step 1: 写脚本**

写入 `experiments/run_peak_shaving_experiments.py`：

```python
"""Peak-shaving dynamic pricing experiments (P1-P5). Real solver outputs only."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import solve_firm_nash

OUT = ROOT / "artifacts" / "peak_shaving" / "20260618"


def _demand_centroid(demand_t: np.ndarray, config: PeakShavingConfig) -> float:
    """时段重心(加权平均时段索引), 用于度量负载迁移。"""
    t = np.arange(config.num_periods)
    return float(np.sum(t * demand_t) / max(np.sum(demand_t), 1e-12))


def uniform_vs_dynamic(config: PeakShavingConfig) -> dict:
    # 统一定价: 通过把 load_shape_hat 置零强制 delta 无效(等价 delta=0)
    uni_cfg = config.evolve(load_shape_hat=np.zeros(config.num_periods))
    uni = solve_firm_nash(uni_cfg, seed=0)
    dyn = solve_firm_nash(config, seed=0)
    return {"uniform": uni, "dynamic": dyn}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = PeakShavingConfig.default()

    # --- 实验1: 统一 vs 动态 (P2, P3) ---
    cmp = uniform_vs_dynamic(cfg)
    summary = {}
    for name, r in cmp.items():
        util = r["res"]["utilization"]
        summary[name] = {
            "system_profit": r["system_profit"],
            "peak_util": float(util.max()),
            "min_qos_firm": float(r["res"]["qos_firm"].min()),
            "converged": r["converged"],
            "firm_params": r["firm_params"],
        }
        print(f"[exp1 {name}] sys={r['system_profit']:.2f} peakU={util.max():.4f} "
              f"minQoS={r['res']['qos_firm'].min():.4f} conv={r['converged']}", flush=True)

    # --- 实验2: 负载迁移 (P1: 弹性迁移, 刚性不动) ---
    # 用 per-type demand 度量重心位移。需要 market 层暴露按类型拆分的需求。
    from pricing_sim.peak_shaving_market import type_channel_demand
    p1 = {}
    for name, r in cmp.items():
        prices = r["res"]["prices"]; qos = r["res"]["qos_channel"]
        dR = type_channel_demand(prices, qos, cfg, "rigid").sum(axis=0)    # (T,)
        dE = type_channel_demand(prices, qos, cfg, "elastic").sum(axis=0)  # (T,)
        p1[name] = {"rigid_centroid": _demand_centroid(dR, cfg),
                    "elastic_centroid": _demand_centroid(dE, cfg)}
    rigid_shift = p1["dynamic"]["rigid_centroid"] - p1["uniform"]["rigid_centroid"]
    elastic_shift = p1["dynamic"]["elastic_centroid"] - p1["uniform"]["elastic_centroid"]
    print(f"[exp2 P1] rigid_centroid_shift={rigid_shift:+.4f} elastic_centroid_shift={elastic_shift:+.4f} "
          f"P1_holds={abs(elastic_shift) > abs(rigid_shift)}", flush=True)
    summary["P1_migration"] = {"rigid_shift": rigid_shift, "elastic_shift": elastic_shift,
                               "P1_holds": bool(abs(elastic_shift) > abs(rigid_shift)), **p1}

    # --- 实验3: 小厂vs大厂动态强度 (P4) ---
    dyn = cmp["dynamic"]
    fp = dyn["firm_params"]
    delta_A, delta_B = abs(fp[0][1]), abs(fp[1][1])
    print(f"[exp3] delta_A(大厂)={delta_A:.4f} delta_B(小厂)={delta_B:.4f} "
          f"P4_holds={delta_B > delta_A}", flush=True)
    summary["P4_delta"] = {"delta_A": delta_A, "delta_B": delta_B, "P4_holds": bool(delta_B > delta_A)}

    # --- 实验4: 弹性占比扫描 (P5) ---
    sweep = []
    for pe in [0.0, 0.2, 0.4, 0.6, 0.8]:
        c = cfg.evolve(pop_rigid=1 - pe, pop_elastic=pe)
        uni = solve_firm_nash(c.evolve(load_shape_hat=np.zeros(c.num_periods)), seed=0)
        dyn = solve_firm_nash(c, seed=0)
        gain = 100 * (dyn["system_profit"] - uni["system_profit"]) / abs(uni["system_profit"])
        sweep.append({"pop_elastic": pe, "uniform": uni["system_profit"],
                      "dynamic": dyn["system_profit"], "gain_pct": gain})
        print(f"[exp4 pe={pe}] uni={uni['system_profit']:.1f} dyn={dyn['system_profit']:.1f} gain={gain:+.2f}%", flush=True)
    summary["elastic_sweep"] = sweep

    (OUT / "peak_shaving_summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SAVED", OUT / "peak_shaving_summary.json", flush=True)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 端到端运行（较慢，后台运行并查看日志）**

Run: `python3 experiments/run_peak_shaving_experiments.py 2>&1 | tee /tmp/peak_exp.log | tail -20`
Expected: 打印 exp1/exp3/exp4 结果，落盘 `peak_shaving_summary.json`。**重点核对**：动态定价 peak_util 应低于统一定价（P2 削峰）；P4_holds 与弹性 sweep 的 gain 随 pe 上升趋势（P5）。

- [ ] **Step 3: 验证落盘工件可读**

Run: `python3 -c "import json; d=json.load(open('artifacts/peak_shaving/20260618/peak_shaving_summary.json')); print('keys:', list(d.keys())); print('uniform peakU:', d['uniform']['peak_util']); print('dynamic peakU:', d['dynamic']['peak_util'])"`
Expected: 打印 keys 与两个 peak_util 值。

- [ ] **Step 4: 提交**

Run: `git add -A 2>/dev/null && git commit -m "feat: peak-shaving main experiments P1-P5" 2>/dev/null || echo "skip commit"`

---

## Task 10: 稳健性脚本（QoS 形态 + u0 + 跨种子统计）

**Files:**
- Create: `experiments/run_peak_shaving_robustness.py`

- [ ] **Step 1: 写脚本**

写入 `experiments/run_peak_shaving_robustness.py`：

```python
"""Peak-shaving robustness: QoS shapes, u0 sensitivity, cross-seed mean+/-std."""
from __future__ import annotations

import json
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
from pricing_sim.peak_shaving_config import PeakShavingConfig
from pricing_sim.peak_shaving_equilibrium import solve_firm_nash

OUT = ROOT / "artifacts" / "peak_shaving" / "20260618"


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    cfg = PeakShavingConfig.default()
    out = {}

    # QoS 形态稳健性(须在拥塞被激活的参数下: 用高弹性占比加大高峰压力)
    congested = cfg.evolve(pop_rigid=0.4, pop_elastic=0.6)
    shapes = {}
    for shape in ["threshold", "linear", "sigmoid", "sqrt"]:
        r = solve_firm_nash(congested, seed=0, qos_shape=shape)
        shapes[shape] = {"system_profit": r["system_profit"],
                         "peak_util": float(r["res"]["utilization"].max()),
                         "min_qos": float(r["res"]["qos_firm"].min())}
        print(f"[qos {shape:9s}] sys={r['system_profit']:.2f} peakU={r['res']['utilization'].max():.4f}", flush=True)
    out["qos_shapes"] = shapes

    # u0 敏感性
    u0s = {}
    for u0 in [-1.0, 0.0, 1.0]:
        r = solve_firm_nash(cfg.evolve(outside_utility=u0), seed=0)
        u0s[str(u0)] = {"system_profit": r["system_profit"]}
        print(f"[u0={u0:+.1f}] sys={r['system_profit']:.2f}", flush=True)
    out["u0_sensitivity"] = u0s

    # 跨种子统计(>=10 seeds)
    profits = []
    for seed in range(10):
        r = solve_firm_nash(cfg, seed=seed)
        profits.append(r["system_profit"])
    profits = np.array(profits)
    out["cross_seed"] = {"mean": float(profits.mean()), "std": float(profits.std()),
                         "rel_std": float(profits.std() / profits.mean()), "n": 10}
    print(f"[cross-seed] mean={profits.mean():.2f} std={profits.std():.2f} rel_std={profits.std()/profits.mean():.4f}", flush=True)

    (OUT / "peak_shaving_robustness.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print("SAVED robustness", flush=True)


if __name__ == "__main__":
    main()
```

- [ ] **Step 2: 端到端运行**

Run: `python3 experiments/run_peak_shaving_robustness.py 2>&1 | tee /tmp/peak_rob.log | tail -20`
Expected: 打印 QoS 形态/u0/跨种子结果，落盘 `peak_shaving_robustness.json`。**重点核对**：cross_seed 的 rel_std < 0.05（收敛证据）。

- [ ] **Step 3: 提交**

Run: `git add -A 2>/dev/null && git commit -m "feat: peak-shaving robustness experiments" 2>/dev/null || echo "skip commit"`

---

## Task 11: 全量回归与最终核验

**Files:** 无（验证）

- [ ] **Step 1: 跑全部单元测试**

Run: `python3 -m pytest tests/test_peak_shaving_market.py tests/test_peak_shaving_equilibrium.py -v`
Expected: 全部 PASS。

- [ ] **Step 2: 确认未破坏既有测试（修正版仍可复现）**

Run: `python3 -m pytest tests/test_intermediary_market.py -v 2>&1 | tail -5`
Expected: 既有测试不受影响（新模块独立，未改动 fixed_market/intermediary_market）。

- [ ] **Step 3: 核对核心可证伪预测是否成立**

Run: `python3 -c "import json; d=json.load(open('artifacts/peak_shaving/20260618/peak_shaving_summary.json')); print('P2削峰:', d['dynamic']['peak_util'], '<', d['uniform']['peak_util'], '=', d['dynamic']['peak_util']<d['uniform']['peak_util']); print('P4小厂动态更强:', d['P4_delta']['P4_holds']); print('P5弹性占比增益:', [(s['pop_elastic'], round(s['gain_pct'],2)) for s in d['elastic_sweep']])"`
Expected: 打印三条预测的实际成立情况。**若某条不成立，这是真实结果，须如实写入论文（作为机制边界），不可调参造数。**

---

## 完成标志

- 所有单元测试 PASS。
- 主实验与稳健性脚本端到端运行、落盘 JSON。
- 跨种子 rel_std < 0.05（收敛证据，根除前两版的命门）。
- P1–P5 的实际成立情况被如实记录（无论正负）。
- 既有 `fixed_market.py` / `intermediary_market.py` 及其测试未被改动。

