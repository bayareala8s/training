# INCIDENT-1001 — CrashLoopBackOff

**Type:** INCIDENT  
**Module:** 10 — Kubernetes and OpenShift  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/kubernetes/INC-K8S-1001](../../incidents/kubernetes/INC-K8S-1001/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

10:22 Pacific on a synthetic `baypay-prod` morning in November 2026. Harbor Market reports that `POST /api/v1/payments` never returns 201. The pager names `payment-service` in namespace `baypay-prod`. Teaching-cluster paste shows pods leaving `Running` and sitting in a restart loop. Ingress still has a host. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. Each retry during a CrashLoop is another failed authorization. Finance does not care that the ReplicaSet still lists three desired pods. They care that no Ready replica is taking traffic.

Do not bounce Postgres. Do not bounce `dmgr-east`. This is the container estate in [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md), not the Module 5 cell. A live OpenShift or EKS API is **not** required.

---

## Learning objectives

- Follow gated evidence: `kubectl describe` paste first, then container logs, then the ConfigMap excerpt the Deployment mounts.
- Treat **CrashLoopBackOff** as a restart-policy symptom you still have to reconcile with Exit code and Spring startup, not as a closed RCA.
- Separate “the image is bad” from “the process refused to start with the env it was given.”
- Write stabilization that restores a Ready replica without inventing a database outage.
- Produce a comms update that does not name a missing key before the ConfigMap file supports it.

---

## Architecture

```text
Merchants / Avery Chen
  → Ingress payments.apps.baypay.example
       → Service payment-service (ClusterIP 8080)
            → Deployment payment-service  (3 desired)
                 env from ConfigMap payment-config
                 env from Secret baypay-db
                 Spring Boot 3.5.5 / Java 21
                 → baypay DB
```

One process composition root inside a container. You do not need a live cluster. The contracts are restart count, last Exit code, and whether ApplicationContext finished. Module 8 canary VMs are a different estate.

---

## Prerequisites

- Locked cluster names from [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md).
- Incident worksheet: [student-worksheet.md](../../incidents/kubernetes/INC-K8S-1001/student-worksheet.md).
- Optional PAKS: `docs/17-kubernetes-and-platform-engineering/kubernetes-architecture.md`. Lessons stand alone without it.
- You may read BUILD-305 for Actuator literacy. This pack is about startup, not probes.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/kubernetes/INC-K8S-1001/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset**. Gate 1 is a `describe` paste. Gate 2 is container logs. Gate 3 is a ConfigMap excerpt. The pack README documents what shipped and what was omitted.

Do not open `solutions/INCIDENT-1001/` until you have filled the worksheet through remediation.

Do not run `kubectl` against a paid or shared cluster. The files are the cluster.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note who rolled configuration, and when restarts began.
2. **Gate 1:** open `evidence/describe.txt` only. Record Ready, Restarts, last State, Exit code, and whether the image pulled. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/logs.txt`. Update the hypothesis. Quote the Spring bind / ApplicationContext lines; do not promote `CrashLoopBackOff` to a closed RCA.
4. **Gate 3:** open `evidence/configmap.yaml` only if it answers a question you already wrote about the env the process received.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Sam Okada).
6. Optional: one sentence on required env in a schema versus shipping an optional JDBC URL — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “CrashLoop” or “bad ConfigMap” with no Exit-code-plus-bind comparison scores low on Diagnostic method (see rubric). Skipping to the ConfigMap before a written question also scores low. Opening the solution first fails Diagnostic method.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- The Deployment still shows 3 replicas and merchants see errors: desired is not Ready. Table it.
- You want a thread dump or heap histogram: they are omitted. Say what that would mean for a process that never finished start.
- You are about to bounce Postgres or `dmgr-east`: re-read CLUSTER.md.
- You want to rebuild the image first: write whether `describe` showed ImagePullBackOff or an Exit after start.
- You copied INCIDENT-1002’s memory story: check the Exit code and last Reason before you reuse OOMKilled.
- Logs mention Binding and ApplicationContext: quote them. Do not invent a SQL outage the files do not show.
- You want to `kubectl apply` a live fix: write the change on paper. This lab does not require a cluster.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you which ConfigMap key matters.

---

## Interview questions

1. Why is “CrashLoopBackOff” a weak first sentence when it is a kubelet backoff, not a Java exception?
2. What does Exit 1 after a few seconds usually mean for a Spring Boot process versus Exit 137?
3. Why read logs before you blame the image tag?
4. When do you revert a Deployment revision versus patch the ConfigMap the pods already mount?
5. What does a successful image pull plus a failed ApplicationContext tell you about “the registry is down”?

---

## Architecture/trade-off questions

1. Required env in a schema or policy versus an optional JDBC URL with a localhost default — who owns the fail-fast?
2. Should ConfigMap rolls be gated by a dry-run that boots the JAR with the rendered env?
3. Why is `kubectl rollout undo` a stabilize move and not a remediating control?
4. What do you lose if you bake `BAYPAY_DB_URL` into the image to “avoid ConfigMap mistakes”?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down. No live cluster to delete.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live Kubernetes API. No paid OpenShift.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-1001/` and `instructor/rubrics/INCIDENT-1001.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

CrashLoopBackOff is a restart loop, not a diagnosis. Last Exit code, Spring bind logs, and the ConfigMap the Deployment mounts have to be read together. Stabilization (restore the env contract or revert the revision) is a different sentence from remediation (required keys in schema; do not ship an optional URL). A lucky CrashLoop label does not replace gate order.

---

## Portfolio deliverable

Attach the completed INC-K8S-1001 worksheet to your notes if this is the Module 10 incident you will write up. The Module 10 portfolio artifact is [student/worksheets/PF-k8s.md](../../student/worksheets/PF-k8s.md): you pick **one** of INCIDENT-1001 through INCIDENT-1006 and write the scored RCA plus a healthy YAML sketch there.
