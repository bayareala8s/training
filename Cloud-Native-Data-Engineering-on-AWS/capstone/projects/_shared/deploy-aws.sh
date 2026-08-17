#!/usr/bin/env bash
# Deploy shared course lab stack for capstone demos (optional AWS path).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../../.." && pwd)"
exec "$ROOT/scripts/lab-cycle.sh" start
