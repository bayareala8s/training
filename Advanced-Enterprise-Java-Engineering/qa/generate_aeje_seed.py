#!/usr/bin/env python3
"""Generate baylearn-seed JSON and BayLearn Portal aeje-course.ts from COURSE_MANIFEST.json."""
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PORTAL = Path("/Users/hbhadra/BayLearn-Portal")
PREFIX = "curriculum/advanced-enterprise-java"
TITLE = "Advanced Enterprise Java Engineering"


def ts_str(value: object) -> str:
    return json.dumps(value, ensure_ascii=False)


def material(title: str, file_type: str, rel: str, order: int) -> dict:
    return {
        "title": title,
        "fileType": file_type,
        "s3Key": f"{PREFIX}/{rel}",
        "order": order,
    }


def main() -> None:
    data = json.loads((ROOT / "COURSE_MANIFEST.json").read_text())
    diagrams = {d["id"]: d for d in data["diagrams"]}
    portfolio_sources = {item["source"] for item in data["portfolioArtifacts"]}
    quizzes = {q["id"]: q for q in data["quizzes"]}

    seed_lessons: list[dict] = []
    seed_assignments: list[dict] = []
    seed_modules: list[dict] = []
    ts_sections: list[str] = []

    for mod in data["modules"]:
        lessons_ts: list[str] = []
        order = 0
        for idx, lesson in enumerate(mod["lessons"]):
            order += 1
            materials = [
                material(
                    Path(lesson["path"]).stem,
                    "md",
                    lesson["path"],
                    1,
                )
            ]
            next_order = 2
            if idx == 0:
                materials.append(
                    material("Module overview", "md", mod["overviewPath"], next_order)
                )
                next_order += 1
                materials.append(
                    material("Getting started", "md", "GETTING_STARTED.md", next_order)
                )
                next_order += 1
            for did in mod.get("diagramIds") or []:
                diagram = diagrams.get(did)
                if diagram and diagram.get("mapsTo") == lesson["id"]:
                    materials.append(
                        material(diagram["title"], "png", diagram["png"], next_order)
                    )
                    next_order += 1
            seed_lessons.append(
                {
                    "id": lesson["id"],
                    "moduleId": mod["id"],
                    "title": lesson["title"],
                    "kind": "lesson",
                    "path": lesson["path"],
                    "order": order,
                }
            )
            lessons_ts.append(
                lesson_ts(
                    title=lesson["title"],
                    order=order,
                    minutes=lesson.get("durationMinutes") or 30,
                    description=f"{mod['title']} — {lesson['title']}",
                    kind="lesson",
                    materials=materials,
                )
            )

        for lab in mod["labs"]:
            order += 1
            materials = [material(f"{lab['id']} README", "md", lab["path"], 1)]
            assignment = None
            if lab["id"] in portfolio_sources:
                assignment = {
                    "title": f"Portfolio: {lab['title']}",
                    "description": (
                        f"Submit the {mod['portfolioArtifact']} from {lab['id']}. "
                        "GitHub URL, zip, PDF, or diagram. Synthetic BayPay names only."
                    ),
                    "maxScore": 100,
                }
                seed_assignments.append(
                    {"id": lab["id"], "title": assignment["title"], "lessonTitle": lab["title"]}
                )
            aws = bool(lab.get("awsLab"))
            seed_lessons.append(
                {
                    "id": lab["id"],
                    "moduleId": mod["id"],
                    "title": lab["title"],
                    "kind": "lab",
                    "path": lab["path"],
                    "order": order,
                    "labType": lab["labType"],
                    "awsLab": aws,
                }
            )
            lessons_ts.append(
                lesson_ts(
                    title=f"Lab: {lab['id']} — {lab['title']}" + (" (AWS)" if aws else ""),
                    order=order,
                    minutes=180 if aws else 90,
                    description=lab["title"],
                    kind="lab",
                    lab_type=lab["labType"],
                    lab_id=lab["id"],
                    materials=materials,
                    assignment=assignment,
                )
            )

        quiz = quizzes[mod["quizId"]]
        order += 1
        seed_lessons.append(
            {
                "id": quiz["id"],
                "moduleId": mod["id"],
                "title": quiz["title"],
                "kind": "quiz",
                "path": quiz["studentView"],
                "order": order,
            }
        )
        lessons_ts.append(
            lesson_ts(
                title=f"Quiz: {quiz['title']}",
                order=order,
                minutes=20,
                description=f"Eight-question knowledge check for {mod['title']}. Unscored in Phase A.",
                kind="quiz",
                materials=[
                    material(f"{quiz['id']} student view", "md", quiz["studentView"], 1),
                ],
            )
        )

        seed_modules.append(
            {
                "id": mod["id"],
                "title": f"Module {mod['number']}: {mod['title']}",
                "order": mod["number"],
                "lessonCount": order,
            }
        )
        ts_sections.append(
            section_ts(
                title=f"Module {mod['number']}: {mod['title']}",
                section_type="module",
                order=mod["number"],
                description=mod.get("theme") or mod["title"],
                lessons=lessons_ts,
            )
        )

    cap_lessons_ts: list[str] = []
    for cap in data["capstones"]["items"]:
        assignment = {
            "title": f"Capstone: {cap['title']}",
            "description": cap["summary"],
            "maxScore": 100,
        }
        seed_assignments.append(
            {"id": cap["id"], "title": assignment["title"], "lessonTitle": cap["title"]}
        )
        seed_lessons.append(
            {
                "id": cap["id"],
                "moduleId": "capstones",
                "title": cap["title"],
                "kind": "capstone",
                "path": cap["path"],
                "order": cap["order"],
                "labType": "CAPSTONE",
            }
        )
        cap_lessons_ts.append(
            lesson_ts(
                title=cap["title"],
                order=cap["order"],
                minutes=480,
                description=cap["summary"],
                kind="capstone",
                lab_type="CAPSTONE",
                lab_id=cap["id"],
                materials=[material(f"{cap['id']} README", "md", cap["path"], 1)],
                assignment=assignment,
            )
        )

    ts_sections.append(
        section_ts(
            title="Capstones: BayPay Enterprise Delivery",
            section_type="capstone",
            order=17,
            description="Build, modernize, cloud, and a progressive SEV-1.",
            lessons=cap_lessons_ts,
        )
    )

    expected = data["counts"]["portalLessonsEstimated"]
    if len(seed_lessons) != expected:
        raise SystemExit(
            f"portal lesson count {len(seed_lessons)} != {expected}"
        )

    seed_dir = ROOT / "baylearn-seed"
    seed_dir.mkdir(exist_ok=True)
    (seed_dir / "course.json").write_text(
        json.dumps(
            {
                "catalogId": data["course"]["catalogId"],
                "title": TITLE,
                "curriculumPrefix": PREFIX,
                "portalLessonCount": len(seed_lessons),
            },
            indent=2,
        )
        + "\n"
    )
    (seed_dir / "modules.json").write_text(json.dumps(seed_modules, indent=2) + "\n")
    (seed_dir / "lessons.json").write_text(json.dumps(seed_lessons, indent=2) + "\n")
    (seed_dir / "quizzes.json").write_text(
        json.dumps(
            [{"id": q["id"], "title": q["title"], "path": q["studentView"]} for q in data["quizzes"]],
            indent=2,
        )
        + "\n"
    )
    (seed_dir / "assignments.json").write_text(json.dumps(seed_assignments, indent=2) + "\n")

    ts = render_ts(",\n".join(ts_sections), len(seed_lessons))
    out = PORTAL / "backend/src/seed/aeje-course.ts"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(ts)
    print(f"wrote {out} ({len(seed_lessons)} lessons, {len(seed_assignments)} assignments)")
    print(f"wrote {seed_dir}")


