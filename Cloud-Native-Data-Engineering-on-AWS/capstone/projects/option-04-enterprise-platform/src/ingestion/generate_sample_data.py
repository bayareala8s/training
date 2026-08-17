#!/usr/bin/env python3
"""Generate synthetic enterprise platform sample data (orders, inventory, vendor feeds).

Includes intentional bad records so the local pipeline can demonstrate quarantine.
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "sample-data"
RNG = random.Random(7)

BUSINESS_UNITS = ["retail", "wholesale", "marketplace", "b2b"]
STATUSES = ["pending", "confirmed", "shipped", "delivered", "cancelled", "returned"]
STOCK_STATUSES = ["in_stock", "low_stock", "out_of_stock", "discontinued"]
FEED_STATUSES = ["accepted", "pending_review", "rejected", "stale"]
SKU_PREFIXES = ["EL", "AP", "HM", "SP", "GR"]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows → {path.relative_to(ROOT)}")


def sku(i: int) -> str:
    return f"SKU-{SKU_PREFIXES[(i - 1) % len(SKU_PREFIXES)]}-{i:04d}"


def gen_inventory() -> list[dict]:
    rows = []
    for i in range(1, 23):
        qoh = RNG.randint(0, 800)
        reorder = RNG.randint(10, 120)
        if qoh == 0:
            status = "out_of_stock"
        elif qoh <= reorder:
            status = "low_stock"
        else:
            status = "in_stock"
        if i == 20:
            status = "discontinued"
        rows.append(
            {
                "sku": sku(i),
                "warehouse_id": f"WH-{(i % 4) + 1:02d}",
                "quantity_on_hand": str(qoh),
                "reorder_point": str(reorder),
                "stock_status": status,
                "last_counted_at": f"2024-01-{(i % 14) + 1:02d}",
            }
        )
    rows.extend(
        [
            {
                "sku": "BADSKU",
                "warehouse_id": "WH-01",
                "quantity_on_hand": "10",
                "reorder_point": "5",
                "stock_status": "in_stock",
                "last_counted_at": "2024-01-15",
            },
            {
                "sku": "SKU-EL-0099",
                "warehouse_id": "WH-02",
                "quantity_on_hand": "-3",
                "reorder_point": "10",
                "stock_status": "in_stock",
                "last_counted_at": "2024-01-15",
            },
            {
                "sku": "SKU-AP-0098",
                "warehouse_id": "WH-03",
                "quantity_on_hand": "50",
                "reorder_point": "20",
                "stock_status": "ghost_stock",
                "last_counted_at": "2024-01-15",
            },
        ]
    )
    return rows


def gen_orders() -> list[dict]:
    rows = []
    for i in range(1, 36):
        qty = RNG.randint(1, 8)
        unit = round(RNG.uniform(5, 250), 2)
        rows.append(
            {
                "order_id": f"EO-{i:06d}",
                "customer_id": f"CUST-{(i % 18) + 1:04d}",
                "sku": sku(((i - 1) % 22) + 1),
                "order_amount": f"{unit * qty:.2f}",
                "quantity": str(qty),
                "status": STATUSES[(i - 1) % len(STATUSES)],
                "business_unit": BUSINESS_UNITS[(i - 1) % len(BUSINESS_UNITS)],
                "order_date": f"2024-01-{(i % 14) + 1:02d}",
            }
        )
    rows.extend(
        [
            {
                "order_id": "",
                "customer_id": "CUST-0001",
                "sku": "SKU-EL-0001",
                "order_amount": "20.00",
                "quantity": "1",
                "status": "pending",
                "business_unit": "retail",
                "order_date": "2024-01-15",
            },
            {
                "order_id": "EO-000991",
                "customer_id": "CUST-0002",
                "sku": "SKU-EL-0002",
                "order_amount": "-9.99",
                "quantity": "1",
                "status": "confirmed",
                "business_unit": "retail",
                "order_date": "2024-01-15",
            },
            {
                "order_id": "EO-000992",
                "customer_id": "CUST-0003",
                "sku": "SKU-AP-0003",
                "order_amount": "45.00",
                "quantity": "2",
                "status": "lost_in_space",
                "business_unit": "marketplace",
                "order_date": "2024-01-15",
            },
            {
                "order_id": "BAD-ORDER",
                "customer_id": "CUST-0004",
                "sku": "SKU-HM-0004",
                "order_amount": "30.00",
                "quantity": "1",
                "status": "shipped",
                "business_unit": "wholesale",
                "order_date": "2024-01-15",
            },
            {
                "order_id": "EO-000993",
                "customer_id": "CUST-0005",
                "sku": "SKU-SP-0005",
                "order_amount": "12.00",
                "quantity": "900",
                "status": "pending",
                "business_unit": "b2b",
                "order_date": "2024-01-15",
            },
        ]
    )
    return rows


def gen_vendor_feeds() -> list[dict]:
    rows = []
    for i in range(1, 18):
        rows.append(
            {
                "feed_id": f"VF-{i:05d}",
                "vendor_id": f"VND-{(i % 6) + 1:03d}",
                "sku": sku(((i - 1) % 22) + 1),
                "unit_cost": f"{round(RNG.uniform(2, 180), 2):.2f}",
                "feed_status": FEED_STATUSES[(i - 1) % len(FEED_STATUSES)],
                "lead_time_days": str(RNG.randint(2, 45)),
                "received_at": f"2024-01-15T{8 + (i % 10):02d}:00:00Z",
            }
        )
    rows.extend(
        [
            {
                "feed_id": "",
                "vendor_id": "VND-001",
                "sku": "SKU-EL-0001",
                "unit_cost": "10.00",
                "feed_status": "accepted",
                "lead_time_days": "5",
                "received_at": "2024-01-15T09:00:00Z",
            },
            {
                "feed_id": "VF-00991",
                "vendor_id": "VND-002",
                "sku": "SKU-EL-0002",
                "unit_cost": "-1.00",
                "feed_status": "pending_review",
                "lead_time_days": "7",
                "received_at": "2024-01-15T09:30:00Z",
            },
            {
                "feed_id": "VF-BAD",
                "vendor_id": "VND-003",
                "sku": "SKU-AP-0003",
                "unit_cost": "22.00",
                "feed_status": "corrupted",
                "lead_time_days": "3",
                "received_at": "2024-01-15T10:00:00Z",
            },
        ]
    )
    return rows


def main() -> None:
    SAMPLE.mkdir(parents=True, exist_ok=True)
    inventory = gen_inventory()
    orders = gen_orders()
    vendor_feeds = gen_vendor_feeds()

    write_csv(SAMPLE / "inventory.csv", inventory)
    write_csv(SAMPLE / "orders.csv", orders)
    (SAMPLE / "vendor_feeds.json").write_text(json.dumps(vendor_feeds, indent=2), encoding="utf-8")
    print(f"Wrote {len(vendor_feeds)} feeds → sample-data/vendor_feeds.json")
    print(
        f"Totals: inventory={len(inventory)} orders={len(orders)} vendor_feeds={len(vendor_feeds)}"
    )


if __name__ == "__main__":
    main()
