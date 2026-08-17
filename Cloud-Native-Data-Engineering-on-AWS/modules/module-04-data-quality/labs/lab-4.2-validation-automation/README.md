# Lab 4.2: Validation Automation in ETL Pipelines

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-4.2-validation-automation.drawio)](../../../../docs/diagrams/drawio/lab-4.2-validation-automation.drawio) · [PNG](../../../../docs/diagrams/png/lab-4.2-validation-automation.png) · [SVG](../../../../docs/diagrams/svg/lab-4.2-validation-automation.svg)

**Estimated time:** 90 minutes · **Module 4**

---

## Objectives

- Integrate the Lab 4.1 validation framework into AWS Lambda for ingestion-time checks
- Embed validation in an AWS Glue ETL job for batch processing at scale
- Publish quality metrics to Amazon CloudWatch
- Trigger SNS alerts when pass rate falls below SLO threshold
- Understand how the same patterns map to Great Expectations checkpoints

---

## Prerequisites

- Lab 4.1 complete (validators and quality_runner working locally)
- Lab 1.1 S3 data lake deployed with `quarantine/` and `metadata/` zones
- Module 3 Glue ETL familiarity (Glue job, DynamicFrame basics)
- AWS CLI configured; `boto3` installed locally

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

```text
                    ┌─────────────────────────────────────┐
                    │           EventBridge / S3 Event     │
                    └──────────────────┬──────────────────┘
                                       │
              ┌────────────────────────┼────────────────────────┐
              ▼                        ▼                        │
     ┌─────────────────┐     ┌─────────────────┐               │
     │ Lambda Ingest   │     │ Glue ETL Job    │               │
     │ (lightweight)   │     │ (batch validate)│               │
     └────────┬────────┘     └────────┬────────┘               │
              │                       │                         │
              │    Lab 4.1 validators │                         │
              └───────────┬───────────┘                         │
                          ▼                                     │
              ┌───────────────────────┐                         │
              │   RuleEngine + Runner │                         │
              └───────────┬───────────┘                         │
                          │                                     │
         ┌────────────────┼────────────────┐                    │
         ▼                ▼                ▼                    │
    raw/            cleaned/        quarantine/                 │
                          │                                     │
                          ▼                                     │
              metadata/quality-reports/                         │
                          │                                     │
                          ▼                                     │
              CloudWatch Metrics ──→ SNS Alert                  │
```

---

## Part A: Lambda Ingestion Validation

### Step 1: Package Validators for Lambda

Lambda needs the validation code in the deployment package:

```bash
cd modules/module-04-data-quality/labs/lab-4.1-quality-framework

mkdir -p ../../lab-4.2-validation-automation/lambda-package
cp src/validators.py ../../lab-4.2-validation-automation/lambda-package/
cp rules/orders_rules.json ../../lab-4.2-validation-automation/lambda-package/
```

Create the Lambda handler at `lambda-package/handler.py`:

```python
"""Lambda handler: validate incoming order records before raw zone write."""

import json
import os
from datetime import datetime, timezone

import boto3

from validators import RuleEngine

s3 = boto3.client("s3")
RULES_PATH = os.path.join(os.path.dirname(__file__), "orders_rules.json")
engine = RuleEngine(RULES_PATH)
BUCKET = os.environ["DATA_LAKE_BUCKET"]
PASS_RATE_SLO = float(os.environ.get("PASS_RATE_SLO", "99.9"))


def lambda_handler(event, context):
    records = event.get("records", [event])
    results = engine.validate_batch(records)

    passed = []
    quarantined = []
    for result in results:
        if result.has_errors:
            quarantined.append(
                {
                    **result.record,
                    "_violations": [
                        {
                            "rule": v.rule,
                            "field": v.field,
                            "message": v.message,
                            "severity": v.severity,
                        }
                        for v in result.violations
                    ],
                }
            )
        else:
            passed.append(result.record)

    now = datetime.now(timezone.utc)
    prefix = (
        f"year={now.year}/month={now.month:02d}/day={now.day:02d}/"
        f"lambda-{context.aws_request_id}"
    )

    if passed:
        s3.put_object(
            Bucket=BUCKET,
            Key=f"raw/retail/orders/{prefix}/passed.json",
            Body=json.dumps(passed).encode(),
            ContentType="application/json",
        )

    if quarantined:
        s3.put_object(
            Bucket=BUCKET,
            Key=f"quarantine/retail/orders/{prefix}/failed.json",
            Body=json.dumps(quarantined).encode(),
            ContentType="application/json",
        )

    total = len(records)
    pass_rate = (len(passed) / total * 100) if total else 100.0

    cloudwatch = boto3.client("cloudwatch")
    cloudwatch.put_metric_data(
        Namespace="CNDE/DataQuality",
        MetricData=[
            {
                "MetricName": "RecordsProcessed",
                "Value": total,
                "Unit": "Count",
                "Dimensions": [{"Name": "Dataset", "Value": "retail/orders"}],
            },
            {
                "MetricName": "RecordsQuarantined",
                "Value": len(quarantined),
                "Unit": "Count",
                "Dimensions": [{"Name": "Dataset", "Value": "retail/orders"}],
            },
            {
                "MetricName": "PassRate",
                "Value": pass_rate,
                "Unit": "Percent",
                "Dimensions": [{"Name": "Dataset", "Value": "retail/orders"}],
            },
        ],
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "processed": total,
                "passed": len(passed),
                "quarantined": len(quarantined),
                "pass_rate_pct": round(pass_rate, 2),
                "within_slo": pass_rate >= PASS_RATE_SLO,
            }
        ),
    }
```

