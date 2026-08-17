#!/usr/bin/env python3
"""Generate synthetic e-commerce sample data (orders, products, customers, clickstream).

Includes intentional bad records so the local pipeline can demonstrate quarantine.
"""

from __future__ import annotations

import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
SAMPLE = ROOT / "sample-data"
RNG = random.Random(42)

CATEGORIES = ["electronics", "apparel", "home", "beauty", "sports", "grocery"]
BRANDS = ["Northpeak", "Lumen", "HarborHome", "Vivid", "AeroFit", "FreshDay"]
SEGMENTS = ["new", "loyal", "vip", "churn_risk", "wholesale"]
REGIONS = ["us-east", "us-west", "eu-west", "ap-south", "latam"]
STATUSES = ["pending", "shipped", "delivered", "cancelled", "returned"]
CHANNELS = ["web", "mobile", "marketplace", "store"]
DEVICES = ["desktop", "mobile", "tablet"]
EVENTS = ["page_view", "add_to_cart", "remove_from_cart", "checkout_start", "purchase", "search"]
PAGES = ["/", "/search", "/p/detail", "/cart", "/checkout", "/account", "/deals"]


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows → {path.relative_to(ROOT)}")


def gen_products() -> list[dict]:
    rows = []
    for i in range(1, 15):
        rows.append(
            {
                "product_id": f"PRD-{i:04d}",
                "product_name": f"{RNG.choice(BRANDS)} Item {i}",
                "category": CATEGORIES[(i - 1) % len(CATEGORIES)],
                "brand": RNG.choice(BRANDS),
                "unit_price": round(RNG.uniform(8, 450), 2),
                "is_active": "true" if i != 12 else "false",
            }
        )
    # Bad: invalid category, bad id, negative price
    rows.append(
        {
            "product_id": "PRD-0099",
            "product_name": "Broken Catalog Entry",
            "category": "toys",
            "brand": "Unknown",
            "unit_price": "12.50",
            "is_active": "true",
        }
    )
    rows.append(
        {
            "product_id": "BAD-PROD",
            "product_name": "Bad ID Product",
            "category": "electronics",
            "brand": "Lumen",
            "unit_price": "99.00",
            "is_active": "true",
        }
    )
    rows.append(
        {
            "product_id": "PRD-0098",
            "product_name": "Negative Price Widget",
            "category": "home",
            "brand": "HarborHome",
            "unit_price": "-5.00",
            "is_active": "true",
        }
    )
    return rows


def gen_customers() -> list[dict]:
    rows = []
    for i in range(1, 19):
        rows.append(
            {
                "customer_id": f"CUST-{i:04d}",
                "email": f"shopper{i}@example.com",
                "segment": SEGMENTS[(i - 1) % len(SEGMENTS)],
                "region": REGIONS[(i - 1) % len(REGIONS)],
                "signup_date": f"2023-{(i % 12) + 1:02d}-{((i * 3) % 27) + 1:02d}",
                "lifetime_orders": str(RNG.randint(0, 40)),
            }
        )
    rows.append(
        {
            "customer_id": "CUST-0099",
            "email": "not-an-email",
            "segment": "loyal",
            "region": "us-east",
            "signup_date": "2023-05-01",
            "lifetime_orders": "3",
        }
    )
    rows.append(
        {
            "customer_id": "CUSTX-1",
            "email": "odd@example.com",
            "segment": "platinum",
            "region": "us-west",
            "signup_date": "2022-11-11",
            "lifetime_orders": "8",
        }
    )
    return rows


