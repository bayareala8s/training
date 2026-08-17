"""Sweeper — heals stuck idempotency rows (EventBridge + Lambda locally)."""

from __future__ import annotations

from .service import PaymentService


def run_sweeper(service: PaymentService, older_than_seconds: float = 0) -> int:
    count = service.run_sweeper(older_than_seconds)
    print(f"Sweeper healed {count} stuck processing row(s)")
    return count
