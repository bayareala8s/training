#!/usr/bin/env bash
# Capstone Option D — Enterprise Agent demo
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source .stack.env 2>/dev/null || { echo "Run ./scripts/start.sh && source .stack.env first"; exit 1; }

API="${API_ENDPOINT:?}"
echo "=== Option D: Summarize (tool_hint) ==="
curl -sS -X POST "$API/capstone/agent" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/agent_multiturn.json" | python3 -m json.tool

echo
echo "=== Option D: Incident triage tool ==="
curl -sS -X POST "$API/capstone/agent" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/agent_incident.json" | python3 -m json.tool

echo
echo "=== Option D: Risky text → deny / pending approval ==="
curl -sS -X POST "$API/capstone/agent" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/agent_risky_deny.json" | python3 -m json.tool

echo
echo "Same session_id shows memory_used=true on second call within session."
