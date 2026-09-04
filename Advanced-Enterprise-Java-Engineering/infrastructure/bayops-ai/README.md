# BayOps AI — teaching prototype (stubs)

**Not a production service. Not a required AWS apply.**

This folder is the Module 15 sketch: a JSON **output contract**, fixtures used by AI-1501–1504, and a paper architecture (AEJE-D-069). Students pass by writing files that match [schema/output.schema.json](schema/output.schema.json). Amazon Bedrock is optional extra credit.

## Allowed AWS sketch (paper)

`us-west-2`. Short-lived. Tags `Course=AEJE`, `Module=15`, `Lab`, `Environment=student`, `Expiration`.

| Piece | Teaching role |
|---|---|
| API Gateway | HTTPS entry for “summarize this pack” |
| Lambda | Orchestrates retrieve → prompt → validate schema |
| S3 | Synthetic evidence objects (never PAN) |
| DynamoDB | Incident id + approval record |
| Bedrock | Optional model; fixtures replace it in class |
| CloudWatch | Invocation logs — not a substitute for traces |

Do **not** apply NAT, EKS, OpenSearch, or a provisioned Bedrock throughput lab “for realism.” Prefer paper + JSON. If someone applies, destroy the same day. Estimate before apply; idle API Gateway and DynamoDB still bill.

## Contract

Every response must contain **Evidence**, **Hypotheses** (`status=unproven`), **Recommended investigation**, **Suggested remediation** with `approvalRequired=true`, and `humanApproval`.

Never emit a proven RCA field. Never auto-approve.

## Fixtures

| File | Lab |
|---|---|
| [fixtures/ai-1501-mixed-summary.json](fixtures/ai-1501-mixed-summary.json) | Starter (bad mix) — students rewrite |
| [fixtures/ai-1504-hallucination.json](fixtures/ai-1504-hallucination.json) | Planted unsupported diagnosis |

Instructor-good outputs live under `solutions/AI-150N/`, not here.
