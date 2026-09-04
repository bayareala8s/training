# Advanced Enterprise Java Engineering — Course Implementation Plan

**Version:** 1.0.0  
**Date:** 2026-09-03  
**Stage:** 14 — Final validation complete; portal seed authored (DynamoDB sync not run)  
**Source spec:** `COURSE_MASTER_SPEC.md`  
**Companion artifacts:** `COURSE_MANIFEST.json`, `BAYLEARN_INTEGRATION_MAP.md`, `COURSE_QA_REPORT.md`  
**Platform inspected:** `/Users/hbhadra/BayLearn-Portal` (BayLearn Portal v2.0.0)  
**Closest existing course pattern:** Enterprise Integration Architecture (`baylearn-eia-001`)

This plan maps every requirement in the master specification to BayLearn. Stages 1–14 are implemented. Portal seed files are authored. Live DynamoDB sync is not started.

---

## 1. Inspection summary

BayLearn is a serverless LMS: CloudFront + S3 frontend, Cognito auth, API Gateway + Lambda, DynamoDB, S3 materials/certificates, SES email. Courses are **not** authored in the portal. They are authored as curriculum repositories, then registered through TypeScript seed files and DynamoDB sync scripts.

### What BayLearn already does well

| Capability | How it works today |
|---|---|
| Catalog cards, pricing, bundles | `shared/src/catalog.ts`, `shared/src/pricing.ts`, `frontend/src/components/courses/*` |
| Auth and roles | Cognito groups `student` / `instructor` / `admin` |
| Course tree | `Course → Section → Lesson → Material` (+ optional `Assignment`) |
| Progress | Manual “Mark Complete”; percent = completed lessons / total lessons |
| Material delivery | S3 presigned URL, then GitHub raw fallback via `metadata.repositoryUrl` |
| Certificates | Manual admin/instructor issue; PDF via pdfkit to S3 |
| AWS lab content pattern | Seed `awsLab` flag, lab README + Terraform, cost/cleanup in markdown |
| Design system | `--ba-navy`, `--ba-teal`, `--ba-gold`, DM Sans, Badge/Card/Button/Progress |

### What BayLearn does **not** have (required by this course)

| Spec requirement | Portal reality | Plan |
|---|---|---|
| Native quiz engine | Quizzes are markdown downloads | Additive quiz types + APIs; Phase A ships markdown quizzes |
| Lab type badges | Category + level badges only | Optional `labType` on `Lesson`; existing courses omit it |
| Progressive incident simulator | None | New optional routes/UI; content-first evidence packs in this repo |
| Interview simulator | Interview Accelerator is markdown + assignments | New optional simulator; 100-question bank lives in this repo |
| Portfolio artifact tracking | No store; `submissions` table exists with **zero handlers** | Wire existing Assignment/Submission first |
| Auto-certificate on completion | Manual issue only | Metadata-gated auto-issue for this course only |
| In-lesson markdown renderer | Learn page downloads files | Keep downloads; optional course-ui player like EIA |
| `java` course category | Enum is cloud/ai/devops/data-engineering/microservices/architecture | **Do not add a category in Stage 1.** Use `microservices` unless product asks for `java` |

### Closest reuse targets

- **Seed/sync:** EIA (`backend/src/seed/eia-course.ts`, `sync-eia-catalog.ts`)
- **AWS lab README shape:** EIA `labs/lab-02-api/README.md` (scenario, cost, validation, cleanup)
- **Interview content:** Principal & Solutions Architect Interview Accelerator (draft, not in public catalog order)
- **Standalone player:** EIA `course-ui/` if portal interactivity is not ready
- **PAKS deep dives:** `/Users/hbhadra/Downloads/Principal-Architect-Knowledge-System` (supplemental only)

---

## 2. Course identity (catalog contract)

These values must stay stable once the course is seeded. Changing the title after publish breaks catalog order, pricing lookup, and bundle membership.

| Field | Proposed value | BayLearn mapping |
|---|---|---|
| Title | Advanced Enterprise Java Engineering | `Course.title` — must be added to `CATALOG_COURSE_ORDER` |
| Subtitle | From Legacy Java to Cloud-Native Production Platforms | Curriculum/marketing only (not a portal field) |
| `catalogId` | `baylearn-aeje-001` | `CourseMetadata.catalogId` |
| Slug / curriculum prefix | `advanced-enterprise-java` | S3 keys `curriculum/advanced-enterprise-java/...` |
| Level | `advanced` | `CourseLevel` |
| Category | `microservices` | Existing `CourseCategory`; review if product wants a new `java` value |
| Pricing tier | `flagship` | Same band as EIA / EA Leadership |
| Self-paced | $999 (`99900`) | `CoursePricing.selfPacedCents` |
| Live cohort | $2,499 (`249900`) | Primary catalog price |
| Premium mentorship | $3,499 (`349900`) | |
| Duration | 16 weeks (90–120 hours) | `Course.duration` + metadata effort hours |
| Certificate name | BayLearn Certificate of Completion: Advanced Enterprise Java Engineering | `CourseMetadata.certificateName` |
| Instructor | BayAreaLa8s Team | Matches every seeded course |
| Case study | BayPay Financial Services (fictional) | Curriculum only |
| Repository URL | TBD — `https://github.com/bayareala8s/training/tree/main/Advanced-Enterprise-Java-Engineering` **or** this standalone repo | `CourseMetadata.repositoryUrl` (required for GitHub raw fallback) |

