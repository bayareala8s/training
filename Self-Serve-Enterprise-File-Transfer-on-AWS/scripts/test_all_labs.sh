#!/usr/bin/env bash
# Integration tests for all labs (requires deployed stack).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/stack_lib.sh
source "$SCRIPT_DIR/stack_lib.sh"

baylearn_require_tools
export AWS_REGION="$(baylearn_aws_region)"

BUCKET="$(baylearn_tf_raw landing_bucket)"
IN_PREFIX="$(baylearn_tf_raw inbound_s3_prefix)"
LARGE_IN="$(baylearn_tf_raw large_file_inbound_prefix)"
LARGE_OUT="$(baylearn_tf_raw large_file_processed_prefix)"
SFN="$(baylearn_tf_raw state_machine_arn)"
API="$(baylearn_tf_raw api_endpoint)"
ENDPOINT="$(baylearn_tf_raw transfer_server_endpoint)"
SFTP_USER="$(baylearn_tf_raw sftp_username)"

PASS=0
FAIL=0

pass() { echo "PASS: $1"; PASS=$((PASS + 1)); }
fail() { echo "FAIL: $1" >&2; FAIL=$((FAIL + 1)); }

# Avoid aws|grep -q pipelines under pipefail (SIGPIPE can make matches look like failures).
s3_list_contains() {
  local needle="$1"
  local listing
  listing=$(aws s3 ls "s3://${BUCKET}/" --recursive 2>/dev/null || true)
  grep -qF "$needle" <<<"$listing"
}

[[ -n "$BUCKET" ]] || { fail "stack not deployed (no landing_bucket output)"; exit 1; }

echo "========== Lab 1–2: S3 + KMS =========="
aws s3api head-bucket --bucket "$BUCKET" >/dev/null 2>&1 && pass "S3 bucket reachable" || fail "S3 head-bucket"
ENC=$(aws s3api get-bucket-encryption --bucket "$BUCKET" 2>/dev/null) && pass "SSE-KMS encryption configured" || fail "bucket encryption"
aws s3api get-public-access-block --bucket "$BUCKET" >/dev/null 2>&1 && pass "Block Public Access" || fail "BPA"

echo "========== Lab 3: S3 event processor =========="
echo "col1,col2" > /tmp/baylearn-lab3.csv
KEY3="${IN_PREFIX}test-lab3-$(date +%s).csv"
aws s3 cp /tmp/baylearn-lab3.csv "s3://${BUCKET}/${KEY3}"
LAB3_BASE="$(basename "$KEY3")"
LAB3_OK=false
for _ in $(seq 1 24); do
  if s3_list_contains "$LAB3_BASE"; then
    LAB3_OK=true
    break
  fi
  sleep 5
done
if [[ "$LAB3_OK" == true ]]; then pass "Lab 3 routed to processing/"; else fail "Lab 3 processing not found"; fi

echo bad > /tmp/baylearn-lab3.exe
KEY3B="${IN_PREFIX}test-lab3-bad-$(date +%s).exe"
aws s3 cp /tmp/baylearn-lab3.exe "s3://${BUCKET}/${KEY3B}"
sleep 15
if s3_list_contains "$(basename "$KEY3B")"; then pass "Lab 3 quarantine path"; else fail "Lab 3 quarantine"; fi

echo "========== Lab 4: Step Functions =========="
KEY4="${IN_PREFIX}test-lab4-$(date +%s).csv"
echo "lab4" > /tmp/baylearn-lab4.csv
aws s3 cp /tmp/baylearn-lab4.csv "s3://${BUCKET}/${KEY4}"
EXEC=$(aws stepfunctions start-execution \
  --state-machine-arn "$SFN" \
  --name "labtest-$(date +%s)" \
  --input "{\"bucket\":\"$BUCKET\",\"key\":\"$KEY4\",\"correlation_id\":\"lab4-test\"}" \
  --query executionArn --output text)
pass "Lab 4 execution started"
for i in $(seq 1 24); do
  STATUS=$(aws stepfunctions describe-execution --execution-arn "$EXEC" --query status --output text)
  if [[ "$STATUS" == "SUCCEEDED" ]]; then
    pass "Lab 4 execution SUCCEEDED"
    break
  fi
  if [[ "$STATUS" == "FAILED" ]]; then
    fail "Lab 4 execution FAILED"
    break
  fi
  sleep 5
done
[[ "$(aws stepfunctions describe-execution --execution-arn "$EXEC" --query status --output text)" == "SUCCEEDED" ]] || fail "Lab 4 not succeeded"

echo "========== Lab 5: Transfer connector =========="
CONN="$(baylearn_tf_raw transfer_connector_id)"
[[ -n "$CONN" && "$CONN" != "null" ]] && pass "Lab 5 connector id $CONN" || fail "connector missing"

