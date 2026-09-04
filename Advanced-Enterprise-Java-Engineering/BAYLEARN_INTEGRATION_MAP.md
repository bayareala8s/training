# BayLearn Integration Map — Advanced Enterprise Java Engineering

**Version:** 1.0.0  
**Date:** 2026-09-03  
**Portal inspected:** `/Users/hbhadra/BayLearn-Portal`  
**Rule:** Reuse first. Additive optional fields and new routes only. Do not break the seven published courses.

This document lists the exact BayLearn types, routes, schemas, services, and UI that AEJE will reuse, and the new capabilities the spec still requires.

---

## 1. Integration principle

AEJE is a **new catalog course**, not a BayLearn redesign.

```text
This repo (curriculum + BayPay + labs + seed JSON)
        │
        ▼
BayLearn-Portal seed: aeje-course.ts + sync-aeje-catalog.ts
        │
        ▼
DynamoDB courses / sections / lessons / materials / assignments
        │
        ▼
Existing catalog, enroll, learn, progress, certificate UI
        │
        ▼
Optional Phase B components (quiz, incident, interview, portfolio)
   loaded only when AEJE lesson metadata asks for them
```

Existing courses keep their titles, UUIDs, seed files, progress math, and UI.

---

## 2. What will be reused (do not duplicate)

### 2.1 Shared types — `/Users/hbhadra/BayLearn-Portal/shared/src/types.ts`

| Type | Reuse |
|---|---|
| `Course` | New row; same shape |
| `CourseMetadata` | `catalogId`, `curriculumVersion`, `format`, effort hours, `prerequisites`, `learningOutcomes`, `audience`, `tags`, `technologies`, `repositoryUrl`, `certificateName`, `capstoneSummary`, `alignment` |
| `CoursePricing` / `PricingTier` | Flagship tier |
| `Section` / `SectionType` | `module` × 16, `capstone` × 1 |
| `Lesson` | Content, lab, quiz, and capstone lessons |
| `Material` / `MaterialType` | `md`, `png`, `jpg`, `zip` (labs/diagrams/code) |
| `Assignment` | Portfolio and capstone submissions |
| `Submission` / `SubmissionType` | `github_url`, `zip`, `pdf`, `diagram` — **schema exists, handlers do not** |
| `Enrollment` / `LessonProgress` | Unchanged progress model |
| `Certificate` | Unchanged PDF + S3 + DynamoDB record |
| `UserRole` | `student` / `instructor` / `admin` |

**Do not create parallel Course/Lesson types in this repo for the portal.** Curriculum JSON in `baylearn-seed/` is a build input to the portal seed, same as EIA.

### 2.2 Catalog and pricing

| File | Reuse / additive edit |
|---|---|
| `shared/src/catalog.ts` | **Append** AEJE to `CATALOG_COURSE_ORDER`, `CATALOG_COURSE_SEEDS`, `CATALOG_METADATA_BY_TITLE` |
| `shared/src/pricing.ts` | **Add** `COURSE_PRICING_BY_TITLE["Advanced Enterprise Java Engineering"]` |
| `shared/src/pricing.ts` `COURSE_BUNDLES` | **Do not change** until product recalculates the seven-course program |
| `frontend/scripts/fetch-catalog.mjs` | No change; rebuild frontend after sync |
| `frontend/src/generated/courses-catalog.json` | Regenerated at frontend build |
| `frontend/src/lib/catalog.ts` | No change |

Title string must match across catalog, pricing, and seed. Catalog lookup is by **title**, not slug.

### 2.3 Seed and sync

