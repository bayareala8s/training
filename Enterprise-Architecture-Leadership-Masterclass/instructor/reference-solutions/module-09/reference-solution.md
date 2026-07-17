# Module 09 — Reference Solution Overview

**Classification:** Instructor-only  
**Case study:** NorthStar Financial Services (fictional)

---

## Recommended dispositions

| Request | Disposition | Rationale (summary) |
| ------- | ----------- | ------------------- |
| CloudNova second cloud | **Reject** | Parallel ops, identity, logging, DR, FinOps; no sovereignty driver |
| VectorForge as SoR | **Reject** | Lock-in, key management gaps, golden-record conflict; benchmarks ≠ enterprise fit |
| PayWireFX custom framework | **Reject** as platform; **Approve limited adapters** on enterprise integration platform | Avoid new integration standard |
| Standing contractor prod admin | **Reject**; **Approve** JIT/PAM with session recording for ≤90 days hypercare | Least privilege |

## Alternate path (standards-aligned)

1. Onboard Retail Payments to primary-cloud landing zone within 3 weeks (platform commitment).  
2. Use approved managed data store with CMEK, PITR, and enterprise backup policy.  
3. Deliver partner integrations via enterprise API gateway + event backbone; allow thin partner-specific adapters.  
4. Provide PAM/JIT production access with MFA (authenticator/hardware), session recording, and ticket linkage.  
5. Re-baseline merchant soft launch by +3–5 weeks if needed; protect hard board narrative with phased scope (onboarding first, settlement exceptions second).

## What “good” student work looks like

- Splits four decisions  
- Names precedent risk  
- Quantifies or ranges dual-running cost  
- Offers a path that can still move merchant outcomes  
- Writes memo without jargon stacks
