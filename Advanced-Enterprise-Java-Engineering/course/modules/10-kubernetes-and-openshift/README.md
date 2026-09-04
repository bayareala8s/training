# Module 10 — Kubernetes and OpenShift

**Duration:** ~3 hours of lessons plus 6 incident labs  
**Case study:** BayPay Financial Services (fictional)  
**Theme:** Run BayPay on Kubernetes; treat OpenShift as a Route / SCC / Project overlay  
**Portfolio artifact:** Kubernetes incident RCA plus healthy-estate sketch from [student/worksheets/PF-k8s.md](../../../student/worksheets/PF-k8s.md)

BayPay is a fictional payments company used throughout this course. It is not a real bank, card network, or employer. Every customer, namespace, hostname, Secret, and kubectl excerpt you see is synthetic. Do not treat this pack as a real employer’s cluster.

**Delivery note:** this module is **paper architecture plus YAML**. You may apply manifests on `kind` or minikube if you want a local API server. A live OpenShift cluster is **not** required. You will not stand up EKS, ROSA, or a paid sandbox. Cost is **$0**.

---

## Business context

Module 9 packaged `payment-service` as an image. This module **schedules** that image. Harbor Bike Co still charges Avery Chen `$84.00` through `POST /api/v1/payments`. The process is the same Java 21 / Spring Boot 3.5.5 modular monolith in `reference-apps/baypay`. The difference is the control plane: a Deployment in namespace `baypay-prod` keeps three Pods labeled `app=payment-service`, a ClusterIP Service publishes port `8080`, and a layer-7 front door (`Ingress` on Kubernetes, `Route` on OpenShift) presents host `payments.apps.baypay.example`.

The Module 8 canary `pay-prod-east-2` is the **same application**, now a Pod. You diagnose that Pod. You do **not** bounce `dmgr-east`. You do **not** recommend stuffing `BayPayCell` into a Pod.

OpenShift is taught as a **compatible overlay**, not a second platform to install. A Project is a Namespace with extra policy. A Route does the same job as Ingress (terminate TLS, pick a Service). SCCs constrain what a Pod may do. `oc` speaks the same objects `kubectl` does, plus those overlays.

The locked inventory lives in [datasets/baypay-k8s/CLUSTER.md](../../../datasets/baypay-k8s/CLUSTER.md). Reuse those names in every diagram, lab, and interview answer:

| Object | Locked name |
|---|---|
| Namespace / Project | `baypay-prod` |
| Deployment | `payment-service` (3 replicas when healthy) |
| Pod labels | `app=payment-service` |
| Service | `payment-service` ClusterIP `8080` |
| Ingress host | `payments.apps.baypay.example` |
| OpenShift Route | `payment-route` (same host) |
| ConfigMap | `payment-config` |
| Secret | `baypay-db` keys `BAYPAY_DB_USER`, `BAYPAY_DB_PASSWORD` |
| TLS Secret | `payment-tls` |
| Image | `registry.baypay.example/baypay/payment-service:<tag>` |

Demo identities remain:

| Role | Synthetic id |
|---|---|
| Customer Avery Chen | `11111111-1111-1111-1111-111111111111` |
| Active USD account | `22222222-2222-2222-2222-222222222221` |

On-call names: **Riley Okonkwo** (application), **Priya Nair** (SRE), **Sam Okada** (platform), **Jordan Voss** (release). Payment happy path is still `RECEIVED → VALIDATING → AUTHORIZED → PROCESSING → COMPLETED`. A Pod `Ready` is not that sentence.

---

## Learning objectives

After this module you can:

- Draw Deployment → ReplicaSet → Pod for `payment-service` in `baypay-prod`, and say what a ReplicaSet actually maintains.
- Route Avery Chen to a Pod through a ClusterIP Service and either Ingress or OpenShift Route `payment-route` on host `payments.apps.baypay.example`, and refuse to treat those two APIs as different products with the same name.
- Inject `payment-config` and Secret `baypay-db` so `BAYPAY_DB_*` never lives in the image or in git.
- Read ServiceAccount, Role, and NetworkPolicy well enough to talk blast radius without inventing a service mesh.
- Map `/actuator/health/liveness` and `/actuator/health/readiness` onto kube probes, and size memory so `-Xmx` is not the container limit.
- Explain a rolling update, a rollback, and HPA *literacy* on paper — without requiring a live metrics-server.

---

## Prerequisites

- Modules 1–8, especially L-3.5 (liveness vs readiness), L-6.4 (`BAYPAY_DB_*`), L-7.6 / L-8.7 (cgroup vs `-Xmx`), and the Boot canary habit (do not bounce `dmgr-east`).
- Module 9 image contract in [CLUSTER.md](../../../datasets/baypay-k8s/CLUSTER.md): `eclipse-temurin:21-jre`, port `8080`, non-root UID, config from env. If Module 9 lessons are still in flight, CLUSTER.md is enough.
- Comfort reading YAML as desired state. You do **not** need a running cluster to pass.

