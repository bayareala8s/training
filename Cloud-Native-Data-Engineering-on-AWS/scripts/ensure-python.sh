#!/usr/bin/env bash
# Resolve Python interpreter with boto3 (prefers repo .venv).
REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
VENV_PY="${REPO_ROOT}/.venv/bin/python3"

if [[ -x "$VENV_PY" ]]; then
  echo "$VENV_PY"
elif python3 -c "import boto3" &>/dev/null; then
  echo "python3"
else
  python3 -m venv "${REPO_ROOT}/.venv"
  "${REPO_ROOT}/.venv/bin/pip" install -q boto3
  echo "$VENV_PY"
fi
