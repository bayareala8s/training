# INTERVIEW-1604 — Instructor solution

**Do not share this file with students before PF-design.md has a chosen prompt and a drawing.**

The compact shapes below are **post-attempt** checks. The scored work is the student’s this-quarter narrative on [student/worksheets/PF-design.md](../../student/worksheets/PF-design.md). Pasting `solutions/ARCHITECT-1401/` is a Diagnostic method fail.

Exactly **one** prompt. No AWS apply. No Bedrock. No portal. Cost **$0**.

Avery Chen `11111111-1111-1111-1111-111111111111`, account `…221`, example payment `c1604d44-0000-4000-8000-111111111604`. Host `payments.apps.baypay.example`. Process `payment-service` Java 21 / Spring Boot 3.5.5 `:8080`.

## Prompt 1 — payment create at 99.99% (acceptable content)

| Domain | Survives multi-AZ single-region `us-west-2`? | Still kills ~52 min/year if… |
|---|---|---|
| Task | Yes if `desired_count` ≥ 2 | Single task |
| AZ | Yes if tasks + ALB + paper datastore span AZs | Single-AZ datastore or tasks |
| ALB / edge | Partially — multi-AZ **and still regional** | Treated as multi-region |
| Identity / TLS | No — independent of AZ count | Leaf merchants cannot handshake |
| Datastore | Only on **paper** multi-AZ | Applied single-AZ RDS or ND-as-store |
| Region | No — that is DR | “Added a region” on a slide and never designed in-region |

**Fifty-two minutes.** 99.99% ≈ 52 minutes/year (TRUST.md). A replaced task and a short AZ blip can fit if already multi-AZ. A 60–90 minute region loss or a day-long handshake failure overdraws the year. Module 13 operated SLO stays **99.9%** (~43 minutes equivalent / 30d per OBSERVABILITY.md) unless Priya and a product owner write a new contract (~4.3 minutes/month at 99.99%).

**This-quarter call.** Multi-AZ single-region **is** allowed to be the 99.99% design. “Just add `us-east-1`” is the wrong *only* answer. `PaymentCluster` is not HA.

## Prompt 2 — modular monolith vs extract (acceptable content)

BayPay is **one** deployable with extractable modules (payments, refunds, posting/worker, notification). IoC keeps boundaries clean **before** a network hop.

**This-quarter call (default acceptable):** **stay monolith**. Criteria **not** met: no separate team owning notification end-to-end; no independent scale number that requires a second JVM; extract would buy a new trust boundary (mTLS, timeouts, dual-deploy, dual-failure) without a funded incident class. `transaction-worker` stays in-process until the bean boundary is already clean **and** a consistency story is written.

**Extract is acceptable** only if the student names **one** module and a concrete criterion (team + SLO + failure isolation) and the new hop’s failure mode. “Microservices are modern” is a fail.

Frozen `…222` and `Idempotency-Key` stay product controls on both sides of any future hop. Leftover ND is not an extract target.

## Shared refusals

- No NAT, EKS, multi-AZ RDS, ACM, Route 53, or `us-east-1` apply.
- No `dmgr-east` / PaymentCluster as HA or as the new service.
- No Bedrock-generated page as the submission.
- No PAN / live secrets / Avery on a metric label.
- ECS Fargate remains the **student apply default** if platforms are mentioned; EKS/OpenShift may win on paper (ARCHITECT-1102 literacy) without an apply.

## Scoring notes

Slogan-only (“add a region” / “split everything”) caps Technical accuracy. Apply caps Production awareness. Both prompts half-done: score the stronger one and cap Communication.

## Comms (acceptable example)

Staff design. This quarter we keep payment-service as a modular monolith on multi-AZ Fargate in us-west-2 behind TLS at payments.apps.baypay.example. Four nines is an in-region failure-domain page, not a second-region apply. We are not bouncing leftover ND and we are not extracting notification without a team and a hop budget. Avery’s create stays idempotent. Operated SLO stays 99.9% until someone changes the contract.
