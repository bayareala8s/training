# INCIDENT-403 — Transaction boundary failure

**Type:** INCIDENT  
**Module:** 04 — Jakarta EE and Enterprise Runtime Concepts  
**Duration:** 45–75 minutes  
**Cost:** $0  
**Pack:** [incidents/jvm/INC-EE-403](../../incidents/jvm/INC-EE-403/README.md)

This student guide does **not** contain a root-cause answer. Work the evidence in gate order.

---

## Scenario

Finance’s synthetic reconciliation job flags payments in `COMPLETED` with no matching `ledger_transactions` row. The API returned success to merchants. You are on call for payment-service in prod-east. All names, ids, and logs are fictional BayPay data.

---

## Business context

A `COMPLETED` payment is a promise that money posted. A missing ledger row means the system of record for money and the system of record for payment status disagree. That is an accounting incident, not a cosmetic UI bug. Avery Chen’s merchant will settle from the ledger, not from the HTTP 201.

---

## Learning objectives

- Use gated evidence: logs, then dashboard, then deployment history.
- Treat “committed payment / missing ledger” as a **boundary** symptom until you prove a mechanism.
- Separate in-process posting (reference app) from whatever this deploy changed.
- Write comms that do not claim a Spring annotation you have not shown.

---

## Architecture

Reference app (known-good teaching shape):

```text
PaymentApplicationService.create  @Transactional
        └── PaymentPostingService.postAuthorized   (no own annotation — joins caller)
                ├── ledger.save
                ├── payment COMPLETED
                └── PaymentCompletedEvent (in-process)
```

The incident pack is a **prod variant**. Do not assume the deployed code still matches the repository on your laptop.

---

## Prerequisites

- L-4.2 and L-4.5.
- Worksheet: [student-worksheet.md](../../incidents/jvm/INC-EE-403/student-worksheet.md).

---

## Environment setup

No cluster required.

```text
incidents/jvm/INC-EE-403/
  README.md
  timeline.json
  student-worksheet.md
  evidence/          # gated — see timeline.json "gates"
```

Do not open `solutions/INCIDENT-403/` until the worksheet is complete.

---

## Challenge/tasks

1. Read the pack README and `timeline.json`.
2. **Gate 1:** `evidence/logs.txt` only. Record what is committed and what is missing. First hypothesis.
3. **Gate 2:** `evidence/dashboard.md`. Does volume, error rate, or lag change the story?
4. **Gate 3:** `evidence/deployment-history.md` after you have a question a deploy record could answer.
5. Stabilization (customer money, retries, feature flags), remediation, comms — on the worksheet.
6. Note how a single shared unit of work vs a second unit of work would appear in this symptom. Do not declare a mechanism until evidence supports it.

---

## Validation

Worksheet has all six fields. Evidence quotes include payment id and a timestamp. You did not copy a solution filename into the hypothesis.

---

## Troubleshooting

- The reference app “can’t do this”: correct — the pack is a deployed variant. Use the pack.
- You want a code diff: deployment history is what you have. Say what file you would request next.
- Notifications fired: in-process events are not proof the ledger committed.

---

## Expected outcome

An evidence-ordered write-up of a status-versus-ledger split. Instructors score method, not speed-to-acronym.

---

## Interview questions

1. Why is a 201 on `POST /payments` insufficient proof that money posted?
2. What does an in-process `PaymentCompletedEvent` guarantee after a crash?
3. Why might isolating the ledger write in its own unit of work appear attractive and still be the wrong tool for in-process posting?

---

## Architecture/trade-off questions

1. When would you accept an outbox plus worker instead of one local transaction?
2. Should audit events be allowed to commit if the ledger rolls back?
3. How would the same split present on a JTA ear with two `EntityManager`s?

---

## Cleanup

None.

---

## Cost estimate

**$0.** Synthetic files only.

---

## Hidden/revealable solution

No reveal in this guide. After you submit, instructors grade against `solutions/INCIDENT-403/` and `instructor/rubrics/INCIDENT-403.md`.

---

## What you learned

Payment status and ledger rows are one unit of work in the teaching app. When they diverge in prod, you investigate the boundary with evidence, then stabilize money, then change code.

---

## Portfolio deliverable

Completed INC-EE-403 worksheet. Optional attachment next to the ARCHITECT-401 brief; the brief remains the named Module 4 portfolio artifact.
