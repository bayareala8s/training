"""Curated fact_orders grain for the e-commerce star schema."""

from __future__ import annotations


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Map cleaned orders to fact_orders (one row per order line)."""
    curated: list[dict] = []
    for row in records:
        amount = float(row.get("order_amount") or 0)
        qty = int(float(row.get("quantity") or 0))
        curated.append(
            {
                "order_id": row.get("order_id"),
                "customer_id": row.get("customer_id"),
                "product_id": row.get("product_id"),
                "amount": round(amount, 2),
                "quantity": qty,
                "status": row.get("status"),
                "channel": row.get("channel", "web"),
                "order_date": row.get("order_date") or processing_date,
                "processing_date": processing_date,
                "gross_margin_proxy": round(amount * 0.32, 2),
            }
        )
    return curated
