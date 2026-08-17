"""FastAPI HTTP surface for Lab 015."""

from __future__ import annotations

from typing import Any

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse

from .schemas import (
    DocumentIngestRequest,
    DocumentIngestResponse,
    DocumentSummary,
    DocumentsListResponse,
    QueryCitation,
    QueryRequest,
    QueryResponse,
)
from .service import RagService

_LANDING_HTML = """<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="utf-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1" />
  <title>Lab 015 — RAG Platform</title>
  <style>
    body { font-family: system-ui, sans-serif; max-width: 760px; margin: 2rem auto; padding: 0 1rem; color: #1a1a1a; }
    h1 { color: #1d4ed8; font-size: 1.5rem; }
    .ok { display: inline-block; background: #dbeafe; color: #1d4ed8; padding: 0.2rem 0.6rem; border-radius: 4px; font-size: 0.9rem; }
    a { color: #1d4ed8; }
    code { background: #f4f4f4; padding: 0.1rem 0.35rem; border-radius: 3px; }
    pre { background: #f6f8fa; padding: 1rem; overflow-x: auto; border-radius: 6px; font-size: 0.85rem; }
    ol li { margin: 0.5rem 0; }
  </style>
</head>
<body>
  <h1>Lab 015 — RAG Platform</h1>
  <p><span class="ok">running</span> In-memory vector store — ingest, hybrid retrieval, LLM gateway stub</p>
  <h2>Demo flow</h2>
  <ol>
    <li><code>POST /v1/documents</code> — ingest document text or file path</li>
    <li><code>GET /v1/documents</code> — list indexed documents</li>
    <li><code>POST /v1/query</code> — hybrid retrieval + answer with citations</li>
  </ol>
  <p><a href="/docs">Swagger UI</a> · <a href="/health">Health</a></p>
  <pre>./scripts/demo_rag.sh</pre>
</body>
</html>"""


def create_app(service: RagService | None = None) -> FastAPI:
    rag = service or RagService()
    app = FastAPI(title="Lab 015 — RAG Platform", version="1.0.0")

    @app.get("/", response_model=None)
    def root(request: Request) -> HTMLResponse | dict[str, Any]:
        accept = request.headers.get("accept", "")
        if "text/html" in accept and "application/json" not in accept.split(",")[0]:
            return HTMLResponse(_LANDING_HTML)
        return {
            "service": "Lab 015 — RAG Platform",
            "status": "running",
            "endpoints": {
                "docs": "GET /docs",
                "health": "GET /health",
                "ingest": "POST /v1/documents",
                "list": "GET /v1/documents",
                "query": "POST /v1/query",
            },
        }

    @app.get("/health")
    def health() -> dict[str, Any]:
        return {"status": "ok", "lab": "lab-015", **rag.stats()}

    @app.post("/v1/documents", status_code=201)
    def ingest_document(body: DocumentIngestRequest) -> DocumentIngestResponse:
        try:
            count = rag.ingest_document(body.doc_id, body.tenant_id, body.text, body.path)
        except FileNotFoundError as exc:
            raise HTTPException(status_code=404, detail=str(exc)) from exc
        except ValueError as exc:
            raise HTTPException(status_code=400, detail=str(exc)) from exc
        return DocumentIngestResponse(
            doc_id=body.doc_id,
            tenant_id=body.tenant_id,
            chunks_ingested=count,
        )

    @app.get("/v1/documents")
    def list_documents() -> DocumentsListResponse:
        docs = rag.list_documents()
        return DocumentsListResponse(
            documents=[
                DocumentSummary(
                    doc_id=d.doc_id,
                    tenant_id=d.tenant_id,
                    chunk_count=d.chunk_count,
                )
                for d in docs
            ],
            total_chunks=len(rag.store.chunks),
        )

    @app.post("/v1/query")
    def query(body: QueryRequest) -> QueryResponse:
        result = rag.query(body.question, body.tenant_id, top_k=body.top_k)
        citations = [QueryCitation(**c) for c in result["citations"]]
        return QueryResponse(
            question=result["question"],
            answer=result["answer"],
            citations=citations,
        )

    return app
