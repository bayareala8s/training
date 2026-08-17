"""In-memory transactional store (PostgreSQL/Kafka stand-in for local demo)."""

from __future__ import annotations

import threading

from .models import Order, OutboxEvent


class InMemoryDB:
    def __init__(self) -> None:
        self.orders: dict[str, Order] = {}
        self.outbox: dict[str, OutboxEvent] = {}
        self._lock = threading.Lock()

    def transaction(self) -> _Transaction:
        return _Transaction(self)

    def pending_outbox_count(self) -> int:
        return sum(1 for e in self.outbox.values() if e.published_at is None)


class _Transaction:
    def __init__(self, db: InMemoryDB) -> None:
        self.db = db
        self._orders: dict[str, Order] = {}
        self._outbox: dict[str, OutboxEvent] = {}
        self._committed = False

    def __enter__(self) -> _Transaction:
        self.db._lock.acquire()
        return self

    def __exit__(self, exc_type: object, *args: object) -> None:
        try:
            if exc_type is None:
                self.db.orders.update(self._orders)
                self.db.outbox.update(self._outbox)
                self._committed = True
        finally:
            self.db._lock.release()

    def insert_order(self, order: Order) -> None:
        self._orders[order.order_id] = order

    def insert_outbox(self, event: OutboxEvent) -> None:
        self._outbox[event.id] = event
