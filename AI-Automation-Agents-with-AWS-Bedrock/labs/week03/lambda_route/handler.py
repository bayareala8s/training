from week03.route_service import route_request


def handler(event, context):
    text = event.get("text", "")
    label = event.get("label", "general")
    correlation_id = event.get("correlation_id", "unknown")
    return route_request(text, correlation_id=correlation_id, label=label)
