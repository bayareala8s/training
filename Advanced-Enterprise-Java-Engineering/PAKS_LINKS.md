# Curated PAKS deep dives — Advanced Enterprise Java Engineering

**PAKS is optional.** Every BayLearn lesson and lab in this course stands alone. Do not treat a missing PAKS login as a blocker.

Host (when your cohort has access): [paks.bayareala8s.com](https://paks.bayareala8s.com).  
Local tree (authors): `Principal-Architect-Knowledge-System/docs/…`  
Paths below are relative to that `docs/` parent (`docs/…`).

Do **not** copy PAKS chapters into this repo. Do **not** paste employer-specific PAKS company-prep into student labs.

## Policy

| Rule | Meaning |
|---|---|
| Supplemental | Related PAKS sections deepen; they never introduce a required fact |
| Curated | Only the paths in this file / `COURSE_MANIFEST.json` `paksDeepDives` |
| Skip-safe | A student who never opens PAKS can still pass every module |
| No secrets | No live keys, no real employer runbooks |

## Module map

| Module | Deep dives |
|---|---|
| 1 Enterprise Java | `docs/09-transactions/overview.md` |
| 2 Concurrency | `docs/01-computer-architecture/memory-ordering-and-concurrency.md`, `docs/02-operating-systems/processes-threads-and-scheduling.md` |
| 3 Spring Boot | `docs/15-api-and-integration-architecture/overview.md`, `docs/14-microservices/overview.md` |
| 4 Jakarta EE | `docs/09-transactions/overview.md` |
| 5 WebSphere ND | `docs/12-messaging-and-streaming/overview.md`, `docs/27-production-failures/overview.md` |
| 6 Liberty | `docs/14-microservices/service-decomposition-and-ddd.md` |
| 7 JVM internals | `docs/01-computer-architecture/cpu-and-memory-fundamentals.md` |
| 8 JVM troubleshooting | `docs/27-production-failures/failure-analysis-methodology.md` |
| 9 Containers | `docs/17-kubernetes-and-platform-engineering/overview.md` |
| 10 Kubernetes / OpenShift | `docs/17-kubernetes-and-platform-engineering/kubernetes-architecture.md`, `docs/17-kubernetes-and-platform-engineering/platform-engineering-and-gitops.md` |
| 11 AWS | `docs/16-cloud-architecture/aws-fundamentals.md`, `docs/26-cost-and-finops/overview.md` |
| 12 Terraform / CI | `docs/17-kubernetes-and-platform-engineering/platform-engineering-and-gitops.md` |
| 13 Observability | `docs/19-observability/overview.md`, `docs/27-production-failures/overview.md` |
| 14 Security / HA / DR | `docs/20-security/overview.md`, `docs/18-reliability-and-resilience/overview.md`, `docs/16-cloud-architecture/multi-region-architecture.md` |
| 15 BayOps AI | `docs/23-agentic-ai-architecture/agent-governance-and-safety.md` |
| 16 Interview | `docs/24-system-design/overview.md`, `docs/30-mock-interviews/overview.md`, `docs/25-architecture-leadership/overview.md` |

Capstones reuse the modules they sit after. No extra required PAKS.

## Author note

`qa/check_paks_links.py` checks that every manifest path is listed here and, if the local PAKS tree is present, that the file exists.
