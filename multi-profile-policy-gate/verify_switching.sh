#!/bin/bash
set -e

echo "Testing dynamic profile switching..."

for profile in healthcare finance retail; do
    echo
    echo "===== Switching to $profile profile ====="

    curl -s -X POST http://localhost:8080/switch-profile \
      -H "Content-Type: application/json" \
      -d "{\"profile\": \"$profile\"}" | jq

    echo
    echo "Current status:"
    curl -s http://localhost:8080/status | jq
done
