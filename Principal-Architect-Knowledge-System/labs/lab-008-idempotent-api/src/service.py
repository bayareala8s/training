"""Lab 008: In-memory idempotent payment service."""

from __future__ import annotations

import hashlib
import json
import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Any


class PaymentState(Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"


class IdempotencyStatus(Enum):
    IN_FLIGHT = "in_flight"
    COMPLETED = "completed"
    FAILED = "failed"


@dataclass
class IdempotencyRecord:
    tenant_id: str
    key: str
    request_hash: str
    status: IdempotencyStatus
    response_status: int = 0
    response_body: bytes = b""
    created_at: float = field(default_factory=time.time)
    expires_at: float = field(default_factory=lambda: time.time() + 86400)


@dataclass
class Payment:
    payment_id: str
    tenant_id: str
    amount: float
    currency: str
    state: PaymentState = PaymentState.PENDING


def request_hash(body: dict[str, Any]) -> str:
    payload = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(payload.encode()).hexdigest()


class IdempotencyStore:
    def __init__(self, ttl_seconds: float = 86400) -> None:
        self._records: dict[tuple[str, str], IdempotencyRecord] = {}
        self._lock = threading.Lock()
        self.ttl_seconds = ttl_seconds

    def lookup(self, tenant_id: str, key: str) -> IdempotencyRecord | None:
        with self._lock:
            record = self._records.get((tenant_id, key))
            if record and record.expires_at < time.time():
                del self._records[(tenant_id, key)]
                return None
            return record

    def save(self, record: IdempotencyRecord) -> None:
        with self._lock:
            self._records[(record.tenant_id, record.key)] = record


class PaymentService:
    def __init__(self, store: IdempotencyStore | None = None) -> None:
        self.store = store or IdempotencyStore()
        self.ledger: list[Payment] = []
        self._lock = threading.Lock()
        self._counter = 0
        self.webhook_dedup: set[str] = set()

    def create_payment(
        self,
        tenant_id: str,
        idempotency_key: str,
        body: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        if not idempotency_key:
            return 400, {"error": "Idempotency-Key header required"}

        if "amount" not in body or "currency" not in body:
            return 400, {
                "error": "amount and currency are required",
                "example": {"amount": 10.0, "currency": "USD"},
            }

        try:
            amount = float(body["amount"])
        except (TypeError, ValueError):
            return 400, {"error": "amount must be a number"}
        if amount <= 0:
            return 400, {"error": "amount must be positive"}

        currency = str(body["currency"]).strip().upper()
        if len(currency) != 3:
            return 400, {"error": "currency must be a 3-letter ISO code (e.g. USD)"}

        body_hash = request_hash(body)
        existing = self.store.lookup(tenant_id, idempotency_key)
        if existing:
            if existing.request_hash != body_hash:
                return 409, {"error": "idempotency key reused with different body"}
            if existing.status == IdempotencyStatus.IN_FLIGHT:
                return 409, {"error": "request in flight"}
            return existing.response_status, json.loads(existing.response_body)

        in_flight = IdempotencyRecord(
            tenant_id, idempotency_key, body_hash, IdempotencyStatus.IN_FLIGHT
        )
        self.store.save(in_flight)

        with self._lock:
            self._counter += 1
            payment = Payment(
                payment_id=f"pay-{self._counter:06d}",
                tenant_id=tenant_id,
                amount=amount,
                currency=currency,
                state=PaymentState.COMPLETED,
            )
            self.ledger.append(payment)

        response = {
            "payment_id": payment.payment_id,
            "status": "completed",
            "amount": amount,
            "currency": currency,
        }
        encoded = json.dumps(response).encode()
        self.store.save(
            IdempotencyRecord(
                tenant_id,
                idempotency_key,
                body_hash,
                IdempotencyStatus.COMPLETED,
                201,
                encoded,
            )
        )
        return 201, response

    def handle_webhook(self, event_id: str, payload: dict[str, Any]) -> bool:
        if event_id in self.webhook_dedup:
            return False
        self.webhook_dedup.add(event_id)
        return True

    def ledger_count(self) -> int:
        return len(self.ledger)
