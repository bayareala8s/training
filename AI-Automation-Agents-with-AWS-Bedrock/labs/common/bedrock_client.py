"""AWS Bedrock client helpers with retries (Converse API)."""

from __future__ import annotations

import json
import os
import time
from typing import Any

import boto3
from botocore.exceptions import ClientError

from common.config import AWS_REGION, BEDROCK_MODEL_ID, DEFAULT_TEMPERATURE, MAX_OUTPUT_TOKENS


def get_bedrock_runtime(region: str | None = None):
    return boto3.client("bedrock-runtime", region_name=region or AWS_REGION)


def converse(
    prompt: str,
    *,
    model_id: str | None = None,
    temperature: float | None = None,
    max_tokens: int | None = None,
    system: str | None = None,
    region: str | None = None,
) -> dict[str, Any]:
    """
    Invoke Bedrock Converse API. Returns dict with text, latency_ms, model_id, usage.
    """
    client = get_bedrock_runtime(region)
    mid = model_id or BEDROCK_MODEL_ID
    temp = temperature if temperature is not None else DEFAULT_TEMPERATURE
    max_tok = max_tokens or MAX_OUTPUT_TOKENS

    messages = [{"role": "user", "content": [{"text": prompt}]}]
    kwargs: dict[str, Any] = {
        "modelId": mid,
        "messages": messages,
        "inferenceConfig": {"maxTokens": max_tok, "temperature": temp},
    }
    if system:
        kwargs["system"] = [{"text": system}]

    start = time.perf_counter()
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            response = client.converse(**kwargs)
            latency_ms = int((time.perf_counter() - start) * 1000)
            text = _extract_text(response)
            usage = response.get("usage", {})
            return {
                "text": text,
                "latency_ms": latency_ms,
                "model_id": mid,
                "usage": usage,
                "raw": response,
            }
        except ClientError as e:
            last_error = e
            code = e.response.get("Error", {}).get("Code", "")
            if code in ("ThrottlingException", "ServiceUnavailableException") and attempt < 3:
                time.sleep(2**attempt)
                continue
            raise
    raise last_error  # type: ignore[misc]


def _extract_text(response: dict[str, Any]) -> str:
    output = response.get("output", {})
    message = output.get("message", {})
    parts = message.get("content", [])
    texts = [p.get("text", "") for p in parts if "text" in p]
    return "".join(texts).strip()


def parse_json_from_text(text: str) -> dict[str, Any]:
    """Extract JSON object from model text (handles markdown fences)."""
    cleaned = text.strip()
    if cleaned.startswith("```"):
        lines = cleaned.split("\n")
        lines = [ln for ln in lines if not ln.strip().startswith("```")]
        cleaned = "\n".join(lines).strip()
    start = cleaned.find("{")
    end = cleaned.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object found in model output")
    return json.loads(cleaned[start : end + 1])
