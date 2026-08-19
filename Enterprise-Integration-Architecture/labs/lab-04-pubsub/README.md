# Lab 4 — Pub/sub fan-out

## Lab Overview

OrderCreated → SNS → inventory, notification, and analytics queues. Prove independence.

## Business Scenario

Harbor checkout must not import email or analytics SDKs.

## Architecture

Style: **Event/notification + queues**. `diagrams/04-pubsub-architecture.md`.

## Learning Objectives

- Fan-out with a queue per subscriber.
- Kill one consumer; others proceed.
- Optional filter for TEST orders.

## Prerequisites

Module 4.

## AWS Services Used

SNS, SQS, Lambda, IAM.

## Estimated Time

2.5 hours.

## Estimated AWS Cost

< $0.20 destroyed.

## Step 1 — Setup

Copy tfvars example.

## Step 2 — Infrastructure

`./scripts/lab_up.sh lab-04-pubsub`

## Step 3 — Application

Three consumers in `lambda/lab04_*`.

## Step 4 — Integration

Publish one OrderCreated. Confirm three DynamoDB projections (or log lines).

## Step 5 — Testing

`python3 scripts/validate_lab.py lab-04-pubsub`

## Step 6 — Failure Testing

Set notification Lambda reserved concurrency to 0. Publish again. Inventory still writes. Restore concurrency.

## Step 7 — Observability

Three log groups, one correlation ID.

## Step 8 — Security Review

Notification role cannot write inventory items.

## Step 9 — Architecture Questions

1. What experiment proves independence?
2. When would EventBridge be a better bus than SNS?
3. If analytics needs PII, how do you minimize the topic payload?

## Step 10 — Cleanup

`./scripts/lab_down.sh lab-04-pubsub`
