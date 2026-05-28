#!/usr/bin/env bash
# Regenerate PNG and SVG from diagrams/sources/*.mmd
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${ROOT}/diagrams/sources"
SVG="${ROOT}/diagrams/svg"
PNG="${ROOT}/diagrams/png"

mkdir -p "$SVG" "$PNG"
for f in "$SRC"/*.mmd; do
  base=$(basename "$f" .mmd)
  echo "Rendering $base..."
  npx -y @mermaid-js/mermaid-cli@11.4.0 -i "$f" -o "${SVG}/${base}.svg" -b transparent
  npx -y @mermaid-js/mermaid-cli@11.4.0 -i "$f" -o "${PNG}/${base}.png" -b white -w 1920 -H 1080
done
echo "Done: $(ls "$SVG"/*.svg | wc -l) SVG, $(ls "$PNG"/*.png | wc -l) PNG"
