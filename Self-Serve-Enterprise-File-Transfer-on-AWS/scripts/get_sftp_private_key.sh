#!/usr/bin/env bash
# Write partner-demo SFTP private key to .lab/sftp_key.pem (mode 600).

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
# shellcheck source=scripts/stack_lib.sh
source "$SCRIPT_DIR/stack_lib.sh"

baylearn_require_tools
export AWS_REGION="$(baylearn_aws_region)"

SECRET="$(baylearn_tf_raw sftp_private_key_secret_arn)"
USER="$(baylearn_tf_raw sftp_username)"
HOST="$(baylearn_tf_raw transfer_server_endpoint)"

[[ -n "$SECRET" ]] || { echo "No SFTP secret (Transfer disabled?)" >&2; exit 1; }

mkdir -p "$BAYLEARN_ROOT/.lab"
OUT="$BAYLEARN_ROOT/.lab/sftp_key.pem"
aws secretsmanager get-secret-value --secret-id "$SECRET" --query SecretString --output text > "$OUT"
chmod 600 "$OUT"

echo "Wrote $OUT"
echo "SFTP: sftp -i $OUT ${USER}@${HOST}"
echo "Test:  put /tmp/baylearn-sample.csv"
