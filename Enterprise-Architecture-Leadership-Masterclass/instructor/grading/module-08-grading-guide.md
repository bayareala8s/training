# Grading Guide — Module 08

**Applies to:** Lab 08 + Module 08 assignment  
**Rubric:** Standard architecture rubric + `assessments/rubrics/module-08-rubric.md`  
**Answer key:** `assessments/answer-keys/module-08-answer-key.md`  
**Reference:** `instructor/reference-solutions/module-08/reference-solution.md`

---

## Score bands

| Band | Lab | Assignment package |
| ---- | --- | ------------------ |
| Excellent (4) | Scorecard + invoke (mock OK) + validation/HITL evidence + eval metric on ≥5 rows + cost note + safe-log | Clear residual risk; HITL policy; architecture gates; no hype |
| Proficient (3) | Most controls present; thinner eval | Scorecard + architecture + HITL; light metrics |
| Developing (2) | Chatbot free text; HITL undefined; no eval | Tool-chasing; missing validation |
| Beginning (1) | Real PII logged; autonomous remediation; no cleanup if AWS used | No go/no-go; ignores risk |

## What to reward

- Conditional-go with explicit HITL triggers  
- Structured outputs + validation  
- Honest mock-mode use  
- Defined quality measure  
- Token/cost as NFR  
- Advise-first posture for financial ops  

## What to penalize

- Free-text-only operational decisions (−1 architecture quality)  
- HITL forever with no triggers (−1 trade-off / operability)  
- Logging sensitive data (−1 security; safety flag)  
- Claiming success with no eval metric (−1 architecture / communication)  
- Auto-execute remediations in lab (−1 security/resilience)

## Quiz

Formative by default. Use answer key. Scenarios graded on governance quality and NorthStar realism.

## Capstone feed

Flag strong scorecards, HITL policies, and eval write-ups for Module 10 AI section.
