# Lab 2 — Security hardening

**Week 2 · Estimated time: 3 hours**

> **Terraform:** KMS, BPA, access logging on landing bucket are **already applied** by the lab stack. This lab focuses on **verification** and checklist completion.

## Objectives

Harden Lab 1: KMS encryption, least-privilege IAM, block public access, enable CloudTrail logging evidence.

## Steps

### 1. Verify KMS (Terraform)

```bash
terraform -chdir=infra/environments/lab output -raw kms_key_arn
aws s3api get-bucket-encryption --bucket $(terraform -chdir=infra/environments/lab output -raw landing_bucket)
```

### 2. Verify IAM (console)

Open IAM role `baylearn-mft-lab-transfer-inbound` — confirm no `s3:*` on `*` resources; prefix scoped to `partners/demo/`.

### 3. Verify Block Public Access

```bash
aws s3api get-public-access-block --bucket $(terraform -chdir=infra/environments/lab output -raw landing_bucket)
```

### 4. Verify access logging

```bash
aws s3api get-bucket-logging --bucket $(terraform -chdir=infra/environments/lab output -raw landing_bucket)
terraform -chdir=infra/environments/lab output -raw logs_bucket
```

### 5. CloudTrail (account)

Confirm account or org trail is enabled (may pre-exist outside this stack).

### 6. Optional hardening exercise

Add bucket policy `DenyInsecureTransport` in a Terraform branch — see [Module 2](../modules/week-02.md).

## Security baseline checklist (deliverable)

Copy into `submissions/week-02/security-checklist.md` and mark each item Pass/Fail/N/A:

- [ ] SSE-KMS on landing bucket  
- [ ] IAM least privilege (no wildcards on actions)  
- [ ] Prefix isolation per partner  
- [ ] Public access blocked  
- [ ] Versioning enabled  
- [ ] Access logging enabled  
- [ ] CloudTrail captures S3/Transfer API calls  
- [ ] Transfer role trust includes `aws:SourceAccount`  
- [ ] Credentials not stored in git  
- [ ] Billing alarm configured  

## Rubric (10 pts)

| Criterion | Points |
|-----------|--------|
| KMS encryption active | 3 |
| IAM scoped policies | 3 |
| Checklist complete + evidence | 4 |
