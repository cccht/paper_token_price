# SMPT 理论—实现一致性审计

日期：2026-07-14
主稿：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex`
进展更新：2026-07-19
基准工件 SHA-256：`70a3b64050c2b0621bbcf0c5a418c43ba554f61b3ee10c2ca4d48fbf26bed226`
状态：公式与实现已核对；800 条统一规则与共同 1,576 条动态规则的正式基准已通过；新阶段 8/8 个正式敏感性场景已通过；依赖新基准的 off-grid、混合分支和派生审计待重建

## 审计范围

本轮逐项核对主稿方法部分、市场实现、连续中间商响应、有限博弈求解和正式工件。审计只判断论文是否准确描述当前代码和结果，不把数值检验改写成解析证明。

## 理论与实现对应

| 理论对象 | TeX 位置 | 实现位置 | 审计结果 |
|---|---|---|---|
| OD 时间迁移与行质量守恒 | Eqs. (3)--(5) | `conserved_temporal_flows` | 每个 origin 的刚性质量与可迁移质量之和等于原生需求；目的时段概率在截断窗口外显式为零，窗口以 `max/min` 截断在八个时段内，不跨日循环；通过 |
| 两阶段 logit 选择 | Eqs. (1)--(3), (6)--(7) | `_channel_utility`、`allocate_spatiotemporal_demand` | inclusive value 与条件渠道份额一致，冲击尺度归一化为 1；通过 |
| 中间商价格/QoS 路由 | Eq. (8) | `routing_from_beta` | 实现为稳定 softmax，价格权重为 `route_beta`，QoS 权重固定为 3；通过 |
| 服务商负载与利用率 | Eq. (9) | `_firm_loads` | 直连需求加中间商路由需求，容量按服务率单位解释；通过 |
| QoS 退化函数 | Eq. (10) | `qos_factor(..., shape="threshold")` | 阈值二次指数形式、阈值和强度与校准工件一致；通过 |
| QoS/路由联合固定点 | Eq. (11) 与命题 1 | `solve_spatiotemporal_joint_market` | 初值、阻尼、200 次上限和 `1e-9` 残差均一致；Brouwer 只证明存在性；通过 |
| 有界线性价格规则 | Eqs. (12)--(14) | `build_burstgpt_load_anchor._normalized_shape`、`expand_price` | 非平坦负载按最大绝对离差缩放至 $[-1,1]$，平坦负载返回零信号；服务商批发/直售价和中间商零售价均按声明边界截断；通过 |
| 服务商与中间商利润 | Eqs. (15)--(16) | `firm_profit`、`intermediary_profit` | 收入、容量成本、退化成本和 `h` 的位置一致；通过 |
| 批发转移抵消 | 命题 2 | `wholesale_settlement_by_firm`、`system_profit` | 服务商正项与中间商负项逐服务商逐时段相消；通过 |
| 中间商三参数连续响应 | Eq. (18) | `IntermediarySearchSpec`、`optimize_intermediary_response_spatiotemporal` | $\Pi_I$ 对应声明初值、阻尼和容差返回的固定点；不收敛评估被排除。$b^*$ 表示最大值可达到时的理想目标，$\widehat b$ 表示多起点 L-BFGS-B 返回值；不声称 $b^*$ 的解析存在性或唯一性；基价、斜率、`beta` 边界和 `log1p(beta)` 变换一致；通过 |
| 双矩阵 Nash 条件 | Eqs. (19)--(23) | `finite_game.py`、`complementarity_solver.py` | 行/列最佳响应不等式和支持互补方向正确；结论针对由 $\widehat b$ 定义、通过缓存的必要支付评价计算的声明有限博弈；通过 |
| 全候选 regret | Eqs. (24)--(25) | `best_response_regret`、double oracle | 两方均按单边纯偏差相对混合收益计算；通过 |
| 有界 off-grid 偏差 | Eq. (26) | `offgrid_diagnostic_tools.py`、`uniform_offgrid_diagnostic_tools.py` | 搜索域、独立随机种子、LHS、边界/局部守卫和成对精化的实现与正文一致；旧数值工件绑定 continuation seed，新基准动态四维审计和九场景统一价格二维审计待重建 |
| 混合均衡分支多初值 | Section 4.3 | `run_submission_equilibrium_branch_audit.py` | 新基准动态均衡为 `26x26` 活跃分支；旧分支工件绑定 continuation seed，1,576 候选下的正式多初值工件待重建 |
| 混合结果聚合 | Eqs. (27)--(29) | `expected_outcome` | 活跃策略对权重为独立混合概率乘积 $x_i y_j$；profile-level 极值期望与逐时段期望曲线分别聚合，未混用 $\mathbb E[\max X]$ 和 $\max\mathbb E[X]$；通过 |
| 混合结果分位数 | Table 5 | `weighted_quantile` | 分位数按离散逆 CDF 定义，返回累计概率达到目标水平时的最小已观测 profile 值；新基准统一/动态 100/676 个活跃剖面的正式工件待重建 |

## 本轮修正

1. 首次出现时补全 `phi_k` 和 `H_k` 的一般定义，并明确刚性类型满足 `phi_R=H_R=0`。
2. 将“随机种子只用于数值审计”改为更准确的说明：市场份额没有个体 Monte Carlo 抽样，seed 用于独立数值审计和 vLLM 测量协议。
3. 精简生成式 AI 声明中的重复项目，不改变工具用途或作者责任声明。
4. 候选集改由 `candidate_manifest_submission.json` 逐元素重建，表 2 报告去重前后数量并列出 18 个新增延续向量；清单现记录生成源码、baseline 和 continuation seed 的 SHA-256，并进入总证据门禁。
5. 将中间商的理论 `argmax` 目标 $b^*$ 与算法返回值 $\widehat b$ 分开；有限 regret 验证由后者定义的声明有限博弈，并只计算均衡支持和全候选偏差扫描所需的支付评价，不暗示完整 $1576^2$ 矩阵已物化。
6. 明确时间迁移窗口在日边界截断，不把 period 8 与下一天 period 1 视为相邻时段。
7. 明确中间商利润采用声明数值规则选择的固定点，不收敛评估不进入响应候选；`argmax` 是理想计算目标，不附带解析存在性或唯一性结论。
8. 在公式首次出现处补全路由权重、QoS 阈值/强度、成本系数和均衡收益符号的文字定义，使 PDF 不依赖代码理解记号。
9. 明确 OD 目的时段概率与条件渠道份额是同一守恒流量的先后分配，不是两个需求项；同时说明含中间商数值响应和市场固定点的纳什互补条件不能给出闭式 tariff，有限博弈均衡由数值方法获得。
10. 将目的时段概率改为分段定义，分母显式限制为 $s\in\mathcal T$，并令迁移窗口外概率为零，消除只看 PDF 时的定义域歧义。
11. 将负载信号写成包含平坦负载零分支的分段定义；将敏感性“complete re-solves”改为“重求有限博弈并检查全部声明的单边偏差”，避免暗示构造了全部 $1576^2$ 支付单元。

## 仍需保持的证据边界

- 固定点命题证明存在性，不证明唯一性或阻尼迭代对所有参数收敛。
- 中间商响应只覆盖声明的三参数策略类，不覆盖逐时段独立零售价和路由份额。
- 中间商自身利润的近似最优误差不自动界定服务商支付误差。当前只读预审显示，低概率近确定性路由剖面可在很小的中间商利润改善下产生较大的服务商间支付重分配；正式 follower-payoff sensitivity 工件仍待 post-sensitivity 审计重建后生成。
- 800/1,576 候选 regret 基于缓存的必要支付评价检查全部声明候选偏差；off-grid 是独立数值充分性检查，二者都不是连续策略均衡证明。
- 当前正式基准已修复旧 12 条统一规则造成的离散化缺口；统一/动态博弈分别使用 800/1,576 条规则并通过 full-candidate regret 门禁。九场景统一价格二维 off-grid 和新基准动态四维 off-grid 尚未完成，因此仍不把有限均衡外推为连续策略均衡。
- `q` 同时进入质量调整收入和退化成本，是公开说明的合成会计设定，不是实际 API 合同估计。
- BurstGPT 与 vLLM 分别锚定平均日内负载形状和 QoS 形状；效用价格系数、迁移成本、容量和成本仍为合成设定，市场层输出未获外部验证。

## 待完成门禁

- 已通过：统一价格候选由旧 12 条扩展为完整 800 条零斜率规则，与动态组成部分合并为 1,576 条共同规则；正式基准的 uniform/dynamic full-candidate regret 分别为 `2.27e-13/1.14e-13`，最大联合残差低于 `1.0e-9`。
- 已通过 8/8 个新阶段扰动场景：`capacity_low`、`capacity_high`、`price_sensitivity_low`、`price_sensitivity_high`、`migration_cost_low`、`migration_cost_high`、`qos_threshold_low` 和 `qos_threshold_high` 已绑定当前基准 SHA、共同候选、来源哈希和中间商配置，并通过 regret、残差、需求守恒与比较算术门禁。
- 待重建：新基准动态四维 off-grid、九场景统一价格二维 off-grid、混合均衡分支、固定点多初值、中间商全局性和 provider-payoff sensitivity。旧同名工件只保留为历史，不作为当前投稿证据。
- 敏感性图、求解器诊断图、正文结果和结论只从通过门禁的工件生成。