def lesson_ts(
    *,
    title: str,
    order: int,
    minutes: int,
    description: str,
    kind: str,
    materials: list[dict],
    lab_type: str | None = None,
    lab_id: str | None = None,
    assignment: dict | None = None,
) -> str:
    extra = f"        lessonKind: {ts_str(kind)},\n"
    if lab_type:
        extra += f"        labType: {ts_str(lab_type)},\n"
    if lab_id:
        extra += f"        labId: {ts_str(lab_id)},\n"
    mats = ",\n".join(
        "          {\n"
        f"            title: {ts_str(m['title'])},\n"
        f"            fileType: {ts_str(m['fileType'])} as MaterialType,\n"
        f"            s3Key: {ts_str(m['s3Key'])},\n"
        f"            order: {m['order']},\n"
        "          }"
        for m in materials
    )
    assign = ""
    if assignment:
        assign = (
            ",\n          assignment: {\n"
            f"            title: {ts_str(assignment['title'])},\n"
            f"            description: {ts_str(assignment['description'])},\n"
            f"            maxScore: {assignment['maxScore']},\n"
            "          }"
        )
    return (
        "        {\n"
        "          lesson: {\n"
        f"            title: {ts_str(title)},\n"
        f"            order: {order},\n"
        f"            durationMinutes: {minutes},\n"
        f"            description: {ts_str(description)},\n"
        f"{extra}"
        "          },\n"
        "          materials: [\n"
        f"{mats}\n"
        "          ]"
        f"{assign}\n"
        "        }"
    )


