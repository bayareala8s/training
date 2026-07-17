# ADR-NS-043 — Production Access for Contractors via PAM/JIT Only

**Status:** Accepted (ARB 2026-07)  
**Date:** 2026-07-15  

## Context

Retail Payments requested standing administrative production access for eight contractors for nine months to speed hypercare.

## Decision drivers

1. Least privilege and zero standing admin  
2. Auditability (session recording, ticket linkage)  
3. Hypercare responsiveness  
4. Contractor lifecycle and offboarding risk  

## Options considered

| Option | Summary |
| ------ | ------- |
| A. Standing cluster-admin for 9 months | Fast; unacceptable privilege concentration |
| B. Standing read-only + on-call FTEs for changes | Safer; may bottleneck |
| C. JIT/PAM elevation with MFA + session recording (≤90 days, renewable) | Balances speed and control |
| D. No contractor prod access | Cleanest security; may fail hypercare staffing |

## Decision

Choose **Option C**. Reject standing admin. Approve JIT/PAM with authenticator/hardware MFA, session recording, change-ticket linkage, named users only, 90-day expiry with ARB/Security renewal.

## Consequences

**Positive:** Reduces blast radius; creates audit evidence; forces ownership of access renewals.  
**Negative:** Requires PAM onboarding before hypercare; slight process overhead.  
**Follow-ups:** Security provisions PAM; Delivery defines severity-based elevation paths.
