#!/usr/bin/env bash
# Run the healthcare analytics local pipeline (offline, no AWS required).
set -euo pipefail
cd "$(dirname "$0")"
python3 ../../_shared/run_pipeline.py --project-root ..
