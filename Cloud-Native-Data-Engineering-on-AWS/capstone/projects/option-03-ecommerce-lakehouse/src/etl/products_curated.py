"""Curated dim_products summary for the e-commerce star schema."""

from __future__ import annotations


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Map cleaned products to dim_products attributes."""
    curated: list[dict] = []
    for row in records:
        price = float(row.get("unit_price") or 0)
        active_raw = str(row.get("is_active", "true")).lower()
        is_active = active_raw in {"true", "1", "yes"}
        curated.append(
            {
                "product_id": row.get("product_id"),
                "product_name": row.get("product_name"),
                "category": row.get("category"),
                "brand": row.get("brand", "generic"),
                "unit_price": round(price, 2),
                "is_active": is_active,
                "price_tier": "premium" if price >= 100 else "standard" if price >= 25 else "value",
                "as_of_date": processing_date,
            }
        )
    return curated
