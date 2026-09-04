# ARCHITECT-1401 — Instructor solution

**Do not share this file with students before they submit the failure-domain table.**

The compact shape in the student lab is a *post-attempt* numbering check. It is not the scored narrative. A worksheet that only says “add a region” must not outscore a page with six domains, a 52-minute paragraph, and refusals.

Single-region multi-AZ `us-west-2` is a valid **99.99% design**. Multi-region is **DR-1403**. Do not apply NAT, EKS, multi-AZ RDS, ACM, or Route 53. Do not recreate `PaymentCluster` as HA. Do not silently change the Module 13 SLO from **99.9%**.

## Failure-domain table (acceptable content)

| Domain | What fails | Merchant symptom | Survives in multi-AZ single-region? | Still kills the 52-minute year if… |
|---|---|---|---|---|
| Task | One Fargate task / JVM | Brief 5xx or retry if the other task is up | Yes — ECS replaces; `desired_count` ≥ 2 | You run `desired_count=1` |
| AZ | One `us-west-2` AZ | Same, if ALB and tasks span AZs | Yes — tasks + ALB + paper datastore in ≥2 AZs | Tasks or datastore are single-AZ |
| ALB / edge | Regional ALB or the teaching name | HTTPS to `payments.apps.baypay.example` fails | Partially — ALB is multi-AZ **and still regional** | You treat the ALB as multi-region |
| Identity / TLS | Leaf, ACM issuance, IAM, `alias/baypay-payments` | Handshake fail; HTTP `:8080` from a jump box may still work | No — this is independent of AZ count | Leaf expires or cannot re-issue (INCIDENT-1402 class) |
| Datastore | Teaching Postgres unavailable | 5xx / pool timeout on authorize | Only on **paper** multi-AZ | You apply single-AZ RDS or pretend ND is the store |
| Region | `us-west-2` gone | Everything in-region is gone | No — that is DR-1403 | You claimed 99.99% *because* you “added a region” on a slide and never designed in-region |

## Fifty-two minutes (acceptable paragraph)

99.99% availability is about **52 minutes/year** (TRUST.md). A replaced task and a short AZ blip, if you already span AZs, can fit. A 60-minute regional outage **overdraws the year**. A leaf merchants cannot handshake for hours (the INCIDENT-1402 symptom class) also overdraws it. The Module 13 operated SLO remains **99.9%** (~43 minutes of equivalent downtime per 30-day month per OBSERVABILITY.md). Architecture goal ≠ dashboard SLO. Do not change 99.9% unless Priya and the product owner write a new contract and a new monthly budget (~4.3 minutes/month at 99.99%).

## Multi-AZ single-region (acceptable design)

- Host `payments.apps.baypay.example`, TLS at the ALB, tasks on **8080**, liveness `/actuator/health/liveness`.
- ALB in at least two `us-west-2` AZs; Fargate service `desired_count` ≥ 2, spread across AZs.
- Datastore: **paper** multi-AZ. Do not `apply` RDS.
- Secrets: `BAYPAY_DB_*` from Secrets Manager; KMS `alias/baypay-payments`; task role ≠ execution role.
- Identity/TLS is a row on the same page as AZ: expiry ticket at 30 days, page at 7 days (TRUST.md).
- This shape **is** allowed to be the 99.99% answer.

## Region is not HA (acceptable paragraph)

“Just add `us-east-1`” is a **DR / RTO** sentence. It does not fix a single-AZ datastore, a `desired_count=1` service, or an expired leaf. 99.99% ≠ automatic multi-region. DR-1403 sets RPO/RTO and picks pilot light versus warm standby versus backup-restore. Applying a second region in a 90-minute lab is a failure.

## Refusals

- Do not apply NAT Gateway, EKS, multi-AZ RDS, ACM, or Route 53 in this lab.
- Do not recreate `PaymentCluster` / `dmgr-east` / `BayPayCell` as the HA design (Module 6 decommission path).
- Do not treat a second region as the only 99.99% answer.
- Do not upgrade Module 13 dashboards to 99.99% without an explicit contract change.

## Diagram

AEJE-D-064: merchants → TLS → regional ALB → tasks in two AZs → paper multi-AZ datastore; region boxed; `us-east-1` dashed as DR.

## Scoring notes

Full marks require six honest rows, a 52-minute paragraph that contrasts 99.9%, a complete multi-AZ single-region sketch, identity/TLS as a first-class domain, and the four refusals. “Always add a region” or “PaymentCluster is HA” caps Technical accuracy and Production awareness.
