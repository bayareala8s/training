# Instructor Guide — Module 06: Integration, Application, and Data Architecture

**Audience:** BayLearn instructors  
**Student materials:** modules/, labs/, assessments/ (non-key)  
**Classification:** Instructor-only when combined with reference solutions / answer keys

---

## 1. Module purpose

Teach pattern selection and ownership for NorthStar’s sync APIs, payment events, partner files, and regulatory batches—then make trade-offs concrete with a low-cost serverless AWS reference lab. Students leave with a pattern matrix, data-flow, ADRs, and working lab evidence (plus cleanup).

## 2. Learning objectives

1. Select integration/data patterns using an explicit multi-criteria matrix (M6-LO1).
2. Draw domain vs shared-platform ownership boundaries (M6-LO2).
3. Define data ownership for account, payment, and partner-file flows (M6-LO3).
4. Deploy a serverless reference architecture illustrating sync, event, file, and batch patterns (M6-LO4).
5. Defend cost/security trade-offs including why Transfer Family is optional in the lab (M6-LO5).

## 3. Prerequisites

Modules 01–05 context; AWS CLI + Terraform 1.5+; sandbox account with budget alert; SNS email available for confirmation; templates 01, 16, 22 skimmed.

## 4. Estimated timing (120 minutes)

| Segment | Minutes |
| ------- | ------: |
| Business scenario + Lesson 6.1 | 15 |
| Domains, data products, ownership (6.2–6.3) | 20 |
| Instructor demonstration (lab06 paths) | 15 |
| Guided lab | 40 |
| Architecture review | 15 |
| Assignment briefing | 10 |
| Buffer / breaks | 5 |

## 5. Opening business scenario

Partner onboarding still depends on three SFTP servers and a point-to-point database link. Payments need near-real-time fraud signals. Customer service needs synchronous account lookups. An “ESB for everything” proposal lands in email. Facilitate the room into **criteria before theology**.

> Fiction notice: NorthStar Financial Services is fictional.

## 6. Lesson flow

1. Pattern families and multi-criteria matrix (forbid “events because modern”).
2. Domain ownership vs platform mechanisms; ban shared-database shortcuts.
3. Data products, master data, events as contracts.
4. Demo four lab paths; sketch ADR Transfer Family vs S3 landing.
5. Lab timebox; protect review + assignment.

## 7. Questions to ask

1. What SLA and failure mode decide sync vs events for this interface?
2. Who owns the *meaning* of `PaymentSubmitted`—platform or Payments LOB?
3. What breaks if partner-file storms share the same worker pool as payments?
4. When would you approve Transfer Family despite idle-endpoint cost?

## 8. Whiteboard sequence

See `whiteboard-plan.md`. Summary:

1. Four swimlanes: Sync | Events | Files | Batch
2. Ownership boxes: Accounts | Payments | Partners | Platform
3. Failure modes: timeout | duplicate | poison | late file
4. Cost callout: Transfer Family hourly vs S3 put

## 9. Demonstration steps

1. Show `infrastructure/terraform/environments/lab06/` structure and tags.
2. Apply (or show pre-applied outputs): POST account; put payment event; S3 partner upload; start Step Functions.
3. Point at SQS DLQ and SNS confirmation; narrate intentional teaching debt (public API, no authZ).
4. Sketch ADR-M06-02: Transfer Family vs S3 landing simulation.

## 10. Break points

- After concept block (~35 min)
- Mid-lab check (~75 min)

## 11. Lab facilitation

See `lab-facilitation-guide.md`.

**Lab goal:** Working sync/event/file/workflow evidence + pattern matrix + ≥2 ADRs + cleanup.

**Timebox rule:** Protect the last 25 minutes for review + assignment briefing even if labs are incomplete. Artifact writing beats perfect Terraform green.

## 12. Common student issues

| Issue | Facilitation response |
| ----- | --------------------- |
| SNS unconfirmed | Walk Confirm subscription; no email = silent notify failures |
| EventBridge JSON typos | Provide source/detail-type snippet; validate with Console |
| Over-scoping Transfer Family | Reiterate optional/conceptual; S3 landing is the lab pattern |
| One ESB for all patterns | Force matrix scores; ask which failure mode worsens |
| Skipping DLQ discussion | Ask: poison message fate without DLQ? |
| No cleanup | Mandatory shout-out; run cleanup script before leaving |

## 13. Debrief questions

Use `modules/module-06-integration-data/debrief-questions.md`.

## 14. Assignment briefing

Integration pattern matrix, payments + partner data-flow, two ADRs (sync vs events; Transfer vs S3), lab evidence + cleanup note. Rubric emphasizes trade-offs, ownership clarity, and feasibility.

## 15. Suggested homework

Finish lab artifacts; formative quiz; skim Module 07 security/resilience (DLQ, IAM, blast radius).

---

## Materials checklist

- [ ] Slides / script reviewed
- [ ] `lab06` Terraform validated in instructor account recently
- [ ] SNS email confirmable
- [ ] Reference solution private
- [ ] Grading guide ready
- [ ] Cleanup script path announced: `infrastructure/terraform/scripts/cleanup-lab06.sh`
