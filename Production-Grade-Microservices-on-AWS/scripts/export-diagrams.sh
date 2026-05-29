#!/usr/bin/env bash
# Regenerate PNG and SVG exports from docs/diagrams/*.md (requires Node.js + npx).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"
exec python3 scripts/export-diagrams.py
