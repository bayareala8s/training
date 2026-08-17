"""
Option B — Document Classification & Routing Platform.

Flow: Bedrock JSON classify → validate → confidence gate → queue → persist → audit.
Supports document_text or text, plus optional uploader metadata (simulates S3 object tags).
"""

from __future__ import annotations

from common.audit import write_audit_event
from common.bedrock_client import converse, parse_json_from_text
from common.prompts import DOC_CLASSIFY_SYSTEM, DOC_CLASSIFY_USER_TEMPLATE
from common.validation import apply_confidence_gate, validate_document
from week08.services.persist import notify_stub, persist_result


def classify_document(
    text: str,
    *,
    correlation_id: str,
    doc_type_hint: str | None = None,
    source_uri: str | None = None,
    content_type: str | None = None,
) -> dict:
    """Classify a document excerpt and route to a processing queue."""
    prompt = DOC_CLASSIFY_USER_TEMPLATE.format(text=text[:8000])
    if doc_type_hint:
        prompt += f"\nHint from uploader: {doc_type_hint}"
    if content_type:
        prompt += f"\nContent-Type: {content_type}"

    raw = converse(prompt, system=DOC_CLASSIFY_SYSTEM, temperature=0.1)
    try:
        parsed = parse_json_from_text(raw["text"])
    except (ValueError, Exception):
        parsed = {"doc_type": "unknown", "confidence": 0.0, "reason": "parse_failed"}

    ok, validated, errors = validate_document(parsed)
    gated = apply_confidence_gate(validated, route_key="queue")
    if gated.get("low_confidence") or not ok:
        gated["queue"] = "human_review"
        gated["needs_review"] = True

    notification = None
    if gated.get("queue") == "human_review":
        notification = notify_stub(
            "document_needs_review",
            f"Document {correlation_id} sent to human_review (type={gated.get('doc_type')})",
            correlation_id=correlation_id,
        )

    result = {
        "correlation_id": correlation_id,
        "capstone_option": "doc_classification",
        "valid": ok and not gated.get("needs_review"),
        "result": gated,
        "errors": errors,
        "source": {
            "uri": source_uri,
            "content_type": content_type,
            "hint": doc_type_hint,
            "chars": len(text),
        },
        "notification": notification,
        "latency_ms": raw["latency_ms"],
        "stored": persist_result(
            correlation_id,
            status="document_classified",
            capstone_option="doc_classification",
            payload={
                "doc_type": gated.get("doc_type"),
                "queue": gated.get("queue"),
                "confidence": gated.get("confidence"),
                "source_uri": source_uri,
            },
        ),
    }

    write_audit_event(
        correlation_id=correlation_id,
        event_type="capstone_doc_classify",
        model_id=raw["model_id"],
        input_size=len(text),
        output_size=len(raw["text"]),
        validation_status="valid" if ok else "fallback",
        route_or_action=gated.get("queue", "human_review"),
        latency_ms=raw["latency_ms"],
        extra={"doc_type": gated.get("doc_type"), "source_uri": source_uri},
    )
    return result
