#!/usr/bin/env python3
"""Stage 5 inventory and heading checks. Exit 0 on pass."""
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
LESSON_GLOBS = [
    "course/modules/07-jvm-internals-performance/lessons/L-*.md",
    "course/modules/08-jvm-troubleshooting/lessons/L-*.md",
]
LABS = [
    "LAB-701",
    "LAB-702",
    "LAB-703",
    "LAB-704",
    "INCIDENT-801",
    "INCIDENT-802",
    "INCIDENT-803",
    "INCIDENT-804",
    "INCIDENT-805",
    "INCIDENT-806",
]
DIAGRAMS = [(f"AEJE-D-{i:03d}", "jvm") for i in range(28, 38)]
RCA_LEAK = re.compile(
    r"catastrophic regex|IdempotencyReplayCache|NightlyReversalJob locks ledger then account|logging\.level\.com\.baypay=DEBUG|-Xmx512m \(100%",
    re.I,
)


def has_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^##+ .*{re.escape(fragment)}", text, re.I | re.M))


def main() -> int:
    issues: list[str] = []
    lessons: list[Path] = []
    for glob in LESSON_GLOBS:
        lessons.extend(sorted(ROOT.glob(glob)))
    if len(lessons) != 13:
        issues.append(f"expected 13 Stage 5 lessons, found {len(lessons)}")
    for path in lessons:
        missing = [h for h in LESSON_HEADINGS if not has_heading(path.read_text(), h)]
        if missing:
            issues.append(f"{path.name} missing {missing}")

    for lab in LABS:
        path = ROOT / "labs" / lab / "README.md"
        if not path.exists():
            issues.append(f"missing lab {lab}")
            continue
        text = path.read_text()
        missing = [h for h in LAB_HEADINGS if not has_heading(text, h)]
        if missing:
            issues.append(f"lab {lab} missing {missing}")
        if len(text.splitlines()) < 80:
            issues.append(f"lab {lab} short")
        if not (ROOT / "solutions" / lab / "README.md").exists():
            issues.append(f"missing solution {lab}")
        if not (ROOT / "instructor/rubrics" / f"{lab}.md").exists():
            issues.append(f"missing rubric {lab}")

    for qid in ("Q-07", "Q-08"):
        data = json.loads((ROOT / "course/quizzes" / f"{qid}.json").read_text())
        qs = data.get("questions", [])
        if len(qs) != 8:
            issues.append(f"{qid} has {len(qs)} questions")
        if len({q.get("id") for q in qs}) != 8:
            issues.append(f"{qid} duplicate ids")
        if not (ROOT / "course/quizzes" / f"{qid}.md").exists():
            issues.append(f"missing {qid}.md")

    for did, folder in DIAGRAMS:
        for ext in (".svg", ".png", ".alt.md", ".source.md"):
            path = ROOT / "diagrams" / folder / f"{did}{ext}"
            if not path.exists():
                issues.append(f"missing {path.relative_to(ROOT)}")

    runtime = (ROOT / "datasets/baypay-jvm/RUNTIME.md").read_text()
    if "IdempotencyReplayCache" in runtime or "catastrophic regex" in runtime:
        issues.append("RUNTIME.md contains instructor RCA")

    student_paths = list((ROOT / "labs").glob("INCIDENT-80*/README.md"))
    student_paths += list((ROOT / "incidents/jvm").glob("INC-JVM-80*/README.md"))
    for path in student_paths:
        if RCA_LEAK.search(path.read_text()):
            issues.append(f"possible RCA leak {path}")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS Stage 5 inventory and headings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
