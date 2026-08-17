"""Curated vendor feed quality metrics for the enterprise platform."""

from __future__ import annotations


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Summarize vendor feeds into steward-friendly quality rows."""
    curated: list[dict] = []
    for row in records:
        cost = float(row.get("unit_cost") or 0)
        status = row.get("feed_status")
        curated.append(
            {
                "feed_id": row.get("feed_id"),
                "vendor_id": row.get("vendor_id"),
                "sku": row.get("sku"),
                "unit_cost": round(cost, 2),
                "feed_status": status,
                "lead_time_days": int(float(row.get("lead_time_days") or 0)),
                "is_actionable": status in {"accepted", "pending_review"},
                "cost_band": "high" if cost >= 100 else "medium" if cost >= 20 else "low",
                "as_of_date": processing_date,
            }
        )
    return curated
