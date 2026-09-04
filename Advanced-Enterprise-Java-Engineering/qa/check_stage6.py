#!/usr/bin/env python3
"""Stage 6 inventory and heading checks. Exit 0 on pass."""
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
    "course/modules/09-containers-for-java/lessons/L-*.md",
    "course/modules/10-kubernetes-and-openshift/lessons/L-*.md",
]
LABS = [
    "BUILD-901",
    "FIX-902",
    "SECURITY-903",
    "PERFORMANCE-904",
    "INCIDENT-1001",
    "INCIDENT-1002",
    "INCIDENT-1003",
    "INCIDENT-1004",
    "INCIDENT-1005",
    "INCIDENT-1006",
]
DIAGRAMS = [
    ("AEJE-D-038", "containers"),
    ("AEJE-D-039", "containers"),
    ("AEJE-D-040", "containers"),
    ("AEJE-D-041", "containers"),
    ("AEJE-D-042", "kubernetes"),
    ("AEJE-D-043", "openshift"),
    ("AEJE-D-044", "kubernetes"),
    ("AEJE-D-045", "kubernetes"),
    ("AEJE-D-046", "kubernetes"),
    ("AEJE-D-047", "kubernetes"),
]
RCA_LEAK = re.compile(
    r"dropped BAYPAY_DB_URL|selector app=payment, Deployment labels|CN=\*\.baypay\.internal|only exposes /actuator/health \(404\)",
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
        issues.append(f"expected 13 Stage 6 lessons, found {len(lessons)}")
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

    for qid in ("Q-09", "Q-10"):
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

    cluster = (ROOT / "datasets/baypay-k8s/CLUSTER.md").read_text()
    if "dropped BAYPAY_DB_URL" in cluster:
        issues.append("CLUSTER.md contains instructor RCA")

    for path in list((ROOT / "labs").glob("INCIDENT-100*/README.md")) + list(
        (ROOT / "incidents/kubernetes").glob("INC-K8S-100*/README.md")
    ):
        if RCA_LEAK.search(path.read_text()):
            issues.append(f"possible RCA leak {path}")

    for df in [
        ROOT / "solutions/BUILD-901/Dockerfile",
        ROOT / "solutions/FIX-902/Dockerfile",
        ROOT / "solutions/SECURITY-903/Dockerfile",
        ROOT / "solutions/PERFORMANCE-904/Dockerfile",
    ]:
        text = df.read_text()
        if "FROM" not in text or "USER" not in text:
            issues.append(f"{df.name} missing FROM/USER")
        if re.search(r"Xmx\s*=\s*\$\{?MEM|Xmx512m", text) and "MaxRAMPercentage" not in text:
            issues.append(f"{df} may set Xmx without percentage")

    yamls = list((ROOT / "infrastructure/kubernetes/payment-service").glob("*.yaml"))
    if len(yamls) < 5:
        issues.append(f"expected healthy YAML set, found {len(yamls)}")
    for y in yamls:
        t = y.read_text()
        if "apiVersion" not in t or "kind" not in t:
            issues.append(f"yaml missing apiVersion/kind {y.name}")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS Stage 6 inventory and headings")
    return 0


if __name__ == "__main__":
    sys.exit(main())
