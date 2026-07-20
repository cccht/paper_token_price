# SMPT 终稿可信度、现实性与文字准确性专项复审

> **历史审计，已被替代。** 本文件用于记录 225 候选和旧中间商响应空间阶段发现的问题及其修复动机。文中的旧主结果、旧九场景范围和当时的阻塞判断不能用于当前投稿稿。当前状态以 `docs/reviews/smpt_submission_evidence_map_2026-07-14.md`、`docs/reviews/smpt_final_three_reviewer_audit_2026-07-14.md` 及 `20260712_expanded_response/*_submission.json` 为准。

日期：2026-07-12  
稿件：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-12.tex`  
目标期刊：*Simulation Modelling Practice and Theory*  
审查方式：`nature-reviewer` 三审稿人框架；正文、代码、机器工件、PDF、公开仓库状态与原始外部来源交叉核验

## Review setup

- **Input scope:** 完整英文 TeX/PDF、`20260712_final` JSON/CSV、时空需求与有限博弈代码、最终测试、Git 状态和公开来源。
- **Assessment boundary:** 本轮没有重求整张服务商博弈，也没有覆盖正式工件。新增检查均为只读、固定主策略剖面的审计性探针，不能替代正式重求解。
- **Shared manuscript claim summary:** 在固定总需求、两家异质容量服务商、一个 API 中间商和有限线性分时价格候选下，价格时序形状可同时改变请求时段和服务商分配；当前九个局部重求解中的峰值、最大利用率和最低 QoS 方向一致，利润方向不一致。
- **Visible evidence base:** BurstGPT 日内 token-load 形状、单卡 vLLM TTFT-SLA 曲线、守恒 OD 流、routing--QoS 联合固定点、225 点服务商候选、有限 bimatrix game、完整单边候选偏离扫描、网格内 Latin-hypercube 诊断、九个单参数重求解和固定政策机制分解。
- **Missing materials affecting confidence:** 真实推理用户价格响应、容量单位与并发负载的物理映射、多 GPU/长上下文 QoS、日级不确定性传播、服务商容量比扫描、可移动请求比例扫描、连续中间商最优响应和最终公开归档。

### 总体可信度判断

| 层面 | 判断 | 依据 |
|---|---|---|
| 公式与实现的一致性 | **较强，但有一处明确正文错误** | OD 守恒、利润结算、QoS 公式和 regret 与代码一致；正文把主结果的路由敏感度写成 1.5，工件实际对应 4.0。 |
| 数值 verification | **强** | 主剖面残差小于 `7e-10`，有限网格 regret 为 0；本轮 64 个随机固定点初值均收敛到同一数值解。 |
| 有限博弈均衡证据 | **中等偏强** | 对最终支持上的全部 225 个单边候选做了偏离检查；但中间商响应集明显命中上界，扩大响应集后得到更高利润。 |
| 外部 validation | **有限** | BurstGPT 只锚定平均日内形状；QoS 只由一张 RTX 4090、两个小模型和少量过载点锚定；经济参数与容量均为合成设定。 |
| 现实结果幅度 | **方向合理，幅度未被验证** | 降峰后 QoS 改善符合排队与拥塞直觉；13.03% 依赖 48% 可移动需求、低迁移成本和固定容量比，不能解释为生产预测。 |
| 语言与 claim 边界 | **整体较好，但尚非终稿状态** | 语句直接、限制写得清楚；仍有路由参数、公开仓库、QoS “calibration”、`system profit` 等准确性问题。 |

**总判断：** 论文当前最可靠的结论是“在所声明的有限、合成校准模型内，分时价格形状产生了 QoS 保护方向”。它不能证明现实 API 市场会获得 13.03% 的降峰，也不能证明当前服务商剖面在更宽的中间商响应空间中仍是均衡。由于存在一处结果参数写错、一处数据可用性陈述不实，以及中间商候选上界被激活，当前版本不应作为“终稿”直接上传。

## Reviewer 1

- **Overall assessment:** 模型的内部会计和有限博弈证书已经达到可审查水平。需求守恒避免了把退出误当作削峰，固定点与支付函数可以从 PDF 独立理解，主数值也能由工件复算。主要风险已经从“求解器是否收敛”转为“声明的策略域是否过窄”。
- **Who would be interested, and why:** 仿真建模、云服务定价、LLM serving 和服务管理研究者会关心该文如何区分市场总峰值与单一服务商热点。

### Major strengths

1. **守恒关系正确。** Eqs. (3)--(5) 与实现均逐 origin 守恒，主结果总需求严格为 1100。峰值下降不由退出、需求缩减或漏记产生。
2. **内部转移已统一。** 服务商批发收入和中间商批发成本调用同一结算函数，系统侧汇总利润中的批发支付严格抵消。
3. **有限网格证书可复查。** 动态游戏最终 regret 为 0，主剖面残差为 `6.63e-10`。这里的“full-grid”是针对最终对手支持扫描全部 225 个单边候选，并非计算全部 `225^2` 个支付对；这种证书对有限 Nash 条件足够。
4. **固定点局部数值稳定。** 本轮以主动态价格和实际 `beta=4.0` 从 64 组随机 QoS/路由初值启动，全部在 56 轮内达到 `1e-9` 容差；终值坐标最大跨度为 `2.05e-9`。这支持主剖面的数值唯一性，但不是全局唯一性定理。
5. **利润负结果得到保留。** 九个场景中汇总利润变化为 `-37.43%` 至 `+9.41%`，正文没有把基准场景的 `+9.25%` 写成普遍规律。

### Major concerns

1. **P0：正文中的中间商路由参数写错。** TeX 第 341 行写“routing sensitivity 1.5”。当前评价函数复现主剖面利润时返回 `route_beta=4.0`；根据工件中的路由份额、批发价格和 QoS 反推，八个时段均得到 `beta=4.0`。该错误不改变已经保存的表 3 数值，但会使读者误解机制。
2. **P1：中间商响应集存在明显截断。** 原候选为 `beta in {1.5,4.0}`，实际选择上界 4.0。固定服务商主剖面后，将中间商网格扩到更密的 retail base/slope 和 `beta<=6`，中间商利润从 `157.170` 提高到 `169.909`，最佳候选又落在 `beta=6` 上界。固定 retail base `0.95`、slope `0.3` 时，利润从 `beta=0` 的 `166.650` 持续上升到 `beta=20` 的 `175.154`。因此当前 follower best response 不能视为对合理策略域的稳定近似。
3. **P1：服务商边界解反复出现。** 主结果中服务商 B 的 wholesale/direct slope 都等于上界 0.4；九个重求解中，B 的 wholesale slope 有 6 次、direct slope 有 7 次命中上界。本轮在原中间商响应集下测试的 12 个网格外 slope 组合 `0.45--0.8` 都没有提高 B 的利润，说明主点附近向上延伸未立即发现有利偏离，但该测试不覆盖 base 联动、负向延伸、更宽 follower response 或对手混合变化。
4. **P1：最终工件没有保存中间商候选参数。** `expected_profiles` 保存 retail price、routing 和 QoS，却未保存 `retail_base`、`retail_slope` 与 `route_beta`。这正是正文参数抄错未被自动发现的原因。
5. **P1：固定点假设仍未完整声明。** Brouwer 命题只证明存在。正文没有报告多初值检查，也没有说明若同一价格存在多个固定点时如何选择。主剖面的 64 初值结果是积极信号，但尚未覆盖所有进入支付矩阵的策略对。
6. **P2：logit 份额缺少随机效用解释。** Eq. (1) 称 `V` 为 deterministic utility，随后直接使用 softmax。应声明用户具有独立同分布的 Type-I extreme-value 扰动，或说明 softmax 是熵正则化的群体份额。否则从确定性效用到概率份额存在未写出的假设。

### Technical failings that need to be addressed before the case is established

1. 将中间商响应由当前 18 点候选扩展到足够宽且最优点不触边的网格，或对三个参数做有界连续优化。
2. 在新的 follower response 下重新计算 provider game、九个 sensitivity cases、机制分解、图表和全文数字。只在主剖面替换中间商策略不够，因为 provider payoff matrix 会改变。
3. 将每个有正概率的 provider pair 对应的中间商最优响应参数写入机器工件，并增加 TeX--artifact 一致性测试。
4. 把“complete finite grid”改成“all unilateral provider candidates against the final opponent support”，避免读者误以为已计算 50,625 个完整支付单元。

### Assessment against journal-style criteria

- **Originality:** 贡献主要在守恒 OD 流与 temporal/spatial 分离，不在新 Nash 定理。
- **Scientific importance:** 对仿真与服务管理具有明确的领域价值，广泛影响仍受外部校准限制。
- **Technical soundness:** 声明的有限 provider game 内部可信；中间商响应截断削弱了整个层级博弈的解释力。
- **Readability:** 数学链条可读，但 logit 假设和 follower 策略边界需要补明。
- **Recommendation posture:** **大修。** 先修 follower response，再谈终稿。

## Reviewer 2

- **Overall assessment:** 主结果的方向符合拥塞系统常识，但现实幅度并未被数据校准。论文现在是一篇条件明确的机制仿真，不是生产流量、用户价格弹性或平台利润的经验研究。
- **Who would be interested, and why:** 电力 demand response、云计算经济学、API 批处理与容量管理研究者会关心价格诱导的计算任务迁移是否能降低热点。

### Major strengths

1. **BurstGPT 来源真实且处理可复查。** 官方数据说明它是 Microsoft Azure 支撑的 GPT-3.5/GPT-4 工作负载；当前稿固定提交和 SHA-256，使用 1,429,737 条记录与 59 个完整日。[BurstGPT official repository](https://github.com/HPMLL/BurstGPT)
2. **失败记录没有实质改变日内形状。** 当前源文件含 25,443 条 `Response tokens=0` 记录，占 1.780%。本轮排除这些记录后，八时段平均 token share 的最大变化仅 `2.19e-5`，峰值仍为第 6 时段。
3. **主仿真没有超出 QoS 测量横轴范围。** 九个场景中的最大模型利用率为 1.570，低于锚点中的 1.714/2.286 过载观测位置，因此主 QoS 数值不是远距离外推。
4. **固定需求使机制识别清楚。** 这有利于判断 aggregate peak 是否真正改变，也使空间转移不可能伪装成市场退出。

### Major concerns

1. **可移动需求比例偏强且未校准。** 60% 人口被设为 flexible，其中 80% 可移动，等于总需求的 48%。统一价格下已有 31.28% 的全部需求跨时段移动，即 65.16% 的可移动质量离开原时段；动态价格下为 68.65%。因此 13.03% 降峰主要来自改变既有迁移的目的时段，而非只增加 1.67 个百分点的迁移量。
2. **该比例只适合部分任务。** OpenAI Batch API 证明评估、分类、嵌入和离线渲染等请求确实可以异步处理，并给出 24 小时完成窗口和价格折扣；它不能证明 48% 的全部推理需求可在 6 小时内移动，也不能代表交互式聊天。[OpenAI Batch API](https://developers.openai.com/api/docs/guides/batch)
3. **13.03% 对普通 TOU 而言偏高。** Faruqui--Sergici 汇总中的普通 TOU 峰值下降约 3--6%，critical-peak pricing 约 13--20%。本结果处于后者量级。它对高比例离线计算任务可以是情景值，但不能用电力文献直接验证推理市场幅度。[Faruqui and Sergici (2010)](https://doi.org/10.1007/s11149-010-9127-y)
4. **QoS 横轴不是物理利用率。** 测量横轴是 concurrency/224，而仿真横轴是 load/capacity。两者被同记为 `u`，但没有 throughput、GPU busy time、KV-cache occupancy 或 arrival-rate 映射。应称为 normalized load index 或 normalized concurrency anchor，而非真实 GPU utilisation calibration。
5. **QoS 曲线识别较弱。** 十个测量点中只有三个点的 QoS 小于 1；阈值被约束为 `>=1` 后正好命中下界 1.000。三个过载点的拟合误差分别约 `+0.111`、`-0.113` 和 `+0.079`。RMSE 0.0561 能概括形状，但不足以精确支撑 `0.888 -> 0.976` 的现实幅度。
6. **结构性参数没有进入 sensitivity。** 当前只共同缩放两家容量，始终保持 `180:72=2.5:1`。空间容量均衡正依赖这种异质性，却没有容量比、服务商数量、渠道偏好、route QoS weight、flexible share 或 shift window 扫描。
7. **负载不确定性未传播。** Figure 2 已显示日间标准差很大，但均衡只使用 59 日平均。没有按日重求、bootstrap 或分位数场景，因而无法判断 13.03% 是否由平均曲线的单一峰位驱动。
8. **`system profit` 不是社会福利。** 它只是两家服务商与中间商利润之和，不含用户效用、迁移不便、未完成服务损失或外部性。固定需求和无 outside option 进一步限制福利解释。
9. **经济单位不完整。** `D` 是三小时区间质量还是平均负载率没有明确单位；利润式又乘以 `h`。由于所有收入和成本项共同乘以 `h`，这不改变当前策略和百分比，但会妨碍现实金额解释。

### Technical failings that need to be addressed before the case is established

1. 在正文首段明确适用对象是 deferrable/background inference jobs，而不是全部在线聊天请求。
2. 至少新增 flexible share、capacity ratio、shift window 和日级负载四类结构敏感性；这些比继续微调当前四个局部参数更重要。
3. 将 QoS 锚点重新表述为 shape anchor；若要称为 calibration，需要在真实 token workload、arrival process 和多 GPU/模型条件下建立 load-to-utilisation 映射并传播拟合不确定性。
4. 增加一个服务管理对照，如 admission control、batch queue、capacity-aware routing 或 central planner，以说明价格机制相对操作型控制的收益和代价。

### Reality readout

- **结果方向是否现实：是。** 把可延迟任务移出峰时、把流量从小容量服务商转到大容量服务商，都会降低局部拥塞并提高 TTFT-SLA。
- **13.03% 是否可以当作现实预测：否。** 它是合成行为参数和固定容量比下的情景结果。
- **QoS 从 0.888 到 0.976 是否可能：数学上与当前曲线一致，生产上未验证。** 该变化正由 `q(u)` 公式产生，但横轴物理映射和曲线不确定性尚未建立。
- **利润结果是否可信：只可信为“符号不稳定”。** 具体 `+9.25%` 或 `-37.43%` 都受合成成本、完成服务计费和 follower response 限制。

### Assessment against journal-style criteria

- **Validation:** 有两个真实锚点，但只覆盖 shape，不覆盖行为与容量尺度。
- **Generalisability:** 当前九个局部一因子场景不足以支持结构泛化。
- **Practical value:** 适合作为机制筛选和实验设计依据，不适合作为平台部署收益预测。
- **Recommendation posture:** **大修。** 现实性问题可以通过更窄定位和关键结构敏感性改善，不必把论文改成完整生产实证。

## Reviewer 3

- **Overall assessment:** 五章结构、摘要和段落推进已经接近正式英文论文，明显优于早期内部报告式写法。语言问题主要不是语法，而是少数术语比证据更强，以及两处可核验事实不准确。
- **Who would be interested, and why:** 非博弈论读者可从 Figure 1、参数表和机制分解理解请求如何迁移、路由和形成 QoS；这对 SMPT 的跨领域读者是优点。

### Major strengths

1. 摘要包含目的、模型、求解、主数字、敏感性和边界，且没有宣称稳定利润提升。
2. Related research 不只是罗列文献，能够说明电力定价提供什么基础，以及 provider switching 为什么使推理市场不同。
3. 公式、表格和结果顺序一致；主结论中的 `13.03%`、`17.08%`、`0.888 -> 0.976` 与工件一致。
4. 全文几乎没有宣传性形容词、伪引语或不自然的长排比。高频词主要是模型必须使用的 `mechanism`、`diagnostic` 和 `support`，不构成明显 AI 文风。

### Major concerns and precise wording corrections

| 位置 | 当前表述 | 问题 | 建议表述 |
|---|---|---|---|
| Abstract, line 36 | `vLLM measurements calibrate the QoS function` | “calibrate” 暗示物理利用率与生产 QoS 已建立。 | `vLLM measurements anchor the shape of a congestion-response curve` |
| Method, line 292 | `normalised utilisation` / reference `u=1` | 实际是 normalized concurrency，非 GPU utilisation。 | 明确 `concurrency-normalised load index`; 说明仿真采用同一无量纲形状但不主张物理等价。 |
| Results, line 341 | `routing sensitivity 1.5` | 与工件和代码不一致，实际为 4.0。 | 修为 4.0，并由工件宏或自动测试注入。 |
| Results, lines 341/406 | `game converged` / `complete finite grids` | 容易被理解为连续算法收敛或完整 `225^2` 支付矩阵。 | `the double-oracle procedure terminated with zero full-grid unilateral regret` |
| Results, line 380 | `remained the best candidate` | 只在 512 个抽样候选中为最高。 | `had the highest payoff among the sampled candidates` |
| Results, line 406 | `under lower and higher capacity` | 两家容量同步 `+/-15%`，容量比未变。 | `under a common 15% decrease or increase in both capacities` |
| Results/conclusion | `system profit` | 容易误读为 social welfare。 | `aggregate market-side profit`, 并保留公式定义。 |
| Data method, line 290 | `source does not state the time zone` | 官方说明时间戳校准到 local time zone，但未公开具体时区。 | `the source does not identify the local time zone` |
| Discussion, line 425 | `reduces concern about nearby discretisation error` | 当前抽样覆盖整个原策略箱且只有单 seed；“nearby”不准确。 | `did not identify a profitable sampled deviation within the declared strategy box` |
| Data availability, line 440 | final files `are organised in the public repository` | 远端 `main` 与本地 HEAD 都是旧提交 `0941d97`; 7 月 12 日 TeX、代码和工件尚未跟踪/推送。 | 发布后引用具体 commit/release；发布前改为 future availability wording。 |

### Additional language and documentation issues

1. `dynamic pricing` 应在首次出现时限定为 **pre-announced time-of-use pricing**。当前价格依赖固定的基准负载形状，不是实时反馈价格。
2. 应在 softmax 公式前增加一句随机效用假设，避免“deterministic utility”与概率份额之间断裂。
3. `The pooled curve reproduces this threshold pattern` 可以保留方向含义，但建议同时报告过载点最大绝对拟合误差约 0.113，避免只给 RMSE。
4. 参数表中的 `migration cost kappa_R=2` 对 rigid type 实际不生效，因为 `phi_R=0`；应标为 inactive 或删除该无效值。
5. `verified routing--QoS fixed point` 建议改成 `numerically checked routing--QoS fixed point`。测试验证残差与实现性质，不验证固定点唯一性。
6. `verified_refs.bib` 的 `srinivasan2017game` 含重复 `doi` 字段。BibTeX 当前未警告，但应删除重复项。
7. `Anonymous Author`、单位、通讯信息、资金、利益冲突、CRediT 和致谢仍未填写；这属于投稿包问题，不是科学结论问题。

### Assessment against journal-style criteria

- **Readability:** 良好；句型直接，专业术语数量适中。
- **Claim precision:** 大部分限制准确，仍有两处事实错误和数个过强术语。
- **Interdisciplinary accessibility:** Figure 1 和机制分解有帮助；QoS 横轴与“system profit”最容易误导跨领域读者。
- **Recommendation posture:** 语言层面可小修，但证据层面的 follower response 问题使整稿仍属大修。

## Cross-review synthesis

### Consensus strengths

- OD 流与总需求守恒建立了可信的时间迁移口径。
- 主表数字、QoS 公式、服务商利用率和有限 provider regret 在现有工件内一致。
- routing--QoS 主剖面残差很低，64 个随机初值没有发现第二个数值固定点。
- 九个重求解如实显示利润不稳健，论文没有隐藏负结果。
- 英文结构和语法已经达到可送审水平，主要问题是科学表述精度而非“英语不像人写”。

### Consensus technical risks

1. 中间商实际选择 `beta=4.0` 上界，正文却写 1.5；扩大响应集后 follower 利润继续提高。
2. 服务商 B 的价格斜率在多数场景触及上界，现有 Latin-hypercube 只在原策略箱内采样。
3. 48% 可移动需求、2.5:1 容量比、价格弹性和迁移成本均未由推理用户数据估计。
4. normalized concurrency 被用于仿真 utilisation 曲线，物理映射未建立。
5. 59 日负载只取均值，QoS 拟合和负载不确定性均未传播至结果区间。
6. 当前 7 月 12 日终稿包尚未公开，Data and code availability 与事实不符。

### Where emphasis differs across reviewers

- Reviewer 1 认为最紧迫的是 follower response 截断和有限均衡的证据域。
- Reviewer 2 认为最影响 Q1 说服力的是可移动需求、容量比和 QoS 映射缺乏现实校准。
- Reviewer 3 认为语言已经基本合格，但准确术语必须跟随证据降调，不能用流畅英文掩盖模型边界。

### Broad-interest / significance readout

论文的可发表价值不在于“证明动态定价普遍有效”，而在于给出一种可守恒地区分时间迁移与跨服务商均衡的仿真方法。这个贡献对 SMPT 是合理的，但必须先证明结果不由过窄的中间商响应集决定。

### Priority order before submission

1. **P0，立即修正：** `route_beta 1.5 -> 4.0`；修正或兑现公开仓库声明；把中间商候选参数写入工件和自动一致性测试。
2. **P1，必须重算：** 扩大或连续优化中间商 retail base、retail slope 和 route beta，直到最优点不触边；随后重求主 provider game 和九个场景。
3. **P1，Q1 可信度：** 增加 flexible share、capacity ratio、shift window、日级 BurstGPT 负载和 QoS 曲线不确定性分析。至少前三项应完整重求均衡。
4. **P2，模型说明：** 补 logit 随机效用假设；区分 normalized concurrency 与 utilisation；明确适用对象是可延迟计算任务；把汇总利润与社会福利分开。
5. **P2，投稿包：** 发布干净 commit/release，最好归档 DOI；补作者与声明元数据；清理重复 BibTeX 字段。

### Final recommendation posture

**推荐：大修后投稿，不建议以当前文件直接投稿。**

现有结果不是“不可信”，而是具有清楚的层级：

- **可信：** 声明的有限服务商候选与当前有限中间商候选共同定义的模型内，QoS 方向和主数值能够复现。
- **条件可信：** 价格诱导负载迁移和容量均衡在现实中有合理机制基础。
- **尚不可信：** 13.03% 是现实平台可预期幅度、当前层级博弈对更宽 follower 策略稳健、汇总利润代表社会福利。

## Risk / unsupported claims

- 不支持生产环境 QoS 或峰值的点预测。
- 不支持连续服务商策略空间或连续中间商响应空间的 Nash/Stackelberg 结论。
- 不支持交互式与离线推理请求具有相同时间弹性。
- 不支持任意容量比、任意服务商数量或任意负载日下的普遍方向。
- 不支持稳定利润提升或社会福利提升。
- 不支持把 concurrency/224 直接解释为真实 GPU utilisation。
- 当前不支持“最终代码与工件已在公开仓库”的陈述。

## Audit-only checks performed

- 主动态剖面 64 个随机 routing/QoS 初值：全部收敛；最大 residual `9.97e-10`；最大终值跨度 `2.05e-9`。
- 服务商 B 网格外 slope 检查：12 个 `0.45--0.8` 组合均无正收益偏离；该检查不是连续最佳响应。
- 中间商扩展检查：原主剖面实际候选为 `(1.1,0,4.0)`；扩展网格候选 `(0.95,0.3,6.0)` 的利润提高至 `169.909`。
- 固定 `(retail base, slope)=(0.95,0.3)` 的 beta 扫描：中间商利润在 `beta=0--20` 区间持续上升。
- BurstGPT failure-row 检查：零 response-token 行占 1.780%；排除后平均八时段 token share 最大变化 `2.19e-5`。
- Git 公开状态：`origin/main` 与本地 HEAD 均为 `0941d97...`，但 7 月 12 日终稿、代码和工件为未跟踪/未提交状态。

这些检查用于发现风险，没有写回主实验 JSON/CSV，也没有替代完整重求解。
