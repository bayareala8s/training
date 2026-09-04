#!/usr/bin/env python3
"""Stage 7 inventory, headings, AWS cost/cleanup, terraform presence."""
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
AWS_LABS = ["BUILD-1101", "SECURITY-1103", "INCIDENT-1104", "COST-1105", "BUILD-1201", "BUILD-1202", "INCIDENT-1205"]
ALL_LABS = AWS_LABS + ["ARCHITECT-1102", "BUILD-1203", "BUILD-1204"]
LESSON_GLOBS = [
    "course/modules/11-aws-container-platforms/lessons/L-*.md",
    "course/modules/12-terraform-ansible-cicd/lessons/L-*.md",
]
DIAGRAMS = (
    [(f"AEJE-D-{i:03d}", "aws") for i in range(48, 54)]
    + [(f"AEJE-D-{i:03d}", "devops") for i in range(54, 59)]
)
RCA_LEAK = re.compile(r"Path=/ on port 8080 returns 404|3\.8\.9-debug.*9080", re.I)
TF_DIRS = [
    ROOT / "solutions/BUILD-1101",
    ROOT / "solutions/BUILD-1201",
    ROOT / "solutions/BUILD-1202",
    ROOT / "infrastructure/terraform/baypay-ecs",
]


def has_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^##+ .*{re.escape(fragment)}", text, re.I | re.M))


def main() -> int:
    issues: list[str] = []
    lessons: list[Path] = []
    for glob in LESSON_GLOBS:
        lessons.extend(sorted(ROOT.glob(glob)))
    if len(lessons) != 14:
        issues.append(f"expected 14 Stage 7 lessons, found {len(lessons)}")
    for path in lessons:
        missing = [h for h in LESSON_HEADINGS if not has_heading(path.read_text(), h)]
        if missing:
            issues.append(f"{path.name} missing {missing}")

    for lab in ALL_LABS:
        path = ROOT / "labs" / lab / "README.md"
        if not path.exists():
            issues.append(f"missing lab {lab}")
            continue
        text = path.read_text()
        missing = [h for h in LAB_HEADINGS if not has_heading(text, h)]
        if missing:
            issues.append(f"lab {lab} missing {missing}")
        if not (ROOT / "solutions" / lab / "README.md").exists():
            issues.append(f"missing solution {lab}")
        if not (ROOT / "instructor/rubrics" / f"{lab}.md").exists():
            issues.append(f"missing rubric {lab}")

    for lab in AWS_LABS:
        text = (ROOT / "labs" / lab / "README.md").read_text()
        if not re.search(r"us-west-2", text):
            issues.append(f"{lab} missing us-west-2")
        if not re.search(r"cleanup|destroy", text, re.I):
            issues.append(f"{lab} missing cleanup language")
        if not re.search(r"\$|cost", text, re.I):
            issues.append(f"{lab} missing cost language")

    for qid in ("Q-11", "Q-12"):
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

    for path in list((ROOT / "labs").glob("INCIDENT-11*/README.md")) + list(
        (ROOT / "labs").glob("INCIDENT-12*/README.md")
    ) + list((ROOT / "incidents/aws").glob("INC-AWS-*/README.md")):
        if RCA_LEAK.search(path.read_text()):
            issues.append(f"possible RCA leak {path}")

    for d in TF_DIRS:
        if not list(d.glob("*.tf")):
            issues.append(f"no tf in {d}")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS Stage 7 inventory and headings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
