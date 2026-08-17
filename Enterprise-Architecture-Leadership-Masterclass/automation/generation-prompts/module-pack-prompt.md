# Generation Prompt — Module Pack

Use this prompt after Phase 1 approval to generate one module at a time.

```text
You are acting as a senior enterprise architect, curriculum designer, AWS lab engineer,
technical instructor, and course-production specialist for BayLearn / BayAreaLa8s.

Generate the COMPLETE asset pack for Module {{MODULE_NUMBER}} only:

Title: {{MODULE_TITLE}}
Slug: {{MODULE_SLUG}}
Lab: {{LAB_TITLE}} ({{LAB_PATH}})
AWS lab: {{YES_NO}}

Follow:
- COURSE_BUILD_PLAN.md
- course-specification/* (especially northstar-case-study.md and content-standards.md)
- templates/module/*, templates/lab/*, templates/assessment/*
- assessments/rubrics/standard-architecture-rubric.md

Requirements for this module:
- Module overview, learning objectives, prerequisites
- 4 detailed lessons (use LESSON.template.md)
- Full instructor package (guide, speaking script, whiteboard, discussion,
  misconceptions, lab facilitation, reference solution, grading guide, slide notes)
- Slide outline 15–25 slides with speaker notes on every slide
- Lab with all required sections (use AWS_LAB.template.md if AWS)
- Assignment + rubric notes
- Quiz: 10 MCQ + 3 scenario + 2 discussion + answer key with explanations,
  difficulty tags, LO mapping, categories
- Workbook section, common mistakes, debrief questions
- LinkedIn promo + YouTube/Loom description
- Mermaid diagrams
- Update COURSE_MANIFEST.json statuses
- Write qa/module-{{MODULE_NUMBER}}-qa-report.md using QA_REPORT.template.md
- Validate internal links
- Do NOT generate other modules
- Do NOT put reference solutions in student paths
- Mark NorthStar as fictional
- Emphasize trade-offs, business alignment, security/cost/ops where relevant

After generation: stop and summarize files created + QA results.
```

## Module sequence

1. Module 01 — The Enterprise Architect’s Role  
2. Module 02 — Business Architecture and Capability Mapping  
3. Module 03 — Current-State Architecture Assessment *(include 40+ app CSV)*  
4. Module 04 — Target-State Architecture and Roadmaps → **Phase 2 checkpoint**  
5. Module 05 — Cloud and Platform Strategy *(Terraform)*  
6. Module 06 — Integration, Application, and Data Architecture *(Terraform)*  
7. Module 07 — Security, Risk, Compliance, and Resilience *(Terraform)*  
8. Module 08 — AI Strategy *(Bedrock lab)* → **Phase 3 checkpoint**  
9. Module 09 — Governance and Executive Communication  
10. Module 10 + Capstone → **Phase 4 checkpoint**
