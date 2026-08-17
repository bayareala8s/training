#!/usr/bin/env python3
"""Revert over-escaping introduced for MDX compatibility."""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"


def unescape_file(path: Path) -> bool:
    text = path.read_text(encoding="utf-8")
    new = (
        text.replace("\\{", "{")
        .replace("\\}", "}")
        .replace("&lt;", "<")
    )
    if new != text:
        path.write_text(new, encoding="utf-8")
        return True
    return False


def main() -> None:
    count = 0
    for path in DOCS.rglob("*.md"):
        if unescape_file(path):
            count += 1
            print(f"Reverted: {path.relative_to(ROOT)}")
    print(f"Reverted {count} files.")


if __name__ == "__main__":
    main()
