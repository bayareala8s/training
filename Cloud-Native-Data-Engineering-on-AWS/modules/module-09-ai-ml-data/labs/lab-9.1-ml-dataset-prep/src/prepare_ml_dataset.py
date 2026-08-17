#!/usr/bin/env python3
"""
Lab 9.1: Prepare ML training datasets from curated zone data.

Reads curated orders Parquet/JSON from local sample data or S3,
engineers features, performs temporal train/val/test split, and
writes ML-ready datasets to output/.
"""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Any

try:
    import pandas as pd
except ImportError:
    print("Install dependencies: pip install pandas pyarrow", file=sys.stderr)
    sys.exit(1)


DEFAULT_FEATURES = [
    "customer_id",
    "order_count_30d",
    "total_spend_30d",
    "avg_order_value_30d",
    "days_since_last_order",
    "distinct_categories_30d",
    "order_day_of_week",
    "is_weekend",
]

LABEL_COLUMN = "will_purchase_again_30d"


def load_orders(path: Path) -> pd.DataFrame:
    """Load orders from JSON or Parquet."""
    if path.suffix == ".parquet":
        return pd.read_parquet(path)
    if path.suffix == ".json":
        with open(path) as f:
            data = json.load(f)
        return pd.DataFrame(data if isinstance(data, list) else data.get("records", []))
    raise ValueError(f"Unsupported format: {path}")


def parse_dates(df: pd.DataFrame, date_col: str = "order_date") -> pd.DataFrame:
    df = df.copy()
    df[date_col] = pd.to_datetime(df[date_col], utc=True)
    return df


def compute_customer_features(
    orders: pd.DataFrame,
    snapshot_date: datetime,
    lookback_days: int = 30,
) -> pd.DataFrame:
    """Point-in-time features as of snapshot_date."""
    window_start = snapshot_date - timedelta(days=lookback_days)
    window_end = snapshot_date

    mask = (orders["order_date"] >= window_start) & (orders["order_date"] < window_end)
    window = orders.loc[mask].copy()

    if window.empty:
        return pd.DataFrame(
            columns=[
                "customer_id",
                "order_count_30d",
                "total_spend_30d",
                "avg_order_value_30d",
                "days_since_last_order",
                "distinct_categories_30d",
            ]
        )

    agg = (
        window.groupby("customer_id")
        .agg(
            order_count_30d=("order_id", "count"),
            total_spend_30d=("order_amount", "sum"),
            avg_order_value_30d=("order_amount", "mean"),
            last_order_date=("order_date", "max"),
            distinct_categories_30d=("product_category", "nunique"),
        )
        .reset_index()
    )

    agg["days_since_last_order"] = (
        snapshot_date - agg["last_order_date"]
    ).dt.days
    agg = agg.drop(columns=["last_order_date"])
    return agg


def compute_labels(
    orders: pd.DataFrame,
    snapshot_date: datetime,
    horizon_days: int = 30,
) -> pd.DataFrame:
    """Label: customer places at least one order in next horizon_days."""
    future_start = snapshot_date
    future_end = snapshot_date + timedelta(days=horizon_days)
    future = orders[
        (orders["order_date"] >= future_start) & (orders["order_date"] < future_end)
    ]
    purchasers = future.groupby("customer_id").size().reset_index(name="_count")
    purchasers[LABEL_COLUMN] = 1
    return purchasers[["customer_id", LABEL_COLUMN]]


def temporal_split(
    df: pd.DataFrame,
    snapshot_dates: list[datetime],
    train_ratio: float = 0.7,
    val_ratio: float = 0.15,
) -> dict[str, pd.DataFrame]:
    """Split by snapshot date (temporal, not random)."""
    sorted_dates = sorted(snapshot_dates)
    n = len(sorted_dates)
    train_end = int(n * train_ratio)
    val_end = train_end + int(n * val_ratio)

    train_keys = {d.isoformat() for d in sorted_dates[:train_end]}
    val_keys = {d.isoformat() for d in sorted_dates[train_end:val_end]}
    test_keys = {d.isoformat() for d in sorted_dates[val_end:]}

    return {
        "train": df[df["snapshot_date"].isin(train_keys)],
        "validation": df[df["snapshot_date"].isin(val_keys)],
        "test": df[df["snapshot_date"].isin(test_keys)],
    }


