# Answer Key — Module 06 (Instructor Only)

| Q | Answer | Explanation |
| - | ------ | ----------- |
| Q1 | B | Multi-criteria selection is the module core method |
| Q2 | B | User-facing lookup needs sync primary for latency SLA |
| Q3 | B | Events + queue + DLQ buffers and isolates poison |
| Q4 | B | Domains own semantics; platform owns mechanisms |
| Q5 | B | Shared DB is coupling debt; require exit / prefer contracts |
| Q6 | B | Transfer Family idle cost unsuitable for ephemeral labs |
| Q7 | B | Files are exchange formats, not masters |
| Q8 | B | Poison without DLQ stalls or storms consumers |
| Q9 | A | Heterogeneous SLAs expose ESB-for-everything weakness |
| Q10 | B | ADR structure with alternatives and consequences |

## Scenario guidance

**S1:** Tellers → sync API (secondary events on change). Fraud → payment events/stream with clear consumer contract. Reject shared DB or ESB-for-everything without criteria.

**S2:** Lab uses S3 landing; production MFT/Transfer when protocol, compliance, and managed connectivity justify cost. Evidence: partner count, SLA, idle cost, ops skills, security controls. Do not deploy Transfer in student labs.

**S3:** Accounts domain owns authoritative corrections; analytics is consumer or proposes via governed API. Guardrails: schema ownership, producer ACL, conflict policy, audit of correction events.

## Discussion

No single script; score for trade-off quality, ownership clarity, and NorthStar realism.