**Bundle decision (needs review):** Do **not** silently add this course to `professional-program`. That bundle’s `individualValueCents` and copy (“all seven courses”) would become wrong. Options for a later pricing change:

1. New “Enterprise Java Modernization” bundle
2. Recalculate Professional Engineer Program after explicit product approval

---

## 3. Requirement-to-implementation map

Every numbered section of `COURSE_MASTER_SPEC.md` is mapped below.

### 3.1 Product vision and positioning (spec §§1–2)

| Requirement | Implementation |
|---|---|
| Single BayPay case study across the course | All lessons, labs, incidents, and capstones use BayPay Financial Services and the BayPay Enterprise Payment Platform. No disconnected sample apps. |
| Philosophy BUILD → MODERNIZE → DEPLOY → BREAK → DIAGNOSE → OPERATE → ARCHITECT → DEFEND | Encoded in module order (1–4 build, 5–6 modernize, 9–12 deploy, 2/8/10/13 break-diagnose, 13–14 operate/defend, 15 AI ops, 16 architect/interview). |
| Advanced / professional audience | `level: "advanced"`, audience metadata, interview bank with Engineer/Senior/Staff/Principal answer maturity. |
| Prerequisites | Stored in `CourseMetadata.prerequisites` and module READMEs. |

### 3.2 Course targets (spec §3)

| Target | Manifest count | Delivery |
|---|---|---|
| 16 modules | 16 | Portal `Section.type = "module"` |
| ~50 hands-on labs | **68 required labs** listed in the spec | Each lab is a portal `Lesson` plus `labs/{labId}/` |
| 4 major capstones | 4 | One `Section.type = "capstone"` with four lessons (EIA pattern) |
| 100 interview questions | 100 | `interview-bank/` JSON; simulator in Stage 10 |
| ~70 diagrams | 72 | `diagrams/` with SVG/PNG/source/alt text |
| BayPay reference app | 5 Maven modules | `reference-apps/baypay/` (Stage 2) |
| Incident simulator | 16 incident packs + reusable player | `incidents/` then optional portal UI |
| BayOps AI prototype | Teaching prototype | Module 15 + `infrastructure` stubs |
| Portfolio artifacts | 15 named artifacts | Assignments first; optional portfolio table later |
| Instructor solutions | Separate tree | `solutions/` and `instructor/` — never in student lab READMEs |
| BayLearn progress/quiz/certificate | Reuse + additive | See §7 and integration map |

The spec’s “approximately 50 labs” is lower than the **68 labs explicitly required** in modules 1–16. This plan implements every listed lab. Module 16 items are `INTERVIEW` lab types (simulator modes), not extra coding labs.

### 3.3 BayPay case study and reference app (spec §§4–5)

| Requirement | Implementation |
|---|---|
| Fictional BayPay Financial Services | Synthetic names, accounts, logs, dumps. No real employer architectures or data. |
| Initial topology: LB → WebSphere ND → Payment/Refund → messaging → DB → reporting | Diagram `AEJE-D-071` and Module 5 current-state architecture. |
| Progressive modernization | Modules 6, 9–12, Capstone 2–3. |
| Java 21, Spring Boot, Maven, REST, JPA | Stage 2 reference app. |
| H2 local / PostgreSQL-compatible prod | `application-local.yml` + `application-prod.yml`. |
| Actuator, Bean Validation, JUnit, Testcontainers, OpenAPI, structured logging | Stage 2 definition of done. |
| Components: payment, refund, notification, transaction-worker, shared | Modular monolith first. Notification and worker stay in-process or separately runnable — taught as extractable modules, not mandatory microservices. |
| Entities and payment state machine | Domain in `shared`; state `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED` plus failure/reversal. |
| Idempotency as a real requirement | `Idempotency-Key` on payment/refund writes; persisted key store; taught in M1–M3 and EIA-style lab validation. |
| Teach when a modular monolith is preferable | Explicit lesson + ARCHITECT labs; do not split services for appearance. |

**Stage 2 stop:** build and test the reference app only. No portal seed yet.

### 3.4 Modules 1–16 (spec module sections)

Each module is a portal `Section` (`type: "module"`). Required coverage topics become lessons. Required labs become additional lessons. Each module also gets a quiz lesson so a future quiz engine has a stable attachment point.

