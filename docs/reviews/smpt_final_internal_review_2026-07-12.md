> **历史审稿，禁止据此判断当前稿件可投稿。** 本报告基于 2026-07-12 的旧 225 候选结果和旧敏感性工件。当前事实源为 `smpt_submission_evidence_map_2026-07-14.md` 与 788 候选 submission 工件；SMPT 图像政策复核也已使当前 Figures 1--6 成为仅供内部审阅的图源。

# SMPT 英文终稿内部审稿报告

日期：2026-07-12  
稿件：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-12.tex`

## Review setup

- **Input scope:** 完整 TeX、15 页编译 PDF、六张终稿图、最终 JSON/CSV 工件、模型与测试代码。
- **Assessment boundary:** 以 *Simulation Modelling Practice and Theory* 的仿真方法、verification、validation 和应用透明度要求为主，不预测编辑决定或 SCI 分区。
- **Shared manuscript claim summary:** 在固定总需求和有限线性价格候选下，time-of-use pricing 同时产生时间迁移和跨服务商容量均衡；QoS 方向在九个局部重求解中保持，利润方向不保持。
- **Visible evidence base:** BurstGPT 负载形状、vLLM QoS 形状、守恒 OD 模型、联合 routing--QoS 固定点、有限 bimatrix game、完整网格 regret、网格外抽样、机制分解和参数重求解。
- **Missing materials affecting confidence:** 推理用户价格实验、多 GPU/长上下文 QoS 数据、日级负载不确定性传播、连续策略空间求解和多中间商市场。

## Reviewer 1

- **Overall assessment:** 理论与实现的一致性较上一版有实质改善。需求守恒、联合固定点、利润内部转移和 finite-game regret 均在正文给出公式，并有代码测试和机器可读工件支持。
- **Who would be interested, and why:** 仿真建模、云服务定价、LLM serving 和 service management 研究者会关注该模型如何区分 market peak 与 provider hotspot。
- **Major strengths:** OD 流避免把退出误判为负载转移；固定点存在性和内部转移守恒写入正文；dynamic 225 候选和 uniform 9 候选均做完整偏离扫描；非收敛候选不会进入支付矩阵。
- **Major concerns:** Brouwer 结果只给存在性，不给唯一性；中间商最优响应仍来自有限候选；纯策略剖面可能依赖当前离散化；Latin-hypercube 只是一组固定种子的抽样。
- **Technical failings to address before a broader case is established:** 若论文要声称连续价格空间均衡，需要连续最佳响应和更强证明；若要声称数值算法普遍收敛，需要多初值或收敛条件。当前稿件没有提出这些更广主张，因此问题属于明确限制，而非正文内部矛盾。
- **Assessment against journal-style criteria:** technical soundness 强；verification 强；算法可复现性强；理论新颖性主要来自模型组合与机制分离，而不是新均衡定理。
- **Recommendation posture:** 可按有限博弈仿真论文送审。预期会收到关于连续策略和多初值的修改要求。

## Reviewer 2

- **Overall assessment:** 论文的主结论比旧稿可信，但外部 validation 仍是最弱环节。当前设计适合回答“在这些条件下机制如何工作”，不适合回答“真实 API 市场会产生多大效应”。
- **Who would be interested, and why:** 关心 demand response 从电力系统迁移到计算服务的读者会关注 conserved OD flow 与 provider switching 的区别。
- **Major strengths:** BurstGPT 和 vLLM 不再被夸大为完整市场校准；九个场景全部重求均衡，不再使用 fixed-policy stress test 代替 equilibrium robustness；利润负结果被完整报告。
- **Major concerns:** price sensitivity、migration cost、channel preference 和成本均为合成参数；BurstGPT 只使用 59 日平均形状；vLLM 只覆盖单卡、两个小模型和 128 输出 token；没有把负载日间方差或 QoS 参数不确定性传播到均衡区间。
- **Technical failings to address before a production-level case is established:** 需要真实价格变化下的行为数据、更多硬件/模型条件以及不确定性传播。它们不是当前“机制仿真”主张成立的必要条件，却会直接决定论文的外部影响力。
- **Assessment against journal-style criteria:** validation 有真实锚点但覆盖较窄；sensitivity 比旧稿明显增强；应用价值可信但条件性强；跨场景泛化证据仍是局部的。
- **Recommendation posture:** 主题适合 SMPT，但严格审稿人仍可能给出 major revision，要求至少扩展一项外部验证。投稿时必须保留当前克制表述。

## Reviewer 3

- **Overall assessment:** 五章结构清楚，语言已从内部实验日志改成完整论文。摘要能独立说明问题、方法、结果和限制，专业术语数量受到控制。
- **Who would be interested, and why:** 非博弈论背景的仿真读者也能从 Figure 1、参数表和机制分解理解模型流程和结果来源。
- **Major strengths:** related research 不再只是文献罗列，而是解释电力定价、serving systems 和 finite games 分别提供什么；公式和图表顺序一致；所有图题均说明比较对象；结论没有重复宣传利润。
- **Major concerns:** Figure 1 信息密度较高，印刷尺寸下需要放大阅读；标题较长但尚可接受；Data and code availability 仍缺持久 DOI；`Anonymous Author` 不符合该刊 single-anonymized submission 的最终 title-page 要求。
- **Technical failings to address before the submission package is complete:** 作者、单位、通讯信息、资金、利益冲突、CRediT、致谢和归档 DOI 必须由作者补齐。它们不应由自动化工具推测。
- **Assessment against journal-style criteria:** readability 良好；摘要 227 词；7 个关键词；5 条 Highlights 均在 85 字符以内；PDF 无未定义引用、溢出版心或缺失字体。
- **Recommendation posture:** 语言和结构可进入投稿阶段，剩余工作主要是作者元数据与期刊上传材料。

## Cross-review synthesis

- **Consensus strengths:** 守恒需求、temporal/spatial 分离、联合 fixed point、完整有限网格 regret、全重求解 sensitivity 和负利润结果构成一致的证据链。
- **Consensus technical risks:** 行为参数和成本缺乏真实估计；单卡 QoS 锚点较窄；连续策略空间和固定点唯一性没有证明；日间随机性未进入均衡区间。
- **Where emphasis differs:** Reviewer 1 更重视 finite-game 与数值证书；Reviewer 2 更重视外部 validation；Reviewer 3 更重视可读性和投稿文件完整性。
- **Broad-interest / significance readout:** 论文的重要性来自把电力 demand response 的时间逻辑与推理市场的 provider switching 分开，而不是来自一个新的通用博弈定理。
- **Most important issues before a stronger case:** 若本轮不再新增实验，应保持当前机制研究定位。若审稿后需要扩展，优先传播真实日级负载不确定性，并增加至少一个多 GPU 或更长上下文 QoS 条件。
- **Internal recommendation:** **可以投稿为边界明确的 SMPT simulation study，但应预期 validation 相关的大修风险。** 在上传前只剩作者元数据、声明和持久归档属于硬性待办。

## Risk / unsupported claims

- 不支持 production prediction。
- 不支持 unrestricted continuous-space Nash equilibrium。
- 不支持 stable profit improvement。
- 不支持所有容量结构或所有需求弹性下的普遍结论。
- 不支持 joint fixed point uniqueness 或 global convergence。
