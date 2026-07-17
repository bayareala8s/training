import json
import os
import time
from datetime import datetime, timezone

import boto3

cw = boto3.client("cloudwatch")
ddb = boto3.resource("dynamodb")


def handler(event, context):
    """Emit recovery-drill metric and optionally record evidence row.

    Expected event example:
    {
      "control_id": "CTRL-RPO-001",
      "elapsed_seconds": 42,
      "object_key": "settlements/sample-001.txt",
      "outcome": "restored"
    }
    """
    namespace = os.environ["METRIC_NAMESPACE"]
    table_name = os.environ["EVIDENCE_TABLE"]
    control_id = event.get("control_id", "CTRL-DRILL-001")
    elapsed = int(event.get("elapsed_seconds", 0))
    outcome = event.get("outcome", "completed")
    object_key = event.get("object_key", "")

    cw.put_metric_data(
        Namespace=namespace,
        MetricData=[
            {
                "MetricName": "RecoveryDrillEvents",
                "Timestamp": datetime.now(timezone.utc),
                "Value": 1.0,
                "Unit": "Count",
                "Dimensions": [
                    {"Name": "Outcome", "Value": outcome},
                ],
            },
            {
                "MetricName": "RecoveryDrillElapsedSeconds",
                "Timestamp": datetime.now(timezone.utc),
                "Value": float(elapsed),
                "Unit": "Seconds",
            },
        ],
    )

    table = ddb.Table(table_name)
    table.put_item(
        Item={
            "control_id": control_id,
            "tested_at": datetime.now(timezone.utc).isoformat(),
            "elapsed_seconds": elapsed,
            "outcome": outcome,
            "object_key": object_key,
            "ttl_note": "Lab evidence only — fictional NorthStar case",
        }
    )

    return {
        "statusCode": 200,
        "body": json.dumps(
            {
                "ok": True,
                "control_id": control_id,
                "elapsed_seconds": elapsed,
                "recorded_at_epoch": int(time.time()),
            }
        ),
    }