| Module | Section title | Lessons | Labs | Quiz | Primary lab types |
|---|---|---|---|---|---|
| 1 | Enterprise Java Engineering | 5 | 4 | Q-01 | BUILD, BREAK/FIX, PERFORMANCE |
| 2 | Advanced Java Concurrency | 6 | 3 | Q-02 | BREAK/FIX, INCIDENT, ARCHITECT |
| 3 | Spring Boot Engineering | 6 | 5 | Q-03 | BUILD, BREAK/FIX |
| 4 | Jakarta EE and Enterprise Runtime Concepts | 5 | 3 | Q-04 | ARCHITECT, INCIDENT |
| 5 | WebSphere Network Deployment | 6 | 4 | Q-05 | ARCHITECT, INCIDENT |
| 6 | WebSphere Liberty Modernization | 5 | 4 | Q-06 | MODERNIZE, ARCHITECT |
| 7 | JVM Internals and Performance | 6 | 4 | Q-07 | PERFORMANCE |
| 8 | JVM Troubleshooting | 7 | 6 | Q-08 | INCIDENT |
| 9 | Containers for Java | 7 | 4 | Q-09 | BUILD, BREAK/FIX, SECURITY, PERFORMANCE |
| 10 | Kubernetes and OpenShift | 6 | 6 | Q-10 | INCIDENT |
| 11 | AWS Container Platforms | 8 | 5 | Q-11 | BUILD, ARCHITECT, SECURITY, INCIDENT, COST |
| 12 | Terraform, Ansible and CI/CD | 6 | 5 | Q-12 | BUILD, INCIDENT |
| 13 | Production Engineering and Observability | 7 | 2 | Q-13 | BUILD, INCIDENT |
| 14 | Security, HA and DR | 7 | 4 | Q-14 | ARCHITECT, INCIDENT, SECURITY |
| 15 | BayOps AI | 6 | 4 | Q-15 | AI |
| 16 | Advanced Engineer Interview Simulator | 9 | 5 | Q-16 | INTERVIEW |

**Per-module asset mapping (spec “Required module assets”):**

| Spec asset | Repo path / portal mapping |
|---|---|
| Module overview and business context | `course/modules/{nn}-{slug}/README.md` attached as material on lesson 1 (EIA pattern) |
| Learning objectives and prerequisites | Same README + lesson front matter |
| Detailed lesson content | `course/lessons/{id}.md` — 15-section lesson template (spec §29) |
| Professional diagrams and alt text | `diagrams/{domain}/{id}.svg|png` + `{id}.alt.md` + `{id}.source.md` |
| Code/configuration examples | In-lesson fenced blocks + `reference-apps/baypay` excerpts |
| Production failure modes and trade-offs | Dedicated lesson sections 8–10 |
| Interview perspective | Lesson section 11 + links into interview bank |
| Knowledge checks | In-lesson checks (not scored) |
| Module quiz with explanations | `course/quizzes/Q-{nn}.json` + markdown student view |
| Lab student guide | `labs/{labId}/README.md` — 17-section lab template (spec §23) |
| Instructor/reference solution | `solutions/{labId}/` — not linked from student README |
| Rubric | `instructor/rubrics/{labId}.md` using standard scoring weights |
| Student portfolio artifact | Listed in manifest; collected via assignment or export |
| Related PAKS deep-dive | Optional “Related PAKS” section; lesson remains self-contained |

**WebSphere / OpenShift realism constraint:** Modules 5, 6, and 10 will use **architecture, configuration, and incident-simulation assets**, not a requirement that every student run WebSphere ND or a full OpenShift cluster. Where a real cluster is optional, the lab says so and provides a local/kind/minikube or paper-architecture path.

### 3.5 Capstones (spec §22)

| Capstone | Lab type | After modules | Portal |
|---|---|---|---|
| C1 Build BayPay | CAPSTONE | 1–3 | Capstone section lesson 1 |
| C2 Modernize BayPay | CAPSTONE | 4–10 | Lesson 2 |
| C3 Cloud BayPay | CAPSTONE | 11–12 | Lesson 3 — AWS lab standards apply |
| C4 BayPay Production Crisis | CAPSTONE | 13–15 | Lesson 4 — progressive SEV-1 using incident simulator |

### 3.6 Lab taxonomy and UX (spec §23)

Every lab uses exactly one of: `BUILD`, `ARCHITECT`, `MODERNIZE`, `BREAK/FIX`, `INCIDENT`, `SECURITY`, `PERFORMANCE`, `COST`, `AI`, `INTERVIEW`, `CAPSTONE`.

Spec IDs that are not taxonomy names map as follows:

| Spec prefix | `labType` |
|---|---|
| BUILD-* | BUILD |
| FIX-*, BREAKFIX-* | BREAK/FIX |
| CHALLENGE-104, LAB-70x | PERFORMANCE |
| INCIDENT-* | INCIDENT |
| ARCHITECT-* | ARCHITECT |
| MODERNIZE-* | MODERNIZE |
| SECURITY-* | SECURITY |
| COST-* | COST |
| AI-* | AI |
| INTERVIEW-* | INTERVIEW |
| DR-1403 | ARCHITECT (tabletop; not an injected outage) |
| CAPSTONE-* | CAPSTONE |

