#!/usr/bin/env bash
# End-to-end test: Modules 7–9 labs against live AWS. Destroys resources when done.
set -uo pipefail

unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy 2>/dev/null || true
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_REGION="${AWS_REGION:-$AWS_DEFAULT_REGION}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TF_DIR="${REPO_ROOT}/infrastructure/environments/dev"
PYTHON="$("${SCRIPT_DIR}/ensure-python.sh")"
REPORT="${REPO_ROOT}/scripts/test-modules-7-9-report.txt"

RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

PASS=0
FAIL=0
SKIP=0

log()  { echo -e "${GREEN}[test]${NC} $*" | tee -a "$REPORT"; }
warn() { echo -e "${YELLOW}[test]${NC} $*" | tee -a "$REPORT"; }
fail() { echo -e "${RED}[FAIL]${NC} $*" | tee -a "$REPORT"; FAIL=$((FAIL + 1)); }
ok()   { echo -e "${GREEN}[PASS]${NC} $*" | tee -a "$REPORT"; PASS=$((PASS + 1)); }
skip() { echo -e "${YELLOW}[SKIP]${NC} $*" | tee -a "$REPORT"; SKIP=$((SKIP + 1)); }

ACCOUNT_ID=""
BUCKET=""
KMS_ALIAS="alias/cnde-dev-datalake-key"
LAB71="${REPO_ROOT}/modules/module-07-security-governance/labs/lab-7.1-kms-bucket-policies"
LAB72="${REPO_ROOT}/modules/module-07-security-governance/labs/lab-7.2-iam-rbac-data-zones"
LAB73="${REPO_ROOT}/modules/module-07-security-governance/labs/lab-7.3-governance-audit"
LAB91="${REPO_ROOT}/modules/module-09-ai-ml-data/labs/lab-9.1-ml-dataset-prep"
LAB92="${REPO_ROOT}/modules/module-09-ai-ml-data/labs/lab-9.2-feature-store-pipeline"
LAB93="${REPO_ROOT}/modules/module-09-ai-ml-data/labs/lab-9.3-ai-data-quality"

cleanup_lab7() {
  log "Cleaning up Lab 7 resources (IAM roles, KMS key)..."
  for PAIR in "cnde-dev-analyst-curated:analyst-curated-read" \
              "cnde-dev-engineer-pipeline:engineer-pipeline-write" \
              "cnde-dev-steward-quarantine:steward-quarantine"; do
    ROLE="${PAIR%%:*}"
    POLICY="${PAIR##*:}"
    aws iam delete-role-policy --role-name "$ROLE" --policy-name "$POLICY" 2>/dev/null || true
    aws iam delete-role --role-name "$ROLE" 2>/dev/null || true
  done
  KEY_ID=$(aws kms describe-key --key-id "$KMS_ALIAS" --query 'KeyMetadata.KeyId' --output text 2>/dev/null || echo "")
  if [[ -n "$KEY_ID" && "$KEY_ID" != "None" ]]; then
    aws kms disable-key --key-id "$KEY_ID" >> "$REPORT" 2>&1 || true
    aws kms schedule-key-deletion --key-id "$KEY_ID" --pending-window-in-days 7 >> "$REPORT" 2>&1 || true
    aws kms delete-alias --alias-name "$KMS_ALIAS" >> "$REPORT" 2>&1 || true
  fi
}

trap cleanup_lab7 EXIT

# ---------------------------------------------------------------------------
echo "=== CNDE Modules 7–9 Lab Test ===" | tee "$REPORT"
echo "Started: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$REPORT"
echo | tee -a "$REPORT"

"${REPO_ROOT}/.venv/bin/pip" install -q boto3 pandas pyarrow 2>/dev/null || \
  "$PYTHON" -m pip install -q boto3 pandas pyarrow 2>/dev/null || true

ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# ---------------------------------------------------------------------------
# DEPLOY
# ---------------------------------------------------------------------------
BUCKET=$(terraform -chdir="$TF_DIR" output -raw data_lake_bucket 2>/dev/null || echo "")
if [[ -z "$BUCKET" ]] || ! aws s3api head-bucket --bucket "$BUCKET" &>/dev/null; then
  log "Phase 0: Deploy infrastructure"
  if ! "${SCRIPT_DIR}/start-labs.sh" >> "$REPORT" 2>&1; then
    fail "start-labs.sh failed"
    exit 1
  fi
  ok "Infrastructure deployed"
else
  log "Phase 0: Using existing deployment (${BUCKET})"
  ok "Infrastructure present"
fi

