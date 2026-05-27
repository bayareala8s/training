# Capstone project

**Weight: 35% of final grade · Due: end of Week 8**

## Purpose

Produce a **stakeholder-ready** artifact set: architecture, working demo, security narrative, and operations story—suitable for an internal platform pitch or BayAreaLa8s consulting discovery.

## Track selection

Choose **one** track by end of Week 5 (submit intent in LMS).

### Track A — Self-serve control plane

**Goal:** Business-aligned users browse connections and submit jobs without touching AWS Console.

**Must include:**

- Cognito-authenticated API (Lab 6 extended)  
- Connection catalog + job history in DynamoDB  
- At least one executable job path into Step Functions or Transfer  
- UI **or** documented Postman + demo script for non-UI reviewers  

### Track B — Governed automation hub

**Goal:** Operations-first platform with strong audit and idempotency.

**Must include:**

- Step Functions workflow (Lab 4 extended) with retries and failure paths  
- Idempotency keys on job submission (`x-idempotency-key` header pattern)  
- Audit export: S3 object or structured log bundle per job  
- Failure injection demo (e.g., bad file → quarantine + alarm)  

### Track C — Migration accelerator

**Goal:** Document migration from legacy MFT to AWS (hypothetical or anonymized real).

**Must include:**

- As-is / to-be diagrams  
- Phased cutover plan (min. 3 phases)  
- Terraform module **layout** (folders + README; full apply optional)  
- Risk register (min. 5 items)  

Hybrid A+B allowed with instructor written approval.

---

## Submission checklist

| # | Item | Required |
|---|------|----------|
| 1 | `README.md` — how to run demo in &lt; 30 min | Yes |
| 2 | Architecture diagram (PNG/PDF) | Yes |
| 3 | `decision-log.md` — 5+ ADRs (short format) | Yes |
| 4 | IaC skeleton (`iac/` Terraform or CDK) | Yes (Tracks A/B); Track C emphasis |
| 5 | `DEMO_SCRIPT.md` — minute-by-minute | Yes |
| 6 | Demo recording (5–10 min) **or** live presentation | Yes |
| 7 | `threat-model-summary.md` (STRIDE-lite) | Yes |
| 8 | `runbook.md` excerpt (on-call section) | Yes |
| 9 | Cost estimate (monthly order-of-magnitude) | Yes |
| 10 | No secrets in git (.env.example only) | Yes |

---

## Rubric (100 points → 35% course weight)

| Category | Points | Excellent (90–100%) | Adequate (70–89%) | Needs work (&lt;70%) |
|----------|--------|---------------------|-------------------|----------------------|
| **Architecture** | 25 | Clear diagrams, justified service choices | Mostly complete, minor gaps | Incomplete or inconsistent |
| **Working demo** | 25 | Reliable end-to-end, rehearsed | Works with caveats | Broken or manual-only |
| **Security & governance** | 20 | KMS, IAM scope, audit trail demonstrated | Described, partially shown | Missing |
| **Operations** | 15 | Runbook, alarms, correlation IDs | Partial runbook | Absent |
| **Communication** | 15 | Crisp narrative, handles Q&A | Understandable | Unclear |

**Pass capstone:** ≥ 70 points.

---

## Presentation format

- **Length:** 10 min demo + 5 min Q&A  
- **Audience role-play:** Enterprise architect + security reviewer  
- **Required slide topics:** problem, architecture, security, ops, roadmap  

---

## Academic integrity

- All work must be your own; cite AWS docs and course materials.  
- You may reference BayAreaLa8s open patterns conceptually; do not commit customer data.  
- AI assistance allowed for drafting; you must explain every design choice in Q&A.

---

## Optional stretch (extra credit +5%)

- Bedrock Agent read-only ops query over runbook (BayRelay pattern)  
- Multi-region DR narrative with replication diagram  
- Partner self-registration workflow with approval gate  
