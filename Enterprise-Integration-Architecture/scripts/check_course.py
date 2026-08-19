#!/usr/bin/env python3
"""Repo completeness check (instructors / before a cohort)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def main() -> int:
    errors: list[str] = []
    catalog = (ROOT / "course-ui" / "js" / "catalog.js").read_text()
    paths = re.findall(r'"path":\s*"([^"]+)"', catalog)
    if len(paths) != 128:
        errors.append(f"catalog lesson paths={len(paths)} expected 128")
    for p in paths:
        if not (ROOT / p).exists():
            errors.append(f"missing lesson {p}")

    labs = [
        "lab-01-classification",
        "lab-02-api",
        "lab-03-messaging",
        "lab-04-pubsub",
        "lab-05-events",
        "lab-06-file-transfer",
        "lab-07-large-files",
        "lab-08-esb-modernization",
        "lab-11-chaos",
        "lab-12-security",
        "lab-13-observability",
        "lab-15-ai-agent",
    ]
    for lab in labs:
        if not (ROOT / "labs" / lab / "README.md").exists():
            errors.append(f"missing labs/{lab}/README.md")
        if lab == "lab-01-classification":
            continue
        tf = ROOT / "terraform" / "labs" / lab / "main.tf"
        if lab == "lab-08-esb-modernization":
            if not tf.exists():
                errors.append("missing optional lab-08 terraform")
            continue
        if not tf.exists():
            errors.append(f"missing terraform for {lab}")

    for cap in ("banking", "ecommerce", "healthcare", "manufacturing"):
        if not (ROOT / "capstones" / cap / "README.md").exists():
            errors.append(f"missing capstone brief {cap}")
        if not (ROOT / "terraform" / "capstones" / cap / "main.tf").exists():
            errors.append(f"missing capstone terraform {cap}")

    chal = (ROOT / "course-ui" / "js" / "challenges.js").read_text()
    n = len(re.findall(r'id: "c\d+"', chal))
    if n != 25:
        errors.append(f"challenges={n} expected 25")

    for rel in (
        "GETTING_STARTED.md",
        "docs/STUDENT_HANDBOOK.md",
        "scripts/validate_lab.py",
        "templates/adr.md",
        "templates/portfolio.md",
        "assessments/final-architecture-assessment.md",
        "course-ui/index.html",
    ):
        if not (ROOT / rel).exists():
            errors.append(f"missing {rel}")

    if errors:
        print("NOT READY")
        for e in errors:
            print(" -", e)
        return 1
    print("READY")
    print(f"128 lessons, 12 labs, 4 capstones, 25 challenges.")
    print("Students start at GETTING_STARTED.md → ./scripts/start_course.sh")
    return 0


if __name__ == "__main__":
    sys.exit(main())