You do **not** need OpenShift Local, a pull secret, or AWS. Optional `kind` / minikube is a convenience, not a grade gate.

---

## Lessons (30 minutes each)

Complete in order. Each lesson is self-contained; PAKS links are optional. Lessons teach **objects and method**. They do not name the root cause of any INCIDENT-100x pack.

| Id | Title | What it unlocks |
|---|---|---|
| [L-10.1](lessons/L-10.1.md) | Pods, Deployments, ReplicaSets | Desired replicas, labels, AEJE-D-042 |
| [L-10.2](lessons/L-10.2.md) | Services, Ingress, OpenShift Routes | ClusterIP, L7 front door, AEJE-D-043 |
| [L-10.3](lessons/L-10.3.md) | ConfigMaps and Secrets | `payment-config`, `baypay-db`, `BAYPAY_DB_*` |
| [L-10.4](lessons/L-10.4.md) | RBAC and networking | ServiceAccount, Role, NetworkPolicy literacy |
| [L-10.5](lessons/L-10.5.md) | Probes and resources | Liveness vs readiness vs startup; limit vs `-Xmx` |
| [L-10.6](lessons/L-10.6.md) | Autoscaling and rollout/rollback | HPA literacy, rolling update, undo |

---

## Labs

| Id | Type | Title | After |
|---|---|---|---|
| [INCIDENT-1001](../../../labs/INCIDENT-1001/README.md) | INCIDENT | CrashLoopBackOff | L-10.1, L-10.6 |
| [INCIDENT-1002](../../../labs/INCIDENT-1002/README.md) | INCIDENT | OOMKilled | L-10.5 |
| [INCIDENT-1003](../../../labs/INCIDENT-1003/README.md) | INCIDENT | Readiness failure | L-10.5 |
| [INCIDENT-1004](../../../labs/INCIDENT-1004/README.md) | INCIDENT | Bad Secret | L-10.3 |
| [INCIDENT-1005](../../../labs/INCIDENT-1005/README.md) | INCIDENT | TLS/certificate issue | L-10.2 |
| [INCIDENT-1006](../../../labs/INCIDENT-1006/README.md) | INCIDENT | Service routing failure | L-10.2, L-10.4 |

Time-box each incident at 45–75 minutes. Student guides show **symptoms only**. Work the pack’s gates. Do not open `solutions/INCIDENT-100x/` until the worksheet has hypothesis, evidence, next investigation, stabilize, remediate, and comms.

Treat CrashLoopBackOff, OOMKilled, or empty Endpoints as *symptom classes*, not closed RCAs. Quote *this* pack’s evidence. A lucky label that matches the title does **not** max Diagnostic method.

---

## Assessment and portfolio

1. Complete all six incidents with gated evidence in order.
2. Take [Q-10](../../quizzes/Q-10.md) when your cohort opens it.
3. Export one incident RCA and a healthy `baypay-prod` YAML sketch using [student/worksheets/PF-k8s.md](../../../student/worksheets/PF-k8s.md).

The worksheet is the Module 10 portfolio artifact. Module 11 will assume you can point at `baypay-prod` and explain Service versus Route versus Ingress without recommending ND-in-a-pod.

---

## Related PAKS deep dive (optional)

If you have access to the Principal Architect Knowledge System, read `docs/17-kubernetes-and-platform-engineering/kubernetes-architecture.md` and `docs/17-kubernetes-and-platform-engineering/platform-engineering-and-gitops.md` (hosted at [paks.bayareala8s.com](https://paks.bayareala8s.com) when your cohort has a login). They deepen control-plane and desired-state ideas. This module stands alone without them.

---

## Guardrails

- Diagnose Pods in `baypay-prod`. Do not restart `BayPayCell` or bounce `dmgr-east` for a kube page.
- Simulation first: YAML on disk, paper Endpoints, optional `kind` / minikube. Live OpenShift is **not** required.
- Do not recommend traditional WAS ND inside a container. The cell is the estate you leave.
- Do not put `BAYPAY_DB_PASSWORD` in a Dockerfile, ConfigMap, or git. Do not ship `:latest` as a production default.
- Do not set `-Xmx` equal to the container memory limit (L-7.6, L-8.7, L-10.5).
- Do not invent a real employer service mesh. NetworkPolicy literacy is enough.
- Local paper and optional local clusters cost **$0**. No AWS in this stage (Module 11).
- Instructor solutions live under `solutions/`. Rubrics live under `instructor/rubrics/`.
