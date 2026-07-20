# SMPT 终稿证据映射表

日期：2026-07-14
进展更新：2026-07-18
状态：实验审计进行中，暂不作为投稿结论
基准均衡：`artifacts/peak_shaving/20260712_expanded_response/spatiotemporal_equilibrium_submission.json`
基准 SHA-256：`70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`
当前基准记录的 20 个来源 SHA-256 已通过投稿证据门禁。旧 SHA-256 `d3717445...aae2f` 仅作为统一候选扩展前的 continuation seed，不再是投稿基准。

## 使用原则

- 摘要、结果表、图注和结论只引用本表中标为“已锁定”的证据。
- 有限候选集内的 Nash 结论与有界离网偏差检查分开陈述。
- `aggregate market-side profit` 仅指两家服务商与中间商利润之和，不称为社会福利。
- 混合策略下，剖面级非线性指标的期望与期望曲线上的同名指标分开报告。
- BurstGPT 和 vLLM 分别只锚定日内负载形状和拥塞响应形状，不用于生产幅度预测。
- OD 守恒、会计抵消、固定点残差和 regret 属于 model verification；BurstGPT 与 vLLM 属于 empirical input anchoring。当前没有市场层输出的 external validation。
- 容量 `(180,72)` 是归一化服务率下的异质拥塞 stress case，不由 RTX 4090 并发点换算，也不表示物理 GPU 数量。
- 约化 QoS 映射允许 `u>1`，超出固定服务率参考值的负载通过 QoS 下降表示；模型没有跨时段队列积压，因此利用率结果不是排队稳定性证明。
- 无 outside option 且总质量守恒，因此 $\alpha_k$ 是 period--channel 分配中的效用价格系数，不是市场总需求 own-price elasticity；扰动结果不能解释为总需求收缩。
- 2026-07-17 已完成统一价格候选扩展并重求基准：统一博弈使用完整 800 条零斜率规则，动态博弈使用共同 1,576 条规则。基准比较已锁定，但八个扰动场景、九场景统一价格 off-grid 审计和依赖新基准的派生工件尚未全部重建，因此跨场景稳健性和派生审计结论仍不得进入投稿结论。

## Claim--evidence 映射

