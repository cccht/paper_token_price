# SMPT 投稿前内部审稿报告（2026-06-21）

## Review setup

- Input scope: `peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex` after electricity-pricing structure adaptation.
- Assessment boundary: 内部预审，重点评估 SMPT 期刊关注的仿真建模、校核、验证、实验设计、证据边界和图表可读性。
- Shared manuscript claim summary: 论文提出一个固定 GPU 容量下的推理服务市场仿真模型，用分时定价、API 中间商路由和有限网格均衡诊断解释拥塞状态下 QoS 改善，但不声称利润稳健提升。
- Visible evidence base: 主文模型公式、有限网格 regret 公式、固定点残差表、vLLM QoS 锚点、拥塞/非拥塞结果表、服务管理基线、结构消融、参数扫描、相图和局部重求解。
- Missing materials affecting confidence: 真实生产请求轨迹、真实用户价格弹性、多 GPU/多模型 QoS 曲线、更大连续策略空间求解。

## Reviewer 1

- Overall assessment: 技术诚实度明显好于早期版本，稿件已经像一篇可审的仿真建模论文。核心 QoS 结论有多层证据，但仍应保持有边界表述。
- Who would be interested in the results, and why: 推理服务平台、云服务定价、服务系统仿真和需求响应建模读者会关注，因为论文把价格、QoS、路由和用户退出放入同一仿真框架。
- Major strengths:
  - 模型链条清楚：用户效用、需求、负载、QoS、利润、候选策略和 regret 都在主文中给出。
  - 有独立 V&V 章节，固定点残差和校准边界写得比较诚实。
  - 利润结论没有过度声称，粗网格、细网格和 mixed diagnostic 的差异被明确解释。
- Major concerns:
  - 电力定价类比现在更清楚，但需要持续避免让读者误解为电力系统物理模型迁移。
  - mixed oracle 仍是有限网格证书，不足以支持连续策略空间均衡。
  - vLLM 锚点是小规模边界验证，不能替代生产 QoS 曲线。
- Technical failings that need to be addressed before the case is established:
  - 若目标是更强的 SCI 结论，仍需要真实负载或真实价格弹性校准。
  - 若目标是强均衡论文，需要更大策略空间或连续优化证据。
  - 若目标是工程部署论文，需要生产式延迟/完成率曲线。
- Assessment against SMPT-style criteria:
  - Originality: 中等偏强，主要在推理服务定价仿真框架组合，而不是新均衡理论。
  - Technical soundness: 当前支持有限网格 QoS 保护结论。
  - Simulation contribution: 已经有 V&V、基线和敏感性，符合 SMPT 关注点。
  - Readability: 结构较清楚，新增相关工作章节提高了定位。
- Recommendation posture: 可进入投稿前深度润色；若按严格审稿尺度，仍接近小修到大修边界，取决于目标期刊对真实校准的要求。

## Reviewer 2

- Overall assessment: 贡献更可信，但需要把创新性放在“可校核仿真模型”上，而不是泛化到生产定价策略。
- Who would be interested in the results, and why: 仿真建模读者会关注模型如何把离散选择、QoS 固定点和有限博弈诊断组合起来；AI 服务市场读者会关注利润边界。
- Major strengths:
  - 新增的电力定价结构定位改善了文献位置。
  - 主文现在更像 demand-response 定价论文：先模型、再求解、再 V&V、再数值研究。
  - 结果展示覆盖峰值利用率、QoS、利润、退出和敏感性。
- Major concerns:
  - Related Work 中新增文献较好，但还应在投稿前确认所有参考文献格式符合 Elsevier 要求。
  - 摘要较长，包含大量数字，投稿前可根据期刊字数限制再压缩。
  - 当前结果偏“机制仿真”，不应在 cover letter 中声称实际平台预测。
- Technical failings that need to be addressed before the case is established:
  - 参数扫描多数为 fixed-policy stress test，不能解释为每个参数点均衡重求解。
  - 局部重求解候选集较小，需要继续作为边界诊断，而不是完整稳健性证明。
- Assessment against SMPT-style criteria:
  - Originality: 主要体现在应用场景和可复现仿真流程。
  - Significance: 对推理服务运营有实际启发，但不是广义定价理论突破。
  - Technical soundness: 结论与证据基本匹配。
  - Readability: 主体结构已经适合人工审阅。
- Recommendation posture: 适合继续向投稿稿推进，下一步重点是图表终检、格式、参考文献和语言压缩。

## Reviewer 3

- Overall assessment: 可读性和图表链条有明显提升。读者现在能从 Figure 1 进入模型，再通过结果图理解 QoS 和利润边界。
- Who would be interested in the results, and why: 跨领域读者会对“电力需求响应思路是否能迁移到 AI 推理服务”感兴趣，但需要清楚看到类比边界。
- Major strengths:
  - Figure 1 更贴近模型，用户路径、路由、固定点和 finite-grid diagnostic 都出现了。
  - Figure 3、Figure 4 和 Figure 5 在 PDF 页面中图注距离正常，标注没有明显遮挡。
  - Figure 7 的相图数值可读，能说明 fixed-policy phase grid 的局部范围。
- Major concerns:
  - Figure 1 信息密度高，单栏或低分辨率打印时可能偏紧。
  - Figure 6 的 x 轴标签较小，但仍可读；若期刊缩图，可能需要横向放大或拆分。
  - 图表很多，投稿前要确保每张图都直接服务于一个明确 claim。
- Technical failings that need to be addressed before the case is established:
  - 目前没有需要立即修复的图表遮挡问题。
  - 若后续改成 Elsevier 双栏模板，需要重新检查所有图在模板中的尺寸和字体。
- Assessment against SMPT-style criteria:
  - Readability: 已经从内部报告风格转向投稿稿风格。
  - Technical communication: 主要数字、图表和限制可以互相对应。
  - Interdisciplinary clarity: 电力定价类比现在较清楚，但仍需在 cover letter 中谨慎描述。
- Recommendation posture: 图表可进入下一轮终稿格式审查。Figure 1 可作为主图保留，但建议保留 `.drawio` 源文件便于期刊格式调整。

## Cross-review synthesis

- Consensus strengths:
  - 主文已经包含足够的公式和求解流程，读者只看 PDF 可以理解仿真模型。
  - QoS 保护结论比利润提升结论更有证据支撑。
  - 新增电力定价结构定位提高了论文组织和文献位置。
- Consensus technical risks:
  - 真实校准不足仍是最大外部有效性风险。
  - 连续策略空间均衡不能声称。
  - fixed-policy stress test 和 restricted local re-solve 的证据强度必须继续分开。
- Where emphasis differs:
  - Reviewer 1 更关注技术证据链。
  - Reviewer 2 更关注贡献定位和期刊适配。
  - Reviewer 3 更关注图表和跨领域可读性。
- Broad-interest/significance readout:
  - 稿件适合定位为仿真建模与机制诊断论文，不适合定位为生产定价预测或一般均衡理论论文。
- Most important issues before strong submission:
  - 完成全图终检和 Elsevier/SMPT 格式适配。
  - 控制摘要长度和 claim 强度。
  - 保持 V&V 和限制章节中的边界语言。

## Risk / unsupported claims

- 不支持：production prediction。
- 不支持：continuous-space Nash equilibrium。
- 不支持：robust profit improvement。
- 有支持但有边界：finite-grid QoS protection under fixed capacity。
- 有支持但较弱：vLLM QoS-shape anchor。
- 有支持但不能过度外推：fixed-policy parameter sweep。
