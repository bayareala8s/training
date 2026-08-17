#!/usr/bin/env python3
"""Validate YAML frontmatter in Markdown files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["docs", "case-studies", "interview"]
REQUIRED_FIELDS = {"id", "title"}
OPTIONAL_BUT_RECOMMENDED = {"domain", "status", "tags"}

FRONTMATTER_RE = re.compile(r"^---\s*\n(.*?)\n---\s*\n", re.DOTALL)


def parse_simple_yaml(text: str) -> dict[str, str]:
    """Minimal YAML parser for frontmatter key: value lines."""
    result: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, value = line.partition(":")
        result[key.strip()] = value.strip()
    return result


def validate_file(path: Path) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")

    if path.name == "overview.md":
        return errors

    if not content.startswith("---"):
        if path.parts[-2].startswith("00-") or "start-here" in str(path):
            return errors
        errors.append(f"{path}: missing YAML frontmatter")
        return errors

    match = FRONTMATTER_RE.match(content)
    if not match:
        errors.append(f"{path}: malformed frontmatter block")
        return errors

    meta = parse_simple_yaml(match.group(1))
    for field in REQUIRED_FIELDS:
        if field not in meta:
            errors.append(f"{path}: missing required field '{field}'")

    return errors


def main() -> int:
    errors: list[str] = []
    for scan_dir in SCAN_DIRS:
        base = ROOT / scan_dir
        if not base.exists():
            continue
        for path in sorted(base.rglob("*.md")):
            if path.name.startswith("."):
                continue
            errors.extend(validate_file(path))

    if errors:
        print("Frontmatter validation failed:\n")
        for err in errors:
            print(f"  - {err}")
        return 1

    print("Frontmatter validation passed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
