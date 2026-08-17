#!/usr/bin/env python3
"""Generate a progress report from skills matrix and readiness data."""

from __future__ import annotations

import sys
from datetime import date
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed; skipping detailed report.")
    sys.exit(0)

ROOT = Path(__file__).resolve().parent.parent


def main() -> int:
    skills_path = ROOT / "progress" / "skills-matrix.yaml"
    readiness_path = ROOT / "progress" / "interview-readiness.yaml"

    with skills_path.open(encoding="utf-8") as f:
        skills = yaml.safe_load(f)
    with readiness_path.open(encoding="utf-8") as f:
        readiness = yaml.safe_load(f)

    print(f"# Progress Report — {date.today().isoformat()}\n")
    print("## Skills Matrix\n")
    for domain, info in skills.get("domains", {}).items():
        current = info.get("current_level", 0)
        target = info.get("target_level", 5)
        print(f"- **{domain}**: {current}/{target} (confidence: {info.get('confidence', 'unknown')})")

    print(f"\n## Interview Readiness: {readiness.get('overall_readiness_score', 0)}%\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
