"""
Lab 2.1 — Lambda handler: secure Bedrock invocation with correlation ID logging.
Deployed via SAM as Week2InvokeFunction.
"""

from __future__ import annotations

import json
import logging
import uuid

from common.audit import write_audit_event
from common.bedrock_client import converse
from common.config import BEDROCK_MODEL_ID

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def handler(event, context):
    correlation_id = event.get("correlation_id") or str(uuid.uuid4())
    prompt = event.get("prompt", "Say hello in one word.")
    temperature = float(event.get("temperature", 0.2))

    logger.info(
        json.dumps({
            "correlation_id": correlation_id,
            "model_id": BEDROCK_MODEL_ID,
            "event": "invoke_start",
        })
    )

    try:
        result = converse(prompt, temperature=temperature)
        write_audit_event(
            correlation_id=correlation_id,
            event_type="bedrock_invoke",
            model_id=result["model_id"],
            input_size=len(prompt),
            output_size=len(result["text"]),
            validation_status="n/a",
            latency_ms=result["latency_ms"],
            success=True,
        )
        logger.info(
            json.dumps({
                "correlation_id": correlation_id,
                "model_id": result["model_id"],
                "latency_ms": result["latency_ms"],
                "success": True,
            })
        )
        return {
            "correlation_id": correlation_id,
            "success": True,
            "latency_ms": result["latency_ms"],
            "model_id": result["model_id"],
            "text_preview": result["text"][:200],
        }
    except Exception as e:
        logger.exception("Bedrock invoke failed")
        write_audit_event(
            correlation_id=correlation_id,
            event_type="bedrock_invoke",
            model_id=BEDROCK_MODEL_ID,
            validation_status="error",
            success=False,
            extra={"error": str(e)[:200]},
        )
        return {
            "correlation_id": correlation_id,
            "success": False,
            "error": str(e),
        }
