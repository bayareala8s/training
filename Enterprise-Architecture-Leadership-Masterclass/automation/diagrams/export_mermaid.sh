#!/usr/bin/env bash
# Export Mermaid sources to SVG/PNG using mermaid-cli.
# Usage: ./automation/diagrams/export_mermaid.sh [module-05|labs/lab-06|all]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
SCOPE="${1:-module-05}"
MMDC=(npx -y @mermaid-js/mermaid-cli@11.4.2)

export_one() {
  local mmd="$1"
  local rel svg png
  rel="${mmd#$ROOT/diagrams/}"
  svg="$ROOT/diagrams/${rel/\/mermaid\//\/svg\/}"
  png="$ROOT/diagrams/${rel/\/mermaid\//\/png\/}"
  svg="${svg%.mmd}.svg"
  png="${png%.mmd}.png"
  mkdir -p "$(dirname "$svg")" "$(dirname "$png")"
  echo "→ $rel"
  "${MMDC[@]}" -i "$mmd" -o "$svg" -b white
  "${MMDC[@]}" -i "$mmd" -o "$png" -b white -s 2
}

cd "$ROOT"
if [[ "$SCOPE" == "all" ]]; then
  mapfile -t FILES < <(find diagrams -name '*.mmd' | sort)
else
  mapfile -t FILES < <(find "diagrams/$SCOPE" -name '*.mmd' 2>/dev/null | sort)
fi

echo "Exporting ${#FILES[@]} diagrams…"
for f in "${FILES[@]}"; do
  export_one "$f" || echo "WARN: failed $f"
done
echo "Done."
