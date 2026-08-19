#!/usr/bin/env bash
set -euo pipefail
NAME=${1:?lab directory under terraform/labs or terraform/capstones}
ROOT=$(cd "$(dirname "$0")/.." && pwd)
if [[ -d "$ROOT/terraform/labs/$NAME" ]]; then
  DIR="$ROOT/terraform/labs/$NAME"
elif [[ -d "$ROOT/terraform/capstones/$NAME" ]]; then
  DIR="$ROOT/terraform/capstones/$NAME"
else
  echo "No terraform/labs/$NAME or terraform/capstones/$NAME"
  exit 1
fi
if [[ ! -f "$DIR/terraform.tfvars" && -f "$DIR/terraform.tfvars.example" ]]; then
  cp "$DIR/terraform.tfvars.example" "$DIR/terraform.tfvars"
fi
terraform -chdir="$DIR" init -input=false
terraform -chdir="$DIR" apply -auto-approve
