#!/usr/bin/env python3
"""
Lab 9.2: AI-ready feature pipeline with offline feature store patterns.

Reads feature definitions from feature_registry.json, computes feature groups
from curated sample data, and writes versioned Parquet to ml/features/.
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


def load_registry(path: Path) -> dict[str, Any]:
    with open(path) as f:
        return json.load(f)


def load_orders(path: Path | None) -> pd.DataFrame:
    if path and path.exists():
        with open(path) as f:
            data = json.load(f)
        df = pd.DataFrame(data if isinstance(data, list) else data.get("records", []))
    else:
        import random

        random.seed(42)
        categories = ["electronics", "apparel", "home", "books", "sports"]
        base = datetime(2024, 1, 1, tzinfo=timezone.utc)
        records = []
        for i in range(1500):
            records.append(
                {
                    "order_id": f"ORD-{i:06d}",
                    "customer_id": f"CUST-{random.randint(1, 150):05d}",
                    "product_id": f"PROD-{random.randint(1, 80):04d}",
                    "order_date": (base + timedelta(days=random.randint(0, 300))).isoformat(),
                    "order_amount": round(random.uniform(10, 400), 2),
                    "product_category": random.choice(categories),
                }
            )
        df = pd.DataFrame(records)
    df["order_date"] = pd.to_datetime(df["order_date"], utc=True)
    return df


def load_products(path: Path | None) -> pd.DataFrame:
    if path and path.exists():
        with open(path) as f:
            data = json.load(f)
        return pd.DataFrame(data if isinstance(data, list) else data.get("records", []))

    import random

    random.seed(7)
    categories = ["electronics", "apparel", "home", "books", "sports"]
    records = []
    for i in range(80):
        price = round(random.uniform(5, 500), 2)
        records.append(
            {
                "product_id": f"PROD-{i+1:04d}",
                "category": random.choice(categories),
                "price": price,
                "avg_rating": round(random.uniform(2.5, 5.0), 1),
            }
        )
    return pd.DataFrame(records)


def compute_customer_behavior(orders: pd.DataFrame, snapshot: datetime) -> pd.DataFrame:
    window_start = snapshot - timedelta(days=30)
    w = orders[(orders["order_date"] >= window_start) & (orders["order_date"] < snapshot)]
    if w.empty:
        return pd.DataFrame(columns=["customer_id"])

    agg = (
        w.groupby("customer_id")
        .agg(
            order_count_30d=("order_id", "count"),
            total_spend_30d=("order_amount", "sum"),
            avg_order_value_30d=("order_amount", "mean"),
            last_order=("order_date", "max"),
            distinct_categories_30d=("product_category", "nunique"),
        )
        .reset_index()
    )
    agg["days_since_last_order"] = (snapshot - agg["last_order"]).dt.days
    agg = agg.drop(columns=["last_order"])

    preferred = (
        w.groupby(["customer_id", "product_category"])
        .size()
        .reset_index(name="cnt")
        .sort_values("cnt", ascending=False)
        .drop_duplicates("customer_id")
        .rename(columns={"product_category": "preferred_category"})
        [["customer_id", "preferred_category"]]
    )
    return agg.merge(preferred, on="customer_id", how="left")


def compute_product_catalog(products: pd.DataFrame) -> pd.DataFrame:
    df = products.copy()
    p33, p66 = df["price"].quantile([0.33, 0.66])

    def tier(price: float) -> str:
        if price <= p33:
            return "budget"
        if price <= p66:
            return "mid"
        return "premium"

    df["price_tier"] = df["price"].apply(tier)
    return df[["product_id", "category", "price_tier", "avg_rating"]]


def write_feature_group(
    df: pd.DataFrame,
    group_name: str,
    version: str,
    output_dir: Path,
    snapshot: datetime,
) -> dict[str, Any]:
    run_id = snapshot.strftime("%Y%m%dT%H%M%SZ")
    group_dir = output_dir / group_name / f"v={version}" / f"snapshot={run_id}"
    group_dir.mkdir(parents=True, exist_ok=True)

    path = group_dir / "features.parquet"
    df["feature_snapshot_ts"] = snapshot.isoformat()
    df["feature_group"] = group_name
    df["feature_version"] = version
    df.to_parquet(path, index=False)

    meta = {
        "feature_group": group_name,
        "version": version,
        "snapshot": snapshot.isoformat(),
        "row_count": len(df),
        "path": str(path.relative_to(output_dir)),
        "columns": list(df.columns),
    }
    with open(group_dir / "metadata.json", "w") as f:
        json.dump(meta, f, indent=2)
    return meta


def main() -> None:
    parser = argparse.ArgumentParser(description="Feature store offline pipeline")
    parser.add_argument(
        "--registry",
        type=Path,
        default=Path(__file__).parent / "feature_registry.json",
    )
    parser.add_argument("--orders", type=Path, help="Curated orders JSON")
    parser.add_argument("--products", type=Path, help="Curated products JSON")
    parser.add_argument(
        "--output",
        type=Path,
        default=Path(__file__).resolve().parent.parent / "output" / "ml" / "features",
    )
    args = parser.parse_args()

    registry = load_registry(args.registry)
    orders = load_orders(args.orders)
    products = load_products(args.products)
    snapshot = datetime.now(timezone.utc).replace(hour=0, minute=0, second=0, microsecond=0)

    manifest: dict[str, Any] = {
        "pipeline_run": snapshot.isoformat(),
        "feature_groups": [],
    }

    for group in registry["feature_groups"]:
        name = group["name"]
        version = group["version"]
        if name == "customer_behavior":
            df = compute_customer_behavior(orders, snapshot)
        elif name == "product_catalog":
            df = compute_product_catalog(products)
        else:
            print(f"Skipping unknown group: {name}", file=sys.stderr)
            continue

        meta = write_feature_group(df, name, version, args.output, snapshot)
        manifest["feature_groups"].append(meta)
        print(f"Wrote {name} v{version}: {meta['row_count']} rows → {meta['path']}")

    manifest_path = args.output / "pipeline_manifest.json"
    manifest_path.parent.mkdir(parents=True, exist_ok=True)
    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2)
    print(f"Pipeline manifest: {manifest_path}")


if __name__ == "__main__":
    main()
