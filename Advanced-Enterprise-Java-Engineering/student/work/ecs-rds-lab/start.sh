#!/usr/bin/env bash
# Optional-spend demo: ECS Fargate + single-AZ RDS Postgres in us-west-2.
# Does not apply NAT, EKS, or Multi-AZ. Stop with ./stop.sh the same day.
set -euo pipefail

LAB_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${LAB_DIR}/../../.." && pwd)"
BAYPAY_DIR="${REPO_ROOT}/reference-apps/baypay"
DOCKERFILE="${LAB_DIR}/Dockerfile"
REGION="${AWS_REGION:-us-west-2}"
EXPIRATION="$(date +%Y-%m-%d)"
TAG="$(date +%Y%m%d%H%M%S)"
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
need docker

if [[ ! -f "${DOCKERFILE}" ]]; then
  echo "Dockerfile not found: ${DOCKERFILE}" >&2
  exit 1
fi
if [[ ! -d "${BAYPAY_DIR}" ]]; then
  echo "BayPay tree not found: ${BAYPAY_DIR}" >&2
  exit 1
fi

echo "==> Caller identity (region ${REGION})"
aws sts get-caller-identity --output table
docker info >/dev/null

cd "${LAB_DIR}"

cat > generated.auto.tfvars <<EOF
expiration      = "${EXPIRATION}"
deploy_service  = false
container_image = ""
EOF

echo "==> terraform init"
terraform init -input=false

echo "==> Phase 1: VPC, ALB, ECR, IAM, single-AZ RDS (no service yet)"
echo "    RDS commonly takes 5–10 minutes. ALB starts billing when this apply finishes."
terraform apply -input=false -auto-approve

ECR_URL="$(terraform output -raw ecr_repository_url)"
IMAGE="${ECR_URL}:${TAG}"

echo "==> Package payment-service on the host (skipTests; JAR is platform-neutral)"
(
  cd "${BAYPAY_DIR}"
  export JAVA_HOME="${JAVA_HOME:-/opt/homebrew/opt/openjdk@21}"
  ./mvnw -pl payment-service -am -DskipTests package
)

echo "==> Build linux/amd64 JRE image (Fargate is X86_64; do not push :latest)"
docker build --platform linux/amd64 \
  -f "${DOCKERFILE}" \
  -t "${IMAGE}" \
  "${BAYPAY_DIR}"

echo "==> Push ${IMAGE}"
aws ecr get-login-password --region "${REGION}" \
  | docker login --username AWS --password-stdin "${ECR_URL%%/*}"
docker push "${IMAGE}"

cat > generated.auto.tfvars <<EOF
expiration      = "${EXPIRATION}"
deploy_service  = true
container_image = "${IMAGE}"
EOF

echo "==> Phase 2: task definition + service (profile ecs, secrets from Secrets Manager)"
terraform apply -input=false -auto-approve

ALB_DNS="$(terraform output -raw alb_dns_name)"
TG_ARN="$(terraform output -raw target_group_arn)"

echo "==> Waiting for ALB target healthy (first Hibernate ddl-auto can take a few minutes)"
for i in $(seq 1 40); do
  STATE="$(aws elbv2 describe-target-health --region "${REGION}" --target-group-arn "${TG_ARN}" \
    --query 'TargetHealthDescriptions[0].TargetHealth.State' --output text 2>/dev/null || echo none)"
  echo "    [${i}/40] target=${STATE}"
  if [[ "${STATE}" == "healthy" ]]; then
    break
  fi
  sleep 15
done

if [[ "${STATE}" != "healthy" ]]; then
  echo "Target is not healthy yet. Check CloudWatch /ecs/baypay-ecsrd/payment-service" >&2
  echo "ALB: http://${ALB_DNS}" >&2
  echo "When you are done, run ${LAB_DIR}/stop.sh — ALB and RDS still bill while this stack exists." >&2
  exit 1
fi

echo
echo "Demo is up. Avery is seeded (profile ecs, not prod)."
echo "  Health:  curl -sS http://${ALB_DNS}/actuator/health/liveness"
echo "  List:    curl -sS \"http://${ALB_DNS}/api/v1/payments?customerId=${AVERY}\""
echo "  Create:  curl -sS -X POST \"http://${ALB_DNS}/api/v1/payments\" \\"
echo "             -H 'Content-Type: application/json' \\"
echo "             -H 'Idempotency-Key: ecs-rds-demo-1' \\"
echo "             -d '{\"customerId\":\"${AVERY}\",\"accountId\":\"${ACCOUNT}\",\"amount\":12.50,\"currency\":\"USD\",\"reference\":\"ecs-rds-demo\"}'"
echo
echo "STOP THE METER:  ${LAB_DIR}/stop.sh"
echo "desired_count=0 does not stop ALB or RDS. Expiration=${EXPIRATION} is a tag, not a delete."
