# Lab Facilitation Guide — Module 08

**Lab:** Build NorthStar’s Governed AI Decision Assistant  
**Student path:** `labs/lab-08-ai-decision-assistant/`  
**Dataset:** `labs/lab-08-ai-decision-assistant/datasets/incident-eval-set.csv`

---

## Setup (before class)

- Default lab var: `use_mock_bedrock = true` unless Bedrock access verified
- Confirm eval CSV readable; skim label fields
- Prep one good invoke payload and one schema-invalid payload
- Keep reference solution private
- Remind: synthetic incidents only; no real customer data

## Launch script (2 min)

> You are Lead EA. Score the incident assistant, deploy a governed invoke path—mock is first-class—validate JSON, route HITL, evaluate on the labeled set, and track tokens/cost. Forty minutes live. Artifacts beat perfect Bedrock enablement.

## Progress checkpoints

| Time | Check |
| ---- | ----- |
| +10 min | Scorecard draft with go/conditional-go |
| +15 min | Invoke path up (mock OK) |
| +25 min | Validation + HITL evidence for one High case |
| +30 min | Eval set: ≥5 rows scored with defined metric |
| +35 min | Safe-log + cost notes started |
| +40 min | Cleanup plan if AWS resources used |

## Stuck-student prompts

- “Which scorecard dimension is weakest—and does that change go/no-go?”
- “What field failing validation should force HITL every time?”
- “What is your quality measure in one sentence?”

## Facilitation risks

- Students blocked on Bedrock access → keep mock; do not derail class
- Over-logging sensitive text → enforce safe-log rules
- HITL forever → force explicit triggers
- Skipping eval → require metric + sample scores before review

## Review selection

Prefer one clear HITL policy with eval numbers over a flashy demo with no metric.