| File | Role |
|---|---|
| `backend/src/seed/eft-course.ts` `SeedCourse` | Interface to implement |
| `backend/src/seed/eia-course.ts` | Structural template (modules + lab lessons + capstone section) |
| `backend/src/seed/catalog-sync-utils.ts` | `syncCourseCatalog`, `insertCourseContent`, `deleteCourseContent` |
| `backend/src/seed/sync-eia-catalog.ts` | Template for `sync-aeje-catalog.ts` |
| `backend/src/seed/courses.ts` | **Append** `aejeSeedCourse` only |
| `backend/src/seed/index.ts` | Picks up aggregator; no special case |
| `backend/src/lib/curriculum-url.ts` | GitHub raw fallback; requires `metadata.repositoryUrl` in `.../tree/{branch}/{repoRoot}` form |

**New portal files (additive):**

- `backend/src/seed/aeje-course.ts`
- `backend/src/seed/sync-aeje-catalog.ts`
- npm scripts in root and `backend/package.json`: `sync-aeje-catalog`

**Do not edit:** `eft-course.ts`, `terraform-course.ts`, `bedrock-course.ts`, `data-engineering-course.ts`, `microservices-course.ts`, `ea-leadership-course.ts`, `eia-course.ts`, `interview-accelerator-course.ts` beyond the aggregator import list.

**Must-fix when AEJE uses assignments:** `insertCourseContent()` currently does not persist `seedLesson.assignment`. Add that write. Deletion already removes assignments. Existing courses without assignments are unaffected.

### 2.4 API routes — `backend/src/router.ts`

Reuse as-is:

| Method | Path | AEJE use |
|---|---|---|
| GET | `/courses` | Catalog |
| GET | `/courses/:id` | Detail |
| GET | `/courses/:id/full` | Learn tree |
| POST | `/courses/:id/enroll` | Enrollment |
| GET | `/courses/:id/enrollment` | Learn + dashboard |
| GET | `/enrollments` | Dashboard |
| POST | `/enrollments/inquiry` | Enterprise inquiry |
| POST | `/progress/complete` | Mark lesson done |
| POST | `/progress/uncomplete` | Undo |
| GET | `/courses/:id/progress` | Progress list |
| GET | `/lessons/:id/materials` | Material list |
| GET | `/materials/:id/download` | S3 or GitHub raw |
| GET | `/dashboard/student` | Enrollments + certs |
| GET | `/certificates` | Student certs |
| POST | `/certificates/issue` | Instructor/admin issue |
| GET | `/certificates/:id/download` | PDF |
| GET | `/users/me` | Auth profile |

No change to Cognito JWT validation (`backend/src/lib/auth.ts`) or role mapping.

### 2.5 Progress and certificates

| File | Reuse |
|---|---|
| `backend/src/lib/progress.ts` | Same formula: completed lessons / total lessons |
| `backend/src/handlers/progress.ts` | Same complete/uncomplete |
| `backend/src/lib/certificate.ts` | Same PDF layout and `BL-{timestamp}-{uuid8}` numbers |
| `backend/src/handlers/certificates.ts` | Same issue/list/download |

AEJE will have more lessons than most courses. That only changes the denominator. Do **not** introduce weighted progress in shared code.

Known issue (do not “fix” as part of AEJE unless separately approved): `issueCertificate` emails the **issuer**, not the student. Out of scope unless product asks.

Optional additive: if `course.metadata.autoIssueCertificate === true` and progress hits 100%, call `generateCertificate`. Other courses omit the flag.

### 2.6 DynamoDB — `infrastructure/terraform/dynamodb.tf`

Reuse tables: `courses`, `sections`, `lessons`, `materials`, `assignments`, `submissions`, `enrollments`, `progress`, `certificates`, `users`, `announcements`.

`submissions` is unused by handlers today. Prefer wiring it before creating a portfolio table.

New tables only for Phase B quiz attempts / incident sessions / interview attempts — prefixed `baylearn-*`, created with Terraform, unused by existing courses.

### 2.7 Frontend routes — `frontend/src/app`

