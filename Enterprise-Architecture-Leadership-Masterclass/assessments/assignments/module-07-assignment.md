# Assignment — Module 07: Security, Risk, Compliance, and Resilience

**Due:** Before the start of Module 08 live session (unless cohort calendar states otherwise)  
**Weight:** Contributes to Weekly labs / Architecture artifacts per assessment model  
**Rubric:** Standard architecture rubric + Module 07 notes  
**Case study:** NorthStar Financial Services (fictional)

---

## Purpose

Produce an executive-ready resilience and control-evidence pack for NorthStar’s settlement landing-zone platform slice, including a clear decision on replication versus simulated DR.

## Learning objectives assessed

1. M07-LO3 — RTO/RPO and recovery validation
2. M07-LO4 — Control-evidence and residual risk communication

## Instructions

1. Refine your lab threat model and trust-boundary diagram for executive readability.
2. Write a 1–2 page executive resilience brief: risks, RTO/RPO, what was tested, residual risk, and 90-day hardening backlog.
3. Complete a control-evidence matrix (≥8 rows) linking risks to implementations and evidence paths.
4. Author one ADR: **Enable CRR now vs. simulated DR + versioning** for Restricted settlement objects.
5. Include cleanup confirmation from the lab (or explain sandbox limitation with instructor approval).

## Required deliverables

| # | Artifact | Format |
| - | -------- | ------ |
| 1 | Executive resilience brief | PDF or Markdown |
| 2 | Control-evidence matrix | Markdown or CSV |
| 3 | ADR (CRR vs simulated DR) | Markdown using ADR template |
| 4 | Lab evidence appendix | Screenshots/CLI excerpts + cleanup note |

## Constraints

- Use NorthStar context and constraints
- Explicitly document assumptions
- Include at least one meaningful trade-off table or ADR-style decision
- Synthetic data only; fiction notice on cover

## Rubric emphasis this week

| Criterion | Emphasis |
| --------- | -------- |
| Business alignment | High — tie RTO/RPO to payment settlement impact |
| Architecture quality | High — boundaries and least privilege coherence |
| Trade-off analysis | High — CRR vs drill cost/risk |
| Security and resilience | Highest |
| Feasibility and roadmap | Medium — 90-day backlog realism |
| Communication quality | High — executive brief clarity |

## Capstone contribution

Feeds: threat model, RTO/RPO worksheet, risk-control / control-evidence artifacts.

## Submission

Upload to BayLearn assignment `module-07`.  
Name files: `M07_<Artifact>_<LastName>.<ext>`
