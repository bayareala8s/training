# Course Labs — AWS Bedrock (Runnable on AWS)

Production-minded labs for **AI Automation & Agents with AWS Bedrock**. Weeks 1–2 include local scripts; Weeks 2–7 deploy to AWS via **AWS SAM** (Lambda, API Gateway, Step Functions, DynamoDB, CloudWatch).

## Prerequisites

| Requirement | Notes |
|-------------|--------|
| AWS account | Sandbox or learner account with billing alerts |
| [Bedrock model access](https://docs.aws.amazon.com/bedrock/latest/userguide/model-access.html) | Enable **Claude 3 Haiku** (default) or change `BedrockModelId` |
| AWS CLI v2 | `aws sts get-caller-identity` |
| [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/install-sam-cli.html) | For deploy (Weeks 2–7) |
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

# Week 1 (local Bedrock)
python week01/invoke_bedrock.py

# Full cycle: unit tests → deploy → AWS integration tests → teardown (recommended)
./scripts/cycle.sh

# Or manual start/stop
./scripts/start.sh    # deploy stack
./scripts/verify.sh   # integration checks
./scripts/stop.sh     # delete stack (avoid ongoing cost)
```

### Start / Stop cycle (cost control)

| Script | Action |
|--------|--------|
| `./scripts/start.sh` | Deploy CloudFormation stack |
| `./scripts/stop.sh` or `./scripts/teardown.sh` | **Delete entire stack** (stops charges for these resources) |
| `./scripts/cycle.sh` | Run unit + integration tests, then **auto-teardown** |
| `./scripts/run-tests.sh` | Local pytest only (free) |
| `./scripts/status.sh` | Show whether stack is up |

```bash
# One command: test everything and tear down
PROJECT_PREFIX=ba-la8s-ai-yourname ./scripts/cycle.sh

# Keep stack running after tests (you will incur storage/API costs)
./scripts/cycle.sh --keep-stack
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
| 8 | Capstone | Extend this stack — see `CAPSTONE_HANDBOOK.md` |

Each week folder has a `README.md` with lab-specific commands.

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
sam delete --stack-name "${PROJECT_PREFIX}-course-labs" --region "$AWS_REGION"
```

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
