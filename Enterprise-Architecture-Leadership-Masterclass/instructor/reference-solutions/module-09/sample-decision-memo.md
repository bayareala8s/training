# Executive Decision Memo — Retail Payments Fast-Path ARB

**To:** CIO / Executive Technology Committee  
**From:** Lead Enterprise Architect  
**Date:** 2026-07-15  
**Re:** Disposition of NS-ARB-2026-091 (Retail Payments divergent proposal)  
**Case study:** NorthStar Financial Services (fictional)

---

## Decision requested

Reject the Retail Payments proposal to adopt a second public cloud (CloudNova), proprietary VectorForge database as system of record, and custom PayWireFX integration platform; reject standing contractor production admin; approve a standards-aligned alternate path with time-bound JIT production access and a platform fast-track.

## Why now

The BU has committed Year-1 spend and a Q4 merchant experience target. Approving as proposed would set enterprise precedent and create parallel operating models that increase run cost, audit gaps, and exit risk.

## Options

1. **Approve as proposed** — maximizes BU short-term velocity; creates multi-year dual-cloud and proprietary data tax; weakens identity and logging coherence.  
2. **Approve with broad exceptions** — similar enterprise tax with weaker accountability.  
3. **Reject divergent platform choices; accelerate golden-path onboarding (recommended)** — protects enterprise standards; may require a 3–5 week schedule rebase and phased scope.  
4. **Defer** — only if critical evidence appears within 5 business days; currently evidence is insufficient, not merely late.

## Recommendation

Choose Option 3.

### Impacts

| Dimension | Assessment |
| --------- | ---------- |
| Customer / merchant | Still achievable via phased delivery on primary platform |
| Cost | Avoids estimated $1.2–1.8M annual dual-running uplift (range; platform estimate) beyond BU Year-1 ask |
| Risk | Reduces identity split-brain, proprietary lock-in, and privileged access exposure |
| Timeline | Soft launch may shift 3–5 weeks; hard outcomes protected by scope phasing |
| Precedent | Prevents other BUs from claiming “payments exception” |

## Conditions / controls (alternate path)

1. Landing-zone namespace + CI guards ready in ≤15 business days (Platform owner).  
2. Managed data store with CMEK and PITR enabled before production data load (Data + Security).  
3. Integrations via enterprise gateway/events only; PayWireFX not adopted as framework (Delivery + Platform).  
4. Contractor production access via PAM/JIT only, MFA authenticator/hardware, session recording, 90-day expiry (Security).  

## Ask

Approve the disposition above and authorize platform fast-track capacity for Retail Payments onboarding to the enterprise landing zone.
