# Module 9 — Containers for Java

**Duration:** ~3.5 hours of lessons plus 4 labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Package BayPay `payment-service` as a production image  
**Portfolio artifact:** Hardened Dockerfile and notes from [student/worksheets/PF-container.md](../../../student/worksheets/PF-container.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, account, hostname, image tag, and registry name you see is synthetic.

**Delivery note:** this module is **Dockerfiles and image design on disk**. Docker or Podman is useful and **not required** to pass if you write and review the files. A live registry, a live OpenShift cluster, and AWS are **not** required. Cost is **$0**.

---

## Business context

BayPay’s **source estate** is still the traditional WebSphere Network Deployment cell `BayPayCell` from Module 5: `payment.ear` on `PaymentCluster` (`Pay1`, `Pay2`, `Pay3`), cell-scoped `jdbc/baypay`, `dmgr-east` as the management JVM. Module 6 moved that estate **toward** Liberty. This module packages the **teaching application** — `reference-apps/baypay`, **Java 21**, **Spring Boot 3.5.5**, composition root `payment-service` — as an **OCI image**.

Containers are the **modernization path**. They are not “ND in Docker.” Do not put `dmgr-east`, a node agent, or a traditional WAS profile into an image and call the cell modern. The image runs one disposable `payment-service` process. The cell remains the estate you leave.

The locked image contract lives in [datasets/baypay-k8s/CLUSTER.md](../../../datasets/baypay-k8s/CLUSTER.md):

| Field | Value |
|---|---|
| Image | `registry.baypay.example/baypay/payment-service:<tag>` |
| Base (runtime) | `eclipse-temurin:21-jre` (not a full JDK in the final stage) |
| Port | `8080` |
| User | non-root numeric UID (example `10001`) |
| Config | `BAYPAY_DB_*` from the runtime environment — never baked into the image |
| JVM | `UseContainerSupport`; **do not** set `-Xmx` equal to the container memory limit |
| Probes | `/actuator/health/liveness`, `/actuator/health/readiness` |

Harbor Bike Co still charges Avery Chen through `POST /api/v1/payments`. The fat JAR that served that request on a laptop is the same artifact you copy into the image. Immutability, tags that are not `:latest`, and secrets that stay out of layers are how Jordan Voss ships `3.8.0` without turning Riley Okonkwo’s page into “which bytes are running?”

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |
| Frozen USD account | `22222222-2222-2222-2222-222222222222` |

On-call: **Riley Okonkwo**. SRE: **Priya Nair**. Release: **Jordan Voss**. Platform: **Sam Okada**. Module 10 will schedule the same image as pods in synthetic namespace `baypay-prod`. This module stops at the image.

---

## Learning objectives

After this module you can:

- Explain an OCI image, a container, and a runtime, and say why BayPay packages `payment-service` rather than `BayPayCell`.
- Choose Docker or Podman for a local build without treating the daemon as the production contract — the OCI image is.
- Layer and tag `registry.baypay.example/baypay/payment-service:<tag>` so production never depends on `:latest`.
- Publish port `8080` and refuse the habit of volume-mounting the fat JAR over the image.
- Inject `BAYPAY_DB_*` at run time; never `ENV` a database password into the image.
- Size the Java 21 heap with `UseContainerSupport` and `MaxRAMPercentage` so native headroom remains. Never set `-Xmx` equal to the container limit (L-7.6).
- Harden the runtime: non-root, read-only root filesystem, no `--privileged`, pin base digests.

---

## Prerequisites

- Modules 1–3: `payment-service`, Actuator probes, `application-prod.yml` and `BAYPAY_DB_*`.
- Module 5–6: `BayPayCell` is the source estate; Liberty and Boot are exits. Do not containerize the Deployment Manager.
- L-6.4 (externalized config) and L-7.6 / L-8.7 (cgroup vs `-Xmx`, headroom). If Module 7–8 labs are unfinished, read those two lessons before L-9.6.
- JDK 21 and `./mvnw` if you want to produce the fat JAR locally. See [GETTING_STARTED.md](../../../GETTING_STARTED.md).
- Docker or Podman is **useful, not required**. Paper review of a Dockerfile is enough to finish.

You do **not** need `registry.baypay.example` to exist, OpenShift, `kind`, minikube, or AWS.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional.

| Id | Title | What it unlocks |
|---|---|---|
| [L-9.1](lessons/L-9.1.md) | OCI and container concepts | Image vs container vs runtime; not ND in Docker |
| [L-9.2](lessons/L-9.2.md) | Docker and Podman | Daemon vs daemonless; same OCI image |
| [L-9.3](lessons/L-9.3.md) | Images and registries | Layers, tags, `registry.baypay.example`, never `:latest` |
| [L-9.4](lessons/L-9.4.md) | Networking and volumes | Publish `8080`; do not volume-mount the fat JAR |
| [L-9.5](lessons/L-9.5.md) | Secrets and configuration | `BAYPAY_DB_*` at runtime; no `ENV` password |
| [L-9.6](lessons/L-9.6.md) | Java resource sizing | `MaxRAMPercentage`, headroom; L-7.6 / INC-JVM-806 class |
| [L-9.7](lessons/L-9.7.md) | Container security | Non-root, read-only rootfs, no privileged, pin digests |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [BUILD-901](../../../labs/BUILD-901/README.md) | BUILD | Containerize BayPay | L-9.1, L-9.2, L-9.3 |
| [FIX-902](../../../labs/FIX-902/README.md) | BREAK/FIX | Repair poor Dockerfile | L-9.4, L-9.5 |
| [SECURITY-903](../../../labs/SECURITY-903/README.md) | SECURITY | Harden container | L-9.7 |
| [PERFORMANCE-904](../../../labs/PERFORMANCE-904/README.md) | PERFORMANCE | Optimize Java container | L-9.6 |

Time-box BUILD and PERFORMANCE labs at 60–90 minutes. FIX-902 and SECURITY-903 do not include the answer in the student guide. Write and review files on disk. Running `docker build` / `podman build` is optional. Do not open `solutions/` until you have attempted the lab. Cost **$0**. No AWS.

---

## Assessment and portfolio

1. Complete BUILD-901, FIX-902, SECURITY-903, and PERFORMANCE-904.
2. Take [Q-09](../../quizzes/Q-09.md) when your cohort opens it.
3. Export the hardened Dockerfile and notes using [student/worksheets/PF-container.md](../../../student/worksheets/PF-container.md).

The worksheet is the Module 9 portfolio artifact. Module 10 assumes you can point at `registry.baypay.example/baypay/payment-service:<tag>` and defend non-root, runtime secrets, a pinned tag, and a heap that is **not** the cgroup limit.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/17-kubernetes-and-platform-engineering/overview.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). It is background on why platforms consume OCI images. This module stands alone without it. You do not need a cluster to finish Module 9.

---

## Guardrails

- Do not treat BayPay, `registry.baypay.example`, or Avery Chen as a real employer estate.
- Traditional WAS ND is the **source**. Containers package Boot (or Liberty later), not `dmgr-east`.
- Do not put `BAYPAY_DB_PASSWORD` in a Dockerfile `ENV`, an image layer, or git.
- Do not recommend `:latest` or container-as-root as production defaults.
- Do not set `-Xmx` equal to the container memory limit. Leave room for metaspace, stacks, and native (L-7.6).
- Docker / Podman optional. No live registry. No OpenShift. No AWS. Cost **$0**.
- Instructor rubrics live under `instructor/rubrics/`. Students should not need them to finish the work.
