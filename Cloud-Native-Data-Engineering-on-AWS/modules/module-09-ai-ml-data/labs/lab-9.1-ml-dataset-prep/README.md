# Lab 9.1: Prepare ML Training Datasets from Curated Zone

> 📊 **Diagrams:** [Mermaid](diagram.md) · [Draw.io (lab-9.1-ml-dataset-prep.drawio)](../../../../docs/diagrams/drawio/lab-9.1-ml-dataset-prep.drawio) · [PNG](../../../../docs/diagrams/png/lab-9.1-ml-dataset-prep.png) · [SVG](../../../../docs/diagrams/svg/lab-9.1-ml-dataset-prep.svg)

**Estimated time:** 120 minutes · **Module 9**

---

## Objectives

- Extract business-ready data from the curated zone for ML consumption
- Engineer point-in-time customer behavior features
- Create temporal train/validation/test splits (avoid leakage)
- Generate a dataset manifest documenting features and label definitions
- Write ML-ready Parquet files to S3 or local output

---

## Prerequisites

- Modules 1–4 complete (curated orders data in S3 or sample data)
- Python 3.10+ with virtual environment
- `pip install pandas pyarrow boto3`

---

## Architecture

```text
curated/sales/fact_orders/ (S3 or local JSON/Parquet)
              │
              ▼
    prepare_ml_dataset.py
    ├── Point-in-time feature engineering
    ├── Label: will_purchase_again_30d
    └── Temporal train / val / test split
              │
              ▼
    output/
    ├── train.parquet
    ├── validation.parquet
    ├── test.parquet
    └── dataset_manifest.json
```

---

## Project Structure

```text
lab-9.1-ml-dataset-prep/
├── README.md
├── src/
│   └── prepare_ml_dataset.py
├── sample-data/
│   └── curated_orders_sample.json   (optional – script generates if missing)
└── output/                          (created at runtime)
```

---

## Step 1: Review Feature Engineering Logic

Open `src/prepare_ml_dataset.py`. Key design decisions:

| Feature | Definition | Leakage Risk |
|---------|------------|--------------|
| `order_count_30d` | Orders in 30 days before snapshot | Low (past window) |
| `total_spend_30d` | Sum of order amounts in window | Low |
| `days_since_last_order` | Days from last order to snapshot | Low |
| `will_purchase_again_30d` | Label: order in next 30 days | Target only |

**Point-in-time:** Features use `[snapshot - 30d, snapshot)`; labels use `[snapshot, snapshot + 30d)`.

---

## Step 2: Run Locally with Sample Data

```bash
cd modules/module-09-ai-ml-data/labs/lab-9.1-ml-dataset-prep

python3 src/prepare_ml_dataset.py --snapshots 12
```

Expected output:

```text
Wrote output/train.parquet (N rows, pos rate=0.xxxx)
Wrote output/validation.parquet (...)
Wrote output/test.parquet (...)
Wrote output/dataset_manifest.json
```

Inspect the manifest:

```bash
python3 -m json.tool output/dataset_manifest.json
```

---

## Step 3: Run Against Curated S3 Data

If you have curated orders in your data lake from Module 3:

```bash
export BUCKET=$(cd ../../../../infrastructure/environments/dev && terraform output -raw data_lake_bucket)

# Download curated sample (adjust path to your deployment)
aws s3 cp s3://$BUCKET/curated/sales/fact_orders/ ./sample-data/ --recursive --exclude "*" --include "*.json"

python3 src/prepare_ml_dataset.py \
  --input sample-data/orders.json \
  --output output/
```

Or query via Athena, export to CSV, convert to JSON/Parquet, and pass `--input`.

---

## Step 4: Validate Splits

Run validation checks:

```bash
python3 << 'EOF'
import pandas as pd
from pathlib import Path

out = Path("output")
for split in ["train", "validation", "test"]:
    df = pd.read_parquet(out / f"{split}.parquet")
    assert df["customer_id"].notna().all(), f"{split}: null customer_id"
    assert df["will_purchase_again_30d"].isin([0, 1]).all(), f"{split}: invalid labels"
    print(f"{split}: {len(df)} rows, label rate={df['will_purchase_again_30d'].mean():.3f}")

# Temporal: no snapshot overlap between splits
train = pd.read_parquet(out / "train.parquet")
test = pd.read_parquet(out / "test.parquet")
train_snaps = set(train["snapshot_date"])
test_snaps = set(test["snapshot_date"])
assert train_snaps.isdisjoint(test_snaps), "Temporal leakage: overlapping snapshots"
print("Temporal split validation passed.")
EOF
```

---

## Step 5: Upload to ML Zone in S3

```bash
export BUCKET=$(cd ../../../../infrastructure/environments/dev && terraform output -raw data_lake_bucket)

aws s3 sync output/ s3://$BUCKET/ml/training/customer-churn/v1/ \
  --exclude "*" --include "*.parquet" --include "dataset_manifest.json"
```

Verify:

```bash
aws s3 ls s3://$BUCKET/ml/training/customer-churn/v1/
```

---

## Step 6: Document Dataset Lineage

Create `DATASET-CARD.md` in this folder:

```markdown
# Dataset Card: Customer Repeat Purchase (v1)

## Purpose
Predict whether a customer will purchase again within 30 days.

## Source
- Curated: s3://<bucket>/curated/sales/fact_orders/
- Script: prepare_ml_dataset.py

## Features
| Name | Type | Description |
|------|------|-------------|
| order_count_30d | int | ... |

## Label
- `will_purchase_again_30d`: binary, 1 if ≥1 order in next 30 days

## Splits
- Temporal weekly snapshots; 70/15/15 train/val/test

## Known Limitations
- Synthetic/sample data for lab; production needs category encoding

## Owner
<your name>
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| `ModuleNotFoundError: pandas` | `pip install pandas pyarrow` |
| Empty feature rows | Check date parsing; verify orders span snapshot range |
| High label imbalance | Document in dataset card; consider stratified sampling in production |
| S3 path not found | Confirm curated ETL completed; use `--input` with local sample |

---

## What You Learned

- Curated-to-ML dataset transformation
- Point-in-time feature engineering without leakage
- Temporal splitting for time-series ML data
- Dataset manifests for reproducibility

**Next:** [Lab 9.2 – Feature Store Pipeline](../lab-9.2-feature-store-pipeline/README.md)
