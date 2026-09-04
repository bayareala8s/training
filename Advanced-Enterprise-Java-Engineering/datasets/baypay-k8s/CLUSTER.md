# BayPay container and cluster notes — Modules 9–10

**Fictional.** Registry, namespaces, and kubectl output are teaching data. Not a real cluster.

Students may read this file. Instructor RCAs live only under `solutions/`.

## Delivery

- **Module 9:** Dockerfile and image design on disk. Docker or Podman is useful and **not required** to pass if you write and review the files.
- **Module 10:** Paper architecture plus YAML. `kind` / minikube is optional. A live OpenShift cluster is **not** required.
- Cost is **$0** unless you choose to run a local engine. No AWS in this stage (Module 11).

## Image contract (Module 9)

| Field | Value |
|---|---|
| Image | `registry.baypay.example/baypay/payment-service:<tag>` |
| Base (target) | `eclipse-temurin:21-jre` (not a full JDK in the runtime stage) |
| Port | `8080` |
| User | non-root numeric UID (example `10001`) |
| Config | `BAYPAY_DB_*` from env — never baked into the image |
| JVM | `UseContainerSupport`; **do not** set `-Xmx` equal to the container memory limit |

The application is still `reference-apps/baypay` (Java 21, Spring Boot 3.5.5). Liveness `/actuator/health/liveness`. Readiness `/actuator/health/readiness`.

## Synthetic cluster (Module 10)

| Object | Name |
|---|---|
| Namespace / Project | `baypay-prod` |
| Deployment | `payment-service` |
| ReplicaSet / replicas | 3 (when healthy) |
| Pod labels (intended) | `app=payment-service` |
| Service | `payment-service` ClusterIP `8080` |
| Ingress | host `payments.apps.baypay.example` |
| OpenShift Route (same host) | `payment-route` — Route is the OpenShift front door; Ingress is the Kubernetes one |
| ConfigMap | `payment-config` |
| Secret | `baypay-db` keys `BAYPAY_DB_USER`, `BAYPAY_DB_PASSWORD` |
| TLS Secret | `payment-tls` |
| Registry pull | `registry.baypay.example` (synthetic) |

Canary sibling from Module 8 (`pay-prod-east-2`) is the **same app**, now scheduled as pods. Do not bounce `dmgr-east` for a kube page.

Demo customer Avery Chen: `11111111-1111-1111-1111-111111111111`.  
On-call: Riley Okonkwo. SRE: Priya Nair. Platform: Sam Okada.

## What you must not do

- Run a paid OpenShift or EKS cluster for these labs.
- Put database passwords in Dockerfile `ENV` or git.
- Recommend `:latest` or container-as-root as production defaults.
- Treat CrashLoopBackOff, OOMKilled, or empty Endpoints as a closed RCA without evidence.

## Optional PAKS

- Module 9: `docs/17-kubernetes-and-platform-engineering/overview.md`
- Module 10: `docs/17-kubernetes-and-platform-engineering/kubernetes-architecture.md`

Lessons stand alone without PAKS.
