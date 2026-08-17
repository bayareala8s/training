"""
Lab 5 — API Gateway handlers: /classify, /summarize, /route
"""

from __future__ import annotations

from common.api_utils import (
    api_response,
    check_text_input,
    get_correlation_id,
    parse_body,
    resolve_route,
)
from common.bedrock_client import converse
from common.config import MAX_INPUT_CHARS
from common.prompts import SUMMARIZE_SYSTEM, SUMMARIZE_USER_TEMPLATE
from week03.classify_service import classify_text
from week03.route_service import route_request


def handler(event, context):
    route = resolve_route(event)
    method = event.get("requestContext", {}).get("http", {}).get("method") or event.get("httpMethod", "POST")

    if method != "POST":
        return api_response(405, {"error": "method_not_allowed"})

    body, err = parse_body(event)
    if err:
        return api_response(400, {"error": err})

    correlation_id = get_correlation_id(event, body)
    text = body.get("text", "")

    size_err = check_text_input(text, correlation_id)
    if size_err:
        return size_err

    if "classify" in route:
        result = classify_text(text, correlation_id=correlation_id)
        return api_response(200, {"operation": "classify", **result}, correlation_id)

    if "summarize" in route:
        prompt = SUMMARIZE_USER_TEMPLATE.format(text=text[:MAX_INPUT_CHARS])
        out = converse(prompt, system=SUMMARIZE_SYSTEM, temperature=0.2)
        return api_response(
            200,
            {
                "operation": "summarize",
                "summary": out["text"],
                "latency_ms": out["latency_ms"],
            },
            correlation_id,
        )

    if "route" in route:
        label = body.get("label", "general")
        result = route_request(text, correlation_id=correlation_id, label=label)
        return api_response(200, {"operation": "route", **result}, correlation_id)

    return api_response(404, {"error": "not_found"}, correlation_id)
