#!/usr/bin/env python3
"""Escape MDX-problematic syntax in Markdown chapters."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"

CODE_FENCE = re.compile(r"^```.*$")


def escape_mdx_specials_in_prose(line: str) -> str:
    """Escape curly braces and less-than outside inline code spans."""
    if line.strip().startswith("```"):
        return line
    if "$$" in line:
        return line

    parts: list[str] = []
    i = 0
    while i < len(line):
        if line[i] == "`":
            j = line.find("`", i + 1)
            if j == -1:
                parts.append(line[i:])
                break
            parts.append(line[i : j + 1])
            i = j + 1
            continue
        if line[i] == "{":
            parts.append("\\{")
            i += 1
            continue
        if line[i] == "}":
            parts.append("\\}")
            i += 1
            continue
        if line[i] == "<" and i + 1 < len(line) and (
            line[i + 1].isdigit() or line[i + 1] in "/{"
        ):
            parts.append("&lt;")
            i += 1
            continue
        parts.append(line[i])
        i += 1
    return "".join(parts)


def fix_math_lines(line: str) -> str:
    stripped = line.strip()
    if stripped.startswith("$$") and stripped.endswith("$$") and len(stripped) > 4:
        inner = stripped[2:-2].strip()
        return f"`{inner}`"
    return line


def process_file(path: Path) -> bool:
    lines = path.read_text(encoding="utf-8").splitlines()
    in_fence = False
    changed = False
    out: list[str] = []

    for line in lines:
        if line.strip().startswith("```"):
            in_fence = not in_fence
            out.append(line)
            continue
        if in_fence:
            out.append(line)
            continue
        new_line = fix_math_lines(line)
        new_line = escape_mdx_specials_in_prose(new_line)
        if new_line != line:
            changed = True
        out.append(new_line)

    if changed:
        path.write_text("\n".join(out) + "\n", encoding="utf-8")
    return changed


def main() -> int:
    count = 0
    for path in sorted(DOCS.rglob("*.md")):
        if process_file(path):
            count += 1
            print(f"Fixed: {path.relative_to(ROOT)}")
    print(f"Updated {count} files.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
