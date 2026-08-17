"""FastAPI HTTP surface for the lab."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse

from .schemas import ChargeRequest
from .service import PaymentService, StoreUnavailableError

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 017 — Stripe Payment Idempotency</title>
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
  <h1>Lab 017 — Stripe Payment Idempotency</h1>
  <p><span class="ok">running</span> Local hands-on lab stack (API + PostgreSQL + Redis)</p>
  <h2>Quick links</h2>
  <ul>
    <li><a href="/docs">Swagger UI</a> — try <code>POST /v1/charges</code> interactively</li>
    <li><a href="/health">Health check</a> — <code>GET /health</code></li>
  </ul>
  <h2>Endpoints</h2>
  <table>
    <tr><th>Method</th><th>Path</th><th>Purpose</th></tr>
    <tr><td>POST</td><td><code>/v1/charges</code></td><td>Create charge (requires <code>Idempotency-Key</code> header)</td></tr>
    <tr><td>POST</td><td><code>/webhooks/stripe</code></td><td>Stripe webhook receiver</td></tr>
  </table>
  <h2>Terminal demo</h2>
  <pre>./scripts/demo_retry.sh</pre>
  <p>Or from the lab directory:</p>
  <pre>curl -X POST http://localhost:8080/v1/charges \\
  -H "Content-Type: application/json" \\
  -H "Idempotency-Key: test-key-1" \\
  -H "X-Tenant-Id: demo" \\
  -d '{"amount_cents": 2500, "currency": "usd"}'</pre>
</body>
</html>"""


def create_app(service: PaymentService) -> FastAPI:
    app = FastAPI(title="Lab 017 — Stripe Payment Idempotency", version="1.0.0")

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 017 — Stripe Payment Idempotency",
            "status": "running",
            "endpoints": {
                "health": "GET /health",
                "charge": "POST /v1/charges (requires Idempotency-Key header)",
                "webhook": "POST /webhooks/stripe",
                "docs": "GET /docs",
            },
        }

    @app.get("/health")
    def health() -> dict[str, str]:
        return {"status": "ok"}

    @app.post("/v1/charges")
    def create_charge(
        body: ChargeRequest,
        idempotency_key: str | None = Header(default=None, alias="Idempotency-Key"),
        x_tenant_id: str | None = Header(default="demo", alias="X-Tenant-Id"),
    ) -> tuple[int, dict[str, Any]] | dict[str, Any]:
        tenant_id = x_tenant_id or "demo"
        try:
            status, payload = service.create_charge(
                tenant_id, idempotency_key or "", body.model_dump()
            )
        except StoreUnavailableError as exc:
            raise HTTPException(status_code=503, detail=str(exc)) from exc
        if status >= 400:
            raise HTTPException(status_code=status, detail=payload)
        return JSONResponse(status_code=status, content=payload)

    @app.post("/webhooks/stripe")
    async def stripe_webhook(request: Request) -> dict[str, Any]:
        event = await request.json()
        processed = service.process_webhook(event)
        return {"processed": processed, "duplicate": not processed}

    return app
