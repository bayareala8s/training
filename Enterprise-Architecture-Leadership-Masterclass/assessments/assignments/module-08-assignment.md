# Assignment — Module 08: AI Strategy and Intelligent Enterprise Architecture

**Due:** Before Module 09 live session  
**Rubric:** Standard architecture rubric + module-08 rubric notes  
**Case study:** NorthStar Financial Services (fictional)

---

## Purpose

Produce an executive-ready AI strategy package for NorthStar’s incident decision assistant: scored use case, governed architecture, HITL policy, evaluation results, and residual risk/cost narrative—without hype or ungoverned autonomy.

## Learning objectives assessed

1. M08-LO1 Use-case scorecard and go/no-go  
2. M08-LO2 Governed architecture with structured outputs  
3. M08-LO3 HITL, safe logging, cost tracking  
4. M08-LO4 Evaluation with labeled dataset and quality measure  

## Instructions

1. Complete Lab 08 using mock or Bedrock mode (document which).
2. Complete an AI use-case scorecard (`student/templates/12-ai-use-case-scorecard.md`) for the incident assistant.
3. Produce an architecture diagram and structured output / validation notes.
4. Write a HITL policy with explicit triggers; complete relevant items in `student/templates/19-ai-governance-checklist.md`.
5. Evaluate ≥10 rows from `labs/lab-08-ai-decision-assistant/datasets/incident-eval-set.csv` (or all rows if fewer) with an explicit quality measure.
6. Attach invoke evidence, safe-log note, cost/token note, and cleanup confirmation if AWS resources were created.
7. Write a one-page executive residual-risk narrative (what you will not automate yet).

## Required deliverables

| # | Artifact | Format |
| - | -------- | ------ |
| 1 | Use-case scorecard + decision | Markdown/table |
| 2 | Architecture diagram + schema/validation notes | Mermaid/PNG + markdown |
| 3 | HITL policy + governance checklist excerpt | Markdown |
| 4 | Eval results + quality measure | Markdown/CSV excerpt |
| 5 | Lab evidence + cost/token + cleanup | Screenshots/CLI + short markdown |
| 6 | Executive residual-risk narrative | ≤1 page |

## Constraints

- NorthStar fictional; synthetic incidents only—no real customer data  
- Mock mode is fully acceptable  
- No autonomous remediations in lab  
- Explicit trade-offs and residual risk required  

## Rubric emphasis this week

| Criterion | Emphasis |
| --------- | -------- |
| Business alignment | High |
| Architecture quality | High |
| Trade-off analysis | High |
| Security and resilience | High (HITL, safe log, no auto-execute) |
| Feasibility and roadmap | High |
| Communication quality | High |

## Capstone contribution

AI use-case scorecard, governed architecture, HITL/eval approach for Module 10.

## Submission

BayLearn assignment `module-08`. Files: `M08_<Artifact>_<LastName>.<ext>`
