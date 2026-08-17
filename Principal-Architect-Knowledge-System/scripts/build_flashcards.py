#!/usr/bin/env python3
"""Generate flashcards from curriculum chapter content."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
OUTPUT_DIR = ROOT / "flashcards"
OUTPUT_JSON = OUTPUT_DIR / "flashcards.json"
OUTPUT_CSV = OUTPUT_DIR / "flashcards.csv"

FRONTMATTER_RE = re.compile(r"^---\s*\n.*?\n---\s*\n", re.DOTALL)
TERM_TABLE_RE = re.compile(
    r"##\s+5\.\s+Essential Terminology\s*\n\n(.*?)(?=\n##\s|\Z)",
    re.DOTALL,
)
TABLE_ROW_RE = re.compile(r"^\|\s*\*\*(.+?)\*\*\s*\|\s*(.+?)\s*\|", re.MULTILINE)
EXEC_SUMMARY_RE = re.compile(
    r"##\s+1\.\s+Executive Summary\s*\n\n(.+?)(?=\n##\s|\Z)",
    re.DOTALL,
)


def parse_frontmatter_title(content: str) -> str:
    match = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
    if not match:
        return ""
    for line in match.group(1).splitlines():
        if line.startswith("title:"):
            return line.split(":", 1)[1].strip()
    return ""


def extract_term_cards(content: str, chapter_id: str, title: str) -> list[dict]:
    cards: list[dict] = []
    section = TERM_TABLE_RE.search(content)
    if not section:
        return cards
    for term, definition in TABLE_ROW_RE.findall(section.group(1)):
        term = term.strip()
        definition = definition.strip()
        if term.lower() in ("term", "definition"):
            continue
        cards.append(
            {
                "id": f"{chapter_id}-term-{re.sub(r'[^a-z0-9]+', '-', term.lower())}",
                "chapter_id": chapter_id,
                "chapter_title": title,
                "card_type": "terminology",
                "front": f"What is **{term}**?",
                "back": definition,
                "tags": [chapter_id, "terminology"],
            }
        )
    return cards


def extract_summary_cards(content: str, chapter_id: str, title: str) -> list[dict]:
    cards: list[dict] = []
    section = EXEC_SUMMARY_RE.search(content)
    if not section:
        return cards
    summary = section.group(1).strip()
    first_para = summary.split("\n\n")[0].strip()
    if len(first_para) < 80:
        return cards
    cards.append(
        {
            "id": f"{chapter_id}-summary",
            "chapter_id": chapter_id,
            "chapter_title": title,
            "card_type": "summary",
            "front": f"Summarize the core idea of **{title}**.",
            "back": first_para[:500],
            "tags": [chapter_id, "summary"],
        }
    )
    return cards


def build_flashcards() -> list[dict]:
    cards: list[dict] = []
    for path in sorted(DOCS.rglob("*.md")):
        if path.name == "overview.md":
            continue
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---"):
            continue
        chapter_id = ""
        fm = re.match(r"^---\s*\n(.*?)\n---", content, re.DOTALL)
        if fm:
            for line in fm.group(1).splitlines():
                if line.startswith("id:"):
                    chapter_id = line.split(":", 1)[1].strip()
        if not chapter_id:
            chapter_id = path.stem
        title = parse_frontmatter_title(content) or chapter_id
        body = FRONTMATTER_RE.sub("", content, count=1)
        cards.extend(extract_term_cards(body, chapter_id, title))
        cards.extend(extract_summary_cards(body, chapter_id, title))
    return cards


def write_outputs(cards: list[dict]) -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    payload = {
        "version": 1,
        "total_cards": len(cards),
        "source": "docs/**/*.md",
        "cards": cards,
    }
    OUTPUT_JSON.write_text(json.dumps(payload, indent=2), encoding="utf-8")
    lines = ["front,back,tags"]
    for card in cards:
        front = card["front"].replace('"', '""')
        back = card["back"].replace('"', '""').replace("\n", " ")
        tags = "|".join(card["tags"])
        lines.append(f'"{front}","{back}","{tags}"')
    OUTPUT_CSV.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    cards = build_flashcards()
    if not cards:
        print("No flashcards extracted — check chapter templates.", file=sys.stderr)
        return 1
    write_outputs(cards)
    print(f"Generated {len(cards)} flashcards")
    print(f"  JSON: {OUTPUT_JSON}")
    print(f"  CSV:  {OUTPUT_CSV}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
