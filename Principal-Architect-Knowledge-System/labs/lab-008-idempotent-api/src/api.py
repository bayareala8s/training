"""FastAPI HTTP surface for Lab 008."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from .schemas import PaymentRequest
from .service import PaymentService

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 008 — Idempotent API</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 720px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #1a5f7a; font-size: 1.5rem; }
    .ok { display: inline-block; background: #e6f4ea; color: #137333; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #1a5f7a; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    table { border-collapse: collapse; width: 100%; margin: 1rem 0; }
    th, td { text-align: left; padding: 0.5rem; border-bottom: 1px solid #e0e0e0; }
  </style>
</head>
<body>
  <h1>Lab 008 — Idempotent API Design</h1>
  <p><span class="ok">running</span> Intro lab — in-memory idempotency store (no database required)</p>
  <p>Graduate to <strong>Lab 017</strong> for PostgreSQL, Stripe mock, webhooks, and sweeper.</p>
  <h2>Quick links</h2>
  <ul>
    <li><a href="/docs">Swagger UI</a> — try <code>POST /v1/payments</code></li>
    <li><a href="/health">Health check</a></li>
  </ul>
  <h2>Example request</h2>
  <pre>curl -X POST http://localhost:8081/v1/payments \\
  -H "Content-Type: application/json" \\
  -H "Idempotency-Key: intro-key-1" \\
  -H "X-Tenant-Id: demo" \\
  -d '{"amount": 10.0, "currency": "USD"}'</pre>
</body>
</html>"""


def create_app(service: PaymentService) -> FastAPI:
    app = FastAPI(title="Lab 008 — Idempotent API Design", version="1.0.0")

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 008 — Idempotent API Design",
            "status": "running",
            "storage": "in-memory",
            "endpoints": {
                "health": "GET /health",
                "payment": "POST /v1/payments (requires Idempotency-Key)",
                "webhook": "POST /v1/webhooks",
                "docs": "GET /docs",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {
            "status": "ok",
            "ledger_entries": service.ledger_count(),
        }

    @app.post("/v1/payments")
    def create_payment(
        body: PaymentRequest,
        idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
        x_tenant_id: str | None = Header(default="demo", alias="X-Tenant-Id"),
    ) -> JSONResponse:
        tenant_id = x_tenant_id or "demo"
        status, payload = service.create_payment(
            tenant_id, idempotency_key or "", body.model_dump()
        )
        if status >= 400:
            raise HTTPException(status_code=status, detail=payload)
        return JSONResponse(status_code=status, content=payload)

    @app.post("/v1/webhooks")
    async def webhook(request: Request) -> dict[str, Any]:
        event = await request.json()
        event_id = event.get("event_id")
        if not event_id:
            raise HTTPException(status_code=400, detail="event_id required")
        processed = service.handle_webhook(str(event_id), event)
        return {"processed": processed, "duplicate": not processed}

    return app
