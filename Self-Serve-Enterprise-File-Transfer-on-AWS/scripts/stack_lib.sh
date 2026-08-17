#!/usr/bin/env bash
# Shared helpers for BayLearn MFT lab stack lifecycle.
# shellcheck disable=SC2034

BAYLEARN_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BAYLEARN_TF_DIR="${BAYLEARN_TF_DIR:-$BAYLEARN_ROOT/infra/environments/lab}"
if [[ "$BAYLEARN_TF_DIR" != /* ]]; then
  BAYLEARN_TF_DIR="$BAYLEARN_ROOT/$BAYLEARN_TF_DIR"
fi

baylearn_tf_raw() {
  terraform -chdir="$BAYLEARN_TF_DIR" output -raw "$1" 2>/dev/null || true
}

baylearn_stack_env_name() {
  local f="$BAYLEARN_TF_DIR/terraform.tfvars"
  if [[ -f "$f" ]]; then
    grep -E '^[[:space:]]*environment[[:space:]]*=' "$f" 2>/dev/null | head -1 | sed -E 's/^[[:space:]]*environment[[:space:]]*=[[:space:]]*"([^"]*)".*/\1/' || true
  fi
}

baylearn_require_tools() {
  local missing=0
  for cmd in terraform aws jq; do
    if ! command -v "$cmd" >/dev/null 2>&1; then
      echo "Missing required command: $cmd" >&2
      missing=1
    fi
  done
  if [[ $missing -ne 0 ]]; then
    exit 1
  fi
}

baylearn_aws_region() {
  local r
  r="$(baylearn_tf_raw aws_region)"
  if [[ -n "$r" && "$r" != "null" ]]; then
    echo "$r"
    return
  fi
  if [[ -f "$BAYLEARN_TF_DIR/terraform.tfvars" ]]; then
    r=$(grep -E '^[[:space:]]*aws_region[[:space:]]*=' "$BAYLEARN_TF_DIR/terraform.tfvars" 2>/dev/null | head -1 | sed -E 's/^[[:space:]]*aws_region[[:space:]]*=[[:space:]]*"([^"]*)".*/\1/' || true)
    [[ -n "$r" ]] && echo "$r" && return
  fi
  echo "${AWS_REGION:-${AWS_DEFAULT_REGION:-us-west-2}}"
}
