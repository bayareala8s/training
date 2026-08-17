# Lab Cost Control — Start / Stop Guide

AWS labs **incur charges only while the stack is deployed** and when you **invoke Bedrock**. There is no "pause" mode — you **delete the stack** to stop charges.

## Quick reference

| Command | AWS cost? | What it does |
|---------|-----------|--------------|
| `./scripts/labs.sh setup` | **No** | Local venv + dependencies |
| `./scripts/labs.sh test` | **No** | Pytest only (18 tests) |
| `./scripts/labs.sh start` | **Yes** (while up) | Deploy all Weeks 2–8 resources |
| `./scripts/labs.sh stop` | **Stops charges** | Delete entire CloudFormation stack |
| `./scripts/labs.sh status` | **No** | Check if stack is up or stopped |
| `./scripts/labs.sh cycle` | **Brief** | test → deploy → verify → **auto-stop** |
| `./scripts/labs.sh restart` | **Yes** (while up) | stop + start (clean redeploy) |

## Recommended workflow

### First time (validate everything, zero leftover cost)

```bash
cd labs
export AWS_REGION=us-east-1
export PROJECT_PREFIX=ba-la8s-ai-yourname
export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0

./scripts/labs.sh setup
./scripts/labs.sh cycle          # auto-deletes stack when done (~5–8 min)
```

### Daily lab / video recording session

```bash
cd labs
source .venv/bin/activate
export PROJECT_PREFIX=ba-la8s-ai-yourname

./scripts/labs.sh start          # deploy (~2–3 min)
source .stack.env                # load API_ENDPOINT, ARNs, etc.

# ... run labs, record demos ...

./scripts/labs.sh stop           # DELETE stack — stop charges (~2–3 min)
```

### Check before leaving for the day

```bash
./scripts/labs.sh status
```

If status shows `CREATE_COMPLETE` or `UPDATE_COMPLETE`, run `./scripts/labs.sh stop`.

## What gets deleted on `stop`

The entire SAM stack is removed:

- All Lambda functions (Weeks 2–8 + capstone)
- API Gateway HTTP API
- Step Functions state machines (Lab 4 + capstone)
- DynamoDB tables (audit, memory, results, approvals)
- CloudWatch dashboard + alarms
- IAM roles created by the stack

**Not deleted:** SAM deployment artifacts in the managed S3 bucket (minimal storage cost). Bedrock model access settings in your account.

## What still costs money (even when stopped)

| Item | When charged |
|------|--------------|
| Bedrock invokes | Only when you call models (during labs) |
| SAM S3 artifacts | Tiny storage in `aws-sam-cli-managed-*` bucket |
| CloudWatch Logs | Retained logs from past runs (if any) — delete log groups manually if needed |

## Environment variables

```bash
export AWS_REGION=us-east-1
export PROJECT_PREFIX=ba-la8s-ai-yourname   # unique per student/team
export BEDROCK_MODEL_ID=amazon.nova-lite-v1:0
```

Stack name: `{PROJECT_PREFIX}-course-labs`

After `start`, load outputs:

```bash
source .stack.env
echo $API_ENDPOINT
```

## Troubleshooting

| Problem | Fix |
|---------|-----|
| Stack stuck deleting | Wait 5 min; check CloudFormation console |
| `stop` says not found | Already stopped — no charges |
| Accidentally left stack up | `./scripts/labs.sh stop` |
| Multiple stacks | Use unique `PROJECT_PREFIX` per person |
| SAM bucket clutter | `sam delete --stack-name ... --resolve-s3` (stop.sh does this) |

## Billing alerts (recommended)

1. AWS Billing → **Budgets** → create alert at $5 / $10
2. Use a **sandbox account** for students when possible
3. Always run `./scripts/labs.sh cycle` before teaching to confirm teardown works
