#!/usr/bin/env python3
"""Generate synthetic retail order data for Module 1 labs."""

import argparse
import csv
import random
from datetime import datetime, timedelta
from pathlib import Path

STATUSES = ["pending", "shipped", "delivered", "cancelled"]
CATEGORIES = ["electronics", "clothing", "home", "books", "sports"]


def generate_orders(count: int, base_date: str) -> list[dict]:
    base = datetime.strptime(base_date, "%Y-%m-%d")
    orders = []
    for i in range(1, count + 1):
        order_date = base + timedelta(hours=random.randint(0, 23), minutes=random.randint(0, 59))
        quantity = random.randint(1, 5)
        unit_price = round(random.uniform(9.99, 499.99), 2)
        orders.append({
            "order_id": f"ORD-{base_date.replace('-', '')}-{i:05d}",
            "customer_id": f"CUST-{random.randint(1000, 9999)}",
            "product_category": random.choice(CATEGORIES),
            "quantity": quantity,
            "unit_price": unit_price,
            "total_amount": round(quantity * unit_price, 2),
            "order_status": random.choice(STATUSES),
            "order_timestamp": order_date.isoformat(),
            "region": random.choice(["us-west", "us-east", "eu-central", "ap-south"]),
        })
    return orders


def main():
    parser = argparse.ArgumentParser(description="Generate sample order CSV")
    parser.add_argument("--count", type=int, default=1000)
    parser.add_argument("--date", default="2024-01-15")
    parser.add_argument("--output-dir", default="sample-data")
    args = parser.parse_args()

    out_dir = Path(args.output_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    out_file = out_dir / f"orders_{args.date}.csv"

    orders = generate_orders(args.count, args.date)
    fieldnames = list(orders[0].keys())

    with open(out_file, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(orders)

    print(f"Generated {len(orders)} orders → {out_file}")


if __name__ == "__main__":
    main()
