#!/usr/bin/env bash
# Export docs/diagrams/*.drawio and Mermaid blocks in week-*.md to PNG + SVG.
#
# Requirements: Docker (fnkr/drawio image), Node/npx (@mermaid-js/mermaid-cli)
#
# Usage (repo root):
#   ./scripts/export_diagram_images.sh

set -euo pipefail
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO="$(cd "$SCRIPT_DIR/.." && pwd)"
DIAG="$REPO/docs/diagrams"
PNG="$DIAG/export/png"
SVG="$DIAG/export/svg"
DOCKER_IMAGE="${DRAWIO_EXPORT_IMAGE:-fnkr/drawio}"
DOCKER_PLATFORM="${DRAWIO_DOCKER_PLATFORM:-linux/amd64}"

mkdir -p "$PNG/drawio" "$SVG/drawio" "$PNG/mermaid" "$SVG/mermaid"

echo "==> Pull Docker image $DOCKER_IMAGE (if needed)"
docker pull --platform "$DOCKER_PLATFORM" "$DOCKER_IMAGE" >/dev/null 2>&1 || true

export_drawio_file() {
  local drawio="$1"
  local base
  base="$(basename "$drawio" .drawio)"
  echo "==> drawio: $base"
  for fmt in png svg; do
    local subdir="drawio"
    local outroot="$PNG"
    [[ "$fmt" == "svg" ]] && outroot="$SVG"
    docker run --rm --platform "$DOCKER_PLATFORM" \
      -v "$DIAG:/data" \
      "$DOCKER_IMAGE" \
      --export --format "$fmt" \
      --output "/data/export/${fmt}/${subdir}/${base}.${fmt}" \
      "/data/$(basename "$drawio")"
  done
}

echo "==> Exporting .drawio files (PNG + SVG)"
shopt -s nullglob
for f in "$DIAG"/*.drawio; do
  export_drawio_file "$f"
done

echo "==> Exporting Mermaid diagrams from week-*.md"
python3 "$SCRIPT_DIR/export_mermaid_images.py" "$DIAG" "$PNG/mermaid" "$SVG/mermaid"

echo ""
echo "OK: exports written under $DIAG/export/"
echo "  drawio PNG: $(find "$PNG/drawio" -name '*.png' 2>/dev/null | wc -l | tr -d ' ')"
echo "  drawio SVG: $(find "$SVG/drawio" -name '*.svg' 2>/dev/null | wc -l | tr -d ' ')"
echo "  mermaid PNG: $(find "$PNG/mermaid" -name '*.png' 2>/dev/null | wc -l | tr -d ' ')"
echo "  mermaid SVG: $(find "$SVG/mermaid" -name '*.svg' 2>/dev/null | wc -l | tr -d ' ')"
