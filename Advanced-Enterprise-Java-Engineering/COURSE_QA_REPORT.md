# Course QA Report

**Date:** 2026-09-04  
**Catalog:** `baylearn-aeje-001` — Advanced Enterprise Java Engineering  
**Latest stage:** 14 + portal seed + runnable lab smoke + Phase B portal engines  
**BayLearn Portal:** AEJE synced to prod DynamoDB. Phase B quiz / incident / interview / assignment UI is additive on the AEJE learn page only.

---

# Phase B — Portal engines

## Verdict

Additive BayLearn engines are implemented. Existing seven courses omit `lessonKind` / `labType` / assignments, so their learn page stays download + mark complete.

| Engine | Mount | Persist | Progress |
|---|---|---|---|
| Quiz player | `lessonKind === quiz` | `baylearn-*-submissions` (`engine:quiz:Q-XX`) | Not updated |
| Incident simulator | INCIDENT labs, BREAKFIX-201, CAPSTONE-4, AI-1504 | `engine:incident:INC-*` | Not updated |
| Interview simulator | `labType === INTERVIEW` | `engine:interview:{mode}` | Not updated |
| Assignment submit | lessons with an assignment | real `assignmentId` | Not updated |

Lucky-guess cap: opening two evidence files with zero hypotheses caps Diagnostic method and Efficiency. Certificates stay manual.

---

---

# Runnable Java labs

## Verdict

Five BUILD/FIX labs now have Maven stubs and JUnit contracts. `qa/smoke_runnable_labs.py` compiles the stubs, overlays instructor sources in a temp tree, and runs the tests. Paper, WAS, OpenShift, and live `terraform apply` stay out of scope.

| Check | Result |
|---|---|
| BUILD-101 / 102 / FIX-103 / CHALLENGE-104 / BREAKFIX-201 stubs compile | **PASS** |
| Contract tests against `solutions/` | **PASS** |
| LAB-701–703 + starter javac | **PASS** |
| `terraform validate` (4 roots) | **PASS** |
| `reference-apps/baypay ./mvnw test` | **PASS** (24 tests) |
| Interview CLI `AEJE-IQ-012` | **PASS** |

Checker: `qa/smoke_runnable_labs.py`. Student command: `cd labs && ../reference-apps/baypay/mvnw -pl BUILD-101 test`. Stubs fail tests until implemented. Instructor solutions are not copied into student `src/main`.

---

# Portal seed — authored

## Verdict

**Portal seed files are ready for review.** AEJE is appended last on the catalog. Flagship pricing is `$999 / $2,499 / $3,499`. It is **not** in the seven-course Professional bundle. `insertCourseContent()` now persists assignments. Existing course seed files were not edited.

`qa/check_portal_seed.py` **PASS**. Shared + backend + frontend `tsc` **PASS**. Live `npm run sync-aeje-catalog` **ran** against `baylearn-prod-*` in `us-west-2`. Frontend rebuilt and uploaded; CloudFront invalidated.

| Item | Result |
|---|---|
| `backend/src/seed/aeje-course.ts` | 16 modules + capstone section, 190 lessons, 17 assignments |
| `backend/src/seed/sync-aeje-catalog.ts` | Added |
| `backend/src/seed/courses.ts` | Append `aejeSeedCourse` only |
| `shared/src/catalog.ts` / `pricing.ts` | Append title + metadata + pricing |
| `COURSE_BUNDLES` | Unchanged (still seven courses) |
| Optional `Lesson.lessonKind` / `labType` / `labId` | Additive |
| Assignment persist | `catalog-sync-utils.ts` |
| Existing course seeds | Untouched |
| DynamoDB / CloudFront catalog | Synced and deployed |
| Live courseId | `f63b4a37-acef-4380-9d41-cb7a8849c6c1` |
| Prod course count | 8 (original 7 + AEJE) |

---

# Stage 14 — Final validation

## Verdict

**Stage 14 is ready for review.** The curriculum QA suite passed. Orchestrator: `qa/run_stage14.py`. Results: `qa/stage14-results.json`. The BayLearn Portal was not modified and `aeje-course.ts` does not exist. Spec “course complete” still waits on a separate portal-seed yes. Existing published courses remain untouched.

