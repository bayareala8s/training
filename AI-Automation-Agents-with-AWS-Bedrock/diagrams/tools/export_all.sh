#!/usr/bin/env bash
# Generate draw.io source + export SVG/PNG (recommended).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT/tools"
python3 generate_all_diagrams.py
python3 export_svg_png.py
echo "All formats ready under $ROOT/{drawio,png,svg}/"
