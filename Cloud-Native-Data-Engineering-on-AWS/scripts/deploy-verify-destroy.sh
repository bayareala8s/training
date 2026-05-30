#!/usr/bin/env bash
# Deploy all labs, verify they are running, then tear down (zero ongoing cost).
set -euo pipefail

unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy 2>/dev/null || true
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_REGION="${AWS_REGION:-$AWS_DEFAULT_REGION}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

echo "=== CNDE Labs: Full Deploy → Verify → Teardown ==="
echo

"${SCRIPT_DIR}/start-labs.sh"

echo
echo "=== Running verification... ==="
"${SCRIPT_DIR}/verify-labs.sh"

echo
echo "=== Verification complete. Tearing down to avoid AWS charges... ==="
echo

"${SCRIPT_DIR}/stop-labs.sh" --yes

echo
echo "=== Done. All resources deployed, verified, and destroyed. ==="
