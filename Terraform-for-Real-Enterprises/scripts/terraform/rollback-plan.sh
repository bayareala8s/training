#!/usr/bin/env bash
# Generate terraform plan against a previous Git ref (rollback preview)
set -euo pipefail

ENV="dev"
REF="HEAD~1"
REPO_ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
LAB_DIR="${REPO_ROOT}/labs/shared/environments/${ENV}"

while [[ $# -gt 0 ]]; do
  case "$1" in
    --env) ENV="$2"; LAB_DIR="${REPO_ROOT}/labs/shared/environments/${ENV}"; shift 2 ;;
    --ref) REF="$2"; shift 2 ;;
    -h|--help)
      echo "Usage: $0 [--env dev|test|prod] [--ref GIT_REF]"
      exit 0
      ;;
    *) echo "Unknown: $1"; exit 1 ;;
  esac
done

WORKDIR=$(mktemp -d)
trap 'rm -rf "$WORKDIR"' EXIT

git archive "$REF" | tar -x -C "$WORKDIR"
cd "${WORKDIR}/labs/shared/environments/${ENV}"

echo "Rollback plan preview for env=${ENV} ref=${REF}"
terraform init -backend=false
terraform plan -input=false || true

echo "Review plan above. To execute rollback: revert Git ref and run approved apply in CI."
