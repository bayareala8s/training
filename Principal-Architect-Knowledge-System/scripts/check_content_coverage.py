#!/usr/bin/env python3
"""Report content coverage against curriculum plan."""

from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    yaml = None  # type: ignore

ROOT = Path(__file__).resolve().parent.parent


def load_curriculum() -> dict:
    path = ROOT / "progress" / "curriculum.yaml"
    if yaml is None:
        return {"domains": []}
    with path.open(encoding="utf-8") as f:
        return yaml.safe_load(f) or {}


def count_chapters(domain_path: Path) -> int:
    if not domain_path.exists():
        return 0
    return sum(
        1
        for p in domain_path.glob("*.md")
        if p.name != "overview.md" and p.stat().st_size > 500
    )


def main() -> int:
    curriculum = load_curriculum()
    domains = curriculum.get("domains", [])

    print("Content Coverage Report")
    print("=" * 50)

    total_planned = 0
    total_complete = 0

    for domain in domains:
        domain_id = domain.get("id", "unknown")
        rel_path = domain.get("path", "")
        domain_path = ROOT / rel_path
        chapters = domain.get("chapters", [])
        planned = len(chapters) if chapters else 1
        written = count_chapters(domain_path)
        status = domain.get("status", "unknown")

        total_planned += planned
        total_complete += min(written, planned)

        print(f"  {domain_id}: {written} chapters written, {planned} planned [{status}]")

    print("=" * 50)
    pct = (total_complete / total_planned * 100) if total_planned else 0
    print(f"Overall: {total_complete}/{total_planned} ({pct:.1f}%)")

  # Coverage check is informational in Phase 0
    print("\nCoverage check completed (informational).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
