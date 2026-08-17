"""In-process Stripe API mock with timeout and delay modes."""

from __future__ import annotations

import threading
import time
import uuid
from dataclasses import dataclass, field
from typing import Any, Callable


@dataclass
class PaymentIntent:
    id: str
    amount_cents: int
    currency: str
    idempotency_key: str
    status: str = "succeeded"


class StripeMock:
    """
    Simulates Stripe PaymentIntents with idempotency-key deduplication.

    Modes (via STRIPE_MOCK_MODE env):
      - normal: immediate success
      - slow: delay before response (client may timeout)
      - fail: raise error (no side effect)
    """

    def __init__(
        self,
        delay_seconds: float = 0.0,
        fail: bool = False,
        on_success: Callable[[dict[str, Any]], None] | None = None,
    ) -> None:
        self.delay_seconds = delay_seconds
        self.fail = fail
        self.on_success = on_success
        self._intents: dict[tuple[str, str], PaymentIntent] = {}
        self._lock = threading.Lock()

    def create_payment_intent(
        self,
        amount_cents: int,
        currency: str,
        idempotency_key: str,
        tenant_id: str = "default",
    ) -> PaymentIntent:
        cache_key = (tenant_id, idempotency_key)
        with self._lock:
            existing = self._intents.get(cache_key)
            if existing:
                return existing

        if self.delay_seconds > 0:
            time.sleep(self.delay_seconds)

        if self.fail:
            raise RuntimeError("stripe_mock: simulated gateway failure")

        intent = PaymentIntent(
            id=f"pi_{uuid.uuid4().hex[:16]}",
            amount_cents=amount_cents,
            currency=currency,
            idempotency_key=idempotency_key,
        )
        with self._lock:
            self._intents[cache_key] = intent

        if self.on_success:
            self.on_success(
                {
                    "event_id": f"evt_{uuid.uuid4().hex[:12]}",
                    "type": "payment_intent.succeeded",
                    "payment_intent_id": intent.id,
                    "amount_cents": amount_cents,
                    "currency": currency,
                }
            )
        return intent

    def get_intent(self, payment_intent_id: str) -> PaymentIntent | None:
        with self._lock:
            for intent in self._intents.values():
                if intent.id == payment_intent_id:
                    return intent
        return None

    def intent_count(self) -> int:
        with self._lock:
            return len(self._intents)
