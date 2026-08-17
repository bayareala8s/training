# Rubric Notes — Module 06

**Base:** [`standard-architecture-rubric.md`](standard-architecture-rubric.md)

| Criterion | “4” this week |
| --------- | ------------- |
| Business alignment | Patterns tied to NorthStar SLAs (teller lookup, payments, partners, regulatory) |
| Architecture quality | Clear sync/event/file/workflow separation; ownership boundaries explicit |
| Trade-off analysis | Matrix scored; ADRs compare real alternatives including cost |
| Security and resilience | DLQ/poison discussed; lab authZ debt acknowledged; no reckless always-on services |
| Feasibility and roadmap | Lab evidence or approved narrative; cleanup; Transfer decision criteria for prod |
| Communication quality | Executive-readable diagrams and ADR prose |

## Automatic deductions

- Shared database proposed as primary integration (−1 architecture quality)  
- Transfer Family / NAT / EKS deployed in lab (−1 feasibility; possible safety flag)  
- No cleanup confirmation (−1 feasibility)  
- ESB-for-everything with no criteria (−1 trade-off analysis)
