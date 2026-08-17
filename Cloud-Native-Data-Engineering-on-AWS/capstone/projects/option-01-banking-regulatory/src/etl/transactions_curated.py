"""Curated transform for banking transactions – enrich for regulatory audit."""

from __future__ import annotations


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Normalize passed transactions into curated audit-ready rows."""
    curated: list[dict] = []
    for row in records:
        amount = float(row["amount"])
        curated.append(
            {
                "transaction_id": row["transaction_id"],
                "account_id": row["account_id"],
                "settlement_id": row.get("settlement_id", ""),
                "amount": round(amount, 2),
                "currency": row["currency"],
                "status": row["status"],
                "transaction_type": row.get("transaction_type", "unknown"),
                "settlement_date": row["settlement_date"],
                "channel": row.get("channel", "unknown"),
                "processing_date": processing_date,
                "amount_bucket": _amount_bucket(amount),
                "is_high_value": amount >= 10000,
            }
        )
    return curated


def _amount_bucket(amount: float) -> str:
    if amount < 100:
        return "micro"
    if amount < 1000:
        return "small"
    if amount < 10000:
        return "medium"
    return "large"