## Suite

| Check | Result |
|---|---|
| Stages 3–11 incremental checkers | Pass |
| Diagram library (72) | Pass |
| PAKS links (23 paths, 102 lessons) | Pass |
| Inventory vs manifest (102 lessons, 68 labs, 4 capstones, 16 quizzes) | Pass |
| Solutions + rubrics | Pass |
| AWS labs: `us-west-2`, cost, cleanup | Pass |
| Relative markdown links (student-facing) | Pass |
| JSON parse (repo; incident dumps allow trailing comments) | Pass |
| Authoring TODO/FIXME leftovers | None |
| Real-employer / secret scan | Pass (synthetic BayPay only) |
| Java 21 `./mvnw test` | **24 passed**, 0 failed |
| `terraform validate` (4 roots) | Pass |
| Kubernetes teaching YAML | Pass (6 files, local parse; no live cluster) |
| Interview simulator `--id AEJE-IQ-012` | Pass |
| Existing BayLearn courses | Untouched |

Kubernetes validation is local YAML (`apiVersion` / `kind`). `kubectl apply` against this machine’s EKS kubeconfig is **not** the bar and was not used.

## Stage 14 exit

- [x] Full build/test/QA
- [x] Manifest `buildPhase` = 14
- [ ] Reviewer approval to start the portal seed

---

# Stage 13 — Curated PAKS links

## Verdict

**Stage 13 is complete.** PAKS remains **optional**. Every module has curated `paksDeepDives`. Index: `PAKS_LINKS.md`. Host when a cohort has a login: `paks.bayareala8s.com`. `qa/check_paks_links.py` **PASS** (23 unique paths, 102 lessons).

## Inventory

| Check | Result |
|---|---|
| Manifest paths exist on local PAKS tree | Pass (23/23) |
| Paths listed in `PAKS_LINKS.md` | Pass |
| Every module has ≥1 `paksDeepDives` | Pass (Module 5 filled) |
| Every lesson Related PAKS cites a curated `docs/…md` | Pass (102/102) |
| Lessons cite only the curated allowlist | Pass |
| PAKS required for comprehension | No (policy + wording) |
| Portal / BayLearn seed | Untouched |

## Stage 13 exit

- [x] Curated index + checker
- [x] Manifest `buildPhase` = 13
- [ ] Reviewer approval to start Stage 14 or the portal seed

---

# Stage 12 — Diagram library

## Verdict

**Stage 12 is complete.** All **72** diagrams (`AEJE-D-001`–`072`) have source, SVG, PNG, and alt text. Catalog: `diagrams/README.md`. `qa/check_diagram_library.py` **PASS**.

---

# Stage 11 — Four capstones

## Verdict

**Stage 11 is complete.** C1 list-by-customer on the reference app. C2 paper leave of `BayPayCell`. C3 Fargate / `terraform validate`. C4 progressive SEV-1 (`INC-CAP-4`). Student C4 files do not lecture the FraudClient timeout RCA. Lucky “database” does not max Diagnostic method.

`qa/check_stage11.py` **PASS**.

---

# Stage 10 — Module 16 (complete)

## Verdict

**Stage 10 is ready for review.** Module 16 is Phase A: paper plus `interview-bank/simulator.py`. The bank is exactly **100** unique questions with locked domain counts and Engineer / Senior / Staff / Principal answers. A BayLearn interview UI is not required. Do not start Stage 11 (capstones) until this review is approved.

## Inventory vs manifest

| Artifact | Required (Stage 10) | Found | Result |
|---|---:|---:|---|
| Lessons | 9 | L-16.1–L-16.9 | Pass |
| Labs | 5 | INTERVIEW-1601–1605 | Pass |
| Quiz | 8 | `Q-16` | Pass |
| Interview bank | 100 unique | `interview-bank/questions.json` | Pass |
| Domain counts | locked | Match manifest | Pass |
| Simulator | Phase A CLI | `simulator.py` | Pass |
| Worksheet | PF-design | `student/worksheets/PF-design.md` | Pass |

`qa/check_stage10.py` **PASS**.

## Guardrails

