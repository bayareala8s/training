#!/usr/bin/env python3
"""Stage 3 inventory and heading checks. Exit 0 on pass."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

LESSON_HEADINGS = [
    "Why this matters",
    "Learning objectives",
    "Concept explanation",
    "Visual explanation",
    "Architecture",
    "Production example",
    "Code/configuration example",
    "Trade-offs",
    "Failure modes",
    "Security/reliability implications",
    "Interview perspective",
    "Key takeaways",
    "Knowledge check",
    "Related lab",
    "Related PAKS",
]
LAB_HEADINGS = [
    "Scenario",
    "Business context",
    "Learning objectives",
    "Architecture",
    "Prerequisites",
    "Environment setup",
    "Challenge",
    "Validation",
    "Troubleshooting",
    "Expected outcome",
    "Interview questions",
    "Architecture/trade-off",
    "Cleanup",
    "Cost",
    "Hidden",
    "What you learned",
    "Portfolio",
]
DIAGRAMS = [
    ("AEJE-D-001", "java"),
    ("AEJE-D-002", "java"),
    ("AEJE-D-003", "java"),
    ("AEJE-D-004", "java"),
    ("AEJE-D-005", "java"),
    ("AEJE-D-006", "java"),
    ("AEJE-D-007", "java"),
    ("AEJE-D-008", "java"),
    ("AEJE-D-009", "spring"),
    ("AEJE-D-010", "spring"),
    ("AEJE-D-011", "spring"),
    ("AEJE-D-012", "spring"),
    ("AEJE-D-013", "spring"),
    ("AEJE-D-014", "java"),
    ("AEJE-D-015", "java"),
    ("AEJE-D-016", "java"),
    ("AEJE-D-017", "java"),
]


def has_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^##+ .*{re.escape(fragment)}", text, re.I | re.M))


def main() -> int:
    issues: list[str] = []

    lesson_globs = [
        "course/modules/01-enterprise-java-engineering/lessons/L-*.md",
        "course/modules/02-advanced-java-concurrency/lessons/L-*.md",
        "course/modules/03-spring-boot-engineering/lessons/L-*.md",
        "course/modules/04-jakarta-ee-enterprise-runtime/lessons/L-*.md",
    ]
    lessons: list[Path] = []
    for glob in lesson_globs:
        lessons.extend(sorted(ROOT.glob(glob)))
    if len(lessons) != 22:
        issues.append(f"expected 22 Stage 3 lessons, found {len(lessons)}")
    for path in lessons:
        text = path.read_text()
        missing = [h for h in LESSON_HEADINGS if not has_heading(text, h)]
        if missing:
            issues.append(f"{path.name} missing {missing}")

    stage3_labs = [
        "BUILD-101",
        "BUILD-102",
        "FIX-103",
        "CHALLENGE-104",
        "BREAKFIX-201",
        "INCIDENT-202",
        "ARCHITECT-203",
        "BUILD-301",
        "BUILD-302",
        "BUILD-303",
        "FIX-304",
        "BUILD-305",
        "ARCHITECT-401",
        "INCIDENT-402",
        "INCIDENT-403",
    ]
    labs = [ROOT / "labs" / name / "README.md" for name in stage3_labs]
    if len(labs) != 15:
        issues.append(f"expected 15 Stage 3 labs, found {len(labs)}")
    for path in labs:
        if not path.exists():
            issues.append(f"missing lab {path.parent.name}")
            continue
        text = path.read_text()
        missing = [h for h in LAB_HEADINGS if not has_heading(text, h)]
        if missing:
            issues.append(f"lab {path.parent.name} missing {missing}")
        if len(text.splitlines()) < 80:
            issues.append(f"lab {path.parent.name} shorter than 80 lines")

    for qid in ("Q-01", "Q-02", "Q-03", "Q-04"):
        data = json.loads((ROOT / "course/quizzes" / f"{qid}.json").read_text())
        questions = data.get("questions", [])
        if len(questions) != 8:
            issues.append(f"{qid} has {len(questions)} questions")
        ids = [q.get("id") for q in questions]
        if len(ids) != len(set(ids)):
            issues.append(f"{qid} duplicate ids")
        if not (ROOT / "course/quizzes" / f"{qid}.md").exists():
            issues.append(f"missing {qid}.md")

    for did, folder in DIAGRAMS:
        for ext in (".svg", ".png", ".alt.md", ".source.md"):
            path = ROOT / "diagrams" / folder / f"{did}{ext}"
            if not path.exists():
                issues.append(f"missing {path.relative_to(ROOT)}")
            elif ext == ".alt.md" and path.stat().st_size < 20:
                issues.append(f"short alt {did}")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS Stage 3 inventory and headings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
