#!/usr/bin/env bash
# Export all Draw.io diagrams to PNG and SVG using AWS-stencil .drawio sources.
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "${SCRIPT_DIR}/.." && pwd)"
DRAWIO_DIR="${REPO_ROOT}/docs/diagrams/drawio"
PNG_DIR="${REPO_ROOT}/docs/diagrams/png"
SVG_DIR="${REPO_ROOT}/docs/diagrams/svg"

mkdir -p "$PNG_DIR" "$SVG_DIR"

echo "=== Generating Draw.io source files (AWS stencils) ==="
python3 "${SCRIPT_DIR}/generate-drawio-diagrams.py"

echo ""
echo "=== Exporting PNG and SVG ==="

export_one() {
  local src="$1"
  local fmt="$2"
  local out_dir="$3"
  local base
  base="$(basename "$src" .drawio)"
  local out="${out_dir}/${base}.${fmt}"

  if command -v drawio &>/dev/null; then
    drawio --export --format "$fmt" --output "$out" "$src" --scale 2
  elif [ -n "${DRAWIO_DOCKER:-1}" ]; then
    docker run --rm -w /data -v "${DRAWIO_DIR}:/data/in" -v "${out_dir}:/data/out" \
      rlespinasse/drawio-desktop-headless \
      -x -f "$fmt" -o "/data/out/${base}.${fmt}" "/data/in/${base}.drawio"
  else
    return 1
  fi
  echo "  ✓ ${base}.${fmt}"
}

# Try macOS draw.io app if installed
if [ -x "/Applications/draw.io.app/Contents/MacOS/draw.io" ]; then
  export DRAWIO="/Applications/draw.io.app/Contents/MacOS/draw.io"
  drawio() { "$DRAWIO" "$@"; }
fi

failed=0
for drawio_file in "${DRAWIO_DIR}"/*.drawio; do
  [ -f "$drawio_file" ] || continue
  name="$(basename "$drawio_file")"
  echo "Exporting ${name}..."
  export_one "$drawio_file" png "$PNG_DIR" || failed=$((failed + 1))
  export_one "$drawio_file" svg "$SVG_DIR" || failed=$((failed + 1))
done

echo ""
if [ "$failed" -gt 0 ]; then
  echo "Some exports failed. Install draw.io or run with Docker:"
  echo "  brew install --cask drawio"
  echo "  # OR"
  echo "  DRAWIO_DOCKER=1 ./scripts/export-drawio.sh"
  exit 1
fi

echo "=== Done ==="
echo "Draw.io: ${DRAWIO_DIR}"
echo "PNG:     ${PNG_DIR} ($(ls -1 "${PNG_DIR}"/*.png 2>/dev/null | wc -l | tr -d ' ') files)"
echo "SVG:     ${SVG_DIR} ($(ls -1 "${SVG_DIR}"/*.svg 2>/dev/null | wc -l | tr -d ' ') files)"
