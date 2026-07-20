# 电力动态定价论文框架图检索与设计参考

检索日期：2026-07-10

## 1. 检索范围与分区口径

本次检索面向电力动态定价、需求响应、电力零售商竞争、双层/多层博弈和聚合商路由等主题。严格清单以 **2024 JCR Q1** 作为“一区”口径，不与中科院分区或 SJR 分区混用。检索优先级为出版社页面、DOI 元数据和高校作者公开稿；只有在可以确认图号、图题和正文解释时才纳入推荐。

此次只记录论文和图形设计信息，不在仓库中保存或再分发原论文框架图。作者公开 PDF 仅用于人工核对图号、页码和构图。

## 2. 严格 Q1 推荐清单

| 优先级 | 论文与期刊 | 具体框架图 | 图形特点 | 对当前论文的可迁移部分 |
|---|---|---|---|---|
| 1 | Meng et al., *Multiple dynamic pricing for demand response with adaptive clustering-based customer segmentation in smart grids*, **Applied Energy**, 2023, 333, 120626. DOI: [10.1016/j.apenergy.2022.120626](https://doi.org/10.1016/j.apenergy.2022.120626) | Fig. 1, “The proposed multiple pricing framework”, 作者稿 PDF 第 6 页；Fig. 2, “Dynamic and adaptive customer segmentation”, 第 7 页。[作者公开 PDF](https://eprints.soton.ac.uk/474021/1/multiple_pricing.pdf) | 很清楚的闭环：零售商、用户分组、分组需求模型、定价优化、分组价格反馈。文字少，箭头有明确方向。 | 最适合作为主参考。把 customer clusters 换成 time-rigid/time-flexible users，把 pricing optimization 换成 providers/intermediary strategy update，把需求模型反馈扩展为 traffic、utilization 和 QoS。 |
| 2 | Hong et al., *A bilevel game-theoretic decision-making framework for strategic retailers in both local and wholesale electricity markets*, **Applied Energy**, 2023, 330, 120311. DOI: [10.1016/j.apenergy.2022.120311](https://doi.org/10.1016/j.apenergy.2022.120311) | Fig. 1, “Bilevel model structure”, PDF 第 6 页（正文页 5）。[作者公开 PDF](https://mst.elsevierpure.com/ws/portalfiles/portal/41042511/A%20Bilevel%20Game-Theoretic%20Decision-Making%20Framework%20for%20Strategic.pdf) | 上层战略决策与三个下层问题分区明确；实线和虚线区分决策与反馈；适合表达博弈层级。 | 用于组织 provider/intermediary/user 三层关系，以及把策略选择、用户选择、市场清算和反馈分开。原图信息较密，不能照搬其框数。 |
| 3 | Meng et al., *An integrated optimization + learning approach to optimal dynamic pricing for the retailer with multi-type customers in smart grids*, **Information Sciences**, 2018, 448–449, 215–232. DOI: [10.1016/j.ins.2018.03.039](https://doi.org/10.1016/j.ins.2018.03.039) | Fig. 1, “Two-level pricing optimization framework with the retailer and its customers”, 作者稿 PDF 第 7 页（正文页 6）。[作者公开 PDF](https://pure.manchester.ac.uk/ws/portalfiles/portal/70314941/An_integrated_optimization_learning_approach_to_optimal_dynamic_pricing_for_the_retailer_with_multi_type_customers_in_smart_grids.pdf) | 单一上层主体、三类用户和双向通信，价格向下、需求向上；视觉结构简单。 | 适合当前论文的两类用户异质性表达。可将双向通信中的上行量扩展为 traffic/QoS feedback，下行量保留 price/QoS signal。 |
| 4 | Feng et al., *Stackelberg game based transactive pricing for optimal demand response in power distribution systems*, **International Journal of Electrical Power & Energy Systems**, 2020, 118, 105764. DOI: [10.1016/j.ijepes.2019.105764](https://doi.org/10.1016/j.ijepes.2019.105764) | Fig. 1, three-level electricity-market hierarchical structure。[出版社页面](https://www.sciencedirect.com/science/article/pii/S0142061519326407) | Wholesale market → electricity utility company → demand-response aggregators → households；价格与用量构成双向反馈。 | 与“服务商 → API 中间商 → 用户”最接近，可直接借鉴聚合商位于上下游之间的结构位置。 |
| 5 | Tang et al., *Game theory based interactive demand side management responding to dynamic pricing in price-based demand response of smart grids*, **Applied Energy**, 2019, 250, 118–130. DOI: [10.1016/j.apenergy.2019.04.177](https://doi.org/10.1016/j.apenergy.2019.04.177) | Fig. 1, “Structure of interaction strategy between the smart grid and grid-responsive buildings”, 作者稿 PDF 第 5 页。[作者公开 PDF](https://ira.lib.polyu.edu.hk/bitstream/10397/95383/1/Tang_Game_Theory_Based.pdf) | 电价向下、需求向上，智能设备位于电网和建筑之间。物联网语义直观，但图标和边框风格已经明显过时。 | 只借鉴箭头语义和中间设备层，不借鉴素材图标、字体、红色斜体标题或多重虚线框。 |
| 6 | Parag and Sovacool, *Electricity market design for the prosumer era*, **Nature Energy**, 2016, 1, 16032. DOI: [10.1038/nenergy.2016.32](https://doi.org/10.1038/nenergy.2016.32) | Fig. 1, “Structural Attributes of Three Prosumer Markets”, 作者稿 PDF 第 7 页（正文页 6）。[作者公开 PDF](https://pure.au.dk/ws/portalfiles/portal/119053924/Electricity_market_design_for_the_prosumer_era.pdf) | 用节点、连线和分组圈表达市场拓扑，几乎不依赖图标或长文本。 | 用于控制视觉复杂度：参与者用简洁节点表示，渠道和交易关系由连线表达。它不是动态定价算法图，因此只作为视觉语言参考。 |

## 3. 高相关补充参考

Subramanian et al., *A data-driven methodology for dynamic pricing and demand response in electric power networks*, **Electric Power Systems Research**, 2019, 174, 105869, DOI [10.1016/j.epsr.2019.105869](https://doi.org/10.1016/j.epsr.2019.105869)。该刊 2024 JCR 为 Q2、SJR 为 Q1，因此不放入严格 JCR Q1 清单。

- Fig. 1（作者稿 PDF 第 2 页）将 demand prediction、day-ahead settlement、real-time settlement 和 demand response 连接为闭环。
- Fig. 2（作者稿 PDF 第 6 页）按 day-ahead、pre-dispatch 和 post-hourly settlement 三个时间阶段组织模块。
- [作者公开 PDF](https://www.chkwon.net/papers/subramanian_data.pdf)

这两张图对当前论文的“固定点仿真流程”很有参考价值，尤其是按阶段分区和用回边表示状态更新，但不适合用来证明目标期刊层级。

## 4. 对当前论文 Figure 1 的结论

当前论文的框架图应采用 **双面板**，避免把市场结构、求解过程和实验结论塞进同一张信息图。

### (a) Market structure and information flow

- 左侧：time-rigid users、time-flexible users。
- 中间：API intermediary；同时保留 direct access 和 exit 两条选择路径。
- 右侧：Provider A（higher capacity）和 Provider B（lower capacity）。
- 下行箭头：price and QoS signals。
- 上行箭头：traffic and observed load。
- 中间商到两家服务商：routing flow；用户到服务商：direct traffic。

### (b) Simulation and strategy-update loop

- Price profiles。
- User choice and traffic allocation。
- Provider utilization。
- QoS fixed point。
- Profits and user surplus。
- Finite-grid strategy update / mixed-strategy diagnostic。
- 从 QoS/payoff 返回 price profiles 的反馈箭头。

QoS protection、peak-utilization reduction、regret 和 profit boundary 属于实验输出，不应作为市场主体或机制节点放在主框架内部。它们可以在面板 (b) 最右侧以一个小型 “Reported metrics” 框出现，但不应写成预设结论。

## 5. 视觉规范建议

- 采用白底、深灰文字和 3 个以内的强调色；颜色用于区分 actor、process 和 feedback，不按每个节点单独着色。
- 只保留两类主箭头：实线表示流量/交易，虚线表示价格、QoS 或信息反馈；在线旁直接标注含义。
- 不使用照片式图标、3D 图标、装饰性阴影、渐变和大面积彩色背景。
- 采用统一的无衬线字体，最终印刷字号不低于约 7.5–8 pt。
- 框架图本身不写公式、实验数值或结论性形容词。
- 结构上优先借鉴 Meng et al. (2023) 的闭环、Hong et al. (2023) 的层级，以及 Parag and Sovacool (2016) 的简洁拓扑。

## 6. 推荐顺序

1. **内容结构首选**：Meng et al. (2023), Applied Energy, Fig. 1。
2. **博弈层级首选**：Hong et al. (2023), Applied Energy, Fig. 1。
3. **用户异质性首选**：Meng et al. (2018), Information Sciences, Fig. 1。
4. **聚合商位置首选**：Feng et al. (2020), IJEPES, Fig. 1。
5. **视觉简化首选**：Parag and Sovacool (2016), Nature Energy, Fig. 1。

最终建议不是复刻任何一张图，而是基于上述结构重新绘制原创框架图，并在正文中分别解释面板 (a) 的市场边界和面板 (b) 的仿真流程。

## 7. 美观物联图专项筛选

用户进一步要求优先寻找视觉完成度较高的物联框架图。本轮重新检查出版社原始高分辨率图片，而不是只依据论文题目或图题判断。筛选标准为：主体层级可在数秒内识别、图标风格基本统一、信息流方向明确、缩小后仍可阅读，并且能够为当前论文的“终端场景—API 中间商—推理服务商—仿真反馈”提供设计参考。

### 7.1 精选图

| 推荐顺序 | 论文与图片 | 视觉判断 | 可借鉴内容 |
|---|---|---|---|
| 1 | Dai et al., **Applied Energy** (2024), Fig. 1, DOI [10.1016/j.apenergy.2024.123868](https://doi.org/10.1016/j.apenergy.2024.123868) | 三个大区块结构规整，智能家居、微电网和 DSO 图标密度适中；颜色用于区分层级，而不是装饰。 | 作为当前论文 Figure 1 的首选视觉参考：将 Smart Homes、Microgrids、DSO 对应为 IoT workloads、API intermediary、inference providers。 |
| 2 | Li et al., **Nature Communications** (2024), Fig. 2, DOI [10.1038/s41467-024-53352-9](https://doi.org/10.1038/s41467-024-53352-9) | 端、边、云三层具有明确纵深，真实设备图标和算法模块能够共存，整体仍有清楚的阅读顺序。 | 借鉴层叠空间和分层连线，但当前论文不应引入其 3D 服务器素材或模型训练细节。 |
| 3 | Wang, **Nature Energy** (2018), Fig. 1, DOI [10.1038/s41560-018-0257-2](https://doi.org/10.1038/s41560-018-0257-2) | 家电、住宅和电网直接建立物联网场景，价格、优先级和负载调整关系直观；配色活跃但文本偏多。 | 借鉴“设备响应价格信号”的视觉叙事，后续原创图必须显著减少句子级标注。 |
| 4 | Langevin et al., **Joule** (2021), graphical abstract, DOI [10.1016/j.joule.2021.06.002](https://doi.org/10.1016/j.joule.2021.06.002) | 留白充足，线性图标、分区标题和阅读方向统一，是五张图中最接近现代期刊信息设计的一张。 | 用作字号、线宽、图标简化和面板留白的基准；不借鉴其美国地图和结果数字。 |
| 5 | Toderean et al., **Energy and Buildings** (2025), graphical abstract, DOI [10.1016/j.enbuild.2024.115067](https://doi.org/10.1016/j.enbuild.2024.115067) | 能源资源、建筑、聚合层和多类参与者构成完整生态，场景丰富；上半部分文字和节点已经接近拥挤上限。 | 用来确定物联网图标丰富度的上限，而不是直接模仿全部节点。 |

### 7.2 剔除情况

多张来自高水平期刊的图仍被剔除，包括照片与矢量素材混用、箭头交叉过多、节点文字过长、渐变或剪贴画风格明显的图。期刊层级不能代替视觉筛选；后续原创图应以 Dai et al. (2024) 的三级结构为主，以 Li et al. (2024) 的分层空间和 Langevin et al. (2021) 的留白规则校正，而不是把多个参考图的元素全部叠加。

### 7.3 本地保存

精选原图已保存到仓库外的本地研究目录：

```text
/root/paper_code/0427_tokenrl/paper_reference_figures/iot_frameworks_2026-07-10/
```

目录中的 `SOURCES.md` 记录了文件名、DOI、图号、推荐理由和许可边界。原图不会加入论文资产目录，也不会直接用于投稿。
