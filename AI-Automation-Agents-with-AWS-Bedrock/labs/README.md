# Course Labs — AWS Bedrock (Runnable on AWS)

Production-minded labs for **AI Automation & Agents with AWS Bedrock**. Week 1 includes local scripts; **Weeks 2–8** deploy to AWS via **AWS SAM** (Lambda, API Gateway, Step Functions, DynamoDB, CloudWatch).

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| AWS account | Sandbox or learner account with billing alerts |
| [Bedrock model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) | Enable **Amazon Nova Lite** (`amazon.nova-lite-v1:0`, default) or change `BedrockModelId` |
| AWS CLI v2 | `aws sts get-caller-identity` |
| [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) | For deploy (Weeks 2–8); install via `pip install -r requirements-dev.txt` |
| Python 3.11+ | Local scripts and tests |
| IAM permissions | CloudFormation, Lambda, API Gateway, Step Functions, DynamoDB, IAM, Bedrock, CloudWatch |

## Quick start

```bash
cd labs
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt

export AWS_REGION=us-east-1
export PROJECT_PREFIX=ba-la8s-ai-yourname
export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0

# One-time setup (optional helper)
./scripts/labs.sh setup

# SAFE FIRST RUN — test everything, auto-delete stack (no leftover cost)
./scripts/labs.sh cycle

# Daily workflow — start when working, stop when done
./scripts/labs.sh start      # deploy (~2–3 min) — COST while running
source .stack.env            # load API_ENDPOINT, ARNs
./scripts/labs.sh stop       # DELETE stack — STOP charges
```

### Unified control (`labs.sh`)

| Command | Cost | Action |
|---------|------|--------|
| `./scripts/labs.sh setup` | Free | Local venv + pip |
| `./scripts/labs.sh start` | **While up** | Deploy / update stack |
| `./scripts/labs.sh stop` | **Stops stack charges** | Delete entire stack |
| `./scripts/labs.sh restart` | While up | stop + start |
| `./scripts/labs.sh status` | Free | Check running or stopped |
| `./scripts/labs.sh test` | Free | Unit tests only |
| `./scripts/labs.sh verify` | Per invoke | Integration tests (stack up) |
| `./scripts/labs.sh verify-capstone` | Per invoke | Week 8 capstone tests |
| `./scripts/labs.sh cycle` | Brief | test → deploy → verify → **auto-stop** |

See **[COST_CONTROL.md](COST_CONTROL.md)** for billing details.

### Start / Stop cycle (cost control)

| Script | Action |
|--------|--------|
| `./scripts/start.sh` | Deploy CloudFormation stack |
| `./scripts/stop.sh` or `./scripts/teardown.sh` | **Delete entire stack** (stops charges) |
| `./scripts/cycle.sh` | Unit + integration + capstone tests, then **auto-teardown** |
| `./scripts/run-tests.sh` | Local pytest only (free) |
| `./scripts/status.sh` | Show whether stack is up |

```bash
# One command: test everything and tear down (recommended first run)
PROJECT_PREFIX=ba-la8s-ai-yourname ./scripts/labs.sh cycle

# Keep stack running after tests (you will incur storage/API costs)
./scripts/labs.sh cycle --keep-stack
```

## What gets deployed

| Resource | Labs |
|----------|------|
| Lambda (Bedrock invoke) | Week 2 |
| Lambda (classify, route, validate, persist, API, agent) | Weeks 3–7 |
| API Gateway HTTP API | Week 5 (`/classify`, `/summarize`, `/route`) |
| Step Functions state machine | Week 4 |
| DynamoDB (audit, memory, results) | Weeks 6–7 |
| CloudWatch dashboard + alarm | Week 6 |

Stack outputs appear after deploy (`ApiEndpoint`, `StateMachineArn`, table names).

### Student lab diagrams

