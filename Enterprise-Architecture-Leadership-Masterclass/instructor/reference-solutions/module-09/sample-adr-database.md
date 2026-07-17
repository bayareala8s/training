# ADR-NS-042 — Reject Proprietary VectorForge DB as Merchant System of Record

**Status:** Accepted (ARB 2026-07)  
**Date:** 2026-07-15  

## Context

Retail Payments proposed VectorForge DB for merchant profile and fee schedules, including KYC attributes. Vendor benchmarks claim higher throughput. Enterprise data strategy requires portable SoR technologies with CMEK, PITR, and alignment to golden-record programs.

## Decision drivers

1. Data portability and exit cost  
2. Key management and backup maturity  
3. Alignment to merchant/customer golden record  
4. Throughput needs validated with production-like tests on approved services  

## Options considered

| Option | Summary |
| ------ | ------- |
| A. Approve VectorForge as SoR | Throughput claims; high lock-in and key gaps |
| B. Approve VectorForge as cache only | Still introduces vendor ops; limited benefit |
| C. Reject; use approved managed relational/NoSQL with CMEK/PITR | Fits standards; validate performance |
| D. Defer pending independent benchmark on approved stack | Acceptable if date allows; not default |

## Decision

Choose **Option C**. VectorForge is not approved as system of record. Any vendor PoC must be non-prod, CMEK-capable evaluation only, with explicit exit criteria.

## Consequences

**Positive:** Reduces lock-in; supports golden-record convergence; improves backup/DR posture.  
**Negative:** BU must redo data model on approved service; license negotiations may need commercial unwind.  
**Follow-ups:** Data architect defines SoR schema ownership; Security verifies CMEK and PITR before prod load.
