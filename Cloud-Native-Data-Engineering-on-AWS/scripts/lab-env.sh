#!/usr/bin/env bash
# Source shared environment variables for all lab demos.
# Usage: source ./scripts/lab-env.sh
set -euo pipefail

unset HTTP_PROXY HTTPS_PROXY http_proxy https_proxy ALL_PROXY all_proxy 2>/dev/null || true
export AWS_DEFAULT_REGION="${AWS_DEFAULT_REGION:-us-east-1}"
export AWS_REGION="${AWS_REGION:-$AWS_DEFAULT_REGION}"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
TF_DIR="${REPO_ROOT}/infrastructure/environments/dev"

export REPO_ROOT TF_DIR
export ACCOUNT_ID="$(aws sts get-caller-identity --query Account --output text)"
export CALLER_ARN="$(aws sts get-caller-identity --query Arn --output text)"

_tf() { terraform -chdir="$TF_DIR" output -raw "$1" 2>/dev/null || echo ""; }

export BUCKET="$(_tf data_lake_bucket)"
export GLUE_JOB="$(_tf glue_job_name)"
export GLUE_DB="$(_tf glue_catalog_database)"
export CRAWLER="$(_tf cleaned_crawler_name)"
export SFN_ARN="$(_tf state_machine_arn)"
export SFN_NAME="$(_tf state_machine_name)"
export DASHBOARD="$(_tf dashboard_name)"
export SNS_CRITICAL="$(_tf sns_critical_topic_arn)"
export QV_LAMBDA="$(_tf quality_validation_lambda)"

# Lambda function names (ingestion)
export FN_FILE="$(terraform -chdir="$TF_DIR" output -json lambda_function_names 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)[0])' 2>/dev/null || echo "")"
export FN_SCHED="$(terraform -chdir="$TF_DIR" output -json lambda_function_names 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)[1])' 2>/dev/null || echo "")"
export FN_S3="$(terraform -chdir="$TF_DIR" output -json lambda_function_names 2>/dev/null | python3 -c 'import json,sys; print(json.load(sys.stdin)[2])' 2>/dev/null || echo "")"

export PYTHON="$("${SCRIPT_DIR}/ensure-python.sh")"
export ATHENA_RESULTS="s3://${BUCKET}/athena-results/"

# Lab paths
export LAB11="${REPO_ROOT}/modules/module-01-foundations/labs/lab-1.1-build-s3-data-lake"
export LAB12="${REPO_ROOT}/modules/module-01-foundations/labs/lab-1.2-data-lake-zones"
export LAB41="${REPO_ROOT}/modules/module-04-data-quality/labs/lab-4.1-quality-framework"
export LAB51="${REPO_ROOT}/modules/module-05-modeling-analytics/labs/lab-5.1-star-schema"
export LAB53="${REPO_ROOT}/modules/module-05-modeling-analytics/labs/lab-5.3-cost-efficient-queries"
export LAB71="${REPO_ROOT}/modules/module-07-security-governance/labs/lab-7.1-kms-bucket-policies"
export LAB72="${REPO_ROOT}/modules/module-07-security-governance/labs/lab-7.2-iam-rbac-data-zones"
export LAB73="${REPO_ROOT}/modules/module-07-security-governance/labs/lab-7.3-governance-audit"
export LAB91="${REPO_ROOT}/modules/module-09-ai-ml-data/labs/lab-9.1-ml-dataset-prep"
export LAB92="${REPO_ROOT}/modules/module-09-ai-ml-data/labs/lab-9.2-feature-store-pipeline"
export LAB93="${REPO_ROOT}/modules/module-09-ai-ml-data/labs/lab-9.3-ai-data-quality"

if [[ -z "$BUCKET" ]]; then
  echo "ERROR: Lab environment not deployed (bucket=NOT DEPLOYED)." >&2
  echo "Start labs first: ./scripts/lab-cycle.sh start" >&2
  return 1 2>/dev/null || exit 1
fi

echo "CNDE lab environment loaded (region=${AWS_REGION}, bucket=${BUCKET})"
