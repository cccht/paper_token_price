import base64
import json
from collections import Counter
from pathlib import Path
from xml.etree import ElementTree

from PIL import Image


PROJECT = Path(__file__).resolve().parents[1]
SCENE_DIR = PROJECT / "figure_sources" / "paper_iot_scene_library"
BASE_MANIFEST = PROJECT / "figure_sources" / "paper_icon_library" / "manifest.json"
SCENE_MANIFEST = SCENE_DIR / "manifest.json"
DRAWIO_LIBRARY = SCENE_DIR / "paper-iot-scenes.xml"
PREVIEW_PNG = PROJECT / "figures" / "paper_iot_scene_library_2026-07-10.png"
PREVIEW_PDF = PROJECT / "figures" / "paper_iot_scene_library_2026-07-10.pdf"
EXPECTED_GROUPS = {
    "endpoints": 4,
    "market_network": 6,
    "serving_qos": 4,
    "simulation": 4,
}


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def base_icon_ids() -> set[str]:
    manifest = load_json(BASE_MANIFEST)
    return {
        icon["id"]
        for category in manifest["categories"]
        for icon in category["icons"]
    }


def test_scene_manifest_has_expected_scope_and_valid_components() -> None:
    manifest = load_json(SCENE_MANIFEST)
    scenes = manifest["scenes"]

    assert len(scenes) == 18
    assert len({scene["id"] for scene in scenes}) == 18
    assert Counter(scene["group"] for scene in scenes) == EXPECTED_GROUPS
    assert Counter(scene["priority"] for scene in scenes) == {"core": 15, "optional": 3}
    assert manifest["base_library_commit"] == "8dc132da4c85671ba6a5962c87aa2bdafbf158e9"

    known_icons = base_icon_ids()
    for scene in scenes:
        assert 2 <= len(scene["components"]) <= 4
        assert {component["icon"] for component in scene["components"]} <= known_icons
        assert all(0 <= component["x"] <= 480 for component in scene["components"])
        assert all(0 <= component["y"] <= 300 for component in scene["components"])


def test_individual_scene_svgs_are_local_and_well_formed() -> None:
    scenes = load_json(SCENE_MANIFEST)["scenes"]
    scene_files = sorted((SCENE_DIR / "scenes").glob("*.svg"))
    assert len(scene_files) == 18

    for scene in scenes:
        path = SCENE_DIR / "scenes" / f"{scene['id']}.svg"
        text = path.read_text(encoding="utf-8")
        root = ElementTree.fromstring(text)
        assert root.attrib["viewBox"] == "0 0 480 300"
        assert "<script" not in text
        assert 'href="http' not in text


def test_drawio_scene_library_embeds_all_scenes() -> None:
    text = DRAWIO_LIBRARY.read_text(encoding="utf-8")
    entries = json.loads(text.removeprefix("<mxlibrary>").removesuffix("</mxlibrary>\n"))

    assert len(entries) == 18
    assert {entry["id"] for entry in entries} == {
        scene["id"] for scene in load_json(SCENE_MANIFEST)["scenes"]
    }
    for entry in entries:
        assert entry["w"] == 480
        assert entry["h"] == 300
        assert entry["data"].startswith("data:image/svg+xml;base64,")
        payload = base64.b64decode(entry["data"].split(",", 1)[1])
        assert ElementTree.fromstring(payload).attrib["viewBox"] == "0 0 480 300"


def test_scene_contact_sheet_is_nonblank_and_large_enough() -> None:
    with Image.open(PREVIEW_PNG) as image:
        assert image.width >= 3600
        assert image.height >= 1900
        colors = image.convert("RGB").getcolors(maxcolors=image.width * image.height)
        assert colors is not None
        assert len(colors) >= 40

    assert PREVIEW_PDF.read_bytes().startswith(b"%PDF-")
    assert PREVIEW_PDF.stat().st_size > 75_000


def test_scene_library_documents_non_ai_provenance() -> None:
    readme = (SCENE_DIR / "README.md").read_text(encoding="utf-8")
    assert "paper-iot-scenes.xml" in readme
    assert "not generated with ImageGen" in readme
    assert "Apache-2.0" in readme
