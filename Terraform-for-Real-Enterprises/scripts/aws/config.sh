#!/usr/bin/env bash
# Shared configuration for BayAreaLa8s Terraform course lab cost controls.
# Source this file from other scripts: source "$(dirname "$0")/config.sh"

# NOTE: This file is sourced by multiple scripts. Do not enable `set -e` here,
# otherwise any non-critical AWS CLI error (e.g. "no tagged resources found")
# can abort the caller unexpectedly.
set -uo pipefail

# AWS region (override: export AWS_REGION=us-east-1)
export AWS_REGION="${AWS_REGION:-us-west-2}"

# Resources managed by start/stop must have ALL of these tags (key=value).
# Set in Terraform: tags = local.lab_tags
export LAB_TAG_KEY="${LAB_TAG_KEY:-Course}"
export LAB_TAG_VALUE="${LAB_TAG_VALUE:-terraform-enterprise}"

# Optional project filter (empty = match any Project tag value)
export LAB_PROJECT_TAG_KEY="${LAB_PROJECT_TAG_KEY:-Project}"
export LAB_PROJECT_TAG_VALUE="${LAB_PROJECT_TAG_VALUE:-}"

# Dry run: export DRY_RUN=1
export DRY_RUN="${DRY_RUN:-0}"

# Logging
export LOG_LEVEL="${LOG_LEVEL:-INFO}"

log() {
  local level="$1"
  shift
  [[ "$LOG_LEVEL" == "DEBUG" || "$level" != "DEBUG" ]] && echo "[$(date +%H:%M:%S)] [$level] $*"
}

require_aws_cli() {
  if ! command -v aws &>/dev/null; then
    echo "ERROR: AWS CLI not found. Install: https://aws.amazon.com/cli/" >&2
    exit 1
  fi
  aws sts get-caller-identity &>/dev/null || {
    echo "ERROR: AWS credentials not configured. Run: aws configure or aws sso login" >&2
    exit 1
  }
}

# Build JMESPath filter for describe-* calls
lab_tag_filter_jmespath() {
  echo "Tags[?Key=='${LAB_TAG_KEY}' && Value=='${LAB_TAG_VALUE}'] | [0]"
}

# Returns 0 if resource tags include required lab tag (and optional project tag)
resource_has_lab_tags() {
  local tags_json="$1"
  if ! echo "$tags_json" | grep -q "\"Key\": \"${LAB_TAG_KEY}\""; then
    return 1
  fi
  echo "$tags_json" | grep -q "\"Key\": \"${LAB_TAG_KEY}\", \"Value\": \"${LAB_TAG_VALUE}\"" || return 1
  if [[ -n "$LAB_PROJECT_TAG_VALUE" ]]; then
    echo "$tags_json" | grep -q "\"Key\": \"${LAB_PROJECT_TAG_KEY}\", \"Value\": \"${LAB_PROJECT_TAG_VALUE}\"" || return 1
  fi
  return 0
}

run_cmd() {
  if [[ "$DRY_RUN" == "1" ]]; then
    log INFO "[DRY-RUN] $*"
  else
    log DEBUG "exec: $*"
    "$@"
  fi
}
