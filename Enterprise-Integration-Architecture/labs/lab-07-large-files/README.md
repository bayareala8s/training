# Lab 7 — Large-file claim-check + status API

## Lab Overview

API init → client uploads to S3 → event → pipeline → GET status. Do not send GB through the gateway.

## Business Scenario

A partner uploads a multi-hundred-MB object. Mobile must not spin for the hash.

## Architecture

Style: **File + API control plane**. `diagrams/09-large-file-architecture.md`.

## Learning Objectives

- Presigned upload to server-chosen key.
- 202 + status resource.
- Claim-check events.
- Worker threshold discussion (Lambda vs Fargate).

## Prerequisites

Module 7. Use a small file in the lab; design for 10 GB in the ADR.

## AWS Services Used

API Gateway, Lambda, S3, EventBridge, DynamoDB.

## Estimated Time

3 hours.

## Estimated AWS Cost

< $0.30. Abort incomplete multipart via lifecycle.

## Step 1 — Setup

Copy tfvars.

## Step 2 — Infrastructure

`./scripts/lab_up.sh lab-07-large-files`

## Step 3 — Application

`lambda/lab07_init_upload`, `lab07_process`, `lab07_status`.

## Step 4 — Integration

POST /uploads, PUT to presigned URL with `sample-data/files/small.bin`, GET status until COMPLETED.

## Step 5 — Testing

`python3 scripts/validate_lab.py lab-07-large-files`

## Step 6 — Failure Testing

Expire a presign (wait or shorten). Upload a checksum mismatch. Confirm FAILED status, not 200 on init.

## Step 7 — Observability

Status transitions in DynamoDB and logs.

## Step 8 — Security Review

Presign cannot PUT to arbitrary keys. Job IDs unguessable. Authz on GET status.

## Step 9 — Architecture Questions

1. Why not API Gateway for 25 GB?
2. What is the claim check on the event?
3. When do you choose Fargate over Lambda?

## Step 10 — Cleanup

`./scripts/lab_down.sh lab-07-large-files`
