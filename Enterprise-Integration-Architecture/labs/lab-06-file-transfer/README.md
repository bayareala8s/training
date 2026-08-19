# Lab 6 — Enterprise file transfer pipeline

## Lab Overview

Partner → SFTP (optional) → Transfer Family → S3 → EventBridge → SQS → Lambda → destination, with validation, duplicates, metadata, audit, failures, notifications.

## Business Scenario

A partner can only land a CSV at night. You still owe posting, ACK, and audit.

## Architecture

Style: **File**. `diagrams/06-file-transfer-architecture.md`.

## Learning Objectives

- Landing prefixes as contracts.
- Checksum + duplicate detection.
- Quarantine vs accept.
- Catalog as the ops API.
- Cost-control the Transfer server.

## Prerequisites

Module 6. SSH client optional.

## AWS Services Used

S3, EventBridge, SQS, Lambda, DynamoDB, SNS (email optional), Transfer Family **optional flag**.

## Estimated Time

4–5 hours.

## Estimated AWS Cost

S3/Lambda path: < $0.30. **Transfer Family is billed per hour while ONLINE.** Default Terraform flag `enable_transfer_family=false`. Enable only during the SFTP hour, then `terraform apply` to disable or destroy.

## Step 1 — Setup

Copy tfvars. Decide whether to enable Transfer Family. Prefer S3 put for the first pass.

## Step 2 — Infrastructure

`./scripts/lab_up.sh lab-06-file-transfer`

## Step 3 — Application

`lambda/lab06_validate`. Sample files in `sample-data/files/`.

## Step 4 — Integration

Upload a good CSV, a duplicate, a bad schema, a wrong checksum sidecar.

## Step 5 — Testing

`python3 scripts/validate_lab.py lab-06-file-transfer`

## Step 6 — Failure Testing

Duplicate post attempt. Poison CSV. Optional: leave Transfer ONLINE and calculate weekend cost (then disable).

## Step 7 — Observability

Catalog items for each file; FileReceived vs FileQuarantined.

## Step 8 — Security Review

Prefix isolation. KMS on the bucket. No public ACL.

## Step 9 — Architecture Questions

1. At which state do you ACK POSTED?
2. Why is ETag not enough integrity?
3. How does Module 15 query this catalog?

## Step 10 — Cleanup

`./scripts/lab_down.sh lab-06-file-transfer` — confirm Transfer server is gone.
