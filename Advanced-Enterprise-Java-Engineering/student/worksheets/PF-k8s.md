# Portfolio artifact — Kubernetes incident RCA

**Course:** Advanced Enterprise Java Engineering  
**Module:** 10 — Kubernetes and OpenShift  
**Artifact id:** PF-k8s  
**Sources:** pick **one** of INCIDENT-1001 / INC-K8S-1001 through INCIDENT-1006 / INC-K8S-1006  
**Case study:** BayPay Financial Services (fictional)

Export this file (or a copy) when you submit. Do not paste instructor solution text. All names and ids you cite must come from the synthetic pack you chose. Locked instructor RCAs live only under `solutions/`.

**Student:**  
**Date:** 2026-09-06  
**Cohort / reviewer (if any):**  

**Incident chosen (circle one):**  
**1001 CrashLoopBackOff** · 1002 OOMKilled · 1003 Readiness failure · 1004 Bad Secret · 1005 TLS · 1006 Service routing

**Pack path:** `incidents/kubernetes/INC-K8S-1001/`

---

## 1. Symptom

What merchants and the pager showed. Quote objects, Ready counts, events, or HTTP status from **gate 1**:

Pager 18:22Z SEV-2: `payment-service` in `baypay-prod` CrashLoopBackOff; Ingress `payments.apps.baypay.example` 502/503; Ready 0. Harbor Market: Avery Chen payment `c1001a11-0000-4000-8000-111111111001` never returned 201; same Idempotency-Key on retry. Describe Events: `Pulled` `3.9.1` then `Error: crash loop detected, last exit 1`.

What the pods were doing (Running / Ready / Restarts) at the same time:

Status Running / Ready **False** / ContainersReady False. Last State Terminated Reason=Error Exit **1** (~6s). Restart Count **7** (siblings 6–8). Desired 3, Ready 0. Image pulled; not ImagePullBackOff.

---

## 2. Hypothesis timeline

Write in gate order. A lucky label that matches the lab title does not replace this table.

| Gate | File opened | Hypothesis after that file | Evidence that supported or killed it |
|---|---|---|---|
| 1 | `evidence/describe.txt` | Process starts and dies Exit 1; env from `payment-config` after Sam’s 17:40Z roll; not bad image / not OOM | Ready False, Exit 1, Pulled 3.9.1, 2Gi limit, envFrom payment-config |
| 2 | `evidence/logs.txt` | Spring bind of `spring.datasource.url` failed because `BAYPAY_DB_URL` empty; CrashLoop is kubelet reaction | 18:18:06Z BindException; ApplicationContext failed; JAVA_TOOL_OPTIONS 75% (not 806) |
| 3 | `evidence/configmap.yaml` | Sam’s BAYPAY-10011 cleanup **dropped** `BAYPAY_DB_URL` | Keys: profile, USER, LOG_LEVEL, JAVA_TOOL_OPTIONS only |

---

## 3. Root cause (your words)

Mechanism, object names, and the contract that broke (env, probe, selector, cert, heap vs limit). Quote describe, logs, YAML, or openssl. Do not import a Module 8 JVM story unless you say why you ruled it in or out:

Sam Okada rolled ConfigMap `payment-config` (BAYPAY-10011, “non-secret env cleanup”). The live object no longer has `BAYPAY_DB_URL`. Deployment still `envFrom` that ConfigMap (Optional:false). Spring 3.9.1 prod profile binds `spring.datasource.url` from `BAYPAY_DB_URL`, refuses the localhost default, ApplicationContext fails, JVM Exit **1**, kubelet CrashLoopBackOff. Secret `baypay-db` / password was present. Image pull succeeded.

What this is **not** (one sentence, with evidence):

Not a registry outage, not a bad `3.9.1` bit, not INC-JVM-806 / Exit 137, not a probe kill (died at 6s; liveness delay 30s), and not a Postgres bounce candidate — no SQL error in the shipped files.

---

## 4. Stabilize vs remediate

| Stabilize (restores merchant path *now*) | Remediate (keeps the next roll safe) |
|---|---|
| Put `BAYPAY_DB_URL=jdbc:postgresql://db-east.baypay.example:5432/baypay` back on `payment-config`; rolling-restart pods so they remount env. Undo Deployment only if a revision also shipped (timeline names ConfigMap). | Required-key schema / Kyverno / CI boot of the JAR against rendered env. Keep prod fail-fast. Review BAYPAY-10011. Do not bake the URL into the image. |

What you explicitly **did not** do (Postgres bounce, `dmgr-east`, live `kubectl` against a paid cluster, inventing a password in git):

Did not bounce Postgres or `dmgr-east`. Did not rebuild/repin the image. Did not bake `BAYPAY_DB_URL` into the image. Did not put a password in git. Paper restore only.

---

## 5. Evidence table

| Gate | File | One quote (timestamp + text) | What it proved |
|---|---|---|---|
| 1 | `describe.txt` | `Exit Code: 1` … `Successfully pulled image "…:3.9.1"` … `Ready replicas: 0` | Started, died, image ok; desired ≠ Ready |
| 2 | `logs.txt` | `2026-11-03T18:18:06.220Z` … `BAYPAY_DB_URL is not set (empty). Prod profile refuses the localhost default.` | Bind / ApplicationContext, not CrashLoop-as-RCA |
| 3 | `configmap.yaml` | `baypay.example/ticket: BAYPAY-10011` — data has no `BAYPAY_DB_URL` | Which key Sam dropped |

