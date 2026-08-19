"""CareMesh agent tools — call the patient API. Never DynamoDB / Scan."""

from __future__ import annotations

import json
import os
import urllib.error
import urllib.request
from typing import Any

API = os.environ["PATIENTS_API_URL"].rstrip("/")
DENIED = {"ScanAllPatients", "QueryWarehouse", "DumpEhr"}


def _body(event):
    raw = event.get("body") or "{}"
    return json.loads(raw) if isinstance(raw, str) else raw


def _ok(status, body):
    return {"statusCode": status, "headers": {"content-type": "application/json"}, "body": json.dumps(body, default=str)}


def lambda_handler(event: dict[str, Any], _ctx: Any) -> dict[str, Any]:
    payload = _body(event)
    tool = payload.get("tool")
    if tool in DENIED:
        return _ok(403, {"code": "DENIED_TOOL", "tool": tool, "reason": "AI must not reach production data stores"})
    if tool != "GetPatientSummary":
        return _ok(400, {"code": "UNKNOWN_TOOL", "tool": tool})
    pid = payload.get("patientId")
    role = payload.get("actorRole") or "clinician"
    actor = payload.get("actorId") or "clin-1"
    req = urllib.request.Request(
        f"{API}/patients/{pid}",
        headers={
            "x-actor-role": role,
            "x-actor-id": actor,
            "x-correlation-id": payload.get("correlationId") or "agent",
        },
        method="GET",
    )
    try:
        with urllib.request.urlopen(req, timeout=10) as resp:
            result = json.loads(resp.read().decode())
            return _ok(200, {"tool": tool, "via": "authorized-api", "result": result})
    except urllib.error.HTTPError as exc:
        raw = exc.read().decode()
        try:
            parsed = json.loads(raw)
        except json.JSONDecodeError:
            parsed = {"raw": raw}
        return _ok(exc.code, {"tool": tool, "via": "authorized-api", "error": parsed})
