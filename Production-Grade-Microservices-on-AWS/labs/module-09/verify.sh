#!/usr/bin/env bash
set -euo pipefail
source "$(dirname "$0")/../_common.sh"

echo "Lab 09 verification — CI/CD"

[[ -f "${ROOT}/.github/workflows/ci-service.yml" ]] || fail "CI workflow missing"
pass "CI workflow exists"

[[ -f "${ROOT}/.github/workflows/deploy-ecs.yml" ]] || fail "CD workflow missing"
pass "CD workflow exists"

[[ -x "${ROOT}/scripts/run-all-tests.sh" ]] || fail "test script missing"
"${ROOT}/scripts/run-all-tests.sh"
pass "All unit tests pass"

echo "Lab 09 PASSED"
