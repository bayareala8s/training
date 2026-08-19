# Lab 1 — Integration Architecture Classification

## Lab Overview

Apply the course decision framework to 15 business requirements. No AWS. Architecture only.

## Business Scenario

You are the integration architect for **Northbridge Bank** (instructional fiction). Product, operations, and partner teams have filed 15 requests. None of them start with an AWS service name. Your job is to choose a **style** and defend it.

## Architecture

```text
Business requirement → characteristics → style → (optional) AWS mapping last
```

Styles: **API · Message · Event · File · ESB/Adapter · AI Agent (tools only)**

## Learning Objectives

- Classify integrations from NFRs, not from habit.
- Write a four-sentence rationale: requirement, characteristics, pattern, rejected options.
- Mix styles when one sentence hides multiple flows.

## Prerequisites

Module 1 complete. Course player open at Challenges is optional extra practice.

## AWS Services Used

None.

## Estimated Time

90–120 minutes.

## Estimated AWS Cost

$0.

## Step 1 — Setup

Copy `labs/lab-01-classification/worksheet.md` to `submissions/lab-01/worksheet.md`. Do **not** copy `sample-completed-worksheet.md`.

## Step 2 — Infrastructure

None.

## Step 3 — Application

None.

## Step 4 — Integration

For each item in `requirements.md`, fill: style, one-line architecture, AWS example *last*, and rationale.

## Step 5 — Testing

Peer or instructor review: if your rationale names a service before an NFR, revise.

## Step 6 — Failure Testing

For three items, write the incident that occurs if you pick the popular wrong style (e.g. API Gateway for 20 GB).

## Step 7 — Observability

Name the correlation identifier you would require for three of the flows.

## Step 8 — Security Review

Mark data class (public / internal / confidential / restricted) per flow.

## Step 9 — Architecture Questions

1. Which two requests are actually four flows in disguise?
2. Where would an agent be allowed, and which tool would it call?
3. Which request should remain on an adapter for 18 months and why?

## Step 10 — Cleanup

None.

## Validation

```bash
python3 scripts/validate_lab.py lab-01-classification
```

PASS requires a worksheet with 15 non-empty rationales ≥ 40 characters each.