Every student lab README includes the 17 required sections. Challenge and incident labs **do not** reveal the root cause in the student guide. Solutions stay under `solutions/`.

### 3.7 Incident simulator (spec §24)

**Content (this repo, Stages 3–8, 11):**

- Timeline JSON per incident
- Evidence packs: dashboards, logs, thread dumps, deploy history, JVM/container metrics, DB metrics, queue depth, dependency latency
- Evidence is gated — not all files are visible at start
- Student worksheet: hypothesis, supporting evidence, next investigation, stabilization, remediation, communication update

**Platform (additive, only if we implement a BayLearn-native player):**

- New optional routes and a `IncidentSimulator` component
- Existing courses never load it
- Scoring weights from the spec (lucky guess must not score like evidence-based diagnosis)

**Phase A fallback:** progressive markdown + revealable evidence in `course-ui` or lab pages, scored by rubric on submission. This does not block curriculum authoring.

### 3.8 Interview bank and simulator (spec §25)

Exactly 100 questions, domain counts fixed in `COURSE_MANIFEST.json`. Each record schema:

`id`, `domain`, `difficulty`, `question`, `followUps`, `expectedConcepts`, `seniorAnswer`, `staffAnswer`, `principalAnswer`, `commonMistakes`, `scoreRubric`

Maturity levels: Engineer / Senior / Staff / Principal — not one memorized answer.

Simulator modes (Module 16 labs): Practice, Timed Interview, Rapid Fire, Troubleshooting, System Design, Full Mock Loop.

Stage 10 authors the bank and simulator. Until then, Module 16 lessons can exist as outlines only if we stop after earlier stages as specified.

### 3.9 BayOps AI (spec §26)

Teaching prototype only. Synthetic/sanitized ops data. Allowed AWS sketch: Bedrock, Lambda, S3, DynamoDB, API Gateway, CloudWatch — **low-cost, short-lived**, with cleanup and cost warning.

Outputs always separated: Evidence / Hypotheses / Recommended investigation / Suggested remediation. Never present an AI root cause as proven.

Lab AI-1504 is mandatory: students catch a planted hallucination.

Human approval is a first-class step in the prototype UX.

### 3.10 Diagram standard (spec §27)

72 diagrams, IDs `AEJE-D-001` … `AEJE-D-072`. Each has: id, title, module/lesson mapping, learning purpose, complexity (concept/application/production/enterprise), editable source, SVG, PNG, alt text.

AWS diagrams use official Architecture Icons where the asset pipeline supports them. Non-AWS vendors: labeled components unless a licensed mark is available.

Stage 12 generates/exports/validates the full library. Earlier stages create the diagrams they need and register them in the manifest.

### 3.11 AWS lab standards (spec §28)

Apply to every AWS-touching lab (primarily 1101, 1103, 1104, 1105, 1201–1205, C3, BayOps). Required sections match EIA Lab 2: architecture, service list, region, prerequisites, least privilege, duration, cost + warning, IaC, validation, failure scenario, troubleshooting, cleanup, expected final state.

Defaults:

- Region assumption: `us-west-2` (same as BayLearn Portal)
- Prefer Fargate/serverless/short-lived
- **No** NAT Gateway, always-on EC2, OpenSearch, or required EKS cluster unless the learning objective needs it and cost is disclosed
- ARCHITECT-1102 and EKS content are **design-comparison** unless an optional expensive path is clearly marked
- Tags: `Course=AEJE`, `Module`, `Lab`, `Environment`, `Expiration`

### 3.12 Lesson content standard (spec §29)

Lesson template (every content lesson):

1. Why this matters  
2. Learning objectives  
3. Concept explanation  
4. Visual explanation  
5. Architecture  
6. Production example  
7. Code/configuration example  
8. Trade-offs  
9. Failure modes  
10. Security/reliability implications  
11. Interview perspective  
12. Key takeaways  
13. Knowledge check  
14. Related lab  
15. Related PAKS deep dive  

PAKS is optional. A student who never opens PAKS can still complete the lesson.

### 3.13 Student portfolio (spec §30)

| Artifact | Source |
|---|---|
| Java service | Capstone 1 / reference app |
| Concurrency RCA | BREAKFIX-201 / INCIDENT-202 |
| WebSphere architecture | ARCHITECT-501 |
| Liberty migration assessment | MODERNIZE-601 / ARCHITECT-604 |
| JVM incident RCA | Module 8 incidents |
| Container architecture | BUILD-901 / SECURITY-903 |
| Kubernetes/OpenShift deployment | Module 10 |
| AWS architecture | ARCHITECT-1102 / Capstone 3 |
| Terraform | BUILD-1201 / BUILD-1202 |
| CI/CD design | BUILD-1204 |
| Security model | SECURITY-1404 |
| DR strategy | DR-1403 / ARCHITECT-1401 |
| Production RCA | Capstone 4 |
| AI-operations evaluation | AI-1504 |
| System-design response | INTERVIEW-1604 |

