# Lab 7.1 — IAM Least Privilege

**Duration:** 2 hours · **Week 7**

## Objectives

- Tighten lab IAM policy from Week 2
- Remove wildcard actions where possible

## Steps

### 1. Audit current policy

Review `labs/week-02/iam/terraform-runner-policy.json`.

### 2. Replace `ec2:*` with scoped actions

Use IAM policy generator or AWS docs for minimum EC2 actions for your modules.

### 3. Enable IAM Access Analyzer (optional)

```bash
aws accessanalyzer create-analyzer --analyzer-name bal8s-lab --type ACCOUNT
```

## Deliverable

Updated policy JSON + justification in security report.

## Next

[Lab 7.2 — Tagging](LAB-02-tagging.md)