| Route | File | AEJE |
|---|---|---|
| `/` | `page.tsx` | Catalog card via `buildCatalogCourses` |
| `/courses` | `courses/page.tsx` | Listing + category filter |
| `/courses/[courseId]` | `courses/[courseId]/page.tsx` | Syllabus accordion |
| `/enroll/[courseId]` | `enroll/[courseId]/page.tsx` | Enroll / inquiry |
| `/learn/[courseId]` | `learn/[courseId]/page.tsx` | Download materials, mark complete |
| `/dashboard` | `dashboard/page.tsx` | Progress + certificates |
| `/pricing` | `pricing/page.tsx` | Flagship price |
| `/login`, `/register` | existing | Unchanged |
| `/admin`, `/admin/builder` | existing | Not used to author AEJE |

Course IDs are UUIDs assigned at first sync. Seed JSON in this repo uses stable slugs (`baylearn-aeje-001`, `module-01`, `BUILD-101`). The portal seed maps slugs → UUIDs.

### 2.8 Design system and UI components

Reuse tokens and components. Do not introduce a second theme.

| Asset | Path |
|---|---|
| Tokens | `frontend/src/app/globals.css` (`--ba-navy`, `--ba-teal`, `--ba-gold`, `--ba-slate`, `--ba-border`) |
| Brand copy | `frontend/src/lib/brand.ts` |
| Button / Card / Badge / BadgeMuted / Input / Progress | `frontend/src/components/ui/*` |
| Header / Footer / PageHeader / AuthLayout | `frontend/src/components/layout/*` |
| CourseCard / CoursePricing / CourseCatalogDetails / CategoryFilter | `frontend/src/components/courses/*` |
| Paths (trailing slash for static export) | `frontend/src/lib/paths.ts` |

**Badge today:** category + level only. Phase B may add a `LabTypeBadge` used only when `lesson.labType` is set.

### 2.9 Auth

Cognito user pool and groups unchanged. AEJE students are `student`. Instructors issue certificates as today. No new IAM roles for the portal itself.

Student AWS lab accounts are **outside** BayLearn auth (same as EIA). Lab READMEs document sandbox IAM separately.

### 2.10 Material and diagram delivery

- `MaterialType` already includes `md`, `png`, `jpg`, `zip`
- Diagrams are materials (download), not an in-app Mermaid renderer
- EIA `course-ui` is a **course-local** player, not a portal feature — AEJE may ship `course-ui/` the same way for rich incident/interview UX if Phase B is delayed

### 2.11 AWS lab content pattern (not a portal engine)

Reuse EIA lab conventions in markdown/IaC:

- `labs/{id}/README.md` with cost, cleanup, validation
- `terraform/labs/{id}/` + `scripts/lab_up.sh` / `lab_down.sh` style helpers
- Seed lesson title may include `(AWS)` when `awsLab: true`
- Low-cost default; destroy after lab

There is no lab autograder in the portal. Validation scripts stay in this repo (`qa/`, `scripts/`).

---

## 3. New capabilities required by the spec

Add only these, and only as optional/opt-in.

### 3.1 `labType` metadata and badges — **required for spec UX, optional for MVP**

**Why:** Spec §23 requires lab types and badges. Portal has no `Lesson` extras.

**Additive shared fields (all optional):**

```typescript
export type LessonKind = "lesson" | "lab" | "quiz" | "capstone" | "interview";

export type LabType =
  | "BUILD"
  | "ARCHITECT"
  | "MODERNIZE"
  | "BREAK/FIX"
  | "INCIDENT"
  | "SECURITY"
  | "PERFORMANCE"
  | "COST"
  | "AI"
  | "INTERVIEW"
  | "CAPSTONE";

// on Lesson
lessonKind?: LessonKind;
labType?: LabType;
labId?: string;
```

**UI:** `LabTypeBadge` on learn + course detail when `labType` is present.

**Compatibility:** Existing lessons omit fields → current UI.

**Category change:** Not required. Recommended catalog category is `microservices`. Adding `java` would also require `category-filter.tsx` and `admin/builder/page.tsx`. Defer unless product wants a dedicated filter chip.

### 3.2 Progressive incident simulator — **new**

