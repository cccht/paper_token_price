# 电力定价论文结构对标记录（2026-06-21）

## 目标

将当前 SMPT 英文主稿与电力实时定价（real-time pricing, RTP）、分时定价（time-of-use pricing, TOU）和需求响应（demand response, DR）论文的常见结构对齐。对齐对象是论文组织方式、公式展开程度和仿真结果展示逻辑，不把电力系统机制直接等同于 GPU 推理服务。

## 检索范围

- 检索主题：electricity real-time pricing, time-of-use pricing, demand response, utility maximization, Stackelberg game, simulation model。
- 重点论文类型：RTP/TOU 定价模型、DR 效用最大化、博弈/Stackelberg 定价、仿真实验和敏感性分析。
- 核对方式：已用 Crossref 核对新增候选文献的题名、期刊/会议、年份和 DOI。

## 结构模板

电力定价论文通常遵循以下顺序：

1. 说明峰谷负载、固定或短期刚性供给、价格作为需求响应工具的动机。
2. 明确系统参与者、时间离散化、负载/需求、效用、成本和约束。
3. 写出用户需求响应或效用最大化模型，再写供应侧/平台侧目标函数。
4. 给出均衡、Stackelberg、优化算法或迭代求解流程。
5. 用数值仿真展示价格曲线、负载曲线、峰值削减、利润/福利/用户成本。
6. 通过参数扫描、基线对比、收敛或稳定性诊断限制结论外推。

## 对标文献与可借鉴点

- Schweppe et al., *Spot Pricing of Electricity*, 1988.  
  结构借鉴：将价格视为稀缺容量和时变负载之间的协调信号。  
  链接：https://doi.org/10.1007/978-1-4613-1683-1

- Borenstein, “The Long-Run Efficiency of Real-Time Electricity Pricing,” *The Energy Journal*, 2005.  
  结构借鉴：用仿真模型比较 RTP 与平价/固定电价，并明确效率结果依赖于需求响应与系统参数。  
  链接：https://doi.org/10.5547/ISSN0195-6574-EJ-Vol26-No3-5

- Faruqui and Sergici, “Household Response to Dynamic Pricing of Electricity,” *Journal of Regulatory Economics*, 2010.  
  结构借鉴：把 TOU/critical-peak pricing 的实证响应作为动态定价是否有效的背景证据。  
  链接：https://doi.org/10.1007/s11149-010-9127-y

- Allcott, “Rethinking Real-Time Electricity Pricing,” *Resource and Energy Economics*, 2011.  
  结构借鉴：把 RTP 的效率收益和用户响应边界分开讨论，避免只给单一正向结论。  
  链接：https://doi.org/10.1016/j.reseneeco.2011.06.003

- Samadi et al., “Optimal Real-Time Pricing Algorithm Based on Utility Maximization for Smart Grid,” SmartGridComm, 2010.  
  结构借鉴：先写用户效用和系统目标，再给算法流程和仿真对比。  
  链接：https://doi.org/10.1109/SMARTGRID.2010.5622077

- Yang, Tang, and Nehorai, “A Game-Theoretic Approach for Optimal Time-of-Use Electricity Pricing,” *IEEE Transactions on Power Systems*, 2013.  
  结构借鉴：TOU 定价论文通常显式给出博弈参与者、价格策略、需求响应和均衡条件。  
  链接：https://doi.org/10.1109/TPWRS.2012.2207134

- Yu and Hong, “Supply-Demand Balancing for Power Management in Smart Grid: A Stackelberg Game Approach,” *Applied Energy*, 2016.  
  结构借鉴：领导者-跟随者顺序、求解算法、供需平衡和仿真灵敏度需要分开呈现。  
  链接：https://doi.org/10.1016/j.apenergy.2015.12.039

- Srinivasan et al., “Game-Theory Based Dynamic Pricing Strategies for Demand Side Management in Smart Grids,” *Energy*, 2017.  
  结构借鉴：动态定价策略要配套展示峰值负载、用户响应、成本/收益和稳定性边界。  
  链接：https://doi.org/10.1016/j.energy.2016.11.142

## 对当前稿件的修改要求

- 引言保留研究问题和贡献，独立增加 “Related Work and Modelling Positioning”。
- 电力文献只作为建模模板：时段、效用、需求响应、价格策略、峰值削减、敏感性分析。
- 明确差异：推理服务没有电力潮流方程；QoS 来自 GPU 利用率、排队和完成率。
- 在 Solution Method 中突出有限网格、固定点和 regret 证书，而不是声称连续空间 Nash 证明。
- 在 Experimental Design 中先交代场景、基线、指标、V&V 边界，再展示结果。
- 结果展示优先采用电力 DR 论文常见逻辑：时段曲线、峰值削减、服务质量/负载、利润或福利、敏感性。

## 当前判定

当前稿件已有较完整公式和实验结果，但相关工作与引言混在一起，电力定价类比不够显式。优化方向不是增加新实验，而是把已有模型、求解和结果按电力定价/仿真建模论文的阅读顺序重新组织，使读者只看主文就能理解模型、验证范围和证据边界。
