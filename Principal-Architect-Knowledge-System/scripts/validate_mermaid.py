#!/usr/bin/env python3
"""Validate Mermaid diagram blocks in Markdown files."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCAN_DIRS = ["docs", "case-studies", "labs", "diagrams/mermaid"]

FENCE_RE = re.compile(r"```mermaid\s*\n(.*?)```", re.DOTALL)

# Common Mermaid syntax issues
FORBIDDEN_PATTERNS = [
    (re.compile(r"\t"), "tabs inside mermaid block (use spaces)"),
]


def validate_block(content: str, source: Path, index: int) -> list[str]:
    errors: list[str] = []
    stripped = content.strip()
    if not stripped:
        errors.append(f"{source}: diagram {index} is empty")
        return errors

    for pattern, msg in FORBIDDEN_PATTERNS:
        if pattern.search(content):
            errors.append(f"{source}: diagram {index} — {msg}")

    # Unbalanced brackets (rough check — skip sequence diagram notes with intervals)
    if "sequenceDiagram" not in content:
        for open_c, close_c, name in [("{", "}", "braces"), ("[", "]", "brackets")]:
            if content.count(open_c) != content.count(close_c):
                errors.append(f"{source}: diagram {index} — unbalanced {name}")

    # MDX-problematic alone on a line
    if re.search(r"^\s*<[^>]+>\s*$", content, re.MULTILINE):
        errors.append(f"{source}: diagram {index} — raw HTML tags may break MDX")

    return errors


def audit_file(path: Path) -> tuple[int, list[str]]:
    text = path.read_text(encoding="utf-8")
    if path.suffix == ".mmd":
        blocks = [text]
    else:
        blocks = FENCE_RE.findall(text)
    errors: list[str] = []
    for i, block in enumerate(blocks, 1):
        errors.extend(validate_block(block, path.relative_to(ROOT), i))
    return len(blocks), errors


def min_required(path: Path) -> int:
    rel = str(path.relative_to(ROOT))
    if rel.endswith(".mmd"):
        return 1
    if rel.endswith("overview.md"):
        return 1
    if rel.startswith("case-studies/"):
        return 2
    if "/28-company-specific-preparation/" in rel:
        return 2
    if "/29-behavioral-and-leadership/" in rel or "/30-mock-interviews/" in rel:
        return 2
    if rel.startswith("labs/") and "architecture.md" in rel:
        return 2
    if rel.startswith("labs/") and "requirements.md" in rel:
        return 0
    if rel.startswith("labs/"):
        return 0
    if rel.startswith("docs/00-start-here/") and rel.endswith("welcome.md"):
        return 1
    if rel.startswith("docs/00-start-here/"):
        return 0
    if rel.startswith("docs/31-reference/"):
        return 1
    if rel.startswith("docs/32-real-world-scenarios/"):
        return 1
    if rel.startswith("docs/") and not rel.endswith("overview.md"):
        return 3
    return 1


def main() -> int:
    errors: list[str] = []
    warnings: list[str] = []
    total_blocks = 0
    files_with_diagrams = 0

    paths: list[Path] = []
    for scan in SCAN_DIRS:
        base = ROOT / scan
        if base.is_file() and base.suffix in {".md", ".mmd"}:
            paths.append(base)
        elif base.is_dir():
            paths.extend(base.rglob("*.md"))
            paths.extend(base.rglob("*.mmd"))

    for path in sorted(set(paths)):
        if "node_modules" in path.parts:
            continue
        count, block_errors = audit_file(path)
        total_blocks += count
        if count > 0:
            files_with_diagrams += 1
        errors.extend(block_errors)

        required = min_required(path)
        if count < required:
            warnings.append(
                f"{path.relative_to(ROOT)}: {count}/{required} diagrams (below minimum)"
            )

    print("Mermaid Diagram Report")
    print("=" * 50)
    print(f"Files scanned: {len(paths)}")
    print(f"Files with diagrams: {files_with_diagrams}")
    print(f"Total diagram blocks: {total_blocks}")
    print(f"Syntax errors: {len(errors)}")
    print(f"Coverage warnings: {len(warnings)}")

    if warnings:
        print("\nCoverage gaps:")
        for w in warnings[:30]:
            print(f"  - {w}")
        if len(warnings) > 30:
            print(f"  ... and {len(warnings) - 30} more")

    if errors:
        print("\nSyntax errors:")
        for e in errors[:20]:
            print(f"  - {e}")
        return 1

    if warnings:
        return 2  # coverage gaps only

    print("\nAll diagrams pass validation.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
