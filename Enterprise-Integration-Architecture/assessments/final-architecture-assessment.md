# Final architecture assessment

This is **not** a multiple-choice exam.

## Scenario

A company has:

- 80 internal applications
- 30 external partners
- REST APIs
- SFTP partners
- 10 GB nightly files
- Legacy ERP
- Real-time customer events
- An AI operations assistant requirement

## Required artifacts

1. Integration inventory  
2. Pattern selection (per flow, using the course framework)  
3. Architecture diagram  
4. Technology selection (**after** style)  
5. Security  
6. Resiliency  
7. Observability  
8. AI-agent boundaries (forbidden vs required path)  
9. Migration approach (strangler; what stays on adapters)  
10. ADRs (at least three: file vs API, event vs queue, agent HITL)

## Timebox

Cohort: 3–4 hours take-home or 90 minutes timed design + 20 minutes oral defense.

## Rubric (summary)

| Band | Signal |
|------|--------|
| Distinction | NFRs drive styles; mixed patterns; honest residue; cost; agent governance |
| Pass | Framework used; some AWS named last; DLQ/idempotency present |
| Fail | Service-first; LLM→database; 10 GB through API Gateway; no inventory |

Submit under `submissions/final-assessment/`.
