# Lab 8.3: Cost Reporting with Tags and Cost Explorer

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-8.3-cost-reporting.drawio)](../../../../docs/diagrams/drawio/lab-8.3-cost-reporting.drawio) · [PNG](../../../../docs/diagrams/png/lab-8.3-cost-reporting.png) · [SVG](../../../../docs/diagrams/svg/lab-8.3-cost-reporting.svg)

**Estimated time:** 75 minutes · **Module 8**

---

## Objectives

- Apply and activate cost allocation tags across data platform resources
- Generate Cost Explorer reports grouped by service and tag
- Create an AWS Budget with email alerts
- Produce a cost summary suitable for capstone `COST-ANALYSIS.md`

---

## Prerequisites

- Labs 8.1–8.2 complete
- Terraform-deployed resources with standard tags (`Project`, `Environment`, `Student`, `Course`)
- AWS Billing console access (may require root or billing admin in org accounts)

---

## Architecture

```text
Terraform common_tags
├── Project=cnde
├── Environment=dev
├── Student=<name>
├── Course=cloud-native-data-engineering
└── ManagedBy=terraform
        │
        ▼
Cost Allocation Tags (activated in Billing)
        │
        ▼
Cost Explorer → Filter by Project → Group by Service
        │
        ▼
AWS Budgets → Alert at 80% / 100%
```

---

## Step 1: Verify Resource Tags

Confirm tags on deployed resources:

```bash
# S3 bucket tags
aws s3api get-bucket-tagging --bucket $(cd infrastructure/environments/dev && terraform output -raw data_lake_bucket)

# List Glue jobs with tags (if deployed)
aws glue get-jobs --query "Jobs[?contains(Name, 'cnde')].Name" --output text | \
  xargs -I {} aws glue get-tags --resource-arn "arn:aws:glue:us-east-1:$(aws sts get-caller-identity --query Account --output text):job/{}"
```

Expected tag keys from course Terraform modules:

| Tag Key | Example Value | Purpose |
|---------|---------------|---------|
| `Project` | `cnde` | Cost grouping |
| `Environment` | `dev` | Separate dev spend |
| `Student` | `jane-doe` | Lab attribution |
| `Course` | `cloud-native-data-engineering` | Program tracking |
| `ManagedBy` | `terraform` | IaC vs manual resources |

If tags are missing, update Terraform modules and re-apply.

---

## Step 2: Activate Cost Allocation Tags

Cost tags must be activated before appearing in Cost Explorer.

**Console path:**

1. Open **AWS Billing → Cost Allocation Tags**
2. Under **User-defined cost allocation tags**, select:
   - `Project`
   - `Environment`
   - `Student`
   - `Course`
3. Click **Activate**
4. Wait up to 24 hours for tags to propagate (often within a few hours)

**CLI (if supported in your account):**

```bash
aws ce list-cost-allocation-tags --status Active --query "CostAllocationTags[].TagKey"
```

---

## Step 3: Cost Explorer – Service Breakdown

Follow this guide to build your first report.

### Report 1: Total Spend by Service (Last 7 Days)

1. Open **AWS Cost Explorer**
2. Set **Date range:** Last 7 days
3. **Granularity:** Daily
4. **Group by:** Service
5. **Filter:** Tag → `Project` → `cnde`
6. **Chart type:** Stacked area

**Expected top services for this course:**

| Service | Typical Cost Driver |
|---------|---------------------|
| Amazon S3 | Storage and requests |
| AWS Glue | ETL DPU-hours |
| Amazon Athena | Query data scanned |
| AWS Lambda | Ingestion invocations |
| Amazon CloudWatch | Logs and custom metrics |

Export: **Download CSV** → save as `cost-by-service-7d.csv`

### Report 2: Spend by Environment

1. Same date range
2. **Group by:** Tag → `Environment`
3. Filter `Project = cnde`

Save as `cost-by-environment-7d.csv`

### Report 3: Daily Trend (Glue Focus)

1. **Filter:** Service = AWS Glue AND Tag `Project` = cnde
2. **Granularity:** Daily
3. **Group by:** None

Note which days had Glue job runs (correlate with lab activity).

---

## Step 4: Cost Explorer – CLI Export

```bash
# Last 7 days, grouped by service, filtered by Project tag
START=$(date -u -v-7d +%Y-%m-%d 2>/dev/null || date -u -d '7 days ago' +%Y-%m-%d)
END=$(date -u +%Y-%m-%d)

aws ce get-cost-and-usage \
  --time-period Start=$START,End=$END \
  --granularity DAILY \
  --metrics "UnblendedCost" \
  --group-by Type=DIMENSION,Key=SERVICE \
  --filter '{
    "Tags": {
      "Key": "Project",
      "Values": ["cnde"]
    }
  }' \
  --output json > cost-explorer-export.json
```

