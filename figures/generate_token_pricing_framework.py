from pathlib import Path

import matplotlib as mpl
import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch, Rectangle


PALETTE = {
    "navy": "#0F4D92",
    "blue": "#3775BA",
    "teal": "#42949E",
    "slate": "#5B6B7A",
    "ink": "#272727",
    "grey": "#767676",
    "line": "#AAB5BF",
    "panel": "#F7F9FB",
    "blue_soft": "#E7EFF8",
    "teal_soft": "#E7F3F4",
    "grey_soft": "#EEF1F3",
    "green": "#2E7D4A",
    "green_soft": "#E8F3EB",
    "amber_soft": "#F7F1E2",
}


mpl.rcParams.update(
    {
        "font.family": "sans-serif",
        "font.sans-serif": ["Microsoft YaHei", "Arial", "SimHei", "DejaVu Sans"],
        "font.size": 5.5,
        "svg.fonttype": "none",
        "pdf.fonttype": 42,
        "ps.fonttype": 42,
        "axes.unicode_minus": False,
    }
)


def add_box(
    ax,
    rect,
    *,
    title,
    body,
    face="white",
    edge=PALETTE["line"],
    accent=PALETTE["navy"],
    title_size=5.8,
    body_size=5.1,
    linewidth=0.75,
):
    x, y, width, height = rect
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.006,rounding_size=0.008",
        linewidth=linewidth,
        edgecolor=edge,
        facecolor=face,
    )
    ax.add_patch(patch)
    ax.add_patch(Rectangle((x, y + height - 0.006), width, 0.006, color=accent, lw=0))
    ax.text(
        x + 0.012,
        y + height - 0.018,
        title,
        ha="left",
        va="top",
        fontsize=title_size,
        fontweight="bold",
        color=PALETTE["ink"],
    )
    ax.text(
        x + 0.012,
        y + height - 0.043,
        body,
        ha="left",
        va="top",
        fontsize=body_size,
        linespacing=1.38,
        color=PALETTE["ink"],
    )


def add_arrow(ax, start, end, *, color=PALETTE["navy"], style="-|>", width=0.9):
    arrow = FancyArrowPatch(
        start,
        end,
        arrowstyle=style,
        mutation_scale=8,
        linewidth=width,
        color=color,
        connectionstyle="arc3,rad=0.0",
        shrinkA=2,
        shrinkB=2,
    )
    ax.add_patch(arrow)


def add_panel(ax, rect, *, letter, title):
    x, y, width, height = rect
    patch = FancyBboxPatch(
        (x, y),
        width,
        height,
        boxstyle="round,pad=0.004,rounding_size=0.010",
        linewidth=0.65,
        edgecolor="#D4DBE1",
        facecolor=PALETTE["panel"],
    )
    ax.add_patch(patch)
    ax.text(x - 0.018, y + height - 0.006, letter, fontsize=8, fontweight="bold")
    ax.text(x + 0.014, y + height - 0.018, title, fontsize=6.4, fontweight="bold")


def draw_background_panel(ax):
    add_panel(
        ax,
        (0.035, 0.755, 0.93, 0.165),
        letter="a",
        title="研究背景与问题：以跨时段价格协调可迁移的 Token 请求",
    )
    boxes = [
        ((0.060, 0.782, 0.185, 0.092), "电力需求响应启发", "峰谷负载不均\n价格表达时段稀缺性", PALETTE["grey_soft"]),
        ((0.285, 0.782, 0.185, 0.092), "Token 推理服务", "GPU 容量有限\n过载抬升 TTFT 与超时", PALETTE["blue_soft"]),
        ((0.510, 0.782, 0.185, 0.092), "核心问题", "固定平均标价下\n能否迁移弹性需求？", PALETTE["teal_soft"]),
        ((0.735, 0.782, 0.190, 0.092), "研究问题", "RQ1 缓解拥挤  RQ2 QoS 价值\nRQ3 关键假设稳健性", PALETTE["amber_soft"]),
    ]
    for rect, title, body, face in boxes:
        add_box(ax, rect, title=title, body=body, face=face)
    for left, right in [(0.245, 0.285), (0.470, 0.510), (0.695, 0.735)]:
        add_arrow(ax, (left, 0.828), (right, 0.828))


def draw_model_panel(ax):
    add_panel(
        ax,
        (0.035, 0.392, 0.93, 0.335),
        letter="b",
        title="理论模型与求解：领导者发布价格，聚合需求响应，QoS 影响有效服务收益",
    )
    boxes = [
        ((0.060, 0.595, 0.190, 0.078), "价格约束",
         "mean(p_t) = p_bar\np_min <= p_t <= p_max\n可选：发布账单 <= 基线",
         PALETTE["grey_soft"], PALETTE["slate"]),
        ((0.300, 0.595, 0.155, 0.078), "平台：领导者",
         "发布时段价格向量 p\n表达跨时段稀缺性", PALETTE["blue_soft"], PALETTE["navy"]),
        ((0.505, 0.595, 0.185, 0.078), "用户：跟随者响应",
         "刚性需求 R_t(p_t)\n弹性需求 F_t(p)：logit 迁移", PALETTE["teal_soft"], PALETTE["teal"]),
        ((0.740, 0.595, 0.175, 0.078), "负载与 QoS 代理",
         "D_t = R_t + F_t\nu_t = D_t / G -> q(u_t)", PALETTE["amber_soft"], PALETTE["slate"]),
        ((0.690, 0.465, 0.225, 0.078), "平台目标",
         "利润：有效结算收入 - 服务成本\n       - 流失成本 - QoS 退化成本\n并记录模型内福利组成",
         PALETTE["green_soft"], PALETTE["green"]),
        ((0.390, 0.465, 0.235, 0.078), "数值求解",
         "有界均值投影 + 多起点 SLSQP\n返回经过约束校验的最佳可行候选\n不声称非凸问题的全局最优证书",
         PALETTE["blue_soft"], PALETTE["navy"]),
        ((0.060, 0.465, 0.265, 0.078), "理论性质",
         "可行域非空条件\n有界均值投影的欧氏最优性质\n平台最优解存在性",
         PALETTE["grey_soft"], PALETTE["slate"]),
    ]
    for rect, title, body, face, accent in boxes:
        add_box(ax, rect, title=title, body=body, face=face, accent=accent)
    for start, end in [
        ((0.250, 0.634), (0.300, 0.634)),
        ((0.455, 0.634), (0.505, 0.634)),
        ((0.690, 0.634), (0.740, 0.634)),
        ((0.827, 0.595), (0.805, 0.543)),
        ((0.690, 0.504), (0.625, 0.504)),
        ((0.507, 0.543), (0.380, 0.593)),
    ]:
        add_arrow(ax, start, end)
    ax.text(0.410, 0.554, "优化更新价格", fontsize=4.9, color=PALETTE["ink"])


