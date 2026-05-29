#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../_common.sh"
require_cmd docker

echo "Lab 03 verification — Docker Compose platform"

if $LOCAL_MODE; then
  docker compose -f "${ROOT}/docker-compose.yml" ps --status running | grep -q user-service || \
    fail "Run: docker compose up -d --build"
  pass "Compose services running"
fi

for port in 8001 8002 8003 8004; do
  if $LOCAL_MODE; then
    curl -sf "http://localhost:${port}/health" >/dev/null || fail "health port ${port}"
    pass "health :${port}"
  fi
done

if $LOCAL_MODE; then
  "${ROOT}/scripts/demo-platform.sh"
fi
pass "End-to-end demo"
echo "Lab 03 PASSED"
