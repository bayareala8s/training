"""Lab 4 — Validate classification output from prior step."""


def handler(event, context):
    from common.validation import validate_classification

    classification = event.get("classification", {})
    result_body = classification.get("result", classification)
    ok, validated, errors = validate_classification(result_body)

    simulate_failure = event.get("simulate_validation_failure", False)
    if simulate_failure:
        ok = False
        validated = {"label": "unknown", "confidence": 0.0, "reason": "simulated", "valid": False}
        errors = ["simulated_failure"]

    return {
        "correlation_id": event.get("correlation_id"),
        "valid": ok,
        "validated": validated,
        "errors": errors,
        "classification": classification,
    }
