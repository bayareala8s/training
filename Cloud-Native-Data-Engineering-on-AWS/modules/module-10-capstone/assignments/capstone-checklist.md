# Capstone Milestone Checklist

**Module 10 · Week-by-Week Guide**  
**Total estimated effort:** ~8 hours focused work + presentation prep

Use this checklist to track capstone progress. Check items as completed and note blockers in the **Notes** column.

---

## Before You Start

- [ ] Read [capstone/README.md](../../capstone/README.md)
- [ ] Review [capstone/rubric.md](../../capstone/rubric.md)
- [ ] Attend [Week 10 Lecture](../lectures/week-10-lecture.md)
- [ ] Choose capstone scenario (Option 1–4)
- [ ] Copy project template:

```bash
cp -r capstone/templates/project-structure capstone/my-project
cd capstone/my-project
```

- [ ] Set AWS Budget alert ($50 recommended)
- [ ] Confirm AWS CLI and Terraform work

---

## Day 1 – Architecture & Planning (Monday)

**Goal:** Frozen architecture scope; no code yet.

| Task | Done | Notes |
|------|------|-------|
| Write problem statement and success criteria | [ ] | |
| Draft context diagram | [ ] | `architecture/diagrams/` |
| Draft component diagram | [ ] | |
| Complete ARCHITECTURE.md sections 1–5 | [ ] | |
| Define datasets and S3 paths | [ ] | |
| List AWS services per layer | [ ] | |
| Identify scenario-specific requirements | [ ] | Banking/Healthcare/E-Commerce/Enterprise |
| Self-review against rubric Architecture criterion | [ ] | Target ≥ 20/25 |

**Deliverable:** ARCHITECTURE.md draft + 2 diagrams

---

## Day 2 – Infrastructure Foundation (Tuesday)

**Goal:** Deployable data lake with zones.

| Task | Done | Notes |
|------|------|-------|
| Customize Terraform (or extend course modules) | [ ] | |
| Deploy S3 bucket with all zones | [ ] | raw/cleaned/curated/quarantine/metadata |
| Enable encryption, block public access | [ ] | |
| Apply lifecycle rules on raw/ | [ ] | |
| Tag all resources Project=capstone | [ ] | |
| Document deploy steps in README | [ ] | |
| Save `terraform output` to deploy-outputs.json | [ ] | |
| Verify zones via AWS CLI | [ ] | |

**Deliverable:** Working Terraform + README Quick Start (steps 1–2)

---

## Day 3 – Ingestion & Sample Data (Wednesday)

**Goal:** Data landing in raw zone.

| Task | Done | Notes |
|------|------|-------|
| Prepare sample datasets for scenario | [ ] | `sample-data/` |
| Implement ingestion (Lambda / S3 upload / EventBridge) | [ ] | `src/ingestion/` |
| Upload sample data to raw/ | [ ] | |
| Verify raw partition structure | [ ] | year=/month=/day= |
| Document ingestion in ARCHITECTURE.md data flow | [ ] | |
| (Optional) Event-driven trigger configured | [ ] | |

**Deliverable:** Data visible in S3 raw/

---

## Day 4 – ETL Pipeline (Thursday)

**Goal:** Raw → Cleaned → Curated path working.

| Task | Done | Notes |
|------|------|-------|
| Implement Glue ETL script | [ ] | `src/etl/` |
| Deploy Glue job via Terraform or console | [ ] | |
| Run job successfully | [ ] | |
| Verify cleaned/ and curated/ outputs | [ ] | |
| Register tables in Glue Data Catalog | [ ] | |
| Run Athena query on curated table | [ ] | |
| Document ETL in ARCHITECTURE.md section 6 | [ ] | |

**Deliverable:** Successful Glue run + Athena query result (screenshot)

---

## Day 5 – Data Quality (Friday)

**Goal:** Validation and quarantine demonstrated.

| Task | Done | Notes |
|------|------|-------|
| Define validation rules JSON (≥ 5 rules) | [ ] | `src/validation/rules/` |
| Implement or adapt quality runner | [ ] | Module 4 pattern |
| Route failed records to quarantine/ | [ ] | |
| Generate quality report | [ ] | metadata/ or local reports/ |
| Include bad records in sample data to demo quarantine | [ ] | |
| Update ARCHITECTURE.md quality section | [ ] | |

**Deliverable:** quality_report.json + quarantine path with records

