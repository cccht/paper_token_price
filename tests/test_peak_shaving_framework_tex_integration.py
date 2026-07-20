from pathlib import Path


PROJECT = Path(__file__).resolve().parents[1]
ENGLISH_TEX = PROJECT / "peak_shaving_dynamic_pricing_SMPT_final_2026-06-20.tex"
CHINESE_TEX = PROJECT / "peak_shaving_dynamic_pricing_SMPT_final_zh_2026-06-20.tex"
FIGURE_NAME = "peak_shaving_framework_2026-07-11.pdf"
FIGURE_PATH = PROJECT / "figures" / FIGURE_NAME
OLD_FIGURE_NAME = "framework_imagegen_final_2026-07-10.png"


def manuscript_text(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def test_final_manuscripts_use_the_submission_safe_framework_export() -> None:
    for path in (ENGLISH_TEX, CHINESE_TEX):
        text = manuscript_text(path)
        assert f"\\includegraphics[width=\\textwidth]{{{FIGURE_NAME}}}" in text
        assert OLD_FIGURE_NAME not in text
        assert text.count("\\label{fig:market_schematic}") == 1


def test_submission_framework_export_uses_compatible_pdf_version() -> None:
    data = FIGURE_PATH.read_bytes()
    assert data.startswith(b"%PDF-1.3")
    assert len(data) > 1_000_000


def test_framework_captions_match_the_figure_and_credit_icons() -> None:
    english = manuscript_text(ENGLISH_TEX)
    chinese = manuscript_text(CHINESE_TEX)

    for phrase in (
        "Solid arrows denote requests or routed traffic",
        "dashed arrows denote price and QoS signals",
        "finite-grid regret",
        "Streamline Ultimate Color",
        "CC BY 4.0",
    ):
        assert phrase in english

    for phrase in (
        "实线表示请求或路由流量",
        "虚线表示价格和 QoS 信号",
        "有限网格 regret",
        "Streamline Ultimate Color",
        "CC BY 4.0",
    ):
        assert phrase in chinese


def test_framework_provenance_and_ai_declarations_are_current() -> None:
    english = manuscript_text(ENGLISH_TEX)
    chinese = manuscript_text(CHINESE_TEX)

    assert "figure_sources/peak_shaving_framework_2026-07-11.drawio" in english
    assert "figure_sources/peak_shaving_framework_2026-07-11.drawio" in chinese
    assert "No generative image model was used to create or alter the vector artwork" in english
    assert "未使用生成式图像模型创建或修改该矢量图稿" in chinese
    assert "must be replaced by an author-approved non-AI artwork" not in english
    assert "在正式投稿前应替换为作者确认的非 AI 图稿" not in chinese