def section_ts(
    *,
    title: str,
    section_type: str,
    order: int,
    description: str,
    lessons: list[str],
) -> str:
    return (
        "    {\n"
        "      section: {\n"
        f"        title: {ts_str(title)},\n"
        f"        type: {ts_str(section_type)} as const,\n"
        f"        order: {order},\n"
        f"        description: {ts_str(description)},\n"
        "      },\n"
        "      lessons: [\n"
        + ",\n".join(lessons)
        + "\n      ],\n"
        "    }"
    )


def render_ts(sections: str, lesson_count: int) -> str:
    return f'''import type {{ CourseMetadata, MaterialType }} from "@baylearn/shared";
import {{
  COURSE_PRICING_BY_TITLE,
  buildCoursePricing,
}} from "@baylearn/shared";
import type {{ SeedCourse }} from "./eft-course";

export const AEJE_COURSE_TITLE = {ts_str(TITLE)};

export const AEJE_LEGACY_TITLES = [AEJE_COURSE_TITLE];

export const AEJE_REPOSITORY_URL =
  "https://github.com/bayareala8s/training/tree/main/Advanced-Enterprise-Java-Engineering";

/** Portal lessons = 102 content + 68 labs + 16 quizzes + 4 capstones = {lesson_count}. */
export const AEJE_PORTAL_LESSON_COUNT = {lesson_count};

export const aejeMetadata: CourseMetadata = {{
  catalogId: "baylearn-aeje-001",
  curriculumVersion: "1.0.0",
  format: "Instructor-led, hybrid, or self-paced with labs",
  effortHoursMin: 90,
  effortHoursMax: 120,
  certificateName:
    "BayLearn Certificate of Completion: Advanced Enterprise Java Engineering",
  repositoryUrl: AEJE_REPOSITORY_URL,
  alignment:
    "BayPay Financial Services is a fictional payments company. Traditional WebSphere ND is the source estate to leave, not a greenfield target. Pattern first: build, modernize, deploy, diagnose, operate.",
  audience: [
    "Java engineers",
    "Senior software engineers",
    "Platform, DevOps and cloud engineers",
    "Technical leads",
    "Staff and principal engineer candidates",
    "Architects deepening Java-platform knowledge",
  ],
  prerequisites: [
    "Working Java knowledge",
    "Git",
    "Basic Linux",
    "REST and API fundamentals",
    "Basic cloud concepts",
  ],
  learningOutcomes: [
    "Design and implement a production-shaped Java 21 / Spring Boot payment service",
    "Read and leave a fictional WebSphere ND cell without recommending a new one",
    "Diagnose JVM, container, and AWS failures from evidence, not lucky guesses",
    "Apply Fargate-first AWS design with cost, cleanup, and terraform validate",
    "Operate to SLOs and write an RCA that separates evidence from hypothesis",
    "Evaluate AI ops output without treating it as a proven root cause",
    "Answer staff/principal interview prompts with trade-offs and BayPay names",
    "Deliver four capstones: build, modernize, cloud, and a progressive SEV-1",
  ],
  tags: [
    "Enterprise Java",
    "Spring Boot",
    "WebSphere",
    "JVM",
    "Kubernetes",
    "AWS",
    "Terraform",
    "Observability",
  ],
  technologies: [
    "Java 21",
    "Spring Boot",
    "Jakarta EE",
    "WebSphere ND",
    "WebSphere Liberty",
    "JVM",
    "Docker",
    "Kubernetes",
    "OpenShift",
    "AWS",
    "Terraform",
    "Ansible",
    "CI/CD",
  ],
  capstoneSummary:
    "Build a list-by-customer payment API, leave BayPayCell on paper, design Fargate in us-west-2 (terraform validate bar), and run a gated SEV-1. Pass requires labs and capstones, not lesson-complete alone.",
}};

const p = COURSE_PRICING_BY_TITLE[AEJE_COURSE_TITLE];

export const aejeSeedCourse: SeedCourse = {{
  course: {{
    title: AEJE_COURSE_TITLE,
    description:
      "From legacy Java to cloud-native production platforms — Java 21, Spring Boot, WebSphere ND literacy, JVM diagnostics, containers, AWS Fargate, Terraform, observability, and a BayPay SEV-1. 16 weeks, 68 labs, 4 capstones. Offered by BayAreaLa8s on BayLearn.",
    price: p.liveCohortCents,
    pricing: buildCoursePricing(p),
    duration: "16 weeks (90–120 hours)",
    level: "advanced",
    category: "microservices",
    instructor: "BayAreaLa8s Team",
    published: true,
    metadata: aejeMetadata,
  }},
  sections: [
{sections}
  ],
}};
'''


if __name__ == "__main__":
    main()
