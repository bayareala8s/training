#!/usr/bin/env python3
"""Fix internal doc links to include /docs/ prefix for Docusaurus."""

from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

LINK_RE = re.compile(r"\[([^\]]*)\]\((/[^)]+)\)")


def fix_link(url: str) -> str:
    if url.startswith(("/docs/", "http://", "https://", "mailto:", "#")):
        return url
    return f"/docs{url}"


def fix_links(text: str) -> str:
    def repl(match: re.Match[str]) -> str:
        label, url = match.group(1), match.group(2)
        return f"[{label}]({fix_link(url)})"

    return LINK_RE.sub(repl, text)


def main() -> None:
    count = 0
    for path in DOCS.rglob("*.md"):
        original = path.read_text(encoding="utf-8")
        updated = fix_links(original)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            count += 1
    print(f"Fixed links in {count} files.")


if __name__ == "__main__":
    main()