| Check | Result |
|---|---|
| Duplicate question ids/text | None |
| Four maturity layers | Pass |
| Lucky RCA cannot max Diagnostic method (1603) | Pass (rubric) |
| No portal UI / Bedrock required | Pass |
| Prior-module RCA not lectured in student labs | Pass |
| Existing BayLearn courses | Untouched |

## Stage 10 exit

- [x] Module 16 content, quiz, bank, solutions, rubrics
- [x] Manifest `buildPhase` = 10
- [x] Reviewer approval to start Stage 11 (capstones)

---

# Stage 9 — Module 15 (complete)

## Verdict

**Stage 9 is ready for review.** BayOps AI is a teaching prototype: four output buckets, hypotheses stay unproven, and a named human must approve any mutating remediation. Live Bedrock is optional extra credit. AI-1504 requires students to catch a planted unsupported diagnosis. No existing BayLearn course was touched. Do not start Stage 10 (interview simulator) until this review is approved.

## Inventory vs manifest

| Artifact | Required (Stage 9) | Found | Result |
|---|---:|---:|---|
| Lessons | 6 | L-15.1–L-15.6 | Pass |
| Labs | 4 | AI-1501–1504 | Pass |
| Quiz | 8 | `Q-15` | Pass |
| Diagrams | 3 | `AEJE-D-068`–`070` | Pass |
| Prototype | schema + fixtures | `infrastructure/bayops-ai/` | Pass |
| Hallucination lab | AI-1504 + INC-AI-1504 | Pack + planted JSON | Pass |
| Worksheet | PF-ai | `student/worksheets/PF-ai.md` | Pass |

`qa/check_stage9.py` **PASS**.

## Guardrails

| Check | Result |
|---|---|
| No proven-RCA field as success | Pass (schema + labs) |
| Human approval required | Pass |
| Live Bedrock not required | Pass |
| Student files do not lecture 1301/1402 RCAs | Pass |
| Lucky “AI is wrong” cannot max Diagnostic method | Pass (AI-1504 rubric) |
| Existing BayLearn courses | Untouched |

## Stage 9 exit

- [x] Module 15 content, quiz, diagrams, solutions, rubrics
- [x] Teaching prototype stubs; hallucination lab
- [x] Manifest `buildPhase` = 9
- [x] Reviewer approval to start Stage 10 (Module 16)

---

# Stage 8 — Modules 13–14 (complete)

## Verdict

**Stage 8 is ready for review.** Module 13 is paper observability: RED/USE, a **99.9%** payment-create SLO, dashboards, and gated INC-PROD-1301. Module 14 is TLS/IAM/encryption, **99.99%** failure domains, regional DR tabletop, and a STRIDE threat model. No live Grafana, ACM, Route 53, or second-region apply. No existing BayLearn course was touched. Do not start Stage 9 (BayOps AI) until this review is approved.

## Inventory vs manifest

| Artifact | Required (Stage 8) | Found | Result |
|---|---:|---:|---|
| Lessons | 14 | 7 + 7 | Pass |
| Labs | 6 | BUILD-1300, INCIDENT-1301, ARCHITECT-1401, INCIDENT-1402, DR-1403, SECURITY-1404 | Pass |
| Quizzes | 2 × 8 | `Q-13`, `Q-14` | Pass |
| Diagrams | 9 | `AEJE-D-059`–`067` | Pass |
| Incident packs | 2 | `INC-PROD-1301`, `INC-SEC-1402` | Pass |
| Worksheets | 3 | `PF-ops`, `PF-security`, `PF-dr` | Pass |
| Locked notes | 2 | `OBSERVABILITY.md`, `TRUST.md` | Pass |

`qa/check_stage8.py` **PASS**.

## Guardrails

| Check | Result |
|---|---|
| Student incident READMEs contain no locked RCA | Pass |
| Lucky “database” / “cert expired” cannot max Diagnostic method | Pass (rubrics) |
| Dashboard SLO stays 99.9%; 99.99% is architecture | Pass |
| No live Grafana / ACM / Route 53 / second-region apply | Pass |
| Traditional ND is not a DR target | Pass |
| Existing BayLearn courses | Untouched |

## Stage 8 exit

