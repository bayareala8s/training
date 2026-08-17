#!/usr/bin/env bash
# Start the Principal Architect Knowledge System documentation site locally.
set -euo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

if [[ ! -d node_modules ]]; then
  echo "Installing Node dependencies..."
  npm install
fi

echo ""
echo "Starting site at http://localhost:3000"
echo "  Start Here:  http://localhost:3000/docs/start-here/welcome"
echo "  Curriculum:  http://localhost:3000/docs/start-here/curriculum-overview"
echo ""
echo "Press Ctrl+C to stop."
echo ""

exec npm start
