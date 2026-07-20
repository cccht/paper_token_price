# SMPT / Elsevier 投稿适配检查表（更新于 2026-07-16）

## 当前状态

- 目标期刊：*Simulation Modelling Practice and Theory*。
- 当前主稿：`peak_shaving_dynamic_pricing_SMPT_final_2026-07-14.tex`。
- 当前格式：generic A4 article manuscript，适合投稿前审阅 PDF。
- 当前 PDF：20 页，A4；Section 4.5 的 Figure 6 与敏感性表仍等待九场景工件。
- 官方依据：[Elsevier/ScienceDirect SMPT Guide for Authors](https://www.sciencedirect.com/journal/simulation-modelling-practice-and-theory/publish/guide-for-authors)，2026-07-16 复核。

## 已适配内容

- 摘要包含研究目的、仿真模型、求解方法、关键结果、证据边界和主要结论。
- 摘要为 205 词，不超过官方 250 词上限；不含引用。
- 关键词共 7 个，符合官方 1--7 个要求。
- 独立设置 `Related work`，把电力定价文献作为建模基础而非物理等同模型。
- 主文包含完整公式链：
  - conserved OD movement 和两阶段随机效用选择；
  - demand / routing / load / utilisation / QoS fixed point；
  - provider / intermediary / system profit；
  - mixed Nash complementarity、finite-candidate regret 和 bounded off-grid regret；
  - reported metrics、机制分解和全量敏感性设计。
- 验证、校核与可信度边界合并在 Methodology 和 Experimental results 中，以保持用户要求的五章结构。
- 正文只有五个编号主章节：Introduction、Related work、Methodology、Experimental results、Conclusions and future work。
- Figures 1--5 均在正文中引用且内部审阅文件存在；Figure 6 和对应敏感性表将在九场景门禁通过后生成并插入，当前不得写成已完成。
- Highlights 为 5 条，每条 64--76 个字符，符合 3--5 条且每条不超过 85 字符的要求。
- 表格使用可编辑 LaTeX，不含竖线或单元格底色；公式为可编辑文本并连续编号。
- 生成式 AI 声明位于参考文献之前，包含工具名称、用途、人工复核和作者责任。
- 2026-07-16 复核确认官方政策同时禁止 generative AI 和 AI-assisted tools 创建或修改投稿图像。当前 Figure 1 的 Draw.io 布局、Figures 2--5 的绘图脚本及计划生成 Figure 6 的脚本曾接受 Codex 辅助，因此只能作为内部审阅蓝图，不能因其为矢量图或确定性数据图而视为已满足投稿图像政策。
- 当前 Figure 1 蓝图没有引用历史 imagegen PNG 或 `framework_imagegen_p2p_reference_2026-07-10.png`。实际链路为 `build_final_spatiotemporal_framework_drawio.py`、可编辑 Draw.io 和固定提交 `52d750c9ce051e51cb181b7a78932120c48541d0` 的未修改 Streamline SVG；许可为 CC BY 4.0，逐文件来源和校验值已保存。该事实只说明素材来源可追溯，不解除作者独立重建正式投稿图的阻塞项。

## 模板与参考文献状态

- 通过 SMPT 官方 Guide for Authors 提供的链接下载 Elsevier CAS 2.4 模板包至 `/tmp`；下载包 SHA-256 为 `36d97da01c6bbd134f315bff6c3de553735e2550444a6ddd4f869ddc67a20757`。本轮未把 class 或示例文件写入仓库。
- 当前 TeX Live 可直接找到 `unsrtnat.bst` 和 `xurl.sty`，但找不到 `cas-sc.cls` 或 `cas-common.sty`。正式投稿目录需携带官方未修改的这两个 CAS 2.4 文件和版本/许可说明；官方 README 说明该 bundle 可按 LPPL 1.2 或更高版本分发。
- 使用 `cas-sc.cls` 和 `cas-common.sty` 对当前完整正文做了隔离预检。CAS 不接受 `[H]` 浮动选项，临时稿改用 `[htbp]` 后可正常编译。
- 首次全文预检沿用作者年份标签，多篇引用展开为完整作者列表并产生页面越界。临时稿显式加入 `\usepackage[numbers]{natbib}` 后不再越界，但通用 `cas-model2-names.bst` 仍按作者字母排序编号，不符合 SMPT 要求的首次出现顺序。改用 TeX Live 的 `unsrtnat` 后，正文首组引用为 `[1,2,3,4,5]`，XeLaTeX/BibTeX 编译退出码为 0，生成 18 页 PDF，无正文 overfull、undefined citation/reference 或 annotation 越界。
- CAS 标题页仍报告固定的 117.0831 pt overfull。该诊断已定位到 `cas-common.sty` 将 `ARTICLE INFO` 关键词盒放入零宽覆盖盒的内部实现，并非论文内容超出版心。在临时全文稿中拆分混合策略系数长句并加载标准 `xurl` 后，正文两条 underfull 和 MLSys 长 URL 的一条 underfull 均已消失；这两项修正将在当天日期的正式匿名稿中复用。
- 当前 generic A4 主稿继续作为数值完成前的审读版本。正式匿名稿应在八场景结果和全部证据门禁通过后迁移到 CAS 单栏模板，再进行一次完整页面视觉检查。
- SMPT 初投不强制标点和字段格式，但正式参考文献风格要求方括号数字引用并按出现顺序编号。最终 CAS 稿使用 `numbers` + `unsrtnat`，避免通用 CAS 作者排序 BST 在数字模式下产生非顺序编号。

## 仍需投稿前人工确认

- **阻塞项：**作者须在不使用生成式或 AI 辅助图像工具的条件下独立重建 Figures 1--6，并逐图核对数据、标签、图注、字体和可访问性。当前 Draw.io、PDF、SVG、PNG 和绘图脚本可用于核对研究内容，但不得直接进入 SMPT 上传包。完成后应在本检查表中记录作者、日期和重建文件的校验值。
- **阻塞项：**SMPT 采用 single-anonymized review，官方 title-page 要求作者、单位、完整邮政地址和通讯作者信息；当前 `Anonymous Author` 不能作为正式投稿信息。
- **阻塞项：**由作者确认 ORCID、Declaration of competing interests、Funding 和 CRediT author statement；这些内容不得推测生成。
- **阻塞项：**该刊研究数据采用 Option C，要求把研究数据存入相关仓储并在论文中引用、链接；若无法共享则必须说明原因。当前 GitHub 链接尚无持久标识符，最终应优先绑定 Zenodo DOI。
- 在数值门禁完成后生成当天日期的 CAS 匿名主稿，并重新检查章节编号、图表位置、字体嵌入、交叉引用和完整 PDF 页面。
- 在正式 CAS 目录中加入官方未修改的 `cas-sc.cls` 与 `cas-common.sty`，并用仓库内文件而不是 `/tmp` 临时路径完成一次干净复编。
- GitHub 地址已通过禁用本地凭证的匿名 `ls-remote` 检查，但本轮终稿和新工件尚未提交；全部门禁通过后再建立冻结 release。如条件允许，再创建 Zenodo DOI，并把最终 commit/release 标识写回 Data and code availability。
- 敏感性八场景仍在全量重求。混合均衡分支审计已通过；固定点、中间商和机制分解工件需在源码复杂度重构后重新生成，随后再执行最终证据门禁和语言终审。

## 当前不应声称

- 不声称生产预测。
- 不声称连续策略空间 Nash 均衡。
- 不声称稳健利润提升。
- 不声称真实价格弹性已校准。
- 不声称 vLLM 单卡锚点等同生产 QoS 曲线。