- [x] Modules 13–14 content, quizzes, diagrams, solutions, rubrics
- [x] Gated incident packs; RCA only under `solutions/`
- [x] Manifest `buildPhase` = 8
- [x] Reviewer approval to start Stage 9 (Module 15)

---

# Stage 7 — Modules 11–12 (complete)

## Verdict

**Stage 7 is ready for review.** Module 11 is ECR + ECS/Fargate in `us-west-2` (EKS is literacy). Module 12 is Git → CI → image → Terraform → leftover Ansible → rollback. `terraform apply` is optional; `terraform validate` passed on the four solution/example roots (outside the sandbox). No existing BayLearn course was touched. Do not start Stage 8 (Modules 13–14) until this review is approved.

## Inventory vs manifest

| Artifact | Required (Stage 7) | Found | Result |
|---|---:|---:|---|
| Lessons | 14 | 8 + 6 | Pass |
| Labs | 10 | BUILD-1101, ARCHITECT-1102, SECURITY-1103, INCIDENT-1104, COST-1105, BUILD-1201–1204, INCIDENT-1205 | Pass |
| Quizzes | 2 × 8 | `Q-11`, `Q-12` | Pass |
| Diagrams | 11 | `AEJE-D-048`–`058` | Pass |
| AWS labs region/cost/cleanup | 7 | All name `us-west-2`, cost, destroy | Pass |
| Terraform validate | 4 dirs | BUILD-1101, 1201, 1202, `baypay-ecs` | Pass |
| Incident packs | 2 | `INC-AWS-1104`, `INC-AWS-1205` | Pass |

`qa/check_stage7.py` **PASS**.

## Guardrails

| Check | Result |
|---|---|
| No NAT/EKS/RDS required for student apply | Pass (ACCOUNT.md + labs) |
| Idle ALB cost warned | Pass |
| Student incident READMEs contain no locked RCA | Pass |
| No AWS keys in repo | Pass |
| Existing BayLearn courses | Untouched |

## Stage 7 exit

- [x] Modules 11–12 content, quizzes, diagrams, solutions, rubrics
- [x] Terraform validate
- [x] Manifest `buildPhase` = 7
- [x] Reviewer approval to start Stage 8 (Modules 13–14)

---

# Stage 6 — Modules 9–10 (complete)

Stage 6 was approved; Stage 7 followed.

## Inventory vs manifest

| Artifact | Required (Stage 6) | Found | Result |
|---|---:|---:|---|
| Module overviews | 2 | 2 | Pass |
| Lessons | 13 | 13 (`L-9.1`–`L-9.7`, `L-10.1`–`L-10.6`) | Pass |
| Labs | 10 | BUILD-901, FIX-902, SECURITY-903, PERFORMANCE-904, INCIDENT-1001–1006 | Pass |
| Quizzes | 2 × 8 | `Q-09`, `Q-10` | Pass |
| Diagrams | 10 | `AEJE-D-038`–`047` | Pass |
| Solutions + rubrics | 10 each | Present | Pass |
| Incident packs | 6 | `INC-K8S-1001`–`1006` | Pass |
| Healthy YAML | 6 files | `infrastructure/kubernetes/payment-service/` parses | Pass |
| Worksheets | 2 | `PF-container`, `PF-k8s` | Pass |

`qa/check_stage6.py` **PASS**. Cost **$0**. Solution Dockerfiles: multi-stage JRE + `USER 10001`.

## Guardrails

| Check | Result |
|---|---|
| 15 lesson / 17 lab headings | Pass |
| No TODO / lorem | Pass |
| Student incident READMEs contain no locked RCA lecture | Pass |
| `CLUSTER.md` has no instructor RCA | Pass |
| `-Xmx` = limit recommended | Not found |
| Live OpenShift / EKS required | No |
| Existing BayLearn courses | Untouched |

## Stage 6 exit

- [x] Modules 9–10 lessons, labs, quizzes, diagrams, solutions, rubrics
- [x] Six Kubernetes incident packs
- [x] Heading / JSON / YAML / Dockerfile QA
- [x] Manifest `buildPhase` = 6
- [x] Reviewer approval to start Stage 7 (Modules 11–12)

