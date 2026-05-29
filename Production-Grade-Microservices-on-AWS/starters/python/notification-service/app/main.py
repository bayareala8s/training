import logging
from typing import Any

from fastapi import FastAPI
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("notification-service")

app = FastAPI(title="Notification Service", version="1.0.0")

# In-memory log for lab verification
EVENT_LOG: list[dict[str, Any]] = []


class CloudEvent(BaseModel):
    source: str
    detail_type: str = Field(alias="detail-type")
    detail: dict[str, Any]

    class Config:
        populate_by_name = True


@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service", "events_received": len(EVENT_LOG)}


@app.post("/events")
def receive_event(event: CloudEvent):
    record = {
        "source": event.source,
        "detail_type": event.detail_type,
        "detail": event.detail,
    }
    EVENT_LOG.append(record)
    logger.info("Event received: %s — %s", event.detail_type, event.detail)

    if event.detail_type == "OrderPlaced":
        _send_order_confirmation(event.detail)

    return {"status": "processed", "detail_type": event.detail_type}


@app.get("/events")
def list_events():
    return {"events": EVENT_LOG[-50:]}


def _send_order_confirmation(detail: dict[str, Any]):
    # Simulated notification — students extend with SES/SNS in advanced labs
    logger.info(
        "EMAIL to user %s: Your order %s for $%.2f was placed.",
        detail.get("user_id"),
        detail.get("order_id"),
        detail.get("total", 0),
    )
