#!/usr/bin/env bash
# Serve the BayLearn course player. Must run from the repository root.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
cd "$ROOT"
PORT=${PORT:-8080}
echo "Course player: http://localhost:${PORT}/course-ui/"
echo "Stop with Ctrl+C. Do not use file:// — lessons will not load."
exec python3 -m http.server "$PORT"
