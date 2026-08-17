#!/usr/bin/env python3
"""Scaffold a new chapter from the chapter template."""

from __future__ import annotations

import argparse
import re
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TEMPLATE = ROOT / "templates" / "chapter-template.md"


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"[-\s]+", "-", text).strip("-")


def main() -> int:
    parser = argparse.ArgumentParser(description="Create a new chapter from template")
    parser.add_argument("title", help="Chapter title")
    parser.add_argument("domain_dir", help="Target directory under docs/, e.g. 04-distributed-systems-foundations")
    parser.add_argument("--domain", default="general", help="Domain metadata field")
    args = parser.parse_args()

    chapter_id = slugify(args.title)
    target_dir = ROOT / "docs" / args.domain_dir
    target_dir.mkdir(parents=True, exist_ok=True)
    target = target_dir / f"{chapter_id}.md"

    if target.exists():
        print(f"Error: {target} already exists")
        return 1

    template = TEMPLATE.read_text(encoding="utf-8")
    content = template.replace("chapter-id", chapter_id)
    content = content.replace("Chapter Title", args.title)
    content = content.replace("domain-name", args.domain)
    content = content.replace("YYYY-MM-DD", date.today().isoformat())

    target.write_text(content, encoding="utf-8")
    print(f"Created {target.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
