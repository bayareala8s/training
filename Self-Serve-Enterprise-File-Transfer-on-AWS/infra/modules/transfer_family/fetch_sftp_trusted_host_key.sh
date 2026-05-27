#!/usr/bin/env bash
# Terraform external data source: discover SFTP host key via ssh-keyscan (with retries).
set -euo pipefail
INPUT="$(cat)"
ENDPOINT="$(echo "$INPUT" | jq -r '.endpoint // empty')"
PORT="$(echo "$INPUT" | jq -r '.port // "22"')"
if [[ -z "$ENDPOINT" ]]; then
  echo "fetch_sftp_trusted_host_key: missing endpoint" >&2
  exit 1
fi

MAX_ATTEMPTS="${MAX_ATTEMPTS:-36}"
SLEEP_SEC="${SLEEP_SEC:-5}"

for attempt in $(seq 1 "$MAX_ATTEMPTS"); do
  LINE="$(ssh-keyscan -t rsa -p "$PORT" "$ENDPOINT" 2>/dev/null | head -1 || true)"
  if [[ -n "$LINE" ]]; then
    KEY="$(echo "$LINE" | awk '{print $2, $3}')"
    jq -n --arg k "$KEY" '{"key":$k}'
    exit 0
  fi
  echo "fetch_sftp_trusted_host_key: attempt ${attempt}/${MAX_ATTEMPTS} waiting for ${ENDPOINT}:${PORT}..." >&2
  sleep "$SLEEP_SEC"
done

echo "fetch_sftp_trusted_host_key: ssh-keyscan failed for ${ENDPOINT}:${PORT} after ${MAX_ATTEMPTS} attempts" >&2
exit 1
