"""Curated enterprise_kpi_daily – inventory-driven platform KPIs."""

from __future__ import annotations


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Roll inventory rows into a daily enterprise KPI snapshot."""
    if not records:
        return [
            {
                "kpi_date": processing_date,
                "sku_count": 0,
                "warehouse_count": 0,
                "total_units_on_hand": 0,
                "stockout_skus": 0,
                "low_stock_skus": 0,
                "fill_rate_pct": 0.0,
                "avg_quantity_on_hand": 0.0,
                "reorder_needed_skus": 0,
            }
        ]

    skus = {r.get("sku") for r in records}
    warehouses = {r.get("warehouse_id") for r in records}
    qoh_values = [float(r.get("quantity_on_hand") or 0) for r in records]
    stockout = sum(1 for r in records if r.get("stock_status") == "out_of_stock" or float(r.get("quantity_on_hand") or 0) <= 0)
    low = sum(1 for r in records if r.get("stock_status") == "low_stock")
    reorder = sum(
        1
        for r in records
        if float(r.get("quantity_on_hand") or 0) <= float(r.get("reorder_point") or 0)
    )
    in_stockish = len(records) - stockout
    fill_rate = (in_stockish / len(records) * 100.0) if records else 0.0

    return [
        {
            "kpi_date": processing_date,
            "sku_count": len(skus),
            "warehouse_count": len(warehouses),
            "total_units_on_hand": int(sum(qoh_values)),
            "stockout_skus": stockout,
            "low_stock_skus": low,
            "fill_rate_pct": round(fill_rate, 2),
            "avg_quantity_on_hand": round(sum(qoh_values) / len(qoh_values), 2),
            "reorder_needed_skus": reorder,
        }
    ]
