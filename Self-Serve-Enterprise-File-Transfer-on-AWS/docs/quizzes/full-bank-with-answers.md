# Full quiz bank — 72 questions with answers

**Instructor / answer key edition** · Weeks 1–6 · 12 questions per week  
Learner-facing (questions only): see `week-NN-quiz.md` files.

---

## Week 1 — Enterprise MFT on AWS

| # | Question (summary) | Answer |
|---|-------------------|--------|
| 1 | Transfer Family vs EC2 SFTP primary advantage | **B** — Managed protocol edge |
| 2 | Push inbound — who initiates connection | **B** — Partner (client) |
| 3 | S3 home directory description | **B** — S3 key prefix mapping |
| 4 | IAM principal for Transfer access role | **C** — `transfer.amazonaws.com` |
| 5 | Why S3 versioning on landing | **B** — Audit/recovery on overwrite/delete |
| 6 | Multi-tenant prefix layout | **B** — `partners/{partner_id}/inbound/` |
| 7 | Connectors primarily used for | **B** — Remote SFTP/FTPS endpoints |
| 8 | Unable to AssumeRole common cause | **B** — Trust policy issues |
| 9 | Why separate edge from processing | **B** — Security boundaries + async automation |
| 10 | Lab 1 protocol focus | **C** — SFTP |
| 11 | **Short:** Two audit metadata questions | Who/when; filename; size/hash; partner ID; status (any two) |
| 12 | **Short:** Server vs connector | Server = inbound to you; connector = remote SFTP |

---

## Week 2 — Security & governance

| # | Question (summary) | Answer |
|---|-------------------|--------|
| 1 | Passwords in Git — STRIDE risk | **B** — Disclosure/spoofing |
| 2 | SSE-KMS vs SSE-S3 enterprise reason | **B** — CMK, key policies, audit narrative |
| 3 | ListBucket partner subtree | **A** — `s3:prefix` condition |
| 4 | Landing bucket Block Public Access | **B** — All four ON |
| 5 | CloudTrail S3 data events value | **B** — Object-level API audit |
| 6 | Deny insecure transport policy | **B** — Block HTTP S3 API |
| 7 | Connector credentials store | **C** — Secrets Manager |
| 8 | S3 access logging provides | **B** — HTTP request logs |
| 9 | Tight SourceArn on Transfer trust | **B** — AssumeRole failures |
| 10 | S3 gateway VPC endpoint benefit | **B** — Private path to S3 |
| 11 | **Short:** Two upload evidence sources | CloudTrail, access logs, Transfer logs, versions (any two) |
| 12 | **Short:** `s3:prefix` purpose | Restrict list/access to partner subtree |

---

## Week 3 — Event-driven automation

| # | Question (summary) | Answer |
|---|-------------------|--------|
| 1 | S3 event delivery semantics | **B** — At-least-once |
| 2 | Idempotency table purpose | **B** — Prevent duplicate processing |
| 3 | Failed validation routing | **B** — `quarantine/` |
| 4 | Keep validation Lambda fast | **B** — Heavy work in SFN/batch |
| 5 | Strong business idempotency key | **B** — partner + key + ETag/hash |
| 6 | EventBridge vs direct S3→Lambda | **B** — Fan-out, decoupling |
| 7 | Missing kms:Decrypt symptom | **B** — AccessDenied on object |
| 8 | Structured logs must include | **B** — correlation_id, safe context |
| 9 | Duplicate payroll without idempotency | **B** — Double processing risk |
| 10 | Prefix filter on notifications | **B** — Avoid wrong invocations |
| 11 | **Short:** Why at-least-once | Duplicates/retries/re-uploads require idempotent consumers |
| 12 | **Short:** Two Lab 3 validation rules | Max 100MB; extensions csv/json/xml; non-zero (any two) |

---

## Week 4 — Workflow orchestration

| # | Question (summary) | Answer |
|---|-------------------|--------|
| 1 | Orchestration vs choreography | **B** — Central order + execution history |
| 2 | Default workflow type for MFT audit | **B** — Standard |
| 3 | Retry block best for | **B** — Transient Lambda/service errors |
| 4 | Catch block purpose | **B** — Failure routing/recovery |
| 5 | Why not Express as default | **B** — ~5 min limit, lighter audit history |
| 6 | correlation_id originates | **B** — Job/API edge, propagate through |
| 7 | Map state use case | **B** — Batch/manifest of files |
| 8 | Alarm SFN ExecutionsFailed | **B** — Workflow can fail after Lambda ok |
| 9 | Workflow idempotency | **B** — DynamoDB + existing execution ARN |
| 10 | Choice state branches on | **B** — Business valid flag |
| 11 | **Short:** Catch vs Retry | Retry transient; Catch business/terminal |
| 12 | **Short:** SFN history for audit | Durable state transition evidence |

---

## Week 5 — Connectors & partners

| # | Question (summary) | Answer |
|---|-------------------|--------|
| 1 | Push S3 file to partner SFTP | **B** — Connector |
| 2 | Partner firewall — document | **B** — Egress/NAT IP |
| 3 | Connector passwords | **B** — Secrets Manager |
| 4 | Trusted host keys | **B** — MITM protection |
| 5 | Partner matrix purpose | **B** — Operational partner documentation |
| 6 | S3_TO_SFTP meaning | **B** — S3 staged → remote SFTP |
| 7 | Multi-hop attention | **B** — Idempotency + correlation per hop |
| 8 | Connector vs server | **B** — Initiates remote sessions |
| 9 | Onboarding — network needs | **A** — Egress IP, host keys |
| 10 | SFTP_TO_SFTP pattern | **B** — Stage via S3 hub |
| 11 | **Short:** When use server | Partner uploads inbound to you |
| 12 | **Short:** Three matrix columns | partner_id, direction, schedule, credential_store, prefix, etc. |

---

## Week 6 — Self-serve platform

| # | Question (summary) | Answer |
|---|-------------------|--------|
| 1 | Self-serve primary goal | **B** — Guardrailed APIs, no raw creds |
| 2 | Owner-scoped authZ claim | **B** — JWT `sub` vs `owner_sub` |
| 3 | POST /jobs returns 202 | **B** — Async processing |
| 4 | Never in API response | **B** — IAM keys / secret values |
| 5 | New connection status | **B** — PENDING_APPROVAL |
| 6 | JWT authorizer validates | **B** — Signature, iss, aud, exp |
| 7 | source_key check | **B** — Allowed connection prefix |
| 8 | DynamoDB stores | **B** — Connections + jobs metadata |
| 9 | x-idempotency-key prevents | **B** — Duplicate executions |
| 10 | GET job 403 when | **A** — owner_sub mismatch |
| 11 | **Short:** Two entities + fields | Connection (id, type); Job (id, state, correlation_id) |
| 12 | **Short:** No bucket-wide listing | Tenant isolation / least exposure |

---

## Scoring guide

| Questions correct | Score (12-pt scale) | Score (100-pt LMS) |
|-------------------|---------------------|---------------------|
| 12 | 12 | 100 |
| 11 | 11 | 92 |
| 10 | 10 | 83 |
| 9 | 9 | 75 (recommended minimum) |
| ≤8 | Fail retake policy (instructor discretion) | |

---

## Files

- Questions only: `week-01-quiz.md` … `week-06-quiz.md`  
- Per-week answer keys: `week-01-answers.md` … `week-06-answers.md`  
- Index: [README.md](README.md)
