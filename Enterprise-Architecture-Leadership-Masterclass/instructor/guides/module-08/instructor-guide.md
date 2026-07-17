# Instructor Guide — Module 08: AI Strategy and Intelligent Enterprise Architecture

**Audience:** BayLearn instructors  
**Student materials:** modules/, labs/, assessments/ (non-key)  
**Classification:** Instructor-only when combined with reference solutions / answer keys

---

## 1. Module purpose

Equip students to select governed AI use cases for NorthStar, architect an incident decision assistant with structured outputs, validation, HITL, safe logging, and cost/token tracking, and evaluate quality with a labeled dataset—without hype or ungoverned chatbot theater.

## 2. Learning objectives

1. Score AI use cases with explicit criteria and go/no-go rationale (M08-LO1).
2. Design governed AI architecture with structured JSON outputs and validation (M08-LO2).
3. Route high-risk outputs through HITL with safe logging and cost tracking (M08-LO3).
4. Evaluate assistant quality with a labeled dataset and defined metric (M08-LO4).

## 3. Prerequisites

Modules 01–07 context; Module 07 security/resilience mindset; AWS CLI + Terraform optional for full lab; Bedrock model access **or** mock mode; dataset `labs/lab-08-ai-decision-assistant/datasets/incident-eval-set.csv`.

## 4. Estimated timing (120 minutes)

| Segment | Minutes |
| ------- | ------: |
| Scenario + use-case selection (8.1) | 15 |
| Governed architecture + HITL/eval (8.2–8.3) | 20 |
| Instructor demonstration (mock or Bedrock) | 15 |
| Guided lab | 40 |
| Architecture review | 15 |
| Assignment briefing | 10 |
| Buffer / breaks | 5 |

## 5. Opening business scenario

COO wants “AI everywhere.” Three BUs propose chatbots with no KPI. Incident Response drowns in noisy tickets. Facilitate: **scorecard before model brand**.

> Fiction notice: NorthStar Financial Services is fictional. Use synthetic incidents only.

## 6. Lesson flow

1. Use-case scorecard dimensions; conditional-go with HITL.
2. Reference architecture: API → orchestrate → infer → validate → persist → HITL.
3. Separate model inference from deterministic business rules.
4. Demo mock (default) or Bedrock path; show validation fail → HITL.
5. Lab: scorecard, invoke, eval set, cost notes.

## 7. Questions to ask

1. What operating KPI improves if this assistant works?
2. What happens on wrong High severity routing during a payment outage?
3. Which fields must be schema-validated versus free text?
4. Is token cost an architecture concern or only FinOps’ problem?

## 8. Whiteboard sequence

See `whiteboard-plan.md`.

## 9. Demonstration steps

1. Show scorecard for incident assistant (conditional-go).
2. Walk architecture Mermaid; highlight validation + HITL gates.
3. Invoke mock path; show structured JSON + DynamoDB/S3 safe log.
4. Force a validation failure; show HITL routing.
5. Score 3–5 eval-set rows with an explicit quality measure.

## 10. Break points

After concept (~35); mid-lab (~75).

## 11. Lab facilitation

See `lab-facilitation-guide.md`. Default **mock Bedrock** unless model access confirmed. Protect final 25 minutes for review + assignment.

## 12. Common student issues

| Issue | Facilitation response |
| ----- | --------------------- |
| Chatbot without schema | Force JSON schema + validation |
| HITL for everything | Define triggers (severity, confidence, regulated) |
| Logging PII | Safe-log rules; redact; synthetic only |
| Bedrock access denied | Stay on mock; still grade architecture/eval |
| No quality metric | Require accuracy/agreement definition on eval set |
| Cost ignored | Token/cost notes mandatory |

## 13. Debrief questions

Use `modules/module-08-ai-strategy/debrief-questions.md`.

## 14. Assignment briefing

AI strategy package: scorecard, governed architecture, HITL policy, eval results, cost/risk narrative. Capstone: AI governance checklist + architecture.

## 15. Suggested homework

Finish lab/eval; formative quiz; skim Module 09 governance (ARB for AI).

---

## Materials checklist

- [ ] Slides / script reviewed
- [ ] Mock path verified; Bedrock optional path documented
- [ ] Eval dataset available to students
- [ ] Reference solution private
- [ ] Grading guide ready
- [ ] Fiction + synthetic-incident reminder announced
