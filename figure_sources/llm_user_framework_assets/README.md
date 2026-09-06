# LLM 用户框架图资源

用于“应用入口—时序市场模型—服务商/中间商”的可编辑图 1。中间利润曲线来自 round-20 的真实后处理数据，不使用 imagegen 示意数值。

- VS Code、Word、Excel 标识从 [vscode-icons](https://github.com/vscode-icons/vscode-icons) 的固定提交 `8dbc8ce02e64fa31a7f81737f7244842fb6de5ca` 下载。
- 上游明确区分源代码 MIT 许可、普通图标许可与品牌标识的原权利人许可。本目录的品牌标识不被重新声明为 MIT 或 CC BY；品牌和商标权利仍归原权利人。
- 对话与服务端图标来自 [Streamline](https://streamlinehq.com)，采用 CC BY 4.0。
- 各文件来源与 SHA-256 见 `sources.json`；图标内容未改，仅缩放。应用标识仅说明示例入口，不表示合作、认可或真实数据来自这些应用。

```bash
TMPDIR=/tmp TEMP=/tmp TMP=/tmp uv run --no-project --with cairosvg python figure_sources/build_llm_user_framework.py
```

加 `--fetch-icons` 可从固定提交重新取得图标。构建输出位于 `figures/user_temporal_20260906/framework/`，Draw.io 源文件为 `figure_sources/llm_user_framework_20260906.drawio`。
