# SECURITY-1404 — Instructor solution

**Do not share this file with students before they submit the threat-model section.**

The compact scope box in the student lab is a *post-attempt* check. It is not the scored STRIDE table. Generic OWASP with no BayPay names must not outscore a page that names `/api/v1/payments`, frozen `…222`, and `alias/baypay-payments`.

**Do not** grade exploit steps, payloads, or malware language as extra credit. Those fail Security / reliability.

Out of scope stays out of scope: real PCI ROC, live attacks, applying KMS/ACM/RDS, `PaymentCluster` as the model.

## Acceptable STRIDE (architecture notes only)

| Surface | S | T | R | I | D | E |
|---|---|---|---|---|---|---|
| `POST /api/v1/payments` | Spoofed merchant / stolen session cookie — TLS + app auth (teaching) | Amount/body tamper in transit — edge TLS; server-side amount rules | Denied authorize with no `paymentId` / `correlationId` in logs | PAN or account id in logs/metrics — **forbidden** (TRUST + OBSERVABILITY) | Flood of creates — rate/size limits; thread + Hikari saturation (Module 13) | Task role `AdministratorAccess` — SECURITY-1103 split |
| `GET /api/v1/payments/{id}` | IDOR: Avery reads another customer’s id — authorize on customer `11111111-…1111` | Rewrite id in transit — TLS | Missing audit on reads of settlement-sensitive rows | Payment body leaking PAN — do not persist PAN | Enumerate ids — no sequential ids; teaching UUIDs | Internal GET that skips auth because “same JVM” |
| `POST/GET /api/v1/refunds` | Refund for a payment Avery does not own | Tamper refund amount | Refund with no actor in logs | Refund reason containing account numbers | Refund flood against one payment | Refunds module calls “internal authorize” |
| `Idempotency-Key` | Captured key presented as another merchant — bind key to caller + body hash | Same key, different body — **conflict**, do not silently replace | No record of which key produced `c1402b22-…1402` | Key on a **metric label** — cardinality + leak | Replay storm of the same key — store absorbs; do not open extra authorizes | Forged key that maps to another tenant’s store |
| Frozen `…222` | Actor claims the account is active | Bypass flag in a request field | No log when frozen is refused | Frozen flag as a high-cardinality label | Retry storms on a frozen account | **Internal module path** that skips accounts |
| Secrets / IAM | Stolen task-role creds | Swap secret ARN in task def | No CloudTrail on `GetSecretValue` (execution role) | `BAYPAY_DB_PASSWORD` in git / task JSON | Secret API throttling at deploy | Execution role = task role = admin |
| Edge TLS | Fake payments host (phishing) — not solved by BayPay TLS alone | Strip TLS / HTTP downgrade | No inventory of which leaf the ALB presents | Leaf + key in a ticket | Handshake failures = merchant outage (identity domain) | Listener opened HTTP “for DR” |
| Modular monolith | One module trusts another’s “already checked” flag | Cross-module write to ledger without accounts | Module-internal calls with no `correlationId` | Shared heap dumps containing secrets | One module saturates the one JVM | Refunds → payments “private” authorize |

Students need not fill every cell at this density. They **must** hit all eight surfaces with at least one honest threat + control + gap. Equivalent methods (LINDDUN lite, a custom “threat / control / gap” table) are acceptable if named.

## Idempotency (acceptable paragraph)

Same key + same body: return the original payment (`c1402b22-0000-4000-8000-111111111402` as teaching id), do not authorize twice. Same key + different body: conflict (4xx), do not overwrite. Client retry after timeout is the **intended** use (Avery). A captured key is a **spoofing / replay** threat: bind the key to the authenticated caller and a body hash; keep it off metric labels; store it with the ledger intent. Do **not** write how to capture or replay a key.

## Frozen account (acceptable paragraph)

Account `22222222-2222-2222-2222-222222222222` must not authorize. The **accounts** module is the source of truth. Payments **and** refunds call it. An “internal” shortcut that skips frozen is elevation of privilege inside the monolith. Riley’s 02:00 question is answered: hurry is not a bypass. Log `outcome` without putting `accountId` on Prometheus labels.

## Secrets / IAM (acceptable)

Execution role pulls ECR, logs, **one** secret, **one** CMK (`alias/baypay-payments`). Task role is the JVM — no `GetSecretValue` unless the app calls the API (it does not). No `AdministratorAccess`. No `changeme`. Compromised JVM + admin task role = account compromise. Paper JSON is enough; do not apply.

## Edge TLS (acceptable)

Merchants handshake at `payments.apps.baypay.example`. Jump-box HTTP `:8080` is operator evidence, not a customer control. Ticket ≤ 30 days, page ≤ 7 days. Do not disable TLS. Do not paste INCIDENT-1402 instructor RCA; students may cite **their** worksheet quotes only.

## Modular monolith boundary (acceptable)

| From | May | Must not |
|---|---|---|
| Payments | Accounts (frozen), idempotency store, ledger write | Raw SQL that skips frozen; issue refunds without refund rules |
| Refunds | Accounts, original payment lookup, idempotency | “Internal authorize”; mutate another customer’s payment |
| Accounts | Frozen/active flag for `…221` / `…222` | Trust a client-supplied “not frozen” boolean |
| One JVM | Shared process, shared deploy | Shared “already authenticated” without a call |

Extracting refunds later **adds** a network trust boundary; it does not remove the frozen check.

## Refusals

No prod scanner as the lab path. No exploit PoC. No PAN storage. No `PaymentCluster` security design. No KMS/ACM/RDS/`us-east-1` apply.

## Diagram

AEJE-D-067: TLS edge → ALB → modular monolith (payments, refunds, accounts, idempotency) → secrets/KMS and teaching Postgres without PAN.

## Scoring notes

Full marks require named BayPay surfaces, idempotency + frozen paragraphs, IAM split, edge TLS as a boundary, and a module table. Exploit language caps Security / reliability at 1. `PaymentCluster` as the model caps Technical accuracy at 3 or below.
