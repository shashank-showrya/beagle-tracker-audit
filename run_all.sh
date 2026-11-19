#!/usr/bin/env bash
set -euo pipefail

echo "==> Running build_tracker.py"
set +e
python build_tracker.py
status=$?
set -e
if [[ "${status}" -ne 0 ]]; then
  echo "STUB NOT IMPLEMENTED: build_tracker. This is expected until that file is written."
  exit 1
fi

echo "==> Running chart_a_counts.py"
python chart_a_counts.py

echo "==> Running chart_b_gap.py"
python chart_b_gap.py

echo "All steps completed."