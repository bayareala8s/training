# INCIDENT-1003 — Readiness failure

**Type:** INCIDENT  
**Module:** 10 — Kubernetes and OpenShift  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/kubernetes/INC-K8S-1003](../../incidents/kubernetes/INC-K8S-1003/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

09:40 Pacific on a synthetic `baypay-prod` morning in November 2026. Harbor Market reports HTTP 503 on `payments.apps.baypay.example`. The pager names `payment-service`. Teaching-cluster paste shows pods **Running** and not Ready. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. A 503 from Ingress is not a domain decline. Finance does not care that `kubectl get pods` shows `Running`. They care that the Service has nobody to send traffic to.

Do not bounce Postgres. Do not bounce `dmgr-east`. Probe contracts come from BUILD-305 and [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md). A live cluster is **not** required.

---

## Learning objectives

- Follow gated evidence: describe first, then Endpoints, then the Ingress curl paste.
- Treat **Running** as a container-process fact, not as “the Service can take traffic.”
- Separate liveness success from readiness failure when the paths differ.
- Write stabilization that restores Ready without pretending a bounce fixes a 404 probe.
- Produce a comms update that does not invent a database outage before Endpoints support it.

---

## Architecture

```text
Merchants / Avery Chen
  → Ingress payments.apps.baypay.example
       → Service payment-service (ClusterIP 8080)
            → Endpoints (Ready pods only)
                 kubelet readinessProbe  (path in describe)
                 kubelet livenessProbe   (path in describe)
                 Spring Actuator groups    (BUILD-305)
```

One process, two probe questions. You do not need a live cluster. The contracts are Ready 0/1, Endpoints empty, and the HTTP status the probe received. Module 5 plugin-cfg membership is a different estate.

---

## Prerequisites

- BUILD-305 (liveness / readiness / aggregate health) completed, or read in the same sitting.
- Locked cluster names from [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md).
- Incident worksheet: [student-worksheet.md](../../incidents/kubernetes/INC-K8S-1003/student-worksheet.md).
- Optional PAKS: `docs/17-kubernetes-and-platform-engineering/kubernetes-architecture.md`. Lessons stand alone without it.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/kubernetes/INC-K8S-1003/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset**. Gate 1 is `describe`. Gate 2 is Endpoints. Gate 3 is an Ingress curl paste. The pack README documents what shipped and what was omitted.

Do not open `solutions/INCIDENT-1003/` until you have filled the worksheet through remediation.

Do not run `kubectl` against a paid or shared cluster. The files are the cluster.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note who shipped the image or probe YAML, and when 503s began.
2. **Gate 1:** open `evidence/describe.txt` only. Record Ready, probe paths, and probe HTTP status. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/endpoints.txt`. Update the hypothesis. Quote emptiness; do not promote “503” to a closed RCA.
4. **Gate 3:** open `evidence/curl-ingress.txt` only if it answers a question you already wrote about the edge versus the pod.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Sam Okada).
6. Optional: one sentence mapping BUILD-305 groups (`/actuator/health`, `/liveness`, `/readiness`) to kubelet probes — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “readiness” with no probe-path-versus-Actuator comparison scores low on Diagnostic method (see rubric). Skipping to curl before a written question also scores low. Opening the solution first fails Diagnostic method.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- Pods are Running and merchants see 503: Running is not Ready. Table it.
- You want application `logs.txt`: they are omitted. Write what a 404 on the probe path would look like versus a DB-down readiness.
- You are about to bounce Postgres or `dmgr-east`: re-read CLUSTER.md.
- You want to delete the Ingress: write whether Endpoints are empty first.
- You copied INCIDENT-1006’s selector story: check whether describe already names a probe status.
- You copied INCIDENT-1001’s CrashLoop: Ready 0/1 on a Running pod is a different last State.
- You want to `kubectl apply` a live fix: write the change on paper. This lab does not require a cluster.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you which Actuator path the image exposes.

---

## Interview questions

1. Why is “the pods are up” a weak first sentence when Ready is 0/1?
2. What does a 404 on a readiness path prove that a 503 from Ingress does not?
3. Why can liveness pass while readiness fails?
4. When do you change the probe path versus add the readiness group to the image?
5. How does an empty Endpoints object explain a 503 without blaming PostgreSQL?

---

## Architecture/trade-off questions

1. Who owns the contract that kubelet paths match BUILD-305 groups — app repo or platform YAML?
2. Should a CI check curl the probe paths against the image before the Deployment is merged?
3. Why is a single `/actuator/health` probe a reliability smell for both liveness and readiness?
4. What do you lose if readiness includes a 30-second database blip that should not restart the JVM?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down. No live cluster to delete.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live Kubernetes API. No paid OpenShift.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-1003/` and `instructor/rubrics/INCIDENT-1003.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

Running is not Ready. Probe HTTP status, Endpoints, and the Ingress 503 have to be read together. Stabilization (fix the probe path or add the readiness group) is a different sentence from remediation (probes match Actuator groups from BUILD-305). A lucky “readiness” label does not replace gate order.

---

## Portfolio deliverable

Attach the completed INC-K8S-1003 worksheet to your notes if this is the Module 10 incident you will write up. The Module 10 portfolio artifact is [student/worksheets/PF-k8s.md](../../student/worksheets/PF-k8s.md): you pick **one** of INCIDENT-1001 through INCIDENT-1006 and write the scored RCA plus a healthy YAML sketch there.
