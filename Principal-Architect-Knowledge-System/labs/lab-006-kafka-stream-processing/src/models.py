"""Domain models for Lab 006."""

from __future__ import annotations

import time
from dataclasses import dataclass, field
from typing import Any


@dataclass
class Order:
    order_id: str
    customer_id: str
    amount: float
    region: str
    event_time: float = field(default_factory=time.time)

    def to_dict(self) -> dict[str, Any]:
        return {
            "order_id": self.order_id,
            "customer_id": self.customer_id,
            "amount": self.amount,
            "region": self.region,
            "event_time": self.event_time,
        }


@dataclass
class WindowMetrics:
    window_start: int
    region: str
    count: int = 0
    revenue: float = 0.0

    def to_dict(self) -> dict[str, Any]:
        return {
            "window_start": self.window_start,
            "region": self.region,
            "count": self.count,
            "revenue": round(self.revenue, 2),
        }
