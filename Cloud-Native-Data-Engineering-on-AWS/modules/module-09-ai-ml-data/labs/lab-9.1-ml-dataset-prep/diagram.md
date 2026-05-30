# Lab 9.1 Architecture: ML Training Dataset Preparation

Transform curated business data into point-in-time ML features with temporal train/validation/test splits, producing Parquet datasets and a manifest for reproducible model training.

---

## Architecture Diagram

```mermaid
flowchart TB
    subgraph Source["Curated Zone"]
        CUR[(S3 curated/sales/fact_orders/<br/>or local sample JSON)]
    end

    subgraph Processing["Feature Engineering"]
        SCRIPT[prepare_ml_dataset.py]
        PIT[Point-in-Time Windows<br/>features: snapshot - 30d<br/>labels: snapshot + 30d]
        SPLIT[Temporal Split<br/>70/15/15 train/val/test]
    end

    subgraph Output["ML Training Artifacts"]
        TRAIN[train.parquet]
        VAL[validation.parquet]
        TEST[test.parquet]
        MAN[dataset_manifest.json]
    end

    subgraph MLZone["S3 ML Zone"]
        S3ML[(s3://bucket/ml/training/<br/>customer-churn/v1/)]
    end

    CUR --> SCRIPT
    SCRIPT --> PIT --> SPLIT
    SPLIT --> TRAIN & VAL & TEST & MAN
    TRAIN & VAL & TEST & MAN --> S3ML
```

---

## Key Components

| Component | Artifact / Path | Role in Lab |
|-----------|-----------------|-------------|
| Source Data | `curated/sales/fact_orders/` | Business-ready orders from Module 3 ETL |
| Prep Script | `src/prepare_ml_dataset.py` | Feature engineering, labeling, splitting |
| Entity Key | `customer_id` | One row per customer per snapshot |
| Snapshot Date | `snapshot_date` | Temporal anchor for point-in-time features |
| Label | `will_purchase_again_30d` | Binary target: order in next 30 days |
| Features | `order_count_30d`, `total_spend_30d`, `days_since_last_order` | Past-window aggregates (no leakage) |
| Train Split | `output/train.parquet` | 70% of snapshots (earliest) |
| Validation Split | `output/validation.parquet` | 15% middle snapshots |
| Test Split | `output/test.parquet` | 15% latest snapshots |
| Dataset Manifest | `output/dataset_manifest.json` | Feature definitions, split stats, lineage |
| Dataset Card | `DATASET-CARD.md` | Human-readable documentation for ML team |

---

## Data Flows

### Flow 1: Point-in-Time Feature Engineering

| Window | Time Range | Used For |
|--------|------------|----------|
| Feature window | `[snapshot - 30d, snapshot)` | `order_count_30d`, `total_spend_30d`, `days_since_last_order` |
| Label window | `[snapshot, snapshot + 30d)` | `will_purchase_again_30d` |

```mermaid
sequenceDiagram
    participant Orders as fact_orders
    participant Script as prepare_ml_dataset.py
    participant Out as Parquet + Manifest

    Orders->>Script: Load order history
    loop Each weekly snapshot
        Script->>Script: Aggregate features (past 30d)
        Script->>Script: Compute label (future 30d)
    end
    Script->>Script: Assign snapshots to train/val/test
    Script->>Out: Write splits + manifest
```

### Flow 2: Temporal Split (Leakage Prevention)

| Split | Snapshot Assignment | Rule |
|-------|---------------------|------|
| Train | Earliest 70% of snapshot dates | No overlap with val/test |
| Validation | Next 15% | Disjoint snapshot sets |
| Test | Latest 15% | Simulates future prediction |

**Validation check:** `train_snaps.isdisjoint(test_snaps)` must pass.

### Flow 3: Upload to ML Zone

| Step | Action | S3 Path |
|------|--------|---------|
| 1 | `aws s3 sync output/` | `ml/training/customer-churn/v1/` |
| 2 | Include `.parquet` + manifest | Versioned training bundle |
| 3 | Verify with `aws s3 ls` | Ready for Lab 9.2 / SageMaker |

---

## Feature → Label Relationship

```mermaid
flowchart LR
    subgraph Past["Feature Window (known at snapshot)"]
        F1[order_count_30d]
        F2[total_spend_30d]
        F3[days_since_last_order]
    end

    SNAP((snapshot_date))

    subgraph Future["Label Window (unknown at training inference time)"]
        L[will_purchase_again_30d]
    end

    Past --> SNAP
    SNAP --> Future
```

---

## Downstream Consumers

| Consumer | Uses | Lab |
|----------|------|-----|
| Feature pipeline | Same entity key, richer feature groups | Lab 9.2 |
| AI quality validator | train.parquet + test.parquet | Lab 9.3 |
| SageMaker Training | S3 Parquet input | Assignment 9 / Capstone |
