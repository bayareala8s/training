# DR-1403 — Instructor solution

**Do not share this file with students before they submit PF-dr.md.**

The compact TRUST.md numbers in the student lab are a *post-attempt* check. Students **may argue** those numbers with a Harbor Market / settlement / chargeback justification. A page that only says “warm standby in us-east-1” must not outscore a page with split RTO/RPO, a pattern pick, an idempotency story, and a do-not-fail-over list.

This is a **paper tabletop**. Do not apply `us-east-1`. Do not fail over to `BayPayCell` / `dmgr-east` / `PaymentCluster`.

## Starting numbers (TRUST.md — acceptable default)

| Workload | RPO | RTO | Pattern to defend |
|---|---|---|---|
| Payment authorize / complete | Seconds (idempotent retry + replicated ledger intent) | 60 minutes regional | Pilot light **or** warm standby in paper `us-east-1` |
| Merchant reporting | 24 hours | 24 hours | Backup restore |
| Leftover `BayPayCell` / `dmgr-east` | Not a DR target | Do not fail over to ND | Decommission path (Module 6) |

Acceptable arguments **away** from the defaults (must be written):

- Payments RTO 15–30 minutes → that **forces** warm standby (or hotter) and a standing `us-east-1` bill you must name.
- Payments RTO 4 hours → backup-restore can be honest if settlement allows it; you must say who accepts chargeback risk.
- Reporting RPO 1 hour → you are no longer “daily dump only”; say why finance needs it.

Unacceptable: same 24-hour RPO for authorize and reporting with no chargeback sentence; “fail over to PaymentCluster”; “apply the stack during the tabletop.”

## Pattern pick (acceptable)

**Default teaching pick for payments:** **pilot light** in `us-east-1` — core data replication (ledger intent, not PAN), a stopped or tiny compute footprint, DNS *plan* (not a lab flip), RTO aligned to **60 minutes** if the runbook is rehearsed.

**Warm standby** is acceptable if the student names the idle ALB + Fargate + replica cost and why 60 minutes is too slow for Harbor Market.

**Backup-restore for payments** is acceptable only with an explicit RTO change (hours) and a product owner. It is the **default for reporting**, not for authorize, unless they argue.

Losers to write:

- Active-active two-region payments: split-brain / dual authorize; new failure domain; not this quarter.
- Backup-restore for authorize at a 60-minute RTO: you will miss it.
- Hot copy of BUILD-1101 applied in the lab: cost and policy failure.

## Data and idempotency (acceptable paragraph)

Replicate **ledger intent** and idempotency keys, not PAN (tokenize or never persist). Avery’s client retries the same `Idempotency-Key` for `c1402b22-0000-4000-8000-111111111402`. After a regional cut, the surviving store must return the original payment outcome (or a documented conflict), not a second authorize. Secrets stay `BAYPAY_DB_*` from a **planned** replica of the secret / `alias/baypay-payments` — paper only; do not create a second key in the lab. Module 13 log/metric rules still apply: do not put the key on a metric label.

## Do not fail over

- `BayPayCell`, `dmgr-east`, `PaymentCluster`, IHS/`payment.ear` — decommission, not a bunker.
- Student `terraform apply` in `us-east-1`.
- NAT, EKS, multi-AZ RDS apply “to rehearse.”
- Disable TLS “because DR.”
- Flip Route 53 on hope before the secondary can serve `:8080` + Actuator + a valid leaf.

## First 60 minutes (acceptable runbook)

1. Priya declares regional SEV; Riley owns app comms; Sam owns platform inventory (what exists on paper in `us-east-1`); Jordan does **not** merge a DNS flip yet.
2. Merchant success: handshake/5xx vs “we are in a regional tabletop / incident”; Avery retries are expected.
3. Confirm `us-west-2` is actually gone (not INCIDENT-1402 TLS, not a single-AZ blip). Identity/TLS in-region is ARCHITECT-1401 / INCIDENT-1402, not this page.
4. If a paper pilot/warm path exists: start compute, check readiness, check a **planned** leaf for the teaching host, *then* talk DNS.
5. Do not bounce leftover ND. Do not invent a second DNS zone.

## 99.99% versus DR

ARCHITECT-1401: in-region four nines can be multi-AZ single-region (~52 minutes/year). This page: the **region** is gone — RTO/RPO. Do not silently rewrite the Module 13 SLO to 99.99%. A 60-minute regional event **blows** the four-nines year; that is why DR is a separate contract.

## Diagram

AEJE-D-066: `us-west-2` crossed out; paper `us-east-1` pilot/warm; `BayPayCell` marked not a target.

## Scoring notes

Full marks require split workloads, a named pattern with losers, idempotency for `c1402b22-…1402`, and an explicit ND refusal. “Apply us-east-1” or “fail over to dmgr-east” caps Production awareness at 1.
