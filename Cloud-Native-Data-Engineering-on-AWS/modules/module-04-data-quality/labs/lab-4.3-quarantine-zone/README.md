# Lab 4.3: Bad Record Isolation and Quarantine Zone

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-4.3-quarantine-zone.drawio)](../../../../docs/diagrams/drawio/lab-4.3-quarantine-zone.drawio) · [PNG](../../../../docs/diagrams/png/lab-4.3-quarantine-zone.png) · [SVG](../../../../docs/diagrams/svg/lab-4.3-quarantine-zone.svg)

**Estimated time:** 90 minutes · **Module 4**

---

## Objectives

- Implement enterprise quarantine zone conventions on S3
- Structure quarantined records with violation metadata for remediation
- Build a quarantine review workflow for data stewards
- Replay corrected records from quarantine back into the cleaned zone
- Configure lifecycle policies for quarantine retention

---

## Prerequisites

- Lab 4.1 complete (quality_runner produces quarantined output)
- Lab 4.2 complete (optional: Lambda/Glue writing to quarantine)
- S3 data lake with `quarantine/` zone from Lab 1.1

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
Raw Orders
     │
     ▼
Validation (Lab 4.1 / 4.2)
     │
     ├── PASS ──────────────────→ cleaned/retail/orders/
     │
     └── FAIL ──────────────────→ quarantine/retail/orders/
                                           │
                                           ▼
                                  ┌─────────────────┐
                                  │ Steward Review  │
                                  │ (Athena / CLI)  │
                                  └────────┬────────┘
                                           │
                              ┌────────────┼────────────┐
                              ▼            ▼            ▼
                         Fix Source   Approve      Discard
                              │         Override        │
                              └────────────┴────────────┘
                                           │
                                           ▼
                                    Replay Job
                                           │
                                           ▼
                              cleaned/retail/orders/
                              (reprocessed partition)
```

---

## Quarantine Zone Conventions

### Path Structure

```text
s3://{bucket}/quarantine/{domain}/{dataset}/year={YYYY}/month={MM}/day={DD}/
    run_id={pipeline_run_id}/
        failed_records.json          # or .parquet for Glue
        violations_summary.json
        _MANIFEST.json
        _SUCCESS
```

### Required Metadata Fields

Every quarantined record must include:

| Field | Example | Purpose |
|-------|---------|---------|
| `_violations` | `[{"rule":"amount_in_range",...}]` | Why it failed |
| `_quarantine_timestamp` | `2024-01-15T14:30:00Z` | When isolated |
| `_source_path` | `s3://.../raw/.../orders.csv` | Traceability |
| `_batch_id` | `a1b2c3d4-...` | Pipeline run ID |
| `_record_hash` | `sha256:abc123...` | Deduplication on replay |

---

## Step 1: Upload Quarantined Records with Manifest

Use Lab 4.1 output and enrich with quarantine metadata:

```bash
cd modules/module-04-data-quality/labs/lab-4.1-quality-framework

python src/quality_runner.py \
  --rules rules/orders_rules.json \
  --input sample-data/orders_sample.json \
  --output-dir output \
  --batch-id "lab43-$(date +%Y%m%d-%H%M%S)"

export BUCKET=$(cd ../../../../../infrastructure/environments/dev && terraform output -raw data_lake_bucket)
export RUN_ID="lab43-$(date +%Y%m%d-%H%M%S)"
export YEAR=$(date +%Y)
export MONTH=$(date +%m)
export DAY=$(date +%d)
export QUARANTINE_PREFIX="quarantine/retail/orders/year=${YEAR}/month=${MONTH}/day=${DAY}/run_id=${RUN_ID}"
```

Create manifest script inline:

```bash
python << 'PYEOF'
import json
from datetime import datetime, timezone
from pathlib import Path

output_dir = Path("output")
quarantined = json.loads((output_dir / "quarantined_records.json").read_text())
report = json.loads((output_dir / "quality_report.json").read_text())

now = datetime.now(timezone.utc).isoformat()
for record in quarantined:
    record["_quarantine_timestamp"] = now
    record["_source_path"] = "s3://lab/sample-data/orders_sample.json"
    record["_batch_id"] = report["batch_id"]

manifest = {
    "dataset": "retail/orders",
    "run_id": report["batch_id"],
    "quarantine_timestamp": now,
    "record_count": len(quarantined),
    "violation_summary": report["top_violations"],
    "pass_rate_pct": report["summary"]["pass_rate_pct"],
    "status": "pending_review",
}

Path("output/enriched_quarantine.json").write_text(json.dumps(quarantined, indent=2))
Path("output/_MANIFEST.json").write_text(json.dumps(manifest, indent=2))
print(f"Enriched {len(quarantined)} quarantined records")
PYEOF
```

