#!/usr/bin/env python3
"""Create an in-project dated manuscript snapshot."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
import argparse
import hashlib
import json
from pathlib import Path
import re
import shutil


PAPER_DIR = Path(__file__).resolve().parent
MANUSCRIPT = "token_dynamic_pricing_game.tex"
MANUSCRIPT_SOURCES = [
    MANUSCRIPT,
    "token_dynamic_pricing_game_sci_main.tex",
    "token_dynamic_pricing_game_supplement.tex",
]
CORE_FILES = [
    MANUSCRIPT,
    "archive_daily_snapshot.py",
    "token_dynamic_pricing_game.pdf",
    "token_dynamic_pricing_game_sci_main.tex",
    "token_dynamic_pricing_game_sci_main.pdf",
    "token_dynamic_pricing_game_supplement.tex",
    "token_dynamic_pricing_game_supplement.pdf",
    "verified_refs.bib",
    "docs/system-benchmark.md",
    "docs/vllm-system-benchmark.md",
    "docs/reviews/review_report.md",
    "docs/reviews/review_report_round2.md",
    "experiments/README.md",
    "README.md",
]
SNAPSHOT_GLOBS = [
    "artifacts/calibration_uncertainty/*/*.csv",
    "artifacts/calibration_uncertainty/*/*.json",
    "artifacts/review_strengthening/*/*.csv",
    "artifacts/review_strengthening/*/*.json",
    "docs/reviews/*.md",
    "experiments/*.py",
    "figures/reference_aligned/*.mmd",
    "paper_rewriting_output/**/*.bib",
    "paper_rewriting_output/**/*.json",
    "paper_rewriting_output/**/*.md",
    "paper_rewriting_output/**/*.pdf",
    "paper_rewriting_output/**/*.tex",
    "tests/*.py",
]


@dataclass(frozen=True)
class FileRecord:
    path: str
    sha256: str
    size: int


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Archive today's manuscript snapshot.")
    parser.add_argument("--date", help="Archive date in YYYY-MM-DD format. Defaults to today.")
    return parser.parse_args()


def includegraphics_paths(tex_path: Path) -> list[str]:
    text = tex_path.read_text(encoding="utf-8")
    pattern = re.compile(r"\\includegraphics(?:\[[^\]]*\])?\{([^}]+)\}")
    paths = []
    for raw in pattern.findall(text):
        candidate = raw.strip()
        if candidate and not candidate.startswith(("http://", "https://")):
            paths.append(candidate)
    return sorted(set(paths))


def snapshot_paths() -> list[str]:
    paths = [name for name in CORE_FILES if (PAPER_DIR / name).exists()]
    for source in MANUSCRIPT_SOURCES:
        source_path = PAPER_DIR / source
        if source_path.exists():
            paths.extend(includegraphics_paths(source_path))
    for pattern in SNAPSHOT_GLOBS:
        paths.extend(path.relative_to(PAPER_DIR).as_posix() for path in PAPER_DIR.glob(pattern) if path.is_file())
    return sorted(set(paths))


def organize_existing_root_files(day_dir: Path, stamp: str) -> list[str]:
    protected = {"README.md", "CHANGELOG.md"}
    loose_files = [path for path in day_dir.iterdir() if path.is_file() and path.name not in protected]
    if not loose_files:
        return []
    target = day_dir / "legacy_loose_files" / stamp
    target.mkdir(parents=True, exist_ok=True)
    moved = []
    for src in sorted(loose_files):
        dst = target / src.name
        shutil.move(str(src), str(dst))
        moved.append(dst.relative_to(day_dir).as_posix())
    return moved


def copy_snapshot(paths: list[str], source_root: Path) -> None:
    for rel in paths:
        src = PAPER_DIR / rel
        if not src.is_file():
            raise FileNotFoundError(f"Missing snapshot input: {src}")
        dst = source_root / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(src, dst)


def hash_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_manifest(source_root: Path) -> list[FileRecord]:
    records = []
    for path in sorted(p for p in source_root.rglob("*") if p.is_file()):
        rel = path.relative_to(source_root).as_posix()
        records.append(FileRecord(rel, hash_file(path), path.stat().st_size))
    return records


def write_manifest(records: list[FileRecord], records_dir: Path) -> None:
    records_dir.mkdir(parents=True, exist_ok=True)
    lines = [f"{item.sha256}  {item.size:>10}  {item.path}\n" for item in records]
    (records_dir / "MANIFEST.sha256").write_text("".join(lines), encoding="utf-8")


def parse_manifest(path: Path) -> dict[str, str]:
    result = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if not line.strip():
            continue
        sha, _size, rel = line.split(maxsplit=2)
        result[rel] = sha
    return result


def previous_manifest(current_snapshot: Path) -> dict[str, str] | None:
    manifests = sorted(PAPER_DIR.glob("20??-??-??/snapshots/*/records/MANIFEST.sha256"))
    previous = [path for path in manifests if current_snapshot not in path.parents]
    if not previous:
        return None
    return parse_manifest(previous[-1])


def change_summary(previous: dict[str, str] | None, records: list[FileRecord]) -> list[str]:
    current = {item.path: item.sha256 for item in records}
    if previous is None:
        return [f"- initial snapshot with {len(current)} files"]
    added = sorted(set(current) - set(previous))
    removed = sorted(set(previous) - set(current))
    modified = sorted(path for path in current.keys() & previous.keys() if current[path] != previous[path])
    lines = [f"- added: {len(added)}", f"- modified: {len(modified)}", f"- removed: {len(removed)}"]
    lines.extend(f"  - added `{path}`" for path in added[:20])
    lines.extend(f"  - modified `{path}`" for path in modified[:20])
    lines.extend(f"  - removed `{path}`" for path in removed[:20])
    return lines


def write_metadata(records: list[FileRecord], records_dir: Path, day: str, now: datetime) -> None:
    metadata = {
        "created_at": now.isoformat(timespec="seconds"),
        "archive_date": day,
        "source_dir": str(PAPER_DIR),
        "file_count": len(records),
        "manifest": "MANIFEST.sha256",
    }
    target = records_dir / "snapshot_meta.json"
    target.write_text(json.dumps(metadata, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def write_day_readme(day_dir: Path) -> None:
    readme = day_dir / "README.md"
    if readme.exists():
        return
    readme.write_text(
        "# Daily Manuscript Archive\n\n"
        "This folder preserves dated manuscript snapshots without changing the active working files.\n\n"
        "## Layout\n\n"
        "```text\n"
        "snapshots/HHMMSS/source_root/   copied manuscript files and referenced figures\n"
        "snapshots/HHMMSS/records/       manifest and metadata\n"
        "legacy_loose_files/             files that were already loose in this date folder\n"
        "CHANGELOG.md                    snapshot-by-snapshot change summary\n"
        "```\n",
        encoding="utf-8",
    )


def append_changelog(day_dir: Path, stamp: str, changes: list[str], moved: list[str], now: datetime) -> None:
    with (day_dir / "CHANGELOG.md").open("a", encoding="utf-8") as handle:
        handle.write(f"## {now.isoformat(timespec='seconds')} snapshot `{stamp}`\n\n")
        if moved:
            handle.write(f"- organized loose files: {len(moved)}\n")
            handle.writelines(f"  - `{path}`\n" for path in moved[:20])
        handle.write("\n".join(changes))
        handle.write("\n\n")


def create_snapshot(day: str, now: datetime) -> Path:
    stamp = now.strftime("%H%M%S")
    day_dir = PAPER_DIR / day
    day_dir.mkdir(parents=True, exist_ok=True)
    write_day_readme(day_dir)
    moved = organize_existing_root_files(day_dir, stamp)
    snapshot_dir = day_dir / "snapshots" / stamp
    source_root = snapshot_dir / "source_root"
    records_dir = snapshot_dir / "records"
    copy_snapshot(snapshot_paths(), source_root)
    records = build_manifest(source_root)
    write_manifest(records, records_dir)
    write_metadata(records, records_dir, day, now)
    append_changelog(day_dir, stamp, change_summary(previous_manifest(snapshot_dir), records), moved, now)
    return snapshot_dir


def main() -> int:
    args = parse_args()
    now = datetime.now().astimezone()
    day = args.date or now.strftime("%Y-%m-%d")
    snapshot = create_snapshot(day, now)
    print(snapshot)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
