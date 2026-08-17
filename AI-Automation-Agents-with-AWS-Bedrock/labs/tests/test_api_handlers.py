"""Handler routing tests (no AWS / Bedrock required)."""

from __future__ import annotations

import json
import sys
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from week05.lambda_api import handler as api_handler
from week08.lambda_capstone import handler as capstone_handler


def _api_event(route: str, body: dict, *, method: str = "POST") -> dict:
    return {
        "routeKey": f"{method} {route}",
        "requestContext": {"http": {"method": method}},
        "headers": {"x-correlation-id": "test-cid"},
        "body": json.dumps(body),
    }


def _load_body(resp: dict) -> dict:
    return json.loads(resp["body"])


def test_api_rejects_get():
    event = _api_event("/classify", {"text": "hello"}, method="GET")
    resp = api_handler.handler(event, None)
    assert resp["statusCode"] == 405


def test_api_classify_route():
    with patch("week05.lambda_api.handler.classify_text") as mock_classify:
        mock_classify.return_value = {"result": {"label": "billing"}, "valid": True}
        resp = api_handler.handler(_api_event("/classify", {"text": "invoice issue"}), None)
    body = _load_body(resp)
    assert resp["statusCode"] == 200
    assert body["operation"] == "classify"
    assert body["result"]["label"] == "billing"


def test_api_rejects_empty_text():
    resp = api_handler.handler(_api_event("/classify", {"text": ""}), None)
    body = _load_body(resp)
    assert resp["statusCode"] == 400
    assert body["error"] == "text_required"


def test_capstone_incident_route():
    with patch("week08.lambda_capstone.handler.triage_incident") as mock_triage:
        mock_triage.return_value = {"ticket_stub": {"severity": "high"}}
        resp = capstone_handler.handler(
            _api_event("/capstone/incident", {"text": "API 503 in production"}), None
        )
    body = _load_body(resp)
    assert resp["statusCode"] == 200
    assert body["ticket_stub"]["severity"] == "high"


def test_capstone_approval_decide_validation():
    resp = capstone_handler.handler(_api_event("/capstone/approval/decide", {}), None)
    body = _load_body(resp)
    assert resp["statusCode"] == 400
    assert body["error"] == "approval_id_and_decision_required"


def test_capstone_unknown_route():
    resp = capstone_handler.handler(_api_event("/capstone/unknown", {"text": "x"}), None)
    body = _load_body(resp)
    assert resp["statusCode"] == 404
    assert body["error"] == "not_found"
