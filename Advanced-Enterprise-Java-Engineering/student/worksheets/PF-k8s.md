# Portfolio artifact — Kubernetes incident RCA

**Course:** Advanced Enterprise Java Engineering  
**Module:** 10 — Kubernetes and OpenShift  
**Artifact id:** PF-k8s  
**Sources:** pick **one** of INCIDENT-1001 / INC-K8S-1001 through INCIDENT-1006 / INC-K8S-1006  
**Case study:** BayPay Financial Services (fictional)

Export this file (or a copy) when you submit. Do not paste instructor solution text. All names and ids you cite must come from the synthetic pack you chose. Locked instructor RCAs live only under `solutions/`.

**Student:**  
**Date:**  
**Cohort / reviewer (if any):**  

**Incident chosen (circle one):**  
1001 CrashLoopBackOff · 1002 OOMKilled · 1003 Readiness failure · 1004 Bad Secret · 1005 TLS · 1006 Service routing

**Pack path:** `incidents/kubernetes/INC-K8S-100N/`

---

## 1. Symptom

What merchants and the pager showed. Quote objects, Ready counts, events, or HTTP status from **gate 1**:

What the pods were doing (Running / Ready / Restarts) at the same time:

---

## 2. Hypothesis timeline

Write in gate order. A lucky label that matches the lab title does not replace this table.

| Gate | File opened | Hypothesis after that file | Evidence that supported or killed it |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

---

## 3. Root cause (your words)

Mechanism, object names, and the contract that broke (env, probe, selector, cert, heap vs limit). Quote describe, logs, YAML, or openssl. Do not import a Module 8 JVM story unless you say why you ruled it in or out:

What this is **not** (one sentence, with evidence):

---

## 4. Stabilize vs remediate

| Stabilize (restores merchant path *now*) | Remediate (keeps the next roll safe) |
|---|---|
|  |  |

What you explicitly **did not** do (Postgres bounce, `dmgr-east`, live `kubectl` against a paid cluster, inventing a password in git):

---

## 5. Evidence table

| Gate | File | One quote (timestamp + text) | What it proved |
|---|---|---|---|
| 1 | | | |
| 2 | | | |
| 3 | | | |

Omitted evidence you wanted, and what you expected it to show:

---

## 6. Communication samples

### Internal bridge (five lines max)

What we know / do not know / next update:

### Merchant-safe note

No invented cause. No confidential-sounding runbook language:

---

## 7. Healthy YAML sketch

Sketch the **intended** `baypay-prod` objects (not the broken incident files). Use names from [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md). Placeholders only for secrets (`${BAYPAY_DB_PASSWORD}`, `***`). You may cite `infrastructure/kubernetes/payment-service/` as the reference.

```yaml
# namespace + Deployment labels + Service selector + Ingress host/TLS + ConfigMap keys + Secret keys
```

What must match across objects (labels, probe paths, env names, heap vs limit):

---

## 8. Architecture / trade-off

One policy you would enforce next week (schema, Kyverno, cert-manager, commonLabels, MaxRAMPercentage), and the cost of that policy:

---

## 9. Interview talking points

Write four bullets you would actually say, labeled Engineer / Senior / Staff / Principal:

- Engineer:
- Senior:
- Staff:
- Principal:

---

## Honesty

- [ ] I did not open `solutions/INCIDENT-100N/` before attempting the worksheet
- [ ] I requested evidence in the documented gate order
- [ ] Every claim has a source (describe, logs, YAML, events, openssl, or curl paste)
- [ ] I did not paste an instructor RCA
- [ ] I did not put a live password in this file
- [ ] If I had done INC-JVM-806, I did not copy those heap numbers unless they appear in **this** pack
