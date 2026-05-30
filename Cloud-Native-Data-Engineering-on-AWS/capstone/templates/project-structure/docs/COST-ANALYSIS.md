# Cost Analysis – [Project Name]

**Author:** [Your Name]  
**Last Updated:** [Date]  
**Environment:** dev  
**Reporting Period:** [Start Date] – [End Date]

---

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| **Total spend (period)** | $[amount] USD |
| **Daily average** | $[amount] USD |
| **Projected monthly (if unchanged)** | $[amount] USD |
| **Budget limit** | $[amount] USD |
| **Budget utilization** | [X]% |

[2–3 sentences summarizing primary cost drivers and optimization status.]

---

## 2. Cost Allocation Tags

All capstone resources must use:

| Tag Key | Value |
|---------|-------|
| `Project` | `capstone` |
| `Student` | `[your-name]` |
| `Environment` | `dev` |
| `Course` | `cloud-native-data-engineering` |

**Activation status:** [ ] Tags activated in Cost Allocation Tags console

---

## 3. Spend by AWS Service

| Service | Cost (USD) | % of Total | Primary Driver |
|---------|------------|------------|----------------|
| Amazon S3 | | | Storage + requests |
| AWS Glue | | | ETL DPU-hours |
| Amazon Athena | | | Data scanned |
| AWS Lambda | | | Invocations |
| Amazon CloudWatch | | | Logs + custom metrics |
| Amazon SNS | | | Notifications |
| AWS Step Functions | | | State transitions |
| Other | | | |
| **Total** | | **100%** | |

*Source: AWS Cost Explorer, filter `Project=capstone`, period [dates]*

### Daily Trend

[Insert screenshot from Cost Explorer or brief narrative: "Glue costs spike on Tue/Thu when ETL labs ran."]

---

## 4. Top Cost Drivers (Detailed)

### Driver 1: [e.g., Glue ETL Jobs]

| Attribute | Value |
|-----------|-------|
| Job name(s) | |
| Runs in period | |
| Avg DPU-hours per run | |
| Estimated cost per run | |
| Optimization applied | Job bookmarks, worker right-sizing |

### Driver 2: [e.g., S3 Storage]

| Prefix | Size (GB) | Storage Class | Monthly Est. |
|--------|-----------|---------------|--------------|
| `raw/` | | Standard | |
| `curated/` | | Standard | |
| `quarantine/` | | Standard | |

### Driver 3: [e.g., Athena Queries]

| Workgroup | Queries | Data Scanned (TB) | Cost |
|-----------|---------|-------------------|------|
| primary | | | |

---

## 5. Optimizations Implemented

| # | Optimization | Service | Est. Savings | Status |
|---|--------------|---------|--------------|--------|
| 1 | S3 lifecycle: raw/ → IA @ 90 days | S3 | [X]% on aged raw | Implemented |
| 2 | Parquet + partition pruning | Athena | Reduced scan [X]% | Implemented |
| 3 | Glue job bookmarks | Glue | Avoid full reprocess | Implemented |
| 4 | CloudWatch log retention 14d | CloudWatch | Lower log storage | Implemented |
| 5 | [Your optimization] | | | Planned |

---

## 6. Optimizations Planned (Future)

| Optimization | Effort | Impact | Timeline |
|--------------|--------|--------|----------|
| Intelligent-Tiering on raw/ | Low | Medium | Next sprint |
| Athena workgroup scan cap | Low | High (dev) | Immediate |
| Schedule Glue off-peak | Low | Low | Optional |
| Reserved capacity (if prod) | Medium | High at scale | Production only |

---

## 7. Budget and Alerts

| Budget Name | Limit | Alert Thresholds | Notifications |
|-------------|-------|------------------|---------------|
| `capstone-dev-monthly` | $[50] | 80%, 100% | [email] |

**Alert history:** [None / Alert fired on DATE at X%]

---

## 8. Production Cost Projection

Assumptions for production at **10× data volume**:

| Service | Dev Cost | Projected Prod | Notes |
|---------|----------|----------------|-------|
| S3 | $ | $ | Lifecycle + IA |
| Glue | $ | $ | More DPUs, same frequency |
| Athena | $ | $ | Partition strategy critical |
| Lambda | $ | $ | Linear with events |
| **Total** | $ | $ | |

[Explain which optimizations are required before production scale.]

---

## 9. Showback / Chargeback (Optional)

If this were an enterprise deployment:

| Cost Center | Allocated Spend | Allocation Method |
|-------------|-----------------|-------------------|
| [Analytics team] | $ | Tag `CostCenter` |
| [ML team] | $ | Tag `Dataset=ml` |

---

## 10. Cost Explorer Export

Attach or reference:

- `cost-by-service-[period].csv`
- `cost-daily-trend-[period].csv`

**How to reproduce:**

```bash
aws ce get-cost-and-usage \
  --time-period Start=YYYY-MM-DD,End=YYYY-MM-DD \
  --granularity DAILY \
  --metrics UnblendedCost \
  --group-by Type=DIMENSION,Key=SERVICE \
  --filter '{"Tags":{"Key":"Project","Values":["capstone"]}}'
```

---

## 11. References

- Module 8 Lab 8.3 – Cost reporting
- [AWS Pricing Calculator](https://calculator.aws/)
- Course infrastructure Terraform modules
