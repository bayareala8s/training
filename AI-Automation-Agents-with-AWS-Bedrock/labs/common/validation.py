"""Deterministic validation for structured AI outputs."""

from __future__ import annotations

from typing import Any

from common.config import CLASSIFICATION_LABELS, CONFIDENCE_THRESHOLD, DOCUMENT_LABELS, DOCUMENT_QUEUES, ROUTE_TARGETS

FALLBACK_CLASSIFICATION = {
    "label": "unknown",
    "confidence": 0.0,
    "reason": "validation_failed",
    "valid": False,
}

FALLBACK_ROUTE = {
    "route": "human_review",
    "confidence": 0.0,
    "reason": "validation_failed",
    "valid": False,
}


def validate_classification(data: dict[str, Any], *, max_reason_len: int = 200) -> tuple[bool, dict[str, Any], list[str]]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return False, {**FALLBACK_CLASSIFICATION}, ["payload_not_object"]

    label = data.get("label")
    confidence = data.get("confidence")
    reason = data.get("reason", "")

    if label not in CLASSIFICATION_LABELS:
        errors.append("invalid_label")
    if not isinstance(confidence, (int, float)) or not (0 <= float(confidence) <= 1):
        errors.append("invalid_confidence")
    if not isinstance(reason, str):
        errors.append("invalid_reason_type")
    elif len(reason) > max_reason_len:
        errors.append("reason_too_long")

    if errors:
        out = {**FALLBACK_CLASSIFICATION, "errors": errors}
        return False, out, errors

    return True, {
        "label": label,
        "confidence": float(confidence),
        "reason": reason[:max_reason_len],
        "valid": True,
    }, []


def validate_route(data: dict[str, Any], *, max_reason_len: int = 200) -> tuple[bool, dict[str, Any], list[str]]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return False, {**FALLBACK_ROUTE}, ["payload_not_object"]

    route = data.get("route")
    confidence = data.get("confidence")
    reason = data.get("reason", "")

    if route not in ROUTE_TARGETS:
        errors.append("invalid_route")
    if not isinstance(confidence, (int, float)) or not (0 <= float(confidence) <= 1):
        errors.append("invalid_confidence")
    if not isinstance(reason, str):
        errors.append("invalid_reason_type")
    elif len(reason) > max_reason_len:
        errors.append("reason_too_long")

    if errors:
        return False, {**FALLBACK_ROUTE, "errors": errors}, errors

    return True, {
        "route": route,
        "confidence": float(confidence),
        "reason": reason[:max_reason_len],
        "valid": True,
    }, []


def apply_confidence_gate(
    validated: dict[str, Any],
    *,
    route_key: str = "route",
    threshold: float | None = None,
) -> dict[str, Any]:
    """If confidence below threshold, force human_review route."""
    th = threshold if threshold is not None else CONFIDENCE_THRESHOLD
    conf = validated.get("confidence", 0)
    if conf < th:
        return {
            **validated,
            route_key: "human_review",
            "low_confidence": True,
        }
    return validated


FALLBACK_DOCUMENT = {
    "doc_type": "unknown",
    "confidence": 0.0,
    "reason": "validation_failed",
    "valid": False,
}

DOC_TYPE_TO_QUEUE = {
    "invoice": "queue_invoices",
    "contract": "queue_contracts",
    "hr": "queue_hr",
    "legal": "queue_legal",
    "general": "queue_general",
    "unknown": "human_review",
}


def validate_document(data: dict[str, Any], *, max_reason_len: int = 200) -> tuple[bool, dict[str, Any], list[str]]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return False, {**FALLBACK_DOCUMENT}, ["payload_not_object"]

    doc_type = data.get("doc_type")
    confidence = data.get("confidence")
    reason = data.get("reason", "")

    if doc_type not in DOCUMENT_LABELS:
        errors.append("invalid_doc_type")
    if not isinstance(confidence, (int, float)) or not (0 <= float(confidence) <= 1):
        errors.append("invalid_confidence")
    if not isinstance(reason, str):
        errors.append("invalid_reason_type")
    elif len(reason) > max_reason_len:
        errors.append("reason_too_long")

    if errors:
        return False, {**FALLBACK_DOCUMENT, "errors": errors}, errors

    queue = DOC_TYPE_TO_QUEUE.get(doc_type, "human_review")
    return True, {
        "doc_type": doc_type,
        "confidence": float(confidence),
        "reason": reason[:max_reason_len],
        "queue": queue,
        "valid": True,
    }, []
