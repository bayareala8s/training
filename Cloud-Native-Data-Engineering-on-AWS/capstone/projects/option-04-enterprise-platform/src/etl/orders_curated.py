"""Curated customer_order_features – ML-ready features from retail orders."""

from __future__ import annotations

from collections import defaultdict


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Aggregate cleaned orders into per-customer feature rows."""
    by_customer: dict[str, list[dict]] = defaultdict(list)
    for row in records:
        cid = row.get("customer_id") or "UNKNOWN"
        by_customer[cid].append(row)

    features: list[dict] = []
    for customer_id, rows in sorted(by_customer.items()):
        amounts = [float(r.get("order_amount") or 0) for r in rows]
        qtys = [int(float(r.get("quantity") or 0)) for r in rows]
        statuses = [r.get("status") for r in rows]
        units = {r.get("business_unit") for r in rows}
        cancelled = sum(1 for s in statuses if s == "cancelled")
        delivered = sum(1 for s in statuses if s == "delivered")
        total_amount = sum(amounts)
        order_count = len(rows)
        features.append(
            {
                "customer_id": customer_id,
                "feature_date": processing_date,
                "order_count_30d": order_count,
                "gmv_30d": round(total_amount, 2),
                "avg_order_value": round(total_amount / order_count, 2) if order_count else 0.0,
                "units_ordered": sum(qtys),
                "cancel_rate": round(cancelled / order_count, 4) if order_count else 0.0,
                "delivery_rate": round(delivered / order_count, 4) if order_count else 0.0,
                "business_unit_diversity": len(units),
                "primary_business_unit": max(
                    units,
                    key=lambda u: sum(1 for r in rows if r.get("business_unit") == u),
                )
                if units
                else "retail",
                "recency_proxy_days": 0,
            }
        )
    return features