BUCKET=$(terraform -chdir="$TF_DIR" output -raw data_lake_bucket)
DASHBOARD=$(terraform -chdir="$TF_DIR" output -raw dashboard_name 2>/dev/null || echo "")
SNS_CRITICAL=$(terraform -chdir="$TF_DIR" output -raw sns_critical_topic_arn 2>/dev/null || echo "")
SNS_WARNING=$(terraform -chdir="$TF_DIR" output -json 2>/dev/null | python3 -c \
  "import json,sys; d=json.load(sys.stdin); print(d.get('sns_warning_topic_arn',{}).get('value',''))" 2>/dev/null || echo "")

log "Bucket=${BUCKET} Account=${ACCOUNT_ID}"

# Seed curated zone placeholder for RBAC tests
echo '{"order_id":"cur-001","amount":100}' | aws s3 cp - "s3://${BUCKET}/curated/sales/fact_orders/test.json" >> "$REPORT" 2>&1 || true

# ---------------------------------------------------------------------------
# MODULE 7
# ---------------------------------------------------------------------------
log "Phase 7: Module 7 — Security & Governance"

# Lab 7.1: KMS encryption
export BUCKET
cd "$LAB71"
if ./scripts/apply_encryption.sh >> "$REPORT" 2>&1; then
  ENC=$(aws s3api get-bucket-encryption --bucket "$BUCKET" \
    --query 'ServerSideEncryptionConfiguration.Rules[0].ApplyServerSideEncryptionByDefault.SSEAlgorithm' \
    --output text 2>/dev/null || echo "")
  if [[ "$ENC" == "aws:kms" ]]; then
    ok "M7 Lab 7.1: SSE-KMS default encryption enabled"
  else
    fail "M7 Lab 7.1: Expected aws:kms, got ${ENC}"
  fi
  if aws kms describe-key --key-id "$KMS_ALIAS" --query 'KeyMetadata.Enabled' --output text 2>/dev/null | grep -q True; then
    ok "M7 Lab 7.1: KMS key alias ${KMS_ALIAS} active"
  else
    fail "M7 Lab 7.1: KMS key not found or disabled"
  fi
else
  fail "M7 Lab 7.1: apply_encryption.sh failed"
fi

# Lab 7.2: IAM RBAC roles
cd "$LAB72"
CALLER_ARN=$(aws sts get-caller-identity --query Arn --output text)
ASSUME_DOC='{"Version":"2012-10-17","Statement":[{"Effect":"Allow","Principal":{"AWS":["arn:aws:iam::'"$ACCOUNT_ID"':root","'"$CALLER_ARN"'"]},"Action":"sts:AssumeRole"}]}'
for ROLE in cnde-dev-analyst-curated cnde-dev-engineer-pipeline cnde-dev-steward-quarantine; do
  aws iam create-role --role-name "$ROLE" --assume-role-policy-document "$ASSUME_DOC" >> "$REPORT" 2>&1 || true
done
sleep 10

for PAIR in "cnde-dev-analyst-curated:analyst-curated-read" \
            "cnde-dev-engineer-pipeline:engineer-pipeline-write" \
            "cnde-dev-steward-quarantine:steward-quarantine"; do
  ROLE="${PAIR%%:*}"
  POLICY="${PAIR##*:}"
  sed "s/BUCKET_NAME/${BUCKET}/g" "policies/${POLICY}.json" > "/tmp/${POLICY}-resolved.json"
  aws iam put-role-policy --role-name "$ROLE" --policy-name "${POLICY}" \
    --policy-document "file:///tmp/${POLICY}-resolved.json" >> "$REPORT" 2>&1
done
ok "M7 Lab 7.2: IAM roles and zone policies attached"

# Test RBAC via IAM policy simulation (works without sts:AssumeRole on caller)
simulate_s3() {
  local role_arn="$1" action="$2" resource="$3"
  aws iam simulate-principal-policy \
    --policy-source-arn "$role_arn" \
    --action-names "$action" \
    --resource-arns "$resource" \
    --query 'EvaluationResults[0].EvalDecision' --output text 2>/dev/null || echo "error"
}

ANALYST_ARN="arn:aws:iam::${ACCOUNT_ID}:role/cnde-dev-analyst-curated"
ENGINEER_ARN="arn:aws:iam::${ACCOUNT_ID}:role/cnde-dev-engineer-pipeline"

RAW_LIST=$(simulate_s3 "$ANALYST_ARN" "s3:ListBucket" "arn:aws:s3:::${BUCKET}")
CURATED_GET=$(simulate_s3 "$ANALYST_ARN" "s3:GetObject" "arn:aws:s3:::${BUCKET}/curated/sales/fact_orders/test.json")
ENG_RAW_LIST=$(simulate_s3 "$ENGINEER_ARN" "s3:ListBucket" "arn:aws:s3:::${BUCKET}")

