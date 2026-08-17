#!/usr/bin/env bash
# Export all .drawio files to PNG and SVG (draw.io desktop headless via Docker).
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
SRC="${ROOT}/drawio"
PNG="${ROOT}/png"
SVG="${ROOT}/svg"
IMAGE="${DRAWIO_IMAGE:-rlespinasse/drawio-desktop-headless:minimal}"

mkdir -p "$PNG" "$SVG"

shopt -s nullglob
files=("$SRC"/*.drawio)
if [[ ${#files[@]} -eq 0 ]]; then
  echo "No .drawio files — run: python3 tools/generate_all_diagrams.py"
  exit 1
fi

if ! command -v docker &>/dev/null; then
  echo "ERROR: Docker required for headless export."
  exit 1
fi

echo "Using Docker image: $IMAGE"
echo "Exporting ${#files[@]} diagrams..."

for f in "${files[@]}"; do
  base="$(basename "$f" .drawio)"
  echo "  -> $base"
  docker run --rm \
    -w /data \
    -v "$ROOT:/data" \
    "$IMAGE" \
    -x -f png -s 2 --no-sandbox --disable-gpu \
    -o "/data/png/${base}.png" "/data/drawio/${base}.drawio" 2>/dev/null \
    || docker run --rm -w /data -v "$ROOT:/data" "$IMAGE" \
         -x -f png -s 2 -o "/data/png/${base}.png" "/data/drawio/${base}.drawio"

  docker run --rm \
    -w /data \
    -v "$ROOT:/data" \
    "$IMAGE" \
    -x -f svg --no-sandbox --disable-gpu \
    -o "/data/svg/${base}.svg" "/data/drawio/${base}.drawio" 2>/dev/null \
    || docker run --rm -w /data -v "$ROOT:/data" "$IMAGE" \
         -x -f svg -o "/data/svg/${base}.svg" "/data/drawio/${base}.drawio"
done

echo ""
echo "Done."
echo "  PNG: ${#files[@]} files in $PNG"
echo "  SVG: ${#files[@]} files in $SVG"
ls "$PNG" | wc -l | xargs echo "PNG count:"
ls "$SVG" | wc -l | xargs echo "SVG count:"
