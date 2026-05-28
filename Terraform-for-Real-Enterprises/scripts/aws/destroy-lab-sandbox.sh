#!/usr/bin/env bash
# Optional: run terraform destroy for dev environment (confirmation required)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../.." && pwd)"
ENV="${ENV:-dev}"
LAB_DIR="${REPO_ROOT}/labs/shared/environments/${ENV}"

if [[ ! -d "$LAB_DIR" ]]; then
  echo "Environment not found: $LAB_DIR" >&2
  exit 1
fi

echo "WARNING: This will destroy Terraform-managed resources in ${ENV}."
read -r -p "Type 'destroy-${ENV}' to confirm: " confirm
[[ "$confirm" == "destroy-${ENV}" ]] || { echo "Aborted."; exit 1; }

cd "$LAB_DIR"
terraform init -input=false
terraform destroy -input=false

echo "Sandbox destroyed. Remote state bucket (bootstrap) is retained."
