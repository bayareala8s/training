#!/usr/bin/env python3
"""Merge interview-bank/domains/*.json into interview-bank/questions.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOM = ROOT / "interview-bank" / "domains"
OUT = ROOT / "interview-bank" / "questions.json"


def main() -> None:
    items: list[dict] = []
    for path in sorted(DOM.glob("*.json")):
        data = json.loads(path.read_text())
        chunk = data if isinstance(data, list) else data.get("questions", [])
        items.extend(chunk)
    items.sort(key=lambda q: q["id"])
    OUT.write_text(json.dumps(items, indent=2, ensure_ascii=False) + "\n")
    print(f"wrote {len(items)} questions to {OUT.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