**Why:** Spec §24. No portal types, routes, or UI.

**Content (this repo, always):** `incidents/**` timelines and gated evidence.

**Portal (Phase B, additive):**

| Piece | Notes |
|---|---|
| Types | `Incident`, `IncidentEvidence`, `IncidentSession` |
| Routes | `GET /incidents/:incidentId`, `POST /incidents/:incidentId/sessions`, `POST /sessions/:id/request-evidence`, `PUT /sessions/:id/worksheet`, `POST /sessions/:id/score` |
| UI | `IncidentSimulator` on learn page when lesson has `labType === "INCIDENT"` and an incident id |
| Scoring | Spec weights; lucky guess cannot max Diagnostic method or Efficiency |

Existing courses never reference incident IDs → they never load the component.

### 3.3 Interview simulator — **new**

**Why:** Spec §25. Interview Accelerator is content-only and `published: false`.

**Content (this repo):** `interview-bank/` with exactly 100 records.

**Portal (Phase B):**

| Piece | Notes |
|---|---|
| Types | `InterviewQuestion`, `InterviewAttempt` |
| Routes | `GET /interview-questions`, `POST /interview/sessions`, mode-specific submit |
| UI | Modes: Practice, Timed, Rapid Fire, Troubleshooting, System Design, Full Mock Loop |
| Answers | Engineer / Senior / Staff / Principal panes — not a single key |

Do not reuse Interview Accelerator seed or launch flags. AEJE is a published flagship course with its own bank.

### 3.4 Quiz engine — **new (spec §3, §29, §32)**

**Today:** EIA `baylearn-seed/quizzes.json` is `[]`. Quizzes are markdown materials.

**Phase A:** `course/quizzes/Q-01.json` … `Q-16.json` as downloadable materials + instructor explanations.

**Phase B:**

| Piece | Notes |
|---|---|
| Types | `Quiz`, `QuizQuestion`, `QuizAttempt` |
| Tables | `baylearn-quizzes`, `baylearn-quiz-attempts` |
| Routes | `GET /lessons/:id/quiz`, `POST /quizzes/:id/attempt` |
| UI | `QuizPlayer` with answer explanations after submit |

Do not store quiz scores on `Enrollment.progress`.

### 3.5 Portfolio artifact tracking — **partially exists**

| Exists | Missing |
|---|---|
| `Assignment`, `Submission` types | API handlers |
| `assignments` and `submissions` tables | Learn-page submit UI |
| `SubmissionType` including `diagram` | Instructor review UI |

**Plan:** implement handlers + a small submit form on lessons that have assignments. No new table unless review workflow outgrows `Submission`.

### 3.6 Auto-certificate — **optional flag**

`CourseMetadata.autoIssueCertificate?: boolean` (additive). Only AEJE sets it. Certificate PDF, numbering, and download stay the same.

---

## 4. Proposed Phase B routes (do not add until approved)

These routes must 404-or-absent on environments that have not deployed Phase B. Existing clients never call them.

```text
GET  /lessons/{lessonId}/quiz
POST /quizzes/{quizId}/attempt
GET  /incidents/{incidentId}
POST /incidents/{incidentId}/sessions
POST /incident-sessions/{sessionId}/evidence/{evidenceId}
PUT  /incident-sessions/{sessionId}/worksheet
POST /incident-sessions/{sessionId}/score
GET  /interview-questions?domain=&mode=
POST /interview/sessions
POST /interview/sessions/{id}/answer
POST /assignments/{assignmentId}/submissions
GET  /courses/{courseId}/portfolio
```

---

## 5. Frontend component plan

