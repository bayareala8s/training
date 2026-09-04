#!/usr/bin/env python3
"""Stage 14: full-repo inventory, links, JSON, AWS, TODOs, synthetic-data, K8s YAML."""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTAL = Path("/Users/hbhadra/BayLearn-Portal")
SKIP_DIR_NAMES = {
    ".git",
    ".terraform",
    "target",
    "node_modules",
    "__pycache__",
}
LINK_RE = re.compile(r"\[[^\]]*\]\(([^)]+)\)")
TODO_RE = re.compile(r"(?:^|\n)\s*(?:TODO|FIXME|TBD)\s*:|lorem ipsum|\[placeholder\]", re.I)
SECRET_RE = re.compile(
    r"AKIA[0-9A-Z]{16}|BEGIN (RSA |OPENSSH |EC )?PRIVATE KEY|aws_secret_access_key\s*=\s*[\"'][A-Za-z0-9/+=]{20,}",
    re.I,
)
EMPLOYER_RE = re.compile(
    r"\b(our employer|production runbook from|confidential IBM|"
    r"Wells Fargo|JPMorgan|Chase Bank|Bank of America)\b",
    re.I,
)
NEGATED_CLAIM = re.compile(
    r"\bno\b.*\breal customer\b|\bnot a real\b|do not .*real customer|without .*real customer",
    re.I,
)
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


def has_heading(text: str, fragment: str) -> bool:
    return bool(re.search(rf"^##+ .*{re.escape(fragment)}", text, re.I | re.M))


def skip_dir(path: Path) -> bool:
    return any(part in SKIP_DIR_NAMES for part in path.parts)


def resolve_link(src: Path, href: str) -> Path | None:
    href = href.strip()
    if href.startswith(("<", "{")):
        return None
    href = href.split()[0] if href else href
    href = href.split("#", 1)[0]
    if not href or href.startswith(("http://", "https://", "mailto:", "docs/")):
        return None
    if href.startswith("paks."):
        return None
    return (src.parent / href).resolve()


