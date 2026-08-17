# Lab 2.2: EventBridge Scheduled API Ingestion

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-2.2-eventbridge-automation.drawio)](../../../../docs/diagrams/drawio/lab-2.2-eventbridge-automation.drawio) · [PNG](../../../../docs/diagrams/png/lab-2.2-eventbridge-automation.png) · [SVG](../../../../docs/diagrams/svg/lab-2.2-eventbridge-automation.svg)

**Estimated time:** 90 minutes · **Module 2**

---

## Objectives

- Schedule recurring ingestion with Amazon EventBridge rules
- Fetch external API data from Lambda and land snapshots in S3
- Maintain ingestion watermarks in the metadata zone
- Monitor scheduled runs in CloudWatch Logs

---

## Prerequisites

- Lab 2.1 concepts understood (Lambda + S3 raw writes)
- S3 data lake bucket from Module 1
- Lambda outbound internet access (default; no VPC required for this lab)

---


## Platform Setup

From the **repository root**, start the shared lab environment (once per session):

```bash
./scripts/lab-cycle.sh start
source ./scripts/lab-env.sh
```

Stop when finished: `./scripts/lab-cycle.sh stop --yes` (avoids ongoing AWS charges).

---


## Architecture

```mermaid
flowchart TB
    EB[EventBridge Rule<br/>rate(15 minutes)]
    L[Lambda: scheduled_ingestion.py]
    API[JSONPlaceholder API]
    RAW[(S3 raw/api-ingest/posts/)]
    WM[(S3 metadata/watermarks/)]
    CW[CloudWatch Logs]

    EB -->|Invoke| L
    L -->|HTTPS GET| API
    L -->|PutObject snapshot| RAW
    L -->|Update watermark| WM
    L --> CW
```

---

## Step 1: Configure Bucket

```bash
export BUCKET=$(cd ../../../../infrastructure/environments/dev && terraform output -raw data_lake_bucket)
export AWS_REGION=us-east-1
```

---

## Step 2: Package Lambda

```bash
cd modules/module-02-ingestion/labs/lab-2.2-eventbridge-automation
mkdir -p build
pip install --target build boto3
cp src/scheduled_ingestion.py build/
cd build && zip -r ../scheduled-ingest.zip . && cd ..
```

---

## Step 3: Create IAM Role

Reuse Lab 2.1 pattern with expanded S3 permissions for metadata watermarks.

`s3-policy.json`:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Sid": "ReadWriteIngestionPaths",
      "Effect": "Allow",
      "Action": ["s3:PutObject", "s3:GetObject"],
      "Resource": [
        "arn:aws:s3:::BUCKET/raw/*",
        "arn:aws:s3:::BUCKET/metadata/*"
      ]
    }
  ]
}
```

```bash
# Create role (skip if reusing cnde-lab21 role with updated policy)
aws iam create-role \
  --role-name cnde-lab22-scheduled-ingest \
  --assume-role-policy-document file://../lab-2.1-lambda-ingestion/trust-policy.json

aws iam attach-role-policy \
  --role-name cnde-lab22-scheduled-ingest \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam put-role-policy \
  --role-name cnde-lab22-scheduled-ingest \
  --policy-name s3-ingest-metadata \
  --policy-document file://s3-policy.json
```

---

## Step 4: Deploy Lambda

```bash
ROLE_ARN=$(aws iam get-role --role-name cnde-lab22-scheduled-ingest --query Role.Arn --output text)

aws lambda create-function \
  --function-name cnde-lab22-scheduled-ingest \
  --runtime python3.11 \
  --handler scheduled_ingestion.lambda_handler \
  --role "$ROLE_ARN" \
  --zip-file fileb://scheduled-ingest.zip \
  --timeout 120 \
  --memory-size 512 \
  --environment "Variables={DATA_LAKE_BUCKET=$BUCKET,RAW_PREFIX=raw/,SOURCE_SYSTEM=api-ingest,DATASET=posts,API_URL=https://jsonplaceholder.typicode.com/posts,WATERMARK_KEY=metadata/watermarks/api-ingest/posts.json}"
