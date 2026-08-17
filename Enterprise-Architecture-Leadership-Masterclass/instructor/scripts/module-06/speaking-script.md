# Speaking Script — Module 06: Integration, Application, and Data Architecture

**Total runtime target:** 120 minutes  
**Tone:** Executive, practical, trade-off aware  
**Case study:** NorthStar Financial Services (fictional)

Instructors may paraphrase; timing cues are targets.

---

## [0:00–0:05] Welcome and framing

> Welcome back to the Enterprise Architecture Leadership Masterclass.  
> Today is Module 06: Integration, Application, and Data Architecture.  
> Remember: you are the Lead Enterprise Architect at NorthStar Financial Services—our fictional enterprise case study.  
> By the end of this session you will select patterns with explicit criteria, clarify domain versus platform ownership, and deploy a low-cost AWS reference architecture that makes those trade-offs tangible.

---

## [0:05–0:15] Business scenario

> Partner onboarding still depends on three SFTP servers, two nightly batches, and a point-to-point database link nobody wants to own. Payments need near-real-time fraud signals. Customer service needs synchronous account lookups. And someone just emailed an “ESB for everything” proposal.  
> If your first move is to bless the hub, you skipped the hard part: **pattern selection with failure modes**.

**Ask the room:**

> What criteria decide sync API versus events versus files for a single NorthStar interface?

---

## [0:15–0:35] Architecture concept

> Patterns are not fashion. We score latency, coupling, volume, reliability, security, cost, and ops complexity. Account lookup is usually sync-primary. Payment submitted is usually event-plus-queue with a DLQ. Partner exchange is still often file landing. Regulatory windows want orchestration.  
> Domains own the *meaning* of business events. The shared platform owns buses, queues, gateways, and operational patterns. Shared databases as integration are hidden coupling—treat them as debt, not strategy.  
> Data products and master data need owners. Partner files are exchange formats, not systems of record.

**Check for understanding:**

> Who owns `PaymentSubmitted` semantics—platform team or Payments LOB? Defend the line.

---

## [0:35–0:50] Instructor demonstration

> Watch how I would prove the reference architecture on AWS without lighting money on fire. Transfer Family is conceptual only—we simulate partner files with S3 landing.

**Demo steps (narrate while doing):**

1. Show `infrastructure/terraform/environments/lab06/` and required tags.
2. POST account create/lookup via API Gateway; show DynamoDB write.
3. Put a `PaymentSubmitted` event; follow EventBridge → SQS (+ DLQ) → Lambda.
4. Drop a partner file into S3 `incoming/`; show file Lambda and event fan-out.
5. Start Step Functions for batch/analytics/notify; confirm SNS email was subscribed.
6. Sketch ADR: when NorthStar would buy Transfer Family or MFT versus S3 landing.

> Notice intentional teaching debt: this lab API is not production-authorized. Your artifacts must still name the production controls you would add.

---

## [0:50–1:30] Guided lab

> You now have about 40 minutes. Work in pairs if you want; submissions are individual.  
> Lab: Build NorthStar’s Integration Reference Architecture.  
> Deliverables: working evidence for four paths, pattern matrix, data-flow, two ADRs, cleanup confirmation.  
> Confirm SNS early. Midway I will call a two-minute progress check. Artifact writing starts by minute thirty-five even if Step Functions is still pending.

**[1:10] Mid-lab check**

> Which path is green, which is stuck, and what failure mode worries you most?

---

## [1:30–1:45] Architecture review

> Let’s review one or two volunteer artifacts ARB-style: alignment, risk, alternatives, feasibility—not Mermaid aesthetics.

**Prompt:**

> Walk us from one interface SLA to one pattern choice to one ownership decision—and name the consumer who breaks if the schema changes.

---

## [1:45–1:55] Assignment briefing

> Assignment Module 06: polished pattern matrix, payments-plus-partner data-flow, ADR-M06-01 and ADR-M06-02, lab evidence and cleanup note. Rubric weights trade-offs and ownership clarity. These artifacts feed the capstone integration reference architecture.

---

## [1:55–2:00] Close and cleanup

> Destroy resources today using `infrastructure/terraform/scripts/cleanup-lab06.sh`. Formative quiz is available. Next week: Module 07—security and resilience on the paths you just built.  
> Thank you—see you with DLQs and blast-radius thinking.
