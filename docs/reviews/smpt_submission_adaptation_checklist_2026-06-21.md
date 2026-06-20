# SMPT / Elsevier 投稿适配检查表（2026-06-21）

## 当前状态

- 目标期刊：*Simulation Modelling Practice and Theory*。
- 当前主稿：`peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex`。
- 当前格式：generic A4 article manuscript，适合投稿前审阅 PDF。
- 当前 PDF：23 页，A4。

## 已适配内容

- 摘要包含研究目的、仿真模型、求解方法、关键结果、证据边界和主要结论。
- 关键词包含 `verification and validation`、`inference-service simulation`、`finite-grid regret` 等 SMPT 相关词。
- 独立设置 `Related Work and Modelling Positioning`，把电力定价文献作为结构模板而非物理等同模型。
- 主文包含完整公式链：
  - 用户效用和外部选项；
  - demand / load / utilization / QoS fixed point；
  - provider / intermediary / system profit；
  - finite-grid pure and mixed regret；
  - reported metrics and demand-centroid shift。
- 独立设置 `Verification, Validation, and Credibility Boundaries`。
- 结果按仿真论文逻辑展开：场景、基线、主结果、求解证据、结构消融、参数扫描、相图、局部重求解。
- 图表均在正文中引用，图文件均存在。

## 本机模板状态

- 已检查 `elsarticle.cls`：

```bash
kpsewhich elsarticle.cls || true
```

- 结果：当前 WSL TeX 环境未找到 `elsarticle.cls`。
- 决策：本轮不强制迁移到 Elsevier 模板，避免引入未安装类文件导致的不可验证编译失败。当前版本保留为可审阅投稿稿；若后续用户确认需要 Elsevier 模板，可在安装/提供模板后迁移。

## 仍需投稿前人工确认

- 作者、单位、通讯作者、ORCID、邮箱。
- 是否需要 Highlights、Graphical Abstract、Declaration of Interest、Funding Statement、CRediT author statement。
- 参考文献是否需改为目标期刊最终格式。
- 是否使用匿名审稿版本。
- GitHub 仓库是否需要冻结 release 或 Zenodo DOI。
- 目标期刊最终模板中图表是否仍保持清晰，特别是 Figure 1 和 Figure 6。

## 当前不应声称

- 不声称生产预测。
- 不声称连续策略空间 Nash 均衡。
- 不声称稳健利润提升。
- 不声称真实价格弹性已校准。
- 不声称 vLLM 单卡锚点等同生产 QoS 曲线。
