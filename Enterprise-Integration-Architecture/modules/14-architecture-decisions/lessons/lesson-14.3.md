# Lesson 14.3 — Challenge: 20 GB × 50 Organizations Nightly

**Module:** 14 — Architecture Decision Making  
**Duration:** 25–35 minutes  
**BayLearn philosophy:** WHY → WHEN → HOW. Pattern first. Technology second.

---

## Learning outcomes

By the end of this lesson you will be able to:

1. Choose file style with a landing platform.
2. Reject API Gateway, SQS payload, DynamoDB item as transports.
3. Address partner heterogeneity and cost.

---

## Enterprise scenario

This is the spec’s challenge. Students who pick API Gateway fail. Students who pick S3 + Transfer + validation + catalog + events pass if they explain.

> **Fiction notice:** Named companies in this course (Northbridge Bank, Harbor Retail, CareMesh Health, Atlas Manufacturing) are instructional fictions.

---

## WHY this exists

Characteristics: huge payload, batch rhythm, 50 partners with mixed SFTP skill, nightly cutoff, reconciliation, cost of Transfer hours vs S3 APIs, duplicate detection, encryption. Architecture: landing zone, per-partner prefixes, optional SFTP edge, EventBridge FileReceived, workers, archive. Agent later asks “who has not delivered?”

---

## WHEN an Enterprise Architect uses it

- This challenge.
- Capstone 4.

### When NOT to use it

- One REST POST per 20 GB.
- One shared user for 50 orgs.

---

## HOW — the pattern (vendor-neutral)

Write the ADR. Include cost controls (destroy/stop SFTP, lifecycle). Include a late-file SLO.

### Architecture diagram

```mermaid
flowchart LR
  Orgs[50 orgs] -->|SFTP or S3 API| Land[Landing]
  Land --> Cat[Catalog]
  Cat --> Proc[Nightly processing]
```

---

## HOW — AWS implementation (after the pattern)

S3, Transfer Family where SFTP is required, EventBridge, SQS for per-file commands, DynamoDB catalog, KMS.

Do not start here. If you cannot explain the requirement and pattern without naming an AWS service, you are not ready to select technology.

---

## Anti-patterns

- Kafka for the bytes.
- A single 20GB API multipart through a gateway as Plan A.

---

## Tradeoffs

| Dimension | Benefit | Cost / risk |
|-----------|---------|-------------|
| SFTP edge | Partner reach | Hourly cost |
| S3 API only | Cheaper | Not all orgs can speak it |

---

## Architecture decision prompt

Defend why not EventBridge as the transport of the 20 GB.

Write four sentences: the requirement, the integration characteristics, the pattern, and why the rejected options fail the NFRs.

---

## Knowledge check

**Q1.** What style is this?

*Answer.* File, with events as notifications of file facts, not as byte transport.

---

## Architect's note

Explain every box. Silent boxes fail the challenge.

---

## Next

Complete any architecture challenge attached to this lesson in the course player. Record an ADR fragment if the decision would survive a design review.
