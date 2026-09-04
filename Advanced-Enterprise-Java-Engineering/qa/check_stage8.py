#!/usr/bin/env python3
"""Stage 8 inventory, headings, and student RCA-leak checks."""
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
ALL_LABS = [
    "BUILD-1300",
    "INCIDENT-1301",
    "ARCHITECT-1401",
    "INCIDENT-1402",
    "DR-1403",
    "SECURITY-1404",
]
LESSON_GLOBS = [
    "course/modules/13-production-engineering-observability/lessons/L-*.md",
    "course/modules/14-security-ha-dr/lessons/L-*.md",
]
DIAGRAMS = [(f"AEJE-D-{i:03d}", "observability") for i in range(59, 63)] + [
    (f"AEJE-D-{i:03d}", "security") for i in range(63, 68)
]
# Instructor RCA phrases that must not appear in student-facing incident surfaces.
RCA_LEAK = re.compile(
    r"cardinality explosion|unbounded labels on payment\.create|"
    r"validation CNAME was deleted|PENDING_VALIDATION is the RCA|"
    r"customerId and accountId tags caused",
    re.I,
)


def has_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^##+ .*{re.escape(fragment)}", text, re.I | re.M))


def main() -> int:
    issues: list[str] = []
    lessons: list[Path] = []
    for glob in LESSON_GLOBS:
        lessons.extend(sorted(ROOT.glob(glob)))
    if len(lessons) != 14:
        issues.append(f"expected 14 Stage 8 lessons, found {len(lessons)}")
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

    for name in ("PF-ops.md", "PF-security.md", "PF-dr.md"):
        if not (ROOT / "student/worksheets" / name).exists():
            issues.append(f"missing worksheet {name}")

    for qid in ("Q-13", "Q-14"):
        data = json.loads((ROOT / "course/quizzes" / f"{qid}.json").read_text())
        qs = data.get("questions", [])
        if len(qs) != 8 or len({q.get("id") for q in qs}) != 8:
            issues.append(f"{qid} question problem")
        if not (ROOT / "course/quizzes" / f"{qid}.md").exists():
            issues.append(f"missing {qid}.md")

    for did, folder in DIAGRAMS:
        for ext in (".svg", ".png", ".alt.md", ".source.md"):
            path = ROOT / "diagrams" / folder / f"{did}{ext}"
            if not path.exists():
                issues.append(f"missing {path.relative_to(ROOT)}")

    for extra in (
        ROOT / "course/modules/13-production-engineering-observability/README.md",
        ROOT / "course/modules/14-security-ha-dr/README.md",
        ROOT / "datasets/baypay-ops/OBSERVABILITY.md",
        ROOT / "datasets/baypay-security/TRUST.md",
        ROOT / "incidents/production/INC-PROD-1301/README.md",
        ROOT / "incidents/production/INC-SEC-1402/README.md",
        ROOT / "labs/BUILD-1300/starter/dashboard.json",
        ROOT / "solutions/BUILD-1300/dashboard.json",
    ):
        if not extra.exists():
            issues.append(f"missing {extra.relative_to(ROOT)}")

    student_surfaces = (
        list((ROOT / "labs").glob("BUILD-1300/README.md"))
        + list((ROOT / "labs").glob("INCIDENT-13*/README.md"))
        + list((ROOT / "labs").glob("INCIDENT-14*/README.md"))
        + list((ROOT / "incidents/production").glob("INC-*/README.md"))
        + list((ROOT / "incidents/production").glob("INC-*/timeline.json"))
        + list((ROOT / "course/modules/13-production-engineering-observability").glob("**/*.md"))
        + list((ROOT / "course/modules/14-security-ha-dr").glob("**/*.md"))
    )
    for path in student_surfaces:
        if RCA_LEAK.search(path.read_text()):
            issues.append(f"possible RCA leak {path.relative_to(ROOT)}")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS Stage 8 inventory and headings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
