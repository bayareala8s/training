"""NorthStar integration platform Lambdas (BayLearn lab — fictional case)."""

import json
import os
import uuid
from datetime import datetime, timezone

import boto3

dynamodb = boto3.resource("dynamodb")
events = boto3.client("events")
s3 = boto3.client("s3")
sqs = boto3.client("sqs")

ACCOUNTS_TABLE = os.environ["ACCOUNTS_TABLE"]
EVENT_BUS_NAME = os.environ["EVENT_BUS_NAME"]
PARTNER_BUCKET = os.environ["PARTNER_BUCKET"]
PAYMENT_QUEUE_URL = os.environ.get("PAYMENT_QUEUE_URL", "")


def _now():
    return datetime.now(timezone.utc).isoformat()


def account_api_handler(event, context):
    """Real-time account lookup / create via HTTP API."""
    table = dynamodb.Table(ACCOUNTS_TABLE)
    method = event.get("requestContext", {}).get("http", {}).get("method", "GET")
    path_params = event.get("pathParameters") or {}
    account_id = path_params.get("accountId")

    if method == "GET" and account_id:
        item = table.get_item(Key={"account_id": account_id}).get("Item")
        if not item:
            return _response(404, {"error": "account_not_found", "account_id": account_id})
        return _response(200, item)

    if method == "POST":
        body = json.loads(event.get("body") or "{}")
        new_id = body.get("account_id") or str(uuid.uuid4())
        item = {
            "account_id": new_id,
            "customer_name": body.get("customer_name", "Unknown"),
            "status": body.get("status", "ACTIVE"),
            "created_at": _now(),
            "source": "account-api",
        }
        table.put_item(Item=item)

        events.put_events(
            Entries=[
                {
                    "Source": "northstar.accounts",
                    "DetailType": "AccountCreated",
                    "Detail": json.dumps(item),
                    "EventBusName": EVENT_BUS_NAME,
                }
            ]
        )
        return _response(201, item)

    return _response(400, {"error": "unsupported_operation"})


def payment_processor_handler(event, context):
    """Consume payment events from SQS (EventBridge → SQS)."""
    table = dynamodb.Table(ACCOUNTS_TABLE)
    results = []

    for record in event.get("Records", []):
        body = json.loads(record["body"])
        # EventBridge → SQS wraps the event
        detail = body.get("detail") if isinstance(body.get("detail"), dict) else body
        if isinstance(detail, str):
            detail = json.loads(detail)

        payment_id = detail.get("payment_id") or str(uuid.uuid4())
        account_id = detail.get("account_id", "UNKNOWN")
        amount = detail.get("amount", 0)

        table.put_item(
            Item={
                "account_id": f"PAYMENT#{payment_id}",
                "payment_id": payment_id,
                "linked_account": account_id,
                "amount": str(amount),
                "status": "PROCESSED",
                "processed_at": _now(),
            }
        )
        results.append({"payment_id": payment_id, "status": "PROCESSED"})

    return {"processed": len(results), "results": results}


def partner_file_handler(event, context):
    """Simulate partner SFTP arrival: S3 object create → normalize → queue analytics."""
    processed = []
    for record in event.get("Records", []):
        bucket = record["s3"]["bucket"]["name"]
        key = record["s3"]["object"]["key"]
        obj = s3.get_object(Bucket=bucket, Key=key)
        raw = obj["Body"].read().decode("utf-8", errors="replace")
        lines = [ln for ln in raw.strip().splitlines() if ln.strip()]

        summary = {
            "file_key": key,
            "record_count": len(lines),
            "received_at": _now(),
            "channel": "partner-sftp-simulation",
        }

        events.put_events(
            Entries=[
                {
                    "Source": "northstar.partners",
                    "DetailType": "PartnerFileReceived",
                    "Detail": json.dumps(summary),
                    "EventBusName": EVENT_BUS_NAME,
                }
            ]
        )
        processed.append(summary)

    return {"files": processed}


def analytics_handler(event, context):
    """Step Functions task: mark regulatory/analytics batch complete."""
    batch_id = event.get("batch_id") or str(uuid.uuid4())
    result = {
        "batch_id": batch_id,
        "status": "ANALYTICS_COMPLETE",
        "completed_at": _now(),
        "case_study": "NorthStar Financial Services (fictional)",
    }
    return result


def notification_prep_handler(event, context):
    """Step Functions task: prepare notification payload for SNS."""
    return {
        "subject": "NorthStar lab notification",
        "message": json.dumps(
            {
                "event": event,
                "notice": "Fictional NorthStar Financial Services — BayLearn lab",
                "timestamp": _now(),
            }
        ),
    }


def _response(status, body):
    return {
        "statusCode": status,
        "headers": {"content-type": "application/json"},
        "body": json.dumps(body),
    }
