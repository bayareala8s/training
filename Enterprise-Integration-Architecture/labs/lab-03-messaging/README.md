# Lab 3 — Enterprise messaging (SQS, DLQ, replay)

## Lab Overview

Build Producer → SQS → Lambda → DynamoDB with a DLQ. Break it, inspect, fix, replay.

## Business Scenario

Northbridge must process payment commands even when the poster is down. Commands are not broadcasts.

## Architecture

Style: **Message**. See `diagrams/03-queue-architecture.md`.

## Learning Objectives

- Configure visibility vs function timeout.
- Send poison to DLQ.
- Replay after fix.
- Idempotent consumer.

## Prerequisites

Module 3. Lab 2 optional.

## AWS Services Used

SQS, SQS DLQ, Lambda, DynamoDB, IAM, CloudWatch.

## Estimated Time

3 hours.

## Estimated AWS Cost

< $0.20 if destroyed. No Transfer Family.

## Step 1 — Setup

Copy `terraform/labs/lab-03-messaging/terraform.tfvars.example` to `terraform.tfvars`.

## Step 2 — Infrastructure

`./scripts/lab_up.sh lab-03-messaging`

## Step 3 — Application

`lambda/lab03_producer` and `lambda/lab03_consumer`. Consumer fails when `fail` is true or amount is the string `POISON`.

## Step 4 — Integration

Send a good message, then a poison message using the producer script in the lab folder.

## Step 5 — Testing

`python3 scripts/validate_lab.py lab-03-messaging`

## Step 6 — Failure Testing

1. Poison message → DLQ.
2. Shrink visibility in console (or tf) and send a slow message → duplicates.
3. Replay from DLQ after removing POISON.

## Step 7 — Observability

Find correlation IDs on main queue vs DLQ. Alarm mentally: DLQ > 0.

## Step 8 — Security Review

Queue policies: only producer send, only consumer receive. No `sqs:*` on `*`.

## Step 9 — Architecture Questions

1. Is this an event or a command? Why?
2. Why is FIFO not required for independent payment IDs?
3. Write the inspect → fix → replay runbook in five lines.

## Step 10 — Cleanup

`./scripts/lab_down.sh lab-03-messaging`
