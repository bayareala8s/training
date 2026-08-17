# ADR-NS-041 — Reject Second Public Cloud for Retail Payments Workloads

**Status:** Accepted (ARB 2026-07)  
**Date:** 2026-07-15  
**Deciders:** ARB (Lead EA, Platform, Security, Delivery, Data, Business sponsor)

## Context

Retail Payments proposed hosting new merchant services exclusively on CloudNova (second public cloud), citing contractor familiarity and vendor credits. NorthStar’s strategy is to standardize on a primary cloud landing zone with shared identity, logging, FinOps, and DR patterns.

## Decision drivers

1. Minimize dual operating models  
2. Preserve enterprise identity and audit evidence paths  
3. Control run-cost and skills concentration  
4. Meet merchant outcomes with acceptable schedule risk  

## Options considered

| Option | Summary |
| ------ | ------- |
| A. Approve CloudNova for payments domain | Fast for current contractors; permanent dual-cloud ops |
| B. Multi-cloud active-active by design | Strategic complexity unjustified by drivers |
| C. Reject; use primary landing zone with fast-track onboarding | Aligns to strategy; requires platform capacity |
| D. Time-bound CloudNova pilot (non-prod only) | Learning value without production precedent |

## Decision

Choose **Option C**. Reject CloudNova for production Retail Payments workloads. Non-prod experiments require separate exception with expiry and no production data.

## Consequences

**Positive:** Single operating model; clearer audit story; reusable platform investment.  
**Negative:** Contractor ramp on primary cloud; possible 3–5 week schedule impact.  
**Follow-ups:** Platform publishes onboarding runbook; BU revises plan without CloudNova dependencies.
