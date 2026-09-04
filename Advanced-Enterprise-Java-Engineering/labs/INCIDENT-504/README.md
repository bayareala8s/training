# INCIDENT-504 — Deployment failure

**Type:** INCIDENT  
**Module:** 05 — WebSphere Network Deployment  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/production/INC-WAS-504](../../incidents/production/INC-WAS-504/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

16:08 Pacific on a synthetic prod-east change window in September 2026. Jordan Voss is installing a new `payment.ear` edition onto `PaymentCluster`. Merchants start reporting that the same `Idempotency-Key` sometimes returns 201 and sometimes returns a naming or class error. The console may already show the new edition as the cell target. You are the engineer on call. The incident pack is synthetic BayPay data for `BayPayCell`.

---

## Business context

Avery Chen (`11111111-1111-1111-1111-111111111111`) can be routed by `ihs-east` to `Pay1` on `node-pay-1` or to `Pay2`/`Pay3` on `node-pay-2`. If those JVMs do not agree on the ear edition or on JNDI, retries look like flaky clients. They are not. Finance will reconcile duplicate attempts only if the API is idempotent **and** every member runs the same contract.

`dmgr-east` being up is not the same as `nodeagent-pay-2` having finished synchronize. Do not tell merchant success “the deploy succeeded” because one checkbox is green.

---

## Learning objectives

- Follow gated evidence: dashboard first, then logs, then deployment history.
- Contrast a **rolling install** with a **completed node sync**.
- Treat mixed member editions as a customer-visible defect, not as an in-progress aesthetic.
- Write stabilization that restores **one** edition on all members before you invent a new feature flag.
- Produce a comms update that does not name a JNDI bind you have not quoted.

---

## Architecture

```text
Jordan / Morgan  →  dmgr-east  →  node agents  →  cluster members
Merchants        →  ihs-east   →  Pay1 (node-pay-1)
                                 Pay2 (node-pay-2)
                                 Pay3 (node-pay-2)
PaymentCluster target: payment.ear
JNDI of interest: jdbc/baypay (historical), jdbc/baypayXA (not on every node)
```

Rollout clock (who was asked to run the new bits) and synchronize clock (who has the files) are not the same. You do not need a live cell to read that split. Traditional ND is the source estate; you are not designing a second DMGR.

---

## Prerequisites

- L-5.2 and L-5.6 completed (clusters, plugin, sync, operations).
- Incident worksheet: [student-worksheet.md](../../incidents/production/INC-WAS-504/student-worksheet.md).
- Locked names from [datasets/baypay-cell/TOPOLOGY.md](../../datasets/baypay-cell/TOPOLOGY.md).

---

## Environment setup

No runtime required. Open the pack:

```text
incidents/production/INC-WAS-504/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

This pack is a **gated subset** of the eleven evidence kinds the course catalog lists. The pack README documents what shipped and what was omitted. Do not invent a heap summary or SIBus depth.

Do not open `solutions/INCIDENT-504/` until you have filled the worksheet through remediation.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`. Note the install start, any node-agent event on `node-pay-2`, and when merchants paged.
2. **Gate 1:** open `evidence/dashboard.md` only. Record which members look healthy, which error classes appear, and whether versions match. Write a first hypothesis and the next investigation.
3. **Gate 2:** after that hypothesis, open `evidence/logs.txt`. Update the hypothesis. Quote naming or class lines with the server name; do not close the RCA on “bad deploy.”
4. **Gate 3:** open `evidence/deployment-history.md` only if it answers a question you already wrote about edition, sync, or bindings.
5. Write stabilization (how the cluster becomes one edition), remediation (what gate you add next time), and a 5-line comms update.
6. Optional: one sentence on how a Boot rolling deploy with a readiness gate differs from an ND install that did not wait for the node agent — literacy only.

---

## Validation

A complete worksheet has all six fields: hypothesis (updated per gate), evidence, next investigation, stabilization, remediation, comms. A lucky “sync failed” with no member/version table scores low on Diagnostic method (see rubric).

---

## Troubleshooting

- You opened deployment history first: stop, write what a release record would confirm or refute, then continue.
- Pay1 works and Pay2 fails (or the reverse): that is the incident, not noise. Table it.
- You want to finish the install “to clean up”: write both directions (forward to one new edition vs back to one old edition) and pick from evidence, not from hope.
- `NameNotFoundException` feels like a code bug: ask *which server* and *which name* before you blame `payment.ear` authors.
- You are missing a plugin file: it is omitted. Say whether you still have enough to stabilize membership via the console story in the history notes.

---

## Expected outcome

A written diagnosis path an instructor can score. The student guide will not tell you which edition to keep. Your worksheet must show how you chose a single consistent cluster.

---

## Interview questions

1. Why is a green “application installed” checkbox on `dmgr-east` not proof that `Pay3` is running that edition?
2. What still serves `/payment` if `nodeagent-pay-2` is restarting, and what can Jordan **not** do in that window?
3. Why is an intermittent `NameNotFoundException` a cluster-consistency smell rather than a random JNDI outage?
4. What deploy gate would you add that does not require sitting in the admin console for an hour?

---

## Architecture/trade-off questions

1. Roll `Pay1` back versus complete sync and bind the missing resource on every node — what does each choice cost merchants in this window?
2. Why is stopping the **node** `was-pay-2` a worse roll than stopping `Pay2` then `Pay3`?
3. Should `ihs-east` drain a member whose reported edition does not match the cell target?
4. Feature flag in the ear versus edition discipline on the cluster — which actually saves you when bindings differ by node?

---

## Cleanup

None. Do not delete the evidence pack. No cloud resources to tear down.

---

## Cost estimate

**$0.** Synthetic files only. No AWS. No live WAS install.

---

## Hidden/revealable solution

The student guide does not include the answer. Submit the worksheet first. Instructors use `solutions/INCIDENT-504/` and `instructor/rubrics/INCIDENT-504.md`. Opening the solution before you write is a failed diagnostic method score.

---

## What you learned

Install and synchronize are different clocks. `STARTED` plus a new cell target can still mean two editions behind one plugin. Stabilization is “one edition on every member.” Remediation is a gate that refuses to deploy when a node agent is down or distribution is incomplete.

---

## Portfolio deliverable

Attach the completed INC-WAS-504 worksheet to your notes. The Module 5 portfolio artifact remains the ARCHITECT-501 cell brief; this incident is evidence you can read a rollout without running `wsadmin`.