if [[ "$RAW_LIST" == "explicitDeny" || "$RAW_LIST" == "implicitDeny" ]]; then
  ok "M7 Lab 7.2: Analyst denied ListBucket on raw (simulated: ${RAW_LIST})"
else
  fail "M7 Lab 7.2: Analyst should be denied raw access, got ${RAW_LIST}"
fi

if [[ "$CURATED_GET" == "allowed" ]]; then
  ok "M7 Lab 7.2: Analyst allowed GetObject on curated/"
else
  fail "M7 Lab 7.2: Analyst should read curated/, got ${CURATED_GET}"
fi

if [[ "$ENG_RAW_LIST" == "allowed" ]]; then
  ok "M7 Lab 7.2: Engineer allowed ListBucket on bucket"
else
  fail "M7 Lab 7.2: Engineer should list bucket, got ${ENG_RAW_LIST}"
fi

# Lab 7.3: Governance audit checks
cd "$LAB73"
export BUCKET REPORT_DIR="/tmp/cnde-audit-evidence"
rm -rf "$REPORT_DIR"
if ./scripts/run_audit_checks.sh >> "$REPORT" 2>&1; then
  if [[ -f "${REPORT_DIR}/s3-encryption.txt" && -f "${REPORT_DIR}/iam-roles.txt" ]]; then
    ok "M7 Lab 7.3: Audit evidence collected"
  else
    fail "M7 Lab 7.3: Missing audit evidence files"
  fi
  if grep -qi "aws:kms\|SSEAlgorithm" "${REPORT_DIR}/s3-encryption.txt" 2>/dev/null; then
    ok "M7 Lab 7.3: Encryption evidence documents KMS"
  else
    fail "M7 Lab 7.3: Encryption evidence incomplete"
  fi
else
  fail "M7 Lab 7.3: run_audit_checks.sh failed"
fi

# ---------------------------------------------------------------------------
# MODULE 8
# ---------------------------------------------------------------------------
log "Phase 8: Module 8 — Monitoring & Operations"

# Lab 8.1: CloudWatch dashboard
if [[ -n "$DASHBOARD" ]]; then
  if aws cloudwatch get-dashboard --dashboard-name "$DASHBOARD" >> "$REPORT" 2>&1; then
    ok "M8 Lab 8.1: CloudWatch dashboard '${DASHBOARD}' exists"
  else
    fail "M8 Lab 8.1: Dashboard not found"
  fi
else
  fail "M8 Lab 8.1: dashboard_name output missing"
fi

