"""In-memory Kafka stand-in with partitioned topics and DLT."""

from __future__ import annotations

from collections import defaultdict, deque
from typing import Any


class InMemoryBroker:
    """Topic partition simulation keyed by customer_id hash."""

    PARTITIONS = 4
    TOPICS = ("orders", "orders-enriched", "order-metrics")

    def __init__(self) -> None:
        self.topics: dict[str, dict[int, deque[dict[str, Any]]]] = defaultdict(
            lambda: defaultdict(deque)
        )
        self.dlt: list[dict[str, Any]] = []

    def partition_for(self, key: str) -> int:
        return hash(key) % self.PARTITIONS

    def produce(self, topic: str, key: str, value: dict[str, Any]) -> int:
        partition = self.partition_for(key)
        self.topics[topic][partition].append(value)
        return partition

    def consume(self, topic: str, partition: int, limit: int = 100) -> list[dict[str, Any]]:
        queue = self.topics[topic][partition]
        batch: list[dict[str, Any]] = []
        while queue and len(batch) < limit:
            batch.append(queue.popleft())
        return batch

    def peek(self, topic: str) -> dict[str, list[dict[str, Any]]]:
        return {str(p): list(self.topics[topic][p]) for p in range(self.PARTITIONS)}

    def topic_depth(self, topic: str) -> int:
        return sum(len(self.topics[topic][p]) for p in range(self.PARTITIONS))

    def send_dlt(self, raw: str, error: str) -> None:
        self.dlt.append({"raw": raw, "error": error})
