#!/usr/bin/env bash
set -euo pipefail
NAME=${1:?lab or capstone directory name}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
if [[ -d "$ROOT/terraform/labs/$NAME" ]]; then
  DIR="$ROOT/terraform/labs/$NAME"
elif [[ -d "$ROOT/terraform/capstones/$NAME" ]]; then
  DIR="$ROOT/terraform/capstones/$NAME"
else
  echo "No terraform/labs/$NAME or terraform/capstones/$NAME"
  exit 1
fi
terraform -chdir="$DIR" destroy -auto-approve
