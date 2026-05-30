"""Stub quality validation Lambda for Step Functions orchestration labs."""

import json
import os


def lambda_handler(event, context):
    """Return a passing quality result for pipeline orchestration tests."""
    processing_date = event.get("processing_date", "unknown")
    dataset = event.get("dataset", "unknown")
    pass_rate = float(os.environ.get("PASS_RATE", "100"))

    result = {
        "status": "PASS",
        "pass_rate": pass_rate,
        "processing_date": processing_date,
        "dataset": dataset,
        "records_checked": 0,
        "records_quarantined": 0,
        "message": "Course stub validator — replace with Lab 4.2 implementation",
    }
    print(json.dumps(result))
    return result
