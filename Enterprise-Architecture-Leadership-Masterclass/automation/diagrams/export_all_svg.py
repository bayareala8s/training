#!/usr/bin/env python3
"""Export all Mermaid diagram sources to real SVG via local mmdc."""
from __future__ import annotations

import argparse
import concurrent.futures
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DIAGRAMS = ROOT / "diagrams"
MMDC = ROOT / "node_modules" / ".bin" / "mmdc"
LOG_DIR = DIAGRAMS / "_export-logs"


def mmd_to_svg_path(mmd: Path) -> Path:
    rel = mmd.relative_to(DIAGRAMS)
    parts = list(rel.parts)
    # .../mermaid/category/file.mmd -> .../svg/category/file.svg
    parts = ["svg" if p == "mermaid" else p for p in parts]
    out = DIAGRAMS.joinpath(*parts).with_suffix(".svg")
    return out


def mmd_to_png_path(mmd: Path) -> Path:
    rel = mmd.relative_to(DIAGRAMS)
    parts = ["png" if p == "mermaid" else p for p in rel.parts]
    return DIAGRAMS.joinpath(*parts).with_suffix(".png")


def export_one(mmd: Path, do_png: bool) -> tuple[str, bool, str]:
    rel = str(mmd.relative_to(DIAGRAMS))
    svg = mmd_to_svg_path(mmd)
    svg.parent.mkdir(parents=True, exist_ok=True)
    err_file = LOG_DIR / f"{mmd.stem}.err"
    try:
        r = subprocess.run(
            [str(MMDC), "-i", str(mmd), "-o", str(svg), "-b", "white"],
            capture_output=True,
            text=True,
            timeout=120,
        )
        if r.returncode != 0:
            err_file.write_text((r.stderr or r.stdout or "mmdc failed")[:4000])
            return rel, False, "mmdc_failed"
        text = svg.read_text(encoding="utf-8", errors="ignore")
        # Placeholder cards lack rendered chart groups / paths
        if "<g" not in text and "path" not in text.lower() and svg.stat().st_size < 2500:
            return rel, False, "placeholder_or_tiny"
        if do_png:
            png = mmd_to_png_path(mmd)
            png.parent.mkdir(parents=True, exist_ok=True)
            subprocess.run(
                [str(MMDC), "-i", str(mmd), "-o", str(png), "-b", "white", "-s", "2"],
                capture_output=True,
                text=True,
                timeout=120,
            )
        return rel, True, "ok"
    except Exception as e:
        err_file.write_text(str(e))
        return rel, False, str(e)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--jobs", type=int, default=4)
    ap.add_argument("--png", action="store_true")
    ap.add_argument("--limit", type=int, default=0, help="Export only first N (debug)")
    args = ap.parse_args()

    if not MMDC.exists():
        print("Missing node_modules/.bin/mmdc — run: npm install @mermaid-js/mermaid-cli@11.4.2", file=sys.stderr)
        return 1

    LOG_DIR.mkdir(parents=True, exist_ok=True)
    files = sorted(DIAGRAMS.glob("**/mermaid/**/*.mmd"))
    if args.limit:
        files = files[: args.limit]
    print(f"Exporting {len(files)} diagrams with {args.jobs} workers…")

    ok, fail = [], []
    with concurrent.futures.ThreadPoolExecutor(max_workers=args.jobs) as ex:
        futs = {ex.submit(export_one, f, args.png): f for f in files}
        done = 0
        for fut in concurrent.futures.as_completed(futs):
            rel, success, reason = fut.result()
            done += 1
            if success:
                ok.append(rel)
            else:
                fail.append(f"{rel}\t{reason}")
            if done % 20 == 0 or done == len(files):
                print(f"  progress {done}/{len(files)}  ok={len(ok)} fail={len(fail)}")

    (LOG_DIR / "success.txt").write_text("\n".join(sorted(ok)) + ("\n" if ok else ""))
    (LOG_DIR / "failures.txt").write_text("\n".join(sorted(fail)) + ("\n" if fail else ""))
    print(f"Done. success={len(ok)} fail={len(fail)}")
    if fail:
        print("Failures (first 40):")
        for line in fail[:40]:
            print(" ", line)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