| 论文主张或方法说明 | 证据位置 | 当前值/状态 | 终稿允许的表述 |
|---|---|---:|---|
| 服务商候选空间已扩大 | `candidate_manifest_submission.json`、`candidate_grid` | 完整统一价格域有 800 条零斜率规则；与动态候选组成部分合并后依次累计为 `800,1178,1298,1362,1389,1489,1558,1576`，最终清单与均衡工件逐元素相同 | common 1,576-rule audit-adaptive finite candidate set；不称连续策略空间 |
| 中间商响应已扩大 | `intermediary_response.dynamic` | 零售基价 `[0.45,2.10]`、斜率 `[-1,1]`、路由参数 `[0,10^6]` 上的三参数连续多起点优化；利润由声明初值、阻尼与容差返回的固定点计算，不收敛评估被排除 | bounded continuous three-parameter policy response；$b^*$ 只表示最大值可达到时的理想目标，不称逐时段任意响应、解析存在/唯一性或全局最优 |
| 动态有限博弈均衡 | `dynamic.method`、`dynamic.row_mix`、`dynamic.col_mix` | Fischer--Burmeister 支持集校正；两方各 26 个正概率策略 | mixed Nash equilibrium of the declared finite provider game under the cached numerical payoff evaluations |
| 统一价格比较基线 | `uniform.candidate_count`、`uniform.row_mix`、`uniform.col_mix` | 完整 800 条零斜率规则；两方各 10 个正概率策略；full-candidate regret 为 `2.27e-13`，最大联合残差为 `9.97e-10` | mixed Nash equilibrium of the declared 800-rule uniform-price game；独立二维 off-grid 审计完成前不外推到连续零斜率域 |
| 有限候选 regret | `uniform/dynamic.full_max_regret`、`relative_full_max_regret` | 统一/动态绝对 regret 分别为 `2.27e-13/1.14e-13`；动态相对 regret 为 `1.36e-16`；全部 800/1,576 个声明候选已扫描 | low full-candidate unilateral regret for the reported mixed profiles under the cached numerical payoff evaluations，容差 `10^{-7}` |
| 数值支付矩阵规模 | `uniform/dynamic.evaluated_pairs` | 统一/动态分别评价 43,246/81,276 个唯一策略对 | evaluated provider pairs；不写成完整 `800^2` 或 `1576^2` 矩阵 |
| 总需求守恒 | `uniform/dynamic.expected_metrics.total_demand` | 两者均为 1,100 | 峰值变化不是退出或市场收缩造成 |
| 剖面级实现峰值期望 | `expected_metrics.aggregate_peak_load` | 225.043 降至 196.903，变化 `-12.5045%` | $E[\max_t L_t]$；这是主表的 aggregate peak |
| 期望负载曲线峰值 | `expected_profiles.aggregate_load` | 动态曲线峰值 194.865 | $\max_t E[L_t]$；仅用于解释图中期望曲线 |
| 剖面级最大利用率期望 | `expected_metrics.maximum_provider_utilization` | 1.3715 降至 1.2228，变化 `-10.8438%` | $E[\max_{m,t}u_{m,t}]$ |
| 期望利用率曲线最大值 | `expected_profiles.provider_utilization` | 动态曲线最大值约 1.202 | $\max_{m,t}E[u_{m,t}]$；不得替代主表值 |
| 最低 QoS | `expected_metrics.minimum_provider_qos` | 0.9012 升至 0.9586，增加 0.0574 | 当前有限混合均衡下的期望剖面级最低 QoS |
| 期望 QoS 曲线最低值 | `expected_profiles.provider_qos` | 0.9012 升至 0.9591 | $\min_{m,t}E[q_{m,t}]$；与动态情形的 $E[\min q]=0.9586$ 在四位小数上不同，不得混用 |
| 时间迁移比例 | `expected_metrics.temporal_moved_fraction` | 0.3128 升至 0.3266 | 总迁移质量只小幅增加；降峰还来自迁移方向变化 |
| 市场侧汇总利润 | `expected_metrics.system_profit` | 1,880.935 升至 1,922.935，变化 `+2.2329%` | baseline aggregate market-side profit rises；不称福利改善；单位为归一化货币单位 |
| 利润分配 | `expected_metrics.firm_A_profit` 等字段 | A 利润下降约 1.08%，B 利润上升约 3.65%，中间商利润上升约 7.78% | 可解释为基准情景下的渠道利润再分配，不声称跨扰动稳健利润改善 |
| 中间商参数边界 | `dynamic.active_profiles[*].search_diagnostics` | $\beta=0$、$\beta\approx10^6$ 和近确定性路由的概率质量分别为 `29.0%`、`0.013%` 和 `24.9%` | route beta 是数值路由控制量，不解释为经济弹性 |
| 有界离网服务商偏差 | `spatiotemporal_offgrid_diagnostic_submission.json`、`uniform_offgrid_audit_submission.json` | 旧动态 off-grid 工件绑定 continuation seed；新基准动态审计和九场景统一价格二维审计均待重建 | 工件通过新基准 SHA 与来源门禁后，报告有界采样与局部精化得到的非零 epsilon；不写连续 Nash 证明 |
| 中间商独立全局搜索 | `intermediary_globality_audit_submission.json`、`intermediary_payoff_sensitivity_submission.json` | 现有工件绑定旧基准；新基准 26-by-26 活跃剖面审计待重建 | independent differential-evolution audit；不得用中间商目标误差替代服务商支付误差，不写全局最优证明，也不称覆盖全部 81,276 个 baseline 缓存支付对、全候选 deviation payoff 或八个敏感性均衡 |
| 固定点多初值结果 | `fixed_point_multistart_audit_submission.json` | 现有工件绑定旧基准；新基准动态均衡仍为 26-by-26 活跃剖面，正式多初值工件待重建 | numerical initialization audit；不写唯一性定理，也不外推到所有 baseline 缓存支付对或敏感性均衡 |
| 混合均衡分支多初值 | `equilibrium_branch_audit_submission.json` | 现有工件绑定旧基准；1,576 候选基准的分支恢复审计待重建 | numerical branch-recovery audit；不写穷举所有均衡或解析唯一性 |
| 参数敏感性 | `sensitivity_*_submission.json` | 新 800/1,576 共同规则阶段已通过 `capacity_low`、`capacity_high`、`price_sensitivity_low`、`price_sensitivity_high`、`migration_cost_low`、`migration_cost_high`、`qos_threshold_low` 和 `qos_threshold_high`。八者统一/动态评价对分别为 81,358/153,576、20,658/133,687、72,290/144,406、26,157/142,876、42,529/92,116、44,078/82,826、50,252/119,882 和 23,036/109,131；支持分别为 18-by-18/15-by-15、3-by-3/10-by-10、20-by-20/21-by-21、5-by-5/16-by-16、9-by-9/26-by-26、10-by-10/26-by-26、10-by-10/24-by-24 和 6-by-6/24-by-24。峰值变化为 `-13.3577%/-12.9817%/-12.8392%/-11.9828%/-13.0813%/-12.0043%/-12.3544%/-12.7809%`，最大利用率变化为 `-10.9106%/-7.6212%/-8.7991%/-10.3771%/-11.5249%/-10.5939%/-10.9019%/-11.1948%`，最低 QoS 变化为 `+0.0662/+0.0279/+0.0423/+0.0533/+0.0603/+0.0553/+0.0534/+0.0583`，市场侧利润变化为 `-9.1390%/+0.4854%/-9.4905%/+0.0058%/+1.9171%/+2.1446%/-0.3160%/+1.4609%`。八者最大 regret 不高于 `3.38e-11`、最大残差不高于 `1.00e-9`。 | 当前支持 baseline plus eight verified perturbations；只写共同有限规则集内的局部参数水平敏感性，不外推异质性比例、参数交互或全局稳健性 |
| 敏感性结论事实 | `sensitivity_claims_submission.json` | 正式九场景 summary 已生成，SHA-256 为 `7bfbd0d471a73ffe23b50034c463b536c9ea0e601a86e7c6f59f8d8bbaa41626`；claims 工件 SHA-256 为 `9d9bf3fd7d1b9689b82888fc365ce5f61f7d9e2b1882b6000cafe5b3fe15a558` | 只报告九场景范围、方向和利润符号计数；绑定 summary SHA，不外推连续域或生产系统 |
| 机制分解 | `mechanism_decomposition_submission.json` | 现有工件绑定旧基准；新基准 temporal/spatial/combined 三组对照待重建 | fixed-policy decomposition；渠道选择、路由和 QoS 在各设置中联合重求，三组结果不可相加；isolated 数值依赖 spatial-off 的固定渠道份额与按容量路由，也不称均衡反事实 |
| 价格形状分解 | `price_shape_decomposition_submission.json` | 现有工件绑定旧基准；新基准 100/676 个 uniform/dynamic 活跃剖面待重建 | fixed-profile accounting decomposition；不称单独均衡效应 |
| 混合结果分布 | `mixed_outcome_distribution_submission.json` | 现有工件绑定旧基准；新基准统一/动态 100/676 个活跃剖面待重建 | profile quantiles；不是置信区间或抽样误差 |

