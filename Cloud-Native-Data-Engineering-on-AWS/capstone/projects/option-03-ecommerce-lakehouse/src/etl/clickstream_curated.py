"""Curated clickstream event facts for funnel analytics."""

from __future__ import annotations


FUNNEL_WEIGHT = {
    "page_view": 1,
    "search": 2,
    "add_to_cart": 3,
    "remove_from_cart": 2,
    "checkout_start": 4,
    "purchase": 5,
}


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Map cleaned clickstream events to analytics-ready event facts."""
    curated: list[dict] = []
    for row in records:
        event_type = row.get("event_type") or "page_view"
        curated.append(
            {
                "event_id": row.get("event_id"),
                "session_id": row.get("session_id"),
                "customer_id": row.get("customer_id") or "",
                "product_id": row.get("product_id") or "",
                "event_type": event_type,
                "device": row.get("device"),
                "page_path": row.get("page_path"),
                "event_ts": row.get("event_ts"),
                "funnel_weight": FUNNEL_WEIGHT.get(event_type, 1),
                "processing_date": processing_date,
            }
        )
    return curated
