"""Rate limiting algorithms and middleware."""

from __future__ import annotations

import time
from collections import defaultdict, deque
from dataclasses import dataclass, field


@dataclass
class TokenBucket:
    rate: float
    burst: float
    tokens: float = 0.0
    last_refill: float = field(default_factory=time.monotonic)

    def __post_init__(self) -> None:
        self.tokens = self.burst

    def allow(self, n: float = 1.0) -> bool:
        now = time.monotonic()
        elapsed = now - self.last_refill
        self.tokens = min(self.burst, self.tokens + elapsed * self.rate)
        self.last_refill = now
        if self.tokens >= n:
            self.tokens -= n
            return True
        return False


@dataclass
class RateLimitResult:
    allowed: bool
    limit: int
    remaining: int
    retry_after: float | None = None


class InMemoryRedis:
    """ZSET sliding window backing store."""

    def __init__(self) -> None:
        self.zsets: dict[str, deque[float]] = defaultdict(deque)
        self.available: bool = True

    def zadd_prune(self, key: str, now: float, window_seconds: float) -> int:
        if not self.available:
            raise ConnectionError("redis unavailable")
        z = self.zsets[key]
        cutoff = now - window_seconds
        while z and z[0] <= cutoff:
            z.popleft()
        z.append(now)
        return len(z)


REDIS = InMemoryRedis()


class SlidingWindowLog:
    def __init__(self, redis_url: str, window_seconds: float, limit: int = 100) -> None:
        self.redis_url = redis_url
        self.window_seconds = window_seconds
        self.default_limit = limit

    def check(self, key: str, limit: int | None = None) -> RateLimitResult:
        effective_limit = limit if limit is not None else self.default_limit
        now = time.monotonic()
        count = REDIS.zadd_prune(key, now, self.window_seconds)
        allowed = count <= effective_limit
        retry_after = None if allowed else self.window_seconds
        return RateLimitResult(
            allowed=allowed,
            limit=effective_limit,
            remaining=max(0, effective_limit - count),
            retry_after=retry_after,
        )


class RateLimitMiddleware:
    def __init__(self, local: TokenBucket, global_limiter: SlidingWindowLog) -> None:
        self.local = local
        self.global_limiter = global_limiter

    def check(self, tenant_id: str, route: str) -> RateLimitResult:
        if not self.local.allow():
            return RateLimitResult(False, 0, 0, retry_after=1.0)
        key = f"{tenant_id}:{route}"
        return self.global_limiter.check(key, limit=self.global_limiter.default_limit)