| Component | Action |
|---|---|
| `CourseCard` | Reuse. AEJE appears after catalog append. |
| `CategoryFilter` | Reuse. AEJE under Microservices unless `java` is added. |
| `CourseCatalogDetails` | Reuse metadata sections. |
| `CoursePricingDisplay` | Reuse flagship pricing. |
| Learn page accordion | Reuse downloads + complete. |
| `LabTypeBadge` | **New**, render if `labType` set. |
| `QuizPlayer` | **New**, mount if quiz id present. |
| `IncidentSimulator` | **New**, mount if incident id present. |
| `InterviewSimulator` | **New**, Module 16. |
| `AssignmentSubmit` | **New**, mount if assignment present. |
| `course-ui/` in this repo | Optional local player (EIA pattern) if Phase B slips. |

No change to landing, login, register, or admin builder beyond an optional later `java` category option.

---

## 6. Seed payload mapping

| Curriculum object | Portal object |
|---|---|
| Course `baylearn-aeje-001` | `Course` + metadata |
| Module 1–16 | `Section` `type: "module"` order 1–16 |
| Capstones group | `Section` `type: "capstone"` order 17 |
| Coverage topic | `Lesson` `lessonKind: "lesson"` |
| Lab | `Lesson` `lessonKind: "lab"` + `labType` + `labId` |
| Module quiz | `Lesson` `lessonKind: "quiz"` |
| Capstone | `Lesson` `lessonKind: "capstone"` `labType: "CAPSTONE"` |
| Lesson markdown | `Material` `fileType: "md"` `s3Key: curriculum/advanced-enterprise-java/...` |
| Diagram PNG | `Material` `fileType: "png"` |
| Lab zip / starter | `Material` `fileType: "zip"` |
| Portfolio / capstone | `Assignment` on that lesson |

S3 key prefix: `curriculum/advanced-enterprise-java/`.

GitHub fallback requires:

```text
metadata.repositoryUrl = https://github.com/{org}/{repo}/tree/{branch}/{root}
```

Example if this repo is copied into the training monorepo:

```text
https://github.com/bayareala8s/training/tree/main/Advanced-Enterprise-Java-Engineering
```

---

## 7. Published catalog that must keep working

| Title | catalogId | UUID (prod catalog snapshot) |
|---|---|---|
| Self-Serve Enterprise File Transfer on AWS | `baylearn-mft-aws-001` | `bb3748b8-18f9-4aa9-bbeb-a20f94ce4047` |
| Terraform for Real Enterprises | `baylearn-tf-enterprise-001` | `3f787c97-9ebd-4164-bab6-193232f0c2e8` |
| AI Automation & Agents with AWS Bedrock | `baylearn-bedrock-ai-001` | `9d6c8974-eab4-45b3-aa0d-a058b9cda228` |
| Cloud-Native Data Engineering on AWS | `baylearn-data-aws-001` | `873ba8c3-458f-4a9e-843c-0284bc71b35e` |
| Production-Grade Microservices on AWS | `baylearn-ms-aws-001` | `523d1e6a-6c62-4006-bc22-ec583b939495` |
| Enterprise Architecture Leadership Masterclass | `baylearn-ea-leadership-001` | `43a7a641-eac5-41f3-ae53-95a87eaf1197` |
| Enterprise Integration Architecture | `baylearn-eia-001` | `aee8019c-24c1-4043-ba39-e00f8bb20838` |

Draft, not in `CATALOG_COURSE_ORDER`: Principal & Solutions Architect Interview Accelerator (`baylearn-arch-interview-001`).

**Regression checks after AEJE sync + frontend rebuild:**

- All seven titles still in catalog order
- Existing UUIDs unchanged (sync updates by title; must not recreate those courses)
- Enroll + learn still work on at least one existing course
- Pricing table still shows seven (or eight if AEJE is appended) without bundle math errors
- Category filters still match existing categories

---

## 8. PAKS integration (supplemental)

