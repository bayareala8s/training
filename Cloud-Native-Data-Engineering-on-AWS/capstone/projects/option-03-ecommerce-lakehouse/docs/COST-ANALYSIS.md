# Cost Analysis – E-Commerce Analytics Lakehouse

**Project:** `cnde-cap-ecommerce`  
**Scenario:** Capstone Option 3 · Dev / demo scale  
**Assumptions:** us-east-1, ~40 orders/day sample (production model scaled to ~2M order lines/month)

---

## 1. Monthly Estimate (Production-like)

| Service | Usage assumption | Est. monthly |
|---------|------------------|--------------|
| S3 Standard | 80 GB lake + requests | $2.50 |
| S3 IA / lifecycle | 40% raw aged | $0.80 |
| Glue ETL | 2 DPU × 20 min × 30 days | $7.40 |
| Athena | 150 GB scanned / month (partitioned Parquet) | $0.75 |
| Lambda (quality) | 50k invocations | $0.20 |
| CloudWatch | Logs + 1 dashboard | $3.00 |
| SNS | Alerts | $0.10 |
| **Total** | | **~$14.75** |

Student/dev with lab-cycle start/stop and tiny samples: typically **under $5** for a demo week if torn down daily.

---

## 2. Cost Drivers & Optimizations

| Driver | Risk | Mitigation |
|--------|------|------------|
| Athena SELECT * on raw CSV | High scan $ | Query curated Parquet only; column projection |
| Unpartitioned Glue writes | Full refresh cost | Hive partitions by date; overwrite one day |
| Clickstream volume growth | Storage + ETL | Compress JSON→Parquet early; sample non-purchase events |
| Idle Glue endpoints | Fixed cost | Prefer jobs over always-on; use lab-cycle stop |

---

## 3. Athena Efficiency Pattern

Target curated scan under 50 MB per daily KPI query:

```sql
SELECT status, sum(amount) AS gmv
FROM fact_orders
WHERE year='2024' AND month='01' AND day='15'
GROUP BY status;
```

Partition filters + Parquet typically reduce cost 10–50× vs raw CSV scans.

---

## 4. Tagging for Cost Allocation

```text
Project=capstone-option-3
Course=cloud-native-data-engineering
Environment=dev
Owner=capstone-student
```

Use Cost Explorer filter on `Project=capstone-option-3`.

---

## 5. Budget Alarm

- Monthly budget: $45 (dev) / $200 (prod pilot)
- Alert at 50% and 80% via Budgets → SNS
- Hard stop: `./scripts/lab-cycle.sh stop --yes` after demos

---

## 6. What We Deliberately Did Not Buy

| Option | Why deferred |
|--------|--------------|
| Redshift | Overkill for this volume; Athena sufficient |
| MWAA | Step Functions / EventBridge enough for nightly |
| Always-on Glue Flex without need | Jobs on schedule only |