- **Deploy cycle:** [lab-deploy-cycle](../diagrams/student/png/lab-deploy-cycle.png) — what `cycle.sh` does
- **Console checkpoints:** [lab-console-checkpoints](../diagrams/student/png/lab-console-checkpoints.png) — where to look after deploy

## Lab index

| Week | Folder | Type |
|------|--------|------|
| 1 | `week01/` | Local Python → Bedrock |
| 2 | `week02/` | Local eval + Lambda |
| 3 | `week03/` | Lambda classify/route + unit tests |
| 4 | `week04/` | Step Functions + validate/persist |
| 5 | `week05/` | HTTP API |
| 6 | `week06/` | Audit query + dashboard (in stack) |
| 7 | `week07/` | Agent Lambda + memory |
| 8 | `week08/` | **Capstone** — 4 student project tracks (see below) |

Each week folder has a `README.md` with lab-specific commands.

### Week 8 Capstone (4 options)

Deploy with the main stack — no separate deploy needed:

| Option | API | Docs |
|--------|-----|------|
| A — Incident triage | `POST /capstone/incident` | [`week08/option_a_incident_triage/`](week08/option_a_incident_triage/README.md) |
| B — Doc classification | `POST /capstone/document` | [`week08/option_b_doc_classification/`](week08/option_b_doc_classification/README.md) |
| C — Approval workflow | `POST /capstone/approval/*` | [`week08/option_c_approval_workflow/`](week08/option_c_approval_workflow/README.md) |
| D — Enterprise agent | `POST /capstone/agent` | [`week08/option_d_enterprise_agent/`](week08/option_d_enterprise_agent/README.md) |

```bash
./scripts/verify-capstone.sh   # after ./scripts/start.sh
```

## Configuration

| Variable | Default | Description |
|----------|---------|-------------|
| `AWS_REGION` | `us-east-1` | Bedrock + deploy region |
| `BEDROCK_MODEL_ID` | `amazon.nova-lite-v1:0` | Foundation model (Converse API) |
| `PROJECT_PREFIX` | `ba-la8s-ai` | Resource naming prefix |
| `CONFIDENCE_THRESHOLD` | `0.65` | Low-confidence → `human_review` |

### Alternate models

If Claude is not enabled, deploy with Amazon Titan (example):

```bash
export BEDROCK_MODEL_ID=amazon.titan-text-lite-v1
./scripts/deploy.sh
```

> Titan uses a different request format. This course defaults to the **Bedrock Converse API** (Claude, etc.). For Titan-only accounts, use Converse-compatible models or adapt `common/bedrock_client.py`.

## Unit tests (no AWS required)

```bash
source .venv/bin/activate
pytest tests/ -v
```

## Tear down

```bash
./scripts/labs.sh stop
# or
./scripts/stop.sh
```

Deletes stack `{PROJECT_PREFIX}-course-labs`. **This is the only way to stop ongoing charges** for Lambda, API Gateway, DynamoDB, and Step Functions.

See [COST_CONTROL.md](COST_CONTROL.md) for full billing guide.

## Troubleshooting

| Issue | Fix |
|-------|-----|
| `AccessDeniedException` on Bedrock | Enable model access in Bedrock console for your region |
| Lambda works locally but not in AWS | Check region, execution role, and `BEDROCK_MODEL_ID` env var |
| Empty audit query | Set `AUDIT_TABLE_NAME` or run after API/Lambda calls |
| Step Functions fails at Classify | Check CloudWatch logs for `${ProjectPrefix}-classify` |
| API 403/429 | HTTP API throttling (20 burst / 10 rps) — retry with backoff |

## Shared library

- `common/bedrock_client.py` — Converse API + retries
- `common/validation.py` — JSON schema validation + fallbacks
- `common/audit.py` — DynamoDB audit events (metadata only)
- `common/memory.py` — Session memory with TTL

See also: `../LABS_GUIDE.md` (acceptance criteria), `../weeks/` (weekly lesson modules).