PAKS is `/Users/hbhadra/Downloads/Principal-Architect-Knowledge-System`. It is **not** loaded by BayLearn. Host when a cohort has a login: [paks.bayareala8s.com](https://paks.bayareala8s.com). Curated file paths and policy: [PAKS_LINKS.md](PAKS_LINKS.md). Checker: `qa/check_paks_links.py`.

Lessons stand alone. A missing PAKS login is not a blocker.

| AEJE area | Curated PAKS deep dives (optional) |
|---|---|
| M1 / M4 transactions | `docs/09-transactions/overview.md` |
| M2 concurrency / memory | `docs/01-computer-architecture/memory-ordering-and-concurrency.md`, `docs/02-operating-systems/processes-threads-and-scheduling.md` |
| M3 APIs / services | `docs/15-api-and-integration-architecture/overview.md`, `docs/14-microservices/overview.md` |
| M5 WebSphere ND (operate-to-leave) | `docs/12-messaging-and-streaming/overview.md`, `docs/27-production-failures/overview.md` |
| M6 Liberty | `docs/14-microservices/service-decomposition-and-ddd.md` |
| M7 JVM internals | `docs/01-computer-architecture/cpu-and-memory-fundamentals.md` |
| M8 JVM troubleshooting | `docs/27-production-failures/failure-analysis-methodology.md` |
| M9–M10 containers / K8s | `docs/17-kubernetes-and-platform-engineering/overview.md`, `kubernetes-architecture.md`, `platform-engineering-and-gitops.md` |
| M11–M12 AWS / IaC | `docs/16-cloud-architecture/aws-fundamentals.md`, `docs/26-cost-and-finops/overview.md`, `platform-engineering-and-gitops.md` |
| M13 observability / RCA | `docs/19-observability/overview.md`, `docs/27-production-failures/overview.md` |
| M14 security / HA / DR | `docs/20-security/overview.md`, `docs/18-reliability-and-resilience/overview.md`, `docs/16-cloud-architecture/multi-region-architecture.md` |
| M15 AI ops | `docs/23-agentic-ai-architecture/agent-governance-and-safety.md` |
| M16 interview | `docs/24-system-design/overview.md`, `docs/30-mock-interviews/overview.md`, `docs/25-architecture-leadership/overview.md` |

---

## 9. Backward-compatibility contract

A portal PR for AEJE is acceptable only if:

1. No existing course seed file changes except `courses.ts` import/array append.
2. Shared type changes are optional fields or new exported types — no required new fields on `Course`, `Lesson`, or `Enrollment`.
3. `CATALOG_COURSE_ORDER` **appends** AEJE; it does not reorder existing titles.
4. `COURSE_BUNDLES` is unchanged unless product updates pricing copy and totals.
5. Progress formula is unchanged.
6. New UI mounts only when AEJE-specific metadata is present.
7. New API routes do not replace existing paths.
8. Terraform for the **portal** stack does not require recreate of Cognito, CloudFront, or existing DynamoDB tables. New tables are additive.
9. Frontend static export and trailing-slash paths stay as they are.
10. After deploy, the seven published courses remain enrollable and their materials still download.

---

## 10. What we will not do

- Redesign BayLearn navigation, auth, or landing page
- Replace markdown-download learn UX for all courses
- Require WebSphere ND or a paid OpenShift cluster in the portal
- Put instructor solutions in student-facing materials
- Use real employer logs, runbooks, or architectures
- Treat Bedrock output as a proven root cause
- Add AEJE to the Professional Engineer Program bundle without a pricing review
- Author the course through `/admin/builder`

---

## 11. Two-repo checklist (when Stage 2+ is approved)

**This repo**

- [x] Curriculum tree per spec §31
- [x] `baylearn-seed/*.json` aligned to `COURSE_MANIFEST.json`
- [x] Reference app, labs, incidents, diagrams, interview bank

**BayLearn-Portal (authored; DynamoDB sync not run)**

- [x] Catalog + pricing append
- [x] `aeje-course.ts` + sync script
- [x] Assignment persist fix in `insertCourseContent`
- [ ] Optional Phase B types/routes/UI
- [x] Frontend rebuild and catalog smoke test
- [x] Regression on one existing published course (EFT still published)
- [x] `npm run sync-aeje-catalog` against baylearn-prod (`us-west-2`)
