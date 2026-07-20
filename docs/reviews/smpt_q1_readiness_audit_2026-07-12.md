# SMPT / SCI Q1 投稿就绪度复审

> **历史审计，已被替代。** 本文件审查的是 2026-07-11/12 的 225 候选版本。其公式/实现缺陷已在后续 788 候选重构中处理，旧数值和就绪度评分不能作为当前投稿判断。当前事实源见 `docs/reviews/smpt_submission_evidence_map_2026-07-14.md` 和通过门禁的 `artifacts/peak_shaving/20260712_expanded_response/*_submission.json`。

日期：2026-07-12  
稿件：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex`  
目标：*Simulation Modelling Practice and Theory*（SMPT）或同等 SCI Q1 仿真建模期刊

## 总体结论

**当前不建议按 SCI Q1 终稿直接投稿，建议等级为 Major Revision。**

稿件已经具备完整论文结构，英文摘要、相关工作、公式说明、图表和限制声明也达到可审阅水平。主要结论已经主动收窄为有限网格、合成校准条件下的 QoS 保护，而不是生产预测、连续策略空间均衡或稳健利润提升。这些都是明显优点。

当前阻塞并不主要来自英文语法，而来自计算口径、联合固定点校核、网格外均衡证据和外部验证。至少两处公式与实现不一致需要修复，并且修复后必须重跑核心求解、参数实验和论文图表。现有结果不能直接作为 Q1 终稿保留。

| 维度 | 当前评价 | Q1 就绪度 |
|---|---:|---|
| 研究问题与期刊匹配 | 8/10 | 接近 |
| 相关工作与贡献定位 | 8/10 | 接近 |
| 模型说明与可复现性 | 7/10 | 尚需校核 |
| 数值求解与均衡证据 | 5/10 | 不足 |
| 实验设计与稳健性 | 5/10 | 不足 |
| 外部验证与校准 | 4/10 | 明显不足 |
| 英文语言与结构 | 7.5/10 | 可投稿但未到终稿 |
| 综合投稿状态 | Major Revision | 暂不投稿 |

SMPT 官网要求论文对建模与仿真作出显著贡献，并将实验设计、敏感性分析、比较程序及 verification/validation 列为重要范围。当前稿件的主题匹配，但证据强度尚未达到该要求的高水平实现。[SMPT Aims and Scope](https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory)

## 审稿范围

- 完整英文 TeX 和当前 25 页 PDF。
- 市场、利润、路由和固定点核心实现。
- 225 点 mixed-oracle 工件、参数扫描、SMPT 扩展实验和 vLLM 锚点。
- 当前测试与既有投稿审计。
- 不把期刊分区当作固定事实。JCR/CAS 分区会随年份和类别变化，正式投稿前应通过本单位订阅的 JCR 或中科院分区表核验。

## Reviewer 1：理论、实现与实验可信度

### 总体评价

模型链条已经写得较完整，但目前存在会影响求解目标和结果解释的实现一致性问题。Q1 审稿中，这类问题优先级高于增加文字或再画图。

### 主要优点

- 用户选择、需求、负载、QoS、利润和 regret 均给出公式。
- 主文明确区分纯策略快照、有限网格 mixed profile 和连续空间均衡。
- 低 regret 混合结果对全部 225 个候选进行偏离扫描，有限博弈内证据较强。
- 负利润结果和同质容量反例没有被隐藏。

### 阻塞问题 1：批发内部转移支付不守恒

服务商批发收入按下式逐服务商计算：

```text
sum_m r_m,t * w_m,t * D_I,t * q_m,t
```

对应实现位于 `pricing_sim/peak_shaving_market.py:168`。中间商批发成本却先分别计算平均批发价和平均 QoS，再将二者相乘：

```text
(sum_m r_m,t * w_m,t) * (sum_m r_m,t * q_m,t) * D_I,t
```

对应实现位于 `pricing_sim/peak_shaving_market.py:185-187`，论文公式位于主稿第 223-236 行。除非批发价或 QoS 在服务商之间相同，两种计算一般不相等。系统利润中的内部收入与内部成本因此不能严格抵消。

在当前 mixed support 上，复核得到期望差额约 `-0.0101`，占已报告系统利润约 `-0.00058%`。当前数值虽小，但该成本直接进入中间商最优响应，修正后可能改变离散最优点、路由、QoS、支付矩阵和 regret，不能只修正文公式而不重跑。

### 阻塞问题 2：联合路由-QoS 固定点没有被最终校核

`pricing_sim/peak_shaving_equilibrium.py:53-84` 在内部迭代 QoS 和路由，并计算联合残差，但 `converged` 和 `resid` 没有返回。随后代码又在固定路由下调用 `solve_market_fixed_point` 重新计算 QoS。此时最终 QoS 可能与生成该路由时的 QoS 不完全一致。

论文的 V&V 表和 `experiments/peak_shaving_smpt_tools.py` 中的残差跟踪只验证固定路由下的 QoS 更新，没有同时验证：

```text
q = QoS(load(q, r))
r = routing(w, q)
```

因此，当前 `10^-9` 残差不能证明支付矩阵中的最终状态满足联合固定点。mixed oracle 共评估 2225 个策略对，但工件没有给出这些策略对的联合收敛率或最坏联合残差。

### 阻塞问题 3：论文指标与工件口径不一致

论文第 434-437 行将平均支付价格定义为按 `D*q` 加权。`experiments/peak_shaving_smpt_tools.py:91` 则按原始需求 `D` 加权。当前几个主状态中的差值较小，但公式、表格、图和代码必须使用同一口径。

### 主要实验不足

1. `0.203` 只证明 225 点候选集内低 regret。服务商参数间距和中间商 24 点响应网格仍可能隐藏网格外偏离。
2. 9 个扰动场景和 25 点相图均固定已有策略，没有在每个参数点重新求均衡。
3. 5 个重求解场景只使用 5 个候选和 4 轮最佳响应，不能替代完整 mixed-oracle 重求解。
4. mixed oracle 只使用一组初始 support 和一条求解路径，没有多初值、网格细化或替代求解器一致性结果。
5. 当前 V&V 审计已有 3/27 个静态拥塞组合不收敛，但候选支付矩阵没有逐项收敛报告。
6. 同质容量消融中 QoS 增益为 `-0.054`。因此结论是条件性的，不能概括为所有固定容量推理市场均受益。

### 推荐意见

当前不满足 Q1 技术门槛。先修复计算一致性并重跑，再评价结论是否仍成立。

## Reviewer 2：创新性、重要性与泛化

### 总体评价

将电力需求响应思路迁移到推理服务，并同时考虑服务商竞争、中间商路由、直连渠道、退出与 QoS，具有中等且可信的组合创新。新版相关工作已经解释了这种迁移为何不是简单照搬。

问题在于，当前证据仍更像一个边界清楚的机制案例，而不是高水平期刊所期待的可推广仿真结论。研究重要性主要依赖真实校准、跨结构泛化或更强的数值方法，目前三者都偏弱。

### 主要优点

- 电力动态定价的理论、实证和博弈研究已形成连续的文献逻辑。
- 论文明确区分峰值需求削减和低谷需求转移，这与当前 outside option 设计有关。
- QoS 改善与利润不稳健之间的分离具有解释价值。

### 主要问题

- 所有经济参数仍为 synthetic calibration，缺少推理用户价格弹性、迁移成本和退出效用的观测依据。
- vLLM 锚点只有 RTX 4090、两个小模型、短生成长度和有限并发水平。它拟合的是 threshold-type 曲线，而主实验使用阈值为 `0.82` 的 sigmoid，二者没有完成参数级校准和留出验证。
- 真实负载只体现在人工构造的 8 时段形状中，没有公开请求轨迹或生产式到达过程。
- 市场结构只包含两个服务商和一个中间商。结果在同质容量下反转，说明异质容量不是次要设定，而是结论成立的重要条件。
- 统一定价、单边折扣和单边加价属于必要但偏弱的基线。缺少中央规划 oracle、福利最优策略、连续优化策略和一种公认的自适应控制/定价基线。

### 推荐意见

主题适合 SMPT，但目前只能支持“特定合成设定中的机制证据”。要达到 Q1 水平，需要真实锚点和重求解泛化至少补强一项，最好两项同时完成。

## Reviewer 3：英文、结构与读者体验

### 总体评价

英文已经没有明显的基础语法障碍。摘要为 239 词，五个一级章节清楚，新版相关工作显著优于旧版。读者能够理解研究问题、模型、主要结果和限制。

语言仍未达到完全终稿状态。全文反复使用内部审计式表达。自动扫描得到 `diagnostic/diagnostics` 高频出现，`boundary` 约 12 次，`rather than` 约 17 次。多次出现 `current artifact set`、`solution budget`、`reported object` 一类面向内部研发过程的措辞。

### 主要优点

- 术语基本统一，QoS、TTFT、finite-grid regret 和 mixed profile 均有定义。
- 摘要包含问题、方法、关键数值和限制，没有宣传式结论。
- 相关工作已从文献列表改成评价和研究缺口分析。
- 图表标题和正文引用完整，当前 PDF 无越界或未定义引用。

### 需要修改

- 将部分 `diagnostic` 改为具体对象，如 solver result、finite-grid profile、sensitivity result 或 comparison。
- 减少每段末尾重复声明“不是什么”，把证据边界集中到 Methods、Results 和 Limitations 的关键位置。
- Conclusion and outlook 仍较长，并重复 Results 和 Limitations 的多个数值。建议压缩 10%-15%。
- `current artifact set` 等工程记录式表达应改为 manuscript、available data 或 current calibration。
- 最终需由作者逐句核对专业含义，尤其是 newly expanded Related work 和 AI 使用声明。

### 推荐意见

语言不是当前第一阻塞项。完成实验重跑后再做一轮母语级 copy-edit，否则数值和结论变化会造成重复返工。

## Cross-review synthesis

### 共识优点

- 研究问题与 SMPT 的仿真建模范围相符。
- 论文的证据边界比早期版本诚实。
- 有限网格 mixed profile 的 regret 结果是当前最可信的数值证据。
- 利润不稳健和结构反例得到如实报告。
- 英文已达到可供审稿人完整阅读的水平。

### 共识风险

- 代码和公式存在两个可定位的一致性问题。
- 联合固定点没有被当前 V&V 证据完整验证。
- 低 regret 没有延伸到网格外策略。
- 参数稳健性以固定策略为主，外部校准不足。
- 同质容量反例限制了主结论的泛化范围。

### 最终推荐

**现在可以上传投稿系统，但不应以 SCI Q1 终稿身份投稿。内部推荐为 Major Revision / Do not submit yet。**

## 达到 Q1 水平的最小工作包

### P0：必须完成，否则不投稿

1. 统一批发收入和批发成本公式，加入内部转移守恒单元测试。
2. 统一平均支付价格及其他论文指标的代码和公式。
3. 返回并记录联合路由-QoS 残差、迭代次数和收敛标志；非收敛候选不得静默进入支付矩阵。
4. 重跑静态基线、粗/细网格、mixed oracle、所有参数实验、表格和图。
5. 对比修复前后结果，确认 QoS 和 profit-boundary 结论是否仍成立。

### P1：Q1 实验门槛

1. 在 mixed support 周围运行连续或准连续的网格外最佳响应搜索，例如多起点差分进化、CMA-ES 或大规模 Latin-hypercube 候选扫描。
2. 对 mixed oracle 使用多组初始 support、网格细化和独立求解路径，报告 regret 与 QoS 的分布。
3. 在一组预先定义的参数样本上完整重求解，不再只固定策略。报告 QoS 增益、profit change、regret 和非收敛率的分布。
4. 用至少一条真实或公开请求负载形状替换纯人工 8 时段曲线，并保留合成曲线作为受控对照。
5. 将主 QoS 函数直接拟合到测量数据，并进行留出验证。扩展模型大小、输入/输出长度或硬件条件中的至少两个维度。
6. 增加中央规划 oracle 和一种自适应定价/控制基线。强化学习不是必需项；只有在存在序列不确定性和在线状态时才值得加入。

### P2：终稿语言和投稿材料

1. 将内部报告式术语减少，压缩 Conclusion and outlook。
2. 根据修复后实验重新检查摘要、表 2 以后所有数值、图注和限制段落。
3. 替换 `Anonymous Author`，补齐单位、通讯作者、CRediT、利益冲突、资金和致谢。
4. 将代码与最终工件归档到 Zenodo/OSF 等持久仓库并取得 DOI。
5. 使用投稿时有效的 SMPT/Elsevier 模板完成最后编译和图表检查。[SMPT Guide for Authors](https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors)

## 复核命令与结果

第一次测试命令使用 pytest 默认捕获，因临时捕获文件丢失而在退出时出现 `FileNotFoundError`，没有执行测试。关闭捕获后运行：

```bash
uv run --no-project --with pytest --with numpy --with scipy --with matplotlib \
  pytest -q -s tests/test_peak_shaving_market.py \
  tests/test_peak_shaving_submission_tools.py \
  tests/test_peak_shaving_smpt_experiments.py
```

结果：`23 passed in 1.18s`。

现有测试没有覆盖内部转移守恒、平均价格口径或联合固定点残差。测试通过只能说明已有断言成立，不能证明当前论文计算已经满足 Q1 终稿要求。
