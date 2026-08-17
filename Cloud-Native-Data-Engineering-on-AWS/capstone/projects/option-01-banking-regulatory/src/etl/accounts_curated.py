"""Curated transform for account master – compliance-ready account view."""

from __future__ import annotations


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Produce curated account snapshot for regulatory joining."""
    curated: list[dict] = []
    for row in records:
        balance = float(row["balance"])
        curated.append(
            {
                "account_id": row["account_id"],
                "customer_name": row["customer_name"],
                "account_type": row["account_type"],
                "status": row["status"],
                "currency": row["currency"],
                "balance": round(balance, 2),
                "opened_date": row.get("opened_date", ""),
                "branch_code": row.get("branch_code", ""),
                "risk_tier": row.get("risk_tier", "standard"),
                "processing_date": processing_date,
                "is_overdrawn": balance < 0,
                "balance_band": _balance_band(balance),
            }
        )
    return curated


def _balance_band(balance: float) -> str:
    if balance < 0:
        return "overdrawn"
    if balance < 1000:
        return "low"
    if balance < 50000:
        return "medium"
    return "high"
