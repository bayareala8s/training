# Capstone Grading Rubric

**Cloud-Native Data Engineering on AWS · Module 10**  
**Weight:** 30% of course grade

---

## Overview

Evaluators score each criterion independently, then apply weights. Use this rubric for self-assessment before submission and as the official grading standard.

**Total points:** 100

---

## 1. Architecture & Design (25 points)

| Level | Points | Criteria |
|-------|--------|----------|
| **Excellent** | 22–25 | Complete architecture covering ingestion, storage (all zones), processing, catalog, analytics, monitoring, and security. Diagrams are clear and match implementation. Design decisions documented with trade-offs in ARCHITECTURE.md. Scalable and follows course best practices (medallion, IaC, fail-safe quality). |
| **Good** | 17–21 | Solid architecture with minor gaps (e.g., orchestration documented but not implemented). Diagrams present and mostly accurate. Some design rationale missing. |
| **Satisfactory** | 12–16 | Basic architecture covers core layers but missing components (e.g., no quarantine zone, no monitoring layer in diagram). Limited documentation of decisions. |
| **Needs Improvement** | 0–11 | Incomplete or inconsistent architecture. Diagram missing or does not match deployment. No ARCHITECTURE.md or equivalent. |

### Checklist for Evaluators

- [ ] Context and component diagrams included
- [ ] All S3 zones defined with path examples
- [ ] AWS services justified per layer
- [ ] Non-functional requirements addressed (scale, cost, security, reliability)
- [ ] Scenario-specific requirements met (banking audit, healthcare PII, etc.)

---

## 2. Implementation Quality (25 points)

| Level | Points | Criteria |
|-------|--------|----------|
| **Excellent** | 22–25 | End-to-end data flow works: data lands in raw/, processes to curated/, queryable in Athena or equivalent. Terraform deploys cleanly. Glue/Lambda code is readable, error-handled, and follows course patterns. README setup instructions work without evaluator assistance. |
| **Good** | 17–21 | Core pipeline functional with minor bugs or manual steps not documented. Most code follows best practices. One ingestion or ETL path fully working. |
| **Satisfactory** | 12–16 | Partial implementation—e.g., S3 zones exist but ETL incomplete, or ETL runs but curated empty. Setup requires clarification. |
| **Needs Improvement** | 0–11 | Minimal or non-functional implementation. Cannot deploy or verify. Code missing or copied without adaptation. |

### Checklist for Evaluators

- [ ] `terraform apply` succeeds (or documented alternative)
- [ ] Sample data flows Raw → Cleaned → Curated
- [ ] At least one Glue job or equivalent ETL script runs successfully
- [ ] Ingestion pattern implemented (Lambda, EventBridge, or S3 event)
- [ ] Code in `src/` with reasonable structure
- [ ] No hardcoded secrets; `.gitignore` covers tfvars

---

## 3. Data Quality & Governance (20 points)

| Level | Points | Criteria |
|-------|--------|----------|
| **Excellent** | 18–20 | Validation rules defined (JSON or code). Quarantine routing demonstrated. GOVERNANCE.md complete with IAM, encryption, PII handling, audit logging. Quality report generated. Scenario-appropriate controls (HIPAA, SOX, etc.). |
| **Good** | 14–17 | Basic validation present. Quarantine zone used or documented. GOVERNANCE.md covers IAM and encryption with minor gaps. |
| **Satisfactory** | 10–13 | Validation mentioned but not enforced in pipeline. Governance doc incomplete. PII not addressed for healthcare scenario. |
| **Needs Improvement** | 0–9 | No quality framework. No governance documentation. Sensitive data exposed in curated zone without controls. |

### Checklist for Evaluators

- [ ] Validation rules catalog (minimum 5 rules on primary dataset)
- [ ] Quarantine path demonstrated or sample quarantined records shown
- [ ] IAM roles follow least privilege
- [ ] S3 encryption enabled
- [ ] GOVERNANCE.md completed (not just template placeholders)
- [ ] CloudTrail or audit logging mentioned/enabled

---

## 4. Monitoring & Operations (15 points)

