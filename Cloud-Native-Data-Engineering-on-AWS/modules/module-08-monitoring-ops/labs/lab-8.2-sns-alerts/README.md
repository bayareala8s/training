# Lab 8.2: SNS Alerts and Anomaly Detection

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-8.2-sns-alerts.drawio)](../../../../docs/diagrams/drawio/lab-8.2-sns-alerts.drawio) · [PNG](../../../../docs/diagrams/png/lab-8.2-sns-alerts.png) · [SVG](../../../../docs/diagrams/svg/lab-8.2-sns-alerts.svg)

**Estimated time:** 90 minutes · **Module 8**

---

## Objectives

- Configure SNS topics for severity-based alert routing
- Create CloudWatch alarms for Glue failures, quality SLO breaches, and Lambda errors
- Enable anomaly detection on ingestion error metrics
- Test end-to-end alert delivery and document escalation paths

---

## Prerequisites

- Lab 8.1 complete (dashboard deployed)
- Monitoring Terraform module available at `infrastructure/modules/monitoring/main.tf`
- Valid email address for SNS subscriptions

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
CloudWatch Alarms
├── glue_job_failure (critical) ──→ SNS cnde-dev-alerts-critical ──→ Email (on-call)
├── lambda_errors (critical)    ──→ SNS cnde-dev-alerts-critical
├── quality_pass_rate_low (warn)──→ SNS cnde-dev-alerts-warning  ──→ Email (stewards)
└── lambda_errors_anomaly (warn)──→ SNS cnde-dev-alerts-warning
                                          │
                                          └── (optional) Lambda → Slack
```

---

## Step 1: Deploy Monitoring Stack

If not deployed in Lab 8.1, create `infrastructure/environments/dev/monitoring.tf`:

```hcl
module "monitoring" {
  source      = "../../modules/monitoring"
  project     = var.project
  environment = var.environment
  student     = var.student
  aws_region  = var.aws_region
  alert_email = "your-email@example.com"

  glue_job_names = [
    "cnde-orders-etl",
    "cnde-inventory-etl",
  ]
}
```

Apply:

```bash
cd infrastructure/environments/dev
terraform apply -target=module.monitoring
```

---

## Step 2: Confirm SNS Subscriptions

AWS sends a confirmation email for each SNS subscription.

1. Check your inbox for **AWS Notification – Subscription Confirmation**
2. Click **Confirm subscription** for both critical and warning topics
3. Verify subscription status:

```bash
aws sns list-subscriptions-by-topic \
  --topic-arn $(terraform output -raw sns_critical_topic_arn 2>/dev/null || \
    aws sns list-topics --query "Topics[?contains(TopicArn, 'alerts-critical')].TopicArn" --output text)
```

Status should be `Confirmed`, not `PendingConfirmation`.

---

## Step 3: Review Alarm Configuration

List deployed alarms:

```bash
aws cloudwatch describe-alarms \
  --alarm-name-prefix cnde-dev \
  --query "MetricAlarms[].{Name:AlarmName,State:StateValue,Actions:AlarmActions}" \
  --output table
```

Expected alarms (from `infrastructure/modules/monitoring/main.tf`):

| Alarm | Threshold | Severity | Action |
|-------|-----------|----------|--------|
| `glue-failure-{job}` | Failed tasks > 0 | Critical | SNS critical |
| `lambda-ingestion-errors` | Errors > 0 | Critical | SNS critical |
| `quality-pass-rate-low` | Pass rate < 99% | Warning | SNS warning |
| `lambda-errors-anomaly` | Outside anomaly band | Warning | SNS warning |

Open each alarm in the console and verify the **Description** field references your runbook (Assignment 8).

---

## Step 4: Test Critical Alert (Lambda Errors)

Simulate a Lambda error alarm by temporarily lowering the threshold (dev only):

```bash
aws cloudwatch put-metric-alarm \
  --alarm-name cnde-dev-test-lambda-error \
  --alarm-description "Lab 8.2 test alarm - delete after lab" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 60 \
  --evaluation-periods 1 \
  --threshold 0 \
  --comparison-operator GreaterThanThreshold \
  --dimensions Name=FunctionName,Value=cnde-dev-ingestion \
  --alarm-actions $(aws sns list-topics --query "Topics[?contains(TopicArn,'alerts-critical')].TopicArn" --output text) \
  --treat-missing-data notBreaching
```

Publish a test error metric:

```bash
aws cloudwatch put-metric-data \
  --namespace AWS/Lambda \
  --metric-data '[{
    "MetricName": "Errors",
    "Dimensions": [{"Name": "FunctionName", "Value": "cnde-dev-ingestion"}],
    "Value": 1,
    "Unit": "Count"
  }]'
