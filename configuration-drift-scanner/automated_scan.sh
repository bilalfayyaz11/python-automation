#!/bin/bash

echo "Running automated drift scan..."

./scripts/capture_current.sh

python3 scripts/drift_scanner.py

LATEST_REPORT=$(ls -t reports/*.json | head -1)

DRIFT_COUNT=$(jq '.drifts_detected' "$LATEST_REPORT")

if [ "$DRIFT_COUNT" -gt 0 ]; then
    echo "WARNING: $DRIFT_COUNT configuration drift(s) detected!"
    exit 1
else
    echo "No configuration drift detected."
    exit 0
fi
