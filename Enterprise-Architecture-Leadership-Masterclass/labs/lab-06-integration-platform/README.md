# Lab 06 — Build NorthStar’s Integration Reference Architecture

**Module:** 06 — Integration, Application, and Data Architecture  
**Estimated duration:** 40 minutes live + homework completion (90–120 minutes total)  
**Estimated cost:** ~<$5 USD when cleaned up promptly  
**Case study:** NorthStar Financial Services (fictional)  
**Region recommendation:** `us-east-1`

---

## Quick links

| Asset | Path |
| ----- | ---- |
| Student instructions | [`student-instructions.md`](student-instructions.md) |
| Submission checklist | [`submission-checklist.md`](submission-checklist.md) |
| Stretch objectives | [`stretch-objectives.md`](stretch-objectives.md) |
| Terraform environment | [`../../infrastructure/terraform/environments/lab06/`](../../infrastructure/terraform/environments/lab06/) |
| Terraform module | [`../../infrastructure/terraform/modules/integration-platform/`](../../infrastructure/terraform/modules/integration-platform/) |
| Cleanup script | [`../../infrastructure/terraform/scripts/cleanup-lab06.sh`](../../infrastructure/terraform/scripts/cleanup-lab06.sh) |
| Cost estimate | [`../../infrastructure/cost-estimates/lab-06.md`](../../infrastructure/cost-estimates/lab-06.md) |
| Pattern matrix template | [`../../student/templates/16-integration-pattern-matrix.md`](../../student/templates/16-integration-pattern-matrix.md) |
| Data-flow template | [`../../student/templates/22-data-flow-diagram.md`](../../student/templates/22-data-flow-diagram.md) |
| ADR template | [`../../student/templates/01-architecture-decision-record.md`](../../student/templates/01-architecture-decision-record.md) |

---

## What you will build

A serverless reference architecture covering:

1. Real-time account APIs (sync)  
2. Payment events (async + queue + DLQ)  
3. Partner file landing (S3 simulation of SFTP)  
4. Regulatory/analytics workflow (Step Functions + SNS notify)

**AWS Transfer Family is conceptual/optional only** — not deployed (idle endpoints cost money).

---

## Safety rules

- Serverless only; no NAT Gateway, always-on EC2, EKS, or OpenSearch  
- Confirm SNS email subscription after apply  
- Tag all resources; destroy same day  
- Create/verify a budget alert before applying

### Required tags

```text
Project=BayLearn
Course=EnterpriseArchitectureLeadership
Module=06
Student=<student-id>
Environment=Lab
ExpirationDate=<YYYY-MM-DD>
```

---

## Deliverables

- Integration pattern matrix for NorthStar scenarios  
- Mermaid reference architecture diagram  
- Data-flow diagram for payments + partner files  
- ≥2 ADRs (sync vs events; Transfer/MFT vs S3 landing)  
- Lab evidence (CLI/screenshots) + cleanup confirmation + cost note  

Start with [`student-instructions.md`](student-instructions.md).
