# 路线 C 实施与证据更新

日期：2026-07-12  
对象：fixed-capacity inference pricing 的时序迁移与跨服务商容量均衡分解  
状态：核心计算修复完成；守恒机制原型与真实负载锚点完成；尚未形成新均衡主结果

## 当前决定

路线 C 可以继续。修复后的受控模型已经将两种机制区分开：

- 对称 time-of-use pricing 通过 origin--destination 时间迁移降低 aggregate peak；
- 大服务商高峰折价、小服务商高峰加价通过 channel/provider substitution 降低 maximum provider utilization；
- provider hotspot relief 不要求 aggregate peak 同时下降。

这一结果在人工受控负载和 BurstGPT 日内 token profile 上方向一致。它支持把论文从单一“peak shaving”改为“temporal shifting versus spatial capacity balancing”。但当前实验使用固定政策、固定路由和合成行为参数，不能直接替代服务商博弈均衡、利润或生产预测。

## P0 计算修复

### 内部批发转移

新增唯一的 per-provider wholesale settlement。服务商批发收入和中间商批发成本均读取：

```text
h * sum_t w[m,t] * r[m,t] * D[I,t] * q[m,t]
```

在容量成本和退化成本设为零的非对称测试中，系统利润现在等于外部零售收入，内部转移严格抵消。

### 平均支付价格

`average_paid_price` 统一按完成服务量 `D * q` 加权，与论文定义一致。旧工件按原始需求量加权，必须在正式重跑中替换。

### 联合 routing--QoS 固定点

中间商候选现在同时验证：

```text
q = QoS(load(q, r))
r = routing(wholesale, q)
```

最终结果返回 joint/qos/routing residual、迭代数和收敛标志。未达到 `1e-9` 联合容差的候选不会进入中间商最优响应。SMPT 记录函数也已暴露这些字段，不再只报告固定路由的 QoS residual。

## 可识别的需求原型

新模块使用两阶段结构：

1. 每个用户类型拥有显式原生时段请求量；
2. 可迁移质量在给定时间窗口内形成 origin--destination 流；
3. 每个 origin 的流量逐行守恒；
4. 到达目标时段后再进行 within-period channel choice；
5. temporal 和 spatial 两个机制可以独立关闭；
6. 主原型固定总需求，不启用 market growth 或 outside option。

这使 `temporal_moved_fraction` 成为直接由 OD 流计算的指标，不再依赖质心差反推迁移。新增指标同时报告：

- aggregate peak load；
- aggregate peak-to-average ratio；
- maximum provider utilization；
- provider utilization imbalance；
- minimum provider QoS；
- temporal moved fraction；
- type-specific destination centroids。

## 明确定义的价格政策

价格生成器现支持：

- `uniform`；
- `peak_surcharge`；
- `off_peak_discount`；
- `symmetric`；
- `reverse_diagnostic`。

前四个名称的峰/谷符号由测试约束。`reverse_diagnostic` 只用于检验大服务商高峰折价的容量均衡机制，不再伪装成 off-peak discount baseline。

## BurstGPT 负载锚点

来源为 BurstGPT 官方仓库固定提交：

```text
commit: d895a53bb7b8ec137d0d2fe203b335835a78c10a
file: data/BurstGPT_1.csv
raw bytes: 50,853,373
raw SHA-256: 46fc9480ef0b748ecb2b51d512ff08c196b031782cbe6f78e28044d768e86d5a
license: CC BY 4.0
```

原始 CSV 仅缓存于 `/tmp`。聚合器读取 `1,429,737` 行，跳过 0 行，去除首尾日后保留 59 个完整日。每个自然日先分别按 request count 和 total tokens 归一化，再对 8 个三小时时段求均值和标准差。主锚点使用 token share，所得 load shape 零均值且最大绝对值为 1。

该锚点只提供真实日内到达形状。价格敏感度、迁移成本、可迁移比例、服务商容量和 QoS 参数仍是合成设定。公开时间戳使用源服务本地时间，但未公开具体时区，因此时段仅表示记录日内的相对位置。

## 四格结果

所有 24 个单元（2 种负载 × 3 种价格结构 × 4 种机制开关）均在 `1e-9` 容差下收敛，总需求均保持 1100。