**Stop.** Do not author AWS / Terraform labs until that approval.

---

# Stage 5 — Modules 7–8 (complete)

Stage 5 was approved; Stage 6 followed.

## Inventory vs manifest

| Artifact | Required (Stage 5) | Found | Result |
|---|---:|---:|---|
| Module overviews | 2 | 2 | Pass |
| Lessons | 13 | 13 (`L-7.1`–`L-7.6`, `L-8.1`–`L-8.7`) | Pass |
| Labs | 10 | LAB-701–704, INCIDENT-801–806 | Pass |
| Quizzes | 2 × 8 | `Q-07`, `Q-08` | Pass |
| Diagrams | 10 | `AEJE-D-028`–`037` | Pass |
| Solutions + rubrics | 10 each | Present | Pass |
| Incident packs | 6 | `INC-JVM-801`–`806` | Pass (gated subset) |
| Java harnesses | LAB-701–703 | `javac --release 21` | Pass |
| Worksheets | 2 | `PF-jvm-observe`, `PF-jvm-rca` | Pass |

`qa/check_stage5.py` **PASS**. Cost **$0**. Docker optional for LAB-704 only.

## Guardrails

| Check | Result |
|---|---|
| 15 lesson / 17 lab headings | Pass |
| No TODO / lorem in Stage 5 authored content | Pass (scanned at close) |
| Student incident READMEs contain no locked RCA lecture | Pass |
| `RUNTIME.md` has no instructor RCA block | Pass |
| Lucky guess cannot max Diagnostic method | Pass |
| `-Xmx` = container limit recommended | Not found; lessons forbid it |
| Existing BayLearn courses | Untouched |

## Incident RCAs (solutions only)

| Pack | Symptom class | Mechanism (instructor) |
|---|---|---|
| 801 | CPU 98% | Catastrophic `String.matches` on POST body |
| 802 | Old-gen climb | Unbounded in-process idempotency map |
| 803 | Deadlock | Opposite lock order vs nightly job |
| 804 | HTTP 200/200 WAITING | FX client, no timeout; Hikari idle |
| 805 | GC pauses | DEBUG `toString` allocation storm |
| 806 | cgroup OOMKilled | `-Xmx` equals 512Mi limit |

## Stage 5 exit

- [x] Modules 7–8 lessons, labs, quizzes, diagrams, solutions, rubrics
- [x] Six JVM incident packs
- [x] Heading / JSON / alt-text / compile / leak QA
- [x] Manifest `buildPhase` = 5
- [x] Reviewer approval to start Stage 6 (Modules 9–10)

**Stop.** Do not author containers / Kubernetes / OpenShift until that approval.

---

# Stage 4 — Modules 5–6 (complete)

Stage 4 was approved; Stage 5 followed.

## Inventory vs manifest

| Artifact | Required (Stage 4) | Found | Result |
|---|---:|---:|---|
| Module overviews | 2 | 2 | Pass |
| Lessons | 11 | 11 (`L-5.1`–`L-5.6`, `L-6.1`–`L-6.5`) | Pass |
| Labs | 8 | 8 READMEs, all ≥155 lines | Pass |
| Quizzes | 2 × 8 | `Q-05`, `Q-06` JSON + student markdown | Pass |
| Diagrams | 10 | `AEJE-D-018`–`027` (source, SVG, PNG, alt) | Pass |
| Solutions + rubrics | 8 each | Present | Pass |
| Incident packs | 3 | `INC-WAS-502`, `INC-WAS-503`, `INC-WAS-504` | Pass (gated subset) |
| Liberty XML | starters + solutions | `xmllint` well-formed | Pass |
| Topology lock file | 1 | `datasets/baypay-cell/TOPOLOGY.md` | Pass (RCA block removed from student-facing inventory) |
| Portfolio worksheets | 3 | `PF-was-nd`, `PF-liberty-assessment`, `PF-liberty-waves` | Pass |

Lesson length range: 203–229 lines. `qa/check_stage4.py` **PASS**.

## Structure and guardrails