def main() -> int:
    issues: list[str] = []
    data = json.loads((ROOT / "COURSE_MANIFEST.json").read_text())

    lessons = []
    labs = []
    for mod in data["modules"]:
        if not (ROOT / mod["overviewPath"]).exists():
            issues.append(f"missing overview {mod['overviewPath']}")
        for lesson in mod["lessons"]:
            lessons.append(lesson)
            path = ROOT / lesson["path"]
            if not path.exists():
                issues.append(f"missing lesson {lesson['path']}")
                continue
            text = path.read_text()
            missing = [h for h in LESSON_HEADINGS if not has_heading(text, h)]
            if missing:
                issues.append(f"{lesson['id']} missing {missing}")
        for lab in mod["labs"]:
            labs.append(lab)
            path = ROOT / lab["path"]
            if not path.exists():
                issues.append(f"missing lab {lab['path']}")
                continue
            text = path.read_text()
            missing = [h for h in LAB_HEADINGS if not has_heading(text, h)]
            if missing:
                issues.append(f"{lab['id']} missing {missing}")
            sol = ROOT / lab["solutionPath"]
            if not sol.exists() and not (sol / "README.md").exists():
                issues.append(f"missing solution {lab['solutionPath']}")
            elif sol.is_dir() and not (sol / "README.md").exists() and not list(sol.iterdir()):
                issues.append(f"empty solution {lab['solutionPath']}")
            if not (ROOT / lab["rubricPath"]).exists():
                issues.append(f"missing rubric {lab['rubricPath']}")
            if lab.get("awsLab"):
                if not re.search(r"us-west-2", text):
                    issues.append(f"{lab['id']} missing us-west-2")
                if not re.search(r"cleanup|destroy", text, re.I):
                    issues.append(f"{lab['id']} missing cleanup")
                if not re.search(r"\$|cost", text, re.I):
                    issues.append(f"{lab['id']} missing cost")
        quiz = ROOT / "course/quizzes" / f"{mod['quizId']}.md"
        quiz_json = ROOT / "course/quizzes" / f"{mod['quizId']}.json"
        if not quiz.exists():
            issues.append(f"missing {mod['quizId']}.md")
        if not quiz_json.exists():
            issues.append(f"missing {mod['quizId']}.json")

    if len(lessons) != data["counts"]["contentLessons"]:
        issues.append(
            f"lesson count {len(lessons)} != counts.contentLessons {data['counts']['contentLessons']}"
        )
    if len(labs) != data["counts"]["moduleLabs"]:
        issues.append(
            f"lab count {len(labs)} != counts.moduleLabs {data['counts']['moduleLabs']}"
        )

    for cap in data["capstones"]["items"]:
        if not (ROOT / cap["path"]).exists():
            issues.append(f"missing capstone {cap['path']}")
        if not (ROOT / "solutions" / cap["id"] / "README.md").exists():
            issues.append(f"missing solution {cap['id']}")
        if not (ROOT / "instructor/rubrics" / f"{cap['id']}.md").exists():
            issues.append(f"missing rubric {cap['id']}")
        if cap.get("awsLab"):
            text = (ROOT / cap["path"]).read_text()
            if not re.search(r"us-west-2", text):
                issues.append(f"{cap['id']} missing us-west-2")
            if not re.search(r"cleanup|destroy", text, re.I):
                issues.append(f"{cap['id']} missing cleanup")
            if not re.search(r"\$|cost", text, re.I):
                issues.append(f"{cap['id']} missing cost")

    for path in ROOT.rglob("*.json"):
        if skip_dir(path.relative_to(ROOT)):
            continue
        raw = path.read_text()
        try:
            json.loads(raw)
        except json.JSONDecodeError:
            try:
                json.JSONDecoder().raw_decode(raw.lstrip())
            except json.JSONDecodeError as exc:
                issues.append(f"invalid JSON {path.relative_to(ROOT)}: {exc}")

    md_roots = [
        ROOT / "course",
        ROOT / "labs",
        ROOT / "capstones",
        ROOT / "student",
        ROOT / "GETTING_STARTED.md",
        ROOT / "PAKS_LINKS.md",
        ROOT / "diagrams" / "README.md",
    ]
    md_files: list[Path] = []
    for item in md_roots:
        if item.is_file():
            md_files.append(item)
        elif item.is_dir():
            md_files.extend(p for p in item.rglob("*.md") if not skip_dir(p.relative_to(ROOT)))

    for path in md_files:
        text = path.read_text()
        if TODO_RE.search(text):
            issues.append(f"placeholder in {path.relative_to(ROOT)}")
        for href in LINK_RE.findall(text):
            target = resolve_link(path, href)
            if target is None:
                continue
            try:
                target.relative_to(ROOT)
            except ValueError:
                continue
            if not target.exists():
                issues.append(
                    f"broken link {path.relative_to(ROOT)} -> {href}"
                )

    scan_roots = [ROOT / "course", ROOT / "labs", ROOT / "capstones", ROOT / "incidents", ROOT / "datasets"]
    for scan in scan_roots:
        for path in scan.rglob("*"):
            if not path.is_file() or skip_dir(path.relative_to(ROOT)):
                continue
            if path.suffix.lower() not in {".md", ".json", ".yml", ".yaml", ".txt", ".log"}:
                continue
            text = path.read_text(errors="ignore")
            if SECRET_RE.search(text):
                issues.append(f"possible secret {path.relative_to(ROOT)}")
            for line in text.splitlines():
                if EMPLOYER_RE.search(line) and not NEGATED_CLAIM.search(line):
                    issues.append(
                        f"possible real-employer claim {path.relative_to(ROOT)}: {line.strip()[:80]}"
                    )

    try:
        import yaml  # type: ignore
    except ImportError:
        issues.append("PyYAML missing; cannot parse Kubernetes YAML")
    else:
        k8s_dirs = [
            ROOT / "infrastructure/kubernetes",
        ]
        for kdir in k8s_dirs:
            for path in kdir.rglob("*.yaml"):
                try:
                    docs = list(yaml.safe_load_all(path.read_text()) or [])
                except yaml.YAMLError as exc:
                    issues.append(f"invalid YAML {path.relative_to(ROOT)}: {exc}")
                    continue
                if not docs:
                    issues.append(f"empty YAML {path.relative_to(ROOT)}")
                for i, doc in enumerate(docs):
                    if not isinstance(doc, dict) or not doc.get("apiVersion") or not doc.get("kind"):
                        issues.append(
                            f"{path.relative_to(ROOT)} doc {i} missing apiVersion/kind"
                        )

    if PORTAL.exists():
        seed = PORTAL / "backend/src/seed/aeje-course.ts"
        if seed.exists():
            issues.append("portal aeje-course.ts already exists (seed must be a later stage)")
        catalog = PORTAL / "backend/src/seed/courses.ts"
        if catalog.exists() and "baylearn-aeje-001" in catalog.read_text():
            issues.append("portal courses.ts already lists AEJE (seed must be a later stage)")

    if issues:
        print("FAIL")
        for issue in issues:
            print("-", issue)
        return 1
    print(
        f"PASS Stage 14 inventory ({len(lessons)} lessons, {len(labs)} labs, "
        f"{len(data['capstones']['items'])} capstones)"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
