"""Payment checkout service — idempotency + Stripe mock."""

from __future__ import annotations

import hashlib
import json
from typing import Any

from .db import Database
from .queue import WebhookQueue
from .stripe_mock import StripeMock


class IdempotencyConflictError(Exception):
    pass


class StoreUnavailableError(Exception):
    pass


def request_hash(body: dict[str, Any]) -> str:
    normalized = json.dumps(body, sort_keys=True, separators=(",", ":"))
    return hashlib.sha256(normalized.encode()).hexdigest()


class PaymentService:
    def __init__(
        self,
        db: Database,
        stripe: StripeMock,
        webhook_queue: WebhookQueue,
        *,
        store_available: bool = True,
    ) -> None:
        self.db = db
        self.stripe = stripe
        self.webhook_queue = webhook_queue
        self.store_available = store_available

    def create_charge(
        self,
        tenant_id: str,
        idempotency_key: str,
        body: dict[str, Any],
    ) -> tuple[int, dict[str, Any]]:
        if not self.store_available:
            raise StoreUnavailableError("idempotency store unavailable — fail closed")

        if not idempotency_key:
            return 400, {"error": "Idempotency-Key header required"}

        if "amount_cents" not in body or "currency" not in body:
            return 400, {
                "error": "amount_cents and currency are required",
                "example": {"amount_cents": 2500, "currency": "usd"},
            }

        try:
            amount_cents = int(body["amount_cents"])
        except (TypeError, ValueError):
            return 400, {"error": "amount_cents must be an integer"}
        if amount_cents < 1:
            return 400, {"error": "amount_cents must be positive"}

        currency = str(body.get("currency", "")).strip().upper()
        if len(currency) != 3:
            return 400, {"error": "currency must be a 3-letter ISO code (e.g. usd)"}

        body_digest = request_hash(body)
        existing = self.db.get_idempotency(tenant_id, idempotency_key)
        if existing:
            if existing.request_hash != body_digest:
                return 409, {"error": "idempotency key reused with different body"}
            if existing.status == "processing":
                return 409, {"error": "request in flight"}
            if existing.status == "completed" and existing.response_body:
                return existing.response_status or 200, existing.response_body

        inserted = self.db.insert_processing(tenant_id, idempotency_key, body_digest)
        if not inserted:
            row = self.db.get_idempotency(tenant_id, idempotency_key)
            if row and row.status == "completed" and row.response_body:
                return row.response_status or 200, row.response_body
            return 409, {"error": "request in flight"}

        intent = self.stripe.create_payment_intent(
            amount_cents=amount_cents,
            currency=currency,
            idempotency_key=idempotency_key,
            tenant_id=tenant_id,
        )
        order_id = self.db.insert_order(
            tenant_id, amount_cents, currency, intent.id
        )
        response = {
            "order_id": order_id,
            "payment_intent_id": intent.id,
            "status": intent.status,
            "amount_cents": amount_cents,
            "currency": currency,
        }
        self.db.complete_idempotency(
            tenant_id, idempotency_key, 201, response, intent.id
        )
        return 201, response

    def process_webhook(self, event: dict[str, Any]) -> bool:
        event_id = event["event_id"]
        return self.db.mark_webhook_processed(event_id, event)

    def run_sweeper(self, older_than_seconds: float = 0) -> int:
        """Heal stuck processing rows when Stripe intent exists."""
        healed = 0
        for row in self.db.list_stuck_processing(older_than_seconds):
            if row.stripe_payment_intent_id:
                intent = self.stripe.get_intent(row.stripe_payment_intent_id)
                if intent:
                    response = {
                        "payment_intent_id": intent.id,
                        "status": intent.status,
                        "recovered_by": "sweeper",
                    }
                    self.db.complete_idempotency(
                        row.tenant_id,
                        row.idempotency_key,
                        201,
                        response,
                        intent.id,
                    )
                    healed += 1
        return healed
