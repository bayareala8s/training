"""Domain models for Lab 009."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from typing import Any


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


@dataclass
class OutboxEvent:
    id: str
    aggregate_id: str
    event_type: str
    payload: dict[str, Any]
    created_at: datetime = field(default_factory=utcnow)
    published_at: datetime | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "aggregate_id": self.aggregate_id,
            "event_type": self.event_type,
            "payload": self.payload,
            "created_at": self.created_at.isoformat(),
            "published_at": self.published_at.isoformat() if self.published_at else None,
        }


@dataclass
class Order:
    order_id: str
    sku: str
    quantity: int
    created_at: datetime = field(default_factory=utcnow)

    def to_dict(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id,
            "sku": self.sku,
            "quantity": self.quantity,
            "created_at": self.created_at.isoformat(),
        }


def new_order_id() -> str:
    return f"ord_{uuid.uuid4().hex[:12]}"


def new_event_id() -> str:
    return f"evt_{uuid.uuid4().hex[:12]}"
