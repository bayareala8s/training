# Lab 8 — Legacy ESB redesign + ADR

## Lab Overview

You receive a legacy ESB architecture. You do **not** receive the answer. Produce keep/change/retire, strangler, risks, and a full ADR.

## Business Scenario

Northbridge’s bus team has a six-week lead time. Digital wants events. Settlement is ISO on MQ. Marketing email is on the bus for historical reasons.

## Architecture

As-is: `labs/lab-08-esb-modernization/as-is.md`. Target must use styles, not a new hub.

## Learning Objectives

- Inventory flows.
- Keep/change/retire table.
- Strangler waves.
- Dual-run for money.
- Complete ADR.

## Prerequisites

Modules 8–9. Terraform optional.

## AWS Services Used

None required. Optional strangler slice: `./scripts/lab_up.sh lab-08-esb-modernization` deploys `GET /balances/{id}` that does **not** hop the ESB.

## Estimated Time

3–4 hours (architecture). +1 hour optional façade.

## Estimated AWS Cost

$0 unless you deploy the optional slice.

## Step 1 — Setup

Read `as-is.md`, `strangler_demo.py`, and `templates/adr.md`. Copy the ADR template to `submissions/lab-08/adr.md`.

## Step 2 — Infrastructure

None required. Optional:

```bash
./scripts/lab_up.sh lab-08-esb-modernization
```

## Step 3 — Application

None required.

## Step 4 — Integration

Write `submissions/lab-08/adr.md` and a target diagram.

## Step 5 — Testing

`python3 scripts/validate_lab.py lab-08-esb-modernization`

## Step 6 — Failure Testing

Describe the incident if you strangler settlement first with no dual-run.

## Step 7 — Observability

How will you see drift during dual-run?

## Step 8 — Security Review

What identity replaces the bus service account?

## Step 9 — Architecture Questions

1. What stays on an adapter for 18 months and why?
2. What is the policy for *new* maps?
3. Defend EventBridge vs SNS vs SQS for each remaining flow.

## Step 10 — Cleanup

None, or destroy optional slice.
