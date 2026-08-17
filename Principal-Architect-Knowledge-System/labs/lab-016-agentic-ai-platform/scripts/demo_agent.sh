#!/usr/bin/env bash
# Demo: agentic AI platform — run agent, list runs, invoke tool
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8106}"

echo "==> Health (before)"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/agents/run"
curl -sS -X POST "$BASE_URL/v1/agents/run" \
  -H "Content-Type: application/json" \
  -d '{"agent_id": "support-agent", "task": "search_kb docs about quorum", "tenant_id": "default"}' | python3 -m json.tool

echo "==> GET /v1/agents/runs"
curl -sS "$BASE_URL/v1/agents/runs" | python3 -m json.tool

echo "==> POST /v1/tools/invoke (search_kb)"
curl -sS -X POST "$BASE_URL/v1/tools/invoke" \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "search_kb", "tenant_id": "default", "arguments": {"query": "quorum"}}' | python3 -m json.tool

echo "==> POST /v1/tools/invoke (send_email — approval required)"
curl -sS -X POST "$BASE_URL/v1/tools/invoke" \
  -H "Content-Type: application/json" \
  -d '{"tool_name": "send_email", "tenant_id": "default", "arguments": {"query": "alert"}}' | python3 -m json.tool

echo "==> Health (after)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — agent run completed; send_email blocked by policy"
