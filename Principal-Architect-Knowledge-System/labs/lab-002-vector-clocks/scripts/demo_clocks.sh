#!/usr/bin/env bash
# Demo: vector clocks — local events, send, causal delivery, compare
set -euo pipefail
BASE_URL="${BASE_URL:-http://localhost:8097}"

echo "==> Health"
curl -sS "$BASE_URL/health" | python3 -m json.tool

echo "==> GET /v1/processes"
curl -sS "$BASE_URL/v1/processes" | python3 -m json.tool

echo "==> POST /v1/events/local (P0)"
curl -sS -X POST "$BASE_URL/v1/events/local" \
  -H "Content-Type: application/json" \
  -d '{"process_id": 0, "num_processes": 2}' | python3 -m json.tool

echo "==> POST /v1/messages/send (P0 -> P1)"
curl -sS -X POST "$BASE_URL/v1/messages/send" \
  -H "Content-Type: application/json" \
  -d '{"from": 0, "to": 1, "payload": "hello", "msg_id": "m1"}' | python3 -m json.tool

echo "==> POST /v1/events/local (P1)"
curl -sS -X POST "$BASE_URL/v1/events/local" \
  -H "Content-Type: application/json" \
  -d '{"process_id": 1, "num_processes": 2}' | python3 -m json.tool

echo "==> GET /v1/mailbox/delivered"
curl -sS "$BASE_URL/v1/mailbox/delivered" | python3 -m json.tool

echo "==> POST /v1/clocks/compare"
curl -sS -X POST "$BASE_URL/v1/clocks/compare" \
  -H "Content-Type: application/json" \
  -d '{"clock_a": [1, 1], "clock_b": [2, 2]}' | python3 -m json.tool

echo "Done — relation should be 'before' for [1,1] vs [2,2]"
