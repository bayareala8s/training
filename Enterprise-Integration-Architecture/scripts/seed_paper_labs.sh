#!/usr/bin/env bash
# Copy paper-lab samples so instructors can smoke-test validators.
# Students: do not use this. Validators reject these files unless EIA_ALLOW_SAMPLES=1.
set -euo pipefail
ROOT=$(cd "$(dirname "$0")/.." && pwd)
mkdir -p "$ROOT/submissions/lab-01" "$ROOT/submissions/lab-08" "$ROOT/submissions/lab-11"
cp "$ROOT/labs/lab-01-classification/sample-completed-worksheet.md" "$ROOT/submissions/lab-01/worksheet.md"
cp "$ROOT/labs/lab-08-esb-modernization/reference/adr.md" "$ROOT/submissions/lab-08/adr.md"
cp "$ROOT/labs/lab-11-chaos/sample-notes.md" "$ROOT/submissions/lab-11/notes.md"
echo "Seeded instructor samples. Smoke-test with:"
echo "  EIA_ALLOW_SAMPLES=1 python3 scripts/validate_lab.py lab-01-classification"
echo "  EIA_ALLOW_SAMPLES=1 python3 scripts/validate_lab.py lab-08-esb-modernization"
echo "Wipe submissions/ before handing the repo to students."