Portal: reuse `Assignment` + `Submission` (`github_url` / `zip` / `pdf` / `diagram`). Handlers must be added (table already exists). This is additive and unused by current courses.

### 3.14 Required repository structure (spec §31)

This workspace will adopt the spec tree. Stage 1 creates only planning files at the root. Later stages fill directories without inventing a second conflicting layout.

Portal seed files are **not** authored inside this repo’s runtime. They are produced as `baylearn-seed/` JSON **and** a TypeScript seed in BayLearn-Portal (`aeje-course.ts` + `sync-aeje-catalog.ts`), matching EIA.

### 3.15 BayLearn integration (spec §32)

See `BAYLEARN_INTEGRATION_MAP.md`. Rules:

- Reuse catalog, auth, progress, certificates, materials, design tokens
- Add capabilities only for labType, incident simulator, interview simulator, portfolio
- Shared type changes are **optional fields only**
- Do not edit existing course seed files except to register the new course in aggregator/catalog/pricing lists

### 3.16 QA and definition of done (spec §33)

Automate in `qa/` (Stage 14, with incremental checks per stage):

- Missing modules/lessons/labs vs manifest
- Broken links
- Invalid JSON
- Missing solutions/rubrics
- AWS labs missing cleanup or cost disclosure
- Diagrams missing alt text
- Duplicate interview questions
- Java compile + tests
- Terraform validate (where present)
- Kubernetes YAML validate (where tools exist)
- Missing prerequisites
- Placeholder/TODO scan
- Unsupported factual claims review (manual + checklist)
- No real confidential enterprise data

Output: `COURSE_QA_REPORT.md`.

Course is complete only when all 16 modules, 68 labs, 4 capstones, 100 questions, diagram library, simulators, reference app, seed, instructor/student assets, and QA pass **and** existing BayLearn courses still list, enroll, and learn unchanged.

### 3.17 Execution stages (spec §34)

| Stage | Work | Stop |
|---|---|---|
| **1 (this stage)** | Inspect portal; write plan, manifest, integration map | Review |
| 2 | BayPay reference app + tests | Review |
| 3 | Modules 1–4 + QA | Review |
| 4 | Modules 5–6 + QA | Review |
| 5 | Modules 7–8 + incident datasets + QA | Review |
| 6 | Modules 9–10 + QA | Review |
| 7 | Modules 11–12 + Terraform validation + QA | Review |
| 8 | Modules 13–14 + QA | Review |
| 9 | Module 15 BayOps AI + safety + QA | Review |
| 10 | Module 16 + 100-question bank + simulator + QA | Review |
| 11 | Four capstones + QA | |
| 12 | Full diagram library export/validate | |
| 13 | Curated PAKS links | |
| 14 | Full build/test/QA; final manifest + `COURSE_QA_REPORT.md` | |

Stages 1–14 are complete. Portal seed files are authored. Do not run live DynamoDB catalog sync until that review.

### 3.18 Guardrails (spec §36)

Enforced in authoring and QA:

- Synthetic BayPay / incident data only
- No confidential employer architectures, runbooks, logs, or procedures
- No claimed affiliation with a real employer
- Historical WebSphere taught for modernization, not as recommended greenfield practice
- Trade-offs over one-true architecture
- Cloud cost and cleanup always visible
- Security, reliability, operability in designs
- Evidence-based troubleshooting
- AI is never final RCA authority
- Solutions separated from student challenges

---

## 4. How this course will be added to BayLearn (no existing course changes)

Mirror EIA. All portal edits are additive.

1. Author curriculum in this repository.
2. Produce `baylearn-seed/course.json`, `modules.json`, `lessons.json`, `quizzes.json`, `assignments.json`.
3. In **BayLearn-Portal** (separate change set):
   - Append title to `CATALOG_COURSE_ORDER`
   - Add `CATALOG_COURSE_SEEDS` and `CATALOG_METADATA_BY_TITLE`
   - Add `COURSE_PRICING_BY_TITLE` entry
   - Add `backend/src/seed/aeje-course.ts`
   - Register in `backend/src/seed/courses.ts`
   - Add `sync-aeje-catalog.ts` + npm scripts
   - Optionally extend `Lesson` with optional `lessonKind` / `labType` / `labId`
4. Upload materials to S3 under `curriculum/advanced-enterprise-java/` **or** rely on GitHub raw fallback.
5. `npm run build -w backend && npm run sync-aeje-catalog -w backend`
6. `npm run build:frontend` so `courses-catalog.json` picks up the new UUID.
7. Verify catalog, course detail, enroll, learn, and that the original seven published courses still render.

**Do not** use `/admin/builder` for this course. It creates bare courses without metadata, pricing tiers, or curriculum materials.

### Known portal bug to fix when seeding assignments

`insertCourseContent()` in `backend/src/seed/catalog-sync-utils.ts` writes materials but **skips `assignment`**. Initial `seed/index.ts` writes assignments; later syncs drop them. Fix this in the AEJE portal PR. Existing courses that do not rely on synced assignments stay compatible.