Omitted evidence you wanted, and what you expected it to show:

Deployment revision history: whether only the ConfigMap moved. Thread dump / heap: n/a — process never finished start. DB metrics: would be used only to *rule out* SQL; do not invent them.

---

## 6. Communication samples

### Internal bridge (five lines max)

What we know / do not know / next update:

SEV-2 `baypay-prod` payment-service Ready 0/3; Ingress 502/503. Avery `c1001a11-…-111001` no 201; same Idempotency-Key.  
Exit 1 in ~6s after pull of `3.9.1` — not ImagePull, not 137.  
Spring: `BAYPAY_DB_URL` empty; ApplicationContext did not refresh.  
Sam 17:40Z `payment-config` (BAYPAY-10011) is missing that key. Restoring it; rolling pods. Not a DB outage.  
Next update when a replica is Ready.

### Merchant-safe note

No invented cause. No confidential-sounding runbook language:

We are restoring payment create for Harbor Market. Avery’s authorization `c1001a11-…-111001` did not complete; the same Idempotency-Key can be retried after we confirm the service is taking traffic. We will send an update when a replica is Ready. We are not asking you to change cards or retry a different key yet.

---

## 7. Healthy YAML sketch

Sketch the **intended** `baypay-prod` objects (not the broken incident files). Use names from [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md). Placeholders only for secrets (`${BAYPAY_DB_PASSWORD}`, `***`). You may cite `infrastructure/kubernetes/payment-service/` as the reference.

```yaml
# namespace + Deployment labels + Service selector + Ingress host/TLS + ConfigMap keys + Secret keys
# Reference: infrastructure/kubernetes/payment-service/
apiVersion: v1
kind: Namespace
metadata:
  name: baypay-prod
---
apiVersion: v1
kind: ConfigMap
metadata:
  name: payment-config
  namespace: baypay-prod
  labels:
    app: payment-service
data:
  SPRING_PROFILES_ACTIVE: prod
  BAYPAY_DB_URL: jdbc:postgresql://db-east.baypay.example:5432/baypay
  BAYPAY_DB_USER: baypay_app
  JAVA_TOOL_OPTIONS: -XX:+UseContainerSupport -XX:MaxRAMPercentage=75
---
apiVersion: v1
kind: Secret
metadata:
  name: baypay-db
  namespace: baypay-prod
stringData:
  BAYPAY_DB_PASSWORD: ${BAYPAY_DB_PASSWORD}
---
# Deployment payment-service: replicas 3, labels app=payment-service,
# image registry.baypay.example/baypay/payment-service:3.9.1,
# envFrom payment-config, env BAYPAY_DB_PASSWORD from secretKeyRef baypay-db,
# containerPort 8080, probes /actuator/health/liveness|readiness,
# runAsUser 10001, memory limit 2Gi (not -Xmx=limit)
---
# Service payment-service ClusterIP 8080 selector app=payment-service
# Ingress host payments.apps.baypay.example tls secret payment-tls → Service 8080
# OpenShift Route payment-route: same host
```

What must match across objects (labels, probe paths, env names, heap vs limit):

`app=payment-service` on Deployment template **and** Service selector. Probes hit **8080** `/actuator/health/liveness` and `/readiness`. ConfigMap must keep `BAYPAY_DB_URL`; Secret keeps password. Heap is `MaxRAMPercentage=75` of the **2Gi** limit — never `-Xmx` = limit.

---

## 8. Architecture / trade-off

One policy you would enforce next week (schema, Kyverno, cert-manager, commonLabels, MaxRAMPercentage), and the cost of that policy:

**Required env schema** (Kyverno or CI): `payment-config` must contain `BAYPAY_DB_URL` (and documented `BAYPAY_DB_*` keys) or the apply fails. Cost: a “cleanup” ticket like BAYPAY-10011 is blocked until someone names the URL; false positives if a new optional key is added to the policy. Cheaper than Ready 0 and Avery retries. Do **not** bake the URL into the image to avoid ConfigMap mistakes — rotation and per-env JDBC then become a rebuild. Optional localhost default is a laptop convenience; 3.9.1 prod fail-fast is correct — own the fail in CI with a dry-run boot of the rendered env.

---

## 9. Interview talking points

Write four bullets you would actually say, labeled Engineer / Senior / Staff / Principal:

- Engineer: CrashLoopBackOff is the kubelet backing off. I quote Ready, Restarts, last Exit code, and whether the image pulled before I say “bad image.”
- Senior: Exit 1 in six seconds on Spring is usually bind / ApplicationContext. Exit 137 is OOMKilled. I read logs before I revert the tag.
- Staff: Sam rolled `payment-config` and dropped `BAYPAY_DB_URL`. I restore the key (or undo a Deployment revision that actually shipped). I do not bounce Postgres or bake the URL into the image. Avery reused the Idempotency-Key — good.
- Principal: Required keys in schema plus a CI boot against rendered env. `rollout undo` is stabilize, not a control. Optional JDBC with a localhost default means production discovers the hole; fail-fast in prod without a gate just moves the outage to 10:22.

---

## Honesty

- [x] I did not open `solutions/INCIDENT-100N/` before attempting the worksheet
- [x] I requested evidence in the documented gate order
- [x] Every claim has a source (describe, logs, YAML, events, openssl, or curl paste)
- [x] I did not paste an instructor RCA
- [x] I did not put a live password in this file
- [x] If I had done INC-JVM-806, I did not copy those heap numbers unless they appear in **this** pack
