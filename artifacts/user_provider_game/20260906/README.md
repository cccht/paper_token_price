# 用户自主换时与厂家定价博弈：完整新模型结果

本目录只对应 2026-09-06 新建的“厂家定价竞争 + 原子用户 Nash 子博弈”，不混用旧 Logit 聚合响应模型及其数值。原稿、旧实验和旧图均保留。

## 先看结果

- [新论文 PDF](../../../llm_user_provider_game_2026-09-06.pdf) / [TeX](../../../llm_user_provider_game_2026-09-06.tex)，共 13 页。
- [同一分时价格下，算法使用前后](../../../figures/user_provider_game_20260906/same_price_before_after.pdf)，论文第 7 页。
- [双方均求均衡的统一价与分时价对比](../../../figures/user_provider_game_20260906/fair_tariff_comparison.pdf)，论文第 9 页。
- [个人效用与可行时段](../../../figures/user_provider_game_20260906/individual_time_choices.pdf)，论文第 8 页。
- [用户响应收敛](../../../figures/user_provider_game_20260906/user_convergence.pdf)，论文第 9 页。
- [厂家分时负载与 QoS](../../../figures/user_provider_game_20260906/provider_load_quality.pdf)，论文第 10 页。
- [新框架图](../../../figures/user_provider_game_20260906/user_game_framework.pdf) / [可编辑 Draw.io](../../../figure_sources/user_game_framework_20260906.drawio)，论文第 2 页。

| 指标 | 同价算法前 | 同价算法后 | 变化 |
|---|---:|---:|---:|
| 平均个人净效用 | 0.92698 | 0.97718 | +0.05021 绝对单位 |
| 平均广义成本 | 1.07302 | 1.02282 | -4.68% |
| 平均费用 | 0.99125 | 0.92659 | -6.52% |
| 期望峰值负载 | 59.00 | 53.06 | -10.07% |
| 期望最大用户偏离收益 | 0.50789 | 0 | 无可获利单边偏离 |

同价比较固定最终分时价格的混合策略和每个价格对，只改变用户安排。算法前是原生安排，不是均衡。算法后 14.34% 的用户换时、20.37% 换厂家，两者可以重合。平均延期 0.484 小时，灵活用户平均 0.967 小时。121/240 人期望效用增加，119/240 人降低。效用零点由任务价值决定，不能把绝对效用差包装成效用增长百分比。

**公平机制比较结果不利于用户。** 统一价和分时价都求用户与厂家均衡时，分时价的平均费用增加 13.66%，广义成本增加 13.76%，平均效用降低 0.12373，峰值增加 1.29%；197/240 人期望效用下降。五个预声明种子的平均效用差均为负。以上同价算法收益不能解释为分时制度优于统一价制度。

## 文件与验证

- `experiment.json`：完整协议参数、输入和代码 SHA、全部厂家菜单和收益矩阵、用户群、支持策略、四项边界、五个种子、三种补充用户顺序和均价对照。
- `analysis.json`：两个不同比较、全部个人效用差和示例选择规则；`*_table.tex` 为程序生成的论文表格。
- `outcomes.csv`、`user_outcomes.csv`（240 人）、`period_outcomes.csv`、`convergence.csv`、`boundary_cases.csv`：可核对源数据。
- `verification.json`：50,625 个场景与价格组合完整重算，独立费用、效用、QoS、计费和偏离公式；全部用户 regret 为 0，厂家最大 regret 约 4.3e-14，收益矩阵最大误差为 0。代表状态额外对 824 个可行用户偏离逐一重建完整安排。
- `document_checks.json`、`document_preview/`：编译与页面边界检查，完整逐页预览。
- `bundle_manifest.json`、`reproducible_bundle.zip`：自包含新模型快照与逐文件 SHA。仅包含显式列出的相关文件，不删除或移动原文件。

新实验 SHA-256：`3e7f8993088822f32f6900f3d8eb22c601a3536675cafedbb9891353fc610450`。

## 复现

在论文项目根目录运行。实验原始环境为 Python 3.12.13、NumPy 2.4.4、SciPy 1.17.1；下列命令使用仓库依赖。重复运行会重建本新模型目录内的同名输出，执行前可先保留本目录的压缩快照，不影响历史模型目录。

需要锁定完整 Python 依赖时，将下列 `requirements.txt` 替换为 `requirements-user-game-20260906.txt`，并在 `uv run` 后加 `--python 3.12.13`。图件沿用项目的 Times New Roman 字体；该商业字体不随压缩包分发，异机重绘应安装已获授权的字体或另存为明确标注替代字体的版本。LaTeX 编译另需 `latexmk` 和常规 TeX Live 宏包。

```bash
env TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --no-project --with-requirements requirements.txt python -m experiments.run_user_provider_game --workers 4 --maximum-level 9
uv run --no-project --with-requirements requirements.txt python -m experiments.report_user_provider_game
uv run --no-project --with-requirements requirements.txt python -m experiments.plot_user_provider_game
uv run --no-project --with-requirements requirements.txt --with cairosvg python -m figure_sources.build_user_game_framework
env TMPDIR=/tmp TEMP=/tmp TMP=/tmp OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1 MKL_NUM_THREADS=1 uv run --no-project --with-requirements requirements.txt python -m experiments.verify_user_provider_game
uv run --no-project --with-requirements requirements.txt python -m pytest -q tests/test_user_time_game.py tests/test_user_provider_pricing.py tests/test_user_provider_artifacts.py
latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=latex_aux/user_provider_game_20260906 llm_user_provider_game_2026-09-06.tex
uv run --no-project --with-requirements requirements.txt --with pymupdf --with pillow python -m experiments.check_user_game_document
uv run --no-project --with-requirements requirements.txt python -m experiments.package_user_provider_game
```

## 认证边界

这里只认证预声明有限游戏，不认证连续价格域。价格菜单加密显示粗网格存在实质性漏检，因此不声称已经证明连续均衡。用户任务等工作量、拥塞成本同质，延期成本为合成参数；实际请求差异、用户退出、个体补偿及中间商均未纳入。期限是允许选择的时段边界，不是真实队列的完成时间保证。更换用户响应顺序的检查只在支持价格对上进行，不能外推为新的厂家均衡证书。本结果不是“所有用户获益”或“可直接投稿”的认证。