---

## 5. Content architecture (this repository)

```text
advanced-enterprise-java-engineering/
├── COURSE_MASTER_SPEC.md          # source of truth
├── COURSE_IMPLEMENTATION_PLAN.md  # this file
├── COURSE_MANIFEST.json
├── BAYLEARN_INTEGRATION_MAP.md
├── course/                        # modules, lessons, quizzes, assessments
├── reference-apps/baypay/         # Stage 2
├── labs/                          # student guides (no hidden answers)
├── incidents/{jvm,kubernetes,aws,production}/
├── capstones/
├── interview-bank/
├── diagrams/{java,spring,websphere,liberty,jvm,containers,kubernetes,openshift,aws,devops,observability,security,ai,capstones}/
├── infrastructure/{terraform,kubernetes,openshift,scripts}/
├── instructor/                    # rubrics, facilitation notes
├── student/                       # getting started, worksheets
├── datasets/                      # synthetic dumps, logs, metrics
├── solutions/                     # instructor-only
├── baylearn-seed/                 # JSON consumed by portal seed
└── qa/
```

Lesson and lab markdown stay understandable as files. Portal materials point at those paths via `s3Key`.

---

## 6. New platform capabilities — phased

The spec asks for BayLearn-native quiz, incident, interview, and portfolio features. The portal cannot do those today. To avoid blocking the curriculum or breaking existing courses:

### Phase A — ship with current portal (Stages 2–8 can proceed)

- Lessons and labs as markdown materials
- Quizzes as markdown/JSON downloads with answer explanations in instructor pack
- Incidents as gated evidence folders + student worksheet
- Interview bank as JSON + markdown practice
- Progress via existing Mark Complete
- Certificate via existing manual issue (or metadata-gated auto-issue if implemented)

### Phase B — additive portal features (can start in parallel after Stage 1 review)

| Feature | Compatibility rule |
|---|---|
| Optional `labType` on Lesson + badge | Absent field = current UI |
| Quiz API + `QuizPlayer` | Only lessons with quiz IDs |
| `IncidentSimulator` | Only lessons with incident IDs |
| `InterviewSimulator` | Only Module 16 / interview lessons |
| Submission handlers for existing `Assignment`/`Submission` | New routes; unused tables today |
| Auto-certificate when `metadata.autoIssueCertificate === true` | Other courses unchanged |

Phase B must not change existing seed files’ behavior, Cognito groups, or progress formula for courses that do not opt in.

---

## 7. Progress, quiz, and certificate integration

| Concern | Current | AEJE plan |
|---|---|---|
| Progress | Equal weight per lesson | Keep formula. Do not introduce weighted progress in shared code (would change every course). Communicate that labs/capstones are lessons students must mark complete. |
| Quiz scores | None | Phase A: unscored knowledge + instructor-reviewed quiz markdown. Phase B: `QuizAttempt` stored separately; **do not** fold into `Enrollment.progress` unless product later wants an opt-in flag. |
| Certificate | Manual POST `/certificates/issue` | Keep manual path. Optional auto-issue only when this course’s metadata flag is set and progress is 100%. Use `metadata.certificateName`. |
| Completion meaning | Any lesson marked complete | Rubrics still require labs/capstones for a “passed” professional outcome; portal completion ≠ rubric pass unless we add assessment later. |

---

## 8. Risks and assumptions

### Assumptions

- This workspace is the curriculum repo; BayLearn-Portal remains a separate repo.
- Eventual GitHub location follows other courses (`bayareala8s/training/...`) so `curriculum-url.ts` GitHub fallback works.
- Java 21, Spring Boot 3.x, Maven, JUnit 5.
- AWS labs default to `us-west-2`, student sandbox accounts, destroy-after-lab.
- WebSphere ND and OpenShift are taught with topology, config, and incident datasets; a live ND cell is not a student prerequisite.
- All names, logs, dumps, and metrics are fictional.
- PAKS remains a separate site (`paks.bayareala8s.com` or CloudFront). Links are curated, never required.
- Pricing matches other 16-week flagship courses until product says otherwise.

### Risks

| Risk | Impact | Mitigation |
|---|---|---|
| 68 labs vs “~50” target | Scope/cost | Implement all specified labs; interview modes are simulator labs, not extra coding work |
| ~190 portal lessons | Noisy progress UX | Group labs under clear titles; overview stays a material, not a lesson |
| Portal has no markdown player | Weak in-app reading | Downloads + optional `course-ui` like EIA; do not rewrite the learn page for all courses |
| Quiz/incident/interview engines missing | Spec gap | Phase A content; Phase B additive UI |
| Assignment sync bug | Lost assessments | Fix `insertCourseContent` in AEJE portal PR |
| EKS / OpenShift cost | Student bill shock | Design-first; Fargate default; cost warnings |
| Adding to Professional bundle | Breaks “seven courses” copy and pricing math | Separate product decision |
| New `java` category | Touches shared enum + filters | Defer; use `microservices` |
| Confidential data leakage | Guardrail violation | Synthetic-data QA check; no employer runbooks |
| AI presented as RCA authority | Spec violation | Forced evidence/hypothesis split; AI-1504 hallucination lab |
| Two-repo drift | Seed paths break | Manifest IDs == seed IDs == file paths |

