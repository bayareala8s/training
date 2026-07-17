# Learning Objectives — Module 08

**Module:** AI Strategy and Intelligent Enterprise Architecture  
**Course outcomes mapped:** LO 22, 23, 24  
**Case study:** NorthStar Financial Services (fictional)

---

## Module-level objectives

| ID | Objective | Bloom | Primary lesson | Lab evidence |
| -- | -------- | ----- | -------------- | ------------ |
| M08-LO1 | Score AI use cases with explicit criteria and go/no-go rationale | Evaluate | 8.1 | Use-case scorecard |
| M08-LO2 | Design governed AI architecture with structured outputs and validation | Create | 8.2 | Architecture + prompt/schema |
| M08-LO3 | Route high-risk outputs through HITL with safe logging and cost tracking | Apply | 8.3 | HITL path + log/cost evidence |
| M08-LO4 | Evaluate assistant quality with a labeled dataset and defined metric | Analyze | 8.4 | Eval results write-up |

---

## Lesson-level outcomes

### 8.1
- Distinguish strategy theater from measurable AI outcomes
- Apply scorecard dimensions: value, feasibility, data, risk, operability, cost, alignment

### 8.2
- Explain reference architecture: API → orchestration → model → validate → persist → HITL
- Prefer structured JSON over free text for operational decisions

### 8.3
- Define HITL triggers (severity, confidence, regulated actions)
- Separate model inference from deterministic business rules

### 8.4
- Track tokens/cost as architecture concerns
- Communicate residual AI risk to executives without hype

---

## Success criteria

1. Scorecard with go/no-go and HITL stance
2. Diagram showing validation and HITL gates
3. Successful invoke in Bedrock **or** documented mock mode
4. Eval set scored with an explicit quality measure
