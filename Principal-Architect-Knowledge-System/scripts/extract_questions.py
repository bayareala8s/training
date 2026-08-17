#!/usr/bin/env python3
"""Extract interview questions from Markdown chapters."""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUTPUT = ROOT / "interview" / "question-bank" / "extracted.md"

SECTION_RE = re.compile(r"^##\s+21\.\s+Interview Questions\s*$", re.MULTILINE)
QUESTION_RE = re.compile(r"^[-*]\s+(.+)$", re.MULTILINE)


def extract_from_file(path: Path) -> list[str]:
    content = path.read_text(encoding="utf-8")
    match = SECTION_RE.search(content)
    if not match:
        return []

    rest = content[match.end() :]
    next_section = re.search(r"^##\s+\d+\.", rest, re.MULTILINE)
    section_text = rest[: next_section.start()] if next_section else rest

    return [q.strip() for q in QUESTION_RE.findall(section_text) if len(q.strip()) > 10]


def main() -> int:
    questions: list[str] = []
    for path in sorted(DOCS.rglob("*.md")):
        questions.extend(extract_from_file(path))

    OUTPUT.parent.mkdir(parents=True, exist_ok=True)
    lines = ["# Extracted Interview Questions\n", f"Total: {len(questions)}\n"]
    for i, q in enumerate(questions, 1):
        lines.append(f"{i}. {q}\n")

    OUTPUT.write_text("".join(lines), encoding="utf-8")
    print(f"Extracted {len(questions)} questions to {OUTPUT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
