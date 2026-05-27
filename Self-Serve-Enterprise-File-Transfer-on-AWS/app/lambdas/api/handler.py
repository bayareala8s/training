"""Lab 6: self-serve connections and jobs API."""
import json
import os
import uuid
from datetime import datetime, timezone

import boto3

ddb = boto3.resource("dynamodb")
sfn = boto3.client("stepfunctions")

CONNECTIONS_TABLE = os.environ["CONNECTIONS_TABLE"]
JOBS_TABLE = os.environ["JOBS_TABLE"]
IDEMPOTENCY_TABLE = os.environ.get("IDEMPOTENCY_TABLE", "")
STATE_MACHINE_ARN = os.environ.get("STATE_MACHINE_ARN", "")
LANDING_BUCKET = os.environ["LANDING_BUCKET"]
ALLOWED_PREFIX = os.environ.get("ALLOWED_PREFIX", "partners/demo/")


def _response(status, body, headers=None):
    h = {"Content-Type": "application/json", "Access-Control-Allow-Origin": "*"}
    if headers:
        h.update(headers)
    return {"statusCode": status, "headers": h, "body": json.dumps(body)}


def _owner_sub(event):
    claims = event.get("requestContext", {}).get("authorizer", {}).get("jwt", {}).get("claims", {})
    return claims.get("sub") or event.get("requestContext", {}).get("authorizer", {}).get("sub")


def _path(event):
    return event.get("rawPath") or event.get("path", "")


def _method(event):
    return event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod", "GET")


def _body(event):
    raw = event.get("body") or "{}"
    if event.get("isBase64Encoded"):
        import base64
        raw = base64.b64decode(raw).decode()
    return json.loads(raw) if raw else {}


def list_connections(owner_sub):
    table = ddb.Table(CONNECTIONS_TABLE)
    resp = table.scan(
        FilterExpression="owner_sub = :o",
        ExpressionAttributeValues={":o": owner_sub},
    )
    items = [
        {
            "connection_id": i["connection_id"],
            "name": i.get("name"),
            "type": i.get("type"),
            "status": i.get("status"),
        }
        for i in resp.get("Items", [])
    ]
    return _response(200, {"connections": items})


def create_connection(owner_sub, payload):
    cid = f"c-{uuid.uuid4().hex[:8]}"
    item = {
        "connection_id": cid,
        "owner_sub": owner_sub,
        "name": payload.get("name", "My connection"),
        "type": payload.get("type", "SFTP_INBOUND"),
        "status": "ACTIVE",
        "config": {"allowed_prefix": ALLOWED_PREFIX},
        "created_at": datetime.now(timezone.utc).isoformat(),
    }
    ddb.Table(CONNECTIONS_TABLE).put_item(Item=item)
    return _response(201, {k: item[k] for k in ("connection_id", "name", "type", "status")})


def get_job(owner_sub, job_id):
    table = ddb.Table(JOBS_TABLE)
    item = table.get_item(Key={"job_id": job_id}).get("Item")
    if not item or item.get("owner_sub") != owner_sub:
        return _response(403, {"error": "forbidden"})
    return _response(200, item)


def submit_job(owner_sub, payload, idempotency_key=None):
    connection_id = payload.get("connection_id")
    source_key = payload.get("source_key", "")
    conn = ddb.Table(CONNECTIONS_TABLE).get_item(Key={"connection_id": connection_id}).get("Item")
    if not conn or conn.get("owner_sub") != owner_sub:
        return _response(403, {"error": "forbidden"})
    if conn.get("status") != "ACTIVE":
        return _response(400, {"error": "connection_not_active"})
    prefix = conn.get("config", {}).get("allowed_prefix", ALLOWED_PREFIX)
    if not source_key.startswith(prefix):
        return _response(400, {"error": "source_key_out_of_scope"})

    jobs = ddb.Table(JOBS_TABLE)
    if idempotency_key and IDEMPOTENCY_TABLE:
        idem = ddb.Table(IDEMPOTENCY_TABLE).get_item(Key={"event_key": f"job:{idempotency_key}"}).get("Item")
        if idem and idem.get("job_id"):
            existing = jobs.get_item(Key={"job_id": idem["job_id"]}).get("Item")
            if existing:
                return _response(202, existing)

    job_id = f"j-{uuid.uuid4().hex[:8]}"
    correlation_id = str(uuid.uuid4())
    item = {
        "job_id": job_id,
        "connection_id": connection_id,
        "owner_sub": owner_sub,
        "state": "QUEUED",
        "correlation_id": correlation_id,
        "source_key": source_key,
        "created_at": datetime.now(timezone.utc).isoformat(),
    }

    if STATE_MACHINE_ARN:
        exec_input = json.dumps({
            "bucket": LANDING_BUCKET,
            "key": source_key,
            "correlation_id": correlation_id,
            "valid": True,
        })
        resp = sfn.start_execution(stateMachineArn=STATE_MACHINE_ARN, name=job_id.replace("-", "")[:80], input=exec_input)
        item["state"] = "RUNNING"
        item["execution_arn"] = resp["executionArn"]

    jobs.put_item(Item=item)
    if idempotency_key and IDEMPOTENCY_TABLE:
        ddb.Table(IDEMPOTENCY_TABLE).put_item(Item={"event_key": f"job:{idempotency_key}", "job_id": job_id})

    return _response(202, {k: item[k] for k in ("job_id", "correlation_id", "state") if k in item})


def handler(event, context):
    owner = _owner_sub(event)
    if not owner:
        return _response(401, {"error": "unauthorized"})

    method = _method(event)
    path = _path(event)

    if path.endswith("/v1/connections") and method == "GET":
        return list_connections(owner)
    if path.endswith("/v1/connections") and method == "POST":
        return create_connection(owner, _body(event))
    if "/v1/jobs/" in path and method == "GET":
        job_id = path.rstrip("/").split("/")[-1]
        return get_job(owner, job_id)
    if path.endswith("/v1/jobs") and method == "POST":
        headers = event.get("headers") or {}
        idem = headers.get("x-idempotency-key") or headers.get("X-Idempotency-Key")
        return submit_job(owner, _body(event), idem)

    return _response(404, {"error": "not_found"})
