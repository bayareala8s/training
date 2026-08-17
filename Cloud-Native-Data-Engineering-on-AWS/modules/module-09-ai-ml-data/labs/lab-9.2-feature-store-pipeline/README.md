# Lab 9.2: AI-Ready Pipeline with Feature Store Patterns

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-9.2-feature-store-pipeline.drawio)](../../../../docs/diagrams/drawio/lab-9.2-feature-store-pipeline.drawio) · [PNG](../../../../docs/diagrams/png/lab-9.2-feature-store-pipeline.png) · [SVG](../../../../docs/diagrams/svg/lab-9.2-feature-store-pipeline.svg)

**Estimated time:** 120 minutes · **Module 9**

---

## Objectives

- Define feature groups in a versioned feature registry
- Build an offline feature pipeline that writes to `ml/features/`
- Implement feature group metadata and pipeline manifests
- Understand how this pattern maps to SageMaker Feature Store in production
- Upload feature artifacts to S3 with partition conventions

---

## Prerequisites

- Lab 9.1 complete (understand point-in-time features)
- Python 3.10+ with `pandas`, `pyarrow`, `boto3`
- Curated orders data (optional; script generates sample data)

---

## Architecture

```text
feature_registry.json
        │
        ▼
feature_pipeline.py
        │
        ├── customer_behavior/  (entity: customer_id)
        │     v=1.0.0/snapshot=.../features.parquet
        │
        └── product_catalog/    (entity: product_id)
              v=1.0.0/snapshot=.../features.parquet
        │
        ▼
pipeline_manifest.json
        │
        ▼
s3://bucket/ml/features/  (offline store)
```

---

## Project Structure

```text
lab-9.2-feature-store-pipeline/
├── README.md
├── src/
│   ├── feature_registry.json
│   └── feature_pipeline.py
└── output/
    └── ml/features/
```

---

## Step 1: Review Feature Registry

Open `src/feature_registry.json`. Each feature group defines:

- **Entity key** — Join column for training/inference
- **Features** — Name, dtype, computation description
- **Freshness SLA** — Maximum staleness before recompute
- **Source datasets** — Lineage back to curated zone

This file is the **contract** between data engineering and ML teams.

---

## Step 2: Run Feature Pipeline

```bash
cd modules/module-09-ai-ml-data/labs/lab-9.2-feature-store-pipeline

python3 src/feature_pipeline.py
```

Expected structure:

```text
output/ml/features/
├── customer_behavior/v=1.0.0/snapshot=YYYYMMDDTHHMMSSZ/
│   ├── features.parquet
│   └── metadata.json
├── product_catalog/v=1.0.0/snapshot=YYYYMMDDTHHMMSSZ/
│   ├── features.parquet
│   └── metadata.json
└── pipeline_manifest.json
```

Inspect manifest:

```bash
python3 -m json.tool output/ml/features/pipeline_manifest.json
```

---

## Step 3: Validate Feature Outputs

```bash
python3 << 'EOF'
import json
import pandas as pd
from pathlib import Path

base = Path("output/ml/features")
with open(base / "pipeline_manifest.json") as f:
    manifest = json.load(f)

for group in manifest["feature_groups"]:
    path = base / group["path"]
    df = pd.read_parquet(path)
    print(f"\n{group['feature_group']}: {len(df)} rows")
    print(f"  Columns: {list(df.columns)}")
    assert "feature_snapshot_ts" in df.columns
    assert "feature_version" in df.columns
    print("  Schema checks passed.")
EOF
```

---

## Step 4: Upload to S3 Offline Store

```bash
export BUCKET=$(cd ../../../../infrastructure/environments/dev && terraform output -raw data_lake_bucket)

aws s3 sync output/ml/features/ s3://$BUCKET/ml/features/ \
  --exclude "*.pyc"
```

Verify partition layout:

```bash
aws s3 ls s3://$BUCKET/ml/features/ --recursive | head -20
```

---

## Step 5: Schedule with EventBridge (Conceptual)

In production, trigger the feature pipeline after curated ETL completes:

```text
Glue ETL Success Event
        │
        ▼
EventBridge Rule (source: aws.glue, detail-type: Glue Job State Change)
        │
        ▼
Lambda or Step Functions → feature_pipeline.py
        │
        ▼
S3 ml/features/ updated → SNS notify ML team
```

Document your proposed schedule in `SCHEDULING-NOTES.md`:

- Trigger: daily after `cnde-orders-etl` succeeds
- Idempotency: snapshot timestamp in path prevents overwrite collisions
- Backfill: re-run with historical `--snapshot` flag (extension exercise)

---

## Step 6: Map to SageMaker Feature Store

Complete this comparison table in your lab report:

| Course Pattern | SageMaker Feature Store Equivalent |
|----------------|-----------------------------------|
| `feature_registry.json` | Feature group definition in API |
| `ml/features/` Parquet | Offline store (S3) |
| `metadata.json` per run | Record ingestion metadata |
| Entity key column | Record identifier |
| `feature_snapshot_ts` | Event time for point-in-time queries |
| DynamoDB (not implemented) | Online store for real-time inference |

---

## Step 7: Lab Report

Create `LAB-REPORT.md`:

```markdown
# Lab 9.2 Report

## Feature Groups Deployed
- customer_behavior v1.0.0: <row count>
- product_catalog v1.0.0: <row count>

## S3 Path
s3://<bucket>/ml/features/

## Scheduling Design
<Link to SCHEDULING-NOTES.md>

## SageMaker Mapping
<Completed comparison table>

## Training/Serving Skew Prevention
How does the registry prevent duplicate feature logic?
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| Empty customer_behavior group | Expand sample date range or pass real orders file |
| Version path conflicts | Each run uses new snapshot timestamp |
| Registry/schema mismatch | Align feature names in registry with pipeline output |

---

## What You Learned

- Feature registry as ML data contract
- Offline feature store layout on S3
- Versioned, snapshot-partitioned feature artifacts
- Bridge from course patterns to SageMaker Feature Store

**Next:** [Lab 9.3 – AI Data Quality Validation](../lab-9.3-ai-data-quality/README.md)
