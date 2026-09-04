#!/usr/bin/env python3
"""Stage 13: curated PAKS paths exist in manifest, index, lessons, and optional local tree."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
INDEX = ROOT / "PAKS_LINKS.md"
MODULES = ROOT / "course" / "modules"
PATH_RE = re.compile(r"docs/[0-9]{2}[-a-z0-9]+(?:/[a-z0-9][-a-z0-9]*)*\.md")
CANDIDATES = [
    Path("/Users/hbhadra/Downloads/Principal-Architect-Knowledge-System/Principal-Architect-Knowledge-System"),
    Path("/Users/hbhadra/Downloads/Principal-Architect-Knowledge-System"),
]


def related_tail(text: str) -> str | None:
    matches = list(re.finditer(r"^## Related PAKS", text, re.MULTILINE))
    if not matches:
        return None
    return text[matches[-1].start() :]


def main() -> int:
    issues: list[str] = []
    data = json.loads((ROOT / "COURSE_MANIFEST.json").read_text())
    if not INDEX.exists():
        print("FAIL")
        print("- missing PAKS_LINKS.md")
        return 1
    index = INDEX.read_text()
    if "optional" not in index.lower():
        issues.append("PAKS_LINKS.md must say links are optional")
    if "paks.bayareala8s.com" not in index:
        issues.append("PAKS_LINKS.md must name paks.bayareala8s.com")

    declared: set[str] = set()
    by_slug: dict[str, set[str]] = {}
    for mod in data["modules"]:
        paths = set(mod.get("paksDeepDives") or [])
        if not paths:
            issues.append(f"{mod['id']} has no paksDeepDives")
        declared.update(paths)
        by_slug[mod["slug"]] = paths
        for rel in paths:
            if rel not in index:
                issues.append(f"{rel} not listed in PAKS_LINKS.md")

    paks_root = next((p for p in CANDIDATES if (p / "docs").is_dir()), None)
    if paks_root:
        for rel in sorted(declared):
            if not (paks_root / rel).exists():
                issues.append(f"missing on disk: {rel}")
    else:
        print("note: local PAKS tree not found; skipped file existence")

    lesson_count = 0
    for lesson in sorted(MODULES.glob("*/lessons/*.md")):
        lesson_count += 1
        slug = lesson.parent.parent.name
        allowed = by_slug.get(slug, set())
        text = lesson.read_text()
        tail = related_tail(text)
        rel = lesson.relative_to(ROOT)
        if tail is None:
            issues.append(f"{rel} missing Related PAKS heading")
            continue
        cited = set(PATH_RE.findall(tail))
        if not cited:
            issues.append(f"{rel} Related PAKS cites no docs/*.md path")
            continue
        extra = cited - declared
        if extra:
            issues.append(f"{rel} cites uncurated path(s): {sorted(extra)}")
        if allowed and not (cited & allowed):
            issues.append(f"{rel} cites none of its module paksDeepDives")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print(
        f"PASS Stage 13 PAKS links ({len(declared)} unique paths, {lesson_count} lessons)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