---

## Day 6 – Security, Orchestration & Monitoring (Saturday AM)

**Goal:** Governance and observability in place.

| Task | Done | Notes |
|------|------|-------|
| Complete GOVERNANCE.md (IAM, encryption, PII) | [ ] | |
| Define IAM roles with least privilege | [ ] | |
| Deploy CloudWatch dashboard | [ ] | Module 8 JSON/Terraform |
| Configure ≥ 1 CloudWatch alarm + SNS | [ ] | |
| Confirm SNS subscription | [ ] | |
| (Optional) Step Functions workflow | [ ] | Module 6 |
| (Optional) ML/features zone | [ ] | Module 9 |

**Deliverable:** GOVERNANCE.md + dashboard screenshot + alarm test

---

## Day 7 – Cost & Documentation (Saturday PM)

**Goal:** Professional documentation package.

| Task | Done | Notes |
|------|------|-------|
| Activate cost allocation tags | [ ] | |
| Run Cost Explorer report | [ ] | |
| Complete COST-ANALYSIS.md | [ ] | |
| Finalize README (deploy, verify, cleanup) | [ ] | |
| Complete ARCHITECTURE.md (all sections) | [ ] | |
| Remove template placeholder text | [ ] | |
| Commit all code; tag `capstone-v1.0` | [ ] | |
| Self-assess with rubric worksheet | [ ] | Target ≥ 85/100 |

**Deliverable:** Complete docs/ folder + README

---

## Day 8 – Presentation Prep (Sunday)

**Goal:** Confident 15–20 minute delivery.

| Task | Done | Notes |
|------|------|-------|
| Build slide deck (12–15 slides) | [ ] | `presentation/slides/` |
| Write demo script | [ ] | See presentation-guide.md |
| Rehearse with timer (target 17 min) | [ ] | |
| Capture backup screenshots | [ ] | |
| (Optional) Record backup video | [ ] | |
| Prepare Q&A for cost, security, scale | [ ] | |
| Submit repo link to LMS | [ ] | |
| Submit slides before session | [ ] | |

**Deliverable:** Presentation ready + backup materials

---

## Presentation Day (Final Session)

| Task | Done | Notes |
|------|------|-------|
| Demo environment verified 1 hour before | [ ] | |
| Presentation delivered (15–20 min) | [ ] | |
| Q&A completed | [ ] | |
| Peer feedback noted for portfolio | [ ] | |

---

## Post-Capstone Cleanup

| Task | Done | Notes |
|------|------|-------|
| Run `terraform destroy` | [ ] | |
| Verify no orphaned costly resources | [ ] | Glue, NAT, EMR |
| Update resume / LinkedIn | [ ] | CAREER-OUTCOMES.md |
| Archive final repo state | [ ] | |

---

## Integration Checklist (All Modules)

Ensure your capstone demonstrates course integration:

| Module | Evidence in Capstone | Done |
|--------|---------------------|------|
| 1 – Foundations | S3 zones, medallion architecture | [ ] |
| 2 – Ingestion | Lambda or event-driven ingest | [ ] |
| 3 – Glue ETL | Glue job Raw → Curated | [ ] |
| 4 – Data Quality | Rules + quarantine + report | [ ] |
| 5 – Modeling | Curated schema / star schema | [ ] |
| 6 – Orchestration | Step Functions or documented workflow | [ ] |
| 7 – Security | IAM, encryption, GOVERNANCE.md | [ ] |
| 8 – Monitoring | Dashboard, alarm, COST-ANALYSIS.md | [ ] |
| 9 – AI/ML | Feature pipeline or ML zone (optional) | [ ] |

Minimum for strong score: Modules **1–5, 7, 8** fully evidenced.

---

## Blocker Log

| Date | Blocker | Resolution | Resolved |
|------|---------|------------|----------|
| | | | [ ] |
| | | | [ ] |

---

## Submission Package

Confirm before deadline:

- [ ] GitHub repository URL submitted
- [ ] README allows evaluator to deploy without you
- [ ] All docs customized (no `[Your Name]` placeholders)
- [ ] Architecture diagrams in repo
- [ ] Presentation slides submitted
- [ ] AWS tags verified: `Project=capstone`, `Student=<name>`

---

**Good luck!** See [presentation-guide.md](../../capstone/presentation-guide.md) and [rubric.md](../../capstone/rubric.md).
