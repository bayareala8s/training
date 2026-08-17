"""Curated dim_customers summary for the e-commerce star schema."""

from __future__ import annotations


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Map cleaned customers to dim_customers attributes (email partially masked)."""
    curated: list[dict] = []
    for row in records:
        email = str(row.get("email") or "")
        local, _, domain = email.partition("@")
        masked = f"{local[:2]}***@{domain}" if domain else "***"
        curated.append(
            {
                "customer_id": row.get("customer_id"),
                "email_masked": masked,
                "segment": row.get("segment"),
                "region": row.get("region"),
                "signup_date": row.get("signup_date"),
                "lifetime_orders_est": int(float(row.get("lifetime_orders") or 0)),
                "as_of_date": processing_date,
            }
        )
    return curated
