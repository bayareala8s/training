# Cost Analysis – Enterprise Data Platform

**Project:** `cnde-cap-enterprise`  
**Scenario:** Capstone Option 4 · Dev / pilot scale  
**Assumptions:** us-east-1; sample tens of rows locally; production model ~5M order lines/month + daily inventory snapshots + vendor feeds

---

## 1. Monthly Estimate (Pilot)

| Service | Usage assumption | Est. monthly |
|---------|------------------|--------------|
| S3 Standard | 200 GB multi-domain lake | $5.00 |
| S3 requests / lifecycle | IA for aged raw | $1.50 |
| Glue ETL | 4 DPU × 30 min × 30 | $22.20 |
| Step Functions | 30 × ~8 state transitions | $0.10 |
| Lambda ingest/quality | 200k invocations | $0.40 |
| Athena | 300 GB scanned | $1.50 |
| CloudWatch | Dashboard + logs + alarms | $6.00 |
| SNS | Ops alerts | $0.20 |
| **Total** | | **~$37** |

Local-only demos with lab-cycle stop: typically **&lt; $5/week**.

---

## 2. Cost by Module Layer

| Layer | Primary cost | Control |
|-------|--------------|---------|
| Ingestion | Lambda + S3 PUT | Batch coalesce small files |
| Quality | Lambda duration | Vectorize rules; avoid per-row remote calls |
| ETL | Glue DPU-hours | Job bookmarks; partition overwrite |
| Orchestration | SFN transitions | Keep state machine shallow |
| Serving | Athena bytes scanned | Curated Parquet only |
| Observability | CW logs retention | 14–30 day retention in dev |

---

## 3. Optimization Backlog

1. Convert cleaned JSON to Parquet before Athena  
2. Compact vendor micro-files daily  
3. Sample clickstream-like high-churn feeds (N/A here but pattern applies)  
4. Stop lab stack after demos (`lab-cycle.sh stop --yes`)  
5. Glue Flex workers for non-SLA backfills  

---

## 4. Tagging & Chargeback

```text
Project=capstone-option-4
Course=cloud-native-data-engineering
Environment=dev
Owner=capstone-student
```

Cost Explorer → Group by tag `Project` → filter `capstone-option-4`.

---

## 5. Budgets

| Environment | Monthly budget | Alert |
|-------------|----------------|-------|
| Dev / student | $60 | 50%, 80% |
| Pilot prod | $250 | 50%, 80%, 100% |

---

## 6. Rejected Costly Alternatives

| Alternative | Why not for v1 |
|-------------|----------------|
| EMR persistent cluster | Ops + idle cost |
| Redshift RA3 | Volume does not justify |
| Managed Airflow (MWAA) | SFN covers daily DAG |
| Always-on Feature Store | Parquet features sufficient initially |
