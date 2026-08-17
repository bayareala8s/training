#!/usr/bin/env bash
# Export .drawio sources to PNG/SVG (requires Draw.io Desktop CLI: brew install --cask drawio).
set -euo pipefail
ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SRC="$ROOT/docs/diagrams/aws-stencils/drawio"
PNG="$ROOT/docs/diagrams/aws-stencils/drawio-png"
SVG="$ROOT/docs/diagrams/aws-stencils/drawio-svg"
mkdir -p "$PNG" "$SVG"

if ! command -v drawio >/dev/null 2>&1; then
  echo "Draw.io CLI not found. Install: brew install --cask drawio"
  echo "Or open sources in https://app.diagrams.net and export manually:"
  echo "  $SRC"
  exit 0
fi

shopt -s nullglob
files=("$SRC"/*.drawio)
if ((${#files[@]} == 0)); then
  echo "No .drawio files. Run: python3 scripts/generate-aws-drawio-sources.py"
  exit 0
fi

for f in "${files[@]}"; do
  base="$(basename "$f" .drawio)"
  echo "Exporting $base ..."
  drawio -x -f png -s 2 -o "$PNG/${base}.png" "$f"
  drawio -x -f svg -o "$SVG/${base}.svg" "$f"
done
echo "Done → drawio-png/ and drawio-svg/"
