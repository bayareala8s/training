# INCIDENT-1002 — OOMKilled

**Type:** INCIDENT  
**Module:** 10 — Kubernetes and OpenShift  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/kubernetes/INC-K8S-1002](../../incidents/kubernetes/INC-K8S-1002/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

15:10 Pacific on a synthetic `baypay-prod` afternoon in November 2026. Harbor Market reports intermittent 502s. The pager names `payment-service` pods restarting in namespace `baypay-prod`. Teaching-cluster paste shows Last State `OOMKilled`. You are the engineer on call. The incident pack is synthetic BayPay data.

This is the **same class** as [INCIDENT-806](../INCIDENT-806/README.md), but the evidence surface is `kubectl describe` plus events — not the Module 8 dashboard pack. Do not copy 806’s numbers unless they appear in **this** pack.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. Each retry during a kill is another 502. Finance does not care that the new container becomes `Running`. They care that replicas keep dying on the same memory limit.

Do not bounce Postgres. Do not bounce `dmgr-east`. Locked names live in [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md). A live cluster is **not** required.

---

## Learning objectives

- Follow gated evidence: describe first, then events, then JVM flags from last state.
- Treat **OOMKilled** as a cgroup story you still have to reconcile with heap flags, not as a Java `OutOfMemoryError` by default.
- Separate heap OOME from the kubelet killing the container at the limit.
- Write stabilization that restores a living replica without pretending `-Xmx` equal to the limit is “using all the RAM.”
- Produce a comms update that does not invent a leak before flags and events support one.

---

## Architecture

```text
Merchants / Avery Chen
  → Ingress payments.apps.baypay.example
       → Service payment-service
            → Pods payment-service-*
                 cgroup memory limit (see pack)
                 JAVA_TOOL_OPTIONS / heap flags (see pack)
                 → baypay DB
```

One process composition root inside a container. You do not need a live cluster. The contracts are Last State, Exit 137, limit, and whether `-Xmx` leaves room for metaspace, stacks, and native. Module 5 WAS cells are a different estate.

---

## Prerequisites

- L-8.7 / INCIDENT-806 completed, or read CLUSTER.md in the same sitting.
- Locked cluster names from [datasets/baypay-k8s/CLUSTER.md](../../datasets/baypay-k8s/CLUSTER.md).
- Incident worksheet: [student-worksheet.md](../../incidents/kubernetes/INC-K8S-1002/student-worksheet.md).
- Optional PAKS: `docs/17-kubernetes-and-platform-engineering/kubernetes-architecture.md`. Lessons stand alone without it.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/kubernetes/INC-K8S-1002/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset**. Gate 1 is `describe`. Gate 2 is events. Gate 3 is JVM flags from last state. The pack README documents what shipped and what was omitted.

Do not open `solutions/INCIDENT-1002/` until you have filled the worksheet through remediation.

Do not run `kubectl` against a paid or shared cluster. The files are the cluster.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note when the limit or flags changed, and when kills began.
2. **Gate 1:** open `evidence/describe.txt` only. Record Last State, Exit code, limit, and `JAVA_TOOL_OPTIONS` if present. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/events.txt`. Update the hypothesis. Quote the reason; do not promote `OOMKilled` to a closed Java-heap RCA.
4. **Gate 3:** open `evidence/jvm-flags.txt` only if it answers a question you already wrote about heap versus cgroup limit.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Sam Okada).
6. Optional: one sentence on `MaxRAMPercentage=75` versus a fixed `-Xmx` that matches the limit — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “container OOM” with no flag-versus-limit comparison scores low on Diagnostic method (see rubric). Skipping to flags before a written question also scores low. Opening the solution first fails Diagnostic method.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- The pod is `Running` and merchants still saw 502s: that is the restart window. Table it.
- You want a Java `hs_err` heap OOME: it may be absent. Say what that would mean.
- You are about to bounce Postgres or `dmgr-east`: re-read CLUSTER.md.
- You want to raise `-Xmx` to match a higher limit 1:1: write what still sits outside the heap.
- You pasted INCIDENT-806’s 389 MB GC line: only use numbers from **this** pack.
- You copied INCIDENT-1001’s CrashLoop Exit 1: check Last State Reason before you reuse bind logs.
- You want to `kubectl apply` a live fix: write the change on paper. This lab does not require a cluster.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you the correct percentage of the limit.

---

## Interview questions

1. Why is “the JVM ran out of heap” a weak first sentence when the event is `OOMKilled` and there is no Java OOME?
2. What sits outside `-Xmx` in a Spring Boot process (name three)?
3. Why can `UseContainerSupport` still fail you if `-Xmx` is pinned to the limit?
4. When do you raise the cgroup limit versus shrink the heap for the same pod?
5. How is this pack’s evidence different from INCIDENT-806 if the class is the same?

---

## Architecture/trade-off questions

1. A heap percentage of the container limit versus a reviewed `-Xmx` that leaves headroom — who owns the number when the limit changes?
2. Should a “right-size” roll require a flag review ticket, or is a YAML limit change enough?
3. Native memory tracking versus “just add 2Gi” — what would you measure next week?
4. Why is matching `-Xmx` to the limit a reliability smell rather than “efficient packing”?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down. No live cluster to delete.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live Kubernetes API. No paid OpenShift.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-1002/` and `instructor/rubrics/INCIDENT-1002.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

A container kill is not automatically a Java heap OOME. Flags and the cgroup limit have to be read together on `describe` and events. Stabilization (raise the limit or drop `-Xmx`, then restart) is a different sentence from remediation (never set heap equal to the limit; leave headroom). A lucky “OOM” label does not replace gate order.

---

## Portfolio deliverable

Attach the completed INC-K8S-1002 worksheet to your notes if this is the Module 10 incident you will write up. The Module 10 portfolio artifact is [student/worksheets/PF-k8s.md](../../student/worksheets/PF-k8s.md): you pick **one** of INCIDENT-1001 through INCIDENT-1006 and write the scored RCA plus a healthy YAML sketch there.