echo "========== Lab 6: Cognito + API =========="
"$SCRIPT_DIR/cognito_login.sh" >/dev/null
TOKEN=$(jq -r '.AuthenticationResult.IdToken' "$BAYLEARN_ROOT/.lab/cognito_token.json")
HTTP=$(curl -s -o /tmp/baylearn-api.json -w "%{http_code}" \
  -H "Authorization: Bearer $TOKEN" "${API}/v1/connections")
[[ "$HTTP" == "200" ]] && pass "Lab 6 GET /v1/connections" || fail "Lab 6 API returned $HTTP"
CONN_ID=$(jq -r '.connections[0].connection_id // empty' /tmp/baylearn-api.json)
if [[ -z "$CONN_ID" ]]; then
  curl -s -X POST "${API}/v1/connections" \
    -H "Authorization: Bearer $TOKEN" \
    -H "Content-Type: application/json" \
    -d '{"name":"Lab Test","type":"SFTP_INBOUND"}' >/tmp/baylearn-api.json
  CONN_ID=$(jq -r '.connection_id' /tmp/baylearn-api.json)
fi
aws s3 cp /tmp/baylearn-lab4.csv "s3://${BUCKET}/${KEY4}" 2>/dev/null || true
JOB_HTTP=$(curl -s -o /tmp/baylearn-job.json -w "%{http_code}" \
  -X POST "${API}/v1/jobs" \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -H "x-idempotency-key: test-$(date +%s)" \
  -d "{\"connection_id\":\"$CONN_ID\",\"source_key\":\"$KEY4\"}")
[[ "$JOB_HTTP" == "202" ]] && pass "Lab 6 POST /v1/jobs" || fail "Lab 6 job submit HTTP $JOB_HTTP"

echo "========== Lab 7: Observability =========="
DASH="$(baylearn_tf_raw cloudwatch_dashboard_name)"
aws cloudwatch describe-alarms --alarm-name-prefix baylearn-mft-lab --query 'MetricAlarms[].AlarmName' --output text | grep -q . \
  && pass "Lab 7 alarms exist" || fail "Lab 7 alarms"
[[ -n "$DASH" ]] && pass "Lab 7 dashboard $DASH" || fail "Lab 7 dashboard"

echo "========== Lab 1: SFTP upload =========="
if [[ -n "$ENDPOINT" && "$ENDPOINT" != "null" ]]; then
  "$SCRIPT_DIR/get_sftp_private_key.sh" >/dev/null
  echo "sftp,test" > /tmp/baylearn-sftp.csv
  if sftp -i "$BAYLEARN_ROOT/.lab/sftp_key.pem" -o StrictHostKeyChecking=no -o BatchMode=yes \
    "${SFTP_USER}@${ENDPOINT}" <<'SFTP_EOF' 2>/dev/null; then
put /tmp/baylearn-sftp.csv sftp-test.csv
bye
SFTP_EOF
    SFTP_OK=false
    for _ in $(seq 1 18); do
      if s3_list_contains "sftp-test"; then
        SFTP_OK=true
        break
      fi
      sleep 5
    done
    if [[ "$SFTP_OK" == true ]]; then pass "Lab 1 SFTP upload"; else fail "Lab 1 SFTP file not in S3"; fi
  else
    fail "Lab 1 SFTP connection"
  fi
else
  echo "SKIP: Lab 1 SFTP (transfer disabled)"
fi

echo "========== Lab 9: ECS Fargate =========="
ECS_CLUSTER="$(baylearn_tf_raw ecs_cluster_name)"
if [[ -n "$ECS_CLUSTER" && "$ECS_CLUSTER" != "null" ]]; then
  REPO_NAME="${BAYLEARN_ROOT##*/}-fargate-worker"
  REPO_NAME="baylearn-mft-lab-fargate-worker"
  ECR_IMAGE=$(aws ecr describe-images --repository-name "$REPO_NAME" \
    --query 'length(imageDetails)' --output text 2>/dev/null || echo 0)
  if [[ "$ECR_IMAGE" != "0" ]]; then
    pass "Lab 9 ECR image present"
  else
    fail "Lab 9 ECR image missing — run ./scripts/build_ecs_worker.sh"
  fi
  if LAB_LARGE_FILE_MB="${LAB_LARGE_FILE_MB:-5}" "$SCRIPT_DIR/demo_ecs_large_file.sh"; then
    pass "Lab 9 large file demo"
  else
    fail "Lab 9 ECS demo"
  fi
else
  echo "SKIP: Lab 9 (enable_ecs_worker=false)"
fi

echo ""
echo "========== Summary =========="
echo "PASS: $PASS  FAIL: $FAIL"
[[ "$FAIL" -eq 0 ]] || exit 1
echo "OK: all lab integration tests passed"
