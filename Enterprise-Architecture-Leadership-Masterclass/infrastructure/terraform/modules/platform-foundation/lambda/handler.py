"""NorthStar platform foundation health endpoint (BayLearn lab — fictional case)."""

import json
import os
from datetime import datetime, timezone

import boto3

dynamodb = boto3.resource("dynamodb")
ssm = boto3.client("ssm")

TABLE_NAME = os.environ["REGISTRY_TABLE"]
SSM_PREFIX = os.environ["SSM_PREFIX"]


def handler(event, context):
    table = dynamodb.Table(TABLE_NAME)
    now = datetime.now(timezone.utc).isoformat()

    # Record a heartbeat for FinOps / platform observability demos
    table.put_item(
        Item={
            "pk": "PLATFORM",
            "sk": f"HEARTBEAT#{now}",
            "source": "platform-health-lambda",
            "request_id": getattr(context, "aws_request_id", "local"),
            "ttl": int(datetime.now(timezone.utc).timestamp()) + 86400,
        }
    )

    env_param = f"{SSM_PREFIX}/environment"
    try:
        env_name = ssm.get_parameter(Name=env_param)["Parameter"]["Value"]
    except Exception:
        env_name = "unknown"

    body = {
        "status": "ok",
        "service": "northstar-platform-foundation",
        "case_study": "NorthStar Financial Services (fictional)",
        "environment": env_name,
        "timestamp": now,
        "message": "Platform foundation health check succeeded",
    }

    return {
        "statusCode": 200,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }
