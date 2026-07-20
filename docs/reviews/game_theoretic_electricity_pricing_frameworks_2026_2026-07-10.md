# 2026 年电力定价博弈论框架图深度检索

检索日期：2026-07-10

## 1. 检索目标与纳入标准

本轮只筛选 2026 年正式发表或已在线发表的研究，要求同时满足以下条件：

1. 电价、充放电价格、交易价格或网络使用费是博弈中的核心决策变量；
2. 论文明确采用 Stackelberg、Nash、合作博弈或组合博弈；
3. 原图能够看出上层/下层、领导者/跟随者、市场/聚合/资源等层次；
4. 出版社提供可核验的高清原图；
5. 图在缩小后仍有清楚的阅读顺序，且没有严重的文字遮挡或连线混乱。

检索使用出版社页面、DOI 元数据和出版社图片服务器。以下“美观度”和
“逻辑清晰度”是对原始高清图的人工筛图评分，满分为 5，仅用于选择设计参考，
不代表论文质量评价。

## 2. 最值得参考的 2026 年框架图

| 排名 | 论文、期刊与图号 | 定价与博弈结构 | 美观度 | 逻辑清晰度 | 结论 |
|---|---|---|---:|---:|---|
| 1 | *Dynamic energy storage pricing for virtual power plants via bilevel game optimization under multiple uncertainties*, **Journal of Energy Storage** 154 (2026), 121259, [DOI](https://doi.org/10.1016/j.est.2026.121259), Figs. 1-2 | 上层 VPP 运营商制定储能充放电价格，下层用户响应；Fig. 1 分为市场层、聚合层和资源层，Fig. 2 把博弈嵌入 Monte Carlo 与差分进化求解流程。 | 5.0 | 4.5 | **单张图的综合首选**。Fig. 1 最适合借鉴整体分层，Fig. 2 适合借鉴求解闭环。 |
| 2 | Wu et al., *Promoting sustainable P2P energy trading among microgrids via a fair and adaptive pricing mechanism*, **Renewable Energy** 262 (2026), 125360, [DOI](https://doi.org/10.1016/j.renene.2026.125360), Figs. 1-2 | ADN 与微电网联盟构成 Stackelberg 博弈，联盟内部以合作博弈确定 P2P 交易量和价格；Fig. 1 分信息层与物理层，Fig. 2 专门解释两阶段博弈。 | 4.8 | 5.0 | **成对参考首选**。一张负责物联市场，一张负责博弈层级，信息分工最合理。 |
| 3 | Chen et al., *Multi-timescale bi-level game optimization of microgrids incorporating unexpected load deviations*, **International Journal of Electrical Power & Energy Systems** 177 (2026), 111832, [DOI](https://doi.org/10.1016/j.ijepes.2026.111832), Fig. 1 | 日前 Stackelberg 定价连接 IESO、用户负荷聚合商和新能源车负荷聚合商；日内层加入 MPC 滚动优化和反馈校正。 | 4.6 | 4.8 | **论文总框架首选**。从方法到实验验证的阅读路径完整，版式接近可投稿的总览图。 |
| 4 | *Peer-to-peer power trading and pricing for rental energy storage shared community microgrid: A coordinated Stackelberg and cooperative game*, **Renewable Energy** 256 (2026), 123963, [DOI](https://doi.org/10.1016/j.renene.2025.123963), Fig. 1 | 上层 DSO 先制定价格，下层产消者与共享租赁储能响应；同时标出合作博弈、功率流和信息流。 | 4.4 | 5.0 | **领导者-跟随者表达首选**。层次直观，但标签略多，不能原样照搬。 |
| 5 | *Distribution system operator-led cloud energy storage investment: A Stackelberg game framework for multi-microgrid coordination and dynamic capacity optimization*, **Journal of Energy Storage** 152 (2026), 120641, [DOI](https://doi.org/10.1016/j.est.2026.120641), Fig. 2 | DSO、云储能运营商和微电网集群形成三方层级，并区分能量流、信息流和资金流。 | 4.3 | 4.5 | 物联网场景丰富，适合参考多主体布局；照片与矢量元素混用，视觉语言不宜直接继承。 |
| 6 | Ran et al., *Optimal dynamic pricing for a charging network operator via a multi-agent Stackelberg game in a coupled power-transportation network*, **Sustainable Energy, Grids and Networks** 46 (2026), 102185, [DOI](https://doi.org/10.1016/j.segan.2026.102185), Fig. 1 | 外层 DNO 以 DLMP 清算市场，内层 CNO 制定充放电价格，EV 用户通过出行决策返回负荷。 | 3.2 | 5.0 | **与“动态定价博弈”字面最贴合**，但黑白框图偏素，适合作为逻辑参考。 |
| 7 | *Multi-entity non-cooperative game pricing strategy for integrated energy distribution network based on flexible resources*, **Electric Power Systems Research** 254 (2026), 112676, [DOI](https://doi.org/10.1016/j.epsr.2025.112676), Fig. 1 | DSO、社区综合能源系统和柔性资源聚合商构成三层定价博弈，价格向下、需求向上。 | 3.5 | 5.0 | **三层价格传递首选**。结构准确，但图片素材和阴影风格不够统一。 |

## 3. 最终推荐顺序

若下一步要为当前论文生成原创框架图，建议按以下方式组合参考，而不是复制某一张图：

1. **整体分层**：采用 Journal of Energy Storage 动态储能定价论文 Fig. 1 的“市场层—聚合层—资源层”。
2. **信息/物理分离**：采用 Renewable Energy 自适应 P2P 定价论文 Fig. 1 的“双层并列”。
3. **价格与响应箭头**：采用 Sustainable Energy, Grids and Networks 动态充电定价论文 Fig. 1 的“价格向下、负荷向上”。
4. **论文方法闭环**：采用 IJEPES 多时间尺度论文 Fig. 1 的“模型—实时校正—实验结果”阅读顺序。
5. **博弈说明**：另设小型子面板，参考 Renewable Energy 自适应 P2P 定价论文 Fig. 2，明确领导者、跟随者、策略和反馈。

对当前推理服务定价论文而言，后续原创图不应保留电网设备本身，而应替换为：

- 市场层：两家 inference providers 与 API intermediary；
- 用户层：time-rigid 与 time-flexible users，并保留 direct access 与 exit；
- 决策层：time-of-use prices、routing、user choice；
- 服务层：traffic、GPU utilization、QoS feedback；
- 求解层：finite-grid strategy update、mixed-strategy diagnostic 与 reported metrics。

## 4. 未进入主推荐的 2026 年候选

- Scientific Reports 的 V2G 预测—博弈定价—强化学习融合论文虽然题目强调层级，但核心图更像普通流程图，图形完成度不足。
- Scientific Reports 的多能源 Stackelberg-Nash 竞价论文 Fig. 1 主要展示设备和市场连接，未直接画出领导者与跟随者。
- Communications Engineering 的双层 Stackelberg 规划图层次清楚，但研究核心是 DER 规划与强化学习，不是电力动态定价。
- Energy Policy 的电力—碳—绿证书耦合图较美观，但定价反馈不是主图的核心结构。

这些候选可用于扩展检索背景，不适合作为本次“电力定价博弈框架图”的首选视觉模板。

## 5. 年份与版权边界

- Renewable Energy 共享租赁储能论文的卷期日期为 2026-01-01，但 DOI 中为 2025；仍按正式卷期年份归入 2026。
- Electric Power Systems Research 三层定价论文正式卷期为 2026 年 5 月，但 DOI 中为 2025；处理方式相同。
- 本地保存的是出版社高清图，仅用于个人研究比较，不进入论文图目录，也不作为原创图再分发。
- 正式投稿应重新设计原创框架图；即使论文为开放获取，也必须按具体许可进行署名和复用。

## 6. 本地文件

精选原图和来源索引保存在：

```text
/root/paper_code/0427_tokenrl/paper_reference_figures/game_pricing_2026_2026-07-10/
```

其中 `SOURCES.md` 记录了 9 张原图的文件名、DOI、图号、推荐用途和许可边界。
