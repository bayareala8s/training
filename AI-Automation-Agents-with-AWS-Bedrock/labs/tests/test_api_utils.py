import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from common.api_utils import api_response, get_correlation_id, parse_body


def test_parse_body_valid():
    body, err = parse_body({"body": '{"text":"hello"}'})
    assert err is None
    assert body["text"] == "hello"


def test_parse_body_invalid_json():
    body, err = parse_body({"body": "not-json"})
    assert err == "invalid_json"
    assert body == {}


def test_api_response_includes_correlation_id():
    resp = api_response(200, {"ok": True}, "cid-123")
    import json

    payload = json.loads(resp["body"])
    assert payload["correlation_id"] == "cid-123"
    assert resp["headers"]["X-Correlation-Id"] == "cid-123"


def test_get_correlation_id_from_header():
    event = {"headers": {"x-correlation-id": "from-header"}, "body": "{}"}
    assert get_correlation_id(event, {}) == "from-header"