## 方法部分必须同步替换

1. 删除 225 点笛卡尔网格和有限中间商候选集公式，改为审计自适应服务商候选与有界连续中间商响应。
2. 删除 Nashpy 作为正式均衡求解器的表述，写明正仿射归一化、Fischer--Burmeister 互补系统和支持集数值校正；MILP 和经典方法只作为回退求解器。
3. 在 TeX 中给出混合 Nash 的最佳响应不等式、支持互补条件和 regret 定义；用 $b^*$ 表示中间商理论目标，用 $\widehat b$ 表示多起点数值返回值，并说明有限 regret 使用后者生成的缓存支付评价与全部声明候选偏差扫描。
4. 离网搜索域明确为 wholesale base `[0.25,0.90]`、wholesale slope `[-4,4]`、direct base `[0.45,2.10]`、direct slope `[-4,4]`。
5. 明确有限候选证书、有界离网审计、中间商独立全局搜索和固定点多初值检查是四种不同证据。
6. 在 logit 份额前写出独立同分布 Type-I extreme-value 随机效用扰动，避免从“确定性效用”直接跳到概率份额。
7. 将利润式中的 $q$ 解释为 SLA-linked quality-adjusted billable fraction，而不是“请求是否完成”；额外退化项是合成的 SLA/运营成本。

## 混合策略结果的解释

- 两家服务商各有 26 个正概率策略，不能把任一单一价格向量称为动态均衡策略。
- 期望价格、负载、利用率和 QoS 曲线用于解释策略分布的平均运行状态；概率加权均值价格本身不一定构成最佳响应。
- 剖面级 5%、50% 和 95% 分位数描述独立混合策略下的结果离散度，不是数据抽样误差或置信区间。
- 主文应同时报告期望改善和剖面分布，避免把平均 QoS 改善解释成每次价格实现都改善。
- 论文的实践结论是机制方向和适用条件，不是一组可直接部署的确定性价格系数。

## 终稿禁用表述

- production prediction
- continuous-space Nash equilibrium
- globally optimal intermediary response
- robust profit improvement
- social welfare improvement
- calibrated inference-user elasticity
- physical GPU utilisation calibrated by the vLLM anchor
- pure-strategy equilibrium
- complete `1576^2` payoff matrix

## 待完成门禁

- **投稿图像合规：**SMPT 官方政策禁止 generative AI 或 AI-assisted tools 创建或修改投稿图像。当前框架图布局和数据绘图脚本曾接受 Codex 辅助，均只作为内部审阅图源。作者必须独立重建 Figures 1--6 后才能进入上传包；矢量格式、可编辑源或确定性数据生成本身不构成例外。
- **已通过：**统一价格候选已扩展到 800 条，基准动态候选合并为 1,576 条；两场有限博弈均通过全候选 regret、来源、守恒和固定点残差门禁。
- **已完成：**8 个扰动场景按共同 800/1,576 规则重求并全部通过单场景门禁；九场景 summary、claims 和 sensitivity table 已生成。
- **待重建：**九场景统一价格二维 off-grid、基准动态四维 off-grid、固定点多初值、中间商全局性与 provider-payoff、混合分支、机制分解、价格形状和结果分布工件。旧同名文件均绑定 continuation seed，不能作为新基准证据。
- 九场景 summary 与 SHA 绑定的 claims 工件已生成；仍需纳入后续完整结构重算门禁。
- 按重构后的完整依赖清单重建固定点、中间商和机制分解工件，使源码哈希门禁通过。
- 宏文件、图形、英文 TeX、Highlights 和 PDF 只读取通过门禁的正式工件。
