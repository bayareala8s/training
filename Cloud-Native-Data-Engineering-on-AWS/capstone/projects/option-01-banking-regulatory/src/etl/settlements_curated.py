"""Curated transform: daily_settlement_summary by date, currency, status."""

from __future__ import annotations

from collections import defaultdict


def to_curated(records: list[dict], processing_date: str) -> list[dict]:
    """Aggregate settlements into daily_settlement_summary rows.

    Groups by settlement_date, currency, and status for regulatory reporting.
    """
    groups: dict[tuple[str, str, str], dict] = defaultdict(
        lambda: {
            "settlement_count": 0,
            "gross_amount_sum": 0.0,
            "net_amount_sum": 0.0,
            "fee_amount_sum": 0.0,
        }
    )

    for row in records:
        key = (row["settlement_date"], row["currency"], row["status"])
        bucket = groups[key]
        bucket["settlement_count"] += 1
        bucket["gross_amount_sum"] += float(row["gross_amount"])
        bucket["net_amount_sum"] += float(row["net_amount"])
        fee = float(row.get("fee_amount") or 0)
        bucket["fee_amount_sum"] += fee

    curated: list[dict] = []
    for (settlement_date, currency, status), agg in sorted(groups.items()):
        curated.append(
            {
                "settlement_date": settlement_date,
                "currency": currency,
                "status": status,
                "settlement_count": agg["settlement_count"],
                "gross_amount_sum": round(agg["gross_amount_sum"], 2),
                "net_amount_sum": round(agg["net_amount_sum"], 2),
                "fee_amount_sum": round(agg["fee_amount_sum"], 2),
                "avg_net_amount": round(
                    agg["net_amount_sum"] / agg["settlement_count"], 2
                ),
                "processing_date": processing_date,
                "report_name": "daily_settlement_summary",
            }
        )
    return curated
