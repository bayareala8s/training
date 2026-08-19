# Lesson 2.6 — API Versioning

**Module:** 02 — API-Based Integration  
**Duration:** 25–35 minutes  
**BayLearn philosophy:** WHY → WHEN → HOW. Pattern first. Technology second.

---

## Learning outcomes

By the end of this lesson you will be able to:

1. Choose URI, header, or media-type versioning with eyes open.
2. Define compatible vs breaking evolution.
3. Plan deprecation, dual-run, and sunset.

---

## Enterprise scenario

Northbridge’s /v1/customers returns a single address string. /v2 returns structured lines plus country. Mobile can migrate in a quarter; a corporate payroll partner cannot. Versioning is a product strategy, not a URL fashion.

> **Fiction notice:** Named companies in this course (Northbridge Bank, Harbor Retail, CareMesh Health, Atlas Manufacturing) are instructional fictions.

---

## WHY this exists

APIs change. Versioning is how you change without a flag day. Compatible changes (additive optional fields, new endpoints) should not require a major version if consumers ignore unknowns. Breaking changes need a new version and a sunset policy. Running two versions has a real cost: double tests, double bugs, double IAM.

---

## WHEN an Enterprise Architect uses it

- External or numerous consumers.
- Breaking semantic changes to existing fields.
- Regulatory formats that must remain stable for years.

### When NOT to use it

- Do not version every additive field.
- Do not keep v1 forever without an owner and a kill date.
- Do not use versions to hide a bad resource model (fix the model).

---

## HOW — the pattern (vendor-neutral)

Prefer additive evolution. When you must break: introduce vN, route both, emit metrics on vN-1 usage, communicate, sunset. Header versioning keeps URLs pretty but is harder to try in a browser. URI versioning is explicit for partners. Either is fine if it is consistent and automated.

### Architecture diagram

```mermaid
flowchart LR
  C1[v1 clients] --> V1[/v1]
  C2[v2 clients] --> V2[/v2]
  V1 --> T[Translator]
  V2 --> D[(Store)]
  T --> D
```

---

## HOW — AWS implementation (after the pattern)

API Gateway stage variables or path prefixes (/v1, /v2) are implementation. Custom domains can hide this. The hard part is data: can v1 and v2 share the same DynamoDB item shape with translation?

Do not start here. If you cannot explain the requirement and pattern without naming an AWS service, you are not ready to select technology.

---

## Anti-patterns

- Silent reinterpretation of an existing field’s meaning.
- v1, v2, v3 all eternally in production.

---

## Tradeoffs

| Dimension | Benefit | Cost / risk |
|-----------|---------|-------------|
| URI version | Obvious to partners | URL proliferation |
| Header version | Cleaner URLs | Worse discoverability |

---

## Architecture decision prompt

You must add a second address. Is that a new field on v1 or a v2? What is the sunset for the payroll partner?

Write four sentences: the requirement, the integration characteristics, the pattern, and why the rejected options fail the NFRs.

---

## Knowledge check

**Q1.** Is adding an optional field a breaking change?

*Answer.* Usually no, if clients ignore unknown fields and the field is truly optional in behavior.

---

## Architect's note

Put the sunset date in the ADR, not in Slack.

---

## Next

Complete any architecture challenge attached to this lesson in the course player. Record an ADR fragment if the decision would survive a design review.
