#!/usr/bin/env bash
# Demo: chaos engineering — fault enable, experiments, SLO breach
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8103}"

echo "==> Health (before)"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> POST /v1/faults/enable (latency injection)"
curl -sS -X POST "$BASE_URL/v1/faults/enable" \
  -H "Content-Type: application/json" \
  -d '{"fault_type": "latency", "latency_ms": 100, "target": "api-1"}' | python3 -m json.tool

echo "==> POST /v1/experiments/run (latency — should pass)"
curl -sS -X POST "$BASE_URL/v1/experiments/run" \
  -H "Content-Type: application/json" \
  -d '{"name": "dep-slow", "fault_type": "latency", "latency_ms": 50, "target": "api-1", "hypothesis": "p99 stable"}' | python3 -m json.tool

echo "==> POST /v1/faults/disable"
curl -sS -X POST "$BASE_URL/v1/faults/disable" | python3 -m json.tool

echo "==> POST /v1/experiments/run (error rate SLO breach — should fail)"
curl -sS -X POST "$BASE_URL/v1/experiments/run" \
  -H "Content-Type: application/json" \
  -d '{"name": "slo-breach", "fault_type": "error_rate", "error_rate": 1.0, "target": "api-1", "slo_breach": 0.10, "hypothesis": "errors breach SLO"}' | python3 -m json.tool

echo "==> Health (after)"
curl -sS "$BASE_URL/health" | python3 -m json.tool
echo "Done — experiments_fail should be >= 1"
