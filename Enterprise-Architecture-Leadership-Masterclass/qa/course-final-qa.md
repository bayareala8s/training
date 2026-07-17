# Course Final QA — Ready to Teach

**Date:** 2026-07-15  
**Course:** Enterprise Architecture Leadership Masterclass  
**Verdict:** **READY TO TEACH**

---

## Definition of Done

| Criterion | Status |
| --------- | ------ |
| All 10 modules exist with lessons | Pass |
| Instructor guides + speaking scripts | Pass |
| Slide outlines with speaker notes | Pass |
| Labs with student instructions (10) | Pass |
| Quizzes + answer keys (10) | Pass |
| Assignments + rubrics | Pass |
| AWS Terraform labs 5–8 validate | Pass (`terraform validate`) |
| Cleanup scripts present | Pass |
| Capstone brief + rubric + presentation outline | Pass |
| BayLearn seed JSON validates | Pass |
| Student/instructor package separation | Pass (student ZIP excludes keys/solutions) |
| Application inventory dataset (50+ apps) | Pass |
| NorthStar labeled fictional | Pass |
| Instructor + student start guides | Pass |
| Packages built under `packages/` | Pass |

---

## Packages

| Package | Path |
| ------- | ---- |
| Student | `packages/student-course.zip` |
| Instructor | `packages/instructor-course.zip` |
| AWS labs | `packages/aws-labs.zip` |
| Capstone | `packages/capstone.zip` |
| BayLearn seed | `packages/baylearn-seed.zip` |

---

## How to start teaching (today)

1. Open [`INSTRUCTOR_START_HERE.md`](../INSTRUCTOR_START_HERE.md)
2. Schedule cohort using [`course-specification/teaching-calendar.md`](../course-specification/teaching-calendar.md)
3. Send welcome email from [`course-specification/email-templates.md`](../course-specification/email-templates.md)
4. Teach Week 1 from `instructor/guides/module-01/` + `instructor/scripts/module-01/speaking-script.md`
5. For Weeks 5–8, prep AWS accounts and run `infrastructure/terraform/environments/lab0X`

---

## Known operational notes

- Slide files are **outlines with speaker notes** (Markdown), ready to paste into PowerPoint/Google Slides with BayLearn navy/gold branding — not binary `.pptx` decks.
- `terraform validate` succeeds; live `apply` requires an AWS account, budgets, and (for Lab 8) Bedrock model access or documented mock mode.
- Formative quizzes by default; weight only if cohort policy changes.

---

## Sign-off

Course materials are sufficient to deliver a live BayLearn cohort without requiring additional content creation for the core 10-week path.
