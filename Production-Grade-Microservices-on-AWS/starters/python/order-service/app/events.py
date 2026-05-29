import json
import os
from typing import Any

import httpx

EVENT_PUBLISH_MODE = os.getenv("EVENT_PUBLISH_MODE", "http")
EVENT_HTTP_ENDPOINT = os.getenv(
    "EVENT_HTTP_ENDPOINT", "http://notification-service:8004/events"
)
EVENT_BUS_NAME = os.getenv("EVENT_BUS_NAME", "")
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")


def publish_event(source: str, detail_type: str, detail: dict[str, Any]) -> None:
    if EVENT_PUBLISH_MODE == "eventbridge" and EVENT_BUS_NAME:
        import boto3

        client = boto3.client("events", region_name=AWS_REGION)
        client.put_events(
            Entries=[
                {
                    "Source": source,
                    "DetailType": detail_type,
                    "Detail": json.dumps(detail),
                    "EventBusName": EVENT_BUS_NAME,
                }
            ]
        )
    else:
        payload = {
            "source": source,
            "detail-type": detail_type,
            "detail": detail,
        }
        with httpx.Client(timeout=10.0) as client:
            response = client.post(EVENT_HTTP_ENDPOINT, json=payload)
            response.raise_for_status()
