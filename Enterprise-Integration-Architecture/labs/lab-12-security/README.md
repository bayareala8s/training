# Security lab — insecure architecture

## Lab Overview

Start from an intentionally weak stack. Find and fix identity, encryption, secrets, public access, and audit gaps.

## Business Scenario

A contractor “got it working” with `*` policies and a public bucket.

## Architecture

`diagrams/10-integration-security.md`. Findings table required.

## Learning Objectives

- Least privilege.
- KMS.
- No public write.
- Secrets not in git.
- CloudTrail awareness.

## Prerequisites

Module 12. Lab 2 knowledge.

## AWS Services Used

IAM, S3, KMS, Lambda, optional Secrets Manager.

## Estimated Time

3 hours.

## Estimated AWS Cost

< $0.30 destroyed.

## Step 1 — Setup

Apply lab-12, which **starts insecure** (`insecure=true` default in example tfvars). Then tighten.

## Step 2 — Infrastructure

`./scripts/lab_up.sh lab-12-security` then edit Terraform until validate passes.

## Step 3 — Application

Do not add security theater. Fix data paths.

## Step 4 — Integration

Attempt to list other prefixes as the partner role—should fail after the fix.

## Step 5 — Testing

`python3 scripts/validate_lab.py lab-12-security` — FAIL until public access blocked and policies tightened.

## Step 6 — Failure Testing

Try the pre-fix exploit paths documented in the lab notes (in your account only).

## Step 7 — Observability

CloudTrail / access logs conceptually; app audit of who invoked.

## Step 8 — Security Review

Entire lab is a security review.

## Step 9 — Architecture Questions

1. Why is encryption-on plus * IAM still a fail?
2. Would an agent with this role be acceptable?
3. Cross-account: what is ExternalId for?

## Step 10 — Cleanup

`./scripts/lab_down.sh lab-12-security`