| Check | Result |
|---|---|
| 15 lesson headings / 17 lab headings | Pass |
| No TODO / FIXME / lorem in Stage 4 authored content | Pass |
| Incident student guides contain no RCA | Pass |
| `TOPOLOGY.md` has no instructor RCA block | Pass (removed so students can read the inventory) |
| Lucky guess cannot max Diagnostic method | Pass (rubrics) |
| Traditional ND recommended as greenfield | Not found; lessons treat it as source estate |
| AWS labs / live ND install | None. Cost $0. |
| Existing BayLearn courses | Untouched |

## Incident packs (gated subsets)

| Pack | Evidence shipped | RCA (solutions only) |
|---|---|---|
| INC-WAS-502 | Timeline, dashboard, logs, plugin-status | TCP plugin health + hung JDBC threads on Pay2/Pay3 |
| INC-WAS-503 | Timeline, dashboard, logs, PMI pool | Cell-scoped `jdbc/baypay` shared with `reporting.ear` |
| INC-WAS-504 | Timeline, dashboard, logs, deployment-history | Partial sync during `nodeagent-pay-2` restart; mixed 4.11/4.12 |

## Known Stage 4 limits (accepted)

1. No live WebSphere ND or required Open Liberty runtime.
2. Incident evidence is a teaching subset, not 11 file kinds.
3. Phase A quizzes remain markdown + JSON.
4. Portal seed still not started.
5. Modules 7–16 not started.

## Stage 4 exit

- [x] Modules 5–6 lessons, labs, quizzes, diagrams, solutions, rubrics
- [x] Three WAS incident packs
- [x] Heading / JSON / alt-text / XML / leak QA
- [x] Manifest `buildPhase` = 4
- [x] Reviewer approval to start Stage 5 (Modules 7–8)

**Stop.** Do not author JVM internals / Module 7–8 content until that approval.

---

# Stage 3 — Modules 1–4 (complete)

**Scope:** Modules 1–4. Stage 3 was approved; Stage 4 followed.

---

## Inventory vs manifest

| Artifact | Required (Stage 3) | Found | Result |
|---|---:|---:|---|
| Module overviews | 4 | 4 | Pass |
| Lessons | 22 | 22 (`L-1.1`–`L-1.5`, `L-2.1`–`L-2.6`, `L-3.1`–`L-3.6`, `L-4.1`–`L-4.5`) | Pass |
| Labs | 15 | 15 READMEs, all ≥141 lines | Pass |
| Quizzes | 4 × 8 | `Q-01`–`Q-04` JSON + student markdown | Pass |
| Diagrams | 17 | `AEJE-D-001`–`017` each with `.source.md`, `.svg`, `.png`, `.alt.md` | Pass |
| Solutions | 15 | 15 `solutions/*/README.md` | Pass |
| Rubrics | 15 | 15 `instructor/rubrics/*.md` | Pass |
| Incident packs | 4 | `INC-JVM-201`, `INC-JVM-202`, `INC-EE-402`, `INC-EE-403` | Pass (gated subset; see notes) |
| Student worksheets | 3 | `PF-domain-model`, `PF-concurrency-rca`, `PF-spring-jakarta` | Pass |
| Getting started | 1 | `GETTING_STARTED.md`, `student/README.md`, `instructor/README.md` | Pass |

Lesson length range: 173–250 lines. Lab README range: 141–216 lines. Alt-text files are 161–198 characters.

---

## Structure checks

| Check | Result |
|---|---|
| Every lesson has the 15 required section headings | Pass |
| Every lab has the 17 required section headings (including Hidden/revealable solution and Architecture/trade-off) | Pass after renaming Module 3 “After you attempt” headings |
| Quiz JSON: 8 unique question ids, `correctIndex`, explanation | Pass |
| Quiz JSON parse | Pass |
| Diagram alt text present and non-empty | Pass |
| No `TODO` / `FIXME` / `lorem ipsum` in `course/` or `labs/` | Pass |
| Confidential-employer / real-runbook wording in authored content | Pass — only guardrail language in the spec and plan |
| AWS labs in this stage | None. Cost disclosed as `$0` / local JVM. Cleanup is local process only. |
| Existing BayLearn courses | Untouched (this repo only; no portal seed) |

---

## Incident / challenge answer leak

