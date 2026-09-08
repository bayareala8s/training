#!/usr/bin/env bash
# Optional-spend demo: EKS + the ECS lab's RDS (same VPC, no second database).
# Does not apply NAT or Multi-AZ. Stop with ./stop.sh before ../ecs-rds-lab/stop.sh.
set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ECS_DIR="$(cd "${LAB_DIR}/../ecs-rds-lab" && pwd)"
REGION="${AWS_REGION:-us-west-2}"
EXPIRATION="$(date +%Y-%m-%d)"
AVERY="11111111-1111-1111-1111-111111111111"
ACCOUNT="22222222-2222-2222-2222-222222222221"

need() {
  command -v "$1" >/dev/null 2>&1 || {
    echo "Missing required command: $1" >&2
    exit 1
  }
}

need aws
need terraform
need kubectl

if [[ ! -f "${ECS_DIR}/terraform.tfstate" ]]; then
  echo "ECS lab state not found at ${ECS_DIR}/terraform.tfstate" >&2
  echo "Start ../ecs-rds-lab/start.sh first so this lab can reuse that VPC and RDS." >&2
  exit 1
fi

echo "==> Caller identity (region ${REGION})"
aws sts get-caller-identity --output table

echo "==> Refresh ECS outputs (VPC / RDS / ECR / secret) so remote state is complete"
(
  cd "${ECS_DIR}"
  terraform init -input=false >/dev/null
  terraform apply -input=false -auto-approve -refresh-only >/dev/null || \
    terraform apply -input=false -auto-approve
)

ECR_URL="$(terraform -chdir="${ECS_DIR}" output -raw ecr_repository_url)"
SECRET_ARN="$(terraform -chdir="${ECS_DIR}" output -raw secret_arn)"
REPO_NAME="${ECR_URL#*/}"

TAG="$(aws ecr describe-images --region "${REGION}" --repository-name "${REPO_NAME}" \
  --query 'sort_by(imageDetails,& imagePushedAt)[-1].imageTags[0]' --output text)"
if [[ -z "${TAG}" || "${TAG}" == "None" ]]; then
  echo "No image in ${REPO_NAME}. Run ../ecs-rds-lab/start.sh so the shared image exists." >&2
  exit 1
fi
IMAGE="${ECR_URL}:${TAG}"
echo "    Reusing image ${IMAGE} (same OCI image as ECS)"

cd "${LAB_DIR}"
cat > generated.auto.tfvars <<EOF
expiration = "${EXPIRATION}"
EOF

echo "==> terraform init / apply (EKS control plane ~10 min, then one t3.small)"
echo "    EKS control plane bills ~\$0.10/hour from the moment the cluster is ACTIVE."
terraform init -input=false
terraform apply -input=false -auto-approve

CLUSTER="$(terraform output -raw cluster_name)"
echo "==> kubeconfig ${CLUSTER}"
aws eks update-kubeconfig --region "${REGION}" --name "${CLUSTER}"

echo "==> Wait for the node"
kubectl wait --for=condition=Ready node --all --timeout=10m

echo "==> Kubernetes secret from the shared Secrets Manager JSON"
SECRET_JSON="$(aws secretsmanager get-secret-value --region "${REGION}" --secret-id "${SECRET_ARN}" \
  --query SecretString --output text)"
DB_URL="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["url"])' "${SECRET_JSON}")"
DB_USER="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["username"])' "${SECRET_JSON}")"
DB_PASSWORD="$(python3 -c 'import json,sys; print(json.loads(sys.argv[1])["password"])' "${SECRET_JSON}")"

kubectl apply -f "${LAB_DIR}/k8s/namespace.yaml"
kubectl create secret generic baypay-db -n baypay \
  --from-literal=BAYPAY_DB_URL="${DB_URL}" \
  --from-literal=BAYPAY_DB_USER="${DB_USER}" \
  --from-literal=BAYPAY_DB_PASSWORD="${DB_PASSWORD}" \
  --dry-run=client -o yaml | kubectl apply -f -

sed "s|\${CONTAINER_IMAGE}|${IMAGE}|g" \
  "${LAB_DIR}/k8s/deployment.yaml.tpl" > "${LAB_DIR}/k8s/generated-deployment.yaml"

kubectl apply -f "${LAB_DIR}/k8s/generated-deployment.yaml"
kubectl apply -f "${LAB_DIR}/k8s/service.yaml"

echo "==> Wait for the Deployment and NLB hostname"
kubectl -n baypay rollout status deployment/payment-service --timeout=5m

LB=""
for i in $(seq 1 40); do
  LB="$(kubectl -n baypay get svc payment-service -o jsonpath='{.status.loadBalancer.ingress[0].hostname}' 2>/dev/null || true)"
  echo "    [${i}/40] NLB=${LB:-pending}"
  if [[ -n "${LB}" ]]; then
    break
  fi
  sleep 15
done

if [[ -z "${LB}" ]]; then
  echo "NLB hostname not assigned yet. kubectl -n baypay get svc payment-service" >&2
  echo "When you are done: ${LAB_DIR}/stop.sh — then you may destroy the ECS lab." >&2
  exit 1
fi

STATE="down"
for i in $(seq 1 40); do
  CODE="$(curl -sS -o /dev/null -w '%{http_code}' -m 8 "http://${LB}/actuator/health/liveness" || echo 000)"
  echo "    [${i}/40] liveness=${CODE}"
  if [[ "${CODE}" == "200" ]]; then
    STATE="up"
    break
  fi
  sleep 15
done

if [[ "${STATE}" != "up" ]]; then
  echo "Pod is not serving 200 yet. kubectl -n baypay logs deploy/payment-service" >&2
  echo "NLB: http://${LB}" >&2
  echo "STOP: ${LAB_DIR}/stop.sh (do not destroy ECS/RDS first)" >&2
  exit 1
fi

echo
echo "EKS demo is up on the shared RDS (profile eks). ECS may still be serving the same Avery rows."
echo "  Health:  curl -sS http://${LB}/actuator/health/liveness"
echo "  Swagger: http://${LB}/swagger-ui.html"
echo "  List:    curl -sS \"http://${LB}/api/v1/payments?customerId=${AVERY}\""
echo "  Create:  curl -sS -X POST \"http://${LB}/api/v1/payments\" \\"
echo "             -H 'Content-Type: application/json' \\"
echo "             -H 'Idempotency-Key: eks-rds-demo-1' \\"
echo "             -d '{\"customerId\":\"${AVERY}\",\"accountId\":\"${ACCOUNT}\",\"amount\":8.25,\"currency\":\"USD\",\"reference\":\"eks-rds-demo\"}'"
echo
echo "STOP EKS FIRST:  ${LAB_DIR}/stop.sh"
echo "Then, when you want RDS gone: ${ECS_DIR}/stop.sh"
echo "EKS control plane bills until destroy. Expiration=${EXPIRATION} is a tag, not a delete."