```

Within 2–5 minutes you should receive an SNS email. Document the email subject, timestamp, and alarm name in your lab report.

**Cleanup test alarm:**

```bash
aws cloudwatch delete-alarms --alarm-names cnde-dev-test-lambda-error
```

---

## Step 5: Configure Anomaly Detection Alarm

The Terraform module deploys an anomaly detection alarm using:

```text
ANOMALY_DETECTION_BAND(m1, 2)
```

This creates a band ±2 standard deviations from the learned baseline.

**Train the baseline:** Anomaly detection needs ~2 weeks of data in production. For the lab:

1. Open **CloudWatch → Alarms → cnde-dev-lambda-errors-anomaly**
2. View the **Metric** graph—note the gray anomaly band
3. Publish varying error counts over 30 minutes to observe band behavior:

```bash
for i in 0 0 0 1 0 0 2 0 0; do
  aws cloudwatch put-metric-data \
    --namespace AWS/Lambda \
    --metric-data "[{\"MetricName\":\"Errors\",\"Dimensions\":[{\"Name\":\"FunctionName\",\"Value\":\"cnde-dev-ingestion\"}],\"Value\":$i,\"Unit\":\"Count\"}]"
  sleep 300
done
```

Document when the alarm would trigger vs a static threshold alarm.

---

## Step 6: Define Escalation Matrix

Create `escalation-matrix.md` in this folder:

```markdown
# Alert Escalation Matrix

| Alarm | Severity | Primary Responder | Escalation (30 min) | Business Notify |
|-------|----------|-------------------|---------------------|-----------------|
| Glue job failure | P1 | Data engineer on-call | Platform lead | Finance if orders stale |
| Lambda errors | P1 | Ingestion owner | Data engineer on-call | — |
| Pass rate low | P2 | Data steward | Data engineer | Analytics team |
| Anomaly detected | P3 | Data engineer | — | — |

## Response SLA
- P1: Acknowledge within 15 minutes
- P2: Acknowledge within 1 hour
- P3: Review next business day
```

---

## Step 7: Optional – Slack Integration

Create a Lambda function subscribed to SNS that posts to Slack:

```python
# slack_notifier.py (conceptual – deploy only if your org uses Slack)
import json
import urllib.request
import os

def handler(event, context):
    webhook = os.environ["SLACK_WEBHOOK_URL"]
    for record in event["Records"]:
        message = json.loads(record["Sns"]["Message"])
        alarm_name = message.get("AlarmName", "Unknown")
        state = message.get("NewStateValue", "UNKNOWN")
        reason = message.get("NewStateReason", "")
        payload = {
            "text": f":warning: *{alarm_name}* is *{state}*\n{reason}"
        }
        req = urllib.request.Request(
            webhook,
            data=json.dumps(payload).encode(),
            headers={"Content-Type": "application/json"},
        )
        urllib.request.urlopen(req)
    return {"statusCode": 200}
```

This step is optional for the course; email routing satisfies lab requirements.

---

## Step 8: Lab Report

Create `LAB-REPORT.md`:

```markdown
# Lab 8.2 Report

## SNS Topics
- Critical: <ARN>
- Warning: <ARN>

## Subscriptions Confirmed
- [ ] Critical email confirmed
- [ ] Warning email confirmed

## Test Results
- Test alarm triggered at: <timestamp>
- Email received: Yes/No
- Time from metric to email: <minutes>

## Anomaly Detection Observations
<Describe baseline behavior vs static threshold>

## Escalation Matrix
Link to escalation-matrix.md
```

---

## Deliverables

- [ ] SNS topics and subscriptions configured for critical/warning severities
- [ ] CloudWatch alarms tested (metric breach → email received)
- [ ] `LAB-REPORT.md` with test results and escalation matrix reference

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No email received | Confirm SNS subscription; check spam folder |
| Alarm stuck in INSUFFICIENT_DATA | Publish metrics or adjust `TreatMissingData` |
| Anomaly band not visible | Needs historical data; use static alarm for demo |
| Too many alert emails | Increase evaluation periods; use composite alarms |

---

## What You Learned

- Severity-based SNS routing for data platforms
- CloudWatch alarm configuration for pipeline SLIs
- Anomaly detection vs static thresholds
- Escalation matrix design for operational readiness

**Next:** [Lab 8.3 – Cost Reporting with Tags](../lab-8.3-cost-reporting/README.md)
