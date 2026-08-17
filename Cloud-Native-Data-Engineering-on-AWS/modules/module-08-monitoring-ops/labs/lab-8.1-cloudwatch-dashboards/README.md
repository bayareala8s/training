# Lab 8.1: CloudWatch Dashboards for ETL Pipelines

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-8.1-cloudwatch-dashboards.drawio)](../../../../docs/diagrams/drawio/lab-8.1-cloudwatch-dashboards.drawio) · [PNG](../../../../docs/diagrams/png/lab-8.1-cloudwatch-dashboards.png) · [SVG](../../../../docs/diagrams/svg/lab-8.1-cloudwatch-dashboards.svg)

**Estimated time:** 90 minutes · **Module 8**

---

## Objectives

- Design an operations dashboard for batch ETL and ingestion pipelines
- Deploy a CloudWatch dashboard using JSON and Terraform
- Configure widgets for Glue, Lambda, custom data quality metrics, and S3 storage
- Verify dashboard visibility in the AWS Console

---

## Prerequisites

- Modules 1–7 complete (data lake, Glue jobs, quality framework)
- Terraform 1.5+ and AWS CLI configured
- Glue jobs and Lambda functions deployed from prior modules (or use placeholder names)

---

## Architecture

```text
Glue Jobs ──→ AWS/Glue metrics ──┐
Lambda      ──→ AWS/Lambda metrics ──┼──→ CloudWatch Dashboard
Quality Runner ──→ CNDE/DataQuality ──┤         (JSON / Terraform)
Step Functions ──→ AWS/States metrics ──┘
S3 Data Lake ──→ AWS/S3 metrics ────────┘
```

---

## Project Structure

```text
lab-8.1-cloudwatch-dashboards/
├── README.md
└── src/
    └── etl_pipeline_dashboard.json    # Dashboard body (import or Terraform)
```

The Terraform module at `infrastructure/modules/monitoring/main.tf` provides an IaC deployment path.

---

## Step 1: Review Dashboard JSON

Open `src/etl_pipeline_dashboard.json`. Note the widget categories:

| Widget | Metrics Source | Purpose |
|--------|----------------|---------|
| Glue Job Failures | `AWS/Glue` | Detect failed ETL runs |
| Glue Job Duration | `AWS/Glue` | Track performance regression |
| Lambda Health | `AWS/Lambda` | Ingestion errors and latency |
| Pass Rate | `CNDE/DataQuality` | SLO tracking (custom metrics) |
| Quarantine Count | `CNDE/DataQuality` | Quality incident visibility |
| Step Functions | `AWS/States` | Orchestration success/failure |
| S3 Storage | `AWS/S3` | Capacity and cost trend |
| Logs Insights | Glue log group | Recent ERROR lines |

**Customize placeholders:**

Replace `ACCOUNT_ID` with your AWS account ID and update job/function names to match your deployment:

```bash
export ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
sed "s/ACCOUNT_ID/${ACCOUNT_ID}/g" src/etl_pipeline_dashboard.json > src/etl_pipeline_dashboard_resolved.json
```

Update Glue job names (`cnde-orders-etl`, `cnde-inventory-etl`) and Lambda function name if different.

---

## Step 2: Deploy via AWS CLI (Console Alternative)

Create the dashboard directly from JSON:

```bash
cd modules/module-08-monitoring-ops/labs/lab-8.1-cloudwatch-dashboards

aws cloudwatch put-dashboard \
  --dashboard-name cnde-dev-etl-pipeline \
  --dashboard-body file://src/etl_pipeline_dashboard_resolved.json
```

Verify:

```bash
aws cloudwatch list-dashboards --query "DashboardEntries[?DashboardName=='cnde-dev-etl-pipeline']"
```

Open **CloudWatch → Dashboards → cnde-dev-etl-pipeline** in the AWS Console.

---

## Step 3: Deploy via Terraform (Recommended)

Add the monitoring module to your environment. Create or edit `infrastructure/environments/dev/monitoring.tf`:

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
terraform init
terraform plan -target=module.monitoring
terraform apply -target=module.monitoring
```

Save outputs:

```bash
terraform output -json > ../../../modules/module-08-monitoring-ops/labs/lab-8.1-cloudwatch-dashboards/monitoring-outputs.json
```

---

## Step 4: Publish Custom Metrics (Optional)

If you completed Lab 4.1, extend `quality_runner.py` to publish metrics, or run this script to simulate pipeline metrics:

```bash
python3 << 'EOF'
import boto3

cw = boto3.client("cloudwatch")
cw.put_metric_data(
    Namespace="CNDE/DataQuality",
    MetricData=[
        {
            "MetricName": "ValidationPassRate",
            "Dimensions": [
                {"Name": "Dataset", "Value": "retail/orders"},
                {"Name": "Environment", "Value": "dev"},
            ],
            "Value": 99.92,
            "Unit": "Percent",
        },
        {
            "MetricName": "QuarantinedRecords",
            "Dimensions": [
                {"Name": "Dataset", "Value": "retail/orders"},
                {"Name": "Environment", "Value": "dev"},
            ],
            "Value": 12,
            "Unit": "Count",
        },
    ],
)
print("Custom metrics published.")
EOF
```

Refresh the dashboard—pass rate and quarantine widgets should show data within 5 minutes.

---

## Step 5: Add SLO Annotation

In the AWS Console:

1. Edit the **Data Quality Pass Rate** widget
2. Add a horizontal annotation at **99%** labeled `SLO Threshold`
3. Save the dashboard

Document why 99% was chosen (reference Assignment 4 SLAs).

---

## Step 6: Document Your Dashboard

Create `LAB-REPORT.md` in this folder:

```markdown
# Lab 8.1 Report

## Dashboard Name
cnde-dev-etl-pipeline

## Widgets Configured
- [ ] Glue job failures and duration
- [ ] Lambda ingestion health
- [ ] Custom data quality metrics
- [ ] Step Functions (if deployed)
- [ ] S3 storage trend

## Customizations Made
<Describe job names, regions, SLO thresholds>

## Screenshots
Attach dashboard screenshot showing at least 4 widgets with data.

## Observations
What would you add for a production executive dashboard?
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Dashboard shows "No data" | Confirm Glue jobs have run recently; check region matches |
| Custom metrics missing | Run Step 4 script; verify namespace `CNDE/DataQuality` |
| Invalid JSON on put-dashboard | Validate with `python3 -m json.tool src/etl_pipeline_dashboard.json` |
| Terraform module not found | Run `terraform init` after adding `monitoring.tf` |
| SNS email not confirmed | Check inbox for AWS subscription confirmation (Lab 8.2) |

---

## Cleanup

Keep the dashboard for Labs 8.2 and 8.3. To remove only the Terraform-managed resources:

```bash
cd infrastructure/environments/dev
terraform destroy -target=module.monitoring
```

---

## What You Learned

- Dashboard-as-code with CloudWatch JSON
- Mapping pipeline SLIs to CloudWatch widgets
- Combining native AWS metrics with custom application metrics
- Terraform deployment of observability infrastructure

**Next:** [Lab 8.2 – SNS Alerts and Anomaly Detection](../lab-8.2-sns-alerts/README.md)
