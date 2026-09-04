#!/usr/bin/env python3
"""Stage 9 inventory, headings, and student RCA-leak checks."""
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
ALL_LABS = ["AI-1501", "AI-1502", "AI-1503", "AI-1504"]
# Instructor RCA lectures from prior modules + 1504 is allowed to SHOW the planted
# hallucination in the student lab (it is the artifact). Still forbid prior-module RCAs.
RCA_LEAK = re.compile(
    r"cardinality explosion|validation CNAME was deleted|"
    r"customerId and accountId tags caused",
    re.I,
)


def has_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^##+ .*{re.escape(fragment)}", text, re.I | re.M))


def main() -> int:
    issues: list[str] = []
    lessons = sorted((ROOT / "course/modules/15-bayops-ai/lessons").glob("L-15.*.md"))
    if len(lessons) != 6:
        issues.append(f"expected 6 Stage 9 lessons, found {len(lessons)}")
    for path in lessons:
        text = path.read_text()
        missing = [h for h in LESSON_HEADINGS if not has_heading(text, h)]
        if missing:
            issues.append(f"{path.name} missing {missing}")
        lines = text.count("\n") + (0 if text.endswith("\n") else 1)
        if lines < 190 or lines > 260:
            issues.append(f"{path.name} line count {lines} not in 190–260")

    for lab in ALL_LABS:
        path = ROOT / "labs" / lab / "README.md"
        if not path.exists():
            issues.append(f"missing lab {lab}")
            continue
        text = path.read_text()
        missing = [h for h in LAB_HEADINGS if not has_heading(text, h)]
        if missing:
            issues.append(f"lab {lab} missing {missing}")
        if text.count("\n") < 80:
            issues.append(f"lab {lab} too short")
        if not (ROOT / "solutions" / lab / "README.md").exists():
            issues.append(f"missing solution {lab}")
        if not (ROOT / "instructor/rubrics" / f"{lab}.md").exists():
            issues.append(f"missing rubric {lab}")

    if not (ROOT / "student/worksheets/PF-ai.md").exists():
        issues.append("missing worksheet PF-ai.md")

    data = json.loads((ROOT / "course/quizzes/Q-15.json").read_text())
    qs = data.get("questions", [])
    if len(qs) != 8 or len({q.get("id") for q in qs}) != 8:
        issues.append("Q-15 question problem")
    if not (ROOT / "course/quizzes/Q-15.md").exists():
        issues.append("missing Q-15.md")

    for did in ("AEJE-D-068", "AEJE-D-069", "AEJE-D-070"):
        for ext in (".svg", ".png", ".alt.md", ".source.md"):
            path = ROOT / "diagrams" / "ai" / f"{did}{ext}"
            if not path.exists():
                issues.append(f"missing {path.relative_to(ROOT)}")

    for extra in (
        ROOT / "course/modules/15-bayops-ai/README.md",
        ROOT / "datasets/baypay-ai/BAYOPS.md",
        ROOT / "infrastructure/bayops-ai/README.md",
        ROOT / "infrastructure/bayops-ai/schema/output.schema.json",
        ROOT / "infrastructure/bayops-ai/fixtures/ai-1501-mixed-summary.json",
        ROOT / "infrastructure/bayops-ai/fixtures/ai-1504-hallucination.json",
        ROOT / "incidents/ai/INC-AI-1504/README.md",
    ):
        if not extra.exists():
            issues.append(f"missing {extra.relative_to(ROOT)}")

    student_surfaces = list((ROOT / "course/modules/15-bayops-ai").glob("**/*.md")) + [
        ROOT / "labs" / lab / "README.md" for lab in ALL_LABS
    ]
    for path in student_surfaces:
        if path.exists() and RCA_LEAK.search(path.read_text()):
            issues.append(f"possible RCA leak {path.relative_to(ROOT)}")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS Stage 9 inventory and headings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
