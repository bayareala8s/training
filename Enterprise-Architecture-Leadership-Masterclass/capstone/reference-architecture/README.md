# Capstone Reference Architecture — INSTRUCTOR ONLY

**Classification:** Instructor-oriented reference  
**Do not distribute as a student answer key wholesale.**  
Selective excerpts may be shown in office hours after students attempt their own designs.

> Fiction notice: NorthStar Financial Services is fictional.

---

## Intent

Provide a coherent reference target for grading calibration: shared landing zone on a primary cloud, enterprise identity, integration backbone, managed data platforms, resilience patterns, and governed AI decision support.

Students may differ and still score Excellent if trade-offs are explicit and feasible.

## Contents

| File | Description |
| ---- | ----------- |
| [`target-state.mmd`](target-state.mmd) | Consolidated target-state Mermaid source (**INSTRUCTOR**) |
| [`01-target-context.md`](01-target-context.md) | Context diagram |
| [`02-platform-landing-zone.md`](02-platform-landing-zone.md) | Landing zone / shared services |
| [`03-integration-backbone.md`](03-integration-backbone.md) | API + events |
| [`04-security-resilience.md`](04-security-resilience.md) | Identity, controls, DR |
| [`05-ai-governed-path.md`](05-ai-governed-path.md) | HITL AI path |

### Target-state narrative (summary)

NorthStar’s reference target consolidates onto a **primary-cloud landing zone** with shared identity/PAM, observability, and FinOps guardrails; an **API + event backbone** for partner and domain integration; **managed data platforms / MDM** for customer and merchant golden records; **proportionate resilience classes** for payments and onboarding; and a **governed AI path** with human-in-the-loop for high-impact decisions. Acquired systems coexist through transition states—mass rewrite is rejected.

## Calibration notes

- Reject uncontrolled second-cloud expansion without sovereignty drivers  
- Prefer golden paths + exceptions over centralizing every change  
- Sequence platform foundations before mass migration
