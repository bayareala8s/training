#!/usr/bin/env bash
# Provision the full BayLearn MFT lab stack (terraform init + apply).
#
# Usage (repo root):
#   ./scripts/start_stack.sh
#   ./scripts/start_stack.sh --yes
#   BAYLEARN_TF_DIR=infra/environments/lab ./scripts/start_stack.sh --yes
#
# Cost: Transfer Family server bills hourly while ONLINE. Always run stop_stack when done.

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/stack_lib.sh
source "$SCRIPT_DIR/stack_lib.sh"

AUTO_APPROVE=false
while [[ $# -gt 0 ]]; do
  case "$1" in
    -y | --yes) AUTO_APPROVE=true; shift ;;
    -h | --help)
      echo "Usage: $0 [--yes]" >&2
      exit 0
      ;;
    *) echo "Unknown option: $1" >&2; exit 1 ;;
  esac
done

baylearn_require_tools

if [[ ! -f "$BAYLEARN_TF_DIR/terraform.tfvars" ]]; then
  echo "==> Creating terraform.tfvars from example (edit admin_email before shared cohorts)"
  cp "$BAYLEARN_TF_DIR/terraform.tfvars.example" "$BAYLEARN_TF_DIR/terraform.tfvars"
fi

mkdir -p "$BAYLEARN_TF_DIR/.build"

echo "==> terraform init ($BAYLEARN_TF_DIR)"
terraform -chdir="$BAYLEARN_TF_DIR" init -upgrade

apply_tf() {
  if $AUTO_APPROVE; then
    terraform -chdir="$BAYLEARN_TF_DIR" apply -auto-approve
  else
    terraform -chdir="$BAYLEARN_TF_DIR" apply
  fi
}

apply_tf || {
  echo "WARN: first apply failed (often connector host-key scan). Retrying once in 60s..." >&2
  sleep 60
  apply_tf
}

export AWS_REGION="$(baylearn_aws_region)"

ECR="$(baylearn_tf_raw ecr_repository_url)"
if [[ -n "$ECR" && "$ECR" != "null" && "${SKIP_ECS_IMAGE_BUILD:-0}" != "1" ]]; then
  echo "==> Building and pushing ECS Fargate worker image (Lab 9)"
  "$SCRIPT_DIR/build_ecs_worker.sh" || {
    echo "WARN: ECS image build failed. Install Docker or set SKIP_ECS_IMAGE_BUILD=1 after manual push." >&2
  }
fi

echo ""
echo "==> Stack outputs"
terraform -chdir="$BAYLEARN_TF_DIR" output lab_stack_summary
echo ""
echo "Next: ./scripts/verify_labs.sh"
echo "Lab 9 demo: ./scripts/demo_ecs_large_file.sh  (set LAB_LARGE_FILE_MB=10 for smaller file)"
echo "Stop:  ./scripts/stop_stack.sh --yes"
