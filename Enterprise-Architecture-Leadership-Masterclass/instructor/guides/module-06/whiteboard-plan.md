# Whiteboard Plan — Module 06: Integration, Application, and Data Architecture

**Session:** Live cohort  
**Boards needed:** 1 large (or digital equivalent)  
**Markers:** Black (structure), blue (ownership), red (risks), green (decisions)

---

## Board 1 — Pattern swimlanes (10 min)

Draw four columns:

| Sync API | Events / Queues | Files / Landing | Batch / Workflow |
| -------- | --------------- | --------------- | ---------------- |
| Account lookup | PaymentSubmitted | Partner SFTP → S3 | Regulatory extract |

**Prompt:** Place each NorthStar interface class; force one primary and one secondary.

## Board 2 — Ownership boxes (8 min)

Boxes: **Accounts domain** · **Payments domain** · **Partners domain** · **Shared integration platform**

Sticky rule: *semantics* stick to domains; *mechanisms* (bus, DLQ, API GW) stick to platform.

## Board 3 — Failure modes (7 min)

Four red cards: timeout · duplicate · poison · late/missing file  

Ask which pattern absorbs each, and what the consumer contract requires.

## Board 4 — Cost callout (5 min)

Two columns: **Transfer Family / MFT** vs **S3 landing + partner connectivity**  
Annotate idle hourly cost vs put/request cost; mark lab choice (S3) and production decision criteria.

## Capture for students

Photograph boards; map to templates `16-integration-pattern-matrix.md` and `22-data-flow-diagram.md`.
