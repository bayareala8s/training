"""Curated transform for lab results – analytics-ready clinical facts."""

from __future__ import annotations


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Normalize lab results for operational analytics (no direct identifiers beyond patient_id)."""
    curated: list[dict] = []
    for row in records:
        value = float(row["numeric_value"])
        curated.append(
            {
                "result_id": row["result_id"],
                "patient_id": row["patient_id"],
                "test_code": row["test_code"],
                "numeric_value": round(value, 3),
                "unit": row.get("unit", ""),
                "result_flag": row["result_flag"],
                "collected_date": row["collected_date"],
                "ordering_dept": row.get("ordering_dept", ""),
                "processing_date": processing_date,
                "is_abnormal": row["result_flag"] in {"high", "low", "critical"},
                "is_critical": row["result_flag"] == "critical",
            }
        )
    return curated
