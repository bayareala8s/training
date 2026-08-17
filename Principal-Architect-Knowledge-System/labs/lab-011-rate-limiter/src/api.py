"""FastAPI HTTP surface for Lab 011."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse

from .schemas import CheckRequest, RedisDownRequest
from .service import RateLimitService

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 011 — Distributed Rate Limiter</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #b45309; font-size: 1.5rem; }
    .ok { display: inline-block; background: #fef3c7; color: #b45309; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #b45309; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 011 — Distributed Rate Limiter</h1>
  <p><span class="ok">running</span> Token bucket (local) + sliding window log (Redis)</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/check</code> — tenant + route quota check</li>
    <li><code>GET /health</code> — allowed/denied stats</li>
    <li><code>POST /v1/chaos/redis-down</code> — fail-open vs fail-closed</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health / stats</a></p>
  <pre>./scripts/demo_rate_limit.sh</pre>
</body>
</html>"""


def create_app(service: RateLimitService) -> FastAPI:
    app = FastAPI(title="Lab 011 — Distributed Rate Limiter", version="1.0.0")

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 011 — Distributed Rate Limiter",
            "status": "running",
            "endpoints": {
                "docs": "GET /docs",
                "health": "GET /health",
                "check": "POST /v1/check",
                "redis_down": "POST /v1/chaos/redis-down",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", **service.stats()}

    @app.post("/v1/check")
    def check_rate(body: CheckRequest) -> JSONResponse:
        result = service.check(body.tenant_id, body.route)
        headers: dict[str, str] = {
            "X-RateLimit-Limit": str(result.limit),
            "X-RateLimit-Remaining": str(result.remaining),
        }
        if result.retry_after is not None:
            headers["Retry-After"] = str(int(result.retry_after))
        status = 200 if result.allowed else 429
        return JSONResponse(
            status_code=status,
            content={
                "allowed": result.allowed,
                "limit": result.limit,
                "remaining": result.remaining,
                "retry_after": result.retry_after,
                "tenant_id": body.tenant_id,
                "route": body.route,
            },
            headers=headers,
        )

    @app.post("/v1/chaos/redis-down")
    def chaos_redis_down(body: RedisDownRequest) -> dict[str, Any]:
        return service.simulate_redis_down(body.enabled, body.mode)

    return app