Review totals:

```bash
python3 << 'EOF'
import json
with open("cost-explorer-export.json") as f:
    data = json.load(f)
total = 0
for result in data["ResultsByTime"]:
    for group in result["Groups"]:
        amt = float(group["Metrics"]["UnblendedCost"]["Amount"])
        if amt > 0.01:
            total += amt
            print(f"{group['Keys'][0]}: ${amt:.2f}")
print(f"\nPeriod total: ${total:.2f}")
EOF
```

---

## Step 5: Create AWS Budget

Set a monthly budget with alerts (recommended: $25–50 for dev labs):

```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
EMAIL="your-email@example.com"

aws budgets create-budget \
  --account-id $ACCOUNT_ID \
  --budget '{
    "BudgetName": "cnde-dev-monthly",
    "BudgetLimit": {"Amount": "50", "Unit": "USD"},
    "TimeUnit": "MONTHLY",
    "BudgetType": "COST",
    "CostFilters": {
      "TagKeyValue": ["Project$cnde"]
    }
  }' \
  --notifications-with-subscribers '[{
    "Notification": {
      "NotificationType": "ACTUAL",
      "ComparisonOperator": "GREATER_THAN",
      "Threshold": 80,
      "ThresholdType": "PERCENTAGE"
    },
    "Subscribers": [{"SubscriptionType": "EMAIL", "Address": "'$EMAIL'"}]
  }]'
```

Verify in **Billing → Budgets → cnde-dev-monthly**.

---

## Step 6: Cost Optimization Recommendations

Document at least **three** optimizations for your deployed platform:

| Optimization | Service | Estimated Savings | Effort |
|--------------|---------|-------------------|--------|
| Lifecycle: raw/ → IA @ 90d | S3 | 40–50% on aged raw data | Low (already in module) |
| Glue job bookmarks | Glue | Avoid reprocessing full dataset | Medium |
| Athena partition projection | Athena | Reduce scan on ad-hoc queries | Medium |
| Reduce CloudWatch log retention | CloudWatch | Lower log storage cost | Low |
| Schedule Glue off-peak | Glue | No direct savings; avoids contention | Low |

Run this S3 storage analysis:

```bash
BUCKET=$(cd infrastructure/environments/dev && terraform output -raw data_lake_bucket)

aws cloudwatch get-metric-statistics \
  --namespace AWS/S3 \
  --metric-name BucketSizeBytes \
  --dimensions Name=BucketName,Value=$BUCKET Name=StorageType,Value=StandardStorage \
  --start-time $(date -u -v-7d +%Y-%m-%dT%H:%M:%SZ 2>/dev/null || date -u -d '7 days ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 86400 \
  --statistics Average \
  --query "Datapoints | sort_by(@, &Timestamp)"
```

---

## Step 7: Produce Cost Summary Report

Create `cost-summary.md` in this folder using this template:

```markdown
# CNDE Dev Environment – Cost Summary

**Period:** <start> to <end>
**Tag filter:** Project=cnde, Environment=dev

## Total Spend
$<amount> USD

## By Service
| Service | Cost (USD) | % of Total |
|---------|------------|------------|
| Amazon S3 | | |
| AWS Glue | | |
| Amazon Athena | | |
| AWS Lambda | | |
| Other | | |

## Top Cost Drivers
1. <driver and explanation>
2. <driver and explanation>

## Optimizations Applied / Planned
- <optimization 1>
- <optimization 2>
- <optimization 3>

## Budget Status
Budget: $50/month | Current: $<amount> (<percent>%)

## Capstone Projection
At 10× data volume, estimated monthly cost: $<projection> with noted optimizations.
```

This document feeds directly into capstone `COST-ANALYSIS.md`.

---

## Step 8: Lab Report Checklist

Create `LAB-REPORT.md`:

- [ ] Tags verified on S3 and at least one compute resource
- [ ] Cost allocation tags activated (or activation requested)
- [ ] Cost Explorer CSV exports attached
- [ ] AWS Budget created with 80% alert
- [ ] `cost-summary.md` completed
- [ ] Three optimization recommendations documented

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| No tag filter in Cost Explorer | Activate tags; wait up to 24 hours |
| Costs show $0 | Account may use credits; check UnblendedCost vs BlendedCost |
| Budget creation denied | Requires `budgets:CreateBudget` IAM permission |
| Glue costs higher than expected | Check DPU count and job frequency; review job bookmarks |

---

## What You Learned

- Cost allocation tagging for data platform showback
- Cost Explorer filtering and export for reporting
- AWS Budgets for proactive spend alerts
- Connecting operational metrics to financial accountability

**Next:** [Assignment 8 – Operations Runbook](../../assignments/assignment-08.md)
