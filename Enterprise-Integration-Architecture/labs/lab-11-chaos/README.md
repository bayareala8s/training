# Chaos lab — break integrations on purpose

## Lab Overview

Deliberately induce Lambda failure, API timeout, consumer unavailable, invalid message, duplicate event, duplicate file, dependency outage. Diagnose with telemetry, then recover.

## Business Scenario

You are on-call for Harbor + Northbridge lab platforms.

## Architecture

Reuse stacks from labs 2–7. See Module 11.6 playbook.

## Learning Objectives

- Break with a hypothesis.
- Observe logs/metrics/DLQ.
- Fix.
- Prove an alarm exists or add one.

## Prerequisites

Labs 2–7 deployed (you may do a subset). Module 11.

## AWS Services Used

Dedicated chaos stack (`terraform/labs/lab-11-chaos`) plus any labs 2–7 you already have up.

## Estimated Time

3–4 hours.

## Estimated AWS Cost

Dedicated stack is serverless; destroy when done.

## Step 1 — Setup

Pick at least four scenarios from `labs/lab-11-chaos/scenarios.md`. Copy notes to `submissions/lab-11/notes.md`.

## Step 2 — Infrastructure

```bash
./scripts/lab_up.sh lab-11-chaos
python3 scripts/validate_lab.py lab-11-chaos
```

## Step 3 — Application

Inject poison via sample-data.

## Step 4 — Integration

Record notes in `submissions/lab-11/notes.md`.

## Step 5 — Testing

`python3 scripts/validate_lab.py lab-11-chaos` — requires notes covering C1–C7 (min four) **and** the dedicated chaos stack (good message posts; poison + invalid JSON hit the DLQ).

## Step 6 — Failure Testing

All seven scenarios if time allows. Minimum four.

## Step 7 — Observability

If nothing paged, add the alarm—that is the deliverable.

## Step 8 — Security Review

Do not use AdministratorAccess to “make chaos easier.”

## Step 9 — Architecture Questions

1. Which failure was silent, and which metric would catch it?
2. How many retry layers fired?
3. What is the user-visible degradation?

## Step 10 — Cleanup

Bring concurrency back. Destroy stacks.
