#!/usr/bin/env python3
"""Stage 11 capstone inventory, headings, AWS cost/cleanup, RCA leak."""
from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
HEADINGS = [
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
CAPS = [
    ("CAPSTONE-1", "capstones/01-build-baypay/README.md", False),
    ("CAPSTONE-2", "capstones/02-modernize-baypay/README.md", False),
    ("CAPSTONE-3", "capstones/03-cloud-baypay/README.md", True),
    ("CAPSTONE-4", "capstones/04-production-crisis/README.md", False),
]
RCA_LEAK = re.compile(
    r"FraudClient has no timeout is the RCA|cardinality explosion|"
    r"validation CNAME was deleted",
    re.I,
)


def has_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^##+ .*{re.escape(fragment)}", text, re.I | re.M))


def main() -> int:
    issues: list[str] = []
    if not (ROOT / "capstones/README.md").exists():
        issues.append("missing capstones/README.md")
    for cid, rel, aws in CAPS:
        path = ROOT / rel
        if not path.exists():
            issues.append(f"missing {rel}")
            continue
        text = path.read_text()
        missing = [h for h in HEADINGS if not has_heading(text, h)]
        if missing:
            issues.append(f"{cid} missing {missing}")
        if text.count("\n") < 80:
            issues.append(f"{cid} too short")
        if not (ROOT / "solutions" / cid / "README.md").exists():
            issues.append(f"missing solution {cid}")
        if not (ROOT / "instructor/rubrics" / f"{cid}.md").exists():
            issues.append(f"missing rubric {cid}")
        if aws:
            if not re.search(r"us-west-2", text):
                issues.append(f"{cid} missing us-west-2")
            if not re.search(r"cleanup|destroy", text, re.I):
                issues.append(f"{cid} missing cleanup")
            if not re.search(r"\$|cost", text, re.I):
                issues.append(f"{cid} missing cost")
        if RCA_LEAK.search(text):
            issues.append(f"possible RCA leak {rel}")

    for name in ("PF-service.md", "PF-modernize.md", "PF-cloud.md", "PF-crisis.md"):
        if not (ROOT / "student/worksheets" / name).exists():
            issues.append(f"missing {name}")

    for extra in (
        ROOT / "incidents/production/INC-CAP-4/README.md",
        ROOT / "incidents/production/INC-CAP-4/timeline.json",
        ROOT / "diagrams/capstones/AEJE-D-071.svg",
        ROOT / "diagrams/capstones/AEJE-D-072.svg",
        ROOT / "diagrams/capstones/AEJE-D-071.png",
        ROOT / "diagrams/capstones/AEJE-D-072.png",
    ):
        if not extra.exists():
            issues.append(f"missing {extra.relative_to(ROOT)}")

    pack = ROOT / "incidents/production/INC-CAP-4/README.md"
    if pack.exists() and RCA_LEAK.search(pack.read_text()):
        issues.append("possible RCA leak INC-CAP-4 README")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print("PASS Stage 11 capstones")
    return 0


if __name__ == "__main__":
    sys.exit(main())
