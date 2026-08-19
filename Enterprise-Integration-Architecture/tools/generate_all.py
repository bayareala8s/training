#!/usr/bin/env python3
"""Generate lesson markdown, module READMEs, diagrams index, and course-ui catalog."""

from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(Path(__file__).resolve().parent))

from render import render_lesson  # noqa: E402
from m01 import M01  # noqa: E402
from m02_m03 import M02, M03  # noqa: E402
from m04_m05 import M04, M05  # noqa: E402
from m06_m07 import M06, M07  # noqa: E402
from m08_m10 import M08, M09, M10  # noqa: E402
from m11_m15 import M11, M12, M13, M14, M15  # noqa: E402

MODULES = [
    {
        "id": "01",
        "slug": "01-fundamentals",
        "title": "Enterprise Integration Fundamentals",
        "lessons": M01,
        "lab": "lab-01-classification",
        "diagram": "01-point-to-point-and-styles",
    },
    {
        "id": "02",
        "slug": "02-api-integration",
        "title": "API-Based Integration",
        "lessons": M02,
        "lab": "lab-02-api",
        "diagram": "02-api-integration",
    },
    {
        "id": "03",
        "slug": "03-messaging",
        "title": "Enterprise Messaging",
        "lessons": M03,
        "lab": "lab-03-messaging",
        "diagram": "03-queue-architecture",
    },
    {
        "id": "04",
        "slug": "04-pubsub",
        "title": "Pub/Sub Architecture",
        "lessons": M04,
        "lab": "lab-04-pubsub",
        "diagram": "04-pubsub-architecture",
    },
    {
        "id": "05",
        "slug": "05-event-driven",
        "title": "Event-Driven Architecture",
        "lessons": M05,
        "lab": "lab-05-events",
        "diagram": "05-event-driven-architecture",
    },
    {
        "id": "06",
        "slug": "06-file-transfer",
        "title": "Enterprise File Transfer",
        "lessons": M06,
        "lab": "lab-06-file-transfer",
        "diagram": "06-file-transfer-architecture",
    },
    {
        "id": "07",
        "slug": "07-large-files",
        "title": "Large File Architecture",
        "lessons": M07,
        "lab": "lab-07-large-files",
        "diagram": "09-large-file-architecture",
    },
    {
        "id": "08",
        "slug": "08-esb",
        "title": "ESB and Traditional Enterprise Integration",
        "lessons": M08,
        "lab": None,
        "diagram": "07-esb-architecture",
    },
    {
        "id": "09",
        "slug": "09-esb-modernization",
        "title": "ESB Modernization",
        "lessons": M09,
        "lab": "lab-08-esb-modernization",
        "diagram": "08-esb-modernization",
    },
    {
        "id": "10",
        "slug": "10-patterns",
        "title": "Enterprise Integration Patterns",
        "lessons": M10,
        "lab": None,
        "diagram": "10-patterns",
    },
    {
        "id": "11",
        "slug": "11-resiliency",
        "title": "Reliability and Resiliency",
        "lessons": M11,
        "lab": "lab-11-chaos",
        "diagram": "11-resiliency",
    },
    {
        "id": "12",
        "slug": "12-security",
        "title": "Security",
        "lessons": M12,
        "lab": "lab-12-security",
        "diagram": "10-integration-security",
    },
    {
        "id": "13",
        "slug": "13-observability",
        "title": "Observability",
        "lessons": M13,
        "lab": "lab-13-observability",
        "diagram": "11-integration-observability",
    },
    {
        "id": "14",
        "slug": "14-architecture-decisions",
        "title": "Architecture Decision Making",
        "lessons": M14,
        "lab": None,
        "diagram": "14-decision-framework",
    },
    {
        "id": "15",
        "slug": "15-ai-agents",
        "title": "Integration Architecture for AI Agents",
        "lessons": M15,
        "lab": "lab-15-ai-agent",
        "diagram": "12-ai-agent-integration",
    },
]


def lesson_filename(lesson_id: str) -> str:
    return f"lesson-{lesson_id}.md"


def write_lessons() -> list[dict]:
    catalog = []
    total = 0
    for mod in MODULES:
        folder = ROOT / "modules" / mod["slug"] / "lessons"
        folder.mkdir(parents=True, exist_ok=True)
        entries = []
        for lesson in mod["lessons"]:
            name = lesson_filename(lesson["id"])
            path = folder / name
            path.write_text(render_lesson(lesson), encoding="utf-8")
            total += 1
            entries.append(
                {
                    "id": lesson["id"],
                    "title": lesson["title"],
                    "path": f"modules/{mod['slug']}/lessons/{name}",
                    "duration": lesson.get("duration", "25–35 minutes"),
                }
            )
        readme = [
            f"# Module {mod['id']} — {mod['title']}",
            "",
            f"**BayLearn · Enterprise Integration Architecture**  ",
            f"Lessons: {len(mod['lessons'])}",
            "",
            "Every lesson answers WHY, WHEN, and HOW. Pattern first. AWS second.",
            "",
            "## Lessons",
            "",
        ]
        for e in entries:
            readme.append(f"- [{e['id']} {e['title']}](lessons/{lesson_filename(e['id'])})")
        if mod["lab"]:
            readme += ["", f"**Lab:** [`labs/{mod['lab']}/`](../../labs/{mod['lab']}/)"]
        readme += ["", f"**Diagrams:** [`diagrams/{mod['diagram']}.md`](../../diagrams/{mod['diagram']}.md)", ""]
        (ROOT / "modules" / mod["slug"] / "README.md").write_text("\n".join(readme), encoding="utf-8")
        catalog.append(
            {
                "id": mod["id"],
                "slug": mod["slug"],
                "title": mod["title"],
                "lab": mod["lab"],
                "lessons": entries,
            }
        )
    print(f"Wrote {total} lessons across {len(MODULES)} modules")
    return catalog


def main() -> None:
    catalog = write_lessons()
    out = ROOT / "course-ui" / "js" / "catalog.js"
    out.parent.mkdir(parents=True, exist_ok=True)
    payload = {
        "courseId": "baylearn-eia-001",
        "title": "Enterprise Integration Architecture",
        "modules": catalog,
        "lessonCount": sum(len(m["lessons"]) for m in catalog),
        "moduleCount": len(catalog),
    }
    out.write_text(
        "window.EIA_CATALOG = " + json.dumps(payload, indent=2) + ";\n",
        encoding="utf-8",
    )
    print(f"Wrote {out}")


if __name__ == "__main__":
    main()
