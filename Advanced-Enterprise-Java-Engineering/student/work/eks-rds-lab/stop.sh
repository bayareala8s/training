#!/usr/bin/env bash
# Tear down the optional EKS overlay only. Leaves the ECS VPC + RDS in place.
set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REGION="${AWS_REGION:-us-west-2}"
cd "${LAB_DIR}"

if [[ ! -d .terraform ]]; then
  echo "No .terraform directory. Nothing to destroy, or run terraform init first." >&2
  exit 1
fi

echo "This destroys the EKS cluster, node, NLB, and the extra RDS SG rule."
echo "It does NOT destroy RDS, the VPC, or the ECS ALB. Run ../ecs-rds-lab/stop.sh after this."
if [[ "${1:-}" != "-y" && "${1:-}" != "--yes" ]]; then
  read -r -p "Type DESTROY to continue: " confirm
  if [[ "${confirm}" != "DESTROY" ]]; then
    echo "Aborted. EKS control plane is still billing."
    exit 1
  fi
fi

if command -v kubectl >/dev/null 2>&1 && kubectl cluster-info >/dev/null 2>&1; then
  kubectl delete -f "${LAB_DIR}/k8s/service.yaml" --ignore-not-found=true || true
  kubectl delete ns baypay --ignore-not-found=true --wait=false || true
  echo "Waiting 30s for the NLB to drop so Terraform can finish..."
  sleep 30
fi

terraform destroy -input=false -auto-approve
rm -f generated.auto.tfvars k8s/generated-deployment.yaml

echo
echo "EKS destroy finished. Confirm in us-west-2 that baypay-eksrd-cluster is gone."
echo "RDS baypay-ecsrd-pg is still up (shared). Destroy it with ../ecs-rds-lab/stop.sh."
