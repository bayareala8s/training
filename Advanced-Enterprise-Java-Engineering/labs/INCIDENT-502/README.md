# INCIDENT-502 — Cluster members stop processing

**Type:** INCIDENT  
**Module:** 05 — WebSphere Network Deployment  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/production/INC-WAS-502](../../incidents/production/INC-WAS-502/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

14:16 Pacific on a synthetic prod-east day in September 2026. Harbor Market reports that `POST /payment` hangs, then fails, then sometimes succeeds on retry. The pager names `PaymentCluster`. Morgan Hale’s console still shows `Pay1`, `Pay2`, and `Pay3` as **STARTED**. You are the engineer on call. The incident pack is synthetic BayPay data for `BayPayCell`.

---

## Business context

Avery Chen’s client (`11111111-1111-1111-1111-111111111111`, active USD account `22222222-2222-2222-2222-222222222221`) retries when a create payment does not return. Each retry is another web-container thread on whichever member `ihs-east` still considers healthy. Finance does not care that the JVM process table is green. They care that authorizations are not completing for the merchants who landed on the members that stopped making progress.

`RefundCluster` is not in the first page. Do not widen the incident to `dmgr-east` because the admin console still loads.

---

## Learning objectives

- Follow gated evidence: dashboard first, then logs, then the IHS / plugin view.
- Treat **STARTED** as a process state, not as proof that a member is processing `/payment`.
- Separate “the plugin still sends traffic” from “the member can finish a request.”
- Write stabilization that restores capacity without bouncing `db-east` or the whole cell.
- Produce a comms update that does not invent a cause you have not supported.

---

## Architecture

```text
Merchants / Avery Chen
  → ihs-east.baypay.example  (plugin-cfg.xml)
    → PaymentCluster
         Pay1  on node-pay-1  (was-pay-1.baypay.example:9080)
         Pay2  on node-pay-2  (was-pay-2.baypay.example:9080)
         Pay3  on node-pay-2  (was-pay-2.baypay.example:9081)
      → jdbc/baypay  →  db-east.baypay.example:5432 / baypay
```

You do not need a live WebSphere ND cell. The contracts are the plugin membership list, web-container threads, and the WAS JDBC pool (`maxConnections = 50`). Traditional ND is the source estate you are diagnosing, not a target you are extending.

---

## Prerequisites

- L-5.4 and L-5.6 completed (pools, hung-thread policy, plugin, bounce card).
- Incident worksheet: [student-worksheet.md](../../incidents/production/INC-WAS-502/student-worksheet.md).
- Locked names from [datasets/baypay-cell/TOPOLOGY.md](../../datasets/baypay-cell/TOPOLOGY.md).

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/production/INC-WAS-502/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset** of the eleven evidence kinds the course catalog lists. The pack README documents what shipped and what was omitted. Do not invent a thread dump or a heap histogram.

Do not open `solutions/INCIDENT-502/` until you have filled the worksheet through remediation.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note the gate rules and the omitted evidence kinds.
2. **Gate 1:** open `evidence/dashboard.md` only. Record which members still complete `/payment` and which only look alive. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/logs.txt`. Update the hypothesis. Quote hung-thread or JDBC lines; do not promote a log phrase to a closed RCA.
4. **Gate 3:** open `evidence/plugin-status.md` only if it answers a question you already wrote about `ihs-east` membership or health.
5. Write stabilization, remediation, and a 5-line comms update on the worksheet. Name people only as they appear in the timeline (Priya Nair, Riley Okonkwo, Morgan Hale, Jordan Voss).
6. Optional: one sentence on how the same symptom would look on Spring Boot (Hikari + load-balancer health) — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky one-word guess with empty evidence scores low on Diagnostic method (see rubric). Skipping to the plugin file before a written question also scores low.

---

## Troubleshooting

- You jumped to later files: stop, write what you *would* have asked, then continue.
- Console says STARTED and merchants still fail: that is data. Write the contradiction.
- You want a javacore: it is not in this pack. Say so and work with dashboard, logs, and plugin status.
- You are about to bounce `dmgr-east` or Postgres: re-read the L-5.6 bounce card, then write what you will **not** do.
- Dashboard and plugin seem to disagree about who is “up”: write that disagreement; do not pick a slogan.

---

## Expected outcome

A written diagnosis path an instructor can score. You may be wrong on the first hypothesis; you may not skip gates. The student guide will not tell you the mechanism.

---

## Interview questions

1. Why is “the cluster is down” a weak first sentence when one member still posts Avery Chen’s payment?
2. What is the difference between a hung-thread **warning** and a proven stall on `jdbc/baypay`?
3. Why can a plugin health check that only opens a TCP port keep sending merchants to a JVM that cannot run `payment.ear`?
4. When do you drain `Pay2` and `Pay3` together versus one at a time?

---

## Architecture/trade-off questions

1. Should `ihs-east` use TCP connect or an HTTP check that exercises `/payment` readiness?
2. Where would you set hung-thread threshold relative to a worst legitimate payment, and why is interrupt dangerous on a money thread?
3. If web-container max is 100 and `jdbc/baypay` max is 50, what happens to the extra 50 threads after a stale-connection event?
4. Why is recycling `Pay2`/`Pay3` stabilization, not remediation, if the plugin still uses the same health test tomorrow?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live WAS install.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-502/` and `instructor/rubrics/INCIDENT-502.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

STARTED is not throughput. The plugin’s idea of health can disagree with the web container’s ability to finish `/payment`. Hung-thread lines are candidates. Stabilization (who you remove from rotation, which JVM you recycle) is a different sentence from remediation (how health and pools are designed next week).

---

## Portfolio deliverable

Attach the completed INC-WAS-502 worksheet to your notes. The Module 5 portfolio artifact remains the ARCHITECT-501 cell brief; this incident is evidence you can operate `PaymentCluster` without installing it.
