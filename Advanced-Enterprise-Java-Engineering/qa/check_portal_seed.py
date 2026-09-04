#!/usr/bin/env python3
"""Validate AEJE portal seed counts and that s3Keys resolve in this repo."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTAL = Path("/Users/hbhadra/BayLearn-Portal")
PREFIX = "curriculum/advanced-enterprise-java/"
S3 = re.compile(r's3Key: "([^"]+)"')


def main() -> int:
    issues: list[str] = []
    seed = PORTAL / "backend/src/seed/aeje-course.ts"
    if not seed.exists():
        print("FAIL")
        print("- missing aeje-course.ts")
        return 1
    text = seed.read_text()
    keys = S3.findall(text)
    if "AEJE_PORTAL_LESSON_COUNT = 190" not in text:
        issues.append("AEJE_PORTAL_LESSON_COUNT is not 190")
    for key in keys:
        if not key.startswith(PREFIX):
            issues.append(f"bad prefix {key}")
            continue
        rel = key[len(PREFIX) :]
        if not (ROOT / rel).exists():
            issues.append(f"missing file for {key}")

    lessons = json.loads((ROOT / "baylearn-seed/lessons.json").read_text())
    if len(lessons) != 190:
        issues.append(f"baylearn-seed lessons {len(lessons)} != 190")
    kinds = {row["kind"] for row in lessons}
    if kinds != {"lesson", "lab", "quiz", "capstone"}:
        issues.append(f"unexpected kinds {kinds}")

    catalog = (PORTAL / "shared/src/catalog.ts").read_text()
    if catalog.index("Enterprise Integration Architecture") > catalog.index(
        "Advanced Enterprise Java Engineering"
    ):
        issues.append("AEJE must be appended after EIA in CATALOG_COURSE_ORDER")
    pricing = (PORTAL / "shared/src/pricing.ts").read_text()
    if "Advanced Enterprise Java Engineering" not in pricing:
        issues.append("missing AEJE pricing")
    if "All seven courses" not in pricing:
        issues.append("COURSE_BUNDLES copy missing — check we did not edit it")
    if "aejeSeedCourse" not in (PORTAL / "backend/src/seed/courses.ts").read_text():
        issues.append("courses.ts missing aejeSeedCourse")
    utils = (PORTAL / "backend/src/seed/catalog-sync-utils.ts").read_text()
    if "seedLesson.assignment" not in utils:
        issues.append("insertCourseContent still skips assignments")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print(f"PASS portal seed ({len(lessons)} lessons, {len(keys)} materials)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
