#!/usr/bin/env bash
# Demo: RAG platform — ingest, list, query with citations
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8105}"

echo "==> Health (before)"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/documents (sample_docs/quorum.txt)"
curl -sS -X POST "$BASE_URL/v1/documents" \
  -H "Content-Type: application/json" \
  -d '{"doc_id": "quorum", "tenant_id": "default", "path": "sample_docs/quorum.txt"}' | python3 -m json.tool

echo "==> GET /v1/documents"
curl -sS "$BASE_URL/v1/documents" | python3 -m json.tool

echo "==> POST /v1/query"
curl -sS -X POST "$BASE_URL/v1/query" \
  -H "Content-Type: application/json" \
  -d '{"question": "What is quorum replication?", "tenant_id": "default"}' | python3 -m json.tool

echo "==> Health (after)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — document ingested; query returns answer with citations"
