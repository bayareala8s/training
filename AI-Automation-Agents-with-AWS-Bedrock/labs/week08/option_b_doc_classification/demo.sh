#!/usr/bin/env bash
# Capstone Option B — Document Classification demo
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"
# shellcheck disable=SC1091
source .stack.env 2>/dev/null || { echo "Run ./scripts/start.sh && source .stack.env first"; exit 1; }

API="${API_ENDPOINT:?}"
echo "=== Option B: Invoice → queue_invoices ==="
curl -sS -X POST "$API/capstone/document" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/document_invoice.json" | python3 -m json.tool

echo
echo "=== Option B: Contract ==="
curl -sS -X POST "$API/capstone/document" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/document_contract.json" | python3 -m json.tool

echo
echo "=== Option B: Unknown / needs review ==="
curl -sS -X POST "$API/capstone/document" \
  -H "Content-Type: application/json" \
  -d @"$ROOT/week08/samples/document_unknown.json" | python3 -m json.tool

echo
echo "Audit tip: python week06/query_audit.py capstone-doc-invoice"
