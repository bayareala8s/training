#!/usr/bin/env bash
set -euo pipefail
if [[ "${1:-}" != "--yes" ]]; then echo "Usage: $0 --yes"; exit 1; fi
ROOT=$(cd "$(dirname "$0")/.." && pwd)
for d in "$ROOT"/terraform/labs/* "$ROOT"/terraform/capstones/*; do
  [[ -d "$d" && -f "$d/main.tf" ]] || continue
  echo "Destroying $(basename "$d")"
  terraform -chdir="$d" destroy -auto-approve || true
done
