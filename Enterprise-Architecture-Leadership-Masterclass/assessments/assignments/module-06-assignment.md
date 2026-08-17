# Assignment — Module 06: Integration, Application, and Data Architecture

**Due:** Before Module 07 live session  
**Rubric:** Standard architecture rubric + module-06 rubric notes  
**Case study:** NorthStar Financial Services (fictional)

---

## Purpose

Produce an executive-ready integration architecture package: pattern selection with criteria, ownership clarity, data-flow for critical paths, and ADRs that include cost-aware file-transfer decisions—backed by Lab 06 evidence.

## Learning objectives assessed

1. M6-LO1 Pattern matrix with multi-criteria selection  
2. M6-LO2 Domain vs platform ownership  
3. M6-LO3 Data ownership for account, payment, partner flows  
4. M6-LO4 Lab reference architecture evidence  
5. M6-LO5 Cost/security trade-offs (Transfer Family vs S3 landing)

## Instructions

1. Complete Lab 06 (or document blockers + architecture-only path with instructor approval).
2. Complete an integration pattern matrix for account API, payments, partner files, and regulatory batch using `student/templates/16-integration-pattern-matrix.md`.
3. Draw a reference architecture diagram and a payments + partner data-flow (`student/templates/22-data-flow-diagram.md`).
4. Write ADR-M06-01 (sync vs events for account create side effects) and ADR-M06-02 (Transfer/MFT vs S3 landing) using `student/templates/01-architecture-decision-record.md`.
5. Attach lab evidence (CLI/screenshots), SNS confirmation note, cleanup confirmation, and a short cost note.

## Required deliverables

| # | Artifact | Format |
| - | -------- | ------ |
| 1 | Pattern matrix | Markdown/table |
| 2 | Reference architecture + data-flow | Mermaid/PNG + narrative |
| 3 | ADR-M06-01 and ADR-M06-02 | Markdown |
| 4 | Ownership notes (domains vs platform) | Markdown ≤1 page |
| 5 | Lab evidence + cleanup + cost note | Screenshots/CLI + short markdown |

## Constraints

- NorthStar fictional context; document assumptions  
- Explicit trade-offs (not pattern slogans)  
- Do not deploy Transfer Family, NAT Gateway, EKS, or always-on EC2 for the lab  
- Call out DLQ and intentional lab security debt  

## Rubric emphasis this week

| Criterion | Emphasis |
| --------- | -------- |
| Business alignment | High |
| Architecture quality | High |
| Trade-off analysis | High |
| Security and resilience | Medium–High (DLQ, authZ debt named) |
| Feasibility and roadmap | High |
| Communication quality | High |

## Capstone contribution

Integration reference architecture, pattern matrix, and ADRs for Module 10.

## Submission

BayLearn assignment `module-06`. Files: `M06_<Artifact>_<LastName>.<ext>`