### 合成守恒负载

| 价格与机制 | Aggregate peak change | Max provider util. change | Min QoS change |
|---|---:|---:|---:|
| Symmetric TOU + temporal only | -28.473 (-13.11%) | -0.0983 (-13.11%) | +0.1015 |
| Asymmetric + spatial only | approximately 0 | -0.2021 (-26.96%) | +0.1075 |
| Asymmetric + combined | +2.602 (+1.20%) | -0.1970 (-26.28%) | +0.1075 |

### BurstGPT token profile

| 价格与机制 | Aggregate peak change | Max provider util. change | Min QoS change |
|---|---:|---:|---:|
| Symmetric TOU + temporal only | -43.253 (-18.13%) | -0.1493 (-18.13%) | +0.5159 |
| Asymmetric + spatial only | 0 | -0.2314 (-28.09%) | +0.5274 |
| Asymmetric + combined | -4.676 (-1.96%) | -0.2211 (-26.84%) | +0.5270 |

### 解释

对称 TOU 的时间作用同时降低总峰值和服务商峰值。Asymmetric spatial-only 保持每个时段总需求不变，因此 aggregate peak 完全不变；它通过把负载从紧容量服务商转向宽容量服务商，提高最低 QoS。combined 结果不是两个单独效果的简单相加，说明时间迁移、渠道选择和 QoS 反馈存在交互。

这组结果把旧主稿的模糊表述拆成两个可证伪命题：

1. `Temporal claim`：对称 TOU 是否在守恒需求下减少 aggregate peak？
2. `Spatial claim`：异质服务商价格是否在 aggregate peak 不变时减少 provider hotspot？

## 当前不能声称的内容

- 不能把 24 个单元称为 Nash equilibrium；它们是固定政策机制实验。
- 不能报告利润改善；原型尚未重新求解服务商与中间商的博弈。
- 不能把 BurstGPT 负载称为用户弹性或迁移参数校准。
- 不能把当前 QoS 增益数值直接写入摘要；QoS 曲线仍含合成阈值。
- 不能继续使用旧 mixed-oracle、参数扫描和图表数值作为修复后结果。
- 不能将 `reverse_diagnostic` 作为通用 time-of-use policy recommendation。

## 对主稿的影响

`peak_shaving_dynamic_pricing_SMPT_final_2026-07-11.tex` 仍保留为历史稿，本轮没有修改。P0 改变了中间商目标函数和支付矩阵，因此旧表格、图和摘要数字已经失去“由当前代码复现”的资格。

只有在新需求模型进入服务商博弈并完成重求解后，才开始新英文主稿。若后续结果保持，推荐题名方向为：

```text
QoS protection beyond aggregate peak shaving:
a verified simulation of temporal pricing and capacity balancing
in heterogeneous inference markets
```

## 下一阶段

1. 将 conserved nested demand 接入中间商 routing--QoS 联合响应和服务商利润函数。
2. 以 BurstGPT 为主负载、合成负载为对照，重建 provider payoff evaluator。
3. 使用标准 bimatrix solver 求有限网格混合均衡，并完整扫描 225 点偏离。
4. 在有限解周围运行连续/Latin-hypercube best response。
5. 对 capacity ratio、price sensitivity、migration cost 和 QoS threshold 做完整重求解，而非固定政策扫描。
6. 用主仿真同一 QoS 函数重新拟合 vLLM 测量并留出验证。
7. 完成后重写摘要、方法、结果、结论和 Figure 1；旧工件不直接迁移。

## 验证

TDD 新增测试覆盖支付守恒、平均价格、联合 residual、价格政策符号、OD 流守恒、nested channel choice、固定点指标、工件 manifest、BurstGPT 聚合和部分下载恢复。

最终相关测试命令包含全部 peak-shaving equilibrium、P0、SMPT、measurement-anchor、spatiotemporal 和 BurstGPT 测试。结果为 `44 passed in 224.49 s`。Ruff 对全部修改 Python 文件报告 `All checks passed`。两个机制工件各含 12 个收敛单元；以 `1e-9` 为需求守恒核验容差时全部通过，BurstGPT 单元的最大浮点偏差约为 `2.3e-13`。