Upload to S3:

```bash
aws s3 cp output/enriched_quarantine.json \
  "s3://${BUCKET}/${QUARANTINE_PREFIX}/failed_records.json"

aws s3 cp output/_MANIFEST.json \
  "s3://${BUCKET}/${QUARANTINE_PREFIX}/_MANIFEST.json"

# Marker file signals successful write (downstream orchestration pattern)
echo "" | aws s3 cp - "s3://${BUCKET}/${QUARANTINE_PREFIX}/_SUCCESS"
```

Verify:

```bash
aws s3 ls "s3://${BUCKET}/${QUARANTINE_PREFIX}/"
aws s3 cp "s3://${BUCKET}/${QUARANTINE_PREFIX}/_MANIFEST.json" - | python -m json.tool
```

---

## Step 2: Query Quarantine with Athena

Register quarantine data in Glue Data Catalog (Console or CLI):

**Table:** `quarantine_orders`
**Location:** `s3://${BUCKET}/quarantine/retail/orders/`
**Format:** JSON (or create external table on Parquet if using Glue output)

Example Athena DDL:

```sql
CREATE EXTERNAL TABLE IF NOT EXISTS quarantine_orders (
  order_id STRING,
  customer_email STRING,
  order_amount DOUBLE,
  status STRING,
  currency STRING,
  _violations STRING,
  _quarantine_timestamp STRING,
  _source_path STRING,
  _batch_id STRING
)
ROW FORMAT SERDE 'org.openx.data.jsonserde.JsonSerDe'
LOCATION 's3://YOUR-BUCKET/quarantine/retail/orders/';
```

Query pending violations:

```sql
SELECT
  order_id,
  order_amount,
  status,
  _violations,
  _quarantine_timestamp
FROM quarantine_orders
WHERE order_id IS NOT NULL
ORDER BY _quarantine_timestamp DESC
LIMIT 20;
```

Violation breakdown:

```sql
SELECT
  json_extract_scalar(violation, '$.rule') AS rule_name,
  COUNT(*) AS failure_count
FROM quarantine_orders
CROSS JOIN UNNEST(CAST(json_parse(_violations) AS ARRAY(JSON))) AS t(violation)
GROUP BY 1
ORDER BY 2 DESC;
```

---

## Step 3: Steward Review Workflow

Simulate a data steward reviewing quarantined records:

| Record | Issue | Steward Action |
|--------|-------|----------------|
| `ORD-003` | Negative amount | **Fix source** — ERP refund misclassified as order |
| `ORD-007` | Invalid status `returned` | **Approve override** — add `returned` to enum (schema change) |
| `ORD-009` | Null order_id | **Discard** — unrecoverable; log for source team |

Document decisions in `review_log.json`:

```json
{
  "run_id": "lab43-20240115-143000",
  "reviewed_by": "data-steward@retailco.com",
  "review_timestamp": "2024-01-15T16:00:00Z",
  "decisions": [
    {
      "order_id": "ORD-003",
      "action": "fix_and_replay",
      "corrected_record": {
        "order_id": "ORD-003",
        "customer_email": "carol@example.com",
        "order_amount": 15.99,
        "status": "pending",
        "currency": "USD"
      },
      "notes": "Refund reclassified; amount corrected to positive value"
    },
    {
      "order_id": "ORD-007",
      "action": "fix_and_replay",
      "corrected_record": {
        "order_id": "ORD-007",
        "customer_email": "grace@example.com",
        "order_amount": 88.25,
        "status": "cancelled",
        "currency": "USD"
      },
      "notes": "Mapped returned status to cancelled pending enum update"
    },
    {
      "order_id": null,
      "action": "discard",
      "notes": "Unrecoverable null order_id; escalated to ecommerce team"
    }
  ]
}
```

---

## Step 4: Replay Corrected Records

Create `scripts/replay_quarantine.py`:

