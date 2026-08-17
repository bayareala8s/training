"""Rate limit service — API/CLI orchestration."""

from __future__ import annotations

from typing import Any

from .models import REDIS, RateLimitMiddleware, RateLimitResult, SlidingWindowLog, TokenBucket


class RateLimitService:
    """Two-tier rate limiter with chaos simulation hooks."""

    def __init__(self) -> None:
        self.local_bucket = TokenBucket(rate=100.0, burst=200.0)
        self.global_limiter = SlidingWindowLog("redis://localhost", 60.0, limit=100)
        self.middleware = RateLimitMiddleware(self.local_bucket, self.global_limiter)
        self.redis_down = False
        self.fail_mode = "fail-closed"
        self.allowed_total = 0
        self.denied_total = 0
        self.checks_total = 0

    def check(self, tenant_id: str, route: str) -> RateLimitResult:
        self.checks_total += 1
        if self.redis_down:
            if self.fail_mode == "fail-open":
                result = RateLimitResult(True, 100, 100)
            else:
                result = RateLimitResult(False, 0, 0, retry_after=60.0)
        else:
            try:
                result = self.middleware.check(tenant_id, route)
            except ConnectionError:
                if self.fail_mode == "fail-open":
                    result = RateLimitResult(True, 100, 100)
                else:
                    result = RateLimitResult(False, 0, 0, retry_after=60.0)
        if result.allowed:
            self.allowed_total += 1
        else:
            self.denied_total += 1
        return result

    def simulate_redis_down(self, enabled: bool, mode: str = "fail-closed") -> dict[str, Any]:
        self.redis_down = enabled
        self.fail_mode = mode
        REDIS.available = not enabled
        return {
            "redis_down": enabled,
            "fail_mode": mode,
            "redis_available": REDIS.available,
        }

    def stats(self) -> dict[str, Any]:
        return {
            "checks_total": self.checks_total,
            "allowed_total": self.allowed_total,
            "denied_total": self.denied_total,
            "redis_down": self.redis_down,
            "fail_mode": self.fail_mode,
            "local_burst": self.local_bucket.burst,
            "global_limit": self.global_limiter.default_limit,
            "window_seconds": self.global_limiter.window_seconds,
        }

    def reset(self) -> None:
        REDIS.zsets.clear()
        self.allowed_total = 0
        self.denied_total = 0
        self.checks_total = 0