---

## 9. Technical decisions for review

Please confirm or redirect before Stage 2:

1. **Category:** `microservices` (no schema change) vs add `java`.
2. **Pricing:** Flagship $999 / $2,499 / $3,499.
3. **Bundles:** Keep out of Professional Program until a pricing update is approved.
4. **Repository home:** Standalone (this folder) vs `training/Advanced-Enterprise-Java-Engineering`.
5. **Monolith vs services:** Modular monolith with extractable modules — confirmed from spec; Stage 2 will not create a service mesh.
6. **Phase B timing:** Build portal quiz/incident/interview engines in parallel, or after content Stages 2–8.
7. **WebSphere/OpenShift:** Simulation + architecture (recommended) vs requiring licensed middleware.
8. **Auto-certificate:** Metadata-gated for this course only, or remain fully manual.

---

## 10. Stage 1 exit criteria

Stage 1 is complete when:

- [x] BayLearn Portal schemas, routes, seed, progress, auth, catalog, certificates, design tokens, and AWS lab patterns inspected
- [x] `COURSE_IMPLEMENTATION_PLAN.md` maps every spec section to an implementation
- [x] `COURSE_MANIFEST.json` enumerates modules, lessons, labs, capstones, diagrams, interview items, incidents, quizzes, assessments, and code components
- [x] `BAYLEARN_INTEGRATION_MAP.md` states reuse vs new work and backward-compatibility rules
- [x] Reviewer approval to start Stage 2 (BayPay reference application)
- [x] BayPay modular monolith built and tested (`reference-apps/baypay`, 24 tests)
- [x] Reviewer approval to start Stage 3 (Modules 1–4)

## 11. Stage 3 exit criteria

Stage 3 is complete when:

- [x] Module 1–4 overviews, 22 lessons, 15 labs, 4 quizzes, 17 diagrams
- [x] Instructor solutions and rubrics for those 15 labs
- [x] Incident packs INC-JVM-201, INC-JVM-202, INC-EE-402, INC-EE-403
- [x] `COURSE_QA_REPORT.md` for Stage 3
- [x] Manifest `buildPhase` = 3; modules 1–4 / Q-01–04 / D-001–017 marked implemented or generated
- [x] Reviewer approval to start Stage 4 (Modules 5–6: WebSphere ND + Liberty, simulation-first)

## 12. Stage 4 exit criteria

Stage 4 is complete when:

- [x] Module 5–6 overviews, 11 lessons, 8 labs, 2 quizzes, 10 diagrams
- [x] Instructor solutions and rubrics for those 8 labs
- [x] Incident packs INC-WAS-502, INC-WAS-503, INC-WAS-504 (gated, simulation)
- [x] Liberty `server.xml` starters and solutions (well-formed XML)
- [x] Locked topology `datasets/baypay-cell/TOPOLOGY.md` (no instructor RCA in the student-facing inventory)
- [x] `COURSE_QA_REPORT.md` updated for Stage 4
- [x] Manifest `buildPhase` = 4; modules 5–6 / Q-05–06 / D-018–027 marked implemented or generated
- [x] Reviewer approval to start Stage 5 (Modules 7–8: JVM internals, performance, troubleshooting)

## 13. Stage 5 exit criteria

Stage 5 is complete when:

- [x] Module 7–8 overviews, 13 lessons, 10 labs, 2 quizzes, 10 diagrams
- [x] Instructor solutions and rubrics for those 10 labs
- [x] Incident packs INC-JVM-801–806 (gated, simulation)
- [x] LAB-701–703 Java harnesses compile on Java 21
- [x] `COURSE_QA_REPORT.md` updated for Stage 5
- [x] Manifest `buildPhase` = 5
- [x] Reviewer approval to start Stage 6 (Modules 9–10: containers, Kubernetes, OpenShift)

## 14. Stage 6 exit criteria

Stage 6 is complete when:

- [x] Module 9–10 overviews, 13 lessons, 10 labs, 2 quizzes, 10 diagrams
- [x] Instructor solutions and rubrics; healthy `infrastructure/kubernetes/payment-service` YAML
- [x] Incident packs INC-K8S-1001–1006
- [x] Solution Dockerfiles use JRE runtime + non-root USER
- [x] `COURSE_QA_REPORT.md` updated for Stage 6
- [x] Manifest `buildPhase` = 6
- [x] Reviewer approval to start Stage 7 (Modules 11–12: AWS and automation)

## 15. Stage 7 exit criteria

Stage 7 is complete when:

