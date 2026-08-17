"""Stream processing pipeline — producer, enricher, aggregator, DLT."""

from __future__ import annotations

import json
import time
import uuid
from typing import Any

from .broker import InMemoryBroker
from .models import Order, WindowMetrics


class OrderProducer:
    """Idempotent producer — dedupes by order_id within session."""

    def __init__(self, broker: InMemoryBroker, topic: str = "orders") -> None:
        self.broker = broker
        self.topic = topic
        self._produced: set[str] = set()
        self.produced_total = 0

    def produce(self, order: Order) -> dict[str, Any]:
        if order.order_id in self._produced:
            return {"status": "duplicate_skipped", "order_id": order.order_id}
        partition = self.broker.produce(self.topic, order.customer_id, order.to_dict())
        self._produced.add(order.order_id)
        self.produced_total += 1
        return {
            "status": "produced",
            "order_id": order.order_id,
            "topic": self.topic,
            "partition": partition,
            "key": order.customer_id,
        }


class EnricherConsumer:
    """At-least-once enricher with idempotent handler and DLT routing."""

    def __init__(self, broker: InMemoryBroker) -> None:
        self.broker = broker
        self.processed_ids: set[str] = set()
        self.enriched_topic = "orders-enriched"
        self.processed_total = 0
        self.duplicates_total = 0

    def enrich(self, raw: dict[str, Any]) -> dict[str, Any]:
        if "order_id" not in raw or "amount" not in raw:
            raise ValueError("invalid schema")
        return {**raw, "enriched": True, "currency": "USD"}

    def run_once(self) -> dict[str, int]:
        enriched = 0
        dlt_routed = 0
        duplicates = 0
        for partition in range(InMemoryBroker.PARTITIONS):
            for raw in self.broker.consume("orders", partition):
                try:
                    record = self.enrich(raw)
                except ValueError:
                    self.broker.send_dlt(json.dumps(raw), "schema validation failed")
                    dlt_routed += 1
                    continue
                order_id = str(record["order_id"])
                if order_id in self.processed_ids:
                    duplicates += 1
                    self.duplicates_total += 1
                    continue
                self.processed_ids.add(order_id)
                self.broker.produce(self.enriched_topic, str(record["customer_id"]), record)
                enriched += 1
                self.processed_total += 1
        return {"enriched": enriched, "dlt_routed": dlt_routed, "duplicates": duplicates}


class WindowAggregator:
    """Tumbling window aggregation keyed by region."""

    def __init__(self, broker: InMemoryBroker, window_size_sec: int = 60) -> None:
        self.broker = broker
        self.window_size_sec = window_size_sec
        self.windows: dict[tuple[int, str], WindowMetrics] = {}
        self.metrics_topic = "order-metrics"

    def aggregate(self, enriched: dict[str, Any]) -> WindowMetrics:
        window_start = int(enriched["event_time"] // self.window_size_sec) * self.window_size_sec
        key = (window_start, str(enriched["region"]))
        if key not in self.windows:
            self.windows[key] = WindowMetrics(window_start, str(enriched["region"]))
        metrics = self.windows[key]
        metrics.count += 1
        metrics.revenue += float(enriched["amount"])
        return metrics

    def run_once(self) -> dict[str, int]:
        emitted = 0
        for partition in range(InMemoryBroker.PARTITIONS):
            for enriched in self.broker.consume("orders-enriched", partition):
                metrics = self.aggregate(enriched)
                self.broker.produce(
                    self.metrics_topic,
                    str(metrics.window_start),
                    metrics.to_dict(),
                )
                emitted += 1
        return {"metrics_emitted": emitted, "windows": len(self.windows)}


class DLTHandler:
    def __init__(self, broker: InMemoryBroker) -> None:
        self.broker = broker

    def list_messages(self) -> list[dict[str, Any]]:
        return list(self.broker.dlt)

    def send_to_dlt(self, raw: str, error: str) -> None:
        self.broker.send_dlt(raw, error)

    def replay(self) -> int:
        count = 0
        for item in list(self.broker.dlt):
            raw = json.loads(item["raw"])
            if "order_id" in raw:
                self.broker.produce("orders", str(raw.get("customer_id", "unknown")), raw)
                count += 1
        return count


class StreamStack:
    """Wires broker + pipeline stages for API and CLI."""

    def __init__(self) -> None:
        self.broker = InMemoryBroker()
        self.producer = OrderProducer(self.broker)
        self.enricher = EnricherConsumer(self.broker)
        self.aggregator = WindowAggregator(self.broker)
        self.dlt = DLTHandler(self.broker)

    def create_order(
        self,
        customer_id: str,
        amount: float,
        region: str,
        *,
        order_id: str | None = None,
    ) -> dict[str, Any]:
        oid = order_id or f"ord-{uuid.uuid4().hex[:8]}"
        order = Order(order_id=oid, customer_id=customer_id, amount=amount, region=region)
        return self.producer.produce(order)

    def inject_poison(self) -> dict[str, Any]:
        self.broker.produce("orders", "bad", {"invalid": True})
        return {"status": "injected", "topic": "orders"}

    def stats(self) -> dict[str, Any]:
        return {
            "orders_topic_depth": self.broker.topic_depth("orders"),
            "enriched_topic_depth": self.broker.topic_depth("orders-enriched"),
            "metrics_topic_depth": self.broker.topic_depth("order-metrics"),
            "dlt_messages": len(self.broker.dlt),
            "produced_total": self.producer.produced_total,
            "enricher_processed": self.enricher.processed_total,
            "enricher_duplicates": self.enricher.duplicates_total,
            "windows": len(self.aggregator.windows),
        }

    def list_metrics(self) -> list[dict[str, Any]]:
        return [m.to_dict() for m in self.aggregator.windows.values()]
