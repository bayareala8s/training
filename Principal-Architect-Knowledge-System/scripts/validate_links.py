#!/usr/bin/env python3
"""Validate internal Markdown links in documentation."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["docs", "case-studies", "interview", "README.md", "templates"]

LINK_RE = re.compile(r"\[([^\]]*)\]\(([^)]+)\)")


def is_external(url: str) -> bool:
    return url.startswith(("http://", "https://", "mailto:", "#"))


def resolve_link(source: Path, target: str) -> Path | None:
    if is_external(target):
        return None
    if target.startswith("/"):
        return None
    clean = target.split("#")[0]
    if not clean:
        return None
    if clean.endswith(".md"):
        resolved = (source.parent / clean).resolve()
    else:
        candidate_md = (source.parent / f"{clean}.md").resolve()
        candidate_plain = (source.parent / clean).resolve()
        if candidate_plain.exists():
            resolved = candidate_plain
        else:
            resolved = candidate_md
    return resolved


def main() -> int:
    errors: list[str] = []
    files: list[Path] = []

    for item in SCAN_DIRS:
        path = ROOT / item
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(path.rglob("*.md"))

    for source in sorted(set(files)):
        content = source.read_text(encoding="utf-8")
        for _text, url in LINK_RE.findall(content):
            resolved = resolve_link(source, url)
            if resolved is None:
                continue
            if not resolved.exists():
                try:
                    resolved.relative_to(ROOT)
                except ValueError:
                    continue
                errors.append(f"{source.relative_to(ROOT)}: broken link -> {url}")

    if errors:
        print("Link validation failed:\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("Link validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
