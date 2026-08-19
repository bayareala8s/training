# Lab — Integration operations dashboard

## Lab Overview

Trace User → API → Event → Queue → Lambda → DB. Dashboard: transactions, success, failure, latency, queue depth, DLQ, file counts, processing duration.

## Business Scenario

Support cannot find a checkout. You will make the path visible.

## Architecture

`diagrams/11-integration-observability.md`.

## Learning Objectives

- Correlation ID everywhere.
- JSON logs.
- Business vs technical metrics.
- Dashboard as code.
- DLQ widget.

## Prerequisites

Module 13. Prefer Lab 2+3 running, or use the bundled mini-stack in lab-13 Terraform.

## AWS Services Used

CloudWatch dashboard, log groups, metric filters, alarms.

## Estimated Time

3 hours.

## Estimated AWS Cost

Log ingestion is the main cost—keep volume tiny; set short retention (3–7 days).

## Step 1 — Setup

Copy tfvars.

## Step 2 — Infrastructure

`./scripts/lab_up.sh lab-13-observability`

## Step 3 — Application

Emit EMF or metric filters from a small generator Lambda included in the stack.

## Step 4 — Integration

Run the generator; open the dashboard URL from Terraform output.

## Step 5 — Testing

`python3 scripts/validate_lab.py lab-13-observability`

## Step 6 — Failure Testing

Stop emitting success metrics and emit failures; confirm widgets and optional alarm.

## Step 7 — Observability

The dashboard *is* this step.

## Step 8 — Security Review

Redact payloads. No customerId as a metric dimension.

## Step 9 — Architecture Questions

1. Which widget would you show a VP vs an SRE?
2. Why is 202 rate a poor settlement SLO?
3. How does the Module 15 agent use these names?

## Step 10 — Cleanup

`./scripts/lab_down.sh lab-13-observability`
