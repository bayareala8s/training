"""Redis-backed queue simulating SQS webhook delivery (in-memory fallback)."""

from __future__ import annotations

import json
import threading
from collections import deque
from typing import Any


class WebhookQueue:
    def __init__(self, redis_url: str | None = None, queue_name: str = "stripe-webhooks") -> None:
        self.queue_name = queue_name
        self._memory: deque[dict[str, Any]] = deque()
        self._lock = threading.Lock()
        self._redis = None
        if redis_url:
            try:
                import redis

                self._redis = redis.from_url(redis_url, decode_responses=True)
            except Exception:
                self._redis = None

    def publish(self, message: dict[str, Any]) -> None:
        payload = json.dumps(message)
        if self._redis:
            self._redis.lpush(self.queue_name, payload)
            return
        with self._lock:
            self._memory.append(message)

    def consume(self, timeout_seconds: int = 1) -> dict[str, Any] | None:
        if self._redis:
            item = self._redis.brpop(self.queue_name, timeout=timeout_seconds)
            if not item:
                return None
            return json.loads(item[1])
        with self._lock:
            if self._memory:
                return self._memory.popleft()
        return None

    def depth(self) -> int:
        if self._redis:
            return int(self._redis.llen(self.queue_name))
        with self._lock:
            return len(self._memory)
