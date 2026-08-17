# Rubric Notes — Module 08

**Base:** [`standard-architecture-rubric.md`](standard-architecture-rubric.md)

| Criterion | “4” this week |
| --------- | ------------- |
| Business alignment | Scorecard tied to IR KPI; conditional-go justified |
| Architecture quality | Structured outputs, validation, propose≠decide, clear gates |
| Trade-off analysis | Autonomy vs risk explicit; mock vs Bedrock reasoned |
| Security and resilience | HITL triggers, safe logging, no auto-execute, residual risk named |
| Feasibility and roadmap | Eval metric with results; cost/token notes; cleanup if AWS used |
| Communication quality | Executive-readable risk narrative without hype |

## Automatic deductions

- Free-text-only ops decisions (−1 architecture quality)  
- Real PII / production data in logs (−1 security; safety flag)  
- Auto-remediation without human gate (−1 security/resilience)  
- No quality measure / no eval (−1 feasibility)  
- “AI everywhere” with no scorecard (−1 business alignment)