def build_training_dataset(
    orders: pd.DataFrame,
    snapshot_dates: list[datetime],
) -> pd.DataFrame:
    rows: list[dict[str, Any]] = []
    for snap in snapshot_dates:
        features = compute_customer_features(orders, snap)
        labels = compute_labels(orders, snap)
        merged = features.merge(labels, on="customer_id", how="left")
        merged[LABEL_COLUMN] = merged[LABEL_COLUMN].fillna(0).astype(int)
        merged["snapshot_date"] = snap.isoformat()
        merged["order_day_of_week"] = snap.weekday()
        merged["is_weekend"] = int(snap.weekday() >= 5)
        rows.append(merged)
    return pd.concat(rows, ignore_index=True)


def generate_sample_orders(n_customers: int = 200, n_orders: int = 2000) -> pd.DataFrame:
    """Generate synthetic orders when no input file is provided."""
    import random

    random.seed(42)
    categories = ["electronics", "apparel", "home", "books", "sports"]
    base = datetime(2024, 1, 1, tzinfo=timezone.utc)
    records = []
    for i in range(n_orders):
        cust = f"CUST-{random.randint(1, n_customers):05d}"
        day_offset = random.randint(0, 364)
        records.append(
            {
                "order_id": f"ORD-{i:06d}",
                "customer_id": cust,
                "order_date": (base + timedelta(days=day_offset)).isoformat(),
                "order_amount": round(random.uniform(10, 500), 2),
                "product_category": random.choice(categories),
                "status": random.choice(["delivered", "shipped", "pending"]),
            }
        )
    return pd.DataFrame(records)


def write_outputs(splits: dict[str, pd.DataFrame], output_dir: Path, feature_cols: list[str]) -> None:
    output_dir.mkdir(parents=True, exist_ok=True)
    manifest = {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "label_column": LABEL_COLUMN,
        "feature_columns": feature_cols,
        "splits": {},
    }
    for name, df in splits.items():
        path = output_dir / f"{name}.parquet"
        export_cols = feature_cols + [LABEL_COLUMN, "snapshot_date"]
        df[export_cols].to_parquet(path, index=False)
        manifest["splits"][name] = {
            "path": str(path.name),
            "rows": len(df),
            "label_positive_rate": round(df[LABEL_COLUMN].mean(), 4) if len(df) else 0,
        }
        print(f"Wrote {path} ({len(df)} rows, pos rate={manifest['splits'][name]['label_positive_rate']})")

    with open(output_dir / "dataset_manifest.json", "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Wrote {output_dir / 'dataset_manifest.json'}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Prepare ML training datasets from curated orders")
    parser.add_argument(
        "--input",
        type=Path,
        help="Path to curated orders JSON or Parquet (optional; generates sample if omitted)",
    )
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "output",
        help="Output directory for train/val/test Parquet files",
    )
    parser.add_argument("--snapshots", type=int, default=12, help="Number of weekly snapshot dates")
    args = parser.parse_args()

    if args.input and args.input.exists():
        orders = load_orders(args.input)
    else:
        print("No input file; generating sample orders data.")
        orders = generate_sample_orders()

    orders = parse_dates(orders)

    base_snapshot = datetime(2024, 6, 1, tzinfo=timezone.utc)
    snapshot_dates = [base_snapshot + timedelta(weeks=i) for i in range(args.snapshots)]

    dataset = build_training_dataset(orders, snapshot_dates)
    splits = temporal_split(dataset, snapshot_dates)
    write_outputs(splits, args.output, DEFAULT_FEATURES)

    print("\nDataset preparation complete.")
    print(f"  Total feature rows: {len(dataset)}")
    print(f"  Train: {len(splits['train'])} | Val: {len(splits['validation'])} | Test: {len(splits['test'])}")


if __name__ == "__main__":
    main()
