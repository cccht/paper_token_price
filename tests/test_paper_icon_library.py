import base64
import json
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

from PIL import Image


PROJECT = Path(__file__).resolve().parents[1]
LIBRARY_DIR = PROJECT / "figure_sources" / "paper_icon_library"
MANIFEST_PATH = LIBRARY_DIR / "manifest.json"
DRAWIO_LIBRARY_PATH = LIBRARY_DIR / "paper-icons.xml"
PREVIEW_PNG = PROJECT / "figures" / "paper_icon_library_2026-07-10.png"
PREVIEW_PDF = PROJECT / "figures" / "paper_icon_library_2026-07-10.pdf"
EXPECTED_CATEGORIES = {
    "market",
    "workloads",
    "network",
    "serving",
    "pricing",
    "simulation",
}


def load_manifest() -> dict:
    return json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))


def manifest_icons(manifest: dict) -> list[dict]:
    return [
        {**icon, "category": category["id"], "color": category["color"]}
        for category in manifest["categories"]
        for icon in category["icons"]
    ]


def test_manifest_has_six_balanced_categories_and_unique_icons() -> None:
    manifest = load_manifest()
    categories = manifest["categories"]
    icons = manifest_icons(manifest)

    assert manifest["upstream"]["commit"] == "8dc132da4c85671ba6a5962c87aa2bdafbf158e9"
    assert manifest["upstream"]["license"] == "Apache-2.0"
    assert {category["id"] for category in categories} == EXPECTED_CATEGORIES
    assert {category["id"]: len(category["icons"]) for category in categories} == {
        category: 8 for category in EXPECTED_CATEGORIES
    }
    assert len(icons) == 48
    assert len({icon["id"] for icon in icons}) == 48
    assert len({icon["source"] for icon in icons}) == 48
    assert Counter(icon["priority"] for icon in icons) == {"core": 30, "optional": 18}


def test_every_manifest_icon_has_a_local_48px_svg() -> None:
    icons = manifest_icons(load_manifest())

    for icon in icons:
        source = LIBRARY_DIR / "upstream_svg" / icon["source"]
        assert source.is_file(), icon["id"]
        text = source.read_text(encoding="utf-8")
        root = ElementTree.fromstring(text)
        assert root.tag.endswith("svg")
        assert root.attrib["viewBox"] == "0 0 48 48"
        assert "<image" not in text
        assert "<script" not in text
        assert 'href="http' not in text


def test_drawio_library_contains_all_embedded_svg_assets() -> None:
    manifest = load_manifest()
    expected_ids = {icon["id"] for icon in manifest_icons(manifest)}
    text = DRAWIO_LIBRARY_PATH.read_text(encoding="utf-8")
    assert text.startswith("<mxlibrary>")
    assert text.endswith("</mxlibrary>\n")
    entries = json.loads(text.removeprefix("<mxlibrary>").removesuffix("</mxlibrary>\n"))

    assert len(entries) == 48
    assert {entry["id"] for entry in entries} == expected_ids
    for entry in entries:
        assert entry["w"] == 48
        assert entry["h"] == 48
        assert entry["data"].startswith("data:image/svg+xml;base64,")
        payload = base64.b64decode(entry["data"].split(",", 1)[1])
        root = ElementTree.fromstring(payload)
        assert root.attrib["viewBox"] == "0 0 48 48"


def test_preview_outputs_are_nonblank_and_publication_sized() -> None:
    with Image.open(PREVIEW_PNG) as image:
        assert image.width >= 2400
        assert image.height >= 1600
        colors = image.convert("RGB").getcolors(maxcolors=image.width * image.height)
        assert colors is not None
        assert len(colors) >= 20

    assert PREVIEW_PDF.read_bytes().startswith(b"%PDF-")
    assert PREVIEW_PDF.stat().st_size > 50_000


def test_provenance_documents_are_complete() -> None:
    licence = (LIBRARY_DIR / "LICENSE-APACHE-2.0.txt").read_text(encoding="utf-8")
    modifications = (LIBRARY_DIR / "MODIFICATIONS.md").read_text(encoding="utf-8")
    readme = (LIBRARY_DIR / "README.md").read_text(encoding="utf-8")

    assert "Apache License" in licence
    assert "Version 2.0" in licence
    assert "8dc132da4c85671ba6a5962c87aa2bdafbf158e9" in modifications
    assert "paper-icons.xml" in readme
    assert "core" in readme
    assert "optional" in readme
