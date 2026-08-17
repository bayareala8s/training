#!/usr/bin/env python3
"""Export Mermaid blocks from docs/diagrams/*.md to png/ and svg/."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
DIAGRAMS = REPO_ROOT / "docs" / "diagrams"
BUILD = DIAGRAMS / ".build"
PNG_DIR = DIAGRAMS / "png"
SVG_DIR = DIAGRAMS / "svg"
CONFIG = DIAGRAMS / "mermaid-config.json"
MERMAID_CLI = ["npx", "-y", "@mermaid-js/mermaid-cli@11.4.0", "mmdc"]


def extract_mermaid_blocks(md_path: Path) -> list[str]:
    text = md_path.read_text(encoding="utf-8")
    return re.findall(r"```mermaid\s*\n(.*?)```", text, re.DOTALL)


def run_mmdc(input_mmd: Path, output_path: Path) -> None:
    cmd = [
        *MERMAID_CLI,
        "-i",
        str(input_mmd),
        "-o",
        str(output_path),
        "-c",
        str(CONFIG),
        "-b",
        "transparent",
    ]
    if output_path.suffix == ".png":
        cmd.extend(["-w", "1920"])

    result = subprocess.run(
        cmd,
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        sys.stderr.write(result.stderr or result.stdout)
        raise RuntimeError(f"mmdc failed for {output_path.name}")


def main() -> int:
    if not CONFIG.is_file():
        print(f"Missing config: {CONFIG}", file=sys.stderr)
        return 1

    BUILD.mkdir(parents=True, exist_ok=True)
    PNG_DIR.mkdir(parents=True, exist_ok=True)
    SVG_DIR.mkdir(parents=True, exist_ok=True)

    md_files = sorted(DIAGRAMS.glob("[0-9][0-9]-*.md"))
    if not md_files:
        print("No numbered diagram markdown files found.", file=sys.stderr)
        return 1

    exported: list[str] = []
    failed: list[str] = []

    for md_path in md_files:
        stem = md_path.stem
        blocks = extract_mermaid_blocks(md_path)
        if not blocks:
            print(f"warning: no mermaid blocks in {md_path.name}", file=sys.stderr)
            continue

        for index, block in enumerate(blocks, start=1):
            suffix = f"-{index}" if len(blocks) > 1 else ""
            base = f"{stem}{suffix}"
            mmd_path = BUILD / f"{base}.mmd"
            mmd_path.write_text(block.strip() + "\n", encoding="utf-8")

            print(f"Exporting {base} ...")
            try:
                run_mmdc(mmd_path, PNG_DIR / f"{base}.png")
                run_mmdc(mmd_path, SVG_DIR / f"{base}.svg")
            except RuntimeError as exc:
                failed.append(base)
                print(f"  FAILED: {exc}", file=sys.stderr)
            else:
                exported.append(base)

    print(f"\nDone. Exported {len(exported)} diagram(s).")
    print(f"  PNG: {PNG_DIR.relative_to(REPO_ROOT)}/")
    print(f"  SVG: {SVG_DIR.relative_to(REPO_ROOT)}/")
    if failed:
        print(f"\nFailed ({len(failed)}): {', '.join(failed)}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
