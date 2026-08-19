# Lab 5 — EventBridge choreography

## Lab Overview

OrderCreated → PaymentAuthorized → InventoryReserved → OrderCompleted.

## Business Scenario

Harbor wants facts, not a hidden ESB process. Keep the saga visible in later capstones; this lab is choreography of facts.

## Architecture

Style: **Event**. `diagrams/05-event-driven-architecture.md`.

## Learning Objectives

- PutEvents with schemas.
- Route by detail-type.
- Idempotent consumers.
- Discuss archive/replay without firing inventory twice.

## Prerequisites

Module 5.

## AWS Services Used

EventBridge custom bus, rules, SQS or Lambda targets, DynamoDB.

## Estimated Time

3.5 hours.

## Estimated AWS Cost

< $0.30 destroyed. Custom event cost is tiny at lab volume.

## Step 1 — Setup

Copy tfvars.

## Step 2 — Infrastructure

`./scripts/lab_up.sh lab-05-events`

## Step 3 — Application

`lambda/lab05_*` plus `sample-data/events/*.json`.

## Step 4 — Integration

Put OrderCreated; observe the chain. Duplicate the same event id.

## Step 5 — Testing

`python3 scripts/validate_lab.py lab-05-events`

## Step 6 — Failure Testing

Invalid schema event. Duplicate PaymentAuthorized. Optional: disable inventory rule and show payments still complete their fact.

## Step 7 — Observability

Trace one correlation ID across four functions.

## Step 8 — Security Review

Only the order producer IAM can PutEvents of OrderCreated (lab may approximate with bus policy notes).

## Step 9 — Architecture Questions

1. Which names are commands in disguise?
2. When do you stop adding rules and start Step Functions?
3. How would you replay *only* analytics?

## Step 10 — Cleanup

`./scripts/lab_down.sh lab-05-events`
