"""Northbridge Bank — payment API (request/reply) + enqueue posting command."""

from __future__ import annotations

import json
import os
import time
import uuid
from decimal import Decimal
from typing import Any

import boto3
from botocore.exceptions import ClientError

ddb = boto3.resource("dynamodb")
payments = ddb.Table(os.environ["PAYMENTS_TABLE"])
catalog = ddb.Table(os.environ["CATALOG_TABLE"])
approvals = ddb.Table(os.environ["APPROVAL_TABLE"])
sqs = boto3.client("sqs")
QUEUE_URL = os.environ["QUEUE_URL"]


def _body(event):
    raw = event.get("body") or "{}"
    return json.loads(raw) if isinstance(raw, str) else raw


def _cid(event):
    headers = {str(k).lower(): v for k, v in (event.get("headers") or {}).items()}
    return headers.get("x-correlation-id") or str(uuid.uuid4())


def _ok(status, body, cid):
    body = {**body, "correlationId": cid}
    return {"statusCode": status, "headers": {"content-type": "application/json", "x-correlation-id": cid}, "body": json.dumps(body, default=str)}


def lambda_handler(event: dict[str, Any], _ctx: Any) -> dict[str, Any]:
    cid = _cid(event)
    method = (event.get("requestContext") or {}).get("http", {}).get("method") or event.get("httpMethod") or ""
    path = event.get("rawPath") or event.get("path") or ""
    payload = _body(event)

    if method == "POST" and path.rstrip("/").endswith("/payments"):
        return create_payment(event, payload, cid)
    if method == "GET" and "/payments/" in path:
        pid = (event.get("pathParameters") or {}).get("id") or path.rstrip("/").split("/")[-1]
        item = payments.get_item(Key={"pk": f"PAY#{pid}"}).get("Item")
        if not item:
            return _ok(404, {"code": "NOT_FOUND"}, cid)
        return _ok(200, {"payment": item}, cid)
    if method == "GET" and "/files/" in path:
        fid = (event.get("pathParameters") or {}).get("id") or path.rstrip("/").split("/")[-1]
        if not fid.startswith("FILE#"):
            fid = f"FILE#{fid}"
        item = catalog.get_item(Key={"pk": fid}).get("Item") or {"status": "UNKNOWN", "pk": fid}
        return _ok(200, {"file": item}, cid)
    if method == "POST" and path.rstrip("/").endswith("/tools"):
        return tools(payload, cid)
    if method == "POST" and path.rstrip("/").endswith("/approve"):
        return approve(payload, cid)
    return _ok(404, {"code": "NOT_FOUND"}, cid)


def create_payment(event, payload, cid):
    headers = {str(k).lower(): v for k, v in (event.get("headers") or {}).items()}
    idem = headers.get("idempotency-key")
    if not idem:
        return _ok(400, {"code": "MISSING_IDEMPOTENCY_KEY"}, cid)
    customer = payload.get("customerId")
    amount = payload.get("amount")
    if not customer or not isinstance(amount, (int, float)) or amount <= 0:
        return _ok(422, {"code": "SCHEMA", "message": "customerId and positive amount required"}, cid)
    existing = payments.get_item(Key={"pk": f"IDEM#{idem}"}).get("Item")
    if existing:
        return _ok(200, {"code": "REPLAY", "paymentId": existing.get("paymentId"), "status": existing.get("status")}, cid)
    pid = str(uuid.uuid4())
    item = {
        "pk": f"PAY#{pid}",
        "paymentId": pid,
        "customerId": customer,
        "amount": Decimal(str(amount)),
        "status": "ACCEPTED",
        "correlationId": cid,
        "idempotencyKey": idem,
    }
    payments.put_item(Item=item)
    payments.put_item(Item={"pk": f"IDEM#{idem}", "paymentId": pid, "status": "ACCEPTED", "correlationId": cid})
    sqs.send_message(
        QueueUrl=QUEUE_URL,
        MessageBody=json.dumps({"paymentId": pid, "customerId": customer, "amount": amount, "correlationId": cid}),
    )
    return _ok(202, {"code": "ACCEPTED", "paymentId": pid, "status": "ACCEPTED"}, cid)


def tools(payload, cid):
    tool = payload.get("tool")
    if tool == "GetFileStatus":
        fid = payload.get("fileId") or "FILE#inbound/good.csv"
        if not str(fid).startswith("FILE#"):
            fid = f"FILE#{fid}"
        item = catalog.get_item(Key={"pk": fid}).get("Item") or {"status": "UNKNOWN"}
        return _ok(200, {"tool": tool, "result": item}, cid)
    if tool == "FindFailedTransactions":
        # Never Scan * from an LLM; this tool is a bounded GetItem on the demo/quarantine catalog key.
        item = catalog.get_item(Key={"pk": payload.get("fileId", "FILE#inbound/poison.csv")}).get("Item")
        return _ok(200, {"tool": tool, "result": {"item": item}}, cid)
    if tool == "RequestReprocess":
        aid = str(uuid.uuid4())
        fid = payload.get("fileId") or "FILE#inbound/poison.csv"
        approvals.put_item(Item={"pk": aid, "status": "PENDING", "fileId": fid, "ts": int(time.time())})
        return _ok(200, {"tool": tool, "approvalId": aid, "status": "PENDING_APPROVAL"}, cid)
    return _ok(400, {"code": "UNKNOWN_TOOL", "tool": tool}, cid)


def approve(payload, cid):
    aid = payload.get("approvalId")
    item = approvals.get_item(Key={"pk": aid}).get("Item")
    if not item or item.get("status") != "PENDING":
        return _ok(409, {"code": "NOT_PENDING"}, cid)
    fid = item.get("fileId")
    catalog.update_item(
        Key={"pk": fid},
        UpdateExpression="SET #s = :s, lastApprovalId = :a",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": "REPROCESSED", ":a": aid},
    )
    approvals.update_item(
        Key={"pk": aid},
        UpdateExpression="SET #s = :s",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": "APPROVED"},
    )
    return _ok(200, {"approved": aid, "fileId": fid, "status": "REPROCESSED", "audit": "FileReprocessRequested"}, cid)
