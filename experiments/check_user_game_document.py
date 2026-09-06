"""Render the new manuscript and record checks without altering source data."""
from __future__ import annotations

import hashlib
import json
import math
import shutil

import numpy as np
import pymupdf
from PIL import Image, ImageDraw

from experiments.run_user_provider_game import OUT, ROOT

STEM = "llm_user_provider_game_2026-09-06"


def main():
    built = ROOT / f"latex_aux/user_provider_game_20260906/{STEM}.pdf"
    pdf = ROOT / f"{STEM}.pdf"
    shutil.copy2(built, pdf)
    log = built.with_suffix(".log").read_text(errors="replace")
    forbidden = ("Overfull", "undefined", "Missing character", "LaTeX Error")
    assert not any(term in log for term in forbidden)
    preview = OUT / "document_preview"
    preview.mkdir(parents=True, exist_ok=True)
    doc = pymupdf.open(pdf)
    contact = Image.new("RGB", (4 * 330, math.ceil(len(doc) / 4) * 490), "#E5E5E5")
    draw = ImageDraw.Draw(contact)
    pages = []
    for idx, page in enumerate(doc):
        text = page.get_text()
        assert "??" not in text
        for word in page.get_text("words"):
            assert word[0] >= 0 and word[1] >= 0 and word[2] <= page.rect.width + 1 and word[3] <= page.rect.height + 1
        pix = page.get_pixmap(matrix=pymupdf.Matrix(1.4, 1.4), alpha=False)
        pixels = np.frombuffer(pix.samples, dtype=np.uint8)
        assert pixels.std() > 12
        path = preview / f"page_{idx + 1:02}.png"
        pix.save(path)
        thumb = Image.frombytes("RGB", (pix.width, pix.height), pix.samples)
        thumb.thumbnail((310, 450))
        x, y = (idx % 4) * 330 + 10, (idx // 4) * 490 + 25
        contact.paste(thumb, (x, y))
        draw.text((x, y - 18), f"Page {idx + 1}", fill="black")
        figures = [number for number in range(1, 7) if f"Figure {number}:" in text]
        pages.append({"page": idx + 1, "word_count": len(page.get_text("words")), "figures": figures,
                      "pixel_std": float(pixels.std()), "png_sha256": hashlib.sha256(path.read_bytes()).hexdigest()})
    contact.save(preview / "contact_sheet.png")
    report = {"automated_checks_passed": True, "visual_review_required": True, "pages": pages,
              "pdf_sha256": hashlib.sha256(pdf.read_bytes()).hexdigest(),
              "tex_sha256": hashlib.sha256((ROOT / f"{STEM}.tex").read_bytes()).hexdigest(),
              "document_check_script_sha256": hashlib.sha256((ROOT / "experiments/check_user_game_document.py").read_bytes()).hexdigest(),
              "checks": ["No overfull boxes, undefined references or missing characters in LaTeX log",
                         "No unresolved question-mark references", "All extracted words within page bounds",
                         "Every page has nonblank pixels"]}
    (OUT / "document_checks.json").write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({"pages": len(doc), "figures": {p["page"]: p["figures"] for p in pages if p["figures"]}, "pdf_sha256": report["pdf_sha256"]}, indent=2))


if __name__ == "__main__":
    main()
