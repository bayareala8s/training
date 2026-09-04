#!/usr/bin/env python3
"""Stage 12: all 72 diagrams have source, SVG, PNG, alt text."""
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    issues: list[str] = []
    data = json.loads((ROOT / "COURSE_MANIFEST.json").read_text())
    diagrams = data.get("diagrams", [])
    if len(diagrams) != 72:
        issues.append(f"manifest diagrams {len(diagrams)} expected 72")
    ids = [d["id"] for d in diagrams]
    if ids != [f"AEJE-D-{i:03d}" for i in range(1, 73)]:
        issues.append("diagram ids are not AEJE-D-001..072 in order")
    for d in diagrams:
        for key in ("source", "svg", "png", "altText"):
            path = ROOT / d[key]
            if not path.exists():
                issues.append(f"missing {d[key]}")
    if not (ROOT / "diagrams/README.md").exists():
        issues.append("missing diagrams/README.md")
    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS Stage 12 diagram library (72)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
