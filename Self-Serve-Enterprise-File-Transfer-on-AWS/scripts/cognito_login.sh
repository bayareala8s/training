#!/usr/bin/env bash
# Obtain Cognito ID token for API calls (Lab 6). Writes .lab/cognito_token.json

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/stack_lib.sh
source "$SCRIPT_DIR/stack_lib.sh"

baylearn_require_tools
export AWS_REGION="$(baylearn_aws_region)"

POOL="$(baylearn_tf_raw cognito_user_pool_id)"
CLIENT="$(baylearn_tf_raw cognito_client_id)"
USER="$(baylearn_tf_raw cognito_test_username)"

PASS="${BAYLEARN_ADMIN_PASSWORD:-}"
if [[ -z "$PASS" && -f "$BAYLEARN_TF_DIR/terraform.tfvars" ]]; then
  PASS=$(grep -E '^[[:space:]]*admin_password[[:space:]]*=' "$BAYLEARN_TF_DIR/terraform.tfvars" 2>/dev/null | head -1 | sed -E 's/^[[:space:]]*admin_password[[:space:]]*=[[:space:]]*"([^"]*)".*/\1/' || true)
fi
[[ -n "$PASS" ]] || { echo "Set BAYLEARN_ADMIN_PASSWORD or admin_password in terraform.tfvars" >&2; exit 1; }

mkdir -p "$BAYLEARN_ROOT/.lab"
OUT="$BAYLEARN_ROOT/.lab/cognito_token.json"

aws cognito-idp initiate-auth \
  --auth-flow USER_PASSWORD_AUTH \
  --client-id "$CLIENT" \
  --auth-parameters "USERNAME=$USER,PASSWORD=$PASS" \
  --output json > "$OUT"

TOKEN=$(jq -r '.AuthenticationResult.IdToken' "$OUT")
echo "IdToken saved in $OUT"
echo "export BAYLEARN_ID_TOKEN='$TOKEN'"

API="$(baylearn_tf_raw api_endpoint)"
echo "Example:"
echo "  curl -s -H \"Authorization: Bearer \$BAYLEARN_ID_TOKEN\" ${API}/v1/connections | jq ."