- [x] Module 11–12 overviews, 14 lessons, 10 labs, 2 quizzes, 11 diagrams
- [x] AWS labs disclose `us-west-2`, cost, and cleanup
- [x] `terraform validate` passes on BUILD-1101, BUILD-1201, BUILD-1202, and `infrastructure/terraform/baypay-ecs`
- [x] Incident packs INC-AWS-1104 and INC-AWS-1205
- [x] `COURSE_QA_REPORT.md` updated for Stage 7
- [x] Manifest `buildPhase` = 7
- [x] Reviewer approval to start Stage 8 (Modules 13–14: production engineering, security, HA/DR)

## 16. Stage 8 exit criteria

Stage 8 is complete when:

- [x] Module 13–14 overviews, 14 lessons, 6 labs, 2 quizzes, 9 diagrams
- [x] AWS/ops labs stay paper-first; no live Grafana, ACM, Route 53, or second-region apply
- [x] Incident packs INC-PROD-1301 and INC-SEC-1402 (student files hide RCA)
- [x] Portfolio worksheets PF-ops, PF-security, PF-dr
- [x] `COURSE_QA_REPORT.md` updated for Stage 8
- [x] Manifest `buildPhase` = 8
- [x] Reviewer approval to start Stage 9 (Module 15: BayOps AI)

## 17. Stage 9 exit criteria

Stage 9 is complete when:

- [x] Module 15 overview, 6 lessons, 4 labs, 1 quiz, 3 diagrams
- [x] BayOps output contract (Evidence / Hypotheses / Investigation / Remediation) + human approval
- [x] Teaching prototype stubs under `infrastructure/bayops-ai/` (no required Bedrock apply)
- [x] AI-1504 hallucination lab with planted unsupported diagnosis
- [x] `COURSE_QA_REPORT.md` updated for Stage 9
- [x] Manifest `buildPhase` = 9
- [x] Reviewer approval to start Stage 10 (Module 16: interview simulator)

## 18. Stage 10 exit criteria

Stage 10 is complete when:

- [x] Module 16 overview, 9 lessons, 5 INTERVIEW labs, 1 quiz
- [x] Exactly 100 unique interview questions with locked domain counts
- [x] Phase A simulator (`interview-bank/simulator.py`); no portal UI required
- [x] Portfolio worksheet `PF-design.md`
- [x] `COURSE_QA_REPORT.md` updated for Stage 10
- [x] Manifest `buildPhase` = 10
- [x] Reviewer approval to start Stage 11 (four capstones)

## 19. Stage 11 exit criteria

Stage 11 is complete when:

- [x] Four capstone student guides, solutions, rubrics, worksheets
- [x] INC-CAP-4 gated SEV-1 pack (student files hide RCA)
- [x] CAPSTONE-3 names `us-west-2`, cost, and cleanup
- [x] AEJE-D-071 and AEJE-D-072 generated
- [x] Manifest capstones implemented
- [x] Reviewer approval to start Stage 12 (diagram library)

## 20. Stage 12 exit criteria

Stage 12 is complete when:

- [x] All 72 diagrams have source, SVG, PNG, and alt text
- [x] `diagrams/README.md` catalog
- [x] `qa/check_diagram_library.py` PASS
- [x] Manifest `buildPhase` = 12
- [x] Reviewer approval to start Stage 13 (curated PAKS links)

## 21. Stage 13 exit criteria

Stage 13 is complete when:

- [x] Every module has curated `paksDeepDives` (Module 5 filled)
- [x] `PAKS_LINKS.md` lists every unique path and states links are optional
- [x] Local PAKS tree files exist for every curated path
- [x] Every lesson Related PAKS section cites at least one curated `docs/…md` path
- [x] `qa/check_paks_links.py` PASS
- [x] Manifest `buildPhase` = 13
- [x] Reviewer approval to start Stage 14 (full build/test/QA)

## 22. Stage 14 exit criteria

Stage 14 is complete when:

- [x] Incremental checkers (Stages 3–13) PASS
- [x] `qa/check_stage14.py` inventory, links, JSON, AWS cost/cleanup, solutions/rubrics
- [x] Java 21 `./mvnw test` — 24 passed
- [x] `terraform validate` on BUILD-1101, BUILD-1201, BUILD-1202, `infrastructure/terraform/baypay-ecs`
- [x] Kubernetes teaching YAML parses locally (`apiVersion` / `kind`)
- [x] Interview simulator smoke (`AEJE-IQ-012`)
- [x] Existing BayLearn courses untouched (no portal seed)
- [x] Manifest `buildPhase` = 14
- [x] `COURSE_QA_REPORT.md` Stage 14 verdict
- [x] Reviewer approval to start the BayLearn Portal seed
- [x] `aeje-course.ts`, `sync-aeje-catalog.ts`, catalog/pricing append, assignment persist fix
- [x] `baylearn-seed/*.json` (190 portal lessons)
- [x] `npm run sync-aeje-catalog` against baylearn-prod (`us-west-2`)
- [x] Frontend rebuild + CloudFront invalidation
- [x] Live API: 8 courses, AEJE 17 sections / 190 lessons
- [x] Existing EFT course still published
