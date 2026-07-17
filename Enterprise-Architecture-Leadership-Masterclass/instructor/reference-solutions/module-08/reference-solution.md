# Reference Solution — Module 08 (Instructor Only)

**Do not distribute to students.**  
**Lab:** Build NorthStar’s Governed AI Decision Assistant  
**Case study:** NorthStar Financial Services (fictional)  
**Data:** Synthetic incidents only (`incident-eval-set.csv`)

---

## 1. Use-case scorecard (exemplar)

| Dimension | Score (1–5) | Notes |
| --------- | ----------- | ----- |
| Business value | 5 | Faster, more consistent triage; reduces MTTR variance |
| Feasibility | 4 | Structured task; mock or Bedrock workable |
| Data readiness | 3 | Needs sanitized historical tickets; lab uses synthetic set |
| Risk / harm | 2 (elevated risk → lower comfort) | Wrong High routing delays payments/ops |
| Operability | 4 | HITL + logging + metrics fit IR operating model |
| Cost sensitivity | 4 | Low at lab scale; monitor tokens if live |
| Strategic alignment | 5 | Ties to resilience and customer impact visibility |

**Decision:** Conditional-go. HITL required for severity ≥ High, schema validation failures, low confidence, or regulated/remediation suggestions. No autonomous remediations.

---

## 2. Architecture (expected shape)

```text
Client → API Gateway → Step Functions
  → Infer (Bedrock or deterministic mock)
  → Validate + route (schema + deterministic HITL rules)
  → Persist (DynamoDB decision record)
  → Safe logs (S3, redacted)
  → CloudWatch metrics (invokes, tokens/cost estimates)
```

**Design rules students should state:**

- Structured JSON output (category, severity, business_impact, routing_team, next_actions, hitl_required, confidence)
- Validation before persistence
- Model proposes; rules decide autonomy
- Mock mode is architecturally valid

---

## 3. JSON schema fields (minimum)

| Field | Type | Notes |
| ----- | ---- | ----- |
| category | enum | e.g., payments, identity, platform, partner, other |
| severity | enum | Low / Medium / High / Critical |
| business_impact | string | Short controlled phrasing |
| routing_team | enum | Known IR/product queues |
| next_actions | array[string] | Advise-only in lab |
| hitl_required | boolean | Forced true on triggers |
| confidence | number 0–1 | Optional but useful for HITL |

Invalid or missing required fields → HITL + do not auto-route as trusted.

---

## 4. HITL policy (exemplar)

Force HITL when any of:

1. severity ∈ {High, Critical}  
2. confidence < 0.6 (if present)  
3. schema validation failure  
4. category = other / unknown  
5. next_actions include remediation verbs (restart, block, delete, transfer funds)

Default posture: **advise and route**, never auto-execute.

---

## 5. Evaluation approach

**Dataset:** `labs/lab-08-ai-decision-assistant/datasets/incident-eval-set.csv`  

**Quality measure (example):** Field agreement rate on `category` and `severity` vs labels; secondary: `routing_team` agreement; track HITL precision (HITL flagged when label severity High/Critical).

**Exemplar narrative:** “On N labeled rows, category agreement = X%, severity agreement = Y%. All Critical labels produced hitl_required=true. Residual risk: Medium severity edge cases under-routed—mitigate with broader HITL band or human QA sample.”

---

## 6. Cost / token notes

- Mock mode: negligible model cost; still note API/Lambda/SFn if deployed  
- Live Bedrock: record input/output token estimates per invoke; monthly projection at expected IR volume  
- Architecture NFR: budget alerts, max tokens per request, logging sampling  

---

## 7. Lab evidence checklist

- [ ] Scorecard with conditional-go  
- [ ] Architecture diagram showing validation + HITL  
- [ ] Successful invoke (mock or Bedrock)  
- [ ] Validation failure → HITL evidence  
- [ ] Eval results with explicit metric  
- [ ] Safe-log / redaction note  
- [ ] Cost/token note  
- [ ] Cleanup if AWS resources created  

---

## 8. Executive one-liner

> NorthStar will pilot a governed incident decision assistant that proposes structured triage with mandatory human review for high-severity and low-confidence cases, measured against a labeled evaluation set before any autonomy expansion.