# Lab 8.2: SNS topics and alarms
if [[ -n "$SNS_CRITICAL" ]]; then
  if aws sns get-topic-attributes --topic-arn "$SNS_CRITICAL" >> "$REPORT" 2>&1; then
    ok "M8 Lab 8.2: SNS critical topic exists"
  else
    fail "M8 Lab 8.2: SNS critical topic missing"
  fi
  MSG_ID=$(aws sns publish --topic-arn "$SNS_CRITICAL" \
    --message "CNDE lab test alert $(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    --query 'MessageId' --output text 2>/dev/null || echo "")
  if [[ -n "$MSG_ID" && "$MSG_ID" != "None" ]]; then
    ok "M8 Lab 8.2: SNS publish to critical topic succeeded"
  else
    fail "M8 Lab 8.2: SNS publish failed"
  fi
else
  fail "M8 Lab 8.2: sns_critical_topic_arn missing"
fi

ALARM_COUNT=$(aws cloudwatch describe-alarms \
  --alarm-name-prefix "cnde-dev-" \
  --query 'length(MetricAlarms)' --output text 2>/dev/null || echo 0)
if [[ "${ALARM_COUNT}" != "None" && "${ALARM_COUNT}" -gt 0 ]]; then
  ok "M8 Lab 8.2: ${ALARM_COUNT} CloudWatch alarm(s) deployed"
else
  fail "M8 Lab 8.2: No CloudWatch alarms found"
fi

# Publish custom quality metric (Lab 8.1 widget source)
if aws cloudwatch put-metric-data \
  --namespace "CNDE/DataQuality" \
  --metric-data "MetricName=ValidationPassRate,Value=99.5,Unit=Percent,Dimensions=[{Name=Dataset,Value=retail/orders},{Name=Environment,Value=dev}]" \
  >> "$REPORT" 2>&1; then
  ok "M8 Lab 8.1: Custom CNDE/DataQuality metric published"
else
  fail "M8 Lab 8.1: put-metric-data failed"
fi

# Lab 8.3: Cost allocation tags
TAGS=$(aws s3api get-bucket-tagging --bucket "$BUCKET" --output json 2>/dev/null || echo "{}")
for KEY in Project Environment Course ManagedBy; do
  if echo "$TAGS" | grep -q "\"Key\": \"${KEY}\""; then
    ok "M8 Lab 8.3: S3 bucket has tag ${KEY}"
  else
    fail "M8 Lab 8.3: Missing tag ${KEY} on data lake bucket"
  fi
done

# ---------------------------------------------------------------------------
# MODULE 9
# ---------------------------------------------------------------------------
log "Phase 9: Module 9 — AI/ML Data Engineering"

# Lab 9.1: ML dataset prep
cd "$LAB91"
rm -rf output
if "$PYTHON" src/prepare_ml_dataset.py --output output >> "$REPORT" 2>&1; then
  if [[ -f output/train.parquet && -f output/validation.parquet && -f output/test.parquet && -f output/dataset_manifest.json ]]; then
    ok "M9 Lab 9.1: ML dataset splits and manifest generated"
  else
    fail "M9 Lab 9.1: Missing output artifacts"
  fi
else
  fail "M9 Lab 9.1: prepare_ml_dataset.py failed"
fi

# Upload to S3 ml/ zone
if aws s3 sync output/ "s3://${BUCKET}/ml/datasets/lab91/" >> "$REPORT" 2>&1; then
  ok "M9 Lab 9.1: ML datasets uploaded to s3://${BUCKET}/ml/datasets/lab91/"
else
  fail "M9 Lab 9.1: S3 upload failed"
fi

# Lab 9.2: Feature store pipeline
cd "$LAB92"
rm -rf output
if "$PYTHON" src/feature_pipeline.py --output output/ml/features >> "$REPORT" 2>&1; then
  if [[ -f output/ml/features/pipeline_manifest.json ]]; then
    ok "M9 Lab 9.2: Feature pipeline manifest generated"
  else
    fail "M9 Lab 9.2: pipeline_manifest.json missing"
  fi
  FG_COUNT=$(find output/ml/features -name 'features.parquet' 2>/dev/null | wc -l | tr -d ' ')
  if [[ "${FG_COUNT}" -ge 2 ]]; then
    ok "M9 Lab 9.2: ${FG_COUNT} feature group Parquet files written"
  else
    fail "M9 Lab 9.2: Expected 2+ feature groups, got ${FG_COUNT}"
  fi
else
  fail "M9 Lab 9.2: feature_pipeline.py failed"
fi

if aws s3 sync output/ml/features/ "s3://${BUCKET}/ml/features/" >> "$REPORT" 2>&1; then
  ok "M9 Lab 9.2: Feature artifacts uploaded to s3://${BUCKET}/ml/features/"
else
  fail "M9 Lab 9.2: S3 feature upload failed"
fi

# Lab 9.3: AI data quality validation
cd "$LAB93"
rm -rf output
if "$PYTHON" src/ai_quality_validator.py \
  --data-dir "${LAB91}/output" \
  --output output >> "$REPORT" 2>&1; then
  if [[ -f output/ai_quality_report.json ]]; then
    OVERALL=$(python3 -c "import json; print(json.load(open('output/ai_quality_report.json'))['overall_passed'])")
    if [[ "$OVERALL" == "True" ]]; then
      ok "M9 Lab 9.3: AI quality validation PASSED"
    else
      fail "M9 Lab 9.3: AI quality validation reported failures"
    fi
  else
    fail "M9 Lab 9.3: ai_quality_report.json missing"
  fi
else
  fail "M9 Lab 9.3: ai_quality_validator.py failed"
fi

if [[ -f output/ai_quality_report.json ]]; then
  if aws s3 cp output/ai_quality_report.json "s3://${BUCKET}/ml/quality/ai_quality_report.json" >> "$REPORT" 2>&1; then
    ok "M9 Lab 9.3: Quality report uploaded to S3"
  else
    fail "M9 Lab 9.3: S3 quality report upload failed"
  fi
fi

# ---------------------------------------------------------------------------
# SUMMARY & TEARDOWN
# ---------------------------------------------------------------------------
echo | tee -a "$REPORT"
echo "=== Test Summary ===" | tee -a "$REPORT"
echo "PASS: ${PASS}  FAIL: ${FAIL}  SKIP: ${SKIP}" | tee -a "$REPORT"
echo "Finished: $(date -u +%Y-%m-%dT%H:%M:%SZ)" | tee -a "$REPORT"
echo "Full log: ${REPORT}" | tee -a "$REPORT"

cleanup_lab7
trap - EXIT

log "Tearing down AWS resources..."
"${SCRIPT_DIR}/stop-labs.sh" --yes >> "$REPORT" 2>&1
ok "Teardown complete"

if [[ $FAIL -gt 0 ]]; then
  exit 1
fi
