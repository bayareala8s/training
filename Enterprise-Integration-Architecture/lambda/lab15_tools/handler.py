"""Governed tools: status reads vs write that requires HITL approval.

Writes never go LLM → database. RequestReprocess creates PENDING; /approve executes.
"""

from __future__ import annotations

import json
import os
import time
import uuid
from typing import Any

import boto3

ddb = boto3.resource("dynamodb")
catalog = ddb.Table(os.environ["CATALOG_TABLE"])
approvals = ddb.Table(os.environ["APPROVAL_TABLE"])
READ = {
    "GetFileStatus",
    "FindFailedTransactions",
    "ExplainError",
    "CheckQueueDepth",
    "GetProcessingStatus",
    "RecommendRemediation",
}
WRITE = {"RequestReprocess"}


def _body(event: dict[str, Any]) -> dict[str, Any]:
    raw = event.get("body") or "{}"
    return json.loads(raw) if isinstance(raw, str) else raw


def _file_id(payload: dict[str, Any]) -> str:
    fid = payload.get("fileId") or "FILE#demo.csv"
    if not str(fid).startswith("FILE#"):
        fid = f"FILE#{fid}"
    return str(fid)


def lambda_handler(event: dict[str, Any], _ctx: Any) -> dict[str, Any]:
    path = event.get("rawPath") or event.get("path") or ""
    payload = _body(event)
    tool = payload.get("tool") or path.rstrip("/").split("/")[-1]

    if path.rstrip("/").endswith("/approve"):
        return _approve(payload)

    if tool in READ:
        return _read(tool, payload)
    if tool in WRITE:
        aid = str(uuid.uuid4())
        file_id = _file_id(payload)
        approvals.put_item(
            Item={
                "pk": aid,
                "status": "PENDING",
                "action": "reprocess",
                "fileId": file_id,
                "ts": int(time.time()),
            }
        )
        return _ok({"tool": tool, "approvalId": aid, "status": "PENDING_APPROVAL", "fileId": file_id})
    return {"statusCode": 400, "headers": {"content-type": "application/json"}, "body": json.dumps({"code": "UNKNOWN_TOOL", "tool": tool})}


def _read(tool: str, payload: dict[str, Any]) -> dict[str, Any]:
    if tool == "GetFileStatus":
        item = catalog.get_item(Key={"pk": _file_id(payload)}).get("Item") or {"status": "UNKNOWN"}
        return _ok({"tool": tool, "result": item})
    if tool == "CheckQueueDepth":
        depth = 0
        qurl = os.environ.get("QUEUE_URL")
        if qurl:
            sqs = boto3.client("sqs")
            attrs = sqs.get_queue_attributes(QueueUrl=qurl, AttributeNames=["ApproximateNumberOfMessages"])
            depth = int(attrs["Attributes"].get("ApproximateNumberOfMessages", 0))
        return _ok({"tool": tool, "result": {"depth": depth}})
    if tool == "FindFailedTransactions":
        item = catalog.get_item(Key={"pk": "FILE#demo.csv"}).get("Item") or {}
        failed = 1 if item.get("status") in {"QUARANTINED", "FAILED"} else 0
        return _ok({"tool": tool, "result": {"failed": failed, "sample": [item.get("pk", "FILE#demo.csv")] if failed else []}})
    if tool == "ExplainError":
        item = catalog.get_item(Key={"pk": _file_id(payload)}).get("Item") or {}
        return _ok({"tool": tool, "result": {"code": item.get("error", "SCHEMA"), "message": item.get("errorMessage", "CSV header missing partner column"), "status": item.get("status")}})
    if tool == "GetProcessingStatus":
        item = catalog.get_item(Key={"pk": _file_id(payload)}).get("Item") or {}
        return _ok({"tool": tool, "result": {"stage": item.get("status", "UNKNOWN")}})
    if tool == "RecommendRemediation":
        return _ok({"tool": tool, "result": {"recommend": "Fix schema and RequestReprocess with HITL"}})
    return {"statusCode": 400, "body": json.dumps({"code": "UNKNOWN_TOOL"})}


def _approve(payload: dict[str, Any]) -> dict[str, Any]:
    aid = payload.get("approvalId")
    if not aid:
        return {"statusCode": 400, "body": json.dumps({"code": "MISSING_APPROVAL_ID"})}
    item = approvals.get_item(Key={"pk": aid}).get("Item")
    if not item:
        return {"statusCode": 404, "body": json.dumps({"code": "NOT_FOUND", "approvalId": aid})}
    if item.get("status") != "PENDING":
        return {"statusCode": 409, "body": json.dumps({"code": "ALREADY_RESOLVED", "status": item.get("status")})}
    file_id = item.get("fileId") or "FILE#demo.csv"
    catalog.update_item(
        Key={"pk": file_id},
        UpdateExpression="SET #s = :s, reprocessedAt = :t, lastApprovalId = :a",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": "REPROCESSED", ":t": int(time.time()), ":a": aid},
    )
    approvals.update_item(
        Key={"pk": aid},
        UpdateExpression="SET #s = :s, decidedAt = :t",
        ExpressionAttributeNames={"#s": "status"},
        ExpressionAttributeValues={":s": "APPROVED", ":t": int(time.time())},
    )
    return _ok({"approved": aid, "fileId": file_id, "status": "REPROCESSED", "audit": "FileReprocessRequested"})


def _ok(body: dict[str, Any]) -> dict[str, Any]:
    return {"statusCode": 200, "headers": {"content-type": "application/json"}, "body": json.dumps(body, default=str)}
