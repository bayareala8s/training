"""Quality validation Lambda — Lab 4.1 RuleEngine integrated for pipeline checkpoints."""

from __future__ import annotations

import json
import os
from pathlib import Path

from validators import RuleEngine

RULES_PATH = Path(__file__).with_name("orders_rules.json")
_engine: RuleEngine | None = None


def _get_engine() -> RuleEngine:
    global _engine
    if _engine is None:
        _engine = RuleEngine(RULES_PATH)
    return _engine


def lambda_handler(event, context):
    """Validate records when provided; otherwise return pipeline checkpoint PASS."""
    processing_date = event.get("processing_date", "unknown")
    dataset = event.get("dataset", "unknown")
    records = event.get("records", [])

    slo = float(os.environ.get("PASS_RATE_SLO", "0"))

    if records:
        results = _get_engine().validate_batch(records)
        passed = sum(1 for r in results if not r.has_errors)
        total = len(records)
        quarantined = total - passed
        pass_rate = (passed / total * 100) if total else 100.0
    else:
        total = 0
        quarantined = 0
        pass_rate = float(os.environ.get("PASS_RATE", "100"))

    status = "PASS" if pass_rate >= slo else "FAIL"
    result = {
        "status": status,
        "pass_rate": round(pass_rate, 2),
        "processing_date": processing_date,
        "dataset": dataset,
        "records_checked": total,
        "records_quarantined": quarantined,
        "message": (
            f"Validated {total} record(s); {quarantined} quarantined"
            if records
            else "Pipeline quality checkpoint passed"
        ),
    }
    print(json.dumps(result))
    return result
