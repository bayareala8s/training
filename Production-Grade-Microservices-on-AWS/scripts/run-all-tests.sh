#!/usr/bin/env bash
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
FAILED=0

run_tests_docker() {
  local svc="$1"
  echo ""
  echo "========== Testing ${svc} (Docker) =========="
  docker build -q -t "test-${svc}" "${ROOT}/starters/python/${svc}"
  docker run --rm "test-${svc}" python -m pytest -q tests
}

run_tests_venv() {
  local svc="$1"
  echo ""
  echo "========== Testing ${svc} (venv) =========="
  local venv="${ROOT}/.venv-${svc}"
  python3 -m venv "$venv"
  # shellcheck disable=SC1091
  source "${venv}/bin/activate"
  pip install -q -r "${ROOT}/starters/python/${svc}/requirements.txt"
  cd "${ROOT}/starters/python/${svc}"
  pytest -q
  deactivate
}

if command -v docker >/dev/null && docker info >/dev/null 2>&1; then
  for svc in user-service product-service order-service notification-service; do
    if ! run_tests_docker "$svc"; then
      FAILED=1
    fi
  done
else
  for svc in user-service product-service order-service notification-service; do
    if ! run_tests_venv "$svc"; then
      FAILED=1
    fi
  done
fi

if [[ $FAILED -eq 0 ]]; then
  echo ""
  echo "All tests PASSED"
  exit 0
fi
echo "Some tests FAILED"
exit 1
