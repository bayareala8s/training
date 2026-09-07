# INC-SEC-1402 student worksheet

Fill in order. Quote evidence. Do not paste instructor solutions.

**Incident:** HTTPS handshake failures while payment tasks stay RUNNING  
**Region:** `us-west-2`  
**Cluster / service:** `baypay-prod-west` / `payment-service`  
**Host:** `payments.apps.baypay.example`  
**Your name / cohort:**  
**Time started:** 2026-09-07  
**Time submitted:** 2026-09-07

## Current hypothesis

(What do you think is happening? Update after each gate.)

Gate 1: Merchants fail **HTTPS verify** on `payments.apps.baypay.example:443`. Leaf CN matches the host; **`notAfter=Sep 1 00:00:00 2026 GMT`**; openssl `verify error:num=10:certificate has expired`; curl **(60)**. TCP completed — not a security-group drop. Jump-box HTTP `10.0.14.22:8080` liveness **200**; GET `/api/v1/payments` **405**. Tasks RUNNING 2/2. Avery `c1402b22-…-111402` never left the browser — no Spring status. This is the identity/TLS domain, not Postgres and not Actuator. “Expired leaf” is a handshake fact, not a closed RCA: I still need **ACM status** (ISSUED vs failed renewal) after Sam’s Aug 12 DNS cleanup.

Gate 2: Lucky “expired cert” is incomplete. ACM has **no ISSUED** row for `payments.apps.baypay.example`. ALB `:443` still presents **`e1402a11-…-aaaaaaaa1402`** — **Status `EXPIRED`**, **`InUse: true`**, `NotAfter=2026-09-01T00:00:00Z` (matches handshake). Replacement **`p1402b22-…-bbbbbbbb1402`** is **`PENDING_VALIDATION`**, `InUse: false`, `IssuedAt: null`, created 2026-08-28. DNS validation wants CNAME **`_2f91d4c0.payments.apps.baypay.example.`** → **`_7c3a1e9f4d2b.acm-validations.aws.`**. Renewal never finished. Next: does that name exist after Sam’s Aug 12 “unused records” cleanup?

Gate 3: **Validation CNAME is gone.** Hosted zone `baypay.example` still has the merchant **A ALIAS** `payments.apps.baypay.example` → `pay-alb-prod-1402.us-west-2.elb.amazonaws.com` (Sam was right about the public name). `_health.payments` TXT is present. **`_2f91d4c0.payments.apps.baypay.example` CNAME is not in the zone**; `dig` → **NXDOMAIN**. No other `_*.payments` CNAMEs. BAYPAY-14021 deleted names that “nothing resolved” — that was the ACM validation record. New cert stays PENDING_VALIDATION; ALB keeps presenting EXPIRED. Every AZ can be up and the 52-minute year is still spent.

## Supporting evidence

Gate 1 — `evidence/tls-handshake.txt` (2026-09-02T07:20:18Z):
- `CN = payments.apps.baypay.example`; issuer Amazon Server CA 1B
- `notBefore=Jun 3 00:00:00 2026 GMT`; `notAfter=Sep 1 00:00:00 2026 GMT` (90-day leaf)
- `verify error:num=10:certificate has expired`
- `curl: (60) SSL certificate problem: certificate has expired` — HTTP status never returned
- Jump box: `http://10.0.14.22:8080/actuator/health/liveness` → **200**; same host GET payments → **405**
- Timeline: leaf reached notAfter 2026-09-01T00:00Z; **no page overnight**. Tasks RUNNING. Sam: leftover names that “nothing resolved” removed 2026-08-12.

Gate 2 — `evidence/acm-describe.txt` (2026-09-02T07:24:11Z, `us-west-2`):
- Domain **`payments.apps.baypay.example`**: Status **`PENDING_VALIDATION`** (`p1402b22-…`, InUse false) and **`EXPIRED`** (`e1402a11-…`, InUse true). No **ISSUED**.
- Validation: method **DNS**, `ValidationStatus: PENDING_VALIDATION`, ResourceRecord **`_2f91d4c0.payments.apps.baypay.example.` CNAME `_7c3a1e9f4d2b.acm-validations.aws.`**
- ALB listener `:443` still presents the EXPIRED ARN.

Gate 3 — `evidence/route53-records.txt` (2026-09-02T07:28:44Z, zone `Z1402BAYPAYEXAMPLE`):
- Present: `payments.apps.baypay.example.` **A ALIAS** → `pay-alb-prod-1402.us-west-2.elb.amazonaws.com.`
- Present: `_health.payments.apps.baypay.example.` TXT `"baypay-prod-west"`
- **Not present / NXDOMAIN:** `_2f91d4c0.payments.apps.baypay.example.` CNAME. No other `_*.payments` CNAMEs.

Optional literacy: INC-K8S-1005 was a **cluster Secret** hostname/expiry. This pack is **edge ACM + DNS validation**. Do not collapse them.

## Next investigation

Gates used in order. If I still wanted an omitted kind: ECS describe would only restate RUNNING 2/2; security-group describe would not explain a completed TCP + verify fail. Application logs omitted — handshake never reached Spring. Do not invent a cluster TLS Secret. Do not request ACM or change Route 53 in a paid account.

## Stabilization action

Restore merchant HTTPS on **`:443`**, not HTTP. Put the ACM validation CNAME back (`_2f91d4c0.payments.apps.baypay.example` → `_7c3a1e9f4d2b.acm-validations.aws.`), wait for **`p1402b22-…` → ISSUED**, attach that ARN on the ALB listener. There is **no last-valid ISSUED** cert to swap immediately — only EXPIRED InUse. Do **not** disable TLS on the listener. Do **not** bounce Postgres, `dmgr-east`, or “fix” a security group. Do not scale tasks. Do not apply a second region.

## Remediation

DNS **as code**: validation CNAMEs live in Terraform / the zone inventory; BAYPAY-14021-style “delete names that nothing resolves” is change-control with an ACM `DomainValidationOptions` check first. TRUST.md alerts: **ticket ≤ 30 days, page ≤ 7 days** — none fired (leaf died Sep 1, page Sep 2). Calendar reminder is not a page. Least privilege for on-call: `acm:DescribeCertificate`, `route53:ListResourceRecordSets` — not `AdministratorAccess`.

## Communication update

SEV-2 `payments.apps.baypay.example`: Harbor Market fails HTTPS (curl 60, expired leaf `notAfter=Sep 1`). Tasks RUNNING 2/2; jump-box `:8080` liveness 200 — we are not bouncing Postgres or `dmgr-east` and we are not turning TLS off. ACM: ALB still presents **EXPIRED** (`InUse true`); replacement **PENDING_VALIDATION**. Route 53: merchant ALIAS to the ALB is present; validation CNAME `_2f91d4c0.payments…` is **NXDOMAIN** after the Aug 12 cleanup. Stabilizing by restoring that CNAME and attaching the issued leaf on `:443`. Avery `c1402b22-…-111402` never left the browser.
