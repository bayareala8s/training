#!/usr/bin/env python3
"""Validate baylearn-seed JSON files parse and meet basic shape checks."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SEED = ROOT / "baylearn-seed"

REQUIRED = [
    "course.json",
    "modules.json",
    "lessons.json",
    "assignments.json",
    "rubrics.json",
    "materials.json",
    "quizzes.json",
    "cohort.json",
]

COURSE_REQUIRED_KEYS = {
    "courseId",
    "slug",
    "title",
    "subtitle",
    "category",
    "level",
    "deliveryMode",
    "durationWeeks",
    "estimatedHours",
    "priceCents",
    "status",
    "certificateName",
}


def load(path: Path):
    with path.open(encoding="utf-8") as f:
        return json.load(f)


def main() -> int:
    errors: list[str] = []
    print(f"==> validate-json ({SEED})")

    for name in REQUIRED:
        path = SEED / name
        if not path.exists():
            errors.append(f"missing {path}")
            continue
        try:
            data = load(path)
        except json.JSONDecodeError as exc:
            errors.append(f"{name}: JSON parse error: {exc}")
            continue
        print(f"  PASS: {name} parses")

        if name == "course.json":
            missing = COURSE_REQUIRED_KEYS - set(data.keys())
            if missing:
                errors.append(f"course.json missing keys: {sorted(missing)}")
            if data.get("courseId") != "enterprise-architecture-leadership-masterclass":
                errors.append("course.json courseId mismatch")
            if data.get("priceCents") != 249900:
                errors.append("course.json priceCents expected 249900")
            if data.get("status") != "PUBLISHED":
                errors.append("course.json status expected PUBLISHED")

        if name == "modules.json":
            if not isinstance(data, list) or len(data) != 10:
                errors.append(f"modules.json expected 10 modules, got {type(data).__name__} len={getattr(data, '__len__', lambda: '?')()}")
            else:
                weeks = sorted(m.get("week") for m in data)
                if weeks != list(range(1, 11)):
                    errors.append(f"modules.json weeks unexpected: {weeks}")

        if name == "lessons.json":
            if not isinstance(data, list) or len(data) != 40:
                errors.append(f"lessons.json expected 40 lessons, got {len(data) if isinstance(data, list) else data}")

        if name == "assignments.json":
            if not isinstance(data, list) or len(data) != 10:
                errors.append(f"assignments.json expected 10 assignments, got {len(data) if isinstance(data, list) else data}")

        if name == "quizzes.json":
            if not isinstance(data, list) or len(data) != 10:
                errors.append(f"quizzes.json expected 10 quizzes, got {len(data) if isinstance(data, list) else data}")

        if name == "cohort.json":
            sessions = data.get("sessions") if isinstance(data, dict) else None
            if not isinstance(sessions, list) or len(sessions) != 10:
                errors.append("cohort.json expected 10 sessions")
            else:
                if sessions[0].get("date") != "2026-09-08":
                    errors.append("cohort.json first session date expected 2026-09-08")
                days = {s.get("dayOfWeek") for s in sessions}
                if days != {"Tuesday"}:
                    errors.append(f"cohort.json sessions expected Tuesdays, got {days}")
            office = data.get("officeHours") if isinstance(data, dict) else None
            if not isinstance(office, list) or len(office) != 10:
                errors.append("cohort.json expected 10 officeHours")
            elif {o.get("dayOfWeek") for o in office} != {"Wednesday"}:
                errors.append("cohort.json officeHours expected Wednesdays")

    if errors:
        print("ERROR:")
        for e in errors:
            print(f"  - {e}")
        return 1

    print("OK: all baylearn-seed JSON files valid")
    return 0


if __name__ == "__main__":
    sys.exit(main())