### Step 2: Deploy Lambda (Console or CLI)

Package and deploy:

```bash
cd modules/module-04-data-quality/labs/lab-4.2-validation-automation/lambda-package
zip -r ../validation-lambda.zip .

export BUCKET=$(cd ../../../../../infrastructure/environments/dev && terraform output -raw data_lake_bucket)

aws lambda create-function \
  --function-name cnde-dev-order-validation \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/cnde-lambda-validation-role \
  --handler handler.lambda_handler \
  --zip-file fileb://../validation-lambda.zip \
  --timeout 30 \
  --environment "Variables={DATA_LAKE_BUCKET=${BUCKET},PASS_RATE_SLO=99.9}"
```

> **Note:** Create an IAM role with `s3:PutObject` on `raw/` and `quarantine/`, plus `cloudwatch:PutMetricData`. Use least-privilege policies scoped to your bucket.

### Step 3: Test Lambda Locally

Simulate an invocation with sample payload:

```bash
cd modules/module-04-data-quality/labs/lab-4.2-validation-automation

cat > test_event.json << 'EOF'
{
  "records": [
    {
      "order_id": "ORD-100",
      "customer_email": "test@example.com",
      "order_amount": 50.00,
      "status": "pending",
      "currency": "USD"
    },
    {
      "order_id": "ORD-101",
      "customer_email": "bad@",
      "order_amount": -10.00,
      "status": "invalid",
      "currency": "USD"
    }
  ]
}
EOF

export DATA_LAKE_BUCKET=$BUCKET
python -c "
import json, os, sys
sys.path.insert(0, '../lab-4.1-quality-framework/lambda-package')
os.environ['DATA_LAKE_BUCKET'] = os.environ.get('DATA_LAKE_BUCKET', 'test-bucket')
from handler import lambda_handler
class Ctx:
    aws_request_id = 'local-test-001'
print(json.dumps(lambda_handler(json.load(open('test_event.json')), Ctx()), indent=2))
"
```

Expected: 1 passed, 1 quarantined, `within_slo: false`.

---

## Part B: Glue ETL Batch Validation

### Step 4: Glue Job Script Pattern

Create `glue-scripts/orders_quality_etl.py`:

```python
"""Glue ETL: read raw orders, validate, write cleaned + quarantine."""

import json
import sys
from datetime import datetime, timezone

import boto3
from awsglue.context import GlueContext
from pyspark.context import SparkContext
from awsglue.job import Job
from awsglue.utils import getResolvedOptions
from pyspark.sql import Row
from pyspark.sql.functions import col, current_timestamp, lit

# Import validators (upload validators.py as an extra Python file in Glue job)
from validators import RuleEngine

args = getResolvedOptions(
    sys.argv,
    ["JOB_NAME", "DATA_LAKE_BUCKET", "RULES_S3_PATH", "INPUT_DATE"],
)

sc = SparkContext.getOrCreate()
glue_context = GlueContext(sc)
spark = glue_context.spark_session
job = Job(glue_context)
job.init(args["JOB_NAME"], args)

bucket = args["DATA_LAKE_BUCKET"]
input_date = args["INPUT_DATE"]  # e.g. 2024-01-15
year, month, day = input_date.split("-")

raw_path = (
    f"s3://{bucket}/raw/retail/orders/"
    f"year={year}/month={month}/day={day}/"
)
cleaned_path = (
    f"s3://{bucket}/cleaned/retail/orders/"
    f"year={year}/month={month}/day={day}/"
)
quarantine_path = (
    f"s3://{bucket}/quarantine/retail/orders/"
    f"year={year}/month={month}/day={day}/"
    f"glue-run-{datetime.now(timezone.utc).strftime('%H%M%S')}/"
)

# Load rules from S3
rules_local = "/tmp/orders_rules.json"
s3_client = boto3.client("s3")
rules_key = args["RULES_S3_PATH"].replace(f"s3://{bucket}/", "")
s3_client.download_file(bucket, rules_key, rules_local)
engine = RuleEngine(rules_local)

# Read raw data
raw_df = spark.read.option("header", "true").csv(raw_path)
records = [row.asDict() for row in raw_df.collect()]

passed_rows = []
quarantine_rows = []
for record in records:
    result = engine.validate_record(record)
    if result.has_errors:
        quarantine_rows.append(
            Row(
                **record,
                _violations=json.dumps(
                    [{"rule": v.rule, "field": v.field, "message": v.message}
                     for v in result.violations]
                ),
            )
        )
    else:
        passed_rows.append(Row(**record))

passed_df = spark.createDataFrame(passed_rows) if passed_rows else None
quarantine_df = spark.createDataFrame(quarantine_rows) if quarantine_rows else None

if passed_df:
    passed_df.withColumn("_validated_at", current_timestamp()).write.mode(
        "overwrite"
    ).parquet(cleaned_path)

if quarantine_df:
    quarantine_df.withColumn("_quarantined_at", current_timestamp()).write.mode(
        "append"
    ).json(quarantine_path)

total = len(records)
pass_rate = (len(passed_rows) / total * 100) if total else 100.0
print(f"Glue validation: {len(passed_rows)}/{total} passed ({pass_rate:.2f}%)")

job.commit()
```

