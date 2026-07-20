# SMPT 英文终稿 Claim--Evidence 审计

> **历史审计，已被替代。** 本文件记录 2026-07-12 的 225 候选阶段，不能作为当前投稿证据。旧的 `13.03%`、`17.08%`、`0.888 -> 0.976`、零 off-grid regret 和“九场景已完成”等内容均不适用于 788 候选投稿基准。当前唯一有效的 claim--evidence 状态见 `docs/reviews/smpt_submission_evidence_map_2026-07-14.md`，并以 `artifacts/peak_shaving/20260712_expanded_response/` 下通过门禁的 `*_submission.json` 为机器可读事实源。

日期：2026-07-12  
稿件：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-12.tex`  
目标期刊：*Simulation Modelling Practice and Theory*  
审计范围：正文主张、数学定义、最终实验工件、图表输入、投稿格式

## 总体结论

当前稿件可以作为一篇边界明确的仿真机制论文进入投稿准备。核心 QoS 结论已由守恒需求模型、联合 routing--QoS 固定点、完整有限网格偏离扫描、网格外抽样和九组完整重求解共同支持。利润结论保持为“符号随场景变化”，没有写成稳定收益。正文没有把有限博弈结果表述为连续策略空间证明，也没有把 BurstGPT 或单卡 vLLM 锚点表述为生产校准。

仍然存在明显的外部效度限制：经济行为参数为合成设定；负载只使用 BurstGPT 的平均日内形状；QoS 测量只覆盖一张 RTX 4090 和两个 Qwen2.5 模型；中间商响应和服务商价格均为有限候选集。这些问题已写入第 4.6 节和第 5 节，因而不构成隐藏性过度声称，但可能成为 SMPT 审稿人要求进一步扩展的主要理由。

## Claim--Evidence 对应

| ID | 论文主张 | 主要证据 | 审计结果 |
|---|---|---|---|
| C1 | 每个请求在时间迁移前后守恒，峰值下降不来自退出或市场收缩。 | Eqs. (3)--(5)；`pricing_sim/spatiotemporal_mechanism.py`；OD 与总需求测试；所有最终工件总需求均为 1100。 | 支持。该结论只适用于最终固定需求模型。 |
| C2 | 给定价格时，channel choice、routing、load 和 QoS 构成联合固定点。 | Eqs. (1)--(11)；Brouwer 存在性命题；`pricing_sim/spatiotemporal_game.py`；最终动态残差 `6.63e-10`。 | 支持存在性与数值残差；不支持唯一性或任意初值收敛。 |
| C3 | 动态定价有限博弈得到零完整网格 regret 的纯策略剖面。 | `spatiotemporal_equilibrium.json`；225 个动态候选；2,445 个已评估策略对；三轮 regret `44.284 -> 20.561 -> 0`。 | 支持有限候选集 Nash 结论。 |
| C4 | 相对统一定价均衡，动态定价降低 aggregate peak 和 maximum provider utilisation，并提高 minimum QoS。 | 表 3、图 3；aggregate peak `224.480 -> 195.226`，即 `-13.03%`；maximum utilisation `1.455 -> 1.207`，即 `-17.08%`；minimum QoS `0.888 -> 0.976`。 | 支持最终基准场景结论。 |
| C5 | 时间响应和空间响应是不同机制。 | `final_mechanism_decomposition.json`、图 5；dynamic temporal-only peak `-42.015`；spatial-only peak `0`，maximum utilisation `-0.1017`，minimum QoS `+0.0377`。 | 支持固定政策分解；不能解释为两个可加的因果效应。 |
| C6 | 局部参数变化下，peak、maximum utilisation 和 minimum QoS 方向保持。 | `spatiotemporal_sensitivity.json`、图 6；九个完整重求解；peak `-14.31%` 至 `-4.23%`；utilisation `-19.27%` 至 `-10.49%`；QoS `+0.0540` 至 `+0.0958`；全部 regret 为 0。 | 支持所列九个局部场景；不支持全参数空间泛化。 |
| C7 | 利润改善不是稳定结论。 | 九个重求解中的 system profit 变化范围 `-37.43%` 至 `+9.41%`。 | 支持。摘要、结果和结论均报告符号变化。 |
| C8 | 抽样未发现网格外有利偏离。 | `spatiotemporal_offgrid_diagnostic.json`；每位服务商 512 个 Latin-hypercube 候选，加 incumbent 共 513 次；两方 off-grid regret 均为 0；最大残差 `<1e-9`。 | 支持抽样诊断；不支持连续空间均衡证明。 |
| C9 | 外部数据只锚定负载形状和 QoS 形状。 | 1,429,737 条 BurstGPT 记录、59 个完整日；10 个 vLLM 测量点；pooled RMSE `0.0561`；leave-one-model-out RMSE `0.0454/0.1046`。 | 支持有限校准；不支持价格弹性、迁移成本或生产 QoS 的经验估计。 |
| C10 | 批发结算是内部转移，系统利润中严格抵消。 | Eqs. (14)--(15) 与 Proposition 2；一致性测试。 | 支持当前实现和公式。 |

## Verification 与 Validation

### Verification

- OD 行守恒和总需求守恒。
- 服务商批发收入与中间商批发成本逐服务商抵消。
- linear price shape 的峰谷符号和候选维度。
- routing--QoS 联合残差与候选收敛状态。
- uniform 九候选与 dynamic 225 候选的完整偏离扫描。
- figure builder 只读取 `20260712_final` 工件。
- TeX 的五章结构、摘要字数、图引用、citation key 和核心数字。

### Validation

- BurstGPT 提供真实日内 token-load shape，但不提供价格响应参数。
- vLLM 提供单卡、两模型条件下的 TTFT-SLA shape，并报告五次重复的 95% CI。
- 经济行为参数仍为 synthetic design，不能称为 empirical market calibration。

## 明确不支持的表述

- 生产环境性能预测。
- 连续价格空间 Nash equilibrium 证明。
- 任意容量结构、任意负载或任意用户行为下的普遍结论。
- 稳定或普遍的利润提升。
- 已从真实推理用户估计价格弹性、迁移成本或渠道偏好。
- 固定点唯一性和任意初始化下的全局收敛。

## SMPT 投稿格式检查

依据 2026-07-12 查询的官方 Guide for Authors：摘要不得超过 250 词；关键词为 1--7 个；Highlights 为单独可编辑文件、3--5 条且每条不超过 85 个字符；LaTeX 源文件可提交；该刊采用 single-anonymized review。

- 摘要：227 词，满足上限。
- 关键词：7 个，满足要求。
- Highlights：5 条，长度 60--77 个字符，文件为 `peak_shaving_dynamic_pricing_SMPT_highlights_2026-07-12.txt`。
- 正文：仅保留 Introduction、Related research、Methodology、Experimental results、Conclusion and outlook 五个编号章节。
- 公式：均为可编辑 LaTeX，不是图片。
- 表格：均为可编辑 LaTeX，并在正文引用。
- 图：六张均在正文引用；数据图和框架图为 PDF 矢量输出；字体已嵌入。
- 语言：统一采用英式拼写，例如 `modelling` 和 `utilisation`。
- 待作者填写：真实作者姓名、单位、通讯作者、邮箱、资金、利益冲突、CRediT 和致谢。
- 待归档：建议在实际上传前生成干净 commit，并把最终代码和工件归档到 Zenodo/OSF 获得 DOI。

## 投稿门禁

实验与正文的一致性门禁：**通过**。  
有限博弈与数值验证门禁：**通过**。  
外部效度：**有限，已在正文说明**。  
投稿元数据：**待作者补齐**。  
接收概率或 SCI 分区：**不可由本审计保证**。
