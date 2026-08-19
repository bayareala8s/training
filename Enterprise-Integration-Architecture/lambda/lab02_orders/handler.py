"""Lab 2 — Orders API. Pattern first: request/reply + idempotent create."""

from __future__ import annotations

import json
import os
import sys
import uuid
from decimal import Decimal
from typing import Any

import boto3
from boto3.dynamodb.conditions import Key
from botocore.exceptions import ClientError

sys.path.append(os.environ.get("EIA_SHARED_PATH", "/opt/python"))
from eia_common import correlation_id, http_method, log, parse_http_body, path_param, raw_path, response, table_name  # type: ignore  # noqa: E402

dynamodb = boto3.resource("dynamodb")


def _table():
    return dynamodb.Table(table_name())


def lambda_handler(event: dict[str, Any], _ctx: Any) -> dict[str, Any]:
    cid = correlation_id(event)
    method = http_method(event)
    path = raw_path(event)
    log("INFO", "request", correlationId=cid, method=method, path=path)

    if method == "POST" and path.rstrip("/").endswith("/orders"):
        return create_order(event, cid)
    if method == "GET" and "/orders/" in path:
        order_id = path_param(event, "id")
        return get_order(order_id, cid)
    return response(404, {"code": "NOT_FOUND", "message": "Unknown route", "retryable": False}, cid)


def create_order(event: dict[str, Any], cid: str) -> dict[str, Any]:
    headers = {str(k).lower(): v for k, v in (event.get("headers") or {}).items()}
    idem = headers.get("idempotency-key")
    if not idem:
        return response(400, {"code": "MISSING_IDEMPOTENCY_KEY", "message": "Idempotency-Key required", "retryable": False}, cid)
    try:
        body = parse_http_body(event)
    except json.JSONDecodeError:
        return response(422, {"code": "INVALID_JSON", "message": "Body must be JSON", "retryable": False}, cid)

    customer_id = body.get("customerId")
    amount = body.get("amount")
    if not customer_id or not isinstance(customer_id, str):
        return response(422, {"code": "SCHEMA", "message": "customerId string required", "retryable": False}, cid)
    if not isinstance(amount, (int, float)) or isinstance(amount, bool) or amount <= 0:
        return response(422, {"code": "SCHEMA", "message": "amount must be a positive number", "retryable": False}, cid)

    order_id = str(uuid.uuid4())
    item = {
        "pk": f"IDEM#{idem}",
        "orderId": order_id,
        "customerId": customer_id,
        "amount": Decimal(str(amount)),
        "status": "CREATED",
        "correlationId": cid,
        "requestHash": json.dumps({"customerId": customer_id, "amount": amount}, sort_keys=True),
    }
    table = _table()
    try:
        table.put_item(Item=item, ConditionExpression="attribute_not_exists(pk)")
    except ClientError as exc:
        if exc.response["Error"]["Code"] != "ConditionalCheckFailedException":
            log("ERROR", "ddb_error", correlationId=cid, error=str(exc))
            return response(503, {"code": "DEPENDENCY", "message": "Store unavailable", "retryable": True}, cid)
        existing = table.get_item(Key={"pk": f"IDEM#{idem}"}).get("Item") or {}
        if existing.get("requestHash") != item["requestHash"]:
            return response(409, {"code": "IDEMPOTENCY_CONFLICT", "message": "Key reused with different body", "retryable": False}, cid)
        return response(
            200,
            {
                "code": "REPLAY",
                "message": "Idempotent replay",
                "orderId": existing.get("orderId"),
                "retryable": False,
            },
            existing.get("correlationId") or cid,
        )
    log("INFO", "order_created", correlationId=cid, orderId=order_id)
    return response(201, {"code": "CREATED", "message": "Order created", "orderId": order_id, "retryable": False}, cid)


def get_order(order_id: str, cid: str) -> dict[str, Any]:
    result = _table().query(
        IndexName="orderId-index",
        KeyConditionExpression=Key("orderId").eq(order_id),
        Limit=1,
    )
    items = result.get("Items") or []
    if not items:
        return response(404, {"code": "NOT_FOUND", "message": "Order not found", "retryable": False}, cid)
    item = items[0]
    return response(
        200,
        {
            "code": "OK",
            "message": "ok",
            "order": {
                "orderId": item["orderId"],
                "customerId": item["customerId"],
                "amount": float(item["amount"]),
                "status": item["status"],
            },
            "retryable": False,
        },
        item.get("correlationId") or cid,
    )
