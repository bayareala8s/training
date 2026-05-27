#!/usr/bin/env python3
"""Extract Mermaid blocks from docs/diagrams/week-*.md and export PNG + SVG via mmdc."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


def slugify(text: str) -> str:
    text = text.lower()
    text = re.sub(r"^##\s*diagram\s*\d+\s*—\s*", "", text, flags=re.I)
    text = re.sub(r"[^a-z0-9]+", "-", text).strip("-")
    return text[:80] or "diagram"


def extract_diagrams(md_path: Path) -> list[tuple[str, str]]:
    """Return list of (name_slug, mermaid_source)."""
    content = md_path.read_text(encoding="utf-8")
    week = md_path.stem  # week-01
    results: list[tuple[str, str]] = []
    diagram_idx = 0
    current_title = "diagram"
    in_mermaid = False
    buffer: list[str] = []

    for line in content.splitlines():
        if line.startswith("## "):
            if in_mermaid and buffer:
                diagram_idx += 1
                name = f"{week}-diagram-{diagram_idx:02d}-{slugify(current_title)}"
                results.append((name, "\n".join(buffer)))
                buffer = []
                in_mermaid = False
            current_title = line[3:].strip()
        if line.strip() == "```mermaid":
            in_mermaid = True
            buffer = []
            continue
        if in_mermaid and line.strip() == "```":
            diagram_idx += 1
            name = f"{week}-diagram-{diagram_idx:02d}-{slugify(current_title)}"
            results.append((name, "\n".join(buffer)))
            buffer = []
            in_mermaid = False
            continue
        if in_mermaid:
            buffer.append(line)

    return results


def run_mmdc(mmd: Path, out: Path, fmt: str) -> None:
    out.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "npx",
            "--yes",
            "@mermaid-js/mermaid-cli@11.4.0",
            "-i",
            str(mmd),
            "-o",
            str(out),
            "-b",
            "white",
        ],
        check=True,
        capture_output=True,
        text=True,
    )


def main() -> None:
    if len(sys.argv) != 4:
        print("Usage: export_mermaid_images.py DIAG_DIR PNG_DIR SVG_DIR", file=sys.stderr)
        sys.exit(1)

    diag_dir = Path(sys.argv[1])
    png_dir = Path(sys.argv[2])
    svg_dir = Path(sys.argv[3])
    tmp = diag_dir / ".export-tmp"
    tmp.mkdir(parents=True, exist_ok=True)

    md_files = sorted(diag_dir.glob("week-*.md"))
    total = 0
    for md in md_files:
        diagrams = extract_diagrams(md)
        for name, source in diagrams:
            mmd_file = tmp / f"{name}.mmd"
            mmd_file.write_text(source + "\n", encoding="utf-8")
            print(f"  mermaid → {name}")
            try:
                run_mmdc(mmd_file, png_dir / f"{name}.png", "png")
                run_mmdc(mmd_file, svg_dir / f"{name}.svg", "svg")
                total += 1
            except subprocess.CalledProcessError as exc:
                print(f"WARN: failed {name}: {exc.stderr or exc}", file=sys.stderr)

    print(f"Mermaid exports: {total} diagrams")


if __name__ == "__main__":
    main()