def gen_orders(products: list[dict], customers: list[dict]) -> list[dict]:
    good_products = [p for p in products if str(p["product_id"]).startswith("PRD-") and p["category"] in CATEGORIES]
    good_customers = [c for c in customers if str(c["customer_id"]).startswith("CUST-") and "@" in c["email"] and c["email"].endswith(".com")]
    rows = []
    for i in range(1, 36):
        p = good_products[(i - 1) % len(good_products)]
        c = good_customers[(i - 1) % len(good_customers)]
        qty = RNG.randint(1, 5)
        unit = float(p["unit_price"])
        rows.append(
            {
                "order_id": f"ORD-{i:05d}",
                "customer_id": c["customer_id"],
                "product_id": p["product_id"],
                "order_amount": f"{unit * qty:.2f}",
                "quantity": str(qty),
                "status": STATUSES[(i - 1) % len(STATUSES)],
                "channel": CHANNELS[(i - 1) % len(CHANNELS)],
                "order_date": f"2024-01-{(i % 14) + 1:02d}",
            }
        )
    # Bad records for quarantine demo
    rows.extend(
        [
            {
                "order_id": "",
                "customer_id": "CUST-0001",
                "product_id": "PRD-0001",
                "order_amount": "25.00",
                "quantity": "1",
                "status": "pending",
                "channel": "web",
                "order_date": "2024-01-15",
            },
            {
                "order_id": "ORD-00991",
                "customer_id": "CUST-0002",
                "product_id": "PRD-0002",
                "order_amount": "-12.50",
                "quantity": "1",
                "status": "shipped",
                "channel": "web",
                "order_date": "2024-01-15",
            },
            {
                "order_id": "ORD-00992",
                "customer_id": "CUST-0003",
                "product_id": "PRD-0003",
                "order_amount": "40.00",
                "quantity": "2",
                "status": "exploded",
                "channel": "mobile",
                "order_date": "2024-01-15",
            },
            {
                "order_id": "BAD-ID",
                "customer_id": "CUST-0004",
                "product_id": "PRD-0004",
                "order_amount": "15.00",
                "quantity": "1",
                "status": "delivered",
                "channel": "store",
                "order_date": "2024-01-15",
            },
            {
                "order_id": "ORD-00993",
                "customer_id": "CUST-0005",
                "product_id": "PRD-0005",
                "order_amount": "10.00",
                "quantity": "999",
                "status": "pending",
                "channel": "web",
                "order_date": "2024-01-15",
            },
        ]
    )
    return rows


def gen_clickstream(customers: list[dict], products: list[dict]) -> list[dict]:
    good_customers = [c["customer_id"] for c in customers if str(c["customer_id"]).startswith("CUST-0")]
    good_products = [p["product_id"] for p in products if str(p["product_id"]).startswith("PRD-0")]
    rows = []
    for i in range(1, 28):
        rows.append(
            {
                "event_id": f"EVT-{i:05d}",
                "session_id": f"SES-{(i % 9) + 1:04d}",
                "customer_id": good_customers[(i - 1) % len(good_customers)],
                "product_id": good_products[(i - 1) % len(good_products)] if i % 3 else "",
                "event_type": EVENTS[(i - 1) % len(EVENTS)],
                "device": DEVICES[(i - 1) % len(DEVICES)],
                "page_path": PAGES[(i - 1) % len(PAGES)],
                "event_ts": f"2024-01-15T{10 + (i % 8):02d}:{i % 60:02d}:00Z",
            }
        )
    rows.extend(
        [
            {
                "event_id": "",
                "session_id": "SES-0099",
                "customer_id": "CUST-0001",
                "product_id": "PRD-0001",
                "event_type": "page_view",
                "device": "desktop",
                "page_path": "/home",
                "event_ts": "2024-01-15T12:00:00Z",
            },
            {
                "event_id": "EVT-00991",
                "session_id": "SES-0098",
                "customer_id": "CUST-0002",
                "product_id": "PRD-0002",
                "event_type": "hover_heatmap",
                "device": "desktop",
                "page_path": "/p/detail",
                "event_ts": "2024-01-15T12:05:00Z",
            },
            {
                "event_id": "EVT-BAD",
                "session_id": "SES-0097",
                "customer_id": "CUST-0003",
                "product_id": "",
                "event_type": "purchase",
                "device": "phablet",
                "page_path": "/checkout",
                "event_ts": "2024-01-15T12:10:00Z",
            },
        ]
    )
    return rows


def main() -> None:
    SAMPLE.mkdir(parents=True, exist_ok=True)
    products = gen_products()
    customers = gen_customers()
    orders = gen_orders(products, customers)
    clickstream = gen_clickstream(customers, products)

    write_csv(SAMPLE / "products.csv", products)
    write_csv(SAMPLE / "customers.csv", customers)
    write_csv(SAMPLE / "orders.csv", orders)
    (SAMPLE / "clickstream.json").write_text(json.dumps(clickstream, indent=2), encoding="utf-8")
    print(f"Wrote {len(clickstream)} events → sample-data/clickstream.json")
    print(
        f"Totals: products={len(products)} customers={len(customers)} "
        f"orders={len(orders)} clickstream={len(clickstream)}"
    )


if __name__ == "__main__":
    main()
