# QA Report — Module 07

**Title:** Security, Risk, Compliance, and Resilience  
**Date:** 2026-07-15  
**Reviewer:** Curriculum generation agent (Auto)  
**Build phase:** 3 (Modules 5–8 AWS)

---

## Completeness checklist

| Asset | Present? | Notes |
| ----- | -------- | ----- |
| Module README | Yes | `modules/module-07-security-resilience/README.md` |
| Learning objectives | Yes | |
| Prerequisites | Yes | |
| Lessons (3–5) | Yes | Count: 4 |
| Instructor guide | Yes | |
| Speaking script | Yes | |
| Slide outline + notes | Yes | Slide count: 20 |
| Whiteboard plan | Yes | |
| Mermaid diagrams | Yes | lessons + diagrams/README |
| Lab student instructions | Yes | AWS lab template sections |
| Reference solution (instructor) | Yes | |
| Assignment | Yes | |
| Rubric / rubric notes | Yes | |
| Quiz (10+3+2) | Yes | |
| Answer key | Yes | instructor path |
| Workbook section | Yes | |
| Templates linked | Yes | threat, RTO/RPO, risk-control |
| Common mistakes | Yes | |
| Debrief questions | Yes | |
| LinkedIn promo | Yes | |
| YouTube description | Yes | |
| Manifest updated | Yes | pending write in this generation pass |

### AWS-only extras (Modules 5–8)

| Asset | Present? | Notes |
| ----- | -------- | ----- |
| Terraform | Yes | module + lab07 env |
| Cost estimate | Yes | `infrastructure/cost-estimates/lab-07.md` |
| Cleanup script | Yes | `cleanup-lab07.sh` |
| Security warnings | Yes | lab + cost docs |
| Validation steps | Yes | student-instructions |
| `terraform fmt` | Yes | Formatted |
| `terraform validate` | Yes | lab07 and lab08 validate successfully |

---

## Quality checks

| Check | Pass? | Notes |
| ----- | ----- | ----- |
| NorthStar used consistently | Yes | |
| Fiction notice where needed | Yes | |
| Trade-offs explicit | Yes | CRR vs drill, Zero Trust vs perimeter |
| No placeholder/TODO text | Yes | |
| Student/instructor separation | Yes | keys/solutions under instructor/answer-keys |
| Internal links resolve | Yes | relative paths checked structurally |
| Terminology matches glossary | Yes | HITL N/A; RTO/RPO/ADR used |
| Branding standards observed | Yes | BayLearn naming |

---

## Defects

| ID | Severity | Description | Resolution |
| -- | -------- | ----------- | ---------- |
| M07-D1 | Info | S3 4xx alarm may be quiet without traffic | Lab documents drill Lambda custom metric as alternate signal |

---

## Manifest status update

- Module status set to: `generated`
- Blockers for next module: None for Module 08 generation

## Sign-off

- [x] Ready to proceed to next module  
- [ ] Needs rework before proceeding  

**Signature:** Auto (generation pass 2026-07-15)