| Level | Points | Criteria |
|-------|--------|----------|
| **Excellent** | 13–15 | CloudWatch dashboard deployed with pipeline-relevant widgets. At least one alarm with SNS notification. Cost tags applied. Runbook excerpt or ops section in docs. Custom metrics optional but valued. |
| **Good** | 10–12 | Dashboard or alarms present but not both. Tags mostly applied. Basic ops documentation. |
| **Satisfactory** | 7–9 | Screenshots only—no IaC deployment. Minimal monitoring awareness in docs. |
| **Needs Improvement** | 0–6 | No monitoring. No cost tags. No operational consideration. |

### Checklist for Evaluators

- [ ] CloudWatch dashboard (JSON, Terraform, or console export)
- [ ] Alarm configured for job failure or quality SLO
- [ ] SNS topic or notification path documented
- [ ] Resources tagged `Project=capstone`, `Student=<name>`
- [ ] COST-ANALYSIS.md with actual or estimated figures

---

## 5. Documentation & Presentation (15 points)

| Level | Points | Criteria |
|-------|--------|----------|
| **Excellent** | 13–15 | README enables independent deployment. All template docs customized. Presentation is 15–20 min, structured, connects tech to business value. Live demo or strong screenshot backup. Professional delivery. |
| **Good** | 10–12 | README adequate with minor gaps. Docs mostly complete. Presentation covers architecture and demo but rushes or omits governance/cost. |
| **Satisfactory** | 7–9 | README minimal. Template docs largely unchanged. Presentation under 10 min or over 25 min; unclear narrative. |
| **Needs Improvement** | 0–6 | Missing README or presentation. Cannot understand project without verbal explanation. |

### Checklist for Evaluators

- [ ] README: prerequisites, deploy, verify, cleanup
- [ ] ARCHITECTURE.md, GOVERNANCE.md, COST-ANALYSIS.md customized
- [ ] Presentation 15–20 minutes
- [ ] Business problem stated in first 2 minutes
- [ ] Demo or screenshots of working system
- [ ] Q&A handled competently

---

## Scenario-Specific Bonus Considerations (+0 to +3 points)

Evaluators may award up to **3 bonus points** for exceptional scenario alignment (does not exceed 100 total):

| Scenario | Bonus Criteria |
|----------|----------------|
| **Banking** | Audit trail, lineage doc, regulatory dataset naming |
| **Healthcare** | PII masking demo, HIPAA-aware access matrix |
| **E-Commerce** | Star schema in curated, KPI query demo |
| **Enterprise** | Multiple ingestion patterns, Step Functions orchestration |

---

## Submission Requirements (Pass/Fail Gate)

Failure to meet any item may cap the capstone at **69%** until remediated:

| Requirement | Mandatory |
|-------------|-----------|
| GitHub repository or equivalent code submission | Yes |
| All AWS resources tagged | Yes |
| Presentation delivered in final session | Yes |
| `terraform destroy` instructions in README | Yes |
| No committed AWS credentials | Yes |

---

## Grade Scale

| Total Score | Letter | Description |
|-------------|--------|-------------|
| 90–100 (+ bonus max 103) | A | Portfolio-ready; hireable demonstration |
| 80–89 | B | Strong project; minor gaps |
| 70–79 | C | Meets minimum; needs polish |
| 60–69 | D | Significant gaps; remediation required |
| < 60 | F | Does not meet capstone requirements |

---

## Self-Assessment Worksheet

Before submitting, score yourself honestly:

| Criterion | Self Score (/25, /20, /15) | Evidence Link |
|-----------|---------------------------|---------------|
| Architecture & Design | /25 | docs/ARCHITECTURE.md |
| Implementation | /25 | README Quick Start |
| Quality & Governance | /20 | GOVERNANCE.md, quarantine sample |
| Monitoring & Ops | /15 | Dashboard, COST-ANALYSIS.md |
| Docs & Presentation | /15 | slides/, README |
| **Total** | /100 | |

Target **≥ 85** before presentation day.

---

## Evaluator Notes Template

```markdown
## Capstone Evaluation – [Student Name]

**Scenario:** Option [N] – [Name]
**Date:**

### Scores
- Architecture: /25
- Implementation: /25
- Quality & Governance: /20
- Monitoring: /15
- Documentation & Presentation: /15
- Bonus: /3
- **Total: /100**

### Strengths
-

### Improvements
-

### Pass gate items
- [ ] Repo submitted
- [ ] Tags verified
- [ ] Presentation complete
```
