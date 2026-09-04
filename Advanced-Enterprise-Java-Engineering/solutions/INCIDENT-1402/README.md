# INCIDENT-1402 — Instructor solution

**Do not share this file with students before they submit a worksheet.**

## RCA

The leaf ACM certificate for `payments.apps.baypay.example` **expired 2026-09-01 00:00 UTC** (`notAfter` on the handshake paste; ALB still presents `certificate/e1402a11-…`, status **EXPIRED**, `InUse: true`). Merchants fail the TLS handshake (`openssl` verify error 10; `curl: (60)`). ECS tasks remain **RUNNING**. HTTP to task `:8080` from the jump box returns Actuator **200**.

A replacement ACM certificate (`certificate/p1402b22-…`) is **PENDING_VALIDATION** (not **ISSUED**) because the Route 53 DNS validation CNAME **`_2f91d4c0.payments.apps.baypay.example`** (`_acm` / `_abc.payments` teaching name) is **missing** (`NXDOMAIN`; not in the zone list). Jordan Voss and Sam Okada removed it in ticket **BAYPAY-14021** (“cleanup unused records,” 2026-08-12). Other records remain (payments ALIAS to the ALB, `_health` TXT).

This is **not** INC-K8S-1005: that pack was Ingress Secret `payment-tls` with **wrong CN** (`*.baypay.internal`) **and** an expired kube-managed leaf. This pack is **edge TLS / ACM / DNS validation**. CN on the expired leaf **matches** `payments.apps.baypay.example`. Do not collapse the two into “TLS is broken.”

This is **not** a security-group drop (TCP to :443 completed). This is **not** Postgres. This is **not** an empty target group (tasks RUNNING; `:8080` answers).

A lucky guess “the cert expired” **without** quoting **ACM status (`PENDING_VALIDATION` or `FAILED`, not `ISSUED`)** **and** the **missing validation CNAME** must **not** max Diagnostic method.

## Differentiation from INC-K8S-1005 (instructor only)

| | INC-K8S-1005 | INC-SEC-1402 |
|---|---|---|
| Estate | OpenShift/Kubernetes Ingress | ALB + ACM in `us-west-2` |
| Object | Secret `payment-tls` | ACM certificates + Route 53 zone `baypay.example` |
| Name mismatch | CN `*.baypay.internal` vs host | CN **matches** the payments host |
| Why renewal failed | Calendar spreadsheet; no cert-manager | Validation CNAME removed in BAYPAY-14021 |
| Evidence | ingress.yaml, openssl-dates, curl-tls | tls-handshake, acm-describe, route53-records |

Students who import `payment-tls` or “wrong SAN” as the RCA are on the Module 10 story. Score Technical accuracy down unless they contrast this pack’s ACM status and NXDOMAIN.

## Stabilization

1. Restore HTTPS on `payments.apps.baypay.example` **:443**. Prefer attaching the **last still-valid** ACM certificate if one remains in the account; in this pack the in-use leaf is already **EXPIRED**, so **re-create the DNS validation CNAME** `_2f91d4c0.payments.apps.baypay.example` → `_7c3a1e9f4d2b.acm-validations.aws.`, wait for the replacement cert to leave **PENDING_VALIDATION**, then attach `certificate/p1402b22-…` (or a newly issued cert) to the ALB listener.
2. Confirm merchants complete the handshake; retest Avery’s POST path. Jump-box `:8080` was never the customer check.
3. Do **not** disable TLS on the listener.
4. Do not bounce Postgres or `dmgr-east`.
5. Do not open 443 to a wider security group “so TLS works.”
6. Do not bounce healthy tasks.

## Remediation

- Restore the ACM DNS validation record **as code** (Terraform `aws_route53_record` keyed to the ACM `domain_validation_options` CNAME). Never “cleanup unused CNAMEs” without an **ACM inventory**.
- Change-control on the `baypay.example` hosted zone (ticket + plan showing ACM `ResourceRecord` names you will keep).
- Expiry **ticket at ≤ 30 days**, **page at ≤ 7 days** (TRUST.md). The page on 2026-09-02 was already past both windows.
- Prefer ACM automatic renewal only after validation records are durable; alert on `PENDING_VALIDATION` / `FAILED`, not only on `EXPIRED`.
- Least privilege: `acm:Describe*`, `route53:List*`, listener update — not `AdministratorAccess`.

## Evidence students should have used

| Gate | What it shows |
|---|---|
| tls-handshake.txt | `notAfter=Sep  1 00:00:00 2026 GMT`; verify error expired; `curl: (60)`; jump-box `:8080` **200**; no HTTP from Spring |
| acm-describe.txt | Replacement **PENDING_VALIDATION**; in-use leaf **EXPIRED**; **not ISSUED**; validation `ResourceRecord` name `_2f91d4c0.payments.apps.baypay.example` |
| route53-records.txt | payments ALIAS **present**; `_2f91d4c0…` **NXDOMAIN** / absent from the list |

A worksheet that says only “expired cert” without ACM status and the missing validation name scores poorly on Diagnostic method even if the catalog title matches.

## Comms (acceptable example)

SEV-2 on `payments.apps.baypay.example`. Merchants fail the TLS handshake. Tasks remain RUNNING and HTTP on :8080 answers. The leaf on the ALB is expired and ACM shows the replacement still pending validation; the validation name is not in Route 53. We are restoring HTTPS. We are not turning TLS off and not bouncing the database. Next update 20 minutes.

## Diagram

AEJE-D-065: merchants HTTPS → ALB/ACM leaf → handshake fail; tasks RUNNING on :8080.