### Step 5: Upload Rules and Run Glue Job

```bash
aws s3 cp ../lab-4.1-quality-framework/rules/orders_rules.json \
  s3://${BUCKET}/metadata/rules/retail/orders_rules.json

# Upload glue script and validators.py to s3://{bucket}/scripts/
# Create/run Glue job via Console or AWS CLI with parameters:
#   DATA_LAKE_BUCKET, RULES_S3_PATH, INPUT_DATE
```

Verify outputs:

```bash
aws s3 ls s3://${BUCKET}/cleaned/retail/orders/ --recursive
aws s3 ls s3://${BUCKET}/quarantine/retail/orders/ --recursive
```

---

## Part C: CloudWatch Alarms and SNS

### Step 6: Create Pass Rate Alarm

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name cnde-orders-pass-rate-below-slo \
  --alarm-description "Order validation pass rate below 99.9% SLO" \
  --namespace CNDE/DataQuality \
  --metric-name PassRate \
  --dimensions Name=Dataset,Value=retail/orders \
  --statistic Average \
  --period 300 \
  --evaluation-periods 1 \
  --threshold 99.9 \
  --comparison-operator LessThanThreshold \
  --alarm-actions arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:cnde-data-quality-alerts
```

Create SNS topic and subscribe your email:

```bash
aws sns create-topic --name cnde-data-quality-alerts
aws sns subscribe \
  --topic-arn arn:aws:sns:us-east-1:YOUR_ACCOUNT_ID:cnde-data-quality-alerts \
  --protocol email \
  --notification-endpoint your-email@example.com
```

---

## Sample Validation Rules (Glue Parameter Store)

Store versioned rules in S3 for pipeline consumption:

```json
{
  "dataset": "retail/inventory",
  "version": "1.1",
  "rules": [
    {
      "name": "sku_not_null",
      "field": "sku",
      "type": "not_null",
      "severity": "error"
    },
    {
      "name": "quantity_non_negative",
      "field": "quantity_on_hand",
      "type": "range",
      "params": { "min": 0, "max": 1000000 },
      "severity": "error"
    },
    {
      "name": "warehouse_valid",
      "field": "warehouse_code",
      "type": "enum",
      "params": { "values": ["WH-EAST", "WH-WEST", "WH-CENTRAL"] },
      "severity": "error"
    }
  ]
}
```

Path: `s3://{bucket}/metadata/rules/retail/inventory_rules.json`

---

## Deliverables

- [ ] Lambda handler validates sample event and writes to S3 paths
- [ ] CloudWatch custom metrics visible in console
- [ ] Glue job script documented (run in dev or submit script + screenshot)
- [ ] SNS alarm configured for pass rate threshold
- [ ] `LAB-REPORT.md` with architecture diagram and test results

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Lambda `Unable to import module 'handler'` | Ensure `validators.py` is in zip root alongside `handler.py` |
| Lambda timeout on large batches | Increase timeout; move batch validation to Glue |
| Glue `ModuleNotFoundError: validators` | Add `validators.py` under **Python library path** in job details |
| Glue job reads empty raw path | Confirm partition path matches `INPUT_DATE` and Lab 1.2 upload |
| CloudWatch metrics not appearing | Check IAM `cloudwatch:PutMetricData`; metrics may take 1–2 minutes |
| SNS alarm never fires | Confirm Lambda/Glue published metrics; verify dimension `Dataset=retail/orders` |
| Pass rate always 100% in Lambda | Test payload must include intentionally bad records |
| S3 `AccessDenied` on quarantine | IAM role needs `s3:PutObject` on `quarantine/*` prefix |

---

## What You Learned

- Validation belongs at multiple pipeline stages (ingestion + transform)
- Lambda suits lightweight, event-driven checks; Glue handles batch scale
- CloudWatch metrics and SNS turn quality data into operational alerts
- Declarative rules in S3 enable rule updates without redeploying all code

---

**Next:** [Lab 4.3 – Quarantine Zone](../lab-4.3-quarantine-zone/README.md)
