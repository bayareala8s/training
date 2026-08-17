from week03.classify_service import classify_text


def handler(event, context):
    text = event.get("text", "")
    correlation_id = event.get("correlation_id", "unknown")
    return classify_text(text, correlation_id=correlation_id)
