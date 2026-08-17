"""
Lab 6.1 — Lambda handler for Step Functions input validation and quality gate.
Deploy as cnde-{env}-pipeline-validation (or use Module 4 quality_runner pattern).
"""
from __future__ import annotations

import json
from datetime import datetime, timezone
from typing import Any


def handler(event: dict[str, Any], context: Any) -> dict[str, Any]:
    action = event.get("action", "validate_input")
    processing_date = event.get("processing_date")
    dataset = event.get("dataset", "retail/orders")

    if action == "validate_input":
        valid = bool(processing_date and dataset)
        return {
            "valid": valid,
            "processing_date": processing_date,
            "dataset": dataset,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }

    if action == "run_quality_check":
        # Lab stub: replace with Module 4 quality_runner integration in production
        pass_rate = float(event.get("mock_pass_rate", 99.95))
        return {
            "dataset": dataset,
            "processing_date": processing_date,
            "pass_rate": pass_rate,
            "within_slo": pass_rate >= 99.9,
            "quarantined_count": 0 if pass_rate >= 99.9 else 42,
            "checked_at": datetime.now(timezone.utc).isoformat(),
        }

    return {"error": f"Unknown action: {action}"}


if __name__ == "__main__":
    print(json.dumps(handler({"action": "validate_input", "processing_date": "2024-01-15", "dataset": "retail/orders"}, None)))
