#!/usr/bin/env bash
# cleanup-lab07.sh — Destroy BayLearn Module 07 lab resources
# Cost warning: run at end of session. Versioned buckets must be emptied first.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../.." && pwd)"
ENV_DIR="${ROOT}/infrastructure/terraform/environments/lab07"

echo "=== BayLearn Lab 07 cleanup ==="
echo "Environment: ${ENV_DIR}"
echo "Fiction notice: NorthStar lab resources only."

if [[ ! -d "${ENV_DIR}" ]]; then
  echo "ERROR: lab07 environment not found at ${ENV_DIR}" >&2
  exit 1
fi

cd "${ENV_DIR}"

if [[ ! -d .terraform && ! -f .terraform.lock.hcl ]]; then
  echo "Initializing Terraform (required for destroy)..."
  terraform init -input=false
fi

if [[ ! -f terraform.tfvars ]]; then
  echo "WARNING: terraform.tfvars not found. Destroy may fail if state expects variables."
fi

BUCKET="$(terraform output -raw primary_bucket_name 2>/dev/null || true)"
REPLICA="$(terraform output -raw replica_bucket_name 2>/dev/null || true)"
REGION="$(terraform output -raw name_prefix >/dev/null 2>&1; grep -E '^aws_region' terraform.tfvars 2>/dev/null | cut -d'"' -f2 || echo us-east-1)"
REPLICA_REGION="$(grep -E '^replica_region' terraform.tfvars 2>/dev/null | cut -d'"' -f2 || echo us-west-2)"

empty_versioned_bucket() {
  local bucket="$1"
  local region="$2"
  if [[ -z "${bucket}" || "${bucket}" == "null" ]]; then
    return 0
  fi
  echo "Emptying versioned bucket s3://${bucket} (region ${region})..."
  aws s3api list-object-versions --bucket "${bucket}" --region "${region}" --output json \
    | python3 -c '
import json,sys
data=json.load(sys.stdin)
objs=[]
for v in data.get("Versions",[]) or []:
  objs.append({"Key":v["Key"],"VersionId":v["VersionId"]})
for m in data.get("DeleteMarkers",[]) or []:
  objs.append({"Key":m["Key"],"VersionId":m["VersionId"]})
# print batches of 1000
for i in range(0,len(objs),1000):
  print(json.dumps({"Objects":objs[i:i+1000],"Quiet":True}))
' | while read -r payload; do
    if [[ -n "${payload}" ]]; then
      aws s3api delete-objects --bucket "${bucket}" --region "${region}" --delete "${payload}" >/dev/null || true
    fi
  done
}

if command -v aws >/dev/null 2>&1; then
  empty_versioned_bucket "${BUCKET}" "${REGION:-us-east-1}"
  if [[ -n "${REPLICA}" && "${REPLICA}" != "null" ]]; then
    empty_versioned_bucket "${REPLICA}" "${REPLICA_REGION:-us-west-2}"
  fi
else
  echo "WARNING: AWS CLI not found; terraform destroy may fail on non-empty versioned buckets."
fi

echo "Running terraform destroy..."
terraform destroy -auto-approve

echo "=== Cleanup complete ==="
echo "Verify in console: no Module=07 Lab-tagged resources remain (KMS may be PendingDeletion)."
echo "Confirm budget: disable unused alarms/subscriptions if any residual."
