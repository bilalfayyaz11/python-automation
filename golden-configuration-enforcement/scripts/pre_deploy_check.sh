#!/bin/bash
set -euo pipefail

echo "Running Golden Configuration Enforcement..."
echo "=========================================="

python3 scripts/config_enforcer.py

echo "All configurations compliant. Deployment allowed."
