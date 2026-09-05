# Getting started — Advanced Enterprise Java Engineering

**Course:** Advanced Enterprise Java Engineering  
**Case study:** BayPay Financial Services (fictional)  
**Live on BayLearn:** Advanced Enterprise Java Engineering is in the prod catalog (16 modules + capstones). DynamoDB sync and frontend deploy are done.

## Prerequisites

- Working Java knowledge
- Git
- Basic Linux command line
- REST / API fundamentals
- Java 21 (`/opt/homebrew/opt/openjdk@21` or `JAVA_HOME` pointing at a JDK 21)

Maven Wrapper is included with the reference app. You do not need a global Maven install.

## Reference application

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd reference-apps/baypay
./mvnw test
./mvnw -pl payment-service -am spring-boot:run
```

- API: http://localhost:8080
- OpenAPI: http://localhost:8080/swagger-ui.html
- Health: http://localhost:8080/actuator/health

Demo identities (fictional):

| Field | Value |
|---|---|
| customerId | `11111111-1111-1111-1111-111111111111` |
| active account | `22222222-2222-2222-2222-222222222221` |
| frozen account | `22222222-2222-2222-2222-222222222222` |

## Capstones

Four delivery projects under [capstones/](capstones/README.md): Build, Modernize, Cloud (`terraform validate` bar), and a progressive SEV-1. Diagrams AEJE-D-071 / AEJE-D-072.

## Interview simulator (Module 16)

Paper plus `interview-bank/simulator.py` still passes the module. Exactly 100 questions. The BayLearn learn page now also has an **Interview simulator** on INTERVIEW-1601–1605 (same bank; Engineer / Senior / Staff / Principal panes). Notes: [datasets/baypay-interview/ROUNDS.md](datasets/baypay-interview/ROUNDS.md).

## Portal engines (Phase B)

On the AEJE learn page only (lessons with `lessonKind` / `labType`):

- **Quiz player** — `Q-01`…`Q-16` JSON, scored separately from course progress
- **Incident simulator** — gated evidence + worksheet; lucky guess cannot max Diagnostic method
- **Interview simulator** — Module 16 labs
- **Assignment submit** — GitHub URL (or notes URL) on portfolio lessons

Existing seven courses are unchanged. Certificates stay manual.

## BayOps AI (Module 15)

Paper JSON contract: Evidence / Hypotheses / Recommended investigation / Suggested remediation, plus **human approval**. A live Bedrock call is **not** required. Notes: [datasets/baypay-ai/BAYOPS.md](datasets/baypay-ai/BAYOPS.md). Prototype stubs: [infrastructure/bayops-ai/](infrastructure/bayops-ai/).

## Production engineering, security, HA/DR (Modules 13–14)

Paper dashboards, gated incident packs, and architecture tabletops. No live Grafana, ACM, Route 53, or second-region apply. Ops contract: [datasets/baypay-ops/OBSERVABILITY.md](datasets/baypay-ops/OBSERVABILITY.md). Trust / HA / DR contract: [datasets/baypay-security/TRUST.md](datasets/baypay-security/TRUST.md). Module 13 SLO is **99.9%**. **99.99%** is the Module 14 architecture target.

## AWS and automation (Modules 11–12)

Region **`us-west-2`**. Default compute is **ECS on Fargate**. `terraform apply` is optional; `terraform validate` is enough to pass if you cannot spend. If you apply: no NAT Gateway, no EKS, no RDS Multi-AZ; **destroy the same day**. Notes: [datasets/baypay-aws/ACCOUNT.md](datasets/baypay-aws/ACCOUNT.md).

## Containers and Kubernetes (Modules 9–10)

Dockerfile and YAML on disk. Docker/Podman and `kind` are optional. A live OpenShift cluster is **not** required. Notes: [datasets/baypay-k8s/CLUSTER.md](datasets/baypay-k8s/CLUSTER.md). No AWS in this stage.

## JVM (Modules 7–8)

Observe first (`jcmd`, GC logs, NMT). Then diagnose from gated dumps. Notes: [datasets/baypay-jvm/RUNTIME.md](datasets/baypay-jvm/RUNTIME.md). Never set `-Xmx` equal to a container memory limit. Docker is optional and only for LAB-704.

## WebSphere / Liberty (Modules 5–6)

These modules are **simulation-first**. You design topologies, read synthetic dumps, and write `server.xml`. You do **not** install WebSphere Network Deployment. Open Liberty is optional and never required.

Locked current-state names: [datasets/baypay-cell/TOPOLOGY.md](datasets/baypay-cell/TOPOLOGY.md). Traditional ND is the source estate to leave, not a greenfield target.

## Runnable Java labs

Five Module 1–2 labs have Maven stubs and JUnit contracts under [labs/](labs/README.md): BUILD-101, BUILD-102, FIX-103, CHALLENGE-104, BREAKFIX-201.

```bash
export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
cd labs
../reference-apps/baypay/mvnw -pl BUILD-101 test
```

Stubs compile; tests fail until you implement the types. Instructor smoke overlays `solutions/` in a temp tree: `python3 qa/smoke_runnable_labs.py`. BUILD-301–305 use the reference app (`./mvnw test`). Paper, WAS, OpenShift, and live AWS apply are still out of scope.

## How to take a module

1. Read the module `README.md`.
2. Complete each lesson in order. Lessons stand alone; PAKS links are optional. Curated map: [PAKS_LINKS.md](PAKS_LINKS.md).
3. Do the labs. Challenge and incident labs do **not** include the answer in the student guide.
4. Take the module quiz (`course/quizzes/Q-0N.md`).
5. Export the portfolio artifact listed in the module README.

Instructor solutions live under `solutions/` and rubrics under `instructor/rubrics/`. Do not open those until you have attempted the lab.

## Lab types

`BUILD`, `ARCHITECT`, `MODERNIZE`, `BREAK/FIX`, `INCIDENT`, `SECURITY`, `PERFORMANCE`, `COST`, `AI`, `INTERVIEW`, `CAPSTONE`.

## PAKS (optional)

The Principal Architect Knowledge System is **supplemental**. You can finish every module without a login.

When your cohort has access, the host is [paks.bayareala8s.com](https://paks.bayareala8s.com). Only the paths in [PAKS_LINKS.md](PAKS_LINKS.md) are curated for this course. Skip any chapter without penalty. Do not copy PAKS chapters into lab write-ups.

## Guardrails

All BayPay names, logs, dumps, and metrics in this course are synthetic. Do not treat them as a real employer’s architecture.
