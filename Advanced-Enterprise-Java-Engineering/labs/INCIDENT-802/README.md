# INCIDENT-802 — Memory leak

**Type:** INCIDENT  
**Module:** 08 — JVM Troubleshooting  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/jvm/INC-JVM-802](../../incidents/jvm/INC-JVM-802/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

14:42 Pacific on a synthetic prod-east afternoon in October 2026. Two days after a canary cut, Harbor Market reports slower creates and a few 502s when `pay-prod-east-2` disappears from the load balancer and comes back. The pager names `payment-service` heap and old-generation usage on that instance. Actuator still returns up until the process is recycled. `pay-prod-east-1` is quiet. You are the engineer on call. The incident pack is synthetic BayPay data.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. Each retry is another object graph on the replica that is already retaining memory. Finance does not care that a heap chart is interesting. They care that the canary keeps falling out of rotation and that duplicate attempts must still be idempotent.

`pay-prod-east-1` remaining healthy is part of the first sentence you write. Do not bounce Postgres. Do not bounce `dmgr-east`. This estate is the Boot canary in [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).

---

## Learning objectives

- Follow gated evidence: dashboard first, then logs, then the heap histogram.
- Treat **old-generation climb** as a growth story you still have to name, not as a finished leak label.
- Separate a rising retained set from short-lived allocation (Module 8 has more than one heap-shaped page).
- Write stabilization that restores capacity without pretending a bounce is a cure.
- Produce a comms update that does not invent a GC bug you have not supported.

---

## Architecture

```text
Merchants / Avery Chen
  → load balancer
       → pay-prod-east-1   payment-service 3.8.0   (stable)
       → pay-prod-east-2   payment-service canary  (first place this page lands)
            → baypay DB
            → in-process caches and maps (whatever the pack shows)
```

One process composition root (`payment-service`). You do not need a live heap dump file. The contracts are old-gen trend, histogram class names, and whether east-1 shares the growth. A histogram without a time story is not a closed leak.

---

## Prerequisites

- L-8.2 (heap-dump reasoning) and L-8.4 (memory leaks) completed, or read in the same sitting.
- Locked runtime names from [datasets/baypay-jvm/RUNTIME.md](../../datasets/baypay-jvm/RUNTIME.md).
- Incident worksheet: [student-worksheet.md](../../incidents/jvm/INC-JVM-802/student-worksheet.md).
- Optional PAKS: `docs/27-production-failures/failure-analysis-methodology.md`. Lessons stand alone without it.

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/jvm/INC-JVM-802/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset** of the evidence kinds the course catalog lists. The pack README documents what shipped and what was omitted. Do not invent a thread dump or a full `jmap -dump` file.

Do not open `solutions/INCIDENT-802/` until you have filled the worksheet through remediation.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note the gate rules, which version is on the canary, and when heap alarms started relative to the deploy.
2. **Gate 1:** open `evidence/dashboard.md` only. Record old-gen, heap used, GC frequency, and whether `pay-prod-east-1` shares the climb. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/logs.txt`. Update the hypothesis. Quote sizes or feature flags; do not promote a log phrase to a closed RCA.
4. **Gate 3:** open `evidence/heap-histogram.md` only if it answers a question you already wrote about *what* is retained.
5. Write stabilization, remediation, and a 5-line comms update on the worksheet. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Jordan Voss).
6. Optional: one sentence on how `jcmd <pid> GC.class_histogram` relates to this teaching file — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “it’s a leak” with no growth story and no histogram classes scores low on Diagnostic method (see rubric). Skipping to the histogram before a written question also scores low.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- Heap is high and GC is working: that is data. Write whether old gen **returns** after a collection.
- You want a thread dump: it is not in this pack. Say so and work with dashboard, logs, and the histogram.
- You are about to bounce Postgres or `dmgr-east`: re-read RUNTIME.md. This is a Boot canary page.
- You want to raise `-Xmx` as the first stabilize: write what that would buy you in hours, not whether it removes the retained set.
- Histogram is dominated by `char[]` / `byte[]`: name the **owners** if the file gives you classes, or say you cannot tell.
- This pack is not INCIDENT-805. Do not paste a GC-pause story unless this dashboard supports it.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you which class is the retainer.

---

## Interview questions

1. Why is “the heap is full” a weak first sentence when `pay-prod-east-1` is flat and still completing Avery Chen’s payment?
2. What is the difference between a leak-shaped old-gen climb and a high allocation rate that G1 is keeping up with?
3. Why can a bounce restore the canary for an hour and still be the wrong close-out?
4. When is a cache allowed to lose entries, and what must still be true for `Idempotency-Key`?
5. What would a second histogram an hour later confirm that a single snapshot cannot?

---

## Architecture/trade-off questions

1. In-process map versus a size-and-TTL cache versus the database idempotency table — which is the source of truth after a restart?
2. Where would you set a maximum cache size relative to a day’s unique keys on Harbor Market?
3. If the canary is a new minor version and the stable replica is not climbing, what do you learn that a single-instance page would hide?
4. Why is “just give the JVM 8g” a weak remediation for a structure that only grows?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live heap dump download.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-802/` and `instructor/rubrics/INCIDENT-802.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

Old-generation climb is a first-class production signal and still only a symptom. A histogram names candidates. Stabilization (bounce, disable, cap) is a different sentence from remediation (bounded cache, source of truth stays the table). A lucky leak label does not replace gate order.

---

## Portfolio deliverable

Attach the completed INC-JVM-802 worksheet to your notes if this is the Module 8 incident you will write up. The Module 8 portfolio artifact is [student/worksheets/PF-jvm-rca.md](../../student/worksheets/PF-jvm-rca.md): you pick **one** of INCIDENT-801 through INCIDENT-806 and write the scored RCA there.
