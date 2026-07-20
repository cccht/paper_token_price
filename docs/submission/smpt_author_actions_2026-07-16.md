# SMPT 作者投稿动作表

日期：2026-07-16  
适用稿件：八场景与证据门禁完成后生成的当天 CAS 匿名审阅稿  
状态：作者输入与人工确认待完成

本文件只记录不能由自动化工具推测或代签的投稿信息。未勾选的项目不得在主稿、title page 或投稿系统中写成已完成。

## 1. 作者与机构信息

- [ ] 最终作者姓名与排序：
- [ ] 各作者完整机构名称：
- [ ] 各机构完整邮政地址：
- [ ] 通讯作者姓名：
- [ ] 通讯作者电子邮箱：
- [ ] 通讯作者电话（若系统要求）：
- [ ] 各作者 ORCID：
- [ ] 所有作者已批准最终稿和作者排序：

## 2. 声明

- [ ] Funding statement 已由作者确认：
- [ ] Declaration of competing interests 已由作者确认并生成投稿系统要求的文件：
- [ ] CRediT author statement 已由全部作者确认：
- [ ] Acknowledgements 已由作者确认；若无，明确记录为无：
- [ ] Generative AI and AI-assisted technologies 声明与实际使用过程一致：

## 3. 数据与代码归档

- [ ] 最终 Git commit：
- [ ] 冻结 GitHub release/tag：
- [ ] Zenodo 或其他合适仓储 DOI：
- [ ] 论文中的 Data and code availability 已写入 DOI 与冻结版本：
- [ ] 按期刊 Option C 数据政策提供仓储链接；若确实无法共享，已写明原因：
- [ ] 原始 BurstGPT 不再分发，官方来源、固定 commit、checksum 和派生步骤可复核：
- [ ] 仓储匿名访问或审稿访问方式已按投稿系统要求检查：

## 4. 投稿图像人工重建与确认

政策复核日期为 2026-07-16。SMPT 的期刊专属 [Guide for Authors](https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors) 仍写明，generative AI 或 AI-assisted tools 不得用于创建或修改投稿图像。Elsevier 较新的通用 [Generative AI policies for journals](https://www.elsevier.com/about/policies-and-standards/generative-ai-policies-for-journals) 对解释性示意图和可复现数据可视化给出了更细的允许条件，但不能据此覆盖期刊专属要求。除非投稿前获得编辑部书面确认，仓库中的现有 Draw.io、绘图脚本、PDF、SVG 和 PNG 只用于内部内容核对。作者须在不使用 AI 辅助图像或绘图工具的条件下独立重建正式图，并逐项记录重建文件。

当前内部 Figure 1 不再引用历史 imagegen 位图。主稿引用
`figures/peak_shaving_final_20260714/spatiotemporal_pricing_framework.pdf`，其可编辑
蓝图由 `build_final_spatiotemporal_framework_drawio.py` 生成，并嵌入固定提交
`52d750c9ce051e51cb181b7a78932120c48541d0` 的原始 Streamline SVG。逐文件上游映射、
校验值、CC BY 4.0 许可和署名分别保存在 `SOURCES.tsv`、`SHA256SUMS.txt`、
`LICENSE-CC-BY-4.0.txt` 和 `ATTRIBUTION.md`。历史 imagegen PNG 以及
`framework_imagegen_p2p_reference_2026-07-10.png` 均不在当前 TeX 或 Figure 1
构建链中。这个素材来源结论只排除“沿用生成位图”的风险；由于当前布局和构建脚本
仍曾接受 Codex 辅助，现有 Figure 1 仍不得直接上传，作者独立重建要求保持不变。

| Figure | 内容核对依据 | 作者重建文件 | 重建人/日期 | SHA-256 | 数据、标签与图注确认 |
|---|---|---|---|---|---|
| 1 | 市场结构、OD 时间移动、渠道选择、路由、QoS 固定点与有限博弈流程 |  |  |  | [ ] |
| 2 | 59 个完整日的 BurstGPT 日内份额；vLLM TTFT-SLA 测量与拟合 |  |  |  | [ ] |
| 3 | uniform 与 time-varying 的期望负载、价格、服务商利用率和 QoS 曲线 |  |  |  | [ ] |
| 4 | 双重 oracle regret、bounded off-grid regret 与数值审计阈值 |  |  |  | [ ] |
| 5 | temporal/spatial fixed-policy mechanism decomposition |  |  |  | [ ] |
| 6 | 九场景 common-candidate re-solve sensitivity |  |  |  | [ ] |

每张图还需确认：

- [ ] 字体已嵌入，正文缩放后可读。
- [ ] 颜色对色觉缺陷读者可区分，灰度打印仍可识别。
- [ ] 图内没有 AI 生成或 AI 辅助修改内容。
- [ ] 图号、面板号、图例、单位和正文引用一致。
- [ ] 提交的是独立文件，格式和分辨率符合 Guide for Authors。
- [ ] Figure 1 使用的第三方图标或素材已取得许可并保留正确署名；若作者改用自绘符号，记录相应来源。
- [ ] Figure 1 若继续使用 Streamline SVG，已在图注、致谢或期刊允许的位置保留 CC BY 4.0 所需署名，并核对固定提交与逐文件来源映射。

## 5. 最终上传前确认

- [ ] 主稿已迁移到 CAS 单栏模板并用真实 title-page 信息生成投稿版。
- [ ] 摘要不超过 250 词，关键词 1--7 个，Highlights 3--5 条且每条不超过 85 个字符。
- [ ] 上传 `simpat_highlights_final_2026-07-16.txt`，不上传旧候选集阶段的 Highlights。
- [ ] 参考文献为方括号数字并按首次出现顺序编号。
- [ ] 所有公式和表格保持可编辑，所有图作为独立文件上传。
- [ ] PDF 无未定义引用、缺失字体、正文溢出或图表遮挡。
- [ ] 作者逐页阅读 PDF，并确认结论没有超出有限 1,576 候选、局部参数扰动和合成经济校准的证据范围。