```

---

## Step 5: Create EventBridge Rule

```bash
aws events put-rule \
  --name cnde-lab22-ingest-schedule \
  --schedule-expression "rate(15 minutes)" \
  --state ENABLED \
  --description "Lab 2.2 scheduled API ingestion"

RULE_ARN=$(aws events describe-rule --name cnde-lab22-ingest-schedule --query Arn --output text)
FUNC_ARN=$(aws lambda get-function --function-name cnde-lab22-scheduled-ingest --query Configuration.FunctionArn --output text)

aws events put-targets \
  --rule cnde-lab22-ingest-schedule \
  --targets "Id"="1","Arn"="$FUNC_ARN"

aws lambda add-permission \
  --function-name cnde-lab22-scheduled-ingest \
  --statement-id eventbridge-invoke \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn "$RULE_ARN"
```

---

## Step 6: Manual Test Invoke

Before waiting for the schedule, invoke once:

```bash
aws lambda invoke \
  --function-name cnde-lab22-scheduled-ingest \
  --payload '{}' \
  --cli-binary-format raw-in-base64-out \
  response.json

cat response.json | python -m json.tool
```

---

## Step 7: Verify Snapshot and Watermark

```bash
# Snapshot in raw zone
aws s3 ls s3://${BUCKET}/raw/api-ingest/posts/ --recursive

# Watermark
aws s3 cp s3://${BUCKET}/metadata/watermarks/api-ingest/posts.json - | python -m json.tool
```

Expected watermark fields:

- `last_successful_run`
- `last_snapshot_key`
- `records_ingested`

Run invoke twice; confirm **two snapshot files** (time-based keys) and watermark **updated**.

---

## Step 8: Confirm Scheduled Execution

Wait 15 minutes (or temporarily set `rate(5 minutes)` for testing), then:

```bash
aws logs filter-log-events \
  --log-group-name /aws/lambda/cnde-lab22-scheduled-ingest \
  --filter-pattern "scheduled_ingestion_complete" \
  --limit 5
```

---

## Deliverables Checklist

- [ ] EventBridge rule `cnde-lab22-ingest-schedule` enabled
- [ ] Lambda executes successfully on manual invoke
- [ ] At least one snapshot under `raw/api-ingest/posts/`
- [ ] Watermark JSON in `metadata/watermarks/api-ingest/`
- [ ] CloudWatch shows `scheduled_ingestion_complete`
- [ ] `LAB-2.2-REPORT.md` documenting schedule, record count, and architecture

---

## Verification Steps

| Check | Expected |
|-------|----------|
| Rule state | `ENABLED` in EventBridge console |
| Lambda permission | EventBridge can invoke function |
| Snapshot content | JSON with `records` array (100 posts from API) |
| Watermark update | `last_successful_run` changes after each run |
| No duplicates in watermark path | Single watermark key overwritten |

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Lambda times out | Increase timeout to 120s; check API URL reachable |
| `URLError` / connection failed | Lambda needs internet; remove VPC or add NAT |
| EventBridge not firing | Confirm rule `ENABLED` and target ARN correct |
| `AccessDenied` on GetObject watermark | Add `s3:GetObject` on `metadata/*` to IAM policy |
| `PermissionDenied` on invoke | Re-run `add-permission` with correct rule ARN |
| Empty posts list | Verify `API_URL`; test with `curl` from your laptop |

---

## Production Considerations (Discussion)

- Replace `rate(15 minutes)` with business-aligned `cron()` in UTC
- Store API keys in **Secrets Manager**, not environment variables
- Add DLQ on Lambda async config for failure isolation
- Implement true incremental fetch using API `updated_since` parameter

---

## Cleanup

```bash
aws events remove-targets --rule cnde-lab22-ingest-schedule --ids 1
aws events delete-rule --name cnde-lab22-ingest-schedule
aws lambda remove-permission --function-name cnde-lab22-scheduled-ingest --statement-id eventbridge-invoke
aws lambda delete-function --function-name cnde-lab22-scheduled-ingest
```

---

## What You Learned

- Scheduled pull ingestion with EventBridge
- Watermark files for operational continuity
- Snapshot-based API landing in the raw zone

**Next:** [Lab 2.3 – S3 Event Processing](../lab-2.3-s3-event-processing/README.md)
