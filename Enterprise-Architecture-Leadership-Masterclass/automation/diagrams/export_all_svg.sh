#!/usr/bin/env bash
# Export ALL Mermaid sources to real SVG (and optionally PNG).
# Usage: ./automation/diagrams/export_all_svg.sh [--png] [--jobs N]
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
cd "$ROOT"

JOBS=4
DO_PNG=0
for arg in "$@"; do
  case "$arg" in
    --png) DO_PNG=1 ;;
    --jobs=*) JOBS="${arg#*=}" ;;
  esac
done

echo "==> Installing @mermaid-js/mermaid-cli locally (if needed)"
if [[ ! -x node_modules/.bin/mmdc ]]; then
  npm init -y >/dev/null 2>&1 || true
  npm install --no-fund --no-audit @mermaid-js/mermaid-cli@11.4.2
fi
MMDC="$ROOT/node_modules/.bin/mmdc"

LOG_DIR="$ROOT/diagrams/_export-logs"
mkdir -p "$LOG_DIR"
FAIL_LOG="$LOG_DIR/failures.txt"
: > "$FAIL_LOG"
OK_LOG="$LOG_DIR/success.txt"
: > "$OK_LOG"

export_one() {
  local mmd="$1"
  local rel svg png
  rel="${mmd#"$ROOT"/diagrams/}"
  # mermaid/foo/bar.mmd -> svg/foo/bar.svg
  svg="$ROOT/diagrams/${rel/\/mermaid\//\/svg\/}"
  svg="${svg%.mmd}.svg"
  png="$ROOT/diagrams/${rel/\/mermaid\//\/png\/}"
  png="${png%.mmd}.png"
  mkdir -p "$(dirname "$svg")"
  if "$MMDC" -i "$mmd" -o "$svg" -b white >/dev/null 2>"$LOG_DIR/$(basename "$mmd").err"; then
    # Detect placeholder (simple title card) vs real render: real mmdc SVGs are usually larger / contain <g
    if ! grep -q '<g' "$svg" 2>/dev/null && [[ $(wc -c < "$svg") -lt 2000 ]]; then
      echo "PLACEHOLDER_OR_TINY $rel" >> "$FAIL_LOG"
      return 1
    fi
    echo "$rel" >> "$OK_LOG"
    if [[ "$DO_PNG" == "1" ]]; then
      mkdir -p "$(dirname "$png")"
      "$MMDC" -i "$mmd" -o "$png" -b white -s 2 >/dev/null 2>&1 || true
    fi
    return 0
  else
    echo "$rel" >> "$FAIL_LOG"
    return 1
  fi
}
export -f export_one
export ROOT MMDC DO_PNG LOG_DIR FAIL_LOG OK_LOG

mapfile -t FILES < <(find "$ROOT/diagrams" -path '*/mermaid/*' -name '*.mmd' | sort)
TOTAL=${#FILES[@]}
echo "==> Exporting $TOTAL SVG diagrams with $JOBS parallel jobs"

# Prefer GNU parallel if present; else xargs
if command -v parallel >/dev/null 2>&1; then
  printf '%s\n' "${FILES[@]}" | parallel -j "$JOBS" export_one {}
else
  printf '%s\n' "${FILES[@]}" | xargs -P "$JOBS" -I{} bash -c 'export_one "$@"' _ {}
fi

OK=$(wc -l < "$OK_LOG" | tr -d ' ')
FAIL=$(wc -l < "$FAIL_LOG" | tr -d ' ')
echo "==> Done. success=$OK fail=$FAIL / total=$TOTAL"
echo "    Success log: $OK_LOG"
echo "    Failure log: $FAIL_LOG"
if [[ "$FAIL" -gt 0 ]]; then
  echo "==> Failures:"
  head -50 "$FAIL_LOG"
  exit 2
fi
