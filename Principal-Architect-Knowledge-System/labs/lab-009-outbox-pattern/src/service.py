"""Transactional outbox — order service, relay, consumer."""

from __future__ import annotations

from typing import Any

from .models import Order, OutboxEvent, new_event_id, new_order_id, utcnow
from .store import InMemoryDB


class OrderService:
    def __init__(self, db: InMemoryDB) -> None:
        self.db = db

    def create_order(self, sku: str, quantity: int) -> tuple[Order, OutboxEvent]:
        if quantity < 1:
            raise ValueError("quantity must be positive")

        order_id = new_order_id()
        order = Order(order_id=order_id, sku=sku, quantity=quantity)
        event = OutboxEvent(
            id=new_event_id(),
            aggregate_id=order_id,
            event_type="OrderCreated",
            payload={"order_id": order_id, "sku": sku, "quantity": quantity},
        )
        with self.db.transaction() as tx:
            tx.insert_order(order)
            tx.insert_outbox(event)
        return order, event

    def list_orders(self) -> list[Order]:
        return sorted(self.db.orders.values(), key=lambda o: o.created_at)

    def list_outbox(self, *, pending_only: bool = False) -> list[OutboxEvent]:
        events = list(self.db.outbox.values())
        if pending_only:
            events = [e for e in events if e.published_at is None]
        return sorted(events, key=lambda e: e.created_at)


class OutboxRelay:
    """Poll unpublished outbox rows and publish to broker (Kafka stand-in)."""

    def __init__(self, db: InMemoryDB, broker: list[OutboxEvent]) -> None:
        self.db = db
        self.broker = broker

    def poll_batch(self, limit: int = 100) -> list[OutboxEvent]:
        unpublished = [e for e in self.db.outbox.values() if e.published_at is None]
        return sorted(unpublished, key=lambda e: e.created_at)[:limit]

    def publish(self, event: OutboxEvent) -> None:
        self.broker.append(event)

    def mark_published(self, event_id: str) -> None:
        if event_id in self.db.outbox:
            self.db.outbox[event_id].published_at = utcnow()

    def run_once(self) -> int:
        count = 0
        for event in self.poll_batch():
            self.publish(event)
            self.mark_published(event.id)
            count += 1
        return count


class InventoryConsumer:
    """Idempotent consumer — dedupes by event_id."""

    def __init__(self) -> None:
        self.processed: set[str] = set()
        self.inventory: dict[str, int] = {}

    def handle(self, event: OutboxEvent) -> bool:
        if event.id in self.processed:
            return False
        self.processed.add(event.id)
        if event.event_type == "OrderCreated":
            sku = str(event.payload.get("sku", "unknown"))
            qty = int(event.payload.get("quantity", 0))
            self.inventory[sku] = self.inventory.get(sku, 0) + qty
        return True

    def process_broker(self, broker: list[OutboxEvent]) -> dict[str, int]:
        processed = 0
        duplicates = 0
        for event in broker:
            if self.handle(event):
                processed += 1
            else:
                duplicates += 1
        return {"processed": processed, "duplicates": duplicates, "inventory": dict(self.inventory)}


class OutboxStack:
    """Wires DB + broker + relay + consumer for API and CLI."""

    def __init__(self) -> None:
        self.db = InMemoryDB()
        self.broker: list[OutboxEvent] = []
        self.orders = OrderService(self.db)
        self.relay = OutboxRelay(self.db, self.broker)
        self.consumer = InventoryConsumer()

    def stats(self) -> dict[str, Any]:
        return {
            "orders": len(self.db.orders),
            "outbox_total": len(self.db.outbox),
            "outbox_pending": self.db.pending_outbox_count(),
            "broker_messages": len(self.broker),
            "consumer_processed": len(self.consumer.processed),
            "inventory": dict(self.consumer.inventory),
        }
