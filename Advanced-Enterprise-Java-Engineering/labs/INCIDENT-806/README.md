# INCIDENT-806 — Container OOM

**Type:** INCIDENT  
**Module:** 08 — JVM Troubleshooting  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/jvm/INC-JVM-806](../../incidents/jvm/INC-JVM-806/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

16:48 Pacific on a synthetic prod-east afternoon in October 2026. Harbor Market reports intermittent 502s. The pager names `payment-service` on `pay-prod-east-2` restarting. Kubernetes (teaching cluster) shows the canary pod leaving and returning. Actuator is not there to ask while the process is gone. `pay-prod-east-1` is quiet. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. Each retry during a restart is another 502. Finance does not care that the new pod becomes `Running`. They care that the canary keeps dying on the same memory limit.

`pay-prod-east-1` remaining healthy is part of the first sentence. Do not bounce Postgres. Do not bounce `dmgr-east`. This is still the Boot canary estate in [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md), now with a container memory limit stated in the pack.

---

## Learning objectives

- Follow gated evidence: dashboard first, then kube events, then JVM flags / last GC.
- Treat **OOMKilled** as a cgroup story you still have to reconcile with heap flags, not as a Java `OutOfMemoryError` by default.
- Separate heap OOME from the kernel killing the process at the container limit.
- Write stabilization that restores a living replica without pretending `-Xmx` equal to the limit is “using all the RAM.”
- Produce a comms update that does not invent a leak before the flags and events support one.

---

## Architecture

```text
Merchants / Avery Chen
  → load balancer
       → pay-prod-east-1   payment-service 3.8.0   (stable VM or larger pod)
       → pay-prod-east-2   payment-service canary pod
            cgroup memory limit (see pack)
            JAVA_TOOL_OPTIONS / heap flags (see pack)
            → baypay DB
```

One process composition root inside a container. You do not need a live cluster. The contracts are restart count, `OOMKilled`, and whether `-Xmx` leaves room for metaspace, stacks, and native. Module 5 WAS cells are a different estate.

---

## Prerequisites

- L-8.7 (container OOM) completed, or read in the same sitting.
- Locked runtime names from [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).
- Incident worksheet: [student-worksheet.md](../../incidents/jvm/INC-JVM-806/student-worksheet.md).
- Optional PAKS: `docs/27-production-failures/failure-analysis-methodology.md`. Lessons stand alone without it.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/jvm/INC-JVM-806/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset**. Gate 2 is **kube events**, not application `logs.txt`. Gate 3 is JVM flags (and what they imply for the last GC). The pack README documents what shipped and what was omitted.

Do not open `solutions/INCIDENT-806/` until you have filled the worksheet through remediation.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note when the canary was resized or flagged, and when restarts began.
2. **Gate 1:** open `evidence/dashboard.md` only. Record restarts, heap used, RSS if present, and whether `pay-prod-east-1` shares the page. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/kube-events.md`. Update the hypothesis. Quote the reason; do not promote `OOMKilled` to a closed Java-heap RCA.
4. **Gate 3:** open `evidence/jvm-flags.md` only if it answers a question you already wrote about heap versus cgroup limit.
5. Write stabilization, remediation, and a 5-line comms update. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Jordan Voss).
6. Optional: one sentence on a heap percentage of the cgroup versus a fixed `-Xmx` that matches the limit — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “container OOM” with no flag-versus-limit comparison scores low on Diagnostic method (see rubric). Skipping to flags before a written question also scores low.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- The pod is `Running` and merchants still saw 502s: that is the restart window. Table it.
- You want a Java `hs_err` heap OOME: it may be absent. Say what that would mean.
- You are about to bounce Postgres or `dmgr-east`: re-read RUNTIME.md.
- You want to raise `-Xmx` to match a higher limit 1:1: write what still sits outside the heap.
- Dashboard heap used is not 1536 MB: this canary may have a smaller heap than the other Module 8 packs.
- You copied INCIDENT-802’s cache story: check whether this process lived long enough to climb for two days.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you the correct percentage of the limit.

---

## Interview questions

1. Why is “the JVM ran out of heap” a weak first sentence when the event is `OOMKilled` and there is no Java OOME?
2. What sits outside `-Xmx` in a Spring Boot process (name three)?
3. Why can `UseContainerSupport` still fail you if `-Xmx` is pinned to the limit?
4. When do you raise the cgroup limit versus shrink the heap for the same pod?
5. What does a last successful GC at 400 MB used tell you if the limit is 512Mi?

---

## Architecture/trade-off questions

1. A heap percentage of the container limit versus a reviewed `-Xmx` that leaves headroom — who owns the number when the limit changes?
2. Should the canary pod match east-1’s memory, or is a smaller canary an acceptable risk if flags leave headroom?
3. Native memory tracking versus “just add 2Gi” — what would you measure next week?
4. Why is matching `-Xmx` to the limit a reliability smell rather than “efficient packing”?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down. No live cluster to delete.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live Kubernetes API.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-806/` and `instructor/rubrics/INCIDENT-806.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

A container kill is not automatically a Java heap OOME. Flags and the cgroup limit have to be read together. Stabilization (raise the limit or drop `-Xmx`, then restart) is a different sentence from remediation (never set heap equal to the limit; leave headroom). A lucky “OOM” label does not replace gate order.

---

## Portfolio deliverable

Attach the completed INC-JVM-806 worksheet to your notes if this is the Module 8 incident you will write up. The Module 8 portfolio artifact is [student/worksheets/PF-jvm-rca.md](../../student/worksheets/PF-jvm-rca.md): you pick **one** of INCIDENT-801 through INCIDENT-806 and write the scored RCA there.
