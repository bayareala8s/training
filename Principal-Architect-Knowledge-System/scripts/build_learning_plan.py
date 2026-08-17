#!/usr/bin/env python3
"""Generate a study plan summary from progress YAML files."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed; skipping detailed report.")
    sys.exit(0)

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    plan_path = ROOT / "progress" / "study-plan.yaml"
    with plan_path.open(encoding="utf-8") as f:
        data = yaml.safe_load(f)

    sprint = next((p for p in data.get("plans", []) if p["id"] == "12-week-sprint"), None)
    if not sprint:
        print("No 12-week sprint plan found.")
        return 1

    print(f"# {sprint['name']}\n")
    print(f"{sprint['description']}\n")
    for week in sprint.get("weeks", []):
        topics = ", ".join(week.get("topics", []))
        print(f"Week {week['week']}: {topics}")

    return 0


if __name__ == "__main__":
    sys.exit(main())
