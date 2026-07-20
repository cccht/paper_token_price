# 论文物联网场景素材库设计

## 目标

在现有 48 个 IconPark 基础图标之上，建立一套更具体的物联网场景素材。每个素材由多个可解释对象组成，能够直接表达论文中的终端负载、API 路由、服务商集群、GPU 状态和仿真诊断，而不是只显示抽象单体图标。

## 风格来源与边界

用户提供的参考图采用彩色设备插画、对象组合、轻微空间层次、明确箭头和少量文字标记。新素材借鉴这些视觉特征，但不复制参考图中的具体图标、构图或装饰细节。

素材全部由已保存的 IconPark SVG 和原创 SVG 几何关系组合，不使用 ImageGen。这样可以继续使用 Apache-2.0 许可链，并避免生成式 AI 图像进入投稿资产。

## 场景清单

### 终端与工作负载

1. Time-rigid user endpoints：交互窗口、手机和时钟。
2. Time-flexible workloads：代码终端、定时任务和批处理。
3. Applied IoT endpoints：多设备、摄像头和智能体。
4. User choice hub：两类用户进入渠道选择。

### 市场与网络

5. API gateway：API 接口、应用网关和路由器。
6. Intermediary routing：API 中间商向两个服务商分流。
7. Provider A cluster：较大 GPU 服务器组和容量状态。
8. Provider B cluster：较小 GPU 服务器组和容量状态。
9. Direct-provider channel：用户绕过中间商直购。
10. Outside option：用户退出内部市场。

### GPU 与 QoS

11. Request stream：请求流进入 GPU 服务节点。
12. GPU utilization：芯片、服务器和利用率仪表。
13. QoS feedback：服务器、利用率和 QoS 的反馈关系。
14. Congestion boundary：利用率、延迟和拥塞阈值。

### 仿真与诊断

15. Price profile and shift：分时价格、曲线和需求迁移。
16. Routing fan-out：中间路由节点向两个服务商分流。
17. Fixed-point loop：路由、QoS 固定点和迭代回路。
18. Payoff and regret：利润、混合策略和 regret 曲线。

## 视觉规范

- 每个独立场景为 480×300 SVG，透明画布。
- 使用浅色等距底板、白色设备面板和低透明度投影建立空间层次。
- 每个场景保留 2–4 个主要对象，避免缩小后成为无法识别的图标堆。
- 实线箭头表示请求或交易，虚线箭头表示价格、QoS 或状态反馈。
- 英文使用 Times New Roman，必要的中文联系表标签使用 SimSun。
- 不在场景内部写完整句子，只允许 `API`、`A`、`B`、`QoS` 等短标记。
- 与基础图标库共用现有六色语义，不引入照片、渐变背景或新的版权素材。

## 输出

```text
figure_sources/paper_iot_scene_library/
├── manifest.json
├── scenes/*.svg
├── paper-iot-scenes.xml
└── README.md
figure_sources/build_paper_iot_scene_library.py
figures/paper_iot_scene_library_2026-07-10.svg
figures/paper_iot_scene_library_2026-07-10.png
figures/paper_iot_scene_library_2026-07-10.pdf
tests/test_paper_iot_scene_library.py
```

## 验收标准

1. 场景清单包含 18 个唯一场景，且每个场景使用 2–4 个已许可的基础图标组件。
2. 18 个独立 SVG 均为 480×300、可解析且不包含远程依赖。
3. Draw.io 自定义库包含 18 个可解码的本地 SVG 数据条目。
4. 联系表为六列三行，不存在图标、箭头、标题或标签遮挡。
5. 生成脚本在无网络条件下可重复构建全部产物。
6. 许可说明明确复用基础 IconPark 库，不引入生成式 AI 图像。

