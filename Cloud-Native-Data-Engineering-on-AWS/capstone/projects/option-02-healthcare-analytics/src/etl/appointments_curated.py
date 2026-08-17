"""Curated transform: appointment summary by department."""

from __future__ import annotations

from collections import defaultdict


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Aggregate appointments into department-level operational summary."""
    groups: dict[str, dict] = defaultdict(
        lambda: {
            "appointment_count": 0,
            "completed_count": 0,
            "cancelled_count": 0,
            "no_show_count": 0,
            "total_duration_minutes": 0,
        }
    )

    for row in records:
        dept = row["department"]
        bucket = groups[dept]
        bucket["appointment_count"] += 1
        status = row.get("status", "")
        if status == "completed":
            bucket["completed_count"] += 1
        elif status == "cancelled":
            bucket["cancelled_count"] += 1
        elif status == "no_show":
            bucket["no_show_count"] += 1
        bucket["total_duration_minutes"] += int(float(row["duration_minutes"]))

    curated: list[dict] = []
    for department, agg in sorted(groups.items()):
        count = agg["appointment_count"]
        curated.append(
            {
                "department": department,
                "appointment_count": count,
                "completed_count": agg["completed_count"],
                "cancelled_count": agg["cancelled_count"],
                "no_show_count": agg["no_show_count"],
                "total_duration_minutes": agg["total_duration_minutes"],
                "avg_duration_minutes": round(agg["total_duration_minutes"] / count, 1),
                "completion_rate_pct": round(agg["completed_count"] / count * 100, 2),
                "processing_date": processing_date,
                "report_name": "appointments_by_department",
            }
        )
    return curated
