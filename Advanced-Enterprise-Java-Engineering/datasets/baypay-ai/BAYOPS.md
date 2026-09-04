# BayOps AI notes — Module 15

**Fictional company. Synthetic operational data only.** Students may read this file. Instructor lab answers live only under `solutions/`.

BayOps AI is a **teaching prototype**, not a production SRE product and not a live Bedrock requirement. The grade bar is **method**: separate the four output buckets, refuse an uncited “proven RCA,” and require a **human approval** before any remediation that mutates prod.

## Defaults

| Field | Value |
|---|---|
| App | `payment-service` (Java 21, Spring Boot 3.5.5) |
| Region (when AWS is named) | `us-west-2` |
| Port / health | `8080` / `/actuator/health/liveness`, `/actuator/health/readiness` |
| Golden request | `POST /api/v1/payments` with `Idempotency-Key` |
| Data | Synthetic timelines, logs, and metrics only — no real merchant traffic, no PAN |
| Live model | **Not required.** Paper fixtures + the JSON contract are enough to pass. |
| Allowed AWS *sketch* | Amazon Bedrock, Lambda, S3, DynamoDB, API Gateway, CloudWatch — short-lived, tagged, destroy-after-lab if anyone applies |
| Do not apply | NAT Gateway, EKS, OpenSearch, always-on GPU, multi-AZ RDS “for the demo” |

## Output contract (mandatory)

Every BayOps response — human or model — must use **four labeled sections**. Never collapse them into “Root cause: …”.

| Section | What it may contain | What it must not do |
|---|---|---|
| **Evidence** | Quotes from files the operator opened (path, timestamp, text) | Invent a file, a metric, or a host |
| **Hypotheses** | Ranked, *unproven* explanations that fit the evidence so far | Mark one as proven / RCA / “confirmed” |
| **Recommended investigation** | The *next* gate or omitted evidence kind, and why | Skip to bounce / apply / force-push |
| **Suggested remediation** | Stabilize then remediations, each needing **human approval** | Auto-execute, auto-rollback, or disable TLS |

A fifth field is required on any mutating suggestion:

| Field | Value |
|---|---|
| `humanApproval` | `pending` until Riley Okonkwo or Priya Nair (or the student playing on-call) writes `approved` or `rejected` with a name and time |

Schema on disk: [infrastructure/bayops-ai/schema/output.schema.json](../../infrastructure/bayops-ai/schema/output.schema.json).

## People and demo identities (synthetic)

Same as [../baypay-ops/OBSERVABILITY.md](../baypay-ops/OBSERVABILITY.md): Avery Chen `11111111-1111-1111-1111-111111111111`, active account `…221`, Riley Okonkwo, Priya Nair, Sam Okada, Jordan Voss, Morgan Hale.

Example payment id for AI labs: `c1501d33-0000-4000-8000-111111111501`.

## What you must not do

- Call a model output a **proven root cause** without a quoted file.
- Send PAN, `BAYPAY_DB_PASSWORD`, or live access keys to a model (or into a fixture).
- Auto-approve a runbook that bounces `dmgr-east`, Postgres, or disables TLS.
- Require a Bedrock API key or `terraform apply` to pass a lab.
- Put instructor answers for AI-1501–1504 in this file.

## Optional PAKS

- `docs/23-agentic-ai-architecture/agent-governance-and-safety.md`