Student READMEs for `BREAKFIX-201`, `INCIDENT-202`, `FIX-304`, `INCIDENT-402`, and `INCIDENT-403` state that the guide does **not** include root cause. RCA lives in `solutions/`. Mentions of “root cause” in those READMEs are instructions, not spoilers.

Incident packs are **gated subsets**, not the full 11 evidence kinds listed on later packs. That is documented in each pack README:

| Pack | Evidence shipped | Intentionally omitted |
|---|---|---|
| INC-JVM-201 | Timeline, dashboard, logs | Thread dump, heap, deploy, extra metrics |
| INC-JVM-202 | Timeline, dashboard, logs, thread dump | Heap, deploy, extra metrics |
| INC-EE-402 | Timeline, dashboard, logs, JVM metrics | Remaining kinds |
| INC-EE-403 | Timeline, logs, dashboard, deployment history | Remaining kinds |

Scoring note (enforced in rubrics): a lucky guess must not max Diagnostic method (20%).

---

## Java compile

| File | Result |
|---|---|
| `MessyPaymentValidator.java` + `CleanPaymentValidator.java` | Compiles. Starter emits unchecked-ops note (intentional). |
| `NaivePostingLoop.java` + `FasterPostingLoop.java` | Compiles when compiled **together** (shared package types). |
| `UnsafePaymentLedger.java` + `SafePaymentLedger.java` | Compiles. |
| `PaymentValidator.java` (BUILD-102) | Compiles standalone. |
| `LeakyRefundService.java` / `FixedRefundService.java` | Spring + `shared` types. Not standalone `javac`. Use `reference-apps/baypay`. |

Stage 2 BayPay suite remains the runtime proof: `./mvnw test` — 24 tests (Java 21, Spring Boot 3.5.5).

---

## Diagrams

Generator: `qa/generate_stage3_diagrams.py`.  
PNGs re-rendered with `rsvg-convert` at 960 px wide (real diagram rasters, not placeholders).

`AEJE-D-001`–`008` and `014`–`017` live under `diagrams/java/`.  
`AEJE-D-009`–`013` live under `diagrams/spring/`.

Remaining 55 diagrams (`AEJE-D-018`–`072`) wait for later stages.

---

## Content spot-check (not placeholders)

| Sample | Observation |
|---|---|
| L-1.2 Object design | BayPay `Money` / `Payment` / SOLID table; frozen Avery account; points at `shared` |
| L-3.1 IoC | Constructor injection, `scanBasePackages`, `Clock` bean, proxy failure modes |
| L-4.1 Servlet model | Filter → `DispatcherServlet` → controller; thread-per-request + JDBC |
| BUILD-101 | Domain invariants, demo UUIDs, illegal transition cases, portfolio excerpt |
| INCIDENT-202 | Gated evidence order; no RCA in student guide |

All names, accounts, and logs are synthetic BayPay (Avery Chen, Harbor Bike Co, fictional UUIDs).

---

## Known Stage 3 limits (accepted)

1. **Phase A delivery.** Quizzes are markdown + JSON downloads. No portal quiz player.
2. **No portal seed.** Catalog, progress, and certificates are unchanged until a later BayLearn-Portal PR.
3. **Incident simulator UI** is not built. Students use pack folders + worksheets.
4. **Incident evidence** is a teaching subset, not a full production dump of every kind.
5. **PAKS** links are optional; lessons stand alone.
6. **WebSphere / Liberty** (Modules 5–6) are not started.

---

## Guardrails

- No real employer architectures, runbooks, or logs.
- No claimed affiliation with a real payments employer.
- No AWS spend in this stage.
- Solutions stay under `solutions/` and `instructor/`.
- Existing BayLearn catalog courses were not edited.

---

## Stage 3 exit

- [x] Modules 1–4 lessons, labs, quizzes, diagrams, solutions, rubrics
- [x] Four incident packs for Modules 2 and 4
- [x] Heading / JSON / alt-text / placeholder / confidential QA
- [x] Standalone Java starters compile; Spring-coupled files live in BayPay
- [x] Manifest `buildPhase` = 3; modules 1–4 marked implemented
- [x] Reviewer approval to start Stage 4 (Modules 5–6)
