# 论文专用图标库设计

## 目标

为固定容量推理服务分时定价论文建立一套可编辑、许可清楚、视觉一致的图标素材。图标库覆盖正文框架图所需概念，并提供少量物联网和仿真诊断备用素材。库本身不改变现有 Figure 1 或 TeX。

## 范围

- 采用 ByteDance IconPark 官方 SVG，固定到上游提交 `8dc132da4c85671ba6a5962c87aa2bdafbf158e9`。
- 选取 48 个图标，分为市场主体、LLM/物联网工作负载、API 与网络、GPU 与 QoS、定价与博弈、仿真与验证六组。
- 每个图标在清单中记录上游路径、英文标签、中文含义、论文用途和 `core`/`optional` 优先级。
- 保留未经改动的上游 SVG；Draw.io 库和预览使用统一的论文配色生成派生版本。
- 生成可导入 Draw.io 的 `.xml` 自定义库，以及 PNG/PDF 联系表。
- 保留 Apache-2.0 许可、上游提交号和修改说明。

## 视觉规则

- 图标统一使用 IconPark 的 48×48 描边体系，不混入其他图标家族。
- 颜色按语义分组，而不是随机着色：深蓝表示市场与信息，青色表示用户与服务，金色表示定价与资源，珊瑚色表示风险与 QoS 边界，浅蓝表示仿真与验证。
- 主色采用 `#24557A`、`#2A9D8F`、`#D49A16`、`#DE6B57`、`#5B9BD5`，辅以深灰 `#344054`。
- 联系表使用白底和固定卡片尺寸。英文标签使用 Times New Roman，中文标签使用 SimSun 字形回退；图标不使用渐变、阴影或照片效果。
- 主框架图只从 `core` 子集中选择，备用素材不会因为已经存在于库中而自动加入论文。

## 输出结构

```text
figure_sources/paper_icon_library/
├── manifest.json
├── upstream_svg/
├── paper-icons.xml
├── LICENSE-APACHE-2.0.txt
├── MODIFICATIONS.md
└── README.md
figure_sources/build_paper_icon_library.py
figures/paper_icon_library_2026-07-10.png
figures/paper_icon_library_2026-07-10.pdf
tests/test_paper_icon_library.py
```

## 验收标准

1. 清单恰好包含 48 个唯一图标，六个类别各 8 个。
2. 每条记录都能解析到本地 SVG，且 SVG 的 `viewBox` 为 `0 0 48 48`。
3. Draw.io 自定义库条目数与清单一致，名称可读且图像数据不依赖网络。
4. PNG 和 PDF 联系表均能打开；PNG 不是空白图，每个图标及标签均在卡片内。
5. 许可、上游提交号和派生修改说明齐全。
6. README 记录实际命令、输出和验证结果。