def draw_experiment_panel(ax):
    add_panel(
        ax,
        (0.035, 0.222, 0.93, 0.145),
        letter="c",
        title="合成实验：区分一般动态定价收益与显式 QoS 建模的增量价值",
    )
    add_box(
        ax,
        (0.060, 0.246, 0.235, 0.073),
        title="策略比较",
        body="统一定价\n短视动态定价（搜索时忽略退化）\nQoS 感知动态定价",
        face=PALETTE["grey_soft"],
        accent=PALETTE["slate"],
    )
    add_box(
        ax,
        (0.345, 0.246, 0.255, 0.073),
        title="验证设计",
        body="10 个随机种子；9 类敏感性与消融\n容量、退化强度、账单保护、反馈等\n完整保存价格、需求、QoS 与诊断",
        face=PALETTE["blue_soft"],
    )
    add_box(
        ax,
        (0.650, 0.246, 0.265, 0.073),
        title="基准结果",
        body="利润：相对短视策略 +5.22%；相对统一定价 +80.51%\n最低 QoS：0.6632 -> 0.9918\n账单保护下：利润相对统一定价 +21.29%",
        face=PALETTE["green_soft"],
        accent=PALETTE["green"],
    )
    add_arrow(ax, (0.295, 0.282), (0.345, 0.282))
    add_arrow(ax, (0.600, 0.282), (0.650, 0.282))


def draw_validation_panel(ax):
    add_panel(
        ax,
        (0.035, 0.050, 0.93, 0.145),
        letter="d",
        title="真实后端测量与解释边界：验证拥挤现象，不将微基准误作生产校准",
    )
    add_box(
        ax,
        (0.060, 0.074, 0.235, 0.073),
        title="单 GPU 压力测试",
        body="Ollama + vLLM；RTX 4090\n记录 TTFT、吞吐、完成率与 SLA\n高并发下 TTFT 上升，SLA 达标率下降",
        face=PALETTE["grey_soft"],
        accent=PALETTE["slate"],
    )
    add_box(
        ax,
        (0.345, 0.074, 0.255, 0.073),
        title="经验 QoS 启发式映射",
        body="以 TTFT SLA 达标率构造稳健性场景\n连接系统测量与合成经济模型\n仅用于参数迁移，不替代生产轨迹校准",
        face=PALETTE["blue_soft"],
    )
    add_box(
        ax,
        (0.650, 0.074, 0.265, 0.073),
        title="论文结论",
        body="约束动态定价可迁移弹性请求并缓解峰时拥挤\nQoS 建模的额外价值在容量紧张时更明显\n适用边界：单平台、合成需求、参数化 QoS 代理",
        face=PALETTE["teal_soft"],
        accent=PALETTE["teal"],
    )
    add_arrow(ax, (0.295, 0.110), (0.345, 0.110))
    add_arrow(ax, (0.600, 0.110), (0.650, 0.110))


def build_figure():
    fig = plt.figure(figsize=(181.4 / 25.4, 168 / 25.4), facecolor="white")
    ax = fig.add_axes((0, 0, 1, 1))
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis("off")
    ax.text(
        0.035,
        0.970,
        "固定平均标价约束下 Token 服务跨时段定价：研究框架",
        fontsize=7,
        fontweight="bold",
        color=PALETTE["ink"],
        ha="left",
        va="top",
    )
    ax.text(
        0.035,
        0.943,
        "从需求响应机制迁移、领导者--跟随者建模到仿真与单 GPU 拥挤验证",
        fontsize=5.5,
        color=PALETTE["ink"],
        ha="left",
        va="top",
    )
    draw_background_panel(ax)
    draw_model_panel(ax)
    draw_experiment_panel(ax)
    draw_validation_panel(ax)
    return fig


def export_figure(fig):
    output_dir = Path(__file__).resolve().parent
    output_base = output_dir / "fig_framework_token_pricing"
    fig.savefig(output_base.with_suffix(".svg"), bbox_inches="tight", pad_inches=0.03)
    fig.savefig(output_base.with_suffix(".pdf"), bbox_inches="tight", pad_inches=0.03)
    fig.savefig(output_base.with_suffix(".png"), dpi=450, bbox_inches="tight", pad_inches=0.03)
    plt.close(fig)


if __name__ == "__main__":
    export_figure(build_figure())
