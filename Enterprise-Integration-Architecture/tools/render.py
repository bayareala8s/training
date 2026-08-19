#!/usr/bin/env python3
"""Render BayLearn EIA lesson markdown from structured lesson records."""

from __future__ import annotations

from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]


def md_list(items: list[str]) -> str:
    return "\n".join(f"- {item}" for item in items)


def md_numbered(items: list[str]) -> str:
    return "\n".join(f"{i}. {item}" for i, item in enumerate(items, 1))


def tradeoff_table(rows: list[tuple[str, str, str]]) -> str:
    lines = [
        "| Dimension | Benefit | Cost / risk |",
        "|-----------|---------|-------------|",
    ]
    for dim, benefit, cost in rows:
        lines.append(f"| {dim} | {benefit} | {cost} |")
    return "\n".join(lines)


def render_lesson(lesson: dict[str, Any]) -> str:
    num = lesson["id"]
    title = lesson["title"]
    module = lesson["module"]
    duration = lesson.get("duration", "25–35 minutes")
    objectives = lesson["objectives"]
    scenario = lesson["scenario"]
    why = lesson["why"]
    when = lesson["when"]
    when_not = lesson["when_not"]
    how_pattern = lesson["how_pattern"]
    how_aws = lesson["how_aws"]
    diagram = lesson.get("diagram", "").strip()
    tradeoffs = lesson.get("tradeoffs", [])
    decision = lesson["decision"]
    checks = lesson.get("checks", [])
    note = lesson.get("architect_note", "")
    anti = lesson.get("anti_patterns", [])
    nfr = lesson.get("nfr", [])

    parts = [
        f"# Lesson {num} — {title}",
        "",
        f"**Module:** {module}  ",
        f"**Duration:** {duration}  ",
        f"**BayLearn philosophy:** WHY → WHEN → HOW. Pattern first. Technology second.",
        "",
        "---",
        "",
        "## Learning outcomes",
        "",
        "By the end of this lesson you will be able to:",
        "",
        md_numbered(objectives),
        "",
        "---",
        "",
        "## Enterprise scenario",
        "",
        scenario,
        "",
        "> **Fiction notice:** Named companies in this course (Northbridge Bank, Harbor Retail, "
        "CareMesh Health, Atlas Manufacturing) are instructional fictions.",
        "",
        "---",
        "",
        "## WHY this exists",
        "",
        why,
        "",
        "---",
        "",
        "## WHEN an Enterprise Architect uses it",
        "",
        md_list(when),
        "",
        "### When NOT to use it",
        "",
        md_list(when_not),
        "",
    ]

    if nfr:
        parts += [
            "### Integration characteristics to inspect",
            "",
            md_list(nfr),
            "",
        ]

    parts += [
        "---",
        "",
        "## HOW — the pattern (vendor-neutral)",
        "",
        how_pattern,
        "",
    ]

    if diagram:
        parts += [
            "### Architecture diagram",
            "",
            "```mermaid",
            diagram,
            "```",
            "",
        ]

    parts += [
        "---",
        "",
        "## HOW — AWS implementation (after the pattern)",
        "",
        how_aws,
        "",
        "Do not start here. If you cannot explain the requirement and pattern without naming an AWS service, you are not ready to select technology.",
        "",
    ]

    if anti:
        parts += [
            "---",
            "",
            "## Anti-patterns",
            "",
            md_list(anti),
            "",
        ]

    if tradeoffs:
        parts += [
            "---",
            "",
            "## Tradeoffs",
            "",
            tradeoff_table(tradeoffs),
            "",
        ]

    parts += [
        "---",
        "",
        "## Architecture decision prompt",
        "",
        decision,
        "",
        "Write four sentences: the requirement, the integration characteristics, the pattern, and why the rejected options fail the NFRs.",
        "",
    ]

    if checks:
        parts += [
            "---",
            "",
            "## Knowledge check",
            "",
        ]
        for i, q in enumerate(checks, 1):
            parts += [
                f"**Q{i}.** {q['q']}",
                "",
                f"*Answer.* {q['a']}",
                "",
            ]

    if note:
        parts += [
            "---",
            "",
            "## Architect's note",
            "",
            note,
            "",
        ]

    parts += [
        "---",
        "",
        "## Next",
        "",
        "Complete any architecture challenge attached to this lesson in the course player. "
        "Record an ADR fragment if the decision would survive a design review.",
        "",
    ]
    return "\n".join(parts)


def write_lesson(rel_dir: str, filename: str, lesson: dict[str, Any]) -> Path:
    path = ROOT / rel_dir / filename
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(render_lesson(lesson), encoding="utf-8")
    return path
