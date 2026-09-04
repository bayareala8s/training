#!/usr/bin/env python3
"""Stage 10: Module 16 lessons/labs + 100 unique interview questions."""
from __future__ import annotations

import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = json.loads((ROOT / "COURSE_MANIFEST.json").read_text())
EXPECTED = MANIFEST["interviewBank"]["domainCounts"]
FIELDS = MANIFEST["interviewBank"]["recordFields"]

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
LABS = [f"INTERVIEW-160{i}" for i in range(1, 6)]
RCA_LEAK = re.compile(
    r"cardinality explosion|validation CNAME was deleted|"
    r"customerId and accountId tags caused|3\.8\.9-debug.*9080",
    re.I,
)


def has_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^##+ .*{re.escape(fragment)}", text, re.I | re.M))


def main() -> int:
    issues: list[str] = []
    lessons = sorted(
        (ROOT / "course/modules/16-advanced-engineer-interview-simulator/lessons").glob("L-16.*.md")
    )
    if len(lessons) != 9:
        issues.append(f"expected 9 Stage 10 lessons, found {len(lessons)}")
    for path in lessons:
        text = path.read_text()
        missing = [h for h in LESSON_HEADINGS if not has_heading(text, h)]
        if missing:
            issues.append(f"{path.name} missing {missing}")
        lines = text.count("\n") + (0 if text.endswith("\n") else 1)
        if lines < 190 or lines > 260:
            issues.append(f"{path.name} line count {lines} not in 190–260")

    for lab in LABS:
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

    if not (ROOT / "student/worksheets/PF-design.md").exists():
        issues.append("missing PF-design.md")
    if not (ROOT / "course/modules/16-advanced-engineer-interview-simulator/README.md").exists():
        issues.append("missing module 16 README")

    q16 = json.loads((ROOT / "course/quizzes/Q-16.json").read_text())
    if len(q16.get("questions", [])) != 8:
        issues.append("Q-16 must have 8 questions")
    if not (ROOT / "course/quizzes/Q-16.md").exists():
        issues.append("missing Q-16.md")

    bank_path = ROOT / "interview-bank/questions.json"
    if not bank_path.exists():
        issues.append("missing interview-bank/questions.json")
    else:
        bank = json.loads(bank_path.read_text())
        qs = bank if isinstance(bank, list) else bank.get("questions", [])
        if len(qs) != 100:
            issues.append(f"bank has {len(qs)} questions, expected 100")
        ids = [q.get("id") for q in qs]
        if len(ids) != len(set(ids)):
            issues.append("duplicate interview question ids")
        texts = [re.sub(r"\s+", " ", (q.get("question") or "").strip().lower()) for q in qs]
        if len(texts) != len(set(texts)):
            issues.append("duplicate interview question text")
        counts = Counter(q.get("domain") for q in qs)
        for domain, n in EXPECTED.items():
            if counts.get(domain) != n:
                issues.append(f"domain {domain} has {counts.get(domain)} expected {n}")
        for q in qs:
            for field in FIELDS:
                val = q.get(field)
                if val in (None, "", [], {}):
                    issues.append(f"{q.get('id')} missing {field}")
                    break
            if q.get("id") == "AEJE-IQ-001" and not q.get("engineerAnswer"):
                # engineerAnswer recommended; only warn via missing if we require it
                pass
        expected_ids = {f"AEJE-IQ-{i:03d}" for i in range(1, 101)}
        if set(ids) != expected_ids:
            issues.append("bank ids are not AEJE-IQ-001..100")

    for extra in (
        ROOT / "interview-bank/schema.json",
        ROOT / "interview-bank/simulator.py",
        ROOT / "datasets/baypay-interview/ROUNDS.md",
    ):
        if not extra.exists():
            issues.append(f"missing {extra.relative_to(ROOT)}")

    for path in list(
        (ROOT / "course/modules/16-advanced-engineer-interview-simulator").glob("**/*.md")
    ) + [ROOT / "labs" / lab / "README.md" for lab in LABS]:
        if path.exists() and RCA_LEAK.search(path.read_text()):
            issues.append(f"possible RCA leak {path.relative_to(ROOT)}")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS Stage 10 inventory, headings, and interview bank")
    return 0


if __name__ == "__main__":
    sys.exit(main())
