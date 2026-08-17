#!/usr/bin/env bash
set -euo pipefail

pass() { echo "  [PASS] $*"; }
fail() { echo "  [FAIL] $*" >&2; exit 1; }
skip() { echo "  [SKIP] $*"; }

require_cmd() {
  command -v "$1" >/dev/null || fail "Command not found: $1"
}

curl_ok() {
  local url="$1"
  curl -sf "$url" >/dev/null || fail "HTTP check failed: $url"
}

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
PLATFORM_URL="${PLATFORM_URL:-}"
LOCAL_MODE=true
[[ -n "$PLATFORM_URL" ]] && LOCAL_MODE=false

if $LOCAL_MODE; then
  export BASE_USER="http://localhost:8001"
  export BASE_PRODUCT="http://localhost:8002"
  export BASE_ORDER="http://localhost:8003"
  export BASE_NOTIFY="http://localhost:8004"
else
  export BASE_USER="$PLATFORM_URL"
  export BASE_PRODUCT="$PLATFORM_URL"
  export BASE_ORDER="$PLATFORM_URL"
  export BASE_NOTIFY="$PLATFORM_URL"
fi