```python
#!/usr/bin/env python3
"""Replay steward-approved records from quarantine to cleaned zone."""

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "lab-4.1-quality-framework" / "src"))
from validators import RuleEngine


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--review-log", required=True)
    parser.add_argument("--rules", required=True)
    parser.add_argument("--output", default="output/replayed_records.json")
    args = parser.parse_args()

    review = json.loads(Path(args.review_log).read_text())
    engine = RuleEngine(args.rules)

    replayed = []
    skipped = []

    for decision in review["decisions"]:
        if decision["action"] != "fix_and_replay":
            skipped.append(decision)
            continue

        record = decision["corrected_record"]
        result = engine.validate_record(record)
        if result.has_errors:
            print(f"SKIP {record.get('order_id')}: still fails validation")
            skipped.append(decision)
            continue

        record["_replayed_at"] = datetime.now(timezone.utc).isoformat()
        record["_original_quarantine_run"] = review["run_id"]
        replayed.append(record)

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    Path(args.output).write_text(json.dumps(replayed, indent=2))
    print(f"Replayed {len(replayed)} records; skipped {len(skipped)}")
    return 0 if replayed else 1


if __name__ == "__main__":
    sys.exit(main())
```

Run replay:

```bash
mkdir -p scripts
# Save replay script above to scripts/replay_quarantine.py
# Save review_log.json from Step 3

python scripts/replay_quarantine.py \
  --review-log review_log.json \
  --rules ../lab-4.1-quality-framework/rules/orders_rules.json \
  --output output/replayed_records.json
```

Upload replayed records to cleaned zone:

```bash
aws s3 cp output/replayed_records.json \
  "s3://${BUCKET}/cleaned/retail/orders/year=${YEAR}/month=${MONTH}/day=${DAY}/replayed_${RUN_ID}.json"
```

Update manifest status:

```bash
python -c "
import json
m = json.load(open('output/_MANIFEST.json'))
m['status'] = 'partially_resolved'
m['replayed_count'] = 2
m['discarded_count'] = 1
json.dump(m, open('output/_MANIFEST_updated.json','w'), indent=2)
"

aws s3 cp output/_MANIFEST_updated.json \
  "s3://${BUCKET}/${QUARANTINE_PREFIX}/_MANIFEST.json"
```

---

## Step 5: Lifecycle Policy for Quarantine

Quarantine data should not accumulate indefinitely. Add lifecycle rule (Terraform or Console):

```hcl
# Example lifecycle rule for quarantine prefix
lifecycle_rule {
  id      = "quarantine-expiration"
  enabled = true

  filter {
    prefix = "quarantine/"
  }

  expiration {
    days = 90
  }

  noncurrent_version_expiration {
    noncurrent_days = 30
  }
}
```

Or via AWS CLI:

```bash
# Review existing lifecycle; extend in Terraform module for production
aws s3api get-bucket-lifecycle-configuration --bucket $BUCKET
```

**Enterprise guideline:** 90-day retention for quarantine; 7-year retention for raw/compliance datasets.

---

## Step 6: Quarantine Metrics Dashboard

Track operational health:

| Metric | Source | Alert Threshold |
|--------|--------|-----------------|
| Quarantine volume (daily) | S3 inventory or custom metric | > 1% of daily ingest |
| Pending review count | `_MANIFEST.json` status=pending | > 100 records for 48h |
| Replay success rate | Replay job logs | < 95% |
| Time-to-resolution | Review timestamp − quarantine timestamp | > 72 hours |

Add to CloudWatch dashboard or QuickSight (Module 8).

---

## Deliverables

- [ ] Quarantined records uploaded with `_MANIFEST.json` and `_SUCCESS`
- [ ] Athena query returns violation breakdown
- [ ] `review_log.json` with steward decisions for all failed records
- [ ] Replay script validates and writes corrected records to cleaned zone
- [ ] `LAB-REPORT.md` documenting workflow and lifecycle policy

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Athena `HIVE_BAD_DATA` on JSON | Ensure `_violations` is valid JSON string; use JsonSerDe |
| Empty Athena results | Run `MSCK REPAIR TABLE` or use partition projection |
| Replay fails validation | Corrected values must pass all error-severity rules |
| Duplicate records in cleaned | Include `_original_quarantine_run` and dedupe in ETL merge |
| Manifest overwrite lost history | Use versioned S3 keys or append-only audit log in `metadata/` |
| `_SUCCESS` file ignored | Orchestrators (Step Functions) check this marker—ensure upload order |
| Lifecycle deletes active quarantine | Exclude `status=pending_review` paths or use tag-based lifecycle |

---

## What You Learned

- Quarantine is a first-class zone, not a logging afterthought
- Violation metadata enables self-service steward review
- Replay workflows close the loop between isolation and remediation
- Retention policies balance storage cost with audit requirements

---

**Next:** [Assignment 4 – Data Quality SLAs](../../assignments/assignment-04.md)
