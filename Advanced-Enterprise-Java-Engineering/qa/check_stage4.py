#!/usr/bin/env python3
"""Stage 4 inventory and heading checks. Exit 0 on pass."""
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
STAGE4_LESSON_GLOBS = [
    "course/modules/05-websphere-network-deployment/lessons/L-*.md",
    "course/modules/06-websphere-liberty-modernization/lessons/L-*.md",
]
STAGE4_LABS = [
    "ARCHITECT-501",
    "INCIDENT-502",
    "INCIDENT-503",
    "INCIDENT-504",
    "MODERNIZE-601",
    "MODERNIZE-602",
    "MODERNIZE-603",
    "ARCHITECT-604",
]
DIAGRAMS = [
    ("AEJE-D-018", "websphere"),
    ("AEJE-D-019", "websphere"),
    ("AEJE-D-020", "websphere"),
    ("AEJE-D-021", "websphere"),
    ("AEJE-D-022", "websphere"),
    ("AEJE-D-023", "liberty"),
    ("AEJE-D-024", "liberty"),
    ("AEJE-D-025", "liberty"),
    ("AEJE-D-026", "liberty"),
    ("AEJE-D-027", "liberty"),
]
RCA_LEAK = re.compile(
    r"root cause is|RCA:|TCP-only so they remain|reporting\.ear on node-pay-1 holds|expects jdbc/baypayXA",
    re.I,
)


def has_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^##+ .*{re.escape(fragment)}", text, re.I | re.M))


def main() -> int:
    issues: list[str] = []
    lessons: list[Path] = []
    for glob in STAGE4_LESSON_GLOBS:
        lessons.extend(sorted(ROOT.glob(glob)))
    if len(lessons) != 11:
        issues.append(f"expected 11 Stage 4 lessons, found {len(lessons)}")
    for path in lessons:
        text = path.read_text()
        missing = [h for h in LESSON_HEADINGS if not has_heading(text, h)]
        if missing:
            issues.append(f"{path.name} missing {missing}")

    for lab in STAGE4_LABS:
        path = ROOT / "labs" / lab / "README.md"
        if not path.exists():
            issues.append(f"missing lab {lab}")
            continue
        text = path.read_text()
        missing = [h for h in LAB_HEADINGS if not has_heading(text, h)]
        if missing:
            issues.append(f"lab {lab} missing {missing}")
        if len(text.splitlines()) < 80:
            issues.append(f"lab {lab} shorter than 80 lines")
        if not (ROOT / "solutions" / lab / "README.md").exists():
            issues.append(f"missing solution {lab}")
        if not (ROOT / "instructor/rubrics" / f"{lab}.md").exists():
            issues.append(f"missing rubric {lab}")

    for qid in ("Q-05", "Q-06"):
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

    student_paths = list((ROOT / "labs").glob("INCIDENT-50*/README.md"))
    student_paths += list((ROOT / "incidents/production").glob("INC-WAS-50*/README.md"))
    student_paths += list((ROOT / "incidents/production").glob("INC-WAS-50*/evidence/*"))
    topo = ROOT / "datasets/baypay-cell/TOPOLOGY.md"
    if "INC-WAS-502:" in topo.read_text():
        issues.append("TOPOLOGY.md still contains instructor RCA block")
    for path in student_paths:
        text = path.read_text()
        if RCA_LEAK.search(text):
            issues.append(f"possible RCA leak {path}")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS Stage 4 inventory and headings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
