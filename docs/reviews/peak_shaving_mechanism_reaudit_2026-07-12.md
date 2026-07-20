# 峰谷定价论文深层机制复核与重构路线

> **历史机制复核，已被替代。** 本文记录了发现旧 225 候选模型无法支撑
> aggregate peak-shaving 主张的过程，并促成 conserved-demand 重构。其数字不
> 属于当前论文结果。当前事实源见 `smpt_submission_evidence_map_2026-07-14.md`。

日期：2026-07-12  
主稿：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex`  
目标期刊：*Simulation Modelling Practice and Theory*（SMPT）或同等水平的仿真建模期刊

## 结论

**现稿不宜继续按“time-of-use peak shaving”直接润色。当前模型确实得到 QoS 改善，但主 mixed profile 的主要作用是跨服务商、跨直连渠道重新分配峰值请求，而不是把请求从高峰移到低谷。**

在当前未修正的支付模型上，独立的 Lemke--Howson 求解得到一个 2×2 受限混合纳什解。对完整 225 点候选网格逐项扫描后，最大 regret 为 `3.67e-9`，比稿件报告的 `0.203` 更强。该解仍有以下特征：

- 期望最低服务商 QoS 为 `0.9693`，高于统一定价的 `0.7565`；
- 期望最高服务商利用率为 `0.7038`，低于统一定价的 `0.7822`；
- 全市场峰值请求量由 `222.11` 增至 `262.18`，增加 `18.04%`；
- 弹性用户需求质心只移动 `+0.0011` 个时段，基本没有时段迁移；
- 峰值时段大服务商 A 的负载上升，服务商 B 的负载下降，容量归一化后的服务商热点得到缓解。

因此，现有证据支持的是 **provider-level hotspot relief / capacity balancing**，不是 aggregate temporal peak shaving。若不重构主张或模型，摘要、题名、引言、图表指标和结论之间会存在实质冲突。

## 复核范围

- 完整英文 TeX、25 页 PDF、五个一级章节和全部图表说明。
- `pricing_sim/peak_shaving_config.py`、`peak_shaving_market.py`、`peak_shaving_equilibrium.py`。
- coarse/fine fictitious-play 工件、225 点 mixed-oracle 工件、SMPT 基线和 vLLM QoS 锚点。
- 对 mixed profile 的需求、负载、价格、路由、用户类型质心和支持集分布重新计算。
- 使用 Nashpy 的 Lemke--Howson 算法独立求解当前 5×5 受限双矩阵博弈，并扫描完整 225 点候选集。

本报告不修改核心代码、实验工件、图表或论文正文。所有数值都属于当前实现，修复支付和联合固定点后必须重新验证。

## 关键定量复核

| 指标 | 统一定价 | 稿件 mixed profile | 独立有限网格解 | 正确解释 |
|---|---:|---:|---:|---|
| 最低服务商 QoS | 0.7565 | 0.9699 | 0.9693 | QoS 明显改善 |
| 最高服务商利用率 | 0.7822 | 0.7030 | 0.7038 | 最拥塞服务商热点下降 |
| 全市场峰值请求量 | 222.11 | 262.43 | 262.18 | 峰值总量上升约 18% |
| 弹性需求质心变化 | --- | +0.0021 | +0.0011 | 几乎没有跨时段迁移 |
| 有限 225 点最大 regret | --- | 0.2025 | `3.67e-9` | 当前有限博弈可得到数值精确解 |
| 系统利润 | 1783.24 | 1733.13 | 1732.58 | 仍不支持稳健利润提升 |

稿件 mixed profile 的支持组合中，QoS 高于统一定价的概率质量为 1.0，而全市场峰值低于统一定价的概率质量为 0。占概率质量 `0.7376` 的主导策略组合将全市场峰值提高 `19.18%`，同时把最高服务商利用率降至 `0.6997`。这不是均值掩盖的偶然现象。

统一定价峰值位于第 6 时段。该时段的期望变化为：

| 对象 | 统一定价 | mixed 期望 | 变化 |
|---|---:|---:|---:|
| 服务商 A 负载 | 128.24 | 178.08 | +38.87% |
| 服务商 B 负载 | 93.87 | 84.35 | -10.14% |
| 中间商渠道需求 | 27.18 | 24.28 | -10.66% |
| A 直连需求 | 109.79 | 164.29 | +49.65% |
| B 直连需求 | 85.14 | 73.85 | -13.25% |

大服务商 A 的 direct-price slope 在独立有限网格解中始终为 `-0.2`，即高峰折价；小服务商 B 的 direct-price slope 始终为 `+0.2`，即高峰加价。QoS 改善主要来自用户从 B 直连转向 A 直连，而不是中间商把更多请求路由到 A。事实上，第 6 时段中间商对 B 的期望路由份额反而从约 `0.321` 上升到 `0.420`。

## 严重问题

### 1. 主 claim 与实际机制相反

主稿摘要第 40 行、引言第 50 行和结论第 692 行把结果写成“time-flexible demand away from congested periods”“peak-period prices are raised”和“reduces peak load”。现有主 mixed 结果不支持这些表述。

论文中的 `peak utilization` 实际定义为 `max_{m,t} L_{m,t}/G_m`。它衡量最拥塞的服务商--时段热点，不等于 `max_t sum_m L_{m,t}`，后者才是全市场时序峰值。两者必须分开命名和报告：

- maximum provider utilization；
- aggregate peak load；
- aggregate peak-to-average ratio；
- provider-capacity imbalance；
- temporal demand shift/earth-mover distance。

### 2. 当前需求模型不能识别真实的“迁移”

当前 multinomial logit 一次性在全部 `channel × period` 选项和一个 outside option之间分配份额。随后同一份额又乘以时段刚性基线和弹性市场规模。由此产生四个问题：

1. 没有原生时段到目标时段的流量守恒，无法回答“多少请求从时段 t 移到 t'”。
2. 时间偏好同时进入 `log(a_t)`、由同一偏好变换得到的 native distribution，以及 `base_rigid[t]`，存在重复塑造时序分布的风险。
3. 每个所谓 time-rigid/time-flexible 类型都同时包含同一个 flexible baseline 和同一个 rigid/replay baseline；类型名称与需求组成并不一一对应。
4. 一个 outside option 与 24 个内部选项共同归一化，退出率会受时段离散数和渠道数量影响；扩展 T 或服务商数量会机械改变参与概率。

若继续主张时间迁移，建议采用两阶段或 nested 结构：先从公开轨迹得到原生到达量，再让允许迁移的请求在有限时间窗内守恒重排，最后选择渠道/服务商和退出。迁移成本应依赖原生时段与目标时段的距离，而不是只依赖目标时段的 native probability。

### 3. 单边价格基线的实现与名称不一致

价格函数为 `p_t = pbar * (1 + delta * load_hat_t)`。在当前正峰值 load shape 下：

- `delta > 0` 同时表示高峰加价和低谷折扣；
- `delta < 0` 表示高峰折扣和低谷加价。

`discount_only_params()` 使用 `min(delta, 0)`，实际保留的是反向时段价格；`peak_only_params()` 使用 `max(delta, 0)`，仍同时包含高峰加价和低谷折扣。因此表 5 中的 “off-peak discount only” 和 “peak surcharge only” 不是所标示的政策。

应改用显式非负基函数：

```text
uniform:              p_t = pbar
peak surcharge only:  p_t = pbar * [1 + d * max(load_hat_t, 0)]
off-peak discount:    p_t = pbar * [1 - d * max(-load_hat_t, 0)]
symmetric TOU:         p_t = pbar * [1 + d * load_hat_t]
reverse TOU:           retained only as a diagnostic
```

### 4. 负载形状的文字与代码不一致

主稿第 256 行称 `load_shape_hat` 来自 rigid-demand baseline。`pricing_sim/peak_shaving_config.py:29-34` 实际从 `time_preference` 生成该向量。直接改文字可以消除表面不一致，但不能解决人工 8 时段形状的外部有效性。建议以公开到达轨迹生成主 load shape，人工形状只保留为 controlled synthetic benchmark。

### 5. 当前 mixed solver 的证据表达不必要地偏弱

现有 fictitious play 从每个受限策略一个伪计数开始，因此约 `0.0005` 的概率并不表示数学意义上的均衡支持。其 `0.203` 是 2000 轮经验平均的剩余误差，不是当前有限博弈的数值下限。

独立试验在同一 5×5 支付矩阵上得到：

- provider A 支持：策略位置 3/4，概率 `0.962156/0.037844`；
- provider B 支持：策略位置 0/3，概率 `0.233979/0.766021`；
- 受限 regret：数值精度内为 0；
- 完整 225 点偏离扫描最大 regret：`3.67e-9`。

这说明主有限博弈可以使用标准 bimatrix solver 给出更强证据。该结果只适用于当前未修正支付矩阵，不构成连续策略空间均衡证明。

### 6. mixed profile 的运行含义没有定义

稿件把 mixed profile 当作主政策效果，但没有说明服务商是在每天、每小时还是每个市场周期随机抽取价格参数。`expected minimum QoS` 是对每个策略组合先取最小 QoS、再按概率求期望；它不是期望价格下的确定性 QoS。

最终稿应至少给出：

- 支持策略及概率；
- QoS、利润和负载的 5/50/95% 分位数；
- 随机化周期和价格稳定性解释；
- 一条可部署的确定性代表策略，或明确 mixed solution 只用于均衡证书而不作为部署建议。

### 7. 工件与当前代码存在版本漂移

`peak_shaving_robustness.json` 报告 3 个 seed 的系统利润均值 `1010.9003`、相对标准差 `4.31e-4`。当前 `intermediary_best_response()` 和 `_firm_best_response()` 都是确定性网格，`seed`/`n_starts` 仅为兼容参数。用当前代码运行 seed 0、1、2 得到完全相同的系统利润 `1139.4043677649` 和相同参数。

旧工件没有 git commit、dirty status、配置 hash 或代码 hash，无法确定它对应哪一版实现。论文不能继续把旧 cross-seed 工件作为当前代码的复现证据。

### 8. 第一轮审计中的计算问题仍然有效

以下问题已经记录在 `smpt_q1_readiness_audit_2026-07-12.md`，在重跑前必须修复：

- 服务商批发收入与中间商批发成本的内部转移支付不守恒；
- 最终状态没有返回或强制满足联合 routing--QoS 固定点；
- 平均支付价格的 TeX 公式和工件代码使用不同权重；
- 固定策略参数扫描不能作为跨参数均衡稳健性证据。

## 外部竞争与期刊门槛

SMPT 明确要求应用型论文透明呈现模型开发、计算实现、数学/可扩展性问题，以及使用真实数据的 validation/verification。当前主题匹配，但人工负载、合成经济参数和版本漂移会直接削弱可信度。官方范围见：<https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory>。

公开的 BurstGPT 数据包含真实 Azure OpenAI 请求时间、token 长度、模型和失败等字段，可用于生成真实日内负载并做轨迹回放：<https://github.com/HPMLL/BurstGPT>。论文版本报告了 213 天、约 1031 万条轨迹：<https://arxiv.org/abs/2401.17644>。

2026 年 AAAI 论文 PriLLM 已将在线 LLM 服务定价表述为 data-calibrated Stackelberg routing game，并报告真实数据上的利润/计算效率结果：<https://ojs.aaai.org/index.php/AAAI/article/view/38748>。这提高了当前论文对数据校准、基线和差异化贡献的要求。只增加英文润色或更多固定策略热图不能缩小这一差距。

## 三条可行路线

### 路线 A：最小修改，改写为容量均衡论文

保留当前需求结构，修复计算问题，使用标准 bimatrix solver 重跑。将题目和主张改为 asymmetric pricing、channel substitution 和 provider-level hotspot relief。电力定价只作为动机，不再声称 aggregate peak shaving。

优点：改动最小，当前反直觉结果可以保留。  
缺点：合成校准和需求结构仍弱，达到高水平 Q1 的把握有限。

### 路线 B：严格重建时间削峰模型

保留原始电力需求响应主线。使用真实轨迹定义原生到达，采用守恒的 origin--destination 时间迁移矩阵，限制 peak surcharge/off-peak discount 的符号，主要实验固定市场总量，市场扩张和退出作为扩展实验。

优点：题名、模型和削峰指标完全一致。  
缺点：重写范围最大，当前结果大多不能沿用，而且可能不再得到显著 QoS 改善。

### 路线 C：推荐，研究时序与空间两种调节边际

把当前“问题”转为论文的核心发现：竞争性推理市场的 QoS 改善可能来自跨服务商容量均衡，而非总峰值下降。模型中显式分离：

1. 原生时序到达；
2. 守恒的时间迁移；
3. 渠道/服务商选择；
4. 中间商路由；
5. outside option 和市场扩张。

设计 temporal-only、spatial-only、combined 和 neither 四个主实验，再加入 direct channel、capacity heterogeneity 和 routing policy 的因子消融。主结论可以检验为：在异质容量和直连选择存在时，spatial reallocation 是否比 temporal shifting 更能解释 QoS 改善，以及 QoS 改善是否可能与 aggregate peak growth 同时发生。

优点：保留电力定价基础，又形成推理市场特有、可证伪的贡献；最符合 SMPT 对模型机制、V&V 和应用创新的要求。  
缺点：需要修模型、重跑实验和重写论文，工作量中等偏大。

## 推荐路线 C 的执行顺序

### P0：计算正确性和工件治理

1. 统一内部批发转移函数和所有论文指标函数。
2. 返回联合固定点的 residual、iterations、converged；非收敛候选不得进入支付矩阵。
3. 为每个工件写 manifest：git commit、dirty status、config/code hash、环境、solver、seed 和生成命令。
4. 对转移守恒、需求守恒、固定点、基线语义和论文指标增加单元测试。
5. 将环境正式纳入 `pyproject.toml`/`uv.lock`，避免每次临时解析依赖。

### P1：可识别的需求与负载模型

1. 从 BurstGPT 提取多个日/周的 8、24 或 48 时段原生到达曲线。
2. 定义 rigid mass 和 flexible mass；只有 flexible mass 可在预设窗口内迁移，迁移前后总量守恒。
3. 使用 nested/sequential choice：先参与和时间迁移，再选渠道/服务商；或先固定原生到达再联合求解，但必须保留 origin--destination 流量。
4. 将 market expansion、exit 和 fixed-total-demand 分成可辨识实验，不在主实验中同时改变所有边际。
5. 将 QoS 曲线直接拟合到主仿真使用的函数，并用留出并发点或另一工作负载长度验证。

### P2：有限博弈和网格外证据

1. 缓存完整 225×225 支付矩阵；当前性能估计表明该规模可计算。
2. 使用 Lemke--Howson/Gambit 等标准双矩阵方法求多个有限网格均衡，并逐一验证 regret。
3. 对每个混合解运行连续或准连续网格外 best response，例如 differential evolution 加大规模 Latin-hypercube 候选。
4. 报告多均衡、初始化和网格细化结果；mixed solution 作为证书，确定性代表策略作为操作结果。

### P3：真正区分机制的实验

至少包含以下基线：

- uniform pricing；
- correctly defined peak-only/off-peak-only/symmetric TOU；
- capacity-proportional routing；
- QoS-aware routing without dynamic pricing；
- central-planner QoS/welfare oracle；
- admission control；
- PriLLM-inspired or clearly specified Stackelberg pricing baseline；
- 可选的 MPC/online pricing；只有建立序列状态和不确定性后才加入强化学习。

核心因子实验：

| 时间迁移 | 跨服务商/渠道选择 | 用途 |
|---|---|---|
| 关闭 | 关闭 | 纯静态对照 |
| 开启 | 关闭 | 识别 temporal shifting |
| 关闭 | 开启 | 识别 spatial reallocation |
| 开启 | 开启 | 检验交互作用 |

每个实验同时报告 aggregate peak、maximum provider utilization、capacity imbalance、temporal EMD/centroid、exit、served volume、QoS、profit 和 welfare。

### P4：重写主稿

实验完成前不再进行整篇语言润色。若路线 C 成立，建议题名方向为：

```text
QoS protection without aggregate peak reduction:
a simulation study of pricing and channel choice in heterogeneous inference markets
```

或：

```text
Beyond peak shaving: simulation of asymmetric pricing and capacity balancing
in competitive inference services
```

摘要先报告“最高服务商利用率下降但总峰值上升”的反直觉结果，再解释 temporal/spatial 分解。相关工作继续保留电力动态定价，但把它作为需要检验的迁移假设，而不是已被当前结果证明的机制。

## 投稿门槛

在以下条件同时满足前，不建议按 Q1 终稿投稿：

1. 修复后所有支付、固定点和指标测试通过；
2. 最终工件可由同一 commit 和 manifest 重建；
3. 主 claim 与 aggregate/provider-level 指标一致；
4. 至少一条真实请求轨迹进入主实验；
5. temporal 与 spatial 机制完成可识别分解；
6. 有限网格达到数值低 regret，并完成网格外 best-response 审计；
7. 关键参数采用完整重求解而非固定策略扫描；
8. 主 QoS 曲线与测量数据使用同一函数并有留出验证；
9. 与容量路由、中央规划和一个近期定价方法公平比较；
10. 最终再做 SMPT 模板、语言、图表、作者信息和归档 DOI 处理。

## 本轮命令与结果

mixed 机制重算使用当前代码逐一评估 25 个支持组合。结果为：

```text
baseline aggregate peak = 222.1066
mixed expected aggregate peak = 262.4296 (+18.1548%)
baseline rigid/elastic centroids = 5.3304 / 5.2715
mixed rigid/elastic centroids = 5.3326 / 5.2736
```

Nashpy support enumeration 因当前 5×5 游戏退化而返回 0 个解；对支付做正仿射缩放后，Lemke--Howson 从 10 个 dropped labels 得到同一个 2×2 解。完整网格偏离扫描命令评估了 896 个去重策略对，耗时 `229.1 s`，结果为：

```text
row full-grid regret = 1.84e-10
column full-grid regret = 3.67e-9
maximum full-grid regret = 3.67e-9
```

该独立求解仅用于决定下一步研究设计，没有写回 JSON/CSV、图表或 TeX。

## 状态

`analysis_complete / awaiting_direction`

推荐选择路线 C。获得方向确认后，先实施 P0 和最小机制分解原型；在看到修复后的结果前，不承诺保留任何现有百分比或结论。
